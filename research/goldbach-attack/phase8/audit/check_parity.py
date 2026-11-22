import mpmath as mp
mp.mp.dps=30
# primitive chars mod 5: trivial, quadratic (even), chi, chibar (odd)
# values on a=1..5 (0 at a=5)
chars={
 'triv': {1:1,2:1,3:1,4:1,5:0},   # even
 'quad': {1:1,2:-1,3:-1,4:1,5:0}, # even
 'chi' : {1:1,2:mp.mpc(0,1),3:mp.mpc(0,-1),4:-1,5:0},  # odd (chi(-1)=chi(4)=-1)
 'chib': {1:1,2:mp.mpc(0,-1),3:mp.mpc(0,1),4:-1,5:0},
}
par={'triv':0,'quad':0,'chi':1,'chib':1}
q=5
def L(u,key):
    ch=chars[key]
    s=mp.mpf(0)
    for a in range(1,q+1):
        if ch[a]!=0: s+=ch[a]*mp.zeta(u,mp.mpf(a)/q)
    return q**(-u)*s
def R(a,b,s,t):
    tot=mp.mpc(0)
    for key,ch in chars.items():
        tot+=L(a,key)*L(b,{'triv':'triv','quad':'quad','chi':'chib','chib':'chi'}[key])/(L(s,key)*L(t,{'triv':'triv','quad':'quad','chi':'chib','chib':'chi'}[key]))
    return tot
def X(e,w):
    return (mp.mpf(q)/mp.pi)**(mp.mpf(1)/2-w)*mp.gamma((mp.mpf(1)-w+e)/2)/mp.gamma((w+e)/2)
eta=mp.mpf('0.05')
s=mp.mpc('0.5','0.0')+eta  # real part 0.55
t=mp.mpc('0.5','0.4')+eta
# choose u,v small complex
for (u,v) in [(mp.mpc('0.01','0.02'),mp.mpc('-0.01','0.03')),(mp.mpc('0.001','0.1'),mp.mpc('0.002','-0.05'))]:
    a=s+u; b=t+v
    # parity-weighted sum
    P=mp.mpc(0)
    inv={'triv':'triv','quad':'quad','chi':'chib','chib':'chi'}
    for key in chars:
        P+=(-1 if par[key]==1 else 1)*L(a,key)*L(b,inv[key])/(L(s,key)*L(t,inv[key]))
    # h_e
    h=[X(e,1-b)*X(e,1-a) for e in (0,1)]
    Rv=R(1-b,1-a,s,t); R0=R(a,b,s,t)
    rhs=(2*Rv-(h[0]+h[1])*R0)/(h[0]-h[1])
    print("u,v=",u,v," parity sum - formula =", abs(P-rhs), " scale=",abs(P),flush=True)
