"""q=101, A=2 (X=10201, Y=1.04e8) W exact (arrays 1.66GB each); a few sets."""
import sys, json, math
sys.path.insert(0,'.')
import numpy as np
import wrap_core as W
from avg_scan import coeffs
def main():
    q=101; X=10201
    sets=[(0.7,1.3,0.4,2.1),(2.6,-1.1,1.7,0.3)]
    out=[]
    for model in ['crit','rat']:
        for eta in [0.05]:
            for si,st in enumerate(sets):
                fc,gc,fd,gd=coeffs(X,model,eta,st)
                r=W.compute_W(q,X,fc,gc,fd,gd,Y_arr_limit=10**9)
                rec=dict(q=q,X=X,Y=X*X,A=2.0,model=model,eta=eta,setidx=si,Wabs=r['Wabs'],W=complex(r['W']),
                         diag=complex(r['diag']) if r['diag'] is not None else None,
                         ratio_plan=r['Wabs']/(X*X/q),target_q=(X*X/q)**0, exact=r['exact'])
                out.append(rec)
                print(f"q={q} X={X} A=2 {model} eta={eta} set{si} |W|={r['Wabs']:.6g} W/(X²/q)={r['Wabs']/(X*X/q):.3g} target q^(1-eta*A)={q**(1-eta*2):.4g} ratio={r['Wabs']/q**(1-eta*2):.3g}",flush=True)
                json.dump(out,open('logs_wrap_a2big.json','w'),indent=1,default=str)
if __name__=='__main__': main()
