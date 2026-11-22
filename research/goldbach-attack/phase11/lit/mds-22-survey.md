# Phase-11：Multiple Dirichlet Series（MDs）对**一般（非二次）primitive Dirichlet 特征族**的 level-aspect 2/2 —— 文献深查

> 执行：proof-digest（task-40）。日期：2026-11-21；URL 访问日期：2026-11-21。
> 目标：更新/确认 phase-9 裁决（`phase9/theory/ratios22.md`：「现有 MDs 技术不能证明 G-W-X 所需 RC_D(ω_D)，最大障碍是 general primitive Dirichlet 族无 level-aspect 2/2 MDs 及其函数方程（无二次互反/theta）」）。
> 记号：**2/2** = 两个分子 shift + 两个分母 shift 的 ratios 平均 `R_q(a,b;s,t)=Σ*_{χ mod q} L(a,χ)L(b,χ)/(L(s,χ)L(t,χ))`（G-W-X Lemma 3.1 / Hypothesis 1.1）。
> 标签：**[事实]**=论文摘要/正文原话或题录直接读到；**[题录]**=仅确认题录（未读全文）；**[推导]**；**[推测]**；**[检索结果]**=arXiv/Crossref/Google 检索未见。

---

## 0. 裁决（先给结论）

**Phase-9 结论：基本成立，但需要两处实质更新（不改变"不能"的结论）。**

1. **[事实｜重要更新] 2025 年出现了"conductor aspect + 一般（even）primitive Dirichlet 特征族"的 MD *启发式构造***：Baluyot–Čech, arXiv:2501.12529（2025-01-21），"Multiple Dirichlet series predictions for moments of L-functions: unitary, symplectic and orthogonal examples"。其 §2 专门研究 **family of Dirichlet L-functions L(s,χ), χ over all even primitive Dirichlet characters of conductor ≤ Q** 的 twisted shifted moment，并明言 **"Our first family studied in Section 2.2 is not a family of quadratic twists and has not been studied before using multiple Dirichlet series."** 对 k=2，这个对象 `Σ_{q≤Q} Σ♭_{χ mod q} L(s1,χ)L(s2,χ)/(L(z1,χ̄)L(z2,χ̄))`（乘光滑权）**形式上就是 q-平均的 2/2 ratios**。**但**：他们只 (a) 在绝对收敛域算极点/留数，(b) 找"来自单个 L 函数函数方程"的 FEs，(c) **对亚纯延拓本身提出猜想**，再经 Perron 得（猜想的）渐近式。**没有证明**亚纯延拓/函数方程/2/2 公式。
   → 所以 phase-9 应把"现有 MDs 只有实/二次族版本"更新为：**"2025 年已有 conductor-aspect 的一般 even primitive 特征族的 MD *启发式*（Baluyot–Čech），但只到猜想层；缺的正好是亚纯延拓那一步。"**
2. **[事实｜重要更新] 2026 年出现了一般 primitive 特征族上 *level-aspect 二阶矩*的已证结果**（不是 ratios、不是 MD）：Chen–Lin, arXiv:2608.25812（2026-08-26）在 Selberg 特征值猜想下证明了
   `Σ_{q∈Q} Σ♭_{χ mod q} |L(1/2,χ) L(1/2,f⊗χ)|²` 的 power-saving 渐近式，其中 Q 为受限的可分解模数集（`q=q1q2≍Q, q2≍Q^{δ1}, δ1<0.0004`）。这说明"一般 primitive 特征族的 level-aspect 平均"在**矩**的层面已可用调和分析（Kloosterman/大筛/谱方法）推进；但它 **既不是 ratios（无分母 shift），也不是 MD 构造**。
3. **[事实] 函数域上**：已证的 2/2 Ratios 只对**二次 Dirichlet 族**（Bui–Florea–Keating, Trans. AMS 376 (2023) 4453–4510），且 shift range 受限；**一般 primitive 特征族**的 Ratios/MDs 在函数域上由几何框架（trace functions/perverse sheaves，Sawin 2024 + 2024/26 的收敛与函数方程工作）处理，但该几何输入在 ℚ 上没有对应物。
4. **[事实] 没有任何已发表的、对 ALL primitive Dirichlet characters（含复合导子、q 在 conductor 变量中变化）的 2/2 MD 的*证明*（亚纯延拓 + 两个独立函数方程 + 极结构）。** phase-9 的"不可行"裁决维持；变化在于"最接近的状态"比 phase-9 描述的更靠前一步（见上 1–2）。

**一句话**：**没有新的已证构造能改变 phase-9 的最终裁决**；但 Baluyot–Čech 2025 把"一般族的 conductor-aspect MD"从"没有"推进到"有启发式 + 明确的猜想缺口"，并且这个缺口（亚纯延拓）在二次族场景正是由 reciprocity/Poisson 型额外函数方程提供的——即 phase-9 指出的结构性障碍依然精确成立。

