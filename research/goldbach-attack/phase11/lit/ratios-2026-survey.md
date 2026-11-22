# Phase-11 文献：Wang–Xu Ratios 猜想、GWX 后续、2024–26 Ratios-over-ℚ 现状、条件性 binary Goldbach 全表

> 作者：goldbach-researcher（task-39）。日期：2026-11-21 23:09–00:20（Asia/Shanghai）。URL/arXiv 访问日期 2026-11-21（部分 11-22 凌晨）。
> 任务：确认 WX25（GWX 引用的 Wang–Xu Conjecture 2.1）；GWX 2611.18825 后续/companion；2024–26 Ratios-over-ℚ 最强结果；所有已知条件性 binary Goldbach 结果（与 H_Ratios+GRH 比较）。
> 标注：**[事实]** 已证/已发表；**[预印本]** 未评审；**[推导]**；**[推测]**；**[二手/未核验]** 非同行评议的评论/网页。

---

## 0. 五条要点（已发 lead）

1. **WX25 = V. Y. Wang, M. W. Xu, “Harper's beyond square-root conjecture”**，Int. Math. Res. Not. IMRN 2025 (2025), no. 18, rnaf279；arXiv:2405.04094v2（2024-05-07 首发，2025-08-26 更新；27 页）。其 **Conjecture 2.1** 只覆盖**素数模 r**的 Dirichlet 特征族（χ≠χ0）：Re(z1)=Re(z2)=1/2，Re(s1)=Re(s2)=1/2+ε，T=max(|Im|)，存在**绝对常数** ω∈(0,1/2] 使
   `Σ_{χ≠χ0} L(z1,χ)L(z2,χ)/(L(s1,χ)L(s2,χ)) = M_T + O_ε((1+T)^ε r^{−ω})`，
   M_T 由 CFZ 2/2 主项 + 函数方程反射项（H·r^{z1+z2−1}）组成。**WX25 没有证明该猜想或任何情形**：其 Thm 1.2 是条件性的（GRH for F_r + Ratios Conjecture for F*_r ⇒ Harper Conjecture 1.1 的 c=λ 离散情形），Cor 1.3 给算术级数中 Liouville 的相消；文中指出 GRH 单独可能足够，函数域已有进展可望无条件版，但均未做。
2. **GWX Hypothesis 1.1 是 WX25 Conjecture 2.1 的强化/推广**：所有导子（含复合 q）、误差 `q^{1−ω_D+ε}(1+T)^B`、指定 ω_D；GWX 在素数 q 时引用 WX25 的“two terms … with the exact primitive parity counts”，复合导子的统一处理是 GWX 新增的、也是最未验证的推广。
3. **GWX 2611.18825 后续/批评**：arXiv 仅 v1（2026-11-13，46 页）；作者另在 **Hexagon**（hexagon:2611.00423v1，36 页，2026-11-13）发布同一论文。Semantic Scholar 的引用列表为空（论文 8 天新）；未发现正式勘误/同行评议。唯一外部评论是研究新闻站 cxy0714.github.io 的精读（2026-11-16，AI 辅助；**[二手/未核验]**），提出若干未经核验的疑虑（Thm 1.1 的 parity-twist 平均非标准 RCD 直接推论、Thm 1.3 依赖更强 Hypothesis 4.1、Thm 1.4 的 Waxman 参数范围未验证）——**不可当作有效批评**。companion：WX25、Wang《Notes on zeta ratio stabilization》（arXiv:2402.01214，函数域 ratios via homological stability）、Harper arXiv:2301.04390 / arXiv:2512.23681（ICM 2026 survey）、Lee arXiv:2610.32672v2、Gou arXiv:2607.08985（两素数平方表示的矩）。
4. **2024–26 无一般 Dirichlet 族的 Ratios-over-ℚ 新定理**。最强已知仍是：Čech（arXiv:2110.04409；Trans. AMS 377 (2024) 9113）实 Dirichlet 特征、**单 shift**、受限 range、**GRH 条件**；Gao–Zhao 2022–24 二次/三次/四次 Dirichlet/Hecke 族、单 shift、受限 range、GRH 条件；WX25 = 素数模 2/2 的**猜想** + 条件性应用；Goes 等 2009 = 1-level density 受限验证；Bui–Keating 2006 / Conrey–Snaith 2007 = 矩/条件性后果。**Lee arXiv:2610.32672 最新为 v2（2026-11-03）**：comment 原文 “The result now covers all fixed positive even gaps. We also weaken the ratios assumption and improve the error bounds”；restricted uniform 2/2 zeta-ratios 误差 `O(U^{ϑ+ε})`，`1/2≤ϑ<(39−√177)/32≈0.8029`，实部 [3/64,5/64]、虚部 ≤U^ν (ν≤1/4)；权误差 `x^{−Δ(ϑ)+ε}`，Δ(ϑ)=7/16−ϑ+ϑ/(3−ϑ)>0；加 RH 后 `x^{ϑ−7/8+ε}`。
5. **条件性 binary Goldbach 全表结论**：只有两条完整条件路线——(a) **GWX：GRH + RC_D(ω_D)**；(b) **Li–Liu：GRH + Hypothesis S（或 R）**（2026-11-13，S/R 是 LL 算子的非标准谱假设，与 RC 强弱不可直接比较）。**没有找到比 H_Ratios+GRH 更弱或不同的、能推出完整 binary Goldbach 的已知条件路线。** 其余“条件结果”都只给 almost-all 或 (1+1.x)：GRH 单独 ⇒ E(x)≪x^{1/2+ε}；GRH+pair correlation ⇒ EH/PNT-AP 改进（Kandhil–Languasco–Moree），仍非 Goldbach；EH/BV/BFI ⇒ (1+2)/(1+1.9)/(1+1.4)；Chowla/Lindelöf/Hooley 未发现蕴含 binary Goldbach 的定理；Piatetski-Shapiro 型只是 Waring–Goldbach/P-S 素数变体。2026 的 Pandey arXiv:2608.02381 提出“偶数 = 素数 + 孪生素数”的**中间猜想**（蕴含 Goldbach 与孪生素数，属**更强**而非更弱；条件结果用孪生素数下界，验证到 10^14）；Zenodo 23155084（Arneth, 2026-10-05）与 arXiv:2611.09007 “elementary proof” 均为未核验/不成立的声明。

---

## 1. WX25：精确识别、Conjecture 2.1、范围与已证情形

### 1.1 文献信息

