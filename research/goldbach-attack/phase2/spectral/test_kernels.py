import numpy as np
from math import log as mlog
from kernels import *
primes=sieve(2_000_000); set_primes(primes)
C2=C2_constant(primes); S,fac=singular_series(30030,C2)
print("C2",C2,"S",S, "fac",fac)
zd=ZetaDeriv(K=64,J=24)
for w in [complex(2.0,0.3), complex(1.5,-2.0)]:
    Dv=D_values(np.array([w]),zd,fac)[0]
    s=1.0+w; tot=0j
    pp=primes[primes<=3_000_000].astype(float)
    for p in pp:
        if any(p%q==0 for q in fac): continue
        lp=mlog(p); x=lp*lp*p**(-s)
        tot+=x/(1.0-p**(-s))
    print(f"w={w}: D_values={Dv:.12f} direct={tot:.12f} diff={abs(Dv-tot):.2e}")
for w in [complex(2.0,0.2), complex(1.2,-1.0)]:
    Pt=Ptilde_values(np.array([w]),zd,fac,Pcut=200000)[0]
    tot=0j
    for p in primes[primes<=3_000_000]:
        if p<=2 or any(p%q==0 for q in fac): continue
        tot+=np.log1p(p**(-w)/(p-2.0))
    print(f"w={w}: log Ptilde={np.log(Pt):.12f} direct-log(p<=3e6)={tot:.12f} diff={np.log(Pt)-tot:.2e}")
# test Ptilde at small Re w against alternative: use mpmath product + E1 tail with known formula (should be self-consistent)
for w in [complex(0.194,0.0), complex(0.2,5.0)]:
    Pt=Ptilde_values(np.array([w]),zd,fac,Pcut=500000)[0]
    Pt2=Ptilde_values(np.array([w]),zd,fac,Pcut=200000)[0]
    print(f"w={w}: Ptilde(5e5)={Pt:.12f} Ptilde(2e5)={Pt2:.12f} diff={abs(Pt-Pt2):.2e}")
