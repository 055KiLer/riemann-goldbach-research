/-
Phase-6 Lean artifact: the finite-dimensional zero–norm dictionary from
Li–Liu, *A Conditional Proof of the Goldbach Conjecture*, §2.4.1–2.4.2 / Theorem 6.1.

## Mathematical statement being formalized

Let `n` be a finite index type, `μ : n → ℝ` a finite family of real eigenvalues
(in the matrix case below, `μ = hC.eigenvalues` for a real symmetric matrix `C`),
`δ > 0`.  Define the finite spectral product

    X(q) = ∏_j (1 − (4 μ_j² / δ²) · q (1 − q)).          (*)

Note on the formula: the paper (1.6) reads
`X_N(q) = ∏_j (1 − (4 μ_j²/δ_N²) q(1-q))`; this is forced by the paper's own
`X_N(0) = X_N(1) = 1` (2.20) and by the factor equation `q(1-q) = d_j/4` with
`d_j = δ²/μ_j²`.  (The task description wrote the factor as `1 − 4μ²/(δ² q(1-q))`
with `q(1-q)` in the denominator, which contradicts (2.20)/(2.21); we formalize
the consistent product (*) that the paper uses.  This is documented honestly in
the report.)

Results formalized (all with no `sorry`, axioms only `propext`, `Classical.choice`,
`Quot.sound`):

* `q_mul_one_sub_pos`, `q_mul_one_sub_le`: for `q ∈ (0,1)`, `0 < q(1-q) ≤ 1/4`.
* `exists_q_mul_one_sub_eq`: `(∃ q ∈ (0,1), q(1-q) = c) ↔ 0 < c ∧ c ≤ 1/4`.
* `factor_zero_iff`: for `δ > 0`, `(∃ q ∈ (0,1), 1 − (4μ²/δ²)q(1-q) = 0) ↔ δ ≤ |μ|`.
* `X_eq_zero_iff_factor`: `X(q) = 0 ↔ ∃ j, (factor j = 0)`.
* `exists_q_zero_iff` (dictionary, part (a)):
    `(∃ q ∈ (0,1), X(q) = 0) ↔ ∃ j, δ ≤ |μ_j|`.
* `no_real_zero_iff` (sharp form of (b)):
    `(∀ q ∈ (0,1), X(q) ≠ 0) ↔ ∀ j, |μ_j| < δ`.
  (The `≤` version is false at the boundary `|μ_j| = δ`, where `q = 1/2` is a zero;
  instead `X_nonneg_of_le` gives `X ≥ 0` on `(0,1)` whenever all `|μ_j| ≤ δ`.)
* `X_one_sub`, `X_zero`, `X_one` (part (c)): `X(1-q) = X(q)`, `X(0) = X(1) = 1`.
* `matrix_exists_q_zero_iff`: instantiation to a real symmetric matrix, with
  `μ := hC.eigenvalues` from Mathlib's spectral theorem for Hermitian matrices.
* `finite_model_chain` (part (d), abstract version): given a self-adjoint operator
  `T` on a real Hilbert space, a unit vector `v` with Rayleigh quotient
  `δ < ⟨T v, v⟩`, and the spectral bridge `(‖T‖ ≤ B ↔ ∀ j, |μ_j| ≤ B)`,
  conclude `¬ (‖T‖ ≤ δ)` (Hypothesis R fails) **and** `X_δ` has a real zero in
  `(0,1)`.  (The bridge is exactly the spectral-theorem content connecting the
  operator norm with the eigenvalue family; here it is an explicit hypothesis.)
-/
import Mathlib.Analysis.Real.Sqrt
import Mathlib.Algebra.BigOperators.GroupWithZero.Finset
import Mathlib.Analysis.Matrix.Spectrum
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.Normed.Operator.Basic
import Mathlib.Tactic

open scoped BigOperators InnerProductSpace
open Finset

namespace LLDictionary

/-! ### Part 1: the finite spectral product and its factor -/

section Algebra

variable {n : Type*} [Fintype n]

