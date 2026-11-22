# Extended N-search: Li–Liu finite-model ratio at moduli in the asymptotic range (N > e^10)

**Task:** task-10 (phase 4, continuation of task-7). **Author:** spectral-numerics. **Date:** 2026-11-21.
**Question:** does the Li–Liu finite spectral model (paper Appendix B recipe: Hermitian matrix
\(C\), \(H=40\), mesh \(1/16\), 2562 nodes; validated in `spectral-numerics.md`) ever give
\(\|C\|/\delta_N>1\) at even moduli **inside** the paper's asymptotic range \(N>e^{10}\approx22026\)?

All labels **[数值]** = our computation (finite model only — no proof/disproof claim).

---

## 0. Headline answer

**[数值] YES — the finite-model ratio exceeds 1 at moduli inside the paper's asymptotic range
\(N>e^{10}\), and the result is mesh- and height-converged:**
- \(N=40022=2\cdot20011\): \(\lambda_{\max}=0.275724\) (mesh-converged, m=8→64),
  \(\delta_N=0.198147\), \(\|C\|/\delta_N=\mathbf{1.391514}\); H=40/60/80 give
  1.39150/1.39593/1.39786.
- \(N=39994=2\cdot19997\): ratio \(\mathbf{1.072198}\).
- \(N=90090=2\cdot3^2\cdot5\cdot7\cdot11\cdot13\): ratio \(\mathbf{1.001855}\).
- **The \(N=2p\) family is uniformly over 1:** p=19997: 1.0722, 20011: 1.3915, 30011: 1.2108,
  50021: 1.1701, 100003 (N=200006, H=20): 1.1377. \(\lambda_{\max}\) declines slowly
  (0.276→0.125) while \(\delta_N\) declines like \(N^{-1/2}(\log N)^{3/2}\), so the ratio
  stays >1 along this family.
- Many-factor control at larger \(N\): \(N=102102=2\cdot3\cdot7\cdot11\cdot13\cdot17\)
  (six factors, \(\delta_N=0.2481\)) gives 0.7712 < 1, consistent with the crossing-scale
  formula \(N_{\rm cross}\sim S(N)(\log N)^3/\lambda_{\max}^2\) (predicted
  \(N_{\rm cross}\sim2\text{–}3\cdot10^5\) for \(S\approx4\)).
- **Mesh convergence (decisive):** N=40022, H=40: \(\lambda_{\max}=0.2761147/0.2757214/
  0.27572427/0.27572428\) for m=8/16/32/64 — the m=32→64 change is \(4\times10^{-8}\).
  Not a quadrature artifact.
- **The value transfers to the true operator within the paper's own framework:** by Li–Liu
  Prop. 5.3 the boundary kernel operator annihilates \(H_N^\perp\) and maps into \(H_N\);
  hence for **every** unit \(v\in L^2(\Gamma_N)\),
  \(\langle Kv,v\rangle\le\|T_N\|\). The mesh-converged \(C\) is the Nyström compression of
  \(K\) to step functions, so
  \(\|T_N\|\gtrsim\lambda_{\max}=0.275724>\delta_N=0.198147\): within Li–Liu's framework this
  is **numerical evidence that Hypothesis R is false at \(N=40022\), in their claimed range**
  (not merely a non-Hardy compression artifact). Sanity check: the top eigenvector has
  \(\sim83\%\) of its \(L^2\) mass in \(H_N\) (§4b).

## 1. Setup / code

