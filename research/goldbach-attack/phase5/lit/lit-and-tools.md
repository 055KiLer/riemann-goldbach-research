# Phase-5 文献与工具调研：E(X) 的 GRH 条件界、N⁻¹ᐟ² 相消工具、2026 动态与 LL 路线评估

> 作者：goldbach-researcher（task-16）。日期：2026-11-21（Asia/Shanghai）。所有 URL 访问日期 2026-11-21，除非另行注明。
> 范围：只做文献/工具调研，不重新推导 LL 逻辑，也不对 task-13/14/17 的数值结论表态（只引用其待定结论）。
> 标注：**[事实]** 已证明/已发表/可核验；**[预印本主张]** 2026 年新发布、未同行评审；**[猜想]** 未证明；**[推导]** 本报告的推理；**[推测]** 启发式/判断。
> 记号（与 phase-4/5 报告一致）：`g_χ(s)=L'/L(1/2+s,χ)`（χ 奇，mod N，含非本原）；`P_N(s,z̄)=(2/φ(N))Σ_{χ∈X_N^-}g_χ(s)g_{χ̄}(z̄)`；`D_N(w)=Σ_{(n,N)=1}Λ²(n)n^{-1-w}`；`K_N`=LL (2.12) Beta 模型；`E_N=P_N−D_N−K_N`（=T_N 的核）；`S_N={s: α_N<Re s<β}`，`α_N=1/log N`，`β=1/8`；`δ_N=√(S(N)/N)(log N)^{3/2}`，其中 `S(N)=2C₂∏_{p|N,p>2}(p−1)/(p−2)` 为 Goldbach 奇异级数。

---

## 0. 五条要点（已先发给 lead）

1. **[事实] “GRH ⇒ E(X)≪X^{1/2+ε}” 是真定理，不是启发式。** 更一般的形式：若所有 Dirichlet L 的非平凡零点满足 Re ρ ≤ Θ < 3/4，则 E(X) ≪_ε X^{2Θ−1/2+ε}；Θ=1/2（GRH）给 X^{1/2+ε}。来源：Bhowmik–Grimmelt 2026 综述 arXiv:2607.27282 §3 Theorem 3.1；等价地 Pintz–Althöfer 2026 arXiv:2610.15559 Theorem 3（g(θ)=θ(5−4θ)/(2(2−θ))，g(1/2)=1/2）；历史 Hardy–Littlewood 1924，Goldston 1992 把 ε 换成 log 幂。
2. **[事实/预印本] 无条件的 E(X) 记录在 2025–26 有实质改进：** Pintz 2018 `E(X)<X^{0.72}` → Zhao 2025 arXiv:2511.05631 `E(X)=O(X^{7/10})`（ineffective，v2 2026-01-23）→ Pintz–Althöfer 2026：只要存在任一固定无零半平面 Re≤θ₀<1 就有 `E(X)≪X^{7/12+ε}`；若接受 OpenAI 2026-09-30 宣称的 quasi-RH（Re s>7/8 无零点）则得无条件形式的 `X^{7/12+ε}`（他们的 Corollary 2）。另有未认证的 AI 辅助 0.684 数值链（论文声明不用于证明）。
3. **[推导] 若 Alpöge GRH 成立，与 Goldbach 相关的无条件化结果：** ① `E(X)≪X^{1/2+ε}`（以及 Goldston 的 `X^{1/2}(log X)^c`）；② Goldston–Suriajaya 的 GRH-条件下 Goldbach 表示数平滑平均（arXiv:2306.04807）变为无条件；③ LL 条件性证明的 GRH 条件被消去，但只剩 S/R；④ 经典“GRH⇒三素数”已被 Vinogradov/Helfgott 无条件化，无新内容。**都不给出逐 N 的哥德巴赫。**
4. **[事实+推导] R 需要的分析输入 = χ 族的平方根相消（跨特征标 L'/L 的二阶/四阶相关 + t-一致），现有已证工具都不够**：字符正交/大筛只给对角；level-aspect 的 L 函数二阶矩已知、四阶矩 Young 2011（素数模）但只对 L 且 χ-平均；L'/L 高阶矩只在固定点（Ghosh 2025）；Selberg CLT 是分布结论（Das 2021 q-aspect）；1-level density 只对受限检验函数；**Dirichlet L 的 pair correlation 本身仍是猜想**（Kandhil–Languasco–Moree 2024/2026 明确“假设 GRH+pair correlation”才能推 Elliott–Halberstam）；零点密度无条件但太弱；AFE/Perron 路线受 phase-4 的“对角记账障碍”限制。→ R 可归约为一个新的族相关估计，超出 2026 主流技术。
5. **[预印本主张/事实] 2026 动态：** LL 2026-11-13 条件性论文之后只有中文科普/知乎讨论，未发现正式批评或独立核验；RH Lean 核验页 2026-11-21 抓取仍与 2026-11-20 22:05 UTC 相同（`lake comparator` 和 Lean kernel replay 仍 running，未同行评审）；真正改变 Goldbach 例外集版图的是 OpenAI 2026-09-30 的 quasi-RH（7/8 无零半平面，主结果已 Lean 形式化、但状态 “claimed, unreviewed”）及 Pintz–Althöfer/Maynard–Pandey–Radziwiłł 的 7/12；未发现任何人把 Alpöge/Stepanov/theta-lift/Weil 正性机器用于加性问题。**评估：** 若 R 渐近为真且可证，LL 路线原则上可行（N₀ 约 10⁶ 以下的有限 N 可直接验证）；但证明 R 需要一座目前不存在的桥（族 pair correlation / 跨 χ 四阶相关），距离现有技术很远。

---

## 1. 二元 Goldbach 例外集 E(X)：无条件与 GRH 条件下的精确现状

### 1.1 定义

对偶数 N，`E(X) = #{n≤X : 4≤n≤X, n 为偶数, n 不能写成两个素数之和}`（本文与 Pintz–Althöfer 的定义一致，忽略 n=2 造成的 ±1 差异）。`r₂(N)=Σ_{p+q=N} log p log q` 为加权表示数；`E(X)` 是“almost-all Goldbach”的精确定量形式。

### 1.2 无条件结果（时间线，全部 [事实]）