/-- The finite spectral product `X(q) = ∏_j (1 − (4 μ_j²/δ²)·q(1−q))` from LL (1.6). -/
noncomputable def X (δ : ℝ) (μ : n → ℝ) (q : ℝ) : ℝ :=
  ∏ j, (1 - 4 * (μ j) ^ 2 * (q * (1 - q)) / δ ^ 2)

/-- For `q ∈ (0,1)`: `0 < q(1-q)`. -/
theorem q_mul_one_sub_pos {q : ℝ} (hq : q ∈ Set.Ioo 0 1) : 0 < q * (1 - q) := by
  have h0 : 0 < q := hq.1
  have h1 : q < 1 := hq.2
  nlinarith

/-- `q(1-q) ≤ 1/4` for all real `q`. -/
theorem q_mul_one_sub_le (q : ℝ) : q * (1 - q) ≤ 1 / 4 := by
  nlinarith [sq_nonneg (q - 1 / 2)]

/-- `q(1-q) = c` is solvable with `q ∈ (0,1)` exactly when `0 < c ≤ 1/4`. -/
theorem exists_q_mul_one_sub_eq {c : ℝ} :
    (∃ q : ℝ, q ∈ Set.Ioo 0 1 ∧ q * (1 - q) = c) ↔ 0 < c ∧ c ≤ 1 / 4 := by
  constructor
  · rintro ⟨q, hq, rfl⟩
    exact ⟨q_mul_one_sub_pos hq, q_mul_one_sub_le q⟩
  · rintro ⟨hc0, hc⟩
    have hc4 : 4 * c ≤ 1 := by linarith
    have hnonneg : 0 ≤ 1 - 4 * c := by linarith
    -- explicit solution q = (1 + sqrt(1-4c))/2  (works also for c = 1/4)
    refine ⟨(1 + Real.sqrt (1 - 4 * c)) / 2, ?_, ?_⟩
    · have hs0 : 0 ≤ Real.sqrt (1 - 4 * c) := Real.sqrt_nonneg _
      have hs1 : Real.sqrt (1 - 4 * c) < 1 := by
        have h := (Real.sqrt_lt hnonneg zero_le_one).mpr (by nlinarith : 1 - 4 * c < 1 ^ 2)
        simpa using h
      constructor <;> nlinarith
    · have hsq : (Real.sqrt (1 - 4 * c)) ^ 2 = 1 - 4 * c := Real.sq_sqrt hnonneg
      nlinarith

