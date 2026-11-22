# Alpöge/Claude RH+GRH Lean 仓库扫描：有没有对 Goldbach 有用的定量/相关型内容？

**执行者**：proof-digest（teammate）· **日期**：2026-11-21 · **时间盒**：45 分钟
**扫描对象**：`/home/kiler/rh-full`（git `7cbf7a0c3`；175,187 个 `.lean` 文件；17,374,215 行；只读，未做任何修改）——Alpöge/Claude 声称证明 RH+GRH 的 Lean 归档（alpo.ge/lean.tar.gz.part01–14 的干净镜像）。
**方法**：`grep -r`（大小写不敏感）/ `find -iname` 全树扫描；对命中文件用 `sed` 读**定理/定义的精确类型**（不读证明体）。无 `rg`（环境未安装）。标注：**【事实】** = 我直接读到的文件内容/命令输出；**【推测】** = 我的判断，未经作者确认。
**任务背景**：LL 的 Hypothesis R 需要 `‖T_N‖ ≤ δ_N`，即**跨特征标 L'/L 相关核的 N^{-1/2} 级估计**。本扫描回答：Alpöge 证明机器里是否有可复用的定量引理。

---

## 0. 结论（TL;DR）

1. **【事实】仓库完全没有 Goldbach/加性结论**：`goldbach`、`sum of two primes`、`binary goldbach`、`Goldbach conjecture` 等字符串全树 **0 命中**（含注释、docstring、文件名）。也没有 twin prime、素数对 `(n,n+h)`、circle method、major/minor arc、exceptional set 的陈述（各 0 命中）。
2. **【事实】仓库完全没有 pair correlation / 素数对相关 / Katz–Sarnak / Montgomery 型统计**：`pair correlation` 0、`correlation` 0、`katz-sarnak` 0、`montgomery` 0、`n-level` 0、`level density` 0、`random matrix` 0、`second moment` 0（`GUE` 作整词 0；`Katz` 564 文件全是 `GlobalTheory.Katz` 形式余边界/Teichmüller 对象，与 Katz–Sarnak 无关；`Weil positivity` 32 命中是 `SplitWeil` + `PositivityTheory` 命名空间拼接的假阳性；`mollifier` 71 文件全是复分析 L²∂̄ 估计里的 mollifier）。
3. **【事实】没有"跨特征标 L'/L 相关核"对象**：仓库里不存在把两个特征标 χ₁, χ₂（或两个谱点）的 L'/L 做相关/二次型/核平均的定理。最接近的只有：**单特征标**的定量 L'/L 界（`LogDerivRegionChi`：零无区里 ‖−L'/L + 例外零点项‖ ≤ C·log²(q(|Im s|+2))，全 q、χ 一致——已证）、s=1 处的单特征标 L'/L 界（`LogDerOne`），以及 §4b 的**角色族（跨特征标求和）工具**（Pólya–Vinogradov、正交/Parseval、四阶矩、特征标族零密度、"KillingLemma"族平均）——这些是跨特征标的**特征和/平均**工具，仍不是 L'/L 的相关核。
4. **【事实】仓库确实包含一批"正宗"定量解析数论接口**（比预料的多）：带定量误差项的显式公式（`PI.ExplicitFormulaWith`、RH 强度版 `explicit_formula_dirichlet_zeros_right_half`）、Siegel–Walfisz 定理及 ψ(x,χ)/ψAP 的一致定量界（已证）、Dirichlet L 的定量零无区与零无区内 L'/L 界（已证）、ζ 的零无区/L'/L 区域（`Formalism/ZeroFreeRegion`）、以及 `ChebyshevGrowthImpliesZeroFree` 这类"Chebyshev 增长 ⇒ 零无区"接口。**但这些是经典解析数论（多为对已发表文献的形式化），不是新定理，也不是"相关型"估计。**
5. **【推测】对 LL 的 Hypothesis R 直接可复用的东西基本没有**；能借鉴的只是**技术骨架**：(a) 显式公式的误差形（uniform in conductor）；(b) 零无区内单特征标 L'/L 的 log² 界；(c) `TwistFamilyExistence/Statement.lean` 里"扭转族二阶矩 + 鸽笼挑出 L'/L 受控的特征标"的模式（但该文件只有定义、无证明、无任何调用者，见 §4.9，是死代码/脚手架）；(d) Chebyshev 增长→零无区的映射；(e) §4b 的 `LFunctionBounds` 跨特征标工具（Pólya–Vinogradov、`CharOrtho`、显式 `ParsevalHolder`、`M4` 四阶矩、`KillingLemma` 族平均、`Density` 族零密度）——这是最可能被改造成 Hypothesis R 所需"族上二次型/矩"的素材，但仓库本身没有 L'/L 相关核。以上都不提供 `‖T_N‖≤δ_N` 形式的现成跨特征相关界。

