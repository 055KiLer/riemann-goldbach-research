"""Fast general-q DFT pipeline for E_q = sum*_{chi primitive mod q} L(a,chi)L(b,chibar)/(L(s,chi)L(t,chibar)).
L(u,chi) for all chi at once via FFT over the character group (CRT decomposition).
Hurwitz zeta vectorized in numpy complex128 (Euler-Maclaurin).
Main term M_q from phase-10 canonical formulas (mpmath scalars + numpy Euler product).
"""
import numpy as np, mpmath as mp
from math import gcd
mp.mp.dps=30

# ---------- factorization / primitive root ----------
def factorize(n):
    f={}; d=2
    while d*d<=n:
        while n%d==0: f[d]=f.get(d,0)+1; n//=d
        d+=1
    if n>1: f[n]=f.get(n,0)+1
    return f

def primitive_root(p):
    m=p-1; fac=[]; mm=m; d=2
    while d*d<=mm:
        if mm%d==0:
            fac.append(d)
            while mm%d==0: mm//=d
        d+=1
    if mm>1: fac.append(mm)
    g=2
    while g<p:
        if all(pow(g,m//q,p)!=1 for q in fac): return g
        g+=1
    raise RuntimeError

# ---------- Bernoulli coefficients ----------
def bern_coeffs(J):
    out=[]
    for j in range(1,J+1):
        B=mp.bernoulli(2*j)
        fact=mp.factorial(2*j)
        out.append(complex(B/fact))
    return np.array(out,dtype=np.complex128)

_BCOEF=bern_coeffs(12)

# ---------- vectorized Hurwitz zeta by Euler-Maclaurin ----------
def hurwitz_np(u, x, K=6, J=12, chunk=200_000, logtab=None):
    """zeta(u, x) for array x (complex u). Returns complex128 array.
    logtab: optional precomputed (K+1, len(x)) array of log(n+x) (n=0..K-1) and log(K+x)."""
    u=complex(u); x=np.asarray(x,dtype=np.float64)
    A=len(x)
    out=np.empty(A,dtype=np.complex128)
    coef=_BCOEF[:J]
    # rising factorials (u)_{2j-1}
    rise=np.empty(J,dtype=np.complex128); rise[0]=u
    for j in range(2,J+1):
        rise[j-1]=rise[j-2]*(u+2*j-3)*(u+2*j-2)
    cj=coef*rise
    for c0 in range(0,A,chunk):
        sl=slice(c0,min(c0+chunk,A)); xx=x[sl]; m=len(xx)
        if logtab is not None:
            L=logtab[:,sl]
        else:
            L=np.empty((K+1,m),dtype=np.float64)
            for n in range(K):
                L[n]=np.log(n+xx)
            L[K]=np.log(K+xx)
        sig=u.real; tim=u.imag
        S=np.zeros(m,dtype=np.complex128)
        for n in range(K):
            Ln=L[n]; e=np.exp(-sig*Ln)
            if abs(tim)>1e-15:
                ph=tim*Ln; e=e*(np.cos(ph)-1j*np.sin(ph))
            S+=e
        ly=L[K]; y=K+xx
        ey=np.exp(-sig*ly)
        if abs(tim)>1e-15:
            ph=tim*ly; tK=ey*(np.cos(ph)-1j*np.sin(ph))
        else:
            tK=ey.astype(np.complex128)
        R=(y/(u-1)+0.5).astype(np.complex128)
        yinv2=y**(-2.0); pj=y**(-1.0)
        for j in range(J):
            R+=cj[j]*pj
            pj=pj*yinv2
        out[sl]=S+tK*R
    return out

def make_logtab(x,K):
    A=len(x); L=np.empty((K+1,A),dtype=np.float64)
    for n in range(K): L[n]=np.log(n+x)
    L[K]=np.log(K+x)
    return L

# ---------- character group data for q ----------
class Group:
    """CRT decomposition of (Z/q)^* into cyclic axes; provides unit array a(x) and FFT utilities."""
    def __init__(self,q):
        self.q=q; fac=factorize(q)
        self.fac=fac
        if q%2==0 and fac.get(2,0)==1:
            self.empty=True; return
        self.empty=False
        self.locals=[]   # list of dicts: {'kind','axes':[sizes], 'value':fn(coord arrays)->local value mod m}
        self.mods=[]     # modulus of each local component
        self.coeffs=[]   # CRT coefficients
        for p,e in sorted(fac.items()):
            m=p**e; self.mods.append(m)
            if p==2:
                if e==2:
                    # axis: sign L in {0,1}; value = (-1)^L mod 4
                    self.locals.append(dict(kind='2_2',sizes=[2],p=2,e=e))
                else: # e>=3
                    self.locals.append(dict(kind='2e',sizes=[2,2**(e-2)],p=2,e=e))
            else:
                n=(p-1)*p**(e-1)
                g=primitive_root(p)
                if pow(g,n//p,m)==1: g+=p
                # powers g^j mod m
                gp=np.empty(n,dtype=np.int64); cur=1
                for j in range(n): gp[j]=cur; cur=cur*g%m
                self.locals.append(dict(kind='odd',sizes=[n],p=p,e=e,g=g,gp=gp))
        # CRT coefficients
        for i,m in enumerate(self.mods):
            M=q//m; inv=pow(M%m,-1,m)
            self.coeffs.append(M*inv % q)
        # build coordinate indices over tensor
        shapes=[1]*len(self.mods)
        for i,loc in enumerate(self.locals):
            self.axes_off = getattr(self,'axes_off',[])
        # global axes: concatenate local axes
        self.axis_sizes=[]; self.axis_local=[]; self.axis_which=[]
        for i,loc in enumerate(self.locals):
            for ai,sz in enumerate(loc['sizes']):
                self.axis_sizes.append(sz); self.axis_local.append(i); self.axis_which.append(ai)
        self.phi=int(np.prod(self.axis_sizes))
        # build unit array a over C-order tensor of global axes
        idx=np.indices(self.axis_sizes,sparse=True) if len(self.axis_sizes)>1 else None
        # compute local values
        a=np.zeros(self.axis_sizes,dtype=np.int64)
        for i,loc in enumerate(self.locals):
            axes=[j for j in range(len(self.axis_local)) if self.axis_local[j]==i]
            val=self._local_value(loc,axes)
            a=(a+ val*self.coeffs[i])%q
        self.a_grid=a
        self.a=a.reshape(-1)
        self.x=self.a.astype(np.float64)/q
        assert np.all(np.gcd(self.a,q)==1)
        # primitivity mask and parity (over full frequency tensor)
        self.k_sizes=self.axis_sizes
        kmask=np.ones(self.axis_sizes,dtype=bool)
        parity=np.zeros(self.axis_sizes,dtype=np.uint8)
        for j,sz in enumerate(self.axis_sizes):
            i=self.axis_local[j]; loc=self.locals[i]; ai=self.axis_which[j]
            kk=np.arange(sz)
            shape=[1]*len(self.axis_sizes); shape[j]=sz
            if loc['kind']=='odd':
                m_=kk%loc['p']!=0; kmask &= m_.reshape(shape)
                parity=(parity+ (kk%2).astype(np.uint8).reshape(shape))%2
            elif loc['kind']=='2_2':
                # only k=1 primitive
                m_=kk==1; kmask &= m_.reshape(shape)
                parity=(parity+ kk.astype(np.uint8).reshape(shape))%2
            elif loc['kind']=='2e':
                if ai==0:  # sign axis: any frequency; parity = k
                    parity=(parity+ kk.astype(np.uint8).reshape(shape))%2
                else:      # 5-part axis: primitive iff k odd; no parity contribution
                    m_=kk%2==1; kmask &= m_.reshape(shape)
        self.prim_mask=kmask.reshape(-1)
        self.parity_flat=parity.reshape(-1)
        self.M0=int(np.sum(self.prim_mask & (self.parity_flat==0)))
        self.M1=int(np.sum(self.prim_mask & (self.parity_flat==1)))
        self.phist=self.M0+self.M1
        # neg-frequency indices per axis (for L(u,chi_k) = q^{-u} F[(-k) mod n])
        self.neg_idx=[(-np.arange(sz))%sz for sz in self.axis_sizes]
    def _local_value(self,loc,axes):
        """local value mod m for each tensor coordinate (axes are global axis indices in this local)."""
        qsizes=[1]*len(self.axis_sizes)
        if loc['kind']=='odd':
            j=axes[0]; gp=loc['gp']
            arr=np.empty(len(gp),dtype=np.int64); arr[:]=gp
            # place along axis j
            shape=[1]*len(self.axis_sizes); shape[j]=len(gp)
            return arr.reshape(shape)
        if loc['kind']=='2_2':
            j=axes[0]
            arr=np.array([1,3],dtype=np.int64)  # (-1)^L mod 4
            shape=[1]*len(self.axis_sizes); shape[j]=2
            return arr.reshape(shape)
        if loc['kind']=='2e':
            e=loc['e']; m=2**e; n5=2**(e-2)
            jL=axes[0]; jM=axes[1]
            sign=np.array([1,-1],dtype=np.int64)  # (-1)^L
            # 5^M mod m
            f=np.empty(n5,dtype=np.int64); cur=1
            for j in range(n5): f[j]=cur; cur=cur*5%m
            shapeL=[1]*len(self.axis_sizes); shapeL[jL]=2
            shapeM=[1]*len(self.axis_sizes); shapeM[jM]=n5
            val=(sign.reshape(shapeL)*f.reshape(shapeM))%m
            return val
    def unit_tuple(self):
        """returns a_grid (tensor) and flattened a,x"""
        return self.a_grid, self.a, self.x
    def fft_data(self,u,K=6,logtab=None):
        """returns (F flattened C-order), so L(u,chi_k)=q^{-u}F[(-k) mod n] and L(u,chibar_k)=q^{-u}F[k]"""
        B=hurwitz_np(u,self.x,K=K,logtab=logtab)
        B=B.reshape(self.k_sizes)
        F=np.fft.fftn(B)
        return F
    def L_all(self,u,K=6,logtab=None):
        """returns (La, Lb_conj): L(u,chi_k) and L(u,chibar_k) as flattened arrays over k."""
        F=self.fft_data(u,K=K,logtab=logtab)
        qfac=complex(self.q**(-complex(u)))
        Fneg=F[np.ix_(*self.neg_idx)] if len(self.axis_sizes)>1 else F[self.neg_idx[0]]
        return qfac*Fneg.reshape(-1), qfac*F.reshape(-1)

if __name__=='__main__':
    import sys
    q=int(sys.argv[1])
    G=Group(q)
    print('q',q,'phi',G.phi,'M0,M1',G.M0,G.M1,'empty',G.empty)
    if not G.empty:
        x=G.x[:5]
        u=complex(0.5,0.3)
        v=hurwitz_np(u,x,K=6)
        print(v[:3])
