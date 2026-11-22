import sys, numpy as np, mpmath as mp
sys.path.insert(0,'.')
from fastpipe import Group, make_logtab
from core import compute_E
from mainterm import zeta_q, Aprod, Xqe
mp.mp.dps=30
def M_variants(G,a,b,s,t):
    q=G.q; M0,M1=G.M0,G.M1; phist=G.phist; cache={}
    def Zq(x,y,c,d):
        return zeta_q(x+y,q,G.fac,cache)*zeta_q(c+d,q,G.fac,cache)/(zeta_q(x+d,q,G.fac,cache)*zeta_q(y+c,q,G.fac,cache))*Aprod(x,y,c,d,q)
    Z=Zq(a,b,s,t); Zd=Zq(1-b,1-a,s,t)
    out={}
    for name,args in (('Xab',(a,b)),('X1m',(1-b,1-a))):
        H=sum((M0 if e==0 else M1)*Xqe(q,e,args[0])*Xqe(q,e,args[1]) for e in (0,1))
        out[name]=complex(phist*Z+H*Zd)
        # swapped parity
        Hs=sum((M1 if e==0 else M0)*Xqe(q,e,args[0])*Xqe(q,e,args[1]) for e in (0,1))
        out[name+'_swapPar']=complex(phist*Z+Hs*Zd)
    out['Z']=complex(Z); out['Zd']=complex(Zd); out['phi']=phist
    return out
for q in (10012, 999956, 100072 if False else 10072):
    G=Group(q); logtab=make_logtab(G.x,6)
    print(f"### q={q} phist={G.phist} M0,M1={G.M0,G.M1}",flush=True)
    for (A,B,S,T,eta) in [(1.0,0.5,0.5,1.0,0.1),(1.5,-0.5,0.5,-1.5,0.1),(0.8,0.3,-0.7,0.6,0.2),(-1.0,0.5,0.5,-1.0,0.2)]:
        a=complex(0.5,A); b=complex(0.5,B); s=complex(0.5+eta,S); t=complex(0.5+eta,T)
        E=compute_E(G,a,b,s,t,logtab=logtab)
        vs=M_variants(G,a,b,s,t)
        line=f" imgs=({A},{B},{S},{T}) eta={eta}: |E|={abs(E):.4g} |M_Xab|={abs(vs['Xab']):.4g}"
        for name in ('Xab','X1m','Xab_swapPar','X1m_swapPar'):
            M=vs[name]; line+=f" rel({name})={abs(E-M)/abs(M):.4f}"
        line+=f" |HZd|={abs(vs['Xab']-vs['phi']*vs['Z']):.4g} |phiZ|={abs(vs['phi']*vs['Z']):.4g}"
        print(line,flush=True)
