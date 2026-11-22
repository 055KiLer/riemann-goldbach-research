import numpy as np
from kernels import D_values, D_values_fast, ZetaDeriv, singular_series, set_primes, h_values, c_small
import model as MOD
primes=MOD.get_primes(2_000_000); set_primes(primes); C2=float(np.load('cache/C2.npy')[0]); S,fac=singular_series(30030,C2)
zd=ZetaDeriv(64,24)
w=np.array([0.25-128.5625j, 0.25+100j, 0.194+128j])
print("old D_values:", D_values(w,zd,fac))
print("fast D_values:", D_values_fast(w,primes,fac))
# inspect R terms for first w
s=1.0+w[0]
print("h(s) =",h_values(np.array([s]),zd)[0])
for n in range(2,51):
    cn=c_small(n)
    if cn!=0:
        hv=h_values(np.array([n*s]),zd)[0]
        if abs(cn*hv)>1e-6: print("n",n,"c",cn,"h(ns)",hv,"contrib",cn*hv)
