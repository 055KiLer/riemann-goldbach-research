import mpmath as mp
mp.mp.dps = 30
from mpmath import mpc, mpf, exp, log
import math

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
    mu=[1]*(N+1)
    # sieve
    mu=[0]*(N+1); mu[0]=0
    if N>=1: mu[1]=1
    primes=[]
    iscomp=[False]*(N+1)
    for i in range(2,N+1):
        if not iscomp[i]: primes.append(i); mu[i]=-1
        for pr in primes:
            if i*pr>N: break
            iscomp[i*pr]=True
            if i%pr==0:
                mu[i*pr]=0; break
            else:
                mu[i*pr]=-mu[i]
    return mu

q = 101
X = 7
eta = mpf('0.1')
a = mpc(mpf('0.6'), mpf('0.3'))
b = mpc(mpf('0.55'), mpf('-0.2'))
c = mpc(mpf('0.6'), mpf('0.1'))
d = mpc(mpf('0.55'), mpf('0.25'))

g = primitive_root(q)
logt = {}
x=1
for e in range(q-1):
    logt[x]=e; x=(x*g)%q

def chi_vals(k):
    # returns dict a->chi_k(a) for a=1..q-1
    return {a: exp(2j*mp.pi*k*logt[a]/(q-1)) for a in range(1,q)}

def lval(s, chid):
    return q**(-s) * sum(chid[a]*mp.zeta(s, mpf(a)/q) for a in chid)

# R_q
R = mpc(0)
for k in range(1,q-1):
    chi = chi_vals(k)
    chib = {a: mp.conj(chi[a]) for a in chi}
    R += lval(a,chi)*lval(b,chib)/(lval(c,chi)*lval(d,chib))

# truncated series
mu = mobius_upto(X)
def P(s, chi, chib=False):
    # sum_{n<=X} chi(n) n^{-s}
    tot=mpc(0)
    for n in range(1,X+1):
        ch = (mp.conj(chi[n]) if chib else chi[n]) if n in chi else 0
        tot += ch*mp.power(n,-s)
    return tot
def Q(s, chi, chib=False):
    tot=mpc(0)
    for m in range(1,X+1):
        if mu[m]==0: continue
        ch = (mp.conj(chi[m]) if chib else chi[m]) if m in chi else 0
        tot += mu[m]*ch*mp.power(m,-s)
    return tot

E = mpc(0)
for k in range(1,q-1):
    chi = chi_vals(k)
    E += P(a,chi)*P(b,chi,True)*Q(c,chi)*Q(d,chi,True)

# coefficient arrays c_A, d_B for A,B <= X*X
M = X*X
cA = [mpc(0)]*(M+1); dB=[mpc(0)]*(M+1)
for n in range(1,X+1):
    for m in range(1,X+1):
        A=n*m
        if A<=M:
            cA[A]+= mp.power(n,-a)*mu[m]*mp.power(m,-c)
            dB[A]+= mp.power(n,-b)*mu[m]*mp.power(m,-d)
D = sum(cA[A]*dB[A] for A in range(1,M+1))
Sc = sum(cA[1:]); Sd=sum(dB[1:])
# W: A!=B, A=B mod q (none here since M<q), (AB,q)=1
W = sum(cA[A]*dB[B] for A in range(1,M+1) for B in range(1,M+1) if A!=B and (A-B)%q==0)
T = sum(cA[A]*dB[B] for A in range(1,M+1) for B in range(1,M+1) if (A*B)%q==0)

print("q,X =",q,X)
print("R_q      =",mp.nstr(R,12))
print("E        =",mp.nstr(E,12))
print("|R-E|    =",mp.nstr(abs(R-E),8))
print("(q-1)D-ScSd+T+ (q-1)W =", mp.nstr((q-1)*D - Sc*Sd + T + (q-1)*W,12))
print("D        =",mp.nstr(D,10),"  Sc =",mp.nstr(Sc,10),"  Sd=",mp.nstr(Sd,10))
print("Sc*Sd    =",mp.nstr(Sc*Sd,10))
print("W=",mp.nstr(W,10),"T=",mp.nstr(T,10))
print("q*D      =",mp.nstr(q*D,10))
