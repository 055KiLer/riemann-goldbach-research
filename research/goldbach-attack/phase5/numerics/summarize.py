"""Collect all N=2p finite-model results (phase-4 + phase-5 logs) into a table + per-scale stats."""
import re, glob, numpy as np, os
from math import log

def parse_log(fn):
    txt=open(fn,errors='ignore').read()
    cfg=re.search(r'cfg N=(\d+) H=([\d.]+) m=(\d+).*?delta=np.float64\(([\d.eE+-]+)\).*?S=([\d.eE+-]+)',txt)
    if not cfg: return None
    N=int(cfg.group(1)); H=float(cfg.group(2)); m=int(cfg.group(3)); delta=float(cfg.group(4)); S=float(cfg.group(5))
    lam=re.search(r'max\|eig\| = np.float64\(([\d.eE+-]+)\)',txt)
    if not lam: return None
    lam=float(lam.group(1))
    return dict(N=N,H=H,m=m,delta=delta,S=S,lam=lam,ratio=lam/delta,
                Y=lam*np.sqrt(N),C=lam*np.sqrt(N)/np.sqrt(S),
                Cmax=float((re.search(r'\|C\|max = ([\d.eE+-]+)',txt) or re.search(r'\|C\|max ([\d.eE+-]+)',txt)).group(1)) if re.search(r'\|C\|max',txt) else None)

rows=[]
for fn in glob.glob('run_*.log')+glob.glob('../../../phase2/spectral/run_*.log'):
    r=parse_log(fn)
    if r: r['file']=fn; rows.append(r)
# dedupe by (N,H,m) keeping most recent/S largest? keep all
seen={}
for r in rows:
    key=(r['N'],r['H'],r['m'])
    if key not in seen: seen[key]=r
rows=list(seen.values())
rows.sort(key=lambda r:(r['N'],r['H']))
print(f"{'N':>9} {'H':>4} {'m':>3} {'lam':>12} {'delta':>12} {'ratio':>10} {'Y':>8} {'C':>8}")
for r in rows:
    print(f"{r['N']:>9} {r['H']:>4.0f} {r['m']:>3} {r['lam']:>12.8f} {r['delta']:>12.8f} {r['ratio']:>10.6f} {r['Y']:>8.3f} {r['C']:>8.3f}")
# per-scale distribution of C and ratio, restricted to N=2p H=10/20 comparable
print("\nPer logN-scale samples (unique p):")
from collections import defaultdict
grp=defaultdict(list)
for r in rows:
    if r['N'] in (30030,): continue
    # use only H=10 results where available and H=20 for 1000166
    key=(r['N'])
    if key not in [g['N'] for g in grp[r['N']]]: pass
# simple grouping by decade of N
buckets={'4e4':[4e4,7e4],'1e5':[7e4,1.5e5],'2-4e5':[1.5e5,5e5],'1e6':[5e5,1.2e6],'1.5-2e6':[1.2e6,2.5e6]}
for name,(lo,hi) in buckets.items():
    sel=[r for r in rows if lo<=r['N']<hi and r['H']<=20]
    if not sel: continue
    Cs=[r['C'] for r in sel]; ratios=[r['ratio'] for r in sel]
    print(f"{name}: n={len(sel)} C mean={np.mean(Cs):.2f} std={np.std(Cs):.2f} min={np.min(Cs):.2f} max={np.max(Cs):.2f} | ratio mean={np.mean(ratios):.3f} range=[{np.min(ratios):.3f},{np.max(ratios):.3f}]")
