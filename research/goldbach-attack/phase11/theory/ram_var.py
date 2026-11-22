import mpmath as mp
import numpy as np
mp.mp.dps=25
I=mp.mpc(0,1)
def primes_upto(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for p in range(2,int(n**0.5)+1):
        if s[p]:
            for m in range(p*p,n+1,p): s[m]=False
    return [i for i,v in enumerate(s) if v]
P=primes_upto(200000)
def zq(w,q):
    v=mp.zeta(w)
    for p in P:
        if p>q: break
        if q%p==0: v*=(1-mp.power(p,-w))
    return v
def Aq(q,a,b,s,t):
    val=mp.mpf(1)
    for p in P:
        if q%p==0: continue
        u=mp.power(p,-a); v=mp.power(p,-s); w=mp.power(p,-b); z=mp.power(p,-t)
        val*=(1-v*z)*(1-u*z-w*v+v*z)/((1-u*z)*(1-w*v))
    return val
def Zq(q,a,b,s,t): return zq(a+b,q)*zq(s+t,q)/(zq(a+t,q)*zq(b+s,q))*Aq(q,a,b,s,t)
def X(q,w,e): return mp.power(q/mp.pi,mp.mpf(1)/2-w)*mp.gamma((1-w+e)/2)/mp.gamma((w+e)/2)
def L_vals_2e(e,u):
    q=2**e; N=2**(e-2)
    A=np.array([complex(mp.zeta(u,mp.mpf(5**k % q)/q)) for k in range(N)],dtype=np.complex128)
    B=np.array([complex(mp.zeta(u,mp.mpf((-5**k) % q)/q)) for k in range(N)],dtype=np.complex128)
    FA=np.fft.fft(A); FB=np.fft.fft(B); qfac=mp.power(q,-u)
    return ({j:complex(qfac)*(FA[j]+FB[j]) for j in range(N)},
            {j:complex(qfac)*(FA[j]-FB[j]) for j in range(N)})
def Rval_2e(e,a,b,s,t):
    q=2**e; N=2**(e-2)
    La0,La1=L_vals_2e(e,a); Lb0,Lb1=L_vals_2e(e,b); Ls0,Ls1=L_vals_2e(e,s); Lt0,Lt1=L_vals_2e(e,t)
    tot=0j
    for m in (0,1):
        Lam=La1 if m else La0; Lbm=Lb1 if m else Lb0; Lsm=Ls1 if m else Ls0; Ltm=Lt1 if m else Lt0
        for j in range(1,N,2): tot+=Lam[j]*Lbm[N-j]/(Lsm[j]*Ltm[N-j])
    return mp.mpc(tot.real,tot.imag)
for e in [6,8]:
  q=2**e; ph=2**(e-2); Me={0:2**(e-3),1:2**(e-3)}
  for ia in [0.2,0.4]:
    a=mp.mpf(1)/2+ia*I; b=mp.mpf(1)/2+0.3*I; s=mp.mpf(6)/10+0.2*I; t=mp.mpf(6)/10+0.5*I
    R=Rval_2e(e,a,b,s,t)
    Z=Zq(q,a,b,s,t); Zs=Zq(q,1-b,1-a,s,t)
    Hq=sum(Me[k]*X(q,a,k)*X(q,b,k) for k in (0,1))
    Hq2=sum(Me[k]*X(q,1-b,k)*X(q,1-a,k) for k in (0,1))   # alternative: X(1-b)X(1-a)
    # alternative Z_s evaluated as Z_q(a? ...) hmm try Z_q(a,b;s,t) with reflected denominators: Zq(1-b,1-a;s,t) standard
    variants={
      "GWX": ph*Z+Hq*Zs,
      "GWX+H2": ph*Z+Hq2*Zs,
      "H2 only": ph*Z+Hq2*Zs,
      "phi Z": ph*Z,
      "phi Z + Hq": ph*Z+Hq*Zs,
    }
    print(f"q=2^{e} ia={ia}: R={mp.nstr(R,8)}")
    for nm,M in variants.items():
        print(f"    {nm:10s}: M={mp.nstr(M,8)} |res|={mp.nstr(abs(R-M),5)} /sqrtq={mp.nstr(abs(R-M)/mp.sqrt(q),4)}")
