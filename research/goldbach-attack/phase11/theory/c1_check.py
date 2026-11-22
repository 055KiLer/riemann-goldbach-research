#!/usr/bin/env python3
"""Phase-11 Lead check of Route C lemma C1 (fast numpy version):
   1/L(s,chi) = sum_{m<=X} mu(m) chi(m) m^{-s} + tail,
tail exponent should be 1/2-sigma = -eta under GRH (up to log powers).
L(s,chi) via q^{-s} sum_a chi(a) zeta(s,a/q) (mpmath); partial sums in numpy complex128."""
import numpy as np, mpmath as mp
mp.mp.dps = 30
NMAX = int(3e5)

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
MM = np.arange(NMAX+1, dtype=np.float64); MM[0]=1.0

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

def Lval_mp(s,q,g,j):
    n=q-1; tot=mp.mpc(0); cur=1; w=mp.exp(2j*mp.pi*j/n)
    for k in range(n):
        tot += (w**k)*mp.zeta(s, mp.mpf(cur)/q)
        cur = cur*g % q
    return mp.power(q,-s)*tot if isinstance(s,mp.mpc) else tot*mp.mpf(q)**(-s)

def chi_arr(q,g,j):
    n=q-1; d=np.zeros(q,dtype=complex); cur=1; w=np.exp(2j*np.pi*j/n)
    for k in range(n):
        d[cur]=w**k; cur=cur*g%q
    return d

def tails(sigma,t,q,g,j,Xs):
    ch = chi_arr(q,g,j)
    # vector over m=1..NMAX: coeff = mu(m) chi(m) m^{-s}
    m = np.arange(1,NMAX+1)
    coef = MU[1:].astype(complex)*ch[m%q]*np.exp(-(sigma+1j*t)*np.log(m))
    cs = np.cumsum(coef)
    return {X: cs[X-1] for X in Xs}

def run(q):
    g=primroot(q)
    print(f"\n=== q={q} prime, g={g} ===", flush=True)
    for eta in [0.1,0.25]:
        sigma=0.5+eta
        for j in [1,3]:
            s=mp.mpc(sigma,0.5)
            L=Lval_mp(s,q,g,j); invL=1/L
            Xs=[50,100,200,500,1000,2000,5000,10000,20000,50000,100000,200000]
            P=tails(sigma,0.5,q,g,j,Xs)
            print(f" eta={eta} j={j}: |L|={abs(L):.3g} |1/L|={abs(invL):.3g}", flush=True)
            rows=[]
            for X in Xs:
                R=invL-P[X]
                rows.append((X,abs(R)))
                print(f"   X={X:7d} |tail|={abs(R):.3e}", flush=True)
            sel=[(X,a) for X,a in rows if X>=2000]
            xs=np.log([r[0] for r in sel]); ys=np.log([float(r[1]) for r in sel])
            A=np.vstack([xs,np.ones_like(xs)]).T
            slope,inter=np.linalg.lstsq(A,ys,rcond=None)[0]
            print(f"   fit: |tail| ~ C X^{slope:.4f}   (predicted slope = 1/2-sigma = {-eta:.2f})", flush=True)

if __name__=="__main__":
    for q in [337,1009]:
        run(q)