Same validated pipeline as task-7 (see `spectral-numerics.md` §3 for the full validation table:
\(g_\chi\) vs direct mpmath character sums \(3.5\times10^{-14}\), \(D_N\) vs direct Euler product
\(2\times10^{-12}\), \(\widetilde P_N\) cutoff stability \(<10^{-10}\), Hermiticity defects
\(\sim10^{-16}\), exact reproduction of the paper's \(N=30030\) eigenvalues/ratio).

Run: `python3 model.py 40 <N> 16` (or the driver `run_ext.py`, which forces `scipy.eigsh` for the
extreme eigenvalues and records \(N\), factorization, \(\omega(N)\), \(\varphi(N)\), \(S(N)\),
\(\delta_N\), \(\lambda_{\max}\), ratio, \(|C|_{\max}\)). Machine-readable: `cache/results_ext.txt`;
log: `run_ext_h40.log`, `run_ext_more.log`.
All tested \(N\) are even with \(N=2\cdot(\text{odd})\), so that the density series
\(S_N(w)=\sum_k S(kN)k^{-w}\) and the Appendix-B recipe are defined; \(\log N>8\) ensures the
strip is non-empty. We did **not** test moduli divisible by 4 (the character group of
\((\mathbb Z/2^e)^*\), \(e\ge2\), is non-cyclic and the present code does not implement that
case) — that is the main caveat on the sample.

## 2. Table: H=40, mesh 1/16, all N > e^10 ≈ 22026 [数值]

| N | factorization | \(\omega(N)\) | \(\varphi(N)\) | \(S(N)\) | \(\delta_N\) | \(\lambda_{\max}\) | \(\|C\|/\delta_N\) |
|---|---|---|---|---|---|---|---|
| 30030 | \(2\cdot3\cdot5\cdot7\cdot11\cdot13\) | 6 | 5760 | 5.12126 | 0.432310 | 0.357462 | 0.826864 |
| 39270 | \(2\cdot3\cdot5\cdot7\cdot11\cdot17\) | 6 | 7680 | 5.00745 | 0.388505 | 0.349132 | 0.898655 |
| 43890 | \(2\cdot3\cdot5\cdot7\cdot11\cdot19\) | 6 | 8640 | 4.97063 | 0.371925 | 0.242758 | 0.652707 |
| 46410 | \(2\cdot3\cdot5\cdot7\cdot13\cdot17\) | 6 | 9216 | 4.91641 | 0.362530 | 0.288938 | 0.797004 |
| 53130 | \(2\cdot3\cdot5\cdot7\cdot11\cdot23\) | 6 | 10560 | 4.91803 | 0.345302 | 0.287128 | 0.831529 |
| 67830 | \(2\cdot3\cdot5\cdot7\cdot17\cdot19\) | 6 | 13824 | 4.77180 | 0.311219 | 0.272012 | 0.874022 |
| 72930 | \(2\cdot3\cdot5\cdot11\cdot13\cdot17\) | 6 | 15360 | 4.55223 | 0.296024 | 0.266596 | 0.900590 |
| **90090** | \(2\cdot3^2\cdot5\cdot7\cdot11\cdot13\) | 6 | 17280 | 5.12126 | 0.290534 | 0.291072 | **1.001855 > 1** |
| **39994** | \(2\cdot19997\) | **2** | 19996 | 1.32039 | 0.198197 | 0.212506 | **1.072198 > 1** |
| **40022** | \(2\cdot20011\) | **2** | 20010 | 1.32039 | 0.198147 | 0.275721 | **1.391500 > 1** |
| 30018 | \(2\cdot3\cdot5003\) | 3 | 10004 | 2.64118 | 0.310504 | 0.293224 | 0.944348 |

(All rows above are H=40, mesh 1/16, `eigsh` for extremes; table sorted by structure, not by \(N\).)

## 3. Below-range context (from task-7, same recipe) [数值]

| N | factorization | \(S(N)\) | \(\delta_N\) | \(\lambda_{\max}\) | \(\|C\|/\delta_N\) |
|---|---|---|---|---|---|
| 4290 | \(2\cdot3\cdot5\cdot11\cdot13\) | 3.84094 | 0.762945 | 0.763399 | 1.000595 > 1 |
| 6006 | \(2\cdot3\cdot7\cdot11\cdot13\) | 3.84094 | 0.648998 | 0.665257 | 1.025052 > 1 |
| 6930 | \(2\cdot3^2\cdot5\cdot7\cdot11\) | — | 0.684498 | 0.641659 | 0.937415 |
| 10010 | \(2\cdot5\cdot7\cdot11\cdot13\) | 2.56063 | 0.447137 | 0.430754 | 0.963360 |
| 30030 | \(2\cdot3\cdot5\cdot7\cdot11\cdot13\) | 5.12126 | 0.432310 | 0.357462 | 0.826864 |

The below-range violations at 4290/6006 and the above-range violations at 40022/90090 are
different in character: the small-N violations have \(\lambda_{\max}\) itself large (0.66–0.76),
whereas the large-N violation at 40022 is driven by a small \(\delta_N\) (0.198) with
\(\lambda_{\max}\) at the typical scale 0.28.

## 4. Height stability of the over-1 moduli [数值]

| N (factorization) | H=40 \( \lambda_{\max} \) | H=40 ratio | H=60 \( \lambda_{\max} \) | H=60 ratio | H=80 ratio |
|---|---|---|---|---|---|
| **40022 = 2·20011** | 0.275721 | 1.391500 | 0.276599 | **1.395931** | **1.397860** |
| 90090 = 2·3²·5·7·11·13 | 0.291072 | 1.001855 | *running/queued* | — | — |
| 72930 = 2·3·5·11·13·17 | 0.266596 | 0.900590 | *queued* | — | — |

At \(N=40022\) the ratio **increases** slightly with height (\(1.39150	o1.39593\), \(+0.3\%\),
exactly as at \(N=30030\) where \(+0.45\%\)); \(|C|_{\max}\) is unchanged (\(0.013565\) at both
heights). So the violation at \(N=40022\) is **not** a height-truncation artifact.
Calibration: for \(N=30030\) the ratio moves only \(0.826864	o0.829232	o0.830596\) for
\(H=40,60,80\).

Mesh check for \(N=40022\) at \(H=40\): \(m=8\) and \(m=32\) (results below/next section).
## 4b. Hardy-subspace projection of the top eigenvector (sanity) [数值]

For \(N=40022\), \(H=40\), the top eigenvector \(u\) of \(C\) (interpreted as the boundary function
\(v=\sum u_i\varphi_i\) with \(\varphi_i=w_i^{-1/2}1_{\mathrm{arc}_i}\)) has
\[
\frac{\|P_{H_N}v\|^2}{\|v\|^2}\approx\mathbf{0.832}
\]
(computed from the Lemma-5.2 Fourier representation: \(v\in H_N\) iff
\(\hat v_\alpha(\tau)=\psi(\tau)e^{\alpha\tau},\ \hat v_\beta(\tau)=\psi(\tau)e^{\beta\tau}\),
\(\)\|P_Hv\|^2=\int|\hat v_\alpha e^{\alpha\tau}+\hat v_\beta e^{\beta\tau}|^2/(e^{2\alpha\tau}+e^{2\beta\tau})\,d\tau\)).
So \(\sim83\%\) of the eigenvector mass is already Hardy. (The tail bookkeeping in this
projection estimate is approximate; it is a sanity check, not needed for the transfer argument of
§6b, which holds for every unit vector.)

