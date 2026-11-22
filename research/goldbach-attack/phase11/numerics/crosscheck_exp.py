"""Cross-check experiments: shift-class dependence and fixed-shift scaling of |E-M| for q=2^e."""
import sys, numpy as np, json, time
sys.path.insert(0,'.')
from fastpipe import Group, make_logtab
from core import compute_E, compute_M
rng=np.random.default_rng(31415)

def gen_class(n, kind, T=2.0):
    out=[]
    while len(out)<n:
        A,B,S,Tt=rng.uniform(-T,T,4)
        if kind=='normal':
            if abs(A+B)<0.5 or abs(A+B)>1.5: continue
            if max(abs(A),abs(B),abs(S),abs(Tt))>1.5: continue
        elif kind=='nearpole':
            # small |A+B| but not too close to 0 (Z_q pole at A+B=0)
            d=rng.choice([-1,1])*rng.uniform(0.03,0.25)
            B=-A+d
            if abs(B)>T: continue
        elif kind=='largeIm':
            if max(abs(A),abs(B),abs(S),abs(Tt))<1.5: continue
        eta=0.1 if len(out)%2==0 else 0.2
        out.append((float(A),float(B),float(S),float(Tt),float(eta)))
    return out

def eval_shift(G,logtab,sh,cache):
    A,B,S,T,eta=sh
    a=complex(0.5,A); b=complex(0.5,B); s=complex(0.5+eta,S); t=complex(0.5+eta,T)
    E=compute_E(G,a,b,s,t,logtab=logtab); M=compute_M(G,a,b,s,t,cache)
    return E,M

def stats(ds):
    ad=np.abs(ds)
    return dict(n=len(ds),rms=float(np.sqrt(np.mean(ad**2))),med=float(np.median(ad)),mx=float(ad.max()))

if __name__=='__main__':
    out={}
    # (C1) standard random ensemble for e=8..18
    sh_std=gen_class(40,'random')
    print("== standard ensemble e=8..18",flush=True)
    out['std']=[]
    for e in range(8,19):
        q=2**e; G=Group(q); logtab=make_logtab(G.x,6); cache={}
        t0=time.time(); ds=[]
        for sh in sh_std:
            E,M=eval_shift(G,logtab,sh,cache); ds.append(E-M)
        st=stats(np.array(ds)); st.update(e=e,q=q,phi=G.phi,phist=G.phist,time=time.time()-t0)
        out['std'].append(st); json.dump(out,open('cache/crosscheck.json','w'))
        print(f"e={e} q={q:>7} RMS={st['rms']:10.1f} RMS/sqrtq={st['rms']/q**0.5:6.2f} RMS/(q/2)={st['rms']/(q/2):.4f} med={st['med']:9.1f} max={st['mx']:10.1f} ({st['time']:.1f}s)",flush=True)
    # (C2) classes for e=8..16 (cheaper)
    print("== shift classes",flush=True)
    out['classes']={}
    for kind in ('normal','nearpole','largeIm'):
        sh=gen_class(20,kind)
        out['classes'][kind]={'shifts':sh,'records':[]}
        for e in range(8,17):
            q=2**e; G=Group(q); logtab=make_logtab(G.x,6); cache={}
            ds=[]
            for s_ in sh:
                E,M=eval_shift(G,logtab,s_,cache); ds.append(E-M)
            st=stats(np.array(ds)); st.update(e=e,q=q)
            out['classes'][kind]['records'].append(st); json.dump(out,open('cache/crosscheck.json','w'))
        recs=out['classes'][kind]['records']
        print(f"class {kind}: "+", ".join(f"e={r['e']}:RMS/√q={r['rms']/r['q']**0.5:.2f}" for r in recs),flush=True)
    # (C3) fixed-shift family scaling
    print("== fixed shifts",flush=True)
    lead=((0.3,0.7,0.4,0.9,0.1),)
    fixed=[(0.3,0.7,0.4,0.9,0.1),(1.0,0.5,0.5,1.0,0.1),(1.5,-0.5,0.5,-1.5,0.2),(0.8,0.3,-0.7,0.6,0.1),(-1.0,0.5,0.5,-1.0,0.2),(0.2,-0.9,1.2,-0.4,0.1)]
    out['fixed']=[]
    for sh in fixed:
        recs=[]
        for e in range(8,19):
            q=2**e; G=Group(q); logtab=make_logtab(G.x,6); cache={}
            E,M=eval_shift(G,logtab,sh,cache)
            recs.append(dict(e=e,q=q,d=float(abs(E-M)),E=[E.real,E.imag],M=[M.real,M.imag]))
        # fit alpha per shift
        qs=np.array([r['q'] for r in recs],float); ds=np.array([r['d'] for r in recs],float)
        A=np.vstack([np.ones_like(qs),np.log(qs)]).T
        sol=np.linalg.lstsq(A,np.log(ds),rcond=None)[0]
        res=np.log(ds)-A@sol; se=np.sqrt(np.sum(res**2)/(len(qs)-2)*np.linalg.inv(A.T@A)[1,1])
        out['fixed'].append(dict(shift=sh,recs=recs,alpha=float(sol[1]),alpha_se=float(se)))
        json.dump(out,open('cache/crosscheck.json','w'))
        print(f"shift {sh}: alpha={sol[1]:.3f}+-{se:.3f}  d(2^8)={recs[0]['d']:.2f} d(2^14)={recs[6]['d']:.2f} d(2^18)={recs[-1]['d']:.2f}",flush=True)
    print("saved cache/crosscheck.json")
