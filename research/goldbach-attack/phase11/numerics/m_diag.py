import sys, numpy as np, mpmath as mp
sys.path.insert(0,'.')
sys.path.insert(0,'../../phase10/numerics')
from fastpipe import Group, make_logtab, factorize
from mainterm import zeta_q, Aprod, Xqe
mp.mp.dps=35
a=complex(0.5,0.3); b=complex(0.5,0.7); s=complex(0.6,0.4); t=complex(0.6,0.9)
for e in (10,12,14):
    q=2**e; G=Group(q)
    phi=G.phi; M0,M1=G.M0,G.M1; phist=G.phist
    cache={}
    def Zq(x,y,c,d):
        return zeta_q(x+y,q,G.fac,cache)*zeta_q(c+d,q,G.fac,cache)/(zeta_q(x+d,q,G.fac,cache)*zeta_q(y+c,q,G.fac,cache))*Aprod(x,y,c,d,q)
    Z=Zq(a,b,s,t); Zd=Zq(1-b,1-a,s,t)
    print(f"e={e} q={q} phi={phi} M0,M1={M0,M1} Z={Z:.6f} Zd={Zd:.6f} phiZ={phist*Z:.4f}")
    # X values
    for ee in (0,1):
        xa=Xqe(q,ee,a); xb=Xqe(q,ee,b)
        print(f"  X_{ee}(a)={complex(xa):.6f} X_{ee}(b)={complex(xb):.6f}")
    H_ab=sum((M0 if ee==0 else M1)*Xqe(q,ee,a)*Xqe(q,ee,b) for ee in (0,1))
    H_1m=sum((M0 if ee==0 else M1)*Xqe(q,ee,1-b)*Xqe(q,ee,1-a) for ee in (0,1))
    M_ab=phist*Z+H_ab*Zd; M_1m=phist*Z+H_1m*Zd
    print(f"  H(a,b)={complex(H_ab):.4f} H(1-b,1-a)={complex(H_1m):.4f}")
    print(f"  M[ours X(a)X(b)] = {complex(M_ab):.6f}")
    print(f"  M[X(1-b)X(1-a)] = {complex(M_1m):.6f}")
    # no-H
    print(f"  phiZ = {complex(phist*Z):.6f}")
