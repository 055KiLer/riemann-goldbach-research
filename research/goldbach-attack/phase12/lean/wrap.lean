/-
Phase-12 Lean artifact, part 2: **wrap counting identities** (Finset-level).

Mathematical content (phase-12 plan §1.3; "wrap" regime `X > q`, where pairs with
`A ≡ B (mod q)` and `A ≠ B` appear):

* `card_pairs_mod_eq`: for `q > 0` and `S, T ⊆ [0, q)`,
    `#{(a,b) ∈ S × T : a ≡ b (mod q)} = #(S ∩ T)`
  (because `a, b < q` forces `a ≡ b ↔ a = b`). This is the elementary count behind
  "no-wrap" vs "wrap" in the 2-vs-2 construction.
* `wrap_identity`: for any `q > 0`, `M` and coefficient functions `c, d : ℕ → ℂ`,
  with `C_r = Σ_{A < M, A ≡ r (mod q)} c_A`, `D_r = Σ_{B < M, B ≡ r (mod q)} d_B`:
    `Σ_{A < M} Σ_{B < M, B ≡ A (mod q), B ≠ A} c_A d_B
        = Σ_{r < q} C_r D_r − Σ_{A < M} c_A d_A`.
  This is the finite "wrap" bookkeeping identity: total same-residue pairing minus the
  diagonal.
* `nat_mod_eq_iff_dvd_sub`: the bridge between the residue form `A % q = B % q` and the
  `kq` difference form `(q : ℤ) ∣ (A - B)` — i.e. `A − B = k q` for some integer `k`.
  This is the arithmetic bridge from plan §1.3's `W = Σ_{k≠0} Σ_{nm−rl = kq} …` form to
  the residue-grouped form.

No `sorry`; axiom audit at the end.
-/
import Mathlib.Algebra.BigOperators.Group.Finset.Defs
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Data.Nat.ModEq
import Mathlib.Data.Int.ModEq
import Mathlib.Tactic

open Finset
open scoped BigOperators
namespace Phase12

/-! ### 1. Pairs with the same residue, when the range is shorter than `q` -/

/-- For `q > 0` and `S, T ⊆ [0, q)`, the pairs `(a,b) ∈ S × T` with `a ≡ b (mod q)`
are exactly the diagonal pairs `(x,x)`, `x ∈ S ∩ T`. -/
theorem card_pairs_mod_eq {q : ℕ} (_hq : 0 < q) (S T : Finset ℕ)
    (hS : ∀ a ∈ S, a < q) (hT : ∀ b ∈ T, b < q) :
    ((S.product T).filter (fun p : ℕ × ℕ => p.1 % q = p.2 % q)).card
      = (S ∩ T).card := by
  classical
  have hiff : ∀ a ∈ S, ∀ b ∈ T, (a % q = b % q ↔ a = b) := by
    intro a ha b hb
    rw [Nat.mod_eq_of_lt (hS a ha), Nat.mod_eq_of_lt (hT b hb)]
  have hset : (S.product T).filter (fun p : ℕ × ℕ => p.1 % q = p.2 % q)
      = (S ∩ T).image (fun x => (x, x)) := by
    ext p
    constructor
    · intro hp
      obtain ⟨hpS, hmod⟩ := Finset.mem_filter.mp hp
      obtain ⟨ha, hb⟩ := Finset.mem_product.mp hpS
      have heq : p.1 = p.2 := (hiff p.1 ha p.2 hb).mp hmod
      obtain ⟨a, b⟩ := p
      simp only at heq
      refine Finset.mem_image.mpr ⟨a, Finset.mem_inter.mpr ⟨ha, heq ▸ hb⟩, Prod.ext rfl ?_⟩
      · simp [heq]
    · intro hp
      obtain ⟨x, hx, rfl⟩ := Finset.mem_image.mp hp
      obtain ⟨hxS, hxT⟩ := Finset.mem_inter.mp hx
      rw [Finset.mem_filter]
      exact ⟨Finset.mem_product.mpr ⟨hxS, hxT⟩, (hiff x hxS x hxT).mpr rfl⟩
  rw [hset, Finset.card_image_of_injective _ (fun a b h => by simpa using congrArg Prod.fst h)]

/-! ### 2. The finite wrap identity -/

section Wrap

variable {q M : ℕ}

