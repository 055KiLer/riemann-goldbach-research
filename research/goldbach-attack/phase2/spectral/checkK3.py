import numpy as np, mpmath as mp
from math import log as mlog, pi, sqrt
import model as MOD
from kernels import sieve, C2_constant, singular_series, ZetaDeriv, Ptilde_values, set_primes
mp.mp.dps=30
N=30030
primes=MOD.get_primes(2_000_000); set_primes(primes); C2=MOD.get_C2(); S,fac=singular_series(N,C2)
zd=ZetaDeriv(64,24)
alpha=1.0/mlog(N); beta=0.125
s=complex(alpha+2j); sj=complex(beta+1j); zbar=np.conj(sj); w=s+zbar
print("w",w)
z_em = zd.eval(np.array([1.0-w]),need=0)[0]
print("zeta(1-w) EM", z_em, "mp", complex(mp.zeta(mp.mpc(1-w))), "diff", abs(z_em-complex(mp.zeta(mp.mpc(1-w)))))
X1s=MOD.gamma_X1(s); X1z=MOD.gamma_X1(np.conj(zbar))
print("X1(s)",X1s,"mp", complex(mp.gamma((mp.mpf(3)/2-mp.mpc(s))/2)/mp.gamma((mp.mpf(3)/2+mp.mpc(s))/2)))
print("X1(zbar)",X1z," mp X1(np.conj(zbar))", complex(mp.gamma((mp.mpf(3)/2-mp.mpc(zbar))/2)/mp.gamma((mp.mpf(3)/2+mp.mpc(zbar))/2)))
Pt=Ptilde_values(np.array([w]),zd,fac)[0]
print("Ptilde",Pt)
# full formula (2.12) in mpmath with same Pt converted
lhs = mp.mpf(S)*(mp.pi/N)**mp.mpc(w)*mp.mpc(Pt)*mp.zeta(1-mp.mpc(w))*(mp.gamma((mp.mpf(3)/2-mp.mpc(s))/2)/mp.gamma((mp.mpf(3)/2+mp.mpc(s))/2))*(mp.gamma((mp.mpf(3)/2-mp.mpc(zbar))/2)/mp.gamma((mp.mpf(3)/2+mp.mpc(zbar))/2))
print("(2.12) mpmath:", complex(lhs))
# (2.11) mpmath
w_=mp.mpc(w); s_=mp.mpc(s); z_=mp.mpc(zbar)
def B(a,b): return mp.gamma(mp.mpc(a))*mp.gamma(mp.mpc(b))/mp.gamma(mp.mpc(a)+mp.mpc(b))
Km = B(0.5-s_,w_)+B(0.5-z_,w_)-B(0.5-s_,0.5-z_)
rhs = N**(-w_)*mp.mpf(S)*mp.zeta(w_)*mp.mpc(Pt)*Km
print("(2.11) mpmath:", complex(rhs))
print("ratio", complex(lhs/rhs))
