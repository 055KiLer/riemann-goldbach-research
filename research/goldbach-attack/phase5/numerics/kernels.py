"""Numerical kernels: D_N(w), Ptilde_N(w), K_N(s,z), singular series.
All accuracy-oriented constructions use zeta-factor extraction:
  h(u) = (zeta'/zeta)'(u) = sum_p (log p)^2 p^{-u}/(1-p^{-u})^2
  R(s) = sum_{k>=2} (k-1) G(ks),  G(u)=sum_p (log p)^2 p^{-u}
  f_all(s) = sum_p (log p)^2 p^{-s}/(1-p^{-s}) = h(s) - R(s)
  Möbius inversion of h(u)=sum_m m G(mu) gives R(s) = sum_{n>=2} c_n h(ns),
  c_n = prod_{p|n}(p-1).
"""
import numpy as np
from math import log as mlog
from hurwitz import bernoulli_numbers

def sieve(limit):
    b = np.ones(limit+1, dtype=bool); b[:2]=False
    for p in range(2, int(limit**0.5)+1):
        if b[p]: b[p*p::p]=False
    return np.nonzero(b)[0]

def prime_factors(n):
    fac=[]; d=2
    while d*d<=n:
        if n%d==0:
            fac.append(d)
            while n%d==0: n//=d
        d+=1
    if n>1: fac.append(n)
    return fac

def singular_series(N, C2):
    fac = prime_factors(N)
    S = 2.0*C2
    for p in fac:
        if p>2: S *= (p-1)/(p-2)
    return S, fac

def C2_constant(primes):
    p = primes[primes>2].astype(float)
    return float(np.prod(1.0-1.0/(p-1.0)**2))

# ---------------- vectorized Euler-Maclaurin for zeta + derivatives ----------------
class ZetaDeriv:
    def __init__(self, K=64, J=24):
        self.K=K; self.J=J
        B = bernoulli_numbers(2*J+2)
        self.c = np.array([float(B[2*j])/float(np.prod(np.arange(1,2*j+1,dtype=float))) for j in range(1,J+1)])
        n = np.arange(1,K+1, dtype=float)
        self.logn = np.log(n); self.logn2 = self.logn**2
        self.y = K+1.0; self.ly = mlog(self.y)
        self.powj = np.array([self.y**(1-2*j) for j in range(1,J+1)], dtype=float)
    def eval(self, u, need=2):
        u = np.asarray(u, dtype=complex); M=u.shape[0]
        E1 = np.exp(-u[:,None]*self.logn[None,:])
        S0 = E1.sum(axis=1); res=[S0]
        if need>=1: S1 = -(self.logn[None,:]*E1).sum(axis=1)
        if need>=2: S2 = (self.logn2[None,:]*E1).sum(axis=1)
        Et = np.exp((1-u)*self.ly); om=u-1.0
        S0 += Et/om
        if need>=1: S1 += Et*(-self.ly/om - 1.0/om**2)
        if need>=2: S2 += Et*(self.ly**2/om + 2*self.ly/om**2 + 2.0/om**3)
        Eu = np.exp(-u*self.ly)
        S0 += 0.5*Eu
        if need>=1: S1 += -0.5*self.ly*Eu
        if need>=2: S2 += 0.5*self.ly**2*Eu
        P = np.ones(M, dtype=complex); Pp=np.zeros(M); Ppp=np.zeros(M)
        for j in range(1, self.J+1):
            if j==1:
                P=u; Pp=np.ones(M); Ppp=np.zeros(M)
            else:
                a=u+(2*j-3); b=u+(2*j-2)
                Pn=P*a*b; Ppn=Pp*a*b+P*(a+b); Pppn=Ppp*a*b+2*Pp*(a+b)+2*P
                P,Pp,Ppp=Pn,Ppn,Pppn
            cj=self.c[j-1]; pw=self.powj[j-1]
            S0 += cj*P*Eu*pw
            if need>=1: S1 += cj*pw*(Pp*Eu - self.ly*P*Eu)
            if need>=2: S2 += cj*pw*(Ppp*Eu - 2*self.ly*Pp*Eu + self.ly**2*P*Eu)
        if need==0: return S0
        if need==1: return S0,S1
        return S0,S1,S2

def h_values(u, zd):
    """h(u) = (zeta'/zeta)'(u) = sum_p (log p)^2 p^{-u}/(1-p^{-u})^2."""
    z,zp,zpp = zd.eval(u, need=2)
    return zpp/z - (zp/z)**2

# ---------------- E1 / prime tail ----------------
def E1_complex_arr(z):
    """E1(z) for complex array z via continued fraction for large |z|, mpmath fallback small."""
    import mpmath as mp
    mp.mp.dps=30
    out = np.empty(z.shape, dtype=complex)
    for i,zz in enumerate(z):
        out[i] = complex(mp.gammainc(0, mp.mpc(complex(zz)), mp.inf))
    return out

# ---------------- D_N(w) ----------------
def c_small(n):
    """c_n = (-1)^{omega(n)+1} prod_{p|n}(p-1)  (R(s)=sum_{n>=2} c_n h(ns))."""
    fs=prime_factors(n)
    c=1
    for p in fs: c*= (p-1)
    return c if (len(fs)%2==1) else -c

