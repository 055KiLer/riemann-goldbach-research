# Phase-9：multiple Dirichlet series 技术能否证明 G-W-X 所需的 2/2 Ratios 平均？

> kernel-theorist，task-33。日期：2026-11-21。
> 目标（G-W-X = Gou–Wang–Xu, arXiv:2611.18825）：RC_D(ω_D)（Hypothesis 1.1）⇒ Goldbach。核心问题：现有 MDs（multiple Dirichlet series）技术能否达到它？
> 标注：**[事实]/[证明]/[推导]/[推测]/[预印本]**。URL 访问日期 2026-11-21。
> 关键源文本：本地 `phase7/lit/gwx.txt`（G-W-X 提取文本）；arXiv abs：G-W-X 2611.18825、Čech 2110.04409、Gao–Zhao 2404.05081、Lee 2610.32672。phase-8 汇总 `phase8/lit/ratios-status.md`。

---

## 0. 裁决与 top-2 第一步引理（先给 Lead）

**可行性裁决：现有 MDs 技术【不能】在可预见时间内证明 RC_D(ω_D)（任意 ω_D>0），即使把范围限制到 q 素、|Im|≤c log q、只要求 q 的 power saving；最大障碍不是"改进范围"，而是 2/2 情形缺少可用的 level-aspect 多重 Dirichlet 级数及其函数方程（general primitive Dirichlet 族没有二次互反/theta 结构），以及两个分子 shift 同时靠近临界线时 reciprocal/交换主项的一致控制。**

**最大障碍（单一）**：**prove the *untwisted* 2/2 ratios formula (G-W-X Lemma 3.1) uniformly in the conductor q with two numerator shifts near the critical line and |Im|≤100 log(2q)** —— 即：需要一个 level-aspect 的"2/2 MDs" `D_{2,2}(z; a,b;s,t)=Σ_q q^{−z}Σ*_{χ mod q} L(a,χ)L(b,χ)/(L(s,χ)L(t,χ))` 的亚纯延拓 + 函数方程 + 在 `Re z≥0` 上的极结构（给出 `φ*(q)Z_q` 与 `H_q Z_q(1−b,1−a;s,t)` 两主项）。现有的 MDs 只有**实/二次特征族**版本（Čech、Gao–Zhao）：其函数方程来自二次互反/theta，**一般 primitive Dirichlet 族没有对应物**。G-W-X §3.1 的 parity twist（用两个 untwisted ratios 平均 `R, R∨` 线性组合出 `Σχ(−1)`）本身是"条件性工程"，只要 Lemma 3.1 在那个一般性下成立即可；其指数系数增长问题他们用 rational Mellin weights + 隔离 `m+n=N` 的权 + 分子 shift 插值解决了。**所以真正缺的是 Lemma 3.1 的证明，不是 parity twist。**

**Top-2 具体第一步引理**（研究纲领）：
```
L1（level-aspect 2/2 MDs 的构造与延拓，最小版本）
   对 q 限制为素数（或 prime-related），构造 D_{2,2}(z;a,b;u,v)（a,b 为分子 shifts，u,v 为分母 shifts 相对 1/2 的位移，
   |Re u|,|Re v|,|Re(a−1/2)|,|Re(b−1/2)| ≤ r₀，|Im|≤c log q），证明其到 Re z ≥ 0 的亚纯延拓，
   唯一可能的极在 z=1 且留数为 (CFZ 主项) Z_q(a,b;s,t) 的 q-平均，并给出垂直方向的多项式增长
   （阶 ≤ polynomial in log q）；由此推出 Lemma 3.1 的 q-平均版本（q 素、|Im|≤c log q、误差 q^{1−ω}，任意小 ω>0）。
L2（reciprocal/交换项的 level-aspect 控制）
   控制 R∨ 的 2/2 交换项：证明对 Re s=Re t=1/2+η、|Im|≤c log q，
   |Σ*_{χ mod q} H_q(a,b)-型因子 × L(1−a,χ)L(1−b,χ)/(L(s,χ)L(t,χ))| 的 q-平均的 power saving；
   等价地：给出一个带两个 shift 的 level-aspect 二阶矩/大筛型引理
   Σ*_{χ mod q} |L(1/2+u,χ)|² |L'/L(1/2+η+iy,χ)|^A ≪ q^{1+ε}(log q)^C，|u|,|y|≤c log q（A=0,1），
   在 GRH 下尽量证明（大筛 + 零点计数；目前只有 A=0、固定 shift 的版本，见 Bui–Keating 型矩结果）。
```
L1 是"构造"缺口（可能只能先做 q 素/二次族）；L2 是"估计"缺口（GRH 下或许可先做 A=0、log q 范围的弱化版）。两者合起来才能拼出 q-素、|Im|≤c log q 的 2/2 ratios。

