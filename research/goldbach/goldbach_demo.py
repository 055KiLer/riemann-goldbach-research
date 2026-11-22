#!/usr/bin/env python3
"""Empirical (evidence only) check of binary Goldbach + comet stats.
NOT a proof.  Runs: (A) full verification 4<=n<=10^7 even; (B) representation
counts r(n) for a 2001-wide window near 10^6."""
import time, math
t0 = time.time()
N = 10**7
print(f"[A] Sieve of Eratosthenes up to {N} ...", flush=True)
sieve = bytearray(b"\x01") * (N + 1)
sieve[0:2] = b"\x00\x00"
r = math.isqrt(N)
for i in range(2, r + 1):
    if sieve[i]:
        start = i * i
        sieve[start::i] = b"\x00" * (((N - start) // i) + 1)
primes = [i for i in range(2, N + 1) if sieve[i]]
print(f"    primes <= {N}: {len(primes)}  ({time.time()-t0:.1f}s)", flush=True)

# (A) verify every even n in [4,N]
P = sieve
fails = []           # (n, reason) if any
max_pmin = 0         # largest minimal Goldbach prime seen
max_pmin_n = 0
record_list = []     # record-setting minimal prime values
for n in range(4, N + 1, 2):
    found = False
    pmin = 0
    for p in primes:
        if p > n // 2:
            break
        if P[n - p]:
            found = True
            pmin = p
            break
    if pmin > max_pmin:
        max_pmin = pmin
        max_pmin_n = n
        record_list.append((n, pmin))
    if not found:
        fails.append(n)
print(f"[A] verified even n in [4,{N}]: failures={len(fails)}  ({time.time()-t0:.1f}s)")
print(f"    largest minimal Goldbach prime p_min up to {N}: {max_pmin} (first at n={max_pmin_n})")
print(f"    record minima (n,p_min): {record_list}")

# (B) reps r(n) = #{p<=n/2: n-p prime} for window near 10^6
try:
    import numpy as np
    lo, hi = 10**6, 10**6 + 4000
    ns = np.arange(lo, hi + 1, 2)
    rcount = np.zeros(len(ns), dtype=np.int32)
    Parr = np.frombuffer(sieve, dtype=np.uint8)
    for p in primes:
        if 2 * p > hi:
            break
        mask = ns >= 2 * p
        rcount[mask] += Parr[ns[mask] - p]
    print(f"[B] window [{lo},{hi}]: evens={len(ns)} min r(n)={rcount.min()} max={rcount.max()} mean={rcount.mean():.2f}")
    print(f"    #n with r(n)=1: {(rcount==1).sum()}  #n with r(n)<=2: {(rcount<=2).sum()}")
    q = np.percentile(rcount, [0, 25, 50, 75, 100])
    print(f"    r(n) min/25%/median/75%/max = {q[0]:.0f}/{q[1]:.0f}/{q[2]:.0f}/{q[3]:.0f}/{q[4]:.0f}")
    print(f"    #n with r(n)=1: {(rcount==1).sum()}   #n with r(n)<=2: {(rcount<=2).sum()}   min r(n) over window: {rcount.min()}")
except ImportError:
    print("[B] numpy not available, skipped")
print(f"total {time.time()-t0:.1f}s")
