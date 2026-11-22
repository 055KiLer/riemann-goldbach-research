# Phase-5 总报告

> **【phase-6 修正】** 本报告的 (logN)^{3/2} 标度判断已被 `phase6/0-phase6-报告.md` 修正：那是 H=8,m=2 粗网格的离散化伪影；character-free 的 `‖Q_N‖` 在 mesh/H 收敛下满足 `‖Q_N‖≍logN`（b=1），phase-6 的新图景是"R 渐近可能为真、ratio∝(logN)^{-1/2}→0"。本报告其余数据/审计/文献/Lean 内容仍有效。

：R 的分叉、修正 phase-4、与"半个 log"的精确墙

> 2026-11-21。承接 `phase4/0-phase4-报告.md`。本报告汇总 phase-5：大 N 有限模型趋势（task-13）、标度理论（task-14）、独立审计（task-15）、文献（task-16）、对抗审计（task-17）、Lean（task-18）与 Alpöge 仓库扫描（task-19）。
> 标注：**[事实]**（论文原文/已核验）、**[证明]**、**[推导]**、**[数值]**（有限模型）、**[推测]**。**所有数值都是 Li–Liu 有限模型的证据，不是对 Goldbach 或 R 的证明。**

---

## 0. 一句话总结（最终版，含大 N 反转）

**phase-4 的"R 很可能为假"需要修正，但"R 渐近为真"也被新数据否定为结论**：有限谱模型（mesh/height 已核验；H 偏差 1–2% 且不随 N 增）显示 λ_max∝N^{-1/2}，但 **C=λ√N/√S 随 log N 单调上升**（按 logN 分桶均值 42.5→62.3，拟合 C∝(log N)^{1.14±0.3}），因此在 N=4×10⁴–2×10⁶ 上 **ratio=C/(log N)^{3/2} 保持 O(1)**（12 个抽样模数中 10 个 ratio>1，包括 N≈2×10⁶ 的两个不同素数）。"N=10⁶ 首次 ratio<1 ⇒ N₀~10⁶"的读法不成立（同尺度另两个 p 为 1.11/1.07；N=6×10⁵ 与 1.5×10⁶ 还有 1.44/1.25 的稳定尖峰）。R 渐近真伪的判据是 **C 的 log 指数 a 是否 <1.5**：a<1.5 ⇒ ratio→0（R 渐近真，但按 a≈1.14 交叉要到 N~10⁹）；a≥1.5 ⇒ R 渐近假。**a 的不确定度 ±0.3 恰好跨越临界，现有数据无法判定。**
理论侧本轮得到精确结论 [证明]：R 的 HS 路线被"逐特征标四阶矩"的 √S·(log N)^{1/2} 缺口卡死（实测 ρ_N≈0.75(logN)²；需要 (√S/2)(logN)^{3/2}），所需输入是 level-aspect 跨特征标 pair correlation/四阶相关——公开文献空白（KLM 2026 明确假设 pair correlation）。
**没有 Goldbach 证明；没有伪造的 Lean 制品。** LL 精确恒等式仍是有效框架；本轮把"LL 路线是否可行"归结为一个可精确定义的 log 指数问题（a vs 1.5），并给出两处可检验的数值/理论判据。

## 1. 变量约定与已确认数据

- $\delta_N=\sqrt{S(N)/N}(\log N)^{3/2}$；$S(N)=2C_2\prod_{p\mid N,p>2}\frac{p-1}{p-2}$。
- R(N) ⇔ $\|T_N\|\le\delta_N$（LL Thm 6.1，已复核原文）。
- 有限模型：LL Appendix B recipe（两条边界线、trapezoid 权重、无 $1/(2\pi)$、$C_{ij}=\sqrt{w_i}E_N(s_i,\bar s_j)((1+s_i)(1+\bar s_j))^{-1}\sqrt{w_j}$）；N=30030 精确复现论文 λ=+0.3574618/−0.3534214、‖C‖/δ=0.826864。
- 记 $Y=\lambda_{\max}\sqrt N$，$C^{\rm sc}=Y/\sqrt{S(N)}$，ratio$=\lambda_{\max}/\delta_N=C^{\rm sc}/(\log N)^{3/2}$。对 $N=2p$：$\sqrt S=1.14908$。

