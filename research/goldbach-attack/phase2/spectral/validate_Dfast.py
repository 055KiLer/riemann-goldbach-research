import numpy as np
from kernels import D_values, D_values_fast, ZetaDeriv, singular_series
import model as MOD
primes=MOD.get_primes(2_000_000); C2=float(np.load('cache/C2.npy')[0]); S,fac=singular_series(30030,C2)
zd=ZetaDeriv(64,24)
rng=np.random.default_rng(0)
for Immax in [20,60,80]:
    w=(0.194+0.05*rng.random(6)) + 1j*rng.uniform(-Immax,Immax,6)
    a=D_values(w,zd,fac); b=D_values_fast(w,primes,fac)
    print(f"|Im|<={Immax}: max diff old-vs-fast {np.abs(a-b).max():.2e}  |D|max {np.abs(b).max():.3f}")
# large Im: compare fast against mpmath reference via Mobius h formula at one point
import mpmath as mp
mp.mp.dps=30
w=0.25-128.5625j
b=D_values_fast(np.array([w]),primes,fac)[0]
s=1.0+w
def hmp(u):
    z=mp.zeta(u); zp=mp.diff(mp.zeta,u,1); zpp=mp.diff(mp.zeta,u,2)
    return zpp/z-(zp/z)**2
# R via Mobius inverse: G(alpha)=sum_k mu(k) k h(alpha) but easier: direct numeric: h(s) - sum c_n h(ns)
def c(n):
    fs=[];m=n;d=2
    while d*d<=m:
        if m%d==0:
            fs.append(d)
            while m%d==0: m//=d
        d+=1
    if m>1: fs.append(m)
    v=1
    for p in fs: v*=(p-1)
    return v if len(fs)%2==1 else -v
R=sum(c(n)*hmp(mp.mpc(n*s)) for n in range(2,31) if c(n)!=0)
diag=sum(mp.mpf(p).__class__(0) for p in []) # none
from math import log as mlog
diagv=sum(mlog(p)**2*p**(-s)/(1-p**(-s)) for p in fac)
ref=hmp(mp.mpc(s))-R-diagv
print("large-Im point: fast=",b," mpmath-ref=",complex(ref)," rel diff",abs(b-complex(ref))/abs(complex(ref)))
