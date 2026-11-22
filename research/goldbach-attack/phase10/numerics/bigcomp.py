import sys, numpy as np
sys.path.insert(0,'.')
from test_mq import compute
from charlib import CharGroup, factorize
qs=[720,900,1008,1260,1680,2000]
imgs=[(1.0,0.5,0.5,1.0),(1.5,-0.5,0.5,-1.5),(0.8,0.3,-0.7,0.6)]
for q in qs:
    cg=CharGroup(q); fac=factorize(q); cache={}
    if cg.n==0: print(f"q={q}: no primitive chars"); continue
    rel=[]; sc=[]; relX=[]; relS=[]
    for (A,B,S,T) in imgs:
        a=complex(0.5,A); b=complex(0.5,B); s=complex(0.6,S); t=complex(0.6,T)
        r=compute(q,a,b,s,t,cg,fac,cache)
        M=r['std_Xab']['M']; d=abs(r['E']-M)
        rel.append(d/abs(M)); sc.append(d/np.sqrt(q))
        relX.append(abs(r['E']-r['std_X1m']['M'])/abs(r['std_X1m']['M']))
        relS.append(abs(r['E']-r['swap_Xab']['M'])/abs(r['swap_Xab']['M']))
    print(f"q={q:>5} prim={cg.n:>3} counts={cg.counts()}: std_Xab rel mean={np.mean(rel):.3f} | |E-M|/sqrt(q) mean={np.mean(sc):.2f} max={np.max(sc):.2f} || X1m rel mean={np.mean(relX):.2f} | swapZ rel mean={np.mean(relS):.2f}",flush=True)