| 项 | 内容 |
|---|---|
| 作者 | Victor Y. Wang, Max Wenqiang Xu |
| 标题 | *Harper's beyond square-root conjecture* |
| 期刊 | Int. Math. Res. Not. IMRN **2025** (2025), no. 18, rnaf279（GWX 参考文献 [WX25] 给出的正式出处） |
| arXiv | **arXiv:2405.04094v2**（v1 2024-05-07；v2 2025-08-26；27 页） |
| URL | https://arxiv.org/abs/2405.04094 |
| 主题 | 用 (shifted) Ratios Conjecture for L(s,χ) 把 Harper 的 randomization 论证从 conductor-limited range 推广到 **unlimited range** of “beyond square-root cancellation”（字符 twist 的 Liouville 函数）；推论：Liouville 在模略超 square-root barrier 的 AP 中有非平凡相消 |

**摘要原文**：
> “We explain how the (shifted) Ratios Conjecture for L(s,χ) would extend a randomization argument of Harper from a conductor-limited range to an unlimited range of ‘beyond square-root cancellation’ for character twists of the Liouville function. As a corollary, the Liouville function would have nontrivial cancellation in arithmetic progressions of modulus just exceeding the well-known square-root barrier. Morally, the paper passes from random matrices to random multiplicative functions.”

### 1.2 Conjecture 2.1（逐字转写自 PDF，第 7 页）

> **Conjecture 2.1.** Let Re(z1)=Re(z2)=1/2 and Re(s1)=Re(s2)=1/2+ε. Let T := max(|Im(z1)|,|Im(z2)|,|Im(s1)|,|Im(s2)|). Then for some absolute constant ω∈(0,1/2] (independent of r and ε), we have for all sufficiently small ε>0
> `E_{χ≠χ0} L(z1,χ)L(z2,χ)/(L(s1,χ)L(s2,χ)) = M_T + O_ε((1+T)^ε r^{−ω})`,
> where
> `M_T := E_f[L*(z1,f)L*(z2,f)/(L*(s1,f)L*(s2,f))] + H·r^{z1+z2−1}·E_f[L*(1−z2,f)L*(1−z1,f)/(L*(s1,f)L*(s2,f))]`,
> `H := (2π)^{z1+z2}/π² · Γ(1−z1)Γ(1−z2) · Σ_{a∈{0,1}} 2 sin(π/2(1−z1+a)) sin(π/2(1−z2+a))`
> （H 的具体形式以论文排版为准；上式为 PDF 文本抽取后的转录，符号/常数位置可能有排版歧义；E_f 为 CFZ [9,(5.6)] 随机矩阵模型中的平均，L* 为模型 L-函数）。

**范围说明（论文原文）**：
- 特征家族：**mod r 的 Dirichlet 特征**，r **primitive**（论文在 §1 约定 “where r is a prime for convenience”；Conjecture 2.1 的求和为 χ≠χ0，即排除 principal）。
- shifts：分子 `Re z_i = 1/2`，分母 `Re s_i = 1/2+ε`（ε 固定充分小）；T=100log? 不，Conjecture 2.1 的 T 为最大虚部，误差 `(1+T)^ε`。
- 误差：`r^{−ω}`，**ω 是绝对常数**（independent of r, ε），可任取 (0,1/2]；论文特别说明 “The power saving r^ω … is a standard part of the Ratios Conjecture … our assumption that ω is independent of r and ε is very convenient.”
- 形式来源：作为 CFZ 2008 一般 recipe [9,(5.6)] 的**特例**导出；论文 §2 给出了 “Derivation via the Ratios Recipe” 详细推导（乘开函数方程、用 Gauss 和/root number 相消、按 [8,(4.3.4)] 平均）。

### 1.3 WX25 证明了什么？（关键：没有证明 Conjecture 2.1）

- **[事实]** WX25 的**主定理是条件性的**：
  > **Theorem 1.2.** Assume GRH for F_r, and the Ratios Conjecture [9,(5.6)] for F*_r. Then Conjecture 1.1 is true in the discrete case (1.2) when c=λ.
  （F_r = mod r 的 Dirichlet 特征族；F*_r = 本原特征子族；Harper 的 Conjecture 1.1 断言 `E_χ|Σ_{n≤x}c(n)χ(n)|=o(√x)` 当 `1≤x≤r^A`，c∈{μ,λ}。）
- **[事实] Corollary 1.3**：同假设下，Liouville 在算术级数中模 r 的相消（略超 square-root barrier 的模范围）。
- **[事实]** 文中明确：**“It is natural to hope that GRH alone might suffice, by adapting techniques of [18,32,34] from moments to ratios. … It would be interesting to pursue this further.”** 以及函数域上“there is now enough progress on the Ratios Conjecture that one can likely prove an unconditional version of Theorem 1.2 in one or more families for all q large enough”，但本论文**没有做**。
- **[事实]** 论文没有对 Conjecture 2.1 做数值检验（从全文结构看只有理论推导与条件性应用）；没有给出任何族的无条件 ratios 定理。
- **结论**：WX25 的价值是（i）给出一个**可引用的、prime-conductor、2/2、带绝对 power saving 的 Ratios 猜想精确形式**；（ii）证明“若该猜想成立，则 Harper 的 beyond-square-root 现象在无限制 range 成立”；（iii）给出 CFZ 2/2 主项的显式形式（含 H 反射项），GWX 直接复用其 prime-q 情形。**它不是 Ratios 猜想的证明，也没有任何已证情形。**

### 1.4 与 GWX Hypothesis 1.1 的精确关系

| 方面 | WX25 Conjecture 2.1 | GWX Hypothesis 1.1（RC_D(ω_D)） |
|---|---|---|
| 导子 q | **素数 r** | **所有 q>1，含复合**（“uniformly for all conductors q>1, including composite conductors”） |
| 特征 | χ≠χ0（mod r，r 素数 ⇒ 非主即本原） | 所有 **primitive** χ mod q |
| shifts | Re z=1/2，Re s=1/2+ε（ε 充分小） | Re a=Re b=1/2，Re s=Re t=1/2+η（η 充分小） |
| 虚部范围 | T=max(|Im|)，误差 (1+T)^ε | T≤**100 log(2q)**，误差 (1+T)^B（B≥0） |
| 误差 | `r^{−ω}`，ω∈(0,1/2] 绝对 | `q^{1−ω_D+ε}`，ω_D∈(0,1/2] 可依赖族但固定；**任意 ω_D>0 足以证 Goldbach** |
| 状态 | **[猜想]**，未证任何情形；有条件性应用（Thm 1.2/Cor 1.3） | **[猜想]**，未证；GWX Thm 1.1 由它推出 Goldbach |
| 关系 | GWX 在素数 q 的 2/2 主项上**直接引用 WX25 Conjecture 2.1 的两项**（GWX 原文：“For prime q, this uses the two terms of Wang–Xu [WX25, Conjecture 2.1], with the exact primitive parity counts”）；复合导子的统一陈述、`(1+T)^B` 与 parity-twist 处理是 GWX 的新内容 | |

