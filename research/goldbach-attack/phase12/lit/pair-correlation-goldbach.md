# Phase-12 追加文献：pair correlation ⇒ Goldbach？与「显式公式直接计算 Goldbach 计数」的已知结果

> 作者：goldbach-researcher（phase-12 追加小任务）。日期：2026-11-22 19:51–21:30（Asia/Shanghai）。URL/DOI 访问日期 2026-11-22。
> 任务：查证「pair correlation ⇒ Goldbach」可能被忽视的条件路线，以及「显式公式 + 零点」直接给 Goldbach 计数的已知结果。
> 标注：**[事实]** 已证/已发表；**[预印本]**；**[推导]**；**[推测]**；**[检索结果]** 未找到。仅文献调研，不重新证明。

---

## 0. 结论先行

1. **Montgomery 的 F(α,T) 在 |α|≤1 的渐近公式是无条件的（2023 年结果）**：Baluyot–Goldston–Suriajaya–Turnage-Butterbaugh, arXiv:2306.04799（2023），**Theorem 1**（不假设 RH）：
   `F(α) = T^{−2α}(log T + O(1)) + α + O(1/√log T)`，uniformly for `0≤α≤1`；
   且 F 实、偶、非负（偶性 ⇒ |α|≤1 全部）。原始 Montgomery 1973 定理在 RH 下证明、Goldston–Montgomery 1987 Lemma 8 改进；**|α|>1 的 “F(α)~1” 是 Montgomery 的强 pair correlation 猜想**（Carneiro–Milinovich–Ramos, arXiv:2310.01913 §1.1）。
2. **存在「pair correlation 型假设 ⇒ Goldbach 例外集」的已知定理，但只到例外集，不到全 N**：**A. Languasco, A. Perelli, “A pair correlation hypothesis and the exceptional set in Goldbach's problem”, Mathematika 43 (1996) 349–361**（DOI 10.1112/S0025579300011827；Zbl 0884.11042）。在 **GRH + 对 Dirichlet L 零点的广义 pair correlation 假设 GMC(ϑ)**（0<ϑ≤1/2，q≤X^θ，q-一致）下证明
   `#{n≤X : n 偶数且 n≠p1+p2} ≪_ε X^{1−2ϑ+ε}`（全区间），
   短区间版：`E(X, X^{2θ}) ≪_ε X^ε`。**取最强 ϑ=1/2 只得到 E(X)≪X^ε——仍可能有无限多（稀疏）例外；它不是“所有充分大偶数”的定理。**
3. **已知的 pair correlation ↔ 素数结果都是“差”（prime differences）而非“和”（Goldbach）**：Goldston–Montgomery 1987 证明 pair correlation 猜想 ⇔ 短区间素数计数的方差公式；Montgomery–Soundararajan 2000 证明该方差公式（在若干假设下）可由 Hardy–Littlewood prime-pair 猜想推出；Conrey–Snaith 从 uniform Ratios Conjecture **严格推出**精确 pair correlation。反方向（pair correlation ⇒ Ratios / ⇒ Goldbach）**没有已知定理**。
4. **Conrey–Keating 2016（arXiv:1604.06124）不是“pair correlation ⇒ twin primes”定理**：其 Theorem 2 证明 **uniform 2/2 ratios 猜想**与**一个算术相关系数猜想**（Conjecture 1）推出**同一个**关于截断 ratios 平均的公式；标题里的 “twin primes” 指算术函数的二点相关（twin-prime-like 的 m 与 m+h 相关），不是孪生素数定理。文中明确说某个相关公式“would be as difficult as proving the Twin Prime conjecture”。
5. **「显式公式 + 零点」直接计算 Goldbach 计数**已有完整系列，但全部是**对 n 求平均**（或短区间平均），不是逐 n：Fujii 1991（RH 下）`G(N)=N²/2−2Σ_ρ N^{ρ+1}/(ρ(ρ+1))+O(N^{4/3}(logN)^{4/3})`（G(N)=Σ_{n≤N}ψ₂(n)）；Bhowmik–Schlage-Puchta 2010 改进到 `O(N log⁵N)` 并证明 `Ω(N log log N)` 最佳；Languasco–Zaccagnini 2012 到 `O(N log³N)`；Billington–Cheng–Schettler–Suriajaya 2023 给**无条件** Fujii 公式且误差 ↔ ζ 的无零区/PNT 余项；Mossinghoff–Trudgian 2022 研究零点振荡项 |G(x)|<0.023059 等。**这些结果离“所有大偶数”差一个层次：平均结果只能排除稀疏例外，无法逐 n 断言。**
6. **对 phase-12 的可用性裁决**：**pair correlation 不是 Ratios 2/2 的替代品，也不是隐藏的“更弱但足够”的路线。** 已知最强（Languasco–Perelli）在 GRH+GMC(1/2) 下只给 E(X)≪X^ε；要推出 **所有** 充分大偶数，pair correlation 型输入差一个本质机制（例外无法清零；phase-6 已证密度-1 不足以推出 Goldbach）。而 **Ratios 2/2 严格强于 pair correlation**（Conrey–Snaith 方向已证），且 GWX 的 Ratios 路线是已知唯一给全 N 的条件路线之一。**因此 phase-12 继续攻 RAT(c>2) 是正确的；pair-correlation 路线的可用性仅为：给出一个“更弱输入能达到什么”的基准（X^{1−2ϑ+ε}，ϑ=1/2 时 X^ε），以及作为 GWX 误差项的独立检验/直觉来源。**

