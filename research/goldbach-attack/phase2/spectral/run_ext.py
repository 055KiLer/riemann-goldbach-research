"""Extended N-search: Li-Liu finite model ratio at N>e^10."""
import os, sys, time, numpy as np
os.environ['EIG']='eigsh'
import model as MOD
from math import log as mlog

def fac_stats(N):
    fs=[]; n=N; d=2
    while d*d<=n:
        if n%d==0:
            fs.append(d)
            while n%d==0: n//=d
        d+=1
    if n>1: fs.append(n)
    phi=N
    for p in fs: phi=phi//p*(p-1)
    return fs, phi, len(fs)

OUT='cache/results_ext.txt'
HDR='H N factorization omega phi S(N) delta_N lambda_max ||C||/delta min_eig max_eig Cmax mode time_s\n'

def do_run(H, N, m=16, outfile=OUT):
    t0=time.time()
    fs, phi, omega = fac_stats(N)
    res = MOD.build_model(N=N, H=H, m=m)
    ev = np.asarray(res['ev']); S=res['delta']; delta=res['delta']
    am=np.abs(ev).max(); ratio=am/delta
    fs_str='*'.join(map(str,fs))
    line=f"{H} {N} {fs_str} {omega} {phi} {res['S']:.10g} {delta:.10g} {am:.10g} {ratio:.10g} {ev.min():.10g} {ev.max():.10g} {res['Cmax']:.10g} {res['mode']} {time.time()-t0:.1f}"
    print("RESULT: "+line, flush=True)
    with open(outfile,'a') as f: f.write(line+'\n')
    return dict(H=H,N=N,fs=fs_str,omega=omega,phi=phi,S=res['S'],delta=delta,lam=am,ratio=ratio,line=line)

if __name__=='__main__':
    mode = sys.argv[1] if len(sys.argv)>1 else 'h40'
    if not os.path.exists(OUT):
        with open(OUT,'w') as f: f.write(HDR)
    if mode=='h40':
        # order by increasing phi (cost)
        for N in [39270, 43890, 46410, 53130, 67830, 72930, 90090, 40022]:
            print(f"=== starting H=40 N={N} ===", flush=True)
            try: do_run(40, N)
            except Exception as e:
                print(f"FAILED N={N}: {type(e).__name__}: {e}", flush=True)
    elif mode=='h40more':
        for N in [30018, 39994]:
            print(f"=== starting H=40 N={N} ===", flush=True)
            try: do_run(40, N)
            except Exception as e:
                print(f"FAILED N={N}: {type(e).__name__}: {e}", flush=True)
    elif mode=='h80_40022':
        print("=== starting H=80 N=40022 ===", flush=True)
        do_run(80, 40022)
    elif mode=='p2':
        for N in [60022, 100042, 102102]:
            print(f"=== starting H=40 N={N} ===", flush=True)
            try: do_run(40, N)
            except Exception as e:
                print(f"FAILED N={N}: {type(e).__name__}: {e}", flush=True)
    elif mode=='mesh':
        FN='cache/results_mesh.txt'
        with open(FN,'a') as f: f.write('H m N phi S delta lambda ratio mode time_s\n')
        for m,N in [(8,40022),(32,40022)]:
            print(f"=== mesh m={m} N={N} H=40 ===", flush=True)
            try: do_run(40, N, m=m, outfile=FN)
            except Exception as e:
                print(f"FAILED m={m}: {type(e).__name__}: {e}", flush=True)
    elif mode=='h20_200006':
        print("=== H=20 N=200006 ===", flush=True)
        do_run(20, 200006)
    elif mode in ('h60','h80'):
        H=int(mode[1:])
        Ns = [int(x) for x in sys.argv[2:]]
        for N in Ns:
            print(f"=== starting H={H} N={N} ===", flush=True)
            try: do_run(H, N)
            except Exception as e:
                print(f"FAILED N={N}: {type(e).__name__}: {e}", flush=True)
