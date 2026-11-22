import sys,os,time,numpy as np
os.environ['OMP_NUM_THREADS']='4'; os.environ['OPENBLAS_NUM_THREADS']='4'; os.environ['MKL_NUM_THREADS']='4'
from bigp_core import BigPModel
# build fast G and compare with phase2 G at same config
t0=time.time()
mod=BigPModel(20011,H=10.0,m=8,K=32)
G=mod.build_G()
print("fast G",G.shape,"|G|max",np.abs(G).max(),"median",np.median(np.abs(G)),"time",time.time()-t0,flush=True)
sys.path.insert(0,'/home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase2/spectral')
from lmat import Config, build_G
from chars import CharacterGroup
cfg=Config(40022,10.0,m=8); cg=CharacterGroup(40022)
t0=time.time(); Gref,idx_odd,inv=build_G(cfg,cg,verbose=False)
print("ref G",Gref.shape,"|G|max",np.abs(Gref).max(),"time",time.time()-t0,flush=True)
Gref_odd=Gref[:,idx_odd]
print("shapes fast/ref",G.shape,Gref_odd.shape)
if G.shape==Gref_odd.shape:
    d=np.abs(G-Gref_odd)
    print("max diff",d.max(),"rel",d.max()/np.abs(Gref_odd).max())
    # locate worst
    i=np.unravel_index(d.argmax(),d.shape)
    print("worst at",i,"fast",G[i],"ref",Gref_odd[i])
