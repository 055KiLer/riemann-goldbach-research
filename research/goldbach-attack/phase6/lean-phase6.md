# Phase-6 Lean 形式化报告：LL 有限维零–范数字典（task-26）

**日期**：2026-11-21 19:17–19:24 CST（= 11:17–11:24 UTC）
**执行**：teammate `lean-feasibility`
**结论一句话**：**零–范数字典的核心引理全部通过 Lean 内核检查**：`lake env lean` **EXIT CODE: 0**、无 sorry、11 条审计引理公理全部 `[propext, Classical.choice, Quot.sound]`。

- 形式化文件：`_rh-work/goldbach-attack/phase6/lean/dictionary.lean`（323 行，13,613 B，sha256 `268ec09a2f0187758b8e6c5d066e617e2fdb0e9c690e155b71aecbf21e83fe61`）
- 验证 transcript：`_rh-work/goldbach-attack/phase6/lean/dictionary.output.txt`（3,500 B，含完整 `#check`/`#print axioms` 与 `[EXIT CODE: 0]`）
- 环境：复用 **Mathlib v4.36.0**（tag commit `fc4f59e577feb1a4956671bc04ac18aaaf8cd842`，`/home/kiler/rh-work/lean-test/mathlib36/mathlib4-4.36.0`；Lean v4.36.0 commit `611c117…`）。为本次新增 import 补拉 96 个 olean（`lake exe cache get Mathlib.Analysis.Matrix.Spectrum …`，20 s）。

---

## 0. TL;DR

| 项目 | 结果 |
|---|---|
| `lake env lean dictionary.lean` | ✅ **EXIT CODE: 0**（15.6 s，含 12 条 `#check` + 11 条 `#print axioms`） |
| sorry / axiom / admit | ✅ 无（grep 只命中 docstring 的说明文字） |
| 公理 | ✅ 全部 11 条 = `[propext, Classical.choice, Quot.sound]` |
| (a) 字典 `exists_q_zero_iff` | ✅ `(∃q∈(0,1), X(q)=0) ↔ ∃j, δ≤|μ_j|` |
| (b) 无零点方向 | ✅ 精确形式 `no_real_zero_iff`：`(∀q∈(0,1), X(q)≠0) ↔ ∀j, |μ_j|<δ`；`≤` 版本只能给 `X_nonneg_of_le`（见 §3 的诚实修正） |
| (c) 对称性 | ✅ `X(1−q)=X(q)`，`X(0)=X(1)=1` |
| 矩阵实例 | ✅ `matrix_exists_q_zero_iff`（μ = Mathlib 谱定理的 `IsHermitian.eigenvalues`，实对称 `C.IsSymm`） |
| (d) 链条 | ✅ `finite_model_chain`（抽象版，谱桥作为显式假设）：Rayleigh 商 > δ ⇒ `¬ HypothesisR` ∧ `∃q, X(q)=0` |
| 未做/限制 | 见 §5（无 ℜq>1−η 半平面版本、无复 q 分类、无 Fredholm 行列式/无限乘积收敛、谱桥未从谱定理推出、文件中复制了 phase5 的 Rayleigh 引理而非 import） |

---

## 1. 数学内容与公式勘误（重要）

论文（本地文本 `/home/kiler/rh-work/liu-goldbach.clean.txt`）§2.4.1 原文：

```
(1.6):  X_N(q) = ∏_j (1 − 4μ²_j(N)/(δ²_N) · q(1 − q))        [PDF 分数为 4μ²/δ²，再乘 q(1−q)]
(2.20): X_N(0) = X_N(1) = 1
(2.21): X_N(1−q) = X_N(q)
"put d_j = δ²_N/μ²_j(N) and write q = x + yI ... The factor equation is q(1−q) = d_j/4."
```

