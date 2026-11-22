# Phase-6 审计：LL 的 ‖T_N‖ 表述、Phase-6 协方差假设、H_Gold 直接攻击、密度-1 逻辑

> 审计：liu-auditor（task-25，2026-11-21）。**只写本目录**；未改动他人文件。数据来源：`phase6/lead/qh8.log`、`qh10.log`、`qconv.log`、`qscale.log`、`qvar.log`；`phase5/numerics/bigN-trend.md`；`phase5/theory/scaling-theory.md`；`phase5/0-phase5-报告.md`；LL 预印本 `/home/kiler/rh-work/liu-goldbach.pdf`（页号=PDF 页，行号=clean text 行）。
> 标注：**[事实]** 可核对；**[证明]/[推导]** 本报告论证；**[数值]** 数值；**[推测]** 判断。

---

## 0. 结论速览

1. **[事实] 论文从未讨论 ‖T_N‖ 的期望大小/增长/最优性，更没有暗示 R 为真。** 全文只有 6 处相关表述（§1 逐字）：
   - p.10："These facts hold for fixed N; **the arithmetic question is the size of this norm as N varies.**"（只说这是算术问题，不预测。）
   - p.12："their separate estimates each have size O((log N)^2)…; **they do not measure cancellation between the components.**"；"This available norm bound is too large…"
   - p.36："These bounds give a zero-free region **without requiring cancellation between the components of the residual.**"
   - p.42–43（§6.5）："**it does not assert optimality of the actual residual norm.**"
   - p.4：R 是"**ultimate conjecture**"，"Together with GRH, it would yield **what we expect** to be the best possible remainder bound"。
   - p.32："We encode the size of these eigenvalues relative to δ_N; the Dirichlet zeros enter through GRH and are a separate set of data."
   Appendix A（p.53–54）只讨论 c 依赖与"best order available from these bounds"，附录 B（p.62）自认 "do not certify Hypothesis R"。
   **⇒ 任何"论文内部与 R 冲突/论文声称 R 最优"的批评都没有文本依据；R 在论文中只是主观 conjectural 期望。**
2. **[数值] Phase-6 的"样本协方差"假设 λ_max(T_N)≈κ‖Q_N‖/√n（n=φ/2）在 matched pipeline 下得到支持**：qh8（H=8,m=2）κ=1.76/1.40/1.79（N=40022/60022/100042）；qh10（H=10,m=8）κ=1.62/1.84/1.83/1.77（N=4.0e5–1.0e6）。κ=O(1) 且无明显随 N 漂移（±15–25% 算术散差）。
3. **[推导] 由该假设可得 C(N):=λ_max√N/√S ≈ 2κ·lQ/√S（N=2p 时 √(N/n)≈2，n=φ/2），故 C 的 log 指数 a≈lQ 的指数 b；R 渐近真 ⟺ a=b<3/2（此时 ratio=C/(logN)^{3/2}→0）。** LL 本身只给 HS 界（Prop 6.5: ‖D‖_HS,‖K‖_HS ≍(logN)^{3/2}；Thm 6.2 三角界 (logN)²），**既不支持也不冲突**典型尺寸/独立性；样本协方差图像是新的、LL 之外的假设。
4. **[证明+推测] 理论上 Q_N=D_N+K_N=κ_NL+R（κ_N=logN−log2π+ψ(3/4)，L=正则化极点核正算子、‖L‖≍1），若 R 的算子范数有界（其核为 O(1+log(1+|Im w|))，HS 范数有限），则 lQ=κ_N‖L‖+O(1) ⇒ **b=1**，于是 a=1<3/2 ⇒ **R 渐近为真**，但 N₀ 由 (2κ‖L‖/√S)² 决定，数值上可达 e^{30}–e^{60} 量级（≫ 任何可测范围）。若 b=1.5（即 lQ∝(logN)^{3/2}，与 HS 同阶），则 ratio→常数：常数>1 时 **R 渐近为假**。**现有数据（N≤2×10⁹ 的 character-free lQ 与 N≤2×10⁶ 的 λ_max）无法判定 b**：线性拟合 lQ≈2.90logN−16.1（残差≤5%，b=1）；幂律拟合 lQ∝(logN)^{1.53}（因截距）；且 lQ 强烈依赖 (H,m)（N=40022: H8m2 16.45 vs H10m8 14.57，−11%），截断未收敛前的指数拟合不可信。**决定性实验：在收敛的 (H,m) 下同时测 λ_max 与 lQ 于 N=10^6–10^8，拟合 lQ 的渐近形式。**
5. **[证明] H_Gold 直接攻击：现有技术不能证明 |r(N)|≤Cδ_N。** 我们给出两条严格恒等式解释 10³ 倍额外相消，并把最小谱充分条件精确化为 **H_fam′**（只控制带限子空间 B_N 与一个方向 w_N^* 的压缩范数）：
   $$H_{fam}':\ \|P_{B_N\cap(w_N^*)^\perp}T_NP_{B_N\cap(w_N^*)^\perp}\|\le\delta_N/Q_\phi\ \Longrightarrow\ |r_\phi(N)|\le\delta_N\ (\text{即 }H_{Gold}).$$
   该条件**严格弱于 R**（R⇒H_fam′；反之构造反例），且比 phase-5 的 H_fam 更针对单一权。但**尚不能从 GRH/已知定理证明 H_fam′**：H_Gold 对所有 N 成立（GRH 下）已蕴含 Goldbach，属公开难题（GRH 单独只给例外集 E(x)≪x^{1/2+ε}）。**[推测] 额外相消的结构来源**：v_ψ 与主导本征方向（近似 w_N^*）正交（精确）、且 v_ψ 是带限的（频率 supp⊂I_N）、平滑 V 使高频/带外本征方向不被激发；这一图像与数值一致，但**不能代替 H_Gold 的算术证明**。
