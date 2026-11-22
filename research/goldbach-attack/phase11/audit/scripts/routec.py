"""Route-C feasibility probe (own code): E_q^{(X)}=sum^*_chi L(a,chi)L(b,chibar) P_s(chi) conj(P_t(chi)),
P_u(chi)=sum_{m<=X} mu(m)chi(m)m^{-u}. Compare to E_q (full ratio sum) and M_q (H_Ratios main term)."""
import sys, numpy as np, mpmath as mp, math, json, time
sys.path.insert(0,'.')
import replicate as R   # own module
from charlib import UnitGroup, factorize
mp.mp.dps=30
LQ=lambda q: math.log(q)

def sieve_mu(n):
    mu=np.zeros(n+1,dtype=np.int64); mu[1]=1
    primes=[]; iscomp=np.zeros(n+1,dtype=bool)
    for i in range(2,n+1):
        if not iscomp[i]: primes.append(i); mu[i]=-1
        for p in primes:
            if i*p>n: break
            iscomp[i*p]=True
            if i%p==0: mu[i*p]=0; break
            mu[i*p]=-mu[i]
    return mu

def Lvec(g,u,q):
    arr=R.zeta_vals(g,mp.mpc(u),q)
    return arr

def run(q, eta, ia, ib, it_=0.0, delta_list=(0.1,0.2,0.3,0.4), X_extra=(5,10,20,50,100,300,1000,3000), Nmax=4000):
    g=UnitGroup(q); prim=g.prim; phistar=g.phistar; Me=g.Me; fac=list(factorize(q).keys())
    a=mp.mpc(0.5,ia); b=mp.mpc(0.5,ib); s=mp.mpc(0.5+eta,0.0); t=mp.mpc(0.5+eta,it_)
    LQq=math.log(q)
    ba=R.zeta_vals(g,a,q); bb=R.zeta_vals(g,b,q); bs=R.zeta_vals(g,s,q); bt=R.zeta_vals(g,t,q)
    La=(g.T@ba)*np.exp(-complex(a)*LQq); Lb=(g.T.conj()@bb)*np.exp(-complex(b)*LQq)
    Ls=(g.T@bs)*np.exp(-complex(s)*LQq); Ltbar=(g.T.conj()@bt)*np.exp(-complex(t)*LQq)  # L(t,chibar)
    # E_q (target) and alternative with t -> conj(t)
    E_q=complex(np.sum((La*Lb/(Ls*Ltbar))[prim]))
    if it_!=0:
        bt2=R.zeta_vals(g,mp.mpc(t.real,-it_),q)
        Lt2=(g.T.conj()@bt2)*np.exp(-complex(t.real,-it_)*LQq)
        E_q_alt=complex(np.sum((La*Lb/(Ls*Lt2))[prim]))
    else:
        E_q_alt=E_q
    M,parts=R.Mq(a,b,s,t,q,phistar,Me,fac)
    # Möbius sieve and P_u checkpoints
    mu=sieve_mu(Nmax)
    Xs=sorted(set([max(2,int(round(q**d))) for d in delta_list]+[x for x in X_extra if x<=Nmax]))
    idx_map={int(m%q):g.uindex[int(m%q)] for m in range(1,min(Nmax,q*2)+1) if math.gcd(m,q)==1}
    P_s=np.zeros(g.nchars,dtype=np.complex128); P_t=np.zeros(g.nchars,dtype=np.complex128)
    P_t_fix=np.zeros(g.nchars,dtype=np.complex128)
    out=[]; m=1
    for X in Xs:
        while m<=X:
            if mu[m]!=0 and math.gcd(m,q)==1:
                idx=g.uindex[m%q]
                cs=complex(mp.mpf(int(mu[m]))*mp.power(m,-s))
                ct=complex(mp.mpf(int(mu[m]))*mp.power(m,-t))
                P_s+=cs*g.T[:,idx]; P_t+=ct*g.T[:,idx]
                P_t_fix+=ct*g.T.conj()[:,idx]
            m+=1
        EX=complex(np.sum((La*Lb*P_s*np.conj(P_t))[prim]))
        # fix variant: P_t evaluated with chibar directly (sum mu(m) chibar(m) m^{-t})
        P_t_bar=P_t_fix  # filled below
        EXfix=complex(np.sum((La*Lb*P_s*P_t_bar)[prim]))
        out.append(dict(X=int(X), EX=mp.nstr(mp.mpc(EX),18), E_q=mp.nstr(mp.mpc(E_q),18),
                        dE=float(abs(mp.mpc(EX)-mp.mpc(E_q))), dM=float(abs(mp.mpc(EX)-M)),
                        dEfix=float(abs(mp.mpc(EXfix)-mp.mpc(E_q))),
                        dEalt=float(abs(mp.mpc(EX)-mp.mpc(E_q_alt))),
                        absEq=float(abs(mp.mpc(E_q))), absM=float(abs(M)),
                        floorEM=float(abs(mp.mpc(E_q)-M))))
    return dict(q=int(q),eta=float(eta),ia=float(ia),ib=float(ib),it=float(it_),phi=g.phi,phistar=phistar,
                Me=Me,E_q=mp.nstr(mp.mpc(E_q),20),E_q_alt=mp.nstr(mp.mpc(E_q_alt),20),M=mp.nstr(M,20),
                rows=out)

def fit_slope(rows,key):
    pts=[(math.log(r['X']),math.log(r[key])) for r in rows if r[key]>0]
    if len(pts)<4: return None
    x=np.array([p[0] for p in pts]); y=np.array([p[1] for p in pts])
    A=np.vstack([np.ones_like(x),x]).T
    return float(np.linalg.lstsq(A,y,rcond=None)[0][1])

if __name__=='__main__':
    cases=[(503,0.1,0.7,1.3,0.0),(503,0.3,0.7,1.3,0.0),(503,0.48,0.7,1.3,0.0),
           (1001,0.1,0.7,1.3,0.0),(1001,0.3,0.7,1.3,0.0),(1001,0.48,0.7,1.3,0.0),
           (2000,0.1,0.7,1.3,0.0),(2000,0.3,0.7,1.3,0.0),(2000,0.48,0.7,1.3,0.0),
           (1001,0.3,0.7,1.3,0.8),(1001,0.3,0.7,1.3,2.0)]  # last: Im t != 0 -> structural test
    allout=[]; t0=time.time()
    for c in cases:
        r=run(*c); r['slope_dE']=fit_slope(r['rows'],'dE'); r['slope_dM']=fit_slope(r['rows'],'dM')
        r['slope_dEalt']=fit_slope(r['rows'],'dEalt')
        allout.append(r)
        print(f"q={r['q']} eta={r['eta']} it={r['it']} phi*={r['phistar']} floor|E-M|={r['rows'][0]['floorEM']:.3g} slope_dE={r['slope_dE']} slope_dM={r['slope_dM']} slope_dEfix={fit_slope(r['rows'],'dEfix')} (naive -eta={-r['eta']})",flush=True)
        for row in r['rows'][-5:]:
            print(f"   X={row['X']:6d} dE={row['dE']:10.4g} dM={row['dM']:10.4g} dEalt={row['dEalt']:10.4g} dEfix={row['dEfix']:10.4g}",flush=True)
        json.dump(allout,open('../logs/B_results.json','w'),indent=1)
    print('TOTAL',time.time()-t0)