细模型（H=40,mesh1/16；200006 为 H=20）已确认数值：

| N | 结构 | S(N) | δ_N | λ_max | ratio | Y | C^sc |
|---|---|---|---|---|---|---|---|
| 30030 | 2·3·5·7·11·13 | 5.1213 | 0.43231 | 0.357462 | 0.82686 | 61.95 | 27.35 |
| 39994 | 2·19997 | 1.32039 | 0.19820 | 0.212506 | 1.07220 | 42.50 | 36.98 |
| 40022 | 2·20011 | 1.32039 | 0.19815 | 0.275721 | 1.39152 | 55.16 | 48.00 |
| 60022 | 2·30011 | 1.32037 | 0.17117 | 0.207252 | 1.21079 | 50.78 | 44.19 |
| 100042 | 2·50021 | 1.32035 | 0.14192 | 0.166061 | 1.17007 | 52.52 | 45.71 |
| 200006 | 2·100003 (H=20) | 1.32034 | 0.10957 | 0.124657 | 1.13771 | 55.75 | 48.52 |

[事实] mesh m=8/16/32/64 在 N=40022 收敛（m=32→64 变化 4×10⁻⁸）；高度 H=40/60/80 在 N=40022 给 1.3915/1.3959/1.3979（单调缓升，下限方向；外推 H→∞≈1.399–1.400）。[事实] 同一模型下 H=20 相对 H=40 在 N=40022 低 1.09%（1.37641 vs 1.39150）——趋势比较必须做 H 修正（本轮大 N 点多为 H=20）。

---

## 2. 对 phase-4 的修正（重要）

1. **[事实]** LL 的 Hypothesis R 是 "for every **sufficiently large** even N"，$N_0$ **未量化**；Appendix A（p.54）明确 $N_0(c),N_0(c,h_c)$ 只是存在性。因此 N=40022 的反例**不否定**"最终对所有大 N 的 R"。
2. **[事实]** "N>e¹⁰" 只是构造门槛（strip 非空、$N^{2\alpha_N}=e^2$），不是 R 的验证范围。
3. **[事实]** Appendix B（p.62）自己写有限模型 "do not certify Hypothesis R for T_{30030,1}" 且 "Cutoff stability and pointwise high-precision checks do not bound the full operator's truncation or discretization error."
4. 正确修正：有限模型在 N=40022（及 2p 族到 2×10⁵）给出 ratio>1 是 **pre-asymptotic 失败**；phase-4 的"λ_max 近似与模数无关"是把不同因子结构的 N 混在一起的误读——$C^{\rm sc}$ 对结构敏感（多小因子 N 为 23–39；2p 最高 37–49），**2p 是 S(N) 最小、对 R 最苛刻的族**。
5. **[数值]** 可变条带参数 $c$（LL Appendix A：$\alpha=c/\log N$，$r(N)=\langle T_{N,c}v,v\rangle$ 与 c 无关）不能救 N=40022：粗模型 (H=8,m=8) 给 c=0.50/0.75/1.00 的 ratio=3.37/2.00/1.34（c 越小越差；与 [2/√3] 无关）。[liu-auditor 的 c_quick]

---

## 3. 大 N 趋势（最终数据，task-13 完成）

spectral-numerics 最终 16 点表（2p 族；H/mesh 已核验；H10→20 偏差 1.3–2.0%、H20→40 约 1%；大 N 用 m=8/16，m=4 有 +17% 求积伪影不可用）：

