import os,sys,time,math
os.environ['EIG']='eigsh'
sys.path.insert(0,'/home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase2/spectral')
import numpy as np
import model as MOD
from lmat import Config as OrigConfig
N=40022; logN=math.log(N); out=open('c_quick.log','w')
def run(c,H=8,m=8):
    def patched(N_,H_,m=8,K=64,J=24):
        cfg=OrigConfig(N_,H_,m=m,K=K,J=J); cfg.alpha=c/math.log(N_)
        cfg.sigma_lines=np.array([0.5+cfg.alpha,0.5+cfg.beta]); return cfg
    MOD.Config=patched
    t0=time.time(); res=MOD.build_model(N=N,H=H,m=m,verbose=False)
    ev=np.asarray(res['ev']); lam=float(np.abs(ev).max()); delta=float(res['delta'])
    s=f"c={c:5.2f} alpha={c/logN:.6f} H={H} m={m} lam={lam:.6f} delta={delta:.6f} ratio={lam/delta:.5f} time={time.time()-t0:.0f}s"
    print(s,flush=True); out.write(s+"\n"); out.flush(); return lam/delta
for c in [0.5,0.75,1.0,1.05]:
    try: run(c)
    except Exception as e: print("FAIL",c,type(e).__name__,e,flush=True)
out.write("DONE\n"); out.close()
