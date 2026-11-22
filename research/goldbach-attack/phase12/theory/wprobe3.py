#!/usr/bin/env python3
"""Decisive test: does F=(1/q)sum_{h!=0} chat(h)conj(dhat(h)) approximate the Euler product D_full=sum_A c_A conj(d_A)?
If yes: Route-C main term survives wrap, and error ~ (q-1)(F-D_full)+truncation."""
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
def Dfull(u1,v1,u2,v2,eta=0.1,nprimes=200000):
    # D_full=sum_A c_A conj(d_A), c_A=A^{-a} prod_{p|A}(1-p^{a-s}); d likewise (b,t)
    sig=0.5+eta
    a=mp.mpc(sig,u1); s=mp.mpc(sig,v1); b=mp.mpc(sig,u2); t=mp.mpc(sig,v2)
    def primes_upto(n):
        sieve=np.ones(n+1,dtype=bool); sieve[:2]=False
        for i in range(2,int(n**0.5)+1):
            if sieve[i]: sieve[i*i::i]=False
        return np.nonzero(sieve)[0]
    P=primes_upto(nprimes)
    prod=mp.mpc(1)
    for p in P:
        lp=mp.log(p)
        pa=mp.e**(-a*lp); ps=mp.e**(-s*lp); pb=mp.e**(-b*lp); pt=mp.e**(-t*lp)
        # local: sum_{e>=0} c_{p^e} conj(d_{p^e}); c_{p^0}=1
        ca1=pa*(1-pa/ps)  # e=1: p^{-a}(1-p^{a-s})
        db1=pb*(1-pb/pt)
        loc=mp.mpc(1)+ca1*mp.conj(db1)/(1-pa*pb)  # geometric: for e>=1, c_{p^e}=p^{-ae}(1-p^{a-s}), product = p^{-e(a+b)}(1-p^{a-s})(1-p^{b-t}); sum e>=1 = (1-sa)(1-sb)/(1-p^{-a-b})
        prod*=loc
    return prod
if __name__=="__main__":
    eta=0.1
    print("D_full =",mp.nstr(Dfull(0.7,0.2,1.1,0.4),10),flush=True)
    for q in [7,11,17,23]:
        print(f"--- q={q}",flush=True)
        for Aexp in [1.0,1.5,2.0]:
            X=int(round(q**Aexp)); Y=X*X
            if Y>3_000_000: continue
            c=build(X,0.7,0.2); d=build(X,1.1,0.4)
            A=np.arange(1,Y+1); chat=np.zeros(q,dtype=np.complex128); dhat=np.zeros(q,dtype=np.complex128)
            for h in range(q):
                e=np.exp(2j*np.pi*h*A/q); chat[h]=np.dot(c[1:],e); dhat[h]=np.dot(d[1:],e)
            F=np.vdot(dhat[1:],chat[1:])/q
            sc=chat[0]; sd=dhat[0]
            Dtr=np.vdot(d[1:],c[1:])
            # exact E (main piece, ignoring coprimality): (q-1)*sum_{A==B mod q} - sum_all
            idx=A%q; Sc=np.zeros(q,dtype=np.complex128); Sd=np.zeros(q,dtype=np.complex128)
            np.add.at(Sc,idx,c[1:]); np.add.at(Sd,idx,d[1:])
            Sb=np.dot(Sc,np.conj(Sd))
            E=(q-1)*Sb - sc*np.conj(sd)
            print(f"  A={Aexp}: X={X:5d} |F|={abs(F):.4e} |Dtr|={abs(Dtr):.4e} |F-Dtr|={abs(F-Dtr):.3e}"
                  f" |E-(q-1)Dtr+(sc sd)|={abs(E-(q-1)*Dtr+sc*np.conj(sd)):.3e}",flush=True)
