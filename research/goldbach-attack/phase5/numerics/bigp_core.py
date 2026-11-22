"""Large-conductor Li-Liu finite model for N = 2p (p prime): efficient (Z/p)^* DFT method.

L(u,chi_k) = p^{-u} sum_{a=1}^{p-1} chi_k(a) zeta(u,a/p),  chi_k(g^e)=omega^{ke}.
Build L'/L for all odd chi (k odd) at all nodes via vectorised Euler-Maclaurin + FFT over the
discrete-log array. Reuses D_N, Ptilde_N, singular series from the validated phase-2 code.
"""
import numpy as np, sys, os, time
from math import log as mlog, pi
PHASE2='/home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase2/spectral'
sys.path.insert(0,PHASE2)
import mpmath as mp
from kernels import (sieve, singular_series, ZetaDeriv, D_values_fast, Ptilde_values, set_primes,
                     bernoulli_numbers)
import model as MOD2

CACHE=os.path.join(os.path.dirname(os.path.abspath(__file__)),'cache')
os.makedirs(CACHE, exist_ok=True)

def get_primes(limit=2_000_000):
    fn=os.path.join(CACHE,f'primes_{limit}.npy')
    if os.path.exists(fn): return np.load(fn)
    pr=sieve(limit); np.save(fn,pr); return pr

def get_C2():
    fn=os.path.join(CACHE,'C2.npy')
    if os.path.exists(fn): return float(np.load(fn)[0])
    pr=sieve(100_000_000); p=pr[pr>2].astype(float)
    C2=float(np.prod(1.0-1.0/(p-1.0)**2)); np.save(fn,np.array([C2])); return C2

def gamma_X1(s):
    return complex(mp.gamma((mp.mpf(3)/2 - mp.mpc(s))/2)/mp.gamma((mp.mpf(3)/2 + mp.mpc(s))/2))

def primitive_root(p):
    # factor p-1
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
    tab=np.full(p,-1,dtype=np.int64)
    cur=1
    for x in range(p-1):
        tab[cur]=x; cur=cur*g%p
    return tab

