"""Test candidate explanation: R_q ~ -phi(q/p)*T_{q/p} (level-(q/p) diagonal main term), T_d=Z_d(a,b;s,t)."""
import sys, json, math, mpmath as mp
sys.path.insert(0,'.')
import ramified as R
from group import factorize
mp.mp.dps=25
def phi_int(n):
    r=n
    for p in factorize(n): r=r//p*(p-1)
    return r
def Z_level(q,a,b,s,t):
    c,d=s,t
    return R.zeta_q(a+b,q)*R.zeta_q(c+d,q)/(R.zeta_q(a+d,q)*R.zeta_q(b+c,q))*R.Aq(a,b,c,d,q)
res=json.load(open('../logs/ramified_results.json'))
out=[]
for rec in res:
    q=rec['q']; fam=rec['label']
    if fam not in ('2^e','3^e'): continue
    p=2 if fam=='2^e' else 3
    d=q//p
    for cls in ('generic','nearpole'):
        rows=[r for r in rec['rows'] if r['cls']==cls]
        for r in rows:
            a=mp.mpc(0.5,float(r['ia'])); b=mp.mpc(0.5,float(r['ib']))
            s=mp.mpc(0.6,float(r['is_'])); t=mp.mpc(0.6,float(r['it_']))
            E=mp.mpc(complex(mp.mpc(r['E']))); M=mp.mpc(r['M'])
            Rv=E-M
            Td=Z_level(d,a,b,s,t)
            coeff=-phi_int(d)
            ratio=Rv/(coeff*Td) if Td!=0 else None
            out.append(dict(q=q,family=fam,cls=cls,ratio_abs=float(abs(ratio)) if ratio else None,
                            ratio_re=float(ratio.real),ratio_im=float(ratio.imag),absR=float(abs(Rv)),
                            pred=float(abs(coeff*Td))))
    print('done q',q,flush=True)
json.dump(out,open('../logs/defect_test.json','w'),indent=1)
import numpy as np
for fam in ('2^e','3^e'):
    for cls in ('generic','nearpole'):
        rs=[r for r in out if r['family']==fam and r['cls']==cls]
        if not rs: continue
        re=np.array([r['ratio_re'] for r in rs]); im=np.array([r['ratio_im'] for r in rs])
        print(f"{fam} {cls}: R/(−φ(q/p)Z_(q/p)) mean={re.mean():+.3f}{im.mean():+.3f}i  std=({re.std():.3f},{im.std():.3f})  |mean|={math.hypot(re.mean(),im.mean()):.3f}")
