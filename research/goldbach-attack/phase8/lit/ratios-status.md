# Phase-8：两条 Goldbach 替代路线的输入现状与精确 gap 表

> 作者：goldbach-researcher（task-32）。日期：2026-11-21 20:44–20:55（Asia/Shanghai）。URL 访问日期 2026-11-21。
> 目标：量化 phase-7 推荐的两条路线距离"可用输入"还差多少：
> **(A)** Ratios Conjecture 路线（Gou–Wang–Xu arXiv:2611.18825：GRH + RC_D(ω_D) ⇒ Goldbach）；
> **(B)** 函数域模板的 ℤ 版：(I) 平方自由 AP 中素数分布水平 >1/2；(II) 两点 Möbius/Chowla 的 power-saving 平均。
> 标注：**[事实]** 已证/已发表；**[预印本]** 未评审；**[推导]**；**[推测]**；**[检索结果]** 未找到/弱证据。
> 前置：phase7/lit/alternative-routes.md（路线全文）；task-30 报告。

---

## 0. 五条要点 + gap 表（已发 lead）

1. **RC_D(ω_D) 的精确要求**（G-W-X Hypothesis 1.1）：固定 0<ω_D≤1/2，存在 η_0>0,B≥0，使对每个 0<η<η_0 和每个 ε>0，
   `Σ*_{χ mod q} L(a,χ)L(b,χ)/(L(s,χ)L(t,χ)) = M_q(a,b;s,t) + O_{η,ε}(q^{1−ω_D+ε}(1+T)^B)`
   对所有导子 q>1（含复合）、`Re a=Re b=1/2, Re s=Re t=1/2+η, T=max{|Im a|,|Im b|,|Im s|,|Im t|}≤100 log(2q)` 一致。**G-W-X 原文：“Any fixed ω_D>0 suffices for Theorem 1.1.”** 因此只需要“任意小但正的 power saving”，不需要 ω_D=1/2。
2. **ℚ 上没有任何 ω_D>0 的已知结果**。已知最好的是：条件性后果（Conrey–Snaith 2005/2007）；低阶项/矩的一致性（Bui–Keating 2006 对 Dirichlet L 的 2k 阶矩 hybrid Euler–Hadamard）；**受限检验函数下的 1-level density 验证**（Goes 等 2009：Dirichlet L 素数导子族，Fourier 支撑 (−1,1) 平方根一致、(0,−2,2) 有 power saving 一致）；**实 Dirichlet 特征的单 shift ratios（GRH 下，受限范围）**（Čech 2021/Trans. AMS 2024）；**二次/三次/四次 Hecke 族单 shift（GRH 下，受限范围）**（Gao–Zhao 2023–24）。函数域：Sawin, Acta Math. 233 (2024) 对 harmonic families 证明平方根相消——这是 G-W-X 无条件的基石。**Gap：从“ω_D=0（无 saving）”到“任意 ω_D>0”，即整个 Ratios Conjecture 的 2/2 情形在 ℚ 上未证。**
3. **输入 (I)（水平）**：无条件已知 BV 水平 1/2（全模）；BFI 1986 水平 **4/7**（well-factorable 模）；Polymath8b 2014 对光滑平方自由模（CRT 条件）给出 **1/2+7/300**（arXiv:1402.0811 摘要原文），Zhang 2014 为 1/2+1/1168（光滑模）。G-W-X 函数域实际用的是 Sawin [Saw24, Prop. 8.16] **level θ=5/6**。2024–26 **未检索到**用 MPR N^{19/24}/Guth–Maynard 把一般 AP 分布水平推过 1/2 的论文（这些工具改进了零点密度/短区间，不是 BV 水平）。Gap：一般模 1/2→>1/2；记录 4/7→5/6 差 **11/42≈0.262**；且 4/7 只对 well-factorable，1/2+7/300 只对光滑平方自由模。
4. **输入 (II)（两点 Chowla）**：MTT/Matomäki–Radziwiłł–Tao 2015：对固定 k，`Σ_{h1..hk≤H}|Σ_{n≤X}λ(n+h1)…λ(n+hk)| = o(H^k X)`（H→∞, H≤X；定量衰减约 loglog H/logH）；Tao 2015：**对数平均**两点 Chowla（`Σ_{x/ω(x)<n≤x}λ(a1n+b1)λ(a2n+b2)/n = o(log ω(x))`），破 parity barrier 但无 power saving；Tao–Teräväinen 2018：k 点 Chowla（k 奇或 2）对**几乎所有尺度**（例外集对数密度 0）。**没有** ℤ 上的 power-saving 两点 Chowla；2026 年 ACD+26 的 twisted Chowla 是**函数域版**（arXiv:2608.22297）。Gap：从 o(1)（log 速率/对数平均/几乎全尺度）到 X^{−δ}（或 H-平均 power saving）——即 parity barrier 本身。
5. **2026 直接攻 RC_D/Goldbach-via-ratios 的新文**：主线是 G-W-X arXiv:2611.18825（2026-11-13）与 Lee arXiv:2610.32672v2（2026-11-03 revised；restricted uniform zeta-ratios ⇒ fixed even difference prime pairs 的 HL 渐近，ratios 误差 O(U^{ϑ+ε})，1/2≤ϑ<(39−√177)/32≈0.8029；RH 下改善到 x^{ϑ−7/8+ε}）；arXiv 检索 2025–26 未发现其他直接结果。**判断：最值得投入的是路线 A（Ratios）**——目标单一（一个猜想），只需任意小 power saving，函数域已证明、ℚ 上有 GRH-条件的部分族结果和活跃的 multiple-Dirichlet-series 技术；路线 B 的 (II) 是 parity barrier 本体，没有已知路径（函数域靠上同调绕过，ℤ 无对应）。