| 年份 | 作者 | 精确陈述 | 出处 |
|---|---|---|---|
| 1937/38 | van der Corput; Čudakov; Estermann | `E(X) ≪_A X/(log X)^A`（任意 A>0） | Pintz 2018 §1；(综述 arXiv:2607.27282 §4) |
| 1972 | Vaughan | `E(X) ≪ X exp(−c√log X)` | Pintz 2018 §1 |
| 1975 | Montgomery–Vaughan | 存在可计算 δ>0：`E(X) ≪ X^{1−δ}` | Acta Arith. 27 (1975) 353–370；综述 Thm 5.1 |
| 1989 | Chen–Liu | δ=0.05 | Pintz 2018 §1 |
| 1999/2000 | Li Hongze | δ=0.079；随后 `E(X)<X^{0.914}` | Pintz 2018 §1 |
| 2010 | Lu Wenchao | `E(X)<X^{0.879}`（ineffective constant） | Pintz 2018 §1 |
| 2018 | Pintz | `E(X)<X^{0.72}`（X 充分大，ineffective） | arXiv:1804.09084 Theorem 1 |
| 2025 | Zhao Genheng | `E(X)=O(X^{7/10})`（ineffective） | arXiv:2511.05631（2025-11-07；v2 2026-01-23）摘要原文 “We prove the bound E(X)=O(X^{7/10})”；Pintz–Althöfer 文中引用值为 `X^{0.709}`（版本差异，以摘要 7/10 为准） |
| 2026 | Pintz–Althöfer | **条件性**：若存在固定 1/2≤θ₀<1 使所有 Dirichlet L 非平凡零点 Re ρ≤θ₀（统一对所有特征、所有高度），则 `E(X) ≪_{θ₀,ε} X^{7/12+ε}`；用 OpenAI quasi-RH（θ₀=7/8）得 `E(X) ≪_ε X^{7/12+ε}` | arXiv:2610.15559 Theorem 1 & Corollary 2 |

补充说明：

- **[预印本主张]** Pintz–Althöfer 还提到他们与 AI 辅助得到的未发表数值链把指数推进到 **0.684**（中间值 0.68601）；论文明确说“The complete numerical chain is not used in the proofs below … No new certification of that chain is asserted in this paper.”——不能作为已证结果引用。
- **[事实]** 7/12 ≈ 0.5833 的改进来自 Maynard–Pandey–Radziwiłł 2026 的素数指数和估计：arXiv:2608.14777（2026-08-14）摘要原文：
  > “Let α=a/q+ε with (a,q)=1, q≤N^{1/2} and |ε|≤1/(qN^{1/2}), and let B:=max(q,qN|ε|). We show that |Σ_{n<N}Λ(n)e(nα)| ≤ N^{o(1)}(N/B^{1/2}+N^{19/24}). This improves on the classical bound of Vinogradov from 1937, which has N^{4/5} in place of N^{19/24}.”
  以及 7/12 = 2·(19/24)−1 的记账（Pintz–Althöfer §1）。
- **[事实]** 这些全是“almost all”型结果：它们只排除 O(X^{something}) 个例外，永远不排除最后一个。

### 1.3 GRH 条件下 E(X) 的精确定理（任务核心问题：这是不是定理？）

**结论：是定理。** 有两套等价的现代陈述：

**(i) Bhowmik–Grimmelt 2026 综述（arXiv:2607.27282，33 页，Gautami Bhowmik & Lasse Grimmelt，2026-07）§3 Theorem 3.1 原文：**

> **Theorem 3.1 (Hardy–Littlewood, conditional exceptional-set bound).** Assume that every zero of every Dirichlet L-function has real part at most Θ < 3/4. Then for every ε > 0 we have
> |E(X)| ≪_ε X^{2Θ−1/2+ε}.

取 Θ=1/2（即 GRH）得 `E(X) ≪_ε X^{1/2+ε}`。该综述同时写明：这一估计最早由 Hardy–Littlewood 在 GRH 下得到，而 **Goldston（1992）** 才把 ε 换成对数幂（“Notice that it was only in 1992 that Goldston could replace the ε above by a logarithm.”）。Goldston 的精确形式在文献中通常写为 `E(X) ≪ X^{1/2}(log X)^c`（某绝对常数 c）；Pintz 2018 §1 的措辞是“apart from the substitution of X^ε by log^c X”。

**(ii) Pintz–Althöfer 2026（arXiv:2610.15559）Theorem 3 原文：**

> **Theorem 3 (Conditional refinement).** Assume H_θ for a fixed 1/2 ≤ θ ≤ 2/3. For every ε > 0,
> E(X) ≪_{θ,ε} X^{g(θ)+ε},  g(θ) = 2θ−3/(2) + 3(1−θ)/(2−θ) = θ(5−4θ)/(2(2−θ)).
> Since g(2/3)=7/12 and g is strictly increasing on [1/2,2/3], every fixed θ<2/3 gives a fixed positive saving below 7/12 …
> H_{5/8} ⇒ E(X) ≪_ε X^{25/44+ε},  7/12 − 25/44 = 1/66.

其中 `H_θ` 定义为“每个本原 Dirichlet L 函数的每个非平凡零点满足 Re ρ ≤ θ”（ζ 作为导子 1 的函数包含在内；统一对所有特征和高度）。**取 θ=1/2 即得 GRH 情形 `g(1/2)=1/2`，即 `E(X) ≪_ε X^{1/2+ε}`。** 这独立地确认了 (i)。

**注意适用条件**：这里需要的是**统一的全局 GRH**（所有模、所有高度、所有本原特征），不是“固定模数 N 的 GRH(N)”。历史出处：Hardy–Littlewood, *Some problems of ‘Partitio Numerorum’, V*, Proc. London Math. Soc. (2) 22 (1924), 46–56；Goldston, *On Hardy and Littlewood’s contribution to the Goldbach conjecture*, Proceedings of the Amalfi Conference on Analytic Number Theory (Maiori, 1989), 115–155, Univ. Salerno, 1992。教科书参考：Montgomery & Vaughan, *Multiplicative Number Theory I: Classical Theory*, CUP 2007, §18.3 “Conditional estimates”（MathOverflow 501900 也指向同一处）。

**[事实] 在 GRH 下目前没有比 X^{1/2+ε} 更好的已发表 E(X) 上界**（本报告检索范围内；7/12 的改进依赖更弱的θ₀<1 半平面 + 新的 minor-arc 估计，而不是在 GRH 下把 1/2 压下去）。是否存在“GRH + 19/24 型 minor-arc 估计 ⇒ 指数 <1/2”的组合，本轮没有在文献中找到；这是一个可以问的问题，但**[推测]**即便有也不会改变“almost all ≠ Goldbach”的结论。

