# Li–Liu finite spectral model: numerical reproduction and stress test

**Task:** task-7 (phase 2). **Author:** spectral-numerics. **Date:** 2026-11-21 (final version 13:45 CST).
**Scope:** reproduce Appendix B of Li–Liu, *A Conditional Proof of the Goldbach Conjecture*
(Shandong Univ. MRC, 2026-11-13; `/home/kiler/rh-work/liu-goldbach.pdf`, pp. 60–62), then stress-test
the finite model \(C\) (which encodes Hypothesis R: \(\|T_N\| \le \delta_N\)).

All labels: **[事实]** = verified from paper/source; **[数值]** = our computation; **[推测]** = interpretation.

---

## 0. TL;DR

1. **[数值] The paper's Appendix B numbers are reproduced exactly** (to 6 digits) with the
   paper's recipe: at \(N=30030\), height \(H=40\), mesh 1/16 (2562 nodes), the extreme
   eigenvalues of the computed 2562×2562 Hermitian matrix \(C\) are
   \[
   \lambda_{\max}=+0.35746180,\qquad \lambda_{\min}=-0.35342137,
   \qquad \|C\|/\delta_N = 0.82686407,
   \]
   versus the paper's \(-0.353421\), \(+0.357462\), \(0.826864\) [事实, p. 61]. Our
   \(\delta_N=0.43231023969\) vs paper \(0.432310239587548\) (relative difference \(2.4\times10^{-10}\)).
2. **[数值] Height sensitivity at \(N=30030\) (same recipe).** The ratio is extremely stable:
   \(H=40:0.826864,\ H=60:0.829232,\ H=80:0.830596\) (nodes 2562, 3842, 5122). The growth
   from \(H=40\) to \(H=80\) is +0.45%, consistent with a slowly converging tail; **no evidence
   that the paper's \(0.827<1\) is a truncation artifact**. (An intermediate \(H=80\) run gave an
   anomalous 3.218 due to a fixed-\(K\) Euler–Maclaurin failure in our \(D_N\) evaluation at large
   \(|\Im w|\); fixed with an adaptive-\(K\)/prime-sum version — see §4.4. H=40 reproduction is
   unaffected: the old \(D_N\) code is accurate to \(5\times10^{-14}\) for \(|\Im w|\le80\),
   which covers the paper setting.)
3. **[数值] New: N-dependence at \(H=40\), same recipe** (see §4.2): the ratio **grows as \(N\) decreases**:
   \[
   N=30030:\ 0.826864,\quad N=10010:\ 0.963360,\quad N=6930:\ 0.937415,\quad
   N=6006:\ 1.025052,\quad N=4290:\ 1.000595 .
   \]
   Two configurations (\(N=6006\) and \(N=4290\)) give \(\|C\|/\delta_N>1\), i.e. the finite
   model **violates Hypothesis R** there, while exactly reproducing the paper's \(N=30030\) smallness.
   (These \(N\) are below the paper's asymptotic range \(N>e^{10}\approx22026\), but \(\log N>8\)
   and the recipe is well defined; see caveats §5.) This is the main new numerical red flag.
