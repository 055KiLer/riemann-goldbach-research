"""Independent validation of E_N via the contour identity (2.34)/(2.35):
   r(N) = c_phi S(N) - G(N) = (1/(2 pi i)^2) int_(sigma) int_(sigma) N^{s+z} Phit(s)Phit(z) E_N(s,z) ds dz
with the explicit weight phi(u)=exp(-1/(1-(6u-3)^2)) on [1/3,2/3].
This validates P_N (character FFT + Hurwitz L'/L), D_N and K_N at interior points."""
import numpy as np, time
from math import log as mlog, pi
from chars import CharacterGroup
from hurwitz import HurwitzEM
from kernels import ZetaDeriv, D_values, D_values_fast, Ptilde_values, singular_series, set_primes
import model as MOD

N=30030
import sys, os
sigma=float(os.environ.get('SIGMA',1.0/9.0))
T=float(os.environ.get('TGRID',100.0)); dt=float(os.environ.get('DT',0.25))
M=int(round(2*T/dt))+1
ts=-T+dt*np.arange(M)   # symmetric grid
print("grid M=",M," dt",dt, flush=True)
primes=MOD.get_primes(2_000_000); set_primes(primes); C2=MOD.get_C2(); S,fac=singular_series(N,C2)
cg=CharacterGroup(N)
em=HurwitzEM(64,24)
# ---------------- Gp: g_chi(sigma + i t) for t>=0 ----------------
tpos=ts[M//2:]   # 0..T
A=len(cg.units); logN=mlog(N)
x=cg.units.astype(np.float64)/N
# forward of character sums
idxs=np.arange(len(tpos))
Gpos=np.zeros((len(tpos), cg.phi), dtype=complex)
t0=time.time()
for ii,t in enumerate(tpos):
    u=0.5+sigma+1j*t
    Bd,Ad=em.zeta_array(u,x)
    Bh=cg.forward(Bd); Ah=cg.forward(Ad)
    Gpos[ii]=(Ah/Bh - logN)
print("Gpos time",time.time()-t0, flush=True)
# full G on symmetric grid: row for -t = conj(Gpos[inv])
idx_odd, inv = MOD_odd = None,None
from lmat import odd_char_index
idx_odd, inv = odd_char_index(cg)   # position mapping in odd-char ordering
# we need g_chi for all chars; here use full char ordering (phi chars) and odd subset later
# g_chi(sigma - i t) = conj(g_{bar chi}(sigma + i t)) ; bar chi = inv permutation in flat order
# build inverse permutation on FULL character set
posfull=-np.ones(cg.phi,dtype=np.int64); posfull[:]=np.arange(cg.phi)
# full inv: kflat -> kflat(-k)
full_inv=np.zeros(cg.phi,dtype=np.int64)
for kf in range(cg.phi):
    k=[cg.kvecs[i][kf] for i in range(len(cg.orders))]
    kinv=[(-kk)%o for kk,o in zip(k,cg.orders)]
    full_inv[kf]=sum(kk*st for kk,st in zip(kinv,cg.strides))
idx_all=np.arange(cg.phi)
# Gfull[ii, chi] = g_chi(sigma + i t)
# row for t=-tpos[ii] : g_chi(sigma - i t) = conj(g_{bar chi}(sigma + i t)) -> conj(Gpos[ii, full_inv[chi]])
# construct G rows in order ts: index map: ts[i] for i<M//2 is negative; ts[M//2+ii]=tpos[ii]
G=np.zeros((M,cg.phi),dtype=complex)
G[M//2:,:]=Gpos
for ii in range(1,M//2+1):
    # ts[M//2-ii] = -tpos[ii]
    G[M//2-ii,:]=np.conj(Gpos[ii, full_inv])
# odd subset
Godd=G[:, idx_odd]
nodd=len(idx_odd)
# ---------------- P matrix (holomorphic both variables) ----------------
t0=time.time()
# Hbar[k,chi] = g_{bar chi}(sigma+i ts[k]) = G[k, full_inv]
Hbar=G[:, full_inv]
P=(2.0/cg.phi)*(Godd @ Hbar[:,idx_odd].T)
print("P time",time.time()-t0, flush=True)
# ---------------- D on distinct w values ----------------
wre=2*sigma
sums=(ts[:,None]+ts[None,:]).ravel()   # in [-2T,2T] step dt
# unique sums: from -2T to 2T step dt
sgrid=-2*T+dt*np.arange(4*int(round(T/dt))+1)
assert len(sgrid)==4*int(round(T/dt))+1
wdist=wre+1j*sgrid
zd=ZetaDeriv(64,24)
t0=time.time(); Ddist=D_values_fast(wdist,primes,fac); Ptdist=Ptilde_values(wdist,zd,fac); z1mw=zd.eval(1.0-wdist,need=0)
print("D,K values time",time.time()-t0, "nw",len(wdist), flush=True)
sidx=np.rint((sums+2*T)/dt).astype(int)
Dmat=Ddist[sidx].reshape(M,M)
# ---------------- X1 and K ----------------
X1=np.array([MOD.gamma_X1(complex(sigma+1j*t)) for t in ts])
Mdist=S*(pi/N)**wdist*Ptdist*z1mw
Mmat=Mdist[sidx].reshape(M,M)
Kmat=(X1[:,None]*Mmat)*X1[None,:]
E=P-Dmat-Kmat
print("E |max|",np.abs(E).max()," mean",np.abs(E).mean(), flush=True)
# symmetry checks: E should be symmetric holomorphic: E(s,z)=E(z,s) -> E^T=E
print("E sym err",np.abs(E-E.T).max()/np.abs(E).max(), flush=True)
# ---------------- Phitilde at grid ----------------
def phi(u):
    x=6*u-3; out=np.zeros_like(u); mm=np.abs(x)<1
    out[mm]=np.exp(-1/(1-x[mm]**2)); return out
def Phi(u): return np.sqrt(u)*phi(u)
Mu=4000
uu=np.linspace(1/3,2/3,Mu); hu=(uu[-1]-uu[0])/(Mu-1)
wq=np.full(Mu,hu); wq[0]/=2; wq[-1]/=2
ph=Phi(uu)
# Phit(sigma+it)=sum wq ph uu^{sigma-1+it}
base=wq*ph*uu**(sigma-1.0)
t0=time.time()
Phit=np.empty(M,dtype=complex)
for i0 in range(0,M,100):
    sl=slice(i0,min(i0+100,M))
    Phit[sl]=np.exp(1j*np.outer(ts[sl],np.log(uu))) @ base
print("Phit time",time.time()-t0, "Phit(0)=",Phit[M//2], flush=True)
# ---------------- double contour integral ----------------
wquad=np.full(M,dt); wquad[0]/=2; wquad[-1]/=2
phase=np.exp(1j*np.outer(ts+ts[0],np.full(M,logN)))  # e^{i t_j logN}; sum t_j+t_k
# r = -(1/(4 pi^2)) N^{2 sigma} sum_{j,k} wquad_j wquad_k Phit_j Phit_k e^{i(t_j+t_k)logN} E_jk
e_j=np.exp(1j*ts*logN)
fac2=(1.0/(4*pi*pi))*N**(2*sigma)
r_num=fac2*np.sum((wquad*Phit*e_j)[:,None]*E*(wquad*Phit*e_j)[None,:])
print("r_num =",r_num, flush=True)
# direct r
def Gdir():
    lam=np.zeros(N+1)
    sieve=np.ones(N+1,bool); sieve[:2]=False
    for p in range(2,int(N**0.5)+1):
        if sieve[p]: sieve[p*p::p]=False
    for p in np.nonzero(sieve)[0]:
        pk=p
        while pk<=N: lam[pk]=mlog(p); pk*=p
    nn=np.arange(1,N); mm=N-nn
    mask=np.gcd(nn*mm,N)==1
    Gn=float(np.sum(lam[nn]*lam[mm]*phi(nn/N)*phi(mm/N)*mask)/N)
    cphi=float(np.sum(wq*phi(uu)**2))
    return cphi*S-Gn
r_direct=Gdir()
print("r_direct =",repr(r_direct), "  ratio r_num/r_direct =", r_num/r_direct, flush=True)
delta=np.sqrt(S/N)*mlog(N)**1.5
print("r_direct/delta =",r_direct/delta," delta=",delta)
