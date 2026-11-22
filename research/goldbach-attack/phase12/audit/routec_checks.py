import numpy as np, cmath, math
# primitive chars mod prime q via pow(g,k,q)
def chars(q):
    # find primitive root
    def fac(n):
        fs=set(); d=2
        while d*d<=n:
            while n%d==0: fs.add(d); n//=d
            d+=1
        if n>1: fs.add(n)
        return fs
    fs=fac(q-1)
    for g in range(2,q):
        if all(pow(g,(q-1)//f,q)!=1 for f in fs): break
    # units index: disc log base g
    log={}; x=1
    for k in range(q-1):
        log[x]=k; x=x*g%q
    out=[]
    for k in range(1,q-1):  # nonprincipal
        out.append({a: cmath.exp(2j*math.pi*k*log[a]/(q-1)) for a in log})
    return out

def check_identity(q=101,A=1.2,seed=1):
    X=int(q**A); rng=np.random.default_rng(seed)
    c=rng.normal(size=X*X+1)+1j*rng.normal(size=X*X+1)
    d=rng.normal(size=X*X+1)+1j*rng.normal(size=X*X+1)
    ch=chars(q)
    L=0j
    for vals in ch:
        P=sum(c[A_]*vals.get(A_,0) for A_ in range(1,X*X+1) if A_%q!=0)
        Q=sum(d[B_]*np.conj(vals.get(B_,0)) for B_ in range(1,X*X+1) if B_%q!=0)
        L+=P*Q
    R=(q-1)*sum(c[A_]*d[A_] for A_ in range(1,X*X+1))-sum(c[1:])*sum(d[1:])
    W=sum(c[A_]*d[B_] for A_ in range(1,X*X+1) for k in range(1,(X*X-A_)//q+1) for B_ in [A_+k*q])
    # wrap contribution as kernel defines W=Σ_{A≠B,A≡B} c_A d_B
    print(f"identity q={q} X={X}: |E - [(q-1)(D+W)-ScSd]| = {abs(L-((q-1)*(sum(c[A_]*d[A_] for A_ in range(1,X*X+1))+W)-sum(c[1:])*sum(d[1:]))):.3e}")
    print(f"  |W|={abs(W):.4g}  X^(2-4eta)/q bound not tested here")
    return L,W

if __name__=='__main__':
    # identity with random coeffs; W exact
    for q in (101,211):
        for A in (0.8,1.2):
            check_identity(q,A)
