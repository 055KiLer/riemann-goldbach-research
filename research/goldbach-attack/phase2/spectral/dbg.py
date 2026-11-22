import numpy as np, mpmath as mp
from math import log as mlog
from kernels import *
mp.mp.dps=30
primes=sieve(2_000_000)
S,C2,fac=singular_series(30030,primes)
zd=ZetaDeriv(K=64,J=24)
for u in [complex(3,0.3), complex(6,0.6), complex(1.2+0.2, 5.0)]:
    z,zp,zpp = zd.eval(np.array([u]),need=2)
    zz=mp.zeta(mp.mpc(u)); 
    f=lambda t: mp.zeta(mp.mpc(t))
    zzp=mp.diff(f,mp.mpc(u),1); zzpp=mp.diff(f,mp.mpc(u),2)
    print(f"u={u}: z err {abs(complex(zz)-z[0]):.2e} zp err {abs(complex(zzp)-zp[0]):.2e} zpp err {abs(complex(zzpp)-zpp[0]):.2e}")
# compare h(s) with direct h_direct(s)=sum_p (logp)^2 p^-s/(1-p^-s)^2 for s=3
from math import log
pp = primes[primes<=3_000_000].astype(float)
for s in [3+0.3j, 3+5j]:
    hd = sum( (log(p))**2 * p**(-s)/(1-p**(-s))**2 for p in pp )
    h = zeta_over_zeta_second_deriv(np.array([s]),zd)[0]
    print(f"s={s}: h direct {hd:.10f} zd {h:.10f} diff {abs(h-hd):.2e}")
# G(3s) etc direct check
for alpha in [9+0.9j, 12+1.2j]:
    Gd = sum( (log(p))**2 * p**(-alpha) for p in pp )
    print("G direct", alpha, Gd)