---

## 1. 输入 A：RC_D(ω_D) 的精确定义、来源与 G-W-X 的需求

### 1.1 定义（G-W-X Hypothesis 1.1，逐字）

**来源**：H. Gou, V. Y. Wang, M. W. Xu, *Landau's problems through ratios of L-functions*, arXiv:2611.18825（2026-11-13），§1.1。

> **Hypothesis 1.1 (Ratios of primitive Dirichlet L-functions (RC_D(ω_D))).** Fix 0<ω_D≤1/2. There exist constants η_0>0 and B≥0 such that for every fixed 0<η<η_0 and every ε>0,
> `Σ*_{χ mod q} L(a,χ)L(b,χ)/(L(s,χ)L(t,χ)) = M_q(a,b;s,t) + O_{η,ε}( q^{1−ω_D+ε}(1+T)^B )`,
> uniformly for all conductors q>1, including composite conductors, and all shifts satisfying ℜa=ℜb=1/2, ℜs=ℜt=1/2+η, `T=max{|ℑa|,|ℑb|,|ℑs|,|ℑt|}≤100 log(2q)`. The starred sum is over primitive characters modulo q. The saving ω_D is independent of η.

**说明（原文 §1.1/§2）**：
- 分子两个 shift 实部 1/2（临界线），分母两个 shift 实部 1/2+η（>1/2）；主项 `M_q` = CFZ 2008 recipe 的 2/2 两个主项之和（diagonal + functional-equation 交换项），在可去奇点处用解析延拓求和。
- 误差是 **power saving** `q^{1−ω_D+ε}(1+T)^B`；`ω_D=1/2` 是“平方根相消”情形（与随机矩阵/CFZ 的预期一致）。
- **G-W-X 原文（§1.1）**：“The case ω_D=1/2 is the square-root error bound for this family. **Any fixed ω_D>0 suffices for Theorem 1.1.**”
- 原始猜想：J. B. Conrey, D. W. Farmer, M. R. Zirnbauer, *Autocorrelation of ratios of L-functions*, Commun. Number Theory Phys. 2 (2008) 593–636, arXiv:0711.0718（CFZ08）。对 ζ 的具体 2/2 形式见 CFZ08 Conjecture 5.1 / Section 6.4（G-W-X 引用为 `M_Z` 的来源）。

### 1.2 从 RC_D 到 Goldbach 的逻辑（G-W-X Theorem 1.1）

> **Theorem 1.1 (Goldbach).** Assume GRH for Dirichlet L-functions, and RC_D(ω_D). For every ε>0 and every even N, we have
> `Σ_{m+n=N} Λ(m)Λ(n) = N𝔖(N) + O_ε(N^{1−ω_D+ε}).`

[推导] 对任意固定 ω_D>0，误差 `N^{1−ω_D+ε}` < 主项 `N𝔖(N)`（𝔖(N)≥c>0，N 偶数），故 N 充分大时表示数 > 0 ⇒ Goldbach。**注意：GRH 现在由 Alpöge/Claude 宣称证明（形式上核验中），所以按本场景，路线的唯一剩余输入就是 RC_D(ω_D) 本身。**

### 1.3 G-W-X 是否接受“更弱的定性版本”？（重要细节）

G-W-X **Appendix A** 给出“Ratios with qualitative errors”版本：
> **Hypothesis 2.4（Zeta ratios with an o(Q) error）** … `∫_0^Q ζ(s+u+iy)ζ(t_0+v−iy)/(ζ(s+iy)ζ(t_0−iy)) dy = M_Z(Q;a,b;u,v) + o(Q)`（uniform shifts 范围见原文 (2.16)）。
> **Hypothesis 2.5（Hecke ratios with an o(1) error）** … `(1/Q)Σ_{1≤k≤Q} L_k(1/2+a)/L_k(1/2+c) = M_H(Q;a,c) + o(1)`（范围见 (2.20)）。

**但 Appendix A 开头明确**：“For prime differences and quadratic values, the power-saving ratios errors in the main theorems can be weakened if only qualitative asymptotics are required. … **The character argument continues to use a positive power saving.**”

**[事实/推导]**：对 **Goldbach**（Dirichlet 族）而言，**定性 o(1) 误差不够**——G-W-X 的 parity-twist + Mellin 反演/特征正交步骤仍需正 power saving。因此路线 A 的最小输入是：
> **RC_D(ω_D) 对某个固定 ω_D>0 成立**（不要求 1/2），在 primitive Dirichlet 族、含复合导子、T≤100 log(2q) 的一致范围内。

---

## 2. RC_D 在 ℚ 上的已知状态（“离目标多远”的核心）

### 2.1 结论先行

**[检索结果/事实]** 在 ℚ 上，**没有任何**关于 primitive Dirichlet L 族 2/2 比值平均的 power-saving 定理；G-W-X 的 RC_D(ω_D) 是**未证猜想**。已知的只是：
1. 各种**条件性后果**（假设 RC 成立，推导别的结论）；
2. **低阶项/矩**的一致性（用 hybrid Euler–Hadamard 等）；
3. **受限检验函数下的 1-level density** 验证（把 ratios 预测与数论计算对比）；
4. **单个 shift** 的 ratios，且只在**受限 range**、对**特殊族**（实特征/二次/三次/四次）且在 **GRH 下**；
5. 函数域上的**完整证明**（Sawin 2024 等）。

