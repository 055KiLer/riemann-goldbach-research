import numpy as np, mpmath as mp
mp.mp.dps = 30

# prime sieve up to PM
def primes_upto(n):
    sieve = np.ones(n+1, dtype=bool); sieve[:2]=False
    for p in range(2,int(n**0.5)+1):
        if sieve[p]: sieve[p*p::p]=False
    return np.nonzero(sieve)[0]

PM = 10**7
pr = primes_upto(PM)
# exclude 2
pr_odd = pr[pr>2].astype(np.float64)
logpr = np.log(pr_odd)

# g(s) = sum_p p^{-s} via g(s) = log zeta(s) - sum_{k>=2} g(ks)/k, iterated for k up to Kmax
def g_p(s):
    # direct sum over primes up to PM plus tail estimate; for Re s>=1.5 this is accurate
    s = mp.mpf(s)
    tot = mp.fsum([mp.exp(-s*mp.log(p)) for p in pr[:200000]]) if False else None
    # vectorized: sum over all primes <= PM, tail ~ int_PM^inf t^{-s}/log t dt ~ PM^{1-s}/((s-1)log PM)
    h = np.exp(-float(s)*logpr)
    head = float(np.sum(np.exp(-float(s)*logpr)))
    tail = PM**(1-float(s))/((float(s)-1)*np.log(PM))
    return mp.mpf(head+tail)

def g(s):
    # g(s)=sum_p p^{-s}, Re s > 1
    K = 40
    tot = mp.mpf(0)
    for k in range(1,K+1):
        tot += mp.log(mp.zeta(s*k))/k if k==1 else mp.mpf(0)
    # recursive: g(s) = log zeta(s) - sum_{k>=2} g(ks)/k. Approximate g(ks) by direct sum for ks>=2, negligible for large k
    corr = mp.mpf(0)
    for k in range(2,K+1):
        idxmax = np.searchsorted(pr, PM)
        x = np.exp(-float(s*k)*logpr)
        corr += float(np.sum(x))/k
        # tail
        sk = float(s*k)
        corr += (PM**(1-sk)/((sk-1)*np.log(PM)))/k
    return mp.log(mp.zeta(s)) - mp.mpf(corr)

def logP(w):
    """log P(w) = sum_{p>2} log(1+p^{-w}/(p-2)) for w complex small, via split terms"""
    w = mp.mpf(w)
    # S1 = sum_{p>2} p^{-w}/(p-2) = sum_{p>2}p^{-1-w} + 2 sum_{p>2} p^{-w}/(p(p-2))
    # term A: sum_{p>2} p^{-1-w} = g(1+w) - 2^{-1-w}
    A = g(1+w) - mp.power(2, -1-w)
    # term B: 2 sum_{p>2} p^{-w}/(p(p-2))
    B = 2*mp.fsum([mp.power(mp.mpf(p), -w)/(mp.mpf(p)*(mp.mpf(p)-2)) for p in pr_odd[:70000]])
    # tail for B: sum_{p>PM} p^{-w}/(p(p-2)) ~ int_PM^inf t^{-2-w}/log t dt  (negligible)
    B += 2*mp.mpf(PM)**(-1-w)/(mp.mpf(1+w)*mp.log(PM))
    K3 = mp.fsum([ mp.log(1+1/(mp.mpf(p)-2)) - 1/(mp.mpf(p)-2) for p in pr_odd[:70000]])
    # tail K3 ~ int_PM^inf [-1/(2(t-2)^2)+...]/log t dt
    K3 += -0.5*mp.mpf(PM)**(-1)/(mp.log(PM))
    # higher j terms (j>=2) of log expansion: sum_{j>=2} (-1)^{j+1}/j S_j; S_j ~ sum_{p>2} (p-2)^{-j}
    # we absorb: K3 already equals sum_{j>=2} (-1)^{j+1}/j sum (p-2)^{-j}
    # but w-dependence at first order: -jw log p; leading correction O(w) -> we compute at finite w
    return A + B + K3

def c2_scaled(w):
    return w*mp.e**logP(w)

for w in [mp.mpf('0.02'), mp.mpf('0.008'), mp.mpf('0.004'), mp.mpf('0.002')]:
    cw = c2_scaled(w)
    print("w=",w," wP(w)=", mp.nstr(cw,12))
C2 = mp.mpf(1)
# C2 = prod_{p>2}(1-1/(p-1)^2)
C2 = mp.fsum([0]) 
val = mp.mpf(1)
for p in pr_odd[:70000]:
    val *= (1-1/((mp.mpf(p)-1)**2))
print("C2 approx:", mp.nstr(val,15), " 2C2=", mp.nstr(2*val,15), " 1/(2C2)=", mp.nstr(1/(2*val),15))
