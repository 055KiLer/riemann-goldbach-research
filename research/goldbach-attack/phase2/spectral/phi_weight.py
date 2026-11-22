import numpy as np
from math import log as mlog, pi
N=30030
def phi(u):
    u=np.asarray(u,dtype=float); x=6*u-3
    out=np.zeros_like(u); m=(np.abs(x)<1)
    out[m]=np.exp(-1.0/(1.0-x[m]**2))
    return out
def Phi(u):
    return np.sqrt(np.asarray(u,dtype=float))*phi(u)
# trapezoid grid on [1/3,2/3], Phi flat at endpoints
M=4000
uu=np.linspace(1/3,2/3,M)
h=(uu[-1]-uu[0])/(M-1)
wq=np.full(M,h); wq[0]*=0.5; wq[-1]*=0.5
ph=Phi(uu)
cphi=float(np.sum(wq*phi(uu)**2))
# careful: trapezoid over [1/3,2/3] with endpoints phi=0 is fine
print("cphi =", repr(cphi))
def phitilde(ts, sigma=1.0/9):
    ts=np.asarray(ts,dtype=float)
    s=sigma+1j*ts
    return np.sum(wq[None,:]*ph[None,:]*uu[None,:]**(s[:,None]-1),axis=1)
for t in [0,5,10,20,30,40,60,80,100]:
    v=phitilde(np.array([t]))[0]
    print(f"Phi_tilde t={t}: |.|={abs(v):.3e}")
# direct arithmetic G(N)
lam=np.zeros(N+1)
sieve=np.ones(N+1,bool); sieve[:2]=False
for p in range(2,int(N**0.5)+1):
    if sieve[p]: sieve[p*p::p]=False
for p in np.nonzero(sieve)[0]:
    pk=p
    while pk<=N:
        lam[pk]=mlog(p); pk*=p
n=np.arange(1,N); m=N-n
mask=(np.gcd(n*m,N)==1)
G=float(np.sum(lam[n]*lam[m]*Phi(n/N)*Phi(m/N)*mask)/N)
import os
C2=float(np.load('cache/C2.npy')[0])
fac=[3,5,7,11,13]; S=2*C2
for p in fac: S*=(p-1)/(p-2)
delta=np.sqrt(S/N)*mlog(N)**1.5
r=cphi*S-G
print("S=",repr(S)," G=",repr(G))
print("cphi*S=",repr(cphi*S)," r=",repr(r)," r/delta=",r/delta)
np.save('cache/cphi.npy',np.array([cphi]))