---

## 1. 搜索证据（命令输出摘要）

**【事实】** 全树（175,187 文件）字符串命中数：

| 词 | 命中文件数 | 备注/样例路径 |
|---|---:|---|
| `goldbach`（任意大小写） | **0** | — |
| `sum of two primes` / `binary goldbach` | **0** | — |
| `twin prime` | **0** | — |
| `pair correlation` / `correlation` | **0** | — |
| `katz-sarnak` | **0** | — |
| `montgomery` | **0** | — |
| `n-level` / `level density` / `random matrix` | **0** / 0 / 0 | — |
| `second moment` | **0** | — |
| `guinand` | **0** | — |
| `stepanov` | **0** | — |
| `weil positivity`（字面） | 32（**假阳性**） | 全是 `GlobalTheory.SplitWeil PositivityTheory` 命名空间拼接，如 `Development/WeilBound/.../SmallFSing.lean:8` |
| `mollifier` | 71（**假阳性**） | 复分析 mollifier：`ReciprocityTheory/L2DbarEstimates/Mollifiers/*`，非 L 函数 mollifier |
| `Katz`（整词） | 564（**假阳性**） | `namespace Katz` / `GlobalTheory.Katz.*`：形式余边界、Teichmüller 提升，非 Katz–Sarnak |
| `chen`（子串） | 60 → `-w Chen` **0** | 无 Chen 定理 |
| `sieve` | 577（假阳性子串） | 抽样路径无筛法定理，如 `Formalism/ThickAverageLoss/*` |
| `explicit formula`（短语） | 0；文件名 `*ExplicitFormula*` | **19** 个文件 |
| `chebyshev` | 141（内容）/ 10（文件名） | `Formalism/ZeroFreeRegion`, `Formalism/ZetaNonvanishingChebyshevWeights.lean`, `Formalism/PeriodIntegrals/Chebyshev*.lean` |
| `vonmangoldt` | 133（内容）/ 16（文件名） | `GlobalInterpolation/*VonMangoldt*`, `Formalism/LandauZeroFreeBounds/*` |
| `logDeriv` | 579 | `Formalism/ZeroFreeRegion/*`, `Formalism/LandauZeroFreeBounds/*` |
| `hermitiancurvature`（目录） | **1,922** 文件 | `Formalism/HermitianCurvature/**`（内部 Fourier 衰减/双陪集核，非数论统计） |
| `thetalift`（文件名子串） | 1,321 | `Development/.../ThetaLifts`, `ThetaCorrespondence` |
| `iwasawa` | 14,585 | 主要是 Iwasawa 分解/局部理论机器 |

**【事实】** 仓库中**没有 docstring 传统**：定理几乎全部是无注释的生成式名字（`Green`、`DesignS`、`DivinNOfHypV`、`gChi`…）。因此本扫描主要依据**类型签名**（§3、§4）和字面词命中（上表）。

---

## 2. 顶层定理的精确陈述（【事实】）

`src/Statements.lean`（全文，只 import Mathlib）：

```lean
def RiemannZetaZerosOnLine : Prop :=
  ∀ s : ℂ, riemannZeta s = 0 → (¬∃ n : ℕ, s = -2 * ((n : ℂ) + 1)) → s ≠ 1 → s.re = 1 / 2

def DirichletLNonvanishingRightOfHalf : Prop :=
  ∀ (N : ℕ) [NeZero N] (χ : DirichletCharacter ℂ N) (s : ℂ),
    1 / 2 < s.re → (χ ≠ 1 ∨ s ≠ 1) → DirichletCharacter.LFunction χ s ≠ 0

def DirichletLZerosOnLine : Prop :=
  ∀ (N : ℕ) [NeZero N] (χ : DirichletCharacter ℂ N) (s : ℂ),
    0 < s.re → s.re < 1 → DirichletCharacter.LFunction χ s = 0 → s.re = 1 / 2

def PrimitiveDirichletLZerosOnLine : Prop :=
  ∀ (N : ℕ) [NeZero N] (χ : DirichletCharacter ℂ N), χ.IsPrimitive →
    ∀ s : ℂ, 0 < s.re → s.re < 1 → DirichletCharacter.LFunction χ s = 0 → s.re = 1 / 2
```

`src/Main.lean`（全文）：

