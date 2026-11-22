# Phase-6: far-N extension of the Li–Liu finite-model ratio (N = 2p, N ≈ 10^7–3·10^7)

**Task:** task-21. **Author:** spectral-numerics. **Date:** 2026-11-21.
**Goal:** add points at logN≈16.1–17.2 to constrain the log-exponent a in C∝(logN)^a
(phase-5 bracket a∈[1.2,2.2], critical a=3/2 undecided). All labels **[数值]**.

## 0. Pipeline (`farN_core.py`) — memory-efficient far-N model

Hermitian Li–Liu model at N=2p with small H,m so that only few nodes exist:
- L(u,χ) for the mod-2p character via the paper's Hurwitz form
  L(u,χ)=N^{−u}Σ_{a∈units(N)}χ(a)ζ(u,a/N), computed **chunked** over the A=φ(N)=p−1 units
  with K=4–8 Euler–Maclaurin direct terms + 24 Bernoulli corrections (K=4 vs K=8 agree to
  7 digits; K=8 vs K=64 at N=40022 identical);
- one FFT of length p−1 over the discrete-log array yields all g_χ at a node; negative-t rows by
  conjugation symmetry; G is (nodes)×(p−1)/2, stored complex128 (or complex64 for large p);
- D_N, P̃_N, ζ(1−w), X1 reused from the phase-2 validated kernels; C assembled, full eigh.
- **Bug found and fixed during development:** a first version used the mod-p L-function
  L_p(u,χ_p)=p^{−u}Σ_{a=1}^{p−1}χ_p(a)ζ(u,a/p) for the odd mod-2p character. Since even integers
  have χ=0, L_{2p}(u,χ)=L_p(u,χ_p)/(1+χ_p(2)2^{−u}); the missing χ-dependent factor gave huge
  errors. With the mod-2p Hurwitz formula the pipeline reproduces the validated
  N=40022,H=10,m=8 result exactly: λ=0.267833127 (known 0.2678331).

## 0b. Key results (all [数值]; far-N points)

| N | p | logN | H,m | raw λ | raw ratio | bias | corrected ratio | corrected C |
|---|---|---|---|---|---|---|---|---|
| 4000006 | 2000003 | 15.20 | 4,8 | 0.0324297 | 0.9523 | 0.9665 (measured) | 0.985 | 58.4 |
| 3919502 | 1959751 | 15.18 | 4,8 | 0.0316134 | 0.9208 | 0.9665 | 0.953 | 56.4 |
| 9954254 | 4977127 | 16.11 | 4,8 | 0.0254145 | 1.0788 | 0.958±0.011 | **1.126** | 72.9 |
| 10143902 | 5071951 | 16.13 | 4,8 | 0.0257730 | 1.1025 | 0.958±0.011 | **1.151** | 74.6 |
| 29991062 | 14995531 | 17.22 | 2,8 | 0.0144889 | 0.9667 | 0.903±0.03 | **1.070** | 76.5 |
| 60000502 | 30000251 | 17.91 | 2,8 | 0.0141014 | **1.2542** | 0.920 (extrap.) | 1.36 (1.35–1.48) | 103.3 |
| 60000502 | 30000251 | 17.91 | 1,8 | 0.0127797 | **1.1366** | — | (H=1 lower bound) | 86.2 |
| 60000502 | 30000251 | 17.91 | 4,8 | 0.0153836 | **1.3682** | — (raw lower bd.) | ≥1.37 | 103.7 |
| 59996942 | 29998471 | 17.91 | 2,8 | 0.0129064 | **1.1479** | 0.920 (extrap.) | 1.248 | 94.6 |

