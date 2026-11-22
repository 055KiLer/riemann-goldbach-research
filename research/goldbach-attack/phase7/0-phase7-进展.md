# Phase-7 进展笔记（R 渐近方向的判定 + 替代路线的发现）

> 2026-11-21 20:50。承接 phase-6（`phase6/0-phase6-报告.md`）。
> 标签：[证明]/[推导]/[数值]/[事实]/[推测]/[预印本]。

---

## 1. 理论判定：R 渐近为假（在 H_cov^low 下）——task-29

kernel-theorist 给出（`phase7/theory/kappa-law.md`）：

**推导链**：
1. `‖Q_N‖≍c_Q logN`（phase-6 定理 7.1/7.2，b=1）。
2. 新命题（**常数经 Lead 修正**）：`trQ_N=(π/4)(logN)²+O((logN)^{1.7})`。
   - **Lead 的 character-free 数值（`phase6/lead/qdiag.log`）**：`D_N(2α)/(logN)² = 0.2392 (logN=10.6) → 0.2488 (37.5) → 1/4` ✓；
   - **`K_N(α,α)` 为负**：−6.315 → −55.47，拟合 ≈ −0.115(logN)^{1.7}（不是 +(logN)²/4）；
   - `Q_N(2α)/(logN)² → 1/4`；`trQ/(logN)² = 0.842 → 0.670 → π/4≈0.785`（非单调，β 线常数项先衰减、α 线系数后缓升）。
   - ⇒ **trQ=(π/4)(logN)²+O((logN)^{1.7})**（原稿 (π/2) 系将 K 双重计入，已修正）。
3. 有效秩：`r_eff=trQ/‖Q‖≈(π/4)/(1.17)·logN≈0.67logN`。
4. 样本协方差律：`λmax(E_N)≈√(‖Q_N‖trQ_N/n)` ⇒ `κ≈c√r_eff≈0.82c√logN`（上界 Koltchinskii–Lounici 型；下界需 H_cov^low）。
5. 数据标定：κ(6e7, raw)=2.50 对应 c≈0.72（1e7 的 κ≈2.1 对应 c≈0.69，单调性由 r_eff 的次阶项解释）。

**修正后（kernel-theorist 确认，2026-11-21 20:55）**：`trQ=(π/4)(logN)²+O((logN)^{1.7})`、`r_eff≈0.671logN`、`κ=0.819c√logN`；farN κ(17.9)=2.5 定 c≈0.72；`ratio_∞=2c√(αβ)/√S≈1.668c≈**1.20**`（c=0.69–0.75 ⇒ **1.15–1.25>1，裕度约 20%**）。Prop 1.1 原 π/2 的错误原因已澄清：K_N 的双极点与 D_N 精确抵消后只剩低阶负项（S(N)c_N=1），实际 K_N(α,α)≈−0.115(logN)^{1.7}。

`ratio→2c√(αβ)/√S =: ratio_∞`（α=0.671, β≈1.17）⇒ **ratio_∞≈1.668c≈1.20（1.15–1.25）>1（常数）** ⇒ **R 渐近为假**；与 farN 数据（ratio 在 logN 15.2→17.9 不降反升；全局 a=1.48±0.13；大 N 子集 a=1.91±0.22 的 1σ 含 3/2）一致。
**唯一两分法**：若 H_cov^low（逐方向四阶矩下界 + 跨 χ 弱混合）成立 ⇒ κ 下界 ∝√logN ⇒ **R 对充分大 N 失败**（条件定理 3.1）；若 H_cov^low 为假（零点刚性/负相关）⇒ κ 有界 ⇒ ratio→0、R 渐近真。[推测] 随机矩阵普适性一侧（R 假）更可能。
**H_cov^low 的来源** = level-aspect 零点四点的**定量下界**（2-级/4-点相关、跨 χ 独立性），远超出 Iwaniec–Luo–Sarnak 型受限检验函数结果 —— 这是 settle R 的唯一未证算术输入。

---

## 2. 替代路线的发现：GRH + Ratios Conjecture ⇒ Goldbach（Gou–Wang–Xu）——task-30 早期

goldbach-researcher（`phase7/lit/alternative-routes.md` 撰写中）发现一条**不依赖 R/pair correlation 的完整条件性路线**：

**[预印本·未评审] Gou–Wang–Xu, arXiv:2611.18825（2026-11-13）Theorem 1.1（Goldbach）**：假设 GRH（Dirichlet L）+ 本原 Dirichlet L 族的 **Ratios Conjecture** `RC_D(ω_D)`（0<ω_D≤1/2）⇒ 对每个偶数 N、每个 ε>0：
  `Σ_{m+n=N}Λ(m)Λ(n) = N·𝔖(N) + O_ε(N^{1−ω_D+ε})`。
取 ω_D=1/2 得误差 O(N^{1/2+ε}) < 主项 ⇒ **所有充分大偶数 N 都是两素数之和**。
**这与 phase-4/5 的 H_Gold 是同一量级目标**（加权二元 HL），但 G-W-X 从 Ratios 一侧给出 ⇒ 若 Alpöge GRH 成立，**Goldbach 只差 Ratios Conjecture 的一个 power-saving 版本**！