**工作判断 [推导]**：GWX 真正需要的是**复合导子 + T 范围 + 全本原特征**的强化版；WX25 只提供了素数模的模板与主项结构。**因此即使 WX25 的猜想被证明，也不能自动得到 GWX 的 RC_D（需要把复合导子情形导出/验证）；反过来 GWX 的 RC_D(ω_D) 在素数 q 上略强于 WX25 Conjecture 2.1（T 范围的形式不同）。**

---

### 1.5 “GRH-alone hope”：精确原文、含义、与 2/2 Ratios/Goldbach 的关系（Lead 追问）

**（a）精确原文与上下文**（WX25 = arXiv:2405.04094v2, p.2；紧接在 Theorem 1.2 之后，逐字）：

> “Theorem 1.2 will follow from Theorem 3.1. Conjecture 2.1 is the precise form of the Ratios Conjecture that we use. See [8–10] for details on the general Moments and Ratios Conjectures, and their rich history based on random matrices.
>
> **It is natural to hope that GRH alone might suffice, by adapting techniques of [18,32,34] from moments to ratios. See [5,6,12], and references within, for progress in this direction. It would be interesting to pursue this further.** Let us also mention that over function fields F_q(t), there is now enough progress on the Ratios Conjecture that one can likely prove an unconditional version of Theorem 1.2 in one or more families for all q large enough in terms of A. See [2,28,31,35], and references within, for some relevant developments on ratios.”

**引用映射**（WX25 参考文献）：[18] Harper, *Sharp conditional bounds for moments of the Riemann zeta function*（2013）；[32] Soundararajan, *Moments of the Riemann zeta function*（Ann. Math. 170 (2009)）；[34] Szabó, *High moments of theta functions and character sums*（Mathematika 70 (2024)）；[5] Bui–Florea, *Negative moments of the Riemann zeta-function*（J. reine angew. Math. 2024）；[6] Bui–Florea–Keating, *The Ratios Conjecture and upper bounds for negative moments of L-functions over function fields*（Trans. AMS 376 (2023)）；[12] Florea, *Negative moments of L-functions with small shifts over function fields*（IMRN 2024）；[2] Bergström–Diaconu–Petersen–Westerland（2023）；[28] Miller–Patzt–Petersen–Randal-Williams（2024）；[31] Sawin（Acta Math. 2024）；[35] Wang, *Notes on zeta ratio stabilization*（2024）。

**（b）“GRH alone might suffice” 到底指什么？（[推导]，基于上下文）**

- 它指：**GRH 单独可能足以证明 Theorem 1.2 的结论**，即 **Harper 的 Conjecture 1.1 的离散情形 c=λ**：
  > **Conjecture 1.1 (Harper).** Fix c∈{μ,λ}. Let A be a fixed positive constant. Then `E_χ|Σ_{1≤n≤x} c(n)χ(n)| = o(√x)` as x→+∞, provided `1≤x≤r^A`. Similarly, if `1≤x≤T^A` and x→+∞, then `(1/T)∫_0^T |Σ_{1≤n≤x} c(n)n^{it}| dt = o(√x)`. Moreover, in both (1.2) and (1.3), the quantitative upper bound `O(√x/(log log x)^{1/4})` holds.
- **不是**指“GRH ⇒ Ratios Conjecture”，也**不是**指“GRH ⇒ WX25 Conjecture 2.1 / 2/2 ratios average”。原文的“from moments to ratios”是把 [18,32,34] 的**矩方法**推广到“ratios 型”估计（即用矩/负矩技术绕过完整 Ratios 假设，直接证明 Harper 的字符和相消），而不是反推 Ratios 本身。
- 换言之：WX25 的定理方向是 **Ratios ⇒ λ-相消（单向）**；其 remark 希望的是 **GRH（+矩方法）⇒ λ-相消**，从而绕开 Ratios 来证明 Harper 的猜想——目标对象始终是 **λ 的一次矩字符和**，不是 GWX 需要的 2/2 L-比值平均。

**（c）无条件进展（ℚ 与函数域）**

| 范围 | 已知无条件进展 | 是否达到 WX25 Thm 1.2 的结论（r^A 范围、λ 字符和、o(√x)） |
|---|---|---|
| ℚ（Q 上） | Harper, arXiv:2301.04390（2023）：对 `1≤x≤r`、`min(x,r/x)→∞` 证明 `E_χ|Σ_{n≤x} c(n)χ(n)|=o(√x)`（conductor-limited range；r 素数）；即 Harper 的 **r-范围**结果，不是 r^A 范围 | **否**（范围限制在 x≤r） |
| ℚ（矩/负矩） | Bui–Florea（2024）ζ 的负矩上界；Bui–Florea–Keating（2023）/Florea（2024）函数域负矩与 ratios 上界；Harper 2013/Soundararajan 2009/Szabó 2024 的矩方法 | **否**（这些是 L^{-k} 的负矩上界/矩方法，不是 2/2 ratios 平均） |
| 函数域 F_q(t) | WX25 原文只说 “**likely** prove an unconditional version of Theorem 1.2 … for all q large enough in terms of A”，依据 [2,28,31,35]；2025–26 相关新文：Verreault–Xu, arXiv:2611.09753（2026-11-06）解决了 Harper 猜想的**随机矩阵版本**（Haar unitary U_N 的 `tr(Sym^k U_N)` 第一绝对矩 →0，`min(N,k)→∞`，无 k/N 限制）；Fouvry–Shparlinski–Xi, arXiv:2610.28822（2026-10-20）给函数域 μ 的短和 power saving；Ma, arXiv:2606.26440（2026-06-24）用同调消失给函数域字符和相消 | **未找到**已发表的“函数域无条件 WX25 Thm 1.2”（截至 2026-11-21 检索）——WX25 的 “likely” 仍是预期，不是定理；随机矩阵版本已由 Verreault–Xu 解决，但那是模型而非数论族 |

**（d）WX25 的技术/remark 能否绕过 Ratios 去得到 2/2 平均？（对“GRH-only Goldbach 路线”的意义）**

[推导/推测]