/-- Sum of the coefficients `c_A` over `A < M` in the residue class `r` mod `q`
(`C_r` in the plan's notation). -/
noncomputable def residueSum (q M : ℕ) (c : ℕ → ℂ) (r : ℕ) : ℂ :=
  ∑ A ∈ (Finset.range M).filter (fun A => A % q = r), c A

/-- **Wrap identity**: total same-residue pairing minus the diagonal.
`Σ_{A < M} Σ_{B < M, B≡A mod q, B≠A} c_A d_B = Σ_{r<q} C_r D_r − Σ_{A<M} c_A d_A`. -/
theorem wrap_identity (hq : 0 < q) (c d : ℕ → ℂ) :
    (∑ A ∈ Finset.range M,
        ∑ B ∈ (Finset.range M).filter (fun B => B % q = A % q ∧ B ≠ A), c A * d B)
      = (∑ r ∈ Finset.range q, residueSum q M c r * residueSum q M d r)
        - ∑ A ∈ Finset.range M, c A * d A := by
  classical
  -- Step 1: the inner sum is `c A * (D_{A%q} - d A)`
  have hinner : ∀ A ∈ Finset.range M,
      (∑ B ∈ (Finset.range M).filter (fun B => B % q = A % q ∧ B ≠ A), c A * d B)
        = c A * (residueSum q M d (A % q) - d A) := by
    intro A hA
    rw [← Finset.mul_sum]
    congr 1
    -- inner sum = residue class sum minus the diagonal term `d A`
    have hset : (Finset.range M).filter (fun B => B % q = A % q ∧ B ≠ A)
        = ((Finset.range M).filter (fun B => B % q = A % q)).erase A := by
      ext B
      simp only [Finset.mem_filter, Finset.mem_erase]
      constructor
      · rintro ⟨hB, hmod, hne⟩
        exact ⟨hne, hB, hmod⟩
      · rintro ⟨hne, hB, hmod⟩
        exact ⟨hB, hmod, hne⟩
    have hAin : A ∈ (Finset.range M).filter (fun B => B % q = A % q) := by
      rw [Finset.mem_filter]
      exact ⟨hA, rfl⟩
    rw [hset]
    -- `Σ over s.erase A = Σ over s − d A`
    have h := Finset.sum_erase_add (s := (Finset.range M).filter (fun B => B % q = A % q))
      (f := d) hAin
    -- h : d A + Σ x ∈ s.erase A, d x = Σ x ∈ s, d x
    rw [residueSum]
    rw [← h]
    ring
  -- Step 2: reindex the sum by residue classes
  have hmem : ∀ A ∈ Finset.range M, A % q ∈ Finset.range q := by
    intro A _
    rw [Finset.mem_range]
    exact Nat.mod_lt _ hq
  have hreindex : (∑ A ∈ Finset.range M, c A * residueSum q M d (A % q))
      = ∑ r ∈ Finset.range q, residueSum q M c r * residueSum q M d r := by
    rw [← Finset.sum_fiberwise_of_maps_to (t := Finset.range q) (g := fun A => A % q)
      (f := fun A => c A * residueSum q M d (A % q)) hmem]
    apply Finset.sum_congr rfl
    intro r _
    have hstep : (∑ A ∈ (Finset.range M).filter (fun A => A % q = r),
        c A * residueSum q M d (A % q))
        = ∑ A ∈ (Finset.range M).filter (fun A => A % q = r),
            c A * residueSum q M d r := by
      apply Finset.sum_congr rfl
      intro A hA
      rw [(Finset.mem_filter.mp hA).2]
    rw [hstep, ← Finset.sum_mul]
    rfl
  -- Step 3: assemble
  rw [Finset.sum_congr rfl hinner]
  simp only [mul_sub]
  rw [Finset.sum_sub_distrib, hreindex]

end Wrap

/-! ### 3. Bridge: residue form ↔ `kq`-difference form -/

/-- The residue form `A % q = B % q` is equivalent to the `kq`-difference form
`(q : ℤ) ∣ (A − B)` (i.e. `A − B = k q` for some integer `k`). -/
theorem nat_mod_eq_iff_dvd_sub {q : ℕ} (a b : ℕ) :
    a % q = b % q ↔ (q : ℤ) ∣ ((a : ℤ) - (b : ℤ)) := by
  rw [← Nat.modEq_iff_dvd]
  exact eq_comm

/-! ### Axiom audit -/

#check card_pairs_mod_eq
#check residueSum
#check wrap_identity
#check nat_mod_eq_iff_dvd_sub
#print axioms card_pairs_mod_eq
#print axioms wrap_identity
#print axioms nat_mod_eq_iff_dvd_sub

end Phase12
