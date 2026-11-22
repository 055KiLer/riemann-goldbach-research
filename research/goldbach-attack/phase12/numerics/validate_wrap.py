"""Independent validation of residue-sum W: brute-force pair sum, h-decomposition, and h=0 dominance."""
import sys, math, json
sys.path.insert(0,'.')
import numpy as np
import wrap_core as W
import cmath

def build_cd(X,q,model,eta):
    F=W.make_fg(model,eta,'c'); fc,gc=F(X)
    if model=='cplx':
        Fd=W.make_fg(model,eta,'d'); fd,gd=Fd(X)
    else: fd,gd=fc,gc
    Y=X*X
    c=np.zeros(Y+1,dtype=np.complex128); d=np.zeros(Y+1,dtype=np.complex128)
    mA=np.arange(1,X+1,dtype=np.int64)
    for nn in range(1,X+1):
        idx=nn*mA
        np.add.at(c,idx,fc[nn-1]*gc)
        np.add.at(d,idx,fd[nn-1]*gd)
    return c,d

def W_bruteforce(c,d,q):
    # W = sum_{A≠B, A≡B} c_A conj(d_B); group by residue then subtract diag
    M=len(c)-1
    Sc=np.zeros(q,complex); Sd=np.zeros(q,complex)
    for A in range(1,M+1):
        r=A%q; Sc[r]+=c[A]; Sd[r]+=d[A]
    Wt=complex(np.sum(Sc*np.conj(Sd)))-np.sum(c[1:]*np.conj(d[1:]))
    return Wt

def h_decomp(c,d,q):
    M=len(c)-1
    A=np.arange(1,M+1,dtype=np.int64)
    Ch=np.zeros(q,dtype=np.complex128); Dh=np.zeros(q,dtype=np.complex128)
    for h in range(q):
        ph=np.exp(2j*np.pi*h*(A%q)/q)
        Ch[h]=np.sum(c[1:]*ph); Dh[h]=np.sum(d[1:]*ph)   # D(h)=sum d_B e(hB/q)
    W_all=complex(np.sum(Ch*np.conj(Dh)))/q
    diag=np.sum(c[1:]*np.conj(d[1:]))
    return W_all-diag, Ch, Dh

if __name__=='__main__':
    print('=== validation: q=101, X=32, models ===')
    for model,eta in [('cplx',0.05),('pos_mu',0.05),('pos',0.05),('rect',0.05)]:
        c,d=build_cd(32,101,model,eta)
        Wb=W_bruteforce(c,d,101)
        F=W.make_fg(model,eta,'c'); fc,gc=F(32)
        if model=='cplx': Fd=W.make_fg(model,eta,'d'); fd,gd=Fd(32)
        else: fd,gd=fc,gc
        r=W.compute_W(101,32,fc,gc,fd,gd)
        Wh,Ch,Dh=h_decomp(c,d,101)
        print(f"{model:7s} eta={eta}: W_residue={r['W']:.10g}  W_bruteforce={Wb:.10g}  diff={abs(r['W']-Wb):.2e}  W_hdecomp={Wh:.10g}  h0={abs(Ch[0]*np.conj(Dh[0])/101):.4g}  sum_h!=0 |Ch*Dh|/q={np.sum(np.abs(Ch[1:]*np.conj(Dh[1:])))/101:.4g}")
    print()
    print('=== validation: q=1009, X=179 (cplx) ===')
    c,d=build_cd(179,1009,'cplx',0.05)
    Wb=W_bruteforce(c,d,1009); Wh,Ch,Dh=h_decomp(c,d,1009)
    F=W.make_fg('cplx',0.05,'c'); fc,gc=F(179)
    Fd=W.make_fg('cplx',0.05,'d'); fd,gd=Fd(179)
    r=W.compute_W(1009,179,fc,gc,fd,gd)
    print(f"W_residue={r['W']:.10g} W_bruteforce={Wb:.10g} diff={abs(r['W']-Wb):.2e}")
    print(f"W_hdecomp={Wh:.10g}  h0term={Ch[0]*np.conj(Dh[0])/1009:.10g}  diag={np.sum(c[1:]*np.conj(d[1:])):.6g}")
    print(f"|sum_h!=0 Ch conj(Dh)/q| = {abs(np.sum(Ch[1:]*np.conj(Dh[1:])))/1009:.6g}")
    # prediction from sum of coefficients
    sc=np.sum(c[1:]); sd=np.sum(d[1:])
    print(f"sumA c_A={sc:.6g} sumB d_B={sd:.6g}  (sum c)*(conj sum d)/q={sc*np.conj(sd)/1009:.6g}")
