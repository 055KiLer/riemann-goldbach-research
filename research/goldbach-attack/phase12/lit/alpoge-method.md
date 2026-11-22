# Phase-12：Alpöge/Claude 证明方法再挖掘——除「GRH 布尔值」外，还给出了哪些可用的定量机器？

> 执行：proof-digest（task-49）。日期：2026-11-22。本地材料：`/home/kiler/rh-full`（HEAD `7cbf7a0c32`，175,187 `.lean`，17,374,215 行；只读）。
> 已读前置材料：`phase12/0-plan.md`、`phase11/status/verification.md` §4（已列过同一批定理的 file:line，本报告在其基础上补：**精确陈述、证明项位置、相对 GRH 的强度判定、家族均匀性、能否升级 Ratios**）、`phase6/0-phase6-报告.md`（避免重复）。
> 标签：**[事实]**=文件/命令直接读到；**[推断]**=我的逻辑推断；**[推测]**=判断，未经独立审计。

---

## 0. 结论先行（四条裁决）

**裁决 1（相对「GRH 的直接推论」是否更强）：不更强。**
[事实] 全部十几项"定量机器"都是**经典解析数论结果的形式化**（Siegel 下界、Siegel–Walfisz、Dirichlet L 零自由区、ζ 零自由区、经典显式公式、零点计数、**D–H 型零点排斥**、零密度盒、大筛、特征和矩、Rankin 均方），没有一个是在"已证 GRH"之外新增的、比 GRH 直接推论更强的定量定理。逐项比较见 §2 的"相对 GRH"列：Siegel–Walfisz / 零自由区 / 零密度在 GRH 下要么被远更强的估计（AP 中 ψ 的 `x^{1/2+ε}` 级误差、`Re>1/2` 无零点）直接覆盖、要么 vacuous。它们的价值在于**无条件（不依赖 GRH）**——而在本场景 GRH 已证，故逻辑上冗余。
**唯一比"布尔 GRH"多出来的公开定量结论**是 Robin/Lagarias 不等式（MIT 页 2026-11-21 12:55 版 "Arithmetic consequences"：`robin_inequality`、`lagarias_inequality`，与 `kimihiro64/Robin1984` 组合导出，导出 axiom 仍仅 3 条）[事实，转引自 `phase11/status/verification.md` §4]。但这两条是 RH 的经典等价/直接推论，不是新解析机器。

**裁决 2（能否升级成 H_Ratios / RAT(c) 的新输入）：不能。**
[事实] 档案中没有：2/2 ratios 定理、pair correlation、跨特征标 L'/L 矩/相关核、level-aspect 的 L 函数 family moments、MDS。上 phase-6 scan 已确认 `correlation`/`pair correlation`/`mollifier(L 函数意义)`/`second moment` 等 0 命中；本 phase 复核 GL3MeanSquares 目录，确认其中没有 GL(3) L 函数矩定理（见裁决 3）。
[推断] archive 的 family-level 定量能力只到：**零点计数/零密度（family over all primitive χ mod q 或 conductor ≤Q）**、**AP 素数误差（modulus-uniform）**、**特征和的二阶/四阶矩与大筛**。这些是 G-W-X 的**主项/交换项结构之外**的输入：Ratios 的主项需要 MD 的函数方程与极结构（phase-11 已确认不存在），而**误差项**的控制即使有 GRH+零密度也不够（RAT(c) 需要 `q^{1−cη}` 级、固定 shift `η` 与 1/2 附近的 1/L 控制，见 §4 的三次具体升级尝试及否决）。