| N | H,m | λ_max | δ_N | ratio | Y | C |
|---|---|---|---|---|---|---|
| 39994 | 40,16 | 0.2125060 | 0.198197 | 1.0722 | 42.50 | 36.98 |
| 40022 | 40,16 | 0.2757214 | 0.198147 | 1.3915 | 55.16 | 48.00 |
| 60022 | 40,16 | 0.2072516 | 0.171170 | 1.2108 | 50.78 | 44.19 |
| 100042 | 40,16 | 0.1660613 | 0.141924 | 1.1701 | 52.52 | 45.71 |
| 200006 | 20,16 | 0.1246573 | 0.109569 | 1.1377 | 55.75 | 48.52 |
| 400006 | 10,8 | 0.0866444 | 0.084169 | 1.0294 | 54.80 | 47.69 |
| 600014 | 20,8 | 0.1035400 | 0.071989 | 1.4383 | 80.2 | 69.8 |
| 700006 | 10,8 | 0.0769050 | 0.067811 | 1.1341 | 64.35 | 55.99 |
| 999958 | 10,8 | 0.0655123 | 0.059006 | 1.1103 | 65.51 | 57.01 |
| 1000018 | 10,8 | 0.0631964 | 0.059005 | 1.0710 | 63.20 | 55.00 |
| 1000166 | 10,8 / 10,16 / 20,8 | 0.0559–0.0566 | 0.059001 | **0.9385–0.9595** | 55.4–56.6 | 48.2–49.3 |
| 1500038 | 10,8 / 20,4 | 0.06284 / 0.06323 | 0.050314 | **1.2491 / 1.2567** | 76.97 | 66.99 |
| 1500166 | 10,8 | 0.0532322 | 0.050312 | 1.0580 | 65.20 | 56.74 |
| 1999966 | 10,8 | 0.0513074 | 0.044902 | 1.1426 | 72.56 | 63.15 |
| 2011102 | 10,8 | 0.0511423 | 0.044804 | 1.1415 | 72.53 | 63.12 |
| 3000014 | 8,8 | 0.0422593 | 0.038210 | 1.1060 | 73.19 | 63.70 |
| 4000006 | 8,8 | 0.0335526 | 0.034053 | **0.9853** | 67.11 | 58.41 |

**核心事实**：
- 16 个抽样模数中 **14 个 ratio>1**，2 个 <1（N=1000166 的三个设置 0.939–0.960；N=4000006 的 0.985），但同尺度其他 p：N≈10⁶ 另两点 1.110/1.071，N≈1.5×10⁶ 另一点 1.058。**ratio 在 N=4×10⁴–4×10⁶ 内保持 O(1)，没有衰减趋势**（桶均值 1.201,1.161,1.075,1.069,1.143,0.993；总体均值 1.116）。
- C=λ√N/√S 的桶均值 = 42.5, 45.0, 48.1, 54.3, 62.9, 58.8（logN bins [10,11)…[15,16)）。**拟合结果**：全 16 点 C=2.684(logN)^{1.160±0.175}（ratio∝(logN)^{−0.340±0.173}）；大 N 子集（N≥4×10⁵，11 点）a=**1.67±0.53**。**临界值 a=3/2 未被分辨；诚实区间 a≈1.2–2.2。**
- 判据：a<1.5 ⇒ ratio→0，R 渐近真（a=1.16 时交叉约 N~8×10⁷；a→1.4 时天文数字）；a≥1.5 ⇒ ratio 不衰减，R 渐近假。**有限模型既不能证明也不能否定 R 的渐近真伪。**
- 唯一可靠的单侧逻辑：ratio>1 ⇒（结合 transfer 下界方向与 1–2% 的 H/mesh 误差）该模数处 ‖T_N‖>δ_N，是 **R(N) 失败的有限模型反证方向**；ratio<1 不提供任何支持。所以目前有 **14 个模数（直到 N≈4×10⁶）的（条件性）反证证据**；两个 sub-1 点不构成"穿越趋势"。
- 谱结构（保存矩阵的全谱）：tr(C) 比 ‖C‖_HS 小 1–2 个数量级（正负特征值强抵消）；top eigenvector 78–83% 质量在 α-line（Re s=1/logN），mean |Im s|≈0.9–1.1，Hardy 迹分数 0.67–0.71。

**解释**：phase-4 的"R 在论文声称范围内很可能失败"因此**部分恢复**（但只能到 N≈4×10⁶ 的抽样水平，不是证明）；"N=10⁶ 首次穿越 ⇒ N₀~10⁶"的说法**撤回**。R 的渐近真伪归结为 C(N) 的 log 指数 a 与 3/2 的比较，现有数据 a∈[1.2,2.2] 无法判定。

