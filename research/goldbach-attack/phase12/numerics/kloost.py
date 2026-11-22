"""Kloosterman/FE-folded phase sums S1=sum c_A conj(d_B) e(B/A), S2=... e(A/B) (q prime).
Own code. Compare with trivial L1 and W."""
import sys, json, math, random, time
sys.path.insert(0,'.')
import numpy as np
import wrap_core as W

def mobius_int(n):
    return W.sieve_mu(n)

def coeffs(X,model,eta,setargs):
    aa,ab,ts,tt=setargs
    n=np.arange(1,X+1,dtype=np.float64); mu=mobius_int(X)[1:].astype(np.complex128)
    if model=='crit':
        a=0.5+1j*aa; b=0.5+1j*ab; s=0.5+eta+1j*ts; t=0.5+eta+1j*tt
    elif model=='rat':
        a=0.5+eta+1j*aa; b=0.5+eta+1j*ab; s=0.5+eta+1j*ts; t=0.5+eta+1j*tt
    elif model=='nomu':
        a=0.5+eta+1j*aa; b=0.5+eta+1j*ab; s=0.5+eta+1j*ts; t=0.5+eta+1j*tt
        return n**(-a),n**(-s),n**(-b),n**(-t)
    return n**(-a),mu*n**(-s),n**(-b),mu*n**(-t)

def residue_sums2(X,q,fc,gc,fd,gd):
    Sc=W.residue_sums(X,q,fc,gc); Sd=W.residue_sums(X,q,fd,gd)
    return Sc,Sd

def kloost(q,Sc,Sd):
    # units mod q
    units=np.array([a for a in range(1,q) if math.gcd(a,q)==1],dtype=np.int64)
    inv=np.array([pow(int(a),q-2,q) for a in units],dtype=np.int64)
    barr=np.arange(q,dtype=np.int64)
    ph=(inv[:,None]*barr[None,:])%q
    E=np.exp(2j*np.pi*ph/q)  # nU x q
    ScU=Sc[units]; SdU=Sd[units]
    S1=np.sum(Sc[units]* (E@Sd))          # sum_{A unit} c_A sum_B d_B e(B inv(A)/q)
    S2=np.sum(np.conj(Sd[units])* (E@Sc)) # sum_{B unit} conj(d_B) sum_A c_A e(A inv(B)/q)
    L1=(np.sum(np.abs(ScU)))*(np.sum(np.abs(Sd)))
    L1u=(np.sum(np.abs(ScU)))*(np.sum(np.abs(SdU)))
    return dict(S1=complex(S1),S2=complex(S2),L1=float(L1),L1u=float(L1u),
                S1_over_L1=abs(S1)/L1 if L1 else None,
                S1_over_L1u=abs(S1)/L1u if L1u else None,
                S2_over_L1=abs(S2)/L1 if L1 else None)

def main():
    random.seed(7)
    sets=[(0.7,1.3,0.4,2.1),(2.6,-1.1,1.7,0.3),(-2.4,0.9,2.2,1.5)]
    out=[]
    for q in [101,1009]:
        for A in [0.5,0.75,1.0]:
            X=max(2,int(round(q**A)))
            for model in ['crit','rat','nomu','rect']:
                for eta in [0.05]:
                    for si,st in enumerate(sets):
                        if model=='rect':
                            fc=gc=fd=gd=np.ones(X,dtype=np.complex128)
                        else:
                            fc,gc,fd,gd=coeffs(X,model,eta,st)
                        Sc,Sd=residue_sums2(X,q,fc,gc,fd,gd)
                        r=kloost(q,Sc,Sd)
                        # also plain W (for comparison, residue only + exact diag via arrays if small)
                        w=W.compute_W(q,X,fc,gc,fd,gd)
                        rec=dict(q=q,X=X,A=A,model=model,eta=eta,set=si,**r,
                                 Wabs=w['Wabs'],diag_over=None,
                                 Y=X*X, trivial_plan=X*X/q)
                        out.append(rec)
                        print(f"q={q:5d} X={X:5d} A={A} {model:5s} set{si} |S1|={abs(r['S1']):10.4g} |S2|={abs(r['S2']):10.4g} |S1|/L1={r['S1_over_L1']:.3g} |W|={w['Wabs']:.4g} |S1|/|W|={abs(r['S1'])/w['Wabs'] if w['Wabs'] else float('inf'):.3g}",flush=True)
            json.dump(out,open('logs_kloost.json','w'),indent=1,default=str)
    print('DONE',time.time())
if __name__=='__main__': main()
