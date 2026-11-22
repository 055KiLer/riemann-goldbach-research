"""Compute Q_N(w)=D_N(w)+K_N(w) on the diagonal w=2sigma for sigma=alpha_N and 1/8, and the trace formula trQ=sum_lines Q(2sigma)*pi/(1+sigma)."""
import sys, math, time
import numpy as np
sys.path.insert(0,'/home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase2/spectral')
from kernels import singular_series, ZetaDeriv, D_values_fast, Ptilde_values, set_primes
import mpmath as mp
CACHE='/home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase2/spectral/cache'
primes=np.load(f'{CACHE}/primes_2000000.npy'); set_primes(primes)
C2=float(np.load(f'{CACHE}/C2.npy')[0])
def gamma_X1(s):
    return complex(mp.gamma((mp.mpf(3)/2-mp.mpc(s))/2)/mp.gamma((mp.mpf(3)/2+mp.mpc(s))/2))
def qdiag(N):
    mp.mp.dps=22
    S,fac=singular_series(N,C2); alpha=1.0/math.log(N); beta=0.125; logN=math.log(N)
    w_a=2*alpha; w_b=2*beta
    w=np.array([w_a,w_b],dtype=complex)
    zd=ZetaDeriv(K=64,J=24)
    D=D_values_fast(1.0*w,primes,fac)
    Pt=Ptilde_values(w,zd,fac,Pcut=200000)
    z=zd.eval(1.0-w,need=0)
    X1a=gamma_X1(complex(alpha+0j)); X1b=gamma_X1(complex(beta+0j))
    K=np.array([S*(np.pi/N)**w_a*Pt[0]*z[0]*X1a*X1a,
                S*(np.pi/N)**w_b*Pt[1]*z[1]*X1b*X1b])
    Q=D+K
    tr=np.real(Q[0]*math.pi/(1+alpha)+Q[1]*math.pi/(1+beta))
    return dict(N=N,logN=logN,S=S,D_a=D[0].real,K_a=K[0].real,Q_a=Q[0].real,D_b=D[1].real,K_b=K[1].real,Q_b=Q[1].real,
                tr=tr, tr_over_log2=tr/logN**2, Qa_over_log2=Q[0].real/logN**2)
def isprime(n):
    if n<2: return False
    for p in [2,3,5,7,11,13,17,19,23,29,31,37]:
        if n%p==0: return n==p
    d=n-1;s=0
    while d%2==0: s+=1; d//=2
    for a in [2,3,5,7,11,13,17,19,23,29,31,37]:
        x=pow(a,d,n)
        if x==1 or x==n-1: continue
        for _ in range(s-1):
            x=x*x%n
            if x==n-1: break
        else: return False
    return True
def find_p(t):
    p=t
    if p%4!=3: p += (3-p%4)%4
    while not isprime(p): p+=4
    return p
for tg in [2e4,1e5,1e6,1e8,1e10,1e12,1e14,1e16]:
    p=find_p(int(tg)); N=2*p
    r=qdiag(N)
    print(f"logN={r['logN']:7.3f} D_a={r['D_a']:10.3f} K_a={r['K_a']:9.3f} Q_a={r['Q_a']:10.3f} Q_a/log^2={r['Qa_over_log2']:7.4f} | Q_b={r['Q_b']:9.3f} tr={r['tr']:10.2f} tr/log^2={r['tr_over_log2']:7.4f}",flush=True)
