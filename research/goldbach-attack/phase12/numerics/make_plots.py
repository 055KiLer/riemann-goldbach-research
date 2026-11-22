import json, math, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import defaultdict
D=json.load(open('logs_delta.json')); G=defaultdict(list)
for r in D: G[(r['q'],r['X1'],r['X2'],r['model'],r['eta'])].append(r)
rows=[]
for k,rr in G.items():
    q,N,M,m,e=k
    if N!=M: continue
    rows.append(dict(q=q,X=N,A=0.5*math.log(N*N)/math.log(q),model=m,eta=e,
                     Delta=float(np.mean([r['absDelta_lead'] for r in rr])),
                     Dmax=float(np.max([r['absDelta_lead'] for r in rr])),
                     qW=float(np.mean([r['qW'] for r in rr])),
                     ScSd=float(np.mean([r['ScSd'] for r in rr]))))
fig,axes=plt.subplots(1,3,figsize=(16,5))
# (a) Delta vs X for eta=.05 and .2, rat model
ax=axes[0]
for eta,mark in [(0.05,'o'),(0.2,'s')]:
    for q,c in [(53,'tab:blue'),(101,'tab:orange'),(199,'tab:green'),(1009,'tab:red')]:
        rs=sorted([r for r in rows if r['model']=='rat' and abs(r['eta']-eta)<1e-9 and r['q']==q],key=lambda r:r['X'])
        if rs: ax.loglog([r['X'] for r in rs],[r['Delta'] for r in rs],mark+'-',color=c,label=f'q={q},η={eta}')
ax.set_xlabel('X');ax.set_ylabel(r'$|\Delta|$ (mean over shifts)');ax.set_title('(a) net wrap quantity Δ, rat model');ax.legend(fontsize=6);ax.grid(True,which='both',alpha=.3)
# (b) cancellation quality Delta/(qW+ScSd) vs A
ax=axes[1]
for model,mark in [('crit','o'),('rat','s')]:
    for eta,c in [(0.05,'tab:blue'),(0.2,'tab:red')]:
        rs=[r for r in rows if r['model']==model and abs(r['eta']-eta)<1e-9]
        if rs:
            A=[r['A'] for r in rs];y=[r['Delta']/(r['qW']+r['ScSd']+1e-300) for r in rs]
            ax.semilogy(A,y,mark,color=c,label=f'{model},η={eta}')
ax.set_xlabel('A=log X/log q');ax.set_ylabel(r'$|\Delta|/(|qW|+|S_cS_d|)$');ax.set_title('(b) cancellation quality (improves with A)');ax.legend(fontsize=7);ax.grid(True,alpha=.3)
# (c) rho = Delta / q^(1-eta*A) for rat
ax=axes[2]
for eta,mark in [(0.05,'o'),(0.2,'s')]:
    for q,c in [(53,'tab:blue'),(101,'tab:orange'),(199,'tab:green'),(1009,'tab:red')]:
        rs=sorted([r for r in rows if r['model']=='rat' and abs(r['eta']-eta)<1e-9 and r['q']==q],key=lambda r:r['A'])
        if rs:
            A=[r['A'] for r in rs];y=[r['Delta']/r['q']**(1-r['eta']*r['A']) for r in rs]
            ax.semilogy(A,y,mark+'-',color=c,label=f'q={q},η={eta}')
ax.axhline(1.0,color='k',ls='--',lw=1)
ax.set_xlabel('A');ax.set_ylabel(r'$\rho=|\Delta|/q^{1-\eta A}$');ax.set_title('(c) wrap condition ρ≤1 (below dashed = c=A feasible)');ax.legend(fontsize=6);ax.grid(True,which='both',alpha=.3)
plt.tight_layout(); plt.savefig('wrap_plots.png',dpi=130)
print('saved wrap_plots.png')
