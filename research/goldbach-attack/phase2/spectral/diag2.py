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
# row permutation S: s_{S(i)} = conj(s_i)
Sperm=np.empty(n,dtype=int)
# node ordering: lines; within line k -> -k
for li in range(2):
    base=li*(2*Kmax+1)
    for idx,k in enumerate(range(-Kmax,Kmax+1)):
        Sperm[base+idx]=base+(Kmax-k)
w_=wts
A=np.sqrt(w_)/(1.0+sig+1j*tt)
# hermitian kernel E(s_i, conj(s_j))
P_herm=(2.0/cg.phi)*(G@G.conj().T)
# holomorphic P_N(s_i,s_j) = (2/phi) sum g_chi(s_i) g_{bar chi}(s_j)
# g_{bar chi}(s_i) = conj(g_chi(conj(s_i))) = conj(G[S(i), chi])
Gbar=np.conj(G[Sperm,:])
P_holo=(2.0/cg.phi)*(Gbar@G.T)
# P2 = (2/phi) sum g_chi(s_i) g_chi(s_j) = G G^T
P2=(2.0/cg.phi)*G@G.T
nimag=4*Kmax+1
reals=np.array([2*cfg.alpha, cfg.alpha+0.125, 0.25])
def build_DK(imagfun):
    wdist=np.empty(3*nimag,dtype=complex)
    for r in range(3): wdist[r*nimag:(r+1)*nimag]=reals[r]+1j*(np.arange(nimag)-2*Kmax)/m
    zd=ZetaDeriv(64,24)
    Ddist=D_values(1.0*wdist,zd,fac); Ptdist=Ptilde_values(wdist,zd,fac); zeta1mw=zd.eval(1.0-wdist,need=0)
    li=np.concatenate([np.zeros(2*Kmax+1,dtype=int), np.ones(2*Kmax+1,dtype=int)])
    ki=np.concatenate([np.arange(-Kmax,Kmax+1), np.arange(-Kmax,Kmax+1)])
    iidx=imagfun(ki)
    ridx=(li[:,None]+li[None,:]).astype(int)
    flat=ridx*nimag+iidx
    Dmat=Ddist[flat].reshape(n,n)
    Mdist=S*(pi/N)**wdist*Ptdist*zeta1mw
    Mmat=Mdist[flat].reshape(n,n)
    X1=np.array([MOD.gamma_X1(complex(sig[i]+1j*tt[i])) for i in range(n)])
    Kmat=(X1[:,None]*Mmat)*X1[None,:]  # holomorphic X1(s_i)X1(s_j)
    return Dmat,Kmat
# D,K for holomorphic arguments (conj s_j -> s_j): w=s_i+s_j, imag t_i+t_j
D_holo,K_holo=build_DK(lambda ki: (ki[:,None]+ki[None,:]+2*Kmax).astype(int))
# for hermitian we computed before; redo with conj: w=s_i+conj(s_j): imag t_i-t_j
D_h,K_h=build_DK(lambda ki: (ki[:,None]-ki[None,:]+2*Kmax).astype(int))

def eigs(C,label):
    herm=np.allclose(C,C.conj().T)
    ev=np.linalg.eigvalsh(C) if herm else np.linalg.eigvals(C)
    order=np.argsort(-np.abs(ev))
    evs=ev[order]
    print(f"{label}: herm={herm} top |eig| {np.round(np.abs(evs[:6]),5)}  maxabs {np.abs(ev).max():.5f}  minreal {ev.real.min():.4f} maxreal {ev.real.max():.4f}")
    return ev

E_herm=P_herm-D_h-K_h
C_herm=(A[:,None]*E_herm)*np.conj(A)[None,:]
eigs(C_herm,"hermitian E(s,conj z) / (1+s)(1+conj z)")
E_holo=P_holo-D_holo-K_holo
A2=np.sqrt(w_)/(1.0+sig+1j*tt)
C_holo=(A2[:,None]*E_holo)*A2[None,:]
eigs(C_holo,"holo E(s,z)/(1+s)(1+z)")
C_mix=(A2[:,None]*E_holo)*np.conj(A2)[None,:]
eigs(C_mix,"holo E, herm denominator")
C2v=(A[:,None]*E_herm)*A2[None,:]
eigs(C2v,"herm E, holo denominator")

# variant: P=GG^T (no conjugate), D/K also holomorphic (s_i+s_j)
E_v1=P2-D_holo-K_holo
eigs((A2[:,None]*E_v1)*A2[None,:],"P=GG^T, D,K holo, holo denom")
eigs((A[:,None]*E_v1)*np.conj(A)[None,:],"P=GG^T, holo D/K, herm denom")
# variant: P=GG^T with D/K hermitian
E_v2=P2-D_h-K_h
eigs((A[:,None]*E_v2)*np.conj(A)[None,:],"P=GG^T, herm D/K, herm denom")
# variant: P_holo with D/K hermitian, holo denom
E_v3=P_holo-D_h-K_h
eigs((A2[:,None]*E_v3)*A2[None,:],"P_holo, herm D/K, holo denom")
# weights as w (not sqrt) => C = W K W
E_herm=P_herm-D_h-K_h
Kherm=E_herm/((1.0+sig[:,None]+1j*tt[:,None])*(1.0+sig[None,:]-1j*tt[None,:]))
eigs((w_[:,None]*Kherm)*w_[None,:],"C = W K W (weights not sqrt)")
# with 1/(2pi)
eigs((w_[:,None]*Kherm)*w_[None,:]/(2*np.pi),"C = WKW/(2pi)")
# scalar weights = h*? try weights normalized
