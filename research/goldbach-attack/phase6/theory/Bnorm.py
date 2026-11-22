import numpy as np, math
# B = PSD operator on H_N with kernel 1/((1+s)(1+zb)(s+zb)) = int_0^inf |k_u><k_u| du, k_u(s)=e^{-su}/(1+s)
# Gram M(u,v)=<k_u,k_v> = pi * sum_{sig in {alpha,beta}} e^{-sig(u+v)-(1+sig)|u-v|}/(1+sig)
# ||B|| = ||M|| as operator on L2(0,inf)
def Mmat(alpha, beta=0.125, U=None, h=0.05):
    if U is None: U = max(20.0, 8.0/alpha)
    n = int(U/h)+1
    u = np.arange(n)*h
    UU, VV = np.meshgrid(u,u,indexing='ij')
    M = np.zeros_like(UU)
    for sig in (alpha,beta):
        M += (math.pi/(1+sig))*np.exp(-sig*(UU+VV)-(1+sig)*np.abs(UU-VV))
    return M*h   # quadrature weight: kernel operator on L2(du): norm of M approx max eig of M*h
for N in [10**4,10**5,10**6,10**7,10**8,10**10]:
    alpha=1.0/math.log(N)
    M=Mmat(alpha)
    ev=np.linalg.eigvalsh((M+M.T)/2)
    print(f"N=1e{int(math.log10(N)):2d} alpha={alpha:.5f} dim={M.shape[0]} ||B||_approx={ev[-1]:.4f}  tr={np.trace(M):.3f}  HS2={np.sum(ev**2):.3f}")
