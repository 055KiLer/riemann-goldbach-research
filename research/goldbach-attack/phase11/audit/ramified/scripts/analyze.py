import sys, json, math, mpmath as mp, numpy as np
sys.path.insert(0,'.')
from group import factorize, Grp
mp.mp.dps=25
R=json.load(open('../logs/ramified_results.json'))
def phi_int(n):
    r=n
    for p in factorize(n): r=r//p*(p-1)
    return r
def mobius(n):
    f=factorize(n)
    if any(e>1 for e in f.values()): return 0
    return (-1)**len(f)
def divisors(n):
    ds=[1]
    for p,e in factorize(n).items():
        ds=[d*p**j for d in ds for j in range(e+1)]
    return sorted(ds)
def defect_coeff(q):
    # sum_{d|q,d<q} mu(q/d) phi(d)  (signed sum); also absolute version
    s=0; sa=0
    for d in divisors(q):
        if d==q: continue
        mu=mobius(q//d)
        s+=mu*phi_int(d); sa+=abs(mu)*phi_int(d)
    return s,sa
out=[]
for rec in R:
    q=rec['q']; fam=rec['label']
    # repeated prime for scaling: for p^e -> p ; 4p/8p -> 2 ; 9p -> 3
    if fam=='2^e': p=2
    elif fam=='3^e': p=3
    elif fam in ('4p','8p'): p=2
    elif fam=='9p': p=3
    else: p=None
    Dsign,Dabs=defect_coeff(q)
    for cls in ('generic','nearpole'):
        rows=[r for r in rec['rows'] if r['cls']==cls]
        if not rows: continue
        arr=np.array([float(r['absR']) for r in rows])
        # signed mean: E in JSON is truncated -> skip (record absR data only)
        Re=None
        rec2=dict(q=q,family=fam,cls=cls,n=len(rows),phi=rec['phi'],phi_star=rec['phi_star'],Me=rec['Me'],
                  repeated_p=p,defect_sign=Dsign,defect_abs=Dabs,
                  median=float(np.median(arr)),rms=float(np.sqrt(np.mean(arr**2))),max=float(arr.max()),
                  mean_abs=None,coh=None,
                  dir_err_max=max([e for e in rec['dir_errs'] if e is not None]) if any(e is not None for e in rec['dir_errs']) else None,
                  fe=rec['fe_check'],
                  orth_max=max(o['err'] for o in rec['orth']))
        for key,val in [('rms_over_sqrtq',rec2['rms']/math.sqrt(q)),
                        ('rms_over_qp',rec2['rms']/(q/p) if p else None),
                        ('rms_over_phiqp',rec2['rms']/phi_int(q//p) if p else None),
                        ('rms_over_defect',rec2['rms']/Dabs if Dabs else None)]:
            rec2[key]=val
        out.append(rec2)
json.dump(out,open('../logs/ramified_summary.json','w'),indent=1)
print(f"{'q':>7} {'fam':>5} {'cls':>8} {'rms':>10} {'rms/√q':>8} {'rms/(q/p)':>10} {'rms/φ(q/p)':>11} {'max/√q':>8} {'coh':>5} {'med/√q':>8}")
for r in sorted(out,key=lambda x:(x['family'],x['q'],x['cls'])):
    print(f"{r['q']:7d} {r['family']:>5} {r['cls']:>8} {r['rms']:10.3f} {r['rms_over_sqrtq']:8.3f} {str(round(r['rms_over_qp'],4) if r['rms_over_qp'] else None):>10} {str(round(r['rms_over_phiqp'],4) if r['rms_over_phiqp'] else None):>11} {r['max']/math.sqrt(r['q']):8.2f} {'-':>5} {r['median']/math.sqrt(r['q']):8.2f}")
# family scaling fits (generic class)
print('\n=== family scaling (generic class, RMS) ===')
for fam in ['2^e','3^e','4p','8p','9p']:
    rs=[r for r in out if r['family']==fam and r['cls']=='generic']
    if len(rs)<3: continue
    lq=np.log([r['q'] for r in rs]); ly=np.log([r['rms'] for r in rs])
    A=np.vstack([np.ones_like(lq),lq]).T; c=np.linalg.lstsq(A,ly,rcond=None)[0]
    print(f"{fam}: alpha=dlogRMS/dlogq={c[1]:.3f}  (q range {rs[0]['q']}-{rs[-1]['q']})")
# global: prime-like nonramified comparison not available here; report 2^e vs q/p expectation
