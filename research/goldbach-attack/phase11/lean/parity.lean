/-
Phase-11 Lean artifact: the GWX parity-projection identity (3.1), machine-checked in
Mathlib v4.36.0.

## Statement (GWX (3.1))

For `N ≥ 1`, `m n : ℤ` with `gcd(m n, N) = 1`:

    (1/φ(N)) · Σ_{χ mod N} χ(−1)·χ(m)·χ̄(n)  =  1   if N ∣ (m+n),   else 0.

Since `χ(−1)·χ(m) = χ(−m)`, the sum is the standard second orthogonality relation of
Dirichlet characters: with `a = (−1)·m·n⁻¹` (units!), one has `χ(−1)χ(m)χ(n)⁻¹ = χ(a)`,
and `Σ_χ χ(a) = φ(N)` if `a = 1` and `0` otherwise. Moreover
`a = 1 ↔ m+n ≡ 0 (mod N) ↔ (N : ℤ) ∣ (m+n)`.

## Formalized results

* `chi_neg_one_mul_apply` (part (C)): `χ(−1) · χ(m) = χ(−m)` for **all** `m : ZMod N`
  (no unit hypothesis needed: `MulChar` is multiplicative on all of `ZMod N`).
* `chi_neg_one_sq`, `chi_neg_one_mul_self`, `norm_chi_neg_one` (part (C)):
  `χ(−1)² = 1`, hence `‖χ(−1)‖ = 1`.
