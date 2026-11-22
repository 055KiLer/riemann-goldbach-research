"""W at A=1.75,2.0 for small q (test extrapolation of fitted exponent)."""
import sys, json, math, time, random
sys.path.insert(0,'.')
import numpy as np
import wrap_core as W
from avg_scan import coeffs, run
def main():
    random.seed(21)
    sets=[(0.7,1.3,0.4,2.1),(2.6,-1.1,1.7,0.3),(-2.4,0.9,2.2,1.5)]
    cases=[(53,[1.75,2.0]),(101,[1.75])]  # q=101 A=2 => Y=1.04e8 heavy, only A=1.75 first
    out=[]
    for q,As in cases:
        for A in As:
            X=max(2,int(round(q**A)))
            for model in ['crit','rat']:
                for eta in [0.05,0.02]:
                    for si,st in enumerate(sets):
                        r=run(q,X,model,eta,st,Ylim=2e8)
                        out.append(r)
                        print(f"q={q:4d} X={X:6d} A={r['A']:.2f} Y={X*X:11d} {model:4s} eta={eta:.2f} set{si} |W|={r['Wabs']:11.4g} W/(X²/q)={r['ratio_plan']:.3g} Wq/X={r['Wabs']*q/X:.3g} diag/|W|={r['diag_over']}",flush=True)
            json.dump(out,open('logs_wrap_a2.json','w'),indent=1,default=str)
    # try q=101 A=2 one set (heavy) if time permits later
    print('DONE')
if __name__=='__main__': main()
