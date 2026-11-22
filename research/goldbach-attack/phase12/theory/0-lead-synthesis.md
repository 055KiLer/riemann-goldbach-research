# Phase-12 Lead 综合：Goldbach 缺口的精确化、可证边界与"离终点多远"——诚实版

> Lead，2026-11-22（phase-12）。本文汇总 phase-12 全部结果（Lead 推导 + 8 个 teammate 的交付），并给出本 phase 的净结论。
> 全部标注 [证明]/[推导]/[数值]/[文献]/[推测]。不造假、不夸大。

---

## 0. 一句话结论

**Goldbach 未被证明。** 本 phase 把"还差什么"推进到如下唯一形式：

> **Goldbach ⇐ GRH（Alpöge/Claude，已声明；官方验证 11-22 04:35 UTC 版仍余 2 项 kernel/comparator replay）+ RAT_sym/der(c>2)**
>
> 其中 RAT_sym/der(c) 是"移位区域 2/2 Ratios 平均"的一个精确陈述（GWX Hyp 1.1 的可替换弱化版）：误差 saving 为 `c·η`，`η` 是离临界线的距离。**c>2 即可推出 Goldbach（Qualitative 与 power-saving 两种形式；见 §2）。**

而本 phase 证明了所有已知技术（Route C / truncation / AFE / Gauss 和折叠 / Poisson / 乘法结构 / 长度不对称）都只能给出 **c≤1/2**，并且给出**精确的"墙"**：c>2 等价于"截断比值非主特征平均的 power saving"（= 2/2 Ratios 的临界线/level-aspect 深度），文献中 over ℚ 完全未证（只有函数域特殊族的结果）。**数值上 Ratios 真值有巨大余量（相对误差 q^{−1/2+o(1)}，与 η 无关的 *指数*、仅常数 blow-up），说明障碍是方法级的（parity barrier），不是命题为假。**

---

## 1. 条件链的精确化（本 phase 最大结构性收获）

### 1.1 GWX 需要什么（逐字核对 LaTeX 源后）
- **Hypothesis 1.1 (RC_D(ω_D))**：`Σ*_{χ mod q} L(a,χ)L(b,χ̄)/(L(s,χ)L(t,χ̄)) = M_q + O(q^{1−ω_D+ε}(1+T)^B)`，uniform：**ℜa=ℜb=1/2（分子恰在临界线）**，ℜs=ℜt=1/2+η，`T≤100log(2q)`，**ω_D 与 η 无关**。[文献：GWX arXiv:2611.18825 §1.1；LaTeX 源已核]
- GWX 由 §3.6 的三点插值从 Hyp 1.1 造出 Lemma 3.1；插值损失 `8(η+r)(2+ω_D)`，要求 `η<ω_D/16`。这是"需要与 η 无关 saving"的技术来源。
- **本 phase 发现**：若**直接假设** Lemma 3.1 的 (3.2)（即在分子/分母都距临界线 η 的构型上、磁盘一致、含反射构型），则 **§3.6 整节可删**，GWX §3.2–§3.5 逐行成立，且"ω>2η"是唯一对 saving 的要求。逐行审计见 `phase12/audit/theorem-A.md`（liu-auditor，给出 (D)/(R) 双构型、|Im|≤5log(2q) 等常数限制）。

### 1.2 定理 A（[推导]，已审计）
**定理 A**：GRH + RAT_sym/der(c)，c>2 ⇒ 所有充分大偶数 N：
`Σ_{m+n=N}Λ(m)Λ(n) = N𝔖(N) + O_ε(N^{1−(c−2)η+ε})`，取固定小 η（满足 `(c−2)η>0`，`cη≤1/2+η`，`(c−2)η≤1/2`）。
（推论：取任意固定 η，误差为 `N^{1−δ}`，δ=(c−2)η>0；主项 `N𝔖(N)≥2C₂N`。故 c>2 ⇒ Goldbach 对所有充分大偶数 + power saving。）
**RAT_sym/der(c)**（liu-auditor 修正版）：对每个固定小 η，q>1，ℜs=ℜt=1/2+η，|Im|≤5log(2q)，在 (D) 直接构型 `a=s+u,b=t+v` 与 (R) 反射构型 `a=1−t−v,b=1−s−u`（|u|,|v|≤r=η/8）上，(3.2) 的**混合导数**误差 ≤ q^{1−cη+ε}(1+T)^B，且在圆盘上全纯/一致。

