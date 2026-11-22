"""Scan W(q,X) for models; own code (wrap_core)."""
import sys, json, math, time
sys.path.insert(0,'.')
import numpy as np
import wrap_core as W

def one(q,X,model,eta):
    F=W.make_fg(model,eta,'c'); fc,gc=F(X)
    if model=='cplx':
        Fd=W.make_fg(model,eta,'d'); fd,gd=Fd(X)
    else:
        fd,gd=fc,gc
    r=W.compute_W(q,X,fc,gc,fd,gd)
    r['model']=model; r['eta']=eta; r['A']=math.log(X)/math.log(q)
    r['Wtriv_plan']=r['Wabs']/(X*X/q) if X*X>0 else None      # vs X^2/q
    r['Wtriv_pairs']=r['Wabs']/((X*X)**2/q) if X*X>0 else None # vs (X^2)^2/q = X^4/q
    r['diag_over']=abs(r['diag'])/r['Wabs'] if r['diag'] is not None and r['Wabs']>0 else None
    return r

def main():
    out=[]
    t0=time.time()
    # ---------- scan 1: X-scan at fixed q (wrap regime) ----------
    for q,models in [(101,['pos_mu','pos','cplx','rect']),(1009,['pos_mu','cplx','rect'])]:
        Xs=sorted(set([int(round(x)) for x in np.geomspace(max(2,math.ceil(math.sqrt(q)*1.02)), q, 14)]))
        for model in models:
            for eta in ([0.05,0.02,0.1] if model=='pos_mu' else [0.05]):
                for X in Xs:
                    r=one(q,X,model,eta); out.append(r)
                    print(f"scan q={q:5d} X={X:5d} Y={X*X:9d} A={r['A']:.2f} {model:7s} eta={eta:.2f} |W|={r['Wabs']:10.4g} W/(X²/q)={r['Wtriv_plan']:.4g} W/(X⁴/q)={r['Wtriv_pairs']:.4g} diag/|W|={r['diag_over']}",flush=True)
        json.dump(out,open('logs_wrap_scan1.json','w'),indent=1,default=str)
    # ---------- design cases (a): A=0.5,0.75,1 for q=101,1009 ----------
    for q in [101,1009]:
        for A in [0.5,0.75,1.0]:
            X=max(2,int(round(q**A)))
            for model in ['pos_mu','pos','cplx']:
                for eta in [0.05,0.02]:
                    r=one(q,X,model,eta); out.append(r)
                    print(f"designA q={q:5d} A={A} X={X:5d} {model:7s} eta={eta:.2f} |W|={r['Wabs']:10.4g} W/(X²/q)={r['Wtriv_plan']:.4g} W/(X⁴/q)={r['Wtriv_pairs']:.4g}",flush=True)
        json.dump(out,open('logs_wrap_scan1.json','w'),indent=1,default=str)
    # ---------- design cases (b): A=1.25,1.5 small q ----------
    for q in [53,101,199]:
        for A in [1.25,1.5]:
            X=max(2,int(round(q**A)))
            for model in ['pos_mu','pos','cplx','rect']:
                for eta in [0.05,0.02]:
                    r=one(q,X,model,eta); out.append(r)
                    print(f"designB q={q:5d} A={A} X={X:5d} {model:7s} eta={eta:.2f} |W|={r['Wabs']:10.4g} W/(X²/q)={r['Wtriv_plan']:.4g} W/(X⁴/q)={r['Wtriv_pairs']:.4g}",flush=True)
        json.dump(out,open('logs_wrap_scan1.json','w'),indent=1,default=str)
    print('TOTAL',time.time()-t0)
    json.dump(out,open('logs_wrap_scan1.json','w'),indent=1,default=str)
if __name__=='__main__': main()
