import mpmath as mp
from math import gcd
import cmath, math
mp.mp.dps=20

# prime list up to P for Aq products (float)
P=200000
sv=bytearray([1])*(P+1); sv[0]=sv[1]=0
for i in range(2,int(P**0.5)+1):
    if sv[i]: sv[i*i::i]=bytearray(len(sv[i*i::i]))
primes=[p for p in range(2,P+1) if sv[p]]

# hardcoded cyclic generators for units mod q: dict q -> [(g,order),...]
GEN={2:[(1,1)],3:[(2,2)],4:[(3,2)],8:[(3,2),(5,2)],9:[(2,6)],12:[(7,2),(5,2)],16:[(15,2),(3,4)],
     18:[(5,6)],20:[(11,2),(17,4)],24:[(5,2),(7,2),(13,2)],25:[(2,20)],27:[(2,18)],
     32:[(31,2),(3,8)],36:[(19,2),(29,6)],45:[(11,6),(37,4)],49:[(3,42)],
     5:[(2,4)],7:[(3,6)],11:[(2,10)],13:[(2,12)],17:[(3,16)],15:[(2,4),(11,2)],21:[(2,6),(19,2)],19:[(2,18)],23:[(5,22)],29:[(2,28)],31:[(3,30)],37:[(2,36)],41:[(6,40)],43:[(3,42)],47:[(5,46)],64:[(63,2),(3,16)],128:[(127,2),(3,32)],256:[(255,2),(3,64)],81:[(2,54)],125:[(2,100)],100:[(51,2),(77,20)],484:[(363,2),(365,110)],196:[(99,2),(101,42)],225:[(101,6),(127,20)]}
# note for 

def units(q): return [a for a in range(1,q) if gcd(a,q)==1]
def divisors(q): return [d for d in range(1,q+1) if q%d==0]
def expvec(q,a,gens):
    # brute force: enumerate products
    unitsq=set(units(q))
    # BFS from 1
    from itertools import product
    orders=[o for g,o in gens]
    for ks in product(*[range(o) for o in orders]):
        x=1
        for (g,o),k in zip(gens,ks):
            x=(x*pow(g,k,q))%q
        if x==a: return ks
    raise ValueError((q,a,'not generated'))

def chars(q,gens,primitive_only=False):
    # returns list of (chi_vals dict unit->complex, parity, primitive?)
    unitsq=units(q); ev={a:expvec(q,a,gens) for a in unitsq}
    orders=[o for g,o in gens]
    out=[]
    from itertools import product
    for ks in product(*[range(o) for o in orders]):
        vals={}
        for a in unitsq:
            ang=2*math.pi*sum(k*e/o for k,(g,o),e in zip(ks,gens,ev[a]))
            vals[a]=complex(math.cos(ang),math.sin(ang))
        # conductor: primitive iff for every prime p|q exists unit u=1 mod q/p with chi(u)!=1
        prim=True
        qq=q; p=2
        ps=[]
        m=q
        d=2
        while d*d<=m:
            if m%d==0:
                ps.append(d)
                while m%d==0: m//=d
            d+=1
        if m>1: ps.append(m)
        for p in ps:
            d=q//p
            kern=[a for a in unitsq if (a-1)%d==0]
            if all(abs(vals[a]-1)<1e-9 for a in kern):
                prim=False; break
        if primitive_only and not prim: continue
        out.append({'vals':vals,'par':0 if abs(vals[q-1 if (q-1) in vals else unitsq[0]]-1)<1e-9 else 1,'prim':prim})
    # parity: chi(-1) where -1 mod q = q-1 if gcd(q-1,q)=1 (q>2)
    for c in out:
        if q>2:
            v=c['vals'][q-1]
            c['par']=0 if abs(v-1)<1e-9 else 1
        else: c['par']=0
    return out

def Lval(u,chi,q):
    s=mp.mpc(0)
    for r in range(1,q+1):
        v=chi['vals'].get(r)
        if v is None: continue
        s+=mp.mpc(v.real,v.imag)*mp.zeta(u,mp.mpf(r)/q)
    return q**(-u)*s

def X(q,e,w):
    return (mp.mpf(q)/mp.pi)**(mp.mpf(1)/2-w)*mp.gamma((mp.mpf(1)-w+e)/2)/mp.gamma((w+e)/2)

def zetaq(s,q):
    z=mp.zeta(s)
    for p in primes:
        if q%p==0: z*= (1-p**(-s))
    return z

import cmath
def Aq(a,b,c,d,q):
    # product over p not|q; double precision complex for speed
    A=complex(a); B=complex(b); C=complex(c); D=complex(d)
    prod=1+0j
    for p in primes:
        if q%p==0: continue
        lp=math.log(p)
        t1=cmath.exp(-(C+D)*lp); t2=cmath.exp(-(A+D)*lp); t3=cmath.exp(-(B+C)*lp)
        num=(1-t1)*(1-t2-t3+t1); den=(1-t2)*(1-t3)
        prod*=num/den
    return prod

def Zq(a,b,c,d,q):
    return zetaq(a+b,q)*zetaq(c+d,q)/zetaq(a+d,q)/zetaq(b+c,q)*Aq(a,b,c,d,q)

def Mq(a,b,s,t,q,prim):
    phis=len(prim)
    H=mp.mpc(0)
    for e in (0,1):
        Me=sum(1 for c in prim if c['par']==e)
        H+=Me*X(q,e,a)*X(q,e,b)
    return phis*Zq(a,b,s,t,q)+H*Zq(1-b,1-a,s,t,q)

def Rq(a,b,s,t,q,prim):
    tot=mp.mpc(0)
    for c in prim:
        tot+=Lval(a,c,q)*Lval(b,{'vals':{k:v.conjugate() for k,v in c['vals'].items()},'par':c['par']},q)/(Lval(s,c,q)*Lval(t,{'vals':{k:v.conjugate() for k,v in c['vals'].items()},'par':c['par']},q))
    return tot

eta=mp.mpf('0.05')
a=mp.mpc('0.5','0.37'); b=mp.mpc('0.5','-0.21')
s=mp.mpc('0.55','0.11'); t=mp.mpc('0.55','-0.29')
print("q  phi* Rq Mq  |res|  |res|/q^.5  |res|/phi(q/p)  res")
for q in [196]:
    if q not in GEN: continue
    try:
        cs=chars(q,GEN[q],primitive_only=False)
        prim=[c for c in cs if c['prim']]
        if not prim: 
            print(q,"no primitive",flush=True); continue
        R=Rq(a,b,s,t,q,prim); M=Mq(a,b,s,t,q,prim)
        res=abs(R-M)
        # largest prime factor and phi(q/p)
        ps=[p for p in primes if q%p==0]
        if not ps:
            pp=1
        else:
            pp=min(ps)  # for p^e use p; phi(q/p)
        from math import prod
        def phi(n):
            r=n; d=2; m=n
            while d*d<=m:
                if m%d==0:
                    r=r//d*(d-1)
                    while m%d==0: m//=d
                d+=1
            if m>1: r=r//m*(m-1)
            return r
        phimax=max(phi(q//p) for p in ps) if ps else 1
        print(f"{q:3d} {len(prim):3d} {mp.nstr(abs(R),6):>12} {mp.nstr(abs(M),6):>12} {mp.nstr(res,6):>12} {mp.nstr(res/mp.sqrt(q),6):>10} {mp.nstr(res/phimax,6):>10}",flush=True)
    except Exception as ex:
        print(q,"ERR",ex,flush=True)
