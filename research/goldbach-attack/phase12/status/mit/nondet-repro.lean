def F (m : Nat → Option Nat) (w : Nat) (c : Option Nat) : Nat :=
  match m w, c with
  | some a, some c => a * c
  | _, _ => 0
theorem t1 (m : Nat → Option Nat) (w : Nat) (h : m w = none) (c : Option Nat) : F m w c = 0 := by
  simp [F, h]
theorem t2 (m : Nat → Option Nat) (w : Nat) (h : m w = none) (c : Option Nat) : F m w c = 0 := by
  cases c with
  | none => simp [F, h]
  | some c => simp [F, h]