### 1.4 若 Alpöge/Claude 的 GRH 被接受：哪些结果变成无条件的？（逐条）

前置：MIT 核验页 https://math.mit.edu/~drew/grh/（2026-11-21 抓取，页面 last updated 2026-11-20 22:05 UTC）确认最终定理包括“GRH = 所有 Dirichlet L-函数”，且 `riemannHypothesis : RiemannHypothesis` 是 Mathlib 定义；形式化核验（leanchecker/nanoda/con-leche/lean4lean）通过，但 `lake comparator` 与 Lean kernel replay 仍在运行、未同行评审。因此以下都应当写成“**若该证明被接受，则**”。

| 结果 | 原条件 | 若 GRH 成立后的无条件陈述 | 对 Goldbach 的意义 |
|---|---|---|---|
| Hardy–Littlewood 1924 / Goldston 1992 | GRH | `E(X) ≪_ε X^{1/2+ε}`；更精确 `E(X) ≪ X^{1/2}(log X)^c`（某绝对 c） | **[事实]** 只给几乎全体偶数；不排除任何例外 |
| Goldston–Suriajaya 2023 平滑平均 | 模 q 的 Dirichlet L 的 GRH | Goldbach 表示数在“q 的倍数 + 平滑平均”意义下的渐近公式变为无条件（arXiv:2306.04807 摘要：“Assuming the GRH for … characters modulo q, we obtain a smoothed version of the average number of Goldbach representations for numbers which are multiples of a positive integer q … we also show how the smoothing can be removed.”） | 平均型，不给出逐 N |
| Li–Liu 2026-11-13 条件性证明 | GRH(N) + Hypothesis S 或 R | GRH 条件消去，变成“S ⇒ Goldbach”或“R ⇒ Goldbach” | 仍缺 S/R，不是无条件证明 |
| Hardy–Littlewood 1923 三素数（GRH 版） | GRH | 早已被 Vinogradov 1937/Helfgott 2013 无条件化 | 无新内容 |

**重要对照**：2026 年还存在一个更弱但更早的外部输入——OpenAI 2026-09-30 的 quasi-RH（“No zeros of the Riemann zeta function or of any Dirichlet L-function with real part above 7/8”，主结果已 Lean 形式化）。[预印本主张/未评审] 若接受它，Pintz–Althöfer 已推出 `E(X) ≪ X^{7/12+ε}`（Corollary 2）。因此 Alpöge 的 GRH 若成立，其“增量”是把 7/12 改进到 1/2，而不是从“什么都没有”变成有了——但两者都不是 Goldbach。

---

## 2. N⁻¹ᐟ² 型相消：LL 的 T_N 需要什么、现有工具能做什么

### 2.1 LL 需要什么：精确量级

LL 的定理 6.2（arXiv 条件性论文 §6）在 GRH(N) 下证明

  `‖T_N‖ ≤ ‖T_N‖_HS ≪ (log N)²`（(2.24)/(6.7)），

而 Hypothesis S/R 需要的是 `‖T_N‖ ≤ δ_N` 或更精细的 `≤ S(N)/(2h√(1−η_N))`，其中

  `δ_N = √(S(N)/N)(log N)^{3/2}`。

两者之比（[推导]）：

  `(log N)² / δ_N = (log N)^{1/2} √(N/S(N))`。

由于 `S(N) ≪ log log N`，这个比值约为 `√N·(log N)^{1/2}`。因此，要把 GRH 的 `(log N)²` 基线推进到 δ_N，需要的是 **√N 量级的额外相消**——这正是本阶段任务里“N^{-1/2} 型工具”的含义：所需估计必须来自 χ 族的平均/正交性，而不是逐 χ 的点态界。

（注意：`(log N)²` 是 ‖T_N‖_HS 的三角不等式产物：`‖T_N‖_HS ≤ ‖P_N‖_HS+‖D_N‖_HS+‖K_N‖_HS`，三项各自有大小；phase-4 报告指出 `‖D_N‖_HS,‖K_N‖_HS ≍ (log N)^{3/2}`，且“no triangle route can beat Ω((log N)^{3/2})”。本报告只引用该结论供定性参考。）

### 2.2 N⁻¹ᐟ² 从哪里来：族正交性启发式 [推导/推测]

`P_N` 是 **φ(N) ≍ N 个奇特征标的平均**：

  `P_N(s,z̄) = (2/φ(N)) Σ_{χ∈X_N^-} g_χ(s) g_{χ̄}(z̄)`。

若把 `{g_χ}` 近似看作“正交且范数相当”的族：设 `M ≈ ∫_{S_N}|g_χ(s)|²|ds|`（与 χ 无关的典型大小）、`⟨g_χ,g_ψ⟩` 在 χ≠ψ 时很小，则

  `‖P_N‖_HS² = (4/φ(N)²) Σ_{χ,ψ} |⟨g_χ,g_ψ⟩|² ≈ (4/φ(N)²)·φ(N)·M² = 4M²/φ(N)`，

即 `‖P_N‖_HS ≈ 2M/√φ(N) ≍ M·N^{-1/2}`。这就是 phase-5 数值中 `λ_max√N/√S ≈ const` 的自然来源（若真）。减去 D_N、K_N 后的残差 `E_N` 是同一族平均的“涨落部分”，预期也是 N^{-1/2} 量级乘 log 幂。

要把它变成定理，至少需要：

- **(族二阶矩)** `Σ_χ ∫_{S_N} |g_χ(s)|² |ds| ≍ φ(N)·(log N)^A`（对角、χ-平均）；
- **(族非对角相关 / 跨 χ 四阶)** `Σ_{χ≠ψ} |⟨g_χ,g_ψ⟩|² ≪ φ(N)^{2−δ}(log N)^B`（off-diagonal；这正是“跨特征标相关”）。

若两条成立，则 `‖P_N‖_HS ≪ N^{-1/2}(log N)^{A/2}`，再处理 D_N/K_N 的对角抵消即可得 R 的 HS 版本。**关键：这两条都不是 GRH 的推论；它们等价于 level-aspect 的 pair-correlation/零点相关型输入。**

### 2.3 工具清单（哪些已证、能否用于 E_N 的 HS/算子范数）

