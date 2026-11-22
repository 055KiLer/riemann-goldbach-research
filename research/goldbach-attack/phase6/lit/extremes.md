# Phase-6 文献调研：Dirichlet 族极值/大偏差、随机协方差算子范数、2026 动态

> 作者：goldbach-researcher（task-24）。日期：2026-11-21 19:17–20:10（Asia/Shanghai）。访问日期均 2026-11-21。
> 任务：解释 LL 路线的经验量 `C(N)=λ_max(T_N)·√N/√S(N) ∝ (log N)^a`（a∈[1.2,2.2]，临界 3/2）的文献背景；找 Dirichlet 字符族极值/大偏差、随机协方差算子范数偏差工具、2026 动态与经典族最大涨落结果。
> 标注：**[事实]** 已证/已发表；**[预印本主张]** 未评审；**[猜想]**；**[推导]**；**[推测]**；**[数值]**。只写文献，不对 task-21/22 的数值下结论。

---

## 0. 五条要点（已先发 lead）

1. **level-aspect 的 CLT/大偏差已证，但对象是 L 值而非 L'/L**：Selberg CLT 的 q-aspect 版本（Das, arXiv:2105.01251, 2021）；大偏差上界（Arguin–Creighton, arXiv:2405.20888, 2024）：对 V~α log log q (0<α<1)，`(1/φ(q))·#{χ even primitive mod q : log|L(χ,1/2)|>V} ≪ e^{−V²/log log q}/√(log log q)`。据此对“族最大值”的启发式是 `log|L|_max ≈ √(log q·log log q)`（[推测]），**不是 (log q)^{1.5}** 型 log 幂。
2. **L'/L 的极值文献只有下界/Ω 型且多条件性**：Lamzouri–Languasco《Small Values of |L'/L(1,χ)|》（Exp. Math., 2021/22，DOI 10.1080/10586458.2021.1927255）；Dong–Li, arXiv:2603.21256（2026-03）用 resonance method 得条件 Ω 结果（改进 Mortada–Murty、推广 Yang）；Dong–Wang–Wang–Zhang–Zhao, arXiv:2610.24958（2026-10）在 GRH 下给二次特征 L 的导数大值下界。**没有** `max_{χ mod q}|L'/L(1/2+α_N,χ)|` 的渐近/上界定理。LL 条带 `Re=α_N=1/log N` 上 L'/L 的 log 幂增长更可能来自**零点密度**（GRH 下 `L'/L=Σ_ρ1/(s−ρ)+O(log q)`；单位高度零点数 ≍ log q；α_N=1/log N ⇒ 近零点的 1/α_N 放大）——这是 [推导/推测]，与 a≈1.5 的定量核对应放在 task-22。
3. **对 a 的最直接线索其实在模型算子 Q_N=D_N+K_N**：用 Lead 的 `phase6/lead/qscale.log` 数据粗算 [数值]：logN 10.597→21.416（×2.021）时 lQ=‖Q_N‖ 16.45→48.25（×2.933），b = ln(2.933)/ln(2.021) ≈ **1.53**，恰在临界 3/2。若随机协方差启发式 `λ_max(T_N)≈κ‖Q_N‖/√n`（n=φ/2）成立，则 `C≈2κ‖Q_N‖/√S`，即 a≈b≈1.5。**结论：C(N) 的 log 幂主要应由确定性 Q_N 解释，而不是“族中最大涨落”。**
4. **随机协方差算子范数偏差工具**：Koltchinskii–Lounici（Bernoulli 2017，sample covariance 集中/矩界）、Adamczak–Litvak–Pajor–Tomczak-Jaegermann（JAMS 2010，log-concave）、Vershynin（非渐近随机矩阵/High-Dimensional Probability）、Bai–Yin（Ann. Probab. 1993，谱端点）、Tropp（矩阵 Bernstein）、Mackey–Jordan–Chen–Farrell–Tropp（exchangeable pairs, Ann. Probab. 2014）等给出 `‖Σ̂−Σ‖ ≲ ‖Σ‖(√(r_eff/n) ∨ r_eff/n)`（r_eff=trΣ/‖Σ‖）。**但它们要求 i.i.d./独立/可交换/混合**；字符族是确定性正交设计，**不能直接套用**。可借用的只是启发式模板与 r_eff 诊断（Q_N 的 r_eff≈11.9，N=2×10⁸，见 §4）。
5. **2026 动态**：MIT 核验页已更新到 **2026-11-21 09:30 UTC**。注意区分：(i) 主 RH 证明自身：leanchecker/nanoda/con-leche/lean4lean 全 pass，但 **`lake comparator` 与 Lean default/paranoid kernel replay 仍 running**；(ii) 新增的“Arithmetic consequences”部分把主证明与 kimihiro64/Robin1984（独立的 Robin/Lagarias 判据形式化）合并，得到无假设、不提及 ζ 的 robin_inequality/lagarias_inequality，**Robin1984 子项目本身通过了 Unmodified Comparator（“Your solution is okay!”，03:31 UTC）与 lake comparator from exports（04:16:52 UTC）**；合并导出 con-leche/nanoda accept、其 lake comparator running。**仍无人类同行评审**、caveats 保留。未发现 LL 后续/正式批评，未发现 Alpöge 机器用于加性问题。2026 年新增 relevant：Gou–Wang–Xu, arXiv:2611.18825（Landau 问题/比值猜想；函数域无条件 Goldbach 渐近）；Kandhil–Languasco–Moree, arXiv:2607.14515（pair-correlation 超越 GRH 界）；Bober–Goldmakher 族最大 character sum 分布（arXiv:1110.0078）；Lamzouri 2026 大值（arXiv:2606.09818）。经典族极值尺度是 `√q log log q` / `log log q`，不是 `(log q)^{1.5}`。

---

## 1. 要解释的对象与三种可能来源

LL 路线（task-3/4 报告）把 Goldbach 归约为 `‖T_N‖≤δ_N`（Hypothesis R），`δ_N=√(S(N)/N)(log N)^{3/2}`。phase-5/6 的有限模型给出

  `C(N) = λ_max(T_N)·√N/√S(N) ∝ (log N)^a`，a∈[1.2,2.2]，临界 3/2。

可能有三种来源（本报告分别核对文献）：

- **(A) 确定性模型算子 `Q_N=D_N+K_N` 的增长**：`λ_max(T_N)` 的随机协方差图像中，样本协方差涨落 ~ `‖Q_N‖/√n`，故 `C ~ ‖Q_N‖/√S` 的 log 幂。Lead 的 qscale 数据（§4）给出 `‖Q_N‖ ≍ (log N)^{1.53}`（[数值]），直接支持这一支。
- **(B) 随机协方差的有效秩/偏差**：`‖Σ̂−Σ‖ ≈ ‖Σ‖·√(r_eff/n)`，若 r_eff 随 N 缓增则 C 额外获得 log 幂。
- **(C) 族极值（max over χ）**：某个或少数 χ 的 |L'/L| 异常大，抬高 λ_max。本报告的主要结论是：**文献中能描述“族极值”的尺度与 (log N)^{1.5} 不匹配**（见 §2–§5），(C) 不太可能是主因；但 (B) 的 r_eff 增长值得数值检验。

---

## 2. Level-aspect 的 CLT 与大偏差（L 值）

### 2.1 Selberg 中心极限定理的 q-aspect

- **[事实]** Selberg (1946) 对 ζ 证明 CLT（log|ζ(1/2+it)| 在 t 方向正态，方差 ~ (1/2)log log T 的规模）；Radziwiłł–Soundararajan 的方法简化/推广。
- **[事实]** Dirichlet L 的 q-aspect CLT：M. Das, *Selberg's Central Limit Theorem for Dirichlet L-functions of q-aspect*, arXiv:2105.01251（2021-05-04）。摘要原文：
  > “We give a simple proof of Selberg's central limit theorem for Dirichlet L-functions for q-aspect by following the method established by Radziwiłł and Soundararajan.”
  即：当 χ 在 mod q 的本原特征中随机时，`log|L(1/2,χ)|` 的分布趋于均值为 0、方差 ~ (1/2)log log q 的高斯（典型值：|L| ≈ (log q)^{N(0,1/2)}，q^{o(1)}）。

### 2.2 q-aspect 大偏差（已在文献中定量化）

- **[预印本/事实候选]** L.-P. Arguin, N. Creighton, *Upper Bounds on Large Deviations of Dirichlet L-functions in the q-aspect*, arXiv:2405.20888（2024-05-31）。摘要原文：
  > “For V~α log log q with 0<α<1, we show that
  > (1/φ(q))·#{χ even, primitive mod q : log|L(χ,1/2)| > V} ≪ e^{−V²/log log q}/√(log log q).
  > This yields the sharp upper bound for the fractional moments … proved by Gao …”
- **[推导] 族最大值的启发式**：把“顶到 1/q 分位”当作 `φ(q)/2 ≍ q` 个样本中的最大值：
  `e^{−V²/log log q}/√(log log q) ~ 1/q` ⇒ `V ≈ √(log q·log log q)`，即
  `log max_{χ mod q}|L(1/2,χ)| ≈ √(log q·log log q)`（[推测]；只有上界方向被 Arguin–Creighton 证明，匹配下界未见）。
  **这个尺度（exp(√(log q log log q))）远大于任何固定 log 幂，与 C(N) 的 (log N)^a 不同。**

### 2.3 在 σ>1/2 的“大值”下界（level aspect）

- **[预印本]** Y. Lamzouri, *A note on large values of Dirichlet L-functions for characters of fixed order at 1/2<σ≤1*, arXiv:2606.09818（2026-06-08）。摘要原文：
  > “for every fixed integer g≥2 we prove the existence of a primitive character χ of order g and conductor Q≍x such that
  > |L(1,χ)| ≥ e^γ(log log x + log log log x − log(2 log g) + o(1)).
  > … for every fixed 1/2<σ<1 there exists a primitive character χ of order g and conductor Q≍x such that
  > log|L(σ,χ)| ≥ (C_g(σ)+o(1))(log x)^{1−σ}(log log x)^{−σ}, …”
  即族内大值在 σ=1 是 log log 级别，在 1/2<σ<1 是 (log x)^{1−σ} 级别。注意 σ→1/2 时 `(log x)^{1−σ}` 会变成 log x 的正幂（σ 固定时是 log 幂，但指数 1−σ 随 σ 变化）；**这不是 L'/L 在临界线附近的算子范数控制**。
- 相关 2026 大值文献：P. Gao, *Large values of quadratic Dirichlet L-functions of prime-related moduli*, arXiv:2606.15635；P. Gao, L. Zhao, *Large values of cubic and quartic Dirichlet L-functions of prime moduli*, arXiv:2609.02392；Z. Dong 等, *Large values of quadratic Dirichlet L-functions near the central point*, arXiv:2508.12205。它们给大值的 Ω 型下界/矩，不是上界/渐近。

### 2.4 对 C(N) 的判断

**[推导]** 若 C(N) 主要由“族最大 |L| 或 |L'/L|”决定，那么它的对数增长率应是 `√(log N log log N)`（L 值，中心点）或 `log log N` / `(log N)^{1−σ}`（σ>1/2），量级完全不同。**因此 (C) 不太可能解释 (log N)^{1.5}。** 但注意：LL 的核涉及 L'/L 而不是 L，且是在 Re=1/logN（紧贴临界线）的条带上积分；这个对象的族极值理论在文献中基本空白（见 §3）。

---

## 3. L'/L 的极值、小值与矩（与 LL 核最相关）

### 3.1 已知结果

- **[事实]** Y. Lamzouri, A. Languasco, *Small Values of |L'/L(1,χ)|*, Experimental Mathematics（2021/2022），DOI 10.1080/10586458.2021.1927255。研究固定点 s=1 处 |L'/L(1,χ)| 的小值/分布。
- **[预印本]** Z. Dong, H. Li, *Large values of logarithmic derivatives of quadratic Dirichlet L-functions*, arXiv:2603.21256（2026-03-22）。摘要原文：
  > “In this article, we apply the resonance method to derive conditional Omega results for logarithmic derivatives of quadratic Dirichlet L-functions. We improve a previous result of Mortada and Murty, as well as generalize some results of Yang.”
  即：L'/L 的大值**下界**（Ω 结果），条件性（resonance/GRH 型）；改进 Mortada–Murty (2013?)、推广 Yang (2023)。
- **[预印本]** Z. Dong, R. Wang, W. Wang, H. Zhang, S. Zhao, *Large values of derivatives of quadratic Dirichlet L-functions*, arXiv:2610.24958（2026-10-18）：在 GRH 下，用 GCD sums/有限 Euler 积给出固定阶导数在 1/2≤σ≤1 的大值下界；中央点处各阶导数与同一 square-free GCD sum 比较；mesoscopic band σ=1/2+A/log₂X 用 resonator。→ 这是最接近“临界线附近 L'/L 大值”的 2026 工作，但仍是下界、条件性、非族最大值渐近。
- **[事实]** 固定点 L'/L(1,χ) 的其他工作：Ihara（L'/L(1,χ) 分布/均值）；phase-4 报告引用了 Ihara 的京都 IMS preprint（本报告未逐字核对）。
- **[事实]** 经典 L'/L 矩：Gonek 关于 ζ 的 L'/L 矩、Selberg 的 S(t) 理论；对 Dirichlet 族的“条带上跨 χ 的 L'/L 二阶/四阶矩”**没有**现成定理（phase-4 audit 结论一致）。

### 3.2 为什么 LL 核里会出现 log 幂：零点密度机制 [推导/推测]

在 GRH 下，对固定的 χ（mod q=q(N)）：

  `L'/L(1/2+s,χ) = Σ_ρ 1/(s−ρ) + O(log q)`（ρ 遍历非平凡零点，按重数）。

