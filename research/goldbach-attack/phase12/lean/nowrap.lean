/-
Phase-12 Lean artifact, part 1: **no-wrap orthogonality** for Dirichlet characters.

Mathematical content (GWX-style, plan §1.2–1.3 "no-wrap" regime):

* For `q ≥ 1` and units `A B : ZMod q`:
      `Σ_{χ : DirichletCharacter ℂ q} χ(A) · \bar χ(B) = φ(q) · 1_{A=B}`
  (second orthogonality relation; `\bar χ(B) = star (χ B)`).
* Subtracting the principal character `χ = 1`:
      `Σ_{χ ≠ 1} χ(A) · \bar χ(B) = φ(q) · 1_{A=B} − 1`.
  For prime `q` and `A, B < q` with `gcd(A B, q) = 1`, this is exactly the no-wrap
  identity `(q−1)[A=B] − 1` (since then `φ(q) = q−1`, and at `A=B` the sum is `q−2`);
  see `isPrimitive_iff_ne_one_of_prime` and the remarks in the report.
* For prime `q`, `χ ≠ 1 ↔ χ.IsPrimitive` (Mathlib has conductor/`IsPrimitive`), so the
  `χ ≠ 1` sum is also the sum over primitive characters.

Mathlib ingredients: `DirichletCharacter.sum_characters_eq` (first orthogonality),
`MulChar.star_apply'` / `MulChar.inv_apply_eq_inv'` (values of a `ℂ`-valued character:
`star (χ a) = (χ a)⁻¹`), `MulChar.map_mul`, `ZMod.inv_mul_of_unit`, `MulChar.one_apply`.

No `sorry`; axiom audit at the end (expected `[propext, Classical.choice, Quot.sound]`).
-/
import Mathlib.NumberTheory.DirichletCharacter.Orthogonality
import Mathlib.NumberTheory.MulChar.Lemmas
import Mathlib.Analysis.Complex.Polynomial.Basic
import Mathlib.RingTheory.RootsOfUnity.AlgebraicallyClosed
import Mathlib.GroupTheory.Exponent
import Mathlib.Algebra.BigOperators.Group.Finset.Defs
import Mathlib.Tactic

open Finset
open scoped BigOperators
namespace Phase12

section RootsInstance

variable {q : ℕ} [NeZero q]

/-- `ℂ` has enough roots of unity for the character group mod `q`
(needed by Mathlib's character orthogonality). -/
instance hasEnoughRootsOfUnity_complex :
    HasEnoughRootsOfUnity ℂ (Monoid.exponent (ZMod q)ˣ) :=
  haveI : NeZero ((Monoid.exponent (ZMod q)ˣ : ℂ)) :=
    ⟨by rw [Nat.cast_ne_zero]; exact Monoid.exponent_ne_zero_of_finite⟩
  inferInstance

/-- Character orthogonality in the form used below: `Σ_χ χ(a) = φ(q)·1_{a=1}`. -/
theorem sum_characters_eq_complex (a : ZMod q) :
    ∑ χ : DirichletCharacter ℂ q, χ a = if a = 1 then (q.totient : ℂ) else 0 :=
  DirichletCharacter.sum_characters_eq (R := ℂ) a

end RootsInstance

section NoWrap

variable {q : ℕ} [NeZero q]

-- For sums over `Finset.univ.filter (… character predicate …)` we use classical
-- decidability locally (Mathlib does not provide `DecidableEq` for `DirichletCharacter`).
attribute [local instance] Classical.decEq Classical.propDecidable

omit [NeZero q] in
/-- For a `ℂ`-valued character, the complex conjugate of a value is its inverse:
`star (χ a) = (χ a)⁻¹`. -/
theorem star_apply_eq_inv (χ : DirichletCharacter ℂ q) (a : ZMod q) :
    star (χ a) = (χ a)⁻¹ :=
  (MulChar.star_apply' χ a).trans (MulChar.inv_apply_eq_inv' χ a)

/-- **Second orthogonality relation**: for units `A, B` mod `q`,
`Σ_χ χ(A)·\bar χ(B) = φ(q)·1_{A=B}` (all characters mod `q`). -/
theorem char_orthogonality_conj (A B : ZMod q) (hB : IsUnit B) :
    ∑ χ : DirichletCharacter ℂ q, χ A * star (χ B)
      = if A = B then (q.totient : ℂ) else 0 := by
  have hBinv : B⁻¹ * B = 1 := ZMod.inv_mul_of_unit B hB
  have hterm : ∀ χ : DirichletCharacter ℂ q, χ A * star (χ B) = χ (A * B⁻¹) := by
    intro χ
    have hinv : (χ B)⁻¹ = χ (B⁻¹) := by
      have hmul : χ (B⁻¹) * χ B = 1 := by
        rw [← map_mul, hBinv, map_one]
      exact (eq_inv_of_mul_eq_one_left hmul).symm
    calc
      χ A * star (χ B) = χ A * (χ B)⁻¹ := by rw [star_apply_eq_inv]
      _ = χ A * χ (B⁻¹) := by rw [hinv]
      _ = χ (A * B⁻¹) := by rw [← map_mul]
  have hsum : (∑ χ : DirichletCharacter ℂ q, χ A * star (χ B))
      = ∑ χ : DirichletCharacter ℂ q, χ (A * B⁻¹) :=
    Finset.sum_congr rfl fun χ _ => hterm χ
  rw [hsum, sum_characters_eq_complex]
  have hcond : A * B⁻¹ = 1 ↔ A = B := by
    constructor
    · intro h
      calc A = A * 1 := (mul_one A).symm
        _ = A * (B⁻¹ * B) := by rw [hBinv]
        _ = (A * B⁻¹) * B := by rw [mul_assoc]
        _ = 1 * B := by rw [h]
        _ = B := by rw [one_mul]
    · intro h
      rw [h, ZMod.mul_inv_of_unit B hB]
  by_cases h : A = B
  · rw [ite_eq_left (hcond.mpr h), ite_eq_left h]
  · rw [ite_eq_right (fun h' => h (hcond.mp h')), ite_eq_right h]

