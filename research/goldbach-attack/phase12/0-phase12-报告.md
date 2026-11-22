# Phase-12 总报告：Goldbach 缺口的最终精确化——条件链、可证边界、精确的墙、数值与文献

> Lead 汇总（2026-11-22，phase-12）。参与：Lead + repo-verifier / proof-digest / goldbach-researcher / liu-auditor / heat-kernel-critic / lean-feasibility / spectral-numerics / kernel-theorist。
> 标注 **[证明]/[推导]/[数值]/[文献]/[事实]/[待核]/[推测]**。不造假、不夸大。
> 分报告：`0-plan.md`、`theory/0-lead-synthesis.md`、`theory/wrap-attack.md`、`audit/theorem-A.md`、`audit/route-c-final-audit.md`、`lit/conditional-routes.md`、`lit/alpoge-method.md`、`numerics/*`、`lean/*`、`status/*`。

---

## 0. 六行摘要

1. **Goldbach 没有被证明；本 phase 也没有证明 H_Ratios/RAT(c)。**
2. 本 phase 把整个缺口**收敛为一个精确、可陈述、可数值靶向的单一估计**：
   > **Goldbach ⇐ GRH（Alpöge/Claude，已声明、官方验证余 3 项）+ RAT_sym/der(c)，c>2**
   > 而 RAT_sym/der(c) 在截断框架内**精确等价于一个 residue-covariance 估计**：`|F−D| ≤ q^{−cη+ε}`（F = (1/q)Σ_{h≠0}ĉ(h)\d̂(h)，D = 对角 Euler 积），c>2 ⇒ Goldbach（误差 `N^{1−(c−2)η+ε}`）。
3. **可证边界已被完全刻画**：所有 Route-C 变体（截断 Möbius / AFE / Gauss-和 FE 折叠 / 模 q Poisson / 乘法结构 / 长度不对称）在 GRH 级工具下只能给 **c≤1/2**（uniform-in-η 意义下；允许 wrap 的平凡计数不改进）。证明包含一个**结构性"没有免费午餐"定理**：截断主块本身 = 非主特征上的"截断比值乘积"平均，wrap 就是该平均的偏离对角部分；`X>√q` 后不可对角化。
4. **精确的墙（定量）**：逻辑上 c>2 等价于**任何**固定的 q-幂节省于 residue covariance `F−D`（因 η 可任意小，δ=cη 可任意小——甚至 δ=0.001 也够）；按 worst-case 平凡界记账需 Δ 比 `X^{2−4η}` 再小 ≈q³（liu：γ>3）；但**真实 Δ 的数值外推显示缺口小得多：只需额外 ≈q^{0.05–0.1}（q≤10⁴ 时 1.5–3×），经验 c_max≈1.5–1.9，A=2 附近是边界**。现有 GRH 级严格工具仍给 0 个 q-幂（大筛 O(1)、trivial q^{4−8η}）。
5. **数值裁决**：Ratios 真值有**巨大余量**（移位区域 med|E−M|/√q 在 q=10⁶、η=.02→.002 为 70→500，拟合 = q^{1/2+o(1)}·C(η)，C(η)≈η^{−0.85}；q-指数 α→0.5 与 η 无关）⇒ H_Ratios 为真且远强于所需；截断法的真实 wrap 净量 Δ 远小于 worst-case（含 μ 抵消 4–5 个量级、A≥1.5 时抵消质量 0.01–0.07），经验 c_max≈1.5–1.9，**c>2 的缺口可能只有 q^{0.05–0.1}，但严格可证为 0** ⇒ **障碍是方法级 = parity barrier，不是命题为假**。
6. **文献/状态**：over ℚ 上 2/2 Ratios 仍只有猜想（1/1 只有 GRH-条件受限结果）；函数域特殊族（BFK）有移位区域 2/2；无"GRH+更弱假设 ⇒ 完整 Goldbach"的已知定理；Alpöge 声明后**无新预印本**（arXiv 11-20～11-23 检索 0 条）；官方验证 11-22 04:35 UTC 版仍 **3 项 running**（主证明 paranoid replay、主证明 lake comparator、组合导出 comparator；沙盒独立 rebuild/导出逐字节一致、con-ron --compare 已通过；paranoid.log 仍 404）。Alpöge 证明**不提供** GRH 之外的可用量化机器。