---

## 1. 已知最接近的结果：方法、精确陈述、单 shift 如何进入

### 1.1 Čech（arXiv:2110.04409v3；Trans. AMS 377 (2024) 9113）[事实/GRH-条件]
- **证明了什么**：对**实 Dirichlet 特征族**，用 **multiple Dirichlet series（MDs）** 证明 ratios 猜想**单 shift**（分子一个 shift、分母一个 shift）在**某些 shift range** 内成立；**所有结果在 GRH 下**。摘要原文："We consider the family of real Dirichlet characters, and use multiple Dirichlet series to prove the ratios conjectures with one shift in the numerator and denominator in some range of the shifts. This range can be improved by extending the family to include non-primitive characters. All of the results are conditional under the Generalized Riemann hypothesis. This extended range is good enough to enable us to compute an asymptotic formula for the sum of shifted logarithmic derivatives for some range of the shift."
- **单 shift 如何进入（方法）**：把 ratios 平均写成对"模/判别式 d 的求和"的 Dirichlet 级数（第二个变量 z）；对实特征 `χ_d`，利用**二次互反 + theta 函数**给出该 MDs 在 `(z, shift)` 上的**函数方程**（Goldfeld–Hoffstein/Diaconu–Goldfeld–Hoffstein 型"double Dirichlet series"）；然后移动 z-围道、取极的留数，极的位置给出 CFZ 主项（对角项 + FE 交换项），围道误差用 GRH 控制（GRH 排除分母 L 在 Re>1/2 的零点，使移动合法；误差由零点计数/边界增长控制）。**"单 shift"的作用**：FE 只作用在一对分子 L 上、交换项只产生**一个** reciprocal 结构；range 限制来自 MDs 的绝对收敛域（shift 的实部必须在 1/2 附近的一个小区间内）。
- **局限**：族是**实特征**（quadratic/判别式族），不是一般 primitive Dirichlet 族；**单 shift**；shift range 受限；q/判别式 aspect 与 G-W-X 的"所有导子 q（含复合）"不同。

### 1.2 Gao–Zhao（2022–2024 系列，例 arXiv:2404.05081v2）[事实/GRH-条件]
- **证明了什么**：用 **multiple Dirichlet series 方法**，对**虚二次域（类数 1）的 quadratic families of Dirichlet/Hecke L-functions、prime-related moduli**，发展 **单 shift**（分子/分母各一个 shift）的 ratios 猜想，在**某些 range**、**GRH 下**；推论：中心值一阶矩、1-level density 的渐近。
- **方法要点**：与 Čech 同源——二次族 + theta/互反 ⇒ MDs 的亚纯延拓与函数方程；prime-related moduli 的选取使得局部 Euler 因子/函数方程显式可控；shift range 限制同上。
- **另**：quadratic twist、cubic/quartic Hecke 族的版本（arXiv:2210.08840, 2304.14600, 2311.08626, 2402.17198）；Cho–Park 2018（三次族 1-level density vs ratios 预测）；Bui–Keating 2006（Dirichlet L 的 2k 阶矩 hybrid Euler–Hadamard，与 ratios/随机矩阵预测**矩层面**一致）；Goes 等 2009（素数导子 Dirichlet 族的 1-level density：Fourier 支撑 (−1,1) 平方根一致、(0,−2,2) power saving 一致——**数值/受限检验函数**，非 2/2 平均本身）。
- **共同技术边界【事实】**：所有 ℚ 上已证 ratios 结果都是 **(a) 特殊族（实/二次/三次/四次 Hecke）；(b) 单 shift；(c) 受限 shift range；(d) GRH 条件**。没有一条覆盖一般 primitive Dirichlet 族的 2/2。

---

## 2. 2/2 情形多出来的东西（精确）

记 `R_q(a,b;s,t)=Σ*_{χ mod q} L(a,χ)L(b,χ)/(L(s,χ)L(t,χ))`（G-W-X 的记号；注意 G-W-X 写 `L(b,χ̄)`，由 `χ̄` 与共轭对称性等价）。

