import mpmath as mp
from math import gcd
mp.mp.dps=35
print("check (3.4) and (3.11)", flush=True)
def X(q,e,s):
    return (mp.mpf(q)/mp.pi)**(mp.mpf(1)/2-s)*mp.gamma((mp.mpf(1)-s+e)/2)/mp.gamma((s+e)/2)
q=7
for (a,b) in [(mp.mpc('0.5','0.3'),mp.mpc('0.5','-0.2')),(mp.mpc('0.5','1.7'),mp.mpc('0.5','-2.3'))]:
    h0=X(q,0,1-b)*X(q,0,1-a); h1=X(q,1,1-b)*X(q,1,1-a); z=a+b-1
    rhs=-4*q**z*(2*mp.pi)**(-z-1)*mp.gamma(a)*mp.gamma(b)*mp.sin(mp.pi*z/2)
    print("(3.4) maxerr", abs(h0-h1-rhs), flush=True)
for (s,t) in [(mp.mpc('0.6','0.2'),mp.mpc('0.55','-0.3')),(mp.mpc('0.5','1.1'),mp.mpc('0.5','-0.7'))]:
    z=s+t-1; Xi=2*(2*mp.pi)**(-z)*mp.gamma(z)*mp.cos(mp.pi*z/2)
    lhs=(X(q,0,s)*X(q,0,t)-X(q,1,s)*X(q,1,t))/2*Xi
    rhs=q**(-z)*mp.gamma(1-s)*mp.gamma(1-t)/mp.gamma(1-z)
    print("(3.11) maxerr", abs(lhs-rhs), flush=True)

# (2.12) identity check with primes up to P
P=30000
sv=bytearray([1])*(P+1); sv[0]=sv[1]=0
for i in range(2,int(P**0.5)+1):
    if sv[i]: sv[i*i::i]=bytearray(len(sv[i*i::i]))
primes=[p for p in range(2,P+1) if sv[p]]
def sig(p,h):
    return mp.mpf(p)/(p-1) if h%p==0 else mp.mpf(p*(p-2))/mp.mpf((p-1)**2)
def Sfun(h):
    out=mp.mpf(1)
    for p in primes: out*=sig(p,h)
    return out
def mobius(n):
    if n==1: return 1
    fac=0;m=n;d=2
    while d*d<=m:
        if m%d==0:
            m//=d
            if m%d==0: return 0
            fac+=1
        d+=1
    return (-1)**(fac+(1 if m>1 else 0))
def divs(n):
    ds=[];d=1
    while d*d<=n:
        if n%d==0:
            ds.append(d)
            if d!=n//d: ds.append(n//d)
        d+=1
    return sorted(ds)
def phi(n):
    r=n;m=n;d=2
    while d*d<=m:
        if m%d==0:
            r=r//d*(d-1)
            while m%d==0: m//=d
        d+=1
    if m>1: r=r//m*(m-1)
    return r
def phistar(q):
    return 1 if q==1 else sum(mobius(q//d)*phi(d) for d in divs(q))
def cq(q,h):
    return sum(d*mobius(q//d) for d in divs(gcd(q,h)))
def Kq(q,h):
    # S_q(h)=prod_{p not| q} sig_p(h)
    out=mp.mpf(1)
    for p in primes:
        if q%p!=0: out*=sig(p,h)
    return mp.mpf(q)/(phi(q)**2)*cq(q,h)*out
for N in [6,12,30]:
    errs=[]
    for h in range(1,2*N+1):
        lhs=sum(phistar(q)*Kq(q,h) for q in divs(N))
        rhs=phi(N)*Sfun(h) if h%N==0 else mp.mpf(0)
        errs.append(abs(lhs-rhs)/max(1,abs(rhs)))
    print("(2.12) N=",N,"max rel err=",max(errs),flush=True)
# S(N) formula check for large N (primes up to 30000 may miss tail; use tail approx via C2)
C2=mp.mpf(1)
for p in primes:
    if p>2: C2*=1-1/mp.mpf(p-1)**2
def S_N(N):
    out=mp.mpf(2)*C2;m=N
    for p in primes:
        if N%p==0 and p>2: out*=mp.mpf(p-1)/(p-2)
    return out
for N in [30030,40022,60022]:
    print("S(1.1) vs 2C2prod N=",N, Sfun(N), S_N(N),flush=True)