| 工具 | 已证形式/精确陈述 | 能否用于 E_N 的 HS/算子范数 | 差距/备注 |
|---|---|---|---|
| **字符正交 + 大筛** | 正交恒等式 `(2/φ(N))Σ_{χ odd}χ(n)χ̄(m)=1(1_{n≡m}−1_{n≡−m})`（LL Lemma 3.1，[事实]）；大筛不等式（Montgomery–Vaughan; Iwaniec–Kowalski 书）：`Σ_{χ mod q}|Σ_{n≤N}a_nχ(n)|² ≤ (q+N−1)Σ|a_n|²` | **只给对角/平方和**；LL 已用尽这一步；不给跨 χ 的非对角相关 | 缺 off-diagonal，这正是 N^{-1/2} 的来源 |
| **Level-aspect L 函数二阶矩** | `Σ_{χ mod q}|L(1/2,χ)|² ≍ φ(q)log q`（q 素数，标准；由近似函数方程+大筛得到）[事实，经典] | 是 L 而非 L'/L；是 χ-平均而非 t-一致；不能直接控制 g_χ=L'/L | 只能作为“族正交性”的弱证据 |
| **Level-aspect 四阶矩** | M. P. Young, *The fourth moment of Dirichlet L-functions*, Ann. of Math. 173 (2011), 1–50：对素数模 q 给出 `Σ_{χ mod q}|L(1/2,χ)|⁴` 的渐近公式（常数与 CFKRS 随机矩阵预测一致）[事实，未逐字核对系数] | 对角、χ-平均、L 而非 L'/L；不覆盖条带上的 t-一致 L² 核 | LL 需要的是双变量 L'/L 核的 L²，不是单个 L 的四阶矩 |
| **L'/L 高阶矩（固定点）** | S. Ghosh, *Moments of Higher Logarithmic Derivatives and Exceptional Zeros in Cyclotomic Fields*, arXiv:2509.06390（2025-09-08；v2 2026-07）：对非主 Dirichlet 特征，给出 `L^{(r)}(1,χ)` 的高阶矩渐近；摘要原文：“prove arithmetic formulas for the higher derivatives L^{(r)}(1,χ) and establish unconditional moment asymptotics for P^{(a,b)}(L^{(r)}(1,χ)) as χ runs over non-principal Dirichlet characters of large prime conductor” | 固定点 s=1、χ-平均；不是条带 Re s∈(1/log N,1/8)、不是 t-一致、不是跨 χ 4 点 | 方向相近但对象不同；phase-4 报告还引用了 Ihara 的 L'/L(1,χ) 结果（本报告未逐字核对） |
| **Selberg 中心极限（q-aspect）** | M. Das, *Selberg's Central Limit Theorem for Dirichlet L-functions of q-aspect*, arXiv:2105.01251（2021-05-04）：摘要“We give a simple proof of Selberg's central limit theorem for Dirichlet L-functions for q-aspect by following the method established by Radziwiłł–Soundararajan.” | 给出 `log|L(1/2,χ)|` 的**分布**（Gaussian CLT），不是 L'/L 的算子范数/一致估计 | 支持“族随机性”启发式，不能作证明输入 |
| **S(t) 的 level-aspect 类似** | Q. Sun & H. Wang, *On a level analog of Selberg's result on S(t)*, arXiv:2407.14867：对素数 level q 的权 2 Hecke 尖形式，给出 S(t,f) 矩的无条件渐近与加权 CLT（normalized by √log log q） | 是 GL(2) 权形式族、S(t) 统计；不是 Dirichlet L 模 N 族、不是 L'/L 核 | 说明 level-aspect 统计工具存在但形式不匹配 |
| **1-level density（低零）** | Iwaniec–Luo–Sarnak, *Low lying zeros of families of L-functions*, Publ. IHÉS 91 (2000)：族平均 1-level density，对 Fourier 变换支撑受限的检验函数成立（q→∞）[事实，具体支撑未逐字核对] | 只控制受限检验函数下的**平均**零点统计；不足以给对所有 t 的 L² 核 | 受限支撑是本质限制（等价于 prime tuples 型信息） |
| **Pair correlation（level aspect）** | Montgomery 1973 对 ζ 的 pair correlation 仍是**猜想**；Dirichlet L 的全强度 pair correlation 只有条件性结果（[推测] 受限检验函数/有限高度的弱无条件版本可能存在，但不足以给 R）：Kandhil–Languasco–Moree, *Pair correlation of zeros of Dirichlet L-functions…*, arXiv:2411.19762（2024-11-29；Math. Ann. 2026, DOI 10.1007/s00208-026-03383-y）摘要原文：“**Assuming** the Generalized Riemann Hypothesis **and a pair correlation conjecture** for the zeros of Dirichlet L-functions, we establish … Montgomery … and … Elliott–Halberstam.” | **这正是 R 需要的类型**；但它是**假设**，不是已证定理 | 若有人证明 level-aspect pair correlation（或其弱形式），R 可能有路；目前这是猜想 |
| **零点密度估计** | 经典无零区/密度定理（Heath-Brown 1992; Xylouris; Pintz 的 log-free density theorem）[事实] | 只给“坏零点不太多”的弱估计；Montgomery–Vaughan/Pintz 用它做到 X^{1−δ}；对 N^{-1/2} 族平均核远远不够 | 弱于 pair correlation；不能给逐 t 的 L² 控制 |
| **AFE / Perron 恒等式** | LL Lemma 6.4：`−L'/L(u,χ)=Σ_{n≤N/2}Λ(n)χ(n)n^{-u}w_X(n)+(1/log x)Σ_ρ(X^{ρ−u}−x^{ρ−u})/(ρ−u)²`（严格恒等式，[事实]）；phase-4 报告证明“AFE+正交性只能看到截断对角，缺失的 Ω((log N)²) 无可用的 √N 抵消” | 已试过的路线；失败原因是**对角质量记账**，不是 AFE 合法性 | phase-4 结论（本报告引用，不复核） |
| **Mollifier / amplification / resonance** | Iwaniec–Sarnak 型 mollifier 用于非零比例（[事实]）；Soundararajan 的 resonance method 给 L 值**下界** | 给非零/下界方向；不能给 E_N 的上界；resonance 可用来**下界** ‖T_N‖（检验 R 是否可能为假） | 方向相反；可做 R 的“证伪工具” |
| **2026 新指数和** | Maynard–Pandey–Radziwiłł arXiv:2608.14777：`|Σ_{n<N}Λ(n)e(nα)| ≤ N^{o(1)}(N/B^{1/2}+N^{19/24})`（取代 Vinogradov N^{4/5}）[预印本主张] | 改进的是圆法 minor arcs → E(X) 的 7/12（Pintz–Althöfer）；不是 LL 的 χ-族 L² 核 | 若走圆法/显式公式路线有用；对 LL 核非直接 |
| **族迹公式 / Weil 正性** | phase-4 报告结论：单变量乘性 Weil 正性不适用于双变量加性核；“张量 Weil 正性”只对每因子非负的和式保正 | 不能直接给 R；族版本的迹公式正性恰等价于 pair correlation 型输入（[推测]） | 与上表 pair correlation 一行呼应 |