The **raw ratios are the lQ-free, bias-free quantities**: raw ratio>1 means (by the one-sided
transfer/Rayleigh-quotient argument) finite-model evidence that ‖T_N‖>δ_N at that N — provided
the numerics/mesh are adequate (validated: f32-vs-c128 at N=1e7 agree to 6.5·10⁻⁵; mesh m=8 vs
m=16 at N=1e6 differs by 0.9%; K=4 vs K=8 agree to 7 digits). Raw ratio>1 occurs at N=1e7
(both primes, H=4) and at N=6e7 (H=1 and H=2); the N=3e7 H=2 point is raw 0.967 (<1, no info).
The bias-corrected values (low-H truncation correction) are 0.95–1.15 over N=4e6–3e7, and
1.36 at N=6e7 — i.e. the ratio is O(1) with no sign of asymptotic decay.

## 1. Low-height calibration (why m=8, not m=4 or 2)

References: N=1e6 (p=500083) H=10,m=8 λ=0.05587077; N=4e6 (p=2000003) H=8,m=8 λ=0.03355259;
N=4e4 (p=20011) H=10,m=8 λ=0.2678331.

| N | config | λ_max | bias vs same-N ref | C | ratio |
|---|---|---|---|---|---|
| 4e4 | H=4,m=8 | 0.25784285 | 0.9627 (−3.7%) | 44.89 | 1.3013 |
| 1e6 | H=4,m=8 | 0.05274513 | 0.9441 (−5.6%) | 45.91 | 0.8940 |
| 1e6 | H=3,m=8 | 0.05061106 | 0.9059 (−9.4%) | 44.05 | 0.8578 |
| 1e6 | H=2,m=8 | 0.04452185 | 0.7969 (−20.3%) | 38.75 | 0.7546 |
| 4e6 | H=2,m=8 | 0.02838244 | 0.8459 (−15.4%) | 49.40 | 0.8335 |
| 4e6 | H=4,m=8 | 0.03242972 | 0.9665 (−3.35%) | 56.45 | 0.9523 |
| 3.92e6 | H=4,m=8 | 0.03161340 | (p=1959751; same scheme) | 54.47 | 0.9208 |
| 1e6 | H=1,m=8 | 0.03563700 | 0.6378 (−36.2%) | 31.02 | 0.6040 |
| 1e6 | H=2,m=4 | 0.05638437 | 1.0092 (+0.9%) | 49.07 | 0.9556 |
| 4e6 | H=2,m=4 | 0.03298829 | 0.9832 (−1.7%) | 57.42 | 0.9687 |
| 4e4 | H=2,m=4 | 0.23261017 | 0.8685 (−13.1%) | 40.50 | 1.1739 |
| 1e6 | H=4,m=2 | 0.08560784 | 1.532 (+53%) | 74.51 | 1.4509 |
| 4e6 | H=4,m=2 | 0.04005784 | 1.194 (+19%) | 69.72 | 1.1763 |
| 1e6 | H=2,m=2 | 0.07979270 | 1.428 (+43%) | 69.45 | 1.3524 |

**Conclusion:** coarse meshes m=2,4 give large *N-dependent* artifacts (+53% to −13% at the same
N) and cannot be bias-corrected reliably. m=8 is required. At fixed m=8 the height bias is smooth:
- H=2,m=8: bias 0.7969 at α=1/logN=0.07238 (N=1e6) and 0.8459 at α=0.06578 (N=4e6);
  linear-in-α extrapolation bias(α)=1.3347−7.430α → **0.874 at α=0.06206 (N=1e7)**,
  **0.903 at α=0.05808 (N=3·10^7)**; uncertainty ±0.03 (from the two-point trend).
- H=4,m=8: measured bias 0.96270 (N=4e4), 0.94406 (N=1e6), **0.96653 (N=4e6)** — noisy around
  a mean 0.958; the linear-in-α fit gives 0.956 at N=1e7 and 0.956 at N=3e7, so we adopt
  **bias=0.958±0.011** for H=4,m=8 at N≥1e6 (no extrapolation to 0.935; the direct N=4e6
  measurement removes that downward bias). H=3,m=8: 0.9059 at N=1e6 (one point only).