---

## 2. 可证范围：c≤1/2 的完全刻画（本 phase 的"上限定理"）

### 2.1 两条独立路线都止步于 c=1/2
- **Route C（截断 Möbius + 精确正交性，phase-11）**：no-wrap 条件 `X²<q`，截断误差 `qX^{−η}` ⇒ saving `ω=ηA`，A=log X/log q<1/2 ⇒ **c≤1/2**。
- **本 phase 的修正与加固**（kernel-theorist `phase12/theory/wrap-attack.md`，liu-auditor `phase12/audit/theorem-A.md` 独立复核）：
  - 进入 R_q 的 wrap 贡献是 **`(q−1)W`**（不是 plan 早先写的 W；plan §1.3 的 "c≈1" 已撤回）。
  - 平凡界 `(q−1)|W| ≲ X^{2−4η}η^{−2}log⁴`；与 `qX^{−η}` 平衡 ⇒ **A≤1/(2−3η) ⇒ c≤1/2**。**允许 wrap 的平凡计数不改进 c**。
  - [证明] **循环性/最小不可行性**：q 素时 `E^{(X)} := Σ*_χ P_aP_bQ_sQ_t = Σ_{χ≠χ₀}(P_aQ_s)(χ)(P_bQ_t)(χ̄)`——Route C 的截断主块**本身就是一个非主特征上的"截断比值乘积"平均**；wrap 项 = 该平均的偏离对角部分，**不能作为独立误差项估计**。任何"改进 W 的估计"都必须证明一个 Ratios 型平均的 power saving。**"X>√q 之后没有免费午餐"**。
  - 五条路线全部失败并给出精确卡点：Gauss 和/FE 折叠（得退化的单相位 `e(nn'r·l̄/q)`，非双相位 Kloosterman；σ>1/2 系数绝对可和、内和 O(1)、Weil √q 无适用结构）；模 q Poisson/FFT（`Σ_{A≡B}c_A\bar d_B=(1/q)Σ_h ĉ(h)\bar d̂(h)`，ĉ 的生成函数就是截断比值 ⇒ 循环）；乘法结构/Weil（补全的边界项 = wrap 本身）；长度不对称（缩短任一段同时降低 saving，最优仍 c≤1/2）。

### 2.2 相位-11 移位区域定理的适用性修正（[待核]→已核）
- phase-11 `shifted-region-lead.md` §1 step 1 的 `L(u,χ)=Σ_{n≤X}+O(X^{−η})` 不能由 PV+Abel 得到（只给 `q^{1/2}X^{−1/2−η}`）；若要用 Perron+GRH 到 `X^{−η}` 需临界线 Lindelöf 型界（GRH 不直接给出，只有亚多项式 `q^{o(1)}`）。因此 phase-11 定理的**严格形式**应把 saving 记为 `c<1/2`（或常数更小），但 **c≤1/2 的结论不受影响**。

---

## 3. 精确的墙：三个等价表述

