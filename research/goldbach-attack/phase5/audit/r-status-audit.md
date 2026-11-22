# Phase-5 独立审计：R 状态分叉、LL Appendix A/B 的声称边界、level-aspect L'/L 文献

> 审计：liu-auditor（task-15，2026-11-21）。**只写本目录**；未改动 phase2–phase4 的任何文件（c≠1 数值用只读 import + monkeypatch，脚本在 `phase5/audit/c_quick.py`）。
> 标注：**[事实]** 有出处/可核对；**[证明]/[推导]** 本报告论证；**[数值]** 数值（标明来源）；**[推测]** 判断。
> 基准：LL 预印本 `/home/kiler/rh-work/liu-goldbach.pdf`（页号=PDF 页）；phase-4 报告 `phase4/0-phase4-报告.md`、`phase4/independent-audit.md`、`phase2/spectral-numerics-extended.md`、`phase2/spectral/cache/results_ext.txt`、`results_mesh.txt`。

---

## 0. 结论速览（给 Lead）

1. **[事实] 论文的逻辑完全容纳任意大的 N₀，而且论文从未声称在 N>e^{10} 处（数值地/有限模型地）验证过 R。**
   - 主文 Hypothesis S/R 的措辞是 "For every *sufficiently large* even N satisfying GRH(N)"，N₀ 不量化（p.4、p.12）。
   - `N>e^{10}≈22026` 只是构造的技术门槛（条带非空、$N^{2\alpha_N}=e^2$，p.3、p.9），**不是**"论文声称 R 已在此范围成立"。
   - Appendix A（p.53–54）明确："Fix c>0 and an even N≥4 with N>e^{10c}"（技术条件）；"For each fixed c>0, preassign a positive h_c…"；"This order of quantifiers is essential"；"**The eventual hypotheses assert these conditions for all sufficiently large even N satisfying GRH(N), with lower bounds N₀(c) and N₀(c,h_c) on N. Neither these lower bounds … need be uniform in c. The main hypotheses are their specializations at c=1.**"
   - Appendix B（p.62）自己写："Cutoff stability and pointwise high-precision checks do not bound the full operator's truncation or discretization error. The figures illustrate the finite spectral model; **they do not certify Hypothesis R for T_{30030,1}**." Prop B.5 也是条件句（"If ‖C‖≤δ_N, every complex zero has real part 1/2"）。
   - **⇒ 我们 phase-4 的标题/结论"R 很可能在论文自己声明的范围内就是假的"是过度解读，须改为"有限模型在 N≈4×10⁴–2×10⁵ 呈 pre-asymptotic 失败；λ_max∝N^{−1/2} 的标度暗示 R 可能在 N₀~3–7×10⁵ 之后为真"。**
2. **[数值] phase-4 的"λ_max 近似与模数无关/不随 N 增长"是误读；正确的不变量是 C:=λ_max√(N/S)，它近似 O(1)（37–49 for N=2p），因此 ratio=C/log^{3/2}N→0。**
   - 数据：N=40022: C=48.00；39994: 36.98；60022: 44.19；100042: 45.71；200006(H=20): 48.52；N=30030: 27.37。多小因子 N 的 C=22.8–38.6。
   - 若 C 有正极限，则 ratio→0，**R 渐近为真**；交叉点解 C=log^{3/2}N ⇒ N*≈3×10⁵–7×10⁵（2p 族；39994 为数值敏感离群点；H=20 对 200006 略低估）。**phase-4 的"可能为假"应改为"pre-asymptotic 失败 + 很大的 N₀（论文的 unquantified 'sufficiently large' 兼容）"。**
3. **[数值] 有限模型本身是稳健的**：N=40022、H=40 的 λ_max 在 mesh m=8/16/32/64 = 0.2761147/0.2757214/0.2757243/0.2757243（m≥16 收敛到 4 位），H=40/60/80 = 0.27572/0.27660/0.27698（截断方向只会低估）。所以 ratio=1.3915 是该有限模型的真值，不是求积伪影。**但**把 C 的 λ_max 解释为 ‖T_N‖ 的下界还依赖"压缩 + 求积误差小"的解释（见 §3.3），这是 phase-4 论证中最需要小心的一步。
4. **[数值] c≠1 不能救回 N=40022**：Appendix A 允许的条带参数受 α_{N,c}<1/10 限制，N=40022 时 0<c<1.063。快速模型（H=8,m=8，仅作相对比较）完整结果：c=0.50: λ=0.668682 (ratio **3.3747**)；c=0.75: 0.396170 (**1.9994**)；c=1.00: 0.265968 (**1.3423**)；c=1.05: 0.248399 (**1.2536**)——随 c↑ 单调下降，但在整个允许范围 $c<1.06$ 内仍 $>1$ 约 25%，**没有 c-逃逸**；与 A.3（c=1 为平衡阶）和 A.4（c↓0 障碍）一致。注意 H=8 粗模型对 c=1 给 1.342（<H=40/m=16 的 1.3915），是截断低估，趋势结论更可靠（见 §3.5）。
5. **[事实+推导] level-aspect 的"pair correlation"在文献中仍只是猜想（不是定理）**：Kandhil–Languasco–Moree, Math. Ann. 394 (2026) 43 明确以 GRH + **pair-correlation conjecture（Yıldırım Conjecture 1 / 他们的 Conjecture 2）** 为假设，且限制 q≤x^{1−ε}、T 范围；这不是可用来证 R 的无条件工具。已知 L'/L 矩（Young 四次矩=关于 L 非 L'；Ghosh=L'/L 在固定点 s=1 的高阶矩；Ihara=L'/L(1,χ)）全是**对角/平均/固定点**型，**给不出跨 χ 的 (logN)^{3/2} 型 operator-norm 估计——这是空白**（§4）。
6. **[推导] H_pair 的精确形式与对照**：kernel-theorist 的分解 $E_N=(2/\phi)\sum_\chi(|\tilde T_\chi\rangle\langle\tilde T_\chi|-\text{center})$ 若成立，且跨 χ 弱相关，则 R 可由"per-character 模型偏差 $\rho_N\lesssim(\sqrt S/2)(\log N)^{3/2}$"推出；文献中没有能给出该 ρ_N 或跨 χ Gram 的 (logN)^{3/2} 级结果（§5）。
7. **对 R 真伪的独立判断 [推测]**：R **可能为真（渐近，N₀~10⁶量级）、当前不可证、亦不可证伪；"很可能假/可能真空"的证据不足**。有限模型的 N^{−1/2} 标度实际上支持渐近 R；phase-4 的"若 λ_max 保持 O(1) 则 R 假"前提未被数据支持（2p 族 λ_max 在下降）。

