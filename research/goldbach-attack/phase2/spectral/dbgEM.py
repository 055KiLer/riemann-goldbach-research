import numpy as np, mpmath as mp
from kernels import ZetaDeriv
mp.mp.dps=40
s=complex(1.2219936605,-172.75)
for n in [2,3,5,10]:
    u=n*s
    zd=ZetaDeriv(64,24)
    z,zp,zpp=zd.eval(np.array([u]),need=2)
    f=lambda t: mp.zeta(mp.mpc(t))
    zz=mp.zeta(mp.mpc(u)); zzp=mp.diff(f,mp.mpc(u),1); zzpp=mp.diff(f,mp.mpc(u),2)
    print(f"n={n} u={u}")
    print("  z err",abs(complex(zz)-z[0]),"|z|",abs(complex(zz)))
    print("  zp err",abs(complex(zzp)-zp[0]),"|zp|",abs(complex(zzp)))
    print("  zpp err",abs(complex(zzpp)-zpp[0]),"|zpp|",abs(complex(zzpp)))
    h_em=zpp[0]/z[0]-(zp[0]/z[0])**2
    h_mp=zzpp/zz-(zzp/zz)**2
    print("  h EM",h_em," mp",complex(h_mp))
