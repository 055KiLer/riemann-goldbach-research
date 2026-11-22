"""Lead probe: decompose finite model into P-side vs M=D+K side; per-character stats."""
import sys, time, json
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

def decompose(N,H,m):
    mp.mp.dps=25
    cfg=Config(N,H,m=m); cg=CharacterGroup(N)
    S,fac=singular_series(N,C2); logN=np.log(N); delta=np.sqrt(S/N)*logN**1.5
    G,idx_odd,inv=build_G(cfg,cg,verbose=False)
    P=(2.0/cg.phi)*(G @ G.conj().T)
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
    Mop=Dmat+Kmat
    A=np.sqrt(wts)/(1.0+sig+1j*tt)
    CP=(A[:,None]*P)*np.conj(A)[None,:]
    CM=(A[:,None]*Mop)*np.conj(A)[None,:]
    CE=CP-CM
    evP=np.linalg.eigvalsh(CP).real; evM=np.linalg.eigvalsh(CM).real; evE=np.linalg.eigvalsh(CE).real
    vP=np.linalg.eigh(CP)[1][:,-1]; vM=np.linalg.eigh(CM)[1][:,-1]; vE=np.linalg.eigh(CE)[1][:,-1]
    out=dict(N=N,H=H,m=m,nodes=n,phi=cg.phi,delta=float(delta),S=float(S),
             lP=float(evP.max()),lM=float(evM.max()),lE=float(evE.max()),
             lEneg=float(evE.min()),hsP=float(np.sqrt((evP**2).sum())),hsM=float(np.sqrt((evM**2).sum())),
             hsE=float(np.sqrt((evE**2).sum())),trP=float(evP.sum()),trM=float(evM.sum()),trE=float(evE.sum()),
             rq_P_on_vE=float(vE@CP@vE),rq_M_on_vE=float(vE@CM@vE),
             overlap_evP=float(abs(vE@vP)),overlap_evM=float(abs(vE@vM)),
             ratio=float(evE.max()/delta))
    # per-character norms Q_chi = ||F_chi||^2 with F=g/(1+s); weights w/(|1+s|^2)
    wnu = wts/np.abs(1.0+sig+1j*tt)**2
    Gv = G*np.sqrt(wnu)[:,None]
    Q = (np.abs(Gv)**2).sum(axis=0)   # norm^2 of F_chi (odd only)
    Hmat = Gv @ Gv.conj().T
    fro2 = np.abs(Hmat)**2
    out.update(avgQ=float(Q.mean()),maxQ=float(Q.max()),minQ=float(Q.min()),
               sumQ2=float((Q**2).sum()), offdiag_gram=float(fro2.sum()-(Q**2).sum()),
               gram_frob=float(np.sqrt(fro2.sum())))
    return out

if __name__=='__main__':
    args=sys.argv[1:]
    for k in range(0,len(args),3):
        N,H,m=int(args[k]),float(args[k+1]),int(args[k+2])
        try: print(json.dumps(decompose(N,H,m)),flush=True)
        except Exception as e: print("FAIL",N,H,m,repr(e),flush=True)
