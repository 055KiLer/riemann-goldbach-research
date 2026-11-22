"""Measure net wrap quantity Delta = E^{(X)} - (q-1)D (own code, q prime).
E^{(X)}=sum^*_chi P_a P_b Q_c Q_d with c_A=sum_{nm=A,n<=N,m<=M} n^{-a}mu(m)m^{-s}, d similar.
Residue-sum formula (q prime): E = q sum_{r!=0} Sc[r] conj(Sd[r]) - (S_c-S_c0)(conj(S_d-S_d0)).
Delta = E - (q-1) D,  D = sum_A c_A conj(d_A).
"""
import sys, json, math, time, random
sys.path.insert(0,'.')
import numpy as np
import wrap_core as W

def build(X1,X2,model,eta,st):
    """c_A=sum_{n<=X1,m<=X2} f(n)g(m); returns c,d arrays length X1*X2+1 and sums."""
    aa,ab,ts,tt=st
    n1=np.arange(1,X1+1,dtype=np.float64); n2=np.arange(1,X2+1,dtype=np.float64)
    mu1=W.sieve_mu(X1)[1:].astype(np.complex128); mu2=W.sieve_mu(X2)[1:].astype(np.complex128)
    if model=='crit':
        a=0.5+1j*aa; b=0.5+1j*ab; s=0.5+eta+1j*ts; t=0.5+eta+1j*tt
    else:
        a=0.5+eta+1j*aa; b=0.5+eta+1j*ab; s=0.5+eta+1j*ts; t=0.5+eta+1j*tt
    Y=X1*X2
    c=np.zeros(Y+1,dtype=np.complex128); d=np.zeros(Y+1,dtype=np.complex128)
    m2=np.arange(1,X2+1,dtype=np.int64)
    for nn in range(1,X1+1):
        idx=nn*m2
        np.add.at(c,idx,n1[nn-1]**(-a)*(mu2*n2**(-s)))
        np.add.at(d,idx,n1[nn-1]**(-b)*(mu2*n2**(-t)))
    return c,d,Y

def residue_sums_rect(X1,X2,q,model,eta,st):
    aa,ab,ts,tt=st
    n1=np.arange(1,X1+1,dtype=np.float64); n2=np.arange(1,X2+1,dtype=np.float64)
    mu2=W.sieve_mu(X2)[1:].astype(np.complex128)
    if model=='crit':
        a=0.5+1j*aa; b=0.5+1j*ab; s=0.5+eta+1j*ts; t=0.5+eta+1j*tt
    else:
        a=0.5+eta+1j*aa; b=0.5+eta+1j*ab; s=0.5+eta+1j*ts; t=0.5+eta+1j*tt
    def rs(f,g):
        S=np.zeros(q,dtype=np.complex128); m2i=np.arange(1,X2+1,dtype=np.int64)
        for nn in range(1,X1+1):
            res=(nn*m2i)%q; w=f[nn-1]*g
            S+=np.bincount(res,weights=w.real,minlength=q)+1j*np.bincount(res,weights=w.imag,minlength=q)
        return S
    Sc=rs(n1**(-a),mu2*n2**(-s)); Sd=rs(n1**(-b),mu2*n2**(-t))
    return Sc,Sd

