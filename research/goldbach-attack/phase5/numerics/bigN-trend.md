# Phase-5: large-N trend of the Li–Liu finite model (N = 2p)

**Task:** task-13. **Author:** spectral-numerics. **Date:** 2026-11-21.
**Question:** does \(\|C\|/\delta_N\) at \(N=2p\) stay \(>1\) as \(N\to\infty\), or does it cross below 1
(asymptotically supporting Hypothesis R)? Define, following the Lead's convention,
\[
Y:=\lambda_{\max}\sqrt N,\qquad C:=Y/\sqrt{S(N)},\qquad
\text{ratio}=\frac{\|C\|}{\delta_N}=\frac{C}{(\log N)^{3/2}} .
\]
If \(C\) stays bounded (prior points \(C\approx44.7\pm5\)), the crossing is at
\(\log N\approx C^{2/3}\), i.e. \(N^*\approx 3\text{–}7\times10^5\).

All labels **[数值]**; finite model only, no proof/disproof claims.

## 0. Summary: final N=2p table [数值]

H/m: 10/8 unless stated; the two largest-N points use H=8, m=8, K=32 EM terms (+0.75% H-bias
correction not applied in the table; ≲2% systematic). ratio=\(\lambda_{\max}/\delta_N\),
Y=\(\lambda_{\max}\sqrt N\), C=Y/√S.

| N=2p | p | H,m | \(\lambda_{\max}\) | \(\delta_N\) | ratio | Y | C |
|---|---|---|---|---|---|---|---|
| 30030 (mixed reference) | — | 40,16 | 0.3574618 | 0.432310 | 0.826864 | 61.95 | 27.35 |
| 39994 | 19997 | 40,16 | 0.2125060 | 0.198197 | 1.0722 | 42.50 | 36.98 |
| 40022 | 20011 | 40,16 | 0.2757214 | 0.198147 | 1.3915 | 55.16 | 48.00 |
| 60022 | 30011 | 40,16 | 0.2072516 | 0.171170 | 1.2108 | 50.78 | 44.19 |
| 100042 | 50021 | 40,16 | 0.1660613 | 0.141924 | 1.1701 | 52.52 | 45.71 |
| 200006 | 100003 | 20,16 | 0.1246573 | 0.109569 | 1.1377 | 55.75 | 48.52 |
| 400006 | 200003 | 10,8 | 0.0866444 | 0.084169 | 1.0294 | 54.80 | 47.69 |
| 700006 | 350003 | 10,8 | 0.0769050 | 0.067811 | 1.1341 | 64.35 | 55.99 |
| 999958 | 499979 | 10,8 | 0.0655123 | 0.059006 | 1.1103 | 65.51 | 57.01 |
| 1000018 | 500009 | 10,8 | 0.0631964 | 0.059005 | 1.0710 | 63.20 | 55.00 |
| 1000166 | 500083 | 10,8 | 0.0558708 | 0.059001 | 0.9469 | 55.87 | 48.63 |
| 1000166 (mesh) | 500083 | 10,16 | 0.0553755 | 0.059001 | 0.9385 | 55.38 | 48.20 |
| 1000166 (H) | 500083 | 20,8 | 0.0566146 | 0.059001 | 0.9595 | 56.62 | 49.27 |
| 1500038 | 750019 | 10,8 | 0.0628448 | 0.050314 | 1.2491 | 76.97 | 66.99 |
| 1500038 (H-test) | 750019 | 20,4 | 0.0632271 | 0.050314 | 1.2567 | 77.44 | 67.39 |
| 1500166 | 750083 | 10,8 | 0.0532322 | 0.050312 | 1.0580 | 65.20 | 56.74 |
| 1999966 | 999983 | 10,8 | 0.0513074 | 0.044902 | 1.1426 | 72.56 | 63.15 |
| 2011102 | 1005551 | 10,8 | 0.0511423 | 0.044804 | 1.1415 | 72.53 | 63.12 |
| 3000014 | 1500007 | 8,8 | 0.0422593 | 0.038210 | 1.1060 | 73.19 | 63.70 |
| 4000006 | 2000003 | 8,8 | 0.0335526 | 0.034053 | 0.9853 | 67.11 | 58.41 |

## 1. Method

