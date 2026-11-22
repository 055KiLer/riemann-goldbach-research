import mpmath as mp
import numpy as np
mp.mp.dps=25
I=mp.mpc(0,1)
def primes_upto(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for p in range(2,int(n**0.5)+1):
        if s[p]:
            for m in range(p*p,n+1,p): s[m]=False
    return [i for i,v in enumerate(s) if v]
P=primes_upto(200000)
def zq(w,q):
    v=mp.zeta(w)
    for p in P:
        if p>q: break
        if q%p==0: v*=(1-mp.power(p,-w))
    return v
def Aq(q,a,b,s,t):
    val=mp.mpf(1)
    for p in P:
        if q%p==0: continue
        u=mp.power(p,-a); v=mp.power(p,-s); w=mp.power(p,-b); z=mp.power(p,-t)
        val*=(1-v*z)*(1-u*z-w*v+v*z)/((1-u*z)*(1-w*v))
    return val
def Zq(q,a,b,s,t): return zq(a+b,q)*zq(s+t,q)/(zq(a+t,q)*zq(b+s,q))*Aq(q,a,b,s,t)
def X(q,w,e): return mp.power(q/mp.pi,mp.mpf(1)/2-w)*mp.gamma((1-w+e)/2)/mp.gamma((w+e)/2)
def phistar(q):
    # sum_{d|q} mu(q/d) phi(d)
    import sympy
    return int(sympy.totient(q)) if False else None
def divisors(q):
    ds=[]
    for d in range(1,q+1):
        if q%d==0: ds.append(d)
    return ds
def mobius(n):
    if n==1: return 1
    f=0; d=2; m=n; cnt=0
    while d*d<=m:
        if m%d==0:
            m//=d; cnt+=1
            if m%d==0: return 0
        d+=1
    if m>1: cnt+=1
    return (-1)**cnt
def phi(n):
    r=n; m=n; d=2
    while d*d<=m:
        if m%d==0:
            while m%d==0: m//=d
            r-=r//d
        d+=1
    if m>1: r-=r//m
    return r
def Me_counts(q):
    # primitive parity counts via formula: q=2^e or odd^e etc -- use brute: count chars mod q with conductor q
    # use: phi*(q)=sum_{d|q}mu(q/d)phi(d); parity split for q odd: equal; q=2^e: equal for e>=3
    # We only need q=2^e here
    e=0;m=q
    while m%2==0: m//=2; e+=1
    assert m==1
    if e<=2: return {0:0,1:0}
    return {0:2**(e-3),1:2**(e-3)}
# load R values computed by ram_fast logic
def L_vals_2e(e,u):
    q=2**e; N=2**(e-2)
    A=np.array([complex(mp.zeta(u,mp.mpf(5**k % q)/q)) for k in range(N)],dtype=np.complex128)
    B=np.array([complex(mp.zeta(u,mp.mpf((-5**k) % q)/q)) for k in range(N)],dtype=np.complex128)
    FA=np.fft.fft(A); FB=np.fft.fft(B)
    qfac=mp.power(q,-u)
    L0={j: complex(qfac)*(FA[j]+FB[j]) for j in range(N)}
    L1={j: complex(qfac)*(FA[j]-FB[j]) for j in range(N)}
    return L0,L1
def Rval_2e(e,a,b,s,t):
    q=2**e; N=2**(e-2)
    La0,La1=L_vals_2e(e,a); Lb0,Lb1=L_vals_2e(e,b); Ls0,Ls1=L_vals_2e(e,s); Lt0,Lt1=L_vals_2e(e,t)
    tot=0j
    for m in (0,1):
        Lam=La1 if m else La0; Lbm=Lb1 if m else Lb0; Lsm=Ls1 if m else Ls0; Ltm=Lt1 if m else Lt0
        for j in range(1,N,2):
            tot+=Lam[j]*Lbm[N-j]/(Lsm[j]*Ltm[N-j])
    return mp.mpc(tot.real,tot.imag)
def cand_M(q,a,b,s,t,level_w='phi_star'):
    ds=divisors(q); tot=0
    Me=Me_counts(q)
    for d in ds:
        muq=mobius(q//d)
        if muq==0: continue
        Z=Zq(q,a,b,s,t)   # for q=2^e all sub-divisors share prime set {2} => Z_d=Z_q
        Hd=sum(Me[e]*X(q,a,e)*X(q,b,e) for e in (0,1))  # FIXME: same for all d? M_e(d) differs!
        tot+=muq*phi(d)*Z   # candidate C1a: phi(d) only
    return tot
if __name__=="__main__":
    a=mp.mpf(1)/2+0.3*I; b=mp.mpf(1)/2+0.4*I; s=mp.mpf(6)/10+0.2*I; t=mp.mpf(6)/10+0.5*I
    for e in [6,7,8]:
        q=2**e; N=2**(e-2)
        R=Rval_2e(e,a,b,s,t)
        # main objects
        Me={0:2**(e-3),1:2**(e-3)}
        phis=2**(e-2)
        Z=Zq(q,a,b,s,t); Zs=Zq(q,1-b,1-a,s,t)
        Hq=sum(Me[k]*X(q,a,k)*X(q,b,k) for k in (0,1))*1  # note X(a)X(b) per GWX
        M_GWX=phis*Z+Hq*Zs
        # divisor-sum candidates (Z_d=Z since same prime set)
        S_mu_phi=sum(mobius(q//d)*phi(d) for d in divisors(q))
        S_mu_phistar=sum(mobius(q//d)*(phi(d)-0) for d in divisors(q))  # placeholder
        # candidate: sum mu(q/d) phi(d) Z  = well-known = ? since sum mu ph = phi*? Actually sum_{d|q}mu(q/d)phi(d)=phi*(q)? no: = prod condition
        M1=S_mu_phi*Z + Hq*Zs   # if Z same for all d, reduces to scalar
        # candidate: sum mu(q/d) [phi(d) Z_d + H_d Zs_d] with H_d using M_e(d) and X_d
        def Me_d(d):
            # primitive parity count mod d (d=2^k)
            m=d; ee=0
            while m%2==0: m//=2; ee+=1
            if ee>=3: return {0:2**(ee-3),1:2**(ee-3)}
            return {0:0,1:0}
        def phi_star(d):
            return sum(mobius(d//x)*phi(x) for x in divisors(d))
        tot=0; tot2=0; tot3=0
        for d in divisors(q):
            muq=mobius(q//d)
            if muq==0: continue
            Med=Me_d(d); Hd=sum(Med[k]*X(d,a,k)*X(d,b,k) for k in (0,1))
            Zd=Zq(d,a,b,s,t) if d>1 else Z  # for d=1 Z undefined; skip d=1 special
            # NB for d=2^k (k>=3) Zd=Z
            tot+=muq*(phi(d)*Z+Hd*Zs)
            tot2+=muq*(phi_star(d)*Z+Hd*Zs)
            tot3+=muq*(phi(d)*Z+Hd*Zs)
        print(f"q=2^{e}: R={mp.nstr(R,9)}")
        for nm,M in [("GWX",M_GWX),("div phi(d)Z+...",tot),("div phi*(d)Z+...",tot2),("scalar sum",M1)]:
            print(f"   {nm:20s}: M={mp.nstr(M,9)} |res|={mp.nstr(abs(R-M),5)} /sqrt(q)={mp.nstr(abs(R-M)/mp.sqrt(q),4)} /(q/p)={mp.nstr(abs(R-M)/(q/2),5)}")
