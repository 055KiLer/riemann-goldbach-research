import numpy as np, mpmath as mp
mp.mp.dps=22
def primes_upto(n):
    s=np.ones(n+1,dtype=bool); s[:2]=False
    for p in range(2,int(n**0.5)+1):
        if s[p]: s[p*p::p]=False
    return np.nonzero(s)[0]
pr=primes_upto(10**6); po=pr[pr>2].astype(object)
NF=[3,5,7,11,13]
psi34=mp.digamma(mp.mpf(3)/4)
C2=mp.mpf(1)
for p in po: C2*=(1-1/(mp.mpf(p)-1)**2)
def S_of(N):
    v=2*C2
    for p in NF:
        if N%p==0: v*=mp.mpf(p-1)/(p-2)
    return v
def F(s):
    gp=mp.diff(lambda x: -mp.zeta(x,derivative=1)/mp.zeta(x), s)
    H=mp.mpf(0)
    for p in po:
        pm=mp.power(p,-s); H-=mp.log(p)**2*pm**2/(1-pm)**2
    return -gp+H
def D_N(N,w):
    val=F(1+w)
    for p in NF:
        if N%p==0:
            x=mp.power(p,-1-w); val-=mp.log(p)**2*x/(1-x)
    return val
def P_euler(N,w):
    z=mp.zeta(1+w)*(1-mp.power(2,-1-w))
    prod=mp.mpf(1)
    for p in po:
        pw=mp.power(p,-w)
        prod*=(1+pw/(p-2))*(1-mp.power(p,-1-w))
    for p in NF:
        if N%p==0:
            pw=mp.power(p,-w)
            prod/=((1+pw/(p-2))*(1-mp.power(p,-1-w)))
    return z*prod
N=30030; S=S_of(N); lg=mp.log(N)
print("logN=",mp.nstr(lg,10),"  predicted leading pole coeff kappa=logN-log2pi+psi(3/4)=",mp.nstr(lg-mp.log(2*mp.pi)+psi34,10))
for a in [0.05,0.03,0.02,0.015,0.01,0.007]:
    w=2*a
    X1=mp.gamma((mp.mpf(3)/2-a)/2)/mp.gamma((mp.mpf(3)/2+a)/2)
    Pe=P_euler(N,w); D=D_N(N,w)
    K=S*mp.power(mp.pi/N,w)*Pe*mp.zeta(1-w)*X1**2
    tot=D+K
    print(f"alpha={a:6.3f} w={w:6.4f} (D+K)*w = {mp.nstr(tot*w,9):>14}   -kappa(w)?; (D+K)*w - (-(kappa)) = {mp.nstr(tot*w+(lg-mp.log(2*mp.pi)+psi34),8)}")