Validated phase-2/4 pipeline (`model.py`: Hermitian recipe of LL Appendix B, \(H\), mesh \(1/m\),
2562-style two-line nodes). For \(N=2p\) the character group \((\mathbb Z/2p)^*\cong(\mathbb Z/p)^*\)
is cyclic of order \(p-1\), units up to \(p-1\); the code uses the discrete-log table and a single
FFT per node to obtain all \(\chi\) (cost \(O(\varphi\log\varphi)\) per node instead of
\(O(\varphi N)\)). Same \(D_N\) (zeta-factor extraction, adaptive EM) and \(\widetilde P_N\)
zeta-extraction as phase 2; \(|C|_{\max}\), Hermiticity defects reported per run.
Copies of the validated modules are in this directory; caches in `phase5/numerics/cache/`.

Commands:
```
cd phase5/numerics
EIG=eigsh python3 model.py 20 1000166 8
EIG=eigsh python3 model.py 20 1500038 8
```

## 2. Results: the N=2p trend (all [数值])

Reference formula: \(\delta_N=\sqrt{S(N)/N}(\log N)^{3/2}\), \(Y=\lambda_{\max}\sqrt N\),
\(C=Y/\sqrt{S(N)}\), ratio \(=\|C\|/\delta_N=C/(\log N)^{3/2}\).

| N=2p | H | m | \(\lambda_{\max}\) | \(\delta_N\) | Y | C | ratio | notes |
|---|---|---|---|---|---|---|---|---|
| 40022 (p=20011) | 40 | 16 | 0.2757214 | 0.198147 | 55.16 | 48.00 | 1.39152 | phase-4 (m=64 stable, H-stable) |
| 39994 (p=19997) | 40 | 16 | 0.2125060 | 0.198197 | 42.50 | 36.98 | 1.07220 | phase-4 |
| 60022 (p=30011) | 40 | 16 | 0.2072516 | 0.171170 | 50.78 | 44.19 | 1.21079 | phase-4 |
| 100042 (p=50021) | 40 | 16 | 0.1660613 | 0.141924 | 52.52 | 45.71 | 1.17007 | phase-4 |
| 200006 (p=100003) | 20 | 16 | 0.1246573 | 0.109569 | 55.75 | 48.52 | 1.13771 | phase-4 |
| **1000166 (p=500083)** | **20** | **8** | **0.05661459** | **0.0590015** | **56.62** | **49.27** | **0.959545** | **first <1 point** |
| 1000166 | 10 | 8 | 0.05587077 | 0.0590015 | 55.87 | 48.62 | 0.946939 | H-sensitivity |

**Updated observation (with the multi-p sampling):** \(C\) is *bounded but fluctuating*, and
the ratio is **not monotonically crossing 1**; it fluctuates around \(C/(\log N)^{3/2}\) with
\(p\)-dependent scatter.

At the **same scale \(N\approx10^6\)** three different primes give (H=10, m=8):
\(p=500083:\ \lambda=0.055871,\ C=48.63,\ \text{ratio}=0.9469\);
\(p=499979:\ \lambda=0.065512,\ C=57.01,\ \text{ratio}=1.1103\);
\(p=500009:\ \lambda=0.063196,\ C=55.00,\ \text{ratio}=1.0710\);
i.e. **ratio mean ≈1.043, range [0.947, 1.110]**; the earlier single "first sub-1 point" at
\(p=500083\) is *one draw* from a distribution straddling 1, not a decisive crossing.
At \(N\approx1.5\text{–}2\cdot10^6\): \(p=750019:\) ratio 1.249 (H=10), 1.257 (H=20,m=4);
\(p=1005551\) (\(N=2.01\cdot10^6\)): ratio 1.141. So the sampled points are above 1 there.
The distribution of \(C\) over all points: mean ≈54, std ≈8, min 37, max 67; \(C\) shows a mild
*increase* with \(N\) in the larger-\(N\) half (mean ≈53.5 at \(N=10^6\), ≈65 at
\(N=1.5\text{–}2\cdot10^6\)), but the sample is small and \(p\)-fluctuation dominates.
If \(C\propto(\log N)^{\alpha}\) with \(\alpha<3/2\), the ratio still decays like
\((\log N)^{\alpha-3/2}\to0\); if \(C\) were truly bounded, ratio \(\to0\) like
\((\log N)^{-3/2}\). Either way the data are compatible with eventual sub-1 ratios, but the
present range \(N\le2\cdot10^6\) has ratio of order 1 with \(\pm30\%\) scatter. A statement
about asymptotic R needs an **upper envelope over \(p\)**, not a single \(p\).

