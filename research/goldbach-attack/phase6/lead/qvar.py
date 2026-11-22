"""Character-free variance prediction: for top eigenvectors q of Q=D+K, compute d1=<D q,q> (=(2/phi)Sum Lambda^2|c_n|^2 diagonal),
k1=<K q,q>; if fluctuation along fixed direction: lambda_E ~ z*sigma/sqrt(n) with sigma^2 = Var_chi(|<f_chi,q>|^2) ~ d1^2 (Gaussian heuristic)
=> predicted ratio_inf ~ 2*z*d1^2/(log^{3/2} sqrt(S)) / ??? Let's just report d1, k1, d1/lQ, d1/(logN)^p fits."""
import sys, math, json, time
import numpy as np
sys.path.insert(0,'/home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase2/spectral')
from lmat import Config, node_meta
from kernels import singular_series, ZetaDeriv, D_values_fast, Ptilde_values, set_primes
import mpmath as mp
CACHE='/home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase2/spectral/cache'
primes=np.load(f'{CACHE}/primes_2000000.npy'); set_primes(primes)
C2=float(np.load(f'{CACHE}/C2.npy')[0])
def gamma_X1(s):
    return complex(mp.gamma((mp.mpf(3)/2-mp.mpc(s))/2)/mp.gamma((mp.mpf(3)/2+mp.mpc(s))/2))
def isprime(n):
    if n<2: return False
    for p in [2,3,5,7,11,13,17,19,23,29,31,37]:
        if n%p==0: return n==p
    d=n-1;s=0
    while d%2==0: s+=1; d//=2
    for a in [2,3,5,7,11,13,17,19,23,29,31,37]:
        x=pow(a,d,n)
        if x==1 or x==n-1: continue
        for _ in range(s-1):
            x=x*x%n
            if x==n-1: break
        else: return False
    return True
def find_p(t):
    p=t
    if p%4!=3: p += (3-p%4)%4
    while not isprime(p): p+=4
    return p
def stats(N,H=8.0,m=2):
    mp.mp.dps=22
    cfg=Config(N,H,m=m); S,fac=singular_series(N,C2)
    sig,tt,wts=node_meta(cfg); n=len(sig)
    nimag=4*cfg.Kmax+1
    reals=np.array([2*cfg.alpha,cfg.alpha+0.125,0.25])
    wdist=np.empty(3*nimag,dtype=complex)
    for r in range(3):
        wdist[r*nimag:(r+1)*nimag]=reals[r]+1j*(np.arange(nimag)-2*cfg.Kmax)/m
    zd=ZetaDeriv(K=64,J=24)
    Ddist=D_values_fast(1.0*wdist,primes,fac)
    Ptdist=Ptilde_values(wdist,zd,fac,Pcut=200000)
    zeta1mw=zd.eval(1.0-wdist,need=0)
    X1=np.array([gamma_X1(complex(sig[i]+1j*tt[i])) for i in range(n)])
    li=np.concatenate([np.zeros(2*cfg.Kmax+1,dtype=int),np.ones(2*cfg.Kmax+1,dtype=int)])
    ki=np.concatenate([np.arange(-cfg.Kmax,cfg.Kmax+1),np.arange(-cfg.Kmax,cfg.Kmax+1)])
    ridx=(li[:,None]+li[None,:]).astype(int); iidx=(ki[:,None]-ki[None,:]+2*cfg.Kmax).astype(int)
    flat=ridx*nimag+iidx
    Dmat=Ddist[flat].reshape(n,n)
    Mmat=(S*(np.pi/N)**wdist*Ptdist*zeta1mw)[flat].reshape(n,n)
    Kmat=(X1[:,None]*Mmat)*np.conj(X1)[None,:]
    Q=Dmat+Kmat
    A=np.sqrt(wts)/(1.0+sig+1j*tt)
    CQ=(A[:,None]*Q)*np.conj(A)[None,:]
    CD=(A[:,None]*Dmat)*np.conj(A)[None,:]
    ev,V=np.linalg.eigh(CQ)
    idx=np.argsort(-np.abs(ev))[:5]
    out={}
    for j,k in enumerate(idx):
        q=V[:,k]
        d1=float(np.real(q.conj()@CD@q)); k1=float(np.real(q.conj()@CQ@q))-d1
        out[f'top{j+1}']=dict(mu=float(ev[k]),d1=d1,k1=k1)
    return dict(N=N,H=H,m=m,logN=math.log(N),S=S,stats=out)
if __name__=='__main__':
    targets=[2e4,5e4,1e5,2e5,5e5,1e6,2e6,5e6,1e7,3e7,1e8,3e8,1e9]
    rows=[]
    for tg in targets:
        p=find_p(int(tg)); N=2*p
        t0=time.time(); r=stats(N); rows.append(r)
        s=r['stats']; logN=r['logN']
        line=f"N={N:>10d} logN={logN:6.3f} lQ={s['top1']['mu']:9.3f} d1={s['top1']['d1']:12.3f} k1={s['top1']['k1']:10.3f} d1/lQ={s['top1']['d1']/s['top1']['mu']:10.3f} d1/log^1.5={s['top1']['d1']/logN**1.5:10.2f} d1/log^2={s['top1']['d1']/logN**2:9.3f}"
        print(line,flush=True)
    json.dump(rows,open('qvar_rows.json','w'))