```lean
theorem riemannHypothesis : RiemannHypothesis := rhOfAll
theorem riemannZeta_eq_zero_re : RiemannZetaZerosOnLine := rhOfAll
theorem LFunction_ne_zero_of_half_lt_re : DirichletLNonvanishingRightOfHalf := allChi
theorem LFunction_eq_zero_re : DirichletLZerosOnLine := claimAll.2.1
theorem LFunction_eq_zero_re_of_isPrimitive : PrimitiveDirichletLZerosOnLine := critAll
```

其中 `RiemannHypothesis` 是 **Mathlib 自己的定义**（README 引 `Mathlib/NumberTheory/LSeries/RiemannZeta.lean`）：

```lean
def RiemannHypothesis : Prop :=
  ∀ (s : ℂ) (_ : riemannZeta s = 0) (_ : ¬∃ n : ℕ, s = -2 * (n + 1)) (_ : s ≠ 1), s.re = 1 / 2
```

`src/Supplements/Kernels/MainTheorems.lean`（全文，桥接层）：

```lean
theorem allChi : UpperTheory.EveryCharacter := UpperTheory.FinalTheorems.everyCharacter
theorem rhOfAll : RiemannHypothesis := Formalism.VW.rh_of_every allChi
theorem critAll (N : ℕ) [NeZero N] (χ : DirichletCharacter ℂ N) (hχ : χ.IsPrimitive) (s : ℂ)
    (h0 : 0 < s.re) (h1 : s.re < 1) (hz : LFunction χ s = 0) : s.re = 1 / 2 :=
  Formalism.VW.critLine allChi N χ hχ s h0 h1 hz
theorem claimAll : Claim.HalfPlane ∧ Claim.Strip ∧ Claim.Zeta :=
  ⟨allChi, Claim.strip allChi, Claim.zeta allChi⟩
```

关键点（前次 digest 已核实，此处重申）：
- **【事实】** "GRH" 指 **Dirichlet L 函数**（所有模 N、所有特征标），不是 GL(n) 自守 L 的 GRH，也不是 ERH。
- **【事实】** `UpperTheory.EveryCharacter` 与 `DirichletLNonvanishingRightOfHalf` 字面同构；证明链：`Main → Formalism.VW.rh_of_every`（由非零半平面 + 函数方程得 RH）与 `Formalism.VW.critLine`；GRH 的硬核是 `UpperTheory.FinalTheorems.everyCharacter`，最终依赖 `galoisLocalGlobalStrong_recParameter ← galoisRepresentations_of_thetaLift UpperTheory.TP.K.tLiftK`（θ 提升链）。
- **【事实】** 最终定理**只有定性/非零性内容**：没有任何素数计数或 L 函数值的显式常数界出现在顶层结论里。

---

## 3. `ChebyshevGrowthImpliesZeroFree` 型接口：精确定义与可用性

**【事实】** 文件：`src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/ExplicitFormulaErrorOfHostConditions.lean`

```lean
structure Level extends KSet where
  o : ℕ                    -- level 序号（"tower" 的层）
namespace Level
def Nt (Λ) : Finset PChar := Λ.KEPT.erase PChar.one
def wt (Λ) (ψ : PChar) : ℝ := if Λ.psK = some ψ then 1 else (3 * (Λ.o : ℝ) + 1)⁻¹
def Gm (Λ) (y : ℝ) : ℝ := Formalism.Gz y + ∑ ψ ∈ Λ.Nt, Λ.wt ψ * (An.gChi ψ.χ y).re

def ChebyshevGrowthImpliesZeroFree : Prop :=
  ∀ θ : ℝ, 0 < θ → θ < 1 → ∀ y0 : ℝ,
    (∀ y ≥ y0, Λ.Gm y ≤ y ^ θ) → Λ.ZeroFreeAbove θ
```

其中（【事实】`Formalism/StatementOC.lean:13`、`.../TotientGaloisClasses/Analytic.lean:14–25`）：
- `Gz y = Sz y − y·log y + (1+γ)·y`，`Sz y = ∑_{n≤y} Λ(n)·(y/n − 1)`（即 remark.pdf item 5 的 Λ 和）；
- `gChi χ y = if χ=1 then G y else ∑_{n≤y} Λ(n)χ(n)(y/n−1)_+ + y·(L'/L)(χ,1)`，
  `G y = ∑_{n≤y} Λ(n)(y/n−1)_+ − y(log y − 1 − γ)`（**注意：χ≠1 时显式用到 `logDerivativeAtOne χ = L'(χ,1)/L(χ,1)`**）。