6. **[证明] "密度 1 充分"命题为假。** LL 的定理是逐 N 条件命题；R 只在密度 1 集合上成立 ⇒ G(N)>0 只在密度 1 集合上；**非负性 G≥0 对稀疏例外集无效（G 可为 0）**。已知 GRH 下例外集 E(x)≪x^{1/2+ε} 允许无限多（密度 0）例外；有限验证到 4×10^18 不延伸。**密度 1 永远不足以推出 Goldbach；需要全 N 的 R/S（或 H_Gold/H_fam′），或一个能排除无限稀疏例外的新机制。**

---

## 1. （任务 1）LL 全文关于 ‖T_N‖ 期望大小/最优性/增长的表述（逐字）

检索方式：`grep -n "expect\|optimal\|best possible\|operator norm\|size of\|growth\|asymptotic.*norm" liu-goldbach.clean.txt`，并通读 §2.4.3、§6.4、§6.5、§7.3、§8、Appendix A/B。

| 页码/位置 | 逐字原文 | 解释 |
|---|---|---|
| p.10（行 598–599） | "These facts hold for fixed N; **the arithmetic question is the size of this norm as N varies.**" | 唯一直接提到"随 N 的大小"：把它定义为算术问题，**不作预测、不声称渐近** |
| p.12（行 755–763，§2.4.3） | "…Their separate estimates each have size O((log N)^2) at α_N=1/log N; **they do not measure cancellation between the components.**"；"This available norm bound is too large to make the Goldbach error smaller than its main term; S and R impose the required improvement." | 明说 GRH 三角界不测量相消；R/S 是额外输入，不是推论 |
| p.36（行 2483–2487，§6.4 开头） | "These bounds give a zero-free region **without requiring cancellation between the components of the residual.**" | 再次确认基线不依赖相消，因此对 ‖T_N‖ 的真实大小无信息 |
| p.42–43（行 3062–3065，§6.5） | "The last factor tends to infinity both as x ↓0 and as x →∞, and has a positive finite minimum in between. Thus α≍1/log N gives the best order obtainable from these separate bounds; **it does not assert optimality of the actual residual norm.**" | 明确：只优化"分离估计"的阶，**不声称实际残差范数最优** |
| p.53–54（Appendix A.3，行 3953–3955） | "Lemma A.3 shows that a fixed positive c gives the best order available from these bounds; they do not select a universal optimal constant. Changing c therefore changes the constants, not the logarithmic gap in the available estimates." | c 只在常量层面；不涉及 R 真伪 |
| p.4（行 227–231，Hypothesis R 前） | "…we nevertheless venture the following stronger, **ultimate conjecture** on the spectral zeros. Together with GRH, it would yield **what we expect to be the best possible remainder bound** in the weighted Goldbach asymptotic formula." | R 被明确称为 conjecture；"we expect"是主观期望，无推导 |
| p.32（行 2182–2184，§6 开头） | "**We encode the size of these eigenvalues relative to δ_N**; the Dirichlet zeros enter through GRH and are a separate set of data." | 只是编码尺度，不预测 |
| §7.3（p.51）/§8（p.51–52，行 3750–3758） | "…The identity thus retains the full signed arithmetic discrepancy and **transfers operator norm bounds to error bounds without a factor growing with N**."；"Hypotheses S and R enter only after this identity has been established: they control ‖T_N‖…" | 只描述"给定界后如何转成误差"；无期望大小 |
| Appendix B（p.62，行 4392–4394） | "Cutoff stability and pointwise high-precision checks do not bound the full operator's truncation or discretization error. The figures illustrate the finite spectral model; **they do not certify Hypothesis R for T_{30030,1}**." | 明确不认证 R |
| Abstract / §1.2 | "additional spectral hypotheses"、"assuming the generalized Riemann hypothesis… together with either of two additional spectral hypotheses" | R/S 是假设 |