**裁决 3（GL3MeanSquares 的作用）：技术工具包，不是可独立使用的 GL(3) Rankin–Selberg 矩定理。**
[事实] `src/Formalism/GL3MeanSquares/`（约 400+ 文件）的内容是：PNT-AP（`PrimeCountAsymptoticInProgressions.lean`：`LogDerivSeries`、`PrimeCountAsymptoticInProgressions`、`ShortIntervalImpliesProgressions` 等）、零密度盒（`CountSt.lean:7 ZeroDensityBox`、`CountZAll.lean:13 zero_density_box`）、prime-pair/box 选择（`PrimePairOfBoxAndWeakMeanSquareHypotheses.lean`）、均方假设（`MeanSquareHypW`）、hook formula/torsion 的数值估计等——**目录内搜索 "Rankin"/"GL(3)"/"Selberg" 均无相关定义**（只有 import 行含路径名）。它服务于 `Formalism/LocalToGlobal/GlobalTheory/*` 的"分析结论"：如 `AnalyticConclusionOfProp25.lean:40 chain6At : Gz x ≤ x^{1/2+(eD+eL+6)ε}`（Chebyshev 增长）、`AnalyticConclusionCompatibleMeanSquare.lean:54 zeroDensityBox`、`:70/:93` 的 PNT/均方变体——即**证明的技术引擎**。[事实] 真正的 Rankin 均方在 `Development/.../FoundationProofs/RankinMeanSquareCuspForm.lean:138 theorem rankin_mean_square`（GL(2) 型 cusp form 系数的均方估计，已证），不在 GL3MeanSquares 目录里，也不是 GL(3) Rankin–Selberg 定理。

**裁决 4（实际可用的东西）：只有"Lean 资产 + 经典引理库"，没有数学新输入。**
[事实/推测] (a) 这些经典定理已在 Lean 中**无 sorry 证明**（除 §1 特别标注的少数"未实现接口"），未来若把 H_Ratios/RAT(c) 的（条件性）论证形式化，可直接复用它们做经典解析输入，节省大量工程；(b) **不要**把它们当作"比 GRH 强"的定理引用——它们要么是 GRH 的推论（更弱）、要么在 GRH 下 vacuous。**特别警示**：`ExplZeta`/`ExplChi` 两个"显式公式接口"在档案中**找不到任何证明项**（只作条件定理的假设/结构字段），`ZeroDensityBound`（含 `10^88`、`10^421`、`Q^99` 显式常数）同样只是**假设接口**（见 §1 的"未实现接口"清单）。

---

## 1. 逐项精确定位：陈述 / 位置 / 证明状态 / 相对 GRH

**总说明**：以下 [事实] 的"证明状态"列：**已证** = 找到 `theorem X : Prop := <proof>`；**接口** = 只有 `def X : Prop`，全树 grep 找不到产生它的证明项（仅作为条件定理的前提或结构字段出现）。全档案无 `axiom`/`sorry`（MIT 静态扫描 + `phase11/status/gh/comm_notes.md`）；"接口"不是 axiom，而是**未被证明的假设**（conditional statement 的输入），引用时不能当已证事实。

