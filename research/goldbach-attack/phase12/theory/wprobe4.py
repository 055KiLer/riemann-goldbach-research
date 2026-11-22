#!/usr/bin/env python3
"""Does the Fourier fluctuation F=(1/q)sum_{h!=0} chat(h)conj(dhat(h)) decay as X grows (fixed q)?
Also: chat(h) sizes. If F ~ X^{-delta}, wrap error via main-term extension could push c. """
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
def Fval(c,d,q):
    Y=len(c)-1; A=np.arange(1,Y+1)
    chat=np.zeros(q,dtype=np.complex128); dhat=np.zeros(q,dtype=np.complex128)
    for h in range(1,q):
        e=np.exp(2j*np.pi*h*A/q); chat[h]=np.dot(c[1:],e); dhat[h]=np.dot(d[1:],e)
    return np.vdot(dhat[1:],chat[1:])/q, np.abs(chat[1:]).max(), np.vdot(d[1:],c[1:])
if __name__=="__main__":
    eta=0.1
    for q in [5,7,11]:
        print(f"--- q={q}",flush=True)
        for Aexp in [1.0,1.5,2.0,2.5,3.0,3.5]:
            X=int(round(q**Aexp)); Y=X*X
            if Y>4_000_000: print(f"  A={Aexp}: X={X} skip",flush=True); continue
            c=build(X,0.7,0.2); d=build(X,1.1,0.4)
            F,mx,D=Fval(c,d,q)
            print(f"  A={Aexp}: X={X:6d} |F|={abs(F):.4e} max|chat|={mx:.3e} |Dtr|={abs(D):.3e} X^-0.2*|F0|={X**-0.2:.2e}",flush=True)