---

## 1. 文献表（paper | object | proven | 2/2 一般 χ？ | 备注）

| # | 论文（venue/arXiv） | 对象/family | 已证内容 | 覆盖 2/2 + 一般 χ？ | 备注/关键限制 |
|---|---|---|---|---|---|
| 1 | Conrey–Farmer–Zirnbauer, *Autocorrelation of ratios of L-functions*, CNTP 2 (2008) 593–636, arXiv:0711.0718 | 一般族的 ratios 乘积平均 | **猜想/启发式**（"new heuristic for all main terms in the quotient of products of L-functions averaged over a family"），与随机矩阵比较 | 给出 2/2 的 recipe（主项），**非证明** | G-W-X 的 RC_D 即此 recipe 的 Dirichlet 族 2/2 形式；注意 lead 所说"Conrey–Farmer"实为 **Conrey–Farmer–Zirnbauer（CFZ08）** |
| 2 | Diaconu–Goldfeld–Hoffstein, *Multiple Dirichlet Series and Moments of Zeta and L-Functions*, Compositio Math. 139 (2003) | 多复变 Dirichlet 级数（"sufficiently many functional equations"）；ζ 与 **quadratic L-series** 的矩 | **证明**：在"亚纯延拓/极除子"猜想下 ⇒ 随机矩阵型矩渐近；应用得 **cubes of central values of Dirichlet L-series** 的最佳已知误差项 | **否**（quadratic 族；单变量/矩结构，非 level-aspect 2/2 一般族） | 这是 MD-moments 的开山之作；其"猜想"部分仍未证；[事实] 摘要明确 quadratic |
| 3 | Katsurada–Matsumoto, *Asymptotic expansions of the mean values of Dirichlet L-functions*, Math. Z. 208 (1991) 23–39（+ II/III，Manuscripta Math. 83 (1994) 425–442） | Dirichlet L 的 **mean values（矩）** 的渐近展开；conductor/modulus aspect | **[题录]** 论文系列已发表；提供 mean-value 渐近展开（moments） | **否**：是矩（mean value）而非 ratios；无 4-shift、无 MD 函数方程构造 | lead 所指"Dirichlet series of Dirichlet L-functions"实为 **"mean values of Dirichlet L-functions"**（题录确认）；内容范围我未读全文，标 [题录/推测] |
| 4 | Bucur–Diaconu, *Moments of Quadratic Dirichlet L-Functions over Rational Function Fields* (2010) | 函数域 F_q(t) 上 **quadratic Dirichlet L** 的矩 | **[题录]** 已发表 | **否**（quadratic + function field） | lead 所指"Bucur–Diaconu"即此文（Crossref 确认） |
| 5 | Chinta–Gunnells, *Constructing Weyl group multiple Dirichlet series*, JAMS 23 (2010), arXiv:0803.0691 | 一般约化根系 Φ 的 Weyl group MDs（r 个复变量；亚纯延拓到 ℂ^r + Weyl 群函数方程） | **证明**：统一构造并证明"expected properties"（对一般约化根系） | **否**：是 root-system/Weil 群 MDs；系数来自局部 Gauss 和/metaplectic 数据（通常需 n-th order reciprocity；已落地情形为二次/函数域等），**不是 conductor-变量上的 ALL primitive Dirichlet 特征族** | 属于"构造技术"，不能直接实例化为 G-W-X 的族 |
| 6 | Whitehead, *Multiple Dirichlet Series for Affine Weyl Groups*（Columbia PhD thesis 2014；arXiv:1408.0937 = *Affine Weyl Group Multiple Dirichlet Series: Type Ã*, Compositio Math. 152 (2016) 2503–2523） | 单连 affine Kac–Moody Weyl 群（除 even rank type A）的 MD；**在有理函数域 F_q(t) 上构造**，四条来自 hyperelliptic curves 参数空间几何的公理；证明唯一性与亚纯延拓 | **证明**（函数域） | **否**：quadratic/metaplectic（应用为 quadratic L 的四阶矩 via affine D4、加权二阶矩 via affine A3）；作者明言 "The construction is limited to the rational function field" | [事实] 摘要原文；这正说明"一般族"缺的是几何/互反输入 |
| 7 | Diaconu–Whitehead, *On the third moment of L(1/2,χ_d) II: the number field case*, arXiv:1804.00690 (2018) | quadratic Dirichlet L 的三阶矩（数域） | **证明**：smoothed asymptotic，含 size x^{3/4} 的 secondary term，误差 O(x^{2/3+δ}) | **否**（quadratic 族） | MDs 在二次族上的"低阶项"能力示例 |
| 8 | Čech, *The ratios conjecture for real Dirichlet characters and multiple Dirichlet series*, Trans. AMS 377 (2024) 9113, arXiv:2110.04409 | **real（二次）Dirichlet 特征族**的 ratios | **证明（GRH 条件下）**：**单 shift**（分子/分母各一）ratios，某些 shift range；扩展非本原可改进 range | **否**（real 族、单 shift、受限 range、GRH） | phase-9 已收录；关键：其函数方程来自二次互反/theta |
| 9 | Gao–Zhao 系列（如 arXiv:2404.05081 二次 Hecke L、arXiv:2402.17198 四次 L 的 prime moduli ratios；另有 2210.08840, 2304.14600, 2311.08626） | quadratic/cubic/quartic Hecke 族、prime-related moduli 的 ratios | **证明（GRH 条件）**：**单 shift**、某些 range | **否**：非二次但"特殊代数族"（CM/Hecke），非一般 χ mod q；单 shift | 说明"非二次"在文献中=特殊可互反族，不是 ALL primitive |
| 10 | Blomer–Fouvry–Kowalski–Michel–Milićević, *The second moment of twisted modular L-functions*, GAFA 25 (2015) 453–516, arXiv:1404.7845 | 固定 cusp forms f,g **twisted by all primitive characters mod q** 的（纯/混合）二阶中心矩 | **证明**：power-saving 渐近，**对所有足够 factorable 的 q（包括 99.9% 的 admissible moduli）**；工具：shifted convolution 谱分析 + Kloosterman 和 power-saving | **否**（是二阶矩，不是 ratios/MD；且 q 需 factorable） | 关键先例：**一般 primitive 特征族的 level-aspect 二阶矩是可行的**（通过调和分析，不是 MD） |
| 11 | Chen–Lin, *The second moment of twisted modular L-functions and Dirichlet L-functions at the central point*, arXiv:2608.25812 (2026-08-26) | Σ♭_{χ mod q} \|L(1/2,χ)L(1/2,f⊗χ)\|²，q 在受限可分解集合 Q 上 | **证明**（在 **Selberg 特征值猜想**下）：power-saving 渐近；Q: q=q1q2≍Q, q2≍Q^{δ1}, δ1<0.0004 | **否**（二阶矩/乘积的绝对值平方；非 ratios；受限模数；条件） | 2026 最新：一般 primitive 字符 level-aspect 的"矩"技术边界 |
| 12 | **Baluyot–Čech, arXiv:2501.12529 (2025-01-21)** | §2: **all even primitive Dirichlet characters of conductor ≤ Q** 的 twisted shifted moments（含 k=2 ⇒ **q-平均 2/2 ratio 形状**）；§3–5: quadratic Dirichlet/twists | **启发式/猜想**：在绝对收敛域算极点留数；找"来自单个 L 函数 FE"的新极点；**猜想**亚纯延拓/极结构 ⇒ Perron ⇒ 猜想渐近式（1–3 族与 CFKRS recipe 一致） | **部分（关键）**：k=2 的对象是 q-平均的 2/2；但 **(a) 仅启发式/未证；(b) shift 范围要求 \|s_j−1/2\| ≪ 1/log Q（随 Q 收缩），G-W-X 需要固定 η 的 shift**；(c) q-平均（光滑权）≠ G-W-X 的逐 q 一致 | **最重要新发现**；明言 family (1) "has not been studied before using multiple Dirichlet series"；解决 continuation 是最大难点 |
| 13 | Saha, *Multiple Dirichlet series associated to additive and Dirichlet characters*, arXiv:1705.05341 (2017) | 与 additive / Dirichlet characters 相关的 MDs | **证明**：additive-character MDs 的亚纯延拓（translation formulas）与奇点集；Dirichlet-character MDs 通过其与 additive MDs 的联系研究 | **否**（不同对象；不是 conductor-aspect ratios 族） | **关键证据**：摘要原话 "while it seems difficult to obtain such a translation formula for the multiple Dirichlet series associated to Dirichlet characters" —— 直接印证一般 Dirichlet 特征的结构困难 |
| 14 | Sawin, *Square-root cancellation for sums of factorization functions over squarefree progressions in F_q[t]*, Acta Math. 233 (2024) 285–418, arXiv:2102.09730 | 函数域 F_q[t] 中 squarefree progressions 上 Möbius/von Mangoldt/divisor 函数的 level of distribution | **证明**：level → 1 (q→∞)，power saving → square-root cancellation；应用于 L-函数矩与 1-level density | **否**（不是 Ratios/MD；是"几何输入"） | G-W-X 函数域部分用其 [Saw24] Prop 8.16 (level θ=5/6) |
| 15 | Sawin 的 axiomatic MDs over F_q(T)（被 2024 工作引用；见 #16） | F_q(T) 上一般 MDs 的公理化 | **证明存在性**：系数为特定 perverse sheaves 的 trace functions；但作者**未证明收敛**（形式幂级数处理） | **否** | 函数域"一般 MD"框架的起点；ℚ 无 perverse sheaf/trace function 对应物 |
| 16 | *A geometric approach to functional equations for general multiple Dirichlet series over function fields*, arXiv:2405.18152 (v3, 2024/2026) | Sawin 公理化 MDs over F_q(T) | **证明**：这些级数在某区域**收敛**，且解析延拓后的函数**满足函数方程**（几何方法） | **否**（函数域一般 MD 框架；不是 Dirichlet 特征族 ratios 的 ℚ 结果） | 说明"general MD"在函数域可行；ℚ 上缺几何 |
| 17 | Bui–Florea–Keating, *The Ratios Conjecture and upper bounds for negative moments of L-functions over function fields*, Trans. AMS 376 (2023) 4453–4510 | **函数域 quadratic Dirichlet L 族**（D monic squarefree deg 2g+1，g→∞）的 ratios | **证明（特殊情形）**：1/1 当 Re β ≫ g^{−1/2+ε}；**2 over 2** 当分母 shift 实部 ≫ g^{−1/4+ε}；**3 over 3** 当 ≫ g^{−1/6+ε}。关键工具：**负矩上界**（expected almost sharp） | **部分**：**2/2 在函数域已证**，但仅 quadratic 族 + 受限 shift range | **函数域 Ratios 的最直接对照**；phase-9 引 Sawin 作为函数域基石，此处补上"2/2 已证到什么程度" |
| 18 | （G-W-X 引用）Bergström–Diaconu–Petersen–Westerland [BDPW23]、[MPPRW24]、[Wan24] | 函数域几何族的矩/Ratios 进展 | 未在本次逐篇核实（G-W-X 引用列表 [事实]） | 一般非二次族？[未核实] | 见 G-W-X §1 注释 "Recent progress on the Ratios Conjecture for geometric families can be found in [BDPW23, MPPRW24, Wan24]" |
| 19 | （2024–2026 相邻）2607.27131 *On the second moment and non-vanishing of central values of Hecke L-functions of r-th order characters* (2026-07)；2411.13143 *Eisenstein Series on Metaplectic Covers and Multiple Dirichlet Series* (2024-11)；2507.08662 *Functional equations of axiomatic multiple Dirichlet series, Weyl groupoids, and quantum algebra* (2025-07)；2607.11834 *A decomposition of Weyl group MDs for symmetrizable Kac–Moody root systems* (2026-07)；2402.07473 *Moments of real Dirichlet L-functions and multiple Dirichlet series* (2024) | higher-order/metaplectic/axiomatic MDs；real Dirichlet moments | 各自为构造/矩结果（多为条件性或 function field/特殊族） | **否**（均非 conductor-aspect ALL primitive 2/2 ratios 的证明） | arXiv 全量检索（2024–2026, "multiple Dirichlet series"/"ratios conjecture"）主要命中；无一般 primitive 2/2 证明 |

