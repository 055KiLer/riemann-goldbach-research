"""Character group machinery for Dirichlet characters mod even N (N = 2 * odd).

Group structure: (Z/N)^* = prod_p (Z/p^e)^*, each cyclic, p odd.
Every unit a <-> exponent vector (e_p) with a = prod g_p^{e_p} (mod p^e).
Character chi_{k} = prod omega_p^{k_p e_p}, omega_p = exp(2 pi i / order_p).
Forward character sums: Bhat[k] = sum_a chi_k(a) B[a].
"""
import numpy as np
from math import gcd

def primitive_root_prime_power(p, e=1):
    assert p % 2 == 1
    n = p**e
    phi = (p-1)*p**(e-1)
    fac = set()
    m = p-1
    d = 2
    while d*d <= m:
        if m % d == 0:
            fac.add(d)
            while m % d == 0: m//=d
        d += 1
    if m > 1: fac.add(m)
    for g in range(2, n):
        if gcd(g, n) != 1: continue
        if all(pow(g, phi//q, n) != 1 for q in fac):
            return g
    raise RuntimeError

class CharacterGroup:
    def __init__(self, N):
        self.N = N
        fac = []
        n = N; d = 2
        while d*d <= n:
            if n % d == 0:
                e = 0
                while n % d == 0:
                    n//=d; e+=1
                fac.append((d,e))
            d+=1
        if n>1: fac.append((n,1))
        self.fac = fac
        self.orders = []; self.gens = []; self.mods = []
        for p,e in fac:
            if p == 2:
                assert e == 1, "only N = 2 * odd supported"
                continue
            self.orders.append((p-1)*p**(e-1))
            self.gens.append(primitive_root_prime_power(p,e))
            self.mods.append(p**e)
        self.orders = tuple(self.orders)
        self.phi = int(np.prod(self.orders))
        # strides for C-order ravel of shape orders
        strides = []; s=1
        for o in reversed(self.orders):
            strides.append(s); s*=o
        self.strides = tuple(reversed(strides))
        self.shape = self.orders
        # discrete-log tables for each cyclic factor (avoids O(order) search per unit)
        dlogs = []
        for m,g in zip(self.mods, self.gens):
            order = 1
            for o,mm in zip(self.orders,self.mods):
                if mm==m: order=o
            tab = np.full(m, -1, dtype=np.int64)
            cur = 1
            for x in range(order):
                tab[cur] = x
                cur = (cur*g) % m
            xs = np.arange(1,m)
            xsu = xs[np.array([gcd(int(x),m)==1 for x in xs])]
            assert np.all(tab[xsu]>=0), "not a primitive root?"
            dlogs.append(tab)
        # units and exponent vectors
        units = []; exps = []
        for a in range(1, N):
            if gcd(a, N) != 1: continue
            ev = [int(tab[a % m]) for tab,m in zip(dlogs,self.mods)]
            units.append(a); exps.append(ev)
        self.units = np.array(units, dtype=np.int64)
        self.exps = np.array(exps, dtype=np.int64)  # shape (phi, nprimes)
        assert len(units) == self.phi, (len(units), self.phi)
        # flat index of each unit; and flat index after negating exponent vector
        flat = self.exps @ np.array(self.strides, dtype=np.int64)
        self.flat = flat
        neg = tuple((o - self.exps[:,i]) % o for i,o in enumerate(self.orders))
        negflat = np.stack(neg, axis=1) @ np.array(self.strides, dtype=np.int64)
        self.negflat = negflat
        # odd character mask over full flat array
        par = (self.exps.sum(axis=1) % 2).astype(int)
        self.chi_parity = np.zeros(self.phi, dtype=np.int8)
        self.chi_parity[flat] = par   # 1 if chi(a)=-1, i.e. a=-1 representation
        # generate full exponent multi-index arrays
        grids = np.meshgrid(*[np.arange(o) for o in self.orders], indexing='ij')
        self.kvecs = [g.ravel() for g in grids]  # each shape (phi,)
        self.kmodd = (sum(self.kvecs) % 2 == 1)  # odd character mask in flat char ordering
        self.nodd = int(self.kmodd.sum())

    def char_matrix(self):
        """Full (phi x phi) table T[a_index, k_flat] = chi_k(a)."""
        T = np.ones((len(self.units), self.phi), dtype=complex)
        for i,o in enumerate(self.orders):
            om = np.exp(2j*np.pi*np.arange(o)/o)
            T *= om[(np.outer(self.exps[:,i], self.kvecs[i])) % o]
        return T

    def forward(self, B):
        """B: array shape (..., phi) indexed by unit ordering (position i <-> units[i]).
        returns Bhat shape (..., phi) ordered by char flat index k."""
        B = np.asarray(B)
        lead = B.shape[:-1]
        X = np.zeros(lead + (self.phi,), dtype=complex)
        # scatter: B[i] goes to flat position negflat[i]
        X[..., self.negflat] = B
        X = X.reshape(lead + self.shape)
        F = np.fft.fftn(X, axes=tuple(range(len(lead), len(lead)+len(self.shape))))
        return F.reshape(lead + (self.phi,))

if __name__ == "__main__":
    import time
    for N in (2*3*5, 2*3*5*7):
        cg = CharacterGroup(N)
        T = cg.char_matrix()
        # test forward: B[a] = 1 for unit a; sum over chars chi(a) expected = phi*1_{a=1}
        B = np.zeros(cg.phi); B[0] = 1.0  # unit a=1 at position 0
        Bh = cg.forward(B)
        # Bh[k] = chi_k(1)=1 for all k
        print(N, "check1", np.abs(Bh-1).max(), "phi", cg.phi)
        # random B, compare forward with T^T B
        rng = np.random.default_rng(1)
        B = rng.standard_normal(cg.phi)+1j*rng.standard_normal(cg.phi)
        Bh = cg.forward(B)
        print(N, "check2", np.abs(Bh - T.T@B).max())
    # now N=30030
    t0=time.time()
    cg = CharacterGroup(30030)
    print("N=30030 phi", cg.phi, "odd", cg.nodd, "orders", cg.orders, "gens", cg.gens, "time", time.time()-t0)
    rng = np.random.default_rng(2)
    B = rng.standard_normal(cg.phi)+1j*rng.standard_normal(cg.phi)
    t0=time.time(); Bh = cg.forward(B); print("forward time", time.time()-t0)
    # validate 8 random chars directly via exponent formula
    from math import gcd
    maxerr=0
    for trial in range(8):
        k = [int(rng.integers(o)) for o in cg.orders]
        # chi_k(a) values
        vals = np.ones(cg.phi, dtype=complex)
        for i,o in enumerate(cg.orders):
            vals *= np.exp(2j*np.pi*(k[i]*cg.exps[:,i] % o)/o)
        kf = sum(kk*st for kk,st in zip(k, cg.strides))
        direct = vals @ B
        maxerr=max(maxerr, abs(direct-Bh[kf]))
    print("char forward validation maxerr", maxerr)
    # check odd mask consistency: chi(-1) for -1 unit
    i_neg = int(np.where(cg.units == 30030-1)[0][0])
    vals = np.ones(cg.phi, dtype=complex)
    for i,o in enumerate(cg.orders):
        vals *= np.exp(2j*np.pi*(cg.kvecs[i]*cg.exps[i_neg,i] % o)/o)
    ok = np.allclose(vals, np.where(cg.kmodd, -1.0, 1.0), atol=1e-10)
    print("odd mask check:", ok)
