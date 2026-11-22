/-!
  Standalone Lean 4 check (NO Mathlib): the "positivity direction" no-go lemma
  in its simplest integer/rational shadow.

  Context: in the Goldbach-attack analysis we proved (informally) that for a real
  inner-product space H, v ≠ 0, c ∈ ℝ, the set of values {c - ⟪T v, v⟫ | T self-adjoint, T ≥ 0}
  equals (-∞, c].  Hence "positivity of T" alone gives only a LOWER constraint on
  c - ⟪Tv,v⟫, never an upper bound: the expression can be made arbitrarily negative,
  while Goldbach needs an upper bound (⟨T v, v⟩ < c).

  Below is the rank-0/integer shadow of that direction lemma:
  as t ranges over the nonnegative integers, c - t ranges exactly over (-∞, c] ∩ ℤ.
  Core Lean 4 only (no Mathlib).
-/

/-- The set of values `c - t` with `t` a nonnegative integer is exactly the set of
integers `x ≤ c`. -/
theorem positivity_direction_int (c x : Int) :
    (∃ t : Int, 0 ≤ t ∧ x = c - t) ↔ x ≤ c := by
  constructor
  · rintro ⟨t, ht, rfl⟩
    omega
  · intro hx
    exact ⟨c - x, by omega, by omega⟩

/-- Consequence: a nonnegative "operator expectation" gives no upper bound; the
resulting expression can be arbitrarily negative, in particular negative. -/
theorem positivity_direction_no_upper_bound (c : Int) :
    ∃ t : Int, 0 ≤ t ∧ c - t < 0 := by
  exact ⟨if 0 ≤ c then c + 1 else 1, by omega, by omega⟩

#check positivity_direction_int
#check positivity_direction_no_upper_bound
#print axioms positivity_direction_int
#print axioms positivity_direction_no_upper_bound