---

## 2. 关键论文的精确内容（带原话/摘要要点）

### 2.1 Baluyot–Čech 2025（arXiv:2501.12529）——最接近"general primitive 的 conductor-aspect MD"

**[事实]** 摘要：*"We devise heuristics using multiple Dirichlet series to predict asymptotic formulas for shifted moments of (1) the family of Dirichlet L-functions of all even primitive characters of conductor ≤ Q …"*。

**[事实]** §2 的对象（记号照原文）：

```text
U_k(Q;S,Z;M,N) = Σ_{q≥1} g(q/Q) Σ♭_{χ (mod q)} χ̄(M) χ(N) L(s_1,χ)…L(s_k,χ) L(z_1,χ̄)…L(z_k,χ̄)
```
其中 S={s_1,…,s_k}, Z={z_1,…,z_k}，"close to 1/2, say s_j − 1/2 ≪ (log Q)^{−1} and z_j − 1/2 ≪ (log Q)^{−1}"；Σ♭ over even primitive χ。

**[事实]** §2.2 方法步骤（原文要点）：在绝对收敛域求极点/留数 → 找"arises from the functional equations of the individual L-functions"的 FEs 及其新极点 → **"We then state a conjecture about the meromorphic continuation and its properties, apply Perron's formula, shift the resulting integral and capture the contribution of the residues to arrive at a (conjectural) asymptotic formula."**

