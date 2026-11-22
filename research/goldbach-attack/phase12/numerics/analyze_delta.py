import json, math, numpy as np
from collections import defaultdict
D=json.load(open('logs_delta.json'))
G=defaultdict(list)
for r in D: G[(r['q'],r['X1'],r['X2'],r['model'],r['eta'])].append(r)
rows=[]
for k,rs in sorted(G.items()):
    q,N,M,model,eta=k
    dl=np.array([r['absDelta_lead'] for r in rs]); de=np.array([r['absDelta'] for r in rs])
    qW=np.array([r['qW'] for r in rs]); SS=np.array([r['ScSd'] for r in rs]); hs=np.array([r['hsum_abs']/q for r in rs])
    rows.append(dict(q=q,N=N,M=M,Y=N*M,A=0.5*math.log(N*M)/math.log(q),model=model,eta=eta,n=len(rs),
                     Delta=float(np.mean(dl)),Dmax=float(np.max(dl)),DeltaE=float(np.mean(de)),
                     qW=float(np.mean(qW)),ScSd=float(np.mean(SS)),hsum=float(np.mean(hs)),
                     cancel=float(np.mean(dl/(qW+SS+1e-300)))))
sq=[r for r in rows if r['N']==r['M']]; asym=[r for r in rows if r['N']!=r['M']]
print('=== combined dataset (mean over shift sets; |Δ_lead|=|(q−1)W−ScSd+T|) ===')
print(f"{'q':>6} {'X':>6} {'A':>5} {'model':>4} {'eta':>4} {'mean|Δ|':>9} {'max|Δ|':>9} {'|qW|':>10} {'|ScSd|':>10} {'cancel':>7} {'rho(max)':>8}")
for r in sorted(sq,key=lambda r:(r['model'],r['eta'],r['q'],r['A'])):
    t=r['q']**(1-r['eta']*r['A'])
    print(f"{r['q']:6d} {r['N']:6d} {r['A']:5.2f} {r['model']:>4} {r['eta']:4.2f} {r['Delta']:9.4g} {r['Dmax']:9.4g} {r['qW']:10.4g} {r['ScSd']:10.4g} {r['cancel']:7.3f} {r['Dmax']/t:8.3f}")
def fit(rs,key='Delta'):
    rs=[r for r in rs if r[key]>0]
    X=np.log([r['N'] for r in rs]); Q=np.log([r['q'] for r in rs]); Y=np.log([r[key] for r in rs])
    M=np.vstack([np.ones_like(X),X,Q]).T
    c=np.linalg.lstsq(M,Y,rcond=None)[0]; res=Y-M@c
    return float(c[0]),float(c[1]),float(c[2]),float(np.std(res)),len(rs)
print('\n=== fits ln Δ = c0 + beta lnX + gamma lnq ===')
fits={}
for model in ['crit','rat']:
    for eta in [0.05,0.1,0.2]:
        rs=[r for r in sq if r['model']==model and abs(r['eta']-eta)<1e-9]
        if len(rs)>=6:
            c0,b,g,sd,N=fit(rs); fits[(model,eta)]=(c0,b,g,sd)
            print(f"{model} eta={eta}: c0={c0:+.3f} beta={b:.3f} gamma={g:.3f} rms={sd:.2f} N={N}")
c0,b,g,sd,N=fit(sq); print(f"ALL: c0={c0:+.3f} beta={b:.3f} gamma={g:.3f} rms={sd:.2f} N={N}")
print('\n=== c_max from fit: A satisfies beta*A+gamma+log_q C0 = 1-eta*A ===')
for (model,eta),(c0,b,g,sd) in sorted(fits.items()):
    vals=[]
    for q in [101,1009,10007]:
        lq=math.log(q); C0=math.exp(c0)
        A=(1-g-math.log(C0)/lq)/(b+eta)
        lo=(1-g-(math.log(C0)+sd)/lq)/(b+eta); hi=(1-g-(math.log(C0)-sd)/lq)/(b+eta)
        vals.append(f"q={q}:c={A:.2f}[{lo:.2f},{hi:.2f}]")
    print(f"{model} eta={eta:.2f}: "+"  ".join(vals))
print('\n=== h-decomposition scale (|sum_{h!=0} C D|/q) vs Delta ===')
for model in ['crit','rat']:
    rs=[r for r in sq if r['model']==model and abs(r['eta']-0.05)<1e-9]
    for r in sorted(rs,key=lambda r:(r['q'],r['A']))[:8]:
        print(f"q={r['q']:6d} A={r['A']:.2f} {model}: |Δ|={r['Delta']:.4g} |hsum|/q={r['hsum']:.4g} qW={r['qW']:.4g}")
print('\n=== asymmetric vs square (q=101) ===')
for r in sorted(asym,key=lambda r:(r['A'],r['model'],r['eta'])):
    print(f"N={r['N']:5d} M={r['M']:5d} A={r['A']:.2f} {r['model']} eta={r['eta']:.2f}: mean|Δ|={r['Delta']:.4g} max={r['Dmax']:.4g} cancel={r['cancel']:.3f}")
print('\n=== direct empirical rho=Δ/q^(1-eta*A) for rat model (primary for RAT(c)) ===')
for eta in [0.05,0.1,0.2]:
    rs=[r for r in sq if r['model']=='rat' and abs(r['eta']-eta)<1e-9]
    for r in sorted(rs,key=lambda r:(r['q'],r['A'])):
        t=r['q']**(1-r['eta']*r['A'])
        print(f"eta={eta}: q={r['q']:6d} A={r['A']:.2f}: mean rho={r['Delta']/t:.3f} max rho={r['Dmax']/t:.3f}")
json.dump(rows,open('logs_delta_summary2.json','w'),indent=1)