LL 取 `Re s = α_N = 1/log N`（以及另一条边界 `β=1/8`）。在高度 t∈[0,H] 内每单位高度的零点数约 `(1/2π)log(q(|t|+2)/(2π)) ≍ log q`。离临界线距离 α_N 处，最近零点的贡献量级 `1/α_N = log N`；若把窗口内 ~log q 个零点的贡献看作随机相消（随机游走），典型量级为

  `|L'/L| ≈ √(log q)·log N`。

当 `q ≍ N` 时这正好是 `(log N)^{3/2}`。**这提供了一个自然的 a=3/2 机制**：零点个数（log q）开方 × 贴线距离的放大（1/α_N = log N）。但若零点近似等距而非随机，则 `Σ 1/(α_N+i(t−γ))` 的实部相消后可能是 `log q · log log N`，指数仍是 1+o(1)；积分/取范数后还可能再变化。**文献中没有把这一机制写成定理（对族平均/HS 范数）；这是 task-22 应该定量化的对象。**

---

## 4. 经典“族中最大涨落”结果（character sums 与 L(1,χ)）

这些是题面第 (4) 项；结论是它们的尺度与 C(N) 的 log 幂不匹配，但提供重要类比。

- **[事实] Pólya–Vinogradov（1918）**：对非主特征 χ mod q，`|Σ_{n≤x}χ(n)| ≤ √q log q`（对所有 x）。
- **[事实] Paley（1932）**：存在二次特征 χ mod q，使 `max_x |Σ_{n≤x}χ(n)| ≫ √q log log q`（下界）。这是“族极值”最经典的“√q × log log q”现象。
- **[事实]** Granville–Soundararajan, *Large character sums*, J. Amer. Math. Soc. 14 (2001), 365–397：大 character sums 的构造与猜想；Bober–Goldmakher, *Pólya–Vinogradov and the least quadratic nonresidue*, arXiv:1311.7556 / Math. Ann.（2016）：把最大 character sum 与最小二次非剩余联系，给出（在假设/无条件范围）`M(χ)` 与 `(e^γ/(π√3))√q log log q` 的比较（详见其论文/相关讲义）。
- **[事实]** Bober–Goldmakher, *The distribution of the maximum of character sums*, arXiv:1110.0078（2011）：摘要原文 “We obtain explicit bounds on the moments of character sums, refining estimates of Montgomery and Vaughan. As an application we obtain results on the distribution of the maximal magnitude of character sums normalized by the square root of the modulus, finding **almost double exponential decay in the tail** of this distribution.” → 族最大 character sums 的分布理论：尾是双指数衰减，典型尺度 √q（乘 log log q 修正）。
- **[事实]** Bober–Goldmakher–Granville–Koukoulopoulos, *The frequency and the structure of large character sums*, arXiv:1410.8189（2014）：大 character sums 的频率/结构。
- **[预印本]** A. P. Mangerel, *On a conjecture of Goldmakher*, arXiv:2605.29111（2026-05-27）：构造 1-bounded completely multiplicative f 否定 Goldmakher (2009) 的一个猜想——说明该领域 2026 年仍活跃，且“族大值”问题远未封闭。
- **[事实]** Y. Lamzouri, *Extreme values of arg L(1,χ)*, arXiv:1005.4425 / Acta Arith. 146 (2011)：primitive χ mod q 变化时 arg L(1,χ) 的极值分布。
- **[事实]** B. Hough, *The angle of large values of L-functions*, arXiv:1304.1241（2013）：带角度约束的 Ω 结果。
- **[预印本]** Kandhil–Languasco–Moree, *Beyond the Riemann Hypothesis bounds: A pair-correlation approach to the least prime in arithmetic progression and the smallest quadratic non-residue*, arXiv:2607.14515（2026-07-16）：用零点 pair correlation 超越 GRH 界；与 2411.19762 同一路线。→ **pair correlation 是“超越 GRH”的已知入口**，也是 §6 评估中 R 所需输入的同级假设。