**[事实]** 摘要/引言：*"Our first family studied in Section 2.2 is not a family of quadratic twists and has not been studied before using multiple Dirichlet series."*

**[事实]** 引言关于"额外函数方程"：对二次族，"these multiple Dirichlet series have (at least heuristically) an extra functional equation, which should be thought of as analogous to Poisson summation (the 'harmonic detector' …). **This extra functional equation is not important in this paper, but plays a major role in extending the regions of meromorphic continuation**."

**[推导]** 对 k=2，`U_2` 的形式正是 2/2 ratio 的 q-平均；因此这篇论文**给出了 general (even) primitive 族 conductor-aspect 2/2 MD 的启发式**，并把"亚纯延拓"明确标为猜想。
**[推导] 与 G-W-X 需求的三处 gap**：
- (i) 只是猜想，未证延拓/FE/极结构；
- (ii) shift 范围 `|s−1/2| ≪ 1/log Q` 是**随 Q 收缩**的（标准矩的 regime），而 G-W-X Hypothesis 1.1 要**固定** `0<η<η_0` 的 `Re s = Re t = 1/2+η`（不随 q 收缩）—— 需要把结论解析延拓到固定 shift，B–Č 未给；
- (iii) B–Č 是**q 的光滑平均**（Perron 反演后的 Q-asymptotic），G-W-X 要**逐 q 一致**的 `q^{1−ω_D+ε}(1+T)^B` 误差（去掉光滑权、逐 q 提取是额外难题）。
- 另有 parity：B–Č 只做 **even** 字符（"our restriction to even primitive characters is only for convenience, and the procedures … also apply to the odd characters with minor modifications"），这一点不构成实质障碍。