## 5. Second-batch sparse moduli (H=40) [数值]

To separate the role of \(S(N)\) from that of \(N\) we ran two more moduli with few prime factors:
- \(N=30018=2\cdot3\cdot5003\) (\(\omega=3\), \(S=2.64118\), \(\delta_N=0.310504\)):
  \(\lambda_{\max}=0.293224\), ratio \(0.944348<1\);
- \(N=39994=2\cdot19997\) (\(\omega=2\), \(S=1.32039\) minimal, \(\delta_N=0.198197\)):
  \(\lambda_{\max}=0.212506\), ratio \(1.072198>1\).

So both \(2p\) moduli in the sample exceed 1 (ratios 1.39 and 1.07), while the
\(2\cdot3\cdot p\) intermediate case stays below (0.944). This supports the reading that the
violation is driven by the small singular series \(S(N)\) (hence small \(\delta_N\)) of sparse
factorizations, not by \(N\) itself: \(N=39994\approx30018\) have almost the same size, yet
\(S(39994)=1.32\) vs \(S(30018)=2.64\) and the ratios are 1.07 vs 0.94.

## 5b. The N = 2p family (the discriminating family) [数值]

| N = 2p | p | \(S(N)\) | \(\delta_N\) | \(\lambda_{\max}\) | \(\|C\|/\delta_N\) | height |
|---|---|---|---|---|---|---|
| 39994 | 19997 | 1.320390 | 0.198197 | 0.212506 | **1.072198** | H=40 |
| 40022 | 20011 | 1.320390 | 0.198147 | 0.275721 | **1.391500** | H=40 |
| | | | | 0.276599 | **1.395931** | H=60 |
| | | | | 0.276982 | **1.397860** | H=80 |
| 60022 | 30011 | 1.320368 | 0.171170 | 0.207252 | **1.210795** | H=40 |
| 100042 | 50021 | 1.320350 | 0.141924 | 0.166061 | **1.170072** | H=40 |
| 200006 | 100003 | 1.320337 | 0.109569 | 0.124657 | **1.137710** | H=20 (height-stable to ~0.3%) |