**(D1) shift 积分数量与 CFZ 主项。** 单 shift 的 CFZ recipe 有 **2 个主项**：对角项 `φ*(q)Z_q(...)` + FE 交换项 `H_q(...)Z_q(1−b,1−a;s,t)`。G-W-X Lemma 3.1 已把 2/2 的这两项写出：
```
R_q(a,b;s,t) = φ*(q) Z_q(a,b;s,t) + H_q(a,b) Z_q(1−b,1−a;s,t) + O(q^{1−ω+ε}(1+|Im s|+|Im t|)^B),
H_q(a,b) = Σ_{e=0,1} M_e(q) X_{q,e}(1−b)X_{q,e}(1−a),   X_{q,e}(s)=(q/π)^{1/2−s}Γ((1−s+e)/2)/Γ((s+e)/2),
```
`φ*(q)=M_0(q)+M_1(q)`（奇偶本原特征计数）。**[推导]** 2/2 的 CFZ recipe 本身**已知**（CFZ08 猜想 + G-W-X Lemma 3.1 的形式），所以"主项是否已知"的答案是**是（recipe 已知）**；缺的是**证明**（q 一致、含复合导子、T≤100log2q）。MDs 匹配：要对 `R_q(a,b;s,t)` 构造 `D_{2,2}`（两个 shift 参数 + 两个分母参数 + z），其极结构要给出**两项**主项；这需要 MDs 有**两个独立函数方程**（分别对 a、b），当前单 shift MDs 只有一个。

**(D2) reciprocal 项/对称平方结构。** 交换项 `H_q(a,b)Z_q(1−b,1−a;s,t)` 把 `L(a)L(b)→L(1−a)L(1−b)`。当 `Re a,Re b=1/2`（G-W-X 的要求）时 `Re(1−a),Re(1−b)=1/2`——**交换项的分母也在临界线上**，其绝对收敛性/零点行为比单 shift 情形（交换项可移到 Re>1/2 一侧）更差。当 `Im a=−Im b`（G-W-X 明说"coefficients in this linear combination may grow exponentially when the imaginary parts of the numerator arguments have opposite signs"）时 `H_q` 的比值 `1/(h_1−h_0)` 指数增长——G-W-X 用 rational Mellin weights + 隔离 `m+n=N` 的权 + 插值处理；**这些技巧要求 ratios 公式在分子 shift 的二维复邻域（|u|,|v|≤r）内一致成立**（Hadamard 三圆/Phragmén–Lindelöf），而 MDs 通常只能给固定 shift 或小 range——这是 2/2 MDs 的额外要求。
**(D3) symmetric-square/矩结构。** 2/2 平均含 `L(a)L(b)`，`|Im a|,|Im b|` 独立 ⇒ 这是家族的**两 shift 相关**（shifted moments / level-aspect pair correlation），其"对角"情形 `a=b` 才退化为二阶矩（Bui–Keating 可及）；单 shift ratios 只对应一阶矩/对数导数平均。MDs 处理"平均"（矩），处理"两个 independent shifts 的相关"需要 level-aspect 的 pair-correlation 型输入。**[推导/推测]**
**(D4) 收敛域与均匀性。** 单 shift：MDs 的 shift range 由收敛域限制（Čech/Gao–Zhao 的 "some range"）；2/2：4 个 shift 参数 ⇒ 收敛域更小，且 G-W-X 要求 (i) 所有导子 q（含复合）、(ii) T≤100log(2q)、(iii) 任意小的 ω_D>0 且不依赖 η。**复合导子**使 MDs 的 q-平均无法用二次互反直接写出（一般 χ mod q 不来自二次域），这是结构性的。

---

## 3. 2/2 restricted range 的条件定理/证明草图（逐条列出缺失引理）