### 2.2 Chen–Lin 2026（arXiv:2608.25812）——level-aspect 一般 primitive 字符的已证**二阶矩**

**[事实]** 摘要：*"We prove an asymptotic formula with a power-saving error term for the second moment Σ_{q∈Q} Σ♭_{χ mod q} |L(1/2,χ) L(1/2,f⊗χ)|² of the twisted GL(2) L-function and the Dirichlet L-function at the central point under the assumption of Selberg's eigenvalue conjecture. … the sum over χ runs over all primitive even Dirichlet characters modulo q, and Q={q=q1q2≍Q: q1≤Q1, q2≤Q2, Q2≍Q^{δ1}, (q,6)=1, (q1,q2)=1} with 0<δ1<0.0004."*
**[推导]** 意义：在一般 primitive 特征族的 **level aspect** 上，**矩**（非 ratios）已有 2026 年的已证结果；但 (a) 是 absolute-value 二阶矩不是 ratios（无 4 shifts、无分母 L^{-1}），(b) q 限制在狭窄可分解集合（δ1<0.0004），(c) 条件于 Selberg 猜想。**不能**替代 2/2 MD。

### 2.3 函数域上 2/2 Ratios 的已证状态（Bui–Florea–Keating 2023）

**[事实]** 摘要原文要点：*"We prove special cases of the Ratios Conjecture for the family of quadratic Dirichlet L-functions over function fields. More specifically, we study the average of L(1/2+α,χ_D)/L(1/2+β,χ_D), when D varies over monic, square-free polynomials of degree 2g+1 over F_q[x], as g→∞, and we obtain an asymptotic formula when Re β ≫ g^{−1/2+ε}. We also study averages of products of **2 over 2** and **3 over 3** L-functions, and obtain asymptotic formulas when the shifts in the denominator have real part bigger than g^{−1/4+ε} and g^{−1/6+ε} respectively. The main ingredient in the proof is obtaining upper bounds for negative moments of L-functions."*
**[推导]** 关键点：
- 函数域上 **2/2 Ratios 已被证明**，但族是 **quadratic**（symplectic），shift range 受限（Re β ≫ g^{−1/4+ε}，g→∞ 时该条件对固定 η>0 最终满足，但误差/范围随族大小退化——与 G-W-X 需要的一致 power saving/固定 shift 不同层面）；
- **没有** general primitive Dirichlet 家族的函数域 2/2 Ratios 证明（检索未见）；一般族的函数域工具是几何 MDs（Sawin 公理化 + 2405.18152 的收敛/FE），它们不是"ALL primitive χ mod q"的族。
- 这直接印证 phase-9 的判断：**2/2 的可行版本需要特殊族（quadratic）；general 族缺互反/theta 结构。**

### 2.4 一般 Dirichlet 特征 MDs 的"困难"文献证词（Saha 2017）

**[事实]** arXiv:1705.05341 摘要：*"For the multiple Dirichlet series associated to additive characters, the meromorphic continuation is established via obtaining translation formulas … **While it seems difficult to obtain such a translation formula for the multiple Dirichlet series associated to Dirichlet characters**, we rely on their intrinsic connection with the multiple Dirichlet series associated to additive characters…"*
**[推导]** 这是一篇 2017 年论文对"一般 Dirichlet 特征 MDs 的（局部/平移）函数方程难以获得"的直接文字证据；可作为 phase-9 障碍的文献支持（尽管对象类型与 conductor-aspect ratios 不同）。

### 2.5 Weyl-group / affine MDs 的边界（Chinta–Gunnells 2010；Whitehead 2014/2016）

