import numpy as np, math
def Mmat(alpha, beta=0.125, U=None, h=0.1):
    if U is None: U = max(12.0, 4.0/alpha)
    n=int(U/h)+1; u=np.arange(n)*h
    UU,VV=np.meshgrid(u,u,indexing='ij'); M=np.zeros_like(UU)
    for sig in (alpha,beta):
        M += (math.pi/(1+sig))*np.exp(-sig*(UU+VV)-(1+sig)*np.abs(UU-VV))
    return M*h
print("alpha   N      logN    ||M||   ||M||/sqrt(logN)  tr   HS2")
for N in [10**3,10**4,10**5,10**6,10**7,10**8]:
    alpha=1.0/math.log(N); M=Mmat(alpha)
    ev=np.linalg.eigvalsh((M+M.T)/2)
    lN=math.log(N)
    print(f"{alpha:.4f} 1e{int(math.log10(N)):d} {lN:7.3f}  {ev[-1]:8.4f}  {ev[-1]/math.sqrt(lN):8.4f}  {np.trace(M):8.3f}  {np.sum(ev**2):8.3f}")