1. **不能直接绕过**：WX25 的对象是 `E_χ|Σ_{n≤x} λ(n)χ(n)|`（关于 χ 的**一次矩**、被加项是 λ 的字符和），Ratios 在其中用于给 λ(n)χ(n) 的随机模型/正交性提供依据；其“GRH-alone”希望针对同一对象（λ 相消），**不是** GWX 需要的 `Σ*_χ L(a,χ)L(b,χ)/(L(s,χ)L(t,χ))`（2/2、两个分子 L、两个分母 L、q-一致 power saving）。
2. **可能的间接路径 = phase-11 “Route C”**：用 `1/L(s,χ)=Σ_{n≤X} μ(n)χ(n)n^{-s}+E`（Perron+GRH）替换分母，再用 Cauchy–Schwarz + 无条件二阶矩 `Σ_χ|L(1/2,χ)|² ≪ q log q` 控制分子；这需要 (i) GRH 下 `1/L` 的一致截断误差（q,t-一致），(ii) 跨 χ 的 μ-相关/Type II 估计（wrap-around 项）。这正是 task-37（H_Ratios^min/Route C 审计）与 task-38（Route C 构造）在做的事；WX25 的 remark 与负矩文献 [5,6,12] 提供动机/工具，但**没有**给出 2/2 平均的证明或条件定理。
3. **负矩文献的类型 mismatch**：[5,6,12] 是 `L^{-k}`（分子为 1）的**上界**；GWX 需要分子 `L(a)L(b)`（不是 1）且分母两个、且要 q 的**正幂 saving**（对任意小 ω_D>0）。从负矩上界到 2/2 比值平均不是形式推论。
4. **结论**：WX25 的 “GRH-alone hope” **不构成 GRH-only Goldbach 路线的证据**；它只提示“GRH+矩方法可能直接证 Harper 的 λ 相消（不需 Ratios）”。若要 GRH-only 推出 GWX 的 Goldbach，需要新的 **GRH 条件下 2/2 负矩/倒数矩估计**（Route C 级别的新定理），目前没有；且 GWX 的 parity-twist 结构（需要 untwisted ratios 的两个函数方程组合出 χ(−1) 加权）本身也要在 GRH-only 方案中重建。**[推测]** 即便 Harper 猜想被 GRH 单独证明，也只给 λ 的字符和相消，不能直接给出 2/2 ratios 或 Goldbach；它最多是 Route C 的一个可能输入。

---

## 2. GWX 2611.18825 的后续、批评、companion papers

### 2.1 状态

| 项 | 内容 |
|---|---|
| arXiv | **arXiv:2611.18825v1**（2026-11-13 18:55 UTC；46 页；无 v2）https://arxiv.org/abs/2611.18825 |
| 其他平台 | **Hexagon**: hexagon:2611.00423v1（2026-11-13；36 页；无 DOI；标注 “A mix of human-written and AI-generated text / Human understanding: all parts”；23 条参考文献）https://hexagonmath.org/2611.00423v1 |
| 引用 | Semantic Scholar API 查询引用列表为**空**（2026-11-21；论文 8 天新，属正常；API 偶发 429）。未发现 arXiv 引用它的论文。 |
| 同行评议/勘误 | 无。 |
| 论坛/博客讨论 | 见 2.2（唯一找到的是 AI 辅助 research-news 精读）。 |

### 2.2 唯一外部评论（必须标为未核验）

**cxy0714.github.io “Research News” 精读**（2026-11-16）：https://cxy0714.github.io/research-news/deep_reads/2026-11-16-hexagon_2611.00423/
- 站点性质：AI 辅助的论文精读/新闻汇总（页面自述“Human understanding: all parts”，但整体是自动生成式研究新闻），**非同行评议、非专家核验**。**[二手/未核验]**
- 其提出的“结论比证明窄”疑虑（原文概括）：
  1. **Theorem 1.1 (Goldbach)** 的 parity-twist 平均“不是标准 RCD 的直接推论，而是需要额外假设（如对特征和的均匀性估计）；作者在文中假设了这一点，但未在 Hypothesis 1.1 中明确列出”；
  2. **Theorem 1.3 (Legendre)** 的素数间隙结论依赖更强的、非标准的 Hypothesis 4.1，“未明确说明标准 RCZ 是否足以推出”；
  3. **Theorem 1.4 (n²+1)** 引用 Waxman (2021) 的参数范围“未验证是否覆盖全部所需范围”。
- **本报告立场**：这些是**未经核验的二手评论**，不能作为“论文有错”的证据；但也提示 Lead：若要引用 GWX 的 Goldbach 结论，最好由独立审计核对 §3 的 parity-twist 推导是否真的只用到 Hypothesis 1.1（phase-8 报告已指出 parity-twist 步骤是核心；phase-11 task-37 的 `H_Ratios^min` 审计正是做这件事）。

### 2.3 同一作者/相关 companion papers

| 论文 | 内容 | 与 GWX 关系 |
|---|---|---|
| **WX25**（Wang–Xu, IMRN 2025, arXiv:2405.04094） | Harper beyond-square-root；素数模 2/2 Ratios 猜想 + 条件性应用 | GWX 的素数模主项来源；RC 的 prime-conductor 版本 |
| **V. Y. Wang, Notes on zeta ratio stabilization**（arXiv:2402.01214，2024-02；updated 2024-03） | 用 homological stability 解决 **F_q(t)** 上的 Ratios Conjecture（large fixed q，uniform power saving at distance ≥q^{−δ}），推论 cancellation-beyond-GRH 大范围、low-lying zeros 统计 | 函数域 ratios 的关键技术对照；GWX 函数域无条件的背景 |
| **A. J. Harper, The typical size of character and zeta sums is o(√x)**（arXiv:2301.04390, 2023） | 无条件证明字符和/ζ 和的 better-than-√ cancellation（r 大素数，1≤x≤r；moments 0≤q≤1 等） | WX25/GWX 的动机与对照；非 ratios 定理 |
| **A. J. Harper, Better than squareroot cancellation in number theory**（arXiv:2512.23681, 2025-12-29；ICM 2026 Proceedings） | 综述 better-than-√ cancellation 与 multiplicative chaos | 综述；非新 ratios 定理 |
| **S. Lee, arXiv:2610.32672v2**（2026-11-03） | 从 restricted uniform 2/2 **zeta-ratios** 证明所有固定偶差的 HL 渐近（Twin Prime 方向），并给权误差/RH 改进 | 与 GWX 同一“ratios ⇒ Landau 问题”框架；处理 ζ 而非 Dirichlet 族 |
| **H. Gou, Moments of the number of representations as sums of two prime squares**（arXiv:2607.08985, 2026-07） | k≥4 阶矩的正确答案（和两素数平方表示），改进了此前条件于 Green–Tao 型猜想的 lower bound | Gou 的加性数论 companion；与 Goldbach 无直接关系 |

