"""Find primes p in target windows with p=3 mod 4 and p-1 smooth (for fast FFT)."""
import sys

def is_prime(n):
    if n < 2: return False
    for q in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n % q == 0: return n == q
    d = n-1; s = 0
    while d % 2 == 0: d//=2; s+=1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37):
        x = pow(a,d,n)
        if x in (1, n-1): continue
        for _ in range(s-1):
            x = x*x % n
            if x == n-1: break
        else:
            return False
    return True

def smooth_numbers(maxprime, limit):
    """all products of primes<=maxprime up to limit, as dict n->factor list"""
    primes=[q for q in (2,3,5,7,11,13,17,19) if q<=maxprime]
    out={}
    def rec(i, cur, fac):
        if i==len(primes):
            if cur not in out or len(fac)<len(out[cur]): out[cur]=tuple(fac)
            return
        p=primes[i]
        v=cur; k=0
        while v<=limit:
            rec(i+1, v, fac+([p]*k))
            v*=p; k+=1
    rec(0,1,[])
    return out

if __name__=='__main__':
    windows=[(2.9e5,3.05e5),(4.9e5,5.05e5),(9.9e5,1.01e6),(1.99e6,2.01e6)]
    sm=smooth_numbers(19, 2_100_000)
    print("smooth count",len(sm))
    for lo,hi in windows:
        best=[]
        for n in sm:
            if lo<=n+1<=hi:
                p=n+1
                if p%4==3 and is_prime(p):
                    best.append((len(sm[n]), max(sm[n]), abs(p-(lo+hi)/2), p, sm[n]))
        best.sort()
        print(f"window {lo:.2e}-{hi:.2e}: found {len(best)}")
        for b in best[:6]:
            print("   p=",b[3],"p-1=",b[4],"omega_deg=",b[0],"maxprime=",b[1])