---

## 1. Montgomery 的 pair correlation：定义、无条件范围与强猜想

### 1.1 精确定义（标准归一化）

Montgomery（1973）定义（见 Baluyot–Goldston–Suriajaya–Turnage-Butterbaugh, arXiv:2306.04799 (1.2)–(1.3) 与 Carneiro–Milinovich–Ramos, arXiv:2310.01913 §1.1）：
`F(α) := (T/(2π) log T)^{−1} Σ_{0<γ,γ'≤T} T^{iα(γ−γ')} w(γ−γ')`，`w(u)=4/(4+u²)`；
等价地 `F(α,T) = N(T)^{−1} Σ T^{iα(γ−γ')}w(γ−γ')`，`N(T)=T log T/(2π)`。
Montgomery 证明（**在其原始论文中假设 RH**）：`F(α,T) = (T^{−2|α|} log T + |α|)(1 + O(√(log log T / log T)))`，uniformly `0≤|α|≤1`；由 Goldston–Montgomery [GM87, Lemma 8] 改进误差；Carneiro–Milinovich–Ramos 原文：“Assuming RH, it is known that … uniformly for 0≤|α|≤1. This was proved by Goldston and Montgomery [17, Lemma 8], refining the original work of Montgomery [19].”

### 1.2 无条件范围（关键更正/更新）

**Baluyot–Goldston–Suriajaya–Turnage-Butterbaugh, arXiv:2306.04799（2023），Theorem 1（原文）**：
> “The function F(α) is real, even, and nonnegative. Moreover, as T→∞, we have
> `F(α) = T^{−2α}(log T + O(1)) + α + O(1/√log T)` (1.4)
> **uniformly for 0≤α≤1**.”

并且原文明确：“Theorem 1 is nearly identical to Montgomery's theorem in [Mon73] and [GM87, Lemma 8] **except it does not assume RH**, and it includes the improvements from [GM87, Lemma 8] where (1.4) holds up to α=1 with explicit error terms. The proof is also nearly identical.” 由 F 的偶性，**无条件范围 = |α|≤1**。

**|α|>1 的情形是猜想**（Carneiro–Milinovich–Ramos §1.1 原文）：
> “Montgomery conjectured that F(α,T) ~ 1 for |α|>1, uniformly for α in bounded intervals. This is sometimes called Montgomery's **strong pair correlation conjecture**.”

**注意**：Montgomery 的原始 pair correlation conjecture（零点差分布的渐近，B-G-S-T (1.1)）本身是**猜想**；但 F(α) 在 |α|≤1 的渐近公式（1.4）现在是**无条件定理**（B-G-S-T 2023）。任务问的“|α|≤1 还是需要 RH”——**答案是：|α|≤1 的 F(α) 渐近已可无条件证明；RH 是历史/原始论文的假设，不是今天必需的；|α|>1 才是猜想。**

### 1.3 pair correlation 与素数：已知的联系是“差”，不是“和”

- **[事实]** Goldston–Montgomery 1987（Progr. Math. 70, 183–203）：pair correlation 猜想 **⇔ 短区间素数计数 ψ(x+h)−ψ(x) 的方差公式**（Conrey–Keating 2016 原文：“Goldston and Montgomery [GM] proved rigorously that the pair correlation conjecture is equivalent to an asymptotic formula for the variance of the number of primes in short intervals”）。
- **[事实]** Montgomery–Soundararajan, *Beyond pair correlation*（arXiv:math/0003234, 2000）：该方差公式（在若干假设下）**由 Hardy–Littlewood prime-pair 猜想推出**；即 **HL prime pairs ⇒ pair correlation**（已知方向）。
- **[事实]** Conrey–Snaith（Proc. LMS 94 (2007) 594–646）从 **uniform Ratios Conjecture** 严格推出精确形式的 pair correlation（Conrey–Keating 2016 原文：“Conrey and Snaith used a uniform version of what is known as the ratios conjecture from which assumption they could rigorously derive this precise form of pair correlation”）。
- **所有这些联系都是关于素数差（prime pairs/短区间），不是关于素数和的 Goldbach。**