**结论（GWX 后续）**：截至 2026-11-21/22，GWX 没有正式后续、勘误、引用或同行评议；唯一外部评论是未核验的 AI 辅助精读。GWX 的复合导子 Ratios 假设仍是完全未证的。

---

## 3. 2024–2026 Ratios-over-ℚ 现状（按“最强已知陈述”排序）

### 3.1 全表

| 结果 | 精确陈述/范围 | 状态 | 与 RC_D 的差距 |
|---|---|---|---|
| **CFZ 2008 猜想** | Conrey–Farmer–Zirnbauer, Commun. Number Theory Phys. 2 (2008) 593–636；arXiv:0711.0718。一般族 2/2 比值平均的 recipe + 主项；ζ 的具体形式 Conjecture 5.1/Section 6.4 | **[猜想]** | 这就是目标本身 |
| **WX25 Conjecture 2.1** | 见 §1.2：素数模、2/2、ω∈(0,1/2] 绝对、误差 (1+T)^ε r^{−ω} | **[猜想]**；条件性应用 Thm 1.2/Cor 1.3 | 缺复合导子/T=100log2q/B 幂次 |
| **Čech（arXiv:2110.04409；Trans. AMS 377 (2024) 9113）** | 实 Dirichlet 特征族，**单 shift** in numerator/denominator，some range of shifts；扩展族到非本原可改进 range；“All of the results are conditional under GRH.”；足以计算某 range 的 shifted logarithmic derivatives 之和 | **[事实/GRH 条件]** | 单 shift、受限 range、实特征 |
| **Gao–Zhao 2022–2024 系列** | 二次/三次/四次 Dirichlet + Hecke 族，**单 shift**（numerator/denominator 各一），**certain ranges**，**under GRH**；推论 first moment/one-level density。arXiv:2210.08840, 2304.14600, 2311.08626, 2402.17198, 2404.05081 | **[事实/GRH 条件]** | 单 shift、特殊族、受限 range |
| **Bui–Keating 2006（arXiv:math/0607199）** | Dirichlet L 的 2k 阶矩（中心点，primitive χ mod q 平均），用 hybrid Euler–Hadamard 方法 recovered ratios/随机矩阵预测（带算术项） | **[事实]** 矩层面的一致性 | 不是 2/2 比值平均本身 |
| **Goes–Jackson–Miller–Montague–Ninsuwan–Peckner–Pham 2009（arXiv:0909.4916）** | 对 **all Dirichlet L with prime conductor** 的 unitary family，验证 ratios 预测：Fourier 支撑 (−1,1) 平方根一致；(0,−2,2) 有 power saving 一致 | **[事实]** 受限检验函数/1-level density 的验证 | 不是 2/2 平均；是间接证据 |
| **Conrey–Snaith 2005/2007（arXiv:math/0509480；Proc. LMS 94 (2007) 594–646）** | 假设 Ratios Conjecture 推导大量后果（lower order terms、mollified moments、discrete averages 等） | **[事实]** 条件性应用 | 不提供 RC 的证明 |
| **Fiorilli–Miller 2011（arXiv:1111.3896）** | 1-level density 在 Fourier 支撑 (−3/2,3/2) 超越 ratios 平方根展开，发现 ratios Conjecture 未预测的新低阶项 | **[事实]** 重要 caveat：ratios recipe 在某些范围可能不完整 | 提示 RC 的精确形式需谨慎 |
| **函数域（无条件）** | Sawin, Acta Math. 233 (2024) 285–418（harmonic families 平方根相消）；Wang arXiv:2402.01214（homological stability 解决 F_q(t) ratios）；Gao–Zhao 之外的几何族进展 BDPW23/MPPRW24/Wang24/LLOP26（GWX 引用） | **[事实]** 函数域已证 | ℚ 上的对照 |
| **Lee arXiv:2610.32672v2** | restricted uniform 2/2 **zeta-ratios**（非 Dirichlet 族）⇒ 所有固定偶差 prime pairs 的 HL 渐近；误差 O(U^{ϑ+ε})，1/2≤ϑ<(39−√177)/32≈0.8029；实部 [3/64,5/64]、虚部 ≤U^ν (ν≤1/4)；权误差 x^{−Δ(ϑ)+ε}，Δ=7/16−ϑ+ϑ/(3−ϑ)>0；加 RH 后 x^{ϑ−7/8+ε} | **[预印本 v2, 2026-11-03]** | 是 ζ-ratios，不是 Dirichlet；Twin prime 而非 Goldbach |
| **GWX arXiv:2611.18825** | 见 phase-7/8 报告：RC_D(ω_D)+GRH ⇒ Goldbach；RC_Z+RH ⇒ twin primes；RC_H+GRH ⇒ n²+1；RC_Z+RH ⇒ Legendre | **[预印本 v1]** | 假设未证；复合导子推广未验证（见 §2.2 二手疑虑） |

### 3.2 “最强已知”的结论

- **[检索结果/事实]** 2024–2026 年**没有**一篇论文证明一般 Dirichlet 族（全部 primitive 特征、2/2、含复合导子）的 Ratios Conjecture——哪怕在受限 shift/range/平均意义下。arXiv 2025–26 “ratios conjecture” 检索仅返回 GWX v1（且其为假设使用者），其余为不相关论文（eigenvalue ratio 等）。
- 最强的 ℚ 上部分结果仍是 **Čech 2024（实 Dirichlet，单 shift，GRH 条件）** 与 **Gao–Zhao 2022–24（特殊族，单 shift，GRH 条件）**；**WX25 的 2/2（素数模）只有猜想形式与条件性后果**。
- **Lee v2** 是 2026 年 ratios 技术最重要的进展之一（从 restricted zeta-ratios 到 Twin Prime HL），但它处理 ζ 族而非 Dirichlet 族，且 Twi 结论不是 Goldbach。
- **GWX 的贡献**：把“Ratios ⇒ Landau 问题”统一起来，并**首次把 Dirichlet 族 2/2（含复合导子）作为 Goldbach 的充分条件写出**；其代价是 RC_D(ω_D) 本身完全未证，且复合导子的 parity-twist 推导是全新的（二手评论有疑虑，需独立审计）。

---

## 4. 条件性 binary Goldbach：全表（与 H_Ratios+GRH 比较）