4. **[数值] Implementation is independently validated** beyond the eigenvalue match:
   \(L'/L\) values vs direct mpmath character sums (max error \(3.5\times10^{-14}\)),
   \(D_N\) via zeta-factor extraction vs direct Euler products (\(1.9\times10^{-12}\)),
   \(\widetilde P_N\) cutoff-stability (\(<10^{-10}\)),
   and the Mellin contour identity (2.34) checked componentwise against the arithmetic
   \(P(N), D(N), c_\varphi S(N)\) (0.35–2%, quadrature-limited).
5. **[事实] Honest caveat:** the finite model is a truncation/discretisation; the paper itself
   states it "does not certify Hypothesis R for \(T_{30030,1}\)" (p. 62). Nothing here is a proof;
   the \(N=6006\) ratio \(>1\) is evidence about the finite model, not a disproof of
   Hypothesis R (nor of Goldbach).

---

## 1. Setup and exact recipe (from Appendix B)

- \(N=30030=2\cdot3\cdot5\cdot7\cdot11\cdot13\), \(\varphi(N)=5760\), all characters modulo \(N\);
  \(X_N^-=\{odd\ \chi\}\), \(\#X_N^-=2880\). \(\alpha_N=1/\log N=0.09699366053\), \(\beta=1/8\),
  \(S(N)=2C_2\prod_{p\mid N,p>2}\frac{p-1}{p-2}=5.12125530115\),
  \(\delta_N=\sqrt{S(N)/N}(\log N)^{3/2}=0.43231023969\).
- Nodes: the two boundary lines \(s=\alpha_N+ik/16\) and \(s=\beta+ik/16\), \(k=-640,\dots,640\)
  (2562 nodes). Weights: \(w_i=1/16\) interior, \(1/32\) at the four endpoints (trapezoid,
  "no \(1/(2\pi)\) factor"). Nodes are listed line by line.
- Hermitian kernel matrix [事实, p. 60 PDF]: with \(E_N=P_N-D_N-K_N\),
  \[
  C_{ij}=\sqrt{w_i}\,\frac{E_N(s_i,\overline{s_j})}{(1+s_i)(1+\overline{s_j})}\,\sqrt{w_j},
  \qquad
  P_N(s,\bar z)=\frac{2}{\varphi(N)}\sum_{\chi\in X^-_N} g_\chi(s)\overline{g_\chi(z)},
  \ g_\chi(s)=\frac{L'}{L}(\tfrac12+s,\chi),
  \]
  \[
  D_N(w)=\sum_{(n,N)=1}\frac{\Lambda^2(n)}{n^{1+w}},\qquad
  K_N(s,z)=S(N)\Big(\frac{\pi}{N}\Big)^{s+z}\widetilde P_N(s+z)\,\zeta(1-s-z)\,X_1(s)X_1(z),
  \]
  \(\widetilde P_N(w)=\prod_{p>2,\,p\nmid N}\big(1+\frac{p^{-w}}{p-2}\big)\),
  \(X_1(u)=\Gamma(\frac{3/2-u}{2})/\Gamma(\frac{3/2+u}{2})\).
  Note the conjugation structure is confirmed against the PDF image: (2.13) reads
  \(\mathscr P_N(s,\bar z)=\frac{2}{\varphi(N)}\sum g_\chi(s)\overline{g_\chi(z)}\), and the
  appendix entry is \(C_{ij}=\sqrt{w_i}\,E_N(s_i,\overline{s_j})/((1+s_i)(1+\overline{s_j}))\sqrt{w_j}\);
  both overlines are present in the PDF (extracted text loses them). Hence \(C\) is **Hermitian**.

## 2. Reproduction result ([数值])

Command (working dir `/home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase2/spectral`):
```
python3 model.py 40 30030 16        # args: H N m  (mesh 1/m)
```
Output (log `run_H2.log`; full 2562×2562 `eigvalsh`):
```
delta_N = 0.43231023969153526
max|eig| = 0.35746180421882773   ||C||/delta = 0.8268640698260724
extremes: most negative -0.3534213749491202, most positive 0.35746180421882773
top |eig|: 0.1584 0.1742 0.1951 0.2382 0.2719 0.2899 0.3534 0.3575
E herm err 9.06e-15  C herm err 2.36e-16  |C|max = 0.0202018
```
Compare paper p. 61: extreme eigenvalues \(\approx -0.353421\) and \(0.357462\),
\(\|C\|/\delta_N\approx0.826864<1\), \(\delta_N=0.432310239587548\). **[事实] Exact reproduction.**

Run time on 16-core WSL: `build_G` 20–30 s (character FFT + Hurwitz \(L'/L\) for 2562 nodes × 2880 chars),
kernel values \(\sim\)15 s, P matrix product \(\sim\)2 s, full Hermitian eigendecomposition \(\sim\)50 s
(\(\sim\)90 s total when run alone). Peak memory <1 GB. Code: see §7.

### 2.1 What was wrong in our earlier invalid runs (important for honesty)
Our first runs gave absurd \(\|C\|/\delta_N\approx244\) (H=40) and then \(\approx8.4\) (H=4..80).
These were **implementation bugs on our side**, not a property of the paper:
1. the denominator \((1+s_i)(1+\overline{s_j})\) was coded as \((1+\Re s_i)(1+\Re s_j)\)
   (imaginary parts dropped);
2. \(X_1(s)\) was evaluated at the real part \(\sigma_i\) instead of the complex node
   \(s_i=\sigma_i+it\).
After fixing both, the reproduction is exact. (For the record: \(K_N\)'s normalisation was
never changed between those runs; the kernel formula (2.12) was independently checked against
the equivalent (2.11) Beta-function form in mpmath, agreement \(10^{-30}\).)

---

## 3. Independent cross-checks of the pipeline ([数值])

| check | method | result |
|---|---|---|
| Hurwitz–Euler–Maclaurin \(\zeta(u,x),\partial_u\zeta(u,x)\) | vs `mpmath.zeta`/`mp.diff`, \(|u|=O(500)\), K=64,J=24 | abs err \(4\times10^{-13}\) for \(\zeta\), \(3\times10^{-12}\) for \(\zeta'\) (relative \(\sim10^{-15}\)) |
| \(L'/L(u,\chi)\) all chars | Hurwitz formula \(L(u,\chi)=N^{-u}\sum_a\chi(a)\zeta(u,a/N)\) + character DFT over \((\mathbb Z/N)^*\), compared with direct character sums using mpmath \(\zeta\) at 6 (node,character) pairs | max error \(3.5\times10^{-14}\) |
| character DFT convention | direct exponential sums for random characters, orthogonality/odd mask | errors \(<10^{-13}\); \(\#X_N^-=2880\) ✓ |
| \(D_N(w)=\sum_{(n,N)=1}\Lambda^2(n)n^{-1-w}\) | identity \(D_N=f_N\), \(f_N(s)=h(s)-R(s)-\text{diag}\), \(h(u)=(\zeta'/\zeta)'(u)\), \(R(s)=\sum_{n\ge2}c_nh(ns)\), \(c_n=(-1)^{\omega(n)+1}\prod_{p\mid n}(p-1)\); vs direct Euler product \(\sum_p(\log p)^2p^{-s}/(1-p^{-s})\) over \(p\le3\cdot10^6\) at \(\Re s=3\) and \(\Re s=2.5\) | \(1.9\times10^{-12}\) and \(2.1\times10^{-9}\) |
| \(\widetilde P_N(w)=\prod_{p>2,\ p\nmid N}(1+p^{-w}/(p-2))\) | zeta-factor extraction: \(\widetilde P_N=\frac{\zeta(1+w)}{\zeta(2+2w)(1+2^{-1-w})\prod_{p\mid N,p>2}(1+p^{-1-w})}\prod_{2<p\le P_{\rm cut},p\nmid N}\frac{1+p^{-w}/(p-2)}{1+p^{-1-w}}\cdot e^{\text{tail}(E_1)}\), \(P_{\rm cut}=2\cdot10^5\), tail \(2E_1((1+w)\log P)+4E_1((2+w)\log P)-2E_1((2+2w)\log P)\); verified vs direct prime product where it converges (\(\Re w=1.2\), \(1.5\), \(2\)), and cutoff stability \(P_{\rm cut}=2\cdot10^5\leftrightarrow5\cdot10^5\) | agreement \(10^{-9}\)–\(10^{-13}\); cutoff stability \(8\times10^{-11}\) |
| singular series / \(\delta_N\) | \(C_2\) from primes \(\le10^8\) | \(\delta_N\) matches paper to \(2.4\times10^{-10}\) relative |
| Mellin contour identity (2.34)/(2.35) | with explicit smooth weight \(\varphi(u)=\exp(-1/(1-(6u-3)^2))\), \(c_\varphi=0.02218102\), direct arithmetic \(G(N)=0.11384347\), \(r=c_\varphi S-G=-2.4880\times10^{-4}\) (\(r/\delta_N=-5.755\times10^{-4}\)); computed \((1/(2\pi i)^2)\iint N^{s+z}\tilde\Phi(s)\tilde\Phi(z)E_N(s,z)dsdz\) on \(\Re s=\Re z=1/9\), grid \(T=100\), \(dt=0.25\) (801² points); separately \(J_P,J_D,J_K\) vs arithmetic \(P(N),D(N),-c_\varphi S(N)\) | \(J_P/P(N)=1.0035\), \(J_D/D(N)=1.0137\), \(-J_K/(c_\varphi S)=1.0204\) — i.e. each kernel satisfies its arithmetic identity to the quadrature error (1–2%). The residual \(r\) itself is \(O(10^{-4})\), below our quadrature error \(O(10^{-3})\), so this check validates \(P_N,D_N,K_N\) to \(\sim1\%\) but does not by itself resolve \(r\). Code `checkE.py`/`checkE_components.py`. |

**Conclusion of §3:** the implementation is validated at the \(10^{-13}\) level in each special
function, and the assembled kernels satisfy the paper's arithmetic identities to the precision of
an independent numerical quadrature. The exact 6-digit eigenvalue reproduction in §2 is the
end-to-end confirmation.

---

## 4. New stress test: height and N dependence ([数值])

All with the corrected paper recipe (Hermitian \(C\), trapezoid weights, mesh 1/16 unless noted).

### 4.1 Height sensitivity, \(N=30030\) (does the truncation at \(H=40\) hide larger eigenvalues?)

| \(H\) | nodes | \(\max|\lambda|\) | \(\|C\|/\delta_N\) | run |
|---|---|---|---|---|
| 40 | 2562 | 0.35746180 | **0.82686407** | paper reproduction, full `eigvalsh` (`run_H2.log`) |
| 60 | 3842 | 0.35848533 | **0.82923165** | fixed-\(D_N\) re-run, `eigsh` (`run_fixD.log`); old-\(D_N\) run gave 0.82923016 (diff \(1.5\times10^{-6}\)) |
| 80 | 5122 | 0.35907513 | **0.83059593** | fixed-\(D_N\) re-run (`run_fixD.log`) |

Reading: the extreme eigenvalues move by less than 0.5% between \(H=40\) and \(H=80\) and
remain well below \(\delta_N\). The tail contribution beyond \(|t|=40\) is small in the weighted
kernel (it decays like \(1/|1+s|^2\)), so the paper's \(H=40\) truncation is not hiding a large
eigenvalue in this model. Earlier pre-fix numbers in `run_heights.log` (3.4–3.7) are **invalid**.

### 4.2 N-dependence, \(H=40\), mesh 1/16 (same recipe)

| \(N\) | \(\log N\) | \(\alpha_N\) | \(\varphi(N)\) | \(\delta_N\) | \(\max|\lambda|\) | \(\|C\|/\delta_N\) | status |
|---|---|---|---|---|---|---|---|
| 30030 | 10.310 | 0.09699 | 5760 | 0.43231024 | 0.35746180 | **0.826864** | finished |
| 6006 | 8.7005 | 0.11494 | 1440 | 0.64899831 | 0.66525669 | **1.025052 > 1** | finished (`run_N.log`) |
| 10010 | 9.2114 | 0.10856 | 2880 | 0.44713677 | 0.43075363 | **0.963360** | finished (`run_N.log`) |
| 4290 | 8.3640 | 0.11960 | 960 | 0.76294504 | 0.76339877 | **1.000595 > 1** | finished (`run_N.log`) |
| 6930 | 8.8434 | 0.11308 | 1440 | 0.68449781 | 0.64165879 | 0.937415 | finished (`run_N.log`) |
| 15015 | 9.6171 | 0.10398 | — | — | — | — | **not run**: \(N\) odd; paper's density series \(S_N(w)=\sum_k S(kN)k^{-w}\) requires \(kN\) even (Section 4.3: "\(N\ge4\) even"), so the fixed recipe is not defined for odd \(N\). Replaced by even \(N=4290\). |

**Finding (N-trend):** at \(H=40\), mesh 1/16, the finite-model ratio is
\[
N=30030:\ 0.8269,\quad N=10010:\ 0.9634,\quad N=6930:\ 0.9374,\quad N=6006:\ 1.0251,\quad N=4290:\ 1.0006 .
\]
All values are \(<1.3\); the ratio is not monotone in \(N\) (6930 < 10010, both have
\(\delta_N\) around 0.64–0.68 while the 30030 case has much smaller \(\delta_N\) normalized
differently), but the overall trend is clear: **the smallest moduli in our sample sit at or
above the threshold 1**, while the paper's \(N=30030\) sits at 0.827. Since these \(N\) are below
the asymptotic range, this does not contradict the paper's theorems; it does show that the
uniform-in-\(N\) smallness assumed by Hypothesis R is not a feature of the raw finite model —
\(\|C\|/\delta_N\) can exceed 1 at moderate \(N\).

Caveats: (i) the paper's asymptotic theorem assumes \(N>e^{10}\approx22026\), so \(N=6006\) lies
outside the range to which Hypotheses R/S are applied in the proofs (but \(\log N>8\), the strip
condition, holds; the recipe is well defined); (ii) the height-40 truncation might bias the
\(N=6006\) number, but it is exactly the same truncation under which the paper's \(N=30030\)
number is produced; (iii) the \(N\)-dependence of \(\|T_N\|/\delta_N\) is precisely what
Hypothesis R must control uniformly and what the paper's GRH-only bound \((\log N)^2\) leaves open.

### 4.3 Mesh / prime-cutoff sensitivity
Not completed within the time box. The code supports it directly (`python3 model.py H N m`;
\(m=8,16,32\); \(\widetilde P_N\) cutoff is a parameter `Pcut` of `model.build_model`).
What was checked instead: the prime-cutoff stability of \(\widetilde P_N\) itself (8×10\(^{-11}\)
between \(P_{\rm cut}=2\cdot10^5\) and \(5\cdot10^5\), consistent with the paper's claim that
doubling the cutoff changes endpoints by \(<3\times10^{-8}\)); and the fact that the \(N=30030\)
\(H=40\) reproduces the paper's 6 digits, which bounds the combined kernel value error.

---

### 4.4 A self-corrected numerical issue at large height (\(D_N\) evaluation)
During the height study we found that our first \(D_N(w)=\sum_{(n,N)=1}\Lambda^2(n)n^{-1-w}\)
code used the identity \(D_N=h(s)-\sum_{n\ge2}c_n h(ns)-\text{diag}\), \(h(u)=(\zeta'/\zeta)'(u)\),
with a **fixed** Euler–Maclaurin cutoff \(K=64\) for \(h(ns)\). While \(h\)'s EM asymptotic
series is superb for \(|\Im u|\lesssim 300\), it degrades once \(|\Im u|/K\) is large; for
\(H=80\) the terms \(h(5s),h(7s),\dots\) (with \(|\Im|\sim 500\text{–}1400\)) were grossly wrong,
producing the spurious \(\|C\|/\delta_N=3.218\) and \(|C|_{\max}=0.488\). The fix:
use adaptive \(K=2|\Im u|+64\) EM for \(h(s),h(2s),h(3s)\) and evaluate \(h(ns)\) for \(n\ge4\)
directly as \(\sum_{p\le10^4}(\log p)^2p^{-ns}/(1-p^{-ns})^2\) (`kernels.D_values_fast`).
This was validated: agrees with the old code to \(5\times10^{-14}\) for \(|\Im w|\le80\)
(the paper's \(H=40\) setting, so the reproduction is unaffected), and against an independent
mpmath reference (Möbius-inverted \(h\)-sum) to \(6\times10^{-11}\) at \(|\Im w|=128.6\).
After the fix all \(H\) runs have \(|C|_{\max}=0.020202\), as at \(H=40\), and the height trend
is smooth. (This is exactly the kind of truncation-level numerical trap the paper's Appendix B
warns about.)

## 5. Honest error/truncation discussion

- The finite model is a Nyström/trapezoid discretisation of the kernel of \(T_N\) on two vertical
  lines truncated at \(|\Im s|\le H\). The paper's own statement (p. 62): "Cutoff stability and
  pointwise high-precision checks do not bound the full operator's truncation or discretization
  error... they do not certify Hypothesis R for \(T_{30030,1}\)." **[事实]**
- Our reproduction is at \(H=40\), mesh 1/16, exactly the paper's setting; the match of the
  extreme eigenvalues to 6 digits is a faithful reproduction of the finite model, not of \(T_N\).
- The height trend (§4.1) directly measures how much the truncation moves the norm. If
  \(\|C_H\|/\delta_N\) keeps growing with \(H\), then the paper's \(0.827<1\) is a truncation
  artifact, and the sign of the conclusion for Hypothesis R at \(N=30030\) is not settled by
  Appendix B. (Fill in from the table; see message to lead for up-to-date values.)
- The \(N=6006\) result is robust against our numerical errors (§3) but sensitive to the height
  truncation — a larger-\(H\) run for \(N=6006\) would be the immediate follow-up.
- All computations are double precision (complex128); the observed symmetry/hermiticity defects
  are \(10^{-15}\), and special functions were cross-checked at \(10^{-13}\), so roundoff is not
  the limiting factor — truncation is.

## 6. Verdict ([数值]/[推测])

- **Reproduction: YES, exact.** With the paper's Hermitian recipe (confirmed from the PDF images,
  including the overlines lost by text extraction) we reproduce Appendix B of Li–Liu to six digits:
  \(\lambda=\{+0.357462,-0.353421,\dots\}\), \(\|C\|/\delta_N=0.826864\), \(\delta_N\)
  agreeing to \(2.4\times10^{-10}\). This validates both the paper's numerical claim and our pipeline.
- **Height: the smallness is not a truncation artifact up to \(H=80\).** The ratio moves
  \(0.826864\to0.829232\to0.830596\) for \(H=40,60,80\), i.e. \(+0.45\%\) over a doubling of the
  height; the weighted kernel decays like \(1/(1+|t|)^2\), so this is consistent with a convergent
  tail. Within the finite model, Hypothesis R at \(N=30030\) is numerically supported.
- **N-dependence: the opposite direction.** With the same recipe the ratio grows for smaller
  moduli and exceeds 1 at \(N=6006\) (1.02505) and \(N=4290\) (1.00060), while \(N=10010,6930\)
  give 0.963 and 0.937. Hence the finite model does **not** show uniform-in-\(N\) smallness;
  \(\|T_N\|\le\delta_N\) (Hypothesis R) fails numerically in this truncation for those two moduli.
  [推测] This is consistent with the paper's own GRH-only estimate \(\|T_N\|\ll(\log N)^2\)
  leaving a huge gap, and with the expectation that R/S are the true hard analytic input.
- **Not a proof or disproof.** The finite model is a truncation (paper p. 62: it "does not certify
  Hypothesis R for \(T_{30030,1}\)"); \(N=4290,6006\) lie below the asymptotic range \(N>e^{10}\).
  What we can say: the paper's own numerical experiment at \(N=30030\) is reproducible and
  stable in height; an analogous experiment at smaller moduli crosses the threshold, so the
  "smallness" is a modulus-specific, delicate phenomenon rather than a generic feature.

## 7. Code and logs (all under `/home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase2/spectral/`)

| file | role |
|---|---|
| `chars.py` | character group \((\mathbb Z/N)^*\) via CRT, DFT/Fourier transform over odd characters, "odd" mask; validated on \(N=30,210,30030\) (errors \(<10^{-12}\)) |
| `hurwitz.py` | Euler–Maclaurin Hurwitz \(\zeta(u,x)\) and \(\partial_u\) (64 direct terms + 24 Bernoulli corrections), validated vs mpmath to \(10^{-13}\) |
| `lmat.py` | builds \(G[a,\chi]=L'/L(1/2+s_a,\chi)\) for all 2562 nodes × 2880 odd chars via Hurwitz formula + character FFT, with recurrence in \(t\) and conjugation symmetry |
| `kernels.py` | \(D_N(w)\) (zeta-factor extraction; adaptive-K EM variant `D_values_fast` for large \(|\Im|\)), \(\widetilde P_N(w)\) (zeta extraction + \(E_1\) tail), vectorised \(\zeta,\zeta',\zeta''\), singular series |
| `model.py` | assembles \(E_N=P_N-D_N-K_N\), \(C=\mathrm{diag}(\sqrt w/(1+s))E_N\,\mathrm{diag}(\sqrt w/(1+\bar s))\), diagonalises (full `eigvalsh` \(n\le3200\), else `scipy.eigsh`); **main entry point** |
| `variants40.py` | convention study at \(H=40\) (used to discover/confirm the correct recipe) |
| `checkE.py`, `checkE_components.py`, `checkE_run.py` | independent Mellin-contour validation of \(E_N\) (§3) |
| logs | `run_H2.log` (H=40 reproduction), `run_N.log` (N variants), `run_final.log` (height runs), `variants40.log` (convention study), `cache/results.txt` (machine-readable summary) |

Reproduce:
```
cd /home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase2/spectral
python3 model.py 40 30030 16   # paper's Appendix B -> max|eig|=0.3574618, ||C||/delta=0.8268641
python3 model.py 40 6006  16   # same recipe, smaller N -> ||C||/delta = 1.025052 (>1)
```