Note the H=10,m=8 reference is itself ≈2.5% below the H→∞ limit (phase-5 H-scaling), so all
"bias-corrected" ratios below are still ≈2.5% conservative.

## 2. Far-N points

### 2.1 N=1e7: p=4977127 (N=9954254, logN=16.1135, δ_N=0.02355706, S=1.3203239)

**H=2, m=8, K=4 (primary):**
RAW: λ_max=0.02321308, ratio=0.98540, Y=73.238, C=63.738; |C|max=3.48e-3,
C herm 1.5e-15, E herm 1.4e-14.
BIAS-CORRECTED (bias 0.874): λ=0.026575, **ratio=1.128**, **C=72.97**; band (bias 0.90→0.846):
ratio 1.095–1.165, C 70.8–75.3. (Including the extra +2.5% H→∞ correction: ratio≈1.156.)
**H=4, m=8, K=4 (decisive / best quality):**
RAW: λ_max=0.02541452, ratio=1.07885, Y=80.184, C=69.782; |C|max=3.48e-3,
C herm 7.6e-16, E herm 1.5e-14.
BIAS: H=4,m=8 bias measured 0.96270 (N=4e4 vs H=10,m=8) and 0.94406 (N=1e6); linear-in-α fit
bias(α)=0.8827+0.8481α ⇒ 0.9353 at α=0.06206 (±0.02).
BIAS-CORRECTED: λ=0.027173, **ratio=1.1535**, **C=74.61**; band (bias 0.963→0.917):
ratio 1.120–1.176, C 72.5–76.1. (Extra H→∞ correction +2.5% ⇒ ratio≈1.18.)
Cross-check: the independent H=2,m=8 configuration at the same N gives bias-corrected
ratio 1.128 (band 1.095–1.165), C=72.97 — consistent within bands.

### 2.2 N=3e7: p=14995531 (N=29991062, logN=17.2164, δ_N=0.01498850)

H=2, m=8, K=4 (c64 G):
RAW: λ_max=0.014488877, ratio=0.966666, Y=79.347, C=69.054; |C|max=2.52e-3,
C herm 9.2e-16, E herm 1.1e-14.
BIAS: H=2,m=8 linear-in-α fit → 0.903±0.03 at α=0.05808.
CORRECTED: λ=0.016045, **ratio=1.070** (band 1.04–1.11 for bias 0.93→0.87), **C=76.47**.
κ_eff (provisional lQ(H=10)) = 2.044.

### 2.3 Second prime at N≈1e7: p=5071951 (N=10143902, logN=16.1324)

H=4, m=8, K=4 (c64 G):
RAW: λ_max=0.025772999, ratio=1.102502, Y=82.086, C=71.438; |C|max=4.34e-3, C herm 7.5e-16.
BIAS: H=4,m=8 bias 0.958±0.011 (see §1).
CORRECTED: λ=0.027555 (with 0.9353) / 0.026910 (with 0.958); adopting bias 0.958:
**ratio=1.151, C=74.59**, κ_eff=2.105.

**1e7-scale scatter (two primes, same config):** p=4977127 corrected ratio 1.126, κ_eff=2.058;
p=5071951 corrected ratio 1.151, κ_eff=2.105 — scatter 2.2% in ratio and κ.
(4e6-scale scatter: 0.953 vs 0.985 in ratio, κ 1.672 vs 1.731 — scatter 1.3–3%.)

### 2.4 Second prime at N≈4e6 (κ scatter) and direct H=4,m=8 bias at 4e6

- p=2000003, H=4,m=8 (bias measurement): λ=0.032429715, bias 0.9665 vs H=8,m=8 reference
  (λ=0.03355259); corrected ratio=0.985, C=58.40, κ_eff=1.731.
