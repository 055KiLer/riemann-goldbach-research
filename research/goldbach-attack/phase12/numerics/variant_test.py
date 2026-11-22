"""Test whether the canonical M_q is missing a second reflection/main term at small eta."""
import sys, os, numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from ratios_lib import Group, make_logtab, compute_E
from corrected import M_correct, Zq_correct, Aq_correct
from mainterm import zeta_q, Xqe
from ratios_lib import gen_shifts, make_ab

def Z(G,x,y,c,d):
    return Zq_correct(x,y,c,d,G.q,G.fac,{})

def variants(G,a,b,s,t):
    q=G.q; M0,M1=G.M0,G.M1; phist=G.phist
    Z1=Z(G,a,b,s,t); Zd=Z(G,1-b,1-a,s,t)
    # also Z with swapped role: Z(1-a,1-b;s,t), Z(b,a;s,t) etc
    def H(x,y):
        return sum((M0 if e==0 else M1)*Xqe(q,e,x)*Xqe(q,e,y) for e in (0,1))
    h_ab=H(a,b); h_1m=H(1-b,1-a)
    out={
      'M0':complex(phist*Z1+h_ab*Zd),                    # canonical
      'Ma':complex(phist*Z1+h_1m*Zd),                    # phase-9 variant
      'Mb':complex(phist*Z1+h_ab*Zd+h_1m*Z1),            # add second reflection term
      'Mc':complex(phist*Z1+h_1m*Z1+h_ab*Zd),            # same as Mb
      'Md':complex(phist*Z1+h_ab*Zd+h_ab*Z1),            # add H_ab*Z1
      'Me':complex(phist*Z1+h_ab*Zd+h_1m*Z(G,1-a,1-b,s,t)),
      'Mf':complex(phist*Z1+h_ab*Zd-h_1m*Z1),            # minus second term
      'Mg':complex(phist*Z1+h_ab*Zd+h_1m*Z(G,b,a,s,t)),
    }
    return out

if __name__=='__main__':
    for eta in (0.05,0.02,0.01,0.005):
        sh=gen_shifts(8,T=2.0,seed=321,config='hyp11',eta=eta)
        print(f"== eta={eta}",flush=True)
        for q in (10007,100003):
            G=Group(q); logtab=make_logtab(G.x,10)
            rows={}
            for s_ in sh:
                a,b,s,t=make_ab(s_,'hyp11',eta)
                R=compute_E(G,a,b,s,t,logtab=logtab)
                vs=variants(G,a,b,s,t)
                for k,v in vs.items():
                    rows.setdefault(k,[]).append(R-v)
            line=[]
            for k in rows:
                d=np.abs(np.array(rows[k]))
                line.append(f"{k}:rms={np.sqrt(np.mean(d**2)):.4g}")
            print(f"  q={q}: "+"  ".join(line),flush=True)