def delta_case(q,X1,X2,model,eta,st):
    c,d,Y=build(X1,X2,model,eta,st)
    Sc,Sd=residue_sums_rect(X1,X2,q,model,eta,st)
    Sc0=complex(Sc[0]); Sd0=complex(Sd[0]); Sct=complex(np.sum(Sc)); Sdt=complex(np.sum(Sd))
    E=(q-1)*np.sum(Sc[1:]*Sd[1:]) - (Sct-Sc0)*(Sdt-Sd0)
    D=np.sum(c[1:]*d[1:])
    Delta_E=complex(E)-(q-1)*complex(D)
    # coprime diagonal / W / T
    notzero=np.arange(1,Y+1)%q!=0
    Dcp=np.sum(c[1:][notzero]*d[1:][notzero])
    ScSd_cp=(Sct-Sc0)*(Sdt-Sd0)
    Wcp=complex(np.sum(Sc[1:]*Sd[1:])-Dcp)
    T=Sc0*Sdt+(Sct-Sc0)*Sd0
    ScSd_tot=Sct*Sdt
    Delta_lead=complex((q-1)*Wcp - ScSd_tot + T)
    # h-decomposition: C(h)=sum_A c_A e(hA/q)=ifft(Sc)*q ; D'(h)=sum_B d_B e(-hB/q)=fft(Sd)
    C=np.fft.ifft(Sc)*q; Dh=np.fft.fft(Sd)
    hsum=complex(np.sum(C[1:]*Dh[1:]))   # sum_{h!=0} C(h) D(-h)
    h0=complex(C[0]*Dh[0])
    return dict(q=int(q),X1=int(X1),X2=int(X2),Y=int(Y),A=0.5*math.log(Y)/math.log(q),
                model=model,eta=eta,
                E=complex(E),D=complex(D),Delta=Delta_E,absDelta=abs(Delta_E),
                Delta_lead=Delta_lead,absDelta_lead=abs(Delta_lead),
                qW=abs((q-1)*Wcp),ScSd=abs(ScSd_cp),ScSd_tot=abs(ScSd_tot),T=abs(T),
                Wcp=Wcp,Dcp=complex(Dcp),hsum_abs=abs(hsum),h0_abs=abs(h0),
                Sct=Sct,Sdt=Sdt,Sc0=Sc0,Sd0=Sd0)

def main():
    random.seed(33)
    sets=[(0.7,1.3,0.4,2.1),(2.6,-1.1,1.7,0.3),(-2.4,0.9,2.2,1.5)]
    out=[]; t0=time.time()
    cases=[]
    base=[(101,0.5),(101,0.75),(101,1.0),(101,1.25),(101,1.5),(1009,0.5),(1009,0.75),(1009,1.0),(10007,0.5),(10007,0.75),(10007,0.9),(53,1.5),(53,1.75),(53,2.0)]
    extra=[(53,0.5),(53,0.75),(53,1.0),(53,1.25),(199,0.5),(199,0.75),(199,1.0),(199,1.25)]
    for q,A in base+extra:
        X=max(2,int(round(q**A))); cases.append((q,X,X))
    # asymmetric shapes at q=101, same Y as square X=q^A (A=0.75,1.0,1.25): N=q^{A-0.25}, M=q^{A+0.25}
    for q,A in [(101,0.75),(101,1.0),(101,1.25)]:
        N=max(2,int(round(q**(A-0.25)))); M=max(2,int(round(q**(A+0.25))))
        cases.append((q,N,M))
    for (q,X1,X2) in cases:
        for model in ['crit','rat']:
            for eta in [0.05,0.1,0.2]:
                for si,st in enumerate(sets):
                    if X1*X2>4e6 and si>1: continue
                    r=delta_case(q,X1,X2,model,eta,st)
                    out.append(r)
                    print(f"q={q:6d} N={X1:6d} M={X2:6d} Y={X1*X2:11d} A={r['A']:.2f} {model:4s} eta={eta:.2f} set{si} |Δ|={r['absDelta']:11.4g} |qW|={r['qW']:10.4g} |ScSd|={r['ScSd']:10.4g} Δ/(qW+ScSd)={r['absDelta']/(r['qW']+r['ScSd']+1e-300):.3g} target q^(1-etaA)={q**(1-eta*r['A']):.4g} ratio={r['absDelta']/q**(1-eta*r['A']):.3g}",flush=True)
        json.dump(out,open('logs_delta.json','w'),indent=1,default=str)
    print('TOTAL',time.time()-t0)
if __name__=='__main__': main()
