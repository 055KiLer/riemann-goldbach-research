"""Extension: 10 generic shifts for 2^e (e=8..16) and 3^e (e=3..6), own code, corrected A_q mask."""
import sys, random, json, math, time
sys.path.insert(0,'.')
import ramified as R
from multiprocessing import Pool
if __name__=='__main__':
    random.seed(777)
    shifts=[]
    while len(shifts)<10:
        ia=round(random.uniform(-2,2),3); ib=round(random.uniform(-2,2),3)
        if abs(ia+ib)<0.5: continue
        shifts.append((ia,ib,round(random.uniform(-2,2),3),round(random.uniform(-2,2),3)))
    fam={'2^e':[2**e for e in (8,10,12,14,16)],'3^e':[3**e for e in (3,4,5,6)]}
    with Pool(14) as pool:
        res=R.run_families(pool,fam,[],shifts,'../logs/ramified_ext.json')
    print('DONE')
