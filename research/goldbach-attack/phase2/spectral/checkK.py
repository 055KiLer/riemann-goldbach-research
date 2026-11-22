import numpy as np, mpmath as mp
from math import log as mlog, pi, sqrt
import model as MOD
from kernels import sieve, C2_constant, singular_series, ZetaDeriv, Ptilde_values, set_primes
mp.mp.dps=30
N=30030
primes=MOD.get_primes(2_000_000); set_primes(primes); C2=MOD.get_C2(); S,fac=singular_series(N,C2)
zd=ZetaDeriv(64,24)
alpha=1.0/mlog(N); beta=0.125
si=alpha+2j; zj=beta-1j   # s_i, conj(s_j) actually z = s_j? choose s_j = beta+1j so conj = beta-1j
s=si; zbar=beta-1j; w=s+zbar
# our K value
warr=np.array([w])
Pt=Ptilde_values(warr,zd,fac)[0]
zeta1mw=zd.eval(np.array([1.0-w]),need=0)[0]
X1=MOD.gamma_X1(complex(s)); X1z=MOD.gamma_X1(complex(np.conj(zbar)))  # X1(conj zbar)=X1(s_j)
K_a = S*(pi/N)**w*Pt*zeta1mw*X1*X1z
print("K formula (2.12):", K_a)
# (2.11) form
zz=complex(zbar)
mpw=mp.mpc(w)
zeta_w=mp.zeta(mp.mpc(w))
# S_N(w) = S(N) zeta(w) Ptilde(w)
SN = S*zeta_w*mp.mpc(Pt)
# K_- = B(1/2-s,w)+B(1/2-z,w)-B(1/2-s,1/2-z)
def B(a,b): return mp.gamma(mp.mpc(a))*mp.gamma(mp.mpc(b))/mp.gamma(mp.mpc(a)+mp.mpc(b))
s_=mp.mpc(s); z_=mp.mpc(zz); w_=s_+z_
Km = B(0.5-s_,w_)+B(0.5-z_,w_)-B(0.5-s_,0.5-z_)
K_b = N**(-w_)*SN*Km
print("K formula (2.11):", complex(K_b))
print("ratio", K_a/complex(K_b))
# check X1 gamma factorization: X1(s)=2^{1-r} sqrt(pi) Gamma(r) sin(pi r/2), r=1/2-s
r=0.5-s
X1_id = 2**(1-r)*sqrt(pi)*mp.gamma(mp.mpc(r))*mp.sin(pi*r/2)
print("X1 direct:", X1, " identity:", complex(X1_id))