omit [NeZero q] in
/-- The principal character evaluated at a unit is `1`. -/
theorem one_apply_of_isUnit {A : ZMod q} (hA : IsUnit A) :
    (1 : DirichletCharacter ℂ q) A = 1 :=
  MulChar.one_apply hA

/-- **No-wrap orthogonality, non-principal form**: for units `A, B`,
`Σ_{χ ≠ 1} χ(A)·\bar χ(B) = φ(q)·1_{A=B} − 1`.

For prime `q` this is `(q−1)·1_{A=B} − 1`; with `A, B < q` and `gcd(A B, q) = 1`
(the no-wrap regime), `1_{A=B}` is the plain equality of integers. -/
theorem nonprincipal_orthogonality_conj (A B : ZMod q) (hA : IsUnit A) (hB : IsUnit B) :
    (∑ χ ∈ Finset.univ.filter (fun χ : DirichletCharacter ℂ q => χ ≠ 1),
        χ A * star (χ B))
      = (if A = B then (q.totient : ℂ) else 0) - 1 := by
  classical
  have htotal := char_orthogonality_conj A B hB
  have hsplit := Finset.sum_filter_add_sum_filter_not
    (Finset.univ : Finset (DirichletCharacter ℂ q)) (fun χ : DirichletCharacter ℂ q => χ = 1)
    (fun χ => χ A * star (χ B))
  -- the `χ = 1` part is a single term, equal to `1`
  have hsingle : (∑ χ ∈ Finset.univ.filter (fun χ : DirichletCharacter ℂ q => χ = 1),
      χ A * star (χ B)) = 1 := by
    have hset : (Finset.univ.filter (fun χ : DirichletCharacter ℂ q => χ = 1)) = {1} := by
      ext χ
      simp
    rw [hset, Finset.sum_singleton]
    rw [one_apply_of_isUnit hA, one_apply_of_isUnit hB, star_one, mul_one]
  -- split the total sum: the `χ = 1` part is `1`, the rest is the non-principal sum
  rw [hsingle] at hsplit
  rw [char_orthogonality_conj A B hB] at hsplit
  rw [← hsplit]
  ring

/-- For prime `q`, a character is primitive iff it is non-principal
(its conductor divides `q`, and `conductor = 1 ↔ χ = 1`). -/
theorem isPrimitive_iff_ne_one_of_prime {q : ℕ} (hq : q.Prime) [NeZero q]
    (χ : DirichletCharacter ℂ q) :
    χ.IsPrimitive ↔ χ ≠ 1 := by
  constructor
  · intro hprim h1
    rw [h1] at hprim
    have hc : (1 : DirichletCharacter ℂ q).conductor = 1 := DirichletCharacter.conductor_one
    rw [DirichletCharacter.isPrimitive_def, hc] at hprim
    exact (Nat.Prime.ne_one hq hprim.symm)
  · intro h1
    rw [DirichletCharacter.isPrimitive_def]
    have hdvd : χ.conductor ∣ q := χ.conductor_dvd_level
    have hne1 : χ.conductor ≠ 1 := by
      intro hc
      exact h1 ((DirichletCharacter.eq_one_iff_conductor_eq_one).mpr hc)
    rcases (Nat.Prime.eq_one_or_self_of_dvd hq _ hdvd) with h | h
    · exact absurd h hne1
    · exact h

/-- **No-wrap orthogonality for prime `q`, primitive-character form.**
For prime `q` and units `A, B`, summing over the *primitive* characters mod `q` gives
the same value as summing over `χ ≠ 1`: `φ(q)·1_{A=B} − 1`. -/
theorem primitive_orthogonality_conj {q : ℕ} (hq : q.Prime) [NeZero q]
    (A B : ZMod q) (hA : IsUnit A) (hB : IsUnit B) :
    (∑ χ ∈ Finset.univ.filter (fun χ : DirichletCharacter ℂ q => χ.IsPrimitive),
        χ A * star (χ B))
      = (if A = B then (q.totient : ℂ) else 0) - 1 := by
  classical
  have hset : (Finset.univ.filter (fun χ : DirichletCharacter ℂ q => χ.IsPrimitive))
      = (Finset.univ.filter (fun χ : DirichletCharacter ℂ q => χ ≠ 1)) := by
    ext χ
    simp only [Finset.mem_filter, Finset.mem_univ, true_and]
    exact isPrimitive_iff_ne_one_of_prime hq χ
  rw [hset]
  exact nonprincipal_orthogonality_conj A B hA hB

omit [NeZero q] in
/-- For prime `q`: `φ(q) = q − 1`. -/
theorem totient_prime (hq : q.Prime) : q.totient = q - 1 :=
  Nat.totient_prime hq

end NoWrap

/-! ### Axiom audit -/

#check star_apply_eq_inv
#check char_orthogonality_conj
#check nonprincipal_orthogonality_conj
#check isPrimitive_iff_ne_one_of_prime
#check primitive_orthogonality_conj
#check totient_prime
#print axioms star_apply_eq_inv
#print axioms char_orthogonality_conj
#print axioms nonprincipal_orthogonality_conj
#print axioms isPrimitive_iff_ne_one_of_prime
#print axioms primitive_orthogonality_conj
#print axioms totient_prime

end Phase12