1. **H_wrap（phase-11 原版）**：`Σ_{1≤|k|≤T}Σ_{nr−ml=kq}c(n,r)\bar d(m,l) ≪ q^{1−ω}`，需 Type II/Chowla 级 power saving。
2. **TL(A)（kernel-theorist 本 phase）**：`c>2 ⇔` 证明截断比值非主特征平均的 power saving：`(1/q)Σ_{χ≠χ₀}(P_aQ_s)(P_bQ_t) = F_pred + O(q^{−Aη+ε})`，X=q^A, A>2；F_pred 由 phase-11 Euler 积恒等式显式给出（= CFZ 主项）。这是"截断版 H_Ratios"，表述精确、可数值/Lean 靶向。
3. **系数 mod q 的均匀性（Lead 本 phase 的重写）**：`E^{(X)} = (q−1)(D+W) − S_cS_d + T`（精确，[证明]，数值验证 1e-16）。因 `E^{(X)}≈R_q≈M_q≈(q−1)Z_q`，需 `Δ := (q−1)W − S_cS_d + T ≪ q^{1−cη}`。若系数 c_A 在 mod q 的 residue 类中"完美均匀"（W≈S_cS_d/q, T≈2S_cS_d/q），则 Δ≈S_cS_d/q 小。**c>2 ⟺ 系数序列 c_A（= ζ(a+w)/ζ(c+w)-型 Dirichlet 级数的截断系数×μ 权）模 q 的均匀性达到 q^{−cη} 精度。** 这是 H_wrap 的"数论内容"版本。

**已知工具差距（kernel-theorist §8 逐条）**：BV（单模无 saving）、Chowla/MRT/Tao–Teräväinen（对数/几乎所有尺度）、additive divisor（无 q-一致、无 μ 权）、Sawin（函数域，ℤ 无对应）、大筛（只给 L²=O(1)，主项也是 O(1)）。**所需一致 power saving 无现有工具。**

---

## 4. 数值现状（真值 vs 方法 vs 墙）

### 4.1 Ratios 真值：巨大余量（支持 H_Ratios 为真）
- **移位区域构型**（四者 Re=1/2+η；spectral-numerics `phase12/numerics/truth_run2.log`，q≤5×10⁵）：`RMS|E−M|/√q` 随 η 增大而下降：η=0.1 时 5.4–10.7；η=0.05 时 20–42；η=0.02 时 37–157；而 M_q 的主项标度 ~q/η²。⇒ 数据与"**相对误差 q^{−1/2+o(1)}、与 η 无关的指数 saving、仅常数 η^{−C} blow-up**"自洽 — 即 **Ratios 真值远强于任何截断方法**（真值 saving 1/2 vs 方法 c≤1/2×η→0）。
- phase-11 已测：H_Ratios 原构型（分子临界线）误差指数 α≈0.53–0.56（所有导体类，修正 A_q 后），T 依赖多项式，signed mean≈0。

### 4.2 墙的实测
- **Lead（q=1009, η=0.2，`phase12/theory/checkE5.py`）**：A=0.5→1.1 时 |Δ|=15→175，目标 q^{1−ηA}=507→220（Δ 仍低于目标但增长 ~X^{0.67}）；|R−E| 衰减 ~X^{−0.5}（远快于 qX^{−η}）⇒ **截断误差不是瓶颈，瓶颈是 Δ（wrap 净量）**。
- **heat-kernel-critic（真实系数，独立代码，`phase12/numerics/`）**：W 比"平凡 X²/q"小 4–5 个数量级（μ 符号大量抵消）；A=2 时（q=53）|W|~12–78、(q−1)W~O(10³)，而目标 q^{1−ηA}=O(10) ⇒ 若 Δ 无额外抵消，A=2 时不够；Δ 的直接测量是决定性实验（进行中，见 wrap.md）。
- **kernel-theorist 模型探针**：Fourier 涨落 `F=(1/q)Σ_{h≠0}ĉ\bar d̂`=O(1)–O(10) 且不随 q/X 衰减 ⇒ 没有 c>2 所需的 `|F|≤q^{−Aη}` 的任何数值迹象（但模型系数，需真实 L 值复核）。

### 4.3 Kloosterman/FE 折叠探针（否定性）
|S1|=|Σ c_A \bar d_B e(BĀ/q)|/L1 ≈ c/q^{0.85–1}，无额外 √-级节省，且 |S1| 比 W 大 6–150 倍 ⇒ 该折叠形式不解决问题。

---

## 5. 文献定位（本 phase 新查证）