**结论 [事实/推导]**：
- 论文**没有**讨论 ‖T_N‖/δ_N 的渐近、没有声称 R 应该为真、没有声称 R 最优（只对"余项误差"表达 "we expect best possible" 的期望）。
- 任何"论文内部存在与 R 冲突的表述"不成立；反过来说，论文也**没有**任何支持 R 为真的证据（除了类比）。
- 论文对"separate bounds 非最优"的自觉表述（§6.5）恰好为 phase-6 的"典型尺寸/样本协方差"假设留出了空间：**论文不主张 (logN)² 是紧的**，而是明确"不 assert optimality"。

---

## 2. （任务 2）Phase-6 假设审计：λ_max(T_N)≈κ‖Q_N‖/√n，a≈b

### 2.1 假设的精确形式与数值检验（[数值]）

**假设（Lead phase-6）**：设 $Q_N=D_N+K_N$（character-free：只依赖 N 的算术/模型部分），$n=\varphi(N)/2=|X_N^-|$，则
$$\lambda_{\max}(T_N)\approx\kappa\,\|Q_N\|/\sqrt n,\qquad \kappa=O(1)\ \text{与 }N\text{ 无关（允许算术散差）}.$$
等价地（$N=2p$ 时 $\sqrt{N/n}\approx2$）：
$$C(N):=\lambda_{\max}\sqrt{N}/\sqrt{S(N)}\approx 2\kappa\|Q_N\|/\sqrt{S(N)}.$$
于是 $C$ 的 log 指数 $a$ ≈ $\|Q_N\|$ 的 log 指数 $b$。

**matched 数值（来自 phase6/lead，λ 与 lQ 用同一 (H,m) 同一 pipeline）**：
- `qh8.log`（H=8,m=2）：N=40022: λ=0.288632, lQ=16.448, hsQ=26.835, trQ=88.96, **κ=λ√n/lQ=1.755**, ratio=1.457, C=50.25；60022: κ=1.396, ratio=1.142, C=41.68；100042: κ=1.792, ratio=1.444, C=56.40。
- `qh10.log`（H=10,m=8）：N=400006: λ=0.086644, lQ=16.951, **κ=1.616**, ratio=1.029, C=47.69；700006: κ=1.837, C=56.00；999958: κ=1.833, C=57.01；1000018: κ=1.769, C=55.00。
- **结论**：κ∈[1.40,1.84]，跨 N 与 (H,m) 无明显漂移（±15–25% 散差，和算术 C 的 ±30% 同量级）⇒ **在 finite model 中，λ_max≈κ‖Q_N‖/√n 是一个数值上成立的标度关系**（比例常数 κ=O(1)）。这是 Lead phase-6 假设目前最直接的证据。

### 2.2 Q_N 的 character-free 尺度（[数值] + [推导]）

- **[数值] `qscale.log`（H=8,m=2，N=2p，N 从 4×10⁴ 到 2×10⁹）**：lQ=‖D_N+K_N‖ 从 16.45(logN=10.60) 增到 48.25(logN=21.42)；hsQ=‖Q‖_HS 26.84→85.92。两种拟合：
  - 线性：$lQ\approx2.897\log N-16.10$（14 点，残差 ≤5%，系统性 U 形：中间 −5%、两端 +12%/+5%）⇒ **b≈1**；
  - 幂律：$\log lQ=1.535\log\log N+\text{const}$（因截距），即 $lQ\propto(\log N)^{1.53}$ ⇒ **b≈1.5**。
- **[数值] (H,m) 依赖性很大**：`qconv.log` N=40022：lQ(H=8,m=2)=16.448，而 lQ(H=10,m=8)=14.567（−11.4%）；qscale 的 H=10,m=8 与 qh10 的 lQ 也不同（同一 N=400006：qscale H8m2=20.841 vs qh10 H10m8=16.951，−19%）。**⇒ 未收敛的截断会系统性高估 lQ，幂律指数 1.53 与线性指数 1 的判别必须在收敛 (H,m) 下做。**
- **[推导] 理论：pole 结构给出 b=1 的强提示。** 我们 phase-2/5 已证（独立复核）：
  $$D_N(w)+K_N(s,\bar z)=\kappa_N/w+R_N(s,\bar z),\qquad \kappa_N=\log N-\log(2\pi)+\psi(3/4)\approx\log N-2.9237,$$
  其中 $w=s+\bar z$，$R_N$ 的核对低高度为 $O(1+\log(1+|\Im w|))$（HS 范数有限）。$L$：$h\mapsto$ 以 $1/((s+\bar z)(1+s)(1+\bar z))$ 为核的算子，是**正算子**且 $\|L\|\le2\pi$、对局部 $h$ 有 $\langle Lh,h\rangle\asymp\|h\|^2$（phase-5 audit §3.2 的显式分解 $L=\int_0^\infty e^{-2\alpha u}\varphi_u\otimes\bar\varphi_u du$）。因此
  $$\|Q_N\|=\kappa_N\|L\|+O(\|R_N\|)=\kappa_N\|L\|+O(1)\quad(N\to\infty,\ \text{收敛 (H,m)}).$$
  即 **b=1（线性于 logN）**，而不是 3/2。若 b=1，则 $a=1$，$\text{ratio}=C/(\log N)^{3/2}\approx(2\kappa\|L\|/\sqrt S)/\sqrt{\log N}\to0$：**在 Phase-6 假设下 R 渐近为真**。
  N₀ 的量级：$\text{ratio}=1$ ⇔ $\sqrt{\log N}=2\kappa\|L\|/\sqrt S$；若 $\kappa\|L\|\approx3$–4（由 lQ≈(1.3–2.2)logN），则 $\log N\approx(6$–$8)^2/1.15^2\approx27$–48，**N₀≈e^{27}–e^{48}≈10^{12}–10^{21}**——远大于任何可测范围。这解释了为何有限模型在 N≤2×10⁶ 仍 ratio>1：**pre-asymptotic 区间极长**。