**小结 [推导]**：上述“族最大值”全部是 `√q`（乘 log log q）或 `log log q` 量级，来自 character sums / L(1,χ) 的结构；**它们不产生 (log q)^{1.5} 型的族极值**。因此 C(N) 的 log 幂不应归因于 (C) 族极值。

---

## 5. 随机协方差算子范数偏差：定理与“依赖样本”问题

### 5.1 已证工具（i.i.d./独立情形）

| 工具 | 精确形式（典型） | 条件 | 能否用于字符族 |
|---|---|---|---|
| Koltchinskii–Lounici, *Concentration inequalities and moment bounds for sample covariance operators*, Bernoulli 23 (2017), 110–133 | `E‖Σ̂_n−Σ‖ ≲ ‖Σ‖(√(r(Σ)/n) ∨ r(Σ)/n)`，`r(Σ)=trΣ/‖Σ‖`；并有集中不等式 | i.i.d. 次高斯/有界样本 | **否**（需独立） |
| Adamczak–Litvak–Pajor–Tomczak-Jaegermann, *Quantitative estimates of the convergence of the empirical covariance matrix in log-concave ensembles*, J. Amer. Math. Soc. 23 (2010), 535–561 | 类似 `√(r/n)` 型界 | i.i.d. log-concave | **否** |
| Vershynin, *Introduction to the Non-asymptotic Analysis of Random Matrices*（2012）/ *High-Dimensional Probability*（CUP 2018） | 次高斯矩阵谱范数 `O(√n)`；协方差集中 | i.i.d. 子高斯行 | **否**（但提供模板） |
| Bai–Yin, *Limit of the smallest eigenvalue of a large dimensional sample covariance matrix*, Ann. Probab. 21 (1993), 1275–1294 | 大维样本协方差谱端点极限（Marchenko–Pastur 型） | 独立高斯/一般 i.i.d. | **否**（渐近 RMT） |
| Tropp, *User-friendly tail bounds for sums of random matrices*, Found. Comput. Math. 12 (2012), 389–434 | 矩阵 Bernstein/Laplace 变换型尾界 | 独立和（或鞅） | 部分：若能把族分解为独立块 |
| Mackey–Jordan–Chen–Farrell–Tropp, *Matrix concentration inequalities via the method of exchangeable pairs*, Ann. Probab. 42 (2014), 906–945 | 用 exchangeable pairs 给矩阵集中 | 可交换对（弱于独立） | **可能**是处理“族依赖”的最现实模板；但字符族没有自然可交换对 |