**IMPORTANT interpretation (transfer direction):** the mesh/height-converged eigenvalue
\(\lambda_{\max}\) of the finite model is a Rayleigh quotient of the true kernel, and by
LL Prop. 5.3 the boundary kernel operator annihilates \(H_N^\perp\) and maps into \(H_N\), so
\(\lambda_{\max}\le\|T_N\|\) (lower bound). Hence ratio \(<1\) at \(N=1000166\)
does **not** prove \(\|T_N\|\le\delta_N\) (R could still fail); it only removes the
finite-model **evidence against** R: the model no longer exhibits a failure at this \(N\).
[数值/有限模型]

## 3. H-scaling at large N, and mesh convergence

Height bias \(\Delta(H_1,H_2)=\lambda(H_2)/\lambda(H_1)-1\) (same mesh \(m=8\) unless noted):
- \(N=40022\): \(\lambda(H=10)=0.2678331\), \(\lambda(H=20)=0.2731279\): \(\Delta(10,20)=+1.98\%\).
- \(N=400006\) (p=200003): \(\lambda(H=10,m=8)=0.08664437\) (ratio 1.02941); the team's
  \(H=20,m=8\) value ratio 1.0461 corresponds to \(\lambda=0.088045\): \(\Delta(10,20)=+1.62\%\).
- \(N=1000166\): \(\lambda(H=10)=0.05587077\), \(\lambda(H=20)=0.05661459\): \(\Delta(10,20)=+1.33\%\);
  \(\lambda(H=40,m=16)=0.2757214\) at \(N=40022\) vs \(H=20,m=8\) \(0.2731279\): \(\Delta(20,40)=+0.95\%\).
  So the H-bias is ~1–2% and does not grow dramatically with \(N\) (calibration in progress at
  \(N=400006\)); even applying the full H=10 bias would give ratio(1000166,H→∞)≈
  \(0.9469\times(1+\Delta)\) with \(\Delta\approx2\text{–}3\%\) still \(<1\).
- Mesh convergence established in phase 4 at \(N=40022\): \(\lambda_{\max}(m=8/16/32/64)=
  0.2761147/0.2757214/0.27572427/0.27572428\) (m=32→64: \(4\times10^{-8}\)).

*Additional H-scaling numbers (N=400006, N=1500038) to be appended.*

**Large-N mesh check (N=1000166, H=10):** \(m=8:\ \lambda_{\max}=0.05587077\), ratio 0.94694;
\(m=16:\ \lambda_{\max}=0.05537546\), ratio 0.93854 — m=8 to m=16 change **−0.89%**, so m=8
large-\(N\) numbers are reliable at the ~1% level (as at \(N=40022\): m=8→16→32→64 =
0.14%, 0.001%, \(4\cdot10^{-8}\)). **m=4 is unusable:** calibration
\(N=1000166,H=8,m=4\) gives \(\lambda=0.06570873\) (ratio 1.1137), +17% above m=8 — a coarse-mesh
quadrature artifact (not a height effect; H=8 subspace should give a *smaller* Rayleigh quotient).
Hence for \(N=3\text{–}4\cdot10^6\) we use H=8, m=8 with K=32 EM direct terms (validated for
|Im u|≤9, memory-saving).

## 4. Spectrum / per-character statistics

- \(N=40022\), H=20, m=8, c=1 (from the c-scan run, full spectrum of the 642×642 matrix):
  \(\mathrm{tr}(C)=0.0227949\), \(\|C\|_{\rm HS}=\sqrt{\sum\mu^2}=0.58158\),
  \(\lambda_{\max}=0.273128\); \(\mathrm{tr}\) is far smaller than \(\|C\|_{\rm HS}\)
  (sign-cancelling spectrum: λmax ≈ +0.273, λmin ≈ −0.2...). The largest HS mass comes from a
  few extreme eigenvalues.
