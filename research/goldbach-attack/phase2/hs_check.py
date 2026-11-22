import numpy as np, math
# primes sieve up to 2e6
M=2_000_000
sieve=np.ones(M+1,bool); sieve[:2]=False
for i in range(2,int(M**0.5)+1):
    if sieve[i]: sieve[i*i::i]=False
primes=np.nonzero(sieve)[0]
logs=np.log(primes)

def D_N(w, N):
    # sum over primes p not dividing N of (log p)^2/(p^{1+w}-1)
    mask=(N % primes)!=0
    return np.sum(logs[mask]**2/(np.exp((1+w)*logs[mask])-1))

def DN_HS2(N, V=30, nv=200001):
    a=1.0/math.log(N); b=0.125
    v=np.linspace(-V,V,nv); W=2*np.pi/(4+v*v)
    # For each pair sigma1,sigma2 in {a,b}
    tot=0.0
    for s1,s2,mult in [(a,a,1.0),(a,b,2.0),(b,b,1.0)]:
        vals=np.array([D_N(complex(s1+s2, x),N) for x in v])
        integ=np.trapezoid(W*np.abs(vals)**2, v)
        tot+=mult*integ
    return tot

for N in [30030, 10**5, 10**6, 10**7, 10**8]:
    hs2=DN_HS2(N)
    print(f"N={N:>10d}  alpha={1/math.log(N):.6f}  ||D_N||_HS^2={hs2:.4e}   ||D_N||_HS={math.sqrt(hs2):.4e}  (logN)^1.5={math.log(N)**1.5:.4e}  ratio={math.sqrt(hs2)/math.log(N)**1.5:.4f}")
