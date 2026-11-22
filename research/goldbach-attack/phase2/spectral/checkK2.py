import mpmath as mp
from math import log as mlog, pi, sqrt
mp.mp.dps=40
N=30030
alpha=1.0/mlog(N); beta=0.125
s=mp.mpc(alpha+2j); z=mp.mpc(beta-1j); w=s+z
def X1(x): return mp.gamma((mp.mpf(3)/2-x)/2)/mp.gamma((mp.mpf(3)/2+x)/2)
def B(a,b): return mp.gamma(mp.mpc(a))*mp.gamma(mp.mpc(b))/mp.gamma(mp.mpc(a)+mp.mpc(b))
Km = B(0.5-s,w)+B(0.5-z,w)-B(0.5-s,0.5-z)
Km2 = 2**(1-w)*mp.gamma(w)*mp.cos(pi*w/2)*X1(s)*X1(z)
print("K_- Beta / K_- factored gamma:", Km/Km2)
# functional equation check
lhs=mp.zeta(1-w); rhs=2*(2*mp.pi)**(-w)*mp.gamma(w)*mp.cos(pi*w/2)*mp.zeta(w)
print("FE ratio:", lhs/rhs)
# so (2.12) vs (2.11)
SN_ratio = mp.zeta(w)*Km2/(mp.pi**(-w)*mp.zeta(1-w))  # (2.11)/(2.12) should be N^{-w}*... hmm
# directly: (2.11)=N^{-w} * S(N)zeta(w)Ptilde * K_- ; (2.12)=S(N)(pi/N)^w Ptilde zeta(1-w)X1X1
ratio = (N**(-w)*mp.zeta(w)*Km2) / ((mp.pi/N)**w*mp.zeta(1-w)*X1(s)*X1(z))
print("(2.11)/(2.12) without Ptilde:", ratio)