| # | 假设（精确） | 结论 | 是否完整 binary Goldbach？ | 出处/状态 |
|---|---|---|---|---|
| 1 | **GRH + RC_D(ω_D)**（RC_D 见 phase-8 §1.1；ω_D>0 任意） | `Σ_{m+n=N}Λ(m)Λ(n)=N𝔖(N)+O_ε(N^{1−ω_D+ε})` 对**每个**偶数 N | **是**（误差<主项） | GWX arXiv:2611.18825 Thm 1.1（[预印本]，2026-11-13） |
| 2 | **GRH + Hypothesis S（或 R）**（LL 算子的谱零点假设；R=所有谱零点实部 1/2） | `G(N)=c_φS(N)+O(S(N)/h(N))` 或 `+O(√(S/N)(logN)^{3/2})`，从而正表示数 | **是**（若 S/R 成立） | Li–Liu, *A Conditional Proof of the Goldbach Conjecture*（[预印本]，2026-11-13；63 页；未评审）；S/R 是 ad hoc 谱假设，非标准猜想 |
| 3 | **Hardy–Littlewood 渐近猜想**（对二元：`D_{1,1}(N)~2C(N)N/log²N`） | 渐近公式 | **是**（且更强） | [猜想]（HL 1923） |
| 4 | **广义 Hardy–Littlewood（素数元组/线性形式）猜想**（对系统 {n, N−n} 的 admissible 情形） | 对应系统的渐近 | **是**（且更强） | [猜想]；比 RC_D 强得多（它也蕴含 twin primes 等） |
| 5 | **GRH 单独** | `E(x)≪_ε x^{1/2+ε}`（例外集） | **否**（almost-all；无法排除单个例外） | Hardy–Littlewood 1924；Goldston 1992；2026 survey/Pintz–Althöfer 精确形式 |
| 6 | **GRH（三素数）** | 充分大奇数 = 三个素数 | 否（不同问题；且已被 Vinogradov/Helfgott 无条件化） | Hardy–Littlewood 1923 |
| 7 | **GRH + pair correlation（Dirichlet L）** | 超越 GRH 的 PNT-AP/最小 AP 素数界（Kandhil–Languasco–Moree 2024/26；K-L-M 2026 arXiv:2607.14515）；由 GRH+PC 可推 Elliott–Halberstam（K-L-M arXiv:2411.19762） | **否**（只到 EH 层面；EH 本身不足以 binary Goldbach） | [预印本/条件] |
| 8 | **Elliott–Halberstam（EH）** | EH + 加权筛 ⇒ (1+1.4)（Li–Liu 2026）；EH 单独不给出 binary Goldbach | **否** | Li–Liu arXiv:2606.05224v2；[事实/预印本] |
| 9 | **Bombieri–Vinogradov / BFI 4/7** | Chen (1+2)、Li–Liu (1+1.9) 等 | **否** | [事实] |
| 10 | **Chowla（两点/任意阶）** | 未发现任何蕴含 binary Goldbach 的定理；Chowla 是 LF/μ 的二点相关，属 parity barrier 范围 | **否（未知蕴含）** | [检索结果] |
| 11 | **Lindelöf（或 subconvexity）** | 未发现任何蕴含 binary Goldbach 的定理；只改进 L 值/零点密度型误差，不触及 additive correlation | **否（未知蕴含）** | [检索结果] |
| 12 | **Hooley 型假设** | 未找到“Hooley 型条件 ⇒ binary Goldbach”的已知定理 | **否（未知）** | [检索结果] |
| 13 | **Piatetski-Shapiro 型** | 只有 Waring–Goldbach / Piatetski-Shapiro 素数的变体（如 arXiv:2603.00660、2511.07164），与 binary Goldbach 无关 | **否** | [检索结果] |
| 14 | **函数域（F_q[t]）无条件** | G-W-X Thm 1.5：q>10^200 固定，次数 d≥3，`Σ_{F∈M_{d−1}}Λ(F)Λ(N−F)=q^{d−1}𝔖_q(N)+O_q(q^{23d/24})` | **不是 ℤ** | GWX arXiv:2611.18825 Thm 1.5（[预印本]） |

### 4.1 “更弱/不同的假设”结论

- **没有已知的、比 H_Ratios+GRH 更弱且能推出完整 binary Goldbach 的假设。** 所有更弱的条件（GRH、GRH+pair correlation、EH、BV/BFI、Chowla、Lindelöf、Hooley、Piatetski-Shapiro）都只给 almost-all 或 (1+1.x)，或根本没有已知蕴含。
- **与 H_Ratios+GRH “强度不可比”的另一条完整路线**是 Li–Liu 的 GRH+Hypothesis S/R；S/R 是关于 LL 构造算子 T_N 的谱零点假设（R 说所有谱零点在 Re=1/2），不是标准猜想，也没有已知的独立证据/反例（phase-6 数值倾向其不成立，但未证明）。
- **强于 Goldbach 的假设**（广义 HL、H_Gold 加权渐近）当然推出 Goldbach，但不算“更弱”。
- **2026 年其他“条件性 Goldbach”声明**：
  - Pandey arXiv:2608.02381（2026-08-03）：“every even n≥6 is the sum of a prime and a member of a twin prime pair” 的**中间猜想**——**蕴含** Goldbach 与 twin prime（更强，不是更弱）。其条件结果：若 twin primes 下界 ~ c z/log²z，则正比例偶数可表示（Romanov+Selberg sieve），并验证到 10^14。**[预印本]**，不是“从更弱假设证明 Goldbach”。
  - Zenodo 23155084（Arneth, 2026-10-05）PIHR-Goldbach-XXV：自述 “This manuscript does not prove the Goldbach conjecture or the Riemann hypothesis”；条件路线缺关键估计，非已知结果。**[未核验社区预印本]**
  - arXiv:2611.09007（2026-11-06）“An Elementary Proof of the Binary Goldbach Conjecture”：**[未核验声明]**，摘要主结论是 O(n/log²n) 上界（已知方向的上界，不能推正性），不可靠（phase-7 已标注）。
  - Waring–Goldbach under GRH in short intervals（Guo, arXiv:2609.16048, 2026-09）：不同问题（Waring–Goldbach），非 binary Goldbach。

---

## 5. “New since phase-8”摘要

