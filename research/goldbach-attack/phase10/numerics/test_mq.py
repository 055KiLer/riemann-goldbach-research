"""Test E_q (barred, primitive) against main-term variants at composite q."""
import numpy as np, mpmath as mp, sys, json, time
sys.path.insert(0,'.')
mp.mp.dps=25
from charlib import CharGroup, factorize
from mainterm import zqa, zeta_q, Aprod, Xqe

def Lval(u,vec,q,units,cache):
    z=zqa(u,q,units,cache)
    return complex(q**(-complex(u)))*(vec@z)

def compute(q,a,b,s,t,cg,fac,cache):
    V=cg.V; Vb=cg.V.conj()
    def L(v): return Lval(v,V,q,cg.units,cache)
    def Lb(v): return Lval(v,Vb,q,cg.units,cache)
    La, Lb_, Ls, Lt = L(a), Lb(b), L(s), Lb(t)
    terms=La*Lb_/(Ls*Lt)
    E=complex(np.sum(terms))
    Ee=[complex(np.sum(terms[np.array(cg.parity)==e])) for e in (0,1)]
    M0,M1=cg.counts(); phist=M0+M1
    def Zq(x,y,c,d,swap=False):
        if swap:
            return zeta_q(x+y,q,fac,cache)*zeta_q(c+d,q,fac,cache)/(zeta_q(x+c,q,fac,cache)*zeta_q(y+d,q,fac,cache))*Aprod(x,y,d,c,q)
        return zeta_q(x+y,q,fac,cache)*zeta_q(c+d,q,fac,cache)/(zeta_q(x+d,q,fac,cache)*zeta_q(y+c,q,fac,cache))*Aprod(x,y,c,d,q)
    res={}
    for swap in (False,True):
        Z=Zq(a,b,s,t,swap); Zd=Zq(1-b,1-a,s,t,swap)
        for Hname,args in (('Xab',(a,b)),('X1m',(1-b,1-a))):
            H=sum((M0 if e==0 else M1)*Xqe(q,e,args[0])*Xqe(q,e,args[1]) for e in (0,1))
            M=phist*Z+H*Zd
            Me=[(M0 if e==0 else M1)*(Z + Xqe(q,e,args[0])*Xqe(q,e,args[1])*Zd) for e in (0,1)]
            tag=('swap' if swap else 'std')+'_'+Hname
            res[tag]=dict(M=complex(M),Me=[complex(Me[0]),complex(Me[1])])
    return dict(E=E,Ee=Ee,**{k:v for k,v in res.items()},phi=phist,counts=(M0,M1))

if __name__=='__main__':
    qs=[int(x) for x in sys.argv[1].split(',')]
    etas=[float(x) for x in sys.argv[2].split(',')]
    imgs=[(1.0,0.5,0.5,1.0),(-1.0,0.5,0.5,-1.0),(1.0,-0.5,-0.5,0.5),(0.5,1.0,-1.0,0.5),(1.5,-0.5,0.5,-1.5),(0.8,0.3,-0.7,0.6)]
    out=[]
    for q in qs:
        cg=CharGroup(q); fac=factorize(q); cache={}
        if cg.n==0:
            print(f"q={q}: NO primitive chars (conductor q impossible: v2(q)=1)",flush=True); continue
        rows=[]
        for eta in etas:
            for (A,B,S,T) in imgs:
                a=complex(0.5,A); b=complex(0.5,B); s=complex(0.5+eta,S); t=complex(0.5+eta,T)
                r=compute(q,a,b,s,t,cg,fac,cache)
                rec=dict(q=q,eta=eta,imgs=(A,B,S,T))
                for tag in ('std_Xab','std_X1m','swap_Xab','swap_X1m'):
                    M=r[tag]['M']; rec[tag+'_rel']=float(abs(r['E']-M)/max(1e-12,abs(M)))
                    rec[tag+'_scaled']=float(abs(r['E']-M)/np.sqrt(q))
                # parity resolved under best-guess variants
                for tag in ('std_X1m','swap_X1m','std_Xab'):
                    Me=r[tag]['Me']
                    rec[tag+'_par0_rel']=float(abs(r['Ee'][0]-Me[0])/max(1e-12,abs(Me[0])))
                    rec[tag+'_par1_rel']=float(abs(r['Ee'][1]-Me[1])/max(1e-12,abs(Me[1])))
                rec['E']=[float(r['E'].real),float(r['E'].imag)]
                rec['Ee']=[[float(x.real),float(x.imag)] for x in r['Ee']]
                rows.append(rec); out.append(rec)
        # summary for q
        print(f"### q={q} chars={cg.n} counts={cg.counts()}",flush=True)
        for tag in ('std_Xab','std_X1m','swap_Xab','swap_X1m'):
            rels=[r[tag+'_rel'] for r in rows]
            print(f"  {tag}: rel median={np.median(rels):.3f} mean={np.mean(rels):.3f} max={np.max(rels):.3f}",flush=True)
        for tag in ('std_X1m','swap_X1m','std_Xab'):
            p0=[r[tag+'_par0_rel'] for r in rows]; p1=[r[tag+'_par1_rel'] for r in rows]
            print(f"  parity {tag}: even rel mean={np.mean(p0):.3f} max={np.max(p0):.3f} | odd rel mean={np.mean(p1):.3f} max={np.max(p1):.3f}",flush=True)
    with open('cache/mq_results.jsonl','a') as f:
        for r in out: f.write(json.dumps(r)+'\n')
