#!/usr/bin/env python3
"""Equidistribution probes for H_wrap (Lead's formulation):
E^X=(q-1)(D+W)-S_c*S_d+T ;  D=sum_A c_A conj(d_A); W=sum_{A!=B,A=B mod q}c_A conj(d_B); T=sum_{q|AB}...
Delta=(q-1)W - S_c*conj(S_d) + T   (must be <= q^{1-c eta}).
Also F=(1/q) sum_{h!=0} chat(h) conj(dhat(h));  F-D = W - S_c*conj(S_d)/q.
D_full = Euler product over all primes;  D_trunc=sum_{A<=X^2}.
Fit Delta ~ X^{alpha}, F-D ~ X^{-beta}."""
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
def build(X,u,v,eta):
    sig=0.5+eta; a=mp.mpc(sig,u); s=mp.mpc(sig,v)
    Y=X*X; mu=mobius(X); c=np.zeros(Y+1,dtype=np.complex128)
    nv=np.array([complex(mp.power(n,-a)) for n in range(1,X+1)])
    for r in range(1,X+1):
        if mu[r]==0: continue
        w=complex(mp.power(r,-s))*mu[r]; nn=min(X,Y//r)
        c[r*np.arange(1,nn+1)] += w*nv[:nn]
    return c
def primes_upto(n):
    sieve=np.ones(n+1,dtype=bool); sieve[:2]=False
    for i in range(2,int(n**0.5)+1):
        if sieve[i]: sieve[i*i::i]=False
    return np.nonzero(sieve)[0]
P=primes_upto(100000)
def Dfull(u1,v1,u2,v2,eta):
    sig=0.5+eta
    a=mp.mpc(sig,u1); s=mp.mpc(sig,v1); b=mp.mpc(sig,u2); t=mp.mpc(sig,v2)
    prod=mp.mpc(1)
    for p in P:
        lp=mp.log(int(p)); pa=mp.e**(-a*lp); ps=mp.e**(-s*lp)
        pb=mp.e**(-b*lp); pt=mp.e**(-t*lp)
        ca1=(1-pa/ps); db1c=mp.conj(1-pb/pt)  # conj of (1-p^{b-t}) with conj exponents -> 1-p^{conj b - conj t}
        # careful: conj(d_{p^e}) = p^{-conj(b) e}(1-p^{conj(b)-conj(t)})
        bcb=mp.mpc(sig,-u2); tct=mp.mpc(sig,-v2)
        pbc=mp.e**(-bcb*lp); ptc=mp.e**(-tct*lp)
        db1c=(1-pbc/ptc)
        num=ca1*db1c; den=1-mp.e**(-(a+bcb)*lp) if False else 1-pa*pbc
        # sum_{e>=1} p^{-e(a+conj b)}(1-p^{a-s})(1-p^{conj b-conj t})
        prod*= 1+num/(1-pa*pbc)
    return prod
def analyze(c,d,q,X,eta):
    Y=X*X; A=np.arange(1,Y+1)
    D=np.vdot(d[1:],c[1:])
    idx=A%q
    Sc=np.zeros(q,dtype=np.complex128); Sd=np.zeros(q,dtype=np.complex128)
    np.add.at(Sc,idx,c[1:]); np.add.at(Sd,idx,d[1:])
    W=np.dot(Sc,np.conj(Sd))-D
    Sc0=Sc[0]; Sd0=Sd[0]
    Scall=Sc.sum(); Sdall=Sd.sum()
    T=Sc0*Sdall+Scall*Sd0-Sc0*Sd0
    Delta=(q-1)*W - Scall*np.conj(Sdall) + T
    chat=np.zeros(q,dtype=np.complex128); dhat=np.zeros(q,dtype=np.complex128)
    for h in range(1,q):
        e=np.exp(2j*np.pi*h*A/q)
        chat[h]=np.dot(c[1:],e); dhat[h]=np.dot(d[1:],e)
    F=np.vdot(dhat[1:],chat[1:])/q
    return dict(D=D,W=W,T=T,Delta=Delta,F=F,Sc=Scall,Sd=Sdall,FD=F-D,WD=W-Scall*np.conj(Sdall)/q)
if __name__=="__main__":
    eta=0.2
    print("D_full=",mp.nstr(Dfull(0.7,0.2,1.1,0.4,eta),10),flush=True)
    data={}
    for q in [5,7,11,13,17,23]:
        rows=[]
        for Aexp in [1.0,1.5,2.0,2.5,3.0]:
            X=int(round(q**Aexp)); Y=X*X
            if Y>2_000_000: continue
            c=build(X,0.7,0.2,eta); d=build(X,1.1,0.4,eta)
            r=analyze(c,d,q,X,eta)
            rows.append((Aexp,X,r))
            print(f"q={q:2d} A={Aexp}: X={X:5d} |D|={abs(r['D']):.3e} |W|={abs(r['W']):.3e} |T|={abs(r['T']):.3e} "
                  f"|Delta|={abs(r['Delta']):.3e} |F-D|={abs(r['FD']):.3e} |Sc|={abs(r['Sc']):.2e}",flush=True)
        data[q]=rows
    # fit exponents Delta~X^alpha, F-D~X^-beta for each q
    print("\nfits (log-log):",flush=True)
    for q,rows in data.items():
        if len(rows)<3: continue
        Xs=np.array([r[1] for r in rows],dtype=float)
        for key in ['Delta','FD']:
            ys=np.array([abs(r[2][key]) for r in rows],dtype=float)
            if np.any(ys<=0): continue
            alpha=np.polyfit(np.log(Xs),np.log(ys),1)[0]
            print(f"  q={q}: {key} ~ X^{alpha:+.3f}",flush=True)
