# Phase-12 文献：Lee 2610.32672v2 / 「GRH + X ⇒ binary Goldbach」路线盘点 / Ratios 近年进展

> 作者：goldbach-researcher（task-50）。日期：2026-11-22 19:36–21:10（Asia/Shanghai）。URL/arXiv 访问日期 2026-11-22。
> 前置：`phase12/0-plan.md`（RAT(c>2) 框架）；`phase11/lit/ratios-2026-survey.md`；`phase7/lit/alternative-routes.md`。
> 标注：**[事实]** 已证/已发表（含已发表预印本声称）；**[预印本]** 未评审；**[推导]**；**[推测]**；**[检索结果]** 未找到。
> 本报告只做文献状态，不重新证明任何定理。

---

## 0. 摘要（结论先行）

1. **Lee, arXiv:2610.32672v2 证明的是「固定偶差 h 的 prime pairs 的 Hardy–Littlewood 渐近」**（Thm 1.1：`Σ_{n≤x}Λ(n)Λ(n+h)=S(h)x+o(x)`，`π_h(x)~S(h)x/(log x)^2`；Thm 1.2 给权函数误差 `x^{−Δ(ϑ)+ε}`，加 RH 后 `x^{ϑ−7/8+ε}`），**不覆盖 Goldbach**：它没有 Dirichlet 族/奇偶投影/任意偶数 N 的论证。其假设 **Hypothesis 2.1** 是 Conrey–Snaith [3, Conjecture 2.1] 的 **2/2 zeta-ratios 有限积分形式**，限制在 **移位区域** `3/64≤Re shifts≤5/64`（即距临界线约 0.047–0.078 的固定距离）、`|Im|≤U^ν`、误差 `O(U^{ϑ+ε})`，`1/2≤ϑ<(39−√177)/32≈0.8029`。**与 GWX Hyp 1.1 不可直接比较**（不同族：ζ vs Dirichlet；不同 shift 构型：移位区域 vs 临界线分子；不同误差形式），但它是最接近 phase-12「移位区域 2/2 Ratios」的已发表模板，且其假设的「saving / shift」比值 ≥2.5（见 §1.5），说明 **c>2 在移位区域并不苛刻**。
2. **「GRH + X ⇒ binary Goldbach（所有大偶数）」的已知完整路线只有两条**：GWX（GRH + RC_D(ω_D)，arXiv:2611.18825, 2026-11-13）与 Li–Liu（GRH + Hypothesis S/R，2026-11-13，S/R 为 LL 算子的 ad hoc 谱假设）。除此之外：**quasi-RH/半平面假设只给 almost-all**（如 H. Li–Z. Liu arXiv:2610.26756：若所有 Dirichlet L 零点 Re≤Θ<11/12，则 `E_+(N)≪N^{1/2}(log N)^{100}`）；**GRH 单独只给 `E(x)≪x^{1/2+ε}`**（Hardy–Littlewood 1924；Goldston 1992 log 改进）；**EH/BV/BFI 只到 1+2/1+1.9/1+1.4**（parity barrier）；**pair correlation 只到 EH 层面**；**Chowla/Sarnak 未发现蕴含 binary Goldbach 的定理**。**没有已知「GRH + 严格弱于 Ratios 的假设 ⇒ 完整 Goldbach」的定理**；phase-12 的 RAT(c>2) 本身是待证目标，不是已知定理。
3. **Montgomery–Vaughan 1975 的准确陈述（纠正常见误记）**：**无条件**证明 `E(X) ≪ X^{1−δ}`（某绝对 δ>0，可有效计算）；**不是** GRH 条件下的结果。GRH 条件下 `E(x)≪_ε x^{1/2+ε}` 属于 Hardy–Littlewood 1924（Goldston 1992 换成 log 幂）。见 §2.4 的三重出处核对。
4. **Ratios Conjecture 2024–2026 进展**：ℚ 上 **Dirichlet 族 q-aspect 的 1/1** 有 GRH-条件结果（Čech 2024, Trans. AMS 377, arXiv:2110.04409：实 Dirichlet 特征、单 shift、受限 range；Gao–Zhao 2022–24：二次/三次/四次 Dirichlet/Hecke 族、单 shift、受限 range，均 GRH 条件）；**ℚ 上 2/2 仍只有猜想**（WX25 素数模 2/2 猜想，arXiv:2405.04094，未证任何情形；GWX 把它推广到全导子并当作假设）。**函数域 Dirichlet 族 2/2 特殊情形已证**：Bui–Florea–Keating（arXiv:2109.10396；Trans. AMS 376 (2023) 4453–4510）对 **平方自由二次 Dirichlet L（F_q[x]）** 证明 1/1 平均（`Re β≫g^{−1/2+ε}`）与 **2/2 乘积平均**（分母 shifts `Re>g^{−1/4+ε}`），3/3 需 `>g^{−1/6+ε}`；关键工具是负矩上界；并恢复 one-level density（Fourier 支撑 (−2,2)）。ℚ 上「移位区域 Ratios」的已发表定理：**没有**；Lee 的 Hypothesis 2.1 是 ζ 的移位区域**假设**，Baluyot–Čech 2025（arXiv:2501.12529）只是 multiple Dirichlet series **启发式**，Baluyot–Conrey–Irfan–Snaith 2026（arXiv:2611.05000）是 shifted moments（条件）+ RH 下的关系，非 Dirichlet ratios 定理。
5. **Alpöge 声明（2026-11-20）之后**：arXiv 检索**未发现**新的 Goldbach/RH→Goldbach 预印本；GWX 仍为 v1（2026-11-13）、OpenAlex 引用数 **0**（2026-11-22 查询）、Semantic Scholar 无引用；未发现对 GWX 的改进或批评（除 phase-11 记录的 AI 辅助精读）。**后 Alpöge 新增的相关文献**：Michael Rubinstein（Waterloo）的 164 页 RH 证明人类可读写作（2026-11-21，仅 ζ 情形）与核验页（2026-11-21：全部检查通过）——不涉及 Goldbach/Ratios。**结论：没有公开工作利用「RH 已被证明」来推进 Goldbach 或改进 GWX。**
6. **对 c>2 目标的可用性裁决**（§4 详述）：Lee 的论文**不能直接使用**（不同族/移位构型/不覆盖 Goldbach），但提供两个可用模板：(i) **移位区域 2/2 ratios 假设**在其参数范围内 saving/shift ≥2.5（见 §1.5 计算），说明 c>2 比 Conrey–Snaith 型移位假设弱得多；(ii) Lee 从 ratios 假设推出零无带 `35/64≤Re s≤37/64` 与零点计数 `N_>(9/16,T)≪T^{ϑ+ε}` 的推导，是「RAT(c) ⇒ 何种 RH 型后果」的现成模板——phase-12 可用它检查 RAT(c>2) 是否甚至能替代完整 GRH（quasi-RH 路线）。函数域 BFK 的负矩方法是最接近「证明移位区域 Dirichlet 2/2」的技术模板。**总裁决：文献没有现成的 c>2 输入；但它指出 c>2 的量级是温和的，并给出两条可试的技术模板。**