- **[推导] 若 b=1.5**（即 lQ 最终 ∝(logN)^{3/2}，与 phase-2 的 HS 尺度一致），则 ratio→$2\kappa\|L_{3/2}\|/\sqrt S$ = 常数；数值上（lQ≈0.48(logN)^{3/2}、κ≈1.7、S≈1.32）常数≈$2·1.7·0.48/1.149\approx1.42>1$，**R 渐近为假**。
- **【推测/判据】现有数据无法区分 b=1 与 b=1.5**：线性拟合残差有 U 形系统偏差；幂律拟合在收敛性未定时不可靠。**决定性实验**（成本低，建议 numerics 做）：
  1. 固定 N 增大 (H,m) 至 lQ 收敛（qconv 只跑了 2 点）；在收敛 (H,m) 下算 N=10^6–10^8 的 lQ 与 λ_max（matched）；
  2. 用 `qscale.py`（character-free，极廉价）推到 N=10^15–10^30，拟合 lQ 是否满足 lQ/logN→常数（b=1）或 lQ/log^{1.5}→常数（b=1.5）；
  3. 同时拟合 κ=λ√n/lQ 是否稳定（现在 ±25%）。
  这三项能定量回答 R 的渐近真伪（在 Phase-6 假设成立的前提下）。

### 2.3 LL 的分量估计是否支持"样本协方差涨落"图像？

- **[事实]** LL Prop 6.5（p.40–42）只给出 $\|P_N\|_{HS}\le\operatorname{tr}P_N\ll(\log N)^2+\alpha_N^{-2}$、$\|D_N\|_{HS}\le\operatorname{tr}D_N\ll\alpha_N^{-2}$、$\|K_N\|_{HS}\ll\alpha_N^{-2}$；phase-2 把后两者 sharpen 到 $\asymp(\log N)^{3/2}$。Thm 6.2（p.36）只给三角界 $\|T_N\|\le\|T_N\|_{HS}\ll(\log N)^2$。
- **[事实]** LL 全文**没有**任何"典型大小/独立性/协方差"表述；§6.5 明确"does not assert optimality of the actual residual norm"（§1）。
- **[推导]** "样本协方差"图像在结构上是自然的：$P_N=(2/\phi)\sum_\chi|f_\chi\rangle\langle f_\chi|=(1/n)\sum_{\chi\in X_N^-}|f_\chi\rangle\langle f_\chi|$（$n=\phi/2$），即 n 个秩一 PSD 算子的样本平均；若它们的均值是 $Q_N=D_N+K_N$（LL 的模型正是"连续化均值"），则 $T_N=P_N-Q_N$ 是中心化样本均值，其算子范数按随机矩阵/协方差涨落 $\approx\kappa\|Q_N\|/\sqrt n$。**这个图像与 LL 的估计完全相容（LL 只给 worst-case 上界），但 LL 不提供任何支持它的论证**（无 independence/decoupling/negative-association 估计；phase-3 的 (G2) 即跨 χ 弱相关也未能证明）。因此：**Phase-6 假设是 LL 之外的、新的典型尺寸假设，不是 LL 的推论；不存在与 LL 冲突的表述。**
- **[推导] 与 no-triangle 天花板的关系**：phase-2/3 的 no-triangle 定理说的是任何"$P_N,D_N,K_N$ 分量 HS+三角"路线 ≥(logN)^{3/2}；Phase-6 图像不是三角分解，而是"中心化样本均值范数"——两者不冲突。**Phase-6 路线若成立，等价于绕过 no-triangle 的 $\|Q_N\|/\sqrt n$ 涨落界；它的正确性完全取决于跨 χ 弱相关（(G2)-型/四阶零点相关），这正是 phase-3 判定"不可证"的输入。**

---

## 3. （任务 3）H_Gold 直接攻击：10³ 倍相消的解释与最小充分条件 H_fam′

