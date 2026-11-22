"""Read-only audit: finite-model ratio at N=40022 for variable strip alpha=c/logN (LL Appendix A).
Monkeypatches model.Config; does NOT modify phase2 files. Run with PYTHONDONTWRITEBYTECODE=1."""
import os, sys, time, math
os.environ['EIG']='eigsh'
sys.path.insert(0,'/home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase2/spectral')
import numpy as np
import model as MOD
from lmat import Config as OrigConfig
import lmat as LM

N=40022
logN=math.log(N)
orig_cfg=OrigConfig

def run(c,H=20,m=16):
    def patched(N_,H_,m=16,K=64,J=24):
        cfg=orig_cfg(N_,H_,m=m,K=K,J=J)
        cfg.alpha=c*math.log(N_)**-1 * (math.log(N_) / math.log(N_))  # c/log N_
        cfg.alpha=c/math.log(N_)
        cfg.sigma_lines=np.array([0.5+cfg.alpha,0.5+cfg.beta])
        return cfg
    MOD.Config=patched
    t0=time.time()
    res=MOD.build_model(N=N,H=H,m=m,verbose=False)
    ev=np.asarray(res['ev']); lam=float(np.abs(ev).max()); delta=float(res['delta'])
    print(f"c={c:5.2f} alpha={c/logN:.6f} H={H} lam={lam:.6f} delta={delta:.6f} ratio={lam/delta:.5f} time={time.time()-t0:.0f}s",flush=True)
    return lam/delta

if __name__=='__main__':
    out=[]
    for c in [0.5,0.75,1.0,1.05]:
        try:
            r=run(c)
            out.append((c,r))
        except Exception as e:
            print("FAILED c=",c,type(e).__name__,e,flush=True)
    print("SUMMARY",out)
