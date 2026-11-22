import sys, numpy as np
import model as MOD
H=float(sys.argv[1]); m=int(sys.argv[2]); N=int(sys.argv[3])
res=MOD.build_model(N=N,H=H,m=m)
ev=np.asarray(res['ev']); delta=res['delta']
line=f"H={H:g} m={m} N={N} phi={res['phi']} S={res['S']:.10g} delta={delta:.10g} lambda_max={np.abs(ev).max():.10g} ratio={np.abs(ev).max()/delta:.10g} |C|max={res['Cmax']:.6g} mode={res['mode']}"
print("MESHRESULT "+line, flush=True)
with open("cache/results_mesh.txt","a") as f: f.write(line+"\n")
