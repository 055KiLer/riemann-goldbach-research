import sys, json, numpy as np
sys.path.insert(0,'.')
from experiments2 import make_shifts, run_q, summarize
rng=np.random.default_rng(4242)
sh=make_shifts(20)
out=[]
for q in (4036,10012,10072,9117,20276,40004):
    r=run_q(q,sh); s=summarize(r); out.append(s)
    print(f"q={q} phi={s['phi']} phist={s['phist']} RMS={s['rms']:.1f} RMS/sqrtq={s['rms_sqrtq']:.2f} RMS/phist={s['rel_phi']:.4f}",flush=True)
json.dump(out,open('cache/ramified_mixed.json','w'))