### 2.4 最小可证输入（把 R 归约成一句“可陈述的猜想”）

综合 §2.2–2.3，[推导] 若接受以下估计，则 R（至少其 HS 版本）成立：

> **(H_fam)** 对每个充分大的偶数 N，在 Hardy 条带 `S_N` 的两条边界线上，有
> (i) `Σ_{χ∈X_N^-} ∫_{S_N} |g_χ(s)|² |ds| ≪ φ(N)(log N)^A`;
> (ii) `Σ_{χ≠ψ∈X_N^-} |⟨g_χ,g_ψ⟩|² ≪ φ(N)^{2−c}`（某 c>0，或 ≪ φ(N)²/(log N)^B）;
> 其中内积为 `⟨g_χ,g_ψ⟩=∫_{S_N} g_χ(s)\overline{g_ψ(s)} w(s)|ds|`，且估计对所有需要的 t 一致。

则 `‖P_N‖_HS ≪ N^{-1/2}(log N)^{A/2}`（若 (ii) 足够强），从而 T_N 的残差达到 δ_N 尺度（再需 D_N/K_N 的精确抵消，LL 已证）。

**(H_fam) 与已知猜想的关系：**
- (i) 是“族二阶矩”，比 (ii) 弱；在 GRH 下可由零点密度/L'/L 的逐点界给出**很弱**的版本（这正是 LL 定理 6.2 的 `(log N)²` 的来源），但常数/幂次远不够。
- (ii) 是“跨特征标 4 点相关”，与 level-aspect pair correlation（Kandhil–Languasco–Moree 的假设）同一层级；[推测] 证明 (ii) 至少和证明该 pair correlation 的一部分一样难。
- **(H_fam) 弱于 Hardy–Littlewood 逐 N 猜想**，也弱于 Goldbach；因此即使 R 被证明，它仍是一个有意义的中间定理，但证明它需要新的族相关技术。

---

## 3. 2026 年动态（截至 2026-11-21）

### 3.1 LL 系列论文的后续/批评

- **[事实/预印本]** Li & Liu 条件性证明：2026-11-13 发布于山东大学 MRC（63 页，PDF 创建时间 2026-11-13 03:06 +08；未上 arXiv；未见同行评审）。截至 2026-11-21，检索中英网络（arXiv API、web search、知乎、头条、mathchina、themitbbs）**没有发现正式批评、勘误或独立核验**。中文讨论存在：知乎问题“继发布「1+1.9定理」后，刘建亚、李嘉旻新给出哥德巴赫猜想的首个条件性证明？这意味着什么？”（https://www.zhihu.com/question/2104680319357907490，2026-11 中；抓取遇 403 需登录，仅据搜索摘要）；头条/科普文章标题如“1+1被攻破了吗?…首个条件性证明”（https://m.toutiao.com/article/7708062452621099560/）、“哥德巴赫没被攻克，但这篇论文厉害在哪”（https://www.toutiao.com/article/7708978933819064883/）。这些属于科普/讨论，不是核验。
- **[事实]** LL 的 (1+1.9) 预印本 arXiv:2606.05224v2（2026-08-08）继续作为“无条件越过 1+2 边界”的 2026 记录；未发现后续改进该指数的公开工作（截至 2026-11-21 检索）。
- **[推测]** 条件性论文的最大风险不在 GRH（若 Alpöge 成立可消去），而在 Hypothesis S/R 本身：它们是关于全新算子谱的假设，既无证明也无已知反例；数值附录只验证 N=30030 的有限模型，明言“does not certify Hypothesis R for T_{30030,1}”。

### 3.2 RH/GRH 核验进展

- **[事实]** MIT 核验页（https://math.mit.edu/~drew/grh/）在 2026-11-21 的抓取内容与 2026-11-20 22:05 UTC 版本一致：编译/公理审计/leanchecker/nanoda/con-leche/lean4lean 全 pass；**`lake comparator` 和 Lean default/paranoid kernel replay 仍 running**（页面自身说明会更新）。**尚未同行评审**；页面 caveat 明确“A passing check shows that the formal statements … follow from the three standard axioms according to the kernels used. It relies on those kernels and on Mathlib's definitions being what they are intended to be.” 以及 “GRH here means Dirichlet L-functions only.”
- **[事实/预印本主张]** 竞争性声明：Scientific American “Dueling claims of Riemann hypothesis proofs emerge”（https://www.scientificamerican.com/article/dueling-claims-of-riemann-hypothesis-proofs-emerge/）；Masullo 的“The Music of the Primes”以及 PhilArchive 上 J. L. Nielsen 的《A Failure of Uniform Boundedness in Masullo's Proposed Proof of the Generalized Riemann Hypothesis》（https://philarchive.org/rec/NIEIOM，未评审）——这些不影响本报告结论，但提醒“GRH 已证”不能当作既成事实引用。

### 3.3 2026 年其他相关数学进展

