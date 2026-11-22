import sys,time
sys.path.insert(0,'.')
from farN_core import FarModel
tests=[
 # (p, H, m, K, known_lam)
 (20011, 10.0, 8, 8, 0.2678331),
 (20011, 10.0, 8, 64, 0.2678331),
 (500083, 10.0, 8, 8, 0.05587077),
]
for p,H,m,K,known in tests:
    t0=time.time()
    mod=FarModel(p,H=H,m=m,K=K,verbose=False); mod.build_C(); r=mod.result()
    print(f"TEST p={p} H={H} m={m} K={K}: lam={r['lam']:.10f} ratio={r['ratio']:.8f} known={known:.10f} reldiff={abs(r['lam']-known)/known:.2e} wall={time.time()-t0:.1f}s",flush=True)
