import numpy as np, time
from math import log as mlog, pi
from lmat import Config, node_meta, build_G
from kernels import (C2_constant, singular_series, ZetaDeriv, D_values, Ptilde_values, set_primes)
from chars import CharacterGroup
import model as MOD
N=30030; H=80.0; m=16
cfg=Config(N,H,m=m); Kmax=cfg.Kmax
sig,tt,wts=node_meta(cfg); n=len(sig)
primes=MOD.get_primes(2_000_000); set_primes(primes); C2=MOD.get_C2(); S,fac=singular_series(N,C2)
cg=CharacterGroup(N)
t0=time.time(); G,idx_odd,inv=build_G(cfg,cg,verbose=False); print("G",time.time()-t0,flush=True)
# check G row sanity: |G|max, median, and compare a row at large |t| with mpmath for one char
print("|G|max",np.abs(G).max(),"median",np.median(np.abs(G)), flush=True)
P=(2.0/cg.phi)*(G@G.conj().T); del G
nimag=4*Kmax+1
reals=np.array([2*cfg.alpha, cfg.alpha+0.125, 0.25])
wdist=np.empty(3*nimag,dtype=complex)
for r in range(3): wdist[r*nimag:(r+1)*nimag]=reals[r]+1j*(np.arange(nimag)-2*Kmax)/m
zd=ZetaDeriv(64,24)
Ddist=D_values(1.0*wdist,zd,fac); Ptdist=Ptilde_values(wdist,zd,fac); z1mw=zd.eval(1.0-wdist,need=0)
li=np.concatenate([np.zeros(2*Kmax+1,dtype=int),np.ones(2*Kmax+1,dtype=int)])
ki=np.concatenate([np.arange(-Kmax,Kmax+1),np.arange(-Kmax,Kmax+1)])
ridx=(li[:,None]+li[None,:]).astype(int); iidx=(ki[:,None]-ki[None,:]+2*Kmax).astype(int)
flat=ridx*nimag+iidx
Dmat=Ddist[flat].reshape(n,n)
Mmat=(S*(pi/N)**wdist*Ptdist*z1mw)[flat].reshape(n,n)
X1=np.array([MOD.gamma_X1(complex(sig[i]+1j*tt[i])) for i in range(n)])
Kmat=(X1[:,None]*Mmat)*np.conj(X1)[None,:]
E=P-Dmat-Kmat
A=np.sqrt(wts)/(1.0+sig+1j*tt)
C=(A[:,None]*E)*np.conj(A)[None,:]
i=np.unravel_index(np.abs(C).argmax(),C.shape)
print("max|C|",np.abs(C).max(),"at",i,"nodes",sig[i[0]]+1j*tt[i[0]],sig[i[1]]+1j*tt[i[1]], flush=True)
print("P=",P[i],"D=",Dmat[i],"K=",Kmat[i],"E=",E[i],flush=True)
# top 10 |C| entries locations
flatC=np.abs(C).ravel(); idx=np.argsort(-flatC)[:10]
for f in idx:
    a,b=np.unravel_index(f,C.shape)
    print(f"C[{a},{b}] |.|={flatC[f]:.3e} t=({tt[a]},{tt[b]}) lines=({li[a]},{li[b]}) P={P[a,b]:.3e} D={Dmat[a,b]:.3e} K={Kmat[a,b]:.3e} E={E[a,b]:.3e}",flush=True)
