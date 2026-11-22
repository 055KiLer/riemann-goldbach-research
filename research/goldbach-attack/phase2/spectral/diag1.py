import numpy as np, time
from math import log as mlog, pi
from lmat import Config, node_meta, build_G
from kernels import (sieve, C2_constant, singular_series, ZetaDeriv, D_values, Ptilde_values, set_primes)
from chars import CharacterGroup
import model as MOD

N=30030; H=4.0; m=16
cfg=Config(N,H,m=m); Kmax=cfg.Kmax
sig,tt,wts=node_meta(cfg); n=len(sig)
primes=MOD.get_primes(2_000_000); set_primes(primes); C2=MOD.get_C2(); S,fac=singular_series(N,C2)
cg=CharacterGroup(N)
G,idx_odd,inv=build_G(cfg,cg,verbose=False)
P=(2.0/cg.phi)*(G@G.conj().T)
nimag=4*Kmax+1
reals=np.array([2*cfg.alpha, cfg.alpha+0.125, 0.25])
wdist=np.empty(3*nimag,dtype=complex)
for r in range(3): wdist[r*nimag:(r+1)*nimag]=reals[r]+1j*(np.arange(nimag)-2*Kmax)/m
zd=ZetaDeriv(64,24)
Ddist=D_values(1.0*wdist,zd,fac); Ptdist=Ptilde_values(wdist,zd,fac); zeta1mw=zd.eval(1.0-wdist,need=0)
li=np.concatenate([np.zeros(2*Kmax+1,dtype=int), np.ones(2*Kmax+1,dtype=int)])
ki=np.concatenate([np.arange(-Kmax,Kmax+1), np.arange(-Kmax,Kmax+1)])
ridx=(li[:,None]+li[None,:]).astype(int); iidx=(ki[:,None]-ki[None,:]+2*Kmax).astype(int)
flat=ridx*nimag+iidx
Dmat=Ddist[flat].reshape(n,n)
Mdist=S*(pi/N)**wdist*Ptdist*zeta1mw
Mmat=Mdist[flat].reshape(n,n)
X1=np.array([MOD.gamma_X1(complex(s)) for s in sig])
Kmat=(X1[:,None]*Mmat)*np.conj(X1)[None,:]
E=P-Dmat-Kmat
A=np.sqrt(wts)/(1.0+sig)
def wnorm(X): 
    Y=(A[:,None]*X)*np.conj(A)[None,:]
    return np.linalg.norm(Y,2), np.abs(Y).max()
for nm,X in [('P',P),('D',Dmat),('K',Kmat),('E',E)]:
    sp,mx=wnorm(X); print(f"{nm}: weighted norm {sp:.4f} weighted |max| {mx:.4e}  raw|max| {np.abs(X).max():.3e}  raw mean|.| {np.abs(X).mean():.3f}")
# check hermiticity of P and trace
print("P trace", np.trace(P).real, " diag P sample", P[0,0], P[10,10])
# fraction of |E| vs |P|
print("ratio max |E|/|P|", np.abs(E).max()/np.abs(P).max())
