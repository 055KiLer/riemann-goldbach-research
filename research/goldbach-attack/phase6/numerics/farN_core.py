"""Far-N (N=2p, low-height, chunked-memory) Li-Liu finite model.

Efficient for p up to ~1.5e7: G[node, k odd] built from Hurwitz-zeta arrays over a=1..p-1
(chunked, K EM direct terms), FFT over the multiplicative group (Z/p)^* via discrete logs.
D_N, Ptilde_N, X1 etc reused from validated phase-2 kernels.
"""
import numpy as np, time, os, sys
from math import log as mlog, pi
PHASE2='/home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase2/spectral'
sys.path.insert(0,PHASE2)
import mpmath as mp
from kernels import (sieve, singular_series, ZetaDeriv, D_values_fast, Ptilde_values, set_primes)

CACHE=os.path.join(os.path.dirname(os.path.abspath(__file__)),'cache')

def get_primes(limit=2_000_000, src='/home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase5/numerics/cache'):
    fn=os.path.join(CACHE,f'primes_{limit}.npy')
    if os.path.exists(fn): return np.load(fn)
    fn2=os.path.join(src,f'primes_{limit}.npy')
    if os.path.exists(fn2):
        pr=np.load(fn2); np.save(fn,pr); return pr
    pr=sieve(limit); np.save(fn,pr); return pr

def get_C2(src='/home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase5/numerics/cache'):
    fn=os.path.join(CACHE,'C2.npy')
    if os.path.exists(fn): return float(np.load(fn)[0])
    fn2=os.path.join(src,'C2.npy')
    if os.path.exists(fn2):
        C2=float(np.load(fn2)[0]); np.save(fn,np.array([C2])); return C2
    pr=sieve(100_000_000); p=pr[pr>2].astype(float)
    C2=float(np.prod(1.0-1.0/(p-1.0)**2)); np.save(fn,np.array([C2])); return C2

def is_prime(n):
    if n<2: return False
    for q in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n%q==0: return n==q
    d=n-1; s=0
    while d%2==0: d//=2; s+=1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37):
        x=pow(a,d,n)
        if x in (1,n-1): continue
        for _ in range(s-1):
            x=x*x%n
            if x==n-1: break
        else: return False
    return True

