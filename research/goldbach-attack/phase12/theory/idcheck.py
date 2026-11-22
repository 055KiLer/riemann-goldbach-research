import numpy as np, mpmath as mp
mp.mp.dps=18
def mobius(n):
    mu=np.zeros(n+1,dtype=np.int64); pr=[]; isc=np.zeros(n+1,dtype=bool); mu[1]=1
    for i in range(2,n+1):
        if not isc[i]: pr.append(i); mu[i]=-1
        for p in pr:
            if i*p>n: break
            isc[i*p]=True
            if i%p==0: mu[i*p]=0; break
            else: mu[i*p]=-mu[i]
    return mu
def build(X,u,v,eta=0.2):
    sig=0.5+eta; a=mp.mpc(sig,u); s=mp.mpc(sig,v)
    Y=X*X; mu=mobius(X); c=np.zeros(Y+1,dtype=np.complex128)
    nv=np.array([complex(mp.power(n,-a)) for n in range(1,X+1)])
    for r in range(1,X+1):
        if mu[r]==0: continue
        w=complex(mp.power(r,-s))*mu[r]; nn=min(X,Y//r)
        c[r*np.arange(1,nn+1)] += w*nv[:nn]
    return c
q=7;X=19
c=build(X,0.7,0.2); d=build(X,1.1,0.4)
Y=X*X; A=np.arange(1,Y+1); idx=A%q
Sc=np.zeros(q,dtype=np.complex128); Sd=np.zeros(q,dtype=np.complex128)
np.add.at(Sc,idx,c[1:]); np.add.at(Sd,idx,d[1:])
D=np.vdot(d[1:],c[1:])
Sb=np.dot(Sc,np.conj(Sd))     # sum_{A=B mod q} c_A conj(d_B)
E=(q-1)*Sb-np.vdot(d[1:],c[1:])   # placeholder
Scall=Sc.sum(); Sdall=Sd.sum(); Sc0=Sc[0]; Sd0=Sd[0]
# E^X exact (coprime restriction ignored; coefficients have no q support issue?) 
Eex=(q-1)*Sb - Scall*np.conj(Sdall)   # (q-1)sum_{A=B}-sum_all  [E^X formula w/o coprime subtleties]
W=Sb-D
T=Sc0*Sdall+Scall*Sd0-Sc0*Sd0
term_pT=(q-1)*(D+W)-Scall*np.conj(Sdall)+T
term_mT=(q-1)*(D+W)-Scall*np.conj(Sdall)-(q-2)*T
print("Eex=",Eex)
print("+T  =",term_pT)
print("-（q-2)T=",term_mT)
print("D,W,T,Sc,Sd:",D,W,T,Scall,Sdall)