---

## 1. LL Appendix A / Appendix B：论文到底声称了什么（逐条原文）

### 1.1 主文与假设（p.3–4、p.9、p.12）

- **[事实]** 主文：$N>e^{10}>22026$，$\alpha_N=1/\log N$，$\beta=1/8$（p.3、p.9、p.25）；"For every sufficiently large even N satisfying GRH(N)"（Hypothesis S/R，p.4）。
- **[事实]** p.12 §2.4.3：GRH 只给 $\|T_N\|_{HS}\ll(\log N)^2$（(2.24)）与宽度 $\eta^{GRH}\asymp S/(N\log N)$（(2.25)）；同页明确："This available norm bound is too large … S and R impose the required improvement."；"they do not measure cancellation between the components."；"**In fact, GRH alone already gives a zero-free region of the same form. Its width, however, falls short…**"（p.4）。
- **[事实]** 全文没有 "we verify R numerically" 之类的陈述；唯一数值是 Appendix B 的 N=30030 有限模型。

### 1.2 Appendix A：c 依赖与量词（p.53–54）

- **[事实] (A.1)**："Fix c > 0 and an even N ⩾ 4 with N > e^{10c}. Put α_{N,c}=c/log N, Δ_{N,c}=β−α_{N,c}." 并在 Prop A.1 中要求 "α_{N,c}<1/10"。
- **[事实] A.2 开头**："We establish the zero–norm correspondence for each realization and state its asymptotic consequences **with c fixed before N grows. This order of quantifiers is essential for the estimates.**"
- **[事实] A.2 中段**："For each fixed c > 0, preassign a positive h_c …"; (A.5) $R(N,c)\iff\|T_{N,c}\|\le\delta_N$；(A.6) $S(N,c;h_c)\iff\|T_{N,c}\|\le S(N)/(2h_c(N)\sqrt{1-\eta_{N,c}})$。
- **[事实] A.2 结尾（p.54）**："**The eventual hypotheses assert these conditions for all sufficiently large even N satisfying GRH(N), with lower bounds N₀(c) and N₀(c,h_c) on N. Neither these lower bounds nor the admissibility and divergence of h_c need be uniform in c. The main hypotheses are their specializations at c = 1. These conclusions concern sufficiently large N; covering every even N ⩾ 4 requires a separate check of the finite initial range.**"
- **[事实] A.3**（Lemma A.3）：$Q_\alpha\asymp_\phi N^{2\alpha}$，$\|\widehat T_{N,\alpha}\|\le M_\alpha=C((\log N)^2+\alpha^{-2})$，$Q_\alpha M_\alpha\asymp_\phi(\log N)^2e^{2c}(1+c^{-2})$；"A fixed positive c gives the best order available from these bounds; they do not select a universal optimal constant."（p.55）
- **[事实] A.4**（Prop A.4）：固定 N 时 $c\downarrow0$ 有 $\liminf c\|T_{N,c}\|\ge 2C_{N,\gamma}\log N/(1+\gamma^2)>0$，故 $R(N,c)$ 对足够小的 c 失效（p.55–56）；"This does not decide the eventual validity of R or S with c fixed before N tends to infinity."（p.57）
- **【推导/结论】** Appendix A 的逻辑是一个"对每个固定 c 都成立的、N₀(c) 可任意大的条件性框架"；"main hypotheses are their specializations at c=1"（主文结论对应 c=1）。**只要 N₀ 足够大，论文逻辑无内部矛盾；我们 phase-4 的 N=40022 有限模型反例不构成对论文逻辑的反驳**，因为它落在 N<N₀ 的"有限初始段"之内（尽管论文未声明 N₀）。

### 1.3 Appendix B：有限模型的自我限定（p.57–62）

- **[事实]** B.1–B.4 数值：N=30030，$\varphi=5760$，无序素数对 **905**（有序 1810），$\widehat J\approx0.05799599$，$\widehat D\approx0.29331844$，区间 $[904.725241,905.274759]\cap\mathbb Z=\{905\}$（(B.4)，p.60）。
- **[事实]** B.4 有限谱模型：2562 节点（两条边界线，高度 40，mesh 1/16），$C_{ij}=\sqrt{w_i}E_N(s_i,\bar s_j)/((1+s_i)(1+\bar s_j))\sqrt{w_j}$，$X_{30030}(q)=\det(I-4q(1-q)\delta_N^{-2}C^2)$；Prop B.5："**If ‖C‖≤δ_N**, every complex zero has real part 1/2."（条件句！）；数值极端特征值 $-0.353421$、$+0.357462$，$\|C\|/\delta_N\approx0.826864$。
- **[事实] p.62 逐字**："Cutoff stability and pointwise high-precision checks do not bound the full operator's truncation or discretization error. The figures illustrate the finite spectral model; **they do not certify Hypothesis R for T_{30030,1}**."
- **【推导】** 论文提供的是"有限模型示例 + 条件性推论"，**没有任何 N>e^{10} 的数值/模型验证主张**；因此 phase-4 以"论文声明范围内"为措辞批评 R 是不准确的：正确说法是"论文的 eventual 假设在测试范围内尚未达到；有限模型 N=40022 的 ratio>1 是 pre-asymptotic 现象"。

---

## 2. phase-4 报告需要修正的具体说法（逐条）

