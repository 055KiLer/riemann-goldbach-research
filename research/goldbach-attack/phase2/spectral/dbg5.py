import numpy as np, time
from math import log as mlog, pi
import model as M
from lmat import Config, node_meta
cfg=Config(30030,4.0); sig,tt,wts=node_meta(cfg)
n=len(sig)
# rebuild pieces quickly via model? redo minimal: load saved? easier: call parts
primes=M.get_primes(2_000_000); from kernels import set_primes, singular_series, ZetaDeriv, D_values, Ptilde_values
set_primes(primes); C2=M.get_C2(); S,fac=singular_series(30030,C2)
Kmax=cfg.Kmax; imin=-2*Kmax; nimag=4*Kmax+1
reals=np.array([2*cfg.alpha, cfg.alpha+0.125, 2*0.125])
wdist=np.empty(3*nimag,dtype=complex)
for r in range(3): wdist[r*nimag:(r+1)*nimag]=reals[r]+1j*(np.arange(nimag)-2*Kmax)/cfg.m
zd=ZetaDeriv(64,24)
Ddist=D_values(1.0*wdist,zd,fac); Ptdist=Ptilde_values(wdist,zd,fac); zeta1mw=zd.eval(1.0-wdist,need=0)
li=np.concatenate([np.zeros(2*Kmax+1,dtype=int), np.ones(2*Kmax+1,dtype=int)])
ki=np.concatenate([np.arange(-Kmax,Kmax+1), np.arange(-Kmax,Kmax+1)])
ridx=(li[:,None]+li[None,:]).astype(int); iidx=(ki[:,None]-ki[None,:]+2*Kmax).astype(int)
flat=ridx*nimag+iidx
Dmat=Ddist[flat].reshape(n,n)
Mdist=S*(pi/30030)**wdist*Ptdist*zeta1mw
Mmat=Mdist[flat].reshape(n,n)
print("Dmat herm", np.abs(Dmat-Dmat.conj().T).max(), "|D|",np.abs(Dmat).max())
print("Mmat herm", np.abs(Mmat-Mmat.conj().T).max(), "|M|",np.abs(Mmat).max())
# check wdist conj mapping: for a random pair, w[j,i] should equal conj(w[i,j])
i,j=5,17
print("w_ij", ridx[i,j], iidx[i,j], wdist[flat[i,j]])
print("w_ji", ridx[j,i], iidx[j,i], wdist[flat[j,i]], "conj", np.conj(wdist[flat[i,j]]))
# X1
X1=np.array([M.gamma_X1(complex(s)) for s in sig])
Kmat=(X1[:,None]*Mmat)*np.conj(X1)[None,:]
print("Kmat herm", np.abs(Kmat-Kmat.conj().T).max(),"|K|",np.abs(Kmat).max())
# check X1 vs conj identity at one node
s=sig[3]+1j*tt[3]
print("X1 conj check", M.gamma_X1(complex(np.conj(s))), np.conj(M.gamma_X1(complex(s))))
# check D at one pair by direct formula
w=wdist[flat[5,17]]
print("w sample", w)
