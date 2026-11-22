import numpy as np, mpmath as mp
mp.mp.dps=25
def primes_upto(n):
    s=np.ones(n+1,dtype=bool); s[:2]=False
    for p in range(2,int(n**0.5)+1):
        if s[p]: s[p*p::p]=False
    return np.nonzero(s)[0]
pr=primes_upto(3*10**6); po=pr[pr>2].astype(np.float64)

# psi(3/4)
psi34 = mp.digamma(mp.mpf(3)/4)
print("psi(3/4) =", mp.nstr(psi34,12), " X1'(0)=-psi(3/4)=", mp.nstr(-psi34,12))

def C2():
    v=mp.mpf(1)
    for p in po: v*= (1-1/(mp.mpf(p)-1)**2)
    return v
def S_of(N):
    # N=30030 => primes 3,5,7,11,13
    v=2*C2()
    for p in [3,5,7,11,13]:
        if N%p==0: v*= mp.mpf(p-1)/(p-2)
    return v
def D(w):
    # sum_{p>2, p\nmid N} (log p)^2 p^{-1-w}/(1-p^{-1-w}), use all primes (N=30030; p=3..13 excluded)
    w=mp.mpf(w) if not isinstance(w,mp.mpf) else w
    out=mp.mpf(0)
    for p in po[:200000]:
        if p in (3,5,7,11,13): continue
        x=mp.power(p,-1-w)
        out += mp.log(p)**2 * x/(1-x)
    return out

def lnP(N,w):
    # log prod_{p>2,p∤N}(1+p^{-w}/(p-2)) via zeta-accelerated: log prod = log zeta(1+w)+log(1-2^{-1-w}) + log prod R_p(w)
    w=mp.mpf(w)
    # direct-ish for tiny w: sum log(1+p^-w/(p-2)) over p<=PM + tail E1; but we need accuracy.
    # Use: log prod_{p>2}(1+p^-w/(p-2)) = log zeta(1+w)+log(1-2^{-1-w}) + sum_p log R_p(w)
    # sum_p log R_p(w) converges as w->0; compute sum over p<=PM and tail (R_p-1 ~ -w^2 log^2 p/(p^2) => tiny)
    s=mp.mpf(0)
    for p in po[:300000]:
        x=mp.log(1+mp.power(p,-w)/(p-2))-mp.power(p,-1-w)  # = log R_p(w) - log(1-p^{-1-w})? careful below
        s+=x
    # Instead compute exactly: log prod = sum log(1+p^-w/(p-2)); split = sum p^{-1-w} + sum [log(1+p^-w/(p-2)) - p^{-1-w}]
    # sum p^{-1-w} = log zeta(1+w) - sum_{k>=2}(1/k) sum_p p^{-k(1+w)}
    S2=mp.mpf(0)
    for k in range(2,50):
        s2=mp.mpf(0)
        for p in po[:300000]:
            s2 += mp.power(p,-k*(1+w))
        S2 += s2/k
    A = mp.log(mp.zeta(1+w)) - S2   # sum_p p^{-1-w}
    # B = sum_{p>2} [log(1+p^-w/(p-2)) - p^{-1-w}]
    B=mp.mpf(0)
    for p in po[:300000]:
        B += mp.log(1+mp.power(p,-w)/(p-2)) - mp.power(p,-1-w)
    # tail B ~ sum_{p>PM} [-w log p/(p^2) + ...] tiny; add estimate ~ -w*int_PM^inf log t/(t^2 log t) dt = -w/PM
    B += -w/mp.mpf(3000000)
    # log prod over ALL p>2 = A - 2^{-1-w} (remove p=2) + B ... but A includes p=2: sum_p p^{-1-w}=2^{-1-w}+sum_{p>2}...
    # log prod_{p>2}(1+p^-w/(p-2)) = (A - 2^{-1-w}) + B
    return A - mp.power(2,-1-w) + B

def lnP_N(N,w):
    lp = lnP(N,w)
    for p in [3,5,7,11,13]:
        if N%p==0:
            lp -= mp.log(1+mp.power(p,-w)/(p-2))
    return lp

N=30030
lg=mp.log(N); alpha=1/lg; w=2*alpha
S=S_of(N)
cN=1/S
print("N=30030 logN=",mp.nstr(lg,10)," alpha=",mp.nstr(alpha,10)," S(N)=",mp.nstr(S,12)," c_N=1/S=",mp.nstr(cN,12))
lp=lnP_N(N,w)
P_N_euler=mp.e**lp
print("P_N^Euler(2alpha)=",mp.nstr(P_N_euler,12)," check w*P=",mp.nstr(w*P_N_euler,12))
Dval=D(w)
print("D_N(2alpha)=",mp.nstr(Dval,12)," 1/w^2=",mp.nstr(1/w**2,12))
# K_N(alpha,alpha) = S(N)(pi/N)^w P^Euler(w) zeta(1-w) X1(alpha)^2
X1=mp.gamma((mp.mpf(3)/2-alpha)/2)/mp.gamma((mp.mpf(3)/2+alpha)/2)
K = S*mp.power(mp.pi/N,w)*P_N_euler*mp.zeta(1-w)*X1**2
print("K_N(alpha,alpha)=",mp.nstr(K,12))
summ = Dval+K
kappa_pred = lg - mp.log(2*mp.pi) + psi34
print("D+K =",mp.nstr(summ,12), " pred -kappa/w =",mp.nstr(-kappa_pred/w,12), " kappa=",mp.nstr(kappa_pred,12))
print("kappa/w =",mp.nstr(kappa_pred/w,12))
# extract kappa from numerics: (D+K)*(-w)
print("empirical kappa =",mp.nstr(-summ*w,12))
