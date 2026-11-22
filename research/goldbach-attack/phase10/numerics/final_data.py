import sys, numpy as np, json
sys.path.insert(0,'.')
from test_mq import compute
from charlib import CharGroup, factorize
from mainterm import Xqe, zeta_q, Aprod
from mpmath import mp
mp.dps=25

qs=[53,97,107,211,307,503,1009,2003, 60,84,105,120,140,165,360,420,720,900,1000,1008,1260,1680,2000]
imgs=[(1.0,0.5,0.5,1.0),(1.5,-0.5,0.5,-1.5),(0.8,0.3,-0.7,0.6),(-1.0,0.5,0.5,-1.0),(0.4,1.2,-0.6,1.8),(1.8,0.2,-1.4,0.9)]
rows=[]
for q in qs:
    cg=CharGroup(q); fac=factorize(q); cache={}
    if cg.n==0:
        rows.append(dict(q=q,n=0,note='no primitive chars (v2(q)=1)')); continue
    for eta in (0.1,0.2):
        for (A,B,S,T) in imgs:
            a=complex(0.5,A); b=complex(0.5,B); s=complex(0.5+eta,S); t=complex(0.5+eta,T)
            r=compute(q,a,b,s,t,cg,fac,cache)
            M0,M1=cg.counts()
            def Zfun(x,y,c,d):
                return zeta_q(x+y,q,fac,cache)*zeta_q(c+d,q,fac,cache)/(zeta_q(x+d,q,fac,cache)*zeta_q(y+c,q,fac,cache))*Aprod(x,y,c,d,q)
            Zv=Zfun(a,b,s,t); Zdv=Zfun(1-b,1-a,s,t)
            pieces=[complex((M0 if e==0 else M1)*(Zv + Xqe(q,e,a)*Xqe(q,e,b)*Zdv)) for e in (0,1)]
            rec=dict(q=q,isprime=None,eta=eta,imgs=(A,B,S,T),n=cg.n,counts=[M0,M1],
                     E=[float(r['E'].real),float(r['E'].imag)],
                     Ee=[[float(x.real),float(x.imag)] for x in r['Ee']],
                     pieces=[[float(x.real),float(x.imag)] for x in pieces])
            for tag in ('std_Xab','std_X1m','swap_Xab','swap_X1m'):
                M=r[tag]['M']
                rec[tag]={'M':[float(M.real),float(M.imag)] if not isinstance(M,complex) else [M.real,M.imag],
                          'abs':float(abs(r['E']-M)),'rel':float(abs(r['E']-M)/max(1e-12,abs(M)))}
            rows.append(rec)
    print("done q",q,flush=True)
json.dump(rows,open('cache/final_data.json','w'),indent=0)
print("saved",len(rows))
