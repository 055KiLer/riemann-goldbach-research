#!/usr/bin/env python3
"""Phase-11 Lead: family-averaged test of Route C lemma C1.
RMS over ALL primitive chi mod q of |1/L(s,chi) - sum_{m<=X} mu(m) chi(m) m^{-s}|.
L(s,chi) for all chi via Hurwitz-zeta vector + FFT over (Z/q)^* (q prime: cyclic).
Predicted (GRH): RMS tail ~ q^{eps} X^{1/2-sigma} (exponent -eta, up to log powers).
[Lead, phase-11]"""
import numpy as np, mpmath as mp
mp.mp.dps = 30
NMAX = int(5e5)

def sieve_mu(n):
    mu = np.ones(n+1, dtype=np.int8); primes=[]; iscomp=np.zeros(n+1,bool); mu[0]=0
    for i in range(2,n+1):
        if not iscomp[i]: primes.append(i); mu[i]=-1
        for p in primes:
            if i*p>n: break
            iscomp[i*p]=True
            if i%p==0: mu[i*p]=0; break
            mu[i*p]=-mu[i]
    return mu
MU = sieve_mu(NMAX)

def primroot(p):
    m=p-1; fac=[]; d=2; mm=m
    while d*d<=mm:
        if mm%d==0:
            fac.append(d)
            while mm%d==0: mm//=d
        d+=1
    if mm>1: fac.append(mm)
    g=2
    while g<p:
        if all(pow(g,m//q,p)!=1 for q in fac): return g
        g+=1

def L_all(q,g,s):
    """return array over j=0..q-2 of L(s, chi_j), chi_j(g)=w^j, w=e^{2pi i/(q-1)}."""
    n=q-1
    a=[]; idx=[]
    cur=1
    for k in range(n):
        a.append(cur); idx.append(k); cur=cur*g%q
    a=np.array(a)
    vals=np.array([mp.zeta(s, mp.mpf(int(x))/q) for x in a], dtype=complex)
    F=np.fft.ifft(vals)   # F[j] = (1/n) sum_k vals[k] e^{+2pi i jk/n} = (1/n) sum_k vals[k] chi_j(g^k)
    Lv = (q**(-s))*n*F
    return Lv, a, idx

def P_all(q, X, s):
    """return array over j of P_s(chi_j)=sum_{m<=X} mu(m) chi_j(m) m^{-s}."""
    n=q-1
    g=None
    # need dlog map: reconstruct from L_all call? simpler: recompute
    return None

def run(q):
    g=primroot(q); n=q-1
    # dlog table
    dl=np.zeros(q,dtype=np.int64); cur=1
    for k in range(n):
        dl[cur]=k; cur=cur*g%q
    print(f"=== q={q} (prime, g={g}) ===", flush=True)
    Xs=[int(round(q**e)) for e in [0.1,0.25,0.4,0.55,0.7,0.85,1.0]]
    Xs=[X for X in Xs if 2<=X<=NMAX]
    for eta in [0.1,0.25,0.4]:
        s=mp.mpc(0.5+eta, 0.5)
        Lv,_,_=L_all(q,g,s)
        invL=np.array(1.0/Lv, dtype=complex)
        rows=[]
        for X in Xs:
            m=np.arange(1,X+1)
            coef = MU[1:X+1].astype(complex)*np.exp(-complex(0.5+eta,0.5)*np.log(m))
            v=np.zeros(n,dtype=complex)
            for mm,c in zip(m,coef):
                r=mm%q
                if r==0: continue
                v[dl[r]] += c
            # P(chi_j) = sum_k v[k] e^{2pi i jk/n}
            P = np.fft.ifft(v)*n
            tail=invL[1:]-P[1:]
            rms=np.sqrt(np.mean(np.abs(tail)**2))
            invnorm=np.sqrt(np.mean(np.abs(invL[1:])**2))
            rows.append((X,rms))
            print(f" eta={eta} X={X:7d}  RMS_tail={rms:.4e}  RMS/|1/L|avg={rms/invnorm:.3e}", flush=True)
        sel=[r for r in rows if r[0]>=q**0.2]
        if len(sel)>=3:
            xs=np.log([r[0] for r in sel]); ys=np.log([r[1] for r in sel])
            A=np.vstack([xs,np.ones_like(xs)]).T
            slope=np.linalg.lstsq(A,ys,rcond=None)[0][0]
            print(f" --> eta={eta}: fitted RMS tail exponent = {slope:.3f}  (GRH prediction 1/2-sigma = {-eta:.2f})", flush=True)

if __name__=="__main__":
    for q in [337,1009]: run(q)
