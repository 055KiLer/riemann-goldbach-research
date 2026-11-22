import numpy as np
from math import log as mlog, pi
from lmat import Config, node_meta
from kernels import ZetaDeriv, D_values, Ptilde_values, singular_series, set_primes
import model as MOD
N=30030; H=4.0; m=16
cfg=Config(N,H,m=m); Kmax=cfg.Kmax
sig,tt,wts=node_meta(cfg)
primes=MOD.get_primes(2_000_000); set_primes(primes); C2=MOD.get_C2(); S,fac=singular_series(N,C2)
zd=ZetaDeriv(64,24)
alpha=cfg.alpha
# diagonal w=2alpha,2beta, alpha+beta? diagonal for same node line -> w=2 sigma_i
for li,sigma in enumerate([alpha,0.125]):
    w=2*sigma+0j
    Dv=D_values(np.array([w]),zd,fac)[0]
    Pt=Ptilde_values(np.array([w]),zd,fac)[0]
    z1=zd.eval(np.array([1.0-w]),need=0)[0]
    X1=MOD.gamma_X1(complex(sigma))
    K=S*(pi/N)**w*Pt*z1*X1*X1   # X1(s)X1(conj s)=X1(s)*conj(X1(s))=|X1|^2
    print(f"line {li}: w={w:.4f} D={Dv:.6f} Ptilde={Pt:.6f} zeta(1-w)={z1:.6f} X1={X1:.4f} |X1|^2={abs(X1)**2:.4f}")
    print(f"   K = {K:.6f}   (S={S:.5f})")