**【事实】这个接口不是无条件定量估计，而是一个"条件归约"**：`ChebyshevGrowthImpliesZeroFree` 接收"增长假设 `∀y≥y0, Gm y ≤ y^θ`"（**常数/起点全是存在量词**，非显式），输出零无区。实际证明链把它"兑现"为：
- `ZeroFreeAllOfTopG.lean:26` `zeroFreeAll_of_topG` ← `zeroFreeOn_of_tiedWin_cyc` ← `UpperTheory.Comparison₂.level_gm_le_on_family_scales`
- `PrimitiveCosets/LevelGmLeOnFamilyScales.lean:28`：`level_gm_le_on_family_scales (Λ) : ChebyshevInequalityOnWindows …` ← `windowInequality_of_artinInputs`（**即由 Artin/自守大机器提供**，不是从显式公式的显式常数推出）。

**【推测】** 因此该接口**不能**为你提供可直接引用的显式常数/一致定量界：它是一个**渐近存在性**归约（∃C, ∃y0），其"增长假设"由 17.4M 行大机器内部证明，常数不可读、不可提取作 Goldbach 计算。

**【事实】** ζ 版本同类接口：`Formalism/ZetaNonvanishingChebyshevWeights.lean` 定义 `ZetaLandauCheb`、`ZetaLandauChebEps`、`ZetaNonvanishingChebyshevWeights`（Chebyshev 权重平均 `chebyshevWeightedAverage` 满足 `s₀·Gcheb x ≤ C x^{θ+ε}` 型假设 ⇒ Re>θ 无零点）；`Formalism/ZeroFreeRegion/Statement.lean` 定义 `ZeroFreeRegion`、`LogDerivRegion`、`GzPNT`（ζ 的经典定量零无区/PNT 误差形式）。

---

## 4. 仓库中确有内容的定量解析数论接口（【事实】清单）

> 判断"已证"依据：找到 `theorem X : Prop` 的具体证明项（非仅 `def X : Prop`）。