---

## 1. SeungJu Lee, arXiv:2610.32672v2：精确内容与假设

### 1.1 文献信息

| 项 | 内容 |
|---|---|
| 标题 | *The Hardy–Littlewood asymptotic for prime pairs of fixed even difference from a uniform zeta-ratios conjecture* |
| 作者 | SeungJu Lee |
| 版本 | **v1 2026-10-23；v2 2026-11-03**（v2 comment：“The result now covers all fixed positive even gaps. We also weaken the ratios assumption and improve the error bounds”；16 页；论文标注 “November 4, 2026”） |
| arXiv | https://arxiv.org/abs/2610.32672 |
| 本地全文 | `phase12/lit/lee_v2.pdf` / `lee_v2.txt`（16 页，已抽取核对） |

### 1.2 Hypothesis 2.1（精确陈述，逐字转写自 §2）

> **Hypothesis 2.1 (Uniform two-over-two ratios formula).** For every ε>0, as U→∞,
> `∫_0^U ζ(1/2+α+it)ζ(1/2+β−it) / (ζ(1/2+γ+it)ζ(1/2+δ−it)) dt
>  = U·Y(α,β;γ,δ) + ∫_0^U (t/2π)^{−α−β}·Y(−β,−α;γ,δ) dt + O_ε(U^{ϑ+ε})`,
> uniformly for
> `3/64 ≤ Re α, Re β, Re γ, Re δ ≤ 5/64`, `|Im α|,|Im β|,|Im γ|,|Im δ| ≤ U^ν`
> with fixed `1/2≤ϑ<ϑ* := (39−√177)/32 ≈ 0.8029` and fixed `0<ν≤1/4`.

其中（原文 (2.1)–(2.2)）：
`Y(α,β;γ,δ) = ζ(1+α+β)ζ(1+γ+δ) / (ζ(1+α+δ)ζ(1+β+γ)) · A(α,β;γ,δ)`，
`A(α,β;γ,δ) = Π_p [(1−p^{−1−γ−δ})(1−p^{−1−β−γ}−p^{−1−α−δ}+p^{−1−γ−δ})] / [(1−p^{−1−β−γ})(1−p^{−1−α−δ})]`.
原文说明：**“The main terms are those in [3, (2.8), (2.10)], restricted to (2.4).”** 即 Conrey–Snaith [3]（Applications of the L-functions ratios conjectures, Proc. LMS 94 (2007) 594–646, arXiv:math/0509480）的 2/2 公式；Lee 把它**限制在 shift 区域 `[3/64,5/64]`、放松误差到 `U^{ϑ+ε}`、作为关于有限积分的独立假设**。原文还指出 Conrey–Snaith 原文“assume RH throughout”；Lee 从该 ratios 假设推导零无带与零点计数，再结合 Ingham 的无条件估计。

### 1.3 主要定理

> **Theorem 1.1.** Assume Hypothesis 2.1. Then, as x→∞，对**每个固定正偶数 h**：
> `Σ_{n≤x} Λ(n)Λ(n+h) = S(h)x + o(x)`，`A_h(x) = S(h)x + o(x)`，`π_h(x) ~ S(h)·x/(log x)^2`。其中 `A_h(x)=Σ_{p≤x, p+h prime} log p log(p+h)`，`S(h)=2C₂Π_{p|h,p>2}(p−1)/(p−2)`，`C₂=Π_{p>2}(1−1/(p−1)²)`。
>
> **Theorem 1.2.** Assume Hypothesis 2.1，W∈C_c^∞((1,κ_h))，κ_h=1+1/(25h)。对每个固定 0<ε<Δ(ϑ)：
> `Σ_{n≥1} Λ(n)Λ(n+h)/n · W(n/x)² = S(h)∫_0^∞ W(u)² du/u + O_{h,W,ε}(x^{−Δ(ϑ)+ε})`，
> 其中 `Δ(ϑ)=7/16−ϑ+ϑ/(3−ϑ)>0`；**若再加 RH**，误差改进为 `O_{h,W,ε}(x^{ϑ−7/8+ε})`。
>
> **Corollary 1.3.** Under Hypothesis 2.1：`B_h(x) = S(h) log x + o(log x)`（B_h 为加权 prime-pair 和）。

