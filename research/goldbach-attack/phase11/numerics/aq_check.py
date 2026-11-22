import sys, numpy as np, mpmath as mp, time
mp.mp.dps=35
PR=np.load('primes_2000000.npy'); PR=PR[PR<=1000000]
a=complex(0.5,0.3); b=complex(0.5,0.7); s=complex(0.6,0.4); t=complex(0.6,0.9)
x,y,c,d=a,b,s,t
# numpy product (as in phase10 Aprod)
mask=(PR%2!=0); p=PR[mask].astype(float); lp=np.log(p)
X=np.exp(-(x+d)*lp); Y=np.exp(-(y+c)*lp); G=np.exp(-(c+d)*lp)
f=((1-G)*(1-X-Y+G))/((1-X)*(1-Y))
Anp=np.exp(np.sum(np.log1p(f-1.0)))
# mpmath product over same primes
t0=time.time(); mp.mp.dps=30
prod=mp.mpf(1)
for p_ in PR[mask]:
    p=int(p_)
    num=(1-mp.power(p,-(c+d)))*(1-mp.power(p,-(x+d))-mp.power(p,-(y+c))+mp.power(p,-(c+d)))
    den=(1-mp.power(p,-(x+d)))*(1-mp.power(p,-(y+c)))
    prod*=num/den
Am=complex(prod)
print("A_np=",Anp," A_mp=",Am," rel diff=",abs(Anp-Am)/abs(Am)," wall",time.time()-t0)
# also check phase10 Aprod directly
sys.path.insert(0,'../../phase10/numerics')
from mainterm import Aprod
print("phase10 Aprod:",Aprod(x,y,c,d,2**14))