**条件定理 3.1（restricted 2/2，q 素）.** 设 GRH 成立，并设以下三个引理成立：
```
(AL1) [level-aspect 2/2 MDs 引理]  D_{2,2}(z;a,b;s,t) := Σ_{q prime} q^{−z} R_q(a,b;s,t)
      在 |Re(a−1/2)|,|Re(b−1/2)|≤r₀、Re s=Re t=1/2+η、|Im|≤c log q 的区域内，
      从 Re z>1 亚纯延拓到 Re z≥0；唯一极 z=1，留数 = φ*(q) 的 q-平均 × Z_q(a,b;s,t)；
      且 |D_{2,2}(z;…)| ≪ q^{σ_z+ε}(log q)^{C} 于 Re z=σ_z≥0（多项式增长，C 只依赖 r₀,η）。
(AL2) [交换项控制引理]  在同上区域内，|H_q(a,b)|·|Z_q(1−b,1−a;s,t)| 的 q-平均满足
      Σ_{q≤Q} |H_q(a,b)||Z_q(1−b,1−a;s,t)| ≪ Q^{1−ω+ε}(log Q)^{C'}（任意小 ω>0）。
(AL3) [shifts 插值引理] 若 R_q 在 |u|,|v|≤r 的二维复邻域一致满足 (D1) 的估计，
      则 R_q 在 Re a=Re b=1/2（临界线）上的相应估计成立（Hadamard 三圆，损失 (log q)^{O(1)}）。
```
则对 q 素、T≤c log(2q)，`R_q(a,b;s,t)=φ*(q)Z_q+H_qZ_q(1−b,1−a;s,t)+O(q^{1−ω+ε}(1+T)^{B'})` 对某个 ω>0 成立（restricted-range RC_D 弱版本）。
**证明草图**：与 Čech 单 shift 相同：对 `D_{2,2}` 的 z-围道移动，极给主项，竖直积分用 (AL1) 的多项式增长 + (AL2) 控制交换项，围道高度取 ~(log q)^D；最后 (AL3) 把 shift 窗口推到临界线。**每个 (ALk) 都是当前技术没有的**：
- (AL1) 的核心是"general primitive Dirichlet 族"的 MDs 函数方程；二次族版本（Čech/Gao–Zhao）靠 theta/互反，一般族**无已知构造**（[推测] 这是最硬的一步；可能要先做"二次特征权 × 一般特征"的混合 MDs）；
- (AL2) 需要 level-aspect 的二阶矩/大筛型估计（见 §0 L2），GRH 下可能用零点计数 + 大筛做到 A=0 的部分（但 `H_q` 的指数增长需要 G-W-X 式 Mellin 权处理）；
- (AL3) 技术上可行（Hadamard 三圆 + L 函数的 Phragmén–Lindelöf），但会损失 log 的幂，需与 (AL1)(AL2) 的 B,C 匹配。

**结论**：restricted 版本的 2/2 也**未被现有文献覆盖**；最乐观的路线是"二次族 + 两个 numerator shifts 的 MDs"（把 Čech 的 MDs 扩展到 2/2 的 quadratic family），而非一般 primitive 族。

---

## 4. 能否达到 G-W-X 的要求？——不能；需要什么新方法

G-W-X 需要：**(a) 所有导子 q（含复合）；(b) T≤100 log(2q) 一致；(c) 任意固定 ω_D>0，且 saving 不随 η→0 退化；(d) Re a=Re b=1/2, Re s=Re t=1/2+η 的完整 2/2 区域。**
- (a) 复合导子：MDs 的 q-平均对复合 q 没有二次互反/theta 结构（现有方法甚至对非本原实特征要靠"extend to include non-primitive"来**改进** range，不是得到复合导子的一般族）。**[事实/推导]**
- (b) T≤100log2q 的均匀性：G-W-X 的 parity twist 需要分子 shift 在 `|u|,|v|≤r` 内的**一致** ratios（用于插值到 a=s+u）；而 MDs 的 power saving 通常对 shift 的虚部是指数/多项式损失的组合，T 的 B 次幂若太大就吃掉 q 的 saving（ε vs ω 的竞争）。**需要 (AL1) 中 T 的损失严格小于 q 的 saving**——这要求非常干净的 MDs 误差，现有文献没有。
- (c) 任意 ω_D>0 且不依赖 η：需要 MDs 在 Q^{1−ω} 量级的误差，且 ω 与 shift 的实部窗口无关；单 shift 文献只给"某些 range"且 range 随 saving 退化。**这基本等于要求完整的 Ratios Conjecture（在 ℚ 上）**。
- **需要的新方法**（[推测]）：
  1. **Level-aspect cohomological/harmonic-family 的 ℤ 对照**：函数域（Sawin 2024）用几何/harmonic families；ℤ 上要类似 Sawin 的 "factorization functions in squarefree progressions" 的 level-aspect 版本，目前没有（phase-8 已列）。
  2. **把 2/2 ratios 归约到 level-aspect 的 1-level/2-level density**（Lee 型 "crossed zero residues" 的 level-aspect 改造，见 §5）；
  3. **绕过 ratios 的 parity-twisted 直接方法**：G-W-X 的 parity twist + Mellin 反演本质是 "Ratios ⇒ 素数对" 的翻译器；如果有一个 **level-aspect 的 pair-correlation/显式公式** 直接给出 parity-twisted ΛΛ 相关（等价于 H_Gold/LL 的墙），可以绕过 Ratios——但那回到 phase-5/7 的未解问题。

---

## 5. 评估 Lee arXiv:2610.32672v2 作为模板