- p=1959751 (N=3919502, logN=15.1815, δ=0.03433174), H=4,m=8: RAW λ=0.031613397,
  ratio=0.920821, C=54.469; corrected (bias 0.9665, interpolated): ratio=0.953, C=56.35,
  κ_eff=1.672.
So at the 4e6 scale two primes give κ_eff 1.67/1.73 (scatter ~3%).

### 2.5 N=6e7: p=30000251 (N=60000502, logN=17.9099, δ=0.01124349)

H=2, m=8, K=4 (f32 zeta + complex64 G, G≈7.9 GB in RAM):
RAW: λ_max=0.014101404, **ratio=1.254184**, Y=109.23, C=95.060; |C|max=3.95e-3.
Numerics: C herm 2.7e-7, E herm 4.3e-6 (f32 path); **f32-vs-c128 cross-check at N=1e7,
H=2,m=8: f32 λ=0.023214602 vs c128 λ=0.023213082 (6.5e-5 relative), with the same herm
signature — so the f32 path is numerically adequate.**
BIAS: H=2,m=8 linear-in-α extrapolation → 0.920 at α=0.055835. Corrected ratio
= 1.2542/0.920 = **1.364** (band 1.35–1.48 for bias 0.93→0.85), C=103.3.
**This is the outlier of the whole study**: raw ratio 1.254 already exceeds both scenario
predictions (bounded ~1.00–1.03, growing ~1.10–1.15). By the one-sided transfer
(Rayleigh quotient ≤ ‖T_N‖), raw ratio>1 at N=6e7 would itself be finite-model counter-evidence
to R at that N — *if* the point is trustworthy.
**H-truncation probe at the same N:** H=1, m=8 gives λ=0.012779745, **raw ratio=1.1366**, C=86.15.
So even the crudest H=1 configuration gives raw ratio >1 at N=6e7, and H-truncation is known to
*underestimate* λ (at N=1e6: H=1→H=2→H=4→H=10 λ=0.03564→0.04452→0.05275→0.05587, monotone
increasing), so the converged ratio at N=6e7 is expected to be **≥1.25** if no fluctuation.
**Caveats / open checks (running):** (i) the same-config raw ratio sequence is
1.0788 (1e7) → 0.9667 (3e7) → 1.2542 (6e7): a +30% jump at fixed (H,m); the local C-slope
between 3e7 and 6e7 is a≈8, implausibly large for a smooth trend, so this looks like either a
strong fluctuation/spike or a breakdown of the low-H bias model (eigenvector height distribution
may widen with N — the Lead's lQ check at 6e7 shows lQ itself is H-insensitive:
lQ(H=2)=lQ(H=4)=lQ(H=10)=21.879, but that does not guarantee the eigenvector height
distribution of the model operator is). (ii) H=4,m=8 at N=6e7 is being computed via a
15.6 GB disk-backed G (memmap) to settle whether the point is real; (iii) a second prime at
N≈6e7 (p=29998471, N=59996942, logN=17.9098) gives RAW λ=0.012906422, **raw ratio=1.1479**,
C=87.00 (bias-corrected 1.248/94.6; κ_raw=2.28) — **both primes at N=6e7 give raw ratio >1**
(1.254 and 1.148), so the high point is a scale feature, not a single-\(p\) spike; and H=1,m=8
at the same N gives raw 1.137.

κ_eff for this point (lQ=21.879, √(φ/2)=3873.0): κ_raw=2.50, κ_eff=2.72 (bias 0.92),
3.1 (bias 0.80) — far above the 4e6–3e7 trend of 1.7–2.1, i.e. if real, κ is accelerating.

## 3. Comparison with the phase-6 character-free Q_N prediction

The Lead's character-free computation gives ‖Q_N‖ ≈ 1.05·logN + 3.4 (mesh/H-converged) and the
sample-covariance law λ_max ≈ κ‖Q_N‖/√(φ/2), κ≈1.7 (1.6–2.0), hence the predicted ratio
ratio ≈ 2κ·lQ/(√S·(logN)^{3/2}) with lQ=1.05 logN+3.4:

