import numpy as np, mpmath as mp
from math import log as mlog
from kernels import *
import model as MOD
mp.mp.dps=30
primes=MOD.get_primes(2_000_000); set_primes(primes); C2=MOD.get_C2(); S,fac=singular_series(30030,C2)
zd=ZetaDeriv(64,24)
w=0.22199366053170907-172.75j
s=1.0+w
print("s",s)
for Nmax in [2,5,10,20,30,40,50]:
    Dv=D_values(np.array([w]),zd,fac,Nmax=Nmax)[0]
    print("Nmax",Nmax,"D=",Dv)
# h values
hs=zeta_over_zeta_second_deriv if False else None
from kernels import h_values
print("h(s)",h_values(np.array([s]),zd)[0])
for n in [2,3,4,5,10,20,30,40,50]:
    print("n",n,"h(ns)=",h_values(np.array([n*s]),zd)[0])
# compare with mpmath h(u)=sum_p (logp)^2 p^-u/(1-p^-u)^2 truncation + zeta ratio method
def h_mp(u):
    z=mp.zeta(u); zp=mp.diff(mp.zeta,u,1); zpp=mp.diff(mp.zeta,u,2)
    return zpp/z-(zp/z)**2
print("h(s) mpmath", complex(h_mp(mp.mpc(s))))
for n in [2,3]:
    print(f"h({n}s) mpmath", complex(h_mp(mp.mpc(n*s))))
