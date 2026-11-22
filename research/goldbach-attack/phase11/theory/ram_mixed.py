import mpmath as mp, math
mp.mp.dps=25
I=mp.mpc(0,1)
def primes_upto(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for p in range(2,int(n**0.5)+1):
        if s[p]:
            for m in range(p*p,n+1,p): s[m]=False
    return [i for i,v in enumerate(s) if v]
P=primes_upto(300000)
def fac(q):
    f={};d=2
    while d*d<=q:
        while q%d==0: f[d]=f.get(d,0)+1;q//=d
        d+=1
    if q>1: f[q]=f.get(q,0)+1
    return f
def group_structure(q):
    U=[a for a in range(1,q) if math.gcd(a,q)==1]
    def order(g):
        o=1;x=g
        while x!=1: x=x*g%q;o+=1
        return o
    for g in U:
        if order(g)==len(U): return [g],[len(U)]
    for g1 in U:
        n1=order(g1)
        for g2 in U:
            n2=order(g2)
            seen=set()
            for i in range(n1):
                xi=pow(g1,i,q)
                for j in range(n2): seen.add(xi*pow(g2,j,q)%q)
            if len(seen)==len(U) and n1*n2==len(U): return [g1,g2],[n1,n2]
    raise RuntimeError("no structure")
def all_chars(q):
    gens,ords=group_structure(q); chars=[]
    if len(gens)==1:
        g,=gens; n,=ords; dlog={1:0};x=1
        for k in range(1,n): x=x*g%q; dlog[x]=k
        for j in range(n):
            chi=[0]*q
            for a,dl in dlog.items(): chi[a-1]=mp.e**(2j*mp.pi*j*dl/n)
            chars.append(chi)
        return chars
    g1,g2=gens; n1,n2=ords; rep={}
    for i in range(n1):
        xi=pow(g1,i,q)
        for j in range(n2): rep[xi*pow(g2,j,q)%q]=(i,j)
    n_g=n1*n2
    if n_g==len([a for a in range(1,q) if math.gcd(a,q)==1]):
        for k in range(n1):
            for l in range(n2):
                chi=[0]*q
                for a,(i,j) in rep.items(): chi[a-1]=mp.e**(2j*mp.pi*(k*i/n1+l*j/n2))
                chars.append(chi)
        return chars
    # dedupe: enumerate all homomorphisms via brute force if needed
    chars=[]
    for k in range(n1):
        for l in range(n2):
            chi=[0]*q
            for a,(i,j) in rep.items(): chi[a-1]=mp.e**(2j*mp.pi*(k*i/n1+l*j/n2))
            chars.append(chi)
    return chars
def isprim(chi,q):
    for p in fac(q):
        m=q//p
        H=[a for a in range(1,q) if math.gcd(a,q)==1 and (a-1)%m==0]
        if all(abs(chi[a-1]-1)<1e-11 for a in H): return False
    return True
def Lval(u,chi,q):
    return mp.power(q,-u)*mp.fsum([chi[a-1]*mp.zeta(u,mp.mpf(a)/q) for a in range(1,q) if chi[a-1]!=0])
def M_GWX(q,a,b,s,t,prims):
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
    Z=lambda A,B,S,T: zq(A+B)*zq(S+T)/(zq(A+T)*zq(B+S))*Aq(A,B,S,T)
    ph=len(prims); Me={0:0,1:0}
    for chi in prims:
        par=chi[q-2].real; Me[0 if par>0 else 1]+=1
    def X(w,e): return mp.power(q/mp.pi,mp.mpf(1)/2-w)*mp.gamma((1-w+e)/2)/mp.gamma((w+e)/2)
    Hq=sum(Me[e]*X(a,e)*X(b,e) for e in (0,1))
    return ph*Z(a,b,s,t)+Hq*Z(1-b,1-a,s,t),ph,Me
def run(q,a,b,s,t):
    chars=all_chars(q); prims=[c for c in chars if isprim(c,q)]
    tot=mp.mpf(0)
    for chi in prims:
        chic=[mp.conj(c) if c!=0 else 0 for c in chi]
        tot+=Lval(a,chi,q)*Lval(b,chic,q)/(Lval(s,chi,q)*Lval(t,chic,q))
    M,ph,Me=M_GWX(q,a,b,s,t,prims)
    return tot,M,ph,Me
if __name__=="__main__":
    a=mp.mpf(1)/2+0.3*I; b=mp.mpf(1)/2+0.4*I; s=mp.mpf(6)/10+0.2*I; t=mp.mpf(6)/10+0.5*I
    for q in [44,52,68,76,92,116,404, 99,117,153,171, 88,104,136]:
        F=fac(q); rep=[p for p,e in F.items() if e>=2]
        if not rep: continue
        p=rep[0]; qp=q//p
        try:
            R,M,ph,Me=run(q,a,b,s,t); res=abs(R-M)
            print(f"q={q:4d} (p={p}) phi*={ph:4d} Me={Me} |R-M|={mp.nstr(res,5)} /sqrt(q)={mp.nstr(res/mp.sqrt(q),4)} /(q/p)={mp.nstr(res/mp.mpf(qp),5)} /phi(q/p)={mp.nstr(res/mp.mpf(len([x for x in range(1,qp+1) if math.gcd(x,qp)==1])),5)}")
        except Exception as ex:
            print(q,"FAIL",ex)