**函数域版本 [预印本]**：同文 Theorem 1.5 对固定奇素数幂 q>10^200、任意首一 N（deg≥3）**无条件**：`Σ_{F∈M_{d−1}}Λ(F)Λ(N−F)=q^{d−1}𝔖_q(N)+O_q(q^{23d/24})`。
机制 = (I) Sawin–Shusterman Type I/II 因子分解：平方自由 AP 中素数分布水平 >1/2（Sawin, Acta Math. 233 (2024)）；(II) 两点 Möbius 相关用 cohomological sieve（Betti 数界 Wan–Zhang、Das–Howe 代数筛、判别式上同调、twisted Chowla）。
**到 ℤ 的精确障碍** = (I) ℤ 上平方自由模的分布水平 >1/2 属 Elliott–Halberstam 型开放问题（BFI 1986 只到 4/7 特殊模）；(II) ℤ 上两点 Möbius/Chowla 相关即 parity barrier，且 Spec ℤ 无 Frobenius/Weil 上同调、von Mangoldt 和也无函数域 factorization-function 的代数对应。

**其他非 R 路线（均不足）**：GRH+新指数和 ⇒ E(X)≪X^{1/2+ε}（almost-all，密度-1 不足以证 Goldbach——phase-6 已证）；EH+加权筛 ⇒ (1+1.4)（LL arXiv:2606.05224），到 1+1 仍被 parity barrier 挡；大筛/larger sieve 无 Goldbach 应用；加性组合覆盖多变量组态不覆盖二元 ΛΛ 相关；Hooley 型条件未见。
**Alpöge 证明的新算术推论**：MIT 页只有 Robin/Lagarias 不等式（RH 等价判据，非新定量输入）；Zenodo 阅读指南（Jaswal，DOI 10.5281/zenodo.24410057）确认核心是定性 `ZeroFreeAll`（Galois 表示/局部参数/VWin(Tate–Shafarevich)），**无显式零无区/L'/L/S(t) 定量内容** ⇒ 不能直接供 Goldbach 路线使用。

**推荐 top-2 路线（非 R）**：
(A) **Ratios Conjecture 路线**：第一步 = 证明本原 Dirichlet L 族的 `RC_D(ω_D)`（ω_D>0 的 power-saving 版，或 G-W-X Appendix A 的弱化定性版本）；函数域已有 Sawin 2024 的 harmonic-family 先例。
(B) **两点 Möbius/Chowla 路线**：第一步 = ℤ 上 power-saving 两点 Chowla/twisted Chowla 的平均版本，例如 `Σ_{h≤H}|Σ_{n≤X}μ(n)μ(n+h)|² = o(HX²)`（合适范围）；这是函数域用上同调拿到的 (II)，也是 parity barrier 的核心；现有最强是 Matomäki–Radziwiłł–Tao 的对数平均 Chowla (2015)。

---

## 3. 当前项目状态

1. **没有 Goldbach 证明**；RH/GRH 本身不推出它。
2. LL 条件性路线：其关键假设 R 在有限模型意义下持续被反证（raw 下界 ratio>1 到 N=6×10⁷），理论判定（H_cov^low 下）**R 渐近为假**（ratio→常数≈1.15–1.25>1）⇒ **LL 渐近路线很可能不可用**。
3. **最有希望的新路线**：GRH（已被 Alpöge 声称证明）+ **Ratios Conjecture（本原 Dirichlet L 族，power-saving）⇒ Goldbach**；其障碍精确对应 (I) 平方自由 AP 中素数分布水平>1/2、(II) 两点 Möbius/Chowla 相关；函数域已有完整先例（Sawin 等）。
4. 待办：task-30 完整报告；修正后的 kappa-law.md；phase-7 综合报告。

---

## 4. Gap 表（task-32 阶段结果，2026-11-21 21:00）

| Input | 已知最好 | G-W-X 需要 | Gap |
|---|---|---|---|
| **RC_D(ω_D) over ℚ** | **无任何无条件 power-saving**；条件性后果 Conrey–Snaith 2007；低阶项一致性 Bui–Keating 2006；受限族/单 shift GRH 条件 ratios Gao–Zhao 2023–24；数值 Goes et al. 2009；函数域 Sawin 2024（harmonic families, square-root cancellation） | 任意固定 ω_D>0，全导子 q（含复合），T≤100log(2q) 一致 | 已知 ω_D=0（定性 p=0）；**要 ω_D>0 = 整个猜想级别**，但只需任意小 saving；G-W-X Appendix A 的"定性弱化版"亦未证 |
| **(I) 平方自由 AP 中素数分布水平** | BV 水平 1/2（全模）；BFI 1986 水平 4/7（well-factorable 模）；Zhang 2014/Polymath8b 1/2+微小（光滑模）；2024–26 未见 >1/2 普遍改进 | >1/2；函数域实际用 Sawin 2024 Prop 8.16 的 θ=5/6 | 1/2→5/6 差 1/3；记录 4/7→5/6 差 11/42≈0.262；且 4/7 仅特殊模 |
| **(II) 两点 (twisted) Chowla** | MRT 2015：h-平均 o(H^kX)，衰减 ~loglogH/logH；Tao 2015：对数平均两点 o(logω)（"breaks parity barrier"但无 saving）；Tao–Teräväinen 2018：几乎全部尺度；无 power saving | power-saving（X^{1−δ} 或 h-平均/仿射族一致 power saving） | 已知 p=0；要求 δ>0 = **parity barrier 本身** |

