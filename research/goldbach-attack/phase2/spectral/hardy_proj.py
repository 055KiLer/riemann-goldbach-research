"""Hardy-subspace projection of finite-model eigenvectors (Lemma 5.2 Fourier representation).

For v in L^2(Gamma_N) with line traces v_alpha, v_beta, its trace is in H_N iff
   hat v_alpha(tau) = psi(tau) e^{alpha tau},  hat v_beta(tau) = psi(tau) e^{beta tau}
with psi in L^2(w dtau), w = e^{2 alpha tau}+e^{2 beta tau}. The orthogonal projection is
   psi(tau) = (hat v_alpha e^{alpha tau} + hat v_beta e^{beta tau}) / w(tau),
   ||P_H v||^2 = int |psi|^2 w dtau.
We build v from the maximal eigenvector u of C: v = sum u_i phi_i, phi_i = w_i^{-1/2}1_{arc_i}.
"""
import numpy as np, sys, time
from math import pi, sqrt, sin, exp
import model as MOD

def arcs(node_t, h, H):
    """return list of (left,right) arcs; node_t sorted with mesh h, endpoints at +-H."""
    n=len(node_t); out=[]
    for i,t in enumerate(node_t):
        if i==0: out.append((t, t+h/2))
        elif i==n-1: out.append((t-h/2, t))
        else: out.append((t-h/2, t+h/2))
    return out

def integral_arc(left,right,tau):
    """int_left^right e^{-i tau t} dt  (vectorised in tau)"""
    tau=np.asarray(tau)
    safe=np.where(np.abs(tau)<1e-12, 1.0, tau)
    val=(np.exp(-1j*tau*left)-np.exp(-1j*tau*right))/(1j*safe)
    return np.where(np.abs(tau)<1e-12, right-left, val)

def hardy_proj(H, N, m=16, verbose=True):
    res=MOD.build_model(N=N,H=H,m=m,return_C=True)
    C=res['C']; sig=res['sig']; tt=res['tt']; wts=res['wts']
    alpha=1.0/__import__('math').log(N); beta=0.125; h=1.0/m; Kmax=int(round(H*m)); nn=2*(2*Kmax+1)
    from scipy.sparse.linalg import eigsh
    ev,u=eigsh(C,k=1,which='LM',return_eigenvectors=True)
    lam=float(ev[0]); vec=u[:,0]; vec=vec/np.linalg.norm(vec)
    delta=res['delta']
    # boundary values v_i = u_i / sqrt(w_i)
    vals=vec/np.sqrt(wts)
    lines=[vals[:2*Kmax+1], vals[2*Kmax+1:]]
    tvals=tt[:2*Kmax+1]
    arc=arcs(tvals,h,H)
    normv2=float(np.sum(np.abs(vec)**2))  # = sum w |c|^2 with c=u/sqrt(w)
    # tau grid
    T=1000.0; dtau=0.1
    taus=np.arange(-T,T+dtau,dtau)
    # Fourier transforms of the two line traces
    Vhat=[]
    for li in range(2):
        c=lines[li]; aline=sig[2*Kmax+1]*0+ (alpha if li==0 else beta)  # not needed
        F=np.zeros(len(taus),dtype=complex)
        for k,(left,right) in enumerate(arc):
            if c[k]==0.0: continue
            # integrate e^{-i tau t} on arc: shift by midpoint
            mid=0.5*(left+right); half=0.5*(right-left)
            F += c[k]*np.exp(-1j*taus*mid)*(np.sinc(taus*half/np.pi))*2*half if False else c[k]*integral_arc(left,right,taus)
        Vhat.append(F/np.sqrt(2*pi))
    # psi and norm
    ea=np.exp(alpha*taus); eb=np.exp(beta*taus); w=ea*ea+eb*eb
    psi=(Vhat[0]*ea+Vhat[1]*eb)/w
    integ=np.sum(np.abs(psi)**2*w)*dtau
    # tails beyond T: int_T^inf |vhat_beta|^2 dtau and int_-inf^{-T}|vhat_alpha|^2 dtau
    # use Plancherel: total ||v_l||^2 = sum w_k |c_k|^2
    Pnorm2=[float(np.sum(wts[:2*Kmax+1]*np.abs(lines[0])**2)), float(np.sum(wts[2*Kmax+1:]*np.abs(lines[1])**2))]
    pos=(taus>=0)
    tailR=0.5*Pnorm2[1]-np.sum(np.abs(Vhat[1][pos])**2)*dtau   # int_0^inf |vhat_beta|^2
    neg=(taus<=0)
    tailL=0.5*Pnorm2[0]-np.sum(np.abs(Vhat[0][neg])**2)*dtau   # int_-inf^0 |vhat_alpha|^2
    total=integ+tailR+tailL
    ratio=total/normv2
    print(f"H={H} N={N} m={m}: lambda_max={lam:.10f} delta_N={delta:.10f} ratio_finite={lam/delta:.10f}")
    print(f"   ||v||^2={normv2:.12f}  ||P_H v||^2={total:.10f}  hardy_fraction={ratio:.10f}  nonHardy_mass={1-ratio:.3e}")
    print(f"   check ||v_alpha||^2+||v_beta||^2={sum(Pnorm2):.12f}  tails R/L={tailR:.3e}/{tailL:.3e}")
    return dict(H=H,N=N,lam=lam,delta=delta,finite_ratio=lam/delta,hardy_frac=ratio)

if __name__=='__main__':
    for H,N in [(40,30030),(40,40022),(60,40022)]:
        try: hardy_proj(H,N)
        except Exception as e:
            print("FAILED",H,N,type(e).__name__,e)
