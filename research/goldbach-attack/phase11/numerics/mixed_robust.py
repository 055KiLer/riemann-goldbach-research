import sys, json, numpy as np
sys.path.insert(0,'.')
from experiments2 import make_shifts, run_q
sh=make_shifts(20)
out=[]
for q in (4036,999956,10072,999928,9117,999981):
    r=run_q(q,sh)
    d=np.array([complex(*s['d']) for s in r['shifts']]); ad=np.abs(d)
    stat=dict(q=q,phist=r['phist'],rms=float(np.sqrt(np.mean(ad**2))),med=float(np.median(ad)),
              q90=float(np.quantile(ad,0.9)))
    out.append(stat)
    print(f"q={q:>7} phist={r['phist']:>7} med={stat['med']:9.1f} med/sqrtq={stat['med']/q**0.5:6.2f} med/phist={stat['med']/r['phist']:.4f} rms/sqrtq={stat['rms']/q**0.5:6.2f}",flush=True)
json.dump(out,open('cache/mixed_robust.json','w'))