具体数值（原文）：`ϑ=3/4` → `x^{−1/48+ε}`，RH 下 `x^{−1/8+ε}`；`ϑ=4/5` → `x^{−1/880+ε}`，RH 下 `x^{−3/40+ε}`；`ϑ=1/2`（平方根 ratios 误差）→ `x^{−11/80+ε}`，RH 下 `x^{−3/8+ε}`。§8 还推出 truncated Chebyshev 函数平方增量的二阶差分与 Nyman–Beurling 判据的有限近似关系。

### 1.4 Lee 覆盖什么、不覆盖什么

- **[事实] 覆盖**：固定偶差 h 的 **prime pairs**（孪生素数型）的 Hardy–Littlewood 渐近；P_h(x)~S(h)x/(log x)^2；加权定量误差；加 RH 的改进；B_h 的对数渐近。
- **[事实] 不覆盖 binary Goldbach**：全文没有 Goldbach 的表述（`grep -i goldbach` 无匹配）；不涉及 Dirichlet 特征族、模 N 的奇偶投影、任意偶数 N=m+n、或 `Σ_{m+n=N}`。它处理的是**固定差 h**（平移相关），不是**固定和 N**。
- **不覆盖 twin prime conjecture 本身**（只有 HL 渐近，不保证非空/无穷多）；也不覆盖一般 primitive character 的 q-aspect。
- 其假设是**ζ 的移位区域 2/2 ratios**（不是 Dirichlet 族），且是**有限积分**（对 t 积分）而非 GWX 的 `T≤100log(2q)` 的逐 shift 一致/全纯形式。

### 1.5 与 GWX Hypothesis 1.1 的比较（弱/强/不可比）

| 方面 | Lee Hypothesis 2.1 | GWX Hypothesis 1.1（RC_D(ω_D)） |
|---|---|---|
| 族 | **ζ**（单个 L-函数，t-积分） | **primitive Dirichlet 族** mod q（q-aspect，含复合导子） |
| shift 构型 | **移位区域**：所有 4 个 shift 实部 ∈[3/64,5/64]（距临界线固定 0.047–0.078） | **分子在临界线** Re a=Re b=1/2；分母 Re s=Re t=1/2+η |
| 误差 | `O(U^{ϑ+ε})`，`1/2≤ϑ<0.8029`（saving `1−ϑ` ∈ (0.197,0.5]） | `O(q^{1−ω_D+ε}(1+T)^B)`，ω_D∈(0,1/2]，**可任意小** |
| 形式 | 有限积分（ordinary finite integral） | 族平均的逐 shift 一致估计（holomorphic errors，供插值） |
| 状态 | **假设**（Lee 明确视为 standalone hypothesis；未证） | **假设**（GWX 明确未证；WX25 素数模版本的推广） |
| 覆盖 Goldbach | **否**（只 prime pairs） | **是**（Thm 1.1，若 RC_D 成立） |

**[推导] 定量比较“saving vs shift”**：Lee 的 shift 最大为 `5/64≈0.0781`，最小 `3/64≈0.0469`；误差 saving `1−ϑ` 在 `ϑ=1/2` 时为 `0.5`、在 `ϑ=ϑ*` 时约 `0.197`。因此在其允许范围内：

  `saving / max-shift ≥ 0.197/0.0781 ≈ 2.52`（最不利端点），而 `saving / min-shift ≥ 0.5/0.0469 ≈ 10.7`（最有利端点）。

**即：Lee 所假设的移位区域 ζ-2/2 ratios，其 saving 至少是 shift 的 2.5 倍。** 而 phase-12 的 RAT(c>2) 只要求 `saving = c·η > 2η`（shift≈η）——**在「saving/shift」这一无量纲意义上，c>2 比 Lee 假设的移位区域 ζ-ratios 更弱/更温和**。**[推测]** 这支持 c>2 不是“苛刻常数”，而是移位区域 ratios 的自然门槛。

**但不可直接迁移**：[事实/推导] (i) Lee 是 ζ 不是 Dirichlet；(ii) 它的 shifts 固定在 [3/64,5/64]（不随族尺寸变小），而 RAT(c) 要求分子距 1/2 约 η（可任意小）且随 η 一致；(iii) Lee 是有限 t-积分，不含 holomorphic/interpolation 结构（GWX 需要）；(iv) Lee 的假设没有被证明，只是被使用。因此 **Lee 不能作为 RAT(c>2) 的现成输入**，只能作为“移位区域 ratios 是合理且温和的”证据与技巧模板。

---

## 2. 「GRH + X ⇒ binary Goldbach」已知条件路线盘点

### 2.1 完整路线（能推出所有充分大偶数）

