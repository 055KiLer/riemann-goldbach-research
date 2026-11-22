"""Dirichlet character machinery for composite q: primitive chars as products of local chars."""
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

def primitive_root(p):
    m=p-1; fac=[]; d=2; mm=m
    while d*d<=mm:
        if mm%d==0:
            fac.append(d)
            while mm%d==0: mm//=d
        d+=1
    if mm>1: fac.append(mm)
    g=2
    while g<p:
        if all(pow(g,m//q,p)!=1 for q in fac): return g
        g+=1
    raise RuntimeError

def dlog_table(p, g, mod):
    tab=np.full(mod,-1,dtype=np.int64); cur=1
    for j in range(mod):
        tab[cur]=j; cur=cur*g%mod
    return tab

class LocalChar:
    """data for primitive characters modulo a prime power p^e"""
    def __init__(self,p,e):
        self.p=p; self.e=e; self.mod=p**e
        if p==2:
            if e==1:
                self.order=1; self.phi=1; self.kind='triv'; self.chars=[]  # no primitive chars
            elif e==2:
                self.phi=2; self.kind='2^2'; self.chars=[('m4',)]
            else:
                self.phi=2**(e-2)*2; self.kind='2^e'
                # exponent decomposition a = (-1)^L * 5^M ; primitive iff k odd
                self.chars=[(eps,k) for eps in (0,1) for k in range(2**(e-2)) if k%2==1]
        else:
            self.phi=(p-1)*p**(e-1); self.kind='odd'
            g=primitive_root(p)
            # check g primitive mod p^e
            if pow(g,self.phi//p,self.mod)==1:
                g2=p+1 if p>2 else g
                # lift: use g for p odd: standard primitive root mod p^e is g if g^(p-1)!=1 mod p^2 else g+p
                if pow(g,p-1,self.mod)==1: g+=p
            self.g=g
            self.tab=dlog_table(p,g,self.mod)
            self.chars=[k for k in range(self.phi) if k%p!=0]
    def values(self,a):
        """array of character values for a (array of residues mod self.mod) for all primitive local chars"""
        a=np.asarray(a,dtype=np.int64)
        out=np.empty((len(self.chars),len(a)),dtype=complex)
        for i,k in enumerate(self.chars):
            if self.kind=='odd':
                e=self.tab[a%self.mod]
                out[i]=np.exp(2j*np.pi*k*e/self.phi)
            elif self.kind=='2^2':
                out[i]=np.where(a%4==3,-1.0,1.0)
            else:
                eps,k=self.chars[i]
                # L,M decomposition
                y=a%self.mod
                # find L: y mod 8 in {1,7}? L=0 if y%8 in (1,5)? convention: (-1)^L*5^M: y mod 8: 1->L0,7->L1,5->L0,3->L1
                L=np.where((y%8==1)|(y%8==5),0,1)
                # M from repeated exponentiation: find M with 5^M = (-1)^L y
                M=np.zeros(len(y),dtype=np.int64)
                target=y.copy()
                # solve 5^M ≡ (-1)^L y mod 2^e by table
                if not hasattr(self,'five_tab'):
                    mod=self.mod; tab={}
                    cur=1
                    for m in range(2**(self.e-2)):
                        tab[cur]=m; cur=cur*5%mod
                    self.five_tab=tab
                for i2,tg in enumerate(target):
                    val=(tg if L[i2]==0 else (-tg)%self.mod)
                    M[i2]=self.five_tab[val]
                out[i]=((-1)**eps)**L * np.exp(2j*np.pi*k*M/2**(self.e-2))
        return out

class CharGroup:
    """primitive characters modulo q as tuples of local primitive characters"""
    def __init__(self,q):
        self.q=q; fac=factorize(q)
        self.trivial_empty = (q%2==0 and fac.get(2,0)==1)  # no char can have even conductor q=2*m (m odd)
        self.locals=[]
        self.chi=[]   # list of tuples of local indices
        import itertools
        comps=[]
        for p,e in sorted(fac.items()):
            lc=LocalChar(p,e)
            if len(lc.chars)==0:
                comps.append(None); continue
            comps.append(lc); self.locals.append(lc)
        # units mod q
        self.units=np.array([a for a in range(1,q) if gcd(a,q)==1],dtype=np.int64)
        self.phi=len(self.units)
        # build character matrix rows for primitive chars
        mats=[]
        idx_lists=[]
        for lc in self.locals:
            vals=lc.values(self.units)   # (nloc, units)
            mats.append(vals)
        self.nloc=[m.shape[0] for m in mats]
        if self.locals:
            total=int(np.prod([n for n in self.nloc]))
            V=np.ones((total,self.phi),dtype=complex)
            # build via iteration
            signs=[]
            Vrows=[]
            for combo in itertools.product(*[range(n) for n in self.nloc]):
                v=np.ones(self.phi,dtype=complex)
                s=1
                for li,ci in enumerate(combo):
                    v=v*mats[li][ci]
                Vrows.append(v)
            self.V=np.array(Vrows)
            self.combos=list(itertools.product(*[range(n) for n in self.nloc]))
        else:
            self.V=np.zeros((0,self.phi),dtype=complex); self.combos=[]
        self.n=len(self.combos)
        # parity of each char: chi(-1); evaluate V at unit representative of -1 (q-1)
        self.parity=[]
        if self.n:
            try:
                iu=int(np.where(self.units==q-1)[0][0])
                vals=self.V[:,iu]
                self.parity=[0 if abs(v-1)<1e-8 else 1 for v in vals]
            except Exception:
                self.parity=[0]*self.n
        if self.trivial_empty:
            self.V=np.zeros((0,self.phi),dtype=complex); self.n=0; self.combos=[]; self.parity=[]
    def counts(self):
        M0=sum(1 for e in self.parity if e==0); M1=len(self.parity)-M0
        return M0,M1
