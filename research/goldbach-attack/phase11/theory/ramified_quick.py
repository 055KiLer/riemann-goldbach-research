import mpmath as mp
import numpy as np, random
mp.mp.dps=25
I=mp.mpc(0,1)
def primes_upto(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for p in range(2,int(n**0.5)+1):
        if s[p]:
            for m in range(p*p,n+1,p): s[m]=False
    return np.array([i for i,v in enumerate(s) if v],dtype=np.int64)
P=primes_upto(200000); LP=np.log(P.astype(float))
def zq(w,q):
    v=mp.zeta(w)
    for p in P:
        if p>q: break
        if q%p==0: v*=(1-mp.power(int(p),-w))
    return v
def Aq_vec(q,a,b,s,t,mask):
    if mask=='correct': sel=P[P.astype(np.int64)!=0]  # placeholder
    qq=int(q)
    mask_keep = (qq % P != 0) if mask=='correct' else np.ones_like(P,dtype=bool)
    p=LP[mask_keep]
    pa=np.exp(-complex(a)*p); pb=np.exp(-complex(b)*p); ps=np.exp(-complex(s)*p); pt=np.exp(-complex(t)*p)
    num=(1-ps*pt)*(1-pa*pt-pb*ps+ps*pt); den=(1-pa*pt)*(1-pb*ps)
    return mp.mpc(complex(np.exp(np.sum(np.log(num/den)))))
def Zq(q,a,b,s,t,mask='correct'):
    return zq(a+b,q)*zq(s+t,q)/(zq(a+t,q)*zq(b+s,q))*Aq_vec(q,a,b,s,t,mask)
def X(q,w,e): return mp.power(q/mp.pi,mp.mpf(1)/2-w)*mp.gamma((1-w+e)/2)/mp.gamma((w+e)/2)
def L_vals_2e(e,u):
    q=2**e; N=2**(e-2)
    V0=np.empty(N,dtype=np.complex128); V1=np.empty(N,dtype=np.complex128)
    for k in range(N):
        V0[k]=complex(mp.zeta(u,mp.mpf((5**k)%q)/q)); V1[k]=complex(mp.zeta(u,mp.mpf((-5**k)%q)/q))
    F0=np.fft.ifft(V0)*N; F1=np.fft.ifft(V1)*N
    qfac=complex(mp.power(q,-u))
    return ({j:qfac*(F0[j]+F1[j]) for j in range(N)},{j:qfac*(F0[j]-F1[j]) for j in range(N)})
def Rval_2e(e,a,b,s,t):
    N=2**(e-2)
    La0,La1=L_vals_2e(e,a); Lb0,Lb1=L_vals_2e(e,b); Ls0,Ls1=L_vals_2e(e,s); Lt0,Lt1=L_vals_2e(e,t)
    tot=0j
    for m in (0,1):
        Lam=La1 if m else La0; Lbm=Lb1 if m else Lb0; Lsm=Ls1 if m else Ls0; Ltm=Lt1 if m else Lt0
        for j in range(1,N,2): tot+=Lam[j]*Lbm[N-j]/(Lsm[j]*Ltm[N-j])
    return mp.mpc(tot.real,tot.imag)
def M_2e(e,a,b,s,t,mask='correct'):
    q=2**e; ph=2**(e-2); Me={0:2**(e-3),1:2**(e-3)}
    Z=Zq(q,a,b,s,t,mask); Zs=Zq(q,1-b,1-a,s,t,mask)
    Hq=sum(Me[k]*X(q,a,k)*X(q,b,k) for k in (0,1))
    return ph*Z+Hq*Zs
rng=random.Random(7)
shifts=[]
for _ in range(8):
    shifts.append((mp.mpf(1)/2+mp.mpf(repr(round(rng.uniform(-1,1),3)))*I,
                   mp.mpf(1)/2+mp.mpf(repr(round(rng.uniform(-1,1),3)))*I,
                   mp.mpf(6)/10+mp.mpf(repr(round(rng.uniform(-1,1),3)))*I,
                   mp.mpf(6)/10+mp.mpf(repr(round(rng.uniform(-1,1),3)))*I))
for e in [8,10,12]:
    q=2**e; rc=[]; rb=[]
    for (a,b,s,t) in shifts:
        R=Rval_2e(e,a,b,s,t)
        rc.append(abs(R-M_2e(e,a,b,s,t,'correct')))
        rb.append(abs(R-M_2e(e,a,b,s,t,'buggy')))
    rms=lambda v: float(mp.sqrt(sum(x*x for x in v)/len(v)))
    print(f"q=2^{e}={q}: RMS_correct={rms(rc):.4g} RMS_correct/sqrt(q)={rms(rc)/q**0.5:.4f} | RMS_buggy={rms(rb):.4g} RMS_buggy/sqrt(q)={rms(rb)/q**0.5:.4f} RMS_buggy/(q/2)={rms(rb)/(q/2):.3e}", flush=True)