---

## 1. 本 phase 的核心结构性收获：定理 A 与 RAT_sym/der(c)

### 1.1 GWX 需要什么（逐字核对 arXiv:2611.18825 LaTeX 源）
- **Hypothesis 1.1 (RC_D(ω_D))**：`Σ*_{χ mod q}L(a,χ)L(b,χ̄)/(L(s,χ)L(t,χ̄)) = M_q + O(q^{1−ω_D+ε}(1+T)^B)`，uniform 于**ℜa=ℜb=1/2（分子恰在临界线）**、ℜs=ℜt=1/2+η、`T≤100log(2q)`、**ω_D 与 η 无关**、全 q（含复合导体）。
- GWX 由 §3.6 三点插值从 Hyp 1.1 得 Lemma 3.1；插值损失 `8(η+r)(2+ω_D)`，导致其证明要求 `η<ω_D/16` —— 这是"需要与 η 无关 saving"的技术来源。

### 1.2 关键观察（phase-12 的杠杆）：绕过插值
若**直接假设** Lemma 3.1 的 (3.2)（双构型、磁盘全纯/一致、对 u,v 的混合导数），则 **§3.6 整节可删**，§3.2–§3.5 逐行成立，且"`ω>2η`"是唯一对 saving 的要求。逐行审计：`audit/theorem-A.md`（liu-auditor）：(3.2) 只在行 973（主项）、1014（E,E∨）、1063–68/1347（Cauchy，仅 |Im|≤5log(2q)）、1181–1195/1363（误差 N^{1−ω+2η}）被使用；无其它"临界线分子"依赖。
**修正**：plan 早先的 RAT(c) 缺**反射构型** (R)，需改为 **RAT_sym/der(c)**：

> **RAT_sym/der(c)**：对每个固定小 η，q>1，ℜs=ℜt=1/2+η，|Im|≤5log(2q)，在 (D) `a=s+u,b=t+v` 与 (R) `a=1−t−v,b=1−s−u`（|u|,|v|≤r=η/8）上，(3.2) 的**混合导数**误差 `≤ C_{η,B,ε}q^{1−cη+ε}(1+T)^B`，盘上全纯/一致。

### 1.3 定理 A（[推导]，已审计）
**GRH + RAT_sym/der(c)，c>2 ⇒ 所有充分大偶数 N**：
`Σ_{m+n=N}Λ(m)Λ(n) = N𝔖(N) + O_ε(N^{1−(c−2)η+ε})`，固定小 η；主项 `N𝔖(N)≥2C₂N`。
⇒ **c>2 ⇒ Goldbach（对所有充分大偶数 + power-saving）**。常数约束：`cη≤1/2+η`、`(c−2)η≤1/2`、η<1/6——均可由固定小 η 满足。

---

## 2. 可证边界：c≤1/2 的完全刻画

### 2.1 两条路线同一终点
- **Route C（截断 Möbius + 精确正交性）**：no-wrap `X²<q`、截断误差 `qX^{−η}` ⇒ saving `ω=ηA`，A<1/2 ⇒ **c≤1/2**（phase-11）。
- **[证明] 结构性定理（kernel-theorist）**：q 素时
  `E^{(X)} := Σ*_χ P_aP_bQ_sQ_t = Σ_{χ≠χ₀}(P_aQ_s)(χ)(P_bQ_t)(χ̄)` —— Route C 截断主块 = **非主特征上"截断比值乘积"的平均**。`X²≤q` 时 `A≡B⇔A=B`，平均对角化（c≤1/2 的机制）；`X²>q` 时 A≠B 的 wrap 项就是该平均的偏离对角部分。
- **账本修正**（liu-auditor + kernel-theorist 独立）：进入 R_q 的 wrap 贡献是 **`(q−1)W`**（不是早先 plan 的 W 或 X²/q）；`(q−1)|W| ≲ X^{2−4η}η^{−2}log⁴`；与 `qX^{−η}` 平衡 ⇒ **uniform c≤1/2**（若固定 η，trivial wrap 给 c≤1/(2−3η)，η→0 时 →1/2）。**允许 wrap 的平凡计数不改进 uniform c。**

