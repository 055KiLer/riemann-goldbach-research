"""Independent-ish pointwise E_N sampler: rebuild model internals, return E at selected nodes.
Usage: python3 point_e.py N H m
Writes one JSON line to stdout with E(alpha,alpha), E(beta,beta), E(alpha,beta), trace, HS, lam_max, eigenvector height stats."""
import sys, os, json, numpy as np
from math import log as mlog, pi
sys.path.insert(0, os.environ.get('SPECTRAL','../../../../phase2/spectral'))
from lmat import Config, build_G, node_meta
from kernels import (sieve, singular_series, ZetaDeriv, D_values_fast, Ptilde_values, set_primes)
from chars import CharacterGroup
import mpmath as mp

def run(N,H,m):
    mp.mp.dps=25
    cfg=Config(N,H,m=m); Kmax=cfg.Kmax
    primes=np.load(os.path.join(os.environ.get('SPECTRAL','../../../../phase2/spectral'),'cache','primes_2000000.npy'))
    set_primes(primes)
    C2=float(np.load(os.path.join(os.environ.get('SPECTRAL','../../../../phase2/spectral'),'cache','C2.npy'))[0])
    S,fac=singular_series(N,C2)
    logN=mlog(N); delta=np.sqrt(S/N)*logN**1.5
    alpha=cfg.alpha
    sig,tt,wts=node_meta(cfg); n=len(sig)
    cg=CharacterGroup(N)
    G,idx_odd,inv=build_G(cfg,cg,verbose=False)
    P=(2.0/cg.phi)*(G @ G.conj().T); del G
    nimag=4*Kmax+1
    reals=np.array([2*alpha, alpha+0.125, 0.25])
    wdist=np.empty(3*nimag,dtype=complex)
    for r in range(3): wdist[r*nimag:(r+1)*nimag]=reals[r]+1j*(np.arange(nimag)-2*Kmax)/m
    zd=ZetaDeriv(K=64,J=24)
    Ddist=D_values_fast(1.0*wdist,primes,fac)
    Ptdist=Ptilde_values(wdist,zd,fac,Pcut=Pcut if False else 200000)
    zeta1mw=zd.eval(1.0-wdist,need=0)
    def gamma_X1(s): return complex(mp.gamma((mp.mpf(3)/2-mp.mpc(s))/2)/mp.gamma((mp.mpf(3)/2+mp.mpc(s))/2))
    X1=np.array([gamma_X1(complex(sig[i]+1j*tt[i])) for i in range(n)])
    li=np.concatenate([np.zeros(2*Kmax+1,dtype=int),np.ones(2*Kmax+1,dtype=int)])
    ki=np.concatenate([np.arange(-Kmax,Kmax+1),np.arange(-Kmax,Kmax+1)])
    ridx=(li[:,None]+li[None,:]).astype(int)
    iidx=(ki[:,None]-ki[None,:]+2*Kmax).astype(int)
    flat=ridx*nimag+iidx
    Dmat=Ddist[flat].reshape(n,n)
    Mmat=(S*(pi/N)**wdist*Ptdist*zeta1mw)[flat].reshape(n,n)
    Kmat=(X1[:,None]*Mmat)*np.conj(X1)[None,:]
    E=P-Dmat-Kmat
    k0=Kmax  # t=0 node on line0 (alpha); line1 t=0 node index 2Kmax+1+Kmax
    k1=2*Kmax+1+Kmax
    out=dict(N=N,H=H,m=m,Kmax=Kmax,S=S,delta=delta,
             E_aa=complex(E[k0,k0]).real, E_bb=complex(E[k1,k1]).real,
             E_ab_re=complex(E[k0,k1]).real, E_ab_im=complex(E[k0,k1]).imag, P_aa=complex(P[k0,k0]).real,
             D_2a=complex(Dmat[k0,k0]).real, K_aa=complex(Kmat[k0,k0]).real,
             herm=np.abs(E-E.conj().T).max()/max(1.0,np.abs(E).max()))
    A=np.sqrt(wts)/(1.0+sig+1j*tt)
    C=(A[:,None]*E)*np.conj(A)[None,:]
    ev=np.linalg.eigvalsh(C)
    out['lam_max']=float(np.abs(ev).max()); out['trace']=float(ev.sum()); out['hs']=float(np.sqrt((ev**2).sum()))
    out['ratio']=out['lam_max']/delta
    # top eigenvector height distribution
    evals,evecs=np.linalg.eigh(C)
    j=np.argmax(np.abs(evals)); u=evecs[:,j]
    absu2=np.abs(u)**2; n0=2*Kmax+1
    tts=np.abs(np.concatenate([np.arange(-Kmax,Kmax+1)/m]*2))
    out['mass_frac_gt_H2']=float(absu2[tts>H/2].sum())
    out['mass_frac_gt_3H4']=float(absu2[tts>3*H/4].sum())
    out['mass_frac_gt_Hminus2']=float(absu2[tts>H-2].sum())
    out['mass_line_alpha']=float(absu2[:n0].sum())
    # quantiles of |t| under |u|^2
    order=np.argsort(tts); cum=np.cumsum(absu2[order])
    for q in [0.5,0.9,0.99,0.999]:
        out[f'q{q}_abst']=float(tts[order][np.searchsorted(cum,q)])
    return out

if __name__=='__main__':
    N=int(sys.argv[1]); H=float(sys.argv[2]); m=int(sys.argv[3])
    print(json.dumps(run(N,H,m)))