| # | 文件（行） | 类型签名要点 | 已证？ |
|---|---|---|---|
| 4.1 | `Formalism/PeriodIntegrals/ExplicitFormula.lean` | `ExplicitFormulaWith C := ∀ N χ primitive, ∀ u T (2≤T≤u): (ZerosBelow χ T).Finite ∧ ‖psi0 χ u + ∑_{ρ∈ZerosBelow χ T} ord(ρ)·u^ρ/ρ‖ ≤ C·(u·log(NuT)²/T + log(Nu) + ∑_{ρ≤1} ord(ρ)/‖ρ‖)`；`ExplicitFormula := ∃C>0, ExplicitFormulaWith C` | **是**：`Formalism/PeriodIntegrals/ExplicitFormulaCounts/ExplicitFormula.lean` `theorem explicitFormula_closed : PI.ExplicitFormula` |
| 4.2 | `Development/.../GlobalInterpolation/ExplicitFormulaDirichletZerosRightHalfStatement.lean` | `GlobalTheory.T.explicit_formula_dirichlet_zeros_right_half : ∃C>0 ∀q χ u T (2≤T≤u): ‖∑_{n≤u}Λ(n)χ(n) − (χ=1? u:0) + ∑_{ρ∈zerosBox χ (1/2) T} ord·u^ρ/ρ‖ ≤ C·(u/T + √u·q³)·log²(q u T)` | **是**（`first | exact ... ExplicitFormulaRight.explicit_formula_right`）；**这是 GRH 强度**的 ψ(x,χ) 显式公式（取 T=u 得 √u·q³ 级误差） |
| 4.3 | `Formalism/LandauZeroFreeBounds/SiegelWalfiszAP.lean` | `SiegelWalfisz`, `SiegelWalfiszAP`: ∀A>0 ∃c,C>0 ∀q≤log^A x: \|ψ(x,χ)−(χ=1?x:0)\| ≤ C·x·e^{−c√log x}；`psiAP` 版 \|ψAP(q,a,x)−x/φ(q)\| 同型；`PsiChiBound`（含例外零点项，模 q≤e^{c√log x}） | **是**：`SiegelWalfiszAPOfSiegelLower.lean:23 psiChiBound`、`:29 siegelWalfisz_of_siegelLower`、`:34 siegelWalfisz`；`FinalSiegel.lean:25 siegelLower`（Siegel 下界，由积性特征/实特征构造证明） |
| 4.4 | `Formalism/LandauZeroFreeBounds/Statement.lean` | `ZFRDirichlet`：Dirichlet L 的定量零无区（含例外零点 χ²=1、实、单零点结构） | 定义；证明链在 `NoZeroComplexOf.lean` 等（未逐一追，标注**未完全核实**） |
| 4.5 | `Formalism/LandauZeroFreeBounds/LogDerivRegionChiOf.lean` | `LogDerivRegionChi : ∀c₁∈(0,1/20] ∃C ∀q χ B(例外零点集), ∀s∈InRegion(c₁/2,q): ‖−L'/L(χ,s) + ∑_{β∈B} 1/(s−β)‖ ≤ C·log²(q(|Im s|+2))` | **是**：`SiegelWalfiszAPOfSiegelLower.lean:17 theorem logDerivRegionChi` —— **全 q、全 χ 一致的 L'/L 定量界（零无区内）** |
| 4.6 | `Formalism/ZeroFreeRegion/Statement.lean` | `ZeroFreeRegion`（ζ 的 1−c/log(|t|+2) 区域）、`LogDerivRegion`（ζ'/ζ 的 log² 界）、`GzPNT`（\|Gz y\| ≤ K y e^{−c√log y}） | 定义 + `LogDerivRegionOf`/`GzPNTOf` 归约定理（`SmallHeightLogDeriv.lean`）；部分已证 |
| 4.7 | `Development/.../PublishedTheorems/AutomorphicForms₂/LogDerOne.lean:12` | `LogDerOne : ∃C ∀q>1,χ primitive: ‖L'(χ,1)/L(χ,1) − Σ_ρ 1/(1−ρ)‖ ≤ C·log(3q)` | **是**（`GlobalTheory.LogDerOneProof.logDerOne_holds`，前次 digest 已见 `logDerivOne (O) := …_holds`） |
| 4.8 | `Formalism/GL3MeanSquares/PrimeCountAsymptoticInProgressions.lean` | `PNTAPRelW`（相对误差 PNT in AP，含例外零点）、`LogDerivSeries`（Σ Λ(n)χ(n)/n → −L'/L(χ,1)）、`MeanSquareHypW`（Jacobi 特征和的二阶矩） | **是**：`PNTBridge.lean:9 pnt_progressions_relative_weak`，`MSqMain.lean:55 meanSquareHypW_of_pnt` 等 |
| 4.9 | `Formalism/TwistFamilyExistence/Statement.lean:55–90` | `WeightMoments`（扭转族上 Σ_d ‖L(χ_d,1)·GT‖² 与 Σ_d ‖L(χ_d,1)·Mo − 1‖² 的二阶矩上界）；`WeightPrimeCor`（在特征标族上"鸽笼"挑 d，使 ∀ψ∈Ps：L(χ_ψ d)≠0、‖L'/L‖≤2C²log²D log y0、GT 受控） | **否**：该目录只有 `Statement.lean` 一个文件；全树 grep 显示 `WeightMoments`/`WeightPrimeCor`/`TwistFamilyExists` **除定义外无任何引用、无证明** → 死代码/脚手架 |
| 4.10 | `Formalism/SharpRestriction/.../Analytic.lean:145–160` | `ChebyshevCharacterBound`（∀χ induced：‖gChi χ y‖ ≤ y·e^{−c x^{ε/8}}，y≥e^{x^{ε/3}}/3）、`LogDerivativeBound`（对 kept χ：‖L'(χ,1)/L(χ,1)‖≤x^ε；对 bounded χ ≤ C log X）、`BoundedCharsPointwise` | 定义（作为 `HostConditions` 结构字段在零无区证明中作假设用） |
| 4.11 | `Formalism/HermitianCurvature/**`（1,922 文件） | 内部表示论/Fourier 衰减核命题，如 `StatementA.LevelOneKernelPoint`（关于 `BB` 双陪集核非零 ⇒ 线性泛函取值），**无数论统计陈述** | — |
| 4.12 | `PositivityTheory/**`（449 文件） | 445/449 是 `AutomorphicForms/PublishedInputs/**`（Galois 表示/局部 Langlands 输入），**不是** Weil 正性/矩分析 | — |

补充（【事实】）：`Formalism/LandauZeroFreeBounds/` 还有 `SiegelWalfiszAPOf.lean`、`NoZeroComplex.lean`、`ExceptionalZeroBounds/*`（例外零点、Landau 局部化、`ChebyshevCharacterExplicitGeneral.lean` 等）——都是**经典零无区/Siegel–Walfisz 机器**。

---

## 4b. 补充（重要）：`Formalism/LFunctionBounds/` —— 特征标族（跨特征标求和）工具包

**【事实】** 这一目录是仓库中与"跨特征标"最相关的定量包（也是 remark.pdf 里 Stepanov/"Iwasawa tower"/"extra averaging over characters" 的技术实现层之一）：

