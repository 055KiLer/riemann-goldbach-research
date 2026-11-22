#!/usr/bin/env python3
"""Lead independent check of ramified anomaly for GWX (3.2) at q=2^e.
L(u,chi) for all chars via 2D DFT over (Z/2^e)^* = {+-1} x <5>.
chi_(alpha,beta): chi((-1)^s 5^t)=(-1)^{alpha s} exp(2 pi i beta t / 2^{e-2}); primitive iff beta odd."""
import numpy as np, mpmath as mp
mp.mp.dps = 30

def sieve_primes(n):
    iscomp=np.zeros(n+1,bool); ps=[]
    for i in range(2,n+1):
        if not iscomp[i]: ps.append(i)
        for p in ps:
            if i*p>n: break
            iscomp[i*p]=True
            if i%p==0: break
    return np.array(ps)
PRIMES=sieve_primes(10**6)

def dlog5(m,n5):
    d={}; cur=1
    for t in range(n5):
        d[cur]=t; cur=cur*5%m
    return d

def Lall(u,e):
    m=2**e; n5=2**(e-2); d5=dlog5(m,n5)
    V=np.empty((2,n5),dtype=complex)
    for s in (0,1):
        for t in range(n5):
            a=(((-1)**s)*(5**t))%m
            V[s,t]=complex(mp.zeta(u, mp.mpf(a)/m))
    F=np.fft.ifft(V,axis=1)*n5     # F[s,beta]=sum_t V[s,t] e^{+2pi i beta t/n5}
    # L(alpha,beta)=m^{-u}(F[0,beta]+(-1)^alpha F[1,beta])
    ph=mp.mpc(np.complex128(1))*mp.mpc(m)**(-u)
    out={}
    for alpha in (0,1):
        sign=(-1)**alpha
        out[alpha]=np.array([complex(ph)*(F[0,b]+sign*F[1,b]) for b in range(n5)])
    return out

def zeta_q(x,q):
    return mp.zeta(x)*(1-mp.mpf(q)**(-x))

def Aq(a,b,s,t,q):
    P=PRIMES.astype(float); P=P[P!=float(q)]
    la=np.log(P)
    pa=np.exp(-complex(a)*la); pb=np.exp(-complex(b)*la)
    ps=np.exp(-complex(s)*la); pt=np.exp(-complex(t)*la)
    num=(1-ps*pt)*(1-pa*pt-pb*ps+ps*pt); den=(1-pa*pt)*(1-pb*ps)
    return np.prod(num/den)

def Zq(a,b,s,t,q):
    v=zeta_q(a+b,q)*zeta_q(s+t,q)/(zeta_q(a+t,q)*zeta_q(b+s,q))
    return v*Aq(a,b,s,t,q)

def Xq(q,eps,w):
    return (mp.mpf(q)/mp.pi)**(mp.mpf(1)/2-w)*mp.gamma((1-w+eps)/2)/mp.gamma((w+eps)/2)

def run(e,a,b,s,t):
    q=2**e
    La=Lall(a,e); Lb=Lall(mp.mpc(b).conjugate(),e)   # conj -> L(b,chibar)
    Ls=Lall(s,e); Lt=Lall(mp.mpc(t).conjugate(),e)
    n5=2**(e-2)
    R=mp.mpc(0)
    for alpha in (0,1):
        for beta in range(1,n5,2):
            La_v=mp.mpc(complex(La[alpha][beta]))
            Lb_v=mp.conj(mp.mpc(complex(Lb[alpha][beta])))
            Ls_v=mp.mpc(complex(Ls[alpha][beta]))
            Lt_v=mp.conj(mp.mpc(complex(Lt[alpha][beta])))
            R += La_v*Lb_v/(Ls_v*Lt_v)
    M0=2**(e-3) if e>=3 else 0; M1=M0
    phi=M0+M1
    Z=Zq(a,b,s,t,q); Zrev=Zq(1-b,1-a,s,t,q)
    H=M0*Xq(q,0,a)*Xq(q,0,b)+M1*Xq(q,1,a)*Xq(q,1,b)
    M=phi*Z+H*Zrev
    r=abs(R-M)
    print(f"q=2^{e}={q:7d} phi*={phi:6d} |R|={abs(R):.4e} |M|={abs(M):.4e} |R-M|={float(r):.4e}  /sqrt(q)={float(r)/np.sqrt(q):7.2f}  /(q/2)={float(r)/(q/2):8.4f}  /phi*={float(r)/phi:7.4f}")

if __name__=="__main__":
    a=mp.mpc(0.5,0.3); b=mp.mpc(0.5,0.7); s=mp.mpc(0.6,0.4); t=mp.mpc(0.6,0.9)
    for e in [4,6,8,10,12,14]:
        run(e,a,b,s,t)