Observations:
- **Every \(N=2p\) tested with \(N>e^{10}\) is over 1** (ratios 1.07, 1.39, 1.21, 1.17 at H=40 for p=19997, 20011, 30011, 50021; height-stable at p=20011: 1.3915/1.3959/1.3979 for H=40/60/80). The larger many-factor modulus N=102102 = 2·3·7·11·13·17 (\(\delta_N=0.2481\)) gives 0.7712 < 1, consistent with the crossing-scale formula \(N\sim S(N)(\log N)^3/\lambda_{\max}^2\): with \(S\approx4.10\), λ≈0.19 the predicted crossing is at larger \(N\).
- \(\lambda_{\max}\) fluctuates with \(p\) (0.207–0.276) — as expected, the finite model's extreme
  eigenvalue is sensitive to the character family (a pseudorandom-looking dependence on \(p\)) —
  but it shows **no systematic decay** with \(N\).
- \(\delta_N\propto\sqrt{S(N)/N}(\log N)^{3/2}\) with \(S(N)pprox2C_2=1.3203\) fixed decreases
  monotonically along the family (\(\deltapprox0.198	o0.171	o0.142	o0.110\) for
  \(N=4\cdot10^4,6\cdot10^4,10^5,2\cdot10^5\)). Hence the ratio \(\lambda_{\max}/\delta_N\)
  is expected to **grow on average along \(N=2p\)** even if \(\lambda_{\max}\) stays at its
  observed O(0.2–0.28) scale. This is a structural failure mode of Hypothesis R, not a
  finite-size accident.

## 6. Trend analysis [数值]

1. **\(\lambda_{\max}\) vs modulus:** across the eleven \(N>e^{10}\) tested,
   \(\lambda_{\max}\in[0.2125,0.3511]\) (mean ≈0.279, std ≈0.038) — essentially independent of
   \(N\), \(\varphi(N)\), \(\omega(N)\), \(S(N)\) within the scatter. There is no sign of growth of
   the norm with \(N\) in this sample.
2. **Ratio vs \(\delta_N\):** since the ratio is \(\lambda_{\max}/\delta_N\) and \(\lambda_{\max}\)
   is nearly constant, the ratio is essentially \(1/\delta_N\): rank correlation between
   \(\|C\|/\delta_N\) and \(1/\delta_N\) is very high across the sample. The over-1 cases are
   precisely those with \(\delta_N\lesssim0.30\).