### 2.2 逐项证据（精确陈述）

| # | 结果 | 精确陈述/范围 | 状态 |
|---|---|---|---|
| 1 | **CFZ 2008 猜想** | 对 ζ 及一般族给出 2/2 比值平均的 recipe 与主项；Dirichlet 族版本即 G-W-X Hypothesis 1.1 | **[猜想]**（arXiv:0711.0718） |
| 2 | **Conrey–Snaith 2005/2007** | “Applications of the L-functions ratios conjectures”，arXiv:math/0509480；Proc. LMS 94 (2007) 594–646。摘要原文：“In upcoming papers by Conrey, Farmer and Zirnbauer there appear conjectural formulas for averages, over a family, of ratios of products of shifted L-functions. In this paper we will present various applications of these ratios conjectures to a wide variety of problems … such as lower order terms in the zero statistics of L-functions, mollified moments of L-functions and discrete averages…” | **[事实]** 条件性应用（假设 RC，推导后果）；不是 RC 的证明 |
| 3 | **Bui–Keating 2006** | “On the mean values of Dirichlet L-functions”，arXiv:math/0607199（2006）。摘要原文：“We study the 2k-th power moment of Dirichlet L-functions L(s,χ) at the centre of the critical strip (s=1/2), where the average is over all primitive characters χ(mod q). We extend to this case the hybrid Euler-Hadamard product results of Gonek, Hughes & Keating for the Riemann zeta function. This allows us to recover conjectures for the moments based on random matrix models, incorporating the arithmetical terms in a natural way.” | **[事实]** 无条件方法 + 与 ratios/随机矩阵预测一致（moments 层面，不是 2/2 ratios 本身） |
| 4 | **Goes–Jackson–Miller–Montague–Ninsuwan–Peckner–Pham 2009** | “A unitary test of the Ratios Conjecture”，arXiv:0909.4916。摘要原文：“…we verify the conjecture's predictions for the unitary family of all Dirichlet L-functions with prime conductor; we show square-root agreement between prediction and number theory if the support of the Fourier transform of the test function is in (−1,1), and for support up to (−2,2) we show agreement up to a power savings in the family's cardinality.” | **[事实]** 对 **Dirichlet L（素数导子）族的受限检验函数**验证 ratios 预测（这是与 RC_D 最接近的ℚ上证据，但不是 2/2 平均本身） |
| 5 | **Čech 2021 / Trans. AMS 2024** | “The ratios conjecture for real Dirichlet characters and multiple Dirichlet series”，arXiv:2110.04409v3；Trans. Amer. Math. Soc. 377 (2024), no. 5, DOI 10.1090/tran/9113。摘要原文：“We consider the family of **real Dirichlet characters**, and use multiple Dirichlet series to **prove the ratios conjectures with one shift in the numerator and denominator in some range of the shifts**. This range can be improved by extending the family to include non-primitive characters. **All of the results are conditional under the Generalized Riemann hypothesis.** This extended range is good enough to enable us to compute an asymptotic formula for the sum of shifted logarithmic derivatives for some range of the shift.” | **[事实/GRH 条件]** 单 shift、受限 range、实 Dirichlet 族（不是全部 primitive、不是 2/2 一般 shift） |
| 6 | **Gao–Zhao 2022–2024 系列** | 例如 arXiv:2404.05081：“…develop L-functions ratios conjecture with **one shift** in both the numerator and denominator in **certain ranges** for quadratic families of **Dirichlet and Hecke** L-functions of prime-related moduli … **under the generalized Riemann hypothesis**”；另有 quadratic twist、cubic/quartic Hecke 族版本（arXiv:2210.08840, 2304.14600, 2311.08626, 2402.17198） | **[事实/GRH 条件]** 单 shift、受限族/range |
| 7 | **Cho–Park 2018** | “Low-lying zeros of cubic Dirichlet L-functions and the Ratios Conjecture”，arXiv:1802.01762：对 Fourier 支撑 (−1,1) 计算 1-level density，并验证与 ratios 预测一致 | **[事实]** 受限检验函数/单族 |
| 8 | **Fiorilli–Miller 2011** | “Surpassing the Ratios Conjecture in the 1-level density of Dirichlet L-functions”，arXiv:1111.3896：对 Fourier 支撑 (−3/2,3/2) 的 1-level density 给出超出 ratios 平方根展开的结果，发现 ratios Conjecture 未预测的新低阶项 | **[事实]** 重要 caveat：ratios recipe 在较大支撑范围可能**不完备**；但这不否定 G-W-X 所需的 2/2 猜想形式 |
| 9 | **函数域（无条件）** | W. Sawin, *Square-root cancellation for sums of factorization functions over squarefree progressions in F_q[t]*, Acta Math. 233 (2024) 285–418（arXiv:2102.09730）：harmonic families 的 Ratios / 平方根相消；另有几何族进展 BDPW23、MPPRW24、Wang24、LLOP26（G-W-X 引用） | **[事实]** 函数域上的完整证明；这是 RC_D 在 ℚ 上“可望而不可即”的对照 |

### 2.3 精确 gap（路线 A）

