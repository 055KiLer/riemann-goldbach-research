import numpy as np, time
from math import log as mlog, pi
exec(open('checkE.py').read().split('# ---------------- double contour integral')[0])
# now we have P,Dmat,Kmat,E,ts,etc.
for nm,X in [('P',P),('D',Dmat),('K',Kmat),('E',E)]:
    i=np.unravel_index(np.abs(X).argmax(),X.shape)
    print(f"{nm}: |max|={np.abs(X).max():.4e} at (j,k)={i} ts=({ts[i[0]]},{ts[i[1]]}) val={X[i]},  |min|={np.abs(X).min():.2e}, median|.|={np.median(np.abs(X)):.3f}")
# check a few entries
for j,k in [(M//2,M//2),(M//2,M//2+1),(0,M-1),(M//2,M-1),(0,0)]:
    print(f"E[{j},{k}]: ts=({ts[j]},{ts[k]}) P={P[j,k]:.4f} D={Dmat[j,k]:.4f} K={Kmat[j,k]:.4f} E={E[j,k]:.4f}")