`Formalism/LFunctionBounds/PositivityBound.lean`（【事实】类型签名）：
- `PolyaVinogradov`：`∃K ∀ prime l, χ≠1, ∀M,N: ‖Σ_{n∈[M,M+N)} χ(n)‖ ≤ K·√l·(1+log l)`（经典 Pólya–Vinogradov 特征和不等式）。
- `CharOrtho`：`∀ b Y: Σ_{χ∈allChars l} ‖Σ_{n∈Ioc Y l} b n χ(n)‖² ≤ (l−1)·Σ_{n} ‖b n‖²`（特征标正交性，显式常数）。
- `ParsevalHolder`：对任意特征标子集 `BB` 与系数 `a`：`‖Σ_{x≤X} Σ_{χ∈BB} a χ·χ(x)‖² ≤ (Σ_{x∈Ioo 0 l} ‖Σ_{χ∈BB} a χ χ(x)‖²)/(l−1) · √|BB| · √(Σ_{χ∈BB} ‖IX χ X‖⁴)`（显式 Parseval/Cauchy–Schwarz；这是**跨特征标**的二次型不等式）。
- `M4`：`∀ε>0 ∃C ∀ prime l, X≤l: Σ_{χ∈allChars\{1}} ‖IX χ X‖⁴ ≤ C·l^{1+ε}·X²`（对**全体非主特征标**的四阶矩）。**【事实】已证**：`Development/WeilBound/RepresentationTheoryGL/ArchimedeanBaseChange/ArchimedeanBaseChangeProof/SatakeExponents/UniformizerValuations/AdelicHeckeBlocks/MatchAll.lean:26 theorem hM4 : M4`（及 `.../TwistedConjugationNorms/Development.lean:1166 theorem m4 : M4`）。
- `LPartialSum`：`∀q χ≠1 (∀M ‖Σ_{n≤M}χ(n)‖≤B) s N: ‖L(χ,s) − Σ_{n≤N} χ(n)n^{−s}‖ ≤ 2B(1+‖s‖/Re s)N^{−Re s}`。**【事实】已证**：`Formalism/LFunctionBounds/LFunctionBoundsProofs/LPartialSum.lean:136 theorem l_function_partial_sum : LPartialSum`。
- 另有 `SubMeanDisc`（次均值不等式）、`DivisorBound`、`LConj`（L(χ⁻¹, s̄) = conj L(χ,s)）、`AlAsymp`、`LogDerivZeroOdd`（奇特征标在 s=0 的 L'/L 与逆特征标在 s=1 的 L'/L 的关系）、`PositivityBound`（一个带 `triples l` 正权重的正性/三线性不等式）。

`Formalism/LFunctionBounds/Statement.lean`（【事实】类型签名）：
- `triples l`（和为 l 的正整数三元组）、`IsProb`（三元组上的概率权重 ν）、`W`/`Snu`/`cW`（权重的 Weil 型特征标变换）、`PeriodIdentity`（对奇特征标族的周期恒等式 + 权重和 =1 + L'/L(χ⁻¹,1) 的线性关系）。
- `KillingLemma`：`∀ε>0 ∃l₀ ∀ prime l≥l₀, ∀BB⊆oddChars l, BB 对取逆封闭, |BB| ≤ l^{1−ε} ⇒ ∃ 概率 ν 使 ∀χ∈BB: cW(l,ν,χ)=0` —— **在特征标族上"消去/平均"任意足够小的子集**的线性代数工具（正是"extra averaging over characters"/零密度论证的骨架）。
- `Density` / `DensityRect`：**特征标族零密度**：`∀θ∈(1/2,1) ∃δ>0 ∀T≥1,k ∃C ∀ prime l, Z 有限集(|Z|≤k, 实部≥θ, |Im|≤T): #(在 Z 或该区域内为零的特征标) ≤ C·l^{1−δ}`。
- `FixedLPointwise`：在固定素数模 l 下、对 `cW` 加权核的点态/一致估计（用于把 L 值在 l 处的行为转化为对 Λ 和的控制）。

**证明状态（诚实标注）**：`M4`、`LPartialSum` 已找到证明项（见上）；`PolyaVinogradov`、`Density`、`KillingLemma`、`PositivityBound`、`PeriodIdentity` 我只在 `Prop` 定义层读到，**未逐一追到证明项**（可能在 `Development/.../PrimitiveCosets/`、`Development/WeilBound/` 等大机器的其他文件里被证）。

**【推测】对 LL Hypothesis R 的意义**：这是仓库中**唯一**接近"跨特征标平均"的可借鉴工具箱——`CharOrtho`/`ParsevalHolder`/`M4` 给出显式的跨特征标二次型/矩不等式，`KillingLemma` 给出族上"消权重"的线性代数模式，`Density` 给出族零密度。但注意：(i) 对象是**特征和/L 值/零点计数**，不是 L'/L 在谱点上的相关核；(ii) 多按**素数模 l** 与 `triples l` 的特定结构编码（Stepanov 型构造），不是一般模/一般谱点。若 Hypothesis R 的核可写成"特征标族上的二次型 + 显式 Parseval"，此处可能是最接近可改造的素材（**推测**，需要具体核形式才能判断）。