**[事实]** Chinta–Gunnells：对任意约化根系 Φ 构造 Weyl group MDs（r 变量，亚纯延拓到 ℂ^r，满足 Weyl 群函数方程）——**统一构造技术**。
**[事实]** Whitehead：对单连 affine Kac–Moody Weyl 群（除 even rank type A）在 **F_q(t)** 上构造 MDs，证明唯一性与最大区域亚纯延拓；四条公理来自 **hyperelliptic curves 参数空间的几何**；应用为 quadratic L 的四阶矩（affine D4）与除数加权二阶矩（affine A3）；*"The construction is limited to the rational function field, but it also describes the p-part … over an arbitrary global field."*
**[推导]** 这些构造的系数是 metaplectic/Gauss-sum 型数据，需要 n-th order 互反/几何输入；**不能**给出 conductor-变量上 ALL primitive Dirichlet 特征的 MDs。这与 phase-9 的"general primitive 族没有二次互反/theta 结构"一致。

### 2.6 其他文献定位（含 lead 列表的正名）

- **"Conrey–Farmer 'Autocorrelation of ratios'"** = 实际作者 **Conrey–Farmer–Zirnbauer**（CFZ08，arXiv:0711.0718）：**纯 recipe/猜想**，无构造无证明。[事实]
- **"Conrey–Farmer multiple Dirichlet series and moments"**：不存在此标题；MD-moments 的开山文是 **Diaconu–Goldfeld–Hoffstein**（Compositio 2003）。[检索结果/事实]
- **"Katsurada–Matsumoto 'Dirichlet series of Dirichlet L-functions'"** = 实为 **"Asymptotic expansions of the mean values of Dirichlet L-functions"**, Math. Z. 208 (1991) 23–39（I；+II/III 1994）：**mean values（矩）渐近**，非 ratios/MD 构造。[题录]
- **"Bucur–Diaconu"** = "Moments of Quadratic Dirichlet L-Functions over Rational Function Fields"（2010）：**quadratic + function field**。[题录]
- **"Whitehead"** = Columbia 2014 博士论文 + Compositio 2016 type Ã 论文：**affine Weyl group MDs，function field**。[事实]
- **"Blomer–Fouvry–Kowalski–Michel–Milićević twisted moments"** = GAFA 25 (2015) 453–516：一般 primitive 字符的二阶矩（all sufficiently factorable q），**不是 MD**。[事实]

---

## 3. 函数域 Ratios vs ℚ：几何输入与缺什么

**[事实]** 函数域侧：
1. **Sawin, Acta 233 (2024) 285–418（arXiv:2102.09730）**：F_q[t] 中 squarefree progressions 上 Möbius/von Mangoldt/divisor 函数的 **level of distribution → 1（q→∞）** 与 **power saving → square-root cancellation**；应用：L 函数矩、1-level density。[摘要]
2. **Sawin 的 axiomatic MDs over F_q(T)**：MDs 公理化，系数为特定 **perverse sheaves 的 trace functions**；存在性已证，但**未证收敛**。
3. **arXiv:2405.18152（2024/2026）**：证明上述 MDs **在区域收敛**且解析延拓后的函数**满足函数方程**（几何方法）。
4. **Bui–Florea–Keating 2023**：函数域 **quadratic** Dirichlet 族 **2/2** Ratios 已证（受限 shift），工具为**负矩上界**。

**[推导] ℚ 上缺的几何输入（精确化 phase-9 的 "no reciprocity/theta"）**：
- (G1) **trace function / perverse sheaf / Weil II 型精确计数**：函数域的 MDs 与 Ratios 的"额外函数方程"（harmonic detector）由几何（曲线/上同调）提供；ℚ 上对一般 χ mod q 没有对应的上同调/迹公式精确输入。
- (G2) **reciprocity/theta**：quadratic 族有 χ_d↔ℚ(√d)+theta 提供额外函数方程；一般 primitive χ mod q **没有**模 q 参数的二次域/theta 对应（这正是 phase-9 的原句；Baluyot–Čech 2025 的 family (1) 也明言此前没有 MD 研究）。
- (G3) **复合导子**：G-W-X 要 all conductors（含 composite）；函数域几何结果按 squarefree/discriminant 参数化，ℚ 上 composite q 的 χ 无 discriminant/curve 参数化。
- (G4) **去掉光滑权/逐 q 提取**：函数域 Ratios 与 B–Č 均为族平均（smooth weight / sum over q≤Q）；G-W-X 需要逐 q 一致（uniform in conductor, T≤100 log 2q）——需要额外的 unsmoothing/uniformity 技术（函数域亦非直接给出）。

---

## 4. 有没有"conductor 变量上 ALL primitive Dirichlet 特征"的 MD 构造？