**任务书里把公式写成 `X(q)=∏_j (1 − 4μ_j²/(δ² q(1−q)))`（q(1−q) 在分母），这与论文不一致**，且与论文自身 (2.20) 矛盾（在 q=0、q=1 处分母为 0，不可能 X(0)=X(1)=1），也与因子方程 `q(1-q)=d_j/4 = δ²/(4μ_j²)` 不符。正确形式是

$$\boxed{X_\delta(q) = \prod_j \left(1 - \frac{4\mu_j^2}{\delta^2}\, q(1-q)\right)}$$

本报告按论文的正确形式形式化（`LLDictionary.X`）。在此形式下：

- 因子 = 0 ⇔ `q(1−q) = δ²/(4μ²)`；
- 而 `q(1−q)` 在 `q∈(0,1)` 上的值域是 `(0, 1/4]`，
- 故实零点存在 ⇔ `δ²/(4μ²) ≤ 1/4` ⇔ **`δ ≤ |μ|`** —— 正好是任务书 (a) 的 RHS，且与论文 §2.4.1 的分类一致：
  - `|μ| > δ`：两个实零点 `q = 1/2 ± (1/2)√(1−δ²/μ²)`（对称于 1/2）；
  - `|μ| = δ`：`q = 1/2`（因子的二重零点）；
  - `|μ| < δ`：`(0,1)` 内无实零点。
- 若误用"分母形式"，零点条件会变成 `|μ| ≤ δ/4`，与 R（`‖T‖≤δ`）恰好冲突，字典方向反了，进一步印证正确形式。

---

## 2. 形式化文件结构

`dictionary.lean` 分三部分（namespace `LLDictionary`）：

```
Part 1  Algebra      —— 纯代数字典（对任意有限族 μ : n → ℝ、δ > 0）
Part 2  MatrixCase   —— 用 Mathlib 谱定理的特征值实例化到实对称矩阵
Part 3  Chain        —— 与 phase5 Rayleigh 引理组合的抽象链条 (d)
末尾    Axiom audit  —— #check + #print axioms
```

### 2.1 定义

```lean
noncomputable def X (δ : ℝ) (μ : n → ℝ) (q : ℝ) : ℝ :=
  ∏ j, (1 - 4 * (μ j) ^ 2 * (q * (1 - q)) / δ ^ 2)
```

### 2.2 引理与精确类型（来自验证输出原文）

