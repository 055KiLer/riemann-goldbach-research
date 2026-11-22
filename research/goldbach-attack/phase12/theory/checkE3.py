import mpmath as mp
mp.mp.dps = 25
from mpmath import mpc, mpf
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

def run(q, X, eta):
    sigma = mpf('0.5')+eta
    a = mpc(sigma, mpf('0.3')); b = mpc(sigma, mpf('-0.2'))
    c = mpc(sigma, mpf('0.1')); d = mpc(sigma, mpf('0.25'))
    g = primitive_root(q)
    e = np.zeros(q, dtype=np.int64)
    x=1
    for i in range(q-1): e[x]=i; x=(x*g)%q
    Z = {}
    for name,s in [('a',a),('b',b),('c',c),('d',d)]:
        arr = np.zeros(q-1, dtype=np.complex128)
        for k in range(1,q):
            arr[e[k]] = complex(mp.zeta(s, mpf(k)/q))
        Z[name]=arr
    def Lvals(arr, s):
        # X_j = sum_{idx} arr[idx] * exp(2pi i j idx/(q-1)), j=0..q-2
        out=np.zeros(q-1,dtype=np.complex128)
        for j in range(q-1):
            out[j] = np.sum(arr*np.exp(2j*np.pi*j*np.arange(q-1)/(q-1)))
        return (q**(-s))*out
    La=Lvals(Z['a'],a); Lb=Lvals(Z['b'],b); Lc=Lvals(Z['c'],c); Ld=Lvals(Z['d'],d)
    def conj_arr(v): # v[j] -> v[(q-1-j)%(q-1)] ; note for j=0 ->0
        return np.array([v[(-j)%(q-1)] for j in range(q-1)])
    Lbb=conj_arr(Lb); Ldd=conj_arr(Ld)
    idx = np.arange(1,q-1)  # j=1..q-2 : nonprincipal
    R = np.sum(La[idx]*Lbb[idx]/(Lc[idx]*Ldd[idx]))
    mu = mobius_upto(X)
    def series(s, coeffs):
        arr = np.zeros(q-1, dtype=np.complex128)
        for n,cn in coeffs.items():
            arr[e[n%q]] += cn
        out=np.zeros(q-1,dtype=np.complex128)
        for j in range(q-1):
            out[j]=np.sum(arr*np.exp(2j*np.pi*j*np.arange(q-1)/(q-1)))
        return out
    Pa=series(a,{n: mp.power(n,-a) for n in range(1,X+1)})
    Pb=series(b,{n: mp.power(n,-b) for n in range(1,X+1)})
    Qc=series(c,{n: mu[n]*mp.power(n,-c) for n in range(1,X+1) if mu[n]!=0})
    Qd=series(d,{n: mu[n]*mp.power(n,-d) for n in range(1,X+1) if mu[n]!=0})
    Pbb=conj_arr(Pb); Qdd=conj_arr(Qd)
    E = np.sum(Pa[idx]*Pbb[idx]*Qc[idx]*Qdd[idx])
    # coefficients and D, Sc, Sd, W, T
    M=X*X
    cA=np.zeros(M+1,dtype=np.complex128); dB=np.zeros(M+1,dtype=np.complex128)
    for n in range(1,X+1):
        for m in range(1,X+1):
            A=n*m
            cA[A]+= complex(mp.power(n,-a)*mu[m]*mp.power(m,-c))
            dB[A]+= complex(mp.power(n,-b)*mu[m]*mp.power(m,-d))
    D=np.sum(cA[1:]*dB[1:]); Sc=np.sum(cA[1:]); Sd=np.sum(dB[1:])
    idxA=np.arange(1,M+1)
    W=0; T=0
    # wrap: A!=B, A=B mod q, (AB,q)=1
    for A in idxA:
        for B in idxA:
            if A==B: continue
            if (A-B)%q==0:
                W+=cA[A]*dB[B]
            if (A*B)%q==0:
                T+=cA[A]*dB[B]
    formula=(q-1)*(D+W)-Sc*Sd+T
    print(f"q={q} X={X} eta={eta}")
    print(f"  R = {mp.nstr(complex(R),10)}  |R|={mp.nstr(abs(R),8)}")
    print(f"  E = {mp.nstr(complex(E),10)}  |R-E|={mp.nstr(abs(R-E),8)}")
    print(f"  formula (q-1)(D+W)-ScSd+T = {mp.nstr(complex(formula),10)}  |E-formula|={mp.nstr(abs(E-formula),8)}")
    print(f"  D={mp.nstr(complex(D),8)} Sc={mp.nstr(complex(Sc),8)} Sd={mp.nstr(complex(Sd),8)} ScSd={mp.nstr(complex(Sc*Sd),8)}")
    print(f"  W={mp.nstr(complex(W),8)} T={mp.nstr(complex(T),8)}")
    return abs(R-E)

for X in [5,11,21,31]:
    run(1009, X, mpf('0.2'))
