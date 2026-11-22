import sys, numpy as np
sys.path.insert(0,'.')
from test_mq import compute
from charlib import CharGroup, factorize
qs=[60,84,105,120,140,1000,107,211,503]
imgs=[(1.0,0.5,0.5,1.0),(1.5,-0.5,0.5,-1.5),(0.8,0.3,-0.7,0.6),(-1.0,0.5,0.5,-1.0)]
out=[]
for q in qs:
    cg=CharGroup(q); fac=factorize(q); cache={}
    if cg.n==0: continue
    print(f"### q={q} chars={cg.n} counts={cg.counts()}",flush=True)
    agg={k:[] for k in ['even_vs_Me','odd_vs_Me','even_vs_Mswap','odd_vs_Mswap','E_vs_noH','E_vs_phiHalf']}
    for (A,B,S,T) in imgs:
        a=complex(0.5,A); b=complex(0.5,B); s=complex(0.6,S); t=complex(0.6,T)
        r=compute(q,a,b,s,t,cg,fac,cache)
        E=r['E']; Ee=r['Ee']
        Me=r['std_Xab']['Me']
        Z=r['std_Xab'].get('Z'); Zrev=r['std_Xab'].get('Zd')
        # recompute pieces (compute() does not return Z/Zd; patch via M pieces difference): 
        # we have Me; reconstruct diag part: Mdiag_e = Me_e - H_e*Zd. Instead recompute with X directly:
        from mainterm import Xqe, zeta_q, Aprod
        M0,M1=cg.counts()
        def Zfun(x,y,c,d):
            return zeta_q(x+y,q,fac,cache)*zeta_q(c+d,q,fac,cache)/(zeta_q(x+d,q,fac,cache)*zeta_q(y+c,q,fac,cache))*Aprod(x,y,c,d,q)
        Zv=Zfun(a,b,s,t); Zdv=Zfun(1-b,1-a,s,t)
        D=[ (M0 if e==0 else M1)*Zv for e in (0,1)]
        H=[ (M0 if e==0 else M1)*Xqe(q,e,a)*Xqe(q,e,b)*Zdv for e in (0,1)]
        Mm=[complex(D[e]+H[e]) for e in (0,1)]
        agg['even_vs_Me'].append(abs(Ee[0]-Mm[0])/abs(Mm[0]))
        agg['odd_vs_Me'].append(abs(Ee[1]-Mm[1])/abs(Mm[1]))
        agg['even_vs_Mswap'].append(abs(Ee[0]-Mm[1])/abs(Mm[1]))
        agg['odd_vs_Mswap'].append(abs(Ee[1]-Mm[0])/abs(Mm[0]))
        phi=cg.n
        agg['E_vs_noH'].append(abs(E-complex(phi*Zv))/abs(complex(phi*Zv)))
        # wrong parity weights: use phi/2 each instead of M_e
        Hw=sum((phi/2)*(Xqe(q,e,a)*Xqe(q,e,b)) for e in (0,1))
        agg['E_vs_phiHalf'].append(abs(E-complex(phi*Zv+Hw*Zdv))/abs(complex(phi*Zv+Hw*Zdv)))
    print("  even vs M_e: mean=%.3f | odd vs M_e: mean=%.3f || swapped-parity: even=%.3f odd=%.3f || no-H: %.3f | phi/2-weights: %.3f"%(
        np.mean(agg['even_vs_Me']),np.mean(agg['odd_vs_Me']),np.mean(agg['even_vs_Mswap']),np.mean(agg['odd_vs_Mswap']),np.mean(agg['E_vs_noH']),np.mean(agg['E_vs_phiHalf'])),flush=True)
