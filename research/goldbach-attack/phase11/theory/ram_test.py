import mpmath as mp, math, itertools
mp.mp.dps=30
I=mp.mpc(0,1)

def primes_upto(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for p in range(2,int(n**0.5)+1):
        if s[p]:
            for m in range(p*p,n+1,p): s[m]=False
    return [i for i,v in enumerate(s) if v]
P=primes_upto(200000)

def group_structure(q):
    U=[a for a in range(1,q) if math.gcd(a,q)==1]
    # try one generator
    def order(g):
        o=1;x=g
        while x!=1: x=x*g%q;o+=1
        return o
    for g in U:
        if order(g)==len(U): return [g],[len(U)]
    # two generators
    for g1 in U:
        n1=order(g1); H={1}; x=1
        for i in range(n1): H.add(x); x=x*g1%q
        for g2 in U:
            n2=order(g2)
            seen=set(); ok=False
            for i in range(n1):
                xi=pow(g1,i,q)
                for j in range(n2):
                    seen.add(xi*pow(g2,j,q)%q)
            if len(seen)==len(U) and n1*n2==len(U):
                return [g1,g2],[n1,n2]
    raise RuntimeError("no structure")

def all_chars(q):
    gens,ords=group_structure(q)
    chars=[]
    if len(gens)==1:
        g,=gens; n,=ords
        # discrete log
        dlog={1:0}; x=1
        for k in range(1,n): x=x*g%q; dlog[x]=k
        for j in range(n):
            chi=[0]*q
            for a,dl in dlog.items(): chi[a-1]=mp.e**(2j*mp.pi*j*dl/n)
            chars.append(chi)
    else:
        g1,g2=gens; n1,n2=ords
        # representations: find (i,j) for each unit
        rep={}
        for i in range(n1):
            xi=pow(g1,i,q)
            for j in range(n2):
                rep[xi*pow(g2,j,q)%q]=(i,j)
        for k in range(n1):
            for l in range(n2):
                chi=[0]*q
                for a,(i,j) in rep.items():
                    chi[a-1]=mp.e**(2j*mp.pi*(k*i/n1+l*j/n2))
                chars.append(chi)
        # dedupe (in case representations not unique -> n1*n2>phi)
    return chars

def isprim(chi,q):
    for p in set(f for f in range(2,q+1) if q%f==0 and all(f%d for d in range(2,int(f**0.5)+1))):
        m=q//p
        H=[a for a in range(1,q) if math.gcd(a,q)==1 and (a-1)%m==0]
        if all(abs(chi[a-1]-1)<1e-12 for a in H): return False
    return True

def Lval(u,chi,q):
    tot=mp.mpf(0)
    for a in range(1,q):
        ca=chi[a-1]
        if ca!=0: tot+=ca*mp.zeta(u,mp.mpf(a)/q)
    return mp.power(q,-u)*tot

def M_GWX(q,a,b,s,t):
    def zq(w):
        v=mp.zeta(w)
        for p in P:
            if p>q: break
            if q%p==0: v*=(1-mp.power(p,-w))
        return v
    def Aq(a,b,s,t):
        val=mp.mpf(1)
        for p in P:
            if p>200000: break
            if q%p==0: continue
            x=mp.power(p,-a-t); y=mp.power(p,-b-s); z=mp.power(p,-s-t)
            val*=(1-z)*(1-x-y+z)/((1-x)*(1-y))
        return val
    Z=lambda A,B,S,T: zq(A+B)*zq(S+T)/(zq(A+T)*zq(B+S))*Aq(A,B,S,T)
    chars=all_chars(q); ph=0; Me={0:0,1:0}
    for chi in chars:
        if not isprim(chi,q): continue
        ph+=1; par=chi[q-2].real; Me[0 if par>0 else 1]+=1
    def X(w,e): return mp.power(q/mp.pi,mp.mpf(1)/2-w)*mp.gamma((1-w+e)/2)/mp.gamma((w+e)/2)
    Hq=sum(Me[e]*X(a,e)*X(b,e) for e in (0,1))
    return ph*Z(a,b,s,t)+Hq*Z(1-b,1-a,s,t), ph, Me, Hq, Z

def Rexact(q,a,b,s,t):
    chars=all_chars(q); tot=mp.mpf(0); cnt=0
    for chi in chars:
        if not isprim(chi,q): continue
        cnt+=1
        chic=[mp.conj(c) if c!=0 else 0 for c in chi]
        tot+=Lval(a,chi,q)*Lval(b,chic,q)/(Lval(s,chi,q)*Lval(t,chic,q))
    return tot,cnt

if __name__=="__main__":
    tests=[("crit", mp.mpf(1)/2+0.3*I, mp.mpf(1)/2+0.4*I, mp.mpf(6)/10+0.2*I, mp.mpf(6)/10+0.5*I),
           ("shift",mp.mpf(3)/4+0.3*I, mp.mpf(3)/4+0.4*I, mp.mpf(6)/10+0.2*I, mp.mpf(6)/10+0.5*I)]
    for q in [8,9,16,25,27,32,49,12,18,45,50]:
        for nm,a,b,s,t in tests:
            try:
                R,cnt=Rexact(q,a,b,s,t); M,ph,Me,Hq,Z=M_GWX(q,a,b,s,t)
                resid=R-M
                print(f"q={q:4d} {nm}: phi*={ph} Me={Me} cnt={cnt} R={mp.nstr(R,9)} M={mp.nstr(M,9)} |res|={mp.nstr(abs(resid),4)} |res|/sqrt(q)={mp.nstr(abs(resid)/mp.sqrt(q),4)} |res|/phi*={mp.nstr(abs(resid)/ph if ph else 0,4)}")
            except Exception as ex:
                print(f"q={q} {nm}: FAIL {ex}")
