# Phase-6 定量扫描：Alpöge/Claude RH Lean 仓库里有没有可用于 LL Hypothesis R 的定量内容？

**执行者**：proof-digest · **日期**：2026-11-21 · **时间盒**：45 分钟
**对象**：`/home/kiler/rh-full`（git `7cbf7a0c3`，175,187 个 `.lean`，17,374,215 行；**只读**，未修改）
**方法**：全树 `grep -r`（大小写不敏感）+ 读取命中文件的确切类型签名（不读证明体）；对关键 `Prop` 追查是否有证明项（`theorem ... : Prop := ...`）并检查关键目录无 `sorry`/`axiom`。**【事实】**=直接读到的文件内容/命令输出；**【推测】**=我的判断。
**背景**：我们缺 LL Hypothesis R 所需的**跨特征标 L'/L 族相关估计**（‖T_N‖ ≤ δ_N，N^{-1/2} 级）。本扫描找它能提供的定量素材。

---

## 0. 裁决（TL;DR，残酷诚实）

| 问题 | 裁决 | 依据 |
|---|---|---|
| (a) 能否给出**优于 (log N)²** 的 ‖T_N‖ 显式界？ | **不能（没有）** | 仓库里唯一成型的 L'/L 定量界是**零无区内单特征标**的 `log²` 型界 `LogDerivRegionChi`（C·log²(q(|t|+2))，**正是 (log)² 量级、无改进**，且常数 ∃C 不可读、只在 Re ≥ 1−c/log 区域有效）。没有任何跨特征标相关核、也没有把 `C log²` 改进的机制。 |
| (b) 能否给跨特征 L'/L 二阶/四阶矩？ | **不能（没有）** | 仓库有**跨特征标/族**的**特征和**二阶矩/四阶矩与大筛（有显式常数），但都是**特征和**（|Σa_nχ(n)|²、I_Xχ 的四阶矩），**不是 L'/L 值**的矩。唯一带"族平均 + L'/L"字样的 `WeightMoments`（s=1 扭转族二阶矩）是**死代码**（无证明、无引用）。 |
| (c) 能否给 level-aspect pair correlation？ | **不能（没有）** | 全树无 `pair correlation`/`Montgomery`/`Katz–Sarnak`/`n-level`/`random matrix`/`second moment` 对象（0 命中）。只有零点密度、零点 repulsion、零点间距计数（`Spacing`/`Triv`/`Offdiag`），是零密度证明的内部构件，**不是** Montgomery 型 pair correlation（无 Fourier/对相关核）。 |

**但是**：仓库确实包含一批**已证、带明确类型的定量解析数论机器**（多数是对经典文献的形式化），包括：**具有显式常数的乘性大筛/算术大筛**、**log-free 零点密度（族 summed over all χ mod q）**、**Deuring–Heilbronn 型零点 repulsion**、**族求和型 ψ 误差（Σ over all χ）**、**显式公式 + 单位区间零点计数**、**Siegel–Walfisz（含常数形态但无效）**，以及零密度证明中的**显式常数小引理**。这些对理解"族层面的定量控制"有用，但按上面的裁决**不能直接补上 Hypothesis R**。

---

## 1. 零点密度 / repulsion / S(t,χ)

### 1.1 【事实】log-free 零点密度（族：对模 q 的全部特征标求和）——已证

`Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/LogFreeZeroDensityDirichletOneModulusStatement.lean:8`

```lean
theorem _root_.GlobalTheory.T.logFree_zeroDensity_dirichlet_one_modulus :
  ∃ A C η : ℝ, 0 < A ∧ 0 < C ∧ 0 < η ∧
  ∀ (q : ℕ) [NeZero q] (T σ : ℝ), 2 ≤ T → 1 - η ≤ σ → σ ≤ 1 →
    ∑ χ : DirichletCharacter ℂ q,
      (∑ᶠ ρ ∈ zerosBox χ σ T, (ord χ ρ : ℝ))
      ≤ C * ((q : ℝ) * T) ^ (A * (1 - σ))
```