def primitive_root(p):
    m=p-1; fac=[]; d=2
    while d*d<=m:
        if m%d==0:
            fac.append(d)
            while m%d==0: m//=d
        d+=1
    if m>1: fac.append(m)
    g=2
    while g<p:
        if all(pow(g,(p-1)//q,p)!=1 for q in fac): return g
        g+=1
    raise RuntimeError

def dlog_table(p,g):
    tab=np.full(p,-1,dtype=np.int64); cur=1
    for x in range(p-1):
        tab[cur]=x; cur=cur*g%p
    return tab

def gamma_X1(s):
    return complex(mp.gamma((mp.mpf(3)/2 - mp.mpc(s))/2)/mp.gamma((mp.mpf(3)/2 + mp.mpc(s))/2))

class FarModel:
    def __init__(self, p, H=4.0, m=1, K=8, J=24, verbose=True, gdtype=np.complex128):
        assert is_prime(p), p
        self.p=p; self.N=2*p; self.H=H; self.m=m; self.K=K; self.J=J; self.gdtype=gdtype
        self.f32=(os.environ.get('F32')=='1')
        self.gmem=os.environ.get('GMEM')
        logN=mlog(self.N); self.logN=logN
        self.alpha=1.0/logN; self.beta=0.125
        assert self.alpha<self.beta
        A=p-1; self.A=A
        self.S,self.fac=singular_series(self.N,get_C2())
        self.delta=np.sqrt(self.S/self.N)*logN**1.5
        self.Kmax=int(round(H*m))
        tks=np.arange(-self.Kmax,self.Kmax+1)/m
        self.tt=np.concatenate([tks,tks])
        self.sig=np.concatenate([np.full(len(tks),self.alpha),np.full(len(tks),self.beta)])
        self.wts=np.concatenate([np.where(np.abs(tks)<H-1e-12,1.0/m,0.5/m)]*2)
        self.n=len(self.tt)
        g=primitive_root(p); self.g=g
        self.ind=dlog_table(p,g)   # ind[r]=e for r=1..p-1
        # units mod N=2p (odd a, a != p), ascending; L(u,chi)=N^{-u} sum_a chi(a) zeta(u,a/N)
        units=np.arange(1,self.N,2)
        units=units[units!=p]
        assert len(units)==A
        self.units=units
        self.xunits=units.astype(np.float64)/self.N
        self.uexp=self.ind[units % p]
        self.oddk=np.arange(1,A,2)
        if verbose: print(f"FarModel p={p} N={self.N} H={H} m={m} K={K} nodes={self.n} A={A} logN={logN:.4f} alpha={self.alpha:.6f} delta={self.delta:.8f}",flush=True)
    def _zeta_arrays(self, u, chunk=100_000):
        """return B[a-1]=zeta(u,a/p), dB[a-1]=d/du zeta(u,a/p) for a=1..p-1 (chunked)"""
        K=self.K; J=self.J; A=self.A; p=self.p; f32=self.f32
        # Bernoulli coefficients
        from kernels import bernoulli_numbers
        if not hasattr(self,'coeff'):
            Bn=bernoulli_numbers(2*J+2)
            self.coeff=np.array([float(Bn[2*j])/float(np.prod(np.arange(1,2*j+1,dtype=float))) for j in range(1,J+1)])
        coeff=self.coeff
        # rising factorials and derivatives
        rise=np.zeros(J,dtype=complex); drise=np.zeros(J,dtype=complex)
        r=complex(u); rise[0]=r; drise[0]=1.0+0j
        for j in range(2,J+1):
            a=u+2*j-3; b=u+2*j-2
            rise[j-1]=rise[j-2]*a*b
            drise[j-1]=drise[j-2]*a*b+rise[j-2]*(a+b)
        n=np.arange(K,dtype=np.float64)
        bdt=np.complex64 if f32 else complex
        B=np.empty(A,dtype=bdt); dB=np.empty(A,dtype=bdt)
        f32=self.f32
        for c0 in range(0,A,chunk):
            sl=slice(c0,min(c0+chunk,A))
            x=self.xunits[sl]
            if f32:
                X=(n[:,None].astype(np.float32)+x[None,:].astype(np.float32))
                L=np.log(X).astype(np.float32)
                sig=np.float32(u.real); t=np.float32(u.imag)
                e=np.exp(-sig*L)
                if abs(t)<1e-15:
                    z=e.astype(np.complex64)
                else:
                    ph=t*L
                    z=e*(np.cos(ph)-np.complex64(1j)*np.sin(ph))
            else:
                X=n[:,None]+x[None,:]            # (K,chunk)
                L=np.log(X)                      # real
                sig=u.real; t=u.imag
                e=np.exp(-sig*L)
                if abs(t)<1e-15:
                    z=e.astype(complex)
                else:
                    ph=t*L
                    z=e*(np.cos(ph)-1j*np.sin(ph))
            B[sl]=z.sum(axis=0)
            dB[sl]=-(L*z).sum(axis=0)
            # EM tail, y=K+x ; recursive powers y^{1-2j}
            y=K+x; ly=np.log(y)
            tK=np.exp(-u*ly).astype(B.dtype)
            yinv2=(y**(-2.0)).astype(L.dtype)
            pj=y**(-1.0)   # y^{1-2j} at j=1
            R=y/(u-1)+0.5; Rp=-y/(u-1)**2
            cR=coeff*rise; cRp=coeff*drise
            for j in range(J):
                R += cR[j]*pj; Rp += cRp[j]*pj
                pj = pj*yinv2
            B[sl]+=tK*R
            dB[sl]+=tK*(-ly*R+Rp)
        return B,dB
    def _g_row(self, u):
        B,dB=self._zeta_arrays(u)
        # exponent order: Bexp[e]=B[a-1] with e=ind[a]
        Ae=np.empty(self.A,dtype=B.dtype); dAe=np.empty(self.A,dtype=B.dtype)
        Ae[self.uexp]=B; dAe[self.uexp]=dB
        if B.dtype==np.complex64:
            try:
                from scipy.fft import fft as _fft
                Bf=_fft(Ae); dBf=_fft(dAe)
            except Exception:
                Bf=np.fft.fft(Ae).astype(np.complex64); dBf=np.fft.fft(dAe).astype(np.complex64)
        else:
            Bf=np.fft.fft(Ae); dBf=np.fft.fft(dAe)
        idx=(-np.arange(self.A))%self.A
        g=dBf[idx]/Bf[idx]-self.logN
        return g[self.oddk]
    def build_G(self):
        A=self.A; Kmax=self.Kmax; nodd=len(self.oddk)
        if self.gmem:
            G=np.memmap(self.gmem,dtype=self.gdtype,mode='w+',shape=(self.n,nodd))
            print(f"  G memmap {self.gmem} shape {G.shape} dtype {G.dtype} size {G.nbytes/1e9:.2f}GB",flush=True)
        else:
            G=np.empty((self.n,nodd),dtype=self.gdtype)
        t0=time.time()
        # compute t>=0 nodes per line; t=0 once per line
        for li in range(2):
            base=li*(2*Kmax+1)
            for k in range(Kmax+1):
                t=k/self.m; u=(0.5+ (self.alpha if li==0 else self.beta))+1j*t
                row=self._g_row(u)
                G[base+Kmax+k]=row
                if k>0: G[base+Kmax-k]=np.conj(row[::-1])
        if isinstance(G,np.memmap): G.flush(); del G
        print(f"  build_G {time.time()-t0:.1f}s ({2*(Kmax+1)} nodes)",flush=True)
        self.G=G; return G
    def build_C(self):
        t0=time.time()
        if os.environ.get('SKIPBUILD')=='1' and self.gmem:
            G=np.memmap(self.gmem,dtype=self.gdtype,mode='r',shape=(self.n,len(self.oddk)))
            print(f"  loaded G memmap {self.gmem}",flush=True)
        else:
            G=self.build_G()
            if self.gmem:
                G=np.memmap(self.gmem,dtype=self.gdtype,mode='r',shape=(self.n,len(self.oddk)))
        A=self.A
        # chunked Gram matrix to avoid materialising a complex128 copy of a large G
        pdtype=np.complex64 if G.dtype==np.complex64 else np.complex128
        P=np.zeros((self.n,self.n),dtype=pdtype)
        cA=min(262144,A)
        for c0 in range(0,A,cA):
            gc=G[:,c0:min(c0+cA,A)]
            P+=gc@gc.conj().T
        P=P.astype(np.complex128)*(2.0/A)
        primes=get_primes(); set_primes(primes)
        Kmax=self.Kmax; m=self.m; n=self.n
        nimag=4*Kmax+1
        reals=np.array([2*self.alpha, self.alpha+0.125, 0.25])
        wdist=np.empty(3*nimag,dtype=complex)
        for r in range(3): wdist[r*nimag:(r+1)*nimag]=reals[r]+1j*(np.arange(nimag)-2*Kmax)/m
        zd=ZetaDeriv(64,24)
        Ddist=D_values_fast(1.0*wdist,primes,self.fac)
        Ptdist=Ptilde_values(wdist,zd,self.fac)
        zeta1mw=zd.eval(1.0-wdist,need=0)
        X1=np.array([gamma_X1(complex(self.sig[i]+1j*self.tt[i])) for i in range(n)])
        li=np.concatenate([np.zeros(2*Kmax+1,dtype=int),np.ones(2*Kmax+1,dtype=int)])
        ki=np.concatenate([np.arange(-Kmax,Kmax+1),np.arange(-Kmax,Kmax+1)])
        ridx=(li[:,None]+li[None,:]).astype(int); iidx=(ki[:,None]-ki[None,:]+2*Kmax).astype(int)
        flat=ridx*nimag+iidx
        Dmat=Ddist[flat].reshape(n,n)
        Mmat=(self.S*(pi/self.N)**wdist*Ptdist*zeta1mw)[flat].reshape(n,n)
        Kmat=(X1[:,None]*Mmat)*np.conj(X1)[None,:]
        E=P-Dmat-Kmat
        hermE=float(np.abs(E-E.conj().T).max()/max(1.0,np.abs(E).max()))
        Amat=np.sqrt(self.wts)/(1.0+self.sig+1j*self.tt)
        C=(Amat[:,None]*E)*np.conj(Amat)[None,:]
        self.C=C; self.hermE=hermE
        self.Cmax=float(np.abs(C).max()); self.hermC=float(np.abs(C-C.conj().T).max()/max(1.0,self.Cmax))
        ev=np.linalg.eigvalsh(C); self.ev=ev
        print(f"  C herm {self.hermC:.2e} E herm {self.hermE:.2e} |C|max {self.Cmax:.4e} time {time.time()-t0:.1f}s",flush=True)
        return C
    def result(self, H_bias=1.0):
        lam=float(np.abs(self.ev).max())
        C=lam*np.sqrt(self.N)/np.sqrt(self.S)
        return dict(p=self.p,N=self.N,H=self.H,m=self.m,K=self.K,alpha=self.alpha,S=self.S,
                    delta=self.delta,lam=lam,ratio=lam/self.delta,Y=lam*np.sqrt(self.N),C=C,
                    C_bc=C*H_bias,ratio_bc=lam*H_bias/self.delta,Cmax=self.Cmax,hermC=self.hermC,hermE=self.hermE)

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument('H',type=float); ap.add_argument('p',type=int); ap.add_argument('m',type=int,default=1)
    ap.add_argument('--K',type=int,default=8)
    a=ap.parse_args()
    t0=time.time(); mod=FarModel(a.p,H=a.H,m=a.m,K=a.K); mod.build_C(); r=mod.result()
    print("FARR "+repr(r), "wall",time.time()-t0,flush=True)
    with open(os.path.join(CACHE,'farN_results.txt'),'a') as f: f.write(repr(r)+'\n')
