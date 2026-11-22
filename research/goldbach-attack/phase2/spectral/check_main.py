import numpy as np
from math import log as mlog
N=30030
lam=np.zeros(N+1)
sieve=np.ones(N+1,bool); sieve[:2]=False
for p in range(2,int(N**0.5)+1):
    if sieve[p]: sieve[p*p::p]=False
for p in np.nonzero(sieve)[0]:
    pk=p
    while pk<=N: lam[pk]=mlog(p); pk*=p
n=np.arange(1,N); m=N-n
mask=np.gcd(n*m,N)==1
tot=np.sum(lam[n]*lam[m]*mask)
print("sum LambdaLambda (ordered) =",tot,"S*N=",5.121255301154594*N, "S*N/2=",5.121255301154594*N/2)
# integral weight version
def phi(u):
    x=6*u-3; out=np.zeros_like(u); mm=np.abs(x)<1
    out[mm]=np.exp(-1/(1-x[mm]**2)); return out
Phi=lambda u: np.sqrt(u)*phi(u)
cphi=0.02218102014083238
totw=np.sum(lam[n]*lam[m]*mask*Phi(n/N)*Phi(m/N))
print("weighted sum/N=",totw/N, " cphi*S=",cphi*5.121255301154594, " half",cphi*5.121255301154594/2)

# middle third unweighted
mask2 = mask & (n>=N/3) & (n<=2*N/3)
print("mid-third sum=",np.sum(lam[n]*lam[m]*mask2), " predicted S*N/3=",5.121255301154594*N/3)
# with weight exp bump, check integral of phi^2 via Monte Carlo-ish sum over pairs: sum over all n (not prime) of phi(n/N)^2 /N ~ cphi
nn=np.arange(1,N)
print("sum phi(n/N)^2/N =", np.sum(phi(nn/N)**2)/N)
