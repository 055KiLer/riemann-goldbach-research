import sys,os,time,numpy as np
os.environ['OMP_NUM_THREADS']='4'; os.environ['OPENBLAS_NUM_THREADS']='4'; os.environ['MKL_NUM_THREADS']='4'
from bigp_core import BigPModel
for H,K in [(10.0,32),(10.0,64),(20.0,32)]:
    t0=time.time()
    mod=BigPModel(20011,H=H,m=8,K=K)
    mod.build_C()
    r=mod.result()
    print(f"BIGP H={H} K={K}: lam={r['lam']:.10f} ratio={r['ratio']:.10f} X={r['X']:.4f} time={time.time()-t0:.1f}s",flush=True)