- **所需**：`RC_D(ω_D)`，某个固定 `ω_D>0`，primitive Dirichlet 族（含复合导子），2/2 shifts，范围 `Re a=Re b=1/2, Re s=Re t=1/2+η, T≤100 log(2q)` 一致。
- **已知最好（ℚ）**：无 power saving 定理。最接近的四类：
  (i) 单 shift ratios（Čech 2024 实特征；Gao–Zhao 二次/三次/四次族）——**GRH 条件 + 受限 range**；
  (ii) 受限检验函数的 1-level density 平方根一致（Goes 等 2009）——**不是 2/2 平均**；
  (iii) moments 与 ratios 预测一致（Bui–Keating 2006）——**间接**；
  (iv) 条件性后果（Conrey–Snaith）——**不构成证据强度**。
- **Gap 的性质**：不是“差一个指数”，而是**整个 2/2 猜想在 ℚ 上未证**；但两个缓和因素：① 只需**任意小** ω_D>0（不需要 1/2）；② 有函数域完整证明（Sawin 2024）与多个 ℚ 上受限版本的活跃技术（multiple Dirichlet series）。
- **Gap 的量化表述**：已知无条件 power-saving 指数 `ω_D = 0`；所需 `ω_D > 0`（任意小）。若按“最接近的定理”比较：Čech/Gao–Zhao 给的是**单 shift、受限 range**，仍非 2/2 一般 shift；Goes 等给的是 1-level density 的平方根（相当于某个投影量）而**非**比值平均本身。故 **gap 表记作“0 vs >0（整个猜想）”，附注“任意小即可”**。

---

## 3. 输入 (I)：平方自由 AP 中素数分布水平

### 3.1 所需（函数域模板中的精确形式）

G-W-X §7（逐字）：
> “For each j≤K and C∈M_j with (C,D)=1 and μ(C)≠0, **Sawin's estimate [Saw24, Proposition 8.16 at level θ = 5/6]** gives
> `Σ_{F∈M_n, F≡−σD mod C} Λ(F) = q^n/Φ(C) + O_q(q^{(n−j)(1−δ_q)})`, `δ_q = 1/2 − log_q(352e)` …”

即函数域 (I) 用的是 **水平 θ=5/6**、平方自由模 C 上的素数分布 + 平方根型 saving `δ_q`。ℤ 版需要的对应物（[推测]）是：对所有（或足够多的）平方自由模 q，`Σ_{q≤Q} max_{(a,q)=1} |ψ(x;q,a)−x/φ(q)| ≪ x/(log x)^A` 在 **Q=x^θ, θ>1/2**、且对必要范围的模成立（具体 θ 阈值由实现决定；函数域取 5/6）。

### 3.2 已知最好水平（ℤ，无条件）

| 结果 | 精确陈述 | 模限制 | 水平 |
|---|---|---|---|
| Bombieri–Vinogradov（1965） | 对任意 A>0，∃B=B(A)：`Σ_{q≤Q} max_{y≤x} max_{(a,q)=1}|ψ(y;q,a)−y/φ(q)| ≪ x/(log x)^A`，`Q=x^{1/2}/(log x)^B` | 所有模 | **1/2** |
| Bombieri–Friedlander–Iwaniec（1986, Acta Math. 156, 203–251） | BV 型估计 | **well-factorable** 模 | **4/7 ≈ 0.5714** |
| Zhang（2014, Ann. of Math. 179） | BV 型估计 | **光滑**模 | **1/2 + 1/1168 ≈ 0.50086** |
| Polymath8b（2014, arXiv:1402.0811） | 摘要原文：“We prove distribution estimates for primes in arithmetic progressions to large **smooth squarefree moduli**, with respect to congruence classes obeying Chinese Remainder Theorem conditions, obtaining an **exponent of distribution 1/2 + 7/300**。” | 光滑平方自由 + CRT 条件 | **1/2 + 7/300 ≈ 0.52333** |
| 2024–2026 新结果 | [检索结果] 未发现把**一般/平方自由 moduli** 的 BV 水平推过 1/2 的论文；MPR arXiv:2608.14777（N^{19/24}）与 Guth–Maynard arXiv:2405.20552 改进的是零点密度/短区间，**未直接给出 BV 水平 >1/2**。检索到 2026 有卷积型 BV/光滑数 AP 工作（如 arXiv:2608.13299 是最大素因子问题，不是水平改进） | — | — |

### 3.3 精确 gap

- **一般平方自由模**：已知最好是无条件 **1/2**（BV，所有模）；**>1/2 全部模未知**。特殊模类到 4/7（well-factorable）或 1/2+7/300（光滑平方自由）。
- **函数域对照**：Sawin 2024 给 **5/6**（平方自由 progression）；G-W-X 直接使用 θ=5/6。
- **数值 gap**：`5/6 − 4/7 = 11/42 ≈ 0.2619`；`5/6 − (1/2+7/300) ≈ 0.30919`；`5/6 − 1/2 = 1/3`。
- **[推导]** 若 ℤ 版框架最终只需要**某个** θ>1/2（而非 5/6），那么 4/7 已提供“>1/2 但仅 well-factorable”的可能入口；但 4/7 与 5/6 之间没有已知提升机制，且 BFI 的 well-factorable 限制不一定覆盖 G-W-X 需要的模类。
- **障碍**：超过 1/2 的分布水平等价于对 `Λ` 的二阶/双线性结构做超-BV 控制，涉及 Elliott–Halberstam 型猜想或零点密度/大筛的实质性突破；目前 MPR/Guth–Maynard 的新指数和 **不**自动给出（[推测] 需要把新的 minor-arc 估计与显式公式/BV 型均值定理结合，尚未见文献）。

