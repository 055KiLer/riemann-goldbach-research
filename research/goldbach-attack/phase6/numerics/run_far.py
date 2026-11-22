import sys,time,os,json
sys.path.insert(0,'.')
from farN_core import FarModel

def run(p,H,m,K=8,label=''):
    t0=time.time()
    mod=FarModel(p,H=H,m=m,K=K,verbose=True); mod.build_C(); r=mod.result()
    r['label']=label
    print("FARPOINT "+json.dumps({k:(float(v) if isinstance(v,(int,float)) else v) for k,v in r.items()}),flush=True)
    with open('cache/farN_results.jsonl','a') as f:
        f.write(json.dumps({k:(float(v) if isinstance(v,(int,float)) else v) for k,v in r.items()})+'\n')
    return r

if __name__=='__main__':
    # args: H m K p1 p2 ...
    H=float(sys.argv[1]); m=int(sys.argv[2]); K=int(sys.argv[3])
    for p in [int(x) for x in sys.argv[4:]]:
        run(p,H,m,K,label=f"H{H}_m{m}_K{K}")