- **启发式：有（2025，Baluyot–Čech）** —— 对 **all even primitive characters of conductor ≤ Q** 的 twisted shifted moments，k=2 即 q-平均 2/2 ratio 形状；但 **亚纯延拓/极点结构只是猜想**；shift 范围随 Q 收缩；且是光滑平均而非逐 q。
- **证明：没有** —— **[检索结果]** arXiv 全量（2024–2026 "multiple Dirichlet series"/"ratios conjecture"，以及历史文献）**未发现**任何已发表的、对 ALL primitive Dirichlet characters 的 conductor-aspect 2/2 MD 的亚纯延拓 + 两个独立函数方程 + 极结构的定理。
- **相邻已证（不是 ratios/MD）**：一般 primitive 字符族上的 level-aspect **二阶矩**已有已证结果：BFKMM 2015（twisted modular，all sufficiently factorable q，99.9% moduli）；Chen–Lin 2026（product second moment，受限可分解 q，Selberg 条件）。它们说明"一般字符族的 level aspect 平均"在**矩**层面可行，但方法与 MD/ratios 不同，且不覆盖 4-shift ratio。
- **特殊非二次族（不是 ALL primitive）**：Gao–Zhao 的 cubic/quartic Hecke 族单 shift ratios（GRH、受限）——phase-9 已列。

---

## 5. 障碍清单（编号，供 phase-11 报告引用）

- **O1｜互反/theta 缺失**：一般 primitive χ mod q 没有二次互反/theta 结构，无法给出 MDs 的"额外函数方程"（Poisson/harmonic detector）。文献依据：phase-9；Baluyot–Čech 2025 §1（二次族的 extra FE 用于延拓，而 general family 未研究）；Saha 2017（Dirichlet-character MDs 的 translation formula "seems difficult"）。
- **O2｜亚纯延拓只在猜想层**：对 general family，已知的只有绝对收敛域；Baluyot–Čech 2025 明说"state a conjecture about the meromorphic continuation"——这正是 (AL1) 缺口。
- **O3｜两个独立函数方程**：2/2 需要分别对 a、b 的 FEs（4 shifts）；现有已证结果全是**单 shift**（Čech 2024；Gao–Zhao 2022–24）。Baluyot–Čech 的 FEs 来自单个 L 函数，不足以产生第二项主项所需的完整结构（[推导]）。
- **O4｜shift 范围**：已证结果 range 受限（"some range"）；B–Č 要求 shifts ≪ 1/log Q（收缩），G-W-X 要**固定 η**；2/2 交换项分母也在临界线附近，需一致控制。
- **O5｜逐 q 一致 vs 光滑平均**：G-W-X 要 all q（含 composite）、uniform `q^{1−ω_D+ε}(1+T)^B`；MD/Ratios 方法给出族平均渐近，逐 q/去光滑是额外难题。
- **O6｜函数域几何输入在 ℚ 缺失**：trace functions/perverse sheaves/上同调精确计数；即使函数域，已证 2/2 Ratios 也只 quadratic 族（Bui–Florea–Keating 2023），非 all primitive。
- **O7｜"矩"与"ratios"的鸿沟**：level-aspect 一般字符族的二阶矩可证（BFKMM 2015；Chen–Lin 2026），但 ratios 需要分母 L^{-1}（负矩/零点控制）与 4 shifts 的一致信息；已知负矩上界只在函数域 quadratic 族（BFK 2023）有足够强度。
- **O8｜composite conductors**：G-W-X 明确要含 composite；MDs/geometry 结果通常按 squarefree/discriminant 或 prime-related moduli 参数化（Čech/Gao–Zhao/BFK 均如此）。

---

## 6. Phase-9 裁决的更新措辞（建议 Lead 采用）

> **原 phase-9 裁决**："现有 MDs 技术不能证明 RC_D(ω_D)；最大障碍是 general primitive Dirichlet 族无 level-aspect 2/2 MDs 及其函数方程（无二次互反/theta 结构）。"
>
> **Phase-11 更新版**："**结论不变：目前没有已证构造能证明 RC_D(ω_D)；也仍然没有任何已证的 general primitive Dirichlet 族 level-aspect 2/2 MD（亚纯延拓 + 两个独立 FE + 极结构）。** 需要更新的两点事实：(i) **2025 年 Baluyot–Čech 已构造出 general (even) primitive 族的 conductor-aspect shifted-moment MD *启发式***（k=2 即 q-平均 2/2 ratio 形状；明言此前无 MD 研究），但亚纯延拓只是猜想、shift 需 ≪1/log Q、且是光滑平均而非逐 q 一致——**它把缺口从"没有构造"精确定位到"亚纯延拓 + 固定 shift + 逐 q 一致"**；(ii) **2026 年 Chen–Lin 在 Selberg 条件下证明了 general primitive 字符 level-aspect 的 product 二阶矩**（受限可分解导子集），说明"一般字符族平均"在**矩**层面已有硬技术，但完全不是 ratios/MD 路线。函数域侧已证 2/2 Ratios 仅限 quadratic 族（Bui–Florea–Keating 2023）；一般 MD 框架的函数域版本（Sawin 公理化 + 2405.18152 收敛/FE）依赖 perverse sheaves/trace functions 几何输入，ℚ 上无对应，这正是结构性障碍。**没有任何 NEW proven construction 能改变 phase-9 的'当前技术不可行'裁决。**"

