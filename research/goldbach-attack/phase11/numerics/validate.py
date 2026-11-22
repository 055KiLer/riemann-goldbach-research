import sys, numpy as np, mpmath as mp, json, time
sys.path.insert(0,'.')
from fastpipe import Group, hurwitz_np, make_logtab
from core import compute_E, compute_M
mp.mp.dps=30

# 1) Hurwitz validation vs mpmath
print("== Hurwitz validation",flush=True)
for q in (1000,1009,2187):
    G=Group(q)
    idx=np.linspace(0,G.phi-1,25).astype(int)
    x=G.x[idx]; a=G.a[idx]
    for u in (complex(0.5,0.0),complex(0.5,0.3),complex(0.6,1.2),complex(0.5,-1.9)):
        K=max(6,int(abs(u.imag))+3)
        v=hurwitz_np(u,x,K=K)
        ref=np.array([complex(mp.zeta(mp.mpc(u.real,u.imag), mp.mpf(int(ai))/q)) for ai in a])
        err=np.max(np.abs(v-ref))
        print(f"q={q} u={u} K={K}: maxabs err={err:.2e} rel={err/np.max(np.abs(ref)):.2e}",flush=True)

# 2) Reproduce phase-10 E and M for q=1000,2003
print("== phase-10 reproduction",flush=True)
d=json.load(open('../../phase10/numerics/cache/final_data.json'))
rows=[r for r in d if r['q'] in (1000,2003) and r.get('n',0)]
for Gq in (1000,2003):
    G=Group(Gq); logtab=make_logtab(G.x,10); cache={}
    sel=[r for r in rows if r['q']==Gq][:4]
    for r in sel:
        eta=r['eta']; A,B,S,T=r['imgs']
        a=complex(0.5,A); b=complex(0.5,B); s=complex(0.5+eta,S); t=complex(0.5+eta,T)
        E=compute_E(G,a,b,s,t,logtab=logtab)
        M=compute_M(G,a,b,s,t,cache)
        Eref=complex(*r['E']); Mref=complex(r["std_Xab"]["M"][0],r["std_Xab"]["M"][1])
        print(f"q={Gq} imgs={r['imgs']} eta={eta}: |E-Eref|={abs(E-Eref):.2e} |M-Mref|={abs(M-Mref):.2e}",flush=True)
