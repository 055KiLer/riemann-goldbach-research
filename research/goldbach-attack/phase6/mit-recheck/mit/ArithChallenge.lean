import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.NumberTheory.ArithmeticFunction.Misc
import Mathlib.NumberTheory.Harmonic.EulerMascheroni

/-!
Elementary arithmetic consequences of the Riemann Hypothesis, stated with no reference to the
zeta function. This file imports only Mathlib; the proofs are `sorry` here and are supplied in
`ArithSolution.lean` by combining the submitted proof of `RiemannHypothesis` with the
Robin1984 formalization of Robin's and Lagarias's criteria.
-/

/-- Robin's inequality: `σ(n) < e^γ · n · log log n` for every `n > 5040`. -/
theorem robin_inequality :
    ∀ n : ℕ, 5040 < n →
      ((ArithmeticFunction.sigma 1 n : ℕ) : ℝ) <
        Real.exp Real.eulerMascheroniConstant * (n : ℝ) * Real.log (Real.log (n : ℝ)) := by
  sorry

/-- Lagarias's inequality: `σ(n) ≤ H_n + exp(H_n) · log(H_n)` for every `n ≥ 1`. -/
theorem lagarias_inequality :
    ∀ n : ℕ, 0 < n →
      ((ArithmeticFunction.sigma 1 n : ℕ) : ℝ) ≤
        (harmonic n : ℝ) + Real.exp (harmonic n : ℝ) * Real.log (harmonic n : ℝ) := by
  sorry
