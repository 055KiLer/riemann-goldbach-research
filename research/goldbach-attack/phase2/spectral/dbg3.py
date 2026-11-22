import numpy as np
from math import log as mlog
from kernels import *
primes=sieve(3_000_000); set_primes(primes)
C2=C2_constant(primes); S,fac=singular_series(30030,C2)
zd=ZetaDeriv(K=64,J=24)
pp=primes.astype(float); lp=np.log(pp)
for s in [3+0.3j, 2.5-2j]:
    # direct h(u) via prime sums for u=s and n*s
    def hd(u):
        return np.sum(lp**2*pp**(-u)/(1-pp**(-u))**2)
    R_all = np.sum(lp**2*pp**(-2*s)/(1-pp**(-s))**2)
    R_series = 0j
    for n in range(2,51):
        cn=c_small(n)
        R_series += cn*hd(n*s)
    print(f"s={s}: R_all={R_all:.12f} R_series={R_series:.12f} diff={abs(R_all-R_series):.2e}")
    # also direct G check: G(s) = sum mu(k) k h(ks)
    G_direct=np.sum(lp**2*pp**(-s))
    G_mob=0j
    for k in range(1,51):
        mu=0
        # simple mobius
        n=k; cnt=0; sq=False; d=2
        while d*d<=n:
            if n%d==0:
                n//=d; cnt+=1
                if n%d==0: sq=True
                while n%d==0: n//=d
            d+=1
        if n>1: cnt+=1
        mu = 0 if sq else (-1)**cnt
        if mu!=0: G_mob += mu*k*hd(k*s)
    print(f"   G direct={G_direct:.12f} G mobius={G_mob:.12f} diff={abs(G_direct-G_mob):.2e}")
