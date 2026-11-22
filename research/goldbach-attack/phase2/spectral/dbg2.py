import numpy as np
from math import log as mlog
from kernels import *
primes=sieve(3_000_000)
S,C2,fac=singular_series(30030,primes)
zd=ZetaDeriv(K=64,J=24)
w=2.0+0.3j; s=1.0+w
pp = primes.astype(float)
mask = np.array([not any(p%q==0 for q in fac) for p in pp])
pN = pp[mask]
# direct f
f_direct = np.sum((np.log(pN)**2)*pN**(-s)/(1-pN**(-s)))
# h_all, R_all direct
h_all = np.sum((np.log(pp)**2)*pp**(-s)/(1-pp**(-s))**2)
R_all = np.sum((np.log(pp)**2)*pp**(-2*s)/(1-pp**(-s))**2)
# diag (p|N)
diag = sum(mlog(p)**2*p**(-s)/(1-p**(-s)) for p in fac)
print("f_direct", f_direct)
print("h_all-R_all-diag", h_all-R_all-diag)
# R via series h2 + sum c_k G(ks)
h2 = np.sum((np.log(pp)**2)*pp**(-2*s)/(1-pp**(-2*s))**2)
acc = h2
for k in range(3,15):
    ck=(k-1) if k%2 else k//2
    Gk=np.sum((np.log(pp)**2)*pp**(-k*s))
    acc += ck*Gk
print("R via h2+series", acc, " R_all", R_all, " diff", abs(acc-R_all))
print("h zd", zeta_over_zeta_second_deriv(np.array([s]),zd)[0], "h_all", h_all)
print("h2 zd", zeta_over_zeta_second_deriv(np.array([2*s]),zd)[0], "h2 direct", h2)
Dv=D_values(np.array([w]),zd,primes,fac)[0]
print("D_values", Dv)