### 2.2 精确恒等式（[证明]，Lead 与 kernel 独立，数值验证至 1e-16）
q 素：`E^{(X)} = (q−1)(D+W) − S_c\bar S_d + T`（bookkeeping 变体含 `−(q−1)V_cV_d`，V_c=Σ_{q|A}c_A），其中
`D=Σ_Ac_Ad_A`（对角，→ 对角 Euler 积 Z_q）、`W=Σ_{A≠B,A≡B,(AB,q)=1}c_A\bar d_B`（wrap）、`T=Σ_{q|AB}c_A\bar d_B`。
⇒ 因 `E^{(X)}≈R_q≈M_q≈qZ_q`，必须小的是 **`Δ := E^{(X)}−(q−1)D = (q−1)W − S_c\bar S_d + T`**。

### 2.3 相位-11 移位区域定理的适用性修正
phase-11 `shifted-region-lead.md` §1 step 1 的 `L(u,χ)` 截断误差 `X^{−η}` 不能由 PV+Abel 得到（只给 `q^{1/2}X^{−1/2−η}`）；严格化需 Perron+GRH 到 `1/2+ε` 线（给亚多项式常数）⇒ 严格形式下 saving 应记为 **c<1/2**（结论不变）。[待核：用 AFE 分子可绕开该步，但仍死在 wrap。]

---

## 3. 精确的墙：三种等价/等价化的表述

### 3.1 H_wrap（phase-11 原版）
`Σ_{1≤|k|≤T}Σ_{nr−ml=kq}c(n,r)\bar d(m,l) ≪ q^{1−ω}`，需 Type II/Chowla 级一致 saving（现有工具：BV 单模无 saving；MRT/Tao–Teräväinen 只有对数/几乎所有尺度；additive divisor 无 q-一致、无 μ 权；大筛只给 L²=O(1)）。

### 3.2 TL(A)（kernel-theorist；Route C 内的精确重述）
`TL(A)`：`(1/q)Σ_{χ≠χ₀}(P_aQ_s)(P_bQ_t) = F_pred + O(q^{−Aη+ε}(1+T)^B)`，X=q^A；F_pred 由 phase-11 Euler 积恒等式显式给出。**Route C 内：RAT(c) ⇔ TL(A) for A≤c；TL(A)⇒RAT(A)。** （不是数学 no-go：其它方法证 RAT 后 TL 自动成立——liu-auditor 修正了 kernel 的过强表述。）

### 3.3 Residue covariance（Lead 的"数论内容"版；最精确、可数值靶向）
令 `ĉ(h)=Σ_{A≤X²}c_Ae(hA/q)`，`F=(1/q)Σ_{h=1}^{q−1}ĉ(h)\overline{d̂(h)}`。则**[证明]**：
`F = Σ_{ρ=0}^{q−1}(S_ρ−S_c/q)(\overline{S'_ρ−S_d/q})`（residue 类求和的**协方差**），`F−D = W−S_c\bar S_d/q`，且 `Δ=(q−1)(F−D)−(1/q)S_c\bar S_d+T−(q−1)V_cV_d`。
⇒ **H_wrap[A]：`|F−D| ≤ q^{−Aη+ε}(1+T)^B` ⇒ Δ≤q^{1−Aη} ⇒ RAT_sym/der(c=A)。`X²≤q` 时自动成立（S_ρ=c_ρ ⇒ F=D），即 c≤1/2 的机制。**

**"任意小的 saving 就够"（重要）**：因 η 可任意小，若对某个固定 A>2、某个固定 δ>0 有 `|F−D| ≤ q^{−δ+ε}`（对所有大 q、对该 η=δ/A 的系数族），则取 η=δ/A 得 RAT_sym/der(A)，**c=A>2 ⇒ Goldbach**。所以**逻辑上的缺口不是"1/2 的 saving"，而是"任何固定 q-幂 saving（哪怕 δ=0.001）"**。

### 3.4 定量形式（liu-auditor 的 γ 表述）
若 `Δ ≲ X^{2−4η}q^{−γ}` 一致成立，则 `c ≤ (1+γ)/(2−3η)`：trivial γ=0 → c≤1/2；"完美 equidistribution" γ=1 → c≤1；**c>2 需 γ>3**（即比 equidistribution 再多 3 个 q-幂）。
两表述自洽：在 A≈2、η→0 时，"任意固定 δ 的 saving" 对应 γ≥3+δ。

