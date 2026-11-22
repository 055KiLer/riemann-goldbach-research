import sys, numpy as np, mpmath as mp
sys.path.insert(0,'.')
import os
sys.path.insert(0,'../../phase10/numerics')
from fastpipe import Group, make_logtab
from mainterm import zeta_q, Aprod, Xqe
mp.mp.dps=30

def E_all(G,a,b,s,t,logtab,K=6):
    us=[complex(a),complex(b),complex(s),complex(t)]
    La,_=G.L_all(us[0],K,logtab); _,Lb=G.L_all(us[1],K,logtab)
    Ls,_=G.L_all(us[2],K,logtab); _,Lt=G.L_all(us[3],K,logtab)
    return complex(np.sum((La*Lb/(Ls*Lt))))

def E_prim(G,a,b,s,t,logtab,K=6):
    us=[complex(a),complex(b),complex(s),complex(t)]
    La,_=G.L_all(us[0],K,logtab); _,Lb=G.L_all(us[1],K,logtab)
    Ls,_=G.L_all(us[2],K,logtab); _,Lt=G.L_all(us[3],K,logtab)
    return complex(np.sum((La*Lb/(Ls*Lt))[G.prim_mask]))

def M_all(d,a,b,s,t,cache):
    Gd=Group(d); cache={}
    def Zq(x,y,c,dd):
        return zeta_q(x+y,d,Gd.fac,cache)*zeta_q(c+dd,d,Gd.fac,cache)/(zeta_q(x+dd,d,Gd.fac,cache)*zeta_q(y+c,d,Gd.fac,cache))*Aprod(x,y,c,dd,d)
    Z=Zq(a,b,s,t); Zd=Zq(1-b,1-a,s,t)
    M0=int(np.sum(Gd.parity_flat==0)); M1=int(np.sum(Gd.parity_flat==1))
    H=sum((M0 if e==0 else M1)*Xqe(d,e,a)*Xqe(d,e,b) for e in (0,1))
    return complex(Gd.phi*Z+H*Zd),(M0,M1)
def E_all1(a,b,s,t):
    return complex(mp.zeta(a)*mp.zeta(b)/(mp.zeta(s)*mp.zeta(t)))
def divs(n):
    out=[]
    for i in range(1,int(n**0.5)+1):
        if n%i==0:
            out.append(i)
            if i!=n//i: out.append(n//i)
    return sorted(out)
def mobius(n):
    if n==1: return 1
    fac=0; m=n; p=2
    while p*p<=m:
        if m%p==0:
            m//=p
            if m%p==0: return 0
            fac+=1
        p+=1
    if m>1: fac+=1
    return (-1)**fac

shifts=[(1.0,0.5,0.5,1.0,0.1),(1.5,-0.5,0.5,-1.5,0.1),(0.8,0.3,-0.7,0.6,0.2)]
for q in (12,28,10012):
    G=Group(q); logtab=make_logtab(G.x,6)
    print(f"### q={q} phi={G.phi} phist={G.phist}",flush=True)
    for (A,B,S,T,eta) in shifts:
        a=complex(0.5,A); b=complex(0.5,B); s=complex(0.5+eta,S); t=complex(0.5+eta,T)
        Ep=E_prim(G,a,b,s,t,logtab)
        # identity check: E_prim(q) = sum_{d|q} mu(q/d) E_all(d)
        ssum=0j
        for d in divs(q):
            if d==1:
                ssum+=mobius(q//d)*E_all1(a,b,s,t); continue
            G1=Group(d)
            if G1.empty: continue
            lt=make_logtab(G1.x,6)
            ssum+=mobius(q//d)*E_all(G1,a,b,s,t,lt)
        # inclusion-exclusion main term
        mie=0j
        for d in divs(q):
            if d==1:
                # M_all(1): phi=1, M0=1,M1=0, Z_1, A_1 over all primes
                def Z1(x,y,c,dd, cache={}):
                    return zeta_q(x+y,1,{},cache)*zeta_q(c+dd,1,{},cache)/(zeta_q(x+dd,1,{},cache)*zeta_q(y+c,1,{},cache))*Aprod(x,y,c,dd,1)
                Z1v=Z1(a,b,s,t); Zd1=Z1(1-b,1-a,s,t)
                H1=Xqe(1,0,a)*Xqe(1,0,b)
                mie+=mobius(q//d)*complex(Z1v+H1*Zd1); continue
            if Group(d).empty: continue
            Md,_=M_all(d,a,b,s,t,{})
            mie+=mobius(q//d)*Md
        Mtr=0j
        # transcribed main term uses q only: compute via core
        from core import compute_M
        Mtr=compute_M(G,a,b,s,t,{})
        print(f" imgs=({A},{B},{S},{T}): |Ep|= {abs(Ep):.4g} |(sum mu E_all)-Ep|={abs(ssum-Ep):.2e} |Ep-M_IE|/|Ep|={abs(Ep-mie)/abs(Ep):.4f} |Ep-M_trans/|Ep|={abs(Ep-Mtr)/abs(Ep):.4f}",flush=True)