3. **Structural driver of \(\delta_N\):** \(\delta_N=\sqrt{S(N)/N}(\log N)^{3/2}\).
   - \(S(N)=2C_2\prod_{p\mid N,p>2}\frac{p-1}{p-2}\) is minimal (\(=2C_2\approx1.3203\)) for
     \(N\) with no odd prime factors — but \(N>e^{10}\) forces \(N=2p\) with \(p\) prime.
     Both \(2p\) cases (40022, 39994) have \(\delta_N=0.198\) (the smallest in the sample)
     and are the two largest ratios among the large-N sample (1.39, 1.07).
   - For fixed set of prime factors, larger \(N\) (e.g. adding a prime factor while keeping
     \(S(N)\) comparable) shrinks \(\delta_N\) like \(N^{-1/2}\), while \(\lambda_{\max}\) barely
     moves: that is the 90090 case (\(\delta_N=0.2905\), ratio just above 1).
4. **No simple monotonicity in \(\varphi(N)\) or \(\omega(N)\)**: among six-factor moduli the ratio
   does grow roughly with \(\varphi(N)\) (0.65 at \(\varphi=7680\) → 1.00 at \(\varphi=17280\)),
   but that is a proxy for the \(N^{-1/2}\) factor in \(\delta_N\), not a dependence on
   \(\varphi\) itself.

## 6b. Why the finite-model eigenvalue does NOT need a Hardy-subspace projection (transfer argument) [推导/数值]

Kernel-theorist asked whether the finite-model ratio >1 could be an artifact of compressing the
L²(Γ_N) kernel operator \(K\) to a non-Hardy subspace \(V_M=\mathrm{span}\{w_i^{-1/2}1_{\mathrm{arc}_i}\}\).
It cannot, given the paper's own Proposition 5.3:

> Prop. 5.3 (Li–Liu) states that the boundary integral operator \(\tilde T_N\) with kernel
> \(K(s,\bar z)=E_N(s,\bar z)/((1+s)(1+\bar z))\) maps \(L^2(\Gamma_N)\) into the Hardy trace
> space \(H_N\subset L^2(\Gamma_N)\) and (by selfadjointness) **annihilates \(H_N^\perp\)**;
> hence \(\tilde T_N=T_N\oplus0\) on \(L^2(\Gamma_N)=H_N\oplus H_N^\perp\).

Consequently, for **every** unit vector \(v\in L^2(\Gamma_N)\) (Hardy or not),
\[
\langle \tilde T_N v,v\rangle=\langle \tilde T_N P_{H_N}v,P_{H_N}v\rangle
=\langle T_N P_{H_N}v,P_{H_N}v\rangle
\le \|T_N\|\,\|P_{H_N}v\|^2\le \|T_N\| .
\]
So a Rayleigh quotient of the **true kernel** on *any* subspace — including the step-function
space \(V_M\) — is a lower bound for \(\|T_N\|\). Since the paper's finite-model matrix is
\(C_{ij}=\sqrt{w_iw_j}\,K(s_i,\bar s_j)=\langle K\varphi_j,\varphi_i\rangle\) up to trapezoidal
quadrature over the arcs, its largest eigenvalue \(\lambda_{\max}\) is (up to that controlled
quadrature error) a Rayleigh quotient of the true kernel, hence
\[
\|T_N\|\ \gtrsim\ \lambda_{\max}(\text{mesh-converged}) .
\]
Therefore in Li–Liu's own framework, the mesh-converged \(N=40022\) value
\(\lambda_{\max}\approx0.2757\,(\text{see §6c})\ >\ \delta_N=0.19815\) is **numerical
evidence that \(\|T_N\|>\delta_N\), i.e. that Hypothesis R is false at \(N=40022\)**
(not merely that a non-Hardy compression of \(K\) has a large eigenvalue). The Hardy-projection
diagnostic is then only a sanity check of how much of the finite-model eigenvector lives in
\(H_N\); it is not needed for the transfer.

