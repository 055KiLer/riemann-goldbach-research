import sys, numpy as np
sys.path.insert(0,'.')
from test_mq import compute
from charlib import CharGroup, factorize
qs=[107,211,307,503]
imgs=[(1.0,0.5,0.5,1.0),(1.5,-0.5,0.5,-1.5),(0.8,0.3,-0.7,0.6)]
for q in qs:
    cg=CharGroup(q); fac=factorize(q); cache={}
    print(f"### q={q} chars={cg.n}",flush=True)
    for (A,B,S,T) in imgs:
        a=complex(0.5,A); b=complex(0.5,B); s=complex(0.6,S); t=complex(0.6,T)
        r=compute(q,a,b,s,t,cg,fac,cache)
        for tag in ('std_Xab','std_X1m','swap_Xab'):
            M=r[tag]['M']; d=abs(r['E']-M)
            print(f"  imgs={A,B,S,T} {tag}: |E-M|={d:.5f} /sqrt(q)={d/np.sqrt(q):.4f} rel={d/abs(M):.4f}",flush=True)
