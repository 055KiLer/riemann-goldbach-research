import sys, numpy as np, time
sys.path.insert(0,'.')
from farN_core import FarModel
from lmat import Config, build_G
from chars import CharacterGroup
p=20011; N=2*p; H=10.0; m=8
# farN row
mod=FarModel(p,H=H,m=m,K=8,verbose=False)
t0=time.time()
row_far=mod._g_row(complex(0.5+mod.alpha, 0.0))
print("far row time",time.time()-t0,"|row|max",np.abs(row_far).max(),flush=True)
# phase2 G
cfg=Config(N,H,m=m); cg=CharacterGroup(N)
t0=time.time(); G,idx_odd,inv=build_G(cfg,cg,verbose=True)
print("phase2 G time",time.time()-t0, G.shape, flush=True)
row_ref=G[0,:]
print("ref |row|max",np.abs(row_ref).max())
d=np.abs(row_far-row_ref)
print("max abs diff",d.max(),"rel",d.max()/np.abs(row_ref).max())
i=np.argmax(d); print("worst i",i,"far",row_far[i],"ref",row_ref[i])
# also compare at t=1 node (row index Kmax+1 for line 0)
row_far2=mod._g_row(complex(0.5+mod.alpha,1.0))
row_ref2=G[cfg.Kmax+1,:]
print("t=1 max diff",np.abs(row_far2-row_ref2).max(),"rel",np.abs(row_far2-row_ref2).max()/np.abs(row_ref2).max())
