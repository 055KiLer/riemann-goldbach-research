import mpmath as mp, numpy as np
mp.mp.dps = 25
from mpmath import mpc, mpf

def primitive_root(p):
    def factor(n):
        fs=set(); d=2
        while d*d<=n:
            while n%d==0: fs.add(d); n//=d
            d+=1
        if n>1: fs.add(n)
        return fs
    fs=factor(p-1)
    for g in range(2,p):
        if all(pow(g,(p-1)//f,p)!=1 for f in fs): return g

def mobius_upto(N):
    mu=np.zeros(N+1,dtype=np.int64)
    if N>=1: mu[1]=1
    primes=[]; iscomp=np.zeros(N+1,dtype=bool)
    for i in range(2,N+1):
        if not iscomp[i]: primes.append(i); mu[i]=-1
        for pr in primes:
            if i*pr>N: break
            iscomp[i*pr]=True
            if i%pr==0: mu[i*pr]=0; break
            mu[i*pr]=-mu[i]
    return mu

q = 1009
eta = mpf('0.2')
sigma = mpf('0.5')+eta
a = mpc(sigma, mpf('0.3')); b = mpc(sigma, mpf('-0.2'))
c = mpc(sigma, mpf('0.1')); d = mpc(sigma, mpf('0.25'))

# Build c_A,d_B arrays for A<=X^2 for several X, but compute residue sums efficiently:
# For each n<=X, m<=X: A=nm; add to cA[A]. We'll build once for max X and then accumulate residues.
Xmax = 100
mu = mobius_upto(Xmax)
Mmax = Xmax*Xmax
cA=np.zeros(Mmax+1,dtype=np.complex128); dB=np.zeros(Mmax+1,dtype=np.complex128)
for n in range(1,Xmax+1):
    na=complex(mp.power(n,-a)); nb=complex(mp.power(n,-b))
    for m in range(1,Xmax+1):
        A=n*m
        cA[A]+= na*mu[m]*complex(mp.power(m,-c))
        dB[A]+= nb*mu[m]*complex(mp.power(m,-d))

print("q=",q,"eta=",eta)
print("X   | E-(q-1)D |   S_cS_d   |  (q-1)W  |  T  |  K=q(D+W)-ScSd | q^{1-eta*A} ")
D_all = None
for X in [10,20,31,40,60,80,100]:
    M=X*X
    cAx=cA[:M+1].copy(); dBx=dB[:M+1].copy()
    # But truncation: for a given X, indices n,m<=X. Our arrays above included n,m up to Xmax.
    # Need arrays restricted to n,m<=X: rebuild quickly for each X (cheap)
    cX=np.zeros(M+1,dtype=np.complex128); dX=np.zeros(M+1,dtype=np.complex128)
    for n in range(1,X+1):
        na=complex(mp.power(n,-a)); nb=complex(mp.power(n,-b))
        for m in range(1,X+1):
            A=n*m
            cX[A]+= na*mu[m]*complex(mp.power(m,-c))
            dX[A]+= nb*mu[m]*complex(mp.power(m,-d))
    D=np.sum(cX[1:]*dX[1:]); Sc=np.sum(cX[1:]); Sd=np.sum(dX[1:]); ScSd=Sc*Sd
    # residue sums
    C=np.zeros(q,dtype=np.complex128); Dd=np.zeros(q,dtype=np.complex128)
    for A in range(1,M+1):
        C[A%q]+=cX[A]; Dd[A%q]+=dX[A]
    K = np.sum(C[1:]*Dd[1:]) + C[0]*Dd[0]  # full congruence sum (no (AB,q) condition)
    # (q-1)W with W = sum_{A!=B, A=B mod q}: W = sum_r C_r D_r - D  (ignoring q|AB subtleties)
    W = np.sum(C*Dd) - D
    approxE = (q-1)*(D+W) - ScSd
    print(f"{X:4d} | {abs(approxE-(q-1)*D):10.3e} | {abs(ScSd):10.3e} | {abs((q-1)*W):10.3e} | K={abs(K):10.3e} | q^{1-eta*A:.1f}={float(q**(1-eta*mp.log(X)/mp.log(q))):10.2f}")
