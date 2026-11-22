"""Stronger asymmetric truncation: N=q^(A-delta), M=q^(A+delta), delta=0.5; compare Delta to square case."""
import sys, json, math
sys.path.insert(0,'.')
import numpy as np
import delta_scan as DS
def main():
    sets=[(0.7,1.3,0.4,2.1),(2.6,-1.1,1.7,0.3),(-2.4,0.9,2.2,1.5)]
    out=[]
    for q,A,delta in [(101,1.0,0.5),(101,1.25,0.5),(101,1.5,0.5),(199,1.0,0.5),(199,1.25,0.5)]:
        N=max(2,int(round(q**(A-delta)))); M=max(2,int(round(q**(A+delta))))
        for model in ['crit','rat']:
            for eta in [0.05,0.2]:
                for si,st in enumerate(sets):
                    r=DS.delta_case(q,N,M,model,eta,st); out.append(r)
                    print(f"q={q} N={N} M={M} A={r['A']:.2f} {model} eta={eta} set{si} |Delta|={r['absDelta_lead']:.4g} qW={r['qW']:.4g} ScSd={r['ScSd']:.4g} cancel={r['absDelta_lead']/(r['qW']+r['ScSd']+1e-300):.3f}",flush=True)
        json.dump(out,open('logs_delta_asym2.json','w'),indent=1,default=str)
    print('DONE')
if __name__=='__main__': main()
