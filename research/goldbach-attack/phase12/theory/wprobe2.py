#!/usr/bin/env python3
"""Decompose W = (1/q) c(0) d(0)-conj - D + F, F=(1/q) sum_{h!=0} chat(h) conj(dhat(h)).
chat(h)=sum_A c_A e(hA/q).  Question: how does F scale with q,X?"""
import numpy as np, mpmath as mp, math
mp.mp.dps=20
def mobius(n):
    mu=np.zeros(n+1,dtype=np.int64); primes=[]; isc=np.zeros(n+1,dtype=bool); mu[1]=1
    for i in range(2,n+1):
        if not isc[i]: primes.append(i); mu[i]=-1
        for p in primes:
            if i*p>n: break
            isc[i*p]=True
            if i%p==0: mu[i*p]=0; break
            else: mu[i*p]=-mu[i]
    return mu
def build(X,u,v,eta=0.1):
    sig=0.5+eta; a=mp.mpc(sig,u); s=mp.mpc(sig,v)
    Y=X*X; mu=mobius(X); c=np.zeros(Y+1,dtype=np.complex128)
    nv=np.array([complex(mp.power(n,-a)) for n in range(1,X+1)])
    for r in range(1,X+1):
        if mu[r]==0: continue
        w=complex(mp.power(r,-s))*mu[r]; nn=min(X,Y//r)
        c[r*np.arange(1,nn+1)] += w*nv[:nn]
    return c
def analyze(c,d,q):
    Y=len(c)-1; A=np.arange(1,Y+1)
    # hat c(h)
    chat=np.zeros(q,dtype=np.complex128); dhat=np.zeros(q,dtype=np.complex128)
    for h in range(q):
        e=np.exp(2j*np.pi*h*A/q)
        chat[h]=np.dot(c[1:],e); dhat[h]=np.dot(d[1:],e)
    F=np.vdot(dhat[1:],chat[1:])/q
    sumc=chat[0]; sumd=dhat[0]
    D=np.vdot(d[1:],c[1:])
    # W by residue grouping
    idx=A%q
    Sc=np.zeros(q,dtype=np.complex128); Sd=np.zeros(q,dtype=np.complex128)
    np.add.at(Sc,idx,c[1:]); np.add.at(Sd,idx,d[1:])
    W=np.vdot(Sd,Sc)-D
    return W,F,sumc,sumd,D,chat
if __name__=="__main__":
    eta=0.1
    for q in [5,7,11,13,17,23]:
        print(f"--- q={q}",flush=True)
        for Aexp in [1.0,1.5,2.0,2.5]:
            X=int(round(q**Aexp)); Y=X*X
            if Y>3_000_000: print(f"  A={Aexp}: skip",flush=True); continue
            c=build(X,0.7,0.2); d=build(X,1.1,0.4)
            W,F,sumc,sumd,D,chat=analyze(c,d,q)
            print(f"  A={Aexp}: X={X:5d} |W|={abs(W):.3e} |W-(sumc*conj(sumd)/q-D)|={abs(W-(sumc*np.conj(sumd)/q-D)):.3e} "
                  f"|F|={abs(F):.3e} |sumc|={abs(sumc):.3e} q|W|={abs(W)*q:.3e} |D|={abs(D):.3e} max|chat|={max(abs(chat[1:])) if q>1 else 0:.3e}",flush=True)
