"""Independent (fast) recomputation of M_q for q=2^e + variant search, with explicit parity counts."""
import sys, numpy as np, mpmath as mp, json
sys.path.insert(0,'.'); sys.path.insert(0,'../../phase10/numerics')
from fastpipe import Group, make_logtab, factorize
from core import compute_E, compute_M
mp.mp.dps=30
PR=np.load('primes_2000000.npy'); PR=PR[PR<=1000000]
a=complex(0.5,0.3); b=complex(0.5,0.7); s=complex(0.6,0.4); t=complex(0.6,0.9)

def zeta_q(sv,q,fac):
    z=mp.zeta(sv)
    for p in fac: z*=(1-mp.power(p,-sv))
    return complex(z)
def Aq_np(x,y,c,d,q,swap=False):
    mask=(PR%q!=0); p=PR[mask].astype(float); lp=np.log(p)
    X=np.exp(-(complex(x+d))*lp); Y=np.exp(-(complex(y+c))*lp); G=np.exp(-(complex(c+d))*lp)
    if swap:
        X=np.exp(-(complex(x+c))*lp); Y=np.exp(-(complex(y+d))*lp)
    f=((1-G)*(1-X-Y+G))/((1-X)*(1-Y))
    return complex(np.exp(np.sum(np.log1p(f-1.0))))
def Zq(x,y,c,d,q,fac,swap=False):
    return zeta_q(x+y,q,fac)*zeta_q(c+d,q,fac)/(zeta_q(x+d,q,fac)*zeta_q(y+c,q,fac))*Aq_np(x,y,c,d,q,fac and swap)
def X(q,e,w):
    q=mp.mpf(q); w=mp.mpc(w.real,w.imag)
    return mp.power(q/mp.pi, mp.mpf(1)/2-w)*mp.gamma((1-w+e)/2)/mp.gamma((w+e)/2)

def explicit_parity_counts(q):
    """explicitly enumerate primitive chars and evaluate chi(-1) via mpmath roots of unity"""
    fac=factorize(q)
    if q%2==0 and fac.get(2,0)==1: return 0,0
    M0=M1=0
    import itertools
    # only handle pure 2^e here (task focus)
    e=fac[2]
    if e==2:
        return 0,1
    n5=2**(e-2)
    for al in (0,1):
        for be in range(n5):
            if be%2==0: continue
            # chi(-1): -1 = (-1)^1 5^0 -> (-1)^al
            val=(-1)**al
            if val==1: M0+=1
            else: M1+=1
    return M0,M1

def M_variant(q,kind='ours',verbose=False):
    G=Group(q); fac=G.fac
    M0x,M1x=explicit_parity_counts(q)
    M0,M1=G.M0,G.M1
    if verbose: print(f"q={q}: explicit M0,M1={M0x,M1x} vs Group {M0,M1}")
    phist=M0+M1
    Z=Zq(a,b,s,t,q,fac); Zd=Zq(1-b,1-a,s,t,q,fac)
    def H(args,counts=(M0,M1)):
        return sum((counts[0] if e==0 else counts[1])*X(q,e,args[0])*X(q,e,args[1]) for e in (0,1))
    base=complex(phist*Z)
    out={}
    out['ours']=base+complex(H((a,b))*Zd)
    out['x1m']=base+complex(H((1-b,1-a))*Zd)
    out['swapPar']=base+complex(H((a,b),(M1,M0))*Zd)
    out['zd_ab']=base+complex(H((a,b))*Zq(1-a,1-b,s,t,q,fac))
    out['zd_ts']=base+complex(H((a,b))*Zq(1-b,1-a,t,s,q,fac))
    out['zswap']=complex(phist*Zq(a,b,s,t,q,fac,swap=True)+H((a,b))*Zq(1-b,1-a,s,t,q,fac,swap=True))
    out['noH']=base
    return out,(Z,Zd)

if __name__=='__main__':
    res={}
    for e in (10,12,14):
        q=2**e; G=Group(q); logtab=make_logtab(G.x,6)
        E=compute_E(G,a,b,s,t,logtab=logtab)
        Mcore=compute_M(G,a,b,s,t,{})
        variants,(Z,Zd)=M_variant(q,verbose=True)
        print(f"e={e}: E={E:.6f} coreM={Mcore:.6f} Z={Z:.6f} Zd={Zd:.6f}",flush=True)
        for k,v in variants.items():
            print(f"   {k:8s}: M={v:.6f}  |E-M|={abs(E-v):.3f}",flush=True)
        res[e]=dict(E=[E.real,E.imag],Mcore=[Mcore.real,Mcore.imag],variants={k:[v.real,v.imag] for k,v in variants.items()})
    json.dump(res,open('cache/m_variants.json','w'))
