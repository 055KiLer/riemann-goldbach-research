import Init.Data.Rat.Lemmas

/-!
  Standalone Lean 4 check (NO Mathlib): the rank-one (1-dimensional, rational)
  case of the positivity-direction no-go lemma.

  Informal statement being shadowed:
    For a real inner-product space H, v ≠ 0, c ∈ ℝ:
      { c - ⟪T v, v⟫ | T : H → H self-adjoint, T ≥ 0 } = (-∞, c].
  In dimension 1 every self-adjoint operator is multiplication by some t ∈ ℝ,
  every positive one by some t ≥ 0, and ⟪T v, v⟫ = t·v·v.  Here we formalize this
  rank-one lemma over ℚ using ONLY Lean 4 core (Init.Data.Rat.Lemmas), no Mathlib:

    for c v : ℚ with v ≠ 0:  { c - t·(v·v) | t ≥ 0 } = { x | x ≤ c }.

  Consequence: positivity of the operator alone gives only x ≤ c; the achievable
  set is unbounded below, so it can never certify x > 0.
-/

/-- `a - (a - b) = b` over ℚ. -/
theorem rat_sub_sub_aux (a b : Rat) : a - (a - b) = b := by
  simp only [Rat.sub_eq_add_neg, Rat.neg_add, Rat.neg_neg]
  rw [← Rat.add_assoc, Rat.add_neg_cancel, Rat.zero_add]

/-- Products of squares are nonnegative in ℚ: `0 ≤ v·v`. -/
theorem rat_mul_self_nonneg (v : Rat) : 0 ≤ v * v := by
  rcases Rat.le_total (a := (0 : Rat)) (b := v) with h | h
  · exact Rat.mul_nonneg h h
  · have h2 : 0 ≤ -v := by
      have h' : -(-v) ≤ 0 := by rwa [Rat.neg_neg]
      have := Rat.neg_le_iff (a := (0 : Rat)) (b := -v)
      simpa using this.mpr h'
    have h3 : 0 ≤ (-v) * (-v) := Rat.mul_nonneg h2 h2
    rwa [Rat.neg_mul, Rat.mul_neg, Rat.neg_neg] at h3

/-- A nonzero rational has nonzero square. -/
theorem rat_mul_self_ne_zero (v : Rat) (hv : v ≠ 0) : v * v ≠ 0 := by
  intro h
  rcases Rat.mul_eq_zero.mp h with h1 | h1
  · exact hv h1
  · exact hv h1

/-- A nonzero rational has positive square. -/
theorem rat_mul_self_pos (v : Rat) (hv : v ≠ 0) : 0 < v * v :=
  Rat.lt_of_le_of_ne (rat_mul_self_nonneg v) (fun h => rat_mul_self_ne_zero v hv h.symm)

/-- **Positivity-direction lemma, rank-one case over ℚ.**
For `v ≠ 0` and fixed `c`, the values `c - t·(v·v)` with `t ≥ 0` range over exactly
the rationals `x ≤ c`.  In particular the set is unbounded below: positivity of the
operator (`t ≥ 0`) can only push the value *down*, never bound it away from `-∞`. -/
theorem positivity_direction_rat (c v : Rat) (hv : v ≠ 0) :
    ∀ x : Rat, (∃ t : Rat, 0 ≤ t ∧ x = c - t * (v * v)) ↔ x ≤ c := by
  intro x
  constructor
  · rintro ⟨t, ht, rfl⟩
    have hm : 0 ≤ t * (v * v) := Rat.mul_nonneg ht (rat_mul_self_nonneg v)
    rw [Rat.le_iff_sub_nonneg]
    rw [rat_sub_sub_aux c (t * (v * v))]
    exact hm
  · intro hx
    have hcx : 0 ≤ c - x := (Rat.le_iff_sub_nonneg x c).mp hx
    have hv2pos : 0 < v * v := rat_mul_self_pos v hv
    have hv2ne : v * v ≠ 0 := rat_mul_self_ne_zero v hv
    refine ⟨(c - x) / (v * v), ?_, ?_⟩
    · rw [Rat.div_def]
      exact Rat.mul_nonneg hcx (Rat.le_of_lt (Rat.inv_pos.mpr hv2pos))
    · rw [Rat.div_mul_cancel hv2ne]
      exact (rat_sub_sub_aux c x).symm

#check positivity_direction_rat
#print axioms positivity_direction_rat
#print axioms rat_mul_self_nonneg
