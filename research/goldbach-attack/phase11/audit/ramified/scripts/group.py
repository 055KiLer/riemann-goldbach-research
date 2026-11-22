"""Own generic (Z/q)^* decomposition, char enumeration, multi-dim DFT; NO dense character table.
lives in phase11/audit/ramified/scripts (heat-kernel-critic own code)."""
import numpy as np
from math import gcd
from itertools import product

def factorize(n):
    f={}; d=2
    while d*d<=n:
        while n%d==0: f[d]=f.get(d,0)+1; n//=d
        d+=1
    if n>1: f[n]=f.get(n,0)+1
    return f

def primitive_root(p):
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

class Grp:
    def __init__(self,q):
        self.q=q; self.fac=factorize(q); self.comps=[]
        for p,e in self.fac.items():
            m=p**e
            if p==2:
                if e==1: continue
                if e==2: self.comps.append(dict(mod=m,order=2,kind='s2'))
                else:
                    self.comps.append(dict(mod=m,order=2,kind='s'))
                    self.comps.append(dict(mod=m,order=2**(e-2),kind='five'))
            else:
                self.comps.append(dict(mod=m,order=(p-1)*p**(e-1),gen=primitive_root(p),kind='cyc'))
        self.r=len(self.comps); self.orders=np.array([c['order'] for c in self.comps],dtype=np.int64)
        self.phi=int(np.prod(self.orders)) if self.r else 1
        self.units=np.array([a for a in range(1,q) if gcd(a,q)==1],dtype=np.int64)
        assert len(self.units)==self.phi,(q,len(self.units),self.phi,self.comps)
        for c in self.comps:
            m=c['mod']; n=c['order']
            if c['kind']=='cyc':
                tab=np.full(m,-1,dtype=np.int64); cur=1
                for x in range(n): tab[cur]=x; cur=cur*c['gen']%m
                c['tab']=tab
            elif c['kind']=='five':
                tab=np.full(m,-1,dtype=np.int64); cur=1
                for x in range(n): tab[cur]=x; cur=cur*5%m
                c['tab']=tab
        E=np.zeros((self.phi,self.r),dtype=np.int64)
        for i,a in enumerate(self.units):
            for j,c in enumerate(self.comps):
                m=c['mod']
                if c['kind']=='cyc': E[i,j]=c['tab'][a%m]
                elif c['kind']=='five':
                    s=0 if a%4==1 else 1; y=(a%m) if s==0 else ((-a)%m); E[i,j]=c['tab'][y]
                elif c['kind']=='s': E[i,j]=0 if a%4==1 else 1
                elif c['kind']=='s2': E[i,j]=0 if a%m==1 else 1
        self.exps=E
        self.kvecs=np.array(list(product(*[range(int(n)) for n in self.orders])),dtype=np.int64) if self.r else np.zeros((1,0),dtype=np.int64)
        self.nchars=self.phi
        self.shape=tuple(int(n) for n in self.orders)
        self.uindex={int(a):i for i,a in enumerate(self.units)}
        self._primitive()
    def charvals_at_unit_indices(self,idx,chi_conj=False):
        """chi_k(units[idx]) for all chars k: returns array (nchars,len(idx)) complex"""
        ks=self.kvecs.astype(np.float64)/self.orders.astype(np.float64)
        phase=(ks@self.exps[idx].astype(np.float64).T) # nchars x len(idx)
        if chi_conj: phase=-phase
        return np.exp(2j*np.pi*phase)
    def _primitive(self):
        q=self.q
        if q<=2 or self.fac.get(2,0)==1:
            self.prim=np.zeros(self.nchars,dtype=bool); self.Me=[0,0]; self.phistar=0
        else:
            prim=np.ones(self.nchars,dtype=bool)
            for p in self.fac:
                m=q//p
                if m==1: idx=list(range(self.phi))
                else: idx=[i for i,a in enumerate(self.units) if int(a)%m==1]
                if not idx: continue
                V=self.charvals_at_unit_indices(np.array(idx,dtype=np.int64))  # nchars x |K|
                trivial=np.all(np.abs(V-1.0)<1e-9,axis=1)
                prim &= ~trivial
            self.prim=prim
            ineg=self.uindex[q-1]
            v=self.charvals_at_unit_indices(np.array([ineg]))[:,0]
            pos=np.real(v)>0.5; neg=np.real(v)<-0.5
            self.Me=[int(np.sum(prim&pos)),int(np.sum(prim&neg))]
            self.phistar=int(prim.sum())
            assert self.Me[0]+self.Me[1]==self.phistar
        # precompute parity of -1
    def dft_L(self, vals_unit):
        """vals_unit: array len phi in unit order. Returns (Lchi, Lchibar) arrays indexed by char flat index:
        Lchi=q^{-u} sum_x chi(x) vals[x]; Lchibar=q^{-u} sum_x conj(chi(x)) vals[x].
        (caller multiplies q^{-u}).  Convention: B[exp tuple]=vals."""
        B=np.empty(self.shape,dtype=np.complex128)
        for i in range(self.phi):
            B[tuple(self.exps[i])]=vals_unit[i]
        Fplus=np.fft.ifftn(B)*self.phi
        Fminus=np.fft.fftn(B)
        # flatten consistent with kvecs order (C-order)
        return Fplus.ravel(), Fminus.ravel()
