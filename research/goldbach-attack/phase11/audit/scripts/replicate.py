"""Independent replication of H_Ratios error scale (own code; formula from phase10 report §2).
E_q = sum^*_{chi primitive mod q} L(a,chi) L(b,chibar) / (L(s,chi) L(t,chibar))
M_q = phi*(q) Z_q(a,b;s,t) + H_q(a,b) Z_q(1-b,1-a;s,t)
Z_q(a,b;c,d)=zeta_q(a+b)zeta_q(c+d)/(zeta_q(a+d)zeta_q(b+c))*A_q, c=s,d=t
A_q=prod_{p∤q}(1-p^{-c-d})(1-p^{-a-d}-p^{-b-c}+p^{-c-d})/((1-p^{-a-d})(1-p^{-b-c}))
H_q=sum_e M_e(q) X_{q,e}(a)X_{q,e}(b), X_{q,e}(w)=(q/pi)^{1/2-w} Gamma((1-w+e)/2)/Gamma((w+e)/2)
"""
import numpy as np, mpmath as mp, math, json, time, sys
sys.path.insert(0,'.')
from charlib import UnitGroup, factorize
from math import gcd

mp.mp.dps=30
# own prime sieve
def sieve(n):
    s=np.ones(n+1,dtype=bool); s[:2]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]: s[i*i::i]=False
    return np.nonzero(s)[0]
PRIMES=sieve(2_000_000)
PL=np.log(PRIMES.astype(np.float64))
PD=PRIMES.astype(np.float64)

def isprime(n):
    if n<2: return False
    for p in [2,3,5,7,11,13,17,19,23,29,31,37]:
        if n%p==0: return n==p
    d=n-1; r=0
    while d%2==0: d//=2; r+=1
    for a in [2,3,5,7,11,13,17,19,23,29,31,37]:
        x=pow(a,d,n)
        if x in (1,n-1): continue
        for _ in range(r-1):
            x=x*x%n
            if x==n-1: break
        else: return False
    return True

def Aq(a,b,c,d,q):
    # product over primes p<=2e6, p not|q ; complex128 log-sum
    a,b,c,d=complex(a),complex(b),complex(c),complex(d)
    mask=(q % PRIMES)!=0
    n=mask.sum()
    lp=PL[mask]; P=PD[mask]
    X=np.exp(-(a+d)*lp); Y=np.exp(-(b+c)*lp); Z=np.exp(-(c+d)*lp)
    R=(1-Z)*(1-X-Y+Z)/((1-X)*(1-Y))
    return np.exp(np.sum(np.log(R)))

def zeta_q(u,qfac):
    z=mp.zeta(u)
    for p in qfac:
        z*= (1-mp.power(p,-u))
    return z

def Xqe(w,e,q):
    return (mp.mpf(q)/mp.pi)**(mp.mpf(1)/2-w)*mp.gamma((1-w+e)/2)/mp.gamma((w+e)/2)

def Mq(a,b,s,t,q,phistar,Me,fac, A_cache=None):
    # a,b,s,t: mpmath complex
    c,d=s,t
    zq=lambda u: zeta_q(u,fac)
    A1=Aq(a,b,c,d,q) if A_cache is None else A_cache[0]
    Z1=zq(a+b)*zq(c+d)/(zq(a+d)*zq(b+c))*A1
    a2=1-b; b2=1-a
    A2=Aq(a2,b2,c,d,q) if A_cache is None else A_cache[1]
    Z2=zq(a2+b2)*zq(c+d)/(zq(a2+d)*zq(b2+c))*A2
    H=mp.mpf(0)
    for e in range(2):
        if Me[e]>0:
            H+= Me[e]*Xqe(a,e,q)*Xqe(b,e,q)
    return phistar*Z1 + H*Z2, dict(Z1=Z1,Z2=Z2,H=H,A1=A1,A2=A2)

def zeta_vals(g,u,q):
    arr=np.empty(g.phi,dtype=np.complex128)
    qm=mp.mpf(q)
    for i,x in enumerate(g.units):
        arr[i]=complex(mp.zeta(u, qm and mp.mpf(int(x))/qm))
    return arr

def run_case(q, eta_shiftsets):
    """eta_shiftsets: list of (eta,(ia,ib,is,it)). Own code; caches per-shiftset a,b zeta arrays."""
    g=UnitGroup(q); fac=list(factorize(q).keys())
    prim=g.prim; Me=g.Me; phistar=g.phistar
    LQ=math.log(q)
    out=[]; t0=time.time()
    # cache a,b arrays per (ia,ib)
    cache={}
    for eta,(ia,ib,is_,it_) in eta_shiftsets:
        a=mp.mpc(0.5,ia); b=mp.mpc(0.5,ib); s=mp.mpc(0.5+eta,is_); t=mp.mpc(0.5+eta,it_)
        key=(ia,ib)
        if key not in cache:
            ba=zeta_vals(g,a,q); bb=zeta_vals(g,b,q)
            La=(g.T@ba)*np.exp(-complex(a)*LQ); Lb=(g.T.conj()@bb)*np.exp(-complex(b)*LQ)
            cache[key]=(La,Lb)
        La,Lb=cache[key]
        bs=zeta_vals(g,s,q); bt=zeta_vals(g,t,q)
        Ls=(g.T@bs)*np.exp(-complex(s)*LQ); Lt=(g.T.conj()@bt)*np.exp(-complex(t)*LQ)
        with np.errstate(all='ignore'):
            denom=Ls*Lt; nums=La*Lb
            ok=prim & np.isfinite(denom) & (np.abs(denom)>1e-300)
            Eq=complex(np.sum((nums/denom)[ok]))
            fullok=bool(np.all(ok[prim]))
        M,parts=Mq(a,b,s,t,q,phistar,Me,fac)
        E=mp.mpc(Eq); R=E-M; absR=abs(R)
        out.append(dict(q=int(q),eta=float(eta),ia=float(ia),ib=float(ib),is_=float(is_),it_=float(it_),
                        E=mp.nstr(E,20),M=mp.nstr(M,20),absR=mp.nstr(absR,15),
                        ratio=float(absR/math.sqrt(q)), rel=float(absR/abs(M)) if M!=0 else None,
                        H=mp.nstr(parts['H'],12),Z1=mp.nstr(parts['Z1'],12),Z2=mp.nstr(parts['Z2'],12),
                        ok=fullok))
    return dict(q=int(q),phi=g.phi,phistar=phistar,Me=Me,t=time.time()-t0,rows=out)

if __name__=='__main__':
    shiftsets=[(0.7,1.3,0.4,2.1),(2.6,-1.1,1.7,0.3),(-2.4,0.9,2.2,1.5)]
    etas=[0.05,0.1,0.2]
    qs=[307,503,1009,2003,1001,1155,1365,2079,3003,3465,420,1260,1680,2000,2520,3600,330]
    allout=[]; t0=time.time()
    for q in qs:
        es=[(eta,ss) for eta in etas for ss in shiftsets]
        res=run_case(q,es); allout.append(res)
        ratios=[r['ratio'] for r in res['rows'] if r.get('ok')]
        print(f"q={q:5d} phi={res['phi']:4d} phi*={res['phistar']:5d} Me={res['Me']}  median ratio={np.median(ratios) if ratios else None}  max={max(ratios) if ratios else None}  time={res['t']:.1f}s",flush=True)
        json.dump(allout,open('../logs/A_results.json','w'),indent=1)
    print('TOTAL',time.time()-t0)