1. **WX25 确认并细化**：phase-8 只知道“WX25 = 素数导子 Ratios 猜想”；本轮找到精确论文（Wang–Xu, IMRN 2025, arXiv:2405.04094v2）、精确 Conjecture 2.1 陈述、以及“**WX25 没有证明任何情形**（只有条件性 Thm 1.2 + Cor 1.3）”的结论。**GWX 的复合导子 RC_D 是真正的新内容，也是最未验证的推广。**
2. **GWX 已有 Hexagon 版本**（hexagon:2611.00423v1, 36 页，2026-11-13）与一个 AI 辅助精读（cxy0714.github.io, 2026-11-16）；**无 arXiv 引用、无同行评议、无正式批评**。精读的“额外假设”疑虑未核验，需 phase-11 task-37 的 `H_Ratios^min` 审计来回答。
3. **2024–26 Ratios-over-ℚ 无新突破**：一般 Dirichlet 族 2/2 仍只有猜想/受限版本；最强仍是 Čech 2024（实特征、单 shift、GRH）与 Gao–Zhao（特殊族、单 shift、GRH）。WX25 的 2/2 prime-modulus 也仍是猜想。
4. **Lee v2（2026-11-03）更新**：覆盖所有固定偶差、弱化 ratios 假设、改进误差；这是 ratios⇒Twin Prime 的进展，不是 Goldbach/Dirichlet。
5. **条件性 binary Goldbach 格局不变**：仍只有 GWX（RC_D+GRH）与 Li–Liu（S/R+GRH）两条完整路线；没有更弱的已知标准假设路线。函数域 Goldbach 无条件（G-W-X Thm 1.5）仍是蓝图而非 ℤ 结果。

6. **WX25 “GRH-alone hope” 已定位并分析**（新增 §1.5）：原文只希望 “GRH alone” 证明 **Harper 的 Conjecture 1.1（λ 的一次矩字符和 o(√x)，1≤x≤r^A）**，即在不假设 Ratios 的情况下直接得到 λ-相消；**不是** GRH ⇒ Ratios，也不是 GRH ⇒ 2/2 平均。ℚ 上已有 Harper 2023 的 r-范围无条件版；函数域上 WX25 只说 “likely”（2025-08 时点），截至 2026-11-21 未找到已发表的无条件函数域 WX25 Thm 1.2；2026 的 Verreault–Xu arXiv:2611.09753 解决的是**随机矩阵版本**（Harper 猜想的 U(N) 类似物）。对 GWX/Goldbach 而言：WX25 的 remark **不能绕过 Ratios 得到 2/2**，最多是 phase-11 Route C（截断 μ + AFE）的动机；GRH-only Goldbach 需要新的 GRH-条件 2/2 负矩/倒数矩定理，目前没有。

---

## 6. 判断与建议 [推测]

- **WX25 本身不是瓶颈的全部**：它只覆盖素数模，且猜想未证。GWX 真正需要的复合导子 2/2 RC_D(ω_D) 目前**没有任何部分结果**（连单 shift 的复合导子 ratios 都没有）。
- **Ratios-over-ℚ 的下一步现实目标**（与 phase-8 一致）：先把 Čech/Gao–Zhao 的单 shift、受限 range 结果提升到 **2/2**（哪怕只在素数模、|Im|≤c log q 的 range），再尝试复合导子。WX25 的 Conjecture 2.1 提供了精确的“目标陈述”，可作为第一阶段目标。
- **风险**：GWX 的复合导子 parity-twist 推导若确有未声明的额外假设（见 §2.2 二手疑虑），则 RC_D(ω_D) 可能不是充分的；这一点应由独立审计（phase-11 task-37/38）判定，而不是依赖 AI 精读。
- **结论**：截至 2026-11-21/22，**Ratios 路线仍是“单一、明确、未证、但结构最完整”的 Goldbach 条件路线**；WX25 是它的 prime-conductor 模板，GWX 是它的完整（但未验证的）应用。没有更弱条件路线。

---

## 7. 引用清单（URL/DOI；访问日期 2026-11-21，部分 11-22 凌晨）

**WX25 / Ratios 猜想与证据**
1. V. Y. Wang, M. W. Xu, *Harper's beyond square-root conjecture*, Int. Math. Res. Not. IMRN 2025 (2025), no. 18, rnaf279；arXiv:2405.04094v2（v1 2024-05-07；v2 2025-08-26）。https://arxiv.org/abs/2405.04094
2. J. B. Conrey, D. W. Farmer, M. R. Zirnbauer, *Autocorrelation of ratios of L-functions*, Commun. Number Theory Phys. 2 (2008) 593–636；arXiv:0711.0718。
1b. **WX25 中 “GRH-alone hope” 的引用映射与相关**：A. J. Harper, *Sharp conditional bounds for moments of the Riemann zeta function*, arXiv:1305.4618（2013）；K. Soundararajan, *Moments of the Riemann zeta function*, Ann. of Math. 170 (2009) 981–993；B. Szabó, *High moments of theta functions and character sums*, Mathematika 70 (2024)；H. M. Bui, A. Florea, *Negative moments of the Riemann zeta-function*, J. reine angew. Math. 806 (2024) 247–288；H. M. Bui, A. Florea, J. P. Keating, *The Ratios Conjecture and upper bounds for negative moments of L-functions over function fields*, Trans. Amer. Math. Soc. 376 (2023) 4453–4510；A. Florea, *Negative moments of L-functions with small shifts over function fields*, IMRN 2024(3) 2298–2337；W. Verreault, M. W. Xu, *Harper's beyond square-root conjecture for random matrices*, arXiv:2611.09753v2（2026-11-06）；É. Fouvry, I. E. Shparlinski, P. Xi, *Short sums of the Möbius function over function fields*, arXiv:2610.28822（2026-10-20）；Z. Y. Ma, *Optimal homological vanishing: cancellation of character sums and Patterson's conjecture over F_q[t]*, arXiv:2606.26440（2026-06-24）。
3. J. B. Conrey, N. C. Snaith, *Applications of the L-functions ratios conjectures*, Proc. London Math. Soc. (3) 94 (2007) 594–646；arXiv:math/0509480。
4. H. M. Bui, J. P. Keating, *On the mean values of Dirichlet L-functions*, arXiv:math/0607199（2006）。
5. J. Goes, S. Jackson, S. J. Miller, D. Montague, K. Ninsuwan, R. Peckner, T. Pham, *A unitary test of the Ratios Conjecture*, arXiv:0909.4916（2009）。
6. M. Čech, *The Ratios conjecture for real Dirichlet characters and multiple Dirichlet series*, arXiv:2110.04409v3；Trans. Amer. Math. Soc. 377 (2024), no. 5, DOI 10.1090/tran/9113。
7. P. Gao, L. Zhao：arXiv:2210.08840（2022）、2304.14600（2023）、2311.08626（2023）、2402.17198（2024）、2404.05081（2024）。
8. D. Fiorilli, S. J. Miller, *Surpassing the Ratios Conjecture in the 1-level density of Dirichlet L-functions*, arXiv:1111.3896（2011）。
9. A. J. Harper, *The typical size of character and zeta sums is o(√x)*, arXiv:2301.04390（2023）。
10. A. J. Harper, *Better than squareroot cancellation in number theory*, arXiv:2512.23681（2025-12-29；ICM 2026 Proceedings）。
11. V. Y. Wang, *Notes on zeta ratio stabilization*, arXiv:2402.01214（2024-02；updated 2024-03）。
12. W. Sawin, *Square-root cancellation for sums of factorization functions over squarefree progressions in F_q[t]*, Acta Math. 233 (2024) 285–418；arXiv:2102.09730。