def D_values(w, zd, fac, Nmax=50):
    """D_N(w) = sum_{(n,N)=1} Lambda^2(n) n^{-1-w} = h(s) - R(s) - diag(s), s=1+w,
    R(s)=sum_{n>=2} c_n h(ns)."""
    w=np.asarray(w,dtype=complex); M=w.shape[0]
    s=1.0+w
    h = h_values(s, zd)
    R = np.zeros(M, dtype=complex)
    for n in range(2, Nmax+1):
        cn = c_small(n)
        if cn==0: continue
        R += cn*h_values(n*s, zd)
    diag = np.zeros(M, dtype=complex)
    for p in fac:
        lp = mlog(p); pp = p**(-s)
        diag += lp*lp*pp/(1.0-pp)
    return h - R - diag

# ---------------- Ptilde_N(w) ----------------
def Ptilde_values(w, zd, fac, Pcut=200000):
    """Ptilde_N(w) = prod_{p>2,p∤N}(1 + p^{-w}/(p-2)).
    = [zeta(1+w)/zeta(2+2w)] / [(1+2^{-1-w}) prod_{p|N,p>2}(1+p^{-1-w})]
      * prod_{2<p<=Pcut, p∤N} ratio_p * exp(2E1((1+w)L)+4E1((2+w)L)-2E1((2+2w)L))
    with ratio_p=(1+p^{-w}/(p-2))/(1+p^{-1-w}), L=log Pcut."""
    w=np.asarray(w,dtype=complex); M=w.shape[0]
    zd_ = zd
    z1 = zd.eval(1.0+w, need=0)
    z2 = zd.eval(2.0+2.0*w, need=0)
    Pr = zd.Primes if hasattr(zd,'Primes') else None
    # primes are injected via module-level cache
    Pr_all = _PRIMES
    Pr = Pr_all[Pr_all<=Pcut]; Pr = Pr[Pr>2]
    for p in fac:
        if p>2: Pr = Pr[Pr%p!=0]
    lP = np.log(Pr.astype(float)); Pf = Pr.astype(float)
    L = mlog(Pcut)
    out = np.empty(M, dtype=complex)
    for i in range(M):
        wi=w[i]
        y = np.exp(-wi*lP)
        ratio = (1.0+y/(Pf-2.0))/(1.0+np.exp(-(1.0+wi)*lP))
        logprod = np.log(ratio).sum()
        tail = 2.0*_E1((1.0+wi)*L) + 4.0*_E1((2.0+wi)*L) - 2.0*_E1((2.0+2.0*wi)*L)
        A = z1[i]/(z2[i]*(1.0+2.0**(-1.0-wi)))
        for p in fac:
            if p>2: A /= (1.0+p**(-1.0-wi))
        out[i] = A*np.exp(logprod+tail)
    return out

# module-level primes + E1 scalar
_PRIMES = None
def set_primes(primes):
    global _PRIMES
    _PRIMES = primes

_E1_cache = {}
def _E1(z):
    key = complex(z)
    if key in _E1_cache: return _E1_cache[key]
    import mpmath as mp
    mp.mp.dps = 30
    v = complex(mp.gammainc(0, mp.mpc(key), mp.inf))
    if len(_E1_cache)<200000: _E1_cache[key]=v
    return v

def S_N(w, fac):
    """singular series density series S_N(w)=S(N)zeta(w)Ptilde(w) - not needed here."""
    pass

# ---------------- fast (adaptive-K) D_N for small Re s / large |Im s| ----------------
def _h_adapt(u):
    """h(u)=(zeta'/zeta)'(u) with adaptive K to avoid EM divergence at large |Im u|."""
    u=np.asarray(u,dtype=complex)
    im=np.abs(u.imag).max()
    K=max(64,int(2*im)+64)
    zd=ZetaDeriv(K,24)
    z,zp,zpp=zd.eval(u,need=2)
    return zpp/z-(zp/z)**2

def D_values_fast(w, primes, fac, Nmax=40):
    """D_N(w) for Re w>0 (any |Im|), adaptive EM + direct prime sums."""
    w=np.asarray(w,dtype=complex); M=w.shape[0]
    s=1.0+w
    h1=_h_adapt(s); h2=_h_adapt(2*s); h3=_h_adapt(3*s)
    R = 1.0*h2 + 2.0*h3
    Psmall=primes[primes<=10000].astype(float); lP=np.log(Psmall); lP2=lP**2
    diag=np.zeros(M,dtype=complex)
    out=np.empty(M,dtype=complex)
    for i in range(M):
        si=s[i]
        y=np.exp(-si*lP)
        yn=y**4
        for n in range(4,Nmax+1):
            cn=c_small(n)
            if cn!=0:
                R[i] += cn*np.sum(lP2*yn/(1.0-yn)**2)
            yn=yn*y
        for p in fac:
            lp=mlog(p); pp=p**(-si)
            diag[i] += lp*lp*pp/(1.0-pp)
        out[i]=h1[i]-R[i]-diag[i]
    return out
