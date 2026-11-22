import numpy as np, mpmath as mp
# Verify: M2(sigma) = int_R |D_N(sigma+iu)|^2/(4+u^2) du  ~ C/sigma^3
def primes_upto(n):
    sieve=np.ones(n+1,dtype=bool); sieve[:2]=False
    for p in range(2,int(n**0.5)+1):
        if sieve[p]: sieve[p*p::p]=False
    return np.nonzero(sieve)[0]
pr=primes_upto(2*10**6); coef=(np.log(pr)**2)  # Lambda(p)^2
us=np.concatenate([np.linspace(0,2,401)[1:], np.linspace(2,200,2000)])
for sig in [0.2,0.1,0.05,0.02,0.01]:
    # D_N(sigma+iu) = sum_p (log p)^2 p^{-1-sigma-iu}/(1-p^{-1-sigma-iu})  ; approximate (n=N excluded - use N=30030)
    N=30030; mask=(N%pr!=0)
    pp=pr[mask].astype(np.float64); c=mask.sum()*0+ (np.log(pp)**2)
    vals=np.zeros_like(us,dtype=complex)
    for i,u in enumerate(us):
        pw=pp**(-1-sig-1j*u)
        vals[i]=np.sum(c*pw/(1-pw))
    # tail correction: sum p^{-1-sigma} over p>2e6 tail ~ E1; but D_N ~ 1/sigma^2, tail of |D|^2 dominated by small u; skip (small u sum over primes<=2e6 accounts most)
    integ=2*np.trapezoid((np.abs(vals)**2)/(4+us**2),us)
    print(f"sigma={sig:7.4f}  M2={integ:.6e}   M2*sigma^3={integ*sig**3:.6f}")
