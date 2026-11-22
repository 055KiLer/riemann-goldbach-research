"""Extra primes for scaling fit (same shift sets, eta=0.1 only)."""
import sys, json, mpmath as mp, numpy as np, math
sys.path.insert(0,'.')
import replicate as R
mp.mp.dps=30
shiftsets=[(0.7,1.3,0.4,2.1),(2.6,-1.1,1.7,0.3),(-2.4,0.9,2.2,1.5)]
qs=[3001,4001]
allout=[]
for q in qs:
    es=[(0.1,ss) for ss in shiftsets]
    res=R.run_case(q,es); allout.append(res)
    ratios=[r['ratio'] for r in res['rows'] if r.get('ok')]
    print(f"q={q} phi={res['phi']} phi*={res['phistar']} median={np.median(ratios)} max={max(ratios)} time={res['t']:.1f}",flush=True)
json.dump(allout,open('../logs/A_extra.json','w'),indent=1)
