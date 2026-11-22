import numpy as np, sys
sys.path.insert(0,'.')
from fastpipe import factorize
def is_prime(n):
    if n<2: return False
    for q in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n%q==0: return n==q
    d=n-1; s=0
    while d%2==0: d//=2; s+=1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37):
        x=pow(a,d,n)
        if x in (1,n-1): continue
        for _ in range(s-1):
            x=x*x%n
            if x==n-1: break
        else: return False
    return True
def smooth(n,pr=(2,3,5,7,11,13,17,19,23,29)):
    for q in pr:
        while n%q==0: n//=q
    return n==1
targets=[1000,3000,10000,30000,100000,200000,400000,700000,1000000]
found={}
# generate smooth n=p-1 (n even; actually n=p-1 even for odd p) in [800,1.3e6]
res=[]
for n in range(800,1300002,2):
    if smooth(n):
        p=n+1
        if is_prime(p): res.append(p)
res=sorted(set(res))
for t in targets:
    best=min(res,key=lambda p:abs(np.log(p)-np.log(t)))
    found[t]=best
print("smooth primes:",found)
print("all:",[p for p in res if p<=1300000])