### 3.5 已知界的精确差距（[证明]，kernel §10）
(i) 平凡 `|ĉ(h)|≤Σ|c_A|≲X^{1−2η}`；模板 `|F|` 的 trivial 值 ~q^{4−8η}（A=2）；
(ii) 拆 m=ρ+tq 用 GRH 的 μ-in-AP：`|ĉ|≪X^{1/2−2η}q^{1/2+ε}`；
(iii) 大筛：`Σ_h|ĉ|²=qΣ_ρ|S_ρ|²≲qη^{−1}log³` ⇒ `|F|≲η^{−1}log³=O(1)`。
**所需 q^{−cη} 与可证 O(1) 之间是 q 的严格正幂（A=2 时约 q^{2–4}），不是常数因子。**

---

## 4. 数值裁决（真值 vs 方法 vs 墙）

### 4.1 Ratios 真值：巨大余量（支持 H_Ratios）
spectral-numerics `numerics/ratios-truth.md`（q 素 211…10⁶；每 (构型,η,q) 30–50 组随机 shift；|Im|≤2，剔除 a+b≈1；精确 char-by-char 校验管线；A_q 用修正 mask）：
- **移位区域构型**（RAT(c) 构型，四者 Re=1/2+η）：`med|E−M|/√q` 在 q=10⁶ 处 = 70.2 (η=.02), 132.6 (.01), 268.0 (.005), 500.3 (.002)；**q=10⁵→10⁶ 的局部指数回落到 0.48–0.56**（小 q 处 α>0.5 是有限 q/重尾交叉）；`C(η)=med/√q ≈ const·η^{−0.85±0.1}`。**⇒ 误差 = q^{1/2+o(1)}·C(η)：q-指数 saving（=1/2）与 η 无关，η 只进入常数（~η^{−0.85}）。**
- **|M_q| 标度**：`|M_q| ≈ q·f(η)`，f(η)≈η^{−0.14±0.05}（**不是 q/η²**）；相对误差 `|R−M|/|M| ≈ q^{−1/2+o(1)}·η^{−0.7±0.15}`。
- **Hyp 1.1 原构型**（分子临界线、分母 1/2+η）：同类数据，固定 q=10⁵ 时 |R−M| ∝ η^{−1.05±0.1}（RMS）；|M| 随 η 弱增长后饱和。phase-11 已测 q 方向 α≈0.53–0.56（全部导体类，A_q mask 修正后），T 依赖多项式，signed mean≈0，无 ramified 异常。
- **裁决**：H_Ratios 真值的关键性质成立——**q-幂 saving 指数与 η 无关**（η→0 不退化，只常数 blow-up）；Hyp 1.1 的 `O_η` 常数可吸收。真值远强于任何截断法（真值 saving 1/2 vs 方法 c≤1/2 且随 η 退化）。

### 4.2 墙的实测（c_emp≈1.5–1.9，c>2 未达但缺口远小于 worst-case；A=2 附近是边界）
- **Lead（q=1009, η=0.2；`theory/checkE5.py`）**：A=0.5→1.1 时 |Δ|=15→175，目标 q^{1−ηA}=507→220；|R−E|≈X^{−0.5}（远快于 qX^{−η}）⇒ **截断误差不是瓶颈，瓶颈是 Δ**；Δ 拟合 ~X^{0.67}。
- **heat-kernel-critic（真实系数、独立代码、`numerics/wrap.md`，60+ 参数组、5 shifts 平均）**：
  - 模型分离：rect 权重下 W≈X⁴/q（纯几何平凡）；**无 μ 正权模型** W≈(4.6–12.4)X²/q（= plan 的"平凡 X²/q"）；**真实系数（含 μ）** W 比 X²/q 小 4–5 个数量级（拟合 W≈X^{0.84}q^{−0.85}η^{−0.29}，rms 0.36）。
  - 净量 Δ 幂律（crit 构型 β≈0.35, γ≈0.43, δ≈−0.24；rat 构型 β≈0.33, γ≈0.36, δ≈+0.15；rms≈0.6–0.7≈factor 2）。
  - **抵消质量随 A 迅速改善**：Δ/(|qW|+|ScSd|) = 0.62–0.78 (A=1) → **0.01–0.07 (A≥1.5)**。
  - **c 经验上限：crit c≈1.1–1.4；rat（RAT(c) 构型）c≈1.5–1.7**（A≤2）。直接检验：A=1.25 时 ρ=Δ/q^{1−ηA}∈[0.19,2.82]（q=1009 rat=0.19–0.38 pass；crit η=.2 2.82 fail）；**A=2, q=53, rat η=.05：ρ=0.83 pass**（crit η=.2 fail，ρ=1.7）；A=2.25 q=53 已 ρ=1.1–5.6 fail。⇒ **c≈2 附近是边界而非严格不可能**。
  - **c>2 所需额外节省 ≈q^{0.05–0.1}·η^{−O(1)}（q≤10⁴ 时约 1.5–3×，随 q 缓增）——比早先"平凡计数"叙事的 q²–q⁴ 小 1–2 个数量级**（但仍是正的 q-幂，现有截断方法未达）。
  - 非对称四段长度（N≠M）在中等 A、η≥0.1 把 Δ 压 ~1.6–2×（A=1,q=101: 72→39；q=199,A=1.25: 126→74）；更强非对称不普适。
