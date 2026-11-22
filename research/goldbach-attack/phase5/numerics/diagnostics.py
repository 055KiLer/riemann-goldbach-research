"""Kernel-theorist HS-route diagnostics: trP, M4, ||Q||_HS^2, <P,Q>_HS, HS norm of C, avg||Ttilde||^2.
All weighted by |ds|/(|1+s|^2) as in the paper.  Run:  EIG=eigsh python3 diagnostics.py H N m
"""
import numpy as np, sys, time, os
from math import log as mlog, pi
from lmat import Config, build_G, node_meta
from kernels import (sieve, singular_series, ZetaDeriv, D_values_fast, Ptilde_values, set_primes)
from chars import CharacterGroup
from model import get_primes, get_C2, gamma_X1

def run(H,N,m):
    t0=time.time()
    cfg=Config(N,H,m=m); Kmax=cfg.Kmax
    primes=get_primes(); set_primes(primes); C2=get_C2(); S,fac=singular_series(N,C2)
    sig,tt,wts=node_meta(cfg); n=len(sig)
    cg=CharacterGroup(N); phi=cg.phi
    print(f"cfg H={H} N={N} m={m} phi={phi} nodes={n} delta={np.sqrt(S/N)*mlog(N)**1.5:.10f}",flush=True)
    G,idx_odd,inv=build_G(cfg,cg,verbose=False)   # (n, nodd)
    nodd=G.shape[1]
    print(f"build_G {time.time()-t0:.1f}s G{G.shape}",flush=True)
    # Hmat[i,chi] = sqrt(w_i) G[i,chi]/(1+s_i)
    A=np.sqrt(wts)/(1.0+sig+1j*tt)
    Hm=A[:,None]*G
    # f_chi norms
    cn=np.sum(np.abs(Hm)**2,axis=0).real    # ||f_chi||^2
    trP=float((2.0/phi)*cn.sum())
    M4=float((2.0/phi)*np.sum(cn**2))
    # Pw=(2/phi) Hm Hm^H ; Mgram = Hm Hm^H
    Mm=Hm@Hm.conj().T
    Pw=(2.0/phi)*Mm
    trP_b=float(np.trace(Pw).real)
    # Q = Dmat + Kmat (weighted)
    nimag=4*Kmax+1
    reals=np.array([2*cfg.alpha, cfg.alpha+0.125, 0.25])
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
    Mm2=(S*(pi/N)**wdist*Ptdist*zeta1mw)[flat].reshape(n,n)
    Kmat=(X1[:,None]*Mm2)*np.conj(X1)[None,:]
    Q=Dmat+Kmat
    Qw=(A[:,None]*Q)*np.conj(A)[None,:]
    Pw_alt=Pw
    QHS=float(np.sum(np.abs(Qw)**2))
    cross=float(np.sum(Mm*np.conj(Qw)).real)   # Re tr(HmHm^H Qw)=Re sum M_ij conj(Qw_ij)
    PQ=float((2.0/phi)*cross)
    avgT2=QHS-2.0*PQ+M4
    # spectra from C = A (P0-D-K) A^H ; note P0=(2/phi)G G^H ; C=Pw-Qw
    C=Pw-Qw
    ev=np.linalg.eigvalsh(C)
    lam=float(np.abs(ev).max()); HS=float(np.sqrt(np.sum(ev**2))); trC=float(np.sum(ev))
    delta=np.sqrt(S/N)*mlog(N)**1.5
    logN=mlog(N)
    thr_half=(phi/2.0)*delta*delta
    out=dict(H=H,N=N,m=m,phi=phi,nodes=n,S=S,delta=delta,lam=lam,ratio=lam/delta,
             Y=lam*np.sqrt(N),C=lam*np.sqrt(N)/np.sqrt(S),
             trP=trP,trP_alt=trP_b,M4=M4,QHS=QHS,PQ=PQ,avgT2=avgT2,
             PHS=float(np.sum(np.abs(Pw)**2)),trC=trC,CHS=HS,
             ratio_avg_to_thr=avgT2/thr_half, ratio_avg_to_log3=avgT2/logN**3, ratio_avg_to_log4=avgT2/logN**4,
             ratio_S_over_4_log3=avgT2/((S/4)*logN**3),
             maxf2=float(cn.max()), avgf2=float(cn.mean()),
             time=time.time()-t0)
    print("DIAG "+repr(out),flush=True)
    np.save(f'cache/diag_H{H}_N{N}_m{m}.npy', np.array([out],dtype=object), allow_pickle=True)
    return out

if __name__=='__main__':
    H=float(sys.argv[1]); N=int(sys.argv[2]); m=int(sys.argv[3])
    run(H,N,m)
