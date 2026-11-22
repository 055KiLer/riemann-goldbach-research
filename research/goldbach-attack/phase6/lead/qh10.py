"""Matched test at the SAME (H,m) as phase-5 lambda measurements: kappa = lam*sqrt(phi/2)/||Q||."""
import sys, math, json, time
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
    return float(np.abs(ev).max()), S
DATA=[  # (N,H,m,lambda)
 (400006,10,8,0.0866444),(700006,10,8,0.0769050),(999958,10,8,0.0655123),
 (1000018,10,8,0.0631964),(1000166,10,8,0.0558708),(1500038,10,8,0.0628448),
 (1500166,10,8,0.0532322),(1999966,10,8,0.0513074),(2011102,10,8,0.0511423),
 (3000014,8,8,0.0422593),(4000006,8,8,0.0335526),(600014,20,8,0.1035400),
 (200006,20,8,0.12388605),(40022,20,8,0.27313),
]
print(f"{'N':>9} {'H,m':>6} {'lam':>10} {'lQ':>9} {'kappa':>8} {'ratio':>8} {'C':>7} {'C/log^1.5':>10} {'lQ/log^1.5':>11}")
rows=[]
for (N,H,m,lam) in DATA:
    t0=time.time()
    try:
        lq,S=lQ(N,H,m); logN=math.log(N); phi=sum(1 for a in range(1,N) if math.gcd(a,N)==1) if N<1000 else None
        # phi for N=2p: p-1
        p=N//2; phi=p-1
        n=phi/2
        kap=lam*math.sqrt(n)/lq
        delta=math.sqrt(S/N)*logN**1.5
        ratio=lam/delta; C=lam*math.sqrt(N)/math.sqrt(S)
        rows.append(dict(N=N,H=H,m=m,lam=lam,lQ=lq,kappa=kap,ratio=ratio,C=C,logN=logN))
        print(f"{N:9d} {H:2.0f},{m:2d} {lam:10.6f} {lq:9.3f} {kap:8.3f} {ratio:8.3f} {C:7.2f} {C/logN**1.5:10.3f} {lq/logN**1.5:11.3f} t={time.time()-t0:.0f}s",flush=True)
    except Exception as e:
        print("FAIL",N,repr(e),flush=True)
json.dump(rows,open('qh10_rows.json','w'))
