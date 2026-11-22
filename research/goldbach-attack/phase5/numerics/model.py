"""Assemble Li-Liu finite spectral model C (Appendix B) and compute extreme eigenvalues."""
import numpy as np, time, os, sys
from math import log as mlog, pi
from lmat import Config, build_G, node_meta
from kernels import (sieve, C2_constant, singular_series, ZetaDeriv,
                     D_values, D_values_fast, Ptilde_values, set_primes)
from chars import CharacterGroup
import mpmath as mp

CACHE='cache'
os.makedirs(CACHE, exist_ok=True)

def get_primes(limit):
    fn=f'{CACHE}/primes_{limit}.npy'
    if os.path.exists(fn): return np.load(fn)
    t0=time.time(); pr=sieve(limit); print(f"sieve {limit}: {len(pr)} primes {time.time()-t0:.1f}s", flush=True)
    np.save(fn, pr); return pr

def get_C2():
    fn=f'{CACHE}/C2.npy'
    if os.path.exists(fn): return float(np.load(fn)[0])
    pr=sieve(100_000_000); p=pr[pr>2].astype(float)
    C2=float(np.prod(1.0-1.0/(p-1.0)**2)); np.save(fn,np.array([C2])); return C2

def gamma_X1(s):
    return complex(mp.gamma((mp.mpf(3)/2 - mp.mpc(s))/2)/mp.gamma((mp.mpf(3)/2 + mp.mpc(s))/2))

def build_model(N=30030, H=40.0, m=16, Pcut=200000, prime_limit=2_000_000, verbose=True, return_C=False):
    t00=time.time(); mp.mp.dps=25
    cfg=Config(N,H,m=m); Kmax=cfg.Kmax
    primes=get_primes(prime_limit); set_primes(primes)
    C2=get_C2(); S,fac=singular_series(N,C2)
    logN=mlog(N); delta=np.sqrt(S/N)*logN**1.5
    alpha=cfg.alpha
    if verbose: print(f"cfg N={N} H={H} m={m} Kmax={Kmax} alpha={alpha!r} delta={delta!r} S={S!r}",flush=True)
    sig,tt,wts=node_meta(cfg); n=len(sig)
    cg=CharacterGroup(N)
    t0=time.time(); G,idx_odd,inv=build_G(cfg,cg,verbose=False); print(f"build_G {time.time()-t0:.1f}s G{G.shape}",flush=True)
    t0=time.time(); P=(2.0/cg.phi)*(G @ G.conj().T); print(f"P matmul {time.time()-t0:.1f}s",flush=True)
    del G
    # distinct w
    nimag=4*Kmax+1
    reals=np.array([2*alpha, alpha+0.125, 0.25])
    wdist=np.empty(3*nimag,dtype=complex)
    for r in range(3): wdist[r*nimag:(r+1)*nimag]=reals[r]+1j*(np.arange(nimag)-2*Kmax)/m
    zd=ZetaDeriv(K=64,J=24)
    t0=time.time(); Ddist=D_values_fast(1.0*wdist,primes,fac); print(f"Dvals(fast) {time.time()-t0:.1f}s",flush=True)
    t0=time.time(); Ptdist=Ptilde_values(wdist,zd,fac,Pcut=Pcut); print(f"Ptilde {time.time()-t0:.1f}s",flush=True)
    t0=time.time(); zeta1mw=zd.eval(1.0-wdist,need=0); print(f"zeta(1-w) {time.time()-t0:.1f}s",flush=True)
    t0=time.time(); X1=np.array([gamma_X1(complex(sig[i]+1j*tt[i])) for i in range(n)]); print(f"X1 {time.time()-t0:.1f}s",flush=True)
    li=np.concatenate([np.zeros(2*Kmax+1,dtype=int),np.ones(2*Kmax+1,dtype=int)])
    ki=np.concatenate([np.arange(-Kmax,Kmax+1),np.arange(-Kmax,Kmax+1)])
    ridx=(li[:,None]+li[None,:]).astype(int)
    iidx=(ki[:,None]-ki[None,:]+2*Kmax).astype(int)
    flat=ridx*nimag+iidx
    Dmat=Ddist[flat].reshape(n,n); del Ddist
    Mmat=(S*(pi/N)**wdist*Ptdist*zeta1mw)[flat].reshape(n,n); del Ptdist,zeta1mw
    Kmat=(X1[:,None]*Mmat)*np.conj(X1)[None,:]; del Mmat
    E=P-Dmat-Kmat; del P,Dmat,Kmat
    herm_err=np.abs(E-E.conj().T).max()/max(1.0,np.abs(E).max())
    A=np.sqrt(wts)/(1.0+sig+1j*tt)
    C=(A[:,None]*E)*np.conj(A)[None,:]; del E
    herm_err2=np.abs(C-C.conj().T).max()/max(1.0,np.abs(C).max())
    import os as _os
    if _os.environ.get('SAVE_C'):
        np.save(_os.environ['SAVE_C'], C)
    print(f"E herm {herm_err:.2e} C herm {herm_err2:.2e} |C|max {np.abs(C).max():.4e}",flush=True)
    t0=time.time()
    import os as _os
    if n<=3200 and _os.environ.get('EIG','')!='eigsh':
        ev=np.linalg.eigvalsh(C); mode='eigh'
    else:
        try:
            from scipy.sparse.linalg import eigsh
            ev=eigsh(C, k=8, which='LM', return_eigenvectors=False, tol=1e-10, maxiter=2000)
            mode='eigsh'
        except Exception as e:
            print("eigsh failed:",e,flush=True); ev=np.linalg.eigvalsh(C); mode='eigh'
    print(f"eigen {mode} {time.time()-t0:.1f}s",flush=True)
    out=dict(N=N,H=H,m=m,delta=delta,S=S,alpha=alpha,ev=ev,Cmax=np.abs(C).max(),herm=herm_err2,mode=mode,total=time.time()-t00,
             phi=cg.phi,sig=sig,tt=tt,wts=wts,beta=0.125)
    if return_C: out['C']=C
    return out

def report(res, extra=''):
    ev=np.asarray(res['ev']); delta=res['delta']
    am=np.abs(ev); o=np.argsort(-am); evs=ev[o]
    ratio=am.max()/delta
    print(f"[{extra}] N={res['N']} H={res['H']} m={res['m']} mode={res['mode']}")
    print(f"  delta_N = {delta!r}")
    print(f"  max|eig| = {am.max()!r}   ||C||/delta = {ratio!r}")
    print(f"  extremes: most negative {ev.min()!r}, most positive {ev.max()!r}")
    print(f"  top eigenvalues |.|: {np.sort(am)[-8:]}")
    np.save(f"{CACHE}/ev_N{res['N']}_H{res['H']}_m{res['m']}.npy", ev)
    with open(f"{CACHE}/results.txt","a") as f:
        f.write(f"N={res['N']} H={res['H']} m={res['m']} delta={delta!r} maxabs={am.max()!r} ratio={ratio!r} min={ev.min()!r} max={ev.max()!r} |C|max={res['Cmax']!r} mode={res['mode']} time={res['total']:.1f}\n")
    return ratio

if __name__=='__main__':
    H=float(sys.argv[1]) if len(sys.argv)>1 else 40.0
    N=int(sys.argv[2]) if len(sys.argv)>2 else 30030
    m=int(sys.argv[3]) if len(sys.argv)>3 else 16
    res=build_model(N,H,m)
    report(res)
