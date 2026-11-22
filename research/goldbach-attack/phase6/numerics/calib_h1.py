import sys,time,json
sys.path.insert(0,'.')
from farN_core import FarModel
def run(p,H,m,K=4):
    t0=time.time(); mod=FarModel(p,H=H,m=m,K=K,verbose=False); mod.build_C(); r=mod.result()
    print(f"CAL p={p} N={2*p} H={H} m={m} K={K}: lam={r['lam']:.8f} ratio={r['ratio']:.8f} C={r['C']:.5f} |C|max={r['Cmax']:.3e} wall={time.time()-t0:.1f}s",flush=True)
    rec={k:(float(v) if isinstance(v,(int,float)) else v) for k,v in r.items()}
    with open('cache/calibration.jsonl','a') as f: f.write(json.dumps(rec)+'\n')
for p,H,m in [(500083,1.0,8),(500083,2.0,8)]:
    run(p,H,m)