- **GWX arXiv:2611.18825**（2026-11-13，v1）是唯一已知"GRH + Ratios ⇒ 四个 Landau 问题"的完整条件链；**OpenAlex 引用 0**。
- **Lee arXiv:2610.32672v2** 只证**固定偶差 prime pairs**（HL 渐近），**不覆盖 Goldbach**；其假设是**移位区域、有限积分 2/2 ζ-ratios**（Conrey–Snaith），saving/shift 比 ≥2.5（最不利端）——**说明 c>2 比文献中标准移位区域 Ratios 假设更"温和"**（但仍是未证假设）。
- **Ratios 2024–26**：over ℚ，Dirichlet **1/1** 只有 GRH-条件、受限 shift、实特征等特殊结果（Čech 2024 Trans. AMS 377；Gao–Zhao）；**2/2 over ℚ 仍只有猜想**（WX25 素数模 Conjecture 2.1 未证）。Baluyot–Čech 2025 是 multiple Dirichlet series 启发式。**函数域**：Bui–Florea–Keating（Trans. AMS 376 (2023)）证 quadratic Dirichlet 的 1/1 与 **2/2（分母 shift Re>g^{−1/4+ε}）**——"移位区域 2/2 可证"的最强已有证据（但在函数域、特殊族）。
- **"GRH+X⇒完整二元 Goldbach"只有两条已知路线**：GWX（GRH + RC_D）与 Li–Liu（GRH + 谱假设 S/R，ad hoc）。**无已知"GRH+严格更弱假设⇒Goldbach"定理**。弱假设只到 almost-all：quasi-RH ⇒ E(N)≪N^{1/2}(log)¹⁰⁰；GRH 单独 E(x)≪x^{1/2+ε}（Hardy–Littlewood 1924！**MV1975 的结果是无条件的 E(X)≪X^{1−δ}**，本 phase 纠正了旧误记）；EH/BV/BFI 只到 1+2/1+1.9/1+1.4（parity barrier）；Chowla/Sarnak 无已知蕴含。
- Alpöge 声明后（2026-11-20+）：**无新 Goldbach/RH→Goldbach 预印本**。

---

## 6. Alpöge 证明方法再挖掘：无额外机器（proof-digest task-49）

- 定量层 = **经典无条件解析数论的形式化**（Siegel 下界、Siegel–Walfisz、ZFR、显式公式、零点计数、零密度盒、大筛、特征和矩、GL(2) Rankin 均方），**没有一项比 GRH 直接推论更强**（GRH 下多数被超越或 vacuous；ZeroDensityBox 在 GRH 下 vacuous）。
- **重要 axiom/接口警示**：`ExplZeta`/`ExplChi` 只有 def、无证明项；`SiegelWalfiszAP`、`PrimeShareSW`、`ZeroDensityBound`、`CharOrtho`、`ParsevalHolder` 未找到证明项（接口/假设级）。已证：siegelLower、siegelWalfisz、zFRDirichlet、zeroFreeRegion、repulsion、log-free 零密度、logDerOne_holds、zeroCount_holds、zero_density_box、显式常数大筛、M4。
- 三次"升级为 Ratios/family 均方"的尝试全部否决；唯一可做的是 Lean 工程性复用。
- [推断] 经典解析链可能不在最终证明项的依赖路径上（`HostExOfPublished` 唯一 importer 非主链；`ThinChoiceOfZeroDensity:30` 显式忽略全部解析参数）——需完整依赖追踪定论。**对 RAT(c)/wrap 无任何新数学输入。**

---

## 7. Lean 机器验证产物（lean-feasibility task-54）

`phase12/lean/nowrap.lean`（197 行）+ `wrap.lean`（158 行）：**EXIT 0、无 sorry、公理仅 propext/Classical.choice/Quot.sound**。
- no-wrap 正交性：`Σ_{χ≠1}χ(A)\barχ(B) = φ(q)[A=B] − 1`（q 素即 (q−1)[A=B]−1）；primitive 版同一恒等式（Mathlib v4.36 已有 IsPrimitive API）。
- wrap 计数恒等式：`Σ_{A≡B,A≠B}c_Ad_B = Σ_r C_rD_r − Σ_Ac_Ad_A`；`A%q=B%q ↔ q | (A−B)`（residue 形式 ↔ kq 差集形式的桥）。
- 这些是有限组合恒等式（可审计骨架），**本身不证明 H_Ratios/c>2**；完整 2-vs-2 二重和 W 未形式化（1–2 人日）。