- **Saved-C full-spectrum analyses** (all H=10, m=8, 322×322 matrices; N=3000014 H=8,m=8,
  258×258):
  | N | λmax | λmin | tr(C) | ‖C‖_HS | α-line mass | mean|Im s| | Hardy frac |
  |---|---|---|---|---|---|---|---|
  | 700006 | 0.076905 | −0.076905 | −0.01082 | 0.18480 | 77.8% | 1.13 | 0.708 |
  | 999958 | 0.065512 | −0.053840 | 0.01208 | 0.16589 | 81.2% | 1.08 | 0.676 |
  | 1000018 | 0.063196 | −0.055902 | 0.00352 | 0.16067 | 79.7% | 1.00 | 0.691 |
  | 1500166 | 0.053232 | −0.053232 | 0.00600 | 0.14318 | 78.7% | 1.06 | 0.702 |
  | 1999966 | 0.051307 | −0.051307 | 0.00023 | 0.13669 | 82.8% | 0.93 | 0.666 |
  (α-line = the Re s = 1/log N boundary, β-line = Re s = 1/8.) The spectra show strong sign
  cancellation: |tr(C)| is 1–2 orders of magnitude below ‖C‖_HS, so the HS mass is carried by
  the few extreme eigenvalues. The top eigenvector puts 78–83% of its boundary L² mass on the
  α-line, its Im s mass is concentrated near 0 (mean |Im s|≈1), and its Hardy-trace fraction is
  ≈0.67–0.71 (Lemma-5.2 Fourier representation). [数值]
- Top-eigenvector profile at \(N=40022\) (H=40, m=16, phase-4): roughly balanced between the two
  boundary lines, \((\sim83\%\) of its \(L^2\) mass in the Hardy trace subspace; see
  `spectral-numerics-extended.md` §4b).

[数值]

## 5. c-dependence (LL Appendix A: α = c/log N, β=1/8 fixed) [数值]

N=40022, H=20, m=8, same validated assembly; only the line position α=c/logN is changed.
(δ_N does not depend on c; it is defined by S(N),N.)

| c | α | λ_max | ratio λ/δ_N | Y=λ√N | C=Y/√S | Q-weighted λ e^{2c} | tr(C) | ‖C‖_HS |
|---|---|---|---|---|---|---|---|---|
| 0.25 | 0.023591 | 1.54132 | 7.7787 | 308.35 | 268.34 | 308.35 | 0.30556 | 4.5200 |
| 0.50 | 0.047182 | 0.68520 | 3.4581 | 137.08 | 119.29 | 9.40* | 0.03999 | 1.7366 |
| 0.75 | 0.070774 | 0.40662 | 2.0521 | 81.35 | 70.79 | 9.20* | 0.02727 | 0.9248 |
| 1.00 | 0.094365 | 0.27313 | 1.3784 | 54.64 | 47.55 | 10.19* | 0.02279 | 0.5816 |
| 1.25 | 0.117956 | 0.20081 | 1.0134 | 40.17 | 34.96 | 12.35* | 0.01852 | 0.4137 |
| 2 | invalid | — | — | — | — | — | — | — |

\(c=2\) is inadmissible at these \(N\): \(\alpha=2/\log N>\beta=1/8\) (empty strip);
the maximal admissible value is \(c<\beta\log N\approx1.32\) (\(N=40022\)), \(1.53\) (\(N=200006\)).

**Reading:**
- Decreasing \(c\) (wider strip) makes the ratio *much worse* (7.8 at c=0.25, 3.5 at c=0.5).
- Increasing \(c\) toward the strip-collapse limit decreases \(\|T_{N,c}\|\) (ratio 1.013 at c=1.25)
  but does **not** reach below 1 at \(N=40022\).
- The correct target quantity in LL is \(Q_{N,c}\|T_{N,c}\|\) (the Riesz vector norm satisfies
  \(Q_{N,c}\asymp e^{2c}\) in the c-scaling, LL (A.2)). Multiplying the measured ratios by
  \(e^{2c}\): c=0.5: 3.46×e^{1}=9.40; c=0.75: 2.05×e^{1.5}=9.20; c=1: 1.38×e^{2}=10.19;
  c=1.25: 1.01×e^{2.5}=12.35 — the product is minimized around **c≈0.75–1.0**, and the
  paper's c=1 is (near) optimal \([数量级论证]\). So "escape by changing c" does not work for
  the quantity that actually enters the Goldbach error, in this finite model.

## 5b. The critical exponent \(a\) in \(C\propto(\log N)^a\) [数值]

