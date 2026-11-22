/-
Phase-5 Lean artifact (Mathlib version).

Context (LL Prop 5.3 / Hypothesis R):
The Li–Liu construction has a boundary integral operator `T̃_N` on `L²(Γ_N)` which is
self-adjoint, whose range lies in the Hardy trace space `H_N ⊂ L²(Γ_N)`, and which
annihilates `H_N^⊥`; hence `T̃_N = T_N ⊕ 0`, and for every unit `v ∈ L²(Γ_N)`
    ⟨T̃_N v, v⟩ = ⟨T_N (P_H v), (P_H v)⟩  ≤  ‖T_N‖ · ‖P_H v‖² ≤ ‖T_N‖.
So a certified finite-model (Nyström compression) Rayleigh quotient
`λ̃ = ⟨T_N v, v⟩ > δ_N` forces `‖T_N‖ > δ_N`, i.e. refutes Hypothesis R at that N.

This file formalizes the abstract mathematical content of that inference:

* `abs_rayleigh_le_opNorm`:      |⟨T v,v⟩| ≤ ‖T‖·‖v‖²       (no symmetry needed)
* `selfAdjoint_inner_eq_starProjection`:
                                 range(T) ⊆ M ⇒ ⟨T v,v⟩ = ⟨T (P_M v), (P_M v)⟩
                                 (this is the operator-level content of `T̃_N = T_N ⊕ 0`)
* `selfAdjoint_eq_starProjection_comp`:
                                 T = P_M ∘ T ∘ P_M
* `transfer_rayleigh_unit_le`:   unit v ⇒ |⟨T v,v⟩| ≤ ‖T‖ (and, when ‖T‖ ≤ ‖T_M‖,
                                 the bound by ‖T_M‖)
* `hypothesisR_implies_abs_rayleigh_le`:
                                 ‖T‖ ≤ δ ⇒ |⟨T v,v⟩| ≤ δ  for unit v  ("R ⇒ bound")
* `rayleigh_gt_refutes_R`:       δ < ⟨T v,v⟩, ‖v‖ = 1 ⇒ ¬ ‖T‖ ≤ δ  (the phase-5 crux)
* `matrix_rayleigh_gt_implies_norm_gt`: finite-dimensional matrix version (Lemma B)

No `sorry`; `#print axioms` at the end shows the (standard) axiom footprint.
-/
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.InnerProductSpace.Projection.Basic
import Mathlib.Analysis.InnerProductSpace.Orthogonal
import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.Analysis.Matrix.Hermitian
import Mathlib.Analysis.Normed.Operator.Basic
import Mathlib.LinearAlgebra.Matrix.Symmetric
import Mathlib.Tactic.Ring
import Mathlib.Tactic.GCongr

open scoped InnerProductSpace Matrix Matrix.Norms.L2Operator

/-! ### Part 1: abstract Hilbert-space transfer lemmas -/

section Transfer

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℝ H] [CompleteSpace H]

omit [CompleteSpace H] in
/-- Absolute Rayleigh-quotient bound for an arbitrary bounded operator (no symmetry needed). -/
theorem abs_rayleigh_le_opNorm (T : H →L[ℝ] H) (v : H) :
    |⟪T v, v⟫_ℝ| ≤ ‖T‖ * ‖v‖ ^ 2 := by
  calc
    |⟪T v, v⟫_ℝ| ≤ ‖T v‖ * ‖v‖ := abs_real_inner_le_norm (T v) v
    _ ≤ (‖T‖ * ‖v‖) * ‖v‖ := by
      gcongr
      exact T.le_opNorm v
    _ = ‖T‖ * ‖v‖ ^ 2 := by ring

