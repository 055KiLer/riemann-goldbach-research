import numpy as np
from math import log as mlog
from kernels import *
primes=sieve(3_000_000); set_primes(primes)
pp=primes.astype(float); lp=np.log(pp)
for s in [3+0.3j, 2.5-2j]:
    R_all = np.sum(lp**2*pp**(-2*s)/(1-pp**(-s))**2)
    R_G = 0j
    for k in range(2,60):
        Gk=np.sum(lp**2*pp**(-k*s))
        R_G += (k-1)*Gk
    print(f"s={s}: R_all={R_all:.14e} R_G={R_G:.14e} diff={abs(R_all-R_G):.2e}")
    # per n coefficients: compute R as sum over n of h(ns)*c_n via numerical coefficient extraction:
    # c_n = sum_{d|n}(n/d-1)*d*mu(d)  (analytic formula gave prod(p-1))
    def mob(n):
        fac=[]; d=2; x=n
        while d*d<=x:
            if x%d==0:
                fac.append(d)
                while x%d==0: x//=d
            d+=1
        if x>1: fac.append(x)
        return fac, len(fac)
    for n in range(2,8):
        facs,cnt=mob(n)
        sq=any(n%(p*p)==0 for p in facs)
        if sq: 
            mu=0
        else:
            mu=(-1)**cnt
        # divisor sum
        c=0
        for d in range(1,n+1):
            if n%d==0:
                # mu(d)
                fd,cd=mob(d)
                m=0 if any(d%(p*p)==0 for p in fd) else (-1)**cd
                c += (n//d-1)*d*m
        print("  n",n,"c(divsum)",c, " prod(p-1)", c_small(n))
