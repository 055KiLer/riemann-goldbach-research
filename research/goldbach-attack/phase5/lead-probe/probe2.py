"""Cheap finite-model ratios at coarse (H,m) to calibrate against fine runs; also coarse large-N trend."""
import sys, os, time, json
import numpy as np
sys.path.insert(0, '/home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase2/spectral')
from lmat import Config, build_G, node_meta
from kernels import (singular_series, ZetaDeriv, D_values_fast, Ptilde_values, set_primes)
from chars import CharacterGroup
import mpmath as mp

CACHE='/home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase2/spectral/cache'
primes=np.load(f'{CACHE}/primes_2000000.npy'); set_primes(primes)
C2=float(np.load(f'{CACHE}/C2.npy')[0])

def gamma_X1(s):
    return complex(mp.gamma((mp.mpf(3)/2 - mp.mpc(s))/2)/mp.gamma((mp.mpf(3)/2 + mp.mpc(s))/2))

def model(N,H,m):
    mp.mp.dps=25
    cfg=Config(N,H,m=m); cg=CharacterGroup(N)
    S,fac=singular_series(N,C2); logN=np.log(N)
    delta=np.sqrt(S/N)*logN**1.5
    t0=time.time(); G,idx_odd,inv=build_G(cfg,cg,verbose=False); tb=time.time()-t0
    P=(2.0/cg.phi)*(G @ G.conj().T); del G
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
    ridx=(li[:,None]+li[None,:]).astype(int)
    iidx=(ki[:,None]-ki[None,:]+2*cfg.Kmax).astype(int)
    flat=ridx*nimag+iidx
    Dmat=Ddist[flat].reshape(n,n)
    Mmat=(S*(np.pi/N)**wdist*Ptdist*zeta1mw)[flat].reshape(n,n)
    Kmat=(X1[:,None]*Mmat)*np.conj(X1)[None,:]
    E=P-Dmat-Kmat
    A=np.sqrt(wts)/(1.0+sig+1j*tt)
    C=(A[:,None]*E)*np.conj(A)[None,:]
    ev=np.linalg.eigvalsh(C)
    am=np.abs(ev)
    return dict(N=N,H=H,m=m,delta=delta,S=S,phi=cg.phi,nodes=n,
                lmax=float(am.max()),ratio=float(am.max()/delta),
                X=float(am.max()*np.sqrt(N)/np.sqrt(S)),
                hs=float(np.sqrt((ev**2).sum())),tr=float(ev.sum()),
                t=time.time()-t0)

if __name__=='__main__':
    # args: N,H,m triples
    args=sys.argv[1:]
    for k in range(0,len(args),3):
        N,H,m=int(args[k]),float(args[k+1]),int(args[k+2])
        try:
            r=model(N,H,m); print(json.dumps(r),flush=True)
        except Exception as e:
            print("FAIL",N,H,m,repr(e),flush=True)