**GWX / Landau 问题**
13. H. Gou, V. Y. Wang, M. W. Xu, *Landau's problems through ratios of L-functions*, arXiv:2611.18825v1（2026-11-13，46 页）。https://arxiv.org/abs/2611.18825
14. 同论文 Hexagon 版：hexagon:2611.00423v1（2026-11-13，36 页）。https://hexagonmath.org/2611.00423v1
15. S. Lee, *The Hardy-Littlewood asymptotic for prime pairs of fixed even difference from a uniform zeta-ratios conjecture*, arXiv:2610.32672v2（v1 2026-10-23；v2 2026-11-03）。https://arxiv.org/abs/2610.32672
16. H. Gou, *Moments of the number of representations as sums of two prime squares*, arXiv:2607.08985（2026-07-09）。

**条件性 Goldbach / 相关**
17. Li–Liu 条件性证明（2026-11-13）：https://mrc.sdu.edu.cn/english/info/1018/1514.htm ；Li–Liu (1+1.9), arXiv:2606.05224v2。
18. G. H. Hardy, J. E. Littlewood, *Partitio Numerorum* III（Acta Math. 44 (1923)）、V（Proc. LMS (2) 22 (1924)）；D. A. Goldston（Amalfi Conf. 1992）。
19. N. Kandhil, A. Languasco, P. Moree, arXiv:2411.19762（2024-11；Math. Ann. 2026）与 arXiv:2607.14515（2026-07-16）。
20. T. Pandey, *An intermediate conjecture between Goldbach and Dubner: every even number is the sum of a prime and a twin prime*, arXiv:2608.02381v2（2026-08-03）。
21. B. Arneth, *A Conditional Route to Binary Goldbach with an Explicit Correlation Gap (PIHR-Goldbach-XXV)*, Zenodo DOI 10.5281/zenodo.23155084（2026-10-05；**[未核验]**）。
22. K. Qazaqzeh, A. Rawashdeh, *An Elementary Proof of the Binary Goldbach Conjecture*, arXiv:2611.09007（2026-11-06；**[未核验声明，不可依赖]**）。
23. Y. Guo, *The Waring-Goldbach problem in short intervals under the Generalized Riemann Hypothesis*, arXiv:2609.16048（2026-09-12）。
24. H. Gou 之外 Piatetski-Shapiro 相关：arXiv:2603.00660、2511.07164（Waring–Goldbach/P-S 素数，与 binary Goldbach 无关）。
25. 二手评论（**[二手/未核验]**）：cxy0714.github.io, *Landau's problems through ratios of L-functions*（2026-11-16）。https://cxy0714.github.io/research-news/deep_reads/2026-11-16-hexagon_2611.00423/

**本团队报告**
26. phase-7/lit/alternative-routes.md（task-30）；phase-8/lit/ratios-status.md（task-32）；phase-6/0-phase6-报告.md。

---

## 附录 A：关键原文

1. **WX25 Conjecture 2.1**（arXiv:2405.04094v2, p.7）：见 §1.2 全文。
2. **WX25 Theorem 1.2**：
   > “Assume GRH for F_r, and the Ratios Conjecture [9, (5.6)] for F*_r. Then Conjecture 1.1 is true in the discrete case (1.2) when c = λ.”
3. **WX25 关于函数域/GRH-alone 的原文**：
   > “It is natural to hope that GRH alone might suffice, by adapting techniques of [18,32,34] from moments to ratios. … It would be interesting to pursue this further. … over function fields F_q(t), there is now enough progress on the Ratios Conjecture that one can likely prove an unconditional version of Theorem 1.2 in one or more families for all q large enough…”
4. **GWX 与 WX25 的关系（GWX 原文 §1.1）**：
   > “Wang–Xu [WX25, Conjecture 2.1] conjecture a power saving for prime conductors. Hypothesis 1.1 assumes the formula for all primitive conductors and specifies the exponent ω_D.”
5. **GWX 素数 q 引用 WX25（原文 §3.1 附近）**：
   > “For prime q, this uses the two terms of Wang–Xu [WX25, Conjecture 2.1], with the exact primitive parity counts.”
6. **GWX 复合导子**（Hypothesis 1.1 原文）：
   > “…uniformly for all conductors q>1, including composite conductors…”
7. **Lee v2 comment**：
   > “The result now covers all fixed positive even gaps. We also weaken the ratios assumption and improve the error bounds.”
8. **二手精读的疑虑（[二手/未核验]，仅存档）**：
   > 概括：“Theorem 1.1 的 parity-twist 平均并非标准 RCD 的直接推论，需额外未列出的均匀性假设”；“Theorem 1.3 依赖更强的 Hypothesis 4.1”；“Theorem 1.4 的 Waxman 参数范围未验证”。

---

## 附录 B：核查方式与局限

- **逐字核对**：WX25 PDF 全文（27 页，v2）：摘要、Conjecture 1.1/2.1、Theorem 1.2、Corollary 1.3、§2 derivation、关于 GRH-alone/函数域的段落；GWX PDF 全文（46 页）相关段落（Hypothesis 1.1、Theorem 1.1、§3.1、参考文献 [WX25]/[Lee26]/[Saw24]/[SS22a]/[Har23]/[Har26]/[Wan24]）；Hexagon 页面（hexagon:2611.00423v1）；cxy0714 精读页面；Zenodo 23155084 页面；Semantic Scholar API（引用查询：GWX 为空；Lee 查询遇 429）。
- **仅摘要级核对**：Čech、Gao–Zhao 各篇、Goes 等、Bui–Keating、Conrey–Snaith、Harper 2301.04390/2512.23681、Wang 2402.01214、Lee 2610.32672v2（摘要+comment）、Gou 2607.08985、Pandey 2608.02381、arXiv:2611.09007、Guo 2609.16048。
- **未核验/不可信**：cxy0714 精读（AI 辅助研究新闻）；Zenodo 23155084；arXiv:2611.09007；任何未在 arXiv 出现的“Goldbach 证明”声明。
- **局限**：WSL 下 github/Wikipedia 不可达；Semantic Scholar 限流；arXiv 检索偶发限流；Hexagon 为 2026 场景世界的新平台（ID 与 arXiv 不同）；时间盒 75 分钟（本报告按环境时钟约 70 分钟完成）。所有“gap/强弱”判断标 [推导]/[推测]。