| # | 假设 | 结论 | 出处/状态 |
|---|---|---|---|
| 1 | **GRH + RC_D(ω_D)**（Dirichlet primitive 2/2，复合导子，临界线分子，ω_D>0 任意） | `Σ_{m+n=N}Λ(m)Λ(n)=N𝔖(N)+O_ε(N^{1−ω_D+ε})` ⇒ Goldbach | **Gou–Wang–Xu, arXiv:2611.18825**（2026-11-13，[预印本]，Theorem 1.1）。**RC_D 未证**（WX25 素数模 2/2 亦未证，arXiv:2405.04094） |
| 2 | **GRH + Hypothesis S（或 R）**（Li–Liu 构造的算子 T_N 的谱零点假设） | `G(N)=c_φS(N)+O(S(N)/h(N))` 或 `+O(√(S/N)(logN)^{3/2})` ⇒ 正表示数 | **Li–Liu**（2026-11-13，[预印本]，MRC；S/R 是 ad hoc 谱假设，非标准猜想；phase-6 数值倾向 R 不成立但未证明） |
| 3 | **Hardy–Littlewood 渐近（H_Gold）** | 渐近公式 ⇒ Goldbach | **[猜想]**（强于 Goldbach；GWX 的目标量） |
| 4 | **广义 Hardy–Littlewood（素数元组/线性形式）** | 对系统 {n,N−n} 的渐近 | **[猜想]**（最强；蕴含 twin primes 等多问题） |

**结论**：除 GWX 与 Li–Liu 外，**没有第三条已知完整路线**；两者都要求 GRH 之外的新假设（Ratios 或 S/R）。

### 2.2 只能推出 almost-all 的路线（不能推出全部）

| # | 假设 | 结论 | 出处 |
|---|---|---|---|
| 1 | **GRH 单独** | `E(x)≪_ε x^{1/2+ε}`（例外集） | Hardy–Littlewood 1924；Goldston 1992（log 改进）；Pintz 2018 §1；Bhowmik–Grimmelt 2026 survey Thm 3.1（更一般：Re ρ≤Θ<3/4 ⇒ `E(X)≪X^{2Θ−1/2+ε}`；Θ=1/2 即 GRH） |
| 2 | **quasi-RH：所有 primitive Dirichlet L 零点 Re≤Θ<11/12** | `E_+(N)≪_Θ N^{1/2}(log N)^{100}`，`E_−(N)≪N^{1/2}(log N)^{100}`（sums/differences of primes 的例外集） | **H. Li, Z. Liu, arXiv:2610.26756**（2026-10-19，[预印本]）：“Fourth moments of prime exponential sums and exceptional sets for sums and differences of primes”；用 minor arcs 的 smoothed prime exponential sum 四阶矩 |
| 3 | **pair correlation of zeros + GRH** | 推 Elliott–Halberstam/PNT-AP 型改进（Kandhil–Languasco–Moree, arXiv:2411.19762；arXiv:2607.14515），但仍无 full Goldbach | [预印本]；pair correlation 本身是猜想（Montgomery 1973） |

### 2.3 EH / level of distribution / parity barrier 的文献立场

- **[事实] 没有任何定理从 Elliott–Halberstam（或 BV/BFI/level>1/2）推出 binary Goldbach。** 已知后果止于：
  - BV/BFI + Chen 型加权筛 ⇒ (1+2)（Chen 1966/1973）；
  - **Elliott–Halberstam ⇒ (1+1.4)**（Li–Liu, arXiv:2606.05224v2 摘要：“Assuming the Elliott–Halberstam Conjecture, the exponent 1.9 can be improved to 1.4”）；无条件 (1+1.9) 亦是其成果；
  - parity barrier：非负权筛法无法区分 Ω(n) 的奇偶，Chen 的 switching principle 只给上界（Li–Liu (1+1.9) §8.1/§8.2.1 原文；Friedlander–Iwaniec, *Opera de Cribro*, AMS 2010）。
- **结论 [事实/检索结果]**：EH 及以上分布假设**不能**推出 binary Goldbach；这是 parity barrier 的标准立场，文献中没有反例。

### 2.4 Montgomery–Vaughan 1975：准确陈述与常见误记（任务 2(d) 核实）

- **原文/书目**：H. L. Montgomery, R. C. Vaughan, *The exceptional set in Goldbach's problem*, **Acta Arithmetica 27 (1975), 353–370**；Zbl **0301.10043**；DOI 10.4064/aa-27-1-353-370（zbMATH 记录；EuDML doc 205349）。
- **准确结论 [事实]**：**无条件**证明存在绝对常数 δ>0 使 `E(X) ≪ X^{1−δ}`（X 充分大）。见：
  - Bhowmik–Grimmelt, *The exceptional set of the Goldbach problem*, arXiv:2607.27282（2026）§5 原文：“Montgomery and Vaughan were the first to prove a genuine power saving for its size, in 1975. **Theorem 5.1 (Montgomery–Vaughan). There exists a δ>0 such that |E(X)| ≪ X^{1−δ}.**”；文中亦称 δ “positive effectively computable constant”。
  - Pintz, arXiv:1804.09084（2018）§1：“Montgomery and Vaughan [16] showed that the estimate E(X) ≪_δ X^{1−δ} holds with an unspecified but explicitly calculable value δ>0.”
- **常见误记纠正**：**`E(x)≪x^{1/2+ε}` 的 GRH 条件结果不是 MV1975，而是 Hardy–Littlewood 1924**（*Partitio Numerorum* V, Proc. LMS (2) 22 (1924) 46–56）：“They showed under the Generalized Riemann Hypothesis (GRH) the estimate E(X)≪_ε X^{1/2+ε}”；**Goldston（1992）** 才把 `X^ε` 换成 `log^c X`（Pintz 2018 原文：“apart from the substitution of X^ε by log^c X by Goldston [6] even today the best conditional result on GRH”）。**MV1975 本身没有 GRH 条件假设**；“GRH 下例外集”这一说法应归 Hardy–Littlewood 1924 / Goldston 1992。
- **[推测]** 任务提示中“Montgomery–Vaughan 1975 的 GRH 下例外集结果”可能是把 1924/1992 的结果误挂到 1975 上；本报告已按原始出处纠正。