---

## 4. 输入 (II)：power-saving 平均两点（twisted）Chowla

### 4.1 已知最好的精确陈述

| # | 结果 | 精确陈述 | 状态 |
|---|---|---|---|
| 1 | **Matomäki–Radziwiłł–Tao 2015**（arXiv:1503.05121） | 摘要原文：Chowla 断言 `Σ_{n≤X}λ(n+h1)…λ(n+hk)=o(X)`；“In this paper … we establish an **averaged version** of this conjecture, namely `Σ_{h1,…,hk≤H} |Σ_{1≤n≤X} λ(n+h1)…λ(n+hk)| = o(H^k X)`” as X→∞, H=H(X)≤X →∞；“Our arguments in fact give quantitative bounds on the decay rate (**roughly on the order of log log H/log H**), and extend to more general multiplicative functions.” | **[事实]** h-平均，o(1)（无 X 的 power saving） |
| 2 | **Tao 2015**（arXiv:1509.05422） | 两点 Chowla 的**对数平均**版本：`Σ_{x/ω(x)<n≤x} λ(a1n+b1)λ(a2n+b2)/n = o(log ω(x))`（任意 1≤ω(x)≤x，ω(x)→∞）；摘要明确 “thus **breaking the ‘parity barrier’** for this problem”（仅对数平均意义）；工具含 entropy decrement argument | **[事实]** 对数平均；**无 power saving** |
| 3 | **Tao–Teräväinen 2018**（arXiv:1809.02518） | 摘要原文：结构定理 + “we establish the k-point Chowla conjecture `E_{n≤X}λ(n+h1)…λ(n+hk)=o(1)` for k odd or equal to 2 for **all scales X outside of a set of zero logarithmic density**.” | **[事实]** 除了对数密度 0 的尺度集；**无 power saving** |
| 4 | **Tao–Teräväinen 2017**（arXiv:1710.02112） | 奇数阶对数平均 Chowla（log-averaged, k 奇数） | **[事实]** 同上，非 power saving |
| 5 | **2026 新平均型 Chowla** | Wang, *Two averaged dynamical generalizations of Chowla's conjecture*, arXiv:2608.16108v4（2026-08）；Wang–Yi, arXiv:2609.14492v2（2026-09）；Wang–Yang, *Dynamical Chowla conjecture for polynomials of several variables*, arXiv:2610.34912（2026-10） | **[预印本]** 动力系统式推广；不提供所需 ℤ 上幂次节省 |
| 6 | **ACD+26 twisted Chowla（函数域版）** | Anderson–Chow–Dietmann–Hokken–Koymans–Lemke Oliver–Sawin–Shusterman, arXiv:2608.22297v2。摘要原文：“we formulate a **twisted function field version of Chowla's conjecture**, and show how Van der Waerden's conjecture reduces to this conjecture for n≥8. Finally, we make significant progress towards this twisted Chowla conjecture…” | **[预印本]** **函数域**；G-W-X 用它作为函数域 (II) 的筛法灵感；不是 ℤ 结果 |

### 4.2 所需形式（函数域模板的 ℤ 版）

**[推导]** 需要的不是 Chowla 本身，而是与 G-W-X 函数域 (II) 对应的 ℤ 版：对（平方自由/仿射）族中的 shifts，
`Σ_{h∈ℋ} |Σ_{n≤X} μ(n)μ(n+h)|² ≪ H X² (log X)^{−δ}`（或更强：`≪ H X^{2−δ'}`），
或 twisted 版本 `Σ_{h}|Σ_{n≤X} μ(n)μ(n+h)χ(n)|²`，在 `H→∞, X→∞` 的合适范围一致成立。函数域中这正是用 cohomological sieve（Wan–Zhang Betti 界、Das–Howe、判别式上同调）得到的“power-saving 两点 Möbius 相关”。

### 4.3 精确 gap

- **已知**：averaged over shifts 的 `o(H^kX)`（衰减 ~ loglog H/log H）[MRT]；对数平均 `o(log ω)` [Tao]；几乎所有尺度 `o(1)` [TT]。
- **所需**：X（或 H）的**多项式 power saving**（δ>0）。
- **Gap 性质**：从“没有 saving”到“某个 δ>0”——这是 **parity barrier 的本体**；[推测] 需要全新的算术/代数结构（如函数域的上同调），短期内看不到路径；这也说明路线 B 不现实。

---

## 5. 2026 年直接攻 RC_D / Goldbach-via-ratios 的新文

| 论文 | 内容 | 状态 |
|---|---|---|
| **Gou–Wang–Xu, arXiv:2611.18825**（2026-11-13） | 本任务核心：GRH+RC_D(ω_D) ⇒ Goldbach（Theorem 1.1）；函数域无条件 Goldbach/prime pairs（Thm 1.5/1.6）；Appendix A 弱化定性版本；Appendix B reciprocal ratios/Chowla | **[预印本]** 未评审 |
| **Lee, arXiv:2610.32672v2**（2026-10-23 首发，revised 2026-11-03） | “The Hardy–Littlewood asymptotic for prime pairs of fixed even difference from a uniform zeta-ratios conjecture”：从 restricted uniform 2/2 zeta-ratios（误差 `O_ε(U^{ϑ+ε})`，`1/2≤ϑ<(39−√177)/32≈0.8029`，四 shift 实部 [3/64,5/64]，虚部 ≤U^ν, ν≤1/4）证明 fixed even h 的 HL 渐近；误差 `O(x^{−Δ(ϑ)+ε})`，`Δ(ϑ)=7/16−ϑ+ϑ/(3−ϑ)>0`；加 RH 改善为 `O(x^{ϑ−7/8+ε})` | **[预印本]**；说明 ratios 技术正在推进（Twin Prime 条件结果） |
| **Čech, arXiv:2110.04409 / Trans. AMS 377 (2024)** | 实 Dirichlet 特征 ratios（单 shift，受限 range，GRH 条件） | **[事实]**（2021 预印本，2024 发表） |
| **Gao–Zhao 系列（2022–2024）** | 二次/三次/四次 Hecke/Dirichlet 族单 shift ratios（GRH 条件，受限 range）；推论：first moment/1-level density | **[事实]** |
| **Bui–Keating 2006；Conrey–Snaith 2007；Goes 等 2009；Cho–Park 2018；Fiorilli–Miller 2011** | 见 §2.2；均非 2/2 Dirichlet 族的 power-saving 定理 | 见上 |

