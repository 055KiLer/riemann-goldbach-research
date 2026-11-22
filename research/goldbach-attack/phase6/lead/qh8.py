"""Matched H=8,m=2 test of lambda ~ kappa*||Q||/sqrt(n): compute BOTH lambda_max (characters) and lQ (char-free)."""
import sys, os, time, json, math
import numpy as np
sys.path.insert(0,'/home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase2/spectral')
sys.path.insert(0,'/home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase5/lead-probe')
from lmat import Config, node_meta
from kernels import singular_series, ZetaDeriv, D_values_fast, Ptilde_values, set_primes
import mpmath as mp
CACHE='/home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase2/spectral/cache'
primes=np.load(f'{CACHE}/primes_2000000.npy'); set_primes(primes)
C2=float(np.load(f'{CACHE}/C2.npy')[0])
def gamma_X1(s):
    return complex(mp.gamma((mp.mpf(3)/2-mp.mpc(s))/2)/mp.gamma((mp.mpf(3)/2+mp.mpc(s))/2))
def lQ(N,H=8.0,m=2):
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
    return float(np.abs(ev).max()), S, float(np.sqrt((ev**2).sum())), float(ev.sum())
import probe2 as P2
if __name__=='__main__':
    Ns=[40022,60022,100042,200006,400006,600014,1000166]
    print(f"{'N':>8} {'lam':>10} {'lQ':>9} {'hsQ':>9} {'trQ':>9} {'kappa=lam*sqrt(n)/lQ':>20} {'ratio':>8} {'C':>7} {'C/log^1.5':>10}")
    for N in Ns:
        t0=time.time()
        try:
            lq,S,hsq,trq=lQ(N)
            r=P2.model(N,8.0,2)
            lam=r['lmax']; delta=r['delta']; phi=r['phi']; n=phi/2
            kap=lam*math.sqrt(n)/lq
            ratio=lam/delta; C=lam*math.sqrt(N)/math.sqrt(S); logN=math.log(N)
            print(f"{N:8d} {lam:10.6f} {lq:9.3f} {hsq:9.3f} {trq:9.2f} {kap:20.3f} {ratio:8.3f} {C:7.2f} {C/logN**1.5:10.3f}  t={time.time()-t0:.0f}s",flush=True)
        except Exception as e:
            import traceback; traceback.print_exc()
