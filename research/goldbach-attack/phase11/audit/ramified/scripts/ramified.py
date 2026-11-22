"""Phase-11b independent third determination of ramified-conductor residual (own code).
E_q = sum^*_{chi prim mod q} L(a,chi)L(b,chibar)/(L(s,chi)L(t,chibar))
M_q = phi* Z_q(a,b;s,t) + H_q(a,b) Z_q(1-b,1-a;s,t)   [GWX (3.2); Z_q from (2.1)-(2.2)]
"""
import sys, os, json, math, time, random
import numpy as np, mpmath as mp
from multiprocessing import Pool
sys.path.insert(0,'.')
from group import Grp, factorize
mp.mp.dps=30

# ---------- mpmath Hurwitz values in parallel ----------
def _work(args):
    q,u,units=args
    mp.mp.dps=30
    u=mp.mpc(u)
    out=np.empty(len(units),dtype=np.complex128)
    qm=mp.mpf(q)
    for i,a in enumerate(units):
        out[i]=complex(mp.zeta(u, mp.mpf(int(a))/qm))
    return out

POOL=None
def zetas(q,u,units,pool,chunk=256):
    chunks=[units[i:i+chunk] for i in range(0,len(units),chunk)]
    res=pool.map(_work,[(q,complex(u),c) for c in chunks])
    return np.concatenate(res)

# ---------- own prime sieve for A_q ----------
def sieve(n):
    s=np.ones(n+1,dtype=bool); s[:2]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]: s[i*i::i]=False
    return np.nonzero(s)[0]
PRIMES=sieve(2_000_000); PD=PRIMES.astype(np.float64); PL=np.log(PD)
def Aq(a,b,c,d,q):
    a,b,c,d=complex(a),complex(b),complex(c),complex(d)
    mask=(q%PRIMES)!=0
    lp=PL[mask]; P=PD[mask]
    X=np.exp(-(a+d)*lp); Y=np.exp(-(b+c)*lp); Z=np.exp(-(c+d)*lp)
    R=(1-Z)*(1-X-Y+Z)/((1-X)*(1-Y))
    return complex(np.exp(np.sum(np.log(R))))
def zeta_q(u,q):
    z=mp.zeta(u)
    for p in factorize(q):
        z*= (1-mp.power(p,-u))
    return z
def Xqe(w,e,q):
    return (mp.mpf(q)/mp.pi)**(mp.mpf(1)/2-w)*mp.gamma((1-w+e)/2)/mp.gamma((w+e)/2)
def Mq(a,b,s,t,q,phistar,Me):
    c,d=s,t
    Zq=lambda aa,bb: zeta_q(aa+bb,q)*zeta_q(c+d,q)/(zeta_q(aa+d,q)*zeta_q(bb+c,q))*Aq(aa,bb,c,d,q)
    Z1=Zq(a,b); Z2=Zq(1-b,1-a)
    H=mp.mpf(0)
    for e in range(2):
        if Me[e]: H+=Me[e]*Xqe(a,e,q)*Xqe(b,e,q)
    return phistar*Z1+H*Z2

# ---------- orthogonality / parity checks ----------
def mobius(n):
    f=factorize(n); 
    if any(e>1 for e in f.values()): return 0
    return (-1)**len(f)
def phi_int(n):
    r=n
    for p in factorize(n): r=r//p*(p-1)
    return r
def divisors(n):
    ds=[1]
    for p,e in factorize(n).items():
        ds=[d*p**j for d in ds for j in range(e+1)]
    return sorted(ds)
