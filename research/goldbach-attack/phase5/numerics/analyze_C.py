"""Analyse saved C matrices: full spectrum stats, eigenvector profile, Hardy mass."""
import numpy as np, sys, glob, os
from math import log as mlog, pi

def hardy_fraction(u, N, H, m, wts, sig, tt, n):
    alpha=1.0/mlog(N); beta=0.125
    Kmax=int(round(H*m)); h=1.0/m
    vals=u/np.sqrt(wts)
    lines=[vals[:2*Kmax+1], vals[2*Kmax+1:]]
    tvals=tt[:2*Kmax+1]
    arc=[]
    for i,t in enumerate(tvals):
        if i==0: arc.append((t,t+h/2))
        elif i==len(tvals)-1: arc.append((t-h/2,t))
        else: arc.append((t-h/2,t+h/2))
    T=1000.0; dtau=0.1
    taus=np.arange(-T,T+dtau,dtau)
    def iarc(left,right,tau):
        tau=np.asarray(tau); safe=np.where(np.abs(tau)<1e-12,1.0,tau)
        val=(np.exp(-1j*tau*left)-np.exp(-1j*tau*right))/(1j*safe)
        return np.where(np.abs(tau)<1e-12,right-left,val)
    Vhat=[]
    for li in range(2):
        c=lines[li]; F=np.zeros(len(taus),dtype=complex)
        for k,(left,right) in enumerate(arc):
            if c[k]!=0: F+=c[k]*iarc(left,right,taus)
        Vhat.append(F/np.sqrt(2*pi))
    ea=np.exp(alpha*taus); eb=np.exp(beta*taus); w=ea*ea+eb*eb
    psi=(Vhat[0]*ea+Vhat[1]*eb)/w
    integ=np.sum(np.abs(psi)**2*w)*dtau
    Pnorm2=[float(np.sum(wts[:2*Kmax+1]*np.abs(lines[0])**2)),float(np.sum(wts[2*Kmax+1:]*np.abs(lines[1])**2))]
    pos=taus>=0; neg=taus<=0
    tailR=0.5*Pnorm2[1]-np.sum(np.abs(Vhat[1][pos])**2)*dtau
    tailL=0.5*Pnorm2[0]-np.sum(np.abs(Vhat[0][neg])**2)*dtau
    return (integ+tailR+tailL)/np.sum(np.abs(u)**2), Pnorm2

def analyse(fn):
    # filename encodes N,H,m: C_N{N}_H{H}.npy or C_N{N}_H{H}_m{m}.npy
    base=os.path.basename(fn)
    import re
    mm=re.match(r'C_N(\d+)_H(\d+)(?:_m(\d+))?\.npy',base)
    if not mm: 
        print("skip",fn); return
    N=int(mm.group(1)); H=float(mm.group(2)); m=int(mm.group(3)) if mm.group(3) else 8
    C=np.load(fn)
    n=C.shape[0]; Kmax=int(round(H*m)); h=1.0/m
    tks=np.arange(-Kmax,Kmax+1)/m
    tt=np.concatenate([tks,tks])
    alpha=1.0/mlog(N); beta=0.125
    sig=np.concatenate([np.full(len(tks),alpha),np.full(len(tks),beta)])
    wts=np.concatenate([np.where(np.abs(tks)<H-1e-12,1.0/m,0.5/m)]*2)
    ev=np.linalg.eigvalsh(C)
    w,V=np.linalg.eigh(C)
    lam=np.abs(ev).max(); idx=np.argmax(np.abs(ev))
    u=V[:,idx]
    reals=N-2
    S=1.3203254  # approx (2C2 for N=2p)
    tr=float(np.sum(ev)); HS=float(np.sqrt(np.sum(ev**2)))
    mass=np.abs(u)**2
    line_alpha=float(np.sum(mass[:2*Kmax+1])/np.sum(mass))
    line_beta=1-line_alpha
    # |Im s| mass
    tt_mass=np.abs(u)**2
    mean_abs_t=float(np.sum(np.abs(tt)*tt_mass)/np.sum(tt_mass))
    hf,_=hardy_fraction(u,N,H,m,wts,sig,tt,n)
    print(f"{base}: n={n} lam_max={lam:.8f} lam_min={ev.min():.8f} lam_maxpos={ev.max():.8f} tr={tr:.6f} HS={HS:.6f} | eigvec | mass alpha-line={line_alpha:.3f} beta-line={line_beta:.3f} mean|Im|={mean_abs_t:.2f} Hardy_frac={hf:.3f}")

if __name__=='__main__':
    for fn in sorted(glob.glob('cache/C_*.npy')):
        try: analyse(fn)
        except Exception as e: print("FAILED",fn,type(e).__name__,e)
