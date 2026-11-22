import json, math, numpy as np, sys
sys.path.insert(0,'.')
from group import factorize
def phi_int(n):
    r=n
    for p in factorize(n): r=r//p*(p-1)
    return r
def load(fn):
    return json.load(open(fn))
def stats(fn, classes):
    R=load(fn); out=[]
    for rec in R:
        q=rec['q']; fam=rec['label']; ph=rec['phi_star']
        for cls in classes:
            rows=[r for r in rec['rows'] if r['cls']==cls]
            if not rows: continue
            arr=np.array([float(r['absR']) for r in rows])
            rms=float(np.sqrt(np.mean(arr**2))); med=float(np.median(arr)); mx=float(arr.max())
            out.append(dict(q=q,family=fam,cls=cls,n=len(rows),rms=rms,median=med,max=mx,
                            rms_sqrtq=rms/math.sqrt(q), med_sqrtq=med/math.sqrt(q), max_sqrtq=mx/math.sqrt(q),
                            phi_star=ph))
    return out
print('===== EXT: 2^e / 3^e, 10 generic shifts (stored under cls=nearpole) =====')
ext=stats('../logs/ramified_ext.json',['nearpole'])
for r in sorted(ext,key=lambda x:(x['family'],x['q'])):
    print(f"q={r['q']:6d} {r['family']:>4} n={r['n']:2d} RMS={r['rms']:10.3f} RMS/√q={r['rms_sqrtq']:7.3f} median/√q={r['med_sqrtq']:6.3f} max/√q={r['max_sqrtq']:7.2f}")
def fit(rows,key):
    x=np.log([r['q'] for r in rows]); y=np.log([r[key] for r in rows])
    A=np.vstack([np.ones_like(x),x]).T; c=np.linalg.lstsq(A,y,rcond=None)[0]
    resid=y-A@c; return float(c[1]),float(np.std(resid)),len(rows)
print()
for fam in ('2^e','3^e'):
    rs=[r for r in ext if r['family']==fam]
    if len(rs)<3:
        print(f"{fam}: only {len(rs)} q points yet"); continue
    a,sd,N=fit(rs,'rms'); print(f"{fam}: alpha=dlogRMS/dlogq = {a:.3f} (scatter {sd:.2f}, N={N}); RMS/√q range {min(r['rms_sqrtq'] for r in rs):.2f}-{max(r['rms_sqrtq'] for r in rs):.2f}")
print('\n===== MIXED EXT: 4p/8p/9p, 10 generic shifts (cls=nearpole) =====')
mix=stats('../logs/ramified_mixed_ext.json',['nearpole'])
for r in sorted(mix,key=lambda x:(x['family'],x['q'])):
    print(f"q={r['q']:6d} {r['family']:>4} n={r['n']:2d} RMS={r['rms']:10.3f} RMS/√q={r['rms_sqrtq']:7.3f} median/√q={r['med_sqrtq']:6.3f} max/√q={r['max_sqrtq']:7.2f}")
for fam in ('4p','8p','9p'):
    rs=[r for r in mix if r['family']==fam]
    if len(rs)>=3:
        a,sd,N=fit(rs,'rms'); print(f"{fam}: alpha={a:.3f} (scatter {sd:.2f}, N={N}); RMS/√q range {min(r['rms_sqrtq'] for r in rs):.2f}-{max(r['rms_sqrtq'] for r in rs):.2f}")
# combined all ramified families: test RMS ~ q^0.5 vs q^1
allr=ext+mix
for name,rs in [('all ramified',allr),('non-mixed (2^e,3^e)',ext)]:
    a,sd,N=fit(rs,'rms'); print(f"{name}: alpha={a:.3f} (scatter {sd:.2f}, N={N})")
json.dump(dict(ext=ext,mixed=mix),open('../logs/final_stats.json','w'),indent=1,default=str)
# validation summary from main json
main=load('../logs/ramified_results.json')
print('\n===== VALIDATION (main run) =====')
for rec in main:
    orth=max(o['err'] for o in rec['orth']); dirs=[e for e in rec['dir_errs'] if e is not None]
    print(f"q={rec['q']:6d} phi*={rec['phi_star']:5d} Me={rec['Me']} orth_err={orth:.1e} dir_L_relerr_max={max(dirs) if dirs else None:.1e} FE_rel={rec['fe_check']:.1e}")