### 2.5 Chowla / Sarnak 型

- **[检索结果]** 没有已知定理从 Chowla（任意阶）或 Sarnak 的 Möbius randomness 推出 binary Goldbach；Chowla 是两点/多点相关消失，与“每个偶数表示”之间没有已知蕴含。
- 2026 随机模型文献（I. Pylaiev, *Random Chowla and Goldbach Conjectures*, arXiv:2611.14579, 2026-11-10）证明随机乘法函数模型下的 Chowla/Goldbach 型结果；它们是**随机模型**，不是 ℤ 上的条件路线。[预印本]

---

## 3. Ratios Conjecture 2024–2026 进展（Dirichlet 族 q-aspect 的 1/1、2/2、移位区域、函数域）

### 3.1 全表

| 范围 | 结果 | 精确陈述/限制 | 状态/出处 |
|---|---|---|---|
| ℚ，Dirichlet 1/1 | **Čech 2024** | 实 Dirichlet 特征族（real Dirichlet characters），**单 shift**（分子/分母各一个），**some range of shifts**；“This range can be improved by extending the family to include non-primitive characters”；**“All of the results are conditional under the Generalized Riemann hypothesis.”** | **[事实/GRH 条件]** arXiv:2110.04409v3；Trans. AMS 377 (2024), no. 5, DOI 10.1090/tran/9113 |
| ℚ，Dirichlet/Hecke 1/1 | **Gao–Zhao 2022–24** | 二次/三次/四次 Dirichlet 与 Hecke 族，**单 shift**，**certain ranges**，**under GRH**；推论 first moment/one-level density | **[事实/GRH 条件]** arXiv:2210.08840, 2304.14600, 2311.08626, 2402.17198, 2404.05081 |
| ℚ，Dirichlet 2/2 | **无定理** | 只有 WX25 的**素数模 2/2 猜想**（Conjecture 2.1，arXiv:2405.04094，未证任何情形）；GWX 把它推广为全导子 RC_D(ω_D)（假设） | **[猜想]** WX25；[预印本] GWX |
| ℚ，启发式 | **Baluyot–Čech 2025** | 用 multiple Dirichlet series **预测** shifted moments（包括 all even primitive Dirichlet chars conductor ≤Q 的族）；**heuristics，不是定理** | **[预印本/启发式]** arXiv:2501.12529（2025-01-21） |
| ℚ/函数域，移位矩 | **Baluyot–Conrey–Irfan–Snaith 2026** | 研究 `(ζ'/ζ)^k` 长 Dirichlet 截断的均方；在 shifted moments conjecture + RH 下证 short-interval variance 系数 = mean-square 系数的导数；函数域用 unitary trace-sum 平均；**条件性，非 Dirichlet ratios** | **[预印本]** arXiv:2611.05000（2026-11-03） |
| ζ，移位区域 2/2 | **Lee 2610.32672v2** | Hypothesis 2.1：Conrey–Snaith 2/2 的有限积分形式，shift 实部 ∈[3/64,5/64]，误差 `O(U^{ϑ+ε})`，`ϑ<0.8029`；**假设**，用于 prime pairs | **[预印本]**（见 §1） |
| 函数域，Dirichlet 1/1、2/2 | **Bui–Florea–Keating 2021/2023** | 对**平方自由二次 Dirichlet L**（F_q[x]，D 次数 2g+1，g→∞）：1/1 平均 `L(1/2+α,χ_D)/L(1/2+β,χ_D)` 的渐近 for `Re β≫g^{−1/2+ε}`；**2/2 乘积**平均的渐近 for 分母 shifts `Re>g^{−1/4+ε}`；3/3 for `Re>g^{−1/6+ε}`；关键工具是负矩上界；恢复 one-level density 支撑 (−2,2) | **[事实]** arXiv:2109.10396；Trans. AMS 376 (2023) 4453–4510 |
| 函数域，负矩 | **Florea 2021** | 函数域上小 shift 的负矩 | **[事实/预印本]** arXiv:2111.10477 |
| 函数域，Goldbach | **GWX 2026** | 用 Sawin 的 factorization functions/squarefree progressions 方根相消 + 判别式上同调得**无条件**函数域 Goldbach/prime pairs | **[预印本]** arXiv:2611.18825 Thm 1.5/1.6（q>10^200） |
| 函数域，层级 | **Sawin 2024** | 对 μ、Λ、除数函数在 squarefree progressions 中的 level of distribution 估计，随 q→∞ 趋近 1 与平方根相消（G-W-X 的函数域关键输入） | **[事实]** Acta Math. 233 (2024) 285–418；arXiv:2102.09730 |

### 3.2 关键判断

- **[事实]** ℚ 上 **Dirichlet 族 2/2 没有任何定理**（连移位区域、受限 shift 都没有）；1/1 有 GRH-条件的受限族结果（Čech/Gao–Zhao）。WX25 的 2/2 是**素数模猜想**，GWX 把它推广为全导子假设；二者都未证。
- **[事实]** **函数域 Dirichlet 族 2/2 特殊情形已证**（BFK：二次 Dirichlet 族、分母 shifts ≥g^{−1/4+ε}、负矩方法）。这是对 phase-12「移位区域 2/2」最接近的已证技术模板（尽管是函数域、二次族、不是 GWX 的 q-aspect critical-line 形式）。
- **[事实/检索结果]** ℚ 上「移位区域（Re>1/2）Dirichlet 2/2」没有已发表定理；phase-11 报告的“移位区域弱 Ratios 可证（Lead §1 推导）”是**本团队推导**，不是文献。
- **[事实]** Baluyot–Čech 2025 是启发式预测（multiple Dirichlet series），不是定理；Baluyot–Conrey–Irfan–Snaith 2026 是条件性 shifted-moment 关系，不包含 Dirichlet ratios。