| # | phase-4 原文（来源） | 问题 | 修正 |
|---|---|---|---|
| 1 | "**Hypothesis R 很可能在论文自己声明的范围内就是假的**"（`phase4/0-phase4-报告.md` 标题/§5） | N>e^{10} 只是技术门槛；论文 N₀ 未量化且 Appendix B 自承不 certify | "有限模型在 N≈4×10⁴–2×10⁵ 给出 ratio>1（pre-asymptotic）；λ_max∝N^{−1/2} 标度暗示 R 可能在 N₀~3–7×10⁵ 后为真；论文逻辑（N₀ 未量化）不受威胁" |
| 2 | "λ_max 近似与模数无关（0.21–0.36）⇒ 若 λ_max 保持 O(1) 则 R 假"（`phase4/0-phase4-报告.md`、`independent-audit.md`） | 混淆了不同分解的模数；2p 族 λ_max 随 N 下降（40022:0.2757 → 60022:0.2073 → 100042:0.1661 → 200006:0.1247） | 正确不变量 C=λ_max√(N/S)≈O(1)（2p: 37–49；多小因子: 23–39）；ratio=C/log^{3/2}N→0（若 C 有界），R 渐近可能为真，N*≈3–7×10⁵ |
| 3 | "N=40022>e^{10} 在 LL 的工作范围内"（`spectral-numerics-extended.md` §7） | 把技术门槛当 asymptotic 范围 | 改为 ">e^{10} 只说明构造可用；'sufficiently large' 的 N₀ 未指定" |
| 4 | "若最终确认，LL 条件性定理不是未证明 Goldbach，而是假设不可满足、定理空虚"（`0-phase4-报告.md` §5） | 若 N₀~10⁶ 则 R 可能为真，不能称"假设不可满足" | 改为 "若 λ_max 的 N^{−1/2} 标度延续，R 在 N₀~10⁶ 后可能为真；当前数据不支持'最终为假'" |
| 5 | "λ_max=0.275724 > δ_N=0.198147 在 LL 框架内数值上表明 R 在 N=40022 处为假"（`spectral-numerics-extended.md` §6c） | 结论本身对 N=40022 的有限模型成立，但需加两条限定：(i) N=40022 在 unquantified N₀ 之前属"有限初始段"；(ii) 压缩+求积误差无严格界 | 保留为 "有限模型 pre-asymptotic 证据"，并注明 (i)(ii) |
| 6 | "λ_max 与模数无关 ⇒ R 作为 uniform 命题受严重数值压力"（同 §7 caveat (iv)） | 与 2p 下降趋势相反 | 删除该推断 |

**[事实] 保留正确的部分**：mesh（m=8/16/32/64）与高度（H=40/60/80）收敛使 N=40022 的有限模型 ratio=1.3915 可信（§3.1）；这一点 phase-4 做对了，是真实而重要的数值发现。

---

## 3. 独立复核：有限模型的数字与逻辑

### 3.1 S(N)、δ_N、有限模型数字（[数值]）

- **【推导/数值】** $S(N)=2C_2\prod_{p\mid N,p>2}\frac{p-1}{p-2}$：N=40022=2·20011（20011 素数）⇒ S=1.3203896=2C₂·20010/20009；N=39994=2·19997 ⇒ 1.3203897；N=60022=2·30011 ⇒ 1.3203676；N=100042=2·50021 ⇒ 1.3203500；N=200006=2·100003 ⇒ 1.3203368。与 `results_ext.txt` 一致。
- **【推导】** $\delta_N=\sqrt{S/N}(\log N)^{3/2}$（LL (1.5)）：40022 ⇒ 0.19814696；60022 ⇒ 0.17116985；100042 ⇒ 0.14192394；200006 ⇒ 0.10956867。均与表一致。
- **【数值/推导】** $c_N=1/S(N)$：我独立用 `kernels.Ptilde_values` 验证 N=40022：$w\hat P_N(w)$ 在 $w=10^{-2},10^{-3},10^{-4}$ 时为 0.76693, 0.75831, 0.75745 → $1/S=0.7573522$ ✓（KT2 的**摘要行** $c_N=1/(2C_2)$ 是笔误，主定理 1.3 正确；见 phase-4 audit §3.1）。
- **【数值】mesh 收敛**（`cache/results_mesh.txt`）：N=40022, H=40：m=8: λ=0.2761147；m=16: 0.2757214；m=32: 0.2757243；m=64: 0.2757243。H=40/60/80（m=16）：0.2757214/0.2765994/0.2769817。故有限模型值 0.27572（不是求积伪影）。
- **【数值】ratio**：0.27572/0.198147=1.3915；与 phase-4 一致。

### 3.2 全表：N、S、δ、λ_max、ratio、C（[数值]）

见 §6 表。关键：C=λ_max√(N/S)。2p 族：48.00 (40022), 36.98 (39994), 44.19 (60022), 45.71 (100042), 48.52 (200006)。多小因子族：22.81–38.61。**λ_max 不是模数无关；C 才近似有界（±12% 散布，2p 内 39994 vs 40022 相邻 p 差 30% 表明有限模型对具体 p 的敏感度）。**

### 3.3 Prop 5.3 的 $T_N$=T̃⊕0 转移论证：复核（[事实+推导]）

- **【事实】原文（p.29–30）**："Hermitian symmetry will then imply that ẽT_N vanishes on H_N^⊥. Its restriction T_N to H_N therefore has the same Hilbert–Schmidt norm as ẽT_N…"；证明中："Selfadjointness and the range inclusion imply that ẽT_N annihilates the orthogonal complement of the trace space. … Hence on L²(Γ_N)=H_N⊕H_N^⊥ it is T_N⊕0."
- **【推导】复核**：设 ẽT 为 L²(Γ_N) 上核积分算子；Prop 5.3 证其值域⊂H_N（迹子空间）。对 $g∈H_N^⊥$、任意 $f∈L²$：$\langle ẽTg,f\rangle=\langle g,ẽTf\rangle=0$（自伴+值域⊂H_N）⇒ ẽTg=0 ✓；限制在 H_N 上与 T_N 一致 ⇒ ẽT=T_N⊕0；故 HS 范数相同 ✓。**论证成立。**
- **【推导】对有限模型的含义**：若 $C$ 是 ẽT（或 T_N）在子空间 $V_M$（阶梯函数/节点）上的**压缩矩阵**，则 $\|C\|\le\|P_M T_N P_M\|+\text{求积误差}\le\|T_N\|+\text{求积误差}$。**因此 λ_max(C)>δ_N 只给出 "‖T_N‖ ≳ λ_max−err"；要断言 ‖T_N‖>δ_N 需要求积误差 err<λ_max−δ_N≈0.0775（=39% δ_N）。** mesh 收敛（m=16→32 变 0.001%）说明 err 数值上远小于该阈值，但**没有严格误差界**。**[事实] LL Appendix B 原文并未把 C 解释为压缩/求积，只说 X_{30030}(q)=det(I−…C²) 及条件式 Prop B.5**；phase-4 的"压缩/求积"解释是**[推导] 解释**，方向合理但需明确标为解释而非论文陈述。
- **【推测】结论**：phase-4 的 "N=40022 有限模型 ratio>1 ⇒ 数值上 R 在 N=40022 处失败" 作为**有限模型 + 压缩解释**的证据是成立的（误差数值上很小）；作为**论文声称范围内 R 为假**的证据则不成立（N₀ 未量化 + 非严格误差界）。

