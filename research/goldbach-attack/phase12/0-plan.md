# Phase-12 计划：从"缺 H_Ratios"到"精确常数追逐 c>2"——Goldbach 的最后 4 倍指数缺口

> Lead，2026-11-22（phase-12 启动）。本文件是 phase-12 的作战框架与数学总览；所有 teammate 先读本文再动手。
> 标注：[证明]/[推导]/[数值]/[推测]。**不造假、不夸大。**

---

## 0. 当前状态（phase-11 结束时的确定结论）

- 唯一已知归约链：**Goldbach ⇐ Alpöge/Claude 的 GRH（已声明，官方 Lean 验证接近完成）+ GWX 的 H_Ratios**（Gou–Wang–Xu, arXiv:2611.18825, Hypothesis 1.1；复合导体、2/2、临界线分子、saving 与 η 无关）。
- 官方验证最新（实抓 2026-11-22 11:29 UTC，页面 2026-11-22 04:35 UTC 版）：新增"沙盒独立 lake build 逐字节复现导出"与 con-ron --compare 通过；**仍余 2 项 running**：Lean default+paranoid kernel replay（61.5 GB 导出，单线程）、lake comparator（主证明 + 组合算术导出）。
- phase-11 已确立：
  1. Route C（截断 Möbius + 精确正交性）在 GWX 窗内**结构性不可能**（Prop 3.1：`ω/η<1/2` vs 需要 `>16`），唯一缺口 = **H_wrap**（parity barrier 边界）。
  2. **移位区域（Re=1/2+η）弱 Ratios 可证**：误差 `q^{1−ω}`，`ω<η/2`（Lead 的 §1 推导，Euler 积恒等式数值验证）。
  3. H_Ratios 数值支持（修正 A_q mask bug 后）：所有导体类 RMS|E−M|≈q^{1/2+o(1)}，ω_D≈1/2；"ramified 异常"已撤销。

## 1. 本 phase 的**核心新发现**：把缺口精确化为常数 c>2

### 1.1 GWX 到底需要什么（重读原文后的精确化）

- **Hypothesis 1.1 (RCD(ω_D))**：`Σ*_{χ mod q} L(a,χ)L(b,χ)/(L(s,χ)L(t,χ)) = M_q(a,b;s,t) + O(q^{1−ω_D+ε}(1+T)^B)`，uniform：**ℜa=ℜb=1/2（分子恰在临界线）**，**ℜs=ℜt=1/2+η**，`T≤100 log(2q)`，**ω_D 与 η 无关**。
- 证明路线：§3.6 三点插值（从临界线分子插到半径 r 的分子圆盘，ℜξ=1/8 的平凡界 q² 给出损失 `8(η+r)(2+ω_D)`）→ Lemma 3.1：(3.2) 误差 `q^{1−ω+ε}`，`ω = ω_D − 8(η+r)(2+ω_D)`；再由 (3.12) 得 Goldbach 误差 `N^{1−ω+2η+ε}`。
- ⇒ GWX 要求 `ω > 2η`，而插值损失要求 `η < ω_D/16`（ω_D 固定）——这就是"需要与 η 无关的 saving"的来源，也是 phase-11 说"差 ≥4 倍指数"的出处。

### 1.2 **关键观察（本 phase 的杠杆）**：绕过插值

**如果我们能直接证明 (3.2) 在"分子距离 ≈ η、分母距离 η"的构型**（即 phase-11 移位区域弱 Ratios 的加强版，带第二主项 H_q Z_q(1−b,1−a)），则 §3.2–§3.5 **不需要** §3.6 的插值——因为 §3.6 的唯一作用就是从 Hyp 1.1 造出 (3.2)。此时**唯一要求变成 `ω > 2η`**。

**定义 RAT(c)**：存在常数 c>0，使得对每个足够小的固定 η>0、所有 q>1、所有 `|Im|≤100log(2q)`、分子在 `|ℜa,b −(1/2+η)|≤r`（r=η/8）、分母 `ℜs=ℜt=1/2+η`：
```
R_q(a,b;s,t) = φ*(q)Z_q(a,b;s,t) + H_q(a,b)Z_q(1−b,1−a;s,t) + O(q^{1−cη+ε}(1+T)^B).
```
**定理 A（待 liu-auditor 严格化）**：GRH + RAT(c)，c>2 ⇒ 二元 Goldbach（误差 `N^{1−(c−2)η+ε}`；取 η 固定小即得真正的幂次节省）。

### 1.3 截断方法能到多少？——phase-11 只给了 c=1/2，实际可到 c≈1

phase-11 §1 的构造（混合宇称分子 `L(a,χ)L(b,χ̄)`，四段截断 X，X²<q 严格 no-wrap）：误差 `q^{1+ε}X^{−η}`，`ω=η log X/log q`，`X²<q ⇒ c=1/2`。

