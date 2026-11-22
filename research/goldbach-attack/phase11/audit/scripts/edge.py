"""Edge probes for H_Ratios: eta=0.02, near-pole a+b->1, Re a=1/2+-1/8, T up to 20."""
import sys, numpy as np, mpmath as mp, math, json, time
sys.path.insert(0,'.')
import replicate as R
mp.mp.dps=30
qs=[1009,2000,1001]
probes=[]
# (label, a,b,s,t)
for eta in [0.02]:
    for (ia,ib,is_,it_) in [(0.7,1.3,0.4,2.1),(2.6,-1.1,1.7,0.3)]:
        probes.append((f'eta{eta}_set', mp.mpc(0.5,ia),mp.mpc(0.5,ib),mp.mpc(0.5+eta,is_),mp.mpc(0.5+eta,it_)))
# near-pole: Re(a+b)=1 and Im(a)+Im(b)=eps small
for eps in [0.02,0.1]:
    probes.append((f'nearpole_eps{eps}', mp.mpc(0.5,0.6), mp.mpc(0.5,-0.6+eps), mp.mpc(0.6,0.4), mp.mpc(0.6,2.1)))
# Re a = 1/2 +- 1/8, Re b=1/2
for rea in [0.5+1/8, 0.5-1/8]:
    probes.append((f'Rea{rea}', mp.mpc(rea,0.7), mp.mpc(0.5,1.3), mp.mpc(0.6,0.4), mp.mpc(0.6,2.1)))
# large T up to 20
for (ia,ib,is_,it_) in [(12.0,-7.0,18.0,-13.0),(-15.0,9.0,20.0,5.0)]:
    probes.append(('Tbig', mp.mpc(0.5,ia),mp.mpc(0.5,ib),mp.mpc(0.6,is_),mp.mpc(0.6,it_)))
allout=[]
t0=time.time()
for q in qs:
    for label,a,b,s,t in probes:
        g=R.UnitGroup(q); prim=g.prim; phistar=g.phistar; Me=g.Me; fac=list(R.factorize(q).keys())
        LQ=math.log(q)
        ba=R.zeta_vals(g,a,q); bb=R.zeta_vals(g,b,q); bs=R.zeta_vals(g,s,q); bt=R.zeta_vals(g,t,q)
        La=(g.T@ba)*np.exp(-complex(a)*LQ); Lb=(g.T.conj()@bb)*np.exp(-complex(b)*LQ)
        Ls=(g.T@bs)*np.exp(-complex(s)*LQ); Ltbar=(g.T.conj()@bt)*np.exp(-complex(t)*LQ)
        with np.errstate(all='ignore'):
            ok=prim & np.isfinite(Ls*Ltbar) & (np.abs(Ls*Ltbar)>1e-300)
            Eq=complex(np.sum((La*Lb/(Ls*Ltbar))[ok])); allok=bool(np.all(ok[prim]))
        M,_=R.Mq(a,b,s,t,q,phistar,Me,fac)
        absR=abs(mp.mpc(Eq)-M)
        rec=dict(q=int(q),label=label,a=mp.nstr(a,10),b=mp.nstr(b,10),s=mp.nstr(s,10),t=mp.nstr(t,10),
                 E=mp.nstr(mp.mpc(Eq),18),M=mp.nstr(M,18),ratio=float(absR/math.sqrt(q)),
                 rel=float(absR/abs(M)) if M!=0 else None,ok=allok)
        allout.append(rec)
        print(f"q={q:5d} {label:16s} |E-M|/sqrtq={rec['ratio']:10.4g}  rel={rec['rel']}  ok={allok}",flush=True)
json.dump(allout,open('../logs/A_edge.json','w'),indent=1)
print('TOTAL',time.time()-t0)
