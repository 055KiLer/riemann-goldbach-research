"""Independent mpmath validation of M_q for q=2^e and variant search."""
import sys, numpy as np, mpmath as mp
sys.path.insert(0,'.'); sys.path.insert(0,'../../phase10/numerics')
from fastpipe import Group, make_logtab
from core import compute_E
mp.mp.dps=35
PR=np.load('primes_2000000.npy'); PR=PR[PR<=2000000]
a=complex(0.5,0.3); b=complex(0.5,0.7); s=complex(0.6,0.4); t=complex(0.6,0.9)

def zeta_q(sv,q,fac):
    z=mp.zeta(sv)
    for p in fac: z*= (1-mp.power(p,-sv))
    return z
def Aq(x,y,c,d,q,fac,swap=False):
    prod=mp.mpf(1)
    for p in PR:
        p=int(p)
        if q%p==0: continue
        if swap:
            num=(1-mp.power(p,-(c+d)))*(1-mp.power(p,-(x+c))-mp.power(p,-(y+d))+mp.power(p,-(c+d)))
            den=(1-mp.power(p,-(x+c)))*(1-mp.power(p,-(y+d)))
        else:
            num=(1-mp.power(p,-(c+d)))*(1-mp.power(p,-(x+d))-mp.power(p,-(y+c))+mp.power(p,-(c+d)))
            den=(1-mp.power(p,-(x+d)))*(1-mp.power(p,-(y+c)))
        prod*=num/den
    return prod
def Zq(x,y,c,d,q,fac,swap=False):
    return zeta_q(x+y,q,fac)*zeta_q(c+d,q,fac)/(zeta_q(x+d,q,fac)*zeta_q(y+c,q,fac))*Aq(x,y,c,d,q,fac,swap)
def X(q,e,w):
    q=mp.mpf(q); w=mp.mpc(w.real,w.imag)
    return mp.power(q/mp.pi, mp.mpf(1)/2-w)*mp.gamma((1-w+e)/2)/mp.gamma((w+e)/2)
def M_fresh(q,kind='ours'):
    G=Group(q); fac=G.fac; M0,M1=G.M0,G.M1; phist=G.phist
    Z=Zq(a,b,s,t,q,fac); Zd=Zq(1-b,1-a,s,t,q,fac)
    def H(args):
        return sum((M0 if e==0 else M1)*X(q,e,args[0])*X(q,e,args[1]) for e in (0,1))
    base=complex(phist*Z)
    if kind=='ours': return base+complex(H((a,b))*Zd), (Z,Zd,H((a,b)),M0,M1)
    if kind=='x1m': return base+complex(H((1-b,1-a))*Zd), None
    if kind=='swapPar':
        Hsw=sum((M1 if e==0 else M0)*X(q,e,a)*X(q,e,b) for e in (0,1))
        return base+complex(Hsw*Zd), None
    if kind=='zd1': return base+complex(H((a,b))*Zq(1-a,1-b,s,t,q,fac)), None
    if kind=='zd2': return base+complex(H((a,b))*Zq(1-b,1-a,t,s,q,fac)), None
    if kind=='zswap':
        Zs=Zq(a,b,s,t,q,fac,swap=True); Zds=Zq(1-b,1-a,s,t,q,fac,swap=True)
        return complex(phist*Zs+H((a,b))*Zds), None
    if kind=='noH': return base, None
print("q      our core M              fresh M (ours)            |E-M| core / fresh")
for e in (10,12,14):
    q=2**e; G=Group(q); logtab=make_logtab(G.x,6)
    E=compute_E(G,a,b,s,t,logtab=logtab)
    from core import compute_M
    Mcore=compute_M(G,a,b,s,t,{})
    Mf,info=M_fresh(q,'ours')
    print(f"2^{e:<2} core={Mcore:.6f} fresh={Mf:.6f} diff={abs(Mcore-Mf):.2e} |E-M|={(abs(E-Mcore)):.3f}/{(abs(E-Mf)):.3f}")
    for kind in ('x1m','swapPar','zd1','zd2','zswap','noH'):
        Mv,_=M_fresh(q,kind)
        print(f"   variant {kind:8s}: M={Mv:.4f} |E-M|={abs(E-Mv):.3f}")
