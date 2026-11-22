import numpy as np, mpmath as mp, time
from math import log as mlog
from lmat import Config, build_G
from chars import CharacterGroup
mp.mp.dps=30
N=30030
cfg=Config(N,1.0)  # small H for speed
cg=CharacterGroup(N)
t0=time.time(); G,idx_odd,inv=build_G(cfg,cg,verbose=False); print("G",G.shape,"time",time.time()-t0)
# pick node: line 0, k=3 -> t=3/16, u=0.5+alpha+i*3/16
Kmax=cfg.Kmax
def node_index(li,k): return li*(2*Kmax+1)+(k+Kmax)
for (li,k) in [(0,3),(1,-2),(0,0)]:
    i=node_index(li,k); u=cfg.sigma_lines[li]+1j*k/cfg.m
    a=cg.units.astype(float); x=a/N
    S=np.array([mp.zeta(mp.mpc(u),mp.mpf(xx)) for xx in x])
    # derivative via mpmath diff per point is too slow; use hurwitz EM derivative validated earlier
    import sys; sys.path.insert(0,'.')
    from hurwitz import HurwitzEM
    em=HurwitzEM(64,24)
    Sa,dSa=em.zeta_array(u,x)
    # direct character sums for 3 random odd chars
    for trial in range(2):
        p = (trial*977+13) % len(idx_odd)
        kflat=idx_odd[p]
        kk=[cg.kvecs[j][kflat] for j in range(len(cg.orders))]
        vals=np.ones(cg.phi,dtype=complex)
        for j,o in enumerate(cg.orders):
            vals *= np.exp(2j*np.pi*(kk[j]*cg.exps[:,j] % o)/o)
        B = vals@S; dB = vals@dSa
        g_direct = dB/B - mlog(N)
        print(f"node (li={li},k={k}) char p={p}: g_direct={g_direct:.12f}  G={G[i,p]:.12f} diff={abs(g_direct-G[i,p]):.2e}  |L|={abs(B)/N**(u.real):.4f}")