### 1.4 Conrey–Keating 2016 到底说了什么？

**B. Conrey, J. P. Keating, *Pair correlation and twin primes revisited*, Proc. R. Soc. A 472 (2016) 20160548；arXiv:1604.06124v2（13 页）**。

- **摘要原文**：“We establish a connection between the conjectural two-over-two ratios formula for the Riemann zeta-function and a conjecture concerning correlations of a certain arithmetic function. Specifically, we prove that **the ratios conjecture and the arithmetic correlations conjecture imply the same result**. This casts a new light on the underpinnings of the ratios conjecture…”
- **Theorem 1（原文）**：“Assuming the Generalized Riemann Hypothesis `C_{α,β,γ,δ}(s) = B_{−β,−α,γ,δ}(s+1)`.”（这是连接 ratios 与系数相关的恒等式。）
- **Theorem 2（原文）**：“Let α,β,γ,δ be complex numbers smaller than 1/4 in absolute value. Then, **assuming either a uniform version of the ratios conjecture or a uniform version of a conjectured formula for correlations of values of I_{α,γ}(n) (Conjecture 1, Section 4)**, we have for some η>0 and some λ>1,
  `M_{α,β,γ,δ}(T;X) = ∫_0^∞ ψ(t/T)·(1/2πi)∫_{ℜs=2} [ B_{α,β,γ,δ}(s+1) + (t/2π)^{−α−β−s}B_{−β,−α,γ,δ}(s+1) ] X^s/s ds dt + O(T^{1−η}).`
- **结论**：CK2016 **没有**给出“pair correlation（全支撑或部分支撑）⇒ twin primes/prime pairs”的条件定理；它证明的是 **ratios 猜想 ⇔ 一个算术相关系数猜想**（在平均意义上“imply the same result”）。文中的 “twin primes” 指形如 `I_{α,γ}(m)I_{β,δ}(m+h)` 的**算术函数二点相关**（twin-prime-like），并且原文明确：把该相关公式“actually prove … would be as difficult as proving the Twin Prime conjecture”（line 345 附近），因此它被形式化为 Conjecture 1 而非定理。
- **[事实]** CK2016 也确认了 Montgomery 用 HL prime-pair 启发式得到零点 pair correlation 的方向（即“HL prime pairs ⇒ pair correlation”的启发式来源），而不是反方向。

---

## 2. 「pair correlation ⇒ Goldbach」的已知定理：只有例外集

### 2.1 核心文献：Languasco–Perelli 1996

**A. Languasco, A. Perelli, *A pair correlation hypothesis and the exceptional set in Goldbach's problem*, Mathematika 43 (1996), no. 2, 349–361。DOI 10.1112/S0025579300011827；Zbl 0884.11042。**

**假设（GMC(ϑ)，广义 Montgomery pair correlation，对 Dirichlet L 零点）**（据 zbMATH 评论与 OpenAlex 摘要）：
> 设 (a,q)=1，ε>0，θ∈(0,1/2]。定义
> `F(X,T;q,a) = Σ_{χ1,χ2 mod q} χ1(a)χ̄2(a) τ(χ̄1)τ(χ2) Σ_{|γ1|,|γ2|≤T} X^{i(γ1−γ2)} w(γ1−γ2)`，`w(u)=4/(4+u²)`，
> 其中 γ_j 遍历 L(s,χ_j) 的非平凡零点的虚部，τ(χ) 为 Gauss 和。GMC(ϑ) 断言：对每个 ε>0，
> `F(X,T;q,a) ≪_ε q² T X^ε`，uniformly for `X^{1−θ}/q ≤ T ≤ X` 与 `q ≤ X^θ`。
> 即：比平凡界改进一个因子 q 的 pair correlation 假设。

**结论（原文摘要/Zbl 评论）**：
- 在 **GRH + GMC(ϑ)** 下：`#{n≤X : n 偶数, n≠p1+p2} ≪_ε X^{1−2ϑ+ε}` for every ε>0。
- 短区间版：`E(X, X^{2θ}) := #{2n∈[X, X+X^{2θ}] : 2n 非两素数之和} ≪_ε X^ε`（即“for θ>ε/2, all even integers in any interval [X, X+X^{2θ}] but O(X^ε) exceptions are sums of two primes”）。
- 证明沿用 Perelli–Pintz（J. London Math. Soc. 47 (1993) 41–49）与 Heath-Brown（Acta Arith. 41 (1982) 85–99）的路线，并修正 Kaczorowski–Perelli–Pintz（Monatsh. Math. 116 (1993) 275–282）中的一个错误。

