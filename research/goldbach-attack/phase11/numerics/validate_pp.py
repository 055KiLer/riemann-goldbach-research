import sys, numpy as np, time
sys.path.insert(0,'.')
sys.path.insert(0,'../../phase10/numerics')
from fastpipe import Group, make_logtab
from core import compute_E, compute_M
from test_mq import compute as compute_p10   # phase-10 direct (charlib) implementation

shifts=[(1.0,0.5,0.5,1.0,0.1),(1.5,-0.5,0.5,-1.5,0.1),(0.8,0.3,-0.7,0.6,0.2),(-1.0,0.5,0.5,-1.0,0.2)]
for q in (1024,2187,2401,3125,1155,5005):
    G=Group(q); logtab=make_logtab(G.x,10); cache={}
    from charlib import CharGroup, factorize
    cg=CharGroup(q); fac=factorize(q)
    for (A,B,S,T,eta) in shifts:
        a=complex(0.5,A); b=complex(0.5,B); s=complex(0.5+eta,S); t=complex(0.5+eta,T)
        E=compute_E(G,a,b,s,t,logtab=logtab)
        p10=compute_p10(q,a,b,s,t,cg,fac,{})
        Eref=complex(p10['E'])
        print(f"q={q} imgs=({A},{B},{S},{T}) eta={eta}: fastE={E:.6g} p10E={Eref:.6g} reldiff={abs(E-Eref)/max(1e-30,abs(Eref)):.2e}",flush=True)
