"""Own implementation: abelian character group (Z/q)^*, DFT over units, primitive-character filter.
No imports from phase-10/11 code."""
import numpy as np
from math import gcd

def factorize(n):
    f={}; d=2
    while d*d<=n:
        while n%d==0:
            f[d]=f.get(d,0)+1; n//=d
        d+=1
    if n>1: f[n]=f.get(n,0)+1
    return f

def primitive_root_prime(p):
    # p odd prime
    from math import gcd
    phi=p-1; fac=set(); m=phi; d=2
    while d*d<=m:
        if m%d==0:
            fac.add(d)
            while m%d==0: m//=d
        d+=1
    if m>1: fac.add(m)
    for g in range(2,p):
        if all(pow(g,phi//q,p)!=1 for q in fac): return g
    raise RuntimeError

class UnitGroup:
    """(Z/q)^* decomposed into cyclic factors; units and exponent vectors; character table T (nchars x nunits)."""
    def __init__(self,q):
        self.q=q; self.fac=factorize(q)
        qs=list(self.fac.items())
        self.comps=[]  # each: dict(mod=m, order=n, kind, table)
        for p,e in qs:
            m=p**e
            if p==2:
                if e==1: continue
                if e==2:
                    self.comps.append(dict(mod=4,order=2,kind='sign2'))
                else:
                    self.comps.append(dict(mod=m,order=2,kind='sign'))
                    self.comps.append(dict(mod=m,order=2**(e-2),kind='five'))
            else:
                g=primitive_root_prime(p)
                self.comps.append(dict(mod=m,order=(p-1)*p**(e-1),gen=g,kind='cyc'))
        self.r=len(self.comps)
        self.units=np.array([a for a in range(1,q) if gcd(a,q)==1],dtype=np.int64)
        self.phi=len(self.units)
        assert self.phi==int(np.prod([c['order'] for c in self.comps])) if self.r else self.phi==1, (q,self.phi,self.comps)
        # discrete log tables for cyc comps, 5-table for five
        for c in self.comps:
            m=c['mod']; n=c['order']
            if c['kind']=='cyc':
                g=c['gen']; tab=np.full(m,-1,dtype=np.int64); cur=1
                for x in range(n): tab[cur]=x; cur=(cur*g)%m
                c['tab']=tab
            elif c['kind']=='five':
                tab=np.full(m,-1,dtype=np.int64); cur=1
                for x in range(n): tab[cur]=x; cur=(cur*5)%m
                c['tab']=tab
        # exponent vectors (nunits, r)
        E=np.zeros((self.phi,self.r),dtype=np.int64)
        for i,a in enumerate(self.units):
            for j,c in enumerate(self.comps):
                m=c['mod']
                if c['kind']=='cyc':
                    E[i,j]=c['tab'][a%m]
                elif c['kind']=='five':
                    # e>=3: x = (-1)^s 5^t ; s=(a mod 4 ==3)
                    sgn = 0 if (a%4)==1 else 1
                    y = (a % m) if sgn==0 else ((-a) % m)
                    E[i,j]=c['tab'][y]
                    # store sign in the companion 'sign' comp entry too (handled there)
                elif c['kind']=='sign':
                    E[i,j]= 0 if (a%4)==1 else 1
                elif c['kind']=='sign2':
                    E[i,j]=0 if (a%m)==1 else 1
        self.exps=E
        self.orders=np.array([c['order'] for c in self.comps],dtype=np.int64)
        # all char index tuples
        from itertools import product
        self.kvecs=np.array(list(product(*[range(int(n)) for n in self.orders])),dtype=np.int64) if self.r else np.zeros((1,0),dtype=np.int64)
        self.nchars=len(self.kvecs)
        assert self.nchars==self.phi
        # T[k,i] = prod_j omega_j^{k_j E[i,j]} = exp(2pi i * E @ (k/orders))
        self.T=np.empty((self.nchars,self.phi),dtype=np.complex128)
        if self.r:
            app=self.kvecs.astype(np.float64)/self.orders.astype(np.float64).reshape(1,-1)  # nchars x r
            theta=app@self.exps.astype(np.float64).T  # nchars x nunits
        else:
            theta=np.zeros((self.nchars,self.phi))
        self.T=np.exp(2j*np.pi*theta)
        # index of units for fast lookup
        self.uindex={int(a):i for i,a in enumerate(self.units)}
        # parity counts and primitive mask
        self._build_primitives()
    def _build_primitives(self):
        q=self.q
        if q<=2:
            self.prim=np.zeros(1,dtype=bool); self.Me=[0,0]; self.phistar=0; return
        fac=self.fac
        if fac.get(2,0)==1:
            self.prim=np.zeros(self.nchars,dtype=bool); self.Me=[0,0]; self.phistar=0; return
        prim=np.ones(self.nchars,dtype=bool)
        for p in fac:
            m=q//p
            # units x with x % m == 1   (m==1: all units, reduction map trivial)
            if m==1:
                idx=list(range(len(self.units)))
            else:
                idx=[i for i,a in enumerate(self.units) if int(a)%m==1]
            if not idx:
                continue
            trivial=np.all(np.abs(self.T[:,idx]-1.0)<1e-9,axis=1)
            prim &= ~trivial
        self.prim=prim
        # parity: chi(-1)
        i_neg=self.uindex[q-1]
        vals=self.T[:,i_neg]
        mp=np.real(vals)>0.5  # chi(-1)=+1
        mm=np.real(vals)<-0.5
        self.Me=[int(np.sum(prim & mp)), int(np.sum(prim & mm))]
        self.phistar=int(prim.sum())
        assert self.Me[0]+self.Me[1]==self.phistar
    def L_values(self,b,chi_conj=False):
        """L(u,chi_k)=q^{-u} sum_x chi_k(x) zeta(u,x/q); b: complex128 array len phi (zeta values at units ordering).
        chi_conj=True uses conj(chi)."""
        v=(self.T.conj() if chi_conj else self.T)@b
        return v