- **kernel-theorist 模型探针**：F 的 Fourier 涨落 O(1)–O(10) 且不随 q/X 衰减；|F−D|、|Δ| 随 X 缓慢增长（拟合 X^{0.22–0.34}）⇒ H_wrap 的小性是 q-一致负幂，不是 X-衰减。
- **Kloosterman/FE 折叠**（heat-kernel-critic）：|Σ c_A\bar d_Be(BĀ/q)|/L1 ≈ c/q^{0.85–1}，无额外 √-级节省，且 |S1| 比 W 大 6–150 倍 ⇒ 该折叠不解决问题。
- **h-分解**：|F|=(1/q)|Σ_{h≠0}ĉd̂| 在 A≤1 时 ≪Δ，A≥1.5 时与 Δ 同阶（q=53,A=2: 26.7 vs Δ 31）⇒ 高 A 由 residue covariance 主导，与 §3.3 的 F 形式相容（F−D 的复相位未直接算，待完成）。

### 4.3 结论
- 真值：H_Ratios 成立且以**指数性 saving 1/2** 成立（常数 blow-up 无妨）——与 GWX 的假设完全一致。
- 方法：c≤1/2（uniform）是"截断框架"的天花板；允许 wrap 平凡计数不改进；数值上 A≳1.25 已溃败。
- **c>2 需要 net wrap 量的 ≈q³ 个 q-幂的额外节省**（或 residue covariance 的任意固定 q-幂节省）——现有工具为 0。

---

## 5. 文献与状态（goldbach-researcher / proof-digest / repo-verifier）

### 5.1 Ratios over ℚ：2/2 仍只有猜想
- **WX25**（Wang–Xu, IMRN 2025 no.18, arXiv:2405.04094v2）：**素数导体** 2/2 Conjecture 2.1，**未证任何情形**；GWX 推广到全导体并作为假设。
- over ℚ：Dirichlet **1/1** 只有 GRH-条件、受限 shift、实特征等特殊结果（**Čech 2024** Trans. AMS 377, arXiv:2110.04409；**Gao–Zhao** 2022–24 特殊族/单 shift）。**2/2 over ℚ 无任何定理。**
- **Baluyot–Čech 2025**（arXiv:2501.12529）：conductor-aspect MD 的**启发式** + 延拓猜想（未证）。
- **函数域**：**Bui–Florea–Keating**（arXiv:2109.10396；Trans. AMS 376 (2023) 4453–4510）证 quadratic Dirichlet 的 1/1 与 **2/2（分母 shift Re>g^{−1/4+ε}）**；这是"移位区域 2/2 可证"的最强已有证据（函数域、特殊族）。
- **SeungJu Lee arXiv:2610.32672v2**（2026-11-03）：只证**固定偶差 prime pairs 的 HL 渐近**（`Σ_{n≤x}Λ(n)Λ(n+h)=𝔖(h)x+o(x)`），**不覆盖 Goldbach**；其假设是移位区域、有限积分 2/2 ζ-ratios（Conrey–Snaith 型），saving/shift 比 ≥2.5（最不利端）。⇒ **c>2 比文献中标准移位区域 Ratios 假设更"温和"**（但仍是未证假设）。