| 名称 | 精确陈述（缩写；完整见源文件） | 定义位置 | 证明位置 / 状态 | 相对 GRH | moduli/family 一致性 | 能让 RAT(c)/Ratios 升级？ |
|---|---|---|---|---|---|---|
| `SiegelLower` | `∀ε>0 ∃c>0 ∀q χ(χ²=1,χ≠1): c·q^{−ε} ≤ ‖L(χ,1)‖` | `SiegelWalfiszAP.lean:29` | `FinalSiegel.lean:17` **已证**（`siegel_theorem_of …`，Siegel 定理，经典**无效**） | GRH ⇒ 明显更强（`L(1,χ)` 的界远好于 `q^{−ε}`）；SW 是无条件但无效版本 | 对 q 一致 | **否**：只是 main-term 技术输入 |
| `SiegelWalfisz` | `∀A>0 ∃c C>0 ∀q≤(log x)^A, 2≤x: ‖psiChi χ x −(χ=1?x:0)‖ ≤ C x e^{−c√log x}` | `SiegelWalfiszAP.lean:33` | `SiegelWalfiszAPOfSiegelLower.lean:34` **已证**（`siegelWalfisz_of_siegelLower siegelLower`） | GRH ⇒ AP 误差 `O(x^{1/2}log²)`，**远强**；SW 是经典无条件弱版本 | 对 `q ≤ log^A x` 一致 | **否**：经典 major-arc 输入，非新 |
| `SiegelWalfiszAP` | `psiAP(q,a,x)` 版本（同型误差） | `:38` | **接口**（未找到证明项） | 同上 | 同上 | 否 |
| `PsiChiBound` | 带例外零点集 B 的 `psiChi` 界（`q ≤ e^{c√log x}`） | `:22` | `SiegelWalfiszAPOfSiegelLower.lean:23` **已证** | GRH 下例外零点不存在 ⇒ 更强/冗余 | q 一致 | 否 |
| `ZFRDirichlet` | `∃c>0`: 在 `1 − c/log(q(|Im s|+2)) < Re s` 内，唯一可能的零点是实特征标 χ²=1 的实零点 β（单重、且 χ'=χ, s'=β 唯一） | `LandauZeroFreeBounds/Statement.lean:15` | `NoZeroComplex.lean:32` **已证** | GRH ⇒ 无零点，**更强**；ZFR 是经典无条件弱版本 | q 一致 | 否（经典零点区域） |
| `zeroFreeRegion` (ζ) | `∃c>0 ∀s≠1, 1−c/log(|Im s|+2) ≤ Re s ⇒ ζ(s)≠0` | `Formalism/ZeroFreeRegion/Statement.lean:9` | `FinalZFR.lean:17` **已证**（`classicalZeroFreeRegionOfBounds …`） | RH ⇒ 更强 | — | 否 |
| `LogDerivRegionChi` | `∀c₁∈(0,1/20] ∃C ∀q χ B(例外零点), ∀s∈InRegion(c₁/2,q), s≠β: ‖−L'/L(χ,s)+Σ_{β∈B}1/(s−β)‖ ≤ C log²(q(|Im s|+2))` | `LogDerivRegionChiOf.lean` | `SiegelWalfiszAPOfSiegelLower.lean:17` **已证** | GRH ⇒ `Re>1/2` 全域 log² 界（更强、区域更大）；本定理只在经典 ZFR 内 | q 一致 | 否（单特征标、ZFR 内） |
| `one_sub_re_ge_of_exceptional_zero_repulsion` | D–H 型零点排斥：例外零点 β 使任意其他零点 `1−Re ρ ≥ c log(c/((1−β)L))/L`（`L=log(q(|Imρ|+2))`） | `RepulsionStatement.lean:8` | **已证**（`GlobalTheory.Lin.Repulsion.repulsion`） | GRH 下无需；经典无条件 | q 一致、含例外零点 | 否（零点计数型，不产生 ratio 主项） |
| `logFree_zeroDensity_dirichlet_one_modulus` | `∃A C η>0`: `Σ_{χ mod q} Σ_{ρ∈zerosBox χ σ T} ord(ρ) ≤ C(qT)^{A(1−σ)}`（`2≤T`, `1−η≤σ≤1`） | `LogFreeZeroDensityDirichletOneModulusStatement.lean:8` | **已证**（`GlobalTheory.Lin.LogFree.zero_density`）；但全树几乎无消费者（仅 `SumRpowZerosLe.lean`） | GRH ⇒ vacuous（无 `Re>1/2` 零点）；log-free 是无条件经典加强 | **对 q 一致的 family sum（所有 χ mod q）** | **否**：只控制零点计数 |
| `ExplZeta` | ζ 的显式公式（含 `psiChi 1`、`zsum` 零点项、`log(2π)` 项，误差 `C(log x + x/T·log²(xT))`） | `…/PublishedTheorems/AutomorphicForms₂/ExplZeta.lean:12` | **接口（无证明项）** | GRH ⇒ 更强的 ψ 误差；经典显式公式本身标准 | — | 否 |
| `ExplChi` | 同型 Dirichlet L 显式公式（含 `χ(−1)`、`L'/L(χ⁻¹,1)` 项） | `ExplChi.lean:12` | **接口（无证明项）** | 同上 | — | 否 |
| `LogDerOne` | `∃C ∀q>1,χ primitive: ‖L'/L(χ,1) − Σ_ρ 1/(1−ρ)‖ ≤ C log(3q)` | `LogDerOne.lean:12` | `…/Proofs/DivisorProofs/LogDerOneHolds.lean:11` **已证**（用 `LWide.logDeriv_LFunction_strip`） | GRH 下可更强（但 s=1 处 log q 已标准） | q 一致 | 否（s=1 单点、单特征标） |
| `ZeroCount` | `∃C ∀q,χ primitive,t: Σ_{ρ∈单位区间} 1 ≤ C log(q(|t|+2))`（重数计） | `ZeroCount.lean:12` | `…/GlobalInterpolation/ZeroCountHolds.lean:7` **已证**（用 `GlobalTheory.ZeroWindow.count_zeros_window`，`FinsumMemLeOfSubset.lean:43`） | GRH ⇒ 仍有（甚至更强）零点计数；标准 RVdB 型 | q 一致 | 否（计数型） |
| `ZeroDensityBox` | `∃C ∀Q ∀S(primitive χ, conductor ≤Q, 有零点 1−1/400<Re, |Im|≤Q): |S| ≤ C·Q^{1/4}` | `…/JacobiCharacterSums/CountSt.lean:7` | `CountZAll.lean:13` **已证**（mollifier/对偶/Jacobi 和装配；`AnalyticConclusionCompatibleMeanSquare.lean:54` 再包装） | **GRH 下 vacuous**（无 Re>1/2 零点）——纯无条件工具 | **对 conductor≤Q 的 family（所有 primitive χ）一致**，这是档案里最强的 family-level 定量工具之一 | **否**：零点计数，不含 1/L 值/主项 |
| `ZeroDensityBound(σ,Q)`（显式常数） | `#ZeroPairs(σ,Q) ≤ 10^88·(10^421·Q^99)^{1−σ}` | `SmoothedRemainderRealIntegralFormula.lean:81` | **接口**（仅作 `ExceptionalCharacterCountBound` 的假设，`:86-88`；未找到证明项） | GRH 下 vacuous | family over conductor ≤Q | 否 |
| 乘性大筛 | `Σ_{q<Q} Σ_{χ primitive mod q+1} ‖Σ_{n∈(M,M+N]} a_nχ(n)‖² ≤ (Q²+2πN)Σ‖a_n‖²` | `MultiplicativeLargeSieveStatement.lean:6` | **已证** | 无条件经典；GRH 不推出（也不被推出） | **跨模数、跨特征标求和，显式常数** | **否**（只给特征和二阶矩） |
| 算术大筛 | `|S|·(φ(q)/q·log Q) ≤ Q²+2πN`（每素数避一剩余类） | `ArithmeticLargeSieveOneResidueClassPerPrimeStatement.lean:6` | **已证** | 无条件经典（Selberg 型） | 显式常数 | 否 |
| `M4` / `CharOrtho` / `ParsevalHolder` | 非主特征标四阶矩 `Σ_χ‖I_Xχ‖⁴ ≤ C l^{1+ε}X²`；正交性；显式 Parseval/CS（任意特征标子集） | `Formalism/LFunctionBounds/PositivityBound.lean` | `M4` **已证**（`Development/WeilBound/.../MatchAll.lean:26`）；`CharOrtho`/`ParsevalHolder` 仅定义级（证明未逐一追） | 经典特征和矩；GRH 无关 | 跨特征标求和（同一模 l） | **否**（特征和矩，非 L'/L 矩） |
| `rankin_mean_square` | cusp form 系数均方：`h 0=0 ∧ Σ‖h n‖²/n^{k+s}` 收敛且 `s·Σ… ≤ C` | `FoundationProofs/RankinMeanSquareCuspForm.lean:138` | **已证** | 经典自守估计 | — | 否；不是 GL(3) Rankin–Selberg |