**2026 相关新文**：G-W-X arXiv:2611.18825（本路线核心）；Lee arXiv:2610.32672v2（restricted uniform zeta-ratios 证 fixed even difference prime pairs 的 HL 渐近；Ratios 误差 O(U^{ϑ+ε})，1/2≤ϑ<(39−√177)/32，RH 下更强）。无其他 Dirichlet-族 ratios→Goldbach 新文。
**战略判断**：**(A) Ratios 路线最值得投入**——目标单一（CFZ 2008）、只需任意小 power saving、函数域有 Sawin 2024 模板、ℚ 上有 multiple Dirichlet series/Gao–Zhao/Lee 的活跃技术；**(B) 的 (II) 即 parity barrier**，函数域靠上同调绕过、ℤ 无对应工具，短期无路径。

---

## 5. task-32 完成后的更正与细化（2026-11-21 21:05）

1) **更正**：G-W-X Appendix A 的弱化定性版本**不能用于 Goldbach**（原文：“For prime differences and quadratic values, the power-saving ratios errors in the main theorems can be weakened if only qualitative asymptotics are required. … The character argument continues to use a positive power saving.”）⇒ 最小输入 = **RC_D(ω_D) 对某个固定 ω_D>0**；phase-7 报告中“可先证 Appendix A 弱化定性版本”的建议作废。
2) **RC_D 在 ℚ 上的精确现状**：无任何 ω_D>0 定理。最接近证据：① Goes–Jackson–Miller–Montague–Ninsuwan–Peckner–Pham 2009（arXiv:0909.4916）对 Dirichlet L（素数导子）族数值验证 ratios 预测（Fourier 支撑 (−1,1) 平方根一致；(0,−2,2) power saving 一致——1-level density，非 2/2 平均本身）；② Čech arXiv:2110.04409 / Trans. AMS 377 (2024) 9113：实 Dirichlet 特征、单 shift、受限 range、**GRH 条件**的 ratios；③ Gao–Zhao 2022–24：二次/三次/四次（Dirichlet/Hecke）族、单 shift、受限 range、GRH 条件；④ Bui–Keating 2006（arXiv:math/0607199）2k 阶矩 hybrid Euler–Hadamard 与 ratios/随机矩阵预测一致（矩层面）。函数域：Sawin, Acta Math. 233 (2024) harmonic families 平方根相消。**Gap：ω_D 已知=0，所需>0；且现有 ℚ 结果都是单 shift/特殊族/受限 range，无 2/2 一般 shift。**
3) **(I) 精确值**：函数域用 **θ=5/6**（G-W-X §7 引 Sawin [Saw24, Prop 8.16]）；ℤ 上最好 BV 1/2（全模）、BFI 1986 **4/7**（well-factorable）、Polymath8b 2014（arXiv:1402.0811）**1/2+7/300≈0.52333**（光滑平方自由+CRT）；2024–26 无一般模 >1/2 改进。Gap：4/7→5/6 差 11/42≈0.262。
4) **(II) 精确现状**：无 power-saving 两点 Chowla。MRT 2015 h-平均 o(H^kX)（~loglogH/logH）；Tao 2015 对数平均 o(logω)；Tao–Teräväinen 2018 k 点 Chowla（k 奇或 2）除对数密度 0 的尺度集；2026 ACD+26（arXiv:2608.22297）是**函数域** twisted Chowla。Gap = parity barrier。
5) **2026 相关**：G-W-X arXiv:2611.18825；Lee arXiv:2610.32672v2（restricted uniform zeta-ratios ⇒ fixed even difference prime pairs 的 HL 渐近；误差 O(U^{ϑ+ε})，1/2≤ϑ<(39−√177)/32≈0.803，RH 下 x^{ϑ−7/8+ε}）。
6) **第一步细化**：把 Čech/Gao–Zhao 的 multiple-Dirichlet-series 单 shift ratios 提升到 **2/2、restricted range（q 素、|Im|≤c log q）**，再处理 G-W-X §3.1 的 parity-twist 步骤；得到任意固定 ω_D>0 即可推出 Goldbach。**注意 Fiorilli–Miller 2011（arXiv:1111.3896）**：ratios recipe 在 1-level density 大支撑时会漏掉低阶项——引用 RC_D 时须按其精确形式（不是已被普遍验证的公式）。
