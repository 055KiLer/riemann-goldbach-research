"""Extension: 10 generic shifts for mixed ramified families 4p,8p,9p with more q points (own code)."""
import sys, random
sys.path.insert(0,'.')
import ramified as R
from multiprocessing import Pool
if __name__=='__main__':
    random.seed(4242)
    shifts=[]
    while len(shifts)<10:
        ia=round(random.uniform(-2,2),3); ib=round(random.uniform(-2,2),3)
        if abs(ia+ib)<0.5: continue
        shifts.append((ia,ib,round(random.uniform(-2,2),3),round(random.uniform(-2,2),3)))
    fam={
      '4p':[4*p for p in (1009,1259,2003,2503,3001,4001)],
      '8p':[8*p for p in (1009,1259,2003,2503)],
      '9p':[9*p for p in (1009,1013,2003,4001)],
    }
    with Pool(14) as pool:
        res=R.run_families(pool,fam,[],shifts,'../logs/ramified_mixed_ext.json')
    print('DONE')
