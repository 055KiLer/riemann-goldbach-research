"""Analysis of truth_runs2.json: alpha(eta), trimmed statistics, local slopes, c_truth."""
import json, os, sys
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__))
J=os.path.join(HERE,'cache','truth_runs2.json')

def load():
    return json.load(open(J))

def arr(rec,key):
    return np.array([complex(*x) for x in rec[key]])

def stat_from_d(d):
    ad=np.abs(d)
    return ad

def fit_slope(qs, ys, boot_idx=None, nboot=0, recs=None):
    """ys per q; boot_idx: for bootstrap resample of shifts: list of index arrays per q? simpler:
       recs: list of per-q per-shift |d| arrays (same shape). Bootstrap resamples shift indices."""
    qs=np.array(qs,float); ys=np.array(ys,float)
    A=np.vstack([np.ones_like(qs),np.log(qs)]).T
    sol=np.linalg.lstsq(A,np.log(ys),rcond=None)[0]
    res=np.log(ys)-A@sol
    n=len(qs); se=np.sqrt(np.sum(res**2)/max(1,n-2)*np.linalg.inv(A.T@A)[1,1])
    out=dict(alpha=float(sol[1]),const=float(sol[0]),se=float(se))
    if nboot and recs is not None:
        nsh=len(recs[0]); boots=[]
        rng=np.random.default_rng(0)
        for _ in range(nboot):
            idx=rng.integers(0,nsh,nsh)
            yy=[np.sqrt(np.mean(recs[k][idx]**2)) for k in range(len(recs))]
            A2=np.vstack([np.ones_like(qs),np.log(qs)]).T
            boots.append(np.linalg.lstsq(A2,np.log(np.array(yy)),rcond=None)[0][1])
        out['se_boot']=float(np.std(boots)); out['boot_mean']=float(np.mean(boots))
    return out

def summarize_block(b):
    qs=[r['q'] for r in b['records']]
    d_abs=[np.abs(arr(r,'d')) for r in b['records']]
    rms=[np.sqrt(np.mean(x**2)) for x in d_abs]
    med=[np.median(x) for x in d_abs]
    trim=[np.sqrt(np.mean(np.sort(x)[:max(1,int(0.9*len(x)))]**2)) for x in d_abs]
    fit_rms=fit_slope(qs,rms,nboot=400,recs=d_abs)
    fit_med=fit_slope(qs,med)
    fit_trim=fit_slope(qs,trim,nboot=400,recs=d_abs)
    # large-q only fits (q>=10007)
    m=np.array(qs)>=10007
    fit_big=fit_slope(np.array(qs)[m],np.array(rms)[m]) if m.sum()>2 else None
    # local slopes between adjacent q (all 6 points -> 5 segments)
    local=[]
    for i in range(len(qs)-1):
        local.append(dict(q0=qs[i],q1=qs[i+1],alpha=float(np.log(rms[i+1]/rms[i])/np.log(qs[i+1]/qs[i]))))
    # per-shift slope distribution (each shift across q)
    nsh=len(d_abs[0]); slopes=[]
    for i in range(nsh):
        y=np.array([d_abs[k][i] for k in range(len(qs))])
        if np.any(y<=0): continue
        A=np.vstack([np.ones_like(np.array(qs)),np.log(np.array(qs,float))]).T
        slopes.append(np.linalg.lstsq(A,np.log(y),rcond=None)[0][1])
    slopes=np.array(slopes)
    return dict(config=b['config'],eta=b['eta'],T=b['T'],qs=qs,rms=rms,med=med,trim=trim,
                rms_over_sqrtq=[r/q**0.5 for r,q in zip(rms,qs)],
                med_over_sqrtq=[m/q**0.5 for m,q in zip(med,qs)],
                fit_rms=fit_rms,fit_med=fit_med,fit_trim=fit_trim,fit_big=fit_big,local=local,
                per_shift=dict(mean=float(np.mean(slopes)),median=float(np.median(slopes)),
                               q10=float(np.quantile(slopes,0.1)),q90=float(np.quantile(slopes,0.9)),
                               frac_above_06=float(np.mean(slopes>0.6))))

if __name__=='__main__':
    d=load()
    res={}
    for k,b in d['blocks'].items():
        s=summarize_block(b); res[k]=s
        print(f"== {k}  (n={b['records'][0]['n']}, T={b['T']})")
        print(f"   alpha_rms={s['fit_rms']['alpha']:.3f} (se={s['fit_rms']['se']:.3f},boot={s['fit_rms'].get('se_boot',0):.3f})"
              f"  alpha_med={s['fit_med']['alpha']:.3f}  alpha_trim90={s['fit_trim']['alpha']:.3f}"
              + (f"  alpha_big(q>=1e4)={s['fit_big']['alpha']:.3f}" if s['fit_big'] else ""))
        print(f"   RMS/sqrtq: "+", ".join(f"{x:.1f}" for x in s['rms_over_sqrtq']))
        print(f"   med/sqrtq: "+", ".join(f"{x:.1f}" for x in s['med_over_sqrtq']))
        print(f"   local slopes: "+", ".join(f"{l['alpha']:.2f}" for l in s['local'])
              +f" | per-shift slope median={s['per_shift']['median']:.2f} mean={s['per_shift']['mean']:.2f} q10={s['per_shift']['q10']:.2f} q90={s['per_shift']['q90']:.2f}")
    json.dump(res,open(os.path.join(HERE,'cache','analysis2.json'),'w'))
    print("\n== c_truth(eta)=(1-alpha)/eta  [rms / med / trim]")
    for k,s in res.items():
        eta=s['eta']
        print(f" {k}: " + ", ".join(f"{name}={(1-s['fit_'+name]['alpha'])/eta:.1f}" for name in ('rms','med','trim')))
    print("\n== T dependence")
    for r in d['T']:
        print(r)
    print("\n== composites")
    for k,recs in d['composite'].items():
        print(k, [(r['q'],round(r['rms']/r['q']**0.5,2)) for r in recs])