**关键读数**：
- ϑ=1/2（最强 pair correlation，q≤X^{1/2}）：`E(X) ≪_ε X^ε`。
- ϑ<1/2：`E(X) ≪ X^{1−2ϑ+ε}`（弱于 X^ε）。
- **无论 ϑ 取多大（≤1/2），结论都只是“例外集 ≪ X^{1−2ϑ+ε}”，永远不是“E(X)=0”或“所有充分大偶数”。** 因此**没有**已知的“pair correlation ⇒ binary Goldbach（所有大偶数）”定理；LP 是该方向最强的已知定理，其终点是例外集。

### 2.2 相关/前置工作（同一“短区间 Goldbach + 零点”路线）

| 文献 | 精确结论 | 状态 |
|---|---|---|
| **Perelli–Pintz**, *On the exceptional set for Goldbach's problem in short intervals*, J. London Math. Soc. (2) 47 (1993) 41–49（Zbl 0806.11042） | **无条件**：对 0<ε<2/3、A>0，`N^{1/3+ε}≤H≤N` 时 `Σ_{N≤2n≤N+H}|R(2n)−2nS(2n)|² ≪_{ε,A} H N² (log N)^{−A}`（R 为 ΛΛ 表示数，S 为奇异级数） | [事实] |
| **Kaczorowski–Perelli–Pintz**, *A note on the exceptional set for Goldbach's problem in short intervals*, Monatsh. Math. 116 (1993) 275–282；Corrigendum: Monatsh. Math. 119 (1995) 215–216（Zbl 0792.11040） | **GRH 下**：若 `H/log⁶x → ∞`，则区间 (x, x+H) 中除 `≪ H^{1/2} log³ x` 个例外外，所有偶数都是两素数之和 | [事实]（GRH 条件） |
| **Goldston**, *Linnik's theorem on Goldbach numbers in short intervals*, Glasgow Math. J. 32 (1990) 285–297（Zbl 0719.11065） | Goldbach 数在短区间的 Linnik 型定理 | [事实] |
| **Friedlander–Goldston**, *Some singular series averages and the distribution of Goldbach numbers in short intervals*, Illinois J. Math. 39 (1995) 158–180 | 奇异级数平均与短区间 Goldbach 数分布 | [事实] |
| **Heath-Brown**, *Gaps between primes, and the pair correlation of zeros of the zeta-function*, Acta Arith. 41 (1982) 85–99 | pair correlation（ζ）与素数间隙；**差**的方向，不是 Goldbach | [事实] |
| **Languasco–Perelli 1996** | 见 §2.1：GRH+GMC(ϑ) ⇒ E(X)≪X^{1−2ϑ+ε}；短区间 E(X,X^{2θ})≪X^ε | [事实] |

### 2.3 「pair correlation ⇒ 全 N Goldbach」的公认状态

- **[检索结果]** arXiv 中 **没有**摘要同时含 “pair correlation” 与 “Goldbach” 的论文（`abs:"pair correlation" AND abs:"Goldbach"` 返回 0）；没有 “pair correlation ⇒ 所有充分大偶数”的定理。
- **[检索结果]** MathOverflow API 查询 “pair correlation Goldbach” 无结果；web 检索提到该方向时指向的正是 Languasco–Perelli 1996（例外集）与 Korevaar 2008（见下），没有全 N 定理。
- **[事实]** Korevaar, *Prime pairs and Zeta's zeros*, arXiv:0806.0934（2008）：把 Hardy–Littlewood prime-pair 猜想等价于 ζ 零点某些函数的边界行为；摘要称 “A speculative extension of Montgomery's classical work (1973) would imply that there must be an abundance of prime pairs”——**明确标为 speculative**，且仍是 prime pairs（差）不是 Goldbach（和）。
- **[事实]** 从零点 pair correlation 得到的是短区间素数计数的方差/素数差信息；Goldbach 是固定和 `p+q=N`，其主项需要模 N 的所有 Dirichlet 特征（混合 character aspect），ζ 的零点 pair correlation 不含 mod N 信息。**[推导]** 这是“差 vs 和”的结构性区别，而不是技术细节。

---

## 3. 假设强弱的比较：GRH + GMC(ϑ) vs GWX Ratios 2/2 vs phase-12 RAT(c>2)

### 3.1 已知蕴含方向

```
uniform Ratios Conjecture (2/2)  ──[Conrey–Snaith 2007, 严格推导]──▶  precise pair correlation
Hardy–Littlewood prime pairs    ──[Montgomery–Soundararajan 2000, 条件下]──▶  variance of primes in short intervals
pair correlation                ──[Goldston–Montgomery 1987]──▶  variance of primes in short intervals
pair correlation / Ratios  ──[??]──▶ binary Goldbach for all large even N：unknown
```

