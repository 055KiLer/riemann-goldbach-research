"""High-A Delta probes: q=1009 A=1.25, q=199 A=1.5, q=53 A=2.25."""
import sys, json, math
sys.path.insert(0,'.')
import numpy as np
import delta_scan as DS
def main():
    sets=[(0.7,1.3,0.4,2.1),(2.6,-1.1,1.7,0.3),(-2.4,0.9,2.2,1.5)]
    cases=[(1009,1.25),(199,1.5),(53,2.25)]
    out=[]
    for q,A in cases:
        X=max(2,int(round(q**A)))
        for model in ['crit','rat']:
            for eta in [0.05,0.2]:
                for si,st in enumerate(sets):
                    r=DS.delta_case(q,X,X,model,eta,st); out.append(r)
                    t=q**(1-eta*A)
                    print(f"q={q} X={X} A={A} {model} eta={eta} set{si} |Delta|={r['absDelta_lead']:.4g} qW={r['qW']:.4g} ScSd={r['ScSd']:.4g} cancel={r['absDelta_lead']/(r['qW']+r['ScSd']+1e-300):.3f} target={t:.4g} rho={r['absDelta_lead']/t:.3f}",flush=True)
        json.dump(out,open('logs_delta_hiA.json','w'),indent=1,default=str)
    print('DONE')
if __name__=='__main__': main()
