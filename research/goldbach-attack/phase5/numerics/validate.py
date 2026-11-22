import sys,os,time,numpy as np
sys.path.insert(0,'.')
from bigp_core import BigPModel
os.environ['EIG']='eigsh'
sys.path.insert(0,'/home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase2/spectral')
import model as MOD2
# reference from phase2 pipeline
for H in [10.0,20.0]:
    res=MOD2.build_model(N=40022,H=H,m=8)
    ev=np.asarray(res['ev']); lam=np.abs(ev).max()
    print(f"PHASE2 REF H={H} m=8: lam={lam:.10f} ratio={lam/res['delta']:.10f}",flush=True)
for H,K in [(10.0,32),(10.0,64),(20.0,32),(20.0,64)]:
    t0=time.time()
    mod=BigPModel(20011,H=H,m=8,K=K)
    mod.build_C()
    r=mod.result()
    print(f"BIGP H={H} K={K}: lam={r['lam']:.10f} ratio={r['ratio']:.10f} X={r['X']:.4f} time={time.time()-t0:.1f}s",flush=True)