- **证明**：`first | exact @GlobalTheory.Lin.LogFree.zero_density | ...`（同文件），即证明在 `Development/.../GlobalInterpolation/LogFreeZeroDensityDirichletOneModulus.lean` 的 `GlobalTheory.Lin.LogFree.zero_density`。**【事实】已证**（无 `sorry`；该目录扫描未见 sorry/axiom）。
- 形态：**log-free**（右端纯幂 `(qT)^{A(1−σ)}`，无 log 因子），**族求和**（Σ over 所有 χ mod q，且零点按重数 `ord` 计），对 q 一致（A,C,η 与 q 无关）。
- **但**：A,C,η 是 **∃ 量词、无数值**；"one modulus"= 固定 q 的族（对 q 一致，但不求和 over 不同模数）。

### 1.2 【事实】Deuring–Heilbronn 型零点 repulsion —— 已证

`Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/RepulsionStatement.lean:8`

```lean
theorem _root_.GlobalTheory.T.one_sub_re_ge_of_exceptional_zero_repulsion :
  ∃ c : ℝ, 0 < c ∧
  ∀ (q : ℕ) [NeZero q] (χ₁ χ : DirichletCharacter ℂ q) (β L : ℝ) (ρ : ℂ),
    χ₁ ≠ 1 → χ₁ ^ 2 = 1 → β < 1 → 1 / 2 ≤ β → LFunction χ₁ β = 0 →
    LFunction χ ρ = 0 → 1 / 2 ≤ ρ.re → ρ.re < 1 →
    (χ ≠ χ₁ ∨ ρ ≠ β ∨ 2 ≤ ord χ₁ β) →
    Real.log (q * (|ρ.im| + 2)) ≤ L →
    c * Real.log (c / ((1 - β) * L)) / L ≤ 1 - ρ.re
```

- **已证**：`exact @GlobalTheory.Lin.Repulsion.repulsion`（证明在 `.../GlobalInterpolation/Repulsion.lean`）。
- 含义：存在实非主特征标 χ₁ 在 β∈[1/2,1) 有例外零点时，**任意**其他零点 ρ 满足 `1−Reρ ≥ c·log(c/((1−β)L))/L` —— 这正是 Deuring–Heilbronn **repulsion** 的形式化（常数 c 是 ∃ 量词）。
- 另有更强的工程版：`Formalism/GL3MeanSquares/.../PNTDHBSt.lean:11 def DeuringHeilbronnMB`（∃c₀c₁c₂,B，带 `1−c₁/log(MT) < β₁` 与 `c₂·log(c₁/((1−β₁)log(MT)^B))/log(MT) ≤ 1−ρ.re`），**已证** `deuringHeilbronnMB_proof' : DeuringHeilbronnMB`（`PNTFinal.lean:20`，`= deuring_heilbronn_lossy`）。

### 1.3 【事实】零点密度辅助结构（供 log-free 密度证明）—— 已证，部分带显式常数

`Formalism/GL3MeanSquares/GenusMeanAsymptotics/JacobiCharacterSums/`：

| 文件:行 | 定义 | 已证 |
|---|---|---|
| `DeuringHeilbronnM.lean:77` | `LogDensityM`（字符×零点集合的对数密度上界：`∃A B C, ∀M,T,σ,S` …） | **是**：`PNTFinal.lean:18 logDensityM_proof' : LogDensityM := Dens.log_density_bound` |
| `PNTDensPair.lean:106` | `PairCross`：`‖Σ_{n∈(U,2U]} ψ(n)n^{−w}‖ ≤ 4(M+1)(1+‖w‖)`（单特征标部分和，**显式常数 4**） | **是** |
| `PNTDensPair.lean:231` | `PairSame`：主特征标情形，`≤ 4U^{1−Re w}/|Im w| + 4(M+1)(1+‖w‖)` | **是** |
| `PNTDensSpace.lean:140` | `Triv`：零点集合计数 `|S| ≤ M(2T+1)` | **是** |
| `PNTDensSpace.lean:60` | `Spacing`：零间距计数 `Σ_{x∈P\{t}} 1/|t−x| ≤ 2(1+log(2T+1))`（**显式常数 2**） | **是** |
| `PNTDensBlock.lean:108` | `Offdiag`：**跨特征标对**的和：`Σ_{p'∈S} ‖Σ_{n∈(U,2U]} p.1(n)·conj(p'.1(n))·n^{−((p.2−σ)+conj(p'.2−σ))}‖ ≤ U(9+8log(2T+1)) + |S|·8(M+1)(2+2T)` | **是** |
| `PNTDensBlock.lean:164` | `BlockCnt`（dyadic 块计数） | **是** |
| `PNTDensSt.lean` | `DivSq`、`CoefficientBlockBound`、`CoefficientBlock` 等 | 定义（部分已证） |

