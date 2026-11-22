"""Re-run error-term scaling with CORRECTED M_q (proper A_q over p∤q)."""
import sys, numpy as np, json, time
sys.path.insert(0,'.')
from fastpipe import Group, make_logtab
from core import compute_E
from corrected import M_correct
rng=np.random.default_rng(2718)

def gen_shifts(n,kind='avoidpole',T=2.0):
    out=[]
    while len(out)<n:
        A,B,S,Tt=rng.uniform(-T,T,4)
        if kind=='avoidpole':
            if abs(A+B)<0.5: continue
        elif kind=='normal':
            if abs(A+B)<0.5 or abs(A+B)>1.5: continue
            if max(abs(A),abs(B),abs(S),abs(Tt))>1.5: continue
        elif kind=='nearpole':
            d=rng.choice([-1,1])*rng.uniform(0.03,0.25); B=-A+d
            if abs(B)>T: continue
        elif kind=='largeIm':
            if max(abs(A),abs(B),abs(S),abs(Tt))<1.5: continue
        eta=0.1 if len(out)%2==0 else 0.2
        out.append((float(A),float(B),float(S),float(Tt),float(eta)))
    return out

def eval_shift(G,logtab,sh):
    A,B,S,T,eta=sh
    a=complex(0.5,A); b=complex(0.5,B); s=complex(0.5+eta,S); t=complex(0.5+eta,T)
    E=compute_E(G,a,b,s,t,logtab=logtab); M,_=M_correct(G,a,b,s,t)
    return E,M

def stats(ds):
    ad=np.abs(ds)
    return dict(n=len(ds),rms=float(np.sqrt(np.mean(ad**2))),med=float(np.median(ad)),mx=float(ad.max()))

if __name__=='__main__':
    out={}
    sh=gen_shifts(40,'avoidpole')
    out['std40']=[]
    print("== corrected-M standard ensemble (|A+B|>0.5, |Im|<=2)",flush=True)
    for e in range(8,19):
        q=2**e; G=Group(q); logtab=make_logtab(G.x,6)
        ds=[]
        for s_ in sh:
            E,M=eval_shift(G,logtab,s_); ds.append(E-M)
        st=stats(np.array(ds)); st.update(e=e,q=q,phist=G.phist)
        out['std40'].append(st); json.dump(out,open('cache/crosscheck2.json','w'))
        print(f"e={e:>2} q={q:>7} RMS={st['rms']:10.1f} RMS/sqrtq={st['rms']/q**0.5:7.2f} RMS/(q/2)={st['rms']/(q/2):.4f} med={st['med']:9.1f} max={st['mx']:10.1f}",flush=True)
    # slopes
    qs=np.array([r['q'] for r in out['std40']],float); rs=np.array([r['rms'] for r in out['std40']])
    A=np.vstack([np.ones_like(qs),np.log(qs)]).T
    sol=np.linalg.lstsq(A,np.log(rs),rcond=None)[0]; res=np.log(rs)-A@sol
    se=np.sqrt(np.sum(res**2)/(len(qs)-2)*np.linalg.inv(A.T@A)[1,1])
    print(f"FIT alpha (RMS vs q, corrected M) = {sol[1]:.4f} +- {se:.4f}",flush=True)
    out['alpha_std']=[float(sol[1]),float(se)]
    # classes
    print("== classes with corrected M",flush=True)
    out['classes']={}
    for kind in ('normal','nearpole','largeIm'):
        scls=gen_shifts(20,kind); out['classes'][kind]={'records':[]}
        for e in range(8,17):
            q=2**e; G=Group(q); logtab=make_logtab(G.x,6); ds=[]
            for s_ in scls:
                E,M=eval_shift(G,logtab,s_); ds.append(E-M)
            st=stats(np.array(ds)); st.update(e=e,q=q)
            out['classes'][kind]['records'].append(st)
        recs=out['classes'][kind]['records']; json.dump(out,open('cache/crosscheck2.json','w'))
        print(f" class {kind}: "+", ".join(f"e={r['e']}:{r['rms']/r['q']**0.5:.2f}" for r in recs),flush=True)
    # fixed shifts
    print("== fixed shifts with corrected M",flush=True)
    fixed=[(0.3,0.7,0.4,0.9,0.1),(1.0,0.5,0.5,1.0,0.1),(1.5,-0.5,0.5,-1.5,0.2),(0.8,0.3,-0.7,0.6,0.1),(-1.0,0.5,0.5,-1.0,0.2),(0.2,-0.9,1.2,-0.4,0.1)]
    out['fixed']=[]
    for s_ in fixed:
        recs=[]
        for e in range(8,19):
            q=2**e; G=Group(q); logtab=make_logtab(G.x,6)
            E,M=eval_shift(G,logtab,s_); recs.append(dict(e=e,q=q,d=float(abs(E-M))))
        qs=np.array([r['q'] for r in recs],float); ds=np.array([r['d'] for r in recs])
        A=np.vstack([np.ones_like(qs),np.log(qs)]).T
        sol=np.linalg.lstsq(A,np.log(ds),rcond=None)[0]; res=np.log(ds)-A@sol
        se=np.sqrt(np.sum(res**2)/(len(qs)-2)*np.linalg.inv(A.T@A)[1,1])
        out['fixed'].append(dict(shift=s_,recs=recs,alpha=float(sol[1]),alpha_se=float(se)))
        json.dump(out,open('cache/crosscheck2.json','w'))
        print(f" shift {s_}: alpha={sol[1]:.3f}+-{se:.3f} d(2^8)={recs[0]['d']:.2f} d(2^14)={recs[6]['d']:.2f} d(2^18)={recs[-1]['d']:.2f}",flush=True)
    print("saved")
