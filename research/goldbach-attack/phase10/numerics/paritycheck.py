import numpy as np, mpmath as mp, sys
sys.path.insert(0,'.')
mp.mp.dps=30
from charlib import CharGroup, factorize
q=5
cg=CharGroup(q); cache={}
from mainterm import Lvals, zqa
# all characters mod q: use cg.V (primitive) + principal; build full list incl principal
z0={}
def Lval(u, vec):
    z=zqa(u,q,cg.units,cache)
    return complex(q**(-complex(u)))*(vec@z)
V=cg.V.conj()  # barred char values: chi_bar(a)=conj(chi(a))
units=cg.units
# full set: principal + primitive
Vall=cg.V
Vallbar=V
def X(e,w):
    w=mp.mpc(w.real,w.imag)
    return mp.power(q/mp.pi, mp.mpf(1)/2-w)*mp.gamma((1-w+e)/2)/mp.gamma((w+e)/2)
eta=mp.mpf('0.05')
s=mp.mpc('0.5','0.0')+eta; t=mp.mpc('0.5','0.4')+eta
for (u,v) in [(mp.mpc('0.01','0.02'),mp.mpc('-0.01','0.03')),(mp.mpc('0.001','0.1'),mp.mpc('0.002','-0.05'))]:
    a=s+u; b=t+v
    def R(A,B):
        tot=0j
        for i in range(Vall.shape[0]):
            tot+=Lval(A,Vall[i])*Lval(B,Vallbar[i])/(Lval(s,Vall[i])*Lval(t,Vallbar[i]))
        return tot
    R0=R(a,b); Rv=R(1-b,1-a)
    h0=X(0,1-b)*X(0,1-a); h1=X(1,1-b)*X(1,1-a)
    rhs=(2*Rv-(h0+h1)*R0)/(h0-h1)
    # parity-weighted sum
    P=0j
    for i in range(Vall.shape[0]):
        par=cg.parity[i]
        val=Lval(a,Vall[i])*Lval(b,Vallbar[i])/(Lval(s,Vall[i])*Lval(t,Vallbar[i]))
        P+= (1 if par==0 else -1)*val
    print("u,v=",u,v,"P-rhs=",abs(P-complex(rhs))," scale",abs(P),flush=True)
