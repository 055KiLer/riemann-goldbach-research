# Phase-5 Lead 笔记：Li–Liu 的 Hypothesis R 处于"pre-asymptotic 失败"还是"渐近为真"？

> 2026-11-21。承接 phase-4（`phase4/0-phase4-报告.md`）。本文件是 Lead 的过程笔记，最终综合报告见 `phase5/0-phase5-报告.md`。
> 标注：**[事实]**（论文原文/我们已核验的数值）、**[推导]**、**[推测]**。

---

## 0. 变量约定（重要，防止内部数字对不上）

- $\delta_N=\sqrt{S(N)/N}\,(\log N)^{3/2}$，$S(N)=2C_2\prod_{p\mid N,p>2}\frac{p-1}{p-2}$（LL (1.5),(2.12)）。
- $T_N$ = LL (2.17) 的边界核算子；Hypothesis R(N) ⇔ $\|T_N\|\le\delta_N$（LL Thm 6.1；**[事实]**，我们已复核原文）。
- 有限模型 $C$（LL Appendix B, 2562 nodes 等）的
  - $Y:=\lambda_{\max}\sqrt N$，
  - $C^{\rm sc}:=\lambda_{\max}\sqrt N/\sqrt{S(N)}=Y/\sqrt S$，
  - ratio $:=\lambda_{\max}/\delta_N=C^{\rm sc}/(\log N)^{3/2}$。
- 对 $N=2p$ 族：$\sqrt{S}=1.14908$；故 $Y\approx 1.149\,C^{\rm sc}$。

已确认的细模型数值（H=40, mesh 1/16，除标注；来自 phase-4 cache）：

| N | 结构 | S(N) | δ_N | λ_max | ratio | Y=λ√N | C^sc |
|---|---|---|---|---|---|---|---|
| 30030 | 2·3·5·7·11·13 | 5.1213 | 0.43231 | 0.357462 | 0.82686 | 61.95 | 27.35 |
| 39994 | 2·19997 | 1.32039 | 0.19820 | 0.212506 | 1.07220 | 42.50 | 36.98 |
| 40022 | 2·20011 | 1.32039 | 0.19815 | 0.275721 | 1.39152 | 55.16 | 48.00 |
| 60022 | 2·30011 | 1.32037 | 0.17117 | 0.207252 | 1.21079 | 50.78 | 44.19 |
| 100042 | 2·50021 | 1.32035 | 0.14192 | 0.166061 | 1.17007 | 52.52 | 45.71 |
| 200006 | 2·100003 (H=20) | 1.32034 | 0.10957 | 0.124657 | 1.13771 | 55.75 | 48.52 |

（H=20 对 200006 略低估 λ；H=40/60/80 在 N=40022 给 1.3915/1.3959/1.3979，外推 H→∞ 约 1.399–1.400。）

---

## 1. Phase-4 结论的修正（must-correct）

Phase-4 报告写了"R 在论文自己声明的范围（N>e¹⁰）内很可能为假"。**此说法过度解读了论文**，需要修正为：

1. **[事实]** LL 主文 Hypothesis R 的措辞是 "For every **sufficiently large** even N …"，$N_0$ **未量化**；Appendix A（p.54）明确 "The eventual hypotheses assert these conditions for all sufficiently large even N …, with lower bounds $N_0(c)$ and $N_0(c,h_c)$ on N." 因此 $N_0\sim 10^6$ 与论文逻辑**不冲突**。
2. **[事实]** "N>e¹⁰" 只是构造的技术门槛（strip 非空、$N^{2\alpha_N}=e^2$、$Q_N\ll 1$ 等），不是"R 的验证范围"；论文从未声称 N>e¹⁰ 时 R 成立。
3. **[事实]** Appendix B（p.62）自己写："Cutoff stability and pointwise high-precision checks do not bound the full operator's truncation or discretization error. … they **do not certify Hypothesis R** for T_{30030,1}."
4. 因此正确的陈述是：
   - 有限模型（在 mesh/height 收敛意义下）在 $N=40022$ 给出 ratio=1.3915>1，且在 $N=2p$ 族 $p=20011,30011,50021,100003$ 上 ratio 均 >1（到 N=2×10⁵）；
   - 这是 **pre-asymptotic 失败**（若 $N_0$ 很大，不与定理矛盾），不是对 R 的否证；
   - phase-4 的"λ_max 近似与模数无关"是把不同分解结构的 N 混在一起的误读：多小因子 N 的 $C^{\rm sc}$ 只有 23–39，$2p$ 族约 37–49，**2p 是 S(N) 最小、对 R 最苛刻的族**。

---

## 2. 三种标度情景（本轮的判决性问题）

设 $\lambda_{\max}\approx c\,(\log N)^{a}\,N^{-1/2}$。R 渐近等价于 $c(\log N)^a\le\sqrt{S}(\log N)^{3/2}$，即 $a\le 3/2$（且常数合适）。现有 2p 五点（log N: 10.60,10.60,11.00,11.51,12.21）给：