- **[预印本主张]** OpenAI Math Release（2026-09-30，family 003）《The Quasi-Riemann Hypothesis: A Zero-Free Half-Plane Re s > 7/8》Theorem 1.1：ζ 与所有 Dirichlet L 无 Re s>7/8 的零点；主结果已 Lean 形式化。状态跟踪：Cairn Commons 指南“OpenAI's October 2026 math proofs: what is claimed, what is checked”（https://cairn-commons.com/guides/openai-math-proofs-october-2026，updated 2026-11-08）把 quasi-Riemann hypothesis 列为 **“Claimed, unreviewed”**，并注明 “Main result formalized; the 11/12 companion is not”；四个头条结果“As of 8 November 2026, none of these four has been through independent expert review.” 后续：[预印本] arXiv:2610.15291（Yuanda Xu, Hejian Sang, 2026-10-11）摘要原文：“Recently, OpenAI announced a uniform 7/8 zero-free half-plane for finite-order Hecke L-functions over ℚ(√−3), together with its transfer to Dirichlet L-functions. **Assuming the analytic inputs of that work**, we improve the boundary from 7/8=0.875 to 8748867/10000000=0.8748867…”——注意这是**条件于 OpenAI 解析输入**的改进。
- **[预印本主张]** Pintz–Althöfer arXiv:2610.15559（2026-10-11）：7/12 结果（见 §1.2）；用 OpenAI quasi-RH 作外部输入；**明确声明** “This draft takes the uniform Dirichlet statement in [6] as an external input; it does not reprove that result.” 以及“The ε-loss is retained throughout: we do not assert E(X)≪X^{7/12} without it.”
- **[预印本主张]** Maynard–Pandey–Radziwiłł arXiv:2608.14777（2026-08-14）：素数指数和 19/24（见 §1.2）。
- **[事实]** 综述：G. Bhowmik & L. Grimmelt, *The exceptional set of the Goldbach problem*, arXiv:2607.27282（2026-07，33 页）——包含 HL 条件定理、MV、Pintz 方法、新显式公式与 Siegel 零点关联（§8：Goldbach 表示数的稀疏 HL 型假设可以排除 exceptional zeros；引用 Fei, Pintz–Halupczok, Jia, Goldston–Suriajaya, Friedlander–Goldston–Iwaniec–Suriajaya, Matomäki–Merikoski 等工作）。这是目前最好的入口综述。
- **[预印本]** 其他 2026 Goldbach 相关：arXiv:2610.29470（*The exceptional set of Goldbach numbers within the set of squares*，2026-10，范围窄，不改变上述图景）；Zenodo/preprints.org 上仍有若干“完整证明”预印本（无评审、不采用）。
- **[事实] 用 Alpöge 机器（Stepanov/theta lift/Hermitian curvature/Weil 正性）处理加性问题的公开尝试：未找到。** 检索 arXiv/web（2026 年 6–11 月）没有发现把该证明的机械用于 Goldbach/孪生/加性相关的论文或预印本；task-19 对本地 repo 的扫描将给出更直接的证据。

---

## 4. 评估：如果 R 渐近为真，LL 路线是否“可行”？

### 4.1 逻辑上

- **[推导]** 若 Hypothesis R 成立（对所有充分大偶数 N，`‖T_N‖≤δ_N`），则 LL Theorem 1.2 给出 `G(N)=c_φS(N)+O(δ_N)`，即对所有 N≥N₀ 有正表示数；N<N₀ 的有限范围可用直接枚举验证（N₀~10⁶ 远小于已验到的 4×10^18，计算上平凡）。所以 **R ⇒ 二元 Goldbach**（只要 N₀ 有限且可计算）。
- **[推导]** 反过来，不需要整个 R：phase-4 定理 A 指出，只需要 LL 固定权 φ 的加权二元 HL 渐近（带误差 ≪δ_N）在单个二次型方向上成立，就足以推出 Goldbach；R 是一个更强的、全方向的充分条件。因此即使 R 在某个 N 处为假，减弱的路线仍可能存活。
- **[推导]** 若 R 为假（真算子的 ‖T_N‖/δ_N 有子列 >1），LL 的 Theorem 1.2 不能给出 Goldbach；但 Q_N 可能仍 <δ_N（因 Q_N 是特定向量方向），所以 **R 假不等于 LL 路线死**，只是它的“最简充分条件”失效。

### 4.2 证明 R 需要的本质输入

按 §2.4，本质输入是 **(H_fam)：χ 族的二阶矩 + 跨 χ 非对角四阶相关**。这是一种 **level-aspect pair-correlation / 跨特征标零点相关**型信息：

- 它比 GRH 强：GRH 是逐 L 的零点位置，**不控制不同特征标之间的相关**；
- 它比 Montgomery pair correlation（ζ）的 level-aspect 类比同一层级；该 pair correlation 目前是猜想（Kandhil–Languasco–Moree 明确把它作为假设）；
- 它比 Goldbach 本身弱（只是一个族平均算子范数），但**没有已知定理**能推出它；
- 可能的替代输入：族迹公式（Kuznetsov/相对迹公式）的某种正性/上界，或“大筛 + 零点密度”的强化——都需要新想法。

### 4.3 距离与判据

- **[推测]** 与现有技术的距离：**远**。ζ 的 pair correlation 自 1973 年起是猜想，level-aspect 版本只有条件性结果；LL 需要的还是一致到 t 的二阶/四阶族相关。即便 R 数值上渐近为真（task-13/14/17 待确认），把它变成定理也需要一篇独立的强分析论文，而不是本项目能完成的“精化”。
- **可操作的中间目标（建议的判据）：**
  1. 证明 **HS 版本的 R**（更弱）：`‖T_N‖_HS ≤ δ_N`；所需 (H_fam) 只需 L² 平均，不需要全方向算子范数——仍是新定理，但可能是第一步。
  2. 证明 **条件性 R**：`GRH + pair correlation (level aspect) ⇒ ‖T_N‖≤δ_N`；这条能立即与 Kandhil–Languasco–Moree 的假设框架接口，是可发表的定理形态。
  3. 若数值显示 R 在某个 N 处真为假：转而证明“弱化的 R”（二次型方向）或寻找 LL 框架的修正（例如换权 φ、换 Hardy 条带、换范数）。
  4. 无论哪条，都需要**先**确认有限模型发现的 N^{-1/2} 趋势是否真实算子行为（task-13/17 的结论）；本报告不对数值下结论。

### 4.4 对“在 RH 基础上证明 Goldbach”的最终回答（文献层面）

- RH/GRH 本身不蕴含 Goldbach（task-3 已论证，LL 论文 §1.1 明文确认）。
- 2026 年的状况是：**GRH 已足够把 Goldbach 的问题压缩为“一个特定 χ-族算子核的 N^{-1/2} 相消问题”**（Li–Liu 条件性框架），而该问题等价于一个 level-aspect 的族相关估计——这是目前已知的、最接近 Goldbach 的“RH+额外结构”路线；但额外结构（S/R 或 (H_fam)）本身**远超现有技术**，且 RH 证明（若成立）不会自动给出它。
- 另两条路（圆法例外集、筛法 1+1.9→1+1）在 2026 年都有进展，但都被同一个“almost-all/parity”墙挡住，不能到达“所有偶数”。

