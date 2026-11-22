"""Independent validation (not using fastpipe / phase-11 corrected code) for prime q:
   (A) full primitive-character sum R_q via primitive-root character table (numpy complex128,
       mpmath Hurwitz zeta values) -- compared with fastpipe result;
   (B) M_q via fresh mpmath implementation of the CFZ formula with the CORRECT A_q mask
       (q%p != 0), primes up to 2e5 (A_q tail < 1e-10) -- compared with phase-11b corrected.M_correct.
"""
import sys, os, math, time
import numpy as np, mpmath as mp
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,HERE); sys.path.insert(0,os.path.abspath(os.path.join(HERE,'..','..','phase10','numerics')))
from ratios_lib import Group, make_logtab, compute_E, M_correct
mp.mp.dps=30

def primes_upto(n):
    s=np.ones(n+1,bool); s[:2]=False
    for p in range(2,int(n**0.5)+1):
        if s[p]: s[p*p::p]=False
    return np.nonzero(s)[0]

PR=primes_upto(200000)

def primitive_root(q):
    # factor q-1
    m=q-1; fac=[]; p=2
    while p*p<=m:
        if m%p==0:
            fac.append(p)
            while m%p==0: m//=p
        p+=1
    if m>1: fac.append(m)
    for g in range(2,q):
        if all(pow(g,(q-1)//p,q)!=1 for p in fac): return g
    raise RuntimeError

def direct_R(q,us):
    """R_q = sum over nontrivial (primitive) chars mod prime q, exact character table."""
    g=primitive_root(q); n=q-1
    dlog=np.zeros(q,dtype=np.int64); cur=1
    for k in range(n):
        dlog[cur]=k; cur=cur*g%q
    units=np.arange(1,q); dl=dlog[units]
    Z=[]
    for u in us:
        Z.append(np.array([complex(mp.zeta(mp.mpc(u.real,u.imag), mp.mpf(int(a))/q)) for a in units],dtype=complex))
    a,b,s,t=us
    E=0j
    for k in range(1,n):
        ph=np.exp(2j*np.pi*k*dl/n)
        phb=np.exp(-2j*np.pi*k*dl/n)
        La=q**(-a)*(ph@Z[0]); Lb=q**(-b)*(phb@Z[1])
        Ls=q**(-s)*(ph@Z[2]); Lt=q**(-t)*(phb@Z[3])
        E+=La*Lb/(Ls*Lt)
    return complex(E)

def zeta_q_mp(s,q):
    z=mp.zeta(s)
    for p in PR:
        if q%p==0: z*=(1-mp.power(p,-s))
    return z
def Aq_mp(a,b,c,d,q):
    val=mp.mpf(1)
    for p in PR:
        if q%p==0: continue
        x=mp.power(p,-(a+d)); y=mp.power(p,-(b+c)); z=mp.power(p,-(c+d))
        val*=(1-z)*(1-x-y+z)/((1-x)*(1-y))
    return val
def X_mp(q,e,w):
    w=mp.mpc(w.real,w.imag); qq=mp.mpf(q)
    return mp.power(qq/mp.pi,mp.mpf(1)/2-w)*mp.gamma((1-w+e)/2)/mp.gamma((w+e)/2)
def direct_M(q,a,b,s,t):
    def Zq(x,y,c,d):
        return zeta_q_mp(x+y,q)*zeta_q_mp(c+d,q)/(zeta_q_mp(x+d,q)*zeta_q_mp(y+c,q))*Aq_mp(x,y,c,d,q)
    n=q-1
    # parity of nontrivial chars: chi_k(-1)=(-1)^k
    M0=sum(1 for k in range(1,n) if k%2==0); M1=n-1-M0
    H=sum((M0 if e==0 else M1)*X_mp(q,e,a)*X_mp(q,e,b) for e in (0,1))
    return complex((n-1)*Zq(a,b,s,t)+H*Zq(1-b,1-a,s,t)), M0,M1

if __name__=='__main__':
    shifts=[(0.3,0.7,0.4,0.9,0.05),(1.1,-0.6,0.5,-1.2,0.05),(-0.4,1.3,1.0,0.2,0.05)]
    for q in (211,1009,5003):
        G=Group(q); logtab=make_logtab(G.x,10)
        print(f"### q={q}",flush=True)
        for (A,B,S,U,eta) in shifts:
            for config,eta_use in (('hyp11',eta),('shifted',eta)):
                if config=='hyp11':
                    a=complex(0.5,A); b=complex(0.5,B)
                else:
                    a=complex(0.5+eta_use,A); b=complex(0.5+eta_use,B)
                s=complex(0.5+eta_use,S); t=complex(0.5+eta_use,U)
                us=(a,b,s,t)
                t0=time.time(); Ed=direct_R(q,us); tf=time.time()-t0
                Ef=compute_E(G,a,b,s,t,logtab=logtab)
                Mf,_=M_correct(G,a,b,s,t)
                Md,M0,M1=direct_M(q,a,b,s,t)
                print(f" {config} shift={shifts[0] if False else (A,B,S,U)}: |Ed-Ef|/|E|={abs(Ed-Ef)/abs(Ef):.2e} |Mf-Md|/|M|={abs(Mf-Md)/abs(Md):.2e} M0,M1={M0,M1} direct_time={tf:.1f}s",flush=True)
