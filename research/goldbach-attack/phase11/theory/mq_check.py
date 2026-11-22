import mpmath as mp, math, itertools
mp.mp.dps = 30

def primes_upto(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for p in range(2,int(n**0.5)+1):
        if s[p]:
            for m in range(p*p,n+1,p): s[m]=False
    return [i for i,v in enumerate(s) if v]

def Lval(s, chi, q):
    # L(s,chi) = q^{-s} sum_{a=1}^{q} chi(a) zeta(s, a/q)
    tot = mp.mpf(0)
    for a in range(1,q):
        ca = chi[a-1]
        if ca != 0:
            tot += ca*mp.zeta(s, mp.mpf(a)/q)
    return mp.power(q,-s)*tot

def chars_mod_q(q):
    # enumerate characters mod q: chi(a)=exp(2πi * (k * ind(a))/ord) ; need generator of (Z/q)*
    # brute force: units; find generator
    units=[a for a in range(1,q) if math.gcd(a,q)==1]
    # find generator by trial
    def powmod(a,e): return pow(a,e,q)
    gen=None
    for g in units:
        seen=set(); cur=1; ok=False
        for k in range(len(units)):
            if cur in seen: break
            seen.add(cur); cur=cur*g%q
            if len(seen)==len(units): ok=True
        if ok: gen=g; break
    if gen is None: return None
    phi=len(units)
    # discrete log
    dlog={1:0}; cur=1
    for k in range(1,phi):
        cur=cur*gen%q; dlog[cur]=k
    chars=[]
    for j in range(phi):
        chi=[0]*q
        for a in units:
            e=dlog[a]
            chi[a-1]=mp.e**(2j*mp.pi*j*e/phi)
        chars.append((j,chi))
    return chars, phi, gen

def parity(chi,q):
    return chi[q-2] if q>=2 else 1  # chi(-1) = chi(q-1); index a-1 = q-2

def Mq(q,a,b,s,t):
    # CFZ / GWX main term M_q = phi* Z_q(a,b;s,t) + H_q(a,b) Z_q(1-b,1-a;s,t)
    def zeta_q(w, q):
        v = mp.zeta(w)
        for p in primes_upto(q):
            if q%p==0: v *= (1-mp.power(p,-w))
        return v
    def Aq(a,b,s,t,q):
        # prod_{p nmid q} [(1-p^{-c-d})(1-p^{-a-d}-p^{-b-c}+p^{-c-d})] / [(1-p^{-a-d})(1-p^{-b-c})]
        # c=s,d=t
        val = mp.mpf(1)
        ps = primes_upto(4000)
        for p in ps:
            if q%p==0: continue
            x=mp.power(p,-a-t); y=mp.power(p,-b-s); z=mp.power(p,-s-t)
            num = (1-z)*(1-x-y+z); den=(1-x)*(1-y)
            val *= num/den
        return val
    def Zq(a,b,s,t,q):
        return zeta_q(a+b,q)*zeta_q(s+t,q)/(zeta_q(a+t,q)*zeta_q(b+s,q))*Aq(a,b,s,t,q)
    # primitive characters mod q: for q prime all nonprincipal are primitive
    phi_star = q-1   # q prime, excluding principal; both parities
    # M_e counts
    chars, phi, gen = chars_mod_q(q)
    Me={0:0,1:0}
    for j,chi in chars:
        if j==0: continue  # principal
        par = parity(chi,q)
        e = 0 if abs(par-1)<1e-9 else 1
        Me[e]+=1
    def X(w,e):
        return mp.power(q/mp.pi, mp.mpf(1)/2-w)*mp.gamma((1-w+e)/2)/mp.gamma((w+e)/2)
    Hq = sum(Me[e]*X(a,e)*X(b,e) for e in (0,1))
    return phi_star*Zq(a,b,s,t,q) + Hq*Zq(1-b,1-a,s,t,q), (phi_star, Me, Hq)

def Rq_exact(q,a,b,s,t):
    chars, phi, gen = chars_mod_q(q)
    tot=mp.mpf(0)
    for j,chi in chars:
        if j==0: continue
        La=Lval(a,chi,q); Lb=Lval(b,chi,q)  # careful: L(b,chi) with conj? we need L(b,\bar chi)
        # build conj char
        chic=[0]*q
        for idx in range(q):
            if chi[idx]!=0: chic[idx]=mp.conj(chi[idx])
        Lb=Lval(b,chic,q)
        Ls=Lval(s,chi,q); Lt=Lval(t,chic,q)
        tot += La*Lb/(Ls*Lt)
    return tot

q=97
for (a,b,s,t) in [
    (mp.mpf(1)/2+0.3j, mp.mpf(1)/2-0.3j, mp.mpf(1)/2+mp.mpf(1)/10+0.2j, mp.mpf(1)/2+mp.mpf(1)/10-0.2j),
    (mp.mpf(1)/2+0.1j, mp.mpf(1)/2+0.1j, mp.mpf(1)/2+mp.mpf(1)/10+0.1j, mp.mpf(1)/2+mp.mpf(1)/10+0.1j),
]:
    ex=Rq_exact(q,a,b,s,t)
    M,extra=Mq(q,a,b,s,t)
    print("shifts:",a,b,s,t)
    print("  R_exact =",mp.nstr(ex,12))
    print("  M_q     =",mp.nstr(M,12), " diff=",mp.nstr(ex-M,10), " |diff|/q^0.5=",mp.nstr(abs(ex-M)/mp.sqrt(q),8))
