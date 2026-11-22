"""Recompute phase-10 composite-q main-term comparison with CORRECTED A_q."""
import sys, json, numpy as np, mpmath as mp
sys.path.insert(0,'.'); sys.path.insert(0,'../../phase10/numerics')
from fastpipe import Group, make_logtab
from core import compute_E
from corrected import M_correct
from mainterm import zeta_q, Xqe
mp.mp.dps=30
PR=np.load('primes_2000000.npy'); PR=PR[PR<=1000000]
a_cache={}
def Aq(x,y,c,d,q):
    mask=(q % PR)!=0; p=PR[mask].astype(float); lp=np.log(p)
    X=np.exp(-(x+d)*lp); Y=np.exp(-(y+c)*lp); G=np.exp(-(c+d)*lp)
    f=((1-G)*(1-X-Y+G))/((1-X)*(1-Y))
    return complex(np.exp(np.sum(np.log1p(f-1.0))))
def M_corr(G,a,b,s,t):
    q=G.q; fac=G.fac; M0,M1=G.M0,G.M1; phist=G.phist; cache={}
    def Zq(x,y,c,d):
        return zeta_q(x+y,q,fac,cache)*zeta_q(c+d,q,fac,cache)/(zeta_q(x+d,q,fac,cache)*zeta_q(y+c,q,fac,cache))*Aq(x,y,c,d,q)
    Z=Zq(a,b,s,t); Zd=Zq(1-b,1-a,s,t)
    H=sum((M0 if e==0 else M1)*Xqe(q,e,a)*Xqe(q,e,b) for e in (0,1))
    return complex(phist*Z+H*Zd)
d=json.load(open('../../phase10/numerics/cache/final_data.json'))
qs_set=[1000,2003,60,84,105,120,140,165,360,420,720,900,1008,1260,1680,2000]
print("q      n  old-M rel rms   corrected-M rel rms")
for q in qs_set:
    rows=[r for r in d if r['q']==q and r.get('n',0)]
    if not rows: continue
    G=Group(q); logtab=make_logtab(G.x,10)
    old=[]; new=[]; oldsc=[]; newsc=[]
    for r in rows[:12]:
        eta=r['eta']; A,B,S,T=r['imgs']
        a=complex(0.5,A); b=complex(0.5,B); s=complex(0.5+eta,S); t=complex(0.5+eta,T)
        E=compute_E(G,a,b,s,t,logtab=logtab)
        Mold=complex(r['std_Xab']['M'][0],r['std_Xab']['M'][1])
        Mnew=M_corr(G,a,b,s,t)
        old.append(abs(E-Mold)/max(1e-12,abs(Mold)))
        new.append(abs(E-Mnew)/max(1e-12,abs(Mnew)))
        oldsc.append(abs(E-Mold)/q**0.5); newsc.append(abs(E-Mnew)/q**0.5)
    print(f"{q:>5} {len(rows):>3}  old rel={np.mean(old):.4f}/{np.median(old):.4f} |E-M|/sqrtq old={np.mean(oldsc):.3f} new={np.mean(newsc):.3f} | new rel={np.mean(new):.4f}/{np.median(new):.4f}",flush=True)