---

## 8. "离终点多远"——精确度量

| 对象 | 状态 |
|---|---|
| Alpöge/Claude GRH | 已声明；官方 Lean 验证 11-22 04:35 UTC 版：**余 2 项**（Lean default+paranoid kernel replay / lake comparator 主证明+组合算术导出）；沙盒独立 rebuild/导出逐字节一致、con-ron --compare 已通过；无 peer review |
| GWX 归约 | [审计通过] 唯一缺口 = Ratios 型假设 |
| Ratios 真值 | [数值] 强支持：相对误差 q^{−1/2+o(1)}、指数 saving 与 η 无关（常数 blow-up）；所有导体类 α≈0.53–0.56；无 ramified 异常（A_q mask bug 已修正） |
| 可证范围 | c≤1/2（截断法完全刻画；wrap 平凡计数不改进）；Phase-11 移位区域弱 Ratios（saving<η/2，[推导]） |
| 目标 | c>2（RAT_sym/der）；等价于 TL(A>2) / H_wrap / 系数模 q 均匀性 |
| 差距 | 常数因子 ≥4（saving/distance 比：1/2 vs >2）；实质 = **level-aspect 2/2 Ratios 的 power saving**（over ℚ 完全未证） |
| 文献中是否已有 | 无（over ℚ 2/2 只有猜想；函数域特殊族有 BFK；1/1 有 GRH-条件受限结果） |
| 新工具是否出现 | 无（Alpöge 方法不提供；无新预印本） |

## 9. 下一步（若继续）

1. **H_wrap/TL(A>2) 的最小特殊情形**：q 素、|Im|≤1、单一 shift k、光滑权——作为难度标尺；若连这个都不可证，则问题等价于已知未解问题。
2. **函数域 ↔ ℚ 的精确对照**：BFK 的 negative-moment 方法在函数域给移位区域 2/2；明确其在 ℚ 上失败于哪一步（可能是"无 Weil 型求和公式"或"shift 不能 →0"）。
3. **Ratios 的量化率版本（H_UNIF）**：若只求 Goldbach 定性，是否可用 ω(q)log q→∞ 的更弱假设（GWX 未形式化）；liu-auditor 判断：需要 uniform positive power saving 或定量 rate，但均未证。
4. **官方验证跟踪**：若 paranoid/comparator 完成，GRH 部分将闭合；Goldbach 状态不变（仍缺 Ratios）。
5. **真实价值路径**：把 phase-11/12 的正面结果（移位区域弱 Ratios、Euler 积恒等式、精确恒等式 E^{(X)}=(q−1)(D+W)−S_cS_d+T、TL(A) 表述）整理成短文/技术报告；把有限恒等式与 Lean 产物作为可审计资产。

---

## 文件索引
- 框架：`phase12/0-plan.md`
- 审计：`phase12/audit/theorem-A.md`（liu）、`phase12/audit/route-c-final-audit.md`（liu，进行中）
- 理论：`phase12/theory/wrap-attack.md`（kernel）、`phase12/theory/checkE*.py`（Lead 数值）
- 数值：`phase12/numerics/truth_run2.log` 等（spectral）、`phase12/numerics/wrap.md`（heat-kernel，进行中）
- 文献：`phase12/lit/conditional-routes.md`（goldbach-researcher）、`phase12/lit/alpoge-method.md`（proof-digest）、`phase12/lit/pair-correlation-goldbach.md`（进行中）
- Lean：`phase12/lean/nowrap.lean`、`wrap.lean`、`report.md`、日志
- 状态：`phase12/status/verification.md`（进行中）