* `sum_characters_eq_complex`: orthogonality `Σ_χ χ(a) = φ(N)·1_{a=1}`
  (thin wrapper around Mathlib's `DirichletCharacter.sum_characters_eq`).
* `parity_projection` (**main target (A)**): GWX (3.1) with `IsUnit` hypotheses on the
  residues of `m`, `n` modulo `N` (equivalent to `gcd(mn,N)=1`, see
  `parity_projection_coprime`).

Mathlib ingredients used:
`DirichletCharacter.sum_characters_eq`, `MulChar.map_mul`, `ZMod.inv_mul_of_unit`,
`ZMod.mul_inv_of_unit`, `ZMod.intCast_zmod_eq_zero_iff_dvd`, `Nat.totient_pos`,
`Complex.inv_eq_conj` (available; not needed for the inverse form),
`HasEnoughRootsOfUnity` instance for separably closed fields (ℂ).

No `sorry`; `#print axioms` at the end (all `[propext, Classical.choice, Quot.sound]`).
-/
import Mathlib.NumberTheory.DirichletCharacter.Orthogonality
import Mathlib.Analysis.Complex.Polynomial.Basic
import Mathlib.RingTheory.RootsOfUnity.AlgebraicallyClosed
import Mathlib.GroupTheory.Exponent
import Mathlib.Tactic

open Finset
namespace GWXParity

section Elementary

variable {N : ℕ}

/-- **Part (C1): `χ(−1)·χ(m) = χ(−m)`** (holds for all `m : ZMod N`). -/
theorem chi_neg_one_mul_apply (χ : DirichletCharacter ℂ N) (m : ZMod N) :
    χ (-1) * χ m = χ (-m) := by
  rw [← map_mul, neg_one_mul]

/-- **Part (C2): `χ(−1)² = 1`.** -/
theorem chi_neg_one_sq (χ : DirichletCharacter ℂ N) : χ (-1) ^ 2 = 1 := by
  rw [sq, ← map_mul]
  norm_num

/-- **Part (C2'): `χ(−1)·χ(−1) = 1`.** -/
theorem chi_neg_one_mul_self (χ : DirichletCharacter ℂ N) : χ (-1) * χ (-1) = 1 := by
  rw [← chi_neg_one_sq χ, sq]

/-- **Part (C3): `‖χ(−1)‖ = 1`.** -/
theorem norm_chi_neg_one (χ : DirichletCharacter ℂ N) : ‖χ (-1)‖ = 1 := by
  have h2 : χ (-1) ^ 2 = 1 := chi_neg_one_sq χ
  have h : ‖χ (-1)‖ ^ 2 = 1 := by
    have := congrArg norm h2
    simpa [norm_pow] using this
  have hnn : 0 ≤ ‖χ (-1)‖ := norm_nonneg _
  nlinarith [sq_nonneg (‖χ (-1)‖ - 1)]

end Elementary

section Main

variable {N : ℕ} [NeZero N]

/-- The `HasEnoughRootsOfUnity` instance for `ℂ` needed by Mathlib's character
orthogonality: `ℂ` is separably closed and the exponent of `(ZMod N)ˣ` is positive. -/
instance hasEnoughRootsOfUnity_complex :
    HasEnoughRootsOfUnity ℂ (Monoid.exponent (ZMod N)ˣ) :=
  haveI : NeZero ((Monoid.exponent (ZMod N)ˣ : ℂ)) :=
    ⟨by rw [Nat.cast_ne_zero]; exact Monoid.exponent_ne_zero_of_finite⟩
  inferInstance

/-- Character orthogonality in the form used by the parity projection:
`Σ_χ χ(a) = φ(N)` if `a = 1`, else `0`. -/
theorem sum_characters_eq_complex (a : ZMod N) :
    ∑ χ : DirichletCharacter ℂ N, χ a = if a = 1 then (N.totient : ℂ) else 0 :=
  DirichletCharacter.sum_characters_eq (R := ℂ) a

/-- **(B)-adjacent Mathlib fact**: the number of *all* Dirichlet characters mod `N`
(with values in `ℂ`) is `φ(N)` — a Mathlib instance of the character-counting identity
`Nat.card (DirichletCharacter R n) = n.totient`.  (The *primitive*-character analogue
`Σ_{q|N} φ*(q) = φ(N)` is **not** available in Mathlib; see the report.) -/
theorem card_dirichletCharacter :
    Nat.card (DirichletCharacter ℂ N) = N.totient :=
  DirichletCharacter.card_eq_totient_of_hasEnoughRootsOfUnity (R := ℂ) N

omit [NeZero N] in
/-- `φ(N) ≠ 0` in `ℂ` (so that division by `φ(N)` is legitimate). -/
theorem totient_cast_ne_zero (hN : 0 < N) : (N.totient : ℂ) ≠ 0 := by
  rw [Nat.cast_ne_zero]
  exact (Nat.totient_pos.mpr hN).ne'

/-- **GWX parity-projection identity (3.1), inverse form** (unit hypotheses).
For `N ≥ 1`, integers `m, n` whose residues mod `N` are units:
`(1/φ(N))·Σ_{χ mod N} χ(−1)·χ(m)·χ(n)⁻¹ = 1` if `N ∣ m+n`, else `0`. -/
theorem parity_projection
    (m n : ℤ) (_hm : IsUnit ((m : ZMod N))) (hn : IsUnit ((n : ZMod N))) :
    (1 / (N.totient : ℂ)) *
        (∑ χ : DirichletCharacter ℂ N,
          χ (-1) * χ (m : ZMod N) * (χ (n : ZMod N))⁻¹)
      = if (N : ℤ) ∣ (m + n) then 1 else 0 := by
  -- the parity projection: `χ(−1)χ(m) = χ(−m)`, and `χ(n)⁻¹ = χ(n⁻¹)` for a unit `n`
  set a : ZMod N := ((-1 : ZMod N) * (m : ZMod N)) * ((n : ZMod N))⁻¹ with ha
  have hterm : ∀ χ : DirichletCharacter ℂ N,
      χ (-1) * χ (m : ZMod N) * (χ (n : ZMod N))⁻¹ = χ a := by
    intro χ
    have hn_inv_eq : χ ((n : ZMod N))⁻¹ = (χ (n : ZMod N))⁻¹ := by
      have hmul : χ ((n : ZMod N))⁻¹ * χ (n : ZMod N) = 1 := by
        rw [← map_mul, ZMod.inv_mul_of_unit (n : ZMod N) hn, map_one]
      exact eq_inv_of_mul_eq_one_left hmul
    calc
      χ (-1) * χ (m : ZMod N) * (χ (n : ZMod N))⁻¹
          = χ (-1) * χ (m : ZMod N) * χ ((n : ZMod N))⁻¹ := by rw [← hn_inv_eq]
      _ = (χ ((-1 : ZMod N) * (m : ZMod N))) * χ ((n : ZMod N))⁻¹ := by rw [← map_mul]
      _ = χ (((-1 : ZMod N) * (m : ZMod N)) * ((n : ZMod N))⁻¹) := by rw [← map_mul]
      _ = χ a := by rw [ha]
  have hsum : (∑ χ : DirichletCharacter ℂ N,
        χ (-1) * χ (m : ZMod N) * (χ (n : ZMod N))⁻¹)
      = ∑ χ : DirichletCharacter ℂ N, χ a := by
    exact Finset.sum_congr rfl fun χ _ => hterm χ
  rw [hsum, sum_characters_eq_complex]
  -- reduce `a = 1` to the arithmetic condition `N ∣ m + n`
  have ha_iff : a = 1 ↔ (N : ℤ) ∣ (m + n) := by
    constructor
    · intro h
      -- from `((-1)·m)·n⁻¹ = 1` deduce `(-1)·m = n`
      have h1 : ((-1 : ZMod N) * (m : ZMod N)) = (n : ZMod N) := by
        have hthis :
            ((((-1 : ZMod N) * (m : ZMod N))) * ((n : ZMod N))⁻¹) * (n : ZMod N)
              = (n : ZMod N) := by
          have := congrArg (fun x : ZMod N => x * (n : ZMod N)) h
          simpa [ha, one_mul] using this
        rw [mul_assoc, ZMod.inv_mul_of_unit (n : ZMod N) hn, mul_one] at hthis
        exact hthis
      -- hence `m + n = 0` in `ZMod N`
      have h2 : (m : ZMod N) + (n : ZMod N) = 0 := by
        have hm1 : (-1 : ZMod N) * (m : ZMod N) = -(m : ZMod N) := neg_one_mul _
        rw [hm1] at h1
        rw [← h1]
        exact add_neg_cancel _
      have h3 : ((m + n : ℤ) : ZMod N) = 0 := by
        push_cast
        exact h2
      exact (ZMod.intCast_zmod_eq_zero_iff_dvd (m + n) N).mp h3
    · intro hdiv
      have h3 : ((m + n : ℤ) : ZMod N) = 0 :=
        (ZMod.intCast_zmod_eq_zero_iff_dvd (m + n) N).mpr hdiv
      have h2 : (m : ZMod N) + (n : ZMod N) = 0 := by
        rw [← Int.cast_add, h3]
      have h1 : ((-1 : ZMod N) * (m : ZMod N)) = (n : ZMod N) := by
        have hm_eq : (m : ZMod N) = -(n : ZMod N) := (eq_neg_iff_add_eq_zero).mpr h2
        rw [neg_one_mul, hm_eq, neg_neg]
      rw [ha, h1, ZMod.mul_inv_of_unit (n : ZMod N) hn]
  have hleft : (1 / (N.totient : ℂ)) * (if a = 1 then (N.totient : ℂ) else 0)
      = (if a = 1 then (1 : ℂ) else 0) := by
    split_ifs with ha1
    · have hφ : (N.totient : ℂ) ≠ 0 := totient_cast_ne_zero (NeZero.pos N)
      field_simp
    · simp
  rw [hleft]
  by_cases h : (N : ℤ) ∣ (m + n)
  · rw [ite_eq_left (ha_iff.mpr h), ite_eq_left h]
  · rw [ite_eq_right (fun ha1 => h (ha_iff.mp ha1)), ite_eq_right h]

/-- **GWX parity-projection identity (3.1)**, with the hypothesis stated as
`gcd(mn, N) = 1` in the form of two `IsCoprime` conditions. -/
theorem parity_projection_coprime
    (m n : ℤ) (hm : IsCoprime (N : ℤ) m) (hn : IsCoprime (N : ℤ) n) :
    (1 / (N.totient : ℂ)) *
        (∑ χ : DirichletCharacter ℂ N,
          χ (-1) * χ (m : ZMod N) * (χ (n : ZMod N))⁻¹)
      = if (N : ℤ) ∣ (m + n) then 1 else 0 :=
  parity_projection m n
    ((ZMod.isUnit_intCast_iff_isCoprime m N).mpr hm)
    ((ZMod.isUnit_intCast_iff_isCoprime n N).mpr hn)

end Main

/-! ### Axiom audit -/

#check chi_neg_one_mul_apply
#check chi_neg_one_sq
#check norm_chi_neg_one
#check sum_characters_eq_complex
#check parity_projection
#check parity_projection_coprime
#check card_dirichletCharacter
#print axioms chi_neg_one_mul_apply
#print axioms chi_neg_one_sq
#print axioms norm_chi_neg_one
#print axioms sum_characters_eq_complex
#print axioms parity_projection
#print axioms parity_projection_coprime
#print axioms card_dirichletCharacter

end GWXParity
