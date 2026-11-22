"""Fresh char-by-char mpmath implementation of E_q for q=2^e, 3^e (independent of fastpipe)."""
import sys, numpy as np, mpmath as mp, time, json
mp.mp.dps=30

def units_2e(e):
    q=2**e
    units=np.array([a for a in range(1,q) if a%2==1],dtype=np.int64)
    # decomposition a = (-1)^L 5^M mod 2^e
    n5=2**(e-2)
    fivetab={}; cur=1
    for M in range(n5):
        fivetab[cur]=M; cur=cur*5%q
    L=np.where((units%8==1)|(units%8==5),0,1).astype(np.int64)
    M=np.array([fivetab[(int(u) if L[i]==0 else (-int(u))%q)] for i,u in enumerate(units)],dtype=np.int64)
    return units,L,M,q

def fresh_E_2e(e,us,verbose=False):
    """us = (a,b,s,t) complex; returns (E, chars info)"""
    q=2**e; units,L,M,q=units_2e(e); n5=2**(e-2); A=len(units)
    # cache zeta(u,a/q)
    Z={}
    for u in us:
        Z[u]=np.array([complex(mp.zeta(mp.mpc(u.real,u.imag), mp.mpf(int(a))/q)) for a in units],dtype=complex)
    def Lval(u,chi):
        alpha,beta=chi
        vals=((-1.0)**(alpha*L))*np.exp(2j*np.pi*beta*M/n5)
        return complex(q**(-complex(u)))*(vals@Z[u])
    E=0j
    chars=[(al,be) for al in (0,1) for be in range(n5) if be%2==1]
    for chi in chars:
        alph,beta=chi
        chibar=(alph,(-beta)%n5)
        E+=Lval(us[0],chi)*Lval(us[1],chibar)/(Lval(us[2],chi)*Lval(us[3],chibar))
    # verify primitivity: chi(1+2^{e-1}) = -1 for odd beta
    if verbose:
        a=1+2**(e-1)
        iu=int(np.where(units==a%q)[0][0]) if (a%q) in set(units.tolist()) else None
    return E, len(chars)

def fresh_E_3e(e,us):
    q=3**e; n=(2)*3**(e-1)
    # units: a coprime to 3; primitive root 2 mod 3^e (2 is primitive root mod 3^k)
    g=2
    # dlog table
    tab={}; cur=1
    for j in range(n):
        tab[cur]=j; cur=cur*g%q
    units=np.array([a for a in range(1,q) if a%3!=0],dtype=np.int64)
    dlog=np.array([tab[int(a)] for a in units],dtype=np.int64)
    Z={}
    for u in us:
        Z[u]=np.array([complex(mp.zeta(mp.mpc(u.real,u.imag), mp.mpf(int(a))/q)) for a in units],dtype=complex)
    def Lval(u,k):
        vals=np.exp(2j*np.pi*k*dlog/n)
        return complex(q**(-complex(u)))*(vals@Z[u])
    E=0j
    ks=[k for k in range(n) if k%3!=0]
    for k in ks:
        kb=(-k)%n
        E+=Lval(us[0],k)*Lval(us[1],kb)/(Lval(us[2],k)*Lval(us[3],kb))
    return E,len(ks)

if __name__=='__main__':
    shift=(complex(0.5,0.3),complex(0.5,0.7),complex(0.6,0.4),complex(0.6,0.9))
    out={}
    print("== fresh E for 2^e (Lead shift)",flush=True)
    for e in (8,10,12,14):
        t0=time.time(); E,nch=fresh_E_2e(e,shift)
        print(f"e={e} q={2**e} chars={nch} E_fresh={E:.6f} wall={time.time()-t0:.1f}s",flush=True)
        out[f"2^{e}"]=[float(E.real),float(E.imag),nch]
        json.dump(out,open('cache/fresh_E.json','w'))
    print("== fresh E for 3^e",flush=True)
    for e in (4,5,6):
        t0=time.time(); E,nch=fresh_E_3e(e,shift)
        print(f"e={e} q={3**e} chars={nch} E_fresh={E:.6f} wall={time.time()-t0:.1f}s",flush=True)
        out[f"3^{e}"]=[float(E.real),float(E.imag),nch]
        json.dump(out,open('cache/fresh_E.json','w'))
    print("saved")
