import mpmath as mp
mp.mp.dps = 25
from mpmath import mpc, mpf, exp
import numpy as np

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
    raise RuntimeError

def mobius_upto(N):
    mu=np.zeros(N+1,dtype=np.int64); mu[0]=0
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
X = 31  # X^2 = 961 < q
eta = mpf('0.2')   # sigma = 0.7
sigma = 1 - 1/mpf(2)  # placeholder
sigma = mpf('0.5')+eta
a = mpc(sigma, mpf('0.3'))
b = mpc(sigma, mpf('-0.2'))
c = mpc(sigma, mpf('0.1'))
d = mpc(sigma, mpf('0.25'))

g = primitive_root(q)
e = np.zeros(q, dtype=np.int64)  # discrete log e[a] for a in 1..q-1
x=1
for i in range(q-1):
    e[x]=i; x=(x*g)%q

# Hurwitz zeta values via mpmath (q-1 values per s)
print("computing hurwitz zeta...")
Z = {}
for name,s in [('a',a),('b',b),('c',c),('d',d)]:
    arr = np.zeros(q-1, dtype=np.complex128)
    for k in range(1,q):
        arr[e[k]] = complex(mp.zeta(s, mpf(k)/q))
    Z[name]=arr

# FFT along multiplicative group: L(s,chi_j) = q^{-s} sum_k chi_j(k) zeta(s,k/q)
# chi_j(k)=exp(2pi i j e[k]/(q-1)); so L_j = q^{-s} * sum over e-index
def Lvals(arr, s):
    return np.array([q**(-s) * np.sum(arr*np.exp(2j*np.pi*j*np.arange(q-1)/(q-1))) for j in range(q-1)])
# note: sum over k of chi_j(k) zeta_k = sum_{idx} exp(2pi i j idx/(q-1)) zeta_{g^idx}
La = Lvals(Z['a'], a); Lb = Lvals(Z['b'], b); Lc = Lvals(Z['c'], c); Ld = Lvals(Z['d'], d)
# chi_bar = chi_{q-1-j}: L(b,chi_bar)_j = L_b[(q-1-j) mod (q-1)]
Lbb = np.array([Lb[(q-1-j)%(q-1)] for j in range(q-1)])  # careful: map j->(q-1-j)
Ldd = np.array([Ld[(q-1-j)%(q-1)] for j in range(q-1)])
R = np.sum(La*Lbb/(Lc*Ldd))
print("R_q =", R)
print("|R| =", abs(R), " R/q =", R/q)

# truncated series P, Q via same FFT with small vectors (fill values by n)
mu = mobius_upto(X)
def series_vals(s, coeffs):
    # coeffs: dict n->coefficient (for n<=X); returns array over chars j: sum_n coeff[n]*chi_j(n)
    arr = np.zeros(q-1, dtype=np.complex128)
    for n,cn in coeffs.items():
        arr[e[n%q]] += cn
    return np.array([np.sum(arr*np.exp(2j*np.pi*j*np.arange(q-1)/(q-1))) for j in range(q-1)])

Pa = series_vals(a, {n: mp.power(n,-a) for n in range(1,X+1)})
Pb = series_vals(b, {n: mp.power(n,-b) for n in range(1,X+1)})
Qc = series_vals(c, {n: mu[n]*mp.power(n,-c) for n in range(1,X+1) if mu[n]!=0})
Qd = series_vals(d, {n: mu[n]*mp.power(n,-d) for n in range(1,X+1) if mu[n]!=0})
Pbb = np.array([Pb[(q-1-j)%(q-1)] for j in range(q-1)])
Qdd = np.array([Qd[(q-1-j)%(q-1)] for j in range(q-1)])
E = np.sum(Pa*Pbb*Qc*Qdd)
print("E =", E, " |R-E| =", abs(R-E))
# coefficient arrays c_A,d_B, A<=X^2
M = X*X
cA = np.zeros(M+1, dtype=np.complex128); dB=np.zeros(M+1,dtype=np.complex128)
for n in range(1,X+1):
    for m in range(1,X+1):
        A=n*m
        cA[A]+= complex(mp.power(n,-a)*mu[m]*mp.power(m,-c))
        dB[A]+= complex(mp.power(n,-b)*mu[m]*mp.power(m,-d))
D = np.sum(cA[1:]*dB[1:]); Sc=np.sum(cA[1:]); Sd=np.sum(dB[1:])
print("D =",D," Sc=",Sc," Sd=",Sd, " Sc*Sd=",Sc*Sd)
print("(q-1)D - ScSd =", (q-1)*D - Sc*Sd, " vs E")
