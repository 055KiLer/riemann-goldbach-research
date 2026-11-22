"""Supplementary: large-q lever arm (up to 1e6) for small eta, per-shift storage."""
import sys, os, json, time
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from ratios_lib import gen_shifts, run_q
QS=[100003,500009,1000003]
OUT=os.path.join(HERE,'cache','truth_runs3.json')
if __name__=='__main__':
    out={'primes':QS,'blocks':{}}
    for config in ('hyp11','shifted'):
        for eta in (0.02,0.01,0.005,0.002):
            key=f'{config}_eta{eta}'
            print(f"== {config} eta={eta} q={QS}",flush=True)
            sh=gen_shifts(20,T=2.0,seed=20241122,config=config,eta=eta)
            recs=[]
            for q in QS:
                t0=time.time(); res=run_q(q,sh,config,eta)
                d=res['d']
                recs.append(dict(q=q,phist=res['phist'],n=20,secs=time.time()-t0,
                                 d=[[z.real,z.imag] for z in d],
                                 E=[[z.real,z.imag] for z in res['E']],
                                 M=[[z.real,z.imag] for z in res['M']]))
                ad=np.abs(d)
                print(f"  q={q:>8} RMS/√q={np.sqrt(np.mean(ad**2))/q**0.5:8.2f} med/√q={np.median(ad)/q**0.5:8.2f} rel={np.sqrt(np.mean((ad/np.maximum(np.abs(res['M']),1e-300))**2)):.3f} ({recs[-1]['secs']:.1f}s)",flush=True)
            out['blocks'][key]=dict(config=config,eta=eta,T=2.0,shifts=[list(x) for x in sh],records=recs)
            json.dump(out,open(OUT,'w'))
    print("saved")
