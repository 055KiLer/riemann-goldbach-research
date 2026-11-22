import sys, os, numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from ratios_lib import gen_shifts, run_q, stats
qset=[211,1009,5003,10007]
for config in ('hyp11','shifted'):
    print(f"===== config={config}",flush=True)
    for eta in (0.1,0.05,0.02,0.01):
        sh=gen_shifts(12,T=2.0,seed=11,config=config,eta=eta)
        print(f" eta={eta}")
        for q in qset:
            res=run_q(q,sh,config,eta)
            st=stats(res)
            print(f"  q={q:>6} RMS={st['rms']:9.2f} RMS/sqrtq={st['rms_over_sqrtq']:7.2f} med={st['med']:8.2f} rel_rms={st['rel_rms']:.3f} |M|rms={st['M_rms']:9.1f}",flush=True)
