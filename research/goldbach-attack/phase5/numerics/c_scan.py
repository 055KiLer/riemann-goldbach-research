"""c-dependence of the finite model: alpha = c/log N (LL Appendix A set-up), beta=1/8 fixed."""
import numpy as np, sys, time, os
from math import log as mlog, pi
from lmat import Config, build_G, node_meta
from kernels import (singular_series, ZetaDeriv, D_values_fast, Ptilde_values, set_primes)
from chars import CharacterGroup
from model import get_primes, get_C2, gamma_X1

def run_c(N,H,m,c):
    t0=time.time(); logN=mlog(N)
    alpha=c/logN
    if alpha>=0.125: return dict(N=N,H=H,m=m,c=c,error='alpha>=beta strip empty')
    cfg=Config(N,H,m=m)
    cfg.alpha=alpha; cfg.sigma_lines=np.array([0.5+alpha,0.5+0.125])
    Kmax=cfg.Kmax
    primes=get_primes(2_000_000); set_primes(primes); C2=get_C2(); S,fac=singular_series(N,C2)
    sig,tt,wts=node_meta(cfg); n=len(sig)
    cg=CharacterGroup(N); phi=cg.phi
    G,idx_odd,inv=build_G(cfg,cg,verbose=False)
    P=(2.0/phi)*(G@G.conj().T)
    nimag=4*Kmax+1
    reals=np.array([2*alpha, alpha+0.125, 0.25])
    wdist=np.empty(3*nimag,dtype=complex)
    for r in range(3): wdist[r*nimag:(r+1)*nimag]=reals[r]+1j*(np.arange(nimag)-2*Kmax)/m
    zd=ZetaDeriv(64,24)
    Ddist=D_values_fast(1.0*wdist,primes,fac); Ptdist=Ptilde_values(wdist,zd,fac); zeta1mw=zd.eval(1.0-wdist,need=0)
    X1=np.array([gamma_X1(complex(sig[i]+1j*tt[i])) for i in range(n)])
    li=np.concatenate([np.zeros(2*Kmax+1,dtype=int),np.ones(2*Kmax+1,dtype=int)])
    ki=np.concatenate([np.arange(-Kmax,Kmax+1),np.arange(-Kmax,Kmax+1)])
    ridx=(li[:,None]+li[None,:]).astype(int); iidx=(ki[:,None]-ki[None,:]+2*Kmax).astype(int)
    flat=ridx*nimag+iidx
    Dmat=Ddist[flat].reshape(n,n)
    Mm=(S*(pi/N)**wdist*Ptdist*zeta1mw)[flat].reshape(n,n)
    Kmat=(X1[:,None]*Mm)*np.conj(X1)[None,:]
    E=P-Dmat-Kmat
    A_=np.sqrt(wts)/(1.0+sig+1j*tt)
    C=(A_[:,None]*E)*np.conj(A_)[None,:]
    ev=np.linalg.eigvalsh(C)
    lam=float(np.abs(ev).max()); delta=np.sqrt(S/N)*logN**1.5
    res=dict(N=N,H=H,m=m,c=c,alpha=alpha,lam=lam,delta=delta,ratio=lam/delta,
             Y=lam*np.sqrt(N),C=lam*np.sqrt(N)/np.sqrt(S),phi=phi,
             hermC=float(np.abs(C-C.conj().T).max()/max(1.0,np.abs(C).max())),
             trC=float(np.sum(ev)),HS=float(np.sqrt(np.sum(ev**2))),time=time.time()-t0)
    print("CSCAN "+repr(res),flush=True)
    with open('cache/cscan.txt','a') as f: f.write(repr(res)+'\n')
    return res

if __name__=='__main__':
    for args in [(40022,20,8,0.25),(40022,20,8,0.5),(40022,20,8,0.75),(40022,20,8,1.0),(40022,20,8,1.25)]:
        try: run_c(*args)
        except Exception as e: print("FAILED",args,type(e).__name__,e,flush=True)