**【事实】** `Offdiag` 是仓库中**最接近"跨特征标相关"**的定量对象：它把两个特征标 χ_p, χ_{p'} 的乘积（相对特征标）的短区间和与零点对绑定，常数显式（9, 8, 2）。**但**它是零密度证明的中间步骤（对 `n` 的 Dirichlet 多项式乘积求和），**不是 L'/L 的相关核**，也不含 pair correlation 的 Fourier 变换。

### 1.4 【事实】S(t,χ)=arg L(1/2+it,χ) 的界：**没有找到**

搜索 `argument principle`、`winding`、`funcArg`、`argOf`、`Sfun`、`Complex.arg` 与 `LFunction` 组合：无相关定义/定理（命中均为无关文件，如 Skoda/Weil 表示/双陪集核）。**【推测】** 该仓库的零密度证明**绕过了 S(t,χ)**：直接用显式公式 + 大筛 + 零点计数（§1.3）处理零点求和，因此没有独立的 `S(t,χ)` 上界接口。

替代物（已证）：`ExplicitS`（`DeuringHeilbronnM.lean`，证明 `PNTExplMain.lean:15 smoothed_explicit_formula : ExplicitS`）给出**单位区间零点计数**：
`Σ_{ρ∈Z, |Im ρ−t|≤1} m(ρ) ≤ C·log(M(|t|+2))`（**显式 log 形**，C 是 ∃），以及显式公式误差 `≤ C·[((MT)^C·y^{−κ/2}) + log y·log²(MT)/T]`。

---

## 2. `SiegelWalfisz` 及其常数

### 2.1 类型签名（【事实】）

`Formalism/LandauZeroFreeBounds/SiegelWalfiszAP.lean`：

```lean
def psiChi (q) (χ) (x) : ℂ := ∑_{n≤x} Λ(n)·χ(n)
def psiAP (q a x) : ℝ := ∑_{n≤x, n≡a mod q} Λ(n)
def ExcZeros (c₁) (χ) (B) : Prop := ...（例外零点集：|B|≤1，B 中元素为 Re≥1−c₁/log(q(|t|+2)) 的非主实特征标零点）

def PsiChiBound : Prop :=
  ∀ c₁, 0<c₁ → c₁≤1/20 → ∃ c C, 0<c ∧
    ∀ q χ B x, ExcZeros c₁ χ B → 2≤x → q ≤ exp(c√log x) →
      ‖psiChi χ x − (χ=1?x:0) + ∑_{β∈B} x^β/β‖ ≤ C·x·exp(−c√log x)

def SiegelWalfisz : Prop :=
  ∀ A>0, ∃ c C, 0<c ∧ ∀ q χ x, 2≤x → q ≤ (log x)^A →
    ‖psiChi χ x − (χ=1?x:0)‖ ≤ C·x·exp(−c√log x)

def SiegelWalfiszAP : Prop :=
  ∀ A>0, ∃ c C, 0<c ∧ ∀ q a x, 1≤q, (a,q)=1, 2≤x → q ≤ (log x)^A →
    |psiAP q a x − x/φ(q)| ≤ C·x·exp(−c√log x)
```

**【事实】已证**：`SiegelWalfiszAPOfSiegelLower.lean:23 theorem psiChiBound : PsiChiBound`、`:29 theorem siegelWalfisz_of_siegelLower (hS : SiegelLower) : SiegelWalfisz`、`:34 theorem siegelWalfisz : SiegelWalfisz := siegelWalfisz_of_siegelLower siegelLower`；`FinalSiegel.lean:25 theorem siegelLower : SiegelLower`（经 `siegel_theorem_of ...`）。

### 2.2 是否显式/有效？（【事实】+【推测】）

- **类型上：常数是 ∃c, ∃C，没有数值**；`SiegelLower` 定义为 `∀ε>0, ∃c>0, ∀q χ (χ²=1,χ≠1): c·q^{−ε} ≤ ‖L(χ,1)‖` —— 这是 **Siegel 定理**的形态。Siegel 定理在经典数论中是**无效的（ineffective）**：常数存在但不可计算、无显式算法。**【推测】** 因此 `SiegelWalfisz` 的 c,C 同样**不可数值提取**，不是"显式有效界"；它只是"存在界"的形式化。这正好解释了为什么整个仓库的解析界几乎都是 `∃C` 型（机器不提供可计算常数）。
- 依赖链（【事实】）：`SiegelWalfiszOf : Prop := PsiChiBound → ZFRDirichlet → ExcBound → SiegelWalfisz`（`LogDerivRegionChiOf.lean:80`），并有 `theorem siegel_walfisz_character_of : SiegelWalfiszOf`（`SiegelWalfiszOf.lean:172`）。即 `SiegelWalfisz` 依赖三个已被证明的输入：`PsiChiBound`、`ZFRDirichlet`（`NoZeroComplex.lean:32 theorem zFRDirichlet : ZFRDirichlet`）、`ExcBound`。
- 结论：**Siegel–Walfisz 在此仓库是"已证但无效（∃常数）"的经典定理形式化**；给出的是 `x·e^{−c√log x}` 型 unconditional 误差，对 Goldbach 的 major-arc **作为存在性陈述可用，但无任何数值常数**。

---

## 3. `ChebyshevGrowthImpliesZeroFree` 与"实际证明的增长"

### 3.1 接口（【事实】）

`Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/ExplicitFormulaErrorOfHostConditions.lean:40`：

```lean
def Level.Gm (Λ) (y) : ℝ := Formalism.Gz y + ∑ ψ ∈ Λ.Nt, Λ.wt ψ * (An.gChi ψ.χ y).re
def Level.wt (Λ) (ψ) : ℝ := if Λ.psK = some ψ then 1 else (3*(Λ.o : ℝ) + 1)⁻¹
def Level.ChebyshevGrowthImpliesZeroFree : Prop :=
  ∀ θ : ℝ, 0 < θ → θ < 1 → ∀ y0 : ℝ,
    (∀ y ≥ y0, Λ.Gm y ≤ y ^ θ) → Λ.ZeroFreeAbove θ
```

即：**输入**"增长假设 `Gm(y) ≤ y^θ`（θ∈(0,1)，y0 存在）"，**输出**"零无区 Re>θ"。这是一个**条件归约**，本身不给出任何具体增长/常数。

### 3.2 "实际证明的增长"（【事实】）

`Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/TopWin.lean:23,26`：

```lean
def ChebyshevInequalityOnFamilyWindows (Fm) (eD eL : ℝ) : Prop :=
  ∃ K cHH eK CL x0, ∀ x ≥ x0, x ∈ (core Fm).Win → Tied Fm eD eL K cHH eK CL x

def ChebyshevInequalityOnWindows (Λ : Level) : Prop :=
  ∀ eD eL eps, 0<eps → ∀ Fm : Fam eps,
    EFamC Λ (core Fm) → ChebyshevInequalityOnFamilyWindows Fm eD eL →
    ∃ x1, ∀ x ≥ x1, x ∈ (core Fm).Win →
      Λ.Gm x ≤ x ^ ((1:ℝ)/2 + (eD + eL + 7) * eps)
```

即实际被证明的（对 `Λ.Gm` 的）增长是：

> **`Gm(x) = O(x^{1/2 + (eD+eL+7)·ε})`**，ε 可任意小，但 `eD, eL` 是**输入 family 的 tied 参数**（`ChebyshevInequalityOnFamilyWindows` 里的任意实数，不是固定常数），系数 `+7` 是显式符号。

- **常数可否提取？** 【事实】不能：`eD,eL,x0,x1` 全是 ∃ 量词/输入参数；`Λ.wt`（(3o+1)⁻¹）与 `Λ.Nt` 依赖具体 `Level`（tower 层），也无统一数值。**【推测】** 所以这个"实际增长"是**渐近/族相对**的：没有绝对常数可读。
- 兑现路径（【事实】）：`ChebyshevInequalityOnWindows` 由 `Development/AutomorphicArithmetic/PrimitiveCosets/WindowInequalityOfArtinInputs.lean:17 theorem windowInequality_of_artinInputs` 从 `FamCoreConstantBounds`/`CoreAtH`（Artin/Galois 大机器的输入）推出；`core_gm` 提供 `Gm` 的增长。即：**"Chebyshev 增长"由大机器内部证明，不是由显式公式的显式常数推出**。

---

## 4. 显式公式 / PNT 误差 / 族求和

### 4.1 【事实】族求和型 ψ 误差（对模 M 的**所有**特征标求和）——已证

`Formalism/GL3MeanSquares/.../DeuringHeilbronnM.lean`：

```lean
def etaOf (M) : ℝ := match eOf M with | none => 1 | some (_,β₁) => min 1 ((1−β₁)*log M)
def PsiRelA : Prop :=
  ∃ cA c A : ℝ, 0<cA ∧ 0<c ∧ ∀ M [NeZero M], 8∣M → ∀ y≥2,
    log M ≤ cA·√(log y) →
    ∑ χ : DirichletCharacter ℂ M, ‖psiChi χ y − mainPsi (eOf M) χ y‖
      ≤ A·y·etaOf M·exp(−c·√(log y))
def PsiRel : Prop := （更宽范围：… exp(−c log y/log M) + exp(−c√log y)）
```

- **已证**：`PNTRangeA.lean:161 psi_relative_near_range : PsiRelA`；远范围 `PNTBAsm.lean:15 psi_relative_far_range : PsiRelBOf`；合并见 `PNTFinal.lean:23-24`（`glue_ranges ... → prime_count_of_psi`）。
- 意义：这是**跨特征标（族）求和的 PNT 误差**：`Σ_{all χ mod M} ‖ψ(χ) − main term‖`。它是仓库中最接近"族层面定量控制"的对象——**但它是 ψ 误差的和，不是 L'/L 的矩**；且 `mainPsi` 含例外零点项、常数 ∃。
- 另有（前次已报）：`chebyshevPsiProgression_relative_error`（相对误差 PNT in AP，含例外零点），`PNTAPRelW`（已证，`PNTBridge.lean:9`）。

### 4.2 【事实】显式公式（含显式零点计数）——已证

`ExplicitS`（`DeuringHeilbronnM.lean`，`PNTExplMain.lean:15 smoothed_explicit_formula : ExplicitS`）：
- 对任意 κ∈(0,1/20]，存在零点集 Z（重数 m）与常数 K，使
  - 单位区间零点计数 `Σ_{ρ∈Z, |Im ρ − t| ≤ 1} m(ρ) ≤ C·log(M(|t|+2))`（显式 log 形）；
  - 显式公式误差 `‖Schi χ y / y − K − (χ=1?(log y −1):0) + Σ_{ρ∈Z} m(ρ) y^{ρ−1}/(ρ(ρ−1))‖ ≤ C·[((MT)^C·y^{−κ/2}) + log y·log²(MT)/T]`。
- 另：`PI.ExplicitFormula`（`Formalism/PeriodIntegrals/ExplicitFormula.lean`，`explicitFormula_closed` 已证）：`‖ψ0+Σ_{ρ<T}ord u^ρ/ρ‖ ≤ C(u log²(NuT)/T + log(Nu) + Σ_{|Imρ|<1}ord/‖ρ‖)`。

---

## 5. 大筛 / 特征和矩（仓库里**有显式常数**的部分）

### 5.1 【事实】乘性大筛（显式常数 Q² + 2πN）——已证

`Development/.../GlobalInterpolation/MultiplicativeLargeSieveStatement.lean:6`：

```lean
theorem _root_.GlobalTheory.T.sum_norm_sq_primitive_char_sum_le :
  ∀ (Q M N : ℕ) (a : ℕ → ℂ), 1 ≤ Q →
    ∑ q ∈ range Q, ∑ᶠ χ ∈ {χ : DirichletCharacter ℂ (q+1) | χ.IsPrimitive},
      ‖∑ n ∈ Ioc M (M+N), a n * χ(n)‖ ^ 2
    ≤ ((Q:ℝ)^2 + 2*π*N) * ∑ n ∈ Ioc M (M+N), ‖a n‖^2
```

**已证**（`exact @GlobalTheory.multiplicative_large_sieve`）。注意：**跨模数、跨特征标**求和（primitive chars mod q+1，q<Q），常数**显式**（Q²+2πN）。但对象是**特征和**，不是 L'/L。

### 5.2 【事实】算术大筛（one residue class per prime，显式常数）——已证

`ArithmeticLargeSieveOneResidueClassPerPrimeStatement.lean:6`：

```lean
theorem ...arithmeticLargeSieve_one_residue_class_per_prime :
  ∀ (M N Q q : ℕ) (S : Finset ℕ), 1 ≤ Q → 1 ≤ q → S ⊆ Ioc M (M+N) →
    (∀ p prime, p ≤ Q, ¬p∣q → ∃ c, ∀ n∈S, n ≢ c [MOD p]) →
    (S.card : ℝ) * ((q.totient : ℝ)/q * Real.log Q) ≤ (Q:ℝ)^2 + 2*π*N
```

**已证**。这是 Selberg 筛型（one residue class avoided per prime）的显式形式，常数显式。

### 5.3 【事实】特征标矩/正交/Parseval（跨特征标，部分显式）——已证

`Formalism/LFunctionBounds/PositivityBound.lean`（前次已列）：
- `M4`：全体非主特征标四阶矩 `Σ_χ ‖I_X χ‖^4 ≤ C·l^{1+ε}·X²`。**已证**（`Development/WeilBound/.../MatchAll.lean:26`）。
- `CharOrtho`：`Σ_{χ∈allChars l} ‖Σ b_n χ(n)‖² ≤ (l−1)Σ‖b_n‖²`（显式常数 l−1）。
- `ParsevalHolder`：对任意特征标子集 BB 的显式 Parseval/CS。
- `LPartialSum`：`‖L(χ,s) − Σ_{n≤N}χ(n)n^{−s}‖ ≤ 2B(1+‖s‖/Re s)N^{−Re s}`。**已证**（`LPartialSum.lean:136`）。
- `PolyaVinogradov`：`≤ K√l(1+log l)`（K 为 ∃，非显式数值）。

**没有任何 L'/L 的矩**（二阶/四阶都没有）。

---

## 6. 显式常数清单（"explicit" 到底 explicit 到哪一步）

| 对象 | 常数形态 | 是否显式数值 |
|---|---|---|
| 乘性大筛 | `Q² + 2πN` | **是**（显式） |
| 算术大筛 | `φ(q)/q·log Q ≤ Q²+2πN` | **是** |
| `LogDerivBound`（`f'/f`） | `24·log M / R` | **是**（24） |
| `LandauLocal` | `72·log M / r` | **是**（72） |
| `Spacing` | `2(1+log(2T+1))` | **是**（2） |
| `PairCross` | `4(M+1)(1+‖w‖)` | **是**（4） |
| `PairSame` | `4U^{1−Re w}/|Im w| + 4(M+1)(1+‖w‖)` | **是**（4,4） |
| `Offdiag` | `U(9+8log(2T+1)) + |S|·8(M+1)(2+2T)` | **是**（9,8,2） |
| `M4` | `C·l^{1+ε}X²` | 否（∃C） |
| `PolyaVinogradov` | `K√l(1+log l)` | 否（∃K） |
| log-free 零密度 | `C(qT)^{A(1−σ)}`，∃A,C,η | 否 |
| Repulsion | `c·log(c/((1−β)L))/L`，∃c | 否 |
| Siegel–Walfisz | `C·x·e^{−c√log x}`，∃c,C（Siegel 无效） | 否 |
| `ExplicitS`/`PsiRel`/`PI.ExplicitFormula` | ∃C（各文件不同） | 否 |
| Chebyshev 增长 | `x^{1/2+(eD+eL+7)ε}`，eD,eL 输入参数 | 符号显式、无数值 |
| `LogDerivRegionChi` | `C·log²(q(|t|+2))`，∃C | 否 |
| `LogDerOne` | `C·log(3q)`，∃C | 否 |

---

## 7. 对 LL Hypothesis R 的最终裁决（残酷诚实）

**(a) 优于 (logN)² 的 ‖T_N‖ 显式界：不行。** 仓库中 L'/L 的唯一成型定量界 `LogDerivRegionChi` 本身就是 `C·log²` 形态、常数存在、只覆盖零无区 `Re ≥ 1−c/log(q(|t|+2))`；`LogDerOne` 只在 s=1；`ExplicitS`/`PsiRel` 控制的是 ψ 和零点计数。没有跨特征相关核，也没有把 log² 改进的结构。（【推测】即便把 `LogDerivRegionChi` 的代数量级代入某个 T_N 定义，得到的也是 log² 型 + 不可数常数，不可能得到 N^{−1/2}。）

**(b) 跨字符 L'/L 二阶/四阶矩：不行。** 仓库只有**特征和**的跨特征二阶/四阶矩（大筛、`M4`、`CharOrtho`、`ParsevalHolder`），以及**族求和 ψ 误差**（`PsiRel`）；没有 L'/L 值的任何矩。唯一含 L'/L 的族平均（`WeightMoments`/`WeightPrimeCor`，s=1、扭转族）是**死代码**（只有 `Statement.lean`，无证明、无引用——Phase-5 已核实）。

**(c) level-aspect pair correlation：不行。** 无 pair correlation/Montgomery/Katz–Sarnak/随机矩阵对象；`Spacing`/`Triv`/`Offdiag` 是零密度证明中的**零点计数/间距**构件（`1/|t−x|` 求和、简单计数），没有对相关函数/Fourier 对偶/level 方向族平均。

**能借鉴什么（【推测】）**：
1. **大筛的显式常数形态**（Q²+2πN、φ(q)/q·log Q ≤ …）——若 Hypothesis R 可化为"族上特征和/核的二阶量"，这里的显式常数和"跨模数层叠"结构是最接近可改造的模板；
2. **`Offdiag` 的跨特征标对求和技巧**（把两个特征标乘积的短 Dirichlet 多项式求和、与零点对绑定）——形态上最接近"跨特征相关核"，但对象是特征和，不是 L'/L；
3. **`ExplicitS` 的单位区间零点计数 + `logDensityM`/log-free 零密度 + repulsion**——如果要做 level-aspect 的零点统计上界，这些是仓库中现成的零点计数部件（但只给出上界/密度，不给出 pair correlation）；
4. **`ChebyshevInequalityOnWindows` 的 `x^{1/2+(eD+eL+7)ε}` 增长接口**——如果想从"族增长的 δ 预算"反推某个定量界，这是唯一展示"RH 质量增长如何被参数化"的接口；但常数不可读。

**结论一句话**：Alpöge 机器的定量层是**经典解析数论的巨大形式化仓库**（大筛、零点密度、DHB、Siegel–Walfisz、显式公式、族求和 ψ 误差），**不是**跨特征 L'/L 相关/矩的工具箱；对 Hypothesis R，仓库里**没有现成可复用引理**，最多提供 (a) 大筛显式常数形态、(b) 跨特征对求和的技巧模板、(c) 零点计数/密度/repulsion 的现成部件。

---

## 8. 方法、证据与局限

- **搜索**：全树 175,187 文件 `grep -rli/-li -F`（大小写不敏感）；关键词：log-free/logfree、deuring、heilbronn、repulsion、zero-density、large sieve、selberg、S(t、arg L、second moment、pair correlation、Katz、Sarnak、Montgomery、random matrix、mollifier、Weil positivity、effective/ineffective、Selberg sieve、explicit error 等；文件名 `*Density*`(495)、`*LargeSieve*`(5)、`*Selberg*`(112)、`*Moment*`(143)、`*Deuring*`(4)、`*Heilbronn*`(2)、`*LogFree*`(2)、`*Repulsion*`(2)。
- **假阳性已抽样排除**：`Weil positivity`(32)=`SplitWeil PositivityTheory` 命名空间拼接；`Katz`(564)=`GlobalTheory.Katz` 形式余边界；`mollifier`(71)=复分析 mollifier；`sieve`(577) 多为子串；`Selberg`(112) 多为 Rankin–Selberg（自守表示）而非 Selberg 筛——**唯一真正的筛法**是 §5.2 算术大筛（one residue class per prime）。
- **已证判定**：找到 `theorem X : Prop := <证明>` 即标"已证"；对关键目录 `Formalism/GL3MeanSquares`、`Development/.../GlobalInterpolation`、`Formalism/LFunctionBounds`、`Formalism/LandauZeroFreeBounds` 做了 `sorry`/`axiom` 声明扫描：**未发现**（但非全量审计，且仓库整体已由 MIT 验证 175,187 模块零 sorry/axiom——见前次 digest）。
- **局限**：①grep 负结论受生成式命名限制（无 docstring），但语义词已全树扫描；②"是否已证"依赖找到证明项，少数（如 `PolyaVinogradov`、`PositivityBound`）未逐一追到证明文件，已在文中标注；③未做数值/常数计算，仅类型级分析。
