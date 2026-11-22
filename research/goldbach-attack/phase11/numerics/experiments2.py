import sys, time, json, numpy as np
sys.path.insert(0,'.')
from fastpipe import Group, make_logtab
from core import compute_E, compute_M, K_for
rng=np.random.default_rng(777)

def make_shifts(n,T=2.0,minAplusB=0.5):
    out=[]
    while len(out)<n:
        A,B,S,Tt=rng.uniform(-T,T,4)
        if abs(A+B)<minAplusB: continue
        eta=0.1 if len(out)%2==0 else 0.2
        out.append((float(A),float(B),float(S),float(Tt),float(eta)))
    return out

def run_q(q, shifts, Kmin=6):
    G=Group(q)
    if G.empty: return None
    Kmax=max(K_for(complex(0.5+eta,T),Kmin) for (A,B,S,T,eta) in shifts)
    logtab=make_logtab(G.x,Kmax); cache={}
    res=[]
    for (A,B,S,Tt,eta) in shifts:
        a=complex(0.5,A); b=complex(0.5,B); s=complex(0.5+eta,S); t=complex(0.5+eta,Tt)
        E=compute_E(G,a,b,s,t,logtab=logtab); M=compute_M(G,a,b,s,t,cache)
        res.append(dict(sh=[A,B,S,Tt,eta],E=[E.real,E.imag],M=[M.real,M.imag],d=[(E-M).real,(E-M).imag]))
    d=np.array([complex(*r['d']) for r in res])
    return dict(q=q,phi=G.phi,phist=G.phist,M0=G.M0,M1=G.M1,n=len(shifts),K=Kmax,
                rms=float(np.sqrt(np.mean(np.abs(d)**2))), absmean=float(np.mean(np.abs(d))),
                mean=[float(np.mean(d.real)),float(np.mean(d.imag))], max=float(np.max(np.abs(d))),
                shifts=res)

def summarize(rec):
    d=np.array([complex(*s['d']) for s in rec['shifts']]); E=np.array([complex(*s['E']) for s in rec['shifts']]); M=np.array([complex(*s['M']) for s in rec['shifts']])
    ad=np.abs(d)
    return dict(q=rec['q'],phi=rec['phi'],phist=rec['phist'],n=rec['n'],
                rms=float(np.sqrt(np.mean(ad**2))),med=float(np.median(ad)),q90=float(np.quantile(ad,0.9)),
                rms_sqrtq=float(np.sqrt(np.mean(ad**2))/rec['q']**0.5),
                rel_phi=float(np.sqrt(np.mean(ad**2))/rec['phist']),
                mean_abs=float(abs(complex(*rec['mean']))), rms_over_mean=float(abs(complex(*rec['mean']))/np.sqrt(np.mean(ad**2))),
                E_rms=float(np.sqrt(np.mean(np.abs(E)**2))), M_rms=float(np.sqrt(np.mean(np.abs(M)**2))))

if __name__=='__main__':
    out={}
    NS=60
    shifts=make_shifts(NS)
    print("== primes 60 shifts",flush=True)
    out['primes60']=[]
    for q in [1009,3001,10093,29989,99961,199921,400753,700001,1002241]:
        r=run_q(q,shifts); out['primes60'].append(r)
        s=summarize(r); print(f"q={q} rms={s['rms']:.1f} rms/sqrtq={s['rms_sqrtq']:.2f} rel_phi={s['rel_phi']:.4f} mean/rms={s['rms_over_mean']:.3f}",flush=True)
        json.dump(out,open('cache/exp2.json','w'))
    print("== prime power families",flush=True)
    out['families']={}
    sh40=make_shifts(40)
    fams=dict(
        two=[2**e for e in range(10,20)],
        three=[3**e for e in range(7,13)],
        five=[5**e for e in range(5,9)],
        seven=[7**e for e in range(4,7)],
    )
    for name,lst in fams.items():
        out['families'][name]=[]
        for q in lst:
            r=run_q(q,sh40); out['families'][name].append(r)
            s=summarize(r); print(f"  {name} q={q} phi={s['phi']} rms={s['rms']:.1f} rms/sqrtq={s['rms_sqrtq']:.2f} rel_phi={s['rel_phi']:.4f}",flush=True)
            json.dump(out,open('cache/exp2.json','w'))
    print("== squarefree mixed",flush=True)
    out['squarefree']=[]
    sq=[15,105,1155,15015,255255,101*103,317*331,509*1009,991*1009,101*1009,29*1009,1009*1013]
    for q in sq:
        r=run_q(q,sh40); out['squarefree'].append(r)
        s=summarize(r); print(f"  q={q} phi={s['phi']} phist={s['phist']} rms={s['rms']:.1f} rms/sqrtq={s['rms_sqrtq']:.2f} rel_phi={s['rel_phi']:.4f}",flush=True)
        json.dump(out,open('cache/exp2.json','w'))
    print("== T dependence 25 shifts",flush=True)
    out['T']=[]
    for T in (2,5,10,20):
        sh=make_shifts(25,T=T)
        r=run_q(99961,sh); out['T'].append(r)
        s=summarize(r); print(f"  T={T} K={r['K']} rms={s['rms']:.1f} rms/sqrtq={s['rms_sqrtq']:.2f}",flush=True)
        json.dump(out,open('cache/exp2.json','w'))
    print("saved cache/exp2.json")
