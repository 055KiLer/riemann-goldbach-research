import json, numpy as np
E2=json.load(open('cache/exp2.json'))
E1=json.load(open('cache/exp_results.json'))

def rms_of(rec, idx=None):
    d=np.array([complex(*s['d']) for s in rec['shifts']])
    if idx is not None: d=d[idx]
    return float(np.sqrt(np.mean(np.abs(d)**2)))

def fit_slope(qs, rs, nboot=0, recs=None):
    lq=np.log(qs); lr=np.log(rs)
    A=np.vstack([np.ones_like(lq),lq]).T
    sol=np.linalg.lstsq(A,lr,rcond=None)[0]
    alpha=sol[1]
    # residual std error of slope
    res=lr-A@sol; dof=len(lq)-2
    s2=np.sum(res**2)/max(1,dof); se=np.sqrt(s2*np.linalg.inv(A.T@A)[1,1]) if dof>0 else 0.0
    boot=[]
    if nboot and recs is not None:
        n=len(recs[0]['shifts'])
        for _ in range(nboot):
            idx=np.random.randint(0,n,n)
            bq=[];br=[]
            for rec in recs:
                d=np.array([complex(*s['d']) for s in rec['shifts']])[idx]
                bq.append(rec['q']); br.append(float(np.sqrt(np.mean(np.abs(d)**2))))
            Ab=np.vstack([np.ones_like(bq),np.log(bq)]).T
            boot.append(np.linalg.lstsq(Ab,np.log(br),rcond=None)[0][1])
    return alpha,(np.std(boot) if boot else se)

print("=== PRIMES (60 shifts) ===")
recs=E2['primes60']; qs=np.array([r['q'] for r in recs]); rs=np.array([rms_of(r) for r in recs])
for r,rm in zip(recs,rs):
    s=dict(q=r['q'],phi=r['phi'],rms=rm,rms_sqrtq=rm/r['q']**0.5,rel_phi=rm/r['phist'])
    mn=complex(*r['mean']); s['mean_rms']=abs(mn)/rm
    print(f"q={r['q']:>8} RMS={rm:9.2f} RMS/sqrtq={rm/r['q']**0.5:6.2f} RMS/phist={rm/r['phist']:.4f} |mean|/RMS={abs(mn)/rm:.3f}")
a,ea=fit_slope(qs,rs,nboot=400,recs=recs)
print(f"FIT alpha = {a:.4f} +- {ea:.4f}  (bootstrap); RMS/sqrtq mean={np.mean(rs/qs**0.5):.2f} std={np.std(rs/qs**0.5):.2f}")
# prime-like coefficient assuming alpha=0.5
print(f"RMS/sqrtq values: {np.round(rs/qs**0.5,2)}")

print("\n=== PRIME POWERS: within-family fits ===")
for name,lst in E2['families'].items():
    recs=lst; qs=np.array([r['q'] for r in recs]); rs=np.array([rms_of(r) for r in recs])
    a,ea=fit_slope(qs,rs,nboot=200,recs=recs)
    # fit residual = c*q/p
    p={'two':2,'three':3,'five':5,'seven':7}[name]
    y=rs/(qs/p)
    print(f"family {name}={p}^e: alpha={a:.3f}+-{ea:.3f} (=> RMS~q^{a:.2f}); RMS/(q/p): mean={np.mean(y):.3f} std={np.std(y):.3f}")
    for r,rm in zip(recs,rs):
        print(f"   q={r['q']:>7} p*RMS/q={p*rm/r['q']:.3f} RMS/sqrtq={rm/r['q']**0.5:6.2f} RMS/phist={rm/r['phist']:.4f}")
print("\n=== SQUAREFREE (split: min prime >50 vs small-prime) ===")
sq=E2['squarefree']
def minprime(q):
    n=q; d=2
    while d*d<=n:
        if n%d==0: return d
        d+=1
    return q
big=[];small=[]
for r in sq:
    (big if minprime(r['q'])>50 else small).append(r)
for lbl,lst in (('large-prime',big),('small-prime',small)):
    if not lst: continue
    qs=np.array([r['q'] for r in lst]); rs=np.array([rms_of(r) for r in lst])
    a,ea=fit_slope(qs,rs,nboot=200,recs=lst) if len(qs)>2 else (float('nan'),float('nan'))
    print(f"{lbl}: alpha={a:.3f}+-{ea:.3f}")
    for r,rm in zip(lst,rs):
        print(f"   q={r['q']:>8} minp={minprime(r['q']):>4} RMS={rm:9.2f} RMS/sqrtq={rm/r['q']**0.5:6.2f} RMS/phist={rm/r['phist']:.4f}")
print("\n=== T dependence (q=99961, 25 shifts) ===")
Ts=[];Rs=[]
for r in E2['T']:
    rm=rms_of(r); Ts.append(1.0); Rs.append(rm)
# need T values: stored order 2,5,10,20
Tvals=[2,5,10,20]; Rs=[rms_of(r) for r in E2['T']]
lT=np.log(np.array(Tvals,dtype=float)+1.0); lR=np.log(Rs)
A=np.vstack([np.ones_like(lT),lT]).T
sol=np.linalg.lstsq(A,lR,rcond=None)[0]
res=lR-A@sol; s2=np.sum(res**2)/2; se=np.sqrt(s2*np.linalg.inv(A.T@A)[1,1])
print(f"RMS(T): "+", ".join(f"T={t}:{rm:.0f}" for t,rm in zip(Tvals,Rs)))
print(f"fit RMS ~ (1+T)^B: B={sol[1]:.3f}+-{se:.3f}  (exponential would be huge)")
print("\n=== holomorphy / near-pole (from exp1) ===")
for rec in E1['holo']['records']: print(f"Re a off={rec['off']:+.4f}: RMS={rec['rms']:.1f}")
for rec in E1['pole']['records']: print(f"delta={rec['delta']}: RMS={rec['rms']:.1f} |M|={rec['Mabs']:.0f}")
print("\n=== 20-shift composites sanity (exp1) ===")
for r in E1['composites']:
    rm=rms_of(r); print(f"q={r['q']:>7} phi={r['phi']:>7} RMS/sqrtq={rm/r['q']**0.5:6.2f} RMS/phist={rm/r['phist']:.4f}")