### 3.1 数值事实与朴素界的差距（[事实/数值]）

- **[事实]** LL (7.17)：$r(N)=c_\phi S(N)-G(N)=\langle T_Nv_N,v_N\rangle$，$|r|\le Q_N\|T_N\|$（$Q_N=\|v_N\|^2\ll_\phi1$；LL Prop 7.4：$Q_N=\frac{e^2}{2\pi}\int|V|^2du/u+O(1/\log N)$）。
- **[数值]** phase-4 `probe2.c` 直接算术计算：$|r(N)|/\delta_N\approx0.0006$（N=30030）、0.0014（40022）、0.0024（100042）、0.0025（200006）；而有限模型 $\|T_N\|/\delta_N\approx0.83$–1.4。**差 ~500–1000 倍。**
- **[推导]** 对 LL 的归一化权（如 $\phi=1$ 于 [1/3,2/3]，$\Phi=\sqrt u$，$V=\sqrt u/2$）：$Q_N\approx\frac{e^2}{2\pi}\int_{1/3}^{2/3}\frac{u/4}{u}du=\frac{e^2}{2\pi}\frac{1}{12}\approx0.098$。Cauchy–Schwarz 给 $|r|\le0.098\|T_N\|\approx0.098·1.4\delta=0.137\delta$；实际 $|r|\approx0.0014\delta$ ⇒ **仍有 ~100 倍额外相消**。H_Gold 就是要把这 100 倍（以及 N→∞ 的 δ_N 尺度）解释/证明掉。

### 3.2 两条严格恒等式：解释相消的结构来源（[证明]）

**（a）真超平面（phase-5 audit §3.4，已证）**：令 $\Phi_\psi=\sqrt u\psi$，$V_\psi=\Phi_\psi-u\Phi_\psi'$，其中 $\psi$ 为 LL 权类（$C_c^\infty(1/3,2/3)$、对称）。则 $\int_0^\infty V_\psi(u)u^{-2}du=0$；在 Fourier–Laplace 模型中
$$v_{N,\psi}=U_H\Bigl(\frac{V_\psi(e^{-\tau}/N)}{w_N(\tau)}\Bigr),\qquad w_N=e^{2\alpha_N\tau}+e^{2\beta\tau},$$
其支撑在 $I_N=[-\log(2N/3),-\log(N/3)]$。令
$$B_N:=\overline{\{U_H\psi:\ \operatorname{supp}\psi\subset I_N\}}^{\,H_N}\quad(\text{band-limited 闭子空间}),\qquad w_N^*:=U_H(e^{\tau}\mathbf 1_{I_N}(\tau))\in H_N.$$
则对每个 admissible $\psi$（支撑在 (1/3,2/3) 的同一类）：$v_{N,\psi}\in B_N$ 且 $\langle w_N^*,v_{N,\psi}\rangle=0$。**（b）** 因此
$$r_\psi(N)=\langle T_Nv_{N,\psi},v_{N,\psi}\rangle=\langle P_{N,\psi}T_NP_{N,\psi}\,v_{N,\psi},v_{N,\psi}\rangle,\qquad P_{N,\psi}:=B_N\text{ 内向 }(w_N^*)^\perp\text{ 的正交投影}.$$
**证明**：$v\in B_N$ 且 $v\perp w_N^*$，故 $Pv=v$；又 $T_N$ 自伴，$\langle Tv,v\rangle=\langle PTPv,v\rangle$（因 $\langle Tv,v\rangle=\langle TPv,Pv\rangle=\langle PTPv,v\rangle$）。$\square$

### 3.3 最小充分条件 H_fam′（比 R 严格弱）及其证明（[证明]）

**定义（H_fam′，对固定权 ψ）**：
$$H_{fam}'(\psi,N):\qquad \|P_{N,\psi}\,T_N\,P_{N,\psi}\|\le \frac{\delta_N}{Q_\psi}.$$
**定理**：若 GRH(N) 且 $H_{fam}'(\psi,N)$ 成立，则 $|r_\psi(N)|\le\delta_N$，从而 $G_\psi(N)=c_\psi S(N)+O(\delta_N)$；结合素数幂剔除（LL §2.5.3）即得 N 的 Goldbach 表示下界 $\gg_\psi S(N)N/(\log N)^2$。
**证明**：由 §3.2(b)，$|r|=|\langle PTPv,v\rangle|\le\|PTP\|\|v\|^2=\|PTP\|Q_\psi\le\delta_N$（$Q_\psi=\|v\|^2$）。$\square$
**严格弱于 R（[证明]）**：$R$ 是 $\|T_N\|\le\delta_N$；取任意满足 $\|PTP\|=0$ 但 $T$ 在 $B_N^\perp$ 或 $w_N^*$ 方向有大特征值的算子（例如有限维中 $T=\Lambda w^*\otimes w^*$，$v\perp w^*$：$\|T\|=\Lambda\gg\delta_N$ 而 $PTP=0$），故 $H_{fam}'\not\Rightarrow R$；反之 $R\Rightarrow H_{fam}'$（因 $\|PTP\|\le\|T\|$）。**⇒ H_fam′ 是严格弱于 R、且足以推出 H_Gold 的谱假设。**
**与 phase-5 H_fam 的关系 [推测]**：H_fam（族二阶矩+跨 χ 四阶相关）是"对全空间/HS 的族估计"；H_fam′ 是"对带限连续子空间减一维的算子范数"——目标更窄（只服务一个权的二次型），但不显然由 H_fam 推出；两者都未被证明。H_fam′ 是作者已知的"最弱可陈述充分条件"候选。

