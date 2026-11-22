"""Phase-12 task-53 (run 2): per-shift storage, larger q lever arm, smaller eta.

Blocks: hyp11 (Hyp 1.1: Re a=Re b=1/2, Re s=Re t=1/2+eta) and shifted (all four Re=1/2+eta).
q primes: 211, 1009, 10007, 100003, 300007, 500009  (2.7 decades).
"""
import sys, os, json, time
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from ratios_lib import gen_shifts, run_q

PRIMES=[211,1009,10007,100003,300007,500009]
OUT=os.path.join(HERE,'cache'); os.makedirs(OUT,exist_ok=True)
J=os.path.join(OUT,'truth_runs2.json')

def block(config,eta,ns=30,T=2.0,seed=2024,min_ab=0.5):
    sh=gen_shifts(ns,T=T,seed=seed,config=config,eta=eta)
    recs=[]
    for q in PRIMES:
        t0=time.time(); res=run_q(q,sh,config,eta)
        d=res['d']; E=res['E']; M=res['M']
        rec=dict(q=q,phist=res['phist'],n=ns,secs=time.time()-t0,
                 d=[(x.real,x.imag) for x in d], E=[(x.real,x.imag) for x in E],
                 M=[(x.real,x.imag) for x in M])
        recs.append(rec)
        ad=np.abs(d)
        print(f"  [{config} eta={eta} T={T}] q={q:>7} RMS={np.sqrt(np.mean(ad**2)):11.2f} RMS/sqrtq={np.sqrt(np.mean(ad**2))/q**0.5:8.2f} med={np.median(ad):10.2f} ({rec['secs']:.1f}s)",flush=True)
    return dict(config=config,eta=eta,T=T,shifts=[list(x) for x in sh],records=recs)

if __name__=='__main__':
    out={'primes':PRIMES,'blocks':{},'T':[],'composite':{}}
    for config,etas in (('hyp11',(0.1,0.05,0.02,0.01,0.005,0.002)),
                        ('shifted',(0.1,0.05,0.02,0.01,0.005,0.002))):
        for eta in etas:
            key=f'{config}_eta{eta}'
            print(f"== {config} eta={eta}",flush=True)
            out['blocks'][key]=block(config,eta)
            json.dump(out,open(J,'w'))
    # T dependence with per-shift data (hyp11 eta=0.05, q=10007,30011)
    print("== T dependence (hyp11 eta=0.05)",flush=True)
    for q in (10007,30011):
        for T in (2.0,10.0,30.0,50.0):
            sh=gen_shifts(20,T=T,seed=777,config='hyp11',eta=0.05)
            res=run_q(q,sh,'hyp11',0.05)
            d=res['d']
            out['T'].append(dict(q=q,T=T,rms=float(np.sqrt(np.mean(np.abs(d)**2))),
                                 med=float(np.median(np.abs(d))),
                                 d=[[z.real,z.imag] for z in d]))
            print(f"  q={q} T={T:>4} RMS={out['T'][-1]['rms']:10.1f} med={out['T'][-1]['med']:9.1f}",flush=True)
    json.dump(out,open(J,'w'))
    # composite q with corrected mask
    print("== composite q (hyp11, T=2)",flush=True)
    for eta in (0.05,0.02,0.01):
        recs=[]
        for q in (1024,2187,4096,6561,16384,32768):
            sh=gen_shifts(24,T=2.0,seed=909,config='hyp11',eta=eta)
            res=run_q(q,sh,'hyp11',eta)
            d=np.abs(res['d'])
            recs.append(dict(q=q,phist=res['phist'],rms=float(np.sqrt(np.mean(d**2))),
                             med=float(np.median(d)),rel_rms=float(np.sqrt(np.mean((d/np.maximum(np.abs(res['M']),1e-300))**2)))))
            print(f"  eta={eta} q={q:>6} RMS/sqrtq={recs[-1]['rms']/q**0.5:8.3f} med/sqrtq={recs[-1]['med']/q**0.5:8.3f}",flush=True)
        out['composite'][f'hyp11_eta{eta}']=recs
        json.dump(out,open(J,'w'))
    print("saved",J)
