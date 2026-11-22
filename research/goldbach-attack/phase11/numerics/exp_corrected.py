"""Corrected-M experiments: 3^e, mixed ramified, squarefree composites."""
import sys, numpy as np, json, time
sys.path.insert(0,'.')
from fastpipe import Group, make_logtab
from core import compute_E
from corrected import M_correct
rng=np.random.default_rng(999)

def gen_shifts(n,T=2.0):
    out=[]
    while len(out)<n:
        A,B,S,Tt=rng.uniform(-T,T,4)
        if abs(A+B)<0.5: continue
        eta=0.1 if len(out)%2==0 else 0.2
        out.append((float(A),float(B),float(S),float(Tt),float(eta)))
    return out

def run_q(q,sh):
    G=Group(q)
    if G.empty: return None
    logtab=make_logtab(G.x,6)
    ds=[]
    for (A,B,S,T,eta) in sh:
        a=complex(0.5,A); b=complex(0.5,B); s=complex(0.5+eta,S); t=complex(0.5+eta,T)
        E=compute_E(G,a,b,s,t,logtab=logtab); M,_=M_correct(G,a,b,s,t)
        ds.append(E-M)
    ad=np.abs(np.array(ds))
    return dict(q=q,phi=G.phi,phist=G.phist,n=len(sh),
                rms=float(np.sqrt(np.mean(ad**2))),med=float(np.median(ad)),mx=float(ad.max()))

def fit(qs,rs):
    qs=np.array(qs,float); rs=np.array(rs,float)
    A=np.vstack([np.ones_like(qs),np.log(qs)]).T
    sol=np.linalg.lstsq(A,np.log(rs),rcond=None)[0]
    res=np.log(rs)-A@sol; n=len(qs)
    se=np.sqrt(np.sum(res**2)/(n-2)*np.linalg.inv(A.T@A)[1,1]) if n>2 else float('nan')
    return float(sol[1]),float(se)

if __name__=='__main__':
    out={}
    sh40=gen_shifts(40)
    print("== 3^e (corrected M)",flush=True)
    out['three']=[]
    for e in range(7,13):
        q=3**e; r=run_q(q,sh40); out['three'].append(r)
        print(f"q={q:>7} phist={r['phist']:>7} RMS={r['rms']:9.1f} RMS/sqrtq={r['rms']/q**0.5:7.2f} RMS/(q/3)={r['rms']/(q/3):.4f}",flush=True)
    qs=[r['q'] for r in out['three']]; rs=[r['rms'] for r in out['three']]
    print("  3^e alpha =",fit(qs,rs),flush=True); out['alpha_three']=fit(qs,rs)
    print("== 5^e,7^e (corrected M)",flush=True)
    for name,base,es in (('five',5,range(5,9)),('seven',7,range(4,7))):
        out[name]=[]
        for e in es:
            q=base**e; r=run_q(q,sh40); out[name].append(r)
            print(f"q={q:>7} RMS/sqrtq={r['rms']/q**0.5:7.2f} RMS/(q/{base})={r['rms']/(q/base):.4f}",flush=True)
        qs=[r['q'] for r in out[name]]; rs=[r['rms'] for r in out[name]]
        print(f"  {name} alpha =",fit(qs,rs),flush=True); out['alpha_'+name]=fit(qs,rs)
    print("== mixed ramified (corrected M)",flush=True)
    out['mixed']=[]
    for q in (4036,10012,20276,40004,999772,999956,10072,999928,9117,999981):
        r=run_q(q,sh40); out['mixed'].append(r)
        print(f"q={q:>7} phist={r['phist']:>7} RMS={r['rms']:9.1f} RMS/sqrtq={r['rms']/q**0.5:7.2f} RMS/phist={r['rms']/r['phist']:.4f}",flush=True)
    qs=[r['q'] for r in out['mixed']]; rs=[r['rms'] for r in out['mixed']]
    print("  mixed alpha =",fit(qs,rs),flush=True); out['alpha_mixed']=fit(qs,rs)
    print("== squarefree composites (corrected M)",flush=True)
    out['squarefree']=[]
    for q in (15,105,1155,15015,255255,10403,104927,513581,999919,101909,1022117):
        r=run_q(q,sh40); out['squarefree'].append(r)
        print(f"q={q:>8} phist={r['phist']:>7} RMS={r['rms']:9.1f} RMS/sqrtq={r['rms']/q**0.5:7.2f}",flush=True)
    qs=[r['q'] for r in out['squarefree']]; rs=[r['rms'] for r in out['squarefree']]
    print("  squarefree alpha =",fit(qs,rs),flush=True); out['alpha_squarefree']=fit(qs,rs)
    json.dump(out,open('cache/corrected_experiments.json','w'))
    print("saved")