**[检索结果]** arXiv 2025–2026 检索未发现除 G-W-X/Lee 外直接“RC_D ⇒ Goldbach/prime pairs”的论文；Ratios Conjecture 的 ℚ 上进展集中在单 shift/特殊族（Gao–Zhao, Čech）与函数域（Sawin 及几何族）。

---

## 6. Gap 总表（任务要求的交付核心）

| Input | Best known（精确陈述 & range） | Required by G-W-X | Gap factor / 量化 |
|---|---|---|---|
| **RC_D(ω_D)**（primitive Dirichlet 2/2，含复合 q，T≤100 log 2q） | ℚ 上**无** power-saving 定理。最接近：(i) 单 shift 受限 range（Čech 2024 实特征；Gao–Zhao 二次/三次/四次族，均 **GRH 条件**）；(ii) 素数导子 Dirichlet 族的 1-level density 平方根一致（Goes 等 2009，Fourier 支撑 (−1,1)，(−2,2) 有 power saving）；(iii) moments 与 ratios 预测一致（Bui–Keating 2006）；(iv) 条件性后果（Conrey–Snaith） | 某个固定 **ω_D>0**（任意小），2/2，全导子含复合，T≤100 log 2q 一致 | **ω_D: 0 → >0**（整个猜想；但只需任意小）。附加：已知结果均为单 shift/受限 range/GRH 条件；无一条覆盖 2/2 一般 shift。函数域已证（Sawin 2024） |
| **RC_D 的“最弱可实现目标”** | 单 shift（Čech/Gao–Zhao）已证（GRH 条件） | 需要从 1/1 → 2/2，从受限 range → 全 range，从特殊族 → 全 primitive | 概念 gap：两步（shift 数 + range/族）；尚无方法 |
| **(I) 平方自由 AP 素数水平** | BV **1/2**（全模）；BFI **4/7**（well-factorable）；Zhang **1/2+1/1168**（光滑模）；Polymath8b **1/2+7/300**（光滑平方自由+CRT） | 函数域实现用 **θ=5/6**（Sawin Prop 8.16）；ℤ 版至少需 >1/2（具体阈值待定） | 1/2→5/6 差 **1/3**；记录 4/7→5/6 差 **11/42≈0.262**；1/2+7/300→5/6 差 ≈0.309。2024–26 无一般模 >1/2 结果（MPR/Guth–Maynard 未直接改进 BV 水平） |
| **(II) 两点 (twisted) Chowla** | MRT 2015：shift-平均 `o(H^kX)`，衰减 ~loglog H/logH；Tao 2015：对数平均 `o(logω)`（破 parity barrier，无 saving）；TT 2018：k 点 Chowla（k 奇或 2）所有尺度除 log-密度 0 集；无 ℤ 上 power-saving 两点 Chowla（2026 ACD+26 是**函数域** twisted） | power-saving（`X^{−δ}` 或 H-平均 power saving），twisted/仿射族一致 | **无 saving → δ>0**：parity barrier 本体；MRT/Tao/TT 提供了“定性/对数/几乎全尺度”版本，但到多项式 saving 无路径 |
| **函数域对照（全部已证）** | Sawin 2024：harmonic families Ratios/平方根；Sawin–Shusterman 2022：function-field Chowla/twin primes；G-W-X Thm 1.5/1.6：q>10^200 无条件 Goldbach/prime pairs（误差 q^{23d/24}） | —（这是模板） | 说明 (I)+(II) 在函数域同时成立且可推出 Goldbach ⇒ **ℤ 的缺口就是 (I)+(II) 的 ℚ 版** |

**哪条最值得投入（判断 [推测]）**：**路线 A（Ratios）**。

理由：
1. **目标单一且明确**：一个具体猜想（CFZ 2008 的 Dirichlet 族 2/2，任意小 ω_D>0），不是“不知道要证什么”的开问题；G-W-X 已给出完整推导链。
2. **需求弱**：只需任意固定 ω_D>0，不需要 1/2；误差只需 `N^{1−ω_D+ε}` < N。
3. **有成功模板与活跃技术**：函数域 Sawin 2024 证明；ℚ 上有 multiple Dirichlet series（Čech; Gao–Zhao）证明单 shift 受限 range 的 ratios，及 1-level density 的平方根验证（Goes 等）；Lee 2026 的 zeta-ratios ⇒ prime pairs 说明该方向正在快速推进。
4. **路线 B 的 (II) 是 parity barrier 本体**：无 power-saving 两点 Chowla 的已知路径；函数域靠上同调（Frobenius/Weil）绕过，ℤ 无对应工具。即使 (I) 有进展，(II) 仍会卡死。

