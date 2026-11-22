"""Character-free lQ at low H (H=2/4, m=8) for far N; matched kappa test without H-bias corrections:
kappa_raw = lambda_raw * sqrt(phi/2) / lQ(same H,m). N=2p => phi=p-1."""
import sys, math, time
import numpy as np
sys.path.insert(0,'/home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase2/spectral')
from lmat import Config, node_meta
from kernels import singular_series, ZetaDeriv, D_values_fast, Ptilde_values, set_primes
import mpmath as mp
CACHE='/home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase2/spectral/cache'
primes=np.load(f'{CACHE}/primes_2000000.npy'); set_primes(primes)
C2=float(np.load(f'{CACHE}/C2.npy')[0])
def gamma_X1(s):
    return complex(mp.gamma((mp.mpf(3)/2-mp.mpc(s))/2)/mp.gamma((mp.mpf(3)/2+mp.mpc(s))/2))
def lQ(N,H,m):
    mp.mp.dps=22
    cfg=Config(N,H,m=m); S,fac=singular_series(N,C2)
    sig,tt,wts=node_meta(cfg); n=len(sig)
    nimag=4*cfg.Kmax+1
    reals=np.array([2*cfg.alpha,cfg.alpha+0.125,0.25])
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
    return float(np.abs(ev).max()),float(S),n
# (N, lambda_raw, H, m) from spectral-numerics / phase5
DATA=[(1000166,0.04452185,2,8),(4000006,0.02838244,2,8),(9954254,0.02321308,2,8)]
for (N,lam,H,m) in DATA:
    t0=time.time()
    lq,S,nn=lQ(N,H,m)
    phi=N//2-1; n=phi/2
    kap=lam*math.sqrt(n)/lq
    delta=math.sqrt(S/N)*math.log(N)**1.5
    ratio=lam/delta
    print(f"N={N} H={H} m={m} nodes={nn} lQ={lq:.4f} lam_raw={lam:.8f} kappa_raw={kap:.3f} ratio_raw={ratio:.3f} t={time.time()-t0:.0f}s",flush=True)