- (A) **$C^{\rm sc}\approx$ const ≈44.7**（$a=0$）：ratio ≈ $44.7/(\log N)^{3/2}$，交叉 $\log N=44.7^{2/3}=12.6\Rightarrow N_0\approx 3\times10^5$（若取 48：$N_0\approx5.5\times10^5$）。
- (B) **$Y\approx$ const ≈54**（$a=1$）：交叉 $Y=\sqrt S(\log N)^{3/2}\Rightarrow\log N=14.3\Rightarrow N_0\approx1.6\times10^6$。
- (C) **$C^{\rm sc}\propto(\log N)^{3/2}$**（$a=3/2$）：ratio→const>1 ⇒ **R 对所有大 N 为假**，LL 路线（作为渐近定理）死。

**[数值事实]** 目前 5 点对 $Y$ 的拟合斜率 $\approx0.08$（几乎平），对 $\log^{-3/2}$ 的形状优于对 $\log^{-1/2}$；但跨度只有 15%，且 $p=19997$ 与 $p=20011$ 相邻两点 $C^{\rm sc}$ 相差 30%（算术涨落），**统计上无法区分 (A)/(B)/(C)**。区分需要 $\log N\gtrsim14$（$N\gtrsim10^6$）且误差 $\lesssim3\%$。这正是 phase-5 数值扩展的目标（N=1e6、2e6，H/mesh 收敛 + H→∞ 外推）。

**[推导] 理论上如何判断 $a$**：$E_N=P_N-(D_N+K_N)$ 的逐点大小来自 φ(N)≈N 个特征标项的平均涨落（见 §3），其 log 幂由跨特征标 L'/L 的 2 点/4 点相关决定，而不是由零对密度单独决定。若 $(1/\phi)\sum_\chi|g_\chi|^4\asymp(\log N)^A$，则 $\lambda\sim N^{-1/2}(\log N)^{A/2-\text{corr}}$，R 的成败归结为 $A$ 与 3 的精确比较。这是**可攻击的空白**。

---

## 3. 理论框架（与本轮数值一致的分解）

记 $n=\phi(N)/2$（odd 特征标个数；$N=2p$ 时 $n=(p-1)/2$）。在 $L^2(\Gamma_N,|ds|)$ 上定义 $F_\chi=g_\chi/(1+s)$，则

$$P_{\rm op}=\frac1n\sum_{\chi\ \rm odd}|F_\chi\rangle\langle F_\chi|,\qquad E_{\rm op}=P_{\rm op}-M_{\rm op},\quad M_{\rm op}=\text{kernel }(D_N+K_N).$$

**[事实]** 这是样本协方差（$n\approx N/2$ 个"样本"）减去模型协方差；$P_{\rm op}$ 与 $M_{\rm op}$ 各自很大（点值 ~20=O((log N)^2 量级)，HS 范数 ≍(log N)^{3/2}），但**差** $T_N$ 小得多（λ~0.1–0.35）。

**[推导] 样本协方差启发式**：若 $\{F_\chi\}$ 弱相关，$\|E_{\rm op}\|_{\rm HS}^2\approx(1/n)\mathbb E\|\,|F\rangle\langle F|-M\|^2$，因此
$$\|E\|_{\rm HS}\approx \sqrt{2/\phi}\;\rho_N,\qquad \rho_N^2:=\mathbb E_\chi\|\,|F_\chi\rangle\langle F_\chi|-M\|^2 .$$
有限模型粗测（probe4，H=8,m=2）：$\|P\|\approx\|M\|\approx$ 数倍于 $\|E\|$，$\|E\|_{\rm HS}$ 约 0.6–0.9（30030/40022），即 HS/δ≈1.9–2.9——**HS 路线不足以证明 R**（论文 Theorem 6.2 的 (log N)² 也同一量级），必须用算子范数（谱的最上端）。

**[推导] per-character 分解**（kernel-theorist 提出）：$E_N=(2/\phi)\sum_\chi T_\chi$，$T_\chi=|f_\chi\rangle\langle f_\chi|-\frac12(D_N+K_N)$ 或等价中心化。若 $\{T_\chi\}$ 弱相关，则 $\|E_N\|\lesssim(2/\sqrt\phi)\,\rho_N$，R 归结为
$$\rho_N\lesssim \tfrac{\sqrt S}{2}(\log N)^{3/2}.$$
论文的三角/HS 法只能给 $\rho_N\lesssim(\log N)^2$（差一个 $\log^{1/2}$）。**"R 真/假"就卡在这半个 log 幂上**——这是本轮最精确的困难重述。[见 kernel-theorist 报告 phase5/theory/scaling-theory.md]

**[推测] 为什么可能 $a\le1$**：$g_\chi$ 的竖直振荡/零点平均使跨 χ 相关在 L² 意义下比逐点界好 $(\log N)^{1/2}$；若 Alfeld/大筛型"族 pair correlation"成立，则 $A=3$ 恰在边界上，需常数计算。当前无证明。

---

## 4. H 截断（高度）与数值解释的方向性