## 5. 跨特征标 L'/L 相关：明确"没有"（负结论 + 证据）

**【事实】负结论**：仓库不存在以下任何对象（无定义、无定理）：
- 两个不同特征标 χ₁, χ₂ 的 L'/L 值之间的相关/双线性/核；
- 对特征标族的 (L'/L)(χ,ρ₁)·(L'/L)(χ,ρ₂) 求和或二阶矩（除了 4.9 死代码的 s=1、特殊扭转族版本）；
- 素数对相关（p, p+h）、pair correlation、Montgomery 对相关、Katz–Sarnak 密度、n-level 密度、随机矩阵统计；
- "cross-character"、"correlation"、"pair"（作为素数对/谱对含义）的任何字面命中。

**【事实】最接近的 4 个对象**（都不满足 Hypothesis R 的需要）：
1. `LogDerivRegionChi`（4.5）：**单**特征标、零无区内（Re ≥ 1−c/log(q(|t|+2))）的 L'/L 上界；不覆盖临界线/零点附近，也不是跨特征标。
2. `LogDerOne`（4.7）：**单**特征标、**s=1 一点**的 L'/L 界；与高 zeta 零点无关。
3. `WeightMoments`/`WeightPrimeCor`（4.9）：唯一带"特征标族平均 + L'/L"字样的对象——但是 (i) 只有定义无证明无引用；(ii) 限于 s=1 与人工扭转族（d·q，Jacobi 符号）；(iii) 给的是**存在某 d** 的逐 ψ 控制，不是相关性估计。
4. `MeanSquareHypW`（4.8）：素数 q 上 Jacobi 特征和的**二阶矩**——是"特征和平方平均"，不是 L'/L 相关；用途是内部 Stepanov 型构造。

**【推测】对 LL Hypothesis R 的可借鉴性**：只能借鉴**证明技术模板**，不能借用结论：
- 模板 A：显式公式 + uniform-in-conductor 误差（4.1/4.2）——若 Hypothesis R 的核可用显式公式展开，可参考其误差形状与 q-依赖（注意 4.2 有 q³ 损失）。
- 模板 B：零无区内单特征标 L'/L 的 log² 一致界（4.5）——只在远离临界线处有效。
- 模板 C：**族平均二阶矩 + 鸽笼挑元素**（4.9 的骨架、4.8 的实例）——这是最像"用平均控制单个坏对象"的技术，但对象、点、常数都需重新设计。
- 模板 D：Chebyshev 增长→零无区（§3）——是归约，不是定量输入。
**明确**：以上没有任何一条直接给出 `‖T_N‖ ≤ δ_N` 或 `N^{-1/2}` 级跨特征相关界。

---

## 6. Goldbach / 加性数论：确认"没有"（【事实】）

- `goldbach`（任意大小写、含注释）全树 **0 命中**；`sum of two primes`、`binary goldbach`、`goldbach conjecture` 0。
- `twin prime`、`prime pair`（作为孪生素数含义）0；唯一 "PrimePair"/"GoodPrimePair" 命中（`Formalism/GL3MeanSquares/PrimePairOfPrimeNumberTheoremInProgressions.lean`、`Formalism/SizeWindowBrackets/SmoothedRemainderRealIntegralFormula.lean:50 ExistsSplitGoodPrimePair`）含义是**构造扭转族用的一对素数 (q₁,d)**（`SplitsIn`、`IsExcPair` 等），**不是**孪生素数/素数对相关。
- `Chen`（整词）0；`Vinogradov` 的 1 个命中是 `Formalism/LFunctionBounds/PositivityBound.lean:58 def PolyaVinogradov`（**Pólya–Vinogradov 特征和不等式**，乘性数论工具，不是 Vinogradov 三素数定理/加性结果）；`circle method`、`major arc`、`minor arc`、`exceptional set`、`additive combinatorics`、`sumset`（11 命中全是 `TsumSetIntegral` 之类求和集积分）——均**无 Goldbach/加性定理陈述**。
- 结论：仓库**没有任何可转用于哥德巴赫的加性结论**；它的数论结论全部是乘性 L 函数/素数分布方向的。

---

## 7. 局限与提醒（诚实标注）

