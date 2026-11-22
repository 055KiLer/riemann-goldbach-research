import sys,time,numpy as np
sys.path.insert(0,'.')
from fastpipe import Group, make_logtab
from core import compute_E, compute_M
for q in (99961,):
    t0=time.time(); G=Group(q); print('group',q,time.time()-t0,'phi',G.phi,flush=True)
    K=6; t0=time.time(); logtab=make_logtab(G.x,K); print('logtab',time.time()-t0,flush=True)
    cache={}
    t0=time.time()
    for A,B,S,T in [(1.0,0.5,0.5,1.0),(1.5,-0.5,0.5,-1.5)]:
        a=complex(0.5,A); b=complex(0.5,B); s=complex(0.6,S); t=complex(0.6,T)
        E=compute_E(G,a,b,s,t,logtab=logtab); M=compute_M(G,a,b,s,t,cache)
    print('2 shifts E+M',time.time()-t0,flush=True)
