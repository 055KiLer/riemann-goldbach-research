import numpy as np, time
from math import log as mlog, pi
from lmat import Config, node_meta, build_G, odd_char_index
from kernels import (sieve, C2_constant, singular_series, ZetaDeriv, D_values, Ptilde_values, set_primes)
from chars import CharacterGroup
import model as MOD

N=30030; H=40.0; m=16
cfg=Config(N,H,m=m); Kmax=cfg.Kmax
sig,tt,wts=node_meta(cfg); n=len(sig)
print(f"H={H} n={n}",flush=True)
primes=MOD.get_primes(2_000_000); set_primes(primes); C2=MOD.get_C2(); S,fac=singular_series(N,C2)
cg=CharacterGroup(N)
t0=time.time(); G,idx_odd,inv=build_G(cfg,cg,verbose=False); print("G",time.time()-t0,flush=True)
np.save('cache/G_H40.npy',G)
phi=cg.phi
P_herm=(2.0/phi)*(G@G.conj().T)
# row permutation S: s_{S(i)}=conj(s_i)
Sperm=np.empty(n,dtype=int)
for li in range(2):
    base=li*(2*Kmax+1)
    for idx,k in enumerate(range(-Kmax,Kmax+1)): Sperm[base+idx]=base+(Kmax-k)
Gbar=np.conj(G[Sperm,:])
P_holo=(2.0/phi)*(Gbar@G.T)   # = P_N(s_i,s_j)=(2/phi) sum g_chi(s_i) g_{bar chi}(s_j)
P2=(2.0/phi)*(G@G.T)
# w matrices
nimag=4*Kmax+1
reals=np.array([2*cfg.alpha, cfg.alpha+0.125, 0.25])
wdist=np.empty(3*nimag,dtype=complex)
for r in range(3): wdist[r*nimag:(r+1)*nimag]=reals[r]+1j*(np.arange(nimag)-2*Kmax)/m
zd=ZetaDeriv(64,24)
t0=time.time(); Ddist=D_values(1.0*wdist,zd,fac); Ptdist=Ptilde_values(wdist,zd,fac); z1mw=zd.eval(1.0-wdist,need=0)
print("kernel values",time.time()-t0,flush=True)
li=np.concatenate([np.zeros(2*Kmax+1,dtype=int), np.ones(2*Kmax+1,dtype=int)])
ki=np.concatenate([np.arange(-Kmax,Kmax+1), np.arange(-Kmax,Kmax+1)])
ridx=(li[:,None]+li[None,:]).astype(int)
iidx_h=(ki[:,None]-ki[None,:]+2*Kmax).astype(int)   # t_i - t_j  (hermitian w=s_i+conj s_j)
iidx_ho=(ki[:,None]+ki[None,:]+2*Kmax).astype(int)  # t_i + t_j  (holomorphic w=s_i+s_j)
def DK(iidx):
    flat=ridx*nimag+iidx
    Dm=Ddist[flat].reshape(n,n)
    Mm=(S*(pi/N)**wdist*Ptdist*z1mw)[flat].reshape(n,n)
    X1=np.array([MOD.gamma_X1(complex(sig[i]+1j*tt[i])) for i in range(n)])
    Km_herm=(X1[:,None]*Mm)*np.conj(X1)[None,:]
    Km_holo=(X1[:,None]*Mm)*X1[None,:]
    return Dm,Mm,Km_herm,Km_holo,X1
D_h,M_h,Kh_herm,Kh_holo,X1=DK(iidx_h)
D_o,M_o,Ko_herm,Ko_holo,X1=DK(iidx_ho)
A=np.sqrt(wts)/(1.0+sig+1j*tt)
Ah=np.sqrt(wts)/(1.0+sig-1j*tt)   # conj(A)
def herm(C,label):
    ev=np.linalg.eigvalsh(C)
    o=np.argsort(-np.abs(ev)); ev=ev[o]
    print(f"[{label}] herm=True max|eig|={np.abs(ev).max():.6f} top={np.round(ev[:5],6)} bottom={np.round(ev[-3:],6)}",flush=True)
    return ev
def geneig(C,label):
    ev=np.linalg.eigvals(C)
    o=np.argsort(-np.abs(ev)); ev=ev[o]
    print(f"[{label}] max|eig|={np.abs(ev).max():.6f} top={np.round(ev[:5],6)} real_range=({ev.real.min():.4f},{ev.real.max():.4f})",flush=True)
    return ev
t0=time.time()
E=P_herm-D_h-Kh_herm
C=(A[:,None]*E)*np.conj(A)[None,:]
ev0=herm(C,"V0 herm E, herm denom (paper recipe)")
print("eigh time",time.time()-t0,flush=True)
# V1:
E1=P2-D_o-Ko_holo
C1=(A[:,None]*E1)*A[None,:]
geneig(C1,"V1 GG^T, holo D/K, holo denom")
# V2:
C2v=(A[:,None]*E1)*np.conj(A)[None,:]
geneig(C2v,"V2 GG^T, holo D/K, herm denom")
# V3 literal (2.6): P_holo
E3=P_holo-D_o-Ko_holo
C3=(A[:,None]*E3)*A[None,:]
geneig(C3,"V3 P_holo, holo D/K, holo denom")
# V4
C4=(A[:,None]*E3)*np.conj(A)[None,:]
geneig(C4,"V4 P_holo, holo D/K, herm denom")
# V5: herm E but holo denom
C5=(A[:,None]*E)*A[None,:]
geneig(C5,"V5 herm E, holo denom")
# V6: herm E herm denom but weights as w (not sqrt)
Kherm=E/((1.0+sig[:,None]+1j*tt[:,None])*(1.0+sig[None,:]-1j*tt[None,:]))
C6=(wts[:,None]*Kherm)*wts[None,:]
herm(C6,"V6 WKW weights-not-sqrt")
# V7: herm E / (2pi)
C7=C/(2*pi); herm(C7,"V7 paper/2pi")
# V8: normalized weights 1/(2H) per line (sum of weights =1 per line)
w2=np.concatenate([np.full(2*Kmax+1,1.0/(2*H))]*2)
C8=(np.sqrt(w2[:,None]*w2[None,:])*E)/(((1.0+sig[:,None]+1j*tt[:,None])*(1.0+sig[None,:]-1j*tt[None,:])))
herm(C8,"V8 normalized weights 1/(2H)")
# also print |C|max of V0
print("V0 |C|max",np.abs(C).max()," |C|sum/n",np.abs(C).sum()/n,flush=True)
