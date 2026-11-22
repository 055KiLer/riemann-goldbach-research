import sys, numpy as np
sys.path.insert(0,'.')
from test_mq import compute
from mainterm import zqa
from charlib import CharGroup, factorize
for q in (105,1000,107,503):
    cg=CharGroup(q); fac=factorize(q); cache={}
    for (A,B,S,T) in [(1.0,0.5,0.5,1.0),(1.5,-0.5,0.5,-1.5)]:
        a=complex(0.5,A); b=complex(0.5,B); s=complex(0.6,S); t=complex(0.6,T)
        r=compute(q,a,b,s,t,cg,fac,cache)
        z=zqa(a,q,cg.units,cache)
        def L(u): return complex(q**(-complex(u)))*(cg.V@zqa(u,q,cg.units,cache))
        La=L(a); Lb=L(b); Ls=L(s); Lt=L(t)
        E0=complex(np.sum(La*Lb/(Ls*Lt)))
        M=r['std_Xab']['M']
        print(f"q={q} imgs={A,B,S,T}: E_noBar={E0:.4f} E_bar={r['E']:.4f} M={M:.4f} rel(noBar)={abs(E0-M)/abs(M):.3f} rel(bar)={abs(r['E']-M)/abs(M):.3f}",flush=True)