**档案中不存在**（[事实]）：pair correlation（0 命中）、L'/L 跨特征核、2/2 ratios、family moments of L-functions、level-aspect pair correlation、MDs（multiple Dirichlet series）。

---

## 2. 证明主架构（[事实]，file:line）

**最终定理链**（每步都是短文件，可读）：
```
Main.riemannHypothesis := rhOfAll := Formalism.VW.rh_of_every allChi        [Main.lean:5; MainTheorems.lean:9]
  allChi := UpperTheory.FinalTheorems.everyCharacter                        [MainTheorems.lean:7]
    everyCharacter := everyCharacter_of_row galoisLocalGlobalStrong_recParameter   [CharacterBoxes/MainConclusion.lean:7,10]
      ← OpenLiteratureStatements (Row0b, RecTExists) + UpperTheory.One.vwin_of_row (VWin)
      every_character_of_theta_integrals_local_matching (SiegelEisensteinSecondTermHypotheses.lean:69)
      → every_character_of_green_v_win (ThetaPairLifts/ThirdPlaceSeries/TopPlug.lean:16)
      → zero_free_all_of_green_v_win (TopPlug.lean:12)
      → zeroFreeAll_of_topG (CharacterBoxes/ZeroFreeAllOfTopG.lean:26)
         需要 HostExW + Chebyshev 增长（见下） + TopG（Green）
      → imprimitive (CharacterBoxes/Imprimitive.lean:5) ⇒ UpperTheory.EveryCharacter
  Formalism.VW.rh_of_every ⇒ RiemannHypothesis（函数方程，Formalism/GammaFactorNonvanishing/CritLine.lean:29）
```