class BigPModel:
    def __init__(self, p, H=20.0, m=8, c=1.0, K=None, J=24, verbose=True):
        self.p=p; self.N=2*p; self.H=H; self.m=m; self.c=c
        logN=mlog(self.N)
        self.alpha=c/logN; self.beta=0.125
        assert self.alpha<self.beta, f"strip empty: alpha={self.alpha}>=beta"
        if K is None: K = 64 if abs(H)<=12 else 32
        self.K=K; self.J=J
        p_=self.p; A=p_-1
        self.A=A
        self.logp=mlog(p_); self.logN=logN
        g=primitive_root(p_)
        self.g=g
        tab=dlog_table(p_,g)
        self.ind_all=tab[1:p_]     # ind(a) for a=1..p-1 (array indexed by a-1)
        # singular series, fac
        C2=get_C2()
        # factor p (prime) and 2
        S,fac=singular_series(self.N,C2)
        self.S=S; self.fac=fac
        self.delta=np.sqrt(S/self.N)*(logN)**1.5
        self.primes=get_primes(); set_primes(self.primes)
        # nodes: s = alpha + i t  and beta + i t, t=k/m, |k|<=Kmax
        self.Kmax=int(round(H*m))
        tks=np.arange(-self.Kmax,self.Kmax+1)/m
        self.tt=np.concatenate([tks,tks])
        self.sig=np.concatenate([np.full(len(tks),self.alpha), np.full(len(tks),self.beta)])
        self.wts=np.concatenate([np.where(np.abs(tks)<H-1e-12,1.0/m,0.5/m)]*2)
        self.n=len(self.tt)
        if verbose: print(f"BigP p={p} N={self.N} H={H} m={m} c={c} K={K} nodes={self.n} alpha={self.alpha:.6f} delta={self.delta:.8f}",flush=True)
    # ---------- G matrix (nodes x odd chars) ----------
    def build_G(self, chunk=200_000, dtype=complex):
        p_,A,K,J,m=self.p,self.A,self.K,self.J,self.m
        Kmax=self.Kmax
        h=1.0/m
        # Bernoulli coefficients B_{2j}/(2j)!
        B=bernoulli_numbers(2*J+2)
        coeff=np.array([float(B[2*j])/float(np.prod(np.arange(1,2*j+1,dtype=float))) for j in range(1,J+1)])
        x=np.arange(1,p_,dtype=np.float64)/p_    # a/p for a=1..p-1
        n=np.arange(K,dtype=np.float64)
        L=np.empty((K,A),dtype=np.float32)
        for i in range(K):
            L[i]=np.log(n[i]+x).astype(np.float32)
        y=(K+x).astype(np.float64)
        ly=np.log(y)
        # V[a,j]=y^{1-2j}
        V=np.empty((A,J),dtype=np.float64)
        e=(1.0-2.0*np.arange(1,J+1))
        for j in range(J): V[:,j]=np.exp(e[j]*ly)
        sig_lines=np.array([0.5+self.alpha, 0.5+self.beta])
        Efac=[np.exp(-s*L.astype(np.float64)).astype(np.float32) for s in sig_lines]  # (K,A) float32
        q=np.exp(-1j*L.astype(np.float64)/m).astype(dtype)     # (K,A)
        z=np.ones((K,A),dtype=dtype)
        qK=np.exp(-1j*ly/m)
        tKk=np.ones(A,dtype=dtype)
        eK=[np.exp(-s*ly) for s in sig_lines]
        nodd=A//2
        G=np.empty((self.n,nodd),dtype=complex)
        t0=time.time(); tt_fft=0.0; tt_sum=0.0; tt_em=0.0
        for k in range(Kmax+1):
            t=k/m
            for li in range(2):
                u=sig_lines[li]+1j*t
                # rising factorials and derivatives (scalars)
                rise=np.zeros(J,dtype=complex); drise=np.zeros(J,dtype=complex)
                r=complex(u); dr=1.0+0j; rise[0]=r; drise[0]=dr
                for j in range(2,J+1):
                    a=u+2*j-3; b=u+2*j-2
                    rise[j-1]=rise[j-2]*a*b
                    drise[j-1]=drise[j-2]*a*b+rise[j-2]*(a+b)
                R=y/(u-1)+0.5+V@(coeff*rise)
                Rp=-y/(u-1)**2+V@(coeff*drise)
                # direct sums in chunks
                B=np.zeros(A,dtype=complex); dB=np.zeros(A,dtype=complex)
                Ef=Efac[li]
                for c0 in range(0,A,chunk):
                    sl=slice(c0,min(c0+chunk,A))
                    P=z[:,sl]*Ef[:,sl]
                    B[sl]=P.sum(axis=0)
                    dB[sl]=-(L[:,sl].astype(np.float64)*P).sum(axis=0)
                tK=(tKk*eK[li]).astype(complex)
                B+=tK*R
                dB+=tK*(-ly*R+Rp)
                # reorder from a-order to exponent order e=ind(a), then FFT:
                # Bhat[k]=sum_e b[e] omega^{ke} = FFT(b)[(-k) mod A]
                Be=np.empty(A,dtype=complex); dBe=np.empty(A,dtype=complex)
                Be[self.ind_all]=B; dBe[self.ind_all]=dB
                _tf=time.time()
                Bf=np.fft.fft(Be); dBf=np.fft.fft(dBe)
                tt_fft+=time.time()-_tf
                idx=np.arange(A)
                ridx=(-idx)%A
                Bc=Bf[ridx]; dBc=dBf[ridx]
                g=dBc/Bc-self.logp
                tt_sum+=time.time()-t0-tt_fft-tt_em if False else 0
                oddk=np.arange(1,A,2)
                row=g[oddk]
                G[li*(2*Kmax+1)+(Kmax+k)]=row
                if k>0:
                    G[li*(2*Kmax+1)+(Kmax-k)]=np.conj(row[::-1])
            z=(z*q).astype(dtype) if dtype is complex else (z*q).astype(dtype)
            tKk=(tKk*qK).astype(dtype)
        self.G=G
        print(f"  build_G time {time.time()-t0:.1f}s (fft {tt_fft:.1f}s)",flush=True)
        return G
    # ---------- assemble C ----------
    def build_C(self):
        t0=time.time()
        G=self.build_G()
        Phi=self.p-1
        P=(2.0/Phi)*(G@G.conj().T)
        if not hasattr(self,'primes'): self.primes=get_primes(); set_primes(self.primes)
        fac=self.fac
        Kmax=self.Kmax; m=self.m; n=self.n
        nimag=4*Kmax+1
        reals=np.array([2*self.alpha, self.alpha+0.125, 0.25])
        wdist=np.empty(3*nimag,dtype=complex)
        for r in range(3): wdist[r*nimag:(r+1)*nimag]=reals[r]+1j*(np.arange(nimag)-2*Kmax)/m
        zd=ZetaDeriv(64,24)
        Ddist=D_values_fast(1.0*wdist,self.primes,fac)
        Ptdist=Ptilde_values(wdist,zd,fac)
        zeta1mw=zd.eval(1.0-wdist,need=0)
        X1=np.array([gamma_X1(complex(self.sig[i]+1j*self.tt[i])) for i in range(n)])
        li=np.concatenate([np.zeros(2*Kmax+1,dtype=int),np.ones(2*Kmax+1,dtype=int)])
        ki=np.concatenate([np.arange(-Kmax,Kmax+1),np.arange(-Kmax,Kmax+1)])
        ridx=(li[:,None]+li[None,:]).astype(int)
        iidx=(ki[:,None]-ki[None,:]+2*Kmax).astype(int)
        flat=ridx*nimag+iidx
        Dmat=Ddist[flat].reshape(n,n)
        Mm=(self.S*(pi/self.N)**wdist*Ptdist*zeta1mw)[flat].reshape(n,n)
        Kmat=(X1[:,None]*Mm)*np.conj(X1)[None,:]
        E=P-Dmat-Kmat
        hermE=np.abs(E-E.conj().T).max()/max(1.0,np.abs(E).max())
        A_=np.sqrt(self.wts)/(1.0+self.sig+1j*self.tt)
        C=(A_[:,None]*E)*np.conj(A_)[None,:]
        self.C=C; self.hermE=hermE
        self.Cmax=float(np.abs(C).max())
        self.hermC=float(np.abs(C-C.conj().T).max()/max(1.0,self.Cmax))
        # spectra
        ev=np.linalg.eigvalsh(C)
        self.ev=ev
        self.trace=float(np.trace(C).real); self.HSnorm=float(np.sqrt(np.sum(ev**2)))
        print(f"  C herm {self.hermC:.2e} E herm {self.hermE:.2e} |C|max {self.Cmax:.4e} time {time.time()-t0:.1f}s",flush=True)
        return C
    def result(self):
        lam=float(np.abs(self.ev).max())
        self.X=lam*np.sqrt(self.N)/np.sqrt(self.S)
        return dict(p=self.p,N=self.N,H=self.H,m=self.m,c=self.c,alpha=self.alpha,beta=self.beta,
                    phi=self.p-1,S=self.S,delta=self.delta,lam=lam,ratio=lam/self.delta,X=self.X,
                    Cmax=self.Cmax,hermC=self.hermC,trace=self.trace,HS=self.HSnorm,ev=self.ev)

if __name__=='__main__':
    # quick self-test: N=40022 (p=20011) H=20 m=8, compare with phase2 model.py reference
    t0=time.time()
    mod=BigPModel(20011,H=20.0,m=8)
    mod.build_C()
    res=mod.result()
    print("RESULT",res['p'],"lam",res['lam'],"delta",res['delta'],"ratio",res['ratio'],"X",res['X'],"time",time.time()-t0)
