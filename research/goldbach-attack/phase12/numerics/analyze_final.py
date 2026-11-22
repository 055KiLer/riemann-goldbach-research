import json, math, numpy as np
from collections import defaultdict

def load(fn,keys=('q','X','model','eta','Wabs')):
    D=json.load(open(fn)); out=[]
    if isinstance(D,dict): D=[D]
    for r in D:
        if keys[4] not in r: continue
        out.append(r)
    return out

sets=[]
for fn in ['logs_wrap_avg.json','logs_wrap_a2.json','logs_wrap_a2big.json']:
    try: sets+=load(fn)
    except FileNotFoundError: pass
G=defaultdict(list)
for r in sets: G[(r['q'],r['X'],r['model'],r['eta'])].append(r)
rows=[]
for k,rs in sorted(G.items()):
    q,X,model,eta=k
    w=np.array([r['Wabs'] for r in rs]); m=float(np.mean(w)); A=math.log(X)/math.log(q)
    rows.append(dict(q=q,X=X,A=A,model=model,eta=eta,N=len(rs),mean=m,rms=float(np.sqrt(np.mean(w**2)))))
# print table
print(f"{'q':>6} {'X':>6} {'A':>5} {'model':>4} {'eta':>4} {'N':>2} {'mean|W|':>10} {'W/(X²/q)':>10} {'rho=W/q^(1-etaA)':>16}")
for r in sorted(rows,key=lambda r:(r['model'],r['eta'],r['q'],r['A'])):
    rho=r['mean']/r['q']**(1-r['eta']*r['A'])
    print(f"{r['q']:6d} {r['X']:6d} {r['A']:5.2f} {r['model']:>4} {r['eta']:4.2f} {r['N']:2d} {r['mean']:10.4g} {r['mean']/(r['X']**2/r['q']):10.3g} {rho:16.3g}")
def fit(rs):
    X=np.array([math.log(r['X']) for r in rs]); Q=np.array([math.log(r['q']) for r in rs])
    Y=np.array([math.log(r['mean']) for r in rs])
    M=np.vstack([np.ones_like(X),X,Q]).T
    c=np.linalg.lstsq(M,Y,rcond=None)[0]; res=Y-M@c
    return float(c[0]),float(c[1]),float(c[2]),float(np.std(res)),len(rs)
print('\n=== fits lnW = c0 + beta lnX + gamma lnq ===')
fits={}
for model in ['crit','rat']:
    for eta in [0.05,0.02]:
        rs=[r for r in rows if r['model']==model and abs(r['eta']-eta)<1e-9]
        if len(rs)>=5:
            c0,b,g,sd,N=fit(rs); fits[(model,eta)]=(c0,b,g,sd)
            print(f"{model} eta={eta}: c0={c0:+.3f} beta={b:.3f} gamma={g:.3f} rms={sd:.3f} N={N}")
rs=[r for r in rows]
c0,b,g,sd,N=fit(rs); print(f"ALL: c0={c0:+.3f} beta={b:.3f} gamma={g:.3f} rms={sd:.3f} N={N}")
print('\n=== c>2 feasibility: A_max = (1-gamma-log_q C0)/(beta+eta), C0=e^c0 ===')
for (model,eta),(c0,b,gg,sd) in sorted(fits.items()):
    for q in [101,1009,10007]:
        logq=math.log(q); C0=math.exp(c0)
        A_max=(1-gg-math.log(C0)/logq)/(b+eta)
        # uncertainty band via rms
        lo=(1-gg-(math.log(C0)+sd)/logq)/(b+eta); hi=(1-gg-(math.log(C0)-sd)/logq)/(b+eta)
        print(f"{model} eta={eta:.2f} q={q:5d}: A_max={A_max:.2f} (c-band {lo:.2f}..{hi:.2f})  c_max(=ω/η at A_max)={A_max:.2f}")
    print()
json.dump(rows,open('logs_final_rows.json','w'),indent=1)