- **Ratios ⇒ pair correlation**：已知方向（Conrey–Snaith）。
- **pair correlation ⇒ Ratios**：**没有已知定理**（反向未知）。
- 因此 pair correlation 型假设**比 Ratios 弱**（至少不强于 Ratios）。
- **然而“更弱”不等于“足够”**：Languasco–Perelli 定理表明，即使是 GRH + 最强 pair correlation（GMC(1/2)），也只能得到 `E(X)≪X^ε`，不能排除全部例外；**从 X^ε 到 0 没有已知机制**（phase-6 已证“密度-1 不足以推出 Goldbach”）。

### 3.2 与 RAT(c>2) 的比较表

| 假设 | 精确形式 | 给出什么 | 能推出全 N Goldbach？ | 与 Ratios 的关系 |
|---|---|---|---|---|
| **GRH + GMC(ϑ)**（Languasco–Perelli 1996） | 对每个 q≤X^θ，Dirichlet L 零点 pair correlation 的 q-一致估计，`F(X,T;q,a)≪q²TX^ε`，`X^{1−θ}/q≤T≤X` | `E(X)≪X^{1−2ϑ+ε}`；短区间 `E(X,X^{2θ})≪X^ε` | **否**（例外集，非零；最强 ϑ=1/2 仍是 X^ε） | 弱于 Ratios（Ratios ⇒ pair correlation；反向未知） |
| **GWX RC_D(ω_D)**（arXiv:2611.18825） | 全 primitive Dirichlet 族 2/2 ratios，复合导子，临界线分子，`q^{1−ω_D+ε}(1+T)^B` | 每个偶数 N：`Σ_{m+n=N}ΛΛ=N𝔖(N)+O(N^{1−ω_D+ε})` | **是**（ω_D>0 任意） | 目标假设；本身未证 |
| **phase-12 RAT(c)**（团队目标） | 移位区域（分子≈1/2+η、分母 1/2+η）2/2 Dirichlet ratios，误差 `q^{1−cη+ε}` | 若 c>2，可接 GWX 的 §3.2–§3.5 **无需插值**，得 Goldbach | 若 RAT(c>2) 成立：**是** | 比 GWX Hyp 1.1 在“移位区域+不需要临界线分子”意义上更弱；与 pair correlation 不可比（Ratios 类） |

**结论 [推导]**：**pair correlation 型假设不是 RAT(c>2) 的替代，也不构成隐藏的“更弱但足够”路线**。已知定理（LP）说明它最多走到 `E(X)≪X^ε`；而全 N 需要 Ratios 型（每个 N 的模 N 特征族）信息。**从“更弱假设”角度，phase-12 的 RAT(c>2) 仍在 Ratios 类内；pair correlation 类被已知定理“封顶”在例外集。**

---

## 4. 「显式公式 + 零点」直接计算 Goldbach 计数：已知结果与到“全 N”的距离

### 4.1 核心公式链

记 `ψ₂(n)=Σ_{m+m'=n}Λ(m)Λ(m')`（von Mangoldt 加权 Goldbach 表示数），`G(N)=Σ_{n≤N}ψ₂(n)`。

- **[事实] Fujii（1991，三篇）**：在 RH 下，
  `G(N) = N²/2 − 2Σ_ρ N^{ρ+1}/(ρ(ρ+1)) + O(N^{4/3}(log N)^{4/3})`，
  其中 ρ 遍历 ζ 的非平凡零点，零点项绝对收敛（Billington–Cheng–Schettler–Suriajaya 2023 引述，arXiv:2306.09102）。
- **[事实] Bhowmik–Schlage-Puchta（arXiv:0806.3295；2010）**：RH 下改进误差到 `O(N log⁵N)`，并证明 `Ω(N log log N)`-项（表明结果本质上最佳；confirms Egami–Matsumoto 猜想）。其方法：用素数在短区间的分布估计接近 0 的指数和。
- **[事实] Languasco–Zaccagnini（arXiv:1011.3198；2012）**：RH 下
  `Σ_{n=1}^N R(n) = N²/2 − 2Σ_ρ N^{ρ+1}/(ρ(ρ+1)) + O(N log³N)`（R(n) 为未加权 Goldbach 表示数）。
- **[事实] Goldston–Yang（arXiv:1601.06902；2016）**：RH 下平均 Goldbach 表示数的渐近公式，改进 BSP、重证 LZ，并给更光滑的平均。
- **[事实] Goldston–Suriajaya（arXiv:2306.04807；2023）**：GRH（模 q 的 Dirichlet L）下给出 q 的倍数上 Goldbach 表示数的**平滑平均**，并说明可去平滑。
- **[事实] Ikeda–Suriajaya（arXiv:2405.04315；2024）**：GRH 下改进 Granville 的 q 倍数平均估计。
- **[事实] Billington–Cheng–Schettler–Suriajaya（arXiv:2306.09102；2023）**：给出 **无条件** Fujii 公式，并证明其误差项与 ζ 的一般无零区**互为决定**；特别地误差可由 PNT 余项表示（连接无零区）。
- **[事实] Mossinghoff–Trudgian（arXiv:1506.11129；J. Théor. Nombres Bordeaux 34 (2022) 295–307）**：RH 下 Fujii 型公式可写为
  `Σ_{n≤x}Σ_{a+b=n}Λ(a)Λ(b) = x²/2 − 4x^{3/2}G(x) + O(x^{1+ε})`，
  `G(x)=Re Σ_{γ>0} x^{iγ}/((1/2+iγ)(3/2+iγ))`；证明 `|G(x)|<0.023059`（所有 x>0），且 `G(x)<−0.022978`、`G(x)>0.021030` 各无限次成立（后者在零点线性无关假设下可改进）。