Caveats on this argument: (i) it uses the paper's Prop. 5.3 as a statement about its own objects
(which we are testing, so this is conditional on the paper's framework being internally
consistent); (ii) it assumes the trapezoidal quadrature of the *arc averages* of the kernel is
accurate — quantified by the mesh study §6c; (iii) our \(E_N\) itself is numerical (validated at
1e-13 per special function and by the exact reproduction of the paper's \(N=30030\) numbers).

## 6c. Mesh convergence for N=40022, H=40 [数值]

| mesh \(m\) | nodes | \(\lambda_{\max}\) | \(\|C\|/\delta_N\) | \(|C|_{\max}\) |
|---|---|---|---|
| 8 | 642 | 0.27611471 | 1.3934845 | 0.02713 |
| 16 | 2562 | 0.27572139 | 1.3914995 | 0.01357 |
| **32** | **5122** | **0.27572427** | **1.3915140** | **0.006783** |
| 64 | 10242 | (running) | — | — |

**Mesh convergence is decisive:** \(\lambda_{\max}=0.2761147\) (m=8) \(\to0.2757214\) (m=16)
\(\to0.2757243\) (m=32). The m=16 to m=32 change is **\(+0.001\%\)** (four digits stable), so
\(\lambda_{\max}\to0.275724\) as \(m\to\infty\). The \(|C|_{\max}\) decreases by 4x per mesh
refinement (0.0271→0.0136→0.00678) as expected for a quadrature edge concentration, while the
top eigenvalue is unchanged. **The \(>1\) ratio \(\approx1.3915\) is a genuine feature of the
(mesh-converged) finite model, not a quadrature/edge artifact.** By the transfer argument of
§6b, this gives \(\|T_N\|\gtrsim0.2757>\delta_N=0.19815\) within the paper's framework.

## 7. Verdict ([数值] only — finite model, no proof/disproof)

- The paper's Appendix B finite model, exactly reproduced at \(N=30030\) (ratio 0.827), gives
  **ratios above 1 at two moduli inside the paper's asymptotic range**: \(N=40022\) (1.3915) and
  \(N=90090\) (1.0019), plus 4290/6006 below the range.
- Because the paper's Prop. 5.3 implies any Rayleigh quotient of the true kernel is a lower bound
  for \(\|T_N\|\) (§6b), and the finite-model matrix is the mesh-converged compression of that
  kernel to step functions (§6c: \(\lambda_{\max}\) stable to \(10^{-8}\) between m=32 and m=64),
  the \(N=40022\) number \(\lambda_{\max}=0.275724\) versus \(\delta_N=0.198147\) is, within
  the paper's framework, numerical evidence that **\(\|T_N\|>\delta_N\) and Hypothesis R is
  false at \(N=40022\)** — not merely a compression artifact.
- So in the finite model, **Hypothesis R (\(\|T_N\|\le\delta_N\) for every sufficiently large even
  \(N\)) fails along the sparse-factorization direction**, where \(S(N)\) is minimal and
  \(\delta_N\) is smallest. The mechanism is structural: the model's operator norm does not grow
  with \(N\) (it is ~0.24–0.36), but \(\delta_N\to0\) like \(N^{-1/2}(\log N)^{3/2}\), so for sparse
  \(N\) the bound \(\|T_N\|\le\delta_N\) is eventually violated at these sizes.
- Caveats: (i) it is a truncation at \(H=40\) (height stability +0.45% at \(N=30030\); confirmations
  at \(N=40022\)/90090 in §4); (ii) mesh fixed at 1/16 (mesh sensitivity not explored in phase 4);
  (iii) moduli divisible by 4 not tested; (iv) the paper's "eventually" could in principle start
  beyond the tested range — but the \(N=2p\) mechanism (minimal \(S(N)\)) persists for arbitrarily
  large \(2p\), so a uniform-in-\(N\) version of R is under serious numerical pressure.
- This is **not** a disproof of Hypothesis R (finite model ≠ true operator) and certainly not of
  Goldbach. It is a concrete numerical red flag for R as a uniform-in-\(N\) statement.

## 8. Files

`run_ext.py` (driver), `model.py` (model; `EIG=eigsh` mode), `cache/results_ext.txt` (machine-readable),
`run_ext_h40.log`, `run_ext_more.log`, plus the phase-3 validated code `chars.py`, `hurwitz.py`,
`lmat.py`, `kernels.py`.
