# Proof digest — the claimed Alpöge/Claude Riemann Hypothesis proof: what is verified, what is claimed, what is understood

**Prepared by:** proof-digest (team teammate)
**Date:** 2026-11-21 (Asia/Shanghai) · **Access date for all URLs below: 2026-11-21**
**Primary artifacts:** [alpo.ge/remark.pdf](https://alpo.ge/remark.pdf) (author's 4-page note, local extract `/home/kiler/rh-work/remark.txt`); MIT verification page [math.mit.edu/~drew/grh/](https://math.mit.edu/~drew/grh/) (Andrew Sutherland, "checks run with Claude Code", page last updated 2026-11-20 22:05 UTC); local mirror `/home/kiler/rh-full` (git `7cbf7a0c3`, 175,187 `.lean` files, 17,374,215 lines, verified).
**Scope discipline:** claims below are labelled **[verified artifact]**, **[primary claim by author]**, **[secondary press report]**, or **[my inference]**. Nothing is fabricated; where a source could not be retrieved this is stated.

---

## TL;DR (10 points)

1. **The headline formal claim is true as a Lean theorem to the extent that independent kernel checks are trustworthy.** On 2026-11-20, Levent Alpöge announced that he and Claude proved RH and GRH (for Dirichlet L-functions) and formalized the argument in Lean without assumptions. Andrew Sutherland (MIT) compiled the archive and ran independent checks; as of his page's 22:05 UTC snapshot, all 175,187 modules compile, the five headline theorems use only `propext`, `Classical.choice`, `Quot.sound`, and the full proof export is accepted by two independently written kernels (**nanoda**, **con-leche**) and by **lean4lean**. **[verified artifact]**
2. **`RiemannHypothesis` in the code is Mathlib's own definition**, not a bespoke predicate: `∀ s, riemannZeta s = 0 → (¬∃ n, s = -2*(n+1)) → s ≠ 1 → s.re = 1/2`. GRH here means **Dirichlet L-functions only** (not automorphic/GL(n) GRH, not ERH). **[verified artifact]**
3. **The export is hash-pinned and matches a third party's CI**: challenge export sha256 `bd484ac9886a96f26b1d9a7a59ebd45b7a70d102c015d4f31f9302bbdd6ab2b9` (also published by Deicyde/riemann-hypothesis CI); solution export unpacks to 61,570,595,788 bytes, sha256 `5ea74b9121…be244e`. **[verified artifact]**
4. **The official end-to-end `lake comparator` run and the Lean paranoid-kernel replay of the export were still "running"** in that 22:05 UTC snapshot. con-leche's `--compare` mode (an independent implementation of Comparator's statement matching) had already confirmed all five theorems against the challenge. I could not observe a newer snapshot: the page fetched at ≈02:15 UTC 2026-11-21 was unchanged. **[verified artifact + my observation]**
5. **What has *not* been verified: a human-readable proof.** The author did not publish a proof text; he says the generated write-up is 250,000+ pages and "obviously inappropriate to … post some massive unreadable travesty of 'slop'", so he published **only Lean**. The 4-page remark.pdf is an outline, not a proof. **[author's own words]**
6. **The author himself states he has not mastered the mathematics of his own argument**: "I am presenting the world with a complete argument before having mastered a massive neighbourhood around its mathematics"; "I personally have little mastery of automorphic forms on higher rank groups"; he expects (and invites) massive simplification. **[author's own words]**
7. **The claimed idea, in the author's compressed language:** a descendant of **Stepanov's determinant method**, which proves RH over function fields using a divisor with **multiplicity**; over ℤ "multiplicity is hard to find … corresponding to something like differentiating whole numbers", so the argument simulates multiplicity by **chaining theta lifts**, and for the von Mangoldt sum of length X the chain length is **√X**. "An astounding amount of mathematics is present." **[author's claim]**
8. **Expert secondhand description** (Chris Birkbeck, UEA, in the Lean Zulip, quoted by TechCrunch): "The cohomology bound is proved by what looks like an automorphy-lifting argument. It genuinely uses the existence of Galois representations attached to regular algebraic, polarized cuspidal automorphic representations of GL_n over CM fields, along with base change, Jacquet–Shalika, Clozel's purity, Bernstein–Zelevinsky, the main theorem of CM, Deligne–Ribet and more." **[secondary press quoting primary chat]**
9. **"A human did, too"** (TechCrunch headline) refers to a **separate, independent, all-human claim of GRH** by Stanford postdoc **Alessandro Masullo**, posted 2026-11-20 by Ravi Vakil, "12 years of work", draft form, not Lean, not yet checked. It is *not* a human-readable version of Alpöge's proof. **[secondary press; Vakil quote via simonwillison.net]**
10. **Clay Prize rules are not satisfied** (needs formal publication, ~2 years of verification, broad community acceptance — 36kr's rendering); and expert reception is split between "almost certainly true" (Sutherland), "historic if it checks out" (Maynard) and "garbled" (Granville). **[secondary press]**

---

## A. Verification status — the formal layer

### A.1 Timeline (UTC, 2026-11-20 unless marked)

| Time | Event |
|---|---|
| late Sunday 15/16 Nov | Author says the key work was completed; contacts Anthropic CEO about announcing. The "timeline Claude provided" in remark.pdf runs 10/6/26 – 11/16/26. |
| 2026-11-20 | remark.pdf + 14-part `lean.tar.gz` published at alpo.ge; TechCrunch/Nature/SciAm etc. publish stories. |
| 16:43:21 | **All 175,187 modules compile** (Lean v4.33.1, Mathlib v4.33.1), zero errors. |
| ~18:17 | **leanchecker** kernel replay of every module: 175,187/175,187, zero rejections. |
| 19:05:45 | **nanoda** (independent Rust kernel) accepts full export, exit 0; 27 m 42 s on 80 threads. |
| 21:19:04 | **con-leche master** (`cd2eceab`) accepts: 1,468,418 declarations in `--verified` mode. |
| 21:19:12 | **con-leche `--compare`** (`5dc36dc1`): all five theorems "justified by the solution"; 51,692 challenge declarations accepted. |
| ~21:55 | **lean4lean** (`67f63b0c`) passes 175,187/175,187 modules (175,182 default; 5 rerun with raised fuel — see caveats). |
| 22:05 | MIT page last updated. `lake comparator` end-to-end and Lean default+paranoid kernel replay of export **still running**. |

**[verified artifact]** — all rows from the MIT page and its linked logs; audit.log, comparator.json, SHA256SUMS, nanoda.log, con-leche logs downloaded and read by me.

### A.2 What has been independently verified (as of the MIT snapshot)

| Check | Result | Detail / artifact |
|---|---|---|
| 175,187 modules compile | pass | zero errors, 16:43:21 UTC |
| Axioms of the five `Main.lean` theorems | pass | exactly `propext`, `Classical.choice`, `Quot.sound` — see `audit.log` |
| No axioms outside Lean core | pass | 15 axioms in environment, all in `Init` (includes `sorryAx`, `Lean.ofReduceBool`, `Lean.trustCompiler`, etc., *not* used by the five theorems) |
| Mathlib/deps `.olean` integrity | pass | 8,322 Mathlib + 378 dependency files byte-identical to official cache |
| `leanchecker` replay of every module | pass | 175,187/175,187 |
| Challenge export hash | match | `bd484ac9…b2b9`, equals Deicyde mirror CI's challenge export; `challenge.ndjson` unpacked 350,862,970 bytes |
| nanoda (3rd-party kernel) | accepts | exit 0, 27:42, 80 threads, peak RSS ≈ 84.8 GiB |
| lean4lean (3rd-party kernel/checker) | pass module-by-module | 175,187/175,187; 5 files hit lean4lean's default *step limit* ("deterministic timeout") on `decide +kernel` computations and pass with raised limit |
| con-leche (3rd-party kernel) | accepts | 1,468,418 declarations, 3 m 15 s, 64 threads |
| con-leche `--compare` | accepts | all five theorems justified by solution; independent re-implementation of Comparator statement matching |
| Lean default + paranoid kernel on export | **running** at 22:05 | single-threaded, no verdict then |
| `lake comparator` end-to-end | **running** at 22:05 | statement comparison + axiom check had already passed in one run; kernels in progress |
| con-leche/con-ron bundled with Lean v4.36.0 | declined (exit 2) | **not a rejection**: those binaries predate a reflexive inductive used by the proof; con-leche master does support it |
| lean4lean bundled with Lean v4.36.0 | N/A | cannot read a v4.33 core library (`unknown constant 'Decidable.intro'`) |

Additional artifact facts: `audit.log` says **186,200 modules imported; 2,701,132 constants; 2,084,256 theorems**. `comparator.json` declares permitted axioms `propext`, `Quot.sound`, `Classical.choice` and external kernels `leanchecker-paranoid` and `nanoda_bin`.

### A.3 The trust boundary (what a passing formal check does and does not mean)

Sutherland's own "Caveats" section, verbatim points summarized:
- The build ran **on cloud machines without a sandbox**, compiling each file by calling `lean` directly with `lake`'s inputs rather than through `lake build`; a **77-module sample** is byte-identical to a real `lake build`, but the **full set has not been compared** to one.
- The export has the same unsandboxed provenance; a comparison against a sandboxed rebuild (the "Deicyde protocol") has **not been made yet**.
- "A passing check shows that the formal statements, as written in Lean against Mathlib's definitions, follow from the three standard axioms according to the kernels used. It relies on those kernels and on Mathlib's definitions being what they are intended to be."
- A first build attempt used a wrong module root and was discarded in full.

**[my inference]** Therefore the residual trust assumptions are: (i) Lean's kernel + nanoda + con-leche + lean4lean are all correct (multiple independent implementations agreeing makes kernel-bug exploitation extremely unlikely, but they still share Lean's *logic*); (ii) Mathlib's `riemannZeta` and `RiemannHypothesis` definitions mean what mathematicians intend (they are Mathlib-maintained and widely used); (iii) the compilation/export pipeline was not tampered with (unsandboxed provenance is the weakest link, though the export hash matches an independent third party's CI export of the same source archive); (iv) the formal statement that was verified is exactly the intended one (comparator/con-leche `--compare` is designed to catch "redefine a symbol" attacks; it passed).

**Crucel conceptual point:** if the checks hold, then RH *is* a theorem of Lean's foundation + Mathlib definitions. The unresolved issue is not logical correctness but **human understanding, provenance confidence, and community acceptance**. The author himself frames it this way.

### A.4 What is NOT verified / what remains

- **No human-readable proof exists in public.** Only the 4-page remark and 17.4M lines of Lean. Peer review of the mathematical *argument* has not happened.
- **The "250,000+ pages" text proof is not released** (author's footnote: "I of course amused myself, and hit 250,000+ pages. Claude cutely called it the GRH … 'book'").
- **Official end-to-end `lake comparator` was still running** at the last MIT snapshot (the statement-matching part has independent confirmation via con-leche `--compare`).
- **Lean paranoid-kernel replay of the export** was still running.
- **Clay Mathematics Institute rules** (per 36kr/智东西): a Millennium solution must be formally published, survive at least two years of verification, and be broadly accepted. None of that has happened. **[secondary press]**
- **A competing human claim exists** (Masullo, see A.5) — itself unverified; it does not validate Alpöge's argument, it is an independent parallel claim.
- **Statement-level audit of the 17.4M lines by humans is infeasible**; the archive contains enormous formalizations of "published theorems" (Kawamata–Viehweg, Fargues, Deligne–Ribet, Clozel purity, …). These are *proved*, not assumed, so they do not create logical gaps in the final theorem; but whether each formal statement faithfully matches the literature statement has not been human-audited. This matters for scientific credit/understanding, not for the kernel-checked truth of `RiemannHypothesis`.

### A.5 The "human did, too" story (TechCrunch headline)

- **Alessandro Masullo** (Stanford postdoc) has a **proposed proof of GRH**, **all human, no AI**, 12 years of work, announced in a draft on 2026-11-20 by **Ravi Vakil** ("Hurried Announcement: Alessandro Masullo GRH", math216.wordpress.com, 2026-11-20; quote preserved at [simonwillison.net/2026/Nov/20/ravi-vakil](https://simonwillison.net/2026/Nov/20/ravi-vakil/)): "Brian Conrad has been looking closely at it for months and gave extensive feedback which is being incorporated, and it is so far looking good. It is all human, with no AI. … Now it seems best to put out the current draft."
- TechCrunch: "Without being expressed in Lean, it is too early to say whether the proof checks out, much less if anyone understands it."
- It is **not** a human translation of Alpöge's proof; it is a **separate competing claim**. **[secondary press + quoted primary]**

### A.6 Expert/mathematical reception (labelled)

- **Andrew Sutherland (MIT)** (SciAm): "The Lean proof has been compiled and independently rechecked by the Lean kernel with only the three standard axioms… Honestly the chance that anything is fishy here is approximately zero." **[secondary quoting primary]**
- **Kevin Buzzard (Imperial)** (SciAm, quoting his blog): the first question is "what is the statement of the theorem in the Lean code, and does this correspond to the actual theorem statement"; still awaits a full comparator/paranoid-kernel run. **[secondary quoting primary]** *(His blog post at xenaproject.wordpress.com could not be fetched from this environment — WordPress unreachable; relied on SciAm's quotation.)*
- **Terence Tao** (per 36kr/智东西, screenshot of a blog post): the proof appears to comprehensively use modern Langlands-program and arithmetic-geometry results; the community is verifying; this will take time. **I could not locate the blog URL** (WordPress unreachable from this environment); treat as secondary.
- **Alex Kontorovich** (per 36kr): "I am actually more confident that the proof will succeed. The Riemann Hypothesis was proven by using 'all' the proofs!" **[secondary]**
- **James Maynard** (Nature): "If this fully checks out, it is clearly a historic milestone in mathematics." **Andrew Granville** (Nature): "What he released is garbled"; he cites the Anthropic IPO timing as the reason for release. **[secondary press]**
- **Deng Yu** (2026 Fields Medalist), viral screenshot quoted by 36kr: "I will not even glance at it before I reach 500 pages." **[secondary; 36kr itself says the screenshot is of uncertain provenance — labelled unverified]**
- **Elliot Glazer** (per 36kr): preliminary inspection found the formal statement is indeed GRH; estimates chance of a Lean loophole < 1%. **[secondary]**

---

## B. Technical skeleton — reconstructing the claimed proof architecture from the local archive

### B.1 The whole final chain is short; the mass is underneath

The *kernel* of the submission is tiny and readable:

`src/Main.lean` (12 lines) **[verified file]**
- `riemannHypothesis : RiemannHypothesis := rhOfAll` (line 5)
- `riemannZeta_eq_zero_re : RiemannZetaZerosOnLine := rhOfAll`
- `LFunction_ne_zero_of_half_lt_re : DirichletLNonvanishingRightOfHalf := allChi`
- `LFunction_eq_zero_re : DirichletLZerosOnLine := claimAll.2.1`
- `LFunction_eq_zero_re_of_isPrimitive : PrimitiveDirichletLZerosOnLine := critAll` (line 9)

`src/Supplements/Kernels/MainTheorems.lean` (16 lines) builds the five proof terms:
- `allChi : UpperTheory.EveryCharacter := UpperTheory.FinalTheorems.everyCharacter` (line 7)
- `rhOfAll : RiemannHypothesis := Formalism.VW.rh_of_every allChi` (line 9)
- `critAll …` uses `Formalism.VW.critLine allChi` (lines 11–13)
- `claimAll : Claim.HalfPlane ∧ Claim.Strip ∧ Claim.Zeta := ⟨allChi, Claim.strip allChi, Claim.zeta allChi⟩` (line 15)

So the logical dependency graph is:

```
Main.riemannHypothesis
 └─ Formalism.VW.rh_of_every : UpperTheory.EveryCharacter → RiemannHypothesis        [Formalism/GammaFactorNonvanishing/CritLine.lean:29]
     (helper: Formalism.VW.rh_of_right, RhOfRight.lean:5 — functional equation + Γ/cos factors)
 └─ Main.allChi := UpperTheory.FinalTheorems.everyCharacter
     └─ everyCharacter_of_row (h : UpperTheory.GalStar.Row0b …)                          [CharacterBoxes/MainConclusion.lean:7]
         := LiteratureTheorems.every_character_of_literature_of_vWin
              ⟨h, recTExists, h⟩                       -- OpenLiteratureStatements, 3 fields
              (UpperTheory.One.vwin_of_row h)          -- VWin, from the same row hypothesis
         └─ everyCharacter := everyCharacter_of_row galoisLocalGlobalStrong_recParameter    [MainConclusion.lean:10]
             └─ galoisLocalGlobalStrong_recParameter : UpperTheory.GalStar.Row0b recT
                 := galoisRepresentations_of_thetaLift UpperTheory.TP.K.tLiftK             [Foundations/GaloisRepresentations/IntegralStructures/RowSrc.lean:6]
                 └─ tLiftK : UpperTheory.TP.TLiftK := tLift_holds_k                       [ThetaParseval/ThetaKernels/TLiftK.lean:4]
                     └─ tLift_holds_k := tLift_of_tools_k tools_holds_k (hgtEx_of_k stab2Cpt_k)  [TPGHolds.lean:58]
                         └─ TLiftK : Prop — the theta-lift existence statement             [HalfIndexLattices/TLiftK.lean:12]
```

### B.2 `UpperTheory.EveryCharacter` — what it actually says

`src/Development/AutomorphicArithmetic/CharacterBoxes/EveryCharacter.lean:13`:

```lean
def UpperTheory.EveryCharacter : Prop :=
  ∀ (N : ℕ) [NeZero N] (χ : DirichletCharacter ℂ N) (s : ℂ),
    1 / 2 < s.re → (χ ≠ 1 ∨ s ≠ 1) → DirichletCharacter.LFunction χ s ≠ 0
```

This is **literally the GRH-for-Dirichlet-L statement** (compare `Claim.HalfPlane` in `CharacterBoxes/HalfPlane.lean` and `DirichletLNonvanishingRightOfHalf` in `Statements.lean`). It is the *hard theorem* the whole archive exists to prove. It is proved by `plugAll`/`plugWin`:

`CharacterBoxes/EveryCharacter.lean:8–18`:
- `plugWin (hG : GlobalTheory.GLq.Green) (hV : UpperTheory.Top.VWin) (h : Nonempty (Hyps (fun 𝒞 => Closed 𝒞 fun Fm _ => LinkN Fm) DRS)) : Formalism.HC.ZeroFreeAll`
- `plugAll … := UpperTheory.Top.imprimitive (plugWin …)` → `UpperTheory.EveryCharacter`.

The three inputs:
1. **`GlobalTheory.GLq.Green`** — a purely combinatorial/repr-theoretic statement about characters of `GL_d(ℤ/g)` labelled by prime polynomials over `ℤ/g` (`Development/AbelianVarietyTheory/Definitions/NonGaloisDescent/LabelDatum.lean:108`). Structurally this is the **function-field/Stepanov toy model** part: existence of a canonical labelling τ of prime-polynomial labels by cuspidal characters, with the right Gauss-sum normalisation (`τ P 1 = ∏ (g^i - 1)`) and injectivity/surjectivity. *(my inference from the definition; the Lean code does not name it "Stepanov")*
2. **`UpperTheory.Top.VWin`** — `∀ ψ : PChar, VWinAt ψ 401` (`CharacterBoxes/ExistsPageN.lean:44–49`), a "page/window" existence statement with constant 401.
3. **`Nonempty (Hyps (fun 𝒞 => Closed 𝒞 fun Fm _ => LinkN Fm) DRS)`** — the family/box hypotheses of the "upper theory".

`Green` and `VWin` are themselves proved from the single row hypothesis `Row0b`:
- `UpperTheory.One.vwin_of_row : UpperTheory.GalStar.Row0b (fun h rc => IsRecT h rc) → UpperTheory.Top.VWin` (`AutomorphicVarieties/ModularityArgument/ThresholdArguments/DenseThresholdCases/VwinOfRow.lean:4`).
- Green is derived inside `UpperTheory.Lit.every_character_of_theta_integrals_local_matching` via `GlobalTheory.GreenBridge.green_of_regular P.greenRegularCharacters` (`ThetaCorrespondence/…/ThirdPlaceSeries/SiegelEisensteinSecondTermHypotheses.lean:69`).

### B.3 The analytic/zero-free core (`ZeroFreeAll`)

`src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/ExplicitFormulaErrorOfHostConditions.lean`:
- `PChar.ZeroFreeAbove ψ θ := ∀ s, θ < s.re → LFunction ψ.χ s ≠ 0` (line 10)
- `ZeroFreeOn Q := ∀ ψ, Q ψ → ψ.ZeroFreeAbove (1/2)` (line 14)
- `ZeroFreeAll := ZeroFreeOn fun _ => True` (line 18) — **this is exactly "GRH is true"**, expressed for primitive characters
- `structure Level extends KSet where o : ℕ` with `KEPT : Finset PChar`, weights `wt ψ = (if psK = some ψ then 1 else (3*(o:ℝ)+1)⁻¹)`, and
  `Gm y := Formalism.Gz y + ∑_{ψ ∈ Nt} wt ψ * (An.gChi ψ.χ y).re` (lines 28–39)
- **`ChebyshevGrowthImpliesZeroFree : ∀ θ, 0<θ<1 → ∀ y0, (∀ y≥y0, Λ.Gm y ≤ y^θ) → Λ.ZeroFreeAbove θ`** (line 40)
- `zeroFreeOn_of_levels` (line 45): if every character is kept in some level Λ with `Λ.ZeroFreeLevel`, then `ZeroFreeOn Q`.

**Interpretation [my inference, supported by names]:** this is the explicit-formula/Chebyshev-machinery layer: control of a smoothed von-Mangoldt/Chebyshev-type sum `Gm y` by powers `y^θ` yields a zero-free half-plane `Re s > θ`; the `Level`/`KEPT`/weights structure is the **averaging over characters in a "tower" of levels** (the "glue together an integral structure across Hecke characters for a 'gcd', i.e. extra averaging" of remark.pdf item 15; the `1/(3o+1)` weights are a dyadic-style weighting). Calling `Level` an "Iwasawa tower" is *my reading* of remark.pdf item 11, not a name used in the code.

The upper-theory glue is in `CharacterBoxes/ZeroFreeAllOfTopG.lean`:
- `TopG : Prop := ∀ la G, 1<la → HostExW la G.req → (∀ Fm, G.cls la Fm → HypV Fm) → FamilyClassConnected (G.cls la)` (line 12)
- `zeroFreeAll_of_topG (hla) (h:TopG) (hS) : ZeroFreeAll` (line 26), via `zeroFreeOn_of_tiedWin_cyc` + `UpperTheory.Comparison₂.level_gm_le_on_family_scales` + `formB`.
- `FamilyClassConnected ℰ := ∃ eD eL ε₁>0, ∀ eps, ∃ Fm : FamP eps, ℰ Fm ∧ ∃ K cHH eK CL x0, ∀ x≥x0, x∈Fm.Win → ChainTied Fm eD eL K cHH eK CL x` (line ~10) — a **chain-tying/pigeonhole statement over "families of windows" indexed by a real scale x**. This is the formal incarnation of "chaining theta lifts of length √X" / "Iwasawa tower via pigeonhole" (remark.pdf items 8, 11, 19). The chain length itself is not literally named √X in the code I inspected; the constant 3 is used (`Tied` chain of length 3 = "3 = 3·1"? see `Tied` = 3*Fm.x1?) — **mark uncertain**.

### B.4 The "literature" layer and the real mathematical input

`ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/EveryCharacterOfLiteratureOfVWin.lean` (814 lines):
- line 215: `structure UpperTheory.LiteratureTheorems.OpenLiteratureStatements : Prop where`
  - `caraianiLocalGlobalDual : UpperTheory.One.M.Row`
  - `localLanglandsExists : UpperTheory.Zero.LLC.RecTExists`
  - `galoisRepOfPolarizedPairLit : UpperTheory.One.M.Row`
- lines 219–604: ~150 named "published theorem" wrappers `X_of_literature (O) : GlobalTheory.Published.X` — most of them **ignore O** and call directly proved archive theorems (e.g. `deligne_ribet_of_literature := PositivityTheory.PfDR.deligneRibet_holds`), showing the "literature" is *derived*, not assumed.
- line 810: `every_character_of_literature_of_vWin (O) (hV : UpperTheory.Top.VWin) : UpperTheory.EveryCharacter`, which calls the real core:
  `UpperTheory.Lit.every_character_of_theta_integrals_local_matching`
  `(published_results_eigen O) (published_results_first O) (ThetaIntegralsAgree) (LocalMatching) (hX := SelfIntersectionVolumeEstimates.topCovolSlim2…) (RecTExists) hV`
  and inside that theorem (`SiegelEisensteinSecondTermHypotheses.lean:69`) does
  `UpperTheory.Top.every_character_of_green_v_win (GlobalTheory.GreenBridge.green_of_regular P.greenRegularCharacters) hV (Nonempty Hyps …)`.

So the **actual mathematical load-bearing inputs** are:
1. **`UpperTheory.GalStar.Row0b`** (def `Foundations/GaloisRepresentations/TypeConditions/WeightsConjBis.lean:69`): for every CM field E, prime l, regular algebraic polarized cuspidal automorphic representation π of `GL_a` over E (with Hecke character), there is an l-adic Galois representation r with the expected properties (`PropsB`: continuity, semisimplicity, local restrictions, Hodge–Tate weights, weight-conjugation symmetry). This is a **strong automorphy-lifting/Galois-representation statement** — exactly the kind of thing Birkbeck described.
2. **`TLiftK`** (`Foundations/GaloisRepresentations/ThetaParseval/HalfIndexLattices/TLiftK.lean:12`): for all CM data E/B, all n≥1, all Hermitian spaces X with J=1, **there is d₀ such that for all d ≥ d₀** and all skew W at level d, all Hecke characters χX, χW with the right exponents, any automorphic representation U on U(E^n) of weight λ satisfying `(d + mW) ≤ 2λ` is **lifted** (`IsLift B χX χW mX mW lam U U'`) to an automorphic representation U′ on U(E^d). This is the **iterated theta-lift chain statement** (arbitrary depth d, weight/multiplicity bookkeeping via mW and λ). Proved via `tLift_of_tools_k tools_holds_k (hgtEx_of_k stab2Cpt_k)` (`TPGHolds.lean:58`).
3. **`RecTExists`** (local Langlands / reciprocity).
4. **`caraianiLocalGlobalDual` / `galoisRepOfPolarizedPairLit`** (the two `UpperTheory.One.M.Row` fields).
5. **`VWin`** — the combinatorial page/window existence (constant 401).
6. **`Green`** — the `GL_d(ℤ/g)` labelling statement.
7. The analytic explicit-formula/zero-free machinery (B.3).

### B.5 Reduction of GRH/EveryCharacter to RH (the elementary part — fully human-readable)

- `Formalism/GammaFactorNonvanishing/CritLine.lean:11` `critLine`: if `EveryCharacter` (nonvanishing right of ½ for all χ) and χ primitive has a zero s with `0<Re s<1`, then by the completed-L functional equation (`completedLFunction_one_sub`) either `Re s=½` or `1-s` is a zero of `χ⁻¹` to the **right** of ½ — contradiction (needs `gammaFactor_ne_zero` at line 6).
- `Formalism/GammaFactorNonvanishing/RhOfRight.lean:5` `rh_of_right`: if ζ has no zeros for `Re>½` (excluding s=1) then RH, using the functional equation `riemannZeta_one_sub`, `Gammaℝ`, and `cos` nonvanishing.
- `CharacterBoxes/ClaimStrip.lean`: `strip (h : HalfPlane) : Strip` (complex conjugation & primitive-character reduction), `zeta (h) : Zeta` (using `LFunction_modOne_eq`, trivial zeros and functional equation); `zeta_iff : Claim.Zeta ↔ RiemannHypothesis`.
- `CharacterBoxes/Imprimitive.lean:5`: `ZeroFreeAll → UpperTheory.EveryCharacter` (removes the primitive hypothesis via `LFunction_changeLevel`; the Euler factor `1-χ(p)p^{-s}` is nonzero for Re>0).
- `CharacterBoxes/RiemannHypothesisOfEveryCharacter.lean`: two separate direct routes `zeta_ne_zero_of_everyCharacter` and `riemannHypothesis_of_everyCharacter` (via χ=1 and completed ζ). The `Main.lean` route uses `Formalism.VW.rh_of_every`; the other files are essentially alternative/belt-and-braces versions (the archive contains many `_alt` duplicates).

**Net:** the final implication GRH⇒RH is textbook-level, fully readable, and does not depend on the deep machinery; the deep machinery is entirely in proving `EveryCharacter` (zero-free region right of ½).

### B.6 remark.pdf timeline → repository mapping (confidence-labelled)

Narrative terms were searched in the **entire** source tree. Interesting negative result: **"Stepanov", "Guinand", "Vandiver", "sixfold" appear in 0 files**, "Bost" in 7 (as a substring, not the slope inequality), "GGP" in 244, "Rallis" in 232, "Behrend" in 17 (`Formalism/BehrendSets/`), "Chowla" in 79 (mostly `MeanLogPeriodConjugatesEqChowlaSelberg`), "Bessel" in 3009, "Iwasawa" in 14,585 (!), "theta lift"/`ThetaLift` in 1321 filenames, "multiplicity" in 2796 files, "GL5" in 176 (`Formalism/LocalToGlobal/GlobalTheory/GL5/`). The formal archive is *deliberately opaque* (machine-generated names, no narrative docstrings); the author's 4-page outline is a separate poetic narrative, not a map of module names.

| remark.pdf item (date) | Likely repo area | Confidence |
|---|---|---|
| 1 (10/6/26) Stepanov determinant | No literal "Stepanov"; closest `Development/WeilBound` (7050 files) + function-field/toy model `GlobalTheory.GLq` (LabelDatum/Green) | **low** |
| 2 (10/9/26) Dp≡0 on CM curve, divergence/Ω divisibility | `Development/…/FoundationProofs/MeanLogPeriodConjugatesEqChowlaSelberg*`, `CMCurveGoodOutsidePrime*` | medium-low |
| 3 (10/19+) qN=Mk+R, GL5 sixfold cover, theta period integrals | `Formalism/LocalToGlobal/GlobalTheory/GL5/` (176 files), `ThetaCorrespondence/…`, `WeilTensorModels` | medium (GL5 dir) / low (sixfold) |
| 4 (10/6+) W≥0 determinant / Stepanov multiplicity one | `CharacterBoxes/{ShapeWin,WinPairs,RealSplit,…}`, `Formalism/HermitianCurvature` | low |
| 5 (10/20) von Mangoldt sum Λ, Guinand–Weil sign, test function, Parseval k times | `Formalism/HC` (explicit formula: `formB`, `gChi`, `ExplicitFormulaError*`), `Formalism/HermitianCurvature` | medium (explicit formula machinery exists) |
| 6 (10/8) W(1(0,1]+X^η·1(0,1/X]) ≥ 0 | `CharacterBoxes/ShapeWin`, `BoundedTw`, `Supply` | low |
| 7 (10/14) determinants for W containing GGP periods, interlacing weights | `Formalism/PeriodIntegrals` (4350 files), "GGP" 244 files | medium |
| 8 (11/15) iterated theta lifts U(X0)→…→U(Xm), π↦π⊞μj[t], multiplicity m, m ~ √X | `Development/…/ThetaLifts` (788 files), `TLiftK` (`IsLift`), `ThetaCorrespondence` | **high** for theta-lift existence; "√X" not literally encoded |
| 9–10 (11/15) norms of lifts, Chowla–Selberg/Weyl/Siegel mass, divisibility lower bound | `Chowla` 79, `SiegelWeil` dirs, `CompanionTheory/SiegelUnitTheory/ClassNumberMass` | medium-low |
| 11 (10/6) Iwasawa tower / pigeonhole on F_{q^n}/F_q | "Iwasawa" 14,585 files (!), `Formalism/LocalToGlobal/IndefiniteReal`, IwasawaDecomposition dirs; `Level` structure (tower of kept characters) | medium (machinery) / low (narrative link) |
| 12 (11/15) Rallis seesaw → Bessel period independent of Hecke characters | `UpperTheory.Lit.Rallis` namespace, `RallisInnerProduct/`, Bessel 3009 files | **high** |
| 13 (10/6) Bost slope inequality | 7 incidental hits only; not identifiable | low |
| 14 (11/15) cost of each lift, stop at 2/3, transfer constant | `CharacterBoxes/{DesWin,DesignS,DivinNOfHypV}`, `Formalism/…/ThinScalesIffHostBound` (`HostExW`) | low-medium |
| 15 (11/15) glue integral structure across Hecke characters ("gcd"/extra averaging) | `Level`/`KEPT`/`wt` in `ExplicitFormulaErrorOfHostConditions.lean`; `CharacterBoxes/Imports` | medium |
| 16 (10/14) relative trace formula, sixfold GL5 automorphy, Poincaré series, Cauchy–Schwarz | `ReciprocityTheory` (3845 files), `Formalism/SharpRestriction` (3093), `TwistedTraceFormula` dirs | medium |
| 17 (11/15) significant weakening of Vandiver, H¹(o_E[1/ℓ], Q_ℓ/Z_ℓ(−e)), K-groups | No "Vandiver"/"Lichtenbaum" strings; possibly encoded in `ReciprocityTheory/Gal` (Greenberg–Wiles etc.) | **low** |
| 18 (11/15) covolumes, theta series index, congruences between lifts and forms | `WeilTensorModels`, `SiegelWeil*`, `SelfIntersectionVolumeEstimates` | medium |
| 19 (10/19) precise Iwasawa tower choice using Behrend | `Formalism/BehrendSets` (17 files) | medium |
| 20 (11/16) GRH | final chain B.1 | **high** |

### B.7 Formal-verification methodology of the archive (important for reading it)

- The 17.4M lines are organised into: `Development/` (141,928 files, 12.2M lines — mostly `AbelianVarietyTheory/Proofs` 95,418 files, `AutomorphicArithmetic` 18,431, `AutomorphicSpectrum` 15,129, `WeilBound` 7,050); `Formalism/` (18,254 files, 3.2M lines: `LocalToGlobal` 5,501, `PeriodIntegrals` 4,350, `SharpRestriction` 3,093, `HermitianCurvature` 1,922, …); then `GroundTheory` (8,507), `ReciprocityTheory` (3,845), `CompanionTheory` (2,027), `PositivityTheory` (449), `Lemmata` (167), `Supplements` (3). **All per-directory counts match README's table exactly** (I verified with `find … | wc -l`; total 175,187 `.lean`, 17,374,215 lines).
- Lots of `…_alt`, `…₂` (U+2082 subscript!) duplicate filenames and opaque machine names (`DesignS`, `DivinNOfHypV`, `KitS`, `ExS`, `ShapeWin`) — an AI-generation fingerprint. `lakefile.toml` sets global `maxHeartbeats = 4000000` and `--tstack=400000`, consistent with giant tactic scripts.
- No `sorry`, `admit`, `axiom` declarations, `native_decide`, `unsafe`, `opaque`, `implemented_by`, `@[extern]` per README's static scan; one `addDecl` file `Formalism/HermitianCurvature/HermitianCurvatureProofs/CutCptCopy.lean` (copies declarations under new names; still kernel-checked). **(README claim; independent full-tree scan is task-1's job.)**

---

## C. 中文通俗版（800–1200 字）

> 详细版本另见 `layman-zh.md`。

**黎曼猜想说的是什么？** 素数（2,3,5,7,11,…）看起来像随机撒在自然数里的，但它们的数量分布有一条极精确的"乐谱"。黎曼 1859 年把素数信息编码进一个函数 ζ(s)，它的零点（s 使得 ζ(s)=0）就像乐谱上的音符：如果所有非平凡零点都落在同一条竖线 Re(s)=1/2 上，素数的分布就"尽可能均匀"，误差项达到最优。这就是黎曼猜想（RH）；推广到所有狄利克雷 L 函数就是 GRH。

**这次发生了什么？** 2026 年 11 月 20 日，Anthropic 的数学家 Levent Alpöge 宣布：他和 Claude 一起找到了 RH（以及 GRH）的证明，并且把论证**完整形式化**成了 Lean 代码——约 17,400,000 行、175,187 个模块，不设任何假设（没有 sorry、没有额外公理）。MIT 的 Andrew Sutherland 独立编译并做了多重内核检查，到 11 月 20 日 22:05 UTC，结论是：五个主定理只依赖 Lean 的三条标准公理，独立实现的几个内核（nanoda、con-leche、lean4lean）都接受这份证明；但那个最关键的"防作弊"完整检查（Comparator 端到端运行）当时还在跑。

**证明的核心想法（按作者自己的说法）：** 在"函数域"（有限域上的曲线）里，黎曼猜想是一个**定理**，经典证明靠 Stepanov 行列式方法——构造一个辅助多项式/除子，利用"多重性"（重根）来数点。可是在整数 ℤ 上，没有现成的"多重性"可用，作者形容那"相当于要对整数求导"，做不到。他们的新办法是：用**一串 θ 提升（theta lifts）**来"模拟"多重性——θ 提升是自守形式（一种高度对称的"广义周期函数"）之间的升降机器，每做一次就像把"多重性"提高一层；对长度到 X 的 von Mangoldt 求和，所需的链长是 **√X**（作者说：不然还能是多少呢？）。整条论证把函数域/自守表示/Langlands 纲领的现代机器用了个遍，作者说" astounding amount of mathematics"。

**为什么形式化验证重要？** 数学论文会出错，但 Lean 的核（kernel）只认逻辑推演：如果代码编译通过、只依赖标准公理，那么"定理成立"这件事就由机器担保，而不是由"作者说"担保。Comparator 则是"防作弊"检查：确认代码没有偷偷改写定理的含义。

**但是，这不等于"已经完成"：** ①作者只发布了 Lean，没有发布人话写的证明——他说生成的文稿有 25 万页以上，没法读，只肯发布代码；②他本人在 4 页声明里承认：自己"还没有掌握这个论证周围的一大片数学"，"在高层自守形式方面造诣有限"，并期待论证会被大幅简化；③数学界还没有对论证达成理解与共识——2026 年菲尔兹奖得主邓煜据传（截图未经证实）说"没有 500 页的版本我连看都不看"；④按 Clay 数学研究所的规则，要正式发表、经过约两年检验并被广泛接受，才算拿了百万美元奖；⑤同期还有一份"纯人类、12 年工作"的 GRH 证明草稿（Alessandro Masullo，由 Ravi Vakil 发布），同样尚未验证，两者是独立竞争关系，不是互相翻译。

**一个常见误解：** 证明 RH 并不直接破解 RSA 等加密——RH 控制的是素数分布误差，和大数分解不是一回事。

**一句话总结：** 机器层面，"RH 已被 Lean 证明"这一说法目前经得起多项独立内核检查；人类层面，"我们理解了证明"还远远没有——这是一次"证明先到、理解后到"的历史性事件。

---

## D. Sources (all accessed 2026-11-21, Asia/Shanghai)

**Primary**
1. Levent Alpöge, remark.pdf (4 pp., 2026-11-20) — https://alpo.ge/remark.pdf ; local text extract `/home/kiler/rh-work/remark.txt`.
2. alpo.ge homepage — https://alpo.ge/ (author info only).
3. Andrew Sutherland (MIT), verification page + artifacts — https://math.mit.edu/~drew/grh/ ; files read: `audit.log`, `comparator.json`, `SHA256SUMS`, `nanoda.log`, `con-leche-master.log`, `con-leche-compare.log`, `lean4lean-default-fuel-timeouts.log`, `Audit.lean`.
4. Ravi Vakil, "Hurried Announcement: Alessandro Masullo GRH" (2026-11-20) — https://math216.wordpress.com/2026/11/20/hurried-announcement-alessandro-masullo-grh/ (WordPress unreachable from this environment; quote preserved at https://simonwillison.net/2026/Nov/20/ravi-vakil/ ).
5. Kevin Buzzard blog, "And the proof is checked in Lean" — https://xenaproject.wordpress.com/2026/11/12/and-the-proof-is-checked-in-lean/ (unreachable from this environment; quoted in Scientific American).
6. Local Lean archive — `/home/kiler/rh-full` (git `7cbf7a0c3`, mirror of https://alpo.ge/lean.tar.gz.part01…14, sha256 `9631b4f0…c7fc` per README/MIT page). Read-only.

**Secondary press / commentary**
7. TechCrunch (Tim Fernholz, 2026-11-20), "AI claimed a solution to the 167-year-old Riemann hypothesis — and a human did, too" — https://techcrunch.com/2026/11/20/ai-claimed-a-solution-to-the-167-year-old-riemann-hypothesis-and-a-human-did-too/ (includes Chris Birkbeck Zulip quote).
8. Nature news, "Mathematician says he and AI solved Riemann hypothesis…" (2026-11-20), doi:10.1038/d41586-026-03812-7 — https://www.nature.com/articles/d41586-026-03812-7 (Maynard, Granville quotes).
9. Scientific American (Clara Moskowitz, 2026-11-20), "The AI Riemann hypothesis proof is almost certainly true, independent mathematicians attest" — https://www.scientificamerican.com/article/the-ai-riemann-hypothesis-proof-is-almost-certainly-true-independent-mathematicians-attest/ (Sutherland, Buzzard quotes).
10. Scientific American (2026-11-20), "Anthropic mathematician claims to prove Riemann hypothesis…" — https://www.scientificamerican.com/article/anthropic-mathematician-claims-to-prove-riemann-hypothesis-most-famous-problem-in-all-of-math/
11. 36kr / 智东西 (2026-11-21, EN edition), "Has Claude Actually Proven the Riemann Hypothesis? Verified by Terence Tao, Deng Yu & Other Fields Medalists…" — https://eu.36kr.com/en/p/4078708897092744 (Tao blog, Kontorovich, Deng Yu, Sutherland, Glazer, Bloom, Clay rules, 250k pages).
12. Science.org (2026-11-20), "AI may have solved math's greatest mystery. Can humans understand the answer?" — https://www.science.org/content/article/ai-may-have-solved-math-s-greatest-mystery-can-humans-understand-answer (HTTP 403 from this environment; title/URL only).
13. Simon Willison's quotation of Ravi Vakil (2026-11-20) — https://simonwillison.net/2026/Nov/20/ravi-vakil/
14. Ransomnews (2026), "Riemann hypothesis proof would not break encryption" — https://ransomnews.com/riemann-hypothesis-proof-encryption-2026/ (used only for the encryption misconception).

---

## E. Open questions, contradictions and things I could not settle

1. **Comparator status is not knowable from the public snapshot I fetched.** The MIT page was still last-updated 22:05 UTC when fetched at ≈02:15 UTC on 11/21. con-leche `--compare` passing is strong independent evidence for statement-matching, but the official `lake comparator` + Lean paranoid kernel results were pending. **Recommendation:** re-check the MIT page later; it explicitly says it will be updated.
2. **Tao's blog post URL could not be located** (WordPress domains unreachable from this WSL environment; web_fetch and Windows-side network both failed). 36kr/智东西 quotes it; its content is summarized in A.6 as secondary only.
3. **Deng Yu's "500 pages" quote is from a screenshot of uncertain provenance** per 36kr's own framing ("suspected to be"); treat as viral, not confirmed.
4. **Masullo's GRH proof**: I could not retrieve the draft; only Vakil/TechCrunch descriptions. Its relation to Alpöge's work is *competition/independence*, not equivalence. The listing title "Unforced Euler singularity, unforced Navier-Stokes singularity, and the Generalized Riemann Hypothesis" surfaced in search but I could not verify it is Masullo's GRH manuscript — do not assert.
5. **The "√X chain length", "2/3 cost", "Vandiver weakening", "Bost slope inequality", "Behrend trick", "sixfold cover of GL5" are *not* literally present in the Lean source as named objects or docstrings.** The mapping in B.6 is inferred from structural similarity and cannot be considered author-confirmed. The author says in remark.pdf that even his own descriptions are partly paraphrases of a "slop" summary: "The parts in which Claude is the expert and not me I am sort of paraphrasing a 'slop' summary, which might make zero sense."
6. **The "GRH" proved is only for Dirichlet L-functions**; remark.pdf says he "expects, with more time, the Extended Riemann Hypothesis too" — ERH is not in these artifacts.
7. **Formal-vs-mathematical statement fidelity for the enormous "PublishedTheorems" corpus is unaudited.** The final theorem does not depend on those statements *as hypotheses* (they are proved from Mathlib), but their faithful formalization is part of why the project took 17.4M lines; a human review of even a fraction would be needed for the mathematical community to "absorb" it.
8. **Minor inconsistency in counts resolved:** `git ls-tree -r HEAD` gives 175,192 paths; 5 are non-Lean (README, .gitignore, lakefile.toml, lake-manifest.json, lean-toolchain) and 394 `.lean` files are quoted by git because their names contain U+2082 (`₂`), e.g. `SiegelWeil₂/...`; 175,192 − 5 = 175,187 `.lean` — matches README and MIT page. Local clone verified: 175,187 files, 17,374,215 lines.
9. **The 250,000-page textual proof was never released**; consequently the claim "there is a proof argument behind the Lean code" is, at the human level, still only the author's assertion plus a 4-page outline plus the Lean terms themselves. The Lean terms *are* the proof (formally), but no human has (publicly) read a mathematical narrative.
10. **Ethics/timing**: the author acknowledges the announcement timing "is horrible" and that a cynical reading (Anthropic IPO) exists but "is false"; Nature quotes Granville disputing this. This is a sociological, not mathematical, open point.