- **[事实]** transfer 论证（LL Prop 5.3：$\widetilde T_N=T_N\oplus 0$）给出：任意 $L^2(\Gamma_N)$ 单位向量上的 Rayleigh 商 $\le\|T_N\|$。因此固定 mesh、增大 H **只增不减**，且永远 ≤ 真值。
- **[事实]** 所以 phase-4 的 "N=40022 时 $\|T_N\|>\delta_N$"（有限模型+求积收敛）在**下限方向**是可靠的（H=40→80 还升 0.3%）；但**不能**由此推出 $H=\infty$ 时仍 ≤δ_N。
- **[风险]** phase-5 的"$C^{\rm sc}\approx$const ⇒ R 渐近真"需要 **H→∞ 的上界方向**，transfer 给不了；固定 H 若随 N 增大系统性低估 λ（高 |Im s| 模式权重随 N 上升），"平"可能是伪影。heat-kernel-critic 正在跑 N=200006 的 H=20 vs H=40 与 N=400006 新点；我另跑 N=300022/400006/600014/1000166（H=20,m=8）交叉核验。

---

## 5. 本轮已确认 / 待确认

**已确认（[事实]/[数值]）**
1. 论文 N=30030 的谱数值精确复现（λ=±0.353421/0.357462，ratio 0.826864；D_N/P̃_χ/字符 FFT 独立校验）。
2. mesh m=8→64 在 N=40022 收敛（4×10⁻⁸）；H=40/60/80 单调缓升（下限方向）。
3. 有限模型在 N=40022（及 2p 族到 2×10⁵）ratio>1，H 截断只会使真值更大——**这些 N 上 R(N) 很可能确实失败**（[推测]，但下限方向强）。
4. LL 的 $N_0$ 未量化 ⇒ 有限反例不否定定理；Appendix B 自认不 certify R。
5. GRH ⇒ $E_{\rm Gold}(x)\ll x^{1/2+\varepsilon}$ 是**真定理**（2026 综述 arXiv:2607.27282 Thm 3.1；Pintz–Althöfer arXiv:2610.15559；$g(\theta)$ 公式）；若 Alpöge GRH 成立这条会变成无条件，但仍只是 almost-all Goldbach。R 本身**不被 GRH 蕴含**（LL §2.4.3）。
6. 无条件例外集 2025–26 有实质改进（Zhao 2025: $X^{7/10}$；Pintz–Althöfer 2026: 只需任一无零半平面即得 $X^{7/12+\varepsilon}$）——与 R 无关，但应写进背景。

**待确认（决定性问题）**
- Q1: N=1e6、2e6 的 ratio / $Y$ / $C^{\rm sc}$（决定 (A)/(B)/(C)）。
- Q2: 大 N 的 H 收敛（H=20/40/80）与 mesh 收敛（1/8,1/16）。
- Q3: $c\ne1$（LL Appendix A 的 $\alpha=c/\log N$）能否使 R 型不等式在更小 N 成立（liu-auditor 在跑；理论上 $c\downarrow0$ 时 norm 行为未知）。
- Q4: per-character $\rho_N$ 的数值标度（需保存 G、M 矩阵；可判断 $\log$ 幂）。
- Q5: 若 ratio 在 N~1e6 下穿 1，能否做**可信但严格**的下界/上界证书（区间算术 + 截断误差）？——目前看代价高、意义有限（不否定"eventually"命题），暂不做。

---

## 6. 对 LL 路线与 Goldbach 的意义

- 若最终 (A)/(B)：LL 的条件性定理**不真空**（R 可能真，只是 $N_0$ 远大于 e¹⁰），但证明 R 需要全新思想：跨特征标 L'/L 的算子范数型（族 pair correlation）估计；现有 2026 技术不够（goldbach-researcher 核查）。
- 若最终 (C)：LL 的 R 渐近为假 ⇒ Theorem 1.2 假设不可满足、定理空虚；其精确恒等式仍是有效框架，但 Goldbach 的最小未知退回 H_Gold 本身。
- 无论哪种：**本轮没有 Goldbach 证明**；但把"LL 路线可行性"从 phase-4 的"很可能死"修正为"取决于一个具体的 log 幂问题，且数值上更接近'渐近可能为真'"。这是诚实的进展方向。

---

## 7. 下一步（本轮内）

1. spectral-numerics：N=1e6/2e6 的比值 + H/mesh 收敛 + HS/谱/特征向量分布。
2. heat-kernel-critic：对抗审计（高度耦合、独立重算、逻辑方向）。
3. kernel-theorist：per-character 分解严格化 + 把 R 归约为具体 4 点相关估计 + 尝试任何 (log N)^{3/2} 型界。
4. liu-auditor：论文量词/Appendix A-B 审计 + level-aspect 文献 + c≠1 数值。
5. goldbach-researcher：文献与 2026 动态（已完成大部分）。
6. lean-feasibility：transfer 引理与 R-推断链的 Lean 化（可选，低优先）。
7. Lead：汇总 `phase5/0-phase5-报告.md` + 修正 phase-4 报告文件头的警告。