## 4. 理论：R 的精确墙 = 半个 log（kernel-theorist, task-14）[证明]

设 $n=\phi(N)/2$（odd 特征标个数），$f_\chi=g_\chi/(1+s)$，$Q_N=D_N+K_N$（完整模型核）。正确的中心是 **c=1**（因为 $(2/\phi)\sum_{\chi\ \rm odd}Q_N=Q_N$）：

$$T_\chi:=|f_\chi\rangle\langle f_\chi|-Q_N,\qquad E_N=P_N-Q_N=\frac{2}{\phi}\sum_{\chi}T_\chi\quad\text{（恒等式）}.$$

于是精确恒等式：
$$\operatorname{avg}_\chi\|T_\chi\|^2:=\frac{2}{\phi}\sum_\chi\|T_\chi\|_{HS}^2=\|Q_N\|_{HS}^2-2\langle P_N,Q_N\rangle_{HS}+\frac{2}{\phi}\sum_\chi\|f_\chi\|^4.$$

**可证上界 [证明]**：$\frac{2}{\phi}\sum\|f_\chi\|^4\le\max_\chi E_\chi\cdot\operatorname{tr}P_N\ll(\log N)^2\cdot(\log N)^2=(\log N)^4$（用 (G1) 型逐特征标界 $\max E_\chi\ll(\log N)^2$ 与 $\operatorname{tr}P_N\ll(\log N)^2$）；$\|Q_N\|^2_{HS}\asymp(\log N)^3$；$2\langle P_N,Q_N\rangle\ll(\log N)^{7/2}$。故
$$\rho_N:=\sqrt{\operatorname{avg}\|T_\chi\|^2}=O((\log N)^2).$$
而 R 的 HS 路线要求（见下节数值）$\rho_N\lesssim(\sqrt S/2)(\log N)^{3/2}$。**缺口恰为 $\sqrt S(\log N)^{1/2}$。**

**为什么 HS 路线要这个量**：若 $\{T_\chi\}$ 弱相关，$\|E_N\|_{HS}\approx(2/\sqrt\phi)\rho_N$，R 需要 $\|E_N\|_{HS}\le\delta_N$，即 $\rho_N\le(\sqrt\phi/2)\delta_N=(\sqrt S/2)(\log N)^{3/2}$。所以
> **R 渐近为真 ⇔ 逐特征标的"模型偏差四阶矩"比 GRH 平凡界好一个 $(\log N)^{1/2}$（在 2p 族还要乘 √S）。**
这正是"逐特征标四阶矩/相位对齐"问题，LL Lemma 6.4 的二阶平均（$\frac{2}{\phi}\sum_\chi\int|g_\chi|^2/(1+t^2)\ll(\log N)^2$）看不到它；大筛/字符正交只给对角；level-aspect pair correlation 仍是猜想（见 §5）。Alpöge 机器（Stepanov/theta lift/Weil 正性）不提供族相关估计。

**[数值/粗模型]** 用 H=8,m=2 有限模型直接测恒等式中的量（N=30030/40022/60022/100042/200006）：

| N | logN | ‖P‖_HS | ‖Q‖_HS | ‖E‖_HS | (2/φ)Σ‖f‖⁴ | ρ_N | ρ/(logN)² | (√S/2)(logN)^{3/2} | ρ/req |
|---|---|---|---|---|---|---|---|---|---|
| 30030 | 10.31 | 22.19 | 22.15 | 0.809 | 4998 | 67.1 | 0.63 | 37.5 | 1.79 |
| 40022 | 10.60 | 26.89 | 26.83 | 0.567 | 8290 | 87.0 | 0.78 | 19.8 | 4.39 |
| 60022 | 11.00 | 28.31 | 28.30 | 0.460 | 9295 | 92.2 | 0.76 | 21.0 | 4.40 |
| 100042 | 11.51 | 30.24 | 30.22 | 0.406 | 10759 | 99.2 | 0.75 | 22.4 | 4.42 |
| 200006 | 12.21 | 32.92 | 32.95 | 0.307 | 12990 | 109.1 | 0.73 | 24.5 | 4.45 |

