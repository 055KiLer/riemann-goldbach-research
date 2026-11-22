"""Phase-6 adversarial: (a) Q_N=D_N+K_N assembly & compression for kappa test (character-free);
(b) lambda_max + chi-content of top eigenvector for spike test; (c) low-H calibration.
Usage: python3 qk.py q N H m
       python3 qk.py lam N H m [chi]
       python3 qk.py calib N H m
Writes one JSON line to stdout."""
import sys, os, json, time
import numpy as np
from math import log as mlog, pi
SP=os.environ.get('SPECTRAL','/home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase2/spectral')
sys.path.insert(0,SP)
from lmat import Config, build_G, node_meta
from kernels import (singular_series, ZetaDeriv, D_values_fast, Ptilde_values, set_primes)
import mpmath as mp

primes=np.load(f'{SP}/cache/primes_2000000.npy'); set_primes(primes)
C2=float(np.load(f'{SP}/cache/C2.npy')[0])
def gamma_X1(s):
    return complex(mp.gamma((mp.mpf(3)/2-mp.mpc(s))/2)/mp.gamma((mp.mpf(3)/2+mp.mpc(s))/2))

def assemble(N,H,m,with_G=False):
    mp.mp.dps=25
    cfg=Config(N,H,m=m); Kmax=cfg.Kmax
    cfg.K=int(os.environ.get('KD','64')); cfg.J=int(os.environ.get('JD','24'))
    S,fac=singular_series(N,C2); logN=mlog(N); delta=np.sqrt(S/N)*logN**1.5
    sig,tt,wts=node_meta(cfg); n=len(sig)
    nimag=4*Kmax+1
    reals=np.array([2*cfg.alpha, cfg.alpha+0.125, 0.25])
    wdist=np.empty(3*nimag,dtype=complex)
    for r in range(3):
        wdist[r*nimag:(r+1)*nimag]=reals[r]+1j*(np.arange(nimag)-2*Kmax)/m
    zd=ZetaDeriv(K=64,J=24)
    Ddist=D_values_fast(1.0*wdist,primes,fac)
    Ptdist=Ptilde_values(wdist,zd,fac,Pcut=200000)
    zeta1mw=zd.eval(1.0-wdist,need=0)
    X1=np.array([gamma_X1(complex(sig[i]+1j*tt[i])) for i in range(n)])
    li=np.concatenate([np.zeros(2*Kmax+1,dtype=int),np.ones(2*Kmax+1,dtype=int)])
    ki=np.concatenate([np.arange(-Kmax,Kmax+1),np.arange(-Kmax,Kmax+1)])
    ridx=(li[:,None]+li[None,:]).astype(int); iidx=(ki[:,None]-ki[None,:]+2*Kmax).astype(int)
    flat=ridx*nimag+iidx
    Dmat=Ddist[flat].reshape(n,n)
    Mmat=(S*(pi/N)**wdist*Ptdist*zeta1mw)[flat].reshape(n,n)
    Kmat=(X1[:,None]*Mmat)*np.conj(X1)[None,:]
    Q=Dmat+Kmat
    A=np.sqrt(wts)/(1.0+sig+1j*tt)
    CQ=(A[:,None]*Q)*np.conj(A)[None,:]
    out=dict(N=int(N),H=H,m=m,nodes=n,phi=0,n_odd=0,S=float(S),delta=float(delta),alpha=cfg.alpha)
    evq=np.linalg.eigvalsh(CQ).real
    out.update(lQ=float(np.abs(evq).max()), hsQ=float(np.sqrt(np.sum(evq**2))), trQ=float(evq.sum()))
    if with_G:
        from chars import CharacterGroup
        cg=CharacterGroup(N)
        G,idx_odd,inv=build_G(cfg,cg,verbose=False)
        P=(2.0/cg.phi)*(G@G.conj().T)
        E=P-Q
        C=(A[:,None]*E)*np.conj(A)[None,:]
        ev=np.linalg.eigvalsh(C).real
        j=np.argmax(np.abs(ev)); lam=ev[j]
        out.update(phi=int(cg.phi), n_odd=int(cg.nodd), lam=float(lam), ratio=float(np.abs(lam)/delta),
                   trace=float(ev.sum()), hs=float(np.sqrt(np.sum(ev**2))),
                   herm=float(np.abs(C-C.conj().T).max()/max(1.0,np.abs(C).max())))
        if os.environ.get('CHI','')=='1':
            evals,evecs=np.linalg.eigh(C)
            jj=np.argmax(np.abs(evals)); h=evecs[:,jj]
            # boundary test function v = sum h_j phi_j ; chi-content a_chi = <f_chi,v>
            # with F_chi = A*G[:,chi] (nodes), P_comp=(2/phi) sum F_chi F_chi^H => a=F^H h
            F=A[:,None]*G
            a=F.conj().T@h
            ab2=np.abs(a)**2
            tot=ab2.sum()
            w=ab2/tot if tot>0 else ab2
            neff=float(1.0/np.sum(w**2)) if tot>0 else 0.0
            # participation ratio alternative
            npart=float((w.sum()**2)/np.sum(w**2)) if tot>0 else 0.0
            order=np.argsort(-ab2)
            top10=ab2[order[:10]]
            fn=np.abs(G)**2  # per-char norms squared at nodes
            nrm=fn.sum(axis=0)
            # correlation between |a| and ||f||
            corr=float(np.corrcoef(ab2, nrm)[0,1]) if tot>0 else 0.0
            out.update(chi=dict(tot_ab2=float(tot), n_eff=neff, top10_share=float(top10.sum()/tot) if tot>0 else 0.0,
                                top10_abs=[float(x) for x in np.sqrt(top10)],
                                max_abs=float(np.abs(a).max()), med_abs=float(np.median(np.abs(a))),
                                mean_abs=float(np.mean(np.abs(a))),
                                corr_absa2_fn2=corr,
                                q90_abs=float(np.quantile(np.abs(a),0.9)),
                                q99_abs=float(np.quantile(np.abs(a),0.99)),
                                q999_abs=float(np.quantile(np.abs(a),0.999))))
    return out

if __name__=='__main__':
    mode=sys.argv[1]; N=int(sys.argv[2]); H=float(sys.argv[3]); m=int(sys.argv[4])
    t0=time.time()
    if mode=='q':
        out=assemble(N,H,m,with_G=False)
    elif mode=='lam':
        out=assemble(N,H,m,with_G=True)
    elif mode=='calib':
        out=assemble(N,H,m,with_G=True)
    out['mode']=mode; out['t']=time.time()-t0
    print(json.dumps(out),flush=True)
