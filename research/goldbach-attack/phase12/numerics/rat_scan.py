"""Focused scale law for W with realistic (mu-bearing) coefficients; own code."""
import sys, json, math, time
sys.path.insert(0,'.')
import numpy as np
import wrap_core as W

def make_fg2(model,eta,which,X):
    n=np.arange(1,X+1,dtype=np.float64); mu=W.sieve_mu(X)[1:].astype(np.complex128)
    if model=='rect': return np.ones(X,dtype=np.complex128), np.ones(X,dtype=np.complex128)
    if model=='crit':
        if which=='c': a=0.5+0.7j; s=0.5+eta+0.4j
        else: a=0.5+1.3j; s=0.5+eta+2.1j
        return n**(-a), mu*n**(-s)
    if model=='rat':
        if which=='c': a=0.5+eta+0.7j; s=0.5+eta+0.4j
        else: a=0.5+eta+1.3j; s=0.5+eta+2.1j
        return n**(-a), mu*n**(-s)
    if model=='nomu':
        if which=='c': a=0.5+eta; s=0.5+eta
        else: a=0.5+eta; s=0.5+eta
        return n**(-a), n**(-s)
    if model=='pos':
        if which=='c': a=0.5; s=0.5+eta
        else: a=0.5; s=0.5+eta
        return n**(-a), n**(-s)
    raise ValueError

def run_case(q,X,model,eta):
    Y=X*X
    fc,gc=make_fg2(model,eta,'c',X)
    fd,gd=make_fg2(model,eta,'d',X)
    r=W.compute_W(q,X,fc,gc,fd,gd)
    r['model']=model; r['eta']=eta; r['A']=math.log(X)/math.log(q)
    r['Wtriv_plan']=r['Wabs']/(Y/q)
    r['Wtriv_pairs']=r['Wabs']/(Y*Y/q)
    r['W_over_Xq']=r['Wabs']*q/X
    r['W_over_X1m2eta_q']=r['Wabs']*q/(X**(1-2*eta))
    r['W_over_sqrtY_q']=r['Wabs']*q/math.sqrt(Y)  # random-sign heuristic X/q vs sqrt(Y)/q
    r['sumc']=complex(np.sum(fc))*complex(np.sum(gc))
    r['sumd']=complex(np.sum(fd))*complex(np.sum(gd))
    r['h0term']=abs(r['sumc']*np.conj(r['sumd'])/q)
    r['diag_over']=abs(r['diag'])/r['Wabs'] if r['diag'] is not None and r['Wabs']>0 else None
    return r

def main():
    out=[]; t0=time.time()
    cases=[]
    for q in [101,1009]:
        for A in [0.55,0.70,0.85,1.0]:
            cases.append((q,max(2,int(round(q**A)))))
    for q in [10007]:
        for A in [0.55,0.70,0.85]:
            cases.append((q,max(2,int(round(q**A)))))
    for q in [53,101,199]:
        for A in [1.25,1.5]:
            cases.append((q,max(2,int(round(q**A)))))
    for (q,X) in cases:
        for model in ['crit','rat','nomu','rect']:
            for eta in [0.05,0.02]:
                if model in ('nomu','rect') and eta==0.02: continue
                r=run_case(q,X,model,eta); out.append(r)
                print(f"q={q:6d} X={X:6d} Y={X*X:10d} A={r['A']:.2f} {model:5s} eta={eta:.2f} |W|={r['Wabs']:11.4g} W/(X²/q)={r['Wtriv_plan']:.3g} W/(X⁴/q)={r['Wtriv_pairs']:.3g} Wq/X={r['W_over_Xq']:.3g} h0/|W|={r['Wabs'] and r['h0term']/r['Wabs']:.2f}",flush=True)
        json.dump(out,open('logs_wrap_rat.json','w'),indent=1,default=str)
    print('TOTAL',time.time()-t0)
if __name__=='__main__': main()