**Lee 的设定 [事实]（abs 逐字要点）**：从**受限 uniform 2/2 zeta-ratios**（`ζ` 的 ratios，非 Dirichlet 族）证**每个固定正偶数差 h 的 HL 渐近**；ratios 误差 `O(U^{ϑ+ε})`，`1/2≤ϑ<(39−√177)/32≈0.8029`；**四个 shift 的实部都在 [3/64,5/64]**，虚部只需 `≤U^ν`（`0<ν≤1/4`）；固定实光滑权 `W`（支撑 (1,1+1/(25h))）下 error `O(x^{−Δ(ϑ)+ε})`，`Δ(ϑ)=7/16−ϑ+ϑ/(3−ϑ)>0`；加 RH 改进到 `x^{ϑ−7/8+ε}`。方法要点：**Mellin 反演中保留 crossed zero residues**，用**对数导数积分**估计 mixed term；**两个非负时间权**有相同对角项、对差 h 的系数相反——由此得到加权素数对和 `B_h` 的对数渐近，并联系 Nyman–Beurling 判据中的对数加权 Möbius 逼近。
**能否改造到 parity-twisted Goldbach？**
- **有利**：(i) Lee 的 "crossed zero residues" 技术正是处理 ratios 中分母 L 的零点在 Mellin 反演中的贡献——这正是 G-W-X 需要的（2/2 中分母在 1/2+η，零点被 GRH 排除，但**交换项**的分母在临界线附近，零点贡献不可忽略）；(ii) Lee 的 shift 范围（实部在 [3/64,5/64]，略高于 1/2 的窗口）与 G-W-X Lemma 3.1 使用时 `Re a=σ−r` 的窗口形似（G-W-X 用 a=s+u，Re a=1/2+η+Re u，u 复邻域内），**如果 G-W-X 实际只需要窗口内（而非严格临界线）的 ratios，Lee 的 shift 范围是相关的**；(iii) Lee 的 "两权相减" 技巧与 G-W-X 的 parity twist（`2R∨−(h₀+h₁)R` 型线性组合）都是"用两个相关量的组合提取目标"的思路。
- **不利/障碍**：(i) **通道不同**：Lee 是**单个 ζ**（整数对相关），G-W-X 是**模 q 的特征族平均**（level aspect，`Σ*_{χ mod q}`）——Lee 的技术没有任何 χ-平均/大筛结构，改造需要在 χ-族上重新做 "crossed zeros" 分析，而 χ-族零点的联合分布正是 level-aspect pair correlation（未证）；(ii) Lee 的 ratios 假设本身未证（也是 restricted Ratios），所以改造只给出另一个条件性定理；(iii) G-W-X 的 parity twist 需要 ratios 在 `2R∨−(h₀+h₁)R` 中的**微分/差分**结构（分子 shift 的导数）以及插值，Lee 的固定 shift uniform 版本不直接含 derivative 信息；(iv) Lee 的 error `x^{−Δ}` 是**对固定 h** 的，N（Goldbach 的偶 N）变化时 h=N 不是固定的——需要 h 直到 N 的均匀性（G-W-X 的 Mellin/parity 机制正是为此）。
**结论**：Lee 的**技术组件**（crossed zero residues、log-derivative mixed term、两权相消）值得吸收进"level-aspect 2/2 ratios 的误差分析"（可作为 (AL2) 的模板），但**不能直接改造**为 parity-twisted Goldbach 的证明；其真正价值是把"2/2 ratios 的误差项长什么样"具体化，从而给出 (AL2) 的一个可行分析骨架。

---

## 6. 参考（URL，2026-11-21 检索）

- G-W-X: H. Gou, V. Y. Wang, M. W. Xu, *Landau's problems through ratios of L-functions*, arXiv:2611.18825（本地 `phase7/lit/gwx.txt` 有提取全文）。
- Čech: M. Čech, arXiv:2110.04409v3；Trans. AMS 377 (2024) 9113，DOI 10.1090/tran/9113。
- Gao–Zhao: arXiv:2404.05081v2（quadratic Hecke, prime-related moduli）；系列 arXiv:2210.08840, 2304.14600, 2311.08626, 2402.17198。
- CFZ08: arXiv:0711.0718（ratios recipe）。
- Goes–Jackson–Miller–Montague–Ninsuwan–Peckner–Pham, arXiv:0909.4916（unitary test of Ratios）。
- Bui–Keating, arXiv:math/0607199；Cho–Park, arXiv:1802.01762；Fiorilli–Miller, arXiv:1111.3896。
- Sawin, *Square-root cancellation for sums of factorization functions over squarefree progressions in F_q[t]*, Acta Math. 233 (2024) 285–418, arXiv:2102.09730。
- Lee: arXiv:2610.32672v2。
- phase-8 汇总：`phase8/lit/ratios-status.md`（RC_D 精确陈述、known 结果/gap 表）。