### 3.4 有限模型 vs 真 T_N：还能说什么（[推导+推测]）

- **[推导]** λ_max(C)≤‖P_M T_N P_M‖+err≤‖T_N‖+err，所以有限模型**不能证明** R；它只能给下界证据。相反，若 R 真而 λ_max(C) 平台，则说明有系统性的压缩/求积偏差（mesh m=8..64 稳定到 10^{-4} 使此可能性减小，但未排除 e.g. 高度 H 截断之外的模式；H=40→80 只 +0.45%，方向有利于"真值更大"）。
- **[推测]** 有限模型的 λ_max 与真 T_N 的关系：真 T_N 的核 E_N 在 H=40 之外可能有高 |t| 分量（LL (5.9) 的 $(1+|v|+|t|)^2$ 增长被解析性/权重压制），H 稳定说明贡献小；最大不确定项是**离散化/求积误差的严格界**与**E_N 本身数值误差**（phase-2 报告称 L'/L 误差 3.5e-14、D_N 2e-12、P̃ tail <1e-10，hermiticity 1e-16）。

### 3.5 c≠1（Appendix A 的可变条带）：能否让 ‖T_{N,c}‖≤δ_N 而 c=1 失败？（[数值-部分]）

- **【推导】允许范围**：Appendix A Prop A.1 要求 $\alpha_{N,c}=c/\log N<1/10$ 且 $N>e^{10c}$。对 N=40022（$\log N=10.5966$）：$0<c<1.0597$（并且 $\alpha<β=1/8$ 自动满足）。N=200006（$\log N=12.206$）：$c<1.2206$。
- **【数值】** 用只读 import + monkeypatch `model.Config`（α=c/logN，`sigma_lines` 同步），N=40022，H=8，mesh 1/8（**粗模型，仅作 c-相对比较**；baseline c=1 给 1.3423 vs H=40/m=16 的 1.3915，粗模型低估约 3.5%）：
  | c | α | λ_max | ratio | 备注 |
  |---|---|---|---|---|
  | 0.50 | 0.047182 | 0.668682 | **3.3747** | 明显更差 |
  | 0.75 | 0.070774 | 0.396170 | **1.9994** | 更差 |
  | 1.00 | 0.094365 | 0.265968 | **1.3423** | 粗模型 baseline |
  | 1.05 | 0.099083 | 0.248399 | **1.2536** | 允许范围内最大 c |
  结论：ratio 随 c↑ **单调下降**，但允许范围 $0<c<1.06$ 内最低仍 ≈1.25（>1 约 25%），**没有出现 ratio<1 的 c-逃逸**；c↓ 时迅速变差（c=0.5:3.37），与 Appendix A.4 的"c↓0 障碍"、A.3 的"c=1 是平衡阶"一致。若外推到 c≈1.2–1.3 才可能接近 1，但那样 α>1/10（超出 Prop A.1 的允许范围）且论文的 σ*=1/9 不再位于条带内。**建议 numerics 组用 H=40、m=16 复核 c=1.05 一点即可（约 1–2 min）**，趋势已足够清楚。
- **【推导】理论上**：A.3 已说明 $Q_\alpha M_\alpha$ 在 c=1 附近取最优 order；A.4 说明 c↓0 时 norm 发散。c 从 1 增加到 1.06 只把左边界右移 5%，不太可能把 40022 的 ratio 从 1.39 压到 1 以下（但非严格）。

---

## 4. 文献：level-aspect 的 pair correlation 与 L'/L 矩（逐条，含 URL/精确陈述）

### 4.1 level-aspect pair correlation：**仍是猜想，不是定理**

- **[事实]** N. Kandhil, A. Languasco, P. Moree, *Pair correlation of zeros of Dirichlet L-functions: a possible path towards the conjectures of Chowla, Elliott–Halberstam and Montgomery*, Math. Ann. 394 (2026), 43. DOI: 10.1007/s00208-026-03383-y（本地全文 `phase5/audit/pcdirichlet.pdf/.txt`）。摘要（逐字）："**Assuming the Generalized Riemann Hypothesis and a pair correlation conjecture for the zeros of Dirichlet L-functions, we establish the truth of a conjecture of Montgomery … and … the Elliott–Halberstam conjecture holds true.**"
- **[事实]** 该文引用并讨论 Yıldırım 的 **Conjecture 1 (Pair correlation for Dirichlet L-functions)**：对 $G_{\chi_1,\chi_2}^+(x,T)=\sum_{0\le\gamma_1,\gamma_2\le T}x^{i(\gamma_1-\gamma_2)}W(\gamma_1-\gamma_2)$ 及其字符和 $F_q^+(x,T)$，在 GRH 下要求 $F_q^+(x,T)\sim\frac{\phi(q)}{2\pi}T\log(qT)$，uniformly for $q\le\min(\sqrt x/\log^3x,x^{1-\eta}\log x)$、$x^\eta\le T<x/(q\log x)$（q=1 或素数）。他们的 Conjecture 2：$F_q(x,T),F_q^+(x,T)\ll\phi(q)T x^\varepsilon$，uniformly for $1\le q\le x^{1-\varepsilon}$、$x^\varepsilon\le T<x$。
- **【推导】** 注意 (i) 它是**猜想**；(ii) 检验函数/权重由 $W$ 固定且 Fourier 支撑受限（典型 pair correlation 的限制）；(iii) 范围 $q\le x^{1-\varepsilon}$、T 受限；(iv) 它是**平均/渐近**形式，不是逐 q/逐 N 的 operator-norm 或 4 点加性能量上界。**⇒ 不能用来证 R；方向上比 R 所需弱得多。**
- **[事实]** Özlük–Snyder, *On the Pair Correlation of Zeros of Dirichlet L-Functions*, in: Number Theory (de Gruyter), doi 10.1515/9783110848632-037（URL `https://www.degruyterbrill.com/document/doi/10.1515/9783110848632-037/html`）。**我们未能取得全文**（下载为空文件；标记为未核验）。按标题与后续引用，其内容为 Dirichlet L 零点的 pair correlation（t-aspect/受限检验函数）定理；不作为本报告的定量依据。
- **[事实]** 其余经典：Montgomery (1973) pair correlation 猜想（ζ）；Rudnick–Sarnak 的 n-level 猜想；这些都不是 Dirichlet level-aspect 的无条件定理。

