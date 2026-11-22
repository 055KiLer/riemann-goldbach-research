"""M_q term-by-term variants with CORRECT A_q (p∤q) to locate Lead's M value."""
import sys, numpy as np, mpmath as mp, json
sys.path.insert(0,'.'); sys.path.insert(0,'../../phase10/numerics')
from fastpipe import Group, make_logtab
from core import compute_E
from mainterm import zeta_q, Xqe
mp.mp.dps=30
PR=np.load('primes_2000000.npy'); PR=PR[PR<=1000000]
a=complex(0.5,0.3); b=complex(0.5,0.7); s=complex(0.6,0.4); t=complex(0.6,0.9)

def Aq(x,y,c,d,q,exclude=True):
    if exclude: mask=(q % PR)!=0
    else: mask=(PR % q)!=0
    p=PR[mask].astype(float); lp=np.log(p)
    X=np.exp(-(x+d)*lp); Y=np.exp(-(y+c)*lp); G=np.exp(-(c+d)*lp)
    f=((1-G)*(1-X-Y+G))/((1-X)*(1-Y))
    return complex(np.exp(np.sum(np.log1p(f-1.0))))
def Zq(x,y,c,d,q,fac,cache,exclude=True):
    return zeta_q(x+y,q,fac,cache)*zeta_q(c+d,q,fac,cache)/(zeta_q(x+d,q,fac,cache)*zeta_q(y+c,q,fac,cache))*Aq(x,y,c,d,q,exclude)
def M_terms(q,exclude=True,harm='ab',zd='std',zextra=0):
    G=Group(q); fac=G.fac; M0,M1=G.M0,G.M1; phist=G.phist; cache={}
    if zextra==1:
        # variant: zeta_q with squared local removal
        def zq2(sv,fac,cache):
            return zeta_q(sv,q,fac,cache)  # placeholder
    Z=Zq(a,b,s,t,q,fac,cache,exclude); 
    xd,yd=(1-b,1-a) if zd=='std' else (1-a,1-b)
    Zd=Zq(xd,yd,s,t,q,fac,cache,exclude)
    def H(x,y):
        return sum((M0 if e==0 else M1)*Xqe(q,e,x)*Xqe(q,e,y) for e in (0,1))
    if harm=='ab': HH=H(a,b)
    elif harm=='1m': HH=H(1-b,1-a)
    elif harm=='a_1a': HH=H(a,1-b)
    elif harm=='swapPar':
        HH=sum((M1 if e==0 else M0)*Xqe(q,e,a)*Xqe(q,e,b) for e in (0,1))
    M=phist*Z+HH*Zd
    return complex(M),dict(Z=Z,Zd=Zd,H=HH,phi=phist)
if __name__=='__main__':
    for e in (10,12,14):
        q=2**e; G=Group(q); logtab=make_logtab(G.x,6)
        E=compute_E(G,a,b,s,t,logtab=logtab)
        print(f"### e={e} q={q} E={E:.4f}  Lead: |E-M|={ {10:11.7,12:37.6,14:114.3}[e] }",flush=True)
        for exclude in (True,False):
            for harm in ('ab','1m','a_1a','swapPar'):
                for zd in ('std','swap'):
                    M,d=M_terms(q,exclude,harm,zd)
                    print(f"  A_q{'corr' if exclude else 'all-p'}, H={harm:8s}, Zd={zd:4s}: M={M:.4f} |E-M|={abs(E-M):.3f}",flush=True)