- **[事实] 短区间平均**：Perelli–Pintz 1993 的均方结果、KPP 1993 的 GRH 短区间例外集、Languasco–Perelli 1996 的 pair correlation 条件短区间/全局例外集（§2）。

### 4.2 为什么这些结果离“所有大偶数”很远

**[推导]**
1. **平均 vs 逐点**：Fujii/BSP/LZ/GS/IS 全部是对 n 求和（或短区间平均）。零点项 `2Σ_ρ N^{ρ+1}/(ρ(ρ+1))` 的大小约 `N^{3/2}`；RH 下主项 `N²/2` 远大于它，故平均意义下“几乎所有 n 都是 Goldbach 数”。但**逐 n** 的主项是 `n𝔖(n)`，误差涉及**模 n 的所有 Dirichlet L 函数**的零点；对 n 求平均时字符正交性把它们消掉，只剩 ζ 的零点。**因此这些平均公式结构上看不到模 n 的算术，天然无法给逐 n 结论。**
2. **例外集不能清零**：即使把平均误差压到 `O(N log³N)`（近最优，BSP 的 Ω-项表明 `N log log N` 是下限），也只能推出“例外集比主项小”，不能推出“无例外”。pair correlation 型输入（LP）能把例外集压到 `X^ε`（ϑ=1/2），但**不能到 0**。
3. **pair correlation 的层次**：pair correlation 控制零点差（从而素数差/短区间方差）；Fujii 公式的逐点版需要 Dirichlet 特征族（Ratios 型输入），不是 ζ 零点差。GWX 的 Ratios 路线正是补上这个 character-aspect 的输入；LL 的 S/R 路线是另一个（ad hoc 谱）补法。
4. **[推测]** 若有人能证明“pair correlation + 某个 character-average 假设”的混合定理，或许能改善例外集指数；但“全 N”仍需 Ratios 级别的每个 N 信息，除非出现全新的机制（如 LL 的谱路线）。

---

## 5. 对 phase-12 的可用性裁决

**裁决：pair correlation 路线不可用于 c>2 目标；它不是被忽视的捷径。**

1. **【事实】没有 `pair correlation ⇒ binary Goldbach（所有充分大偶数）` 的定理。** 已知最强是 Languasco–Perelli 1996：GRH + GMC(ϑ) ⇒ `E(X)≪X^{1−2ϑ+ε}`（ϑ=1/2 时 `X^ε`）；短区间版 `E(X,X^{2θ})≪X^ε`。**这仍然只是 almost-all（稀疏例外无法排除），比 GWX 所需的全 N 结论严格弱。**
2. **【推导】pair correlation 型假设比 Ratios 弱（Ratios ⇒ pair correlation 已证；反向未知），但“更弱”在这里等于“不够”。** LP 的结论已把该路线的能力“封顶”在 `E(X)≪X^ε`：从例外集到 0 没有已知机制（phase-6 的密度-1 反例说明任何密度/例外集型信息都不足以推出 Goldbach）。
3. **【推导】对 phase-12 的 c>2 目标没有直接帮助**：RAT(c>2) 是 Ratios 类（Dirichlet 族、模 q 的 2/2 比值），pair correlation 是 ζ/Dirichlet 零点差类；两者无法互相替代。若想找“比 Ratios 更弱”的输入，pair correlation 是最明显的候选，但已知定理（LP）证明它在**全 N** 意义上不够；**这反而加强了 phase-12 继续攻 RAT(c>2) 的理由**：它是目前已知能通向“所有 N”的最弱一类输入。
4. **【事实】可用的副产品**：
   - LP 1996 提供“更弱输入能达到的极限”基准：即使有 GRH + 最强 pair correlation，最多 `E(X)≪X^ε`；可用于向 Lead/用户解释“为什么 pair correlation 不够、为什么需要 Ratios/character 信息”。
   - Fujii/BSP/LZ/Billington 等的显式公式平均结果可作为 **GWX/RAT(c) 误差项的独立数值/理论检验**（平均 Goldbach 计数必须匹配这些公式的主项+零点项），并可作为 phase-12 audit 的 sanity check；但它们不构成 Goldbach 证明路线。
   - Conrey–Snaith（uniform Ratios ⇒ pair correlation）与 Conrey–Keating 2016（ratios ⇔ 算术系数相关）给出“Ratios 至少蕴含 pair correlation 级别结构”的证据，说明 RAT(c) 若能证，会顺带给出 pair correlation 型结果；反向仍无。