### 4.2 L'/L 的矩/均值（level aspect）：全是别的东西

| 文献 | 精确陈述 | 与 R 所需的关系 |
|---|---|---|
| **Young**, *The fourth moment of Dirichlet L-functions*, arXiv:math/0610335, Ann. of Math. 173 (2011) 1–50 | "We compute **the fourth moment of Dirichlet L-functions at the central point for prime moduli**, with a power savings in the error term." 即 $\sum_{\chi\bmod q}{}^*|L(1/2,\chi)|^4$（q 素数）渐近。 | 关于 **L**（非 L'/L）的**对角/χ-平均**矩；不控制条带上的 L'/L，更不给跨 χ 双向相关。 |
| **Ghosh**, *Moments of Higher Logarithmic Derivatives and Exceptional Zeros in Cyclotomic Fields*, arXiv:2509.06390（v2 2026-07） | "…we prove arithmetic formulas for the higher derivatives $\mathcal L^{(r)}(1,\chi)$ and establish unconditional moment asymptotics for $P^{(a,b)}(\mathcal L^{(r)}(1,\chi))$ as χ runs over non-principal Dirichlet characters of large prime conductor." | L'/L 的矩，但**固定点 s=1**、且是 χ-族平均；不是条带 $1/\log N<\Re s<1/8$ 的 L²/算子估计，也不是跨 χ 4 点相关。 |
| **Ihara**, *On the logarithmic derivatives of Dirichlet L-functions at s=1*（京都 IMS preprint, URL 见 §7） | L'/L(1,χ) 的值分布/均值型结果（固定点 s=1）。 | 同上，固定点、非条带、非 operator。 |
| **Baluyot–Pratt**, *Dirichlet L-functions of quadratic characters of prime conductor at the central point*（zbmath 1505.11114 有索引） | 二次特征 L 在中心点的矩/值分布。 | 关于 L 值、非 L'/L、非跨 χ 4 点。 |
| **Mine**, *On certain mean values of logarithmic derivatives of L-functions and the related density functions*, arXiv:1805.11072（Funct. Approx. Comment. Math. 61 (2019) 179–199） | 某类 L 函数的 L'/L 均值与密度函数。 | 平均型，不是条带逐 χ 估计。 |
| **大筛（character large sieve）**：Gallagher 型不等式 $\sum_{\chi\bmod q}{}^*|\sum_{n\le N}a_n\chi(n)|^2\le(q+N)\sum|a_n|^2$（见 Kowalski 讲义 `large-sieve-families-torino.pdf` 的三角版本；Iwaniec–Kowalski, *Analytic Number Theory*, Ch. 7 为标准参考） | 对角/二次型平均。 | 只能给 LL Lemma 6.4 那类 χ-平均的二阶界（$\ll(\log N)^2$），**不能**给跨 χ 四阶 Gram 或 operator-norm。 |

- **【推导/结论】文献空白**：已知结果中**没有**任何一条能直接给出
  $$\rho_N\lesssim(\sqrt S/2)(\log N)^{3/2}\quad\text{或}\quad \|E_N\|_{op}\le\delta_N$$
  所需的"per-character 模型偏差"或"跨 χ Gram 的 (logN)^{3/2} 级估计"。最接近的 pair correlation 是**猜想**（KLM 2026），其形式也比所需弱（受限检验函数、χ-平均、非 operator norm）。**这是空白（gap），不是已有定理的推论。**

---

## 5. H_pair：R 的精确充分条件（并与文献对照）

### 5.1 分解与 HS 计算（[推导]；与 kernel-theorist 最新分解对齐）

设 $f_\chi(s)=g_\chi(s)/(1+s)$，$P_N=(2/\phi)\sum_{\chi\in X_N^-}|f_\chi\rangle\langle f_\chi|$。取"中心" $C_\chi$（每个 $\chi$ 的平滑模型贡献）使
$$\sum_{\chi\in X_N^-}C_\chi=\frac{\phi}{2}(D_N+K_N)\qquad\text{（从而 }(2/\phi)\sum_\chi C_\chi=D_N+K_N\text{）},$$
并令 $\widetilde T_\chi=|f_\chi\rangle\langle f_\chi|-C_\chi$，则精确地
$$E_N=P_N-D_N-K_N=\frac{2}{\phi}\sum_{\chi\in X_N^-}\widetilde T_\chi .$$
于是
$$\|E_N\|_{HS}^2=\frac{4}{\phi^2}\Bigl[\sum_\chi\|\widetilde T_\chi\|_{HS}^2+\sum_{\chi\ne\psi}\langle\widetilde T_\chi,\widetilde T_\psi\rangle_{HS}\Bigr].$$
令
$$\rho_N^2:=\frac{1}{\phi}\sum_{\chi\in X_N^-}\|\widetilde T_\chi\|_{HS}^2\quad(\text{per-character mean-square deviation, normalized by }\phi).$$
若**弱相关假设**
$$(W)\qquad \sum_{\chi\ne\psi}\langle\widetilde T_\chi,\widetilde T_\psi\rangle_{HS}\le\varepsilon\sum_\chi\|\widetilde T_\chi\|_{HS}^2\qquad(\varepsilon<1),$$
则
$$\|E_N\|_{HS}\le\frac{2}{\sqrt\phi}\rho_N\sqrt{1+\varepsilon}.$$
因此**充分条件**：
$$(H_{pair})\qquad \rho_N\le\frac{\sqrt\phi}{2}\cdot\frac{\delta_N}{\sqrt{1+\varepsilon}}=\frac{\sqrt{\phi S/N}}{2}\cdot\frac{(\log N)^{3/2}}{\sqrt{1+\varepsilon}}\ \le\ \frac{\sqrt S}{2}(\log N)^{3/2}\quad(\text{用 }\phi(N)\le N).$$
**[推导] 注意**：$H_{pair}$ 给出的是 $\|E_N\|_{HS}\le\delta_N$，比 $R$（operator norm）更强，因此 $H_{pair}\Rightarrow R$。与论文的三角法（$(\log N)^2$）相比，这里把目标降到 $(\log N)^{3/2}$（乘常数 $\sqrt S/2$）——正好是 phase-2 的 $\|D_N+K_N\|_{HS}$ 真阶，因此 $H_{pair}$ 必须同时包含（i）per-character 的 $\log^{1/2}$ 节省与（ii）跨 χ 的弱相关。