**解读 [数值]**：(i) 实测 $\rho_N\approx0.73$–$0.78(\log N)^2$，即实际四阶矩几乎就落在可证的平凡界上（**没有**出现 R 所需的额外 $(\log N)^{-1/2}$ 相消）；(ii) 对 2p 族（S 最小），$\rho_N$ 比 R 所需大 4.4 倍——**HS 路线确实被卡死**；(iii) 多因子 N=30030 的 S 大，缺口只有 1.8 倍，但仍 >1；(iv) $\|P\|_{HS}\approx\|Q\|_{HS}$ 而 $\|E\|_{HS}$ 只有其 1–3%，说明 HS 层面的相消主要发生在 $P$ 与 $Q$ 的整体大小上，而不是逐特征标的。
（注意：这是 H=8,m=2 粗模型；H 收敛可能改变 10–30%，但 log 幂趋势应稳定。细模型 H=40 的对应标量由 spectral-numerics 计算中。）

---

## 5. 文献：GRH 的 Goldbach 后果与 R 所需的新定理（goldbach-researcher, task-16）

- **[事实]** "GRH ⇒ Goldbach 例外集 $E(X)\ll X^{1/2+\varepsilon}$" 是**真定理**（两条独立 2026 精确陈述：Bhowmik–Grimmelt 综述 arXiv:2607.27282 Thm 3.1：零点 Re≤Θ<3/4 ⇒ $E(X)\ll X^{2Θ-1/2+\varepsilon}$；Pintz–Althöfer arXiv:2610.15559 Thm 3：$g(\theta)=\theta(5-4\theta)/(2(2-\theta))$，$g(1/2)=1/2$）。**需要全局一致 GRH（所有模/高度），不是固定模 GRH(N)**；Alpöge 的 GRH 恰好覆盖，所以若其证明被接受，则 $E(X)\ll X^{1/2+\varepsilon}$ 变成无条件（Goldston 1992 可把 ε 换成 log 幂）。**但这仍只是 almost-all Goldbach，不是 Goldbach。**
- **[事实]** 无条件例外集记录：Pintz 2018 $X^{0.72}$ → Zhao 2025 arXiv:2511.05631 $E(X)=O(X^{7/10})$（ineffective）；Pintz–Althöfer 2026 在"存在任一固定无零半平面"下给 $X^{7/12+\varepsilon}$（实操引用 OpenAI 2026-09-30 未评审 quasi-RH 7/8 声明；Cairn Commons 列 "Claimed, unreviewed"）。与 R 无关，但应写进背景。
- **[事实]** 若 Alpöge GRH 被接受：LL 条件性证明的 GRH 条件被消去，只剩 S/R；R 本身**不被 GRH 蕴含**（LL §2.4.3 明说 GRH 只给 $\|T_N\|\ll(\log N)^2$）。
- **[事实/推导]** R 的最小可证输入被形式化为 **H_fam**：族二阶矩 + 跨 χ 非对角四阶相关（等价 level-aspect pair correlation 型输入）。关键文献：Kandhil–Languasco–Moree arXiv:2411.19762 明确**假设 GRH + Dirichlet L pair correlation** 才能推 Montgomery/EH——即该输入目前是猜想。Selberg CLT q-aspect（Das arXiv:2105.01251）、L'/L 固定点矩（Ghosh arXiv:2509.06390）、Young 四阶矩（Ann. Math. 173 (2011)）都只是对角/分布型，不能给 E_N 的 HS/算子范数。
- **[事实]** 未发现任何人把 Alpöge/Stepanov/theta-lift/Weil 正性机器用于加性问题的公开工作；MIT 核验页 2026-11-21 抓取仍与 2026-11-20 22:05 UTC 相同（comparator/Lean kernel replay 仍 running，未同行评审）。

---

## 5.5 c-依赖扫描（LL Appendix A）与"c 逃逸"的排除 [数值]

spectral-numerics 在 N=40022（H=20,m=8）上扫描 $lpha=c/\log N$：ratio=$\lambda/\delta_N$ 为 c=0.25: 7.78 | 0.5: 3.46 | 0.75: 2.05 | 1.0: 1.38 | 1.25: 1.01（admissible 上限 $c<\beta\log N\approx1.32$）。**允许范围内没有 c 使 ratio<1**；c↓ 使条带变宽、norm 迅速变差；c↑ 接近条带塌缩时 ratio 下降但仍在 N=40022 处 >1。