**什么会改变裁决（可检验的里程碑）**：
1. 任何对 ALL primitive Dirichlet characters 的 conductor-aspect MD 的**已证亚纯延拓 + 两个独立函数方程 + 极结构**（哪怕 q 素、shift 小范围）——目前不存在。
2. 把 Baluyot–Čech 2025 的猜想在 q-平均层面**证明**（含 shift 解析延拓到固定 η、去光滑到逐 q）——即使成立，仍需 O5/O8 才能达到 G-W-X。
3. 函数域 2/2 Ratios 从 quadratic 族推广到 general primitive 族（目前 [检索结果] 未见）。
4. 一般字符族的强负矩/零点密度界（足以支撑 2/2 交换项）——目前只有矩（BFKMM；Chen–Lin），无 ratios 级输入。

---

## 7. 来源（URL，访问 2026-11-21）

**Phase-9 基础**：`phase9/theory/ratios22.md`；`phase8/lit/ratios-status.md`；G-W-X 提取文本 `phase7/lit/gwx.txt`（arXiv:2611.18825，2026-11-13）。

**本次逐项核实（arXiv abs / 期刊摘要 / Crossref）**：
- CFZ08：https://arxiv.org/abs/0711.0718（Conrey–Farmer–Zirnbauer, CNTP 2 (2008) 593–636）。
- DGH：https://www.math.columbia.edu/~goldfeld/GoldfeldDiaconuHoffstein.pdf（Compositio Math. 139 (2003)；摘要+§1 已读）。
- Baluyot–Čech：https://arxiv.org/abs/2501.12529（+ HTML 全文 §1–2 已读）。
- Chen–Lin：https://arxiv.org/abs/2608.25812。
- BFKMM：https://arxiv.org/abs/1404.7845（GAFA 25 (2015) 453–516）。
- Diaconu–Whitehead：https://arxiv.org/abs/1804.00690。
- Chinta–Gunnells：https://arxiv.org/abs/0803.0691（JAMS 23 (2010)）。
- Whitehead：https://academiccommons.columbia.edu/doi/10.7916/D8BK19HT（thesis 2014）；https://arxiv.org/abs/1408.0937（Compositio 152 (2016) 2503–2523）。
- Saha：https://arxiv.org/abs/1705.05341。
- Bui–Florea–Keating：https://par.nsf.gov/servlets/purl/10405306（Trans. AMS 376 (2023) 4453–4510；摘要+§1 已读）。
- Sawin：https://arxiv.org/abs/2102.09730（Acta Math. 233 (2024) 285–418）。
- 2405.18152：https://arxiv.org/abs/2405.18152。
- Katsurada–Matsumoto：Crossref DOI 10.1007/BF02571507（Math. Z. 208 (1991) 23–39）；系列 III：DOI 10.1007/BF02567624（Manuscripta Math. 83 (1994) 425–442）——**[题录]**。
- Bucur–Diaconu：Crossref（"Moments of Quadratic Dirichlet L-Functions over Rational Function Fields", 2010）——**[题录]**。
- arXiv 全量检索：`https://export.arxiv.org/api/query`，queries: `all:"multiple Dirichlet series" AND submittedDate:[2024…2026]`（30 条，已列主要）；`all:"ratios conjecture" AND submittedDate:[2024…2026]`；`all:"multiple Dirichlet series" AND all:"Dirichlet characters"`；`ti:"second moment of twisted modular"`；`au:Bucur AND au:Diaconu`（无结果）；`au:Diaconu AND au:Whitehead`。

**局限（诚实标注）**：
- 未读全文的：Katsurada–Matsumoto（仅题录）、Bucur–Diaconu（仅题录）、Gao–Zhao 系列（phase-9 已有摘要级记录，本次未重读）、BDPW23/MPPRW24/Wan24（仅知 G-W-X 引用）、2405.18152 全文（仅摘要）。
- "ALL primitive characters 的 2/2 MD 不存在"是 **[检索结果]**（arXiv 2024–2026 + 已知历史文献），不能 100% 排除未公开/非英文/未索引工作；但结合 Saha 2017、"no extra FE" 与 phase-9 的结构性论证，置信度高。
- 本文的"QD gap"（B–Č 光滑平均 vs G-W-X 逐 q）为 **[推导]**，未在 B–Č 论文中讨论。