### 5.2 "GRH+X ⇒ 完整二元 Goldbach"的已知路线只有两条
- GWX（GRH + RC_D）；Li–Liu（GRH + 谱假设 S/R，ad hoc，phase-2/3 审计）。
- **无已知"GRH+严格更弱假设 ⇒ Goldbach"定理**。弱假设只到 almost-all：quasi-RH（Re≤Θ<11/12）⇒ E(N)≪N^{1/2}(log)¹⁰⁰（H. Li–Z. Liu arXiv:2610.26756）；**GRH 单独 E(x)≪x^{1/2+ε}（Hardy–Littlewood 1924；MV1975 的 E(X)≪X^{1−δ} 是无条件的——本 phase 纠正旧误记）**；EH/BV/BFI 只到 1+2/1+1.9/1+1.4（parity barrier）；Chowla/Sarnak 无已知蕴含。
- **"pair correlation ⇒ Goldbach" 路线的文献裁决**（`lit/pair-correlation-goldbach.md`）：Montgomery F(α,T) 的无条件范围 = |α|≤1（Baluyot–Goldston–Suriajaya–Turnage-Butterbaugh arXiv:2306.04799 Thm 1，不假设 RH；|α|>1 仍是强 pair correlation 猜想）。**Languasco–Perelli, Mathematika 43 (1996) 349–361**：GRH + 广义 pair correlation GMC(ϑ) ⇒ 例外集 `E(X)≪X^{1−2ϑ+ε}`；最强 ϑ=1/2 也只到 `E(X)≪X^ε`——**永远到不了"所有大偶数"**。Ratios ⇒ pair correlation 已证（Conrey–Snaith 2007），反向未知 ⇒ pair correlation 型假设更弱但**可证地不够**（封顶在例外集）；不是隐藏捷径。Conrey–Keating 2016 不是"pair correlation ⇒ twin primes"定理。
- **显式公式直接算 Goldbach 计数**（Fujii 1991；Bhowmik–Schlage-Puchta 2010；Languasco–Zaccagnini 2012；Billington–Cheng–Schettler–Suriajaya 2023 等）都是**对 n 的平均**：对 n 求和时字符正交性消掉模 n 的 Dirichlet L，只剩 ζ 零点 ⇒ 结构上看不到模 n 算术，无法给逐 N/全 N；逐 N 需要模 n 特征族（Ratios 型）输入。
- **post-Alpöge（2026-11-20+）**：无新 Goldbach/RH→Goldbach 预印本；GWX 仍 v1、OpenAlex 引用 0；唯一新 RH 文献是 Rubinstein 164 页 ζ-only 人类可读草稿（与 Goldbach/Ratios 无关）。

### 5.3 官方验证状态（`status/verification.md`，repo-verifier；实抓 2026-11-22 11:36–11:42 UTC + Lead 11:29 UTC，页面自述 2026-11-22 04:35 UTC 版，index.html 27,222 B sha256 `01a43fc8…88a7` 多抓稳定）
- **仍余 3 项 running**：(a) 主证明导出上的 Lean default+paranoid kernel replay；(b) 主证明 `lake comparator` end-to-end；(c) 组合算术导出的 `lake comparator`（62 GB 导出、单线程、"many hours"）。页面 Summary 原句仍 "still in progress"；`paranoid.log`/`comparator.log`/`lake-comparator.log` 均 HTTP 404（三次抓取）→ **无公开结果文件**。
- 11-21 12:55 UTC 之后的**新增（8 行）**：沙盒（bubblewrap，无网络、源码只读）`lake build Main` exit 0（18:07:21Z）；沙盒导出与已发布导出**逐字节 identical**（61,570,595,788 B，sha256 `5ea74b91…244e`，19:32:56Z）；sandbox olean manifest 175,186/175,187 identical（唯一差异 LocModel.olean 系 Lean #15498 变量名竞争，PR #15499 已修）；`con-ron --compare` accept（主证明 23:02:33Z、组合导出 23:15:58Z）。
- `SHA256SUMS` 更新为 3,078 B（sha256 `3c902ade…`，Last-Modified 2026-11-22 04:09:51 GMT），新增条目逐一校验通过；`audit.log`/`comparator.json` 未变。
- 上游未变：本地 `/home/kiler/rh-full` HEAD `7cbf7a0c32…`、dirty=0；本地 archive sha256 `9631b4f0…c7fc` = MIT Provenance Source archive；`CocoSgt` 镜像无新 commit/release（pushed_at 2026-11-20T15:13:36Z）；alpo.ge 主页/remark.pdf sha 未变。社区 Comparator 仓库 `verification/` 仍无结果（NOTES："The build is in progress"），且 NOTES 披露其 `src/` 已被后续 PR 修改（原始档案 = 首 commit `40e56bab`）——**验证对象是原始档案/其导出，不是社区 HEAD**。
- arXiv：GWX 2611.18825 仍 v1（11-13）；Lee 2610.32672 仍 v2（11-03）；`au:Alpoge` 无新条目。新出现 Zenodo 阅读指南（Kokonoha, 24432174, 2026-11-22T02:40:59Z），**非验证**、其"已由社区认证"表述不可引用。
- 仍**不能宣称**：官方验证完成、peer review、数学正确性、一般 GRH（MIT scope 明文仅 Dirichlet L-functions）、社区 HEAD 已验证、Zenodo"社区认证"。**不能**宣称 Goldbach 有任何新证据。