5. **【推测】若 phase-12 要寻找“弱于 Ratios 的替代”**：文献状态是（a）pair correlation 类已被 LP 封顶于例外集；（b）Chowla/Sarnak 类无已知蕴含；（c）唯一另一条全 N 路线是 LL 的 S/R（不同且 ad hoc，phase-6 数值不利）。**因此 phase-12 的 RAT(c>2) 是已知文献范围内最合理的“比完整 Ratios 弱、但可能仍足够”的目标；没有 pair correlation 捷径。**

---

## 6. 引用清单（arXiv/DOI/URL；访问日期 2026-11-22）

1. A. Languasco, A. Perelli, *A pair correlation hypothesis and the exceptional set in Goldbach's problem*, **Mathematika 43 (1996), no. 2, 349–361**；DOI 10.1112/S0025579300011827；Zbl 0884.11042（zbMATH review by D. Wolke，本报告§2.1 精确陈述的来源）。https://doi.org/10.1112/S0025579300011827
2. S. A. C. Baluyot, D. A. Goldston, A. I. Suriajaya, C. L. Turnage-Butterbaugh, *An unconditional Montgomery theorem for pair correlation of zeros of the Riemann zeta function*, arXiv:2306.04799（2023-06-07）。https://arxiv.org/abs/2306.04799
3. E. Carneiro, M. B. Milinovich, A. P. Ramos, *Fourier optimization and Montgomery's pair correlation conjecture*, arXiv:2310.01913v2（2023-10-03；2023-10-05 v2）。https://arxiv.org/abs/2310.01913
4. H. L. Montgomery, *The pair correlation of zeros of the zeta function*, Proc. Sympos. Pure Math. 24 (1973) 181–193。
5. D. A. Goldston, H. L. Montgomery, *Pair correlation of zeros and primes in short intervals*, Progr. Math. 70, Birkhäuser (1987) 183–203。
6. H. L. Montgomery, K. Soundararajan, *Beyond pair correlation*, arXiv:math/0003234（2000）。https://arxiv.org/abs/math/0003234
7. B. Conrey, J. P. Keating, *Pair correlation and twin primes revisited*, Proc. R. Soc. A 472 (2016) 20160548；arXiv:1604.06124v2。https://arxiv.org/abs/1604.06124
8. J. B. Conrey, N. C. Snaith, *Applications of the L-functions ratios conjectures*, Proc. LMS 94 (2007) 594–646；arXiv:math/0509480（uniform Ratios ⇒ pair correlation）。
9. A. Perelli, J. Pintz, *On the exceptional set for Goldbach's problem in short intervals*, J. London Math. Soc. (2) 47 (1993) 41–49；Zbl 0806.11042。
10. J. Kaczorowski, A. Perelli, J. Pintz, *A note on the exceptional set for Goldbach's problem in short intervals*, Monatsh. Math. 116 (1993) 275–282；Corrigendum Monatsh. Math. 119 (1995) 215–216；Zbl 0792.11040。
11. D. A. Goldston, *Linnik's theorem on Goldbach numbers in short intervals*, Glasgow Math. J. 32 (1990) 285–297；Zbl 0719.11065。
12. J. B. Friedlander, D. A. Goldston, *Some singular series averages and the distribution of Goldbach numbers in short intervals*, Illinois J. Math. 39 (1995) 158–180。
13. D. R. Heath-Brown, *Gaps between primes, and the pair correlation of zeros of the zeta-function*, Acta Arith. 41 (1982) 85–99。
14. J. Korevaar, *Prime pairs and Zeta's zeros*, arXiv:0806.0934（2008）。https://arxiv.org/abs/0806.0934
15. G. Bhowmik, J.-C. Schlage-Puchta, *Mean representation number of integers as the sum of primes*, arXiv:0806.3295v3（2010）。https://arxiv.org/abs/0806.3295
16. A. Languasco, A. Zaccagnini, *The number of Goldbach representations of an integer*, arXiv:1011.3198（2010）。https://arxiv.org/abs/1011.3198
17. D. A. Goldston, L. Yang, *The Average Number of Goldbach Representations*, arXiv:1601.06902（2016）。https://arxiv.org/abs/1601.06902
18. D. A. Goldston, A. I. Suriajaya, *On a smoothed average of the number of Goldbach representations*, arXiv:2306.04807（2023）。https://arxiv.org/abs/2306.04807
19. K. Ikeda, A. I. Suriajaya, *The average number of Goldbach representations over multiples of q*, arXiv:2405.04315v4（2024）。https://arxiv.org/abs/2405.04315
20. K. Billington, M. Cheng, J. Schettler, A. I. Suriajaya, *The Average Number of Goldbach Representations and Zero-Free Regions of the Riemann Zeta-Function*, arXiv:2306.09102v2（2023）。https://arxiv.org/abs/2306.09102
21. M. J. Mossinghoff, T. S. Trudgian, *Oscillations in the Goldbach conjecture*, J. Théor. Nombres Bordeaux 34 (2022) 295–307；arXiv:1506.11129。
22. 本团队报告：phase12/0-plan.md；phase12/lit/conditional-routes.md（task-50）；phase11/lit/ratios-2026-survey.md；phase-6 audit（密度-1 不充分）。

