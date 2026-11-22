import Mathlib
open Lean Meta Elab Command

def lagariasStmt : Prop := ∀ n : ℕ, 0 < n → ((ArithmeticFunction.sigma 1 n : ℕ) : ℝ) ≤ (harmonic n : ℝ) + Real.exp (harmonic n : ℝ) * Real.log (harmonic n : ℝ)
def robinStmt : Prop := ∀ n : ℕ, 5040 < n → ((ArithmeticFunction.sigma 1 n : ℕ) : ℝ) < Real.exp Real.eulerMascheroniConstant * (n : ℝ) * Real.log (Real.log (n : ℝ))

partial def defClosure (env : Environment) (start : Array Name) : NameSet := Id.run do
  let mut seen : NameSet := {}
  let mut todo := start
  while !todo.isEmpty do
    let n := todo.back!; todo := todo.pop
    if seen.contains n then continue
    seen := seen.insert n
    if let some ci := env.find? n then
      let mut es := #[ci.type]
      -- definitions contribute their bodies; theorems only their statements (proofs are irrelevant to meaning)
      match ci with
      | .defnInfo v => es := es.push v.value
      | .opaqueInfo v => es := es.push v.value
      | .inductInfo v => todo := todo ++ v.ctors.toArray
      | .ctorInfo v => todo := todo.push v.induct
      | .recInfo v => todo := todo ++ v.all.toArray
      | _ => pure ()
      for e in es do todo := todo ++ e.getUsedConstants
  return seen

run_cmd liftTermElabM do
  let env ← getEnv
  for nm in [``lagariasStmt, ``robinStmt] do
    let some (.defnInfo d) := env.find? nm | throwError "?"
    let direct := d.value.getUsedConstants
    let cl := defClosure env direct
    let kinds := cl.toList.foldl (init := (0,0,0,0)) fun (a,b,c,x) n => match env.find? n with
      | some (.defnInfo _) => (a+1,b,c,x) | some (.thmInfo _) => (a,b+1,c,x) | some (.inductInfo _) => (a,b,c+1,x) | _ => (a,b,c,x+1)
    IO.FS.writeFile s!"{nm}-deps.txt" (String.intercalate "\n" ((cl.toList.map toString).mergeSort (· ≤ ·)) ++ "\n")
    logInfo m!"{nm}: {direct.size} constants named directly; closure {cl.size} declarations (defs, theorems-as-statements, inductives, other) = {kinds}\ndirect: {direct.toList}"

set_option pp.explicit true in
set_option pp.coercions false in
set_option pp.numericTypes true in
set_option format.width 110 in
#print lagariasStmt

set_option pp.explicit true in
set_option pp.coercions false in
set_option pp.numericTypes true in
set_option format.width 110 in
#print robinStmt