### 5.2 与已知文献的对照（[事实+推导]）

- **(W) 弱相关**：展开后 $\langle\widetilde T_\chi,\widetilde T_\psi\rangle$ 是**跨特征标的零点四阶加性能量**（KT2 §3）。已知最接近的是 pair correlation of Dirichlet L zeros（KLM 2026 的 Conjecture 1/2）——**仍是猜想**，且为受限检验函数的平均形式；大筛只给对角项。**无已知定理 ⇒ (W) 无法引用。**
- **per-character 偏差 $\rho_N$**：需要条带上 $L'/L$ 的**逐 χ** 二阶量减去平滑模型后的 $(\log N)^{3/2}$ 界。LL Lemma 6.4 只给 χ-平均的 $(\log N)^2$；G1（逐 χ $(\log N)^2$，若真）仍差 $\log^{1/2}$；已知 L'/L 矩（Ghosh/Ihara/Young）与条带模型偏差无关。**无已知定理 ⇒ $\rho_N$ 无法引用。**
- **结论**：$H_{pair}$ 是一个**新的、比已知任何 pair-correlation/moment 结果都强且不同**的估计；文献空白。**[推测]** 它可能可以从（a）逐 χ 显式公式 + GRH 零点计数 +（b）跨 χ 二阶矩的大筛/谱方法组合得到，但需要新的工作（不是现有文献的推论）。

### 5.3 "paper 三角法 vs $H_{pair}$"

- **论文三角法**：$\|T_N\|\le\|P_N\|_{HS}+\|D_N\|_{HS}+\|K_N\|_{HS}\ll(\log N)^2$（LL (6.7)），baseline $=(\log N)^2$。
- **$H_{pair}$ 路线**：直接对残差 $E_N$ 做 HS 估计，目标 $\|E_N\|_{HS}\le\delta_N=(\log N)^{3/2}\sqrt{S/N}$。由 §5.1，若跨 χ 弱相关 (W)，则 $\|E_N\|_{HS}\le(2/\sqrt\phi)\rho_N$，故充分条件是
  $$\rho_N\le\frac{\sqrt\phi}{2}\delta_N=\frac{(\log N)^{3/2}\sqrt{\phi S/N}}{2}\le\frac{\sqrt S}{2}(\log N)^{3/2}\quad(\text{用 }\phi(N)\le N).$$
  **所以目标正是 $\rho_N\lesssim(\sqrt S/2)(\log N)^{3/2}$**（比论文三角法的 $(\log N)^2$ 低 $\log^{1/2}N$；对 2p 族 $\sqrt{\phi S/N}\approx\sqrt S$，与 Lead 的表述一致）。注意 $H_{pair}$ 给的是 **HS 范数**界（$\ge$ operator norm），故 $H_{pair}\Rightarrow R$；它绕过了 no-triangle 天花板（后者只针对 $P_N,D_N,K_N$ 分量分解）。
- **[事实] 关键点**：这条 $H_{pair}$ 路线**绕过了 no-triangle 天花板**（后者只针对 $P_N,D_N,K_N$ 分量分解；$E_N$ 本身是残差），所以它在逻辑上是正确方向；但它要求的 $\rho_N$ 是**每特征标的 $(\log N)^{3/2}$ 级模型偏差 + 跨 χ 弱相关**，现有文献没有。

---

## 6. 数据表（[数值]，来源 `phase2/spectral/cache/results_ext.txt`、`results_mesh.txt`）

