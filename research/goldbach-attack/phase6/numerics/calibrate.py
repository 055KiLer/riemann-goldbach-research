import sys,time,os,json
sys.path.insert(0,'.')
from farN_core import FarModel

def run(p,H,m,K=8):
    t0=time.time()
    mod=FarModel(p,H=H,m=m,K=K,verbose=False); mod.build_C(); r=mod.result()
    print(f"CAL p={p} N={2*p} H={H} m={m} K={K}: lam={r['lam']:.8f} ratio={r['ratio']:.8f} C={r['C']:.5f} |C|max={r['Cmax']:.3e} wall={time.time()-t0:.1f}s",flush=True)
    rec={k:(float(v) if isinstance(v,(int,float)) else v) for k,v in r.items()}
    with open('cache/calibration.jsonl','a') as f: f.write(json.dumps(rec)+'\n')

if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='p500083':
        for H,m in [(8.0,4),(6.0,4),(4.0,8),(4.0,4),(4.0,2),(2.0,8),(2.0,16),(2.0,4)]:
            run(500083,H,m)
    elif mode=='p2000003':
        for H,m in [(4.0,2),(2.0,8),(2.0,4),(4.0,8)]:
            run(2000003,H,m)