**Chebyshev 增长 + 解析机器的接入点**：
- 增长接口：`ChebyshevInequalityOnWindows`（`Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/TopWin.lean:26`）：`Λ.Gm x ≤ x^{1/2+(eD+eL+7)·ε}`；`windowInequality_of_artinInputs`（`PrimitiveCosets/WindowInequalityOfArtinInputs.lean:17`）把它归约到 `FamCoreConstantBounds`/`core_gm`。
- 解析结论链（GL3MeanSquares/GlobalTheory）：`AnalyticConclusionOfProp25.lean:40 chain6At : Gz x ≤ x^{1/2+(eD+eL+6)ε}`，来自 `LBr2.HostAnalyticConcl ← analytic_input_conditional noRealZeroSmall logNE`；其中 `noRealZeroSmall := GL2b2.no_real_zero_small_modulus`、`logNE := ZeroFreeRegionGL2.log_nonexceptional_bound`；`AnalyticConclusionCompatibleMeanSquare.lean:54 zeroDensityBox`、`:70 chain6AtFinal`、`:93 chain6AtPNT` 是 PNT/均方/零密度变体（条件于 `MeanSquareHypW`/`BoxCountHyp`/`PNTAPRelW`）。这些正是 `GL3MeanSquares` 目录的用途：**为上层理论提供 Chebyshev 增长（Gz ≤ x^{1/2+…}）的技术引擎**。
- Host 条件链（文献分支）：`HostExOfPublished.lean:30 hostEx_of_zeroFreeRegion : ExplZeta → ExplChi → LogDerOne → ZeroCount → ZFRDirichlet → TZRat → PageThm → Jutila → QuadraticHeckeZeroEstimates → HostEx`（经 `qdChoice_of_explicitFormula`、`thin_choice_of_zero_density`、`norm_primes_and_level_prime`、`smallPrimeOne_of_tzRat`、`tops_choice` 组装，`HostExistenceOfChoicesStatement.lean:12`）。`HostExW`/`PreHostAn`/`HostConditions` 在 `TotientGaloisClasses/Analytic.lean`、`ExplicitFormulaErrorOfHostConditions.lean` 定义/使用，给出 `ChebyshevCharacterBound`、`LogDerivativeBound`、`BoundedCharsPointwise`、`ExceptionalCharacterKept` 等**解析输入**，供 §2 的 TopG/Chebyshev 链使用。
- **[推断] 重要结构性观察**：这条经典解析链看起来位于**辅助/文献分支**，不一定是最终证明项的依赖。证据：(a) `HostExOfPublished` 全树唯一 importer 是 `Development/AbelianVarietyTheory/Proofs/HeightProofs/ExistsRecordOverChoices.lean`（非主链文件）；(b) `ThinChoiceOfZeroDensity.lean:30` 的证明体是 `fun _ _ _ _ _ => thinChoice_host`——**显式忽略** ExplZeta/ExplChi/LogDerOne/ZeroCount/ZFRDirichlet 全部参数；(c) 最终 `everyCharacter` 链走 θ-lift/literature（Row0b）路线，而 `OpenLiteratureStatements` 只有 3 个字段。→ **不能依据"文件在 Main import closure"就认为这些定量定理在主证明项中起关键作用**；需要 Lean 依赖追踪才能最终定论（本次未做）。[推测]

---

## 3. 为什么这些**不能**升级为 family average / Pair correlation / Ratios

### 3.1 三次具体升级尝试与否决（[推断]）

