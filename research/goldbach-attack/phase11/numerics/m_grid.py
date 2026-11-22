import sys, numpy as np, mpmath as mp
sys.path.insert(0,'.'); sys.path.insert(0,'../../phase10/numerics')
from fastpipe import Group, make_logtab
from core import compute_E
from mainterm import zeta_q, Xqe
mp.mp.dps=30
PR=np.load('primes_2000000.npy'); PR=PR[PR<=1000000]
a=complex(0.5,0.3); b=complex(0.5,0.7); s=complex(0.6,0.4); t=complex(0.6,0.9)
def Aq(x,y,c,d,q,mode='corr'):
    if mode=='corr': mask=(q % PR)!=0
    elif mode=='all': mask=(PR % q)!=0
    p=PR[mask].astype(float); lp=np.log(p)
    X=np.exp(-(x+d)*lp); Y=np.exp(-(y+c)*lp); G=np.exp(-(c+d)*lp)
    f=((1-G)*(1-X-Y+G))/((1-X)*(1-Y))
    return complex(np.exp(np.sum(np.log1p(f-1.0))))
def zq(sv,q,fac,pow_=1):
    z=complex(mp.zeta(sv))
    for p in fac: z*= (1-mp.power(p,-sv))**pow_
    return z
def Zq(x,y,c,d,q,mode='corr',zpow=1,cache={}):
    fac=Group(q).fac
    return zq(x+y,q,fac,zpow)*zq(c+d,q,fac,zpow)/(zq(x+d,q,fac,zpow)*zq(y+c,q,fac,zpow))*Aq(x,y,c,d,q,mode)
def Xalt(q,e,w,alt=None):
    qq=mp.mpf(q); w=mp.mpc(w.real,w.imag)
    if alt=='w2': return mp.power(qq/mp.pi,mp.mpf(1)/2-(1-w))*mp.gamma((1-(1-w)+e)/2)/mp.gamma(((1-w)+e)/2)
    return mp.power(qq/mp.pi,mp.mpf(1)/2-w)*mp.gamma((1-w+e)/2)/mp.gamma((w+e)/2)
e=14; q=2**e; G=Group(q); logtab=make_logtab(G.x,6)
E=compute_E(G,a,b,s,t,logtab=logtab)
M0,M1=G.M0,G.M1; phist=G.phist
print(f"E={E:.4f} phi*={phist} M0,M1={M0,M1}")
best=[]
for mode in ('corr','all'):
    for zpow in (1,2,0.5,-1):
        Z=Zq(a,b,s,t,q,mode,zpow); Zd=Zq(1-b,1-a,s,t,q,mode,zpow)
        for harm in ('ab','1m','e0','e1','ab_xalt'):
            if harm=='ab': H=sum((M0 if ee==0 else M1)*Xqe(q,ee,a)*Xqe(q,ee,b) for ee in (0,1))
            elif harm=='1m': H=sum((M0 if ee==0 else M1)*Xqe(q,ee,1-b)*Xqe(q,ee,1-a) for ee in (0,1))
            elif harm=='e0': H=M0*Xqe(q,0,a)*Xqe(q,0,b)
            elif harm=='e1': H=M1*Xqe(q,1,a)*Xqe(q,1,b)
            else: H=sum((M0 if ee==0 else M1)*Xalt(q,ee,a,'w2')*Xalt(q,ee,b,'w2') for ee in (0,1))
            for dual in ('std','ab','ts'):
                if dual=='std': Zdd=Zd
                elif dual=='ab': Zdd=Zq(1-a,1-b,s,t,q,mode,zpow)
                else: Zdd=Zq(1-b,1-a,t,s,q,mode,zpow)
                M=complex(phist*Z+H*Zdd)
                d=abs(E-M)
                best.append((abs(M.real-4145.9)+abs(d-114.3), mode,zpow,harm,dual,M,d))
best.sort()
for row in best[:12]:
    score,mode,zpow,harm,dual,M,d=row
    print(f"score={score:.2f} mode={mode} zpow={zpow} H={harm} dual={dual}: M={M:.4f} |M|={abs(M):.4f} |E-M|={d:.3f}")
