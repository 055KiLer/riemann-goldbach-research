import sys, numpy as np, mpmath as mp
sys.path.insert(0,'.')
from fastpipe import Group, make_logtab
from core import compute_E
from mainterm import zeta_q, Aprod
mp.mp.dps=30
def X(q,e,w,modq=None):
    qq=q if modq is None else modq
    w=mp.mpc(w.real,w.imag)
    return mp.power(qq/mp.pi, mp.mpf(1)/2-w)*mp.gamma((1-w+e)/2)/mp.gamma((w+e)/2)
def M_var(G,a,b,s,t,modq=None):
    q=G.q; M0,M1=G.M0,G.M1; phist=G.phist; cache={}
    def Zq(x,y,c,d):
        return zeta_q(x+y,q,G.fac,cache)*zeta_q(c+d,q,G.fac,cache)/(zeta_q(x+d,q,G.fac,cache)*zeta_q(y+c,q,G.fac,cache))*Aprod(x,y,c,d,q)
    Z=Zq(a,b,s,t); Zd=Zq(1-b,1-a,s,t)
    H=sum((M0 if e==0 else M1)*X(q,e,a,modq)*X(q,e,b,modq) for e in (0,1))
    return complex(phist*Z+H*Zd)
for q in (10012,999956,10072):
    G=Group(q); logtab=make_logtab(G.x,6)
    print(f"### q={q}",flush=True)
    for (A,B,S,T,eta) in [(1.0,0.5,0.5,1.0,0.1),(1.5,-0.5,0.5,-1.5,0.1),(0.8,0.3,-0.7,0.6,0.2),(-1.0,0.5,0.5,-1.0,0.2)]:
        a=complex(0.5,A); b=complex(0.5,B); s=complex(0.5+eta,S); t=complex(0.5+eta,T)
        E=compute_E(G,a,b,s,t,logtab=logtab)
        line=f" imgs=({A},{B},{S},{T}): |E|={abs(E):.4g}"
        for mq,tag in ((None,'q'),(q//4,'q/4'),(q//2,'q/2'),(q*1,'q'),(1,'1')):
            if q%4!=0 and tag in ('q/4','q/2'): continue
            M=M_var(G,a,b,s,t,mq)
            line+=f" rel({tag})={abs(E-M)/abs(M):.4f}"
        print(line,flush=True)