**本 phase 的改进（待严格化）**：若允许 wrap（A≡B mod q, A≠B）但用**平凡计数**估计它，可得 c→1：
- wrap 平凡界：`W ≪ X²/q · η^{−O(1)}(log)^{O(1)}`（对固定 k，`Σ_{n,m≤X} d(A)d(A−kq)A^{−2σ}` 的估计）；
- 账本：`q^{1+ε}X^{−η} + X²/q ≤ q^{1−ω}`，`ω=ηA`（`X=q^A`）⇒ `A ≤ 1/(1+η/2)` ⇒ **c≈1**。
但仍 <2。**要 c>2 必须 `X>q²`，此时 wrap 平凡界 `q^{2A−1}` 距目标 `q^{1−ηA}` 差 power `~q^{2A−1−(1−ηA)}`（A=2 时差 q²）** ⇒ 这就是 H_wrap/parity barrier 的**定量形式**：
```
c>2  ⟺  存在 A>2 使   Σ_{1≤|k|≤X²/q} Σ_{nm−rl=kq} c(n,m)\overline{d(r,l)}  ≪  q^{1−ηA+ε}.
```
（现在不是"要不要 saving"，而是"要 saving q^{2A−2+ηA−ε}"。）

### 1.4 可能的突破口（本 phase 要逐个试）

1. **Gauss 和展开/FE 折叠**：GWX 的 R_q 是"双 χ 分子"。用 FE 把一个分子翻转：`L(b,χ)=ε(χ)X_q(b)L(1−b,χ̄)`（b 在临界线上，1−b 也在临界线）。展开 `τ(χ)=Σ_u χ(u)e(u/q)` 后，χ-正交性给出 `A≡B mod q` 再被 `Σ_u e(u/q)` 化为 **Kloosterman 相位 `e(B \bar A/q)`** ⇒ 可能把 H_wrap 变成"双线性 Kloosterman/Voronoi 型"和，从而有额外 √ 节省。**这是本 phase 最值得试的技术路线。**
2. **模 q 的 Poisson 求和 + 乘法结构**：`Σ_{A≡B mod q} c_A d_B` 的乘法（nm≡rl）结构，`(n/r)≡(l/m)`；对 q 素可用 `Σ_{x mod q} e(hx/q)`、Weil/Kloosterman 界。
3. **长度不对称**：四个截断长度 N₁,N₂,M₁,M₂ 独立 + 不同分子距离 ⇒ 优化常数（可能把 c 从 1 推到 ~4/3？待算）。
4. **定性版本（Appendix A 路线）**：GWX 明确指出 Goldbach 的"character argument continues to use a positive power saving"（只有 prime pairs/quadratic 可用定性误差）。若走 `η~1/log N` 路线，需要 saving `≫1/log N`（即 c→∞ 缓慢），比 c>2 更弱/更强？——liu-auditor 判定。
5. **H_Ratios 的结构性替代**：是否存在比 RAT(c>2) 更弱、但足以完成 §3.2–§3.5 的输入（如只在 u=v=0 的导数层、或只对 q|N、或只对光滑权重积分形式）？——liu-auditor。

## 2. 任务分工（phase-12）

| 任务 | 负责人 | 交付 |
|---|---|---|
| task-50 状态刷新（官方验证 11-22 04:35 UTC 版；上游/arXiv/新闻） | repo-verifier | `phase12/status/verification.md` |
| task-51 Alpöge 证明方法再挖掘：除 GRH 外是否给出可用于 Ratios 的新量化机器（SiegelLower/SiegelWalfisz/ZFR/ZeroDensityBox/GL3MeanSquares 的性质与强度） | proof-digest | `phase12/lit/alpoge-method.md` |
| task-52 文献：SeungJu Lee 2610.32672v2 的精确内容/假设；"GRH+X⇒Goldbach"已知条件路线；Ratios 近年进展；函数域 | goldbach-researcher | `phase12/lit/conditional-routes.md` |
| task-53 审计定理 A（不含插值；c 的精确阈值）；判定 §1.3 的 c≈1 账本；判定 §1.4(5) 的最弱输入 | liu-auditor | `phase12/audit/theorem-A.md` |
| task-54 数值：wrap 和 W 的真实尺度（模型系数、q 素、X=q^A）：是否比平凡界小？Kloosterman 折叠后的数值探针 | heat-kernel-critic | `phase12/numerics/wrap.md` |
| task-55 数值：Ratios 真值（Hyp 1.1 构型：临界线分子、分母 1/2+η）的 η-依赖与误差指数；移位区域定理常数 c 的数值确认 | spectral-numerics | `phase12/numerics/ratios-truth.md` |
| task-56 Lean：有限 no-wrap 正交性/计数引理的机器验证（q 素、A,B<q 情形 + 两类指标安排） | lean-feasibility | `phase12/lean/nowrap.lean` + report |
| task-57 理论主攻：wrap 和 W 的新估计（Gauss 和折叠/Kloosterman、Poisson、乘法结构、长度不对称）；若失败给出精确不可行性 | kernel-theorist | `phase12/theory/wrap-attack.md` |

## 3. 纪律

- 每个结论标 [证明]/[推导]/[数值]/[推测]；不把数值当证明；不发明定理。
- 引用必须给文件/行号；外部文献给 arXiv 号。
- 目标不是"造一个证明"，而是：**把 Goldbach 缺口精确化 + 尽可能缩小 + 找到任何可验证的新结论（最好 Lean 可查）**。