The asymptotic behaviour of the finite-model ratio is controlled by the log-exponent \(a\):
\[
C\simeq k(\log N)^a \quad\Longrightarrow\quad
\text{ratio} \simeq k(\log N)^{a-3/2}.
\]
- \(a<3/2\): ratio \(\to0\) (asymptotically R-plausible); crossing where
  \(\log N_*=e^{\ln k/(3/2-a)}\), extremely sensitive to \(a\).
- \(a\ge3/2\): the ratio does **not** tend to 0; the finite model keeps providing
  counter-evidence to R at larger \(N\).

Fits (16 \(N=2p\) points; H=10-equivalent; the last two points use H=8,m=8,K=32 with a
\(+0.75\%\) H-bias correction; caveat: H/mesh systematics \(\lesssim2\%\)):
- **all 16 points:** \[\log C = 0.987 + (1.160\pm0.175)\,\log\log N,\qquad
  C=2.684(\log N)^{1.160\pm0.175},\qquad \text{ratio}\propto(\log N)^{-0.340\pm0.173}.\]
- large-\(N\) subset \(N\ge4\cdot10^5\) (11 points, logN 12.9–15.2):
  \(C=0.697(\log N)^{1.67\pm0.53}\), ratio exponent \(+0.17\pm0.53\).
- bucket means of \(C\) (logN bins [10,11),[11,12),[12,13),[13,14),[14,15),[15,16)):
  \(42.5,\ 45.0,\ 48.1,\ 54.3,\ 62.9,\ 58.8\) and bucket means of the ratio:
  \(1.201,\ 1.161,\ 1.075,\ 1.069,\ 1.143,\ 0.993\)
  (the last bin has a single point, \(N=4\cdot10^6\)).
- Over all 16 points: mean ratio \(=1.116\), and **14/16 sampled moduli have ratio >1**.

**The critical exponent is not resolved.** The critical value for asymptotic behaviour is
\(a=3/2\): \(a<3/2\) gives ratio \(\to0\) (asymptotically R-compatible, crossing at
\(\log N_*=e^{0.987/(3/2-a)}\), i.e. \(N_*\approx8\cdot10^7\) for \(a=1.16\) but
astronomically large for \(a=1.4\)); \(a\ge3/2\) gives no decay. The global fit gives
\(a=1.16\pm0.18\) (a=1.5 at \(1.9\sigma\)), the large-\(N\) fit gives \(a=1.67\pm0.53\)
(a=1.5 inside). **Honest range: \(a\approx1.2\text{–}2.2\); 16 single-\(p\) points with
\(\pm30\%\) scatter cannot resolve \(a\) to \(\pm0.1\).** What *is* established is that
the ratio is \(O(1)\) (mean 1.12, no monotone decay) throughout
\(N=4\cdot10^4\text{–}4\cdot10^6\), with two of 16 points below 1
(\(N=1000166\): 0.939–0.960 depending on H/m; \(N=4000006\): 0.985) and the rest above.

## 6. Verdict [数值] (finite model only; no proof/disproof claims)

**Established by the 16-point N=2p scan (H=10-equivalent, H/mesh systematics ≲2%):**
1. **The ratio is O(1) and does not decay over the sampled range.** All 16 single-\(p\) ratios
   scatter in [0.94,1.39]; mean 1.116; **14 of 16 are >1** (the exceptions: \(N=1000166\),
   ratio 0.939–0.960 depending on H/m, and \(N=4000006\), ratio 0.985). By scale:
   \(N\approx10^6\) (3 primes): 0.947/1.110/1.071 (mean 1.043);
   \(N\approx1.5\cdot10^6\) (2 primes): 1.249/1.058;
   \(N\approx2\cdot10^6\) (2 primes): 1.141/1.143;
   \(N\approx3\cdot10^6\): 1.106; \(N\approx4\cdot10^6\): 0.985.
   Thus the earlier "bounded \(C\) ⇒ crossing at \\(N\approx6\cdot10^5\\)" reading is **falsified**:
   no monotone crossing occurs; the finite model hovers around ratio ~1.1 up to
   \(N=4\cdot10^6\).