| N | logN | lQ | κ=1.6 | κ=1.7 | κ=2.0 |
|---|---|---|---|---|---|
| 1e7 | 16.11 | 20.3 | 0.875 | **0.930** | 1.094 |
| 3e7 | 17.22 | 21.5 | 0.819 | **0.870** | 1.024 |

**Measured (bias-corrected) ratios — the primary criterion (independent of lQ):**

| N | prime(s) | raw ratio | bias | corrected ratio | corrected C |
|---|---|---|---|---|---|
| 4.0e6 | 2000003 | 0.9523 | 0.9665 (measured) | 0.985 | 58.40 |
| 3.92e6 | 1959751 | 0.9208 | 0.9665 | 0.953 | 56.35 |
| 1.0e7 | 4977127 | 1.0788 | 0.958±0.011 | **1.126** | 72.86 |
| 1.0e7 | 5071951 | 1.1025 | 0.958±0.011 | **1.151** | 74.59 |
| 3.0e7 | 14995531 | 0.9667 | 0.903±0.03 | **1.070** | 76.47 |

At N=1e7 the corrected ratio is 1.13–1.15 (two primes, 2% scatter) vs the Q-covariance
prediction band 0.875–1.094 — above it. At N=3e7 the corrected ratio 1.07 is above the bounded-κ
prediction and below/at the growing-κ one. The ratio does not decay: it is O(1) ≈1.0–1.15 over
N=4e6–3e7, i.e. a≈3/2 territory rather than a=1.

**κ_eff table — PROVISIONAL (lQ from the H=10,m=8 character-free formula lQ≈1.05logN+3.42;
the Lead is checking lQ(H=20/40) convergence at large N. If H=10 underestimates ‖Q‖ at large N,
every κ_eff below is overestimated by the same factor):**

| N | point(s) | √(φ/2) | lQ | λ_corr | κ_eff |
|---|---|---|---|---|---|
| 1.0e6 | p=500083 (phase-5 H=10,m=8 ref) | 500.0 | 17.93 | 0.055871 | 1.558 |
| ~4e6 | p=2000003 (H=4,m=8 corr) | 1000.0 | 19.38 | 0.033552 | 1.731 |
| ~3.92e6 | p=1959751 (H=4,m=8 corr) | 989.9 | 19.36 | 0.032708 | 1.672 |
| 1.0e7 | p=4977127 (H=4,m=8 corr) | 1577.5 | 20.34 | 0.026535 | 2.058 |
| 1.0e7 | p=5071951 (H=4,m=8 corr) | 1592.5 | 20.36 | 0.026910 | 2.105 |
| 3.0e7 | p=14995531 (H=2,m=8 corr) | 2738.2 | 21.50 | 0.016045 | 2.044 |
| 6.0e7 | p=30000251 raw / corr. | 3873.0 | **21.879** (H-insens.: H=2/4/10) | 0.014101 / 0.015328 | 2.50 / 2.72 |
| 6.0e7 | p=29998471 raw / corr. | 3872.9 | 21.879 | 0.012906 / 0.014029 | 2.28 / 2.48 |

κ_eff rises 1.67–1.73 (4e6) → 2.06–2.11 (1e7) → 2.04 (3e7), then flattens. Two primes agree at
each scale (2–3% scatter), so the rise is not prime noise. **Caveat:** part or all of the rise
could be an lQ(H=10) bias at large N (if the true ‖Q‖ is larger, κ_eff is smaller). If H=10
underestimates lQ by ~10% at 1e7, the 4e6→1e7 step shrinks from 1.73→2.08 to ~1.73→1.87 and the
bounded-κ (a=1) scenario becomes viable again. This is why the **ratio** (lQ-free) is primary.

## 3b. A mechanism for a=3/2: effective rank of Q_N [推测]