/-- **Transfer identity (operator-level `T̃_N = T_N ⊕ 0`).**
If `T` is self-adjoint and maps `H` into the closed subspace `M`, then the quadratic form of `T`
only depends on the projection `P_M v`: `⟨T v, v⟩ = ⟨T (P_M v), (P_M v)⟩`. -/
theorem selfAdjoint_inner_eq_starProjection
    (T : H →L[ℝ] H) (hT : IsSelfAdjoint T)
    (M : Submodule ℝ H) [M.HasOrthogonalProjection]
    (hTM : ∀ x : H, T x ∈ M) (v : H) :
    ⟪T v, v⟫_ℝ = ⟪T (M.starProjection v), M.starProjection v⟫_ℝ := by
  have hsym : (T : H →ₗ[ℝ] H).IsSymmetric :=
    ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric.mp hT
  have hw : v - M.starProjection v ∈ Mᗮ := M.sub_starProjection_mem_orthogonal v
  -- T kills the `Mᗮ` component of `v`
  have hker : T (v - M.starProjection v) = 0 := by
    have hzero : ⟪T (v - M.starProjection v), T (v - M.starProjection v)⟫_ℝ = 0 := by
      calc
        ⟪T (v - M.starProjection v), T (v - M.starProjection v)⟫_ℝ
            = ⟪v - M.starProjection v, T (T (v - M.starProjection v))⟫_ℝ :=
              hsym (v - M.starProjection v) (T (v - M.starProjection v))
        _ = 0 := (Submodule.mem_orthogonal' (K := M) (v - M.starProjection v)).mp hw _
            (hTM (T (v - M.starProjection v)))
    exact inner_self_eq_zero.mp hzero
  have hTP : T (M.starProjection v) = T v := by
    have hsub : T v - T (M.starProjection v) = 0 := by
      rw [← map_sub]
      exact hker
    exact (sub_eq_zero.mp hsub).symm
  calc
    ⟪T v, v⟫_ℝ = ⟪T (M.starProjection v), v⟫_ℝ := by rw [← hTP]
    _ = ⟪M.starProjection v, T v⟫_ℝ := hsym _ _
    _ = ⟪M.starProjection v, T (M.starProjection v)⟫_ℝ := by rw [hTP]
    _ = ⟪T (M.starProjection v), M.starProjection v⟫_ℝ := real_inner_comm _ _

/-- **Compression identity:** `T = P_M ∘ T ∘ P_M` when `T` is self-adjoint with range in `M`. -/
theorem selfAdjoint_eq_starProjection_comp
    (T : H →L[ℝ] H) (hT : IsSelfAdjoint T)
    (M : Submodule ℝ H) [M.HasOrthogonalProjection]
    (hTM : ∀ x : H, T x ∈ M) (v : H) :
    T v = M.starProjection (T (M.starProjection v)) := by
  have hsym : (T : H →ₗ[ℝ] H).IsSymmetric :=
    ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric.mp hT
  have hker : T (v - M.starProjection v) = 0 := by
    have hzero : ⟪T (v - M.starProjection v), T (v - M.starProjection v)⟫_ℝ = 0 := by
      calc
        ⟪T (v - M.starProjection v), T (v - M.starProjection v)⟫_ℝ
            = ⟪v - M.starProjection v, T (T (v - M.starProjection v))⟫_ℝ :=
              hsym (v - M.starProjection v) (T (v - M.starProjection v))
        _ = 0 := (Submodule.mem_orthogonal' (K := M) (v - M.starProjection v)).mp
            (M.sub_starProjection_mem_orthogonal v) _ (hTM (T (v - M.starProjection v)))
    exact inner_self_eq_zero.mp hzero
  have hTP : T (M.starProjection v) = T v := by
    have hsub : T v - T (M.starProjection v) = 0 := by
      rw [← map_sub]
      exact hker
    exact (sub_eq_zero.mp hsub).symm
  rw [M.starProjection_eq_self_iff.mpr (hTM (M.starProjection v))]
  exact hTP.symm

/-- **Lemma A (transfer / Rayleigh bound).**
For a unit vector `v`, the Rayleigh quotient of a self-adjoint operator with range in `M`
is bounded by the operator norm: `|⟨T v, v⟩| ≤ ‖T‖`.
(With `T = T_M ⊕ 0` one has `‖T‖ = ‖T_M‖`; see `transfer_rayleigh_unit_le_of_le_norm`.) -/
theorem transfer_rayleigh_unit_le
    (T : H →L[ℝ] H) (hT : IsSelfAdjoint T)
    (M : Submodule ℝ H) [M.HasOrthogonalProjection]
    (hTM : ∀ x : H, T x ∈ M) (v : H) (hv : ‖v‖ = 1) :
    |⟪T v, v⟫_ℝ| ≤ ‖T‖ := by
  rw [selfAdjoint_inner_eq_starProjection T hT M hTM v]
  have hb := abs_rayleigh_le_opNorm T (M.starProjection v)
  have hPle : ‖M.starProjection v‖ ≤ 1 := by
    calc
      ‖M.starProjection v‖ ≤ ‖M.starProjection‖ * ‖v‖ := M.starProjection.le_opNorm v
      _ = ‖M.starProjection‖ := by rw [hv, mul_one]
      _ ≤ 1 := M.starProjection_norm_le
  have hsq : ‖M.starProjection v‖ ^ 2 ≤ 1 := pow_le_one₀ (norm_nonneg _) hPle
  calc
    |⟪T (M.starProjection v), M.starProjection v⟫_ℝ|
        ≤ ‖T‖ * ‖M.starProjection v‖ ^ 2 := hb
    _ ≤ ‖T‖ * 1 := by gcongr
    _ = ‖T‖ := by ring

/-- Version of Lemma A with the norm of the compression `T_M` as target bound:
if `‖T‖ ≤ ‖T_M‖` and `‖v‖ = 1` then `|⟨T v,v⟩| ≤ ‖T_M‖`. -/
theorem transfer_rayleigh_unit_le_of_le_norm
    (T : H →L[ℝ] H) (hT : IsSelfAdjoint T)
    (M : Submodule ℝ H) [M.HasOrthogonalProjection]
    (hTM : ∀ x : H, T x ∈ M) (TMnorm : ℝ) (hTle : ‖T‖ ≤ TMnorm)
    (v : H) (hv : ‖v‖ = 1) :
    |⟪T v, v⟫_ℝ| ≤ TMnorm :=
  (transfer_rayleigh_unit_le T hT M hTM v hv).trans hTle

end Transfer

/-! ### Part 2: the phase-5 inference (Hypothesis R ⇒ bound; certified Rayleigh ⇒ ¬ R) -/

section Inference

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℝ H]

/-- The assertion "Hypothesis R holds at this operator with threshold `δ`" in its abstract form:
the operator norm is at most `δ`.  (In LL, `R(N) ⇔ ‖T_N‖ ≤ δ_N`.) -/
def HypothesisR (T : H →L[ℝ] H) (δ : ℝ) : Prop := ‖T‖ ≤ δ

/-- **Lemma C (`R ⇒ quadratic-form bound`).**
If `‖T‖ ≤ δ` then every unit vector has `|⟨T v,v⟩| ≤ δ`. -/
theorem hypothesisR_implies_abs_rayleigh_le
    (T : H →L[ℝ] H) (δ : ℝ) (hR : HypothesisR T δ) (v : H) (hv : ‖v‖ = 1) :
    |⟪T v, v⟫_ℝ| ≤ δ := by
  calc
    |⟪T v, v⟫_ℝ| ≤ ‖T‖ * ‖v‖ ^ 2 := abs_rayleigh_le_opNorm T v
    _ = ‖T‖ := by rw [hv]; ring
    _ ≤ δ := hR

/-- **Phase-5 crux (contrapositive form).**
A certified unit vector whose Rayleigh quotient exceeds `δ` refutes `‖T‖ ≤ δ`
(i.e. refutes Hypothesis R at the corresponding `N`). -/
theorem rayleigh_gt_refutes_R
    (T : H →L[ℝ] H) (δ : ℝ) (v : H) (hv : ‖v‖ = 1) (h : δ < ⟪T v, v⟫_ℝ) :
    ¬ HypothesisR T δ := by
  have h1 : δ < ‖T‖ := h.trans_le (by
    calc
      ⟪T v, v⟫_ℝ ≤ |⟪T v, v⟫_ℝ| := le_abs_self _
      _ ≤ ‖T‖ * ‖v‖ ^ 2 := abs_rayleigh_le_opNorm T v
      _ = ‖T‖ := by rw [hv]; ring)
  exact not_le.mpr h1

end Inference

/-! ### Part 3: finite-dimensional (matrix) version — Lemma B -/

section MatrixCase

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- A real symmetric matrix gives a self-adjoint continuous linear operator on `EuclideanSpace`. -/
theorem isSymm_toEuclideanCLM_isSelfAdjoint (C : Matrix n n ℝ) (hC : C.IsSymm) :
    IsSelfAdjoint (Matrix.toEuclideanCLM (n := n) (𝕜 := ℝ) C) := by
  rw [ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric,
    Matrix.coe_toEuclideanCLM_eq_toEuclideanLin]
  exact Matrix.isSymmetric_toEuclideanLin_iff.mpr (by
    simpa [Matrix.IsSymm, Matrix.IsHermitian] using hC)

/-- **Lemma B (matrix Rayleigh lower bound for the operator norm).**
If `C` is a real symmetric `n × n` matrix, `v` is a unit vector and the quadratic form
satisfies `δ < v ⬝ᵥ (C *ᵥ v)`, then the L2 operator norm of `C` exceeds `δ`. -/
theorem matrix_rayleigh_gt_implies_norm_gt
    (C : Matrix n n ℝ) (hC : C.IsSymm) (v : EuclideanSpace ℝ n) (hv : ‖v‖ = 1)
    (δ : ℝ) (h : δ < v ⬝ᵥ (C *ᵥ v)) :
    δ < ‖C‖ := by
  -- the symmetry hypothesis is exactly what makes the matrix operator self-adjoint
  have hsa : IsSelfAdjoint (Matrix.toEuclideanCLM (n := n) (𝕜 := ℝ) C) :=
    isSymm_toEuclideanCLM_isSelfAdjoint C hC
  have hq : v ⬝ᵥ (C *ᵥ v) = ⟪Matrix.toEuclideanCLM (n := n) (𝕜 := ℝ) C v, v⟫_ℝ := by
    rw [real_inner_comm, Matrix.inner_toEuclideanCLM]
  rw [hq] at h
  have h1 : δ < ‖Matrix.toEuclideanCLM (n := n) (𝕜 := ℝ) C‖ := h.trans_le (by
    calc
      ⟪Matrix.toEuclideanCLM (n := n) (𝕜 := ℝ) C v, v⟫_ℝ ≤ |⟪Matrix.toEuclideanCLM (n := n) (𝕜 := ℝ) C v, v⟫_ℝ| :=
        le_abs_self _
      _ ≤ ‖Matrix.toEuclideanCLM (n := n) (𝕜 := ℝ) C‖ * ‖v‖ ^ 2 :=
        abs_rayleigh_le_opNorm (Matrix.toEuclideanCLM (n := n) (𝕜 := ℝ) C) v
      _ = ‖Matrix.toEuclideanCLM (n := n) (𝕜 := ℝ) C‖ := by rw [hv]; ring)
  rwa [Matrix.l2_opNorm_toEuclideanCLM] at h1

/-- Lemma B stated with the L2 operator norm on matrices (`Matrix.Norms.L2Operator`):
`vᵀ C v > δ` for a unit `v` implies `‖C‖ > δ`. -/
theorem matrix_rayleigh_gt_implies_opNorm_gt
    (C : Matrix n n ℝ) (hC : C.IsSymm) (v : EuclideanSpace ℝ n) (hv : ‖v‖ = 1)
    (δ : ℝ) (h : δ < v ⬝ᵥ (C *ᵥ v)) :
    δ < ‖Matrix.toEuclideanCLM (n := n) (𝕜 := ℝ) C‖ := by
  have hsa : IsSelfAdjoint (Matrix.toEuclideanCLM (n := n) (𝕜 := ℝ) C) :=
    isSymm_toEuclideanCLM_isSelfAdjoint C hC
  have hq : v ⬝ᵥ (C *ᵥ v) = ⟪Matrix.toEuclideanCLM (n := n) (𝕜 := ℝ) C v, v⟫_ℝ := by
    rw [real_inner_comm, Matrix.inner_toEuclideanCLM]
  rw [hq] at h
  exact h.trans_le (by
    calc
      ⟪Matrix.toEuclideanCLM (n := n) (𝕜 := ℝ) C v, v⟫_ℝ ≤ |⟪Matrix.toEuclideanCLM (n := n) (𝕜 := ℝ) C v, v⟫_ℝ| :=
        le_abs_self _
      _ ≤ ‖Matrix.toEuclideanCLM (n := n) (𝕜 := ℝ) C‖ * ‖v‖ ^ 2 :=
        abs_rayleigh_le_opNorm (Matrix.toEuclideanCLM (n := n) (𝕜 := ℝ) C) v
      _ = ‖Matrix.toEuclideanCLM (n := n) (𝕜 := ℝ) C‖ := by rw [hv]; ring)

end MatrixCase

/-! ### Axiom audit (printed at compile time) -/

#check abs_rayleigh_le_opNorm
#check selfAdjoint_inner_eq_starProjection
#check transfer_rayleigh_unit_le
#check hypothesisR_implies_abs_rayleigh_le
#check rayleigh_gt_refutes_R
#check matrix_rayleigh_gt_implies_norm_gt
#print axioms abs_rayleigh_le_opNorm
#print axioms selfAdjoint_inner_eq_starProjection
#print axioms transfer_rayleigh_unit_le
#print axioms hypothesisR_implies_abs_rayleigh_le
#print axioms rayleigh_gt_refutes_R
#print axioms matrix_rayleigh_gt_implies_norm_gt