---

## 附录 A：关键原文

1. **B-G-S-T 2023 Theorem 1**（无条件 pair correlation 范围）：
   > “The function F(α) is real, even, and nonnegative. Moreover, as T→∞, we have `F(α) = T^{−2α}(log T + O(1)) + α + O(1/√log T)` uniformly for 0≤α≤1.”
   > “Theorem 1 is nearly identical to Montgomery's theorem in [Mon73] and [GM87, Lemma 8] except it does not assume RH…”

2. **Carneiro–Milinovich–Ramos §1.1**：
   > “Assuming RH, it is known that `F(α,T) = (T^{−2|α|} log T + |α|)(1 + O(√(log log T/log T)))` … uniformly for 0≤|α|≤1. This was proved by Goldston and Montgomery [17, Lemma 8], refining the original work of Montgomery [19].”
   > “Montgomery conjectured that F(α,T) ~ 1 for |α|>1, uniformly for α in bounded intervals. This is sometimes called Montgomery's strong pair correlation conjecture.”

3. **Languasco–Perelli 1996（Zbl 0884.11042 评论）**：
   > 定义 GMC(ϑ)（$F(X,T;q,a)\ll_\varepsilon q^2TX^\varepsilon$，uniformly $X^{1−\vartheta}/q\le T\le X$，$q\le X^\vartheta$）；“One of their corollaries is: (GRH) and (GMC(ϑ)) imply `#{n≤X, n≡0 mod 2, n≠p1+p2} ≪_ε X^{1−2ϑ+ε}` for every ε>0.”（全区间版；短区间版见 arXiv/OpenAlex 摘要：`E(X, X^{2θ}) ≪ X^ε`。）

4. **Conrey–Keating 2016 摘要/Theorem 2**：见 §1.4 原文。
5. **Mossinghoff–Trudgian 2022（Zbl review）**：
   > 在 RH 下 `Σ_{n≤x}Σ_{a+b=n}Λ(a)Λ(b) = x²/2 − 4x^{3/2}G(x) + O(x^{1+ε})`，`G(x)=Re Σ_{γ>0} x^{iγ}/((1/2+iγ)(3/2+iγ))`；并证明 `|G(x)|<0.023059`、`G(x)<−0.022978` 与 `G(x)>0.021030` 各无限次成立。
6. **Billington et al. 2023 摘要**：
   > “We prove an unconditional form of Fujii's formula for the average number of Goldbach representations and show that the error in this formula is determined by a general zero-free region of the Riemann zeta-function, and vice versa.”

---

## 附录 B：核查方式与局限

- **逐字/精确核对**：Languasco–Perelli 1996 的 zbMATH 评论全文（Zbl 0884.11042）与 OpenAlex 摘要（DOI 10.1112/S0025579300011827）；B-G-S-T arXiv:2306.04799 的 Theorem 1 与引文原文；Carneiro–Milinovich–Ramos arXiv:2310.01913 §1.1 原文；Conrey–Keating arXiv:1604.06124 摘要与 Theorem 2 原文；Perelli–Pintz 1993、KPP 1993 的 zbMATH 评论；Bhowmik–Schlage-Puchta arXiv:0806.3295 摘要与 Theorem 1.1；Billington et al. arXiv:2306.09102 的 Fujii 公式段；Languasco–Zaccagnini arXiv:1011.3198 摘要；Mossinghoff–Trudgian zbMATH 评论。
- **仅摘要/元数据**：Goldston 1990、Friedlander–Goldston 1995、Heath-Brown 1982、Korevaar 2008、Goldston–Yang 2016、Goldston–Suriajaya 2023、Ikeda–Suriajaya 2024（arXiv 摘要）。
- **局限**：部分期刊页 403（Wiley/Cambridge/KAKEN），故以 zbMATH/OpenAlex/arXiv 元数据为准；MathOverflow API 查询无结果（可能确无相应问题）；arXiv `abs:"pair correlation" AND abs:"Goldbach"` 查询为空。时间盒约 60 分钟，本报告为文献核查，不重新证明任何结果。
