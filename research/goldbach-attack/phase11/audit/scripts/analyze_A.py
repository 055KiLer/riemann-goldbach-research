import json, math, numpy as np, mpmath as mp
mp.mp.dps=25
def _isprime(n):
    if n<2: return False
    for p in [2,3,5,7,11,13,17,19,23,29,31,37]:
        if n%p==0: return n==p
    d=n-1; s=0
    while d%2==0: s+=1; d//=2
    for a in [2,3,5,7,11,13,17,19,23,29,31,37]:
        x=pow(a,d,n)
        if x in (1,n-1): continue
        for _ in range(s-1):
            x=x*x%n
            if x==n-1: break
        else: return False
    return True

A=json.load(open('../logs/A_results.json'))
def parse(c): return mp.mpc(c)
rows=[]
for res in A:
    q=res['q']; phi=res['phi']; ph=res['phistar']
    rec=dict(q=q,phi=phi,phi_star=ph,type=('vacuous' if ph==0 else ('prime' if _isprime(q) else 'composite')),
             four=(q%4==0))
    ratios=[]; rels=[]; Rs={}; 
    for r in res['rows']:
        if not r.get('ok'): continue
        R=parse(r['E'])-parse(r['M']); ratios.append(float(abs(R)/math.sqrt(q))); rels.append(r['rel'])
        Rs.setdefault(r['eta'],[]).append(R)
    rec['n']=len(ratios); rec['median_ratio']=float(np.median(ratios)) if ratios else 0.0
    rec['max_ratio']=float(max(ratios)) if ratios else 0.0
    rec['median_rel']=float(np.median([x for x in rels if x is not None])) if rels else None
    # signed mean per eta (only where 3 shift sets)
    means={}
    for eta,arr in Rs.items():
        m=sum(arr)/len(arr); means[str(eta)]=float(abs(m)/math.sqrt(q))
    rec['mean_ratio']=means
    rec['mean_ratio_max']=max(means.values()) if means else None
    # eta=0.1 subset (comparable to extras)
    r01=[float(abs(parse(r['E'])-parse(r['M']))/math.sqrt(q)) for r in res['rows'] if r.get('ok') and abs(r['eta']-0.1)<1e-9]
    rec['median_ratio_eta01']=float(np.median(r01)) if r01 else None
    rows.append(rec)
# redo type with defined function
for r in rows: r['type']=('vacuous' if r['phi_star']==0 else ('prime' if _isprime(r['q']) else 'composite'))
print(f"{'q':>5} {'phi*':>5} {'type':>9} {'4|q':>3} {'med_R/sqrtq':>11} {'max':>8} {'med_rel':>8} {'mean/√q(max over η)':>18} {'eta01_med':>9}")
for r in sorted(rows,key=lambda x:x['q']):
    print(f"{r['q']:5d} {r['phi_star']:5d} {r['type']:>9} {str(r['four']):>3} {r['median_ratio']:11.3f} {r['max_ratio']:8.2f} {str(round(r['median_rel'],3) if r['median_rel'] is not None else None):>8} {str(round(r['mean_ratio_max'],3) if r['mean_ratio_max'] is not None else None):>18} {str(round(r['median_ratio_eta01'],3) if r['median_ratio_eta01'] else None):>9}")
# scaling: log-log fit ratio vs q for primes / all / composites
def fit(rs,key='median_ratio'):
    xs=np.log([r['q'] for r in rs]); ys=np.log([r[key] for r in rs])
    A=np.vstack([np.ones_like(xs),xs]).T; c=np.linalg.lstsq(A,ys,rcond=None)[0]
    resid=ys-A@c; return float(c[1]), float(np.std(resid)), len(rs)
for name,rs in [('all',[r for r in rows if r['median_ratio']>0]),('prime',[r for r in rows if r['type']=='prime']),('composite',[r for r in rows if r['type']=='composite'])]:
    print(name,'loglog slope of median R/√q vs q:',fit(rs))
# correlation with phi*
import scipy.stats as st
allr=[r for r in rows if r['median_ratio']>0]
print('corr log ratio vs log q',st.pearsonr(np.log([r['q'] for r in allr]),np.log([r['median_ratio'] for r in allr])))
print('corr log ratio vs log phi*',st.pearsonr(np.log([r['phi_star'] for r in allr]),np.log([r['median_ratio'] for r in allr])))
json.dump(rows,open('../logs/A_summary.json','w'),indent=1,default=str)