```
LLDictionary.q_mul_one_sub_pos {q : ℝ} (hq : q ∈ Set.Ioo 0 1) : 0 < q * (1 - q)
LLDictionary.q_mul_one_sub_le (q : ℝ) : q * (1 - q) ≤ 1 / 4
LLDictionary.exists_q_mul_one_sub_eq {c : ℝ} :
    (∃ q ∈ Set.Ioo 0 1, q * (1 - q) = c) ↔ 0 < c ∧ c ≤ 1 / 4
LLDictionary.factor_zero_iff {δ : ℝ} (hδ : 0 < δ) (μ : ℝ) :
    (∃ q ∈ Set.Ioo 0 1, 1 - 4 * μ ^ 2 * (q * (1 - q)) / δ ^ 2 = 0) ↔ δ ≤ |μ|
LLDictionary.exists_q_zero_iff {n} [Fintype n] {δ : ℝ} (hδ : 0 < δ) (μ : n → ℝ) :
    (∃ q ∈ Set.Ioo 0 1, X δ μ q = 0) ↔ ∃ j, δ ≤ |μ j|          -- (a)
LLDictionary.no_real_zero_iff {n} [Fintype n] {δ : ℝ} (hδ : 0 < δ) (μ : n → ℝ) :
    (∀ q ∈ Set.Ioo 0 1, X δ μ q ≠ 0) ↔ ∀ (j : n), |μ j| < δ     -- (b) 精确形式
LLDictionary.X_nonneg_of_le {n} [Fintype n] {δ : ℝ} (hδ : 0 < δ) (μ : n → ℝ)
    (h : ∀ j, |μ j| ≤ δ) {q : ℝ} (hq : q ∈ Set.Ioo 0 1) : 0 ≤ X δ μ q   -- (b) 的 ≤ 版本
LLDictionary.X_one_sub {n} [Fintype n] (δ : ℝ) (μ : n → ℝ) (q : ℝ) :
    X δ μ (1 - q) = X δ μ q                                     -- (c)
LLDictionary.X_zero {n} [Fintype n] (δ : ℝ) (μ : n → ℝ) : X δ μ 0 = 1    -- (c)
LLDictionary.X_one  {n} [Fintype n] (δ : ℝ) (μ : n → ℝ) : X δ μ 1 = 1    -- (c)
LLDictionary.matrix_exists_q_zero_iff {n} [Fintype n] [DecidableEq n]
    (C : Matrix n n ℝ) (hC : C.IsSymm) {δ : ℝ} (hδ : 0 < δ) :
    (∃ q ∈ Set.Ioo 0 1, X δ (hH.eigenvalues) q = 0) ↔ ∃ j, δ ≤ |hH.eigenvalues j|
    -- 其中 hH := isHermitian_of_isSymm C hC : C.IsHermitian（Mathlib 谱定理特征值）
LLDictionary.finite_model_chain {H} [NormedAddCommGroup H] [InnerProductSpace ℝ H]
    (T : H →L[ℝ] H) {δ : ℝ} (hδ : 0 < δ) (v : H) (hv : ‖v‖ = 1)
    (hRay : δ < ⟪T v, v⟫_ℝ) {n} [Fintype n] (μ : n → ℝ)
    (hbridge : ∀ B : ℝ, ‖T‖ ≤ B ↔ ∀ j, |μ j| ≤ B) :
    ¬ HypothesisR T δ ∧ ∃ q ∈ Set.Ioo 0 1, X δ μ q = 0          -- (d) 抽象链条
```

### 2.3 证明要点

- `q_mul_one_sub_pos/le`：`q(1−q) = 1/4 − (q−1/2)²`，`nlinarith`。
- `exists_q_mul_one_sub_eq`：显式构造 `q = (1 + √(1−4c))/2`；`c ∈ (0,1/4]` 保证 `0 ≤ 1−4c`，故 `√·` 有意义；`√(1−4c) < 1` 由 `Real.sqrt_lt`；`q(1−q) = (1−(1−4c))/4 = c` 由 `Real.sq_sqrt` + `nlinarith`。
- `factor_zero_iff`：
  - →：由因子方程得 `4μ²q(1−q) = δ²`，再用 `q(1−q) ≤ 1/4` 得 `δ² ≤ μ²`，即 `|δ| ≤ |μ|`，用 `δ>0` 化简；
  - ←：取 `c = δ²/(4μ²)`；由 `δ ≤ |μ|` 得 `c ≤ 1/4`，`c>0`；用上一条取 `q`，再验证因子为 0。
- `X_eq_zero_iff_factor`：`Finset.prod_eq_zero_iff`（`ℝ` 是 `NoZeroDivisors`）。
- `exists_q_zero_iff`：组合前两条。
- `no_real_zero_iff`：由 `factor_zero_iff` 做逻辑对偶（关键：`¬(|μ|<δ) ↔ δ≤|μ|`）。
- `X_nonneg_of_le`：每个因子 `≥ 0`（`4μ²q(1−q)/δ² ≤ 4δ²·(1/4)/δ² = 1`），用 `Finset.prod_nonneg`。
- `X_one_sub`：`(1−q)·(1−(1−q)) = q(1−q)`，`Finset.prod_congr` + `ring_nf`。
- `matrix_exists_q_zero_iff`：`isHermitian_of_isSymm`（实矩阵 `IsSymm` ⇒ `IsHermitian`）取 `IsHermitian.eigenvalues`，转用纯代数 `exists_q_zero_iff`。
- `finite_model_chain`：(d) = phase5 的 `rayleigh_gt_refutes_R`（本文件内附复制版） + 谱桥 + `exists_q_zero_iff`：
  `¬(‖T‖≤δ)` + `hbridge δ` ⇒ `¬∀j |μ_j|≤δ` ⇒ `∃j |μ_j|>δ` ⇒ `δ≤|μ_j|` ⇒ X 有实零点。

