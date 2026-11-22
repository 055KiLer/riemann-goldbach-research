"""Verify the phase-10 A_q mask bug: compare corrected A_q (exclude p|q) with buggy mask (exclude only q|p, i.e. p==q for q>p).
Compute E_q (mpmath Hurwitz, corrected - E does not involve A_q) and M_q under both masks for q=60,120,720,1000,2000."""
import sys, math, json
sys.path.insert(0,'.')
import ramified as R
from group import Grp, factorize
import numpy as np, mpmath as mp
from multiprocessing import Pool
mp.mp.dps=30
def Aq_mask(a,b,c,d,q,mode):
    a,b,c,d=complex(a),complex(b),complex(c),complex(d)
    if mode=='correct':
        mask=(q%R.PRIMES)!=0       # p ∤ q
    else:
        mask=(R.PRIMES%q)!=0       # BUG of phase-10: keeps primes p|q
    lp=R.PL[mask]; P=R.PD[mask]
    X=np.exp(-(a+d)*lp); Y=np.exp(-(b+c)*lp); Z=np.exp(-(c+d)*lp)
    Rv=(1-Z)*(1-X-Y+Z)/((1-X)*(1-Y))
    return complex(np.exp(np.sum(np.log(Rv))))
def Mq_mask(a,b,s,t,q,ph,Me,mode):
    c,d=s,t
    def Zq(aa,bb):
        return R.zeta_q(aa+bb,q)*R.zeta_q(c+d,q)/(R.zeta_q(aa+d,q)*R.zeta_q(bb+c,q))*Aq_mask(aa,bb,c,d,q,mode)
    H=sum(Me[e]*R.Xqe(a,e,q)*R.Xqe(b,e,q) for e in (0,1) if Me[e])
    return ph*Zq(a,b)+H*Zq(1-b,1-a)
if __name__=='__main__':
    shifts=[(0.7,1.3,0.4,2.1),(-1.3,0.6,1.2,-0.7),(2.1,-0.9,0.5,1.8),(-0.4,-1.7,-1.2,0.9)]
    out=[]
    with Pool(8) as pool:
        for q in [60,120,720,1000,2000]:
            g=Grp(q)
            rows=[]
            for (ia,ib,is_,it_) in shifts:
                a=mp.mpc(0.5,ia); b=mp.mpc(0.5,ib); s=mp.mpc(0.6,is_); t=mp.mpc(0.6,it_)
                Eq,ok=R.E_of(g,a,b,s,t,pool)
                Mc=Mq_mask(a,b,s,t,q,g.phistar,g.Me,'correct')
                Mb=Mq_mask(a,b,s,t,q,g.phistar,g.Me,'buggy')
                rows.append(dict(ia=ia,ib=ib,correct=float(abs(mp.mpc(Eq)-Mc)),buggy=float(abs(mp.mpc(Eq)-Mb)),
                                 absEq=abs(Eq),absMc=float(abs(Mc)),absMb=float(abs(Mb))))
            med_c=float(np.median([r['correct'] for r in rows])); med_b=float(np.median([r['buggy'] for r in rows]))
            out.append(dict(q=q,phi_star=g.phistar,med_correct=med_c,med_buggy=med_b,ratio=med_b/med_c if med_c>0 else None))
            print(f"q={q:5d} phi*={g.phistar:4d}  median|E-M_correct|={med_c:10.4g}   median|E-M_buggy|={med_b:10.4g}   buggy/correct={med_b/med_c if med_c else None:8.2f}",flush=True)
    json.dump(out,open('../logs/mask_compare.json','w'),indent=1)
