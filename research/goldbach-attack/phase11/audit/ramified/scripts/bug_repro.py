"""Quantify the phase-10 A_q mask bug: M_q(buggy) vs M_q(correct) for q=2^e shifts; test if |ΔM|~c·q/p reproduces the claimed anomaly."""
import sys, json, math, numpy as np, mpmath as mp
sys.path.insert(0,'.')
import ramified as R
from group import Grp, factorize
mp.mp.dps=25
def Aq_mask(a,b,c,d,q,mode):
    a,b,c,d=complex(a),complex(b),complex(c),complex(d)
    mask=(q%R.PRIMES)!=0 if mode=='correct' else (R.PRIMES%q)!=0
    lp=R.PL[mask]; P=R.PD[mask]
    X=np.exp(-(a+d)*lp); Y=np.exp(-(b+c)*lp); Z=np.exp(-(c+d)*lp)
    Rv=(1-Z)*(1-X-Y+Z)/((1-X)*(1-Y))
    return complex(np.exp(np.sum(np.log(Rv))))
def Mq(a,b,s,t,q,ph,Me,mode):
    c,d=s,t
    def Zq(aa,bb):
        return R.zeta_q(aa+bb,q)*R.zeta_q(c+d,q)/(R.zeta_q(aa+d,q)*R.zeta_q(bb+c,q))*Aq_mask(aa,bb,c,d,q,mode)
    H=sum(Me[e]*R.Xqe(a,e,q)*R.Xqe(b,e,q) for e in (0,1) if Me[e])
    return ph*Zq(a,b)+H*Zq(1-b,1-a)
res=json.load(open('../logs/ramified_results.json'))
out=[]
for rec in res:
    if rec['label']!='2^e': continue
    q=rec['q']; ph=rec['phi_star']; Me=rec['Me']
    rows=[r for r in rec['rows'] if r['cls']=='generic']
    arr=[]; arrsqrt=[]; arrqp=[]
    for r in rows:
        a=mp.mpc(0.5,float(r['ia'])); b=mp.mpc(0.5,float(r['ib']))
        s=mp.mpc(0.6,float(r['is_'])); t=mp.mpc(0.6,float(r['it_']))
        Mc=Mq(a,b,s,t,q,ph,Me,'correct'); Mb=Mq(a,b,s,t,q,ph,Me,'buggy')
        D=abs(Mb-Mc)
        arr.append(D); arrsqrt.append(D/math.sqrt(q)); arrqp.append(D/(q/2))
        out.append(dict(q=q,ia=float(r['ia']),ib=float(r['ib']),D=float(D),D_sqrtq=float(D/math.sqrt(q)),D_qp=float(D/(q/2)),
                        absR_correct=float(r['absR'])))
    print(f"q={q:6d}  RMS|ΔM|={math.sqrt(np.mean(np.array(arr)**2)):10.3f}  RMS ΔM/√q={math.sqrt(np.mean(np.array(arrsqrt)**2)):7.3f}  RMS ΔM/(q/2)={math.sqrt(np.mean(np.array(arrqp)**2)):7.4f}  (corrected RMS |E-M|/√q ~ {math.sqrt(np.mean([float(r['absR'])**2 for r in rows]))/math.sqrt(q):.2f})",flush=True)
json.dump(out,open('../logs/bug_repro.json','w'),indent=1)