### 5.2 字符族的“依赖”结构

**[事实/推导]** 字符族 `{χ mod N}` 不是随机样本：`g_χ(s)=L'/L(1/2+s,χ)` 有精确的代数关系（函数方程、共轭、非本原诱导），Gram 矩阵 `⟨g_χ,g_ψ⟩` 的期望由字符正交 `(2/φ)Σχ(n)χ̄(m)=1(1_{n≡m}−1_{n≡−m})` 决定（LL Lemma 3.1，也是大筛的算术对应物），**不是 i.i.d. 的协方差模型**。因此：

- Koltchinskii–Lounici 型定理**不能直接给出** `λ_max(T_N)` 的界；它们只能解释“若把 {f_χ} 当作独立样本”时的预期尺度 `‖Q‖√(r_eff/n)`（[推测] 模板）。
- 可用的诊断量：`r_eff(Q)=trQ/‖Q‖`。从 Lead qscale.log（N=200000014，H=8,m=2）：`trQ=240.9047`，`hsQ=69.7743`（若 hsQ=‖Q‖_HS=√(tr Q²)），则 `tr(Q²)=4868.4`，`r_eff=trQ²/tr(Q²)≈11.9`；N=40022 时 `trQ=88.962, hsQ=26.835 ⇒ tr(Q²)=720.1, r_eff≈10.99`。**r_eff 仅从 ~11 缓增到 ~12（logN 10.6→21.4）**，即 `r_eff` 的 log 斜率 ≈ ln(12/11)/ln(2.02)≈0.12。若 `C` 中来自随机涨落的因子是 `√(r_eff)`，它只给 ~(logN)^{0.06}，**远不足以制造 a 从 1.5 到 2 的差异**；a 的 log 幂更可能来自 `‖Q_N‖` 本身（b≈1.53）和/或 LL 的 HS 常数。
- 另外，“采样不足”修正：n=φ/2≈N/2 远大于 r_eff，随机协方差偏差 `√(r_eff/n)` 中的 n^{-1/2} 正是 λ_max(T_N) 相对 ‖Q‖ 的 N^{-1/2} 因子——与 phase-5 的 `λ∝N^{-1/2}` 一致。

