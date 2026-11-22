"""Euler-Maclaurin Hurwitz zeta + derivative, vectorized; L'/L matrix construction."""
import numpy as np
from fractions import Fraction
import mpmath as mp

def bernoulli_numbers(nmax):
    """Bernoulli B_0..B_nmax via Akiyama-Tanigawa, returned as Fractions."""
    A = [Fraction(0)]*(nmax+1)
    B = []
    for m in range(nmax+1):
        A[m] = Fraction(1, m+1)
        for j in range(m, 0, -1):
            A[j-1] = j*(A[j-1]-A[j])
        B.append(A[0])
    return B

def rising_and_deriv(u, J):
    """Return ((u)_{2j-1}, d/du (u)_{2j-1}) for j=1..J."""
    rise = np.zeros(J, dtype=complex)
    drise = np.zeros(J, dtype=complex)
    r = complex(u); dr = 1.0+0j
    rise[0] = r; drise[0] = dr
    for j in range(2, J+1):
        # multiply by (u+2j-3)(u+2j-2)
        a = u+2*j-3; b = u+2*j-2
        rise[j-1] = rise[j-2]*a*b
        drise[j-1] = drise[j-2]*a*b + rise[j-2]*(a+b)
    return rise, drise

class HurwitzEM:
    def __init__(self, K=64, J=24):
        self.K=K; self.J=J
        B = bernoulli_numbers(2*J+1)
        self.coeff = np.array([float(B[2*j])/float(np.prod(np.arange(1,2*j+1,dtype=float))) for j in range(1,J+1)])
        self.coeff2 = self.coeff  # B_{2j}/(2j)!
    def zeta_and_deriv(self, u, x, K=None, J=None):
        """scalar u complex, x real in (0,1); returns zeta(u,x), d/du zeta(u,x)."""
        K = K or self.K; J = J or self.J
        n = np.arange(K, dtype=np.float64)
        xa = n + x
        lx = np.log(xa)
        terms = np.exp(-u*lx)
        S = terms.sum(); dS = -(lx*terms).sum()
        y = K + x; ly = np.log(y)
        tK = np.exp(-u*ly)
        rise, drise = rising_and_deriv(u, J)
        R = y/(u-1) + 0.5 + np.sum(self.coeff*rise*(y**(1-2*np.arange(1,J+1))))
        Rp = -y/(u-1)**2 + np.sum(self.coeff*drise*(y**(1-2*np.arange(1,J+1))))
        S += tK*R
        dS += tK*(-ly*R + Rp)
        return S, dS

    def zeta_array(self, u, xarr, K=None, J=None):
        """u complex scalar; xarr real array; returns zeta(u,x) array and derivative array."""
        K = K or self.K; J = J or self.J
        xa = np.arange(K, dtype=np.float64)[None,:] + xarr[:,None]   # (A,K)
        lx = np.log(xa)
        terms = np.exp(-u*lx)                  # (A,K)
        S = terms.sum(axis=1); dS = -(lx*terms).sum(axis=1)
        y = K + xarr
        ly = np.log(y)
        tK = np.exp(-u*ly)
        rise, drise = rising_and_deriv(u, J)
        powj = y[:,None]**(1-2*np.arange(1,J+1))[None,:]  # (A,J)
        R = y/(u-1) + 0.5 + powj @ (self.coeff*rise)
        Rp = -y/(u-1)**2 + powj @ (self.coeff*drise)
        S = S + tK*R
        dS = dS + tK*(-ly*R + Rp)
        return S, dS

def L_over_L_array(u, units, N, logN, em):
    """Compute L'/L(u,chi) for all chars mod N given unit list a (phi of them).
    L(u,chi) = N^{-u} sum_a chi(a) zeta(u,a/N)
    L'/L = sum_a chi(a) zeta'(u,a/N) / sum_a chi(a) zeta(u,a/N) - log N."""
    x = units.astype(np.float64)/N
    S, dS = em.zeta_array(u, x)
    return S, dS

if __name__ == "__main__":
    N=30030
    em = HurwitzEM()
    # accuracy test vs mpmath at extremes
    mp.mp.dps = 30
    tests = [(complex(0.5+0.09699366, 80.0), 1.0/N),
             (complex(0.5+0.125, -80.0), 1.0/N),
             (complex(0.5+0.09699366, 80.0), (N-1)/N),
             (complex(0.5+0.125, 0.0), 0.5),
             (complex(0.5+0.125, 37.3), 1/3)]
    for u,x in tests:
        S,dS = em.zeta_and_deriv(u,x)
        zz = mp.zeta(mp.mpc(u), mp.mpf(x))
        # derivative via mpmath.diff
        f = lambda z: mp.zeta(mp.mpc(z), mp.mpf(x))
        zzp = mp.diff(f, mp.mpc(u), 1)
        print(f"u={u} x={x:.6g}  zeta err {abs(complex(zz)-S):.2e} (|z|={abs(complex(zz)):.3g})  d err {abs(complex(zzp)-dS):.2e} (|dz|={abs(complex(zzp)):.3g})")
    # derivative accuracy with different K,J
    for K,J in [(64,24),(128,24),(64,30)]:
        em2 = HurwitzEM(K,J)
        u=complex(0.5+0.09699366, 80.0); x=1.0/N
        S,dS = em2.zeta_and_deriv(u,x)
        mp.mp.dps=40
        f = lambda z: mp.zeta(mp.mpc(z), mp.mpf(x))
        zzp = mp.diff(f, mp.mpc(u), 1)
        print("K,J",K,J,"d err", abs(complex(zzp)-dS))
