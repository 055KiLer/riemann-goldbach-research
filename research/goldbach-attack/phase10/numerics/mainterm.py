"""Compute E_q and the auditor's parity-resolved main term M_q for composite q."""
import numpy as np, mpmath as mp, sys, os, json, time
sys.path.insert(0,'.')
from charlib import CharGroup, factorize

mp.mp.dps=25
PRIMES=np.load('primes_2000000.npy')
PRIMES=PRIMES[PRIMES<=1000000]

def zqa(u, q, units, cache):
    key=(complex(u), q)
    if key in cache: return cache[key]
    arr=np.array([complex(mp.zeta(mp.mpc(u.real,u.imag), mp.mpf(int(a))/q)) for a in units],dtype=complex)
    cache[key]=arr; return arr

def Lvals(u,q,cg,cache):
    z=zqa(u,q,cg.units,cache)
    Lv=cg.V@z    # (nchars,)
    return Lv*(mp.mpf(q)**(-mp.mpc(u.real,u.imag)) if False else complex(q**(-complex(u))))

def zeta_q(s,q,fac,cache):
    key=('zq',complex(s),q)
    if key in cache: return cache[key]
    z=complex(mp.zeta(mp.mpc(s.real,s.imag)))
    for p in fac:
        z*= (1.0-complex(mp.power(p, -mp.mpc(s.real,s.imag))))
    cache[key]=z; return z

def Aprod(a,b,c,d,q):
    # product over primes p not dividing q
    mask=(PRIMES%q!=0)
    p=PRIMES[mask].astype(float)
    lp=np.log(p)
    X=np.exp(-(a+d)*lp); Y=np.exp(-(b+c)*lp); G=np.exp(-(c+d)*lp)
    with np.errstate(all='ignore'):
        num=(1-G)*(1-X-Y+G); den=(1-X)*(1-Y)
        f=num/den
        w=f-1.0
        s=np.sum(np.log1p(w))
    return complex(np.exp(s))

def Xqe(q,e,w):
    # (q/pi)^{1/2-w} Gamma((1-w+e)/2)/Gamma((w+e)/2)
    w=mp.mpc(w.real,w.imag)
    return mp.power(q/mp.pi, mp.mpf(1)/2-w)*mp.gamma((1-w+e)/2)/mp.gamma((w+e)/2)

def eval_point(q, a, b, s, t, cg, fac, cache):
    e0=cg.parity
    Ls={u:None for u in (a,b,s,t)}
    for u in (a,b,s,t):
        Ls[u]=Lvals(u,q,cg,cache)
    num=Ls[a]*Ls[b]; den=Ls[s]*Ls[t]
    terms=num/den
    E=complex(np.sum(terms))
    Ee=[complex(np.sum(terms[np.array(e0)==e])) for e in (0,1)]
    M0,M1=cg.counts(); phist=M0+M1
    # Z_q(a,b;c=s,d=t)
    def Zq(x,y,c,d):
        return zeta_q(x+y,q,fac,cache)*zeta_q(c+d,q,fac,cache)/(zeta_q(x+d,q,fac,cache)*zeta_q(y+c,q,fac,cache))*Aprod(x,y,c,d,q)
    Z=Zq(a,b,s,t); Zd=Zq(1-b,1-a,s,t)
    H=sum((M0 if e==0 else M1)*Xqe(q,e,a)*Xqe(q,e,b) for e in (0,1))
    M=phist*Z+H*Zd
    Me=[]
    for e in (0,1):
        Me.append((M0 if e==0 else M1)*(Z + Xqe(q,e,a)*Xqe(q,e,b)*Zd))
    return dict(E=E,E0=Ee[0],E1=Ee[1],M=complex(M),M0=phist*Z+H*Zd, Mpar_e=[complex(Me[0]),complex(Me[1])],
                M0_only=Z,Mdual=Zd,phi=phist,counts=(M0,M1))

if __name__=='__main__':
    qs=[int(x) for x in sys.argv[1].split(',')]
    etas=[float(x) for x in sys.argv[2].split(',')]
    imgs=[(1.0,0.5,0.5,1.0),(-1.0,0.5,0.5,-1.0),(1.0,-0.5,-0.5,0.5),(0.5,1.0,-1.0,0.5),(1.5,-0.5,0.5,-1.5)]
    out=[]
    for q in qs:
        t0=time.time(); cg=CharGroup(q); fac=factorize(q); cache={}
        if cg.n==0:
            print(f"q={q}: NO primitive characters (conductor q impossible: v2(q)=1); trivial case",flush=True)
            out.append(dict(q=q,n=0,note='no primitive chars'))
            continue
        for eta in etas:
            for (A,B,S,T) in imgs:
                a=complex(0.5,A); b=complex(0.5,B); s=complex(0.5+eta,S); t=complex(0.5+eta,T)
                r=eval_point(q,a,b,s,t,cg,fac,cache)
                def clean(v):
                    if isinstance(v,mp.mpc) or isinstance(v,complex): 
                        c=complex(v); return [float(c.real),float(c.imag)]
                    if isinstance(v,list): return [clean(x) for x in v]
                    if isinstance(v,tuple): return [clean(x) for x in v]
                    return v
                rec=dict(q=q,eta=eta,imgs=(A,B,S,T),**{k:clean(v) for k,v in r.items()})
                out.append(rec)
        print(f"q={q} chars={cg.n} counts={cg.counts()} time={time.time()-t0:.1f}s",flush=True)
    with open('cache/ratios_results.jsonl','a') as f:
        for r in out: f.write(json.dumps(r)+'\n')
    for r in out:
        if r.get('n',1)==0: continue
        E=complex(*r['E']); M=complex(*r['M']); d=abs(E-M)
        print(f"q={r['q']:>5} eta={r['eta']} imgs={r['imgs']}: E={E:.6f} M={M:.6f} |E-M|={d:.6f} /q^0.5={d/np.sqrt(r['q']):.6f} rel={d/abs(M):.4f}",flush=True)
