"""Diagnose whether |R-M| is dominated by rare resonant characters (small |L(s,chi)|)."""
import sys, os, numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from ratios_lib import Group, make_logtab, gen_shifts, make_ab
from corrected import M_correct
from core import compute_E
sys.path.insert(0,os.path.abspath(os.path.join(HERE,'..','..','phase10','numerics')))
from mainterm import zeta_q, Xqe

def block_terms(G,logtab,a,b,s,t):
    us=[complex(a),complex(b),complex(s),complex(t)]
    La,_=G.L_all(us[0],8,logtab); _,Lb=G.L_all(us[1],8,logtab)
    Ls,_=G.L_all(us[2],8,logtab); _,Lt=G.L_all(us[3],8,logtab)
    m=G.prim_mask
    terms=(La*Lb/(Ls*Lt))[m]
    return terms, np.abs(Ls[m]), np.abs(Lt[m])

if __name__=='__main__':
    for eta in (0.05,0.01,0.005):
        print(f"== eta={eta}",flush=True)
        for q in (100003,):
            G=Group(q); logtab=make_logtab(G.x,10)
            sh=gen_shifts(10,T=2.0,seed=555,config='hyp11',eta=eta)
            print(f"  q={q} n_terms={G.phist}",flush=True)
            rows=[]
            for s_ in sh:
                a,b,s,t=make_ab(s_,'hyp11',eta)
                terms,ls,lt=block_terms(G,logtab,a,b,s,t)
                R=terms.sum(); M,_=M_correct(G,a,b,s,t)
                at=np.abs(terms); order=np.argsort(at)[::-1]
                top1=at[order[0]]; top5=at[order[:5]].sum(); tot=at.sum()
                rows.append((abs(R-M),abs(R),abs(M),top1,top5,tot,ls.min(),np.median(ls),at.max()/np.median(at)))
            rows.sort(key=lambda r:-r[0])
            for r in rows[:6]:
                print(f"    |R-M|={r[0]:10.3g} |R|={r[1]:10.3g} |M|={r[2]:10.3g} top1={r[3]:10.3g} top5/tot={r[4]/max(1e-300,r[5]):.2f} min|L(s)|={r[6]:.3g} max/med term={r[8]:.1f}",flush=True)