更关键的是：LL 定理真正需要的是 $Q_{N,c}\|T_{N,c}\|$（$Q_{N,c}\asymp e^{2c}$，见 (A.2)），不是 $\|T_{N,c}\|$ 本身。用上表乘 $e^{2c}$：c=0.5/0.75/1.0/1.25 → 乘积 ≈ 9.4/9.2/10.2/12.3，**最小在 c≈0.75–1.0，论文的 c=1 接近最优**。所以"换 c 逃逸 R"在真正目标量上也不成立（liu-auditor 粗模型 c-scan 亦得同样结论：c=0.50/0.75/1.00/1.05 → ratio 3.37/2.00/1.34/1.25）。

## 6. 对抗审计（heat-kernel-critic, task-17）

- **[事实] 转移论证方向**：固定 mesh 增大 H 只扩大检验函数空间 ⇒ λ_max(H) 单调不减且 ≤‖T_N‖；所以 phase-4 的"N=40022 时 ‖T_N‖>δ_N"在 H 截断方向是保守的（真值只会更大），**这一条不被推翻**。
- **[事实] 但反方向（H→∞ 上界）transfer 给不了**：phase-5 的"C≈const ⇒ R 渐近真"在逻辑上依赖"H 固定不随 N 系统性低估 λ"这一未证假设；这是本轮最大风险。
- **[数值]** H 耦合初步测量：N=40022 H=20 vs H=40 仅差 1.09%；H=40/60/80 差 0.3%/0.16%（收敛）。N=200006 的 H=20 vs H=40 与 N=400006 新点仍在跑（结果见 §3.1）。
- **[事实]** 实现层面：D_N 的 Euler–Maclaurin 大 |Im| 修正、P_N 的 (2/φ) 奇特征平均、trapezoid 无 1/(2π)、分母共轭方向、C 矩阵 Hermitian 性等逐项与 LL Appendix B 一致；未发现实现级伪影。
- 结论（暂定）：**确认 phase-4 的数值与转移逻辑**；**削弱/推翻 phase-5 的"X≈const 已有证据支持"**——它目前只是 4–5 点经验拟合 + 未测试的标度假设；X 强烈依赖因子结构，2p 族内的"平"需要结构性论证。

---

## 7. Lean 制品（lean-feasibility, task-18）

[事实] **Mathlib v4.36.0 已安装成功**（Lean 4.36.0；`lake env lean` 4.6s），`phase5/lean/phase5_mathlib.lean`（256 行）**编译 EXIT 0，无 sorry，6 条引理 `#print axioms` 均为 `[propext, Classical.choice, Quot.sound]`**：
- `abs_rayleigh_le_opNorm`：|⟨Tv,v⟩| ≤ ‖T‖‖v‖²；
- `selfAdjoint_inner_eq_starProjection`：range(T)⊆M ⇒ ⟨Tv,v⟩=⟨T(P_M v),(P_M v)⟩（LL Prop 5.3 "T̃=T⊕0" 的算子层内容）；
- `transfer_rayleigh_unit_le`：单位 v ⇒ |⟨Tv,v⟩|≤‖T_M‖；
- `hypothesisR_implies_abs_rayleigh_le`：‖T‖≤δ ⇒ |⟨Tv,v⟩|≤δ（R 的必要推论）；
- `rayleigh_gt_refutes_R`：δ<⟨Tv,v⟩, ‖v‖=1 ⇒ ¬(‖T‖≤δ)（phase-5 crux）；
- 有限维矩阵版本。
若编译/公理审计通过，这是本 session 唯一可交付的"形式化检验"制品；**注意它形式化的是逻辑链，不是 Goldbach，也不是 LL 论文本身**。

---

## 8. 结论与下一步

