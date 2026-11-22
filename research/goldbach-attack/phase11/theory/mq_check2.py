import mpmath as mp, math
mp.mp.dps=25
def primes_upto(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for p in range(2,int(n**0.5)+1):
        if s[p]:
            for m in range(p*p,n+1,p): s[m]=False
    return [i for i,v in enumerate(s) if v]
P=primes_upto(30000)
def gen_chars(q):
    units=[a for a in range(1,q) if math.gcd(a,q)==1]
    gen=None
    for g in units:
        seen=set(); cur=1
        for k in range(len(units)):
            if cur in seen: break
            seen.add(cur); cur=cur*g%q
        if len(seen)==len(units): gen=g; break
    phi=len(units); dlog={1:0}; cur=1
    for k in range(1,phi): cur=cur*gen%q; dlog[cur]=k
    chars=[]
    for j in range(phi):
        chi=[0]*q
        for a in units: chi[a-1]=mp.e**(2j*mp.pi*j*dlog[a]/phi)
        chars.append(chi)
    return chars
def Lval(s,chi,q):
    return mp.power(q,-s)*mp.fsum([chi[a-1]*mp.zeta(s,mp.mpf(a)/q) for a in range(1,q) if chi[a-1]!=0])
def isprincipal(chi):
    return all(abs(chi[i]-1)<1e-9 for i in range(len(chi)) if chi[i]!=0)
def Mq(q,a,b,s,t):
    def zq(w):
        v=mp.zeta(w)
        for p in P:
            if p>q: break
            if q%p==0: v*=(1-mp.power(p,-w))
        return v
    def Aq(a,b,s,t):
        val=mp.mpf(1)
        for p in P:
            if q%p==0: continue
            x=mp.power(p,-a-t); y=mp.power(p,-b-s); z=mp.power(p,-s-t)
            val*=(1-z)*(1-x-y+z)/((1-x)*(1-y))
        return val
    def Zq(a,b,s,t): return zq(a+b)*zq(s+t)/(zq(a+t)*zq(b+s))*Aq(a,b,s,t)
    chars=gen_chars(q); phi_star=0; Me=[0,0]
    for chi in chars:
        if isprincipal(chi): continue
        phi_star+=1; Me[0 if chi[q-2].real>0 else 1]+=1
    def X(w,e): return mp.power(q/mp.pi,mp.mpf(1)/2-w)*mp.gamma((1-w+e)/2)/mp.gamma((w+e)/2)
    Hq=sum(Me[e]*X(a,e)*X(b,e) for e in (0,1))
    return phi_star*Zq(a,b,s,t)+Hq*Zq(1-b,1-a,s,t), phi_star,Me
def Rq(q,a,b,s,t):
    chars=gen_chars(q); tot=mp.mpf(0)
    for chi in chars:
        if isprincipal(chi): continue
        chic=[0]*q
        for i in range(q):
            if chi[i]!=0: chic[i]=mp.conj(chi[i])
        tot+=Lval(a,chi,q)*Lval(b,chic,q)/(Lval(s,chi,q)*Lval(t,chic,q))
    return tot
I=1j
print("=== generic shifts, several primes ===")
for q in [97,101,103]:
    tests=[(mp.mpf(1)/2+0.3*I,mp.mpf(1)/2+0.4*I,mp.mpf(6)/10+0.2*I,mp.mpf(6)/10+0.5*I)]
    for a,b,s,t in tests:
        ex=Rq(q,a,b,s,t); M,ph,Me=Mq(q,a,b,s,t)
        print(f"q={q} phi*={ph} Me={Me}: R={mp.nstr(ex,9)} M={mp.nstr(M,9)} |diff|/q^.5={mp.nstr(abs(ex-M)/mp.sqrt(q),5)}")
print("=== generic shifts ===") if False else None
for q in [97,101]:
    a=mp.mpf(1)/2+0.3*I; b=mp.mpf(1)/2+0.4*I
    ex=Rq(q,a,b,a,b)   # ratio=1 identically
    M,ph,Me=Mq(q,a,b,a,b)
    print(f"q={q}: R_exact={mp.nstr(ex,10)} M_q(a,b;a,b)={mp.nstr(M,10)} phi*={ph}")
