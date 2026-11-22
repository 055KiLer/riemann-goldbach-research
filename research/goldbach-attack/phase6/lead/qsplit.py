"""Split Q_N = kappa_N * B + R: compressed norms of Q, B (pole kernel) and remainder R.
B kernel: b(s,zbar)=1/((1+s)(1+zbar)(s+zbar)); kappa_N=logN-log(2pi)+psi(3/4)."""
import sys, math, time
import numpy as np
sys.path.insert(0,'/home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase2/spectral')
from lmat import Config, node_meta
from kernels import singular_series, ZetaDeriv, D_values_fast, Ptilde_values, set_primes
import mpmath as mp
CACHE='/home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase2/spectral/cache'
primes=np.load(f'{CACHE}/primes_2000000.npy'); set_primes(primes)
C2=float(np.load(f'{CACHE}/C2.npy')[0])
PSI34=float(mp.digamma(mp.mpf(3)/4)) if False else None
psi34=float(mp.digamma(mp.mpf(3)/4))
def gamma_X1(s):
    return complex(mp.gamma((mp.mpf(3)/2-mp.mpc(s))/2)/mp.gamma((mp.mpf(3)/2+mp.mpc(s))/2))
def parts(N,H,m):
    mp.mp.dps=22
    cfg=Config(N,H,m=m); S,fac=singular_series(N,C2)
    sig,tt,wts=node_meta(cfg); n=len(sig)
    s=np.array([sig[i]+1j*tt[i] for i in range(n)])
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
    # B matrix: b(s_i, conj(s_j)) = 1/(s_i+conj(s_j)) ; note s+zbar = s_i + conj(s_j)
    Ssum = s[:,None] + np.conj(s)[None,:]
    Bmat = 1.0/Ssum
    CB=(A[:,None]*Bmat)*np.conj(A)[None,:]
    kap=math.log(N)-math.log(2*math.pi)+psi34
    CR=CQ-kap*CB
    eQ=np.linalg.eigvalsh(CQ).real; eB=np.linalg.eigvalsh(CB).real; eR=np.linalg.eigvalsh(CR).real
    return dict(N=N,H=H,m=m,nodes=n,kappa=float(kap),
                lQ=float(np.abs(eQ).max()),lB=float(np.abs(eB).max()),lR=float(np.abs(eR).max()),
                posB=float(eB.max()),negB=float(eB.min()),
                hsQ=float(np.sqrt((eQ**2).sum())),hsB=float(np.sqrt((eB**2).sum())),hsR=float(np.sqrt((eR**2).sum())),
                trQ=float(eQ.sum()),trB=float(eB.sum()),trR=float(eR.sum()))
if __name__=='__main__':
    for (N,H,m) in [(40022,10,8),(40022,10,16),(40022,20,8),(40022,20,16),(400006,10,8),(4000006,10,8)]:
        t0=time.time()
        try:
            r=parts(N,H,m)
            print(f"N={N} H={H} m={m} nodes={r['nodes']} kap={r['kappa']:.4f} | lQ={r['lQ']:.4f} lB={r['lB']:.4f} lR={r['lR']:.4f} | kappa*lB={r['kappa']*r['lB']:.3f} | HSQ={r['hsQ']:.3f} HSB={r['hsB']:.3f} HSR={r['hsR']:.3f} | trQ={r['trQ']:.1f} trB={r['trB']:.1f} trR={r['trR']:.1f} t={time.time()-t0:.0f}s",flush=True)
        except Exception as e:
            print("FAIL",N,H,m,repr(e),flush=True)
