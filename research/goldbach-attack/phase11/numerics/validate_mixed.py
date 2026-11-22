import sys, numpy as np
sys.path.insert(0,'.')
sys.path.insert(0,'../../phase10/numerics')
from fastpipe import Group, make_logtab
from core import compute_E, compute_M
from test_mq import compute as compute_p10
from charlib import CharGroup, factorize
shifts=[(1.0,0.5,0.5,1.0,0.1),(1.5,-0.5,0.5,-1.5,0.2),(0.8,0.3,-0.7,0.6,0.1)]
for q in (10012,10072,9117):
    G=Group(q); logtab=make_logtab(G.x,10)
    cg=CharGroup(q); fac=factorize(q)
    print(f"q={q}: fast phist={G.phist} charlib chars={cg.n}",flush=True)
    for (A,B,S,T,eta) in shifts:
        a=complex(0.5,A); b=complex(0.5,B); s=complex(0.5+eta,S); t=complex(0.5+eta,T)
        Ef=compute_E(G,a,b,s,t,logtab=logtab)
        p10=compute_p10(q,a,b,s,t,cg,fac,{})
        Ep=complex(p10['E'])
        Mf=compute_M(G,a,b,s,t,{})
        rel=abs(Ef-Ep)/max(1e-30,abs(Ep))
        print(f"  imgs=({A},{B},{S},{T}): |E_fast-E_charlib|/|E|={rel:.2e}  |E_fast|={abs(Ef):.4g}",flush=True)