### 3.4 为什么现有技术证不了 H_Gold/H_fam′（[推导]，诚实判断）

尝试过的路线及停止点：
1. **只用 eΦ 的光滑/衰减**：LL 主张的积分在 $\Re s=\sigma\le1/9$ 上被 $N^{2\sigma}$ 放大（$\sigma=1/9$ 时 $N^{2/9}$），移到 $\sigma=\alpha_N=1/\log N$ 后 $N^{2\alpha}=e^2$，但 $E_N$ 在边界有 $-\kappa_N/w$ 单极点，加权 $L^1$ 范数 $\approx\kappa_N\log\log N\approx\log N\log\log N\gg\delta_N$。**光滑性本身不够（差 N^{1/2} 量级）。**
2. **显式公式/零点求和**：把 contour 移到 $\Re s<0$ 会收集零点残基，但其和经显式公式变回同一加权 Goldbach 素数对和（循环），不产生新的小性。
3. **大筛/AFE/矩**：只给对角/平均型界（phase-4 independent-audit §4）；跨 χ 四阶相关是猜想级（Kandhil–Languasco–Moree 2026 的 pair-correlation 假设）。
4. **AR/正性**：Weil 型正性是乘性单变量；对本文双变量核无已知"张量正性"（phase-4 报告）。Alpöge 机器不提供定量 L² 输入。
**结论 [推导]**：$H_{Gold}$（对每个固定 admissible 权、所有充分大 N 的误差 $O(\delta_N)$）在 GRH 下**已经是公开难题**：它蕴含（弱）Goldbach 的大范围表示，而 GRH 单独已知只给例外集 $E(x)\ll x^{1/2+\varepsilon}$（Hardy–Littlewood 1924，LL p.2；phase-4 audit）。因此现有技术不能证明；H_fam′ 是最精确定义的"最小谱替代"。**[推测]** 若有人能证 H_fam′，其证明必然包含新的跨 χ 零点/素数对相关机制，而不只是 LL 现有引理的精细化。

### 3.5 数值上如何检验"额外相消来自 w_N^* 方向"（建议，[推测]）

在有限模型（C 矩阵）上：
1. 计算 $r_\psi=\langle C v,v\rangle$ 的精确值（与 probe2 的算术值比对）；
2. 计算 top-k 本征向量 $\{e_j\}$ 与 $v_\psi$、$w_N^*$（离散化）的重叠；若 $|\langle e_1,v\rangle|^2\ll\|v\|^2$ 且 $e_1\approx w_N^*$，则 §3.2 的机制被数值确认；
3. 计算投影压缩范数 $\|P C P\|$（P=带限∩w*⊥）并比较 δ_N：若 ≪δ_N，H_fam′ 数值上极可信（其证明仍是另一回事）。
（这些量在现有 pipeline 的 G/L'/L 数组上可算，成本 O(nodes²) 或借助 saved C。）

---

## 4. （任务 4）"R 只对密度 1 的 N 成立（稀疏例外）"能否配合 LL 与非负性推出 Goldbach？

### 4.1 命题与反证（[证明]）

