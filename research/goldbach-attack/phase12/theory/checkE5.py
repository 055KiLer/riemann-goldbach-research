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
R = mpc('1196.951294041234','-210.16336126043714')  # from checkE3, same shifts
print(f"q={q} eta={eta} R={R}")
print(f"{'X':>5} {'A':>5} {'|D|':>9} {'|ScSd|':>9} {'|qW|':>9} {'|Delta|':>9} {'|R-E|':>9} {'q^(1-etaA)':>10} {'|E-M|?':>8}")

for X in [31,60,100,200,400,700,1000,1500,2000]:
    M=X*X
    mu = mobius_upto(X)
    cA=np.zeros(M+1,dtype=np.complex128); dB=np.zeros(M+1,dtype=np.complex128)
    mvals=np.arange(1,X+1)
    mupow_c = mu[1:X+1]*np.power(mvals.astype(float),-float(c.real))  # need complex power
    # do complex powers properly
    mc = mupow_c.astype(np.complex128)
    for n in range(1,X+1):
        na=complex(mp.power(n,-a)); nb=complex(mp.power(n,-b))
        # m^{-c} and m^{-d}
        vals_c = np.array([complex(mp.power(m,-c)) for m in mvals]) if n==1 else cached_c
        vals_d = np.array([complex(mp.power(m,-d)) for m in mvals]) if n==1 else cached_d
        if n==1:
            cached_c=vals_c; cached_d=vals_d
        pos = n*mvals
        cA[pos] += na*mu[1:X+1]*vals_c
        dB[pos] += nb*mu[1:X+1]*vals_d
    D=np.sum(cA[1:]*dB[1:]); Sc=np.sum(cA[1:]); Sd=np.sum(dB[1:]); ScSd=Sc*Sd
    C=np.zeros(q,dtype=np.complex128); Dd=np.zeros(q,dtype=np.complex128)
    for r in range(q):
        C[r]=np.sum(cA[r::q]) if r>0 else np.sum(cA[0::q])
        Dd[r]=np.sum(dB[r::q]) if r>0 else np.sum(dB[0::q])
    # fix: cA[r::q] sums A=r, r+q, ... correct indexing since A is index
    K=np.sum(C*Dd)
    W=K - C[0]*Dd[0] - D
    T=C[0]*Sd + Sc*Dd[0] - C[0]*Dd[0]
    E=(q-1)*(D+W)-ScSd+T
    Delta=(q-1)*W-ScSd+T
    A=mp.log(X)/mp.log(q)
    target=float(q**(1-eta*A))
    print(f"{X:5d} {float(A):5.2f} {abs(D):9.3f} {abs(ScSd):9.3e} {abs((q-1)*W):9.3e} {abs(Delta):9.3e} {abs(R-E):9.3e} {target:10.2f}")
