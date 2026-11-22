import sys, os, numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from ratios_lib import Group, make_logtab, gen_shifts, make_ab
from corrected import M_correct
from core import compute_E
if __name__=='__main__':
    for eta in (0.02,0.005):
        for q in (100003,):
            G=Group(q); logtab=make_logtab(G.x,10)
            sh=gen_shifts(12,T=2.0,seed=555,config='hyp11',eta=eta)
            print(f"== eta={eta} q={q}",flush=True)
            rows=[]
            for s_ in sh:
                a,b,s,t=make_ab(s_,'hyp11',eta)
                us=[a,b,s,t]
                La,_=G.L_all(us[0],8,logtab); _,Lb=G.L_all(us[1],8,logtab)
                Ls,_=G.L_all(us[2],8,logtab); _,Lt=G.L_all(us[3],8,logtab)
                terms=((La*Lb/(Ls*Lt))[G.prim_mask]); at=np.abs(terms)
                R=complex(terms.sum()); M,_=M_correct(G,a,b,s,t)
                order=np.argsort(at)[::-1]
                rows.append((abs(R-M),abs(R),abs(M),at[order[0]],at[order[:5]].sum()/max(1e-300,at.sum()),np.min(np.abs(Ls[G.prim_mask]))))
            rows.sort(key=lambda r:-r[0])
            for r in rows[:8]:
                print(f" |R-M|={r[0]:11.4g} |R|={r[1]:11.4g} |M|={r[2]:10.4g} maxterm={r[3]:11.4g} top5/tot={r[4]:.2f} min|L(s)|={r[5]:.3g}",flush=True)