| N | 分解 | S(N) | δ_N | λ_max | ratio | C=λ_max√(N/S) | C=log^{3/2}N 的 N* |
|---|---|---|---|---|---|---|---|
| 30030 | 2·3·5·7·11·13 | 5.1212553 | 0.4323102 | 0.3574618 | 0.8269 | 27.37 | ~9e3 |
| 39270 | 2·3·5·7·11·17 | 5.0074496 | 0.3885049 | 0.3491318 | 0.8987 | 30.92 | ~2e4 |
| 43890 | 2·3·5·7·11·19 | 4.9706301 | 0.3719251 | 0.2427583 | 0.6527 | 22.81 | ~3e3 |
| 46410 | 2·3·5·7·13·17 | 4.9164051 | 0.3625301 | 0.2889380 | 0.7970 | 28.07 | ~1e4 |
| 53130 | 2·3·5·7·11·23 | 4.9180309 | 0.3453018 | 0.2871284 | 0.8315 | 29.84 | ~1.5e4 |
| 67830 | 2·3·5·7·17·19 | 4.7718049 | 0.3112192 | 0.2720124 | 0.8740 | 32.43 | ~2.6e4 |
| 72930 | 2·3·5·11·13·17 | 4.5522269 | 0.2960235 | 0.2665960 | 0.9006 | 33.74 | ~3.4e4 |
| 90090 | 2·3·5·7·11·13 | 5.1212553 | 0.2905336 | 0.2910724 | 1.0019 | 38.61 | ~9e4 |
| 102102 | 2·3·7·11·13·17 | 4.0970042 | 0.2481251 | 0.1913455 | 0.7712 | 30.21 | ~1.6e4 |
| 30018 | 2·3·5003 | 2.6411753 | 0.3105042 | 0.2932241 | 0.9443 | 31.26 | ~2e4 |
| **40022** | **2·20011** | 1.3203896 | 0.1981470 | **0.2757214** | **1.3915** | 48.00 | **5.4e5** |
| 39994 | 2·19997 | 1.3203897 | 0.1981967 | 0.2125060 | 1.0722 | 36.98 | ~6.6e4（敏感离群） |
| **60022** | **2·30011** | 1.3203676 | 0.1711699 | **0.2072516** | **1.2108** | 44.19 | **2.7e5** |
| **100042** | **2·50021** | 1.3203500 | 0.1419239 | **0.1660613** | **1.1701** | 45.71 | **3.6e5** |
| **200006** | **2·100003**（H=20） | 1.3203368 | 0.1095687 | **0.1246573** | **1.1377** | 48.52 | **6.0e5** |
| 40022 H=60 | | | | 0.2765994 | 1.3959 | — | |
| 40022 H=80 | | | | 0.2769817 | 1.3979 | — | |
| 40022 m=8 | | | | 0.2761147 | 1.3935 | — | |
| 40022 m=32 | | | | 0.2757243 | 1.3915 | — | |
| 40022 m=64 | | | | 0.2757243 | 1.3915 | — | |

**[推导] 读表**：
- 2p 族 λ_max 随 N 下降约 $N^{-1/2}$（40022→200006：λ 0.2757→0.1247，√N 比 2.24，λ 比 2.21），C≈37–49 近似常数（±12%，39994 为离群；H=20 对 200006 略低估）。
- 多小因子族 C≈23–39（明显小于 2p），ratio 多数 <1；90090 的 1.0019 是边缘。**2p 是最坏族**（S 最小 ⇒ δ_N 最小）。
- 若 C 有正极限，则 ratio=C/log^{3/2}N→0，**R 渐近为真**；N*（C=log^{3/2}N）≈3×10⁵–7×10⁵（2p 族），与 Lead 的"3–7×10^5"一致。
- 若 C 缓慢增长（如 ~log^a N, a<3/2），ratio→0 仍成立；若 C~log^{3/2}N 则 ratio 有界>1（R 最终假）。**现有数据（N≤2×10⁵）不能区分**；建议 probe 更大 N（多小因子、φ 可控的模数，例如 $2\cdot3\cdot5\cdot7\cdot11\cdot13\cdot17\cdot19=9,699,690$ 的若干倍数、或 $2\cdot p$ 无法到 1e6 因 φ=N），以检验 C 是否有极限。

---

## 7. 对 R 真伪的独立判断（[推测]，含理由）

1. **R 可能为真（渐近）**：有限模型显示 C=λ_max√(N/S) 在 2p 族约 37–49、多小因子族 23–39；如果这是真 T_N 的标度（λ_max≈C√(S/N)），则 ratio=C/log^{3/2}N→0，R 对所有 $N\ge N_0\approx3$–$7\times10^5$ 成立。**这与论文 unquantified 的 "sufficiently large" 完全兼容（N₀(c), N₀(c,h_c) 可任意大）。**
2. **但“可证”目前没有**：证明 R 需要 $\|E_N\|_{op}\le\delta_N$，即 §5 的 $H_{pair}$（per-character $(\log N)^{3/2}$ 偏差 + 跨 χ 弱相关）。文献中：(i) level-aspect pair correlation 仍是猜想（KLM 2026）；(ii) L'/L 矩都是对角/固定点/平均；大筛只给对角。**⇒ 空白，不是已有定理的推论。**
3. **“可能真空”目前没有证据**：phase-4 的"若 λ_max 保持 O(1) 则 R 假"前提被数据否定（2p 族 λ_max 下降）；N=40022 的 ratio>1 属于 pre-asymptotic。若要在更大 N 上确认真空性，需要 (a) 严格求积/压缩误差界把有限模型升级为下界（见 §3.3），(b) 大 N 数据（N≥10^6）。目前两者都没有。
4. **对论文逻辑的判断**：论文的 Theorems 1.1/1.2 是**条件命题**；若 R/S 在某个大 N₀ 后为真，它们成立（但 N₀ 无量化，不可用于"所有≥4"的 Goldbach）；若 R/S 最终为假，则定理"空虚"（假设不可满足）——但**当前既未证明真也未证明假**。**phase-4 的"很可能假/范围内假"必须撤回/降级为"pre-asymptotic 数值现象 + N₀ 可能很大"。**

---

## 8. 给 Lead 的修改清单（具体文件/句子）

1. `phase4/0-phase4-报告.md` 标题与 §0 第 3 条："发现 Li–Liu 谱假设 R 的有限模型反例"/"很可能在论文自己声明的范围内就是假的" → 改为 "有限模型在 N≈4×10⁴–2×10⁵ 的 pre-asymptotic 失败；λ_max∝N^{−1/2} 暗示 N₀~3–7×10⁵ 后可能为真；论文 N₀ 未量化，故不推翻其逻辑"。
2. `phase4/0-phase4-报告.md` §5 第 3 条"若最终确认…假设不可满足" → 加 "未确认；新数据反而不支持最终为假"。
3. `phase2/spectral-numerics-extended.md` §7 "λ_max 与模数无关…严重数值压力" → 改为 "λ_max 沿 2p 族随 N 下降；正确不变量 C≈O(1)⇒ratio→0；R 可能渐近为真（N₀~10⁶）"。
4. `phase4/independent-audit.md`（我上一轮报告）§1.5/§4 的"若 λ_max 保持 O(1) 则 R 假" → 加 "但 2p 族数据表明 λ_max∝N^{−1/2}，故上述前提不成立；R 渐近可能真"。
5. 所有报告中的 "N=40022>e^10 在论文范围内" → 改为 "e^10 是技术门槛，'sufficiently large' 的 N₀ 未量化（Appendix A p.54 明确允许 N₀(c) 任意大）"。
6. 保留 phase-4 的正确部分：有限模型 mesh/height 收敛、ratio 1.3915 是真值、S/δ/c_N 验证、Prop 5.3 转移论证（但标注"压缩+求积"为解释而非论文陈述；求积误差无严格界）。
7. c≠1 补充（已完成，H=8,m=8 粗模型）：c=0.50/0.75/1.00/1.05 → ratio 3.375/1.999/1.342/1.254；在允许范围 $0<c<1.06$ 内单调下降但始终 $>1$（最低 ≈1.25），**无 c-逃逸**；与 A.3/A.4 一致。建议 numerics 组用 H=40/m=16 复核 c=1.05 一点。

