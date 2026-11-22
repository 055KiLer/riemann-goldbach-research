import numpy as np, mpmath as mp
mp.mp.dps=25
pr=np.array([0]); 
def primes_upto(n):
    s=np.ones(n+1,dtype=bool); s[:2]=False
    for p in range(2,int(n**0.5)+1):
        if s[p]: s[p*p::p]=False
    return np.nonzero(s)[0]
pr=primes_upto(10**6); po=pr[pr>2]
# check F(s) identity at s=2 (well-converged)
def F_via(s):
    gp=mp.diff(lambda x: -mp.zeta(x,derivative=1)/mp.zeta(x), s)
    H=mp.mpf(0)
    for p in po[:200000]:
        pm=mp.power(int(p),-s); H-=mp.log(int(p))**2*pm**2/(1-pm)**2
    return -gp+H
def F_direct(s):
    # sum_{p,k} (log p)^2 p^{-ks} over primes to 1e6 ; plus tail estimate for k=1
    tot=mp.mpf(0)
    for p in po:
        L=mp.log(int(p)); ps=mp.power(int(p),-s)
        tot += L**2*ps/(1-ps)
    # tail p>1e6, k=1 only: sum (log p)^2 p^{-s} ~ int_{1e6}^inf (log t)^2 t^{-s} dt/log t
    P=mp.mpf(10)**6
    # int_P^inf (log t) t^{-s} dt = P^{1-s}((s-1)log P+1)/(s-1)^2
    tail = P**(1-s)*((s-1)*mp.log(P)+1)/(s-1)**2
    return tot+tail
for s in [mp.mpf(2), mp.mpf('1.5'), mp.mpf('1.1')]:
    print("s=",mp.nstr(s,4)," F_via=",mp.nstr(F_via(s),12)," F_direct=",mp.nstr(F_direct(s),12))
# also test dpole cancellation directly via w^2*(D+K) limit? we test D_K at w=0.05 by hand