2. **\(C=\lambda_{\max}\sqrt N/\sqrt S\) grows slowly with \(\log N\)**: bucket means
   \(42.5,45.0,48.1,54.3,62.9,58.8\) for \(\log N\in[10,11),\dots,[15,16)\); global fit
   \(C=2.684(\log N)^{1.160\pm0.175}\), i.e. ratio \(\propto(\log N)^{-0.340\pm0.173}\).
   Large-\(N\) subset (\(N\ge4\cdot10^5\), 11 points): \(a=1.67\pm0.53\).
   **The critical exponent \(a=3/2\) is not resolved** (global 1.16±0.18, large-\(N\) 1.67±0.53;
   honest range \(a\approx1.2\text{–}2.2\)). If \(a<3/2\) the ratio eventually decays to 0
   (crossing at \(N_*\approx8\cdot10^7\) for \(a=1.16\), or astronomically far for larger \(a\));
   if \(a\ge3/2\) it does not. The present data cannot decide which.
3. **One-sided transfer (LL Prop. 5.3):** \(\lambda_{\max}\) is a Rayleigh quotient of the true
   kernel, hence \(\lambda_{\max}\le\|T_N\|\).
   Ratio \(>1\) \(\Rightarrow \|T_N\|>\delta_N\): numerical evidence **against** Hypothesis R at
   that modulus. Ratio \(<1\) gives no information about \(\|T_N\|\).
   Therefore the **14 moduli with ratio>1 are finite-model counter-evidence to R inside the
   claimed range** \(N>e^{10}\); the two sub-1 values do not support R.
4. **Robustness:** mesh at \(N=1000166\): m=8→16 changes \(\lambda\) by −0.89%; at \(N=40022\),
   m=8→16→32→64: 0.14%, 0.001%, \(4\cdot10^{-8}\). H-bias H=10→20 is +1.3–2.0% (decreasing with
   \(N\)); H=20→40 ≈+1%. Coarse mesh m=4 is unusable (+17% quadrature artifact at \(N=10^6\)).
   Hermiticity defects \(<10^{-15}\), \(|C|_{\max}\le1.4\cdot10^{-2}\); pipeline validated in
   phase 2/4 (paper's \(N=30030\) reproduced to 6 digits).
5. **c-dependence:** no c escapes: ratios at c=0.5/0.75/1.0/1.25 are 3.46/2.05/1.38/1.01, and the
   true target quantity \(Q_{N,c}\|T_{N,c}\|\) carries a factor \(e^{2c}\), giving
   ≈9.4/9.2/10.2/12.4 — minimized at c≈0.75–1.0, so the paper's c=1 is near-optimal; c=2 is
   inadmissible (\(\alpha>\beta\)). [数量级论证]
6. **Spectrum:** |tr(C)| is 1–2 orders below ‖C‖_HS (sign cancellation; HS mass in extreme
   eigenvalues); the top eigenvector concentrates 78–83% on the α-line, mean |Im s|≈0.9–1.1,
   Hardy-trace fraction ≈0.67–0.71.

**Bottom line:** the finite model at \(N=2p\) gives ratio \(O(1)\) (mean 1.12) with no decay over
\(N=4\cdot10^4\text{–}4\cdot10^6\), and ratio>1 at 14/16 sampled moduli — i.e. within LL's own
framework (one-sided transfer) it remains numerical counter-evidence against Hypothesis R
throughout that range, rather than support for its asymptotic truth. The decisive exponent
\(a\) in \(C\propto(\log N)^a\) is only bracketed to \(1.2\text{–}2.2\), so neither
"R asymptotically true" nor "R asymptotically false" can be concluded; resolving \(a=3/2\)
requires many more primes per scale (upper-envelope statistics), which is the natural next step.

## 7. Files and commands

- `model.py` (+`lmat.py`,`kernels.py`,`chars.py`,`hurwitz.py`): validated phase-2 pipeline (copy).
- `bigp_core.py`: experimental large-conductor DFT implementation (not used for final numbers; the
  phase-2 code path handles \(N=2p\) directly and was used throughout).
- Logs: `run_N*_H*.log`; saved matrices `cache/C_*.npy`; analysis `analyze_C.py`, `summarize.py`,
  `c_scan.py`, `diagnostics.py`; machine-readable `cache/cscan.txt`.
- Commands: `EIG=eigsh python3 model.py 10 999958 8` (H,m,N), etc.; c-scan: `python3 c_scan.py`.