---

## 3. 诚实修正：任务书 (b) 的 `≤` 表述在边界不成立

任务书 (b) 写"若 ∀j, |μ_j| ≤ δ，则 ∀q∈(0,1)，X(q) ≠ 0"。**这在边界 `|μ_j| = δ` 时为假**：此时取 `q = 1/2`，因子 `1 − 4δ²·(1/4)/δ² = 0`，故 `X(1/2) = 0`（这正是论文 §2.4.1 里 `d_j = 1` 的"二重零点"情形）。本文件的形式化因此是：

- `no_real_zero_iff`（**精确**）：无实零点 ⟺ `∀j, |μ_j| < δ`；
- `X_nonneg_of_le`（`≤` 能推出的最强结论）：`∀j,|μ_j|≤δ` ⇒ `X(q) ≥ 0` 于 `(0,1)`（零点可以出现在 `q=1/2`）。

这与论文一致：论文真正的字典是半平面版本
`X_N(q) ≠ 0 (ℜq > 1−η) ⟺ ‖T_N‖ ≤ δ_N/(2√(η(1−η)))`（(2.23) 一带），该半平面是**开**的，边界零点（`q=1/2`）与范数等号均被排除；所以 "R ⇒ 半平面内无零点" 成立，而 "R ⇒ (0,1) 内无零点" 需要严格不等式。本次**未形式化**半平面/η 版本（见 §5）。

---

## 4. 公理审计（`#print axioms` 原文）

```
'LLDictionary.q_mul_one_sub_pos'       depends on axioms: [propext, Classical.choice, Quot.sound]
'LLDictionary.q_mul_one_sub_le'        depends on axioms: [propext, Classical.choice, Quot.sound]
'LLDictionary.exists_q_mul_one_sub_eq' depends on axioms: [propext, Classical.choice, Quot.sound]
'LLDictionary.factor_zero_iff'         depends on axioms: [propext, Classical.choice, Quot.sound]
'LLDictionary.exists_q_zero_iff'       depends on axioms: [propext, Classical.choice, Quot.sound]
'LLDictionary.no_real_zero_iff'        depends on axioms: [propext, Classical.choice, Quot.sound]
'LLDictionary.X_nonneg_of_le'          depends on axioms: [propext, Classical.choice, Quot.sound]
'LLDictionary.matrix_exists_q_zero_iff'depends on axioms: [propext, Classical.choice, Quot.sound]
'LLDictionary.finite_model_chain'      depends on axioms: [propext, Classical.choice, Quot.sound]
'LLDictionary.X_zero'                  depends on axioms: [propext, Classical.choice, Quot.sound]
'LLDictionary.X_one'                   depends on axioms: [propext, Classical.choice, Quot.sound]
```

- 无 `sorry`/`axiom`/`admit`/`native_decide`；`lake env lean` 本身即内核逐条检查。
- （允许集按 phase5 报告约定：`propext, Classical.choice, Quot.sound`。）

---

## 5. 诚实说明：未做到 / 简化

