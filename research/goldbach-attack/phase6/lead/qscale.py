"""Phase-6 Lead: scaling of the model operator Q_N = D_N + K_N (no characters needed!)
Key hypothesis (random-covariance heuristic): lambda_max(T_N) ~ kappa * ||Q_N|| / sqrt(n), n=phi/2 => C=lam*sqrt(N)/sqrt(S) ~ const * ||Q_N||.
So exponent a of C(N) should equal exponent b of ||Q_N||. Q is character-free => can be computed for huge N."""
import sys, os, time, json, math
import numpy as np
sys.path.insert(0, '/home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase2/spectral')
from lmat import Config, node_meta
from kernels import (singular_series, ZetaDeriv, D_values_fast, Ptilde_values, set_primes)
import mpmath as mp

CACHE='/home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase2/spectral/cache'
primes=np.load(f'{CACHE}/primes_2000000.npy'); set_primes(primes)
C2=float(np.load(f'{CACHE}/C2.npy')[0])

def gamma_X1(s):
    return complex(mp.gamma((mp.mpf(3)/2 - mp.mpc(s))/2)/mp.gamma((mp.mpf(3)/2 + mp.mpc(s))/2))

def isprime(n):
    if n<2: return False
    for p in [2,3,5,7,11,13,17,19,23,29,31,37]:
        if n%p==0: return n==p
    d=n-1; s=0
    while d%2==0: s+=1; d//=2
    for a in [2,3,5,7,11,13,17,19,23,29,31,37]:
        x=pow(a,d,n)
        if x==1 or x==n-1: continue
        for _ in range(s-1):
            x=x*x%n
            if x==n-1: break
        else: return False
    return True

def find_p(target):
    p=target
    if p%4!=3: p += (3-p%4)%4
    while not isprime(p): p+=4
    return p

def Q_spectrum(N,H=8.0,m=2,verbose=False):
    mp.mp.dps=25
    cfg=Config(N,H,m=m)
    S,fac=singular_series(N,C2); logN=math.log(N); delta=math.sqrt(S/N)*logN**1.5
    sig,tt,wts=node_meta(cfg); n=len(sig)
    nimag=4*cfg.Kmax+1
    reals=np.array([2*cfg.alpha, cfg.alpha+0.125, 0.25])
    wdist=np.empty(3*nimag,dtype=complex)
    for r in range(3):
        wdist[r*nimag:(r+1)*nimag]=reals[r]+1j*(np.arange(nimag)-2*cfg.Kmax)/m
    zd=ZetaDeriv(K=64,J=24)
    Ddist=D_values_fast(1.0*wdist,primes,fac)
    Ptdist=Ptilde_values(wdist,zd,fac,Pcut=200000)
    zeta1mw=zd.eval(1.0-wdist,need=0)
    X1=np.array([gamma_X1(complex(sig[i]+1j*tt[i])) for i in range(n)])
    li=np.concatenate([np.zeros(2*cfg.Kmax+1,dtype=int),np.ones(2*cfg.Kmax+1,dtype=int)])
    ki=np.concatenate([np.arange(-cfg.Kmax,cfg.Kmax+1),np.arange(-cfg.Kmax,cfg.Kmax+1)])
    ridx=(li[:,None]+li[None,:]).astype(int); iidx=(ki[:,None]-ki[None,:]+2*cfg.Kmax).astype(int)
    flat=ridx*nimag+iidx
    Dmat=Ddist[flat].reshape(n,n)
    Mmat=(S*(np.pi/N)**wdist*Ptdist*zeta1mw)[flat].reshape(n,n)
    Kmat=(X1[:,None]*Mmat)*np.conj(X1)[None,:]
    Q=Dmat+Kmat
    A=np.sqrt(wts)/(1.0+sig+1j*tt)
    CQ=(A[:,None]*Q)*np.conj(A)[None,:]
    ev=np.linalg.eigvalsh(CQ).real
    am=np.abs(ev)
    return dict(N=int(N),H=H,m=m,nodes=n,S=float(S),delta=float(delta),
                lQ=float(am.max()),trQ=float(ev.sum()),hsQ=float(np.sqrt((ev**2).sum())),
                neg=float(ev.min()))

if __name__=='__main__':
    targets=[2e4,3e4,5e4,1e5,2e5,5e5,1e6,2e6,5e6,1e7,3e7,1e8,3e8,1e9]
    rows=[]; t0=time.time()
    for tg in targets:
        p=find_p(int(tg)); N=2*p
        try:
            r=Q_spectrum(N); r['p']=p
            r['logN']=math.log(N); r['Yq']=r['lQ']*math.sqrt(N); r['Cq']=r['Yq']/math.sqrt(r['S'])
            rows.append(r); print(json.dumps(r),flush=True)
        except Exception as e:
            print("FAIL",N,repr(e),flush=True)
    print("total time",time.time()-t0,flush=True)