---

## 5. 引用清单（URL/DOI，访问日期 2026-11-21）

**Goldbach 例外集（当代）**
1. G. Bhowmik, L. Grimmelt, *The exceptional set of the Goldbach problem*, arXiv:2607.27282（2026-07）。https://arxiv.org/abs/2607.27282
2. J. Pintz, I. Althöfer, *The Goldbach exceptional set: an exponent of 7/12 and conditional refinements*, arXiv:2610.15559（2026-10-11）。https://arxiv.org/abs/2610.15559
3. G. Zhao, *The exceptional set of Goldbach problem and Linnik's constant*, arXiv:2511.05631（2025-11-07；v2 2026-01-23）。https://arxiv.org/abs/2511.05631
4. J. Maynard, M. Pandey, M. Radziwiłł, *Exponential sums over primes*, arXiv:2608.14777（2026-08-14）。https://arxiv.org/abs/2608.14777
5. J. Pintz, *A new explicit formula in the additive theory of primes with applications II. The exceptional set in Goldbach's problem*, arXiv:1804.09084v2（2018）。https://arxiv.org/abs/1804.09084
6. J. Pintz, *A new explicit formula … I*, Acta Arithmetica 210 (2023), 53–94; doi:10.4064/aa220728-31-3；预印本 arXiv:1804.05561。
7. H. L. Montgomery, R. C. Vaughan, *The exceptional set in Goldbach's problem*, Acta Arith. 27 (1975), 353–370。
8. G. H. Hardy, J. E. Littlewood, *Some problems of 'Partitio Numerorum', V*, Proc. London Math. Soc. (2) 22 (1924), 46–56；*III*, Acta Math. 44 (1923), 1–70。
9. D. A. Goldston, *On Hardy and Littlewood's contribution to the Goldbach conjecture*, Amalfi Conf. Proc. (1989), 115–155, Univ. Salerno, 1992。
10. D. A. Goldston, A. I. Suriajaya, *On a smoothed average of the number of Goldbach representations*, arXiv:2306.04807（2023）。https://arxiv.org/abs/2306.04807
11. T. Estermann, *On Goldbach's problem: Proof that almost all even positive integers are sums of two primes*, Proc. London Math. Soc. (2) 44 (1938), 307–314；J. G. van der Corput, Acta Arith. 2 (1937), 266–290；N. G. Čudakov, Izv. Akad. Nauk SSSR 2 (1938), 25–40。
12. R. C. Vaughan, *On Goldbach's problem*, Acta Arith. 22 (1972), 21–48。

**GRH 与 L 函数工具**
13. H. L. Montgomery, R. C. Vaughan, *Multiplicative Number Theory I: Classical Theory*, Cambridge Studies in Advanced Mathematics 97, CUP 2007（§18.3 “Conditional estimates”）。
14. M. P. Young, *The fourth moment of Dirichlet L-functions*, Ann. of Math. (2) 173 (2011), 1–50。
15. M. Das, *Selberg's Central Limit Theorem for Dirichlet L-functions of q-aspect*, arXiv:2105.01251（2021-05-04）。https://arxiv.org/abs/2105.01251
16. Q. Sun, H. Wang, *On a level analog of Selberg's result on S(t)*, arXiv:2407.14867（2024-07-20）。https://arxiv.org/abs/2407.14867
17. S. Ghosh, *Moments of Higher Logarithmic Derivatives and Exceptional Zeros in Cyclotomic Fields*, arXiv:2509.06390（2025-09-08；v2 2026-07）。https://arxiv.org/abs/2509.06390
18. N. Kandhil, A. Languasco, P. Moree, *Pair correlation of zeros of Dirichlet L-functions: a possible path towards the conjectures of Chowla, Elliott–Halberstam and Montgomery*, arXiv:2411.19762（2024-11-29；Math. Ann. 2026, doi:10.1007/s00208-026-03383-y）。https://arxiv.org/abs/2411.19762
19. H. Iwaniec, W. Luo, P. Sarnak, *Low lying zeros of families of L-functions*, Publ. Math. IHÉS 91 (2000), 55–131。
20. H. L. Montgomery, *The pair correlation of zeros of the zeta function*, Proc. Sympos. Pure Math. 24 (1973), 181–193。
21. H. Iwaniec, E. Kowalski, *Analytic Number Theory*, AMS Colloq. Publ. 53, 2004（大筛、L 函数均值、圆法）。
22. D. R. Heath-Brown, *Zero-free regions for Dirichlet L-functions, and the least prime in an arithmetic progression*, Proc. London Math. Soc. (3) 64 (1992), 265–338；T. Xylouris, arXiv:0906.2749。

**Li–Liu / Alpöge / 2026 生态**
23. J. Li, J. Liu, *A Conditional Proof of the Goldbach Conjecture*, Shandong Univ. MRC, 2026-11-13（63 pp）。https://mrc.sdu.edu.cn/english/info/1018/1514.htm；http://mrc.sdu.edu.cn/info/1018/2193.htm 。未上 arXiv；未见评审。
24. J. Li, J. Liu, *Theorem (1+1.9) on the Goldbach Conjecture*, arXiv:2606.05224v2（v1 2026-06-01；v2 2026-08-08）。https://arxiv.org/abs/2606.05224
25. L. Alpöge, *remark.pdf*（2026-11-20）。https://alpo.ge/remark.pdf
26. A. Sutherland, *RH Lean proof: verification files*, MIT。https://math.mit.edu/~drew/grh/（last updated 2026-11-20 22:05 UTC）
27. OpenAI Math Release, family 003, *The Quasi-Riemann Hypothesis: A Zero-Free Half-Plane Re s > 7/8*, 2026-09-30（经 Pintz–Althöfer [6] 引用；主结果 Lean 形式化）。状态参考：Cairn Commons, *OpenAI's October 2026 math proofs: what is claimed, what is checked*, updated 2026-11-08。https://cairn-commons.com/guides/openai-math-proofs-october-2026
28. Y. Xu, H. Sang, *Amplified moments and a refinement of the quasi-Riemann hypothesis*, arXiv:2610.15291（2026-10-11）。https://arxiv.org/abs/2610.15291
29. *Dueling claims of Riemann hypothesis proofs emerge*, Scientific American（2026-11）。https://www.scientificamerican.com/article/dueling-claims-of-riemann-hypothesis-proofs-emerge/ ；J. L. Nielsen, PhilArchive（未评审）https://philarchive.org/rec/NIEIOM
30. 中文讨论：知乎问题“继发布「1+1.9定理」后，刘建亚、李嘉旻新给出哥德巴赫猜想的首个条件性证明？这意味着什么？”https://www.zhihu.com/question/2104680319357907490 （抓取 403，仅据搜索摘要）；头条“1+1被攻破了吗?…” https://m.toutiao.com/article/7708062452621099560/ 。