1. **未形式化论文的 ℜq>1−η 半平面字典 / 复 q 分类**（§2.4.1 的 nonreal zeros 两球面、`ℜq=1/2`、`|ℑq|=½√(d_j−1)` 等）。需要复/四元数切片与半平面几何，超出本次 75 分钟目标；其核心代数 `factor_zero_iff` 已经通用（复 q 的因子方程可直接复用）。
2. **未形式化无限乘积收敛、Fredholm 行列式表示** `X_N(q) = det(Id − 4δ^{-2}q(1−q)T²)`。本次 X 是**有限维**乘积（正是 task 要求"避免无限乘积"）；矩阵实例的 X 直接使用有限族特征值。
3. **(d) 的"谱桥"是显式假设**：`hbridge : ∀B, ‖T‖ ≤ B ↔ ∀j, |μ_j| ≤ B` 未从 Mathlib 谱定理证明。要证它需要 `‖C‖ = max_j |eigenvalues j|`（矩阵 L2 算子范数 = 谱半径）这一矩阵范数–特征值定理；本次未做（若需要，可后续单独形式化，预计需要 spectral_theorem 的特征基展开与算子范数估计，中等工作量）。
4. **(d) 本文件复制了 phase5 的 2 条引理**（`abs_rayleigh_le_opNorm`、`rayleigh_gt_refutes_R`、`HypothesisR` 定义），因为 phase5/lead 的 Lean 目录不是 Lake 包、跨目录 `import` 需要额外 `-R` 参数与模块名；为保持单文件可复现而复制。两处证明相同，phase5 版本已单独验证过。
5. **(a) 的 "μ_j 为特征值"**：Part 1 对任意有限族 μ 成立（纯代数字典）；Part 2 用 Mathlib `Matrix.IsHermitian.eigenvalues` 实例化，并给出该特征值的定义性保证（`Matrix.IsHermitian.mulVec_eigenvectorBasis`：`C *ᵥ e_j = μ_j • e_j`，在 Mathlib 中已有，本文件未重复导出）。
6. **没有使用具体数值**（无 N=30030 的具体特征值/δ 数据）；全部是符号化字典。

---

## 6. 复现步骤

```bash
MATHLIB=/home/kiler/rh-work/lean-test/mathlib36/mathlib4-4.36.0
export PATH=/home/kiler/rh-work/lean-test/lean4/lean-4.36.0-linux/bin:$PATH
cd "$MATHLIB"

# 验证（唯一需要的命令；文件在 _rh-work 目录中）
lake env lean /home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase6/lean/dictionary.lean
# → 打印 12 条 #check + 11 条 #print axioms，最后无错误（EXIT 0）

# 如需从头补缓存（本次新增 96 个 olean）：
# lake exe cache get Mathlib.Analysis.Matrix.Spectrum Mathlib.Analysis.Real.Sqrt \
#   Mathlib.Algebra.BigOperators.GroupWithZero.Finset
```

环境事实：`lean --version` = `Lean (version 4.36.0, x86_64-unknown-linux-gnu, commit 611c117bfaf7b7ae1cfcf246ce6fba31e8f509e9, Release)`；`lake --version` = `Lake version 5.0.0-src+611c117`；Mathlib tag v4.36.0（commit `fc4f59e577feb1a4956671bc04ac18aaaf8cd842`）；`.lake/build` 2.9 GB。

---

## 7. 交付文件清单

| 文件 | 大小/行数 | sha256 | 说明 |
|---|---|---|---|
| `phase6/lean/dictionary.lean` | 323 行 / 13,613 B（见下方验证） | `268ec09a2f0187758b8e6c5d066e617e2fdb0e9c690e155b71aecbf21e83fe61` | 主交付（§2 的 11 条审计引理 + 定义 + 审计命令） |
| `phase6/lean/dictionary.output.txt` | 3,500 B | — | `lake env lean` 完整 transcript（`[EXIT CODE: 0]`） |

---

## 8. 与 phase-5 / LL 逻辑的位置关系

- phase-5 已内核验证"自伴 + range⊆M ⇒ transfer 恒等式"与"单位 Rayleigh 商 > δ ⇒ ¬(‖T‖≤δ)"。
- 本次 (d) 把它们与**特征值零点字典**相接：`λ̃ > δ`（有限模型可证数据）⇒ `¬R(N)` **且** `X_δ` 在 `(0,1)` 有实零点。即 LL §2.4.2 字典的"零点 ⇔ 范数界"链条中，零点一侧的代数核心 `exists_q_zero_iff` 已被 Lean 内核验证；范数一侧仍依赖 (d) 的谱桥假设（或未来形式化的矩阵范数–特征值定理）。