### 5.3 可借用的“依赖样本”思路（都不是现成定理）

- **exchangeable pairs / 鞅**（Tropp 2012；Mackey et al. 2014）：若能把字符族按模数/共轭/诱导关系分成可交换块，可能得到分布无关的界；目前没有人这样做。
- **大筛取代独立性**：字符正交/大筛是算术版的“正交样本”工具；它给对角和平方和，但也只到二阶矩层面，off-diagonal 需要零点相关（pair correlation）——回到 §6。
- **随机模型文献**：arXiv:2611.14579 *Random Chowla and Goldbach Conjectures*（2026-11-10，I. Pylaiev）与 arXiv:2605.29111 之类工作用随机模型解释 Goldbach/Chowla；这类模型可作为“有效秩”启发式的依据，但不是定理。

---

## 6. 2026 动态（截至 2026-11-21 20:00）

### 6.1 RH Lean 核验进展（MIT 页，已更新）

**[事实]** https://math.mit.edu/~drew/grh/ 页面 **last updated 2026-11-21 09:30 UTC**（本报告 2026-11-21 19:2x 抓取；本地存档 phase6/mit-recheck/mit/page_text.txt）。当前状态必须分三层引用：

1. **主 RH+GRH 证明自身**：编译/公理审计/leanchecker（175,187 模块）/nanoda/con-leche（含 --compare）/lean4lean 全 pass；但页面主表明确 **`lake comparator` end-to-end 与 Lean default/paranoid kernel replay 仍 running**（单线程、导出 61.57 GB，预计很久）。
2. **新增“Arithmetic consequences”区块**：把主证明与 kimihiro64/Robin1984（commit acab1a3，独立的 Robin/Lagarias 判据形式化，同一 Lean/Mathlib 版本）合并，得到两个**无假设、不提及 ζ** 的定理：
   - `robin_inequality`：∀ n > 5040, σ(n) < e^γ n log log n；
   - `lagarias_inequality`：∀ n > 0, σ(n) ≤ H_n + e^{H_n} log H_n。
   这是“不依赖 Mathlib 对 ζ 的定义”的交叉检验。
