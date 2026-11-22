"""Variant arbitration: compare canonical M_q vs no-H_q vs X(1-b)X(1-a) vs swapped Z_q denominator."""
import sys, mpmath as mp, numpy as np, math, json
sys.path.insert(0,'.')
import replicate as R
from charlib import UnitGroup, factorize
mp.mp.dps=30
def M_variants(a,b,s,t,q,phistar,Me,fac):
    c,d=s,t
    zq=lambda u: R.zeta_q(u,fac)
    def Zq(aa,bb,cc,dd,swap=False):
        if not swap:
            den=zq(aa+dd)*zq(bb+cc); num=zq(aa+bb)*zq(cc+dd)
        else:
            den=zq(aa+cc)*zq(bb+dd); num=zq(aa+bb)*zq(cc+dd)
        return num/den*R.Aq(aa,bb,cc,dd,q)
    Z1=Zq(a,b,c,d); Z2=Zq(1-b,1-a,c,d)
    H=R.Xqe(a,0,q)*R.Xqe(b,0,q)*Me[0]+R.Xqe(a,1,q)*R.Xqe(b,1,q)*Me[1]
    Hrev=R.Xqe(1-b,0,q)*R.Xqe(1-a,0,q)*Me[0]+R.Xqe(1-b,1,q)*R.Xqe(1-a,1,q)*Me[1]
    Zswap=Zq(a,b,c,d,swap=True); Z2swap=Zq(1-b,1-a,c,d,swap=True)
    return dict(canon=phistar*Z1+H*Z2, noH=phistar*Z1, Xrev=phistar*Z1+Hrev*Z2,
                Zswap=phistar*Zswap+H*Z2swap, onlyZ=phistar*Z1, full=phistar*Z1+H*Z2)
qs=[1001,2003]
sets=[(0.7,1.3,0.4,2.1),(2.6,-1.1,1.7,0.3),(-2.4,0.9,2.2,1.5)]
out=[]
for q in qs:
    g=UnitGroup(q); prim=g.prim; ph=g.phistar; Me=g.Me; fac=list(factorize(q).keys()); LQ=math.log(q)
    for eta in [0.1]:
        for (ia,ib,is_,it_) in sets:
            a=mp.mpc(0.5,ia); b=mp.mpc(0.5,ib); s=mp.mpc(0.5+eta,is_); t=mp.mpc(0.5+eta,it_)
            ba=R.zeta_vals(g,a,q); bb=R.zeta_vals(g,b,q); bs=R.zeta_vals(g,s,q); bt=R.zeta_vals(g,t,q)
            La=(g.T@ba)*np.exp(-complex(a)*LQ); Lb=(g.T.conj()@bb)*np.exp(-complex(b)*LQ)
            Ls=(g.T@bs)*np.exp(-complex(s)*LQ); Lt=(g.T.conj()@bt)*np.exp(-complex(t)*LQ)
            with np.errstate(all='ignore'):
                ok=prim & np.isfinite(Ls*Lt) & (np.abs(Ls*Lt)>1e-300)
                Eq=complex(np.sum((La*Lb/(Ls*Lt))[ok]))
            Vs=M_variants(a,b,s,t,q,ph,Me,fac)
            rec=dict(q=q,eta=eta,ia=ia,ib=ib)
            for k,v in Vs.items():
                rec[k]=float(abs(mp.mpc(Eq)-v)/math.sqrt(q))
            out.append(rec)
            print(f"q={q} set(ia={ia}) ratios: "+" ".join(f"{k}={rec[k]:8.3f}" for k in ['canon','noH','Xrev','Zswap']),flush=True)
json.dump(out,open('../logs/A_variants.json','w'),indent=1)
