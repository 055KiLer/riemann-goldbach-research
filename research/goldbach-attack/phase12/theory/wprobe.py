#!/usr/bin/env python3
"""Probe of Route-C wrap sum W: c_A=sum_{nr=A} n^{-a} mu(r) r^{-s}, W=sum_{A!=B, A==B mod q} c_A conj(d_B).
Compare to trivial bound (1/q)(sum|c|)(sum|d|), plan's X^2/q, and random-phase heuristics."""
import numpy as np, mpmath as mp, math
mp.mp.dps=20
def mobius(n):
    mu=np.zeros(n+1,dtype=np.int64); primes=[]
    is_comp=np.zeros(n+1,dtype=bool)
    mu[1]=1
    for i in range(2,n+1):
        if not is_comp[i]: primes.append(i); mu[i]=-1
        for p in primes:
            if i*p>n: break
            is_comp[i*p]=True
            if i%p==0: mu[i*p]=0; break
            else: mu[i*p]=-mu[i]
    return mu
def build(X, u, v):
    # c_A for A<=X^2 with a=0.5+eta+i u, s=0.5+eta+i v
    sig=0.5+0.1
    a=mp.mpc(sig,u); s=mp.mpc(sig,v)
    Y=X*X; mu=mobius(X)
    c=np.zeros(Y+1,dtype=np.complex128)
    nvals=np.array([complex(mp.power(n,-a)) for n in range(1,X+1)])
    for r in range(1,X+1):
        if mu[r]==0: continue
        w=complex(mp.power(r,-s))*mu[r]
        nn=min(X, Y//r)
        c[r*np.arange(1,nn+1)] += w*nvals[:nn]
    return c
def Wval(c,d,q):
    Y=len(c)-1; idx=np.arange(1,Y+1)%q
    Sc=np.zeros(q,dtype=np.complex128); Sd=np.zeros(q,dtype=np.complex128)
    np.add.at(Sc,idx,c[1:]); np.add.at(Sd,idx,d[1:])
    W=np.vdot(Sd,Sc)-np.vdot(d[1:],c[1:])
    D=np.vdot(d[1:],c[1:])
    return W,D,Sc,Sd
if __name__=="__main__":
    eta=0.1
    for q in [5,7,11,13,17]:
        print(f"--- q={q}",flush=True)
        for Aexp in [1.0,1.5,2.0]:
            X=int(round(q**Aexp))
            if X*X>6_000_000:
                print(f"  A={Aexp}: X={X} skip",flush=True); continue
            c=build(X,0.7,0.2); d=build(X,1.1,0.4)
            W,D,Sc,Sd=Wval(c,d,q)
            absc=np.abs(c[1:]).sum(); absd=np.abs(d[1:]).sum()
            triv=absc*absd/q
            print(f"  A={Aexp}: X={X:5d} |W|={abs(W):.4e} q|W|={abs(W)*q:.3e} |D|={abs(D):.2e} triv={triv:.2e} "
                  f"|W|/triv={abs(W)/triv:.2e} X^2/q={X*X/q:.2e} X^-4eta/sqrt(q)={X**(-4*eta)/math.sqrt(q):.2e}",flush=True)
