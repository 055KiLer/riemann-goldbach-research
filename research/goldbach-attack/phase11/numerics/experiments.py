import sys, time, json, numpy as np
sys.path.insert(0,'.')
from fastpipe import Group, make_logtab
from core import compute_E, compute_M, K_for
import mpmath as mp
mp.mp.dps=30

rng=np.random.default_rng(20261121)

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
    Kmax=max(K_for(complex(0.5+eta, T),Kmin) for (A,B,S,T,eta) in shifts)
    t0=time.time(); logtab=make_logtab(G.x,Kmax); ttab=time.time()-t0
    cache={}
    res=[]
    t0=time.time()
    for (A,B,S,Tt,eta) in shifts:
        a=complex(0.5,A); b=complex(0.5,B); s=complex(0.5+eta,S); t=complex(0.5+eta,Tt)
        E=compute_E(G,a,b,s,t,logtab=logtab)
        M=compute_M(G,a,b,s,t,cache)
        res.append(dict(sh=[A,B,S,Tt,eta],E=[E.real,E.imag],M=[M.real,M.imag],d=[(E-M).real,(E-M).imag]))
    dt=time.time()-t0
    d=np.array([complex(*r['d']) for r in res])
    return dict(q=q,phi=G.phi,phist=G.phist,M0=G.M0,M1=G.M1,n=len(shifts),K=Kmax,
                rms=float(np.sqrt(np.mean(np.abs(d)**2))), absmean=float(np.mean(np.abs(d))),
                mean=[float(np.mean(d.real)),float(np.mean(d.imag))], max=float(np.max(np.abs(d))),
                shifts=res, logtab_time=ttab, eval_time=dt)

if __name__=='__main__':
    out={}
    primes=[1009,3001,10093,29989,99961,199921,400753,700001,1002241]
    NS=20
    shifts=make_shifts(NS)
    print("shift set:",[(round(s[0],2),round(s[1],2),round(s[4],1)) for s in shifts[:4]],"...",flush=True)
    out['primes']=[]
    for q in primes:
        r=run_q(q,shifts); out['primes'].append(r)
        print(f"prime q={q} phi={r['phi']} RMS={r['rms']:.4f} RMS/sqrtq={r['rms']/q**0.5:.4f} |mean|={abs(complex(*r['mean'])):.4f} time={r['eval_time']:.1f}s",flush=True)
        json.dump(out,open('cache/exp_results.json','w'))
    # T-dependence
    out['T']=[]
    qT=99961
    for T in (2,5,10,20):
        sh=make_shifts(12,T=T)
        r=run_q(qT,sh); out['T'].append(r)
        print(f"T={T} RMS={r['rms']:.4f} RMS/sqrtq={r['rms']/qT**0.5:.4f} time={r['eval_time']:.1f}s",flush=True)
        json.dump(out,open('cache/exp_results.json','w'))
    # composites
    out['composites']=[]
    comps=[1024,2187,2401,3125,1155,5005,15015,17017,85085,255255,1200,2000,3600,65536,78125,531441]
    for q in comps:
        r=run_q(q,shifts)
        if r is None:
            print(f"q={q}: empty (no primitive chars)",flush=True); continue
        out['composites'].append(r)
        print(f"composite q={q} phi={r['phi']} phist={r['phist']} RMS={r['rms']:.4f} RMS/sqrtq={r['rms']/q**0.5:.4f} time={r['eval_time']:.1f}s",flush=True)
        json.dump(out,open('cache/exp_results.json','w'))
    # holomorphy probe
    out['holo']={'q':10093,'offsets':[0.0625,0.125],'records':[]}
    G=Group(10093); K=6; logtab=make_logtab(G.x,K); cache={}
    base=make_shifts(6)
    for off in (-0.125,-0.0625,0.0625,0.125):
        ds=[]
        for (A,B,S,Tt,eta) in base:
            a=complex(0.5+off,A); b=complex(0.5,B); s=complex(0.5+eta,S); t=complex(0.5+eta,Tt)
            E=compute_E(G,a,b,s,t,logtab=logtab); M=compute_M(G,a,b,s,t,cache)
            ds.append(E-M)
        d=np.array(ds)
        rec=dict(off=off,rms=float(np.sqrt(np.mean(np.abs(d)**2))),absmean=float(np.mean(np.abs(d))))
        out['holo']['records'].append(rec)
        print("holo off",off,"RMS",rec['rms'],flush=True)
    json.dump(out,open('cache/exp_results.json','w'))
    # near-pole probe
    out['pole']={'q':10093,'records':[]}
    for delta in (0.4,0.2,0.1,0.05,0.02):
        ds=[]; Ms=[]
        for i in range(6):
            A=0.5+0.3*i; B=delta-A; S=0.5*i; Tt=-0.3*i; eta=0.1
            a=complex(0.5,A); b=complex(0.5,B); s=complex(0.6,S); t=complex(0.6,Tt)
            E=compute_E(G,a,b,s,t,logtab=logtab); M=compute_M(G,a,b,s,t,cache)
            ds.append(E-M); Ms.append(M)
        d=np.array(ds); M=np.array(Ms)
        rec=dict(delta=delta,rms=float(np.sqrt(np.mean(np.abs(d)**2))),absmean=float(np.mean(np.abs(d))),Mabs=float(np.mean(np.abs(M))))
        out['pole']['records'].append(rec)
        print("pole delta",delta,"RMS",rec['rms'],"|M|",rec['Mabs'],flush=True)
    json.dump(out,open('cache/exp_results.json','w'))
    print("saved cache/exp_results.json")