**本团队内部报告（引用其已核结论）**
31. `_rh-work/goldbach-attack/phase4/afe-attack.md`（task-11：AFE 失败点、最小条件定理 A/B）。
32. `_rh-work/goldbach-attack/phase4/independent-audit.md`（task-12：R 可证伪性、平均结果、文献指针）。
33. `_rh-work/goldbach/report.md`（task-3：RH/GRH 与 Goldbach 的基础文献与逻辑边界）。

---

## 附录 A：关键原文引用（便于 Lead 直接引用）

1. **GRH ⇒ E(X)≪X^{1/2+ε}（一般 Θ 形式）**，arXiv:2607.27282 §3：
> “Theorem 3.1 (Hardy–Littlewood, conditional exceptional-set bound). Assume that every zero of every Dirichlet L-function has real part at most Θ < 3/4. Then for every ε > 0 we have |E(X)| ≪ε X^{2Θ−1/2+ε}.”

2. **θ=1/2 即 GRH 情形**，arXiv:2610.15559 Theorem 3：
> “Assume H_θ for a fixed 1/2 ≤ θ ≤ 2/3. For every ε > 0, E(X) ≪_{θ,ε} X^{g(θ)+ε}, g(θ) = θ(5−4θ)/(2(2−θ)).”

3. **无条件记录**，arXiv:2511.05631 摘要：
> “We prove the bound E(X)=O(X^{7/10}), where the implicit constant is ineffective.”

4. **7/12 与 OpenAI 输入**，arXiv:2610.15559 摘要/Corollary 2：
> “We prove E(X) ≪ε X^{7/12+ε} whenever all Dirichlet L-functions have a common fixed zero-free half-plane Re s > θ₀, with θ₀ < 1. The uniform 7/8 theorem reported in the OpenAI mathematics release supplies this input.”
> “Corollary 2 (Application of the 7/8 theorem). On invoking the uniform Dirichlet L-function theorem of OpenAI [6, Theorem 1.1], one obtains E(X) ≪ε X^{7/12+ε}.”

5. **19/24 指数和**，arXiv:2608.14777 摘要（见 §1.2）。

6. **pair correlation 是假设**，arXiv:2411.19762 摘要：
> “Assuming the Generalized Riemann Hypothesis and a pair correlation conjecture for the zeros of Dirichlet L-functions, we establish the truth of a conjecture of Montgomery (in its corrected form stated by Friedlander and Granville) … As a consequence … the Elliott–Halberstam conjecture holds true.”

7. **Selberg CLT q-aspect**，arXiv:2105.01251 摘要：
> “We give a simple proof of Selberg's central limit theorem for Dirichlet L-functions for q-aspect by following the method established by Radziwiłł and Soundararajan.”

8. **L'/L 矩（固定点）**，arXiv:2509.06390 摘要：
> “… we prove arithmetic formulas for the higher derivatives L^{(r)}(1,χ) and establish unconditional moment asymptotics for P^{(a,b)}(L^{(r)}(1,χ)) as χ runs over non-principal Dirichlet characters of large prime conductor.”

9. **OpenAI quasi-RH 状态**，Cairn Commons 指南（updated 2026-11-08）：
> “Quasi-Riemann hypothesis — No zeros of the Riemann zeta function or of any Dirichlet L-function with real part above 7/8 … Lean: Main result formalized; the 11/12 companion is not. Status: Claimed, unreviewed.”
> “As of 8 November 2026, none of these four has been through independent expert review.”

10. **MIT 核验页状态**（2026-11-21 抓取，last updated 2026-11-20 22:05 UTC）：
> “The `lake comparator` run and the Lean-kernel replay of the export are still in progress.”
> “GRH here means Dirichlet L-functions only.”

11. **LL 的 GRH-alone 声明**（arXiv 条件性论文 §1.1）：
> “No proof of the binary conjecture is known under the generalized Riemann Hypothesis (GRH) alone, even when GRH is assumed for all Dirichlet L-functions.”

12. **LL 的 GRH 不足量级**（同文 §1.2/§2.4.3）：
> “In fact, GRH alone already gives a zero-free region for X_N of the same form. Its width, however, falls short of that required by Hypothesis S, so the resulting estimate is not strong enough to make the Goldbach error o(S(N)).”
> “The available norm bound is too large to make the Goldbach error smaller than its main term; S and R impose the required improvement.”

---

## 附录 B：本报告的核查方式与局限

- **已抓取并逐字核对**：arXiv:2607.27282（PDF 全文）、arXiv:2610.15559（PDF 全文）、arXiv:2511.05631（API 摘要）、arXiv:2608.14777（API 摘要）、arXiv:2306.04807（API 摘要）、arXiv:2105.01251（API 摘要）、arXiv:2407.14867（API 摘要）、arXiv:2509.06390（API 摘要）、arXiv:2411.19762（API 摘要）、arXiv:2610.15291（API 摘要）、MIT 核验页、Cairn Commons 指南、MRC Li–Liu 页面、本地 LL PDF 文本。
- **未逐字核对**（仅据二次引用/记忆，已在正文标注）：Young 2011 四阶矩的精确常数形式；Iwaniec–Luo–Sarnak 1-level density 的精确支撑范围；Montgomery pair correlation 的精确陈述；Goldston 1992 的对数幂 c 的精确值；Hardy–Littlewood 1924 原文定理形式（通过 Pintz 2018 和综述转述核对）。
- **检索局限**：WSL 下 github.com 与 Wikipedia 不可达（任务 20 会另行处理）；部分中文页面（知乎/头条）需登录或动态加载，仅引用标题/搜索摘要；arXiv 检索在批量 API 调用时偶有限流，正文引用均来自单次成功抓取或综述原文。
- **未做**：没有验证 LL 论文的数学正确性（task-4 已做）；没有对 phase-5 数值趋势下结论（task-13/14/17）；没有验证 OpenAI/Alpöge 的任何证明（内容超出本任务）。
