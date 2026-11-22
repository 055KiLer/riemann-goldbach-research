import numpy as np, mpmath as mp
from kernels import ZetaDeriv
mp.mp.dps=30
w=0.25-128.5625j; s=1.0+w
for n in [2,3,5,7,11,14,20]:
    u=n*s
    zd=ZetaDeriv(64,24)
    z,zp,zpp=zd.eval(np.array([u]),need=2)
    h=zpp[0]/z[0]-(zp[0]/z[0])**2
    f=lambda t: mp.zeta(mp.mpc(t))
    zz=mp.zeta(mp.mpc(u))
    hmp = mp.diff(f,mp.mpc(u),2)/zz - (mp.diff(f,mp.mpc(u),1)/zz)**2
    print(f"n={n} u={u} h_em={h:.6e} h_mp={complex(hmp):.6e} zerr={abs(complex(zz)-z[0]):.2e} |z|={abs(complex(zz)):.3e}")