/-- **The factor equation / zero–norm dictionary at one eigenvalue.**
For `δ > 0` and `μ ∈ ℝ`:
`(∃ q ∈ (0,1), 1 − (4μ²/δ²) q(1−q) = 0) ↔ δ ≤ |μ|`. -/
theorem factor_zero_iff {δ : ℝ} (hδ : 0 < δ) (μ : ℝ) :
    (∃ q : ℝ, q ∈ Set.Ioo 0 1 ∧ 1 - 4 * μ ^ 2 * (q * (1 - q)) / δ ^ 2 = 0) ↔
      δ ≤ |μ| := by
  have hδ2 : (0:ℝ) < δ ^ 2 := by positivity
  constructor
  · rintro ⟨q, hq, hfac⟩
    -- from the factor equation: 4 μ² q(1-q) = δ²
    have hmul : 4 * μ ^ 2 * (q * (1 - q)) = δ ^ 2 := by
      field_simp [hδ.ne'] at hfac
      linarith
    have hqpos : 0 < q * (1 - q) := q_mul_one_sub_pos hq
    have hqle : q * (1 - q) ≤ 1 / 4 := q_mul_one_sub_le q
    -- δ² = 4μ²q(1-q) ≤ μ²
    have hsq : δ ^ 2 ≤ μ ^ 2 := by nlinarith
    have habs : |δ| ≤ |μ| := (sq_le_sq).mp hsq
    simpa [abs_of_pos hδ] using habs
  · intro hδμ
    have hμpos : 0 < |μ| := lt_of_lt_of_le hδ hδμ
    have hμne : μ ≠ 0 := by
      intro hμ
      rw [hμ, abs_zero] at hμpos
      exact lt_irrefl 0 hμpos
    have hμ2 : (0:ℝ) < μ ^ 2 := by positivity
    -- the candidate value c = δ²/(4μ²) lies in (0, 1/4]
    have hcpos : 0 < δ ^ 2 / (4 * μ ^ 2) := by positivity
    have hcle : δ ^ 2 / (4 * μ ^ 2) ≤ 1 / 4 := by
      rw [div_le_iff₀ (by positivity : (0:ℝ) < 4 * μ ^ 2)]
      have habs : |δ| ≤ |μ| := by rwa [abs_of_pos hδ]
      have hsq : δ ^ 2 ≤ μ ^ 2 := by simpa using (sq_le_sq).mpr habs
      nlinarith
    obtain ⟨q, hq, hqe⟩ :=
      (exists_q_mul_one_sub_eq (c := δ ^ 2 / (4 * μ ^ 2))).mpr ⟨hcpos, hcle⟩
    refine ⟨q, hq, ?_⟩
    have hmul : 4 * μ ^ 2 * (q * (1 - q)) = δ ^ 2 := by
      rw [hqe]
      field_simp
    field_simp [hδ.ne']
    linarith

/-- `X(q) = 0` if and only if at least one factor vanishes. -/
theorem X_eq_zero_iff_factor {δ : ℝ} {μ : n → ℝ} {q : ℝ} :
    X δ μ q = 0 ↔ ∃ j, 1 - 4 * (μ j) ^ 2 * (q * (1 - q)) / δ ^ 2 = 0 := by
  unfold X
  rw [Finset.prod_eq_zero_iff]
  simp

/-- **Part (a): the zero–norm dictionary (real zeros in `(0,1)`).**
`X_δ` has a real zero in `(0,1)` iff some eigenvalue satisfies `|μ_j| ≥ δ`. -/
theorem exists_q_zero_iff {δ : ℝ} (hδ : 0 < δ) (μ : n → ℝ) :
    (∃ q : ℝ, q ∈ Set.Ioo 0 1 ∧ X δ μ q = 0) ↔ ∃ j, δ ≤ |μ j| := by
  constructor
  · rintro ⟨q, hq, hX⟩
    rw [X_eq_zero_iff_factor] at hX
    obtain ⟨j, hj⟩ := hX
    exact ⟨j, (factor_zero_iff hδ (μ j)).mp ⟨q, hq, hj⟩⟩
  · rintro ⟨j, hj⟩
    obtain ⟨q, hq, hfac⟩ := (factor_zero_iff hδ (μ j)).mpr hj
    exact ⟨q, hq, X_eq_zero_iff_factor.mpr ⟨j, hfac⟩⟩

/-- **Part (b), sharp form (easy direction).**
`X_δ` has no real zero in `(0,1)` iff all eigenvalues satisfy `|μ_j| < δ`.
(The boundary case `|μ_j| = δ` gives the real zero `q = 1/2`; see `factor_zero_iff`.) -/
theorem no_real_zero_iff {δ : ℝ} (hδ : 0 < δ) (μ : n → ℝ) :
    (∀ q : ℝ, q ∈ Set.Ioo 0 1 → X δ μ q ≠ 0) ↔ ∀ j, |μ j| < δ := by
  constructor
  · intro h j
    by_contra hcon
    have hle : δ ≤ |μ j| := not_lt.mp hcon
    obtain ⟨q, hq, hfac⟩ := (factor_zero_iff hδ (μ j)).mpr hle
    exact h q hq (X_eq_zero_iff_factor.mpr ⟨j, hfac⟩)
  · intro h q hq hX
    rw [X_eq_zero_iff_factor] at hX
    obtain ⟨j, hj⟩ := hX
    have hle : δ ≤ |μ j| := (factor_zero_iff hδ (μ j)).mp ⟨q, hq, hj⟩
    have := h j
    linarith

/-- **Part (b), `≤` version can only give nonnegativity** (zeros may occur at `|μ_j| = δ`). -/
theorem X_nonneg_of_le {δ : ℝ} (hδ : 0 < δ) (μ : n → ℝ)
    (h : ∀ j, |μ j| ≤ δ) {q : ℝ} (hq : q ∈ Set.Ioo 0 1) : 0 ≤ X δ μ q := by
  unfold X
  apply Finset.prod_nonneg
  intro j _
  have hq0 : 0 < q * (1 - q) := q_mul_one_sub_pos hq
  have hqle : q * (1 - q) ≤ 1 / 4 := q_mul_one_sub_le q
  have hμ2 : (μ j) ^ 2 ≤ δ ^ 2 := by
    have h' : |μ j| ≤ |δ| := by
      rw [abs_of_pos hδ]
      exact h j
    simpa using (sq_le_sq).mpr h'
  have hδ2 : (0:ℝ) < δ ^ 2 := by positivity
  have hfac : 4 * (μ j) ^ 2 * (q * (1 - q)) / δ ^ 2 ≤ 1 := by
    rw [div_le_one hδ2]
    nlinarith
  linarith

/-- **Part (c): symmetry `X(1−q) = X(q)`** (from `q(1−q)` invariance). -/
theorem X_one_sub (δ : ℝ) (μ : n → ℝ) (q : ℝ) :
    X δ μ (1 - q) = X δ μ q := by
  unfold X
  apply Finset.prod_congr rfl
  intro j _
  ring_nf

/-- **Part (c): `X(0) = 1`** (paper (2.20)). -/
@[simp] theorem X_zero (δ : ℝ) (μ : n → ℝ) : X δ μ 0 = 1 := by
  simp [X]

/-- **Part (c): `X(1) = 1`** (paper (2.20)). -/
@[simp] theorem X_one (δ : ℝ) (μ : n → ℝ) : X δ μ 1 = 1 := by
  simp [X]

end Algebra

/-! ### Part 2: instantiation with Mathlib spectral-theorem eigenvalues -/

section MatrixCase

open Matrix

variable {n : Type*} [Fintype n] [DecidableEq n]

omit [Fintype n] [DecidableEq n] in
/-- A real symmetric matrix is a Hermitian matrix (`IsSymm` is `IsHermitian` for `ℝ`). -/
theorem isHermitian_of_isSymm (C : Matrix n n ℝ) (hC : C.IsSymm) : C.IsHermitian := by
  simpa [Matrix.IsSymm, Matrix.IsHermitian] using hC

/-- **Dictionary for a real symmetric matrix.**
Taking `μ := eigenvalues` of a real symmetric matrix (Mathlib's spectral theorem for
Hermitian matrices, `Matrix.IsHermitian.eigenvalues`), the zero–norm dictionary reads:
`X_δ` has a real zero in `(0,1)` iff some eigenvalue has absolute value at least `δ`. -/
theorem matrix_exists_q_zero_iff
    (C : Matrix n n ℝ) (hC : C.IsSymm) {δ : ℝ} (hδ : 0 < δ) :
    (∃ q : ℝ, q ∈ Set.Ioo 0 1 ∧
        X δ ((isHermitian_of_isSymm C hC).eigenvalues) q = 0) ↔
      ∃ j, δ ≤ |(isHermitian_of_isSymm C hC).eigenvalues j| :=
  exists_q_zero_iff hδ ((isHermitian_of_isSymm C hC).eigenvalues)

end MatrixCase

/-! ### Part 3: abstract chain with the phase-5 Rayleigh-quotient bridge (part (d)) -/

section Chain

open scoped InnerProductSpace

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℝ H]

/-- Absolute Rayleigh-quotient bound (same as `phase5_mathlib.abs_rayleigh_le_opNorm`). -/
theorem abs_rayleigh_le_opNorm (T : H →L[ℝ] H) (v : H) :
    |⟪T v, v⟫_ℝ| ≤ ‖T‖ * ‖v‖ ^ 2 := by
  calc
    |⟪T v, v⟫_ℝ| ≤ ‖T v‖ * ‖v‖ := abs_real_inner_le_norm (T v) v
    _ ≤ (‖T‖ * ‖v‖) * ‖v‖ := by
      gcongr
      exact T.le_opNorm v
    _ = ‖T‖ * ‖v‖ ^ 2 := by ring

/-- Abstract form of Hypothesis R: the operator-norm bound `‖T_N‖ ≤ δ_N`. -/
def HypothesisR (T : H →L[ℝ] H) (δ : ℝ) : Prop := ‖T‖ ≤ δ

/-- Unit Rayleigh quotient above `δ` refutes Hypothesis R
(same as `phase5_mathlib.rayleigh_gt_refutes_R`). -/
theorem rayleigh_gt_refutes_R (T : H →L[ℝ] H) (δ : ℝ) (v : H) (hv : ‖v‖ = 1)
    (h : δ < ⟪T v, v⟫_ℝ) : ¬ HypothesisR T δ := by
  have h1 : δ < ‖T‖ := h.trans_le (by
    calc
      ⟪T v, v⟫_ℝ ≤ |⟪T v, v⟫_ℝ| := le_abs_self _
      _ ≤ ‖T‖ * ‖v‖ ^ 2 := abs_rayleigh_le_opNorm T v
      _ = ‖T‖ := by rw [hv]; ring)
  exact not_le.mpr h1

/-- **Part (d): the finite-model chain** ("certified Rayleigh quotient > δ ⇒ real zero of X
⇒ not R"), in abstract form.

Hypotheses:
* `T` a bounded operator (in LL: the boundary operator `T_N`);
* `hRay : δ < ⟨T v, v⟩` for a unit vector `v` — this is exactly what a certified finite-model
  (Nyström compression) Rayleigh quotient provides, modulo quadrature error;
* `μ : n → ℝ` the eigenvalue family of `T`;
* `hbridge : ∀ B, ‖T‖ ≤ B ↔ ∀ j, |μ_j| ≤ B` — the spectral-theorem content identifying
  the operator norm with the sup of absolute eigenvalues (explicit hypothesis here).

Conclusions: `¬ HypothesisR T δ` (Hypothesis R fails at this `N`) and `X_δ` has a real zero
in `(0,1)` (the zero-side of the dictionary). -/
theorem finite_model_chain
    (T : H →L[ℝ] H) {δ : ℝ} (hδ : 0 < δ) (v : H) (hv : ‖v‖ = 1)
    (hRay : δ < ⟪T v, v⟫_ℝ) {n : Type*} [Fintype n] (μ : n → ℝ)
    (hbridge : ∀ B : ℝ, ‖T‖ ≤ B ↔ ∀ j, |μ j| ≤ B) :
    ¬ HypothesisR T δ ∧ ∃ q : ℝ, q ∈ Set.Ioo 0 1 ∧ X δ μ q = 0 := by
  have hnR : ¬ HypothesisR T δ := rayleigh_gt_refutes_R T δ v hv hRay
  refine ⟨hnR, ?_⟩
  have hnot : ¬ ∀ j, |μ j| ≤ δ := fun h => hnR ((hbridge δ).mpr h)
  push Not at hnot
  obtain ⟨j, hj⟩ := hnot
  exact (exists_q_zero_iff hδ μ).mpr ⟨j, le_of_lt hj⟩

end Chain

/-! ### Axiom audit -/

#check q_mul_one_sub_pos
#check q_mul_one_sub_le
#check exists_q_mul_one_sub_eq
#check factor_zero_iff
#check exists_q_zero_iff
#check no_real_zero_iff
#check X_nonneg_of_le
#check X_one_sub
#check matrix_exists_q_zero_iff
#check finite_model_chain
#check X_zero
#check X_one
#print axioms q_mul_one_sub_pos
#print axioms q_mul_one_sub_le
#print axioms exists_q_mul_one_sub_eq
#print axioms factor_zero_iff
#print axioms exists_q_zero_iff
#print axioms no_real_zero_iff
#print axioms X_nonneg_of_le
#print axioms matrix_exists_q_zero_iff
#print axioms finite_model_chain
#print axioms X_zero
#print axioms X_one

end LLDictionary
