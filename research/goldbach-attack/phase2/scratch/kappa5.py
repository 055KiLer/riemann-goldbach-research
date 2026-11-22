import numpy as np, mpmath as mp
mp.mp.dps=25
def primes_upto(n):
    s=np.ones(n+1,dtype=bool); s[:2]=False
    for p in range(2,int(n**0.5)+1):
        if s[p]: s[p*p::p]=False
    return np.nonzero(s)[0]
pr=primes_upto(2*10**6); pl=[int(p) for p in pr if p>2]
NF=set([3,5,7,11,13])
psi34=mp.digamma(mp.mpf(3)/4)
C2=mp.mpf(1)
for p in pl: C2*=(1-1/(mp.mpf(p)-1)**2)
def S_of(N):
    v=2*C2
    for p in NF:
        if N%p==0: v*=mp.mpf(p-1)/(p-2)
    return v
def F(s):
    # F(s)=-g'(s)-H(s), g=-zeta'/zeta : -g'=-(zeta''/zeta)+((zeta'/zeta)^2) ; H=sum_p (log p)^2/(p^s-1)^2
    z=mp.zeta(s); z1=mp.zeta(s,derivative=1); z2=mp.zeta(s,derivative=2)
    neg_gp = -(z2/z)+(z1/z)**2
    H=mp.mpf(0)
    for p in pl:
        pm=mp.power(p,-s); H+=mp.log(p)**2*pm**2/(1-pm)**2
    return neg_gp-H, neg_gp, H
# sanity at s=2: direct F(2)
fd=mp.mpf(0)
for p in pl: fd+=mp.log(p)**2/(mp.mpf(p)**2-1)
print("F_via(2)=",mp.nstr(F(mp.mpf(2))[0],12)," F_direct(2)=",mp.nstr(fd,12))
def D_N(N,w):
    val=F(1+w)[0]
    for p in NF:
        if N%p==0:
            x=mp.power(p,-1-w); val-=mp.log(p)**2*x/(1-x)
    return val
def P_euler(N,w):
    z=mp.zeta(1+w)*(1-mp.power(2,-1-w)); prod=mp.mpf(1)
    for p in pl:
        pw=mp.power(p,-w); prod*=(1+pw/(p-2))*(1-mp.power(p,-1-w))
    for p in NF:
        if N%p==0:
            pw=mp.power(p,-w); prod/=((1+pw/(p-2))*(1-mp.power(p,-1-w)))
    return z*prod
N=30030; S=S_of(N); lg=mp.log(N); kap=lg-mp.log(2*mp.pi)+psi34
print("logN=",mp.nstr(lg,10)," target (D+K)w ->",mp.nstr(kap,10))
for a in [0.05,0.02,0.01,0.005,0.002]:
    w=2*a
    X1=mp.gamma((mp.mpf(3)/2-a)/2)/mp.gamma((mp.mpf(3)/2+a)/2)
    Pe=P_euler(N,w); D=D_N(N,w)
    K=S*mp.power(mp.pi/N,w)*Pe*mp.zeta(1-w)*X1**2
    print(f"a={a:6.3f} w={w:7.5f}  (D+K)w={mp.nstr((D+K)*w,10):>13}  diff={mp.nstr((D+K)*w-kap,8)}")