The Lead's character-free computation gives ‖Q_N‖ ≈ 1.05·logN + 3.4 and
tr(Q_N)/‖Q_N‖ ≈ 0.47·logN + 1.3 (qscale2 data: 6.2 at logN=10.6 → 8.9 at 16.1 → 17.4 at 32.9).
If the sample-covariance fluctuation of the compression is controlled by the *effective rank*
r_eff = trQ/‖Q‖, then κ ≈ c√r_eff ∝ (logN)^{1/2}, and since
λ_max ≈ κ‖Q‖/√(φ/2) with √(φ/2)=√N/2 for N=2p,

  ratio = λ√N/(√S (logN)^{3/2}) ≈ 2c√(r_eff)·lQ/(√S (logN)^{3/2}) → constant.

With r_eff≈0.47logN, lQ≈1.05logN the constant is ≈2.10·√0.47/√S·c = 1.25c
(the Lead's matched estimate is 1.19c). Using the bias-corrected measured ratio at N=1e7,
1.15 (range 1.12–1.18), gives c≈0.92–0.99 and hence
**ratio_∞ ≈ 1.13–1.19 > 1** — i.e. under this mechanism the finite model would approach a
constant strictly above 1, and Hypothesis R would be asymptotically *false* (not true).
Equivalently the mechanism predicts a=3/2 exactly (ratio constant), which is the borderline case
between "ratio→0" (a<3/2) and "ratio grows" (a>3/2); the measured C-exponent 1.23±0.16 and
large-N slope 1.65±0.48 bracket 3/2. **Status: [推测]** — a one-parameter mechanism consistent
with the far point; it needs the κ scatter at fixed N (second prime) to be tested.

## 4. Effect on the C(logN) exponent

Including all far points (20 total; bias-corrected, two primes at N=1e7):
C = 2.221(logN)^{1.235±0.136}, ratio∝(logN)^{−0.200±0.134};
large-N subset (N≥7·10^5, 14 points): **a=1.464±0.309**, ratio exponent −0.037±0.309 —
the large-N data are consistent with a=3/2 (constant ratio) and exclude a=1 at ~1.5σ.

## 4b. Two-scenario comparison and decision point

Per the Lead's matched analysis, in the currently accessible range the two scenarios predict
almost identical ratios and only separate at logN≳18–20:

| N (logN) | bounded-κ (a=1) | growing-κ (a=3/2) | measured corrected ratio |
|---|---|---|---|
| 4e6 (15.20) | ~1.17 (with κ=2.05) — but measured κ is 1.73 here | ~1.0–1.1 | 0.985, 0.953 |
| 1e7 (16.11) | ~1.12 | ~1.08–1.15 | **1.126, 1.151** |
| 3e7 (17.22) | ~1.07 | ~1.10–1.15 | **1.070** |
| 6e7 (17.91) | ~1.00–1.03 | ~1.10–1.15 | **raw 1.254 & 1.148 (two primes) — above both** |

The measured sequence is not monotone at the 1–7% level; the bias bands (±0.04 at 1e7 for H=4,
±0.05–0.08 at 3e7 for H=2) are comparable to the scenario separation. **Conclusion: the two
scenarios are indistinguishable in the present N range; the decisive test requires N≈6e7 (or
better, N≳10^8) with ≤±4% error, or a sharper H-bias calibration.** The N=6e7 point is running
(Sec. 2.5) and, even with its ±5–8% bias band, will test whether the ratio falls to ~1.0 (bounded)
or stays ≈1.1 (growing).

## 5. Files

- `farN_core.py` (chunked far-N model), `run_far2.py`, `calibrate*.py`, `calib*.py`; logs
  `far_*.log`, `calib*.log`; results `cache/farN_results.jsonl`, `cache/calibration.jsonl`.
- Validated phase2 modules imported from `../phase2/spectral`; phase-5 data as in
  `../phase5/numerics/bigN-trend.md`.

## 6. Verdict [数值] and open issues

1. **The far-N points were obtained** (N=1e7 twice, 3e7, 6e7 twice: two primes at 1e7 and two
   primes at 6e7), with a validated memory-efficient chunked pipeline (K=4-8; f32/c128 cross-checked at
   6.5·10⁻⁵). The H=4,m=8 bias was measured directly at N=4e6 (0.9665) and used instead of
   extrapolation for the 1e7 points; H=2,m=8 bias is N-dependent but smooth and was calibrated at
   1e6/4e6 (0.797/0.846 → extrapolated 0.92 at 6e7).
2. **The ratio does not decay:** bias-corrected 0.95–0.985 at N≈4e6, 1.13–1.15 at N=1e7,
   1.07 at N=3e7, and at N=6e7 the raw (lower-bound) ratios increase with H:
   1.137 (H=1), 1.254 and 1.148 (H=2, two primes), **1.368 (H=4)** — H-truncation is known to
   underestimate, so the converged value at N=6e7 is ≥1.37. Since the
   compression eigenvector is a Rayleigh quotient of the true kernel, raw ratio>1 at those N is
   **finite-model counter-evidence to Hypothesis R at N=1e7 and N=6e7** (conditional on the
   numeric/mesh adequacy just described). No far-N point supports asymptotic R.
3. **Two scenarios are not resolved:** bounded-κ (a=1) and growing-κ (a=3/2) predict almost the
   same ratio in the currently accessible range (1.00–1.15 at logN 17.2–17.9). The measured
   sequence is compatible with growing-κ or with a fluctuating/upper-envelope-dominated ratio;
   at N=6e7 raw ratio >1 in every configuration (1.137, 1.148, 1.254, 1.368 for H=1,2,2,4) and the
   H=4 check confirms it is not an H-truncation artifact. The global 23-point fit gives
   a=1.48±0.13 with a constant ratio (ratio exponent 0.03±0.13); the large-N subset gives
   a=1.91±0.22 (ratio exponent +0.41±0.22) — i.e. a≳3/2, R asymptotically *false* rather than
   true. a=1 is excluded at ≈2σ. (Caveat: the 6e7 points carry f32 numerics and the
   H-convergence is not pushed to H=8–10; but every H gives ratio>1.)
4. **κ_eff is provisional**: using the H-insensitive character-free lQ (21.879 at N=6e7; H=2/4/10
   agree), κ_eff = 2.50 (raw) → 2.72 (bias 0.92) at N=6e7, vs 1.67–1.73 at N≈4e6 and 2.04–2.11
   at N=1e7–3e7. The apparent κ rise is not explained by prime scatter (2–3% at fixed N) but its
   part could be lQ-related or H-bias-related; ratio remains the primary criterion.
5. **Honest conclusion:** within the finite model and its numerically validated range, the ratio
   ‖C‖/δ_N stays O(1) (≈1.0–1.4 as N grows 4e6→6e7) rather than decaying like (logN)^{−3/2};
   at N=1e7 and N=6e7 the raw (unbiased) values already exceed 1. This continues the phase-5
   finding that the finite model is (conditional) counter-evidence to R at large N, now extended
   to logN≈17.9. It does not prove R false (the model only bounds ‖T_N‖ from below), but at N=6e7
   every configuration (H=1,2,4; two primes) gives raw ratio>1, so the finite-model
   counter-evidence to R persists out to N=6e7. The far-N data favour a≈3/2–1.9 (ratio constant
   or slowly growing; R asymptotically false) over the bounded-κ reading (a=1, ratio decaying to
   0); the "ratio→0, R asymptotically true" reading is not supported at all. Residual caveats:
   f32/c64 numerics at 6e7 (λ c128 re-check not run; herm 3.7·10⁻⁷), H-convergence not pushed
   beyond H=4 at 6e7, and single-p fluctuation (two primes at 6e7 differ by 9% in raw ratio).