3. **Robin1984 子项目/合并导出**（注意：这些 pass **不是**主证明的 comparator）：
   - “Robin1984 builds with lake build | pass | 4,435 jobs, exit 0”
   - “con-leche master and --compare | accepts | 69,293 declarations …”
   - “**Unmodified Comparator v4.33.0 with the repository's own config | pass | nanoda accepts, Lean default kernel accepts, ‘Your solution is okay!’; exit 0 at 03:31:06 UTC**”
   - “**lake comparator (Lean v4.36.0) from exports | pass | … ‘Your solution is okay!’; exit 0 at 04:16:52 UTC**”
   - 合并导出（61,752,134,938 bytes）：robin/lagarias 编译+公理 pass；con-leche/nanoda accept；**其 lake comparator 仍 running**（单线程、62 GB 导出）。
4. **结论**：主证明的独立内核/导出核验很充分；但**标准 Comparator 与 Lean 默认内核重放尚未完成**，且**仍无人类同行评审/人类数学检查**（页面 caveats：unsandboxed provenance 等仍适用）。这不改变 Goldbach 的结论（task-3/16），但引用时必须写“claim/形式核验进行中”，不能写成“已完全官方核验”。

### 6.2 Li–Liu 后续/批评

- 检索 arXiv（标题/作者/摘要）、Google 系搜索、知乎/头条：**未发现** 2026-11-13 条件性证明的正式后续、勘误或批评；LL (1+1.9) arXiv:2606.05224 仍为 v2（2026-08-08）。中文讨论仍停留在科普/论坛层面（task-16 报告 §3.1）。
- 推断：LL 条件性论文未上 arXiv、未评审，其 Hypothesis S/R 仍无独立验证。

### 6.3 新的 Goldbach 相关工作（2026-09 → 2026-11）

| 论文 | 内容 | 状态 |
|---|---|---|
| H. Gou, V. Y. Wang, M. W. Xu, *Landau's problems through ratios of L-functions*, arXiv:2611.18825（2026-11-13） | 在 Ratios Conjecture 下给 Landau 四问题的条件渐近（power-saving 误差）；**函数域**用 Sawin 的 squarefree 进估计 + discriminant cohomology 得**无条件** Goldbach/prime-pair 渐近（充分大固定奇函数域，含素域）；提到 Lee 在 Ratios Conjecture 下宣布 Twin Prime 证明 | **[预印本主张]**；函数域结论是 2026 新的无条件结果（但函数域 ≠ ℤ） |
| I. Pylaiev, *Random Chowla and Goldbach Conjectures*, arXiv:2611.14579（2026-11-10） | 随机模型下的 Chowla/Goldbach 猜想 | **[预印本]**，与随机模型/R 的启发式相关 |
| K. Qazaqzeh, A. Rawashdeh, *An Elementary Proof of the Binary Goldbach Conjecture*, arXiv:2611.09007（2026-11-06） | 宣称初等证明二元 Goldbach；摘要称“证明 Goldbach 对数为 O(n/log²n)” | **[未核验声明]**，**不可依赖**：其上界方向是已知的筛法上界，不能推出正性；arXiv 通过≠正确 |
| A. Perelli, J. Pintz, *The exceptional set of Goldbach numbers within the set of squares*, arXiv:2610.29470（2026-10-21） | 平方数集合内的 Goldbach 例外集 | **[预印本]**，范围窄，不改变总体图景 |
| N. Kandhil, A. Languasco, P. Moree, *Beyond the Riemann Hypothesis bounds: A pair-correlation approach …*, arXiv:2607.14515（2026-07-16） | 用 pair correlation 超越 GRH 界（最小 AP 素数、最小二次非剩余） | **[预印本/事实候选]**；说明 pair correlation 是“超越 GRH”的已知入口 |
| Z. Zhang, *Equivalence between the pair correlation functions of primes and the four-point correlation function*, arXiv:2508.14938v4 | 素数 pair correlation 与零点四阶相关的等价 | **[预印本]**；与“跨 χ 四阶相关”的工具相关 |

### 6.4 把 Alpöge/Claude 机器用于加性问题

**[事实]** 检索 arXiv/web（2026-06→2026-11）：**没有**发现把 Stepanov/theta lift/Hermitian curvature/Weil 正性等 Alpöge 证明机器用于 Goldbach/加性问题的公开工作。task-19（phase-5）的 repo 扫描也未发现任何 Goldbach 相关定理；预计 phase-6 的 task-28 会再次确认“只有定性 GRH，无跨特征标相关估计”。

---

## 7. 对 phase-6 的结论与判据

**[推导/推测]**