---

## 4. Alpöge 声明（2026-11-20）之后的动态

### 4.1 arXiv/引用检索结果

- **[检索结果]** arXiv `abs:Goldbach` 按提交日期降序：最新一篇是 **GWX arXiv:2611.18825（2026-11-13）**；2026-11-20 之后**没有**新的 Goldbach 预印本。
- **[检索结果]** arXiv `abs:"Riemann hypothesis"` 最新提交为 2026-11-19 及更早（Alpöge 公告之前），**无** 2026-11-20 后讨论 RH→Goldbach 的新文。
- **[事实/检索结果]** OpenAlex 对 GWX 的 **citation count = 0**（查询 2026-11-22；`cites:W7235807824`）；Semantic Scholar 引用亦为空/限流；arXiv 上未见引用 GWX 的论文。
- **[检索结果]** 未发现 Alpöge 声明后改进 GWX 假设、或以「RH 已证」为前提重写 Goldbach 条件路线的预印本/论文。

### 4.2 后 Alpöge 的 RH 相关新文献（非 Goldbach）

- **[事实]** Michael Rubinstein（Waterloo）：*Alpöge/Claude proof of the Generalized Riemann Hypothesis* 专页 + **164 页人类可读写作草案**（2026-11-21，仅 ζ 情形；“The inequality (M) is not proved there: its proof is taken from the Lean development”；工作草稿）+ 独立 Lean 核验页（2026-11-21：175,187 模块全部编译、仅三标准公理、Lean kernel 重放 175,187/175,187 通过、nanoda 检查 1,484,729 declarations 无错误）。
  URL: https://www.math.uwaterloo.ca/~mrubinst/alpoge_claude_grh/
  该材料**不讨论 Goldbach 或 Ratios**（页面/摘要层面；PDF 下载不完整（缺 EOF，fitz 读取 0 页），故本报告未逐页核对 164 页正文）。
- **[事实]** 其他独立核验：MIT Sutherland 页（2026-11-21/22 更新，见 phase-11/12 status 报告）；Elliot Arledge GitHub receipts；Bartosz Naskręcki riemann-rev 仪表盘；Simon DeDeo 全量重放。
- **[推测]** 这些活动会继续消耗社区注意力，但短期内不会产出 Goldbach/Ratios 的新数学。

### 4.3 Li–Liu 与 GWX 的更新状态

- **[事实]** GWX arXiv 仍 **v1**（2026-11-13；无 v2）；Hexagon 版 hexagon:2611.00423v1（36 页，2026-11-13）。
- **[事实]** Li–Liu 条件性证明（MRC 2026-11-13）与 (1+1.9)（arXiv:2606.05224v2）均无 2026-11-20 后的版本更新（检索结果；无新评论）。

---

## 5. 对 c>2 目标的可用性裁决（phase-12 直接相关）

**裁决：文献不提供现成的 RAT(c>2) 输入；但 Lee 与 BFK 提供两条可操作的技术模板，且显示 c>2 的量级是温和的。**

1. **[推导] Lee 不可直接用于 RAT(c>2)**：
   - 族不同（ζ vs Dirichlet q-aspect）、shift 构型不同（固定移位区域 [3/64,5/64] vs 临界线分子/η 级分母）、形式不同（有限积分 vs 逐 shift 一致/全纯 + T≤100log2q）、不覆盖 Goldbach。
   - 因此不能把 Lee 的 Hypothesis 2.1 直接当作 RAT(c) 的“已证情形”或“弱化版本”。
2. **[推导] 但 Lee 支持“c>2 是温和门槛”**：
   - Lee 假设的移位区域 ζ-2/2 在其整个允许范围内 **saving/shift ≥2.5**（§1.5 计算）；RAT(c>2) 只要求 `saving = cη > 2η`（shift≈η）。若存在 Dirichlet 族移位区域的类似假设，c>2 远弱于 Lee 所假设的强度。
   - **[推测]** 这提示 phase-12 的 c>2 不应被理解为“比 Conrey–Snaith 更强”，而是“移位区域 ratios 的自然弱化形式”；真正的困难在 q-aspect 的 Dirichlet 族（复合导子、临界线分子、uniform T），而不是 c 的大小。
3. **[推导] Lee 的推导是可复用的“RAT ⇒ quasi-RH 后果”模板**：
   - 从 Hypothesis 2.1 推出：ζ 无零点区 `35/64≤Re s≤37/64`（Lemma 2.2 (2.6)）、`ζ'/ζ(σ₀+iv)≪log²(2+|v|)`（σ₀=9/16）、零点计数 `N_>(σ₀,T)≪T^{ϑ+ε}`（(2.7)–(2.8)），再结合 Ingham 无条件估计。
   - **phase-12 可做**：从 RAT(c)（Dirichlet 族、移位区域、saving cη）用同样的“ratios ⇒ 零无带/零点计数”推导，看能否得到**quasi-RH 级别**的 Dirichlet 零点分布，从而让 Goldbach 论证所需的 GRH 输入减弱为 quasi-RH——这可能把 phase-12 的假设从「GRH + RAT」进一步减为「quasi-RH + RAT」。**[推测]** 值得 liu-auditor 检查。
