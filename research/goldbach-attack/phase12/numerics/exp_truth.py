"""Phase-12 task-53: Ratios truth vs eta.

Configurations
  hyp11   : Hyp 1.1 / RCD -- Re a=Re b=1/2, Re s=Re t=1/2+eta  (numerator on critical line)
  shifted : RAT(c) region -- all four Re = 1/2+eta

Measured: R_q (exact full primitive-character sum via validated phase-11 fast DFT) vs
M_q (CFG main term + second main term, corrected A_q mask q%p!=0).
"""
import sys, os, json, time
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from ratios_lib import gen_shifts, run_q, stats

PRIMES=[211,1009,5003,10007,30011,100003]
OUT=os.path.join(HERE,'cache'); os.makedirs(OUT,exist_ok=True)

def compute_block(config, eta, qs, nshifts=48, T=2.0, seed=500, min_ab=0.5):
    sh=gen_shifts(nshifts,T=T,seed=seed,config=config,eta=eta)
    recs=[]
    for q in qs:
        t0=time.time()
        res=run_q(q,sh,config,eta)
        if res is None: continue
        st=stats(res)
        st['secs']=time.time()-t0
        recs.append(st)
        print(f"  [{config} eta={eta}] q={q:>6} n={st['n']} RMS={st['rms']:10.3f} RMS/sqrtq={st['rms_over_sqrtq']:8.3f} med={st['med']:10.3f} rel_rms={st['rel_rms']:.3f} |M|rms={st['M_rms']:10.1f} ({st['secs']:.1f}s)",flush=True)
    return recs,sh

def fit_alpha(recs, nboot=400):
    qs=np.array([r['q'] for r in recs],float); rs=np.array([r['rms'] for r in recs])
    ms=np.array([r['med'] for r in recs])
    def slope(y, x):
        A=np.vstack([np.ones_like(x),np.log(x)]).T
        sol=np.linalg.lstsq(A,np.log(y),rcond=None)[0]
        res=np.log(y)-A@sol
        n=len(x); se=np.sqrt(np.sum(res**2)/max(1,n-2)*np.linalg.inv(A.T@A)[1,1]) if n>2 else float('nan')
        return float(sol[1]),float(sol[0]),float(se)
    a_rms,c_rms,se_rms=slope(rs,qs)
    a_med,c_med,se_med=slope(ms,qs)
    return dict(alpha_rms=a_rms,const_rms=c_rms,se_rms=se_rms,
                alpha_med=a_med,const_med=c_med,se_med=se_med,
                n_q=len(qs), qs=qs.tolist(), rms=rs.tolist(), med=ms.tolist())

if __name__=='__main__':
    out={'primes':PRIMES,'T_default':2.0,'nshifts':48,'blocks':{}}
    # ---- (1) Hyp 1.1 config, eta scan
    for eta in (0.1,0.05,0.02,0.01,0.005):
        key=f'hyp11_eta{eta}'
        print(f"== config=hyp11 eta={eta}",flush=True)
        recs,sh=compute_block('hyp11',eta,PRIMES)
        fit=fit_alpha(recs)
        out['blocks'][key]=dict(config='hyp11',eta=eta,records=recs,fit=fit,shifts=sh)
        print(f"  FIT alpha(rms)={fit['alpha_rms']:.3f}+-{fit['se_rms']:.3f}  alpha(med)={fit['alpha_med']:.3f}+-{fit['se_med']:.3f}  const(rms)={fit['const_rms']:.2f}",flush=True)
        json.dump(out,open(os.path.join(OUT,'truth_runs.json'),'w'))
    # ---- (2) shifted-region config, eta scan
    for eta in (0.1,0.05,0.02,0.01):
        key=f'shifted_eta{eta}'
        print(f"== config=shifted eta={eta}",flush=True)
        recs,sh=compute_block('shifted',eta,PRIMES)
        fit=fit_alpha(recs)
        out['blocks'][key]=dict(config='shifted',eta=eta,records=recs,fit=fit,shifts=sh)
        print(f"  FIT alpha(rms)={fit['alpha_rms']:.3f}+-{fit['se_rms']:.3f}  alpha(med)={fit['alpha_med']:.3f}+-{fit['se_med']:.3f}",flush=True)
        json.dump(out,open(os.path.join(OUT,'truth_runs.json'),'w'))
    # ---- (3) T dependence: hyp11, q=10007 & 30011, eta=0.05, T=2,10,30,50
    print("== T dependence (hyp11, eta=0.05)",flush=True)
    out['T']=[]
    for q in (10007,30011):
        for T in (2.0,10.0,30.0,50.0):
            sh=gen_shifts(24,T=T,seed=777,config='hyp11',eta=0.05)
            res=run_q(q,sh,'hyp11',0.05)
            st=stats(res); st.update(q=q,T=T)
            out['T'].append(st)
            print(f"  q={q} T={T:>4} RMS={st['rms']:10.1f} RMS/sqrtq={st['rms_over_sqrtq']:7.2f}",flush=True)
    json.dump(out,open(os.path.join(OUT,'truth_runs.json'),'w'))
    # ---- (4) composite q spot checks (corrected A_q), hyp11 and shifted
    print("== composite q (hyp11 eta=0.05/0.02)",flush=True)
    out['composite']={}
    comp=[1024,2187,4096,6561,16384,32768]
    for eta in (0.05,0.02):
        recs=[]
        for q in comp:
            sh=gen_shifts(32,T=2.0,seed=909,config='hyp11',eta=eta)
            res=run_q(q,sh,'hyp11',eta)
            st=stats(res); st['eta']=eta; recs.append(st)
            print(f"  eta={eta} q={q:>6} RMS={st['rms']:10.1f} RMS/sqrtq={st['rms_over_sqrtq']:8.3f} rel_rms={st['rel_rms']:.3f}",flush=True)
        out['composite'][f'hyp11_eta{eta}']=recs
        json.dump(out,open(os.path.join(OUT,'truth_runs.json'),'w'))
    print("saved",os.path.join(OUT,'truth_runs.json'))
