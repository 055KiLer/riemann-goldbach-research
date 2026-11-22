"""Lead phase-6: pair measured lambda_max (phase-5) with model operator norm ||Q_N||=||D_N+K_N||.
Test hypothesis lambda ~ kappa * ||Q|| / sqrt(n), n=phi/2 => kappa = lam*sqrt(N)/||Q|| (for N=2p, sqrt(N/n)~2).
Q is character-free, so compute lQ at the SAME (H,m) as the phase-5 measurement (and at H=8,m=2 for cross-check)."""
import sys, os, time, json, math
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
# (N, H, m, lambda_measured, source)
DATA=[
 (40022,40,16,0.2757214,'p5'),
 (60022,40,16,0.2072516,'p5'),
 (100042,40,16,0.1660613,'p5'),
 (200006,20,16,0.1246573,'p5'),
 (400006,10,8,0.0866444,'p5'),
 (600014,20,8,0.1035400,'p3'),
 (700006,10,8,0.0769050,'p5'),
 (999958,10,8,0.0655123,'p5'),
 (1000166,10,8,0.0558708,'p5'),
 (1500038,10,8,0.0628448,'p5'),
 (1999966,10,8,0.0513074,'p5'),
 (2011102,10,8,0.0511423,'p5'),
 (3000014,8,8,0.0422593,'p5'),
 (4000006,8,8,0.0335526,'p5'),
]
print(f"{'N':>9} {'H,m':>7} {'lam':>10} {'lQ':>9} {'S':>8} {'kappa=lam*sqrtN/lQ':>18} {'C_meas':>8} {'C_pred=2.5*lQ/sqrtS':>20}")
rows=[]
for (N,H,m,lam,src) in DATA:
    t0=time.time()
    try:
        lq,S=lQ(N,H,m)
        kap=lam*math.sqrt(N)/lq
        Cmeas=lam*math.sqrt(N)/math.sqrt(S)
        Cpred=kap*lq/math.sqrt(S)
        rows.append(dict(N=N,H=H,m=m,lam=lam,lQ=lq,S=S,kappa=kap,Cmeas=Cmeas,logN=math.log(N)))
        print(f"{N:9d} {H:2.0f},{m:2d} {lam:10.6f} {lq:9.3f} {S:8.4f} {kap:18.3f} {Cmeas:8.2f} {Cpred:20.2f}   t={time.time()-t0:.1f}s",flush=True)
    except Exception as e:
        print("FAIL",N,repr(e),flush=True)
json.dump(rows,open('qpair_rows.json','w'))
# also H=8,m=2 version for all N (cheap, for model consistency check)
print("\n--- H=8,m=2 lQ cross-check ---",flush=True)
for (N,H,m,lam,src) in DATA:
    lq8,S=lQ(N,8.0,2); lq,S=lQ(N,H,m) if H!=8 else (lq8,S)
    print(f"N={N} lQ(H8m2)={lq8:.3f} lQ(H{H},m{m})={lq:.3f} ratio={lq/lq8:.4f}",flush=True)
