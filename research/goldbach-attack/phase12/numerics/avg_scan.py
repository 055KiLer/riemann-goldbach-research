"""Average |W| over random shift sets; fit scale law. Own code."""
import sys, json, math, time, random
sys.path.insert(0,'.')
import numpy as np
import wrap_core as W

def coeffs(X,model,eta,setargs):
    """setargs=(aa,ab,ts,tt) imaginary shifts."""
    aa,ab,ts,tt=setargs
    n=np.arange(1,X+1,dtype=np.float64); mu=W.sieve_mu(X)[1:].astype(np.complex128)
    if model=='crit':   # numerator critical line
        a=0.5+1j*aa; b=0.5+1j*ab; s=0.5+eta+1j*ts; t=0.5+eta+1j*tt
    elif model=='rat':  # numerator at 1/2+eta (RAT(c) configuration)
        a=0.5+eta+1j*aa; b=0.5+eta+1j*ab; s=0.5+eta+1j*ts; t=0.5+eta+1j*tt
    else: raise ValueError
    fc=n**(-a); gc=mu*n**(-s); fd=n**(-b); gd=mu*n**(-t)
    return fc,gc,fd,gd

def run(q,X,model,eta,setargs,Ylim=2.2e7):
    fc,gc,fd,gd=coeffs(X,model,eta,setargs)
    r=W.compute_W(q,X,fc,gc,fd,gd,Y_arr_limit=int(Ylim))
    Y=X*X
    out=dict(q=q,X=X,Y=Y,A=math.log(X)/math.log(q),model=model,eta=eta,setargs=list(setargs),
             Wabs=r['Wabs'],W=complex(r['W']),exact=r['exact'],
             diag_over=(abs(r['diag'])/r['Wabs'] if r['diag'] is not None and r['Wabs']>0 else None),
             sumc=abs(r['sum_Sc']),ratio_plan=r['Wabs']/(Y/q),ratio_X4=r['Wabs']/(Y*Y/q))
    return out

def main():
    random.seed(11)
    sets=[]
    while len(sets)<5:
        s=(round(random.uniform(-2,2),3),round(random.uniform(-2,2),3),round(random.uniform(-2,2),3),round(random.uniform(-2,2),3))
        if abs(s[0]+s[1])<0.5: continue
        sets.append(s)
    cases=[]
    for q,As in [(101,[0.6,0.75,0.9,1.0]),(1009,[0.6,0.75,0.9,1.0]),(10007,[0.6,0.75,0.9]),(53,[1.25,1.5]),(199,[1.25,1.5])]:
        for A in As:
            cases.append((q,max(2,int(round(q**A)))))
    cases.append((10007,10007))  # A=1 big case
    out=[]; t0=time.time()
    for (q,X) in cases:
        for model in ['crit','rat']:
            for eta in [0.05,0.02]:
                for si,st in enumerate(sets):
                    if X>6000 and si>1: continue   # limit big case sets
                    r=run(q,X,model,eta,st); out.append(r)
                    print(f"q={q:6d} X={X:6d} A={r['A']:.2f} {model:4s} eta={eta:.2f} set{si} |W|={r['Wabs']:10.4g} W/(X²/q)={r['ratio_plan']:.3g} Wq/X={r['Wabs']*q/X:.3g} diag/|W|={r['diag_over']}",flush=True)
        json.dump(out,open('logs_wrap_avg.json','w'),indent=1,default=str)
    print('TOTAL',time.time()-t0)
if __name__=='__main__': main()
