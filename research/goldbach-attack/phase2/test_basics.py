import numpy as np, mpmath as mp, time
mp.mp.dps = 30

# Bernoulli numbers B_2j
from fractions import Fraction
def bernoulli(n):
    # Akiyama-Tanigawa
    A = [Fraction(0)]*(n+1); A[0]=Fraction(1)
    for m in range(1,n+1):
        A[m] = Fraction(1, m+1)
        for j in range(m,0,-1):
            A[j-1] = j*(A[j-1]-A[j])
    return A[0]
Bs = [bernoulli(2*j) for j in range(1,25)]
print("B2..B48:", [float(b) for b in Bs[:4]], "...")

def hurwitz_em(u, x, K=64, J=24):
    u = complex(u)
    n = np.arange(K, dtype=np.float64)
    xa = n + x
    # direct
    lu = -u*np.log(xa)
    terms = np.exp(lu)
    B = terms.sum()
    dB = (-np.log(xa)*terms).sum()
    # EM tail
    y = K + x
    ly = np.log(y)
    # (K+x)^{1-u}
    t1 = np.exp((1-u)*ly)
    B += t1/(u-1)
    dB += -t1*ly/(u-1) - t1/(u-1)**2
    t2 = np.exp(-u*ly)
    B += 0.5*t2
    dB += -0.5*ly*t2
    # rising factorial and its derivative
    c = 1.0+0j   # (u)_{2j-1}
    for j in range(1, J+1):
        # update c from (u)_{2j-3} to (u)_{2j-1}: multiply (u+2j-2)
        c = c*(u+2*j-1) if j>1 else c
        # actually handle j=1 separately
        pass
    return B, dB

# Build properly
def hurwitz_em2(u, x, K=64, J=24, want_deriv=True):
    u = complex(u)
    n = np.arange(K, dtype=np.float64)
    xa = n + x
    lx = np.log(xa)
    terms = np.exp(-u*lx)
    B = terms.sum(); dB = -(lx*terms).sum()
    y = K + x; ly = np.log(y)
    t1 = np.exp((1-u)*ly)
    B += t1/(u-1)
    dB += -t1*ly/(u-1) - t1/(u-1)**2
    t2 = np.exp(-u*ly)
    B += 0.5*t2; dB += -0.5*ly*t2
    # rising factorial (u)_{2j-1} and derivative
    rise = 1.0+0j; drise = 0j
    # j=1: (u)_1 = u
    rise = u; drise = 1.0
    pw = np.exp(-u*ly)   # (K+x)^{-u}
    for j in range(1,J+1):
        if j>1:
            # (u)_{2j-1} = (u)_{2j-3} * (u+2j-3)*(u+2j-2)
            rise *= (u+2*j-3)*(u+2*j-2)
        b = float(Bs[j-1]) if abs(float(Bs[j-1]))<1e300 else 0.0
        coeff = b/np.math.factorial(2*j) if False else b/float(np.prod(np.arange(1,2*j+1,dtype=float)))
        # (K+x)^{-u-2j+1} = pw * y^{1-2j}
        term = coeff*rise*pw*(y**(1-2*j))
        B += term
        # derivative
        dterm = coeff*(drise*pw*(y**(1-2*j)) + rise*pw*(y**(1-2*j))*(-ly))
        # note d/ds of pw = -ln y pw ; and y^{1-2j} const
        dB += dterm
        # update drise for next j: d/ds (u)_{2j-1} = (u)_{2j-1} * sum_{m=0}^{2j-2} 1/(u+m)
        # we'll just set after: for j -> j+1 the derivative of rise_next:
        # next rise = rise*(u+2j-1)*(u+2j); next drise = drise*(u+2j-1)*(u+2j) + rise*((u+2j)+(u+2j-1))
        drise_next = drise*(u+2*j-1)*(u+2*j) + rise*((u+2*j-1)+(u+2*j))
        drise = drise_next
    return B, dB

# test
u = complex(0.5970, 80.0)
x = 1.0/30030
t0=time.time()
B,dB = hurwitz_em2(u,x)
print("EM:", B, dB, "time", time.time()-t0)
mp.mp.dps=30
zz = mp.zeta(mp.mpc(u), mp.mpf(x))
# derivative numerically high precision
h = mp.mpf('1e-20')
zzp = (mp.zeta(mp.mpc(u+h), mp.mpf(x)) - mp.zeta(mp.mpc(u-h), mp.mpf(x)))/(2*h)
print("mp:", zz, zzp, "err:", abs(complex(zz)-B), abs(complex(zzp)-dB))
# timing mpmath
t0=time.time()
for k in range(20):
    mp.zeta(mp.mpc(complex(0.6, k*3.0)), mp.mpf(1.0/30030))
print("mpmath zeta avg:", (time.time()-t0)/20)
t0=time.time()
for k in range(20):
    mp.zeta(mp.mpc(complex(1.2, k*3.0)), derivative=2)
print("mpmath zeta deriv2 Re>1 avg:", (time.time()-t0)/20)
t0=time.time()
a = np.random.rand(400000)
_ = np.sin(a); _=np.cos(a)
print("numpy sincos 400k:", time.time()-t0)
