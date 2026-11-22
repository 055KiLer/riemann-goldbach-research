"""Phase-12 (task-52) own code: exact-ish computation of wrap sum
W(q,X) = sum_{A≡B mod q, A≠B} c_A conj(d_B),  c_A = sum_{nm=A, n,m<=X} f(n) g(m)
via residue grouping. No importing others' phase scripts.
"""
import numpy as np, math, cmath

def sieve_mu(n):
    mu=np.zeros(n+1,dtype=np.int8); mu[1]=1
    primes=[]; comp=np.zeros(n+1,dtype=bool)
    for i in range(2,n+1):
        if not comp[i]: primes.append(i); mu[i]=-1
        for p in primes:
            if i*p>n: break
            comp[i*p]=True
            if i%p==0: mu[i*p]=0; break
            mu[i*p]=-mu[i]
    return mu

def coef_pair(X, model, eta, shiftseed=0):
    """returns f(n) for n=1..X and g(m) for m=1..X (complex arrays), such that c_A=sum_{nm=A}f(n)g(m)."""
    n=np.arange(1,X+1,dtype=np.float64)
    if model=='rect':
        return np.ones(X,dtype=np.complex128), np.ones(X,dtype=np.complex128)
    mu=sieve_mu(X).astype(np.complex128)
    if model=='pos':          # f=n^{-1/2}, g=m^{-1/2-eta}, no mu
        f=n**(-0.5); g=n**(-(0.5+eta))
    elif model=='pos_mu':     # with mu
        f=n**(-0.5); g=mu*n**(-(0.5+eta))
    elif model=='pos_mu_eta_a':  # asymmetric real: f=n^{-1/2}, g=mu m^{-1/2-eta} (same) -> same as pos_mu
        f=n**(-0.5); g=mu*n**(-(0.5+eta))
    elif model=='cplx':
        a=0.5+0.7j; b=0.5+1.3j; s=0.5+eta+0.4j; t=0.5+eta+2.1j
        f=n**(-a); g=mu*n**(-s)
        # for d: use b,t -> store in tuple? handled by caller with model2
        return f,g,('cplx2',b,t)
    else:
        raise ValueError(model)
    return f,g,None

def fg(model,eta,which):
    """return (f,g) for c_A (which='c') or d_B (which='d')."""
    pass

def residue_sums(X,q,f,g,chunk=None):
    """Sc[r]=sum_{nm≡r mod q} f(n)g(m) via pair loop. Returns complex array length q."""
    Sc=np.zeros(q,dtype=np.complex128)
    m_arr=np.arange(1,X+1,dtype=np.int64)
    for nn in range(1,X+1):
        res=(nn*m_arr)%q
        w=f[nn-1]*g
        Sc += np.bincount(res, weights=w.real, minlength=q)
        Sc += 1j*np.bincount(res, weights=w.imag, minlength=q)
    return Sc

def arrays_cd(X,Y,f,g,fd,gd):
    """build full c_A,d_A arrays length Y+1 (np.add.at) and diag."""
    c=np.zeros(Y+1,dtype=np.complex128); 
    mA=np.arange(1,X+1,dtype=np.int64)
    for nn in range(1,X+1):
        idx=nn*mA
        w=f[nn-1]*g
        np.add.at(c, idx, w)
    d=np.zeros(Y+1,dtype=np.complex128)
    for nn in range(1,X+1):
        idx=nn*mA
        w=fd[nn-1]*gd
        np.add.at(d, idx, w)
    diag=np.sum(c[1:]*np.conj(d[1:]))
    return c,d,diag

def compute_W(q,X,fc,gc,fd,gd,Y_arr_limit=4_000_000, verbose=False):
    """W = Σ_r Sc[r]*conj(Sd[r]) - diag, exact when Y=X²<=Y_arr_limit; else W_no_diag and diag bound flag."""
    Y=X*X
    Sc=residue_sums(X,q,fc,gc)
    if fd is gc and np.array_equal(fd,fc) and np.array_equal(gd,gc):
        Sd=Sc.copy()
    else:
        Sd=residue_sums(X,q,fd,gd)
    Wnodiag=complex(np.sum(Sc*np.conj(Sd)))
    exact=(Y<=Y_arr_limit)
    if exact:
        try:
            c,d,diag=arrays_cd(X,Y,fc,gc,fd,gd)
            W=Wnodiag-diag; diagerr=0.0
        except MemoryError:
            exact=False; W=Wnodiag; diag=None; diagerr=None
    else:
        W=Wnodiag; diag=None; diagerr=None
    mass=float(np.sum(np.abs(Sc)))
    L1c=float(np.sum(np.abs(fc))*np.sum(np.abs(gc)))  # not exact sum |c_A| but an upper-model mass
    return dict(q=int(q),X=int(X),Y=int(Y),W=complex(W),Wabs=abs(W),Wnodiag=complex(Wnodiag),
                exact=bool(exact),diag=(complex(diag) if diag is not None else None),
                mass_Sc=mass,
                sum_Sc=complex(np.sum(Sc)),sum_Sd=complex(np.sum(Sd)),
                L1model=float(np.sum(np.abs(fc))*np.sum(np.abs(gc)))*float(np.sum(np.abs(fd))*np.sum(np.abs(gd))) if False else None)

def make_fg(model,eta,which):
    X_holder=None
    mu_cache={}
    def F(X):
        n=np.arange(1,X+1,dtype=np.float64)
        if model=='rect':
            return np.ones(X,dtype=np.complex128), np.ones(X,dtype=np.complex128)
        mu=sieve_mu(X)[1:].astype(np.complex128)
        if model=='pos':
            return n**(-0.5), n**(-(0.5+eta))
        if model=='pos_mu':
            return n**(-0.5), mu*n**(-(0.5+eta))
        if model=='cplx':
            if which=='c':
                a=0.5+0.7j; s=0.5+eta+0.4j
            else:
                a=0.5+1.3j; s=0.5+eta+2.1j
            return n**(-a), mu*n**(-s)
        raise ValueError
    return F