4. **[事实] 函数域 BFK 是“移位区域 2/2 可证”的最强证据**：二次 Dirichlet 族、分母 shifts 小至 `g^{−1/4+ε}` 时 2/2 平均的渐近已证（负矩上界方法）。**[推测]** 若把 BFK 的负矩机制搬到 ℚ 的 Dirichlet q-aspect 移位区域，可能得到某个 c 的 RAT(c)（c 待定）；这是 phase-12 值得另开任务的文献驱动方向（但 BFK 是函数域、二次族，迁移非平凡）。
5. **[事实] 没有已知「GRH + 弱于 Ratios ⇒ Goldbach」定理**：除 GWX（Ratios）与 Li–Liu（S/R）外无第三条完整路线；quasi-RH 只给 almost-all（Li–Liu 2610.26756）；EH/pair correlation/Chowla 都不够。因此 phase-12 的 RAT(c>2) 目标在文献上是**新的、未覆盖的**：不是“已知定理的整理”，而是“最弱充分条件的探索”。**[推测]** 如果 RAT(c>2) 能被证明（或从 GRH 推出），将是 GWX 之后 Goldbach 条件路线的实质性进展；文献目前只提供工具模板，不提供结论。
6. **给 Lead 的具体文献建议**：
   - 优先读 **Lee v2 §2–§4**（ratios ⇒ 零无带/零点计数 ⇒ prime pairs 的完整链条）与 **BFK arXiv:2109.10396 §1–§3**（负矩 ⇒ function-field 2/2 ratios）；
   - 检查 Conrey–Keating *Pair correlation and twin primes revisited*（Proc. R. Soc. A 472 (2016) 20160548；Lee 的 [2]）——它用 uniform ratios 与 truncated ratios 联系素数对相关，可能是 RAT(c) 证明的现成结构；
   - 检查 Baluyot–Čech 2025（arXiv:2501.12529）的 multiple Dirichlet series 启发式，是否可给出 Dirichlet 族移位区域 2/2 的预测/证明框架；
   - 继续监控 Cech/Gao–Zhao 后续（2026 无新文）与 GWX 引用（OpenAlex=0）。

---

## 6. 引用清单（URL/arXiv；访问日期 2026-11-22）

