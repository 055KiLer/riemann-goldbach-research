#!/usr/bin/env python3
"""Task-47 redirect: verify GWX (3.2) main term at ramified q with CORRECT A_q mask (p∤q).
Key: L(u,chi) via DFT with the +sign (ifft*n), correct mask q%p!=0, zeta_q over distinct p|q once.
Also recompute the BUGGY-mask variant (include all primes in A_q) to reproduce the apparent anomaly.
"""
import mpmath as mp
import numpy as np, itertools, random
mp.mp.dps=25
I=mp.mpc(0,1)
def primes_upto(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for p in range(2,int(n**0.5)+1):
        if s[p]:
            for m in range(p*p,n+1,p): s[m]=False
    return [i for i,v in enumerate(s) if v]
P=primes_upto(200000)
PS=np.array(P,dtype=np.int64)

def zq(w,q):
    v=mp.zeta(w)
    for p in P:
        if p>q: break
        if q%p==0: v*=(1-mp.power(p,-w))
    return v

def Aq_correct(q,a,b,s,t):
    val=mp.mpf(1)
    for p in P:
        if q%p==0: continue           # correct mask: exclude p|q
        u=mp.power(p,-a); v=mp.power(p,-s); w=mp.power(p,-b); z=mp.power(p,-t)
        val*=(1-v*z)*(1-u*z-w*v+v*z)/((1-u*z)*(1-w*v))
    return val

def Aq_buggy(q,a,b,s,t):
    # wrong mask (phase-10 bug): include p|q, i.e. product over ALL primes
    val=mp.mpf(1)
    for p in P:
        u=mp.power(p,-a); v=mp.power(p,-s); w=mp.power(p,-b); z=mp.power(p,-t)
        val*=(1-v*z)*(1-u*z-w*v+v*z)/((1-u*z)*(1-w*v))
    return val

def Zq(q,a,b,s,t,mask='correct'):
    A=Aq_correct(q,a,b,s,t) if mask=='correct' else Aq_buggy(q,a,b,s,t)
    return zq(a+b,q)*zq(s+t,q)/(zq(a+t,q)*zq(b+s,q))*A
def X(q,w,e): return mp.power(q/mp.pi,mp.mpf(1)/2-w)*mp.gamma((1-w+e)/2)/mp.gamma((w+e)/2)

def L_vals_2e(e,u):
    """all L(u,chi_{m,j}) for chi mod 2^e, (Z/2^e)^*=<5>x{+-1}; primitive iff j odd."""
    q=2**e; N=2**(e-2)
    V0=np.empty(N,dtype=np.complex128); V1=np.empty(N,dtype=np.complex128)
    for k in range(N):
        V0[k]=complex(mp.zeta(u,mp.mpf((5**k)%q)/q))
        V1[k]=complex(mp.zeta(u,mp.mpf((-5**k)%q)/q))
    F0=np.fft.ifft(V0)*N; F1=np.fft.ifft(V1)*N   # F[j]=sum_k V[k] e^{+2pi i jk/N}
    qfac=complex(mp.power(q,-u))
    return ({j:qfac*(F0[j]+F1[j]) for j in range(N)},
            {j:qfac*(F0[j]-F1[j]) for j in range(N)})

def Rval_2e(e,a,b,s,t):
    q=2**e; N=2**(e-2)
    La0,La1=L_vals_2e(e,a); Lb0,Lb1=L_vals_2e(e,b); Ls0,Ls1=L_vals_2e(e,s); Lt0,Lt1=L_vals_2e(e,t)
    tot=0j
    for m in (0,1):
        Lam=La1 if m else La0; Lbm=Lb1 if m else Lb0; Lsm=Ls1 if m else Ls0; Ltm=Lt1 if m else Lt0
        for j in range(1,N,2):   # primitive: j odd
            tot += Lam[j]*Lbm[N-j]/(Lsm[j]*Ltm[N-j])
    return mp.mpc(tot.real,tot.imag)

def M_2e(e,a,b,s,t,mask='correct'):
    q=2**e; ph=2**(e-2); Me={0:2**(e-3),1:2**(e-3)}
    Z=Zq(q,a,b,s,t,mask); Zs=Zq(q,1-b,1-a,s,t,mask)
    Hq=sum(Me[k]*X(q,a,k)*X(q,b,k) for k in (0,1))
    return ph*Z+Hq*Zs

def prime_M(q,a0,b0,s0,t0,a_chars=None):
    a,b,s,t=a0,b0,s0,t0
    # brute force for prime q
    import math
    units=list(range(1,q)); phi=len(units)
    # generator
    def order(g):
        o=1;x=g
        while x!=1: x=x*g%q;o+=1
        return o
    gen=None
    for g in units:
        if order(g)==phi: gen=g; break
    dlog={1:0}; cur=1
    for k in range(1,phi): cur=cur*gen%q; dlog[cur]=k
    chars=[]
    for j in range(phi):
        chi=[0]*q
        for xx in units: chi[xx-1]=mp.e**(2j*mp.pi*j*dlog[xx]/phi)
        chars.append(chi)
    prims=chars[1:]
    Me={0:0,1:0}
    for chi in prims: Me[0 if chi[q-2].real>0 else 1]+=1
    def Lval(u,chi):
        return mp.power(q,-u)*mp.fsum([chi[x-1]*mp.zeta(u,mp.mpf(x)/q) for x in range(1,q) if chi[x-1]!=0])
    R=mp.mpf(0)
    for chi in prims:
        chic=[mp.conj(c) if c!=0 else 0 for c in chi]
        R+=Lval(a,chi)*Lval(b,chic)/(Lval(s,chi)*Lval(t,chic))
    Z=Zq(q,a,b,s,t,'correct'); Zs=Zq(q,1-b,1-a,s,t,'correct')
    Hq=sum(Me[k]*X(q,a,k)*X(q,b,k) for k in (0,1))
    return R, len(prims)*Z+Hq*Zs

if __name__=="__main__":
    rng=random.Random(7)
    shifts=[]
    for _ in range(8):
        a=mp.mpf(1)/2+mp.mpf(repr(round(rng.uniform(-1,1),3)))*I
        b=mp.mpf(1)/2+mp.mpf(repr(round(rng.uniform(-1,1),3)))*I
        s=mp.mpf(6)/10+mp.mpf(repr(round(rng.uniform(-1,1),3)))*I
        t=mp.mpf(6)/10+mp.mpf(repr(round(rng.uniform(-1,1),3)))*I
        shifts.append((a,b,s,t))
    for e in [8,10,12]:
        q=2**e
        res_c=[];res_b=[]
        for (a,b,s,t) in shifts:
            R=Rval_2e(e,a,b,s,t)
            Mc=M_2e(e,a,b,s,t,'correct'); Mb=M_2e(e,a,b,s,t,'buggy')
            res_c.append(abs(R-Mc)); res_b.append(abs(R-Mb))
        rms=lambda v: float(mp.sqrt(sum(x*x for x in v)/len(v)))
        print(f"q=2^{e}={q}: phi*={2**(e-2)}", flush=True)
        print(f"   CORRECT mask: RMS|R-M|={rms(res_c):.4g}  RMS/sqrt(q)={rms(res_c)/q**0.5:.4f}  RMS/(q/2)={rms(res_c)/(q/2):.3e}")
        print(f"   BUGGY  mask: RMS|R-M|={rms(res_b):.4g}  RMS/sqrt(q)={rms(res_b)/q**0.5:.4f}  RMS/(q/2)={rms(res_b)/(q/2):.3e}")
    # prime comparison q=257
    q=257
    res=[]
    for (a,b,s,t) in shifts[:3]:
        R,M=prime_M(q,a,b,s,t); res.append(abs(R-M))
    rms=float(mp.sqrt(sum(x*x for x in res)/len(res)))
    print(f"prime q={q}: RMS|R-M|={rms:.4g}  RMS/sqrt(q)={rms/q**0.5:.4f}")
