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
    for g in units:
        seen=set(); cur=1
        for k in range(len(units)):
            if cur in seen: break
            seen.add(cur); cur=cur*g%q
        if len(seen)==len(units): gen=g; break
    phi=len(units); dlog={1:0}; cur=1
    for k in range(1,phi): cur=cur*gen%q; dlog[cur]=k
    out=[]
    for j in range(phi):
        chi=[0]*q
        for a in units: chi[a-1]=mp.e**(2j*mp.pi*j*dlog[a]/phi)
        out.append(chi)
    return out
def Lval(s,chi,q): return mp.power(q,-s)*mp.fsum([chi[a-1]*mp.zeta(s,mp.mpf(a)/q) for a in range(1,q) if chi[a-1]!=0])
def isprin(chi): return all(abs(chi[i]-1)<1e-9 for i in range(len(chi)) if chi[i]!=0)
def R11(q,a,s):
    tot=mp.mpf(0)
    for chi in gen_chars(q):
        if isprin(chi): continue
        tot+=Lval(a,chi,q)/Lval(s,chi,q)
    return tot
def M11(q,a,s):
    # CFZ 1/1 guess: phi* Z(a;s) + H(a) Z(1-a? ...); try derive: likely phi*ζ_q(1+a−s)A + Σ_χ ε X... 
    def zq(w):
        v=mp.zeta(w)
        for p in P:
            if p>q: break
            if q%p==0: v*=(1-mp.power(p,-w))
        return v
    def A(a,s):
        val=mp.mpf(1)
        for p in P:
            if q%p==0: continue
            x=mp.power(p,-a); y=mp.power(p,-s)
            # 1/1 local factor guess: (1-p^{-1})? standard ratio local: (1-p^{-1})*(1-p^{-?})...
            val*= (1-mp.power(p,-1))/((1-x)*(1-y)) * (1-x*y)* (1-mp.power(p,-1))  # placeholder
        return val
    return zq(1+a-s), A(a,s)
q=97
I=1j
for (a,s) in [(mp.mpf(1)/2+0.3*I, mp.mpf(6)/10+0.2*I),(mp.mpf(1)/2+0.3*I, mp.mpf(6)/10+2.0*I),(mp.mpf(1)/2+0.3*I,mp.mpf(1)/2+0.1+0.3*I)]:
    r=R11(q,a,s); z,A=M11(q,a,s)
    print(f"a={mp.nstr(a,6)} s={mp.nstr(s,6)}: R11={mp.nstr(r,10)} |R|/q={mp.nstr(abs(r)/q,6)}  zeta(1+a-s)={mp.nstr(z,8)}")