1. S. Lee, *The Hardy–Littlewood asymptotic for prime pairs of fixed even difference from a uniform zeta-ratios conjecture*, arXiv:2610.32672v2（2026-10-23/2026-11-03）。https://arxiv.org/abs/2610.32672
2. H. Gou, V. Y. Wang, M. W. Xu, *Landau's problems through ratios of L-functions*, arXiv:2611.18825v1（2026-11-13）。https://arxiv.org/abs/2611.18825 ；Hexagon: hexagon:2611.00423v1。https://hexagonmath.org/2611.00423v1
3. J. B. Conrey, N. C. Snaith, *Applications of the L-functions ratios conjectures*, Proc. LMS 94 (2007) 594–646；arXiv:math/0509480。
4. J. B. Conrey, D. W. Farmer, M. R. Zirnbauer, *Autocorrelation of ratios of L-functions*, Commun. Number Theory Phys. 2 (2008) 593–636；arXiv:0711.0718。
5. V. Y. Wang, M. W. Xu, *Harper's beyond square-root conjecture*, IMRN 2025 no. 18, rnaf279；arXiv:2405.04094v2。
6. Li–Liu 条件性证明（2026-11-13）：https://mrc.sdu.edu.cn/english/info/1018/1514.htm ；(1+1.9)：arXiv:2606.05224v2。
7. H. Li, Z. Liu, *Fourth moments of prime exponential sums and exceptional sets for sums and differences of primes*, arXiv:2610.26756（2026-10-19）。
8. H. L. Montgomery, R. C. Vaughan, *The exceptional set in Goldbach's problem*, Acta Arith. 27 (1975) 353–370；Zbl 0301.10043；DOI 10.4064/aa-27-1-353-370。
9. G. H. Hardy, J. E. Littlewood, *Some problems of 'Partitio Numerorum', V*, Proc. LMS (2) 22 (1924) 46–56；*III*, Acta Math. 44 (1923) 1–70。
10. D. A. Goldston, *On Hardy and Littlewood's contribution to the Goldbach conjecture*, Amalfi Conf. Proc. (1989), 115–155, Univ. Salerno, 1992。
11. G. Bhowmik, L. Grimmelt, *The exceptional set of the Goldbach problem*, arXiv:2607.27282（2026-07）§5（MV1975 精确陈述）。
12. J. Pintz, *A new explicit formula … II. The exceptional set in Goldbach's problem*, arXiv:1804.09084v2（2018）§1（MV1975、HL1924、Goldston 精确陈述）。
13. N. Kandhil, A. Languasco, P. Moree, arXiv:2411.19762（2024-11；Math. Ann. 2026）；arXiv:2607.14515（2026-07-16）。
14. M. Čech, *The Ratios conjecture for real Dirichlet characters and multiple Dirichlet series*, arXiv:2110.04409v3；Trans. AMS 377 (2024) 9113。
15. P. Gao, L. Zhao：arXiv:2210.08840, 2304.14600, 2311.08626, 2402.17198, 2404.05081（2022–2024）。
16. H. M. Bui, A. Florea, J. P. Keating, *The Ratios Conjecture and upper bounds for negative moments of L-functions over function fields*, arXiv:2109.10396；Trans. AMS 376 (2023) 4453–4510。
17. A. Florea, *Negative moments of L-functions with small shifts over function fields*, arXiv:2111.10477（2021）。
18. W. Sawin, *Square-root cancellation for sums of factorization functions over squarefree progressions in F_q[t]*, Acta Math. 233 (2024) 285–418；arXiv:2102.09730。
19. S. Baluyot, M. Čech, *Multiple Dirichlet series predictions for moments of L-functions: unitary, symplectic and orthogonal examples*, arXiv:2501.12529（2025-01-21）。
20. S. Baluyot, J. B. Conrey, A. Irfan, N. C. Snaith, *Almost primes in short intervals and averages of long Dirichlet polynomial approximations to (ζ'/ζ)^k*, arXiv:2611.05000（2026-11-03）。
21. B. Conrey, J. P. Keating, *Pair correlation and twin primes revisited*, Proc. R. Soc. A 472 (2016) 20160548（Lee 的 [2]）。
22. I. Pylaiev, *Random Chowla and Goldbach Conjectures*, arXiv:2611.14579（2026-11-10）。
23. M. Rubinstein, *Alpöge/Claude proof of the Generalized Riemann Hypothesis*（专页 + 164 页人类可读草稿，2026-11-21）。https://www.math.uwaterloo.ca/~mrubinst/alpoge_claude_grh/
24. 本团队报告：phase12/0-plan.md；phase11/lit/ratios-2026-survey.md；phase8/lit/ratios-status.md；phase7/lit/alternative-routes.md。

---

## 附录 A：关键原文

1. **Lee Hypothesis 2.1**：见 §1.2 全文（含 (2.3)/(2.4) 与 “The main terms are those in [3, (2.8), (2.10)], restricted to (2.4).”）。
2. **Lee Theorem 1.1/1.2/Cor 1.3**：见 §1.3。
3. **Lee 与 Goldbach 无关**：全文无 “Goldbach” 字样（`grep -i goldbach lee_v2.txt` 无匹配）；Theorem 1.1 只对固定 h。
4. **MV1975（survey arXiv:2607.27282 §5）**：
   > “Montgomery and Vaughan were the first to prove a genuine power saving for its size, in 1975. **Theorem 5.1 (Montgomery–Vaughan). There exists a δ>0 such that |E(X)| ≪ X^{1−δ}.**”
   Pintz 2018 §1：
   > “Montgomery and Vaughan [16] showed that the estimate E(X) ≪_δ X^{1−δ} holds with an unspecified but explicitly calculable value δ>0.”
5. **GRH 条件例外集（Hardy–Littlewood 1924；Pintz 2018 §1）**：
   > “They showed under the Generalized Riemann Hypothesis (GRH) the estimate E(X) = {n≤X; n∈E} ≪_ε X^{1/2+ε} for any ε>0. This result is apart from the substitution of X^ε by log^c X by Goldston [6] even today the best conditional result on GRH.”
6. **Li–Liu 2610.26756 摘要**：
   > “If every nontrivial zero of every primitive Dirichlet L-function has real part at most a fixed 1/2≤Θ<11/12, then E_+(N)≪_Θ N^{1/2}(log N)^{100} and E_−(N)≪_Θ N^{1/2}(log N)^{100}.”
7. **BFK arXiv:2109.10396 摘要**：
   > “We prove special cases of the Ratios Conjecture for the family of quadratic Dirichlet L-functions over function fields. More specifically, we study the average of L(1/2+α,χ_D)/L(1/2+β,χ_D), when D varies over monic, square-free polynomials of degree 2g+1 over F_q[x], as g→∞, and we obtain an asymptotic formula when Re β≫g^{−1/2+ε}. We also study averages of products of 2 over 2 and 3 over 3 L-functions, and obtain asymptotic formulas when the shifts in the denominator have real part bigger than g^{−1/4+ε} and g^{−1/6+ε} respectively. The main ingredient in the proof is obtaining upper bounds for negative moments of L-functions. … As an application, we recover the asymptotic formula for the one-level density of zeros in the family with the support of the Fourier transform in (−2,2).”
8. **GWX Hyp 1.1 / Thm 1.1**：见 phase-8 报告 §1.1/§1.2（原文已逐字核对）。

---

## 附录 B：核查方式与局限

- **逐字核对**：Lee v2 PDF 全文（16 页，Hypothesis 2.1、Theorem 1.1/1.2、Corollary 1.3、§2 说明、参考文献）；`phase5/lit/exc_survey.txt`（Bhowmik–Grimmelt 2026 survey）§1/§5（MV1975、HL1924、Goldston）；Pintz 2018 clean text §1；zbMATH API（MV1975 书目/Zbl/DOI）；OpenAlex API（GWX 引用数=0）；arXiv API（GWX/Lee/BFK/Li–Liu 2610.26756/最新 Goldbach 提交）。
- **仅摘要级核对**：Čech、Gao–Zhao 各篇、Baluyot–Čech 2025、Baluyot–Conrey–Irfan–Snaith 2026、Florea 2021、Pylaiev 2026、Rubinstein 164 页草稿（仅页面/摘要；PDF 下载不完整（缺 EOF）、fitz 读取 0 页，故未逐页断言）。
- **未核验/不可依赖**：任何声称“无条件证明 Goldbach”的 arXiv/Zenodo 预印本（如 arXiv:2611.09007 已被 phase-7 标注为不可依赖）；本报告只把它们列作背景。
- **局限**：WSL 下部分站点（EuDML/DOI 解析）403/302 不可达；OpenAlex 有免费额度限制；Semantic Scholar 限流；arXiv API 偶发限流。时间盒 75 分钟，本报告为文献状态调研，不重新证明任何结论。