**(T1) 用 `ZeroDensityBox`（family over conductor ≤Q，`|S| ≤ C Q^{1/4}`）+ 例外零点排斥 → 2/2 Ratios 的误差项。**
否决：零密度/排斥控制的是**零点计数**（且 `ZeroDensityBox` 的区域是 `Re>1−1/400`，GRH 下 vacuous）。G-W-X/RCT(c) 需要的是 `R_q(a,b;s,t)=φ*(q)Z_q+H_q Z_q(1−b,1−a)+O(q^{1−ω})` 的**两项主项 + 极结构**，其主项来自 ratios/MD 的**函数方程与留数**，零密度不产生任何主项或交换项；误差项方面，RAT(c) 要固定 shift `η` 与 1/2 附近的 1/L 控制（`q^{−cη}`），零密度给不了这种**值分布**信息。**否决。**

**(T2) 用大筛（`Q²+2πN`）或 `M4`/`ParsevalHolder`（跨特征标二阶/四阶特征和矩）去控制 phase-12 §1.3 的 wrap 和 `W`。**
否决：`W` 是 `nm−rl=kq` 上的双线性计数（wrap 贡献），需要 `≪ q^{1−ηA+ε}` 级别的 saving（A>2 时相对平凡界要 `q^{2A−2+ηA−ε}`）。大筛/Parseval 给出的是**特征和平方的族和**上界（`Q²+2πN` 型），对 `q` 的 saving 至多来自族大小/模数的平方根，且方向不匹配（它们界的是 `Σ_χ |Σ a_nχ(n)|²`，不是双线性 `A≡B mod q` 的系数关联）；不能产生所需的跨特征标高阶相关估计。**否决**（作为 phase-12 wrap 攻击的输入无效；这是 [推断]，建议 kernel-theorist 复核技术细节）。
**(T3) 用 `LogDerivRegionChi`（GRH 区内的统一 L'/L 界）直接推 G-W-X 所需移位区域（`Re=1/2+η`）的 1/L 控制。**
否决：该定理的区域是经典 ZFR：`1−c/log(q(|Im s|+2)) < Re s`，**不覆盖** `Re=1/2+η`（固定 η 与 q 无关时，1/2+η 远在该区域外）；且它只给单特征标、不含跨特征相关；而 Ratios 的交换项需要**第二主项**（`H_q Z_q(1−b,1−a)`）及其 1/L 结构。**否决。**（注：若愿意用"已证 GRH"+Hadamard 自行推 `Re>1/2` 的 L'/L 界，那是标准推论，不是档案内容，也不足以证明 Ratios。）

**(T4) 唯一可尝试的"升级"是工程性的**：把档案中这些经典机器的 Lean 实现作为**H_Ratios/RAT(c) 形式化项目的引理库**（显式公式/零点计数/零密度/大筛/均方均有 Lean 证明或接口）。这能省去经典解析部分的形式化工作量，但**不改变数学缺口**。

### 3.2 与 Lead 的 phase-12 攻防计划的关系
[推断] phase-12 的核心是 `RAT(c)`（c>2 的直接移位 Ratios）与 wrap 和 `W`。Alpöge 档案的定量机器**对这两块都不提供新输入**：
- 对 RAT(c)：缺的是 MDs 函数方程/2/2 结构（phase-11 已结论），不是经典误差项；archive 的经典机器最多用于**主项之外的经典分析**（而 G-W-X 主要 gap 在主项结构）。
- 对 wrap `W`：需要的是双线性/Kloosterman 型 saving；archive 只有大筛/特征和矩（方向不合），且其 `ZeroDensityBox` 等是零点计数而非算术和估计。

---

## 4. 「相对 GRH 更强」的逐类判断（[推断]，基于 §1 表）