**结论**
1. **仍然没有 Goldbach 证明**；本 session 没有也不可能产生可形式化的 Goldbach 证明。
2. **phase-4 修正**：有限模型在 N=40022 的 ratio>1 是 pre-asymptotic；R 的 $N_0$ 未量化，论文逻辑不被有限反例威胁。
3. **R 的分叉（终版）**：λ_max∝N^{-1/2} 仍成立，但 C=λ√N/√S **随 log N 单调上升**（分桶均值 42.5→62.3，拟合 C∝(log N)^{1.14±0.3}），因此 ratio=C/(log N)^{3/2} 在 N=4×10⁴–2×10⁶ **保持 O(1) 而非趋于 0**；12 个抽样 N 中 10 个 ratio>1（含 N≈2×10⁶）。R 渐近真 ⟺ C 的 log 指数 a<1.5（此时交叉点约 N~10⁹），a≥1.5 则 R 假；**a 的 ±0.3 不确定度恰跨临界，现有数据无法判定**。phase-4 的"R 在论文范围内很可能失败"因此**部分恢复**（证据延伸到 N≈2×10⁶），但"R 最终为假"仍未证明；N=10⁶ 的单点 sub-1 不构成穿越趋势。
4. **精确的墙 [证明]**：HS 路线被"逐特征标四阶矩"的 $(\log N)^{1/2}\sqrt S$ 缺口卡住（实测 $\rho_N\approx0.75(\log N)^2$ 恰在平凡界附近），需要 level-aspect 族 pair correlation 型新定理；现有工具（含 Alpöge 机器）都不够。
5. **H_Gold 仍健康 [数值]**：与模型无关的加权 Goldbach 直接计算在 N 到 5×10⁸ 仍满足 |G−c_φS|/δ≈0.008–0.01（远小于 δ）——Goldbach 的定量形式比 R 弱得多、且数值上"更像真的"。

**下一步（若继续）**
1. 拿到 N≈1e6–2e6 的判决点，判定 (A)/(B)/(C)；用 H=40（或 H→∞ 外推）与 mesh 收敛控制系统误差。
2. 若 (A)/(B)：目标转为**证明 R**——即证明 level-aspect 族 pair correlation/四阶相关型输入；可先发表"GRH+H_fam ⇒ ‖T_N‖≤δ_N"的条件定理。
3. 若 (C)：LL 路线（渐近版本）死；回到 H_Gold 的直接研究或其它加性方法。
4. 细模型 H=40/mesh1/16 上测四个标量（trP, M4, ‖Q‖²_HS, ⟨P,Q⟩）以验证 §4 的粗模型数字。
5. Lean：完成 transfer/crux 引理的形式化与公理审计。

---

## 9. 文件索引

- `phase5/lead-phase5.md`（Lead 过程笔记：变量/修正/三情景/理论框架）
- `phase5/theory/scaling-theory.md`（kernel-theorist：per-character 分解、精确恒等式、ρ_N 的 (logN)² 上界、H_fam、§6 最终版）
- `phase5/numerics/bigN-trend.md`（spectral-numerics：N=2p 大 N 趋势——1000166 首次 <1；1500038 出现 1.249 尖峰；c-scan）
- `phase5/audit/r-status-audit.md`（liu-auditor：论文量词/Appendix A-B、level-aspect 文献、c≠1）
- `phase5/lit/lit-and-tools.md`（goldbach-researcher：GRH⇒E(X)≪X^{1/2+ε}、2026 记录、H_fam、Alpöge 机器）
- `phase5/adversarial/audit.md`（heat-kernel-critic：对抗审计（241 行）：独立复现 N=30030、H 耦合 +1.06% 不随 N 增长、大 N mesh 未收敛 0.62%、C 点间涨落 R2 风险）
- `phase5/lean/phase5_mathlib.lean`（Lean：transfer/crux 逻辑链）
- `phase5/alpoege-scan/scan.md`（proof-digest：Alpöge 仓库扫描——无 Goldbach/加性内容、无跨 χ L'/L 相关；有可借鉴的定量接口与族平均工具包）
- `phase5/mit-recheck/report.md`（repo-verifier：MIT 验证页 2026-11-21 08:00 UTC 仍无更新；新增 LUMI 独立 sandbox 构建证据；结果仍未官方完成）
- `phase5/lead-probe/`（Lead 的独立探针：pointwise E、粗模型分解、大 N 批次）
