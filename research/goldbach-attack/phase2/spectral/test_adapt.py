import numpy as np, mpmath as mp
from kernels import ZetaDeriv
mp.mp.dps=40
s=complex(1.2219936605,-172.75)
def h_adapt(u):
    K=max(64,int(2*abs(u.imag))+64)
    zd=ZetaDeriv(K,24)
    z,zp,zpp=zd.eval(np.array([u]),need=2)
    return zpp/z-(zp/z)**2, K
for n in [2,3,5]:
    u=n*s
    h,K=h_adapt(u)
    f=lambda t: mp.zeta(mp.mpc(t))
    zz=mp.zeta(mp.mpc(u)); zzp=mp.diff(f,mp.mpc(u),1); zzpp=mp.diff(f,mp.mpc(u),2)
    hmp=zzpp/zz-(zzp/zz)**2
    print(f"n={n} K={K}: h adapt {h[0]} mp {complex(hmp)} err {abs(h[0]-complex(hmp)):.2e}")