### 5.4 Alpöge 证明方法再挖掘（proof-digest）
- 定量层 = **经典无条件解析数论的形式化**（Siegel 下界、Siegel–Walfisz、ZFR、显式公式、零点计数、零密度盒、大筛、特征和矩、GL(2) Rankin 均方），**无一项比 GRH 直接推论更强**；GRH 下多被超越或 vacuous。
- **axiom/接口警示**：`ExplZeta`/`ExplChi` 只有 def 无证明项；`SiegelWalfiszAP`、`PrimeShareSW`、`ZeroDensityBound`、`CharOrtho`、`ParsevalHolder` 未找到证明项。已证：siegelLower、siegelWalfisz、zFRDirichlet、zeroFreeRegion、repulsion、log-free 零密度、logDerOne_holds、zeroCount_holds、zero_density_box、显式常数大筛、M4。
- 三次"升级为 Ratios/family 均方"的尝试全部否决；**对 RAT(c)/wrap 无任何新数学输入**（唯一价值：Lean 引理库工程性复用）。

---

## 6. Lean 机器验证产物（lean-feasibility）

`phase12/lean/nowrap.lean`（197 行）+ `wrap.lean`（158 行）：**EXIT 0、无 sorry、公理仅 propext/Classical.choice/Quot.sound**。
- `Σ_{χ≠1}χ(A)\barχ(B) = φ(q)[A=B] − 1`（q 素即 (q−1)[A=B]−1）；primitive 版同一恒等式（Mathlib v4.36 已有 IsPrimitive/conductor API）。
- wrap 计数恒等式 `Σ_{A≡B,A≠B}c_Ad_B = Σ_rC_rD_r − Σ_Ac_Ad_A`；`A%q=B%q ↔ q|(A−B)`（residue 形式 ↔ kq 差集形式桥）。
- 诚实边界：这些是有限组合恒等式（可审计骨架），**本身不证明 H_Ratios/c>2**；完整 2-vs-2 二重和 W 未形式化（1–2 人日）。

---

## 7. 净结论：我们倒在哪里？

| 层 | 状态 |
|---|---|
| RH/GRH（ζ + 全部 Dirichlet L） | 已声明、Lean 形式验证接近完成（余 3 项 replay/comparator；沙盒 rebuild/导出逐字节一致/con-ron 已通过；无 peer review） |
| GWX 归约（GRH+Ratios ⇒ 四个 Landau 问题） | [审计通过] 唯一缺口 = Ratios 型假设；Goldbach 需要 level-aspect 2/2 Ratios |
| Ratios 真值 | [数值] 强支持：误差 = q^{1/2+o(1)}·C(η)，q-指数 saving=1/2，与 η 无关（常数 blow-up） |
| 可证范围 | c≤1/2（截断法天花板；uniform-in-η；允许 wrap 平凡计数不改进）；移位区域弱 Ratios（phase-11，严格化后 c<1/2） |
| 需要的输入 | RAT_sym/der(c>2)；等价地 H_wrap[A>2]：residue covariance `|F−D| ≤ q^{−cη}`；等价地 **任何固定 q-幂节省于 F−D（δ 可任意小）**。定量（数值外推）：Δ 需再压 ≈q^{0.05–0.1}（c_emp≈1.5–1.9 → c>2）；worst-case 记账需 q³（γ>3） |
| 已知工具差距 | 严格可证：0 个 q-幂（大筛 O(1)）；数值：c_emp≈1.5–1.9（rat 构型）、A=2 边界（q=53,η=.05 ρ≈0.83 pass；A=2.25 fail）；无不一致工具 |
| 文献中是否已有 | over ℚ 无（2/2 只有猜想；1/1 只有 GRH-条件受限结果）；函数域特殊族有；无 GRH+更弱假设 ⇒ Goldbach |
| 新工具是否出现 | 无（Alpöge 方法不提供；无新预印本） |

