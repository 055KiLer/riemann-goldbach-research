import sys; sys.path.insert(0,'.')
import ramified as R
from multiprocessing import Pool
from group import Grp
import math, mpmath as mp
if __name__=='__main__':
    with Pool(4) as pool:
        g=Grp(256)
        print('q',g.q,'phi',g.phi,'prim',g.phistar,flush=True)
        orth=R.orthogonality_check(g); print('orth',[(o['u'],o['err']) for o in orth],flush=True)
        a=mp.mpc(0.5,0.7); b=mp.mpc(0.5,1.3); s=mp.mpc(0.6,0.4); t=mp.mpc(0.6,2.1)
        Eq,ok=R.E_of(g,a,b,s,t,pool)
        M=R.Mq(a,b,s,t,256,g.phistar,g.Me)
        print('E',Eq,'M',M,'|E-M|',abs(mp.mpc(Eq)-M),'sqrtq',math.sqrt(256), 'ok',ok,flush=True)
        Ld,_=R.Lvalues(g,mp.mpc(1.5,0.8),pool)
        k=int(__import__('numpy').nonzero(g.prim)[0][0])
        d=R.direct_L(g,mp.mpc(1.5,0.8),k,N=200000)
        print('direct-L rel err',abs(Ld[k]-d)/abs(d),flush=True)
