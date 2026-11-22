import sys, numpy as np
sys.path.insert(0,'.')
from fastpipe import Group, make_logtab
from core import compute_M, compute_M_parts
from mainterm import zeta_q, Aprod, Xqe
import mpmath as mp
mp.mp.dps=30

def E_all_and_prim(G,a,b,s,t,logtab,K=6):
    us=[complex(a),complex(b),complex(s),complex(t)]
    La,_=G.L_all(us[0],K,logtab); _,Lb=G.L_all(us[1],K,logtab)
    Ls,_=G.L_all(us[2],K,logtab); _,Lt=G.L_all(us[3],K,logtab)
    terms=La*Lb/(Ls*Lt)
    return complex(np.sum(terms)), complex(np.sum(terms[G.prim_mask]))
def M_all(G,a,b,s,t,cache):
    q=G.q
    M0=int(np.sum(G.parity_flat==0)); M1=int(np.sum(G.parity_flat==1))
    def Zq(x,y,c,d):
        return zeta_q(x+y,q,G.fac,cache)*zeta_q(c+d,q,G.fac,cache)/(zeta_q(x+d,q,G.fac,cache)*zeta_q(y+c,q,G.fac,cache))*Aprod(x,y,c,d,q)
    Z=Zq(a,b,s,t); Zd=Zq(1-b,1-a,s,t)
    H=sum((M0 if e==0 else M1)*Xqe(q,e,a)*Xqe(q,e,b) for e in (0,1))
    return complex((M0+M1)*Z+H*Zd), (M0,M1)

shifts=[(1.0,0.5,0.5,1.0,0.1),(1.5,-0.5,0.5,-1.5,0.1),(0.8,0.3,-0.7,0.6,0.2),(-1.0,0.5,0.5,-1.0,0.2),(0.4,1.2,-0.6,1.8,0.1)]
for q in (1024,3125,65536,2187,2401,531441):
    G=Group(q); logtab=make_logtab(G.x,6); cache={}
    ds_all=[]; ds_prim=[]; ds_prim_expected=[]
    for (A,B,S,T,eta) in shifts:
        a=complex(0.5,A); b=complex(0.5,B); s=complex(0.5+eta,S); t=complex(0.5+eta,T)
        Eall,Eprim=E_all_and_prim(G,a,b,s,t,logtab)
        Mall,counts=M_all(G,a,b,s,t,cache)
        Mprim=compute_M(G,a,b,s,t,cache)
        ds_all.append(Eall-Mall); ds_prim.append(Eprim-Mprim)
    da=np.array(ds_all); dp=np.array(ds_prim)
    print(f"q={q} phi={G.phi} phist={G.phist} E_all rel rms={np.sqrt(np.mean(np.abs(da)**2))/G.phi:.4f} | prim rel rms={np.sqrt(np.mean(np.abs(dp)**2))/G.phist:.4f}",flush=True)