**一句话**：Goldbach 现在精确地"倒在一个 level-aspect 2/2 Ratios 的任意 q-幂 power saving 上"。这个 statement 是标准的、可陈述、可数值/Lean 靶向的；但它也是 parity barrier 侧的已知难题——over ℚ 连 1/1 的完整情形都未证，2/2 完全未证。**我们证明了：用 GRH 级工具做截断/正交性/折叠的一切组合，严格只能到 c≤1/2；数值上真实 wrap 净量 Δ 的抵消远超 worst-case，把经验 c 推到 1.5–1.9，缺口可能只有 q^{0.05–0.1}——但严格可证的额外节省为 0（大筛级），这是 parity barrier 的量化形态。**

---

## 8. 下一步（若继续；按优先级）

1. **H_wrap 最小版本的形式化**：A=2、T 有界、|Im|≤1、光滑权、q 素——写成独立引理（所有误差项显式），供 Lean/数值靶向。kernel-theorist 已提议可写。
2. **residue covariance 的解析攻击（弱化目标：任意固定 δ>0 的 saving）**：`F−D` 的 Fourier 形式 `(1/q)Σ_{h≠0}ĉ(h)\d̂(h)`，`ĉ(h)=Σ_{n,m≤X}n^{-a}μ(m)m^{−c}e(hnm/q)`；注意"任意固定 δ"目标允许把 A 取得更大（X=q^A, A>2 甚至更大）并配合非对称长度/光滑权。heat-kernel-critic 已给出廉价 residue-FFT 管道可把 F 复相位算到 q≤10⁴、A≤1.5——先做该项数值，再决定是否值得解析攻击。kernel §2–§4 的失败是在"固定 A≈2 且要求 2η saving"下的；弱化目标未试。
3. **函数域 ↔ ℚ 精确对照**：BFK 的 negative-moment 方法在函数域给移位区域 2/2；明确 ℚ 上失败于哪一步。
4. **Ratios 量化率（H_UNIF）**：若只求 Goldbach 定性，是否可用 ω(q)log q→∞ 的更弱假设（GWX 未形式化）。
5. **官方验证跟踪**；若 paranoid/comparator 完成，GRH 部分闭合，Goldbach 状态不变。
6. **真实价值路径**：把 phase-11/12 正面结果（移位区域弱 Ratios、Euler 积恒等式、精确恒等式、TL(A)/residue covariance 表述、Lean 恒等式）整理成技术报告/短文。

---

## 9. 文件索引
- 计划/框架：`phase12/0-plan.md`、`phase12/theory/0-lead-synthesis.md`
- 定理 A 审计：`phase12/audit/theorem-A.md`（liu-auditor）
- Route C 终审：`phase12/audit/route-c-final-audit.md`（liu-auditor）
- 理论主攻：`phase12/theory/wrap-attack.md`（kernel-theorist）+ `wprobe*.py`
- Lead 数值：`phase12/theory/checkE*.py`（E/Δ/W 账本验证）
- 数值：`phase12/numerics/`（spectral：`truth_run*.log`；heat-kernel：`logs_delta*`、`logs_wrap*`；报告 `wrap.md`、`ratios-truth.md` 进行中）
- 文献：`phase12/lit/conditional-routes.md`、`alpoge-method.md`、`pair-correlation-goldbach.md`（进行中）、`lee_v2.pdf/txt`
- Lean：`phase12/lean/{nowrap,wrap}.lean`、`report.md`、`nowrap_wrap.output.txt`
- 状态：`phase12/status/`（repo-verifier，进行中）
