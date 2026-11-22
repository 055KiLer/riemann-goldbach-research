import sys, json
sys.path.insert(0,'.')
from experiments2 import make_shifts, run_q, summarize
rng_import=None
sh=make_shifts(12)
out=[]
for q in (4*249989, 8*124991, 9*111109, 4*249943):
    r=run_q(q,sh); s=summarize(r); out.append(s)
    print(f"q={q} phi={s['phi']} phist={s['phist']} RMS={s['rms']:.1f} RMS/sqrtq={s['rms_sqrtq']:.2f} RMS/phist={s['rel_phi']:.4f}",flush=True)
json.dump(out,open('cache/mixed2.json','w'))
