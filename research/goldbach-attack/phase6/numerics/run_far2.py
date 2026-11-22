import sys,time,os,json
sys.path.insert(0,'.')
import numpy as np
from farN_core import FarModel
def run(p,H,m,K=4,gd=np.complex128):
    t0=time.time()
    mod=FarModel(p,H=H,m=m,K=K,verbose=True,gdtype=gd); mod.build_C(); r=mod.result()
    rec={k:(float(v) if isinstance(v,(int,float)) else v) for k,v in r.items()}
    print("FARPOINT "+json.dumps(rec),flush=True)
    with open('cache/farN_results.jsonl','a') as f: f.write(json.dumps(rec)+'\n')
if __name__=='__main__':
    gd=np.complex64 if os.environ.get('GD')=='c64' else np.complex128
    run(int(sys.argv[1]),float(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),gdtype if False else gd)
