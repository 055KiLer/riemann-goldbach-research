"""Corrected main term M_q with proper A_q over p∤q (fixes phase-10 Aprod mask bug)."""
import sys, numpy as np, mpmath as mp
sys.path.insert(0,'.'); sys.path.insert(0,'../../phase10/numerics')
from fastpipe import Group, factorize
from mainterm import zeta_q, Xqe
mp.mp.dps=30
PR=np.load('primes_2000000.npy'); PR=PR[PR<=1000000]

def Aq_correct(a,b,c,d,q):
    # product over primes p with p ∤ q
    mask=(q % PR) != 0
    p=PR[mask].astype(float); lp=np.log(p)
    X=np.exp(-(a+d)*lp); Y=np.exp(-(b+c)*lp); G=np.exp(-(c+d)*lp)
    f=((1-G)*(1-X-Y+G))/((1-X)*(1-Y))
    return complex(np.exp(np.sum(np.log1p(f-1.0))))

def Zq_correct(x,y,c,d,q,fac,cache):
    return zeta_q(x+y,q,fac,cache)*zeta_q(c+d,q,fac,cache)/(zeta_q(x+d,q,fac,cache)*zeta_q(y+c,q,fac,cache))*Aq_correct(x,y,c,d,q)

def M_correct(G,a,b,s,t,correct=True):
    q=G.q; fac=G.fac; M0,M1=G.M0,G.M1; phist=G.phist; cache={}
    def Zq(x,y,c,d):
        return Zq_correct(x,y,c,d,q,fac,cache)
    Z=Zq(a,b,s,t); Zd=Zq(1-b,1-a,s,t)
    H=sum((M0 if e==0 else M1)*Xqe(q,e,a)*Xqe(q,e,b) for e in (0,1))
    return complex(phist*Z+H*Zd), (Z,Zd,H)

if __name__=='__main__':
    a=complex(0.5,0.3); b=complex(0.5,0.7); s=complex(0.6,0.4); t=complex(0.6,0.9)
    print("Lead shift: q, E (fast), M_old (phase10 Aprod), M_correct, |E-M_correct|, |E-M_old|")
    from core import compute_E, compute_M
    from fastpipe import make_logtab
    for e in range(4,15):
        q=2**e; G=Group(q); logtab=make_logtab(G.x,6)
        E=compute_E(G,a,b,s,t,logtab=logtab)
        Mold=compute_M(G,a,b,s,t,{})
        Mnew,(Z,Zd,H)=M_correct(G,a,b,s,t)
        print(f"e={e:>2} q={q:>6} E={E:.4f} Mold={Mold:.4f} Mnew={Mnew:.4f} |E-Mnew|={abs(E-Mnew):.3f} |E-Mold|={abs(E-Mold):.3f}",flush=True)