**路线 A 的具体第一步（细化 phase-7 建议）**：
- 先证 **单 shift → 2/2 的扩展**：用 Gao–Zhao 的 multiple Dirichlet series 把“单 shift ratios（GRH 条件）”提升到 2/2（即分子/分母各两个 shift），先在一维 range（如 `|Im| ≤ c log q`、`q` prime）实现；
- 或直接攻 **G-W-X Appendix A 的 Dirichlet 定性版**（若存在；本报告发现 Appendix A 只对 zeta/Hecke 给出弱化版本，对 Goldbach 的 character argument 仍需正 power saving——所以定性版不够，目标必须是 ω_D>0）；
- 同时检查 **parity-twist 步骤**（G-W-X §3.1）是否可绕开：若能找到不需要从 untwisted ratios 解 parity 平均的写法，可能降低对 RC_D 的要求。

---

## 7. 引用清单（URL/DOI；访问日期 2026-11-21）

**Ratios / Goldbach / 函数域**
1. H. Gou, V. Y. Wang, M. W. Xu, *Landau's problems through ratios of L-functions*, arXiv:2611.18825（2026-11-13）。https://arxiv.org/abs/2611.18825
2. J. B. Conrey, D. W. Farmer, M. R. Zirnbauer, *Autocorrelation of ratios of L-functions*, Commun. Number Theory Phys. 2 (2008) 593–636；arXiv:0711.0718。
3. J. B. Conrey, N. C. Snaith, *Applications of the L-functions ratios conjectures*, Proc. LMS 94 (2007) 594–646；arXiv:math/0509480。
4. H. M. Bui, J. P. Keating, *On the mean values of Dirichlet L-functions*, arXiv:math/0607199（2006）。
5. J. Goes, S. Jackson, S. J. Miller, D. Montague, K. Ninsuwan, R. Peckner, T. Pham, *A unitary test of the Ratios Conjecture*, arXiv:0909.4916（2009）。
6. M. Čech, *The Ratios conjecture for real Dirichlet characters and multiple Dirichlet series*, arXiv:2110.04409v3；Trans. Amer. Math. Soc. 377 (2024), no. 5, DOI 10.1090/tran/9113。
7. P. Gao, L. Zhao, *Ratios conjecture of quadratic Hecke L-functions of prime-related moduli*（arXiv:2404.05081, 2024）；*…quartic L-functions of prime moduli*（arXiv:2402.17198, 2024）；*…cubic L-functions of prime moduli*（arXiv:2311.08626, 2023）；*Ratios conjecture for quadratic twist of modular L-functions*（arXiv:2304.14600, 2023）；*Ratios conjecture for quadratic Hecke L-functions in the Gaussian field*（arXiv:2210.08840, 2022）。
8. P. J. Cho, J. Park, *Low-lying zeros of cubic Dirichlet L-functions and the Ratios Conjecture*, arXiv:1802.01762（2018）。
9. D. Fiorilli, S. J. Miller, *Surpassing the Ratios Conjecture in the 1-level density of Dirichlet L-functions*, arXiv:1111.3896（2011）。
10. W. Sawin, *Square-root cancellation for sums of factorization functions over squarefree progressions in F_q[t]*, Acta Math. 233 (2024) 285–418；arXiv:2102.09730。
11. W. Sawin, M. Shusterman, *On the Chowla and twin primes conjectures over F_q[T]*, Ann. of Math. (2) 196 (2022) 457–506。
12. T. C. Anderson, S. Chow, R. Dietmann, D. Hokken, P. Koymans, R. J. Lemke Oliver, W. Sawin, M. Shusterman, *The strong form of Van der Waerden's conjecture via twisted Chowla*, arXiv:2608.22297v2（2026-08-23）。
13. S. Lee, *The Hardy–Littlewood asymptotic for prime pairs of fixed even difference from a uniform zeta-ratios conjecture*, arXiv:2610.32672v2（revised 2026-11-03）。https://arxiv.org/abs/2610.32672

**AP 分布水平 / 指数和**
14. E. Bombieri, H. Iwaniec, *On the distribution of primes in arithmetic progressions*, 各种综述；Bombieri–Vinogradov 1965 原始。
15. E. Bombieri, J. B. Friedlander, H. Iwaniec, *Primes in arithmetic progressions to large moduli*, Acta Math. 156 (1986) 203–251（level 4/7, well-factorable）。
16. Y. Zhang, *Bounded gaps between primes*, Ann. of Math. 179 (2014) 1121–1174（光滑模 level 1/2+1/1168）。
17. D. H. J. Polymath, *New equidistribution estimates of Zhang type*, arXiv:1402.0811（2014）；摘要：exponent of distribution `1/2 + 7/300`（smooth squarefree moduli + CRT 条件）。
18. J. Maynard, M. Pandey, M. Radziwiłł, *Exponential sums over primes*, arXiv:2608.14777（2026-08-14）。
19. L. Guth, J. Maynard, *New large value estimates for Dirichlet polynomials*, arXiv:2405.20552（2024-05-31）。

