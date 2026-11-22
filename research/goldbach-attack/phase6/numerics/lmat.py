"""Build G[i,chi] = L'/L(1/2+s_i, chi) for nodes on two boundary lines of Hardy strip."""
import numpy as np, time
from math import log as mlog
from chars import CharacterGroup
from hurwitz import HurwitzEM, rising_and_deriv

class Config:
    def __init__(self, N, H, m=16, K=64, J=24):
        self.N=N; self.H=H; self.m=m
        self.alpha=1.0/mlog(N); self.beta=0.125
        self.sigma_lines=np.array([0.5+self.alpha, 0.5+self.beta])  # u=1/2+s real parts
        self.K=K; self.J=J
        self.Kmax=int(round(H*m))
        self.tt=np.arange(-self.Kmax, self.Kmax+1)/m
        self.h=1.0/m

def build_chars(N):
    return CharacterGroup(N)

def odd_char_index(cg):
    idx_odd = np.where(cg.kmodd)[0]
    # inverse character permutation within odd set
    pos = -np.ones(cg.phi, dtype=np.int64)
    pos[idx_odd] = np.arange(len(idx_odd))
    inv = np.zeros(len(idx_odd), dtype=np.int64)
    for p,kflat in enumerate(idx_odd):
        k = [cg.kvecs[i][kflat] for i in range(len(cg.orders))]
        kinv = [(-kk) % o for kk,o in zip(k, cg.orders)]
        kfi = sum(kk*st for kk,st in zip(kinv, cg.strides))
        inv[p] = pos[kfi]
    return idx_odd, inv

def build_G(cfg, cg, verbose=True, chunk_gb=2.0):
    """Return G (n_nodes x n_odd) complex and node metadata.
    Node ordering: line 0 (alpha) k=-Kmax..Kmax then line 1 (beta) same."""
    N=cfg.N; m=cfg.m; K=cfg.K; J=cfg.J; Kmax=cfg.Kmax
    em = HurwitzEM(K,J)
    units = cg.units.astype(np.float64)
    A = len(units); logN = mlog(N); phi=cg.phi
    x = units/N
    n = np.arange(K, dtype=np.float64)
    L1 = np.log(n[None,:] + x[:,None])          # (A,K)
    y = K + x
    ly = np.log(y)
    powj = y[:,None]**(1-2*np.arange(1,J+1))[None,:]   # (A,J)
    coeff = em.coeff
    idx_odd, inv = odd_char_index(cg)
    nodd=len(idx_odd)
    nlines=2
    n_nodes = nlines*(2*Kmax+1)
    G = np.zeros((n_nodes, nodd), dtype=np.complex128)
    lines = cfg.sigma_lines
    Efac = [np.exp(-s*L1) for s in lines]        # list of (A,K) real
    eK = [np.exp(-s*ly) for s in lines]          # list of (A,) real
    # phases q for recurrence: z_k = exp(-i (k/m) L1)
    q = np.exp(-1j*L1/m)
    qK = np.exp(-1j*ly/m)
    z = np.ones((A,K), dtype=np.complex128)
    tKk = np.ones(A, dtype=np.complex128)
    t0=time.time()
    for k in range(Kmax+1):
        t = k/m
        for li in range(nlines):
            u = lines[li] + 1j*t
            rise, drise = rising_and_deriv(u, J)
            cR = coeff*rise; cRp = coeff*drise
            R = y/(u-1) + 0.5 + powj @ cR
            Rp = -y/(u-1)**2 + powj @ cRp
            P = z*Efac[li]
            B = P.sum(axis=1)
            dA = -(L1*P).sum(axis=1)
            tK = tKk*eK[li]
            B += tK*R
            dA += tK*(-ly*R + Rp)
            Bhat = cg.forward(B)
            dAhat = cg.forward(dA)
            g = dAhat/Bhat - logN
            row = g[idx_odd]
            # +t node
            iplus = li*(2*Kmax+1) + (Kmax+k)
            G[iplus] = row
            if k>0:
                iminus = li*(2*Kmax+1) + (Kmax-k)
                G[iminus] = np.conj(row[inv])
        z *= q; tKk *= qK
        if verbose and (k%100==0):
            print(f"  k={k}/{Kmax} time {time.time()-t0:.1f}s", flush=True)
        if verbose:
            pass
    if verbose:
        print("build_G time", time.time()-t0)
    return G, idx_odd, inv

def node_meta(cfg):
    """Returns s-real-parts (alpha,beta), imaginary parts, trapezoid weights for the 2 lines."""
    m=cfg.m; Kmax=cfg.Kmax
    tks = np.arange(-Kmax,Kmax+1)/m
    s_lines=np.array([cfg.alpha, cfg.beta])   # NOT u=1/2+s
    sig = np.concatenate([np.full(len(tks), s_lines[0]), np.full(len(tks), s_lines[1])])
    tt = np.concatenate([tks,tks])
    wts = np.concatenate([np.where(np.abs(tks)<cfg.H-1e-12, cfg.h, cfg.h/2)]*2)
    return sig, tt, wts

if __name__=="__main__":
    import sys
    H=float(sys.argv[1]) if len(sys.argv)>1 else 4.0
    N=int(sys.argv[2]) if len(sys.argv)>2 else 30030
    cfg=Config(N,H); cg=build_chars(N)
    t0=time.time(); G,idx_odd,inv=build_G(cfg,cg); print("total",time.time()-t0,"G shape",G.shape)
    sig,tt,wts=node_meta(cfg)
    print("nodes",len(sig),len(tt),len(wts))