**命题（密度-1 充分性）**：设 (A) 存在偶数集合 $\mathcal A$ 使 $\mathcal A$ 的自然密度为 1（在偶整数中），且对所有 $N\in\mathcal A$，$R(N)$ 成立；(B) $G(N)\ge0$ 对所有 N；(C) Goldbach 已验证到 $4\times10^{18}$。则能否推出"所有充分大偶数 N 有 Goldbach 表示"？
**答案：否。**
**证明（逻辑层面）**：
1. LL 的推导是**逐 N** 的：由 $R(N)$（等价 $\|T_N\|\le\delta_N$）与精确恒等式得 $|G(N)-c_\phi S(N)|\le Q\delta_N$，取 N 大使得 $Q\delta_N<c_\phi S(N)$ 即 $G(N)>0$。**该推理只对满足 R(N) 的那个 N 有效。**
2. 若 R 只在 $\mathcal A$（密度 1）成立，则只能得到 $\{G(N)>0:\ N\in\mathcal A\}$；对补集 $\mathcal E$ 无任何控制。**非负性 $G(N)\ge0$ 只给 $G(N)\ge0$，允许 $G(N)=0$（即该 N 没有素数对在权支撑内）。**
3. 密度 1 对 $\mathcal E$ 的约束仅是 $|\mathcal E\cap[1,x]|=o(x)$；$\mathcal E$ 可以是无限稀疏集（例如 $2^{10^j}$ 的某子列）。有限验证 (C) 只覆盖有界范围，不延伸到无限补集。
4. 因此存在与 (A)+(B)+(C) 相容但 Goldbach 在 $\mathcal E$ 上失败的数学配置：取任意无限偶稀疏集 $\mathcal E$（起点 >4×10^18），令数组 $G$ 在 $\mathcal A$ 上满足 $G=c_\phi S+O(\delta)$、在 $\mathcal E$ 上 $G=0$，在有限范围满足 (C)——则 (A)(B)(C) 全成立而 Goldbach 失败。**这说明假设集不够（非构造真实素数；只是证明这些假设不蕴含结论）。** $\square$
- **[事实] 旁证**：在 GRH 下已知的例外集上界 $E(x)\ll x^{1/2+\varepsilon}$（Hardy–Littlewood 1924；LL p.2 引用）恰恰**允许**无限多（密度 0）Goldbach 例外；没有任何已知定理排除这种稀疏例外。因此"密度 1 的 R"即使为真，也与"存在无限稀疏反例"完全不矛盾。

### 4.2 需要什么才能补上

- **（强）所有 N 的 R/S**（LL 原假设）；或
- **（弱）所有 N 的 H_Gold/H_fam′**（仍是所有 N）；或
- **（根本不同）一个排除无限稀疏例外的机制**：例如证明"若某 N 无表示，则附近某个可计算区间内出现矛盾"（目前无任何此类结构：G(N) 对 N 无连续性/单调性，各 N 的算子 T_N 独立）；或
- **（计算路线）**把有限验证推到某个 X 且证明例外集为空 for x≥X——密度型陈述永远做不到这一点（做不到"无限远处为空"）。
- **[推导] 结论**：密度-1 陈述对 Goldbach 全称命题**逻辑上永远不够**；LL 框架只在逐 N 意义下转移误差。**因此 phase-5/6 讨论"R 只对密度 1 成立"时必须明确：这不构成 Goldbach 的路线，除非另有"所有 N"或"无稀疏例外"的输入。**

---

## 5. 结论与建议（给 Lead）

1. **论文文本**：LL 没有讨论 ‖T_N‖ 的期望大小/渐近/最优性；只称 R 为 "ultimate conjecture" 并表达 "we expect best possible remainder" 的主观期望；§6.5 明说 separate bounds 不 assert optimality。**⇒ 不能以"论文内部"批评 R；也不能引论文支持 R。**
2. **Phase-6 假设**：数值 matched 支持 λ_max≈κ‖Q_N‖/√n（κ=1.4–1.8）；它与 LL 完全相容（LL 只给 worst-case 界），但 LL 不提供典型尺寸/独立性。**a≈b 的关系由 C≈2κ lQ/√S 给出（N=2p）；因此 R 的渐近真伪 = lQ 的 log 指数 b 是否 <3/2。**
3. **b 的判定**：理论 pole 分解（D+K=κ_NL+有界余项，L 正、‖L‖≍1、κ_N≈logN）提示 **b=1** ⇒ **R 渐近为真**（但 N₀ 可能达 10^{12}–10^{21}，与有限模型 N≤2e6 的 ratio>1 完全相容）。数据上 lQ 的拟合在 b=1（线性，残差 U 形 ≤5%）与 b=1.53（幂律，因截距）之间不确定；且 lQ 强烈依赖 (H,m)（未收敛，−11%–−19%）⇒ **需要收敛 (H,m) 下 N=10^6–10^8 的 matched λ_max & lQ 数据，以及 qscale 推到 10^15–10^30，才能判定 R 的渐近真伪。**
4. **H_Gold**：数值上 |r|≈10^{-3}δ（比 Cauchy–Schwarz 小 ~100 倍）；结构解释：v∈带限子空间且 v⊥w_N^*（严格），主导本征方向被正交掉 + 带外方向不被激发。**严格条件定理**：H_fam′（投影压缩范数 ≤δ_N/Q_φ）⇒ H_Gold；H_fam′ 严格弱于 R。**但现有技术不能证明 H_fam′/H_Gold**（它已蕴含 GRH 之外的 Goldbach 型机制；GRH 单独只给例外集）。这是本轮最重要的"负面但精确"的结论。
5. **密度-1**：**不充分**（§4）：LL 逐 N 转移，密度 1 只覆盖密度 1 集合；非负性对稀疏例外无效；GRH 例外集允许无限稀疏例外；有限验证 4×10^18 不延伸。任何"a.e. R ⇒ Goldbach"的论证在逻辑上缺一步（需要全 N 或排除无限稀疏例外的机制）。
6. 建议下一步（按优先级）：
   (a) **判定 b**：用 character-free qscale（廉价）推大 N + 收敛 (H,m) 的 matched 数据；这决定 R 的渐近真伪（在 Phase-6 假设下）。
   (b) **H_Gold 数值机制检验**：在 saved C 上算 v_ψ 与 top 本征向量的重叠、投影压缩范数 ‖PCP‖，验证 §3.2 的机制；若 ‖PCP‖≪δ_N，给出 H_fam′ 的强数值支持（非证明）。
   (c) 文献：H_fam′/H_Gold 属于 level-aspect 跨 χ L'/L 相关 + 平滑权，现有文献空白（phase-4/5 已核）。