1. **C(N) 的 log 幂不能由“族极值”文献解释。** Dirichlet 族的极值/大偏差理论给出的是 `√q log log q`（character sums）、`log log q`（L(1,χ)）、`√(log q log log q)`（L(1/2,χ) 的最大值启发式）、`(log q)^{1−σ}`（σ>1/2 大值）等尺度；没有任何定理给出“族最大值 ∝ (log q)^{1.5}”。
2. **最自然的解释是 (A)：确定性模型算子 Q_N=D_N+K_N 的 log 幂**。用 Lead qscale.log 的 [数值]：`‖Q_N‖` 从 16.45（logN=10.6）到 48.25（logN=21.4），b≈1.53，恰在临界 1.5。随机协方差模板 `λ_max(T_N)≈κ‖Q_N‖/√n` 把它翻译成 `C≈2κ‖Q_N‖/√S`，a≈b。斜率 a 的最终值由 task-22 的解析 b 与 task-21 的 far-N 数值决定；本报告只提供文献背景与 r_eff 诊断。
3. **r_eff 不是主因**：[数值] r_eff(Q) 从 ~11.0（N=40022）到 ~11.9（N=2×10⁸），log 斜率 ~0.12；即使 C 含 √r_eff 也只增加 (logN)^{0.06}。若数值上 a 明显偏离 b，需检查是否 H/mesh/m=2 截断引起（task-17/21）。
4. **若要把 C 的增长变成定理（进而 R 的证明），文献里唯一现成的入口是 pair correlation / 跨 χ 四阶相关**（Kandhil–Languasco–Moree 2024/2026/2026；Zhang 2025）；但那是猜想，不是定理。随机矩阵工具（Koltchinskii–Lounici 等）只适用于独立样本，字符族是依赖设计，不能直接套用。
5. **给 Lead 的建议**：(i) task-22 用 `Q_N` 解析推导 b（D_N 的 1/w² 奇性 + 条带宽度 1/logN + K_N 的 Beta 连续化），并数值验证 b≈1.5 是否对 H/mesh/m 稳定；(ii) 拟合 `a=b+γ` 时把 `ln r_eff` 作为协变量；(iii) 若 a 与 b 在误差内一致，则 R 的“渐近为真”图像主要由确定性模型解释，证明 R 仍需 off-diagonal 估计（与 phase-5 task-16 的结论一致），但至少 C(N) 的增长率不再是“族极值”造成的谜团。

---

## 8. 引用清单（URL/DOI；访问日期 2026-11-21）

**CLT/大偏差/大值（level aspect）**
1. M. Das, *Selberg's Central Limit Theorem for Dirichlet L-functions of q-aspect*, arXiv:2105.01251（2021）。https://arxiv.org/abs/2105.01251
2. L.-P. Arguin, N. Creighton, *Upper Bounds on Large Deviations of Dirichlet L-functions in the q-aspect*, arXiv:2405.20888（2024-05-31）。https://arxiv.org/abs/2405.20888
3. Y. Lamzouri, *A note on large values of Dirichlet L-functions for characters of fixed order at 1/2<σ≤1*, arXiv:2606.09818（2026-06-08）。https://arxiv.org/abs/2606.09818
4. P. Gao, *Large values of quadratic Dirichlet L-functions of prime-related moduli*, arXiv:2606.15635（2026-06-14）；P. Gao, L. Zhao, *Large values of cubic and quartic Dirichlet L-functions of prime moduli*, arXiv:2609.02392（2026-09-02）。
5. Z. Dong, Z. Li, Y. Song, S. Zhao, *Large values of quadratic Dirichlet L-functions near the central point*, arXiv:2508.12205（2025-08-17）。

**L'/L 极值**
6. Y. Lamzouri, A. Languasco, *Small Values of |L'/L(1,χ)|*, Experimental Mathematics（2021/2022），DOI 10.1080/10586458.2021.1927255。https://www.tandfonline.com/doi/full/10.1080/10586458.2021.1927255
7. Z. Dong, H. Li, *Large values of logarithmic derivatives of quadratic Dirichlet L-functions*, arXiv:2603.21256（2026-03-22）。https://arxiv.org/abs/2603.21256
8. Z. Dong, R. Wang, W. Wang, H. Zhang, S. Zhao, *Large values of derivatives of quadratic Dirichlet L-functions*, arXiv:2610.24958（2026-10-18）。https://arxiv.org/abs/2610.24958
9. Y. Lamzouri, *Extreme values of arg L(1,χ)*, arXiv:1005.4425；Acta Arith. 146 (2011)。
10. B. Hough, *The angle of large values of L-functions*, arXiv:1304.1241（2013）。https://arxiv.org/abs/1304.1241

