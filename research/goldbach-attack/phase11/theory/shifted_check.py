#!/usr/bin/env python3
"""Phase-11 Lead: SHIFTED-REGION Ratios identity test (efficient DFT version).
Claim: for q prime, shifts with Re = 1/2+eta (all four), GRH =>
  R_q = phi*(q) Z_q + O(q^{1-omega}), omega < eta/2,
with phi*=q-2, and Z_q(diagonal) = Euler product
  S_inf = prod_p (1 - p^{-a-t} - p^{-b-s} + p^{-s-t})/(1 - p^{-a-b}).
Test: (1) |phi*S_inf - M_q(CFZ)| small (main-term identity);
      (2) |R_q - M_q| level (conjecturally square-root)."""
import numpy as np, mpmath as mp
mp.mp.dps = 30

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

def Lall(q,g,u):
    n=q-1; vals=np.empty(n,dtype=complex); cur=1
    z=mp.zeta
    for k in range(n):
        vals[k]=complex(z(u, mp.mpf(cur)/q)); cur=cur*g%q
    F=np.fft.ifft(vals)   # (1/n) sum_k vals[k] e^{+2pi i jk/n}
    return np.array(n*np.array([mp.power(q,-u)])[0]*F if False else (mp.mpc(q)**(-u))*n*F, dtype=complex)

def Lall_mp(q,g,u):
    n=q-1; vals=np.empty(n,dtype=complex); cur=1
    for k in range(n):
        vals[k]=complex(mp.zeta(u, mp.mpf(cur)/q)); cur=cur*g%q
    F=np.fft.ifft(vals)
    return np.array(np.complex128(mp.mpc(q)**(-u))*n*F, dtype=complex)

def zeta_q(x,q):
    return mp.zeta(x)*(1-mp.mpc(q)**(-x)) if False else mp.zeta(x)*(1-mp.mpf(q)**(-x))

def Zq(a,b,s,t,q,primes):
    v = zeta_q(a+b,q)*zeta_q(s+t,q)/(zeta_q(a+t,q)*zeta_q(b+s,q))
    P=primes[primes!=q].astype(float); la=np.log(P)
    pa=np.exp(-complex(a)*la); pb=np.exp(-complex(b)*la)
    ps=np.exp(-complex(s)*la); pt=np.exp(-complex(t)*la)
    num=(1-ps*pt)*(1-pa*pt-pb*ps+ps*pt); den=(1-pa*pt)*(1-pb*ps)
    return v*np.prod(num/den)

def Aq_raw(a,b,s,t,q,primes):
    P=primes[primes!=q].astype(float); la=np.log(P)
    pa=np.exp(-complex(a)*la); pb=np.exp(-complex(b)*la)
    ps=np.exp(-complex(s)*la); pt=np.exp(-complex(t)*la)
    num=(1-ps*pt)*(1-pa*pt-pb*ps+ps*pt); den=(1-pa*pt)*(1-pb*ps)
    return np.prod(num/den)

def Zq_general(a,b,s,t,q,primes):
    # general Z_q(a,b;c=s,d=t)
    v = zeta_q(a+b,q)*zeta_q(s+t,q)/(zeta_q(a+t,q)*zeta_q(b+s,q))
    return v*Aq_raw(a,b,s,t,q,primes)

def Sinf(a,b,s,t,primes):
    P=primes.astype(float); la=np.log(P)
    u=np.exp(-complex(a)*la); v=np.exp(-complex(s)*la)
    w=np.exp(-complex(b)*la); z=np.exp(-complex(t)*la)
    return np.prod((1-u*z-w*v+v*z)/(1-u*w))

def Xqe(q,e,w):
    return (mp.mpf(q)/mp.pi)**(mp.mpf(1)/2-w)*mp.gamma((1-w+e)/2)/mp.gamma((w+e)/2)

def run(q, avals):
    a,b,s,t=[mp.mpc(x) for x in avals]
    g=primroot(q); n=q-1
    Las=Lall_mp(q,g,a)
    Lcb=Lall_mp(q,g,mp.mpc(b).conjugate())   # L(conj b, chi); conj -> L(b,chibar)
    Ls =Lall_mp(q,g,s)
    Lct=Lall_mp(q,g,mp.mpc(t).conjugate())
    R=np.sum(Las[1:]*np.conj(Lcb[1:])/(Ls[1:]*np.conj(Lct[1:])))
    R=mp.mpc(complex(R))
    phi=q-2; M0=(q-3)//2; M1=(q-1)//2
    Z=Zq(a,b,s,t,q,PRIMES)
    Zrev=Zq_general(1-b,1-a,s,t,q,PRIMES)
    H=M0*Xqe(q,0,a)*Xqe(q,0,b)+M1*Xqe(q,1,a)*Xqe(q,1,b)
    M=phi*Z+H*Zrev
    S=Sinf(a,b,s,t,PRIMES)
    print(f"q={q}  shifts a={a} b={b} s={s} t={t}   Re={mp.re(a)}")
    print(f"  |R|={abs(R):.6e}  |M|={abs(M):.6e}  |phi*Z|={abs(phi*Z):.6e}  |phi*S|={abs(phi*S):.6e}")
    print(f"  |R - M|/|M| = {abs(R-M)/abs(M):.3e}      |R - phi*S|/|M| = {abs(R-phi*S)/abs(M):.3e}")
    print(f"  |phi*S - phi*Z|/|phi*Z| = {abs(phi*S-phi*Z)/abs(phi*Z):.3e}   |phi*S - M|/|M| = {abs(phi*S-M)/abs(M):.3e}")
    print(f"  phase(R/M) = {mp.arg(R/M):.3e}")

if __name__=="__main__":
    run(1009, (0.75+0.4j, 0.75+0.9j, 0.75+0.6j, 0.75+0.7j))
    run(1009, (0.6+0.2j, 0.6-0.3j, 0.6+0.5j, 0.6-0.7j))
    run(211,  (0.75+0.4j, 0.75+0.9j, 0.75+0.6j, 0.75+0.7j))