| 类别 | GRH 直接推论 | archive 的定量机器 | 谁更强 |
|---|---|---|---|
| AP 素数 / ψ(x,χ) | GRH ⇒ `ψ(x,χ;q,a) = x/φ(q) + O(x^{1/2}log²(qx))`（对所有 q） | Siegel–Walfisz：`x e^{−c√log x}`（`q≤log^A x`），**无条件但无效** | **GRH 更强** |
| 零点分布 | GRH ⇒ 临界线上 | ZFR：`Re ≥ 1−c/log`；log-free 零密度 | **GRH 更强/冗余** |
| 零点计数 | GRH ⇒ 仍有 `O(log q)`/单位区间 | ZeroCount、ZeroDensityBox（近 1 区域） | GRH 下 ZeroDensityBox **vacuous**；ZeroCount 与 GRH 兼容（标准） |
| 显式公式 | GRH ⇒ 更强 ψ 误差 | ExplZeta/ExplChi（接口）、PI.ExplicitFormula、ExplicitS | 标准/较弱 |
| L'/L | GRH ⇒ `Re>1/2` 一致界 | LogDerivRegionChi（ZFR 内）、LogDerOne（s=1） | **GRH 更强** |
| 特征和/大筛 | GRH 不直接蕴含（经典工具） | 大筛 `Q²+2πN`、`M4`、`CharOrtho`、`ParsevalHolder` | 互相独立；均非 family L 函数矩 |
| 均方 | — | Rankin mean square（GL(2) 型）、`MeanSquareHypW`（Jacobi 特征和） | 经典；与 GL(3) Rankin–Selberg 无关 |
| 零点排斥 | GRH 下不需要 | D–H repulsion | 经典无条件；GRH 下冗余 |

**结论**：没有任何一项是"GRH 已证之后新获得的、比 GRH 直接推论更强"的解析机器。**唯一新的定量公开推论是 Robin/Lagarias 不等式**（§0 裁决 1），它们是 RH 的经典等价/推论。

---

## 5. 未能落实/需要后续确认的点（诚实标注）

1. **[事实] `ExplZeta`/`ExplChi` 无证明项**：全树只以 `def`（`ExplZeta.lean:12`/`ExplChi.lean:12`）、import、结构字段（`GeneralHyps.lean:112-113`、`DiscreteSeriesCoefficientsCuspidal.lean:364-365` 等）与**条件定理的前提**出现；未发现任何 `theorem … : ExplZeta`。→ 引用时须写"接口/假设"，不能当已证。**建议 Lean 侧独立复核**（可能是某个大结构构造时用别的方式提供，我没找到）。
2. **[事实] `SiegelWalfiszAP`、`PrimeShareSW`、`ZeroDensityBound`、`CharOrtho`、`ParsevalHolder`**：本次只找到定义，未找到证明项（`ZeroDensityBound` 明确只作为 `ExceptionalCharacterCountBound` 的假设出现）；标"接口/部分定义级"。
3. **[推断] 主证明项是否真的依赖经典解析链**：证据（`HostExOfPublished` 仅被一个非主链文件 import；`ThinChoiceOfZeroDensity:30` 显式忽略参数）表明这条链可能是**辅助分支**。需 Lean 依赖追踪（`#print axioms` 只给公理，不能给模块依赖）或 `rhOfAll` 证明项展开才能定论。
4. **[事实] 官方验证状态**：MIT 页 2026-11-21 12:55 UTC 版仍 3 项 running（phase-11 status 实抓）；本报告不依赖"验证完成"。
5. **[事实] MIT 12:55 版新增 "Scope"**：GRH 指**所有模、所有特征的 Dirichlet L**；Dedekind/Hecke/自守 L 不在检查范围——与 §1 的"GRH 布尔值"范围一致。

---

## 6. 来源与证据

- 本地 archive：`/home/kiler/rh-full`（HEAD `7cbf7a0c32`，175,187 `.lean`，17,374,215 行）。
- 关键文件/行号见 §1、§2 内联引用；核验命令：`grep -rn --include='*.lean'`、`sed -n` 直读。
- 前置报告：`phase11/status/verification.md` §4（同一批定理的 file:line 初查）；`phase6/0-phase6-报告.md`（Alpöge 仓库定量扫描 task-28）；本报告在其上补精确陈述/证明项/强度/升级判定。
- 外部：MIT 验证页 https://math.mit.edu/~drew/grh/（2026-11-21 12:55 UTC 版，经 phase-11 status 实抓；访问日期 2026-11-22）；`phase11/status/gh/comm_notes.md`（静态扫描：无 axiom/sorry；818,755 theorem/lemma；242,067 def 等）。
- 局限：本报告为**类型级静态分析**，未做完整 Lean 依赖追踪、未重编译；"接口"判定基于 grep 未找到证明项，可能遗漏（已标注）。
