import numpy as np, mpmath as mp
mp.mp.dps = 30
def primes_upto(n):
    sieve = np.ones(n+1, dtype=bool); sieve[:2]=False
    for p in range(2,int(n**0.5)+1):
        if sieve[p]: sieve[p*p::p]=False
    return np.nonzero(sieve)[0]
PM=10**7
pr = primes_upto(PM)
po = pr[pr>2].astype(np.float64); lp=np.log(po)

def brutelogP(w):
    # sum over p>2 of log(1+p^{-w}/(p-2)), direct + tail via expansion
    w=float(w)
    x = np.exp(-w*lp)/(po-2.0)
    head = np.sum(np.log1p(x))
    # tail: sum_{p>PM} [p^{-w}/(p-2) - x^2/2 + ...] ; leading = sum p^{-1-w} tail
    # E1-style: tail of sum_{p>PM} p^{-1-w}
    eps=w
    # asymptotic tail of sum_{p>PM} p^{-1-w} ~ E1(eps*log PM)
    tail = float(mp.e1(eps*np.log(PM))) if eps>0 else None
    # correction because p^{-w}/(p-2) ~ p^{-1-w}(1+2/p); negligible relative
    return head+tail

for w in [0.02,0.005,0.002]:
    lp_=brutelogP(w)
    print("w=",w," direct logP=",lp_, " -> wP=",w*np.exp(lp_))

# analytic constants
M = 0.2614972128476427837554268386086958590516  # Mertens (Meissel-Mertens)
gam = 0.57721566490153286060651209008240243104215933593992
K1 = 2*np.sum(1/(po*(po-2))) + 2*float(mp.e1(np.log(PM)))  # tail approx of sum 1/(n(n-2)) over primes? use integral
K1 = 2*np.sum(1/(po*(po-2)))
# tail for sum_{p>PM}2/(p(p-2)) ~ 2/(PM log PM)
K1 += 2/(PM*np.log(PM))
K3 = np.sum(np.log1p(1/(po-2)) - 1/(po-2))
K3 += -0.5/(PM*np.log(PM))  # rough tail
print("K1=",K1," K3=",K3)
logc = (M-gam) - 0.5 + K1 + K3
print("analytic log c2=",logc," c2=",np.exp(logc))
C2=1.0
for p in po: C2 *= (1-1/(p-1)**2)
print("2*C2*c2 =",2*C2*np.exp(logc), " c2*2C2 target?")
