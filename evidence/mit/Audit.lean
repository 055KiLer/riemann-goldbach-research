import Main
open Lean Elab Command

-- Where do the constants appearing in the headline statements come from?
run_cmd do
  let env ← getEnv
  for n in [`RiemannHypothesis, `riemannZeta, `DirichletCharacter, `DirichletCharacter.LFunction,
            `DirichletCharacter.IsPrimitive, `RiemannZetaZerosOnLine, `DirichletLNonvanishingRightOfHalf,
            `DirichletLZerosOnLine, `PrimitiveDirichletLZerosOnLine,
            `riemannHypothesis, `riemannZeta_eq_zero_re, `LFunction_ne_zero_of_half_lt_re,
            `LFunction_eq_zero_re, `LFunction_eq_zero_re_of_isPrimitive] do
    match env.getModuleIdxFor? n with
    | some idx => logInfo m!"{n} : declared in module {env.header.moduleNames[idx.toNat]!}"
    | none => logInfo m!"{n} : NOT FOUND or declared in current file"

-- Census of every axiom in the whole environment, by declaring module.
run_cmd do
  let env ← getEnv
  let mut ax : Array (Name × Name) := #[]
  let mut nconst := 0
  let mut nthm := 0
  for (n, ci) in env.constants.toList do
    nconst := nconst + 1
    if ci matches .thmInfo _ then nthm := nthm + 1
    if ci matches .axiomInfo _ then
      let m := match env.getModuleIdxFor? n with
        | some idx => env.header.moduleNames[idx.toNat]!
        | none => `«current»
      ax := ax.push (n, m)
  logInfo m!"modules imported: {env.header.moduleNames.size}; constants: {nconst}; theorems: {nthm}"
  logInfo m!"ALL AXIOMS IN ENVIRONMENT ({ax.size}): {ax.qsort (fun a b => a.1.toString < b.1.toString)}"

#print RiemannHypothesis
#check (riemannHypothesis : RiemannHypothesis)
example : RiemannZetaZerosOnLine = RiemannHypothesis := rfl
#print axioms riemannHypothesis
#print axioms riemannZeta_eq_zero_re
#print axioms LFunction_ne_zero_of_half_lt_re
#print axioms LFunction_eq_zero_re
#print axioms LFunction_eq_zero_re_of_isPrimitive
