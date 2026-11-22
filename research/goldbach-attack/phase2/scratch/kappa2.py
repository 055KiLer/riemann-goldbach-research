import numpy as np, mpmath as mp
mp.mp.dps=25
def primes_upto(n):
    s=np.ones(n+1,dtype=bool); s[:2]=False
    for p in range(2,int(n**0.5)+1):
        if s[p]: s[p*p::p]=False
    return np.nonzero(s)[0]
pr=primes_upto(3*10**6); po=pr[pr>2].astype(object)
psi34 = mp.digamma(mp.mpf(3)/4)
print("psi(3/4) =", mp.nstr(psi34,12))

NF=[3,5,7,11,13]
def S_of(N):
    C2=mp.mpf(1)
    for p in po: C2 *= (1-1/(mp.mpf(p)-1)**2)
    v=2*C2
    for p in NF:
        if N%p==0: v*= mp.mpf(p-1)/(p-2)
    return v

def F(s):
    # F(s)=sum Lambda(n)^2 n^{-s} for Re s>1 ; = -g'(s)+H(s), g=-zeta'/zeta (all primes incl 2)
    g = -mp.zeta(s,derivative=1)/mp.zeta(s)
    gp = mp.diff(lambda x: -mp.zeta(x,derivative=1)/mp.zeta(x), s)
    H = mp.mpf(0)
    for p in po:
        pm=mp.power(p,-s)
        H -= mp.log(p)**2 * pm**2/(1-pm)**2
    # tail H negligible (~1e-9 at s>=1.19)
    return -gp + H

def D_N(N,w):
    val=F(1+w)
    for p in NF:
        if N%p==0:
            x=mp.power(p,-1-w)
            val -= mp.log(p)**2*x/(1-x)
    return val

def P_euler(N,w):
    # exact: zeta(1+w)(1-2^{-1-w}) prod_{p>2,p∤N} R_p(w),  R_p=(1+p^-w/(p-2))(1-p^{-1-w})
    z = mp.zeta(1+w)*(1-mp.power(2,-1-w))
    prod=mp.mpf(1)
    for p in po:
        pw=mp.power(p,-w)
        Rp=(1+pw/(p-2))*(1-mp.power(p,-1-w))
        if p in NF and N%p==0:
            prod *= Rp   # will divide out below
        else:
            prod *= Rp
    # divide out p|N factors
    for p in NF:
        if N%p==0:
            pw=mp.power(p,-w)
            prod /= (1+pw/(p-2))*(1-mp.power(p,-1-w))
    return z*prod

N=30030; lg=mp.log(N); alpha=1/lg; w=2*alpha
S=S_of(N); cN=1/S
print("N=30030 logN=",mp.nstr(lg,12)," alpha=",mp.nstr(alpha,12))
print("S(N)=",mp.nstr(S,12)," c_N=1/S=",mp.nstr(cN,12))
Pe=P_euler(N,w)
print("P_N^Euler(2alpha)=",mp.nstr(Pe,12)," asym c_N/w=",mp.nstr(cN/w,12))
D=D_N(N,w)
X1=mp.gamma((mp.mpf(3)/2-alpha)/2)/mp.gamma((mp.mpf(3)/2+alpha)/2)
K=S*mp.power(mp.pi/N,w)*Pe*mp.zeta(1-w)*X1**2
print("D_N(2alpha)=",mp.nstr(D,12),"  1/w^2=",mp.nstr(1/w**2,12),"  D-1/w^2=",mp.nstr(D-1/w**2,12))
print("K_N(alpha,alpha)=",mp.nstr(K,12))
kappa_pred = lg - mp.log(2*mp.pi) + psi34
print("D+K =",mp.nstr(D+K,12),"   pred -kappa/w=",mp.nstr(-kappa_pred/w,12),"   kappa=",mp.nstr(kappa_pred,12))
print("empirical kappa from D+K:",mp.nstr(-(D+K)*w,12))
