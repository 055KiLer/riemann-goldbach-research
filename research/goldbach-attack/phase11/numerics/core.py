"""E_q (fast FFT route) and M_q (phase-10 canonical formulas)."""
import numpy as np, mpmath as mp, sys, os
sys.path.insert(0,'.')
from fastpipe import Group, hurwitz_np, make_logtab, factorize
# phase-10 scalar helpers (zeta_q, Aprod, Xqe)
_P10=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','phase10','numerics')
sys.path.insert(0,_P10)
from mainterm import zeta_q, Aprod, Xqe
mp.mp.dps=30
_PRIMES=np.load(os.path.join(_P10,'primes_2000000.npy'))
_PRIMES=_PRIMES[_PRIMES<=1000000]

def K_for(u,Kmin=6):
    return max(Kmin,int(abs(complex(u).imag))+3)

def compute_E(G,a,b,s,t,logtab=None,return_parts=False):
    if G.empty: return (0j,0j,0j) if return_parts else 0j
    us=[complex(a),complex(b),complex(s),complex(t)]
    K=max(K_for(u) for u in us)
    if logtab is None: logtab=make_logtab(G.x,K)
    La,_=G.L_all(us[0],K,logtab)
    _,Lb=G.L_all(us[1],K,logtab)
    Ls,_=G.L_all(us[2],K,logtab)
    _,Lt=G.L_all(us[3],K,logtab)
    terms=La*Lb/(Ls*Lt)
    m=G.prim_mask
    E=complex(np.sum(terms[m]))
    if return_parts:
        p=G.parity_flat
        E0=complex(np.sum(terms[m&(p==0)])); E1=complex(np.sum(terms[m&(p==1)]))
        return E,E0,E1
    return E

def compute_M(G,a,b,s,t,cache=None):
    if G.empty: return 0j
    q=G.q; M0,M1=G.M0,G.M1; phist=G.phist
    if cache is None: cache={}
    def Zq(x,y,c,d):
        return zeta_q(x+y,q,G.fac,cache)*zeta_q(c+d,q,G.fac,cache)/(zeta_q(x+d,q,G.fac,cache)*zeta_q(y+c,q,G.fac,cache))*Aprod(x,y,c,d,q)
    Z=Zq(a,b,s,t); Zd=Zq(1-b,1-a,s,t)
    H=sum((M0 if e==0 else M1)*Xqe(q,e,a)*Xqe(q,e,b) for e in (0,1))
    return complex(phist*Z+H*Zd)

def compute_M_parts(G,a,b,s,t,cache=None):
    if G.empty: return 0j,0j
    q=G.q; M0,M1=G.M0,G.M1; phist=G.phist
    if cache is None: cache={}
    def Zq(x,y,c,d):
        return zeta_q(x+y,q,G.fac,cache)*zeta_q(c+d,q,G.fac,cache)/(zeta_q(x+d,q,G.fac,cache)*zeta_q(y+c,q,G.fac,cache))*Aprod(x,y,c,d,q)
    Z=Zq(a,b,s,t); Zd=Zq(1-b,1-a,s,t)
    parts=[complex((M0 if e==0 else M1)*(Z + Xqe(q,e,a)*Xqe(q,e,b)*Zd)) for e in (0,1)]
    return parts[0],parts[1]