---

## 6. 数据附录（[数值]，来源 phase6/lead/ 与 phase5/numerics/）

**A. matched qh8/qh10（λ_max 与 lQ 同 (H,m) 同 pipeline）**

| N | H,m | λ_max | lQ=‖Q_N‖ | hsQ | κ=λ√n/lQ | ratio | C=λ√N/√S |
|---|---|---|---|---|---|---|---|
| 40022 | 8,2 | 0.288632 | 16.448 | 26.835 | 1.755 | 1.457 | 50.25 |
| 60022 | 8,2 | 0.195485 | 17.156 | 28.303 | 1.396 | 1.142 | 41.68 |
| 100042 | 8,2 | 0.204897 | 18.084 | 30.220 | 1.792 | 1.444 | 56.40 |
| 400006 | 10,8 | 0.086644 | 16.951 | — | 1.616 | 1.029 | 47.69 |
| 700006 | 10,8 | 0.076905 | 17.512 | — | 1.837 | 1.134 | 56.00 |
| 999958 | 10,8 | 0.065512 | 17.867 | — | 1.833 | 1.110 | 57.01 |
| 1000018 | 10,8 | 0.063196 | 17.867 | — | 1.769 | 1.071 | 55.00 |

**B. qscale character-free lQ（H=8,m=2）**：(N, lQ, lQ/log^{3/2}N)：40022,16.448,0.477；100046,18.084,0.463；200006,19.414,0.455；400006,20.841,0.450；1000166,22.899,0.446；2000006,24.600,0.445；4000006,26.444,0.446；10000022,29.110,0.450；20000038,31.298,0.454；60000046,35.019,0.462；200000014,39.363,0.471；600000014,43.510,0.479；2000000014,48.247,0.487。（U 形 ⇒ 单一幂律拟合不可靠。）

**C. (H,m) 敏感性（qconv.log）**：N=40022：lQ(H8m2)=16.4484，lQ(H10m8)=14.5672（−11.4%）；hsQ 26.835 vs 23.731；trQ 88.96 vs 90.78。**⇒ 未收敛的 lQ 指数不可作判据。**

**D. qvar.log（d1/lQ≈1.16–1.19，d1/log^{1.5}≈0.53–0.57）**：Q_N 的"主项 d1"与 lQ 同阶、同标度，支持"pole 主导"图像（b=1 的间接证据）。

---

## 7. 复现/文件

- 数据：`phase6/lead/qh8.log`、`qh10.log`、`qconv.log`、`qscale.log`、`qvar.log`、`*.json`（lead 的脚本）。
- 本报告使用的 LL 引文页码：p.4、p.10、p.12、p.32、p.36、p.42–43、p.51–54、p.62（本地 PDF `/home/kiler/rh-work/liu-goldbach.pdf`）。
- 我未重跑 phase6 lead 的脚本（只读日志）；b 的判定实验（qscale 推大 N、qconv 至收敛）**未在本轮完成**（时间盒内），建议 numerics 组执行（qscale 单次 5s 级，qconv 单点 20s 级）。
- H_fam′ 的证明只用 LL Prop 7.4/phase-5 audit §3.4 的已证恒等式，不依赖任何未证猜想；其"能否证明"是 open（§3.4）。

## 8. 引用/URL（本文新增）

- LL 预印本：`/home/kiler/rh-work/liu-goldbach.pdf`（MRC 页面 https://mrc.sdu.edu.cn/english/info/1018/1514.htm）。
- Hardy–Littlewood GRH 例外集：LL p.2 引用 [6]（Proc. LMS (2) 22 (1924) 46–56）。
- level-aspect pair correlation（猜想，非定理）：N. Kandhil, A. Languasco, P. Moree, *Pair correlation of zeros of Dirichlet L-functions…*, Math. Ann. 394 (2026) 43, doi 10.1007/s00208-026-03383-y。
- Young 四次矩：arXiv:math/0610335，Ann. of Math. 173 (2011) 1–50。
- Ghosh L'/L 固定点矩：arXiv:2509.06390。
- Alpöge/MIT 验证页：https://math.mit.edu/~drew/grh/（本地快照 `/home/kiler/rh-work/mit/`）。
