import mpmath as mp, math
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
def Aq_all(q):
    val=mp.mpf(1)
    for p in P:
        if q%p==0: continue
        val*=(p,p)
    return val
def local(p,a,b,s,t):  # unramified diagonal local factor (1-uz-wv+vz)/(1-uw)
    u=mp.power(p,-a); v=mp.power(p,-s); w=mp.power(p,-b); z=mp.power(p,-t)
    return (1-u*z-w*v+v*z)/(1-u*w)
def Zq(q,a,b,s,t):
    return zq(a+b,q)*zq(s+t,q)/(zq(a+t,q)*zq(b+s,q))*Aq(q,a,b,s,t)
def Aq(q,a,b,s,t):
    val=mp.mpf(1)
    for p in P:
        if q%p==0: continue
        u=mp.power(p,-a); v=mp.power(p,-s); w=mp.power(p,-b); z=mp.power(p,-t)
        val*=(1-v*z)*(1-u*z-w*v+v*z)/((1-u*z)*(1-w*v))
    return val
def ramfactor(q,a,b,s,t,swap=False):
    # product over p|q of [(1-u w)(1-v z)/((1-u z)(1-w v))]^{-1} (diagonal unramified correction)
    val=mp.mpf(1)
    AA,BB,SS,TT=(1-b,1-a,s,t) if swap else (a,b,s,t)
    for p in P:
        if p>q: break
        if q%p==0:
            u=mp.power(p,-AA); v=mp.power(p,-SS); w=mp.power(p,-BB); z=mp.power(p,-TT)
            val*=((1-u*w)*(1-v*z)/((1-u*z)*(1-w*v)))**(-1)
    return val
def X(q,w,e): return mp.power(q/mp.pi,mp.mpf(1)/2-w)*mp.gamma((1-w+e)/2)/mp.gamma((w+e)/2)
def chars_2e(e):
    # q=2^e, e>=3. primitive: j odd; parity m
    q=2**e; N=2**(e-2)
    return q,N
def L_vals_2e(e,u):
    q=2**e; N=2**(e-2)
    A=np.array([complex(mp.zeta(u,mp.mpf(5**k % q)/q)) for k in range(N)],dtype=np.complex128)
    B=np.array([complex(mp.zeta(u,mp.mpf((-5**k) % q)/q)) for k in range(N)],dtype=np.complex128)
    FA=np.fft.fft(A); FB=np.fft.fft(B)
    qfac=mp.power(q,-u)
    L0={j: complex(qfac)*(FA[j]+FB[j]) for j in range(N)}
    L1={j: complex(qfac)*(FA[j]-FB[j]) for j in range(N)}
    return L0,L1
def run_2e(e,a,b,s,t):
    q=2**e
    La0,La1=L_vals_2e(e,a); Lb0,Lb1=L_vals_2e(e,b); Ls0,Ls1=L_vals_2e(e,s); Lt0,Lt1=L_vals_2e(e,t)
    N=2**(e-2)
    tot=0j
    for m in (0,1):
        Lam=La1 if m else La0; Lbm=Lb1 if m else Lb0
        Lsm=Ls1 if m else Ls0; Ltm=Lt1 if m else Lt0
        for j in range(1,N,2):
            chi_vals=None
            tot+=Lam[j]*Lbm[N-j]/(Lsm[j]*Ltm[N-j])
    ph=N  # 2^{e-3} odd j times 2 parities = 2^{e-2}
    Me={0:N//2,1:N//2}
    def M(a,b,s,t,unram=False,swapunram=False):
        Z=Zq(q,a,b,s,t); Zw=Zq(q,1-b,1-a,s,t)
        if unram: Z*=ramfactor(q,a,b,s,t)
        if swapunram: Zw*=ramfactor(q,a,b,s,t,swap=True)
        Hq=sum(Me[e_]*X(q,a,e_)*X(q,b,e_) for e_ in (0,1))
        return ph*Z+Hq*Zw
    return tot,ph,Me,M
if __name__=="__main__":
    tests=[("crit", mp.mpf(1)/2+0.3*I, mp.mpf(1)/2+0.4*I, mp.mpf(6)/10+0.2*I, mp.mpf(6)/10+0.5*I)]
    for e in [6,7,8,9]:
        for nm,a,b,s,t in tests:
            R,ph,Me,Mfn=run_2e(e,a,b,s,t)
            q=2**e
            MA=Mfn(a,b,s,t)
            MB=Mfn(a,b,s,t,unram=True)
            MB2=Mfn(a,b,s,t,unram=True,swapunram=True)
            print(f"q=2^{e}={q} {nm}: phi*={ph} R={mp.nstr(mp.mpc(R.real,R.imag),9)}")
            for tag,Val in [("GWX",MA),("unram",MB),("unram+swapunram",MB2)]:
                print(f"   {tag:16s}: M={mp.nstr(Val,9)} |res|={mp.nstr(abs(mp.mpc(R.real,R.imag)-Val),5)} |res|/sqrt(q)={mp.nstr(abs(mp.mpc(R.real,R.imag)-Val)/mp.sqrt(q),4)} |res|/phi(q/p)={mp.nstr(abs(mp.mpc(R.real,R.imag)-Val)/(ph/2),4)}")