def orthogonality_check(g):
    q=g.q; us=[1]
    for p in factorize(q):
        m=q//p
        if m>1:
            x=1+m
            if math.gcd(x,q)==1: us.append(x)
    us.append(int(g.units[-1]))  # a large unit
    res=[]
    for u in us:
        # sum over primitive chi of chi(u)
        idx=g.uindex[u%q]
        V=g.charvals_at_unit_indices(np.array([idx]))[:,0]
        s=complex(np.sum(V[g.prim]))
        # formula sum_{d|q} mu(q/d) phi(d) 1_{u=1 mod d}
        f=sum(mobius(q//d)*phi_int(d) for d in divisors(q) if (u-1)%d==0)
        res.append(dict(u=int(u),sum_prim=complex(s),formula=float(f),err=abs(s-f)))
    return res

# ---------- L-values via DFT ----------
def Lvalues(g,u,pool):
    vals=zetas(g.q,u,g.units,pool)
    Fplus,Fminus=g.dft_L(vals)
    qpow=np.exp(-complex(u)*math.log(g.q))
    return qpow*Fplus, qpow*Fminus

def E_of(g,a,b,s,t,pool):
    La,_=Lvalues(g,a,pool)
    _,Lbbar=Lvalues(g,b,pool)
    Ls,_=Lvalues(g,s,pool)
    _,Ltbar=Lvalues(g,t,pool)
    prim=g.prim
    with np.errstate(all='ignore'):
        term=La*Lbbar/(Ls*Ltbar)
        ok=prim & np.isfinite(term) & (np.abs(term)<1e12)
        return complex(np.sum(term[ok])), bool(np.all(ok[prim]))

# ---------- validation helpers ----------
def direct_L(g,u,chi_idx,N=300000):
    tot=0j; q=g.q
    for n in range(1,N+1):
        if math.gcd(n,q)!=1: continue
        x=n%q; i=g.uindex[x]
        # chi_k(x) from exponent dot
        phase=sum(float(g.kvecs[chi_idx][j])*float(g.exps[i][j])/float(g.orders[j]) for j in range(g.r)) if g.r else 0.0
        tot+=np.exp(2j*np.pi*phase)*n**(-u)
    return tot

# ---------- main experiment ----------
def run_families(pool, families, shifts_generic, shifts_near, outfile):
    results=[]
    for label,qs in families.items():
        for q in qs:
            g=Grp(q); t0=time.time()
            orth=orthogonality_check(g)
            # L validation: direct Dirichlet at u=1.5+0.8i for a few chars
            uval=mp.mpc(1.5,0.8)
            Ld,_=Lvalues(g,uval,pool)
            chars=[np.nonzero(g.prim)[0][0], 1, g.nchars-1]
            print(f"q={q} charidx={chars}",flush=True)
            direct_errs=[]
            for k in chars:
                try:
                    d=direct_L(g,uval,k)
                    direct_errs.append(float(abs(Ld[k]-d)/abs(d)))
                except Exception as e:
                    direct_errs.append(None)
            # functional equation check for first primitive char
            kp=int(np.nonzero(g.prim)[0][0])
            epar=int(np.real(g.charvals_at_unit_indices(np.array([g.uindex[q-1]]))[kp,0])>0.5)
            u0=mp.mpc(0.5,0.7)
            Lp,_=Lvalues(g,u0,pool)
            Lm,_=Lvalues(g,1-u0,pool)   # L(1-u, chi) ; need chibar -> other array
            _,Lmb=Lvalues(g,1-u0,pool)
            def compl(u,L,e):
                u=mp.mpc(u)
                return mp.power(mp.mpf(q)/mp.pi,(u+e)/2)*mp.gamma((u+e)/2)*mp.mpc(L)
            Lam1=abs(compl(u0,Lp[kp],epar))
            Lam2=abs(compl(1-u0,Lmb[kp],epar))
            rec=dict(q=int(q),label=label,phi=g.phi,phi_star=g.phistar,Me=g.Me,
                     orth=orth,dir_errs=direct_errs,fe_check=float(abs(Lam1-Lam2)/max(1e-30,Lam1)),
                     t_build=time.time()-t0)
            # shifts
            rows=[]
            for cls,shifts in [('generic',shifts_generic),('nearpole',shifts_near)]:
                for (ia,ib,is_,it_) in shifts:
                    a=mp.mpc(0.5,ia); b=mp.mpc(0.5,ib); s=mp.mpc(0.6,is_); t=mp.mpc(0.6,it_)
                    t1=time.time()
                    Eq,ok=E_of(g,a,b,s,t,pool)
                    M=Mq(a,b,s,t,q,g.phistar,g.Me)
                    R=abs(mp.mpc(Eq)-M)
                    rows.append(dict(cls=cls,ia=ia,ib=ib,is_=is_,it_=it_,E=str(Eq)[:22],M=mp.nstr(M,18),
                                     absR=float(R),Eabs=abs(Eq),Mabs=float(abs(M)),ok=ok,t=time.time()-t1))
                    print(f"  q={q} {cls} ia={ia:+.2f} ib={ib:+.2f}: |E|={abs(Eq):.3e} |M|={float(abs(M)):.3e} |E-M|={float(R):.4e} /sqrtq={float(R)/math.sqrt(q):8.3f} /(q/p)={float(R)/(q/max(factorize(q),key=lambda p:factorize(q)[p])):8.4f}",flush=True)
            rec['rows']=rows; results.append(rec)
            json.dump(results,open(outfile,'w'),indent=1,default=str)
    return results

if __name__=='__main__':
    random.seed(20261121)
    # 6 generic shifts, |Im|<=2, avoid a+b~1 (Im a + Im b >=0.5)
    shifts_generic=[]
    while len(shifts_generic)<6:
        ia=round(random.uniform(-2,2),3); ib=round(random.uniform(-2,2),3)
        if abs(ia+ib)<0.5: continue
        is_=round(random.uniform(-2,2),3); it_=round(random.uniform(-2,2),3)
        shifts_generic.append((ia,ib,is_,it_))
    # near-pole class: Im b = -Im a + eps
    shifts_near=[]
    for (ia,eps) in [(0.7,0.1),(1.3,0.05),(-0.9,0.1),(1.9,0.05)]:
        shifts_near.append((ia,-ia+eps,0.4,1.7))
    families={
      '2^e':[2**e for e in (8,10,12,14,16)],
      '3^e':[3**e for e in (3,4,5,6)],
      '4p':[4*1009,4*2503,4*4001],
      '8p':[8*1259,8*2503],
      '9p':[9*1013,9*1009],
    }
    with Pool(14) as pool:
        res=run_families(pool,families,shifts_generic,shifts_near,'../logs/ramified_results.json')
    print('DONE',len(res))