---

## 9. 复现命令与文件

- 本报告 c≠1 脚本：`phase5/audit/c_variation.py`（H=20 版，未完成）、`phase5/audit/c_quick.py`（H=8,m=8 快速版，运行中）；日志 `phase5/audit/c_quick.log`。运行方式：`cd phase5/audit && PYTHONDONTWRITEBYTECODE=1 python3 -u c_quick.py`（只读 import phase2/spectral 的 model/lmat/kernels/chars，monkeypatch `model.Config` 的 α）。
- 有限模型数据：`phase2/spectral/cache/results_ext.txt`、`cache/results_mesh.txt`、`phase2/spectral-numerics-extended.md`。
- 文献本地副本：`phase5/audit/pcdirichlet.pdf/.txt`（KLM 2026，已抓取全文并核对 Conjecture 1/2 原文）；`pcdirichlet.txt` 为全文文本。
- **未完成/未核验**：(a) c=1.0/1.05 的完整运行（截稿时 pending）；(b) Özlük–Snyder 全文未能下载（de Gruyter 返回空文件）——本报告只按标题/后续文献描述，不引其定量内容；(c) Baluyot–Li 的具体论文未能定位（arXiv API 查询超时；Baluyot 主页公开列表未逐一核对）——本报告只列已核实的 Young/Ghosh/Ihara/Baluyot–Pratt/Mine。

## 10. URL 清单

- LL 论文：<https://mrc.sdu.edu.cn/english/info/1018/1514.htm>（PDF 本地 `/home/kiler/rh-work/liu-goldbach.pdf`）。
- Kandhil–Languasco–Moree（Math. Ann. 2026）：doi 10.1007/s00208-026-03383-y；本地全文 `phase5/audit/pcdirichlet.pdf`（含 Yıldırım Conjecture 1、其 Conjecture 2、GRH 条件声明的逐字文本）。
- Young 四次矩：<https://arxiv.org/abs/math/0610335>；Ann. of Math. 173 (2011) 1–50。
- Ghosh：<https://arxiv.org/abs/2509.06390>。
- Ihara：<https://www.kurims.kyoto-u.ac.jp/~kenkyubu/emeritus/ihara/Publications-and-Recent-Preprints/RecentArticles/pdf-files/IMS.main.pdf>。
- Mine：<https://arxiv.org/abs/1805.11072>。
- Özlük–Snyder 章节（未能取全文）：<https://www.degruyterbrill.com/document/doi/10.1515/9783110848632-037/html>。
- Baluyot–Pratt（zbmath 索引）：<https://zbmath.org/pdf/1505.11114.pdf>。
- 大筛参考：E. Kowalski, *The large sieve and L-functions over finite fields*（讲义）<https://people.math.ethz.ch/~kowalski/large-sieve-families-torino.pdf>；Iwaniec–Kowalski, *Analytic Number Theory*, AMS Colloq. Publ. 53 (2004), Ch. 7；Bhowmik–Grimmelt 综述（本地 `phase5/lit/exc_7_12.txt`）引用 Gallagher, *A large sieve density estimate near σ=1*, Invent. Math. 11 (1970) 329–339。
- 全局动态：Alpöge/MIT 验证页 <https://math.mit.edu/~drew/grh/>（本地 `/home/kiler/rh-work/mit/`）。

---

## 附录 A：关键引文（逐字，含页码）

1. **LL p.54（Appendix A.2 量词）**："The eventual hypotheses assert these conditions for all sufficiently large even N satisfying GRH(N), with lower bounds N0(c) and N0(c, hc) on N. Neither these lower bounds nor the admissibility and divergence of hc need be uniform in c. The main hypotheses are their specializations at c = 1. These conclusions concern sufficiently large N; covering every even N ⩾ 4 requires a separate check of the finite initial range."
2. **LL p.62（Appendix B 结尾）**："Cutoff stability and pointwise high-precision checks do not bound the full operator's truncation or discretization error. The figures illustrate the finite spectral model; they do not certify Hypothesis R for T30030,1."
3. **LL p.60 Prop B.5**："If ‖C‖⩽δN, every complex zero has real part 1/2."（条件句）
4. **KLM 2026 摘要**："Assuming the Generalized Riemann Hypothesis and a pair correlation conjecture for the zeros of Dirichlet L-functions, we establish the truth of a conjecture of Montgomery … and … the Elliott–Halberstam conjecture holds true."
5. **Young 2011 摘要**："We compute the fourth moment of Dirichlet L-functions at the central point for prime moduli, with a power savings in the error term."
6. **Ghosh 摘要**："…establish unconditional moment asymptotics for P^{(a,b)}(L^{(r)}(1,χ)) as χ runs over non-principal Dirichlet characters of large prime conductor."

## 附录 B：审计范围声明

- 已核对：LL Appendix A/B 原文（p.53–62）、footnote/量词；finite-model 表与 mesh/height 数据；S/δ 公式与数值；c_N=1/S(N) 数值；Prop 5.3 转移论证；c≠1 粗模型部分结果；文献摘要/部分全文（KLM 全文逐字提取；Young/Ghosh/Ihara/Mine 摘要；Özlük–Snyder 全文未得）。
- 未完成：c=1.0/1.05 完整运行、大 N（≥1e6）检验、严格求积误差界、phase2/spectral-numerics 的代码逐行审计（本轮只按 phase-4 报告与结果表核对数字，未重跑其 model.py；数值可信度依据他们报告的 validation 误差）。