**character sums 族极值**
11. G. Pólya（1918）；I. M. Vinogradov（1918）；R. E. A. C. Paley（1932）（经典，见教科书 Montgomery–Vaughan §23? / Iwaniec–Kowalski）。
12. A. Granville, K. Soundararajan, *Large character sums*, J. Amer. Math. Soc. 14 (2001), 365–397。
13. J. Bober, L. Goldmakher, *The distribution of the maximum of character sums*, arXiv:1110.0078（2011）。https://arxiv.org/abs/1110.0078
14. J. Bober, L. Goldmakher, *Pólya–Vinogradov and the least quadratic nonresidue*, arXiv:1311.7556；Math. Ann.（2016）。
15. J. Bober, L. Goldmakher, A. Granville, D. Koukoulopoulos, *The frequency and the structure of large character sums*, arXiv:1410.8189（2014）。https://arxiv.org/abs/1410.8189
16. A. P. Mangerel, *On a conjecture of Goldmakher*, arXiv:2605.29111（2026-05-27）。https://arxiv.org/abs/2605.29111

**随机协方差 / 矩阵集中**
17. V. Koltchinskii, K. Lounici, *Concentration inequalities and moment bounds for sample covariance operators*, Bernoulli 23 (2017), 110–133。
18. R. Adamczak, A. Litvak, A. Pajor, N. Tomczak-Jaegermann, *Quantitative estimates of the convergence of the empirical covariance matrix in log-concave ensembles*, J. Amer. Math. Soc. 23 (2010), 535–561。
19. R. Vershynin, *Introduction to the Non-asymptotic Analysis of Random Matrices*（2012）；*High-Dimensional Probability*（CUP 2018）。
20. Z. D. Bai, Y. Q. Yin, *Limit of the smallest eigenvalue of a large dimensional sample covariance matrix*, Ann. Probab. 21 (1993), 1275–1294。
21. J. A. Tropp, *User-friendly tail bounds for sums of random matrices*, Found. Comput. Math. 12 (2012), 389–434。
22. L. Mackey, M. I. Jordan, R. Y. Chen, B. Farrell, J. A. Tropp, *Matrix concentration inequalities via the method of exchangeable pairs*, Ann. Probab. 42 (2014), 906–945。

**2026 动态**
23. MIT RH Lean 核验页：https://math.mit.edu/~drew/grh/（last updated 2026-11-21 09:30 UTC；本地存档 phase6/mit-recheck/mit/）
24. H. Gou, V. Y. Wang, M. W. Xu, *Landau's problems through ratios of L-functions*, arXiv:2611.18825（2026-11-13）。https://arxiv.org/abs/2611.18825
25. I. Pylaiev, *Random Chowla and Goldbach Conjectures*, arXiv:2611.14579（2026-11-10）。https://arxiv.org/abs/2611.14579
26. K. Qazaqzeh, A. Rawashdeh, *An Elementary Proof of the Binary Goldbach Conjecture*, arXiv:2611.09007（2026-11-06）——**未核验，不可依赖**。https://arxiv.org/abs/2611.09007
27. A. Perelli, J. Pintz, *The exceptional set of Goldbach numbers within the set of squares*, arXiv:2610.29470（2026-10-21）。https://arxiv.org/abs/2610.29470
28. N. Kandhil, A. Languasco, P. Moree, *Beyond the Riemann Hypothesis bounds: A pair-correlation approach …*, arXiv:2607.14515（2026-07-16）。https://arxiv.org/abs/2607.14515
29. Z. Zhang, *Equivalence between the pair correlation functions of primes and the four-point correlation function*, arXiv:2508.14938v4（2025-08-20）。https://arxiv.org/abs/2508.14938
30. 本团队既有报告：phase-5/lit/lit-and-tools.md（task-16：GRH 条件 E(X)、工具清单、H_fam）；phase-4/afe-attack.md、phase-4/independent-audit.md（task-11/12）。

---

## 附录 A：本报告的核查方式与局限

- **逐字核对/抓取**：arXiv 摘要/PDF：2405.20888、2606.09818、2603.21256、2610.24958、2611.18825、2611.14579、2611.09007、2610.29470、2607.14515、1110.0078、1005.4425、1304.1241、1311.7556、1410.8189、2605.29111、2508.12205、2606.15635、2609.02392、2105.01251（摘要）；MIT 页 page_text（本地存档）与 refetch；Lead 的 phase6/lead/qscale.log 原始数据（本报告 §4 的 b、r_eff 计算均基于它，属[数值]）。
- **未逐字核对/仅据引用链**：Paley 1932、Pólya–Vinogradov 原文；Granville–Soundararajan 2001 的精确定理编号；Bober–Goldmakher 2016 Math. Ann. 的卷期；Koltchinskii–Lounici/Adamczak 等精确常数；Lamzouri–Languasco 的精确陈述（仅摘要/标题级）；Selberg 1946 原文。
- **检索局限**：WSL 下 github.com/Wikipedia 不可达；部分页面需登录/动态加载；arXiv API 偶发限流。
- **未做**：没有验证 LL 论文正确性（task-4）或 phase-6 数值（task-21/22/25）；没有把“a≈b≈1.5”当作已证结论，只作为 [数值/推导] 线索。
