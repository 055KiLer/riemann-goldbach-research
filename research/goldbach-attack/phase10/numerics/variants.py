"""Test 4 variants of E (with/without conjugate) x H (X(a)X(b) vs X(1-b)X(1-a))."""
import numpy as np, mpmath as mp, sys, time, json
sys.path.insert(0,'.')
mp.mp.dps=25
from charlib import CharGroup, factorize
from mainterm import Lvals, zqa, zeta_q, Aprod, Xqe

def eval_variants(q,a,b,s,t,cg,fac,cache):
    La=Lvals(a,q,cg,cache); Lb=Lvals(b,q,cg,cache)
    Ls=Lvals(s,q,cg,cache); Lt=Lvals(t,q,cg,cache)
    Vc=cg.V.conj()
    def Lv_conj(u):
        z=zqa(u,q,cg.units,cache)
        return (Vc@z)*complex(q**(-complex(u)))
    LbB=Lv_conj(b); LtB=Lv_conj(t)
    E0=complex(np.sum(La*Lb/(Ls*Lt)))
    E1=complex(np.sum(La*LbB/(Ls*LtB)))
    M0,M1=cg.counts(); phist=M0+M1
    def Zq(x,y,c,d):
        return zeta_q(x+y,q,fac,cache)*zeta_q(c+d,q,fac,cache)/(zeta_q(x+d,q,fac,cache)*zeta_q(y+c,q,fac,cache))*Aprod(x,y,c,d,q)
    Z=Zq(a,b,s,t); Zd=Zq(1-b,1-a,s,t)
    def Hform(e,args): 
        return (M0 if e==0 else M1)*Xqe(q,e,args[0])*Xqe(q,e,args[1])
    HA=sum(Hform(e,(a,b)) for e in (0,1))
    HB=sum(Hform(e,(1-b,1-a)) for e in (0,1))
    MA=phist*Z+HA*Zd; MB=phist*Z+HB*Zd
    return dict(E0=E0,E1=E1,MA=complex(MA),MB=complex(MB),Z=complex(Z),Zd=complex(Zd),HA=complex(HA),HB=complex(HB),phi=phist,counts=(M0,M1))

if __name__=='__main__':
    qs=[int(x) for x in sys.argv[1].split(',')]
    etas=[float(x) for x in sys.argv[2].split(',')]
    imgs=[(1.0,0.5,0.5,1.0),(-1.0,0.5,0.5,-1.0),(1.0,-0.5,-0.5,0.5),(0.5,1.0,-1.0,0.5),(1.5,-0.5,0.5,-1.5)]
    for q in qs:
        cg=CharGroup(q); fac=factorize(q); cache={}
        if cg.n==0: print(f"q={q}: no primitive chars"); continue
        print(f"### q={q} chars={cg.n}",flush=True)
        for eta in etas:
            for (A,B,S,T) in imgs:
                a=complex(0.5,A); b=complex(0.5,B); s=complex(0.5+eta,S); t=complex(0.5+eta,T)
                r=eval_variants(q,a,b,s,t,cg,fac,cache)
                errs={k:abs(r['E'+str(i)]-r[k])/max(1e-12,abs(r[k])) for i in (0,1) for k in ('MA','MB')}
                print(f"eta={eta} imgs={A,B,S,T}: rel E0-MA={errs['MA']:.4f} E0-MB={errs['MB']:.4f} E1-MA={errs['MA']:.4f} E1-MB={errs['MB']:.4f}   |E0|={abs(r['E0']):.3f} |E1|={abs(r['E1']):.3f} |MA|={abs(r['MA']):.3f} |MB|={abs(r['MB']):.3f}",flush=True)
