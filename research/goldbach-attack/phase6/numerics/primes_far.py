"""Find primes p≈targets with p=3 mod 4 and p-1 smooth (fast FFT over (Z/p)^*)."""
import sys
sys.path.insert(0,'/home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase5/numerics')
from primes_search import is_prime

def smooth_numbers(primes, limit):
    out=set()
    def rec(i,cur):
        if i==len(primes):
            out.add(cur); return
        p=primes[i]; v=cur
        while v<=limit:
            rec(i+1,v); v*=p
    rec(0,1); return out

def find(target, window, maxprime=19):
    lo,hi=target*(1-window), target*(1+window)
    primes=[q for q in (2,3,5,7,11,13,17,19,23) if q<=maxprime]
    limit=int(hi)+2
    sm=smooth_numbers(primes, limit)
    cand=[]
    for n in sm:
        p=n+1
        if lo<=p<=hi and p%4==3 and is_prime(p):
            cand.append((abs(p-target),p,n,primes))
    cand.sort()
    return cand[:8]

if __name__=='__main__':
    for target,window in [(1e7,0.15),(3e7,0.15)]:
        print(f"=== target N=2p with p~{target/2:.2e}, N~{target:.2e}")
        res=find(target/2, window)
        for d,p,n,pr in res[:6]:
            print(f"  p={p} (p-1 smooth over {pr}) N=2p={2*p} p%4={p%4}")