1. **【推测/局限】** grep 负结论受"生成式命名"限制：仓库几乎无 docstring，很多内容藏在 `Green`、`DesignS`、`gChi` 这类名字后面；理论上存在"内容是相关型但名字不含相关词"的可能。但：(i) 本次对 `correlation/pair/twin/Goldbach/second moment/mollifier` 等语义词做了全树大小写不敏感扫描；(ii) 4.9 的 `WeightMoments` 说明作者若真做了族平均/矩，会在类型里出现 `∑ ‖·‖²` 结构——我在全树只找到 4.8/4.9 两处此类结构，且都不适用。
2. **【事实】** 本报告的"已证"判断基于找到证明项/证明定理，并非完整依赖图追踪；4.4（ZFRDirichlet）等少数标"未完全核实"。
3. **【事实】** 仓库 17.4M 行中绝大部分与本文问题无关（θ 提升/Iwasawa/自守表示/代数几何机器）；本次只抽取了与"定量解析数论/相关/加性"直接相关的 ~10 个接口。
4. **【推测】** 即使 Alpöge 的 GRH 为真，也不提供比"GRH 本身"更多的素数分布信息：其顶层定理只是**非零性/零点在线上**，最终论证没有输出显式误差常数；顶层结论里没有任何 `π(x)`/`ψ(x)`/素数对估计。

---

## 8. 给 lead 的 6 条要点

1. **【事实】Alpöge 仓库没有 Goldbach/加性内容**（`goldbach`、`sum of two primes`、twin/prime-pair 相关、circle method、sieve 定理：0 命中）。
2. **【事实】没有跨特征标 L'/L 相关核，也没有 pair-correlation**（`correlation`、`pair correlation`、`katz-sarnak`、`montgomery`、`n-level`、`second moment`、`Weil positivity`：0 实质命中；`Weil`/`Katz`/`mollifier`/`sieve` 命中均为假阳性，已抽样排除）。最接近"跨特征标"的是 `Formalism/LFunctionBounds/` 的**特征和/族平均工具**（Pólya–Vinogradov、`CharOrtho`、显式 `ParsevalHolder`、`M4` 四阶矩已证、`KillingLemma` 族平均消去、`Density/DensityRect` 族零密度）——是**特征和/平均**，不是 L'/L 相关核。
3. **【事实】但仓库有一批正宗经典定量解析数论接口（已证）**：带 C(u log²/T + …) 误差的显式公式 `PI.ExplicitFormula`；**GRH 强度**的 ψ(x,χ) 显式公式 `explicit_formula_dirichlet_zeros_right_half`（误差 C(u/T + √u·q³)log²）；**Siegel–Walfisz 及 ψAP/ψχ 一致定量界**（`siegelWalfisz`、`siegelWalfiszAP`、`psiChiBound`，已由 Siegel 下界证出）；**零无区内一致 L'/L 界** `LogDerivRegionChi: ‖−L'/L+Σ1/(s−β)‖ ≤ C log²(q(|t|+2))`（已证）；s=1 的 `LogDerOne`（已证）。
4. **【事实】`ChebyshevGrowthImpliesZeroFree` 是渐近存在性归约，不是显式定量界**：`∀θ∈(0,1), ∀y0, (∀y≥y0, Gm y ≤ y^θ) ⇒ ZeroFreeAbove θ`，其中 `Gm y = Gz y + Σ_{ψ∈KEPT} wt(ψ)·Re gChi(ψ,y)`，`wt=(3o+1)⁻¹`，`gChi` 含 Λ 和与 L'/L(χ,1)；其增长假设由 `level_gm_le_on_family_scales ← windowInequality_of_artinInputs`（大机器）兑现，常数不可提取。ζ 版在 `Formalism/ZetaNonvanishingChebyshevWeights.lean`。
5. **【事实】唯一"族平均+鸽笼+L'/L"骨架是死代码**：`Formalism/TwistFamilyExistence/Statement.lean`（`WeightMoments`、`WeightPrimeCor`、`TwistFamilyExists`）只有定义，全树无证明无引用；另外 `MeanSquareHypW` 是 Jacobi 特征和二阶矩（内部 Stepanov 机器），均**不能**给出 `‖T_N‖≤δ_N` 型跨特征相关界。→【推测】Hypothesis R 只能借鉴技术模板（显式公式误差、零无区 L'/L 界、族平均+鸽笼），不能借用结论。
6. **【事实】顶层定理陈述**：`riemannHypothesis : Mathlib.RiemannHypothesis`（Mathlib 定义，ζ 非平凡零点 Re=1/2）、`DirichletLNonvanishingRightOfHalf`（所有模/所有 χ，Re>1/2 非零）、`DirichletLZerosOnLine`、`PrimitiveDirichletLZerosOnLine`；"GRH"=Dirichlet L only，非 GL(n)/ERH；最终结论是定性非零性，无素数分布定量输出。**可用性结论：对 Goldbach 直接无用，对 LL 的 Hypothesis R 无现成可复用引理。**