**Chowla / 两点相关**
20. K. Matomäki, M. Radziwiłł, T. Tao, *An averaged form of Chowla's conjecture*, arXiv:1503.05121（2015-03-17）。
21. T. Tao, *The logarithmically averaged Chowla and Elliott conjectures for two-point correlations*, arXiv:1509.05422（2015-09-17）。
22. T. Tao, J. Teräväinen, *The structure of correlations of multiplicative functions at almost all scales, with applications to the Chowla and Elliott conjectures*, arXiv:1809.02518（2018-09-07）。
23. T. Tao, J. Teräväinen, *Odd order cases of the logarithmically averaged Chowla conjecture*, arXiv:1710.02112（2017-10-05）。
24. B. Wang, *Two averaged dynamical generalizations of Chowla's conjecture*, arXiv:2608.16108v4（2026-08）；B. Wang, S. Yi, arXiv:2609.14492v2（2026-09）；B. Wang, D. Yang, arXiv:2610.34912（2026-10）。

**本团队报告**
25. phase7/lit/alternative-routes.md（task-30）；phase-6/0-phase6-报告.md；phase-6/audit/hgold-direct.md。

---

## 附录 A：关键原文（便于 Lead 直接引用）

1. **RC_D 定义**（G-W-X Hypothesis 1.1）：见 §1.1 全引。
2. **任意 ω_D>0 足够**（G-W-X §1.1）：
   > “The case ω_D=1/2 is the square-root error bound for this family. **Any fixed ω_D>0 suffices for Theorem 1.1.**”
3. **Goldbach 定理**（G-W-X Theorem 1.1）：
   > “Assume GRH for Dirichlet L-functions, and RC_D(ω_D). For every ε>0 and every even N, we have Σ_{m+n=N}Λ(m)Λ(n) = N𝔖(N) + O_ε(N^{1−ω_D+ε}).”
4. **定性弱化不适用 Goldbach**（G-W-X Appendix A 开头）：
   > “For prime differences and quadratic values, the power-saving ratios errors in the main theorems can be weakened if only qualitative asymptotics are required. … **The character argument continues to use a positive power saving.**”
5. **函数域水平**（G-W-X §7）：
   > “For each j≤K and C∈M_j with (C,D)=1 and μ(C)≠0, Sawin's estimate [Saw24, Proposition 8.16 at level θ = 5/6] gives …”
6. **MRT 平均 Chowla**（arXiv:1503.05121 摘要）：
   > “we establish an averaged version of this conjecture, namely Σ_{h1,…,hk≤H}|Σ_{1≤n≤X}λ(n+h1)…λ(n+hk)| = o(H^kX) as X→∞ whenever H=H(X)≤X goes to infinity … quantitative bounds on the decay rate (roughly on the order of log log H/log H)…”
7. **Tao 对数平均两点**（arXiv:1509.05422 摘要）：
   > “we establish the logarithmically averaged version Σ_{x/ω(x)<n≤x} λ(a1n+b1)λ(a2n+b2)/n = o(log ω(x)) … thus breaking the ‘parity barrier’ for this problem.”
8. **Tao–Teräväinen 几乎全尺度**（arXiv:1809.02518 摘要）：
   > “we establish the k-point Chowla conjecture E_{n≤X}λ(n+h1)…λ(n+hk)=o(1) for k odd or equal to 2 for all scales X outside of a set of zero logarithmic density.”
9. **Polymath8b 水平**（arXiv:1402.0811 摘要）：
   > “We prove distribution estimates for primes in arithmetic progressions to large smooth squarefree moduli … obtaining an exponent of distribution 1/2 + 7/300.”
10. **Goes 等 ratios 检验**（arXiv:0909.4916 摘要）：
    > “we verify the conjecture's predictions for the unitary family of all Dirichlet L-functions with prime conductor; we show square-root agreement … if the support of the Fourier transform of the test function is in (−1,1), and for support up to (−2,2) we show agreement up to a power savings in the family's cardinality.”
11. **Čech**（arXiv:2110.04409 摘要）：
    > “We consider the family of real Dirichlet characters, and use multiple Dirichlet series to prove the ratios conjectures with one shift in the numerator and denominator in some range of the shifts. … All of the results are conditional under the Generalized Riemann hypothesis.”
12. **ACD+26**（arXiv:2608.22297 摘要）：
    > “we formulate a twisted function field version of Chowla's conjecture, and show how Van der Waerden's conjecture reduces to this conjecture for n≥8. Finally, we make significant progress towards this twisted Chowla conjecture…”

---

## 附录 B：核查方式与局限

- **逐字核对**：G-W-X arXiv:2611.18825 PDF 全文（46 页）：Hypothesis 1.1、Theorem 1.1、Appendix A 开头、§7 level θ=5/6；arXiv 摘要：1503.05121、1509.05422、1809.02518、0909.4916（全文摘要）、2110.04409、2404.05081、2608.22297（全文摘要）、1402.0811、math/0607199、math/0509480、2608.14777、2405.20552、2610.32672；Polymath8b 摘要。
- **未逐字核对**：CFZ 2008 原文的 Conjecture 5.1/Section 6.4 编号（经 G-W-X 引用核对）；BFI 1986 的 4/7 精确陈述（经二手综述/标准知识，本轮未取原文）；Bombieri–Vinogradov 1965 原文；Zhang 2014 的 1/2+1/1168 精确形式；Gao–Zhao 各篇的精确 range（仅摘要）。
- **局限**：WSL 下 github/Wikipedia 不可达；部分页面需登录；arXiv 检索偶发限流；时间盒 60 分钟（本报告按环境时钟约 10 分钟完成，检索/抓取轮次见正文），本报告是文献状态调研而非证明审计；所有 gap 表的“gap factor”是粗略量化（指数差），不代表可实现的路径。
