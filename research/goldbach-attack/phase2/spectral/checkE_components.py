import numpy as np, time
from math import log as mlog, pi
exec(open('checkE.py').read().split('# ---------------- double contour integral')[0])
# now available: P, Dmat, Kmat, ts, Phit(no), E, sigma, dt, M, S, fac, cg, ...
# recompute Phit
def phi(u):
    x=6*u-3; out=np.zeros_like(u); mm=np.abs(x)<1
    out[mm]=np.exp(-1/(1-x[mm]**2)); return out
def Phi(u): return np.sqrt(u)*phi(u)
Mu=4000
uu=np.linspace(1/3,2/3,Mu); hu=(uu[-1]-uu[0])/(Mu-1)
wq=np.full(Mu,hu); wq[0]/=2; wq[-1]/=2
ph=Phi(uu)
base=wq*ph*uu**(sigma-1.0)
Phit=np.empty(M,dtype=complex)
for i0 in range(0,M,100):
    sl=slice(i0,min(i0+100,M))
    Phit[sl]=np.exp(1j*np.outer(ts[sl],np.log(uu))) @ base
wquad=np.full(M,dt); wquad[0]/=2; wquad[-1]/=2
Ew=(wquad*Phit*np.exp(1j*ts*mlog(N)))
fac2=(1.0/(4*pi*pi))*N**(2*sigma)
def quad(X): return fac2*np.sum(Ew[:,None]*X*Ew[None,:])
JP=quad(P); JD=quad(Dmat); JK=quad(Kmat); JE=quad(E)
print("J_P =",JP,"  J_D =",JD,"  J_K =",JK,"  J_E =",JE, flush=True)
# direct arithmetic
lam=np.zeros(N+1)
sieve=np.ones(N+1,bool); sieve[:2]=False
for p in range(2,int(N**0.5)+1):
    if sieve[p]: sieve[p*p::p]=False
for p in np.nonzero(sieve)[0]:
    pk=p
    while pk<=N: lam[pk]=mlog(p); pk*=p
nn=np.arange(1,N); mm=N-nn
mask=np.gcd(nn*mm,N)==1
phiN=phi(nn/N)
cphi=float(np.sum(wq*phi(uu)**2))
# D(N)=(1/N) sum_{(n,N)=1} Lambda^2(n) phi(n/N)^2
Ddir=float(np.sum(lam[nn]**2*phiN**2*(np.gcd(nn,N)==1)))/N
# P(N)=(2/phi) sum_{chi odd}|Pchi|^2, Pchi = 1/sqrt(N) sum_n Lambda(n)chi(n)phi(n/N)
an=lam[nn]*phiN/np.sqrt(N)
# vector over units residues mod N: n<N, so unit position lookup
# cg.units sorted ascending; build index map for units
unit_pos=np.full(N, -1, dtype=np.int64)
unit_pos[cg.units]=np.arange(len(cg.units))
B=np.zeros(cg.phi, dtype=complex)
sel=(unit_pos[nn]>=0)
B[unit_pos[nn[sel]]]=an[sel]
Bhat=cg.forward(B)
from lmat import odd_char_index
idx_odd,inv=odd_char_index(cg)
Pchi=Bhat[idx_odd]
Pdir=float((2.0/cg.phi)*np.sum(np.abs(Pchi)**2))
print("D(N) direct =",repr(Ddir)," P(N) direct =",repr(Pdir)," cphi*S =",repr(cphi*S), flush=True)
print("compare: J_D/Ddir =",JD/Ddir," J_P/Pdir =",JP/Pdir," -J_K/(cphi*S) =",-JK/(cphi*S), flush=True)
print("r check: J_E =",JE," D-P+cphi*S =",Ddir-Pdir+cphi*S, " ratio", JE/(Ddir-Pdir+cphi*S), flush=True)
np.save('cache/fac2.npy',np.array([cphi]))
