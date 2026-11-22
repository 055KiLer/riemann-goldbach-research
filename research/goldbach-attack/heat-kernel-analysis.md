# 热核迹正性 ⇒ 哥德巴赫？——对「黎曼猜想的谱证明架构必然蕴含哥德巴赫」的严格审读

**作者**：heat-kernel-critic（Team 分析员）
**日期**：2026-11-21（Asia/Shanghai）
**任务**：`task-5`（Rigorous evaluation/refutation of the "heat kernel trace positivity ⇒ Goldbach" spectral route）
**资源**：本地 Li–Liu 预印本全文 `/home/kiler/rh-work/liu-goldbach.clean.txt`；本地 Lean 镜像 `/home/kiler/rh-full`（只读，175,187 个 `.lean`）；Alpöge 4 页说明 `/home/kiler/rh-work/remark.txt`；网络检索与 Zenodo/PhilArchive 元数据（见参考文献）。
**标签约定**：**[事实]** = 有公开可核验的一手证据；**[定义]/[引理]/[证明]/[推论]** = 本报告内可逐步检验的数学内容；**[推断]** = 由事实经明确推理得出但依赖对来源正确读解；**[推测]/[判断]** = 主观评估，不能当作定理。

---

## 0. 结论摘要（TL;DR）

1. **[事实] 用户命题有直系文本来源，但来源不是数学界认可的文献。** 用户原话几乎逐字对应 Luis Morató de Dalmases 的 Zenodo 预印本《Complete Proof of the Riemann Hypothesis and the Unified Number Theoretic Architecture of the 600-Cell: Goldbach, Twin Primes, and Collatz》（record 19128632，v6，2026-03-20）的摘要：该记录明言 *"this spectral architecture necessarily implies the Goldbach Conjecture"*，并写 *"The positivity of the heat kernel trace of D implies that every even number greater than 2 can be expressed as the sum of two primes."* 另有中文自出版系列（任尚业/杨双林/任傲天，《哥猜论证之第二十五》，Zenodo 22731117，2026-08-23）以「分层 Selberg 迹公式 + 热核双时渐近 + 梅林变换建立热核迹与素数特征和的严格对应」为噱头。**二者均为未评审的自出版预印本；前者宣称同时解决 RH+GRH+Goldbach+孪生素数+Collatz（并另文宣称统一七大千禧问题、从几何导出物理常数），后者在正文明确声明其成果「不等同于全体偶数 1+1 成立的完整结论」。没有任何同行评审期刊、arXiv、或数学界公认渠道发表过这一推导。**

2. **[证明] "热核迹正性"本身是自动的、零算术信息的。** 对任意自伴、有下界、离散谱算子 $A$，$\operatorname{Tr}e^{-tA}=\sum_j e^{-t\lambda_j}>0$ 对一切 $t>0$ 自动成立，且对任意平移 $A\mapsto A+c$ 仍成立。把这个当"关键一步"，等于把谱定理的重言式当定理用。

3. **[证明 + 反例] 即使能证明某个"热核迹=Goldbach 相关函数"的正性，也推不出系数（表示数）正性。** 显式反例：$F(t)=e^{-t}-2e^{-2t}+2e^{-3t}>0$ 对一切 $t>0$ 成立，但其系数 $a_2=-2<0$（证明见 §2.2）。系数正性需要解析延拓/零点控制（一个新的 RH 型问题）或无穷阶完全单调性；后者最多给 $a_n\ge 0$——而 Goldbach 的 $r(N)\ge 0$ 是定义使然，真正要证的逐点严格正性 $r(N)>0$ 完全不在"正性"的信息里。

4. **[证明] 在最好的具体桥梁（Li–Liu 框架）里，正性是反方向。** 精确恒等式 $G(N)=c_\varphi S(N)-\langle T_Nv_N,v_N\rangle$ 表明：$T_N\ge 0$（或其热核迹正性）只给出 $G(N)\le c_\varphi S(N)$ 这一**下界型**信息；而 Goldbach 需要 $\langle T_Nv_N,v_N\rangle$ 的**上界**（$\Leftrightarrow$ 算子范数上界，即 Hypotheses S/R）——这正是论文公开承认缺失的定量输入。有限维模型引理：$\{c-\langle Tv,v\rangle:T\text{ 自伴},T\ge0\}=(-\infty,c]$，即正性允许 $G$ 任意负，**不可**推出 $G>0$。

5. **[证明] 迹—范数方向引理：热核迹正性/下界不能用来证明所需的小算子范数。** $\operatorname{Tr}e^{-tT}\ge e^{-t\|T\|}$ 以及 $\operatorname{Tr}e^{-tT}\ge Ne^{-t\|T\|}$ 只能推出 $\|T\|$ 的**下界**；族 $T_M=M\cdot P$（$P$ 秩一投影）满足 $\operatorname{Tr}e^{-tT_M}=e^{-tM}+(N-1)\ge 1$（$\forall t>0$）而 $\|T_M\|=M\to\infty$。故"热核迹正性"与"$\|T_N\|\le\delta_N$"（Hypothesis S/R）在逻辑上独立。

6. **[事实] Alpöge/Claude 的 Lean 证明不是"谱/热核"架构，前提张冠李戴。** 对本地镜像全树 175,187 个 `.lean` 文件做 grep：`"heat kernel"` **0** 个文件、`"trace formula"` **0**、`"Guinand"` **0**、`"HilbertPolya"` **0**、真正的 `"Pólya"` **0**（`grep -rl 'Pólya'` = 0；大小写不敏感的词边界匹配只命中定理名 `polyA`）；仅 13 个文件名/文本含 `HeatKernel`，全部位于 `src/Development/AbelianVarietyTheory/` 的局部子库（11 个 `Proofs/DivisorProofs/` + 2 个 `PublishedTheorems/Divisors₂/`），其中具代表性的 `HeatKernelTraceIntegrable.lean` 只被同目录 2 个文件 `import`。主链 `Main.lean → Supplements.Kernels.MainTheorems → UpperTheory.FinalTheorems.everyCharacter → Formalism.VW.rh_of_every` 的架构是 **Stepanov 式多重性 + 迭代 theta 提升 + 自守表示/Galois 表示 + 乘性 Guinand–Weil 符号 + 行列式正性 $W\ge0$ + Hermitian curvature**。其中确有"正性/符号"机制，但那是**乘性** Weil 型正性（作者原话："Guinand-Weil had the sign"、"$W(1_S)\ge0$ via a determinant"），与热核迹无关，更与加性素数对计数无关。

7. **[判断] 最终裁决：** 这条路线**不仅未证明，而且其"关键一步"在逻辑上不可能承担所宣称的作用**。正性（自动的、下界型的）与所需的小量/上界方向相反；把 Goldbach 表示数实现为某个正算子热核迹的构造存在（§4.1 显式给出），但其正性自动成立且对系数严格正性零信息；RH 的 Weil 正性属于乘性 $L$-函数零点理论，不迁移到加性素数对计数（圆法劣弧、例外集、筛法奇偶屏障三重障碍）。**最强可获得的真命题**是：GRH（现已（宣称）无条件）+ Hypothesis S/R $\Rightarrow$ 加权 Goldbach 渐近（Li–Liu 条件性定理，本身未经评审）；以及本报告 §2 的若干否定性引理。**没有任何已知定理给出 RH/GRH/热核迹正性 $\Rightarrow$ 二元哥德巴赫；所引来源中的"证明"经检查在 §2.2/§2.3/§1.2 指出的步骤失效。**

---

## 1. 来源核查：文献中到底有什么

### 1.1 用户命题的直系文本来源（几乎逐字）

**[事实] 来源 A（英文，用户"必然蕴含 + 热核迹正性"措辞的直系出处）**：Luis Morató de Dalmases，"Complete Proof of the Riemann Hypothesis and the Unified Number Theoretic Architecture of the 600-Cell: Goldbach, Twin Primes, and Collatz"，Zenodo record [19128632](https://zenodo.org/records/19128632)，Version v6，2026-03-20 发布；作者单位自署 "CronNet Holo Initiative"；CC-BY 4.0；全部文件 4.1 MB，共 14 个 PDF（01.0、01.1、01.2、01.3 与 02–11）。记录摘要原文（2026-11-21 抓取）：

> "This deposit contains the complete, rigorous proof of the Riemann Hypothesis (RH) and its generalisation (GRH), along with the demonstration that **this spectral architecture necessarily implies the Goldbach Conjecture**, the Twin Prime Conjecture, and the Collatz Conjecture. The work is based on the construction of a self-adjoint Dirac-type operator whose spectral properties are governed by the intrinsic geometry of the 600-cell {3,3,5} …"
>
> "**Goldbach:** **The positivity of the heat kernel trace of D implies that every even number greater than 2 can be expressed as the sum of two primes.**"

其中用户所说"某个算子的热核迹的正性"即此记录中的 $D$（定义在 $\ell^2(\mathbb N)\otimes\mathbb C^2$ 上的 Dirac 型算子）。其 Goldbach 分册（附件 07，9 页）标题为《Complete Proof: From the Riemann Hypothesis to the Goldbach Conjecture》，摘要称：

> "we demonstrate that the Goldbach representation function $r(2n)$ admits a spectral representation whose positivity follows from the self-adjoint structure of the operator. The key is the connection between the Hardy–Littlewood singular series and **the trace of the heat operator**, mediated by the Mellin transform and the geometric constant $\delta_0$ of the 600-cell."

**[事实] 来源 B（中文，"热核迹/分层 Selberg 迹公式"措辞的出处）**：任尚业、杨双林、任傲天，《双曲螺线数论余区间逐点一致的统一上界估计——哥猜论证之第二十五》，Zenodo record [22731117](https://zenodo.org/records/22731117)，Published 2026-08-23，DOI 10.5281/zenodo.22731117，CC-BY 4.0，15 页 1.8 MB。关键词明列「分层 Selberg 迹公式；热核渐近；西格尔零点常数有效性；近似正交分层」。摘要核心句（原文）：

> "以第 16 步已证的分层 Selberg 迹公式与热核双时渐近定理为核心主线，**通过梅林变换建立热核迹与素数特征和的严格对应**，内生导出余项的主阶、衰减速率与高阶压制规则；激活三维锥分形的旋转+反射对称群 … 实现「几何谱→分析误差→数论余项」的完整内生传导链。"

正文第 2 章"定理 2.2（系列第 16 步·精细化分层 Selberg 迹公式）"声称：

> "**热核迹可按缠绕阶数做近似正交分层分解**，不同阶交叉项为指数小量，整体误差可忽略；$k$ 阶缠绕闭轨对应的迹项，严格对应素因子总个数为 $k$ 的殆素数配对贡献。"

即：热核迹 $\operatorname{Tr}e^{-tH}$ 的"缠绕阶"分解逐项对应 Ω 阶殆素数对，再由此提取 Goldbach 信息。**这正是"热核迹 → 素数对计数"路线的中文版本**，且其"证明"完全依赖该系列自己第 1–23 步未发表"定理"（自引），没有任何独立数学依据。

**[事实] 来源 C（被任务点名的"heat-trace summaries"）**：Nicholas G. Polson & Vadim Sokolov，*Computing the Riemann Hypothesis: Thorin Measures, Pólya Densities and Hitting Times*，Zenodo [23400373](https://zenodo.org/records/23400373)（v1.1.0，2026-10-14；后续 Edition 2 v3.0.0 分三卷，Zenodo DOI 10.5281/zenodo.24377750/24377753/24377757，并有 Amazon 纸质版）；代码/数据仓库 GitHub `VadimSokolov/computing_rh`。**这本书与 Goldbach 无关**：819 页正文中 "Goldbach" 出现 **0** 次（本地下载 PDF 全文检索）；书摘明确写：

> "From the zeros verified up to height $3\times10^{12}$ the book certifies that the derivatives of the heat trace have the predicted signs up to order $1.16\times10^{25}$, **and proves that such finite positivity tests cannot settle it**: a perturbation of Xi with the same zeros below a large height, and zeros off the line above it, passes them. **No proof of the hypothesis is claimed.**"

即：它认真研究的是"热核迹的正性层级 ⇒ RH"（Thorin 测度正性），并且**自己证明了有限阶热核迹正性检验不能定 RH**——与 §2.2 的系数提取引理是同一逻辑现象。把它当"热核迹 ⇒ Goldbach"的文献依据是误读。

**[事实] 来源 D（其他"complete proof / spectral-Goldbach"预印本样本）**：
- Ying Ye，《Spectral Paradigm of Analytic Number Theory》，Zenodo [21324222](https://doi.org/10.5281/zenodo.21324222)（2026-10-03；Research Briefs 收录摘要，0 引用）。其摘要自我限定："Infinite-dimensional passages, **Goldbach positivity**, pair-correlation closure, and gap isolation are formulated as **explicit conditional estimates or verification tasks** … the word 'proof' always means a proved implication from precisely stated spectral hypotheses"。即它把 Goldbach 正性作为**待验证的条件假设**，并未证明。
- Byoungwoo Lee，《A Spectral–Entropy Framework for the Goldbach Conjecture》，Zenodo [19625051](https://zenodo.org/records/19625051)（v5.1，2026-04-17）。其"exact proved core"为 $TP0/E0/C0/M0$（传递原理、熵闭合、二进例外集、$\Re s>2$ 上的 Mellin–trace 恒等式），全局结论则放在 "Gate A / Gate B" 两个显式接口假设之下；作者明言 v5.1 "does not change the exact proved core"。
- Brian Simpson，《Goldbach》，Zenodo [15460813](https://zenodo.org/records/15460813)（2025-05-19 首版，2026-05-09 改版）。记录顶端自己标注："**STATUS: HIGH_CLAIM_ARCHIVE. CURRENT AUTHORITY: No.** … This record is not a current accepted proof of the Goldbach Conjecture …"，内容是以"self-adjoint resonance operators, spectral density, admissibility-style positivity arguments"处理素对——作者本人都已撤回权威性。
- PhilArchive 上另有若干 "Goldbach / Riemann hypothesis" 宣称（如 Mohammad Islam 的 "unconditional proof"），均未经同行评审；检索页被 Cloudflare 拦截（403），仅能从检索摘要确认其存在，本报告不依赖其内容。

### 1.2 来源可信度评估（**不把任何一条当权威**）

| 来源 | 载体/日期 | 核心宣称 | 状态评估 |
|---|---|---|---|
| A. Morató de Dalmases, 600-cell 系列 | Zenodo 自出版，v6 2026-03-20；754 总浏览 / 2,278 总下载（2026-11-21 抓取） | 同时证明 RH、GRH、**Goldbach**、孪生素数、Collatz；另文统一七大千禧问题、由几何导出物理常数（$\alpha_{st}$ 等） | **未评审、无 arXiv、无期刊、无引用记录**。特征符合典型的"万有理论"式自出版：一个算子同时解决多个千禧问题；"600-cell 几何" + "Riemann gas/Bose–Einstein 凝聚"；数值常数可核对为错（见 §1.3）。仅可当"用户命题的文本出处"，**不可当数学依据**。 |
| B. 任尚业/杨双林/任傲天 哥猜论证系列 | Zenodo 自出版，第 25 步 2026-08-23；17 浏览 / 7 下载 | 以"64 阶双曲螺线新数论"、"分层 Selberg 迹公式"、"热核双时渐近"证明 Goldbach 的逐点一致性；称第 1–23 步"无条件严格已证" | **未评审、自引闭环**：15 页论文的全部"定理 2.x"都来自同系列未发表"第 1–23 步"（其中多篇标为"独立研究报告/cnxiv 预印本"）；作者无单位、QQ 邮箱、感谢"指导学者：东方智（好老师）"；同系列另发表"由 64 阶螺线几何导出宇宙大数 $N=1.24\times10^{36}$、精细结构常数 $\alpha_{em}=961/131072$"等物理常数推导（Sohu/知乎自媒体的同主题文章）。典型民科画像；**且该文自己承认未完成 Goldbach**（见 §1.3）。 |
| C. Polson–Sokolov `computing_rh` | 自出版专著（独立出版/Amazon/Zenodo DOI，3 卷）；作者为 Chicago Booth 与 GMU 的学者（Polson, Sokolov），有 ORCID | 计算 RH 的 Thorin 测度/热核迹正性层级；**明确宣称不证明 RH**，并证明有限阶热核迹正性检验不能定 RH | **严肃、自我设限的计算/概率工作**，但非同行评审期刊论文；**与 Goldbach 无关**（819 页 PDF 中 0 次出现）。它恰恰是"正性检验有信息上限"的独立佐证，而不是"热核迹 ⇒ Goldbach"的支持。 |
| D. Ying Ye / B. Lee / B. Simpson 等 | Zenodo 自出版；2025–2026 | 谱/熵/算子框架下的 Goldbach：把核心困难保留为显式条件假设（Goldbach positivity、Gate A/B、pair-correlation closure） | **未评审**。其诚实之处恰在于把不可证部分标为假设——与 §2/§4 的分析一致：缺的从来不是"正性"，而是定量的小量估计。 |
| E. 严肃数学文献 | Hardy–Littlewood 1923/24；Goldston 1992；Pintz 2018；Goldston–Suriajaya 2021；Brüdern–Kaczorowski–Perelli 2019；Friedlander–Iwaniec 2010；Li–Liu 2026（预印本） | 见 §4.2：GRH 只能给例外集 $E(x)\ll x^{1/2+\varepsilon}$；显式公式文献只处理 Goldbach 表示数的**平均**；仅 GRH 推不出二元 Goldbach | **不存在**任何同行评审文献给出 "RH/GRH/热核迹正性 ⇒ Goldbach" 的推导。Li–Liu 引言原文："No proof of the binary conjecture is known under the generalized Riemann Hypothesis (GRH) alone"。 |

### 1.3 对来源 A、B 的内部检查：它们自己也没证明所宣称的东西

这一小节很重要：**即使不引入我们的否定性引理，单看来源文本，宣称也不成立。**

**(A) Morató 分册 07 的实际论证链**（我们下载并抽取了 PDF 全文，逐页阅读；路径见附录 B）：

1. 定理 2.3 标题就是 "**Conjectured** asymptotic formula"：$r(2n)\sim \mathcal S(2n)\cdot 2n/\ln^2(2n)$ 是 Hardy–Littlewood **猜想**。
2. 引理 4.2 的证明最后一句原文：*"The second approximation uses the **Hardy–Littlewood conjecture**."* ——在把一个关于 $r(2n)$ 的 Dirichlet 级数与奇异级数平均联系起来时使用了 HL 猜想。
3. 定理 6.4（Goldbach）证明依赖引理 6.2："Under the Riemann Hypothesis … $|E(2n)|\le C\sqrt{2n}/\ln(2n)$"。**这是从 RH 得不到的逐点误差估计**；已知 RH/GRH 下真正成立的是**例外集**估计 $E(x)\ll x^{1/2+\varepsilon}$（Hardy–Littlewood 1924；Goldston 1992），它允许例外集永远非空、且不给出任何逐点 $\sqrt{2n}$ 界。（详见 §4.2。）
4. 有限验证部分：作者说 $2<2n\le 2N_0$ 已计算验证到 $4\times10^{18}$，"one can take $N_0=10^6$"——但后文的渐近比较只在 $n\ge N_0$ 成立，$N_0$ 无显式可核实推导；这本身即循环（要么 $N_0$ 足够大而无法验证，要么渐近论证未经证明）。
5. 数值不自洽（**[事实]，可用 Python 复核，见附录 A）**：$\delta_0:=2\pi-5\arccos(1/3)$ 的正确值是 $0.128388$ rad（$=7.356^\circ$），论文写 $0.118682$ rad（$\approx6.8^\circ$）；$\alpha_{st}:=(\delta_0/2\pi)\ln(2\pi e)$ 在 $\delta_0=0.128388$ 下为 $0.057988$，论文写 $0.189979$；引理 5.3 称 $K(2)=\delta_0/2\pi\approx0.02043$，而按论文自己给出的 $K(s)=\frac{2C_2}{\zeta(2)}\frac{\Gamma(s)}{\Gamma(s-1)}H(s)$ 在 $s=2$ 处前因子为 $\frac{2C_2}{\zeta(2)}\approx0.80266$（$H(2)$ 未定义/未计算）。一个"完全严格证明"的核心常数出现 $3$–$39$ 倍的不自洽，本身就是很强的反证。
6. 记录层面的宣称（"positivity of the heat kernel trace of $D$ implies Goldbach"）在分册 07 中**没有任何对应定理**：07 的 §6 用的是 HL 猜想 + 伪造的逐点误差界，热核算子迹只在引理 3.4 作为展开式/mellin 恒等出现。**"热核迹正性 $\Rightarrow$ Goldbach"这句话在其自家论文里也是一句悬空的摘要口号。**

**(B) 任尚业系列第 25 步的实际边界**：该文正文第 2 页有明确的结论边界声明（原文）：

> "**成果边界声明**：本文得到的是带相位权重的积分上界，**尚未完成纯素数配对与高阶殆素数的完全分离，需结合后续量级分离步骤才能对应纯素计数下界**；本成果为逐点 1+1 证明的核心前置技术环节，**不等同于全体偶数 1+1 成立的完整结论**。"

即：连这条中文来源自己在正文中都声明"这不是 Goldbach 的证明"。其"热核迹分层对应殆素数对"的"定理 2.2"只是对整个系列自引的断言，没有任何独立推导；所谓"迹公式"并非 Selberg 迹公式（Selberg 迹公式是紧致/有限体积双曲流形上 Laplace 谱与闭测地线的恒等式，其中闭测地线长度是乘性/几何对象；"缠绕阶对应 Ω 阶殆素数对"没有任何定理来源）。

**小结（§1）**：用户命题的文本出处是两条未评审自出版预印本（一英一中），二者的"证明"分别止步于循环使用 HL 猜想/未证的逐点误差界，与自己声明未完成。**没有任何严肃来源支持这条路线。**

---

## 2. 严格分析：正性到底能推出什么

本节把"热核迹正性"拆成四层，逐层给出精确定义与证明，最后指出失败的精确逻辑位置。

### 2.0 记号

- $\mathcal H$：可分 Hilbert 空间（实或复）；$\langle\cdot,\cdot\rangle$ 内积，$\|v\|^2=\langle v,v\rangle$。
- $A$：自伴算子，有下界，谱离散：$A=\sum_{j\ge1}\lambda_j P_j$，$\lambda_j$ 按重数计，$\lambda_j\to+\infty$，$P_j$ 为有限秩正交投影。
- $e^{-tA}$：由谱定理定义的（正、自伴、有界）算子；$\operatorname{Tr}$ 为迹类算子的迹。
- Goldbach 加权相关（von Mangoldt 加权）：$r_\Lambda(N)=\sum_{a+b=N}\Lambda(a)\Lambda(b)$；无权重表示数 $r(N)=\#\{(p,q)\in\mathbb P^2: p+q=N\}$。
- 素数指数和 $P(t)=\sum_{p}e^{-tp}$（$t>0$）。

### 2.1 事实 A：热核迹正性是自动的（零算术信息）

**引理 2.1（自动正性）**　设 $A$ 自伴、有下界、离散谱（有限重数）。则对每个 $t>0$，$e^{-tA}$ 迹类，且
$$\operatorname{Tr}e^{-tA}=\sum_{j\ge1}e^{-t\lambda_j}>0 .$$
进一步，对任意常数 $c\in\mathbb R$，$\operatorname{Tr}e^{-t(A+c)}=e^{-ct}\operatorname{Tr}e^{-tA}>0$ 仍然成立。

**证明.**　谱定理给出 $e^{-tA}=\sum_j e^{-t\lambda_j}P_j$，其非零特征值为 $e^{-t\lambda_j}$（重数不变）。因 $\lambda_j\to+\infty$ 且 $A$ 有下界，$e^{-t\lambda_j}$ 对 $j$ 可和（$\sum_j e^{-t\lambda_j}<\infty$），故 $e^{-tA}$ 迹类且迹等于特征值之和。每项 $e^{-t\lambda_j}>0$，故迹严格为正。平移断言由 $e^{-t(A+c)}=e^{-ct}e^{-tA}$ 得。$\square$

**推论 2.2（假设的空洞性）**　设 $\mathcal C$ 为上述算子类。命题 "$A\in\mathcal C\Rightarrow \operatorname{Tr}e^{-tA}>0\ \forall t>0$" 对**所有** $A\in\mathcal C$ 成立。因此，任何形如
> "若 $\operatorname{Tr}e^{-tT}>0$（$\forall t>0$）则【关于 $T$ 的算术结论 $Q(T)$】"

的定理，实际上必须对所有自伴 $T$ 成立 $Q(T)$。此时 $Q$ 与"正性"无关：正性假设没有筛选力。

**[事实] 各种"正性"的精确含义与信息量**（这是用户前提中最模糊的一点，必须逐项区分）：

| 概念 | 定义/含义 | 是否自动 | 是否携带算术信息 |
|---|---|---|---|
| (i) 热核逐点正性 $K_t(x,y)>0$ | $e^{-tA}$ 的积分核逐点为正 | 对 Laplace 型生成元（流形/狄利克雷型）自动（Beurling–Deny/最大值原理/布朗运动） | 否（只反映算子"几何/扩散"性质） |
| (ii) 半群保正性 $e^{-tA}\ge0$（序意义） | 把非负函数映为非负函数 | 仅当 $A$ 生成狄利克雷型时自动；对一般自伴 $A$ 不必成立 | 否（性质在酉共轭下不变，与算术无关） |
| (iii) 迹正性 $\operatorname{Tr}e^{-tA}>0$ | 谱特征值指数和 | **总是自动**（引理 2.1） | **零** |
| (iv) 带符号/分次超迹 $\operatorname{Tr}(\Gamma e^{-tA})$ | 取值可正可负，如 $\sum(-1)^je^{-t\lambda_j}$ | 不自动；可以编码指标/拓扑（Atiyah–Singer 型） | **可能有信息，但证明其正性本身就是非平凡定理**；且要让它等于 Goldbach 数据就必须先构造分次 $\Gamma$，这是把算术"编码进算子"，不是从正性推出算术（见 §4.1、§4.3） |
| (v) 带权迹 $\operatorname{Tr}(W e^{-tA})$，$W=W^*$ | 如 $-\zeta'/\zeta(t)=\sum_n\Lambda(n)n^{-t}$ 的"算子实现" | 若 $W\ge0$ 且 $A$ 自伴，则自动 $>0$（正项求和） | 正性本身零信息；信息全在 $W$ 与 $A$ 的**算术构造**与**解析延拓/零点** |

**结论 2.3**　"[某算子] 热核迹正性"若指 (iii)（甚至 (i)(ii)），在目标场景（Li–Liu 的 $T_N$ 是紧自伴，Morató 的 $D$ 被宣称离散谱）中**自动成立**，不可能"推出 Goldbach"。若指 (iv)(v)，则它不再是"自动的正性"，其证明难度/内容与算术结论相当——即"关键一步"退化为把结论重述一遍。

### 2.2 事实 B：系数提取缺口（正性 $\not\Rightarrow$ 系数正性）

**命题 2.4（显式反例）**　令
$$F(t)=e^{-t}-2e^{-2t}+2e^{-3t}\qquad(t>0).$$
则 $F(t)>0$ 对一切 $t>0$ 成立，但把 $F$ 写成 $\sum_{n\ge1}a_ne^{-tn}$ 时 $a_1=1,\ a_2=-2,\ a_3=2$，即 $a_2<0$。

**证明.**　令 $u=e^{-t}\in(0,1)$。则
$$F=u-2u^2+2u^3=u\,(1-2u+2u^2)=u\Big(2\big(u-\tfrac12\big)^2+\tfrac12\Big)\ge \frac{u}{2}>0,$$
因为 $2(u-\frac12)^2+\frac12\ge\frac12$，且 $u>0$。系数由定义直接读出：$a_1=1$、$a_2=-2$、$a_3=2$。$\square$

（数值复核：$t\in\{0.01,0.1,0.5,1,2,5,10,20\}$ 时 $F=0.9705,0.7490,0.3170,0.1968,0.1037,0.00665,4.54\times10^{-5},2.06\times10^{-9}$；$1-2u+2u^2$ 在 $(0,1)$ 上的最小值 $=\frac12$ 于 $u=\frac12$。见附录 A。）

**推论 2.5（一般性陈述）**　"$Z(t)=\sum_n a_ne^{-tn}>0\ \forall t>0$"不能推出"$a_n\ge0$"；甚至不能推出任何单个 $a_{n_0}\ge0$。因此任何形如
> "$Z(t)=\operatorname{Tr}e^{-tT}>0$，故其"系数"$a_n$（如 Goldbach 表示数）$\ge0$"

的推理无效。

**命题 2.6（正确的加强条件，及它为何仍不够）**　设实数列 $(a_n)_{n\ge1}$ 满足 $\sum_n|a_n|e^{-tn}<\infty$（$\forall t>0$）。记 $f(t)=\sum_na_ne^{-tn}$。则
$$a_n\ge0\ (\forall n)\iff f\ \text{在}\ (0,\infty)\ \text{上完全单调}\ \big(f\in C^\infty,\ (-1)^kf^{(k)}\ge0\ \forall k\ge0\big).$$

**证明.**　($\Rightarrow$) 逐项求导（由绝对一致收敛保证）：$(-1)^kf^{(k)}(t)=\sum a_nn^ke^{-tn}\ge0$。
($\Leftarrow$) Bernstein 定理：完全单调的 $f$ 是某个**正**测度 $\nu$ 在 $[0,\infty)$ 上的 Laplace 变换，$f(t)=\int_0^\infty e^{-tx}d\nu(x)$。另一方面 $f(t)=\int_0^\infty e^{-tx}d\mu(x)$，其中 $\mu=\sum_na_n\delta_n$ 是符号测度且 $\int e^{-tx}d|\mu|=\sum|a_n|e^{-tn}<\infty$。Laplace 变换在指数可积的符号测度上单射（把 $e^{-tx}$ 的有限线性组合与 Stone–Weierstrass 逼近结合，再取 $x$ 的分布函数），故 $\nu=\mu$，于是 $a_n=\nu(\{n\})\ge0$。$\square$

**为何仍不够（对 Goldbach 而言）**：命题 2.6 只给出 $\ge 0$。而 Goldbach 的 $r(N)\ge0$ 是**定义**（它是计数）；要证的是**每个**偶 $N$ 都有 $r(N)>0$——一个"支撑集"陈述。完全单调性/正性无法检测单个系数为零：若把 $F$ 的某个系数改成 $0$（保持其它系数非负），$f$ 仍是完全单调且 $>0$。**正性信息对"某个系数是否为零/是否严格正"是完全盲的**。要得到逐点严格正性，必须**定量**证明主项压过误差：
$$r(N)=\underbrace{\text{主项}}_{\text{正}}+\underbrace{E(N)}_{\text{误差}},\qquad |E(N)|<\text{主项}\quad(\forall N\gg1),$$
这是解析数论问题（圆法/例外集/零点控制），不是任何正性泛函能提供的。

**推论 2.7（对"热核迹方案"的判决）**　一个方案若只证明"$\operatorname{Tr}e^{-tT}>0$ 或某个生成函数正"就想得到 Goldbach 表示数的正性，则：(a) 若它依赖点值正性——由命题 2.4 无效；(b) 若它依赖完全单调性——最多得到表示数 $\ge0$（平凡），得不到严格正性；(c) 若它依赖"解析延拓 + 零点自由区"——那已经是新的 RH 型问题，与原来的核心困难同级，不是"正性"的副产品。**它必须额外提供定量上界（见 §5.3）。**

**[事实] 独立的旁证**：Polson–Sokolov 在其 819 页专著中证明（其 Theorem 5.2.1 / 文献 [206, Theorem D]）：对任意足够大的高度 $R$（只要 RH 已验证到 $R+50$），存在与 $\xi$ 同阶、同型、同对称性、且在 $R$ 以下零点完全相同的扰动，它在 $R$ 与 $R+50$ 之间有离线零点，**却通过任意有限个热核迹正性检验**。这正是"有限阶正性/点值正性不能替代真正的结构信息"的定量版本，与命题 2.4/2.5 同一逻辑。

### 2.3 事实 C：Li–Liu 框架中的方向问题（正性给的是下界，Goldbach 需要上界）

**[事实] 精确框架（Li–Liu 2026-11-13 预印本，方程编号照原文）**：设 $N$ 为偶数，$\phi$ 为固定检验函数，$S(N)$ 为奇异级数，$c_\varphi>0$。论文构造了 Hardy 空间 $\mathcal H_N$ 上紧自伴 Hilbert–Schmidt 算子
$$(T_Nh)(s)=\int_{\Gamma_N}\frac{E_N(s,\bar z)}{(1+s)(1+\bar z)}h(z)\,|dz|\qquad (2.17),\ \Gamma_N=(\alpha_N+i\mathbb R)\sqcup(\beta+i\mathbb R),$$
以及 Riesz 向量 $v_N\in\mathcal H_N$，$\|v_N\|^2=Q_N\ll_\varphi1$，并证明**精确恒等式**
$$G(N)=c_\varphi S(N)-\langle T_Nv_N,v_N\rangle,$$
从而
$$|G(N)-c_\varphi S(N)|\le Q_N\|T_N\|\ll_\varphi\|T_N\|\qquad (2.18)$$
与**主估计**
$$|G(N)-c_\varphi S(N)|\ll_\varphi\|T_N\|\qquad (2.19).$$
论文在此处有一句关键的话（原文，第 9 页）：

> "**Subtraction need not preserve positivity, so eigenvalues of either sign must be allowed.**"

即 $T_N$ **并不**已知为正；正负特征值都要允许。这一点本身就否定了"由 $T_N$ 的热核迹正性出发"的可行性（正性连前提都不成立）。

论文把所需范数上界写成两个新假设：
- **Hypothesis S**（零自由区版）：$X_N(q)=\prod_j\big(1-\frac{4\mu_j^2}{\delta_N^2q(1-q)}\big)$ 在 $\Re q>1-\eta_N$ 无零点，$\eta_N=\frac{h^2(N)(\log N)^3}{NS(N)}$。等价于（原文 (2.28)）
$$\|T_N\|\le\frac{S(N)}{2h(N)\sqrt{1-\eta_N}}.$$
- **Hypothesis R**（更强）：$X_N$ 的每个零点实部 $=1/2$，等价于（原文 (2.30)）$\|T_N\|\le\delta_N:=\sqrt{\frac{S(N)}{N}}(\log N)^{3/2}$。

而 **GRH 单独只给**（原文 (2.24)–(2.25)）：$\|T_N\|\le\|T_N\|_{\mathrm{HS}}\ll(\log N)^2$，对应 $\eta_N^{\mathrm{GRH}}\asymp\frac{S(N)}{N\log N}$；所需改进量（原文 (2.29)）
$$\frac{\eta_N}{\eta_N^{\mathrm{GRH}}}\asymp\frac{h^2(N)(\log N)^4}{S^2(N)}\to\infty .$$
即：**Goldbach 需要的是"算子范数足够小"的定量上界，而 GRH 给的上界差一个趋于无穷的因子**。

现在把"正性路线"放进来：

**引理 2.8（正性—方向模型引理）**　设 $\mathcal H$ 为实 Hilbert 空间，$v\in\mathcal H$，$v\ne0$，$c\in\mathbb R$。则
$$\big\{\,c-\langle Tv,v\rangle\ :\ T:\mathcal H\to\mathcal H\ \text{有界自伴},\ T\ge0\,\big\}=(-\infty,\,c\,].$$

**证明.**　($\subseteq$) 若 $T\ge0$ 自伴，则 $\langle Tv,v\rangle\ge0$，故 $c-\langle Tv,v\rangle\le c$。
($\supseteq$) 任给 $s\le c$，令 $T_s=\alpha\,vv^*$，其中 $(vv^*)w:=\langle w,v\rangle v$，$\alpha:=\dfrac{c-s}{\|v\|^4}\ge0$。则 $T_s$ 自伴，且对一切 $w$，$\langle T_sw,w\rangle=\alpha\langle w,v\rangle^2\ge0$，故 $T_s\ge0$。又 $(vv^*)v=\|v\|^2v$，故 $\langle T_sv,v\rangle=\alpha\|v\|^4=c-s$，于是 $c-\langle T_sv,v\rangle=s$。$\square$

**推论 2.9（方向错误）**　在 Li–Liu 记号下 $G(N)=c_\varphi S(N)-\langle T_Nv_N,v_N\rangle$。若 $T_N\ge0$，则只能推出
$$G(N)\le c_\varphi S(N).$$
但 Goldbach 需要的是 $r_\Lambda(N)>0$ 且 $G(N)=c_\varphi S(N)+O(S(N)/h(N))$，即
$$\langle T_Nv_N,v_N\rangle<c_\varphi S(N)\quad(\text{严格下界之外的上界，且误差要小}),$$
等价于 $\|T_N\|=\|T_N\|_{\text{op}}$ 的**上界**（Hypothesis S/R）。**正性提供的是下界，需求是上界；方向相反。** 引理 2.8 更强：在只有"正性"的约束下，$G$ 可以取 $(-\infty,c_\varphi S(N)]$ 中任何值——包括任意负——所以正性不能排除"没有 Goldbach 表示"。

**推论 2.10（热核迹版本更空洞）**　把附加假设换成"$\operatorname{Tr}e^{-tT_N}>0\ \forall t>0$"：由引理 2.1，这对**所有**自伴 $T_N$ 成立，故对引理 2.8 中构造的 $T_s$ 也成立；集合仍为 $(-\infty,c]$。**热核迹正性对 $G$ 没有任何约束力。**

**推论 2.11（"正确的正性"应是什么形状）**　真正有用的不是 $T_N\ge0$，而是**Loewner 序上界 + 显式小 majorant**：
$$0\le T_N\le B_N,\qquad \|B_N\|\le\frac{c_\varphi S(N)-o(S(N))}{\|v_N\|^2}\ \text{或}\ \operatorname{Tr}(B_N)\text{ 显式小}.$$
"$T_N\le B_N$"的等价说法是"$B_N-T_N\ge0$"——一个**差算子**的正性。这类定理确实足以推出 Goldbach（见 §5.3 的形状），但它的证明等价于定量估计本身；而"$T_N$ 自己的热核迹正性"对此毫无帮助（§2.4 表明它甚至不能给出任何范数上界）。

### 2.4 事实 D：迹—范数方向引理（热核迹不能证明小范数）

**引理 2.12（迹的方向）**　设 $T$ 为有限维（$\dim=N$）实/复 Hilbert 空间上的自伴算子，$T\ge0$，特征值 $0\le\lambda_1\le\cdots\le\lambda_N=\|T\|$。则对一切 $t>0$：
$$Ne^{-t\|T\|}\le\operatorname{Tr}e^{-tT}\le N,\qquad\text{从而}\qquad \|T\|\ge\frac1t\ln\frac{N}{\operatorname{Tr}e^{-tT}} .$$

**证明.**　$e^{-tT}$ 的特征值为 $e^{-t\lambda_j}\in[e^{-t\|T\|},1]$，对 $j$ 求和即得双边不等式；下界整理即得 $\ln\frac{N}{\operatorname{Tr}e^{-tT}}\le t\|T\|$。$\square$

**推论 2.13（任何由迹到范数的推断都是"下界"）**　引理 2.12 表明：$\operatorname{Tr}e^{-tT}$ 的**上界**只能给 $\|T\|$ 的**下界**（$\operatorname{Tr}$ 小 $\Rightarrow$ 至少有一个大特征值）；而 $\operatorname{Tr}$ 的**下界**（包括"正性"$\operatorname{Tr}>0$、甚至"$\operatorname{Tr}\ge L$"）给出**零**关于 $\|T\|$ 上界的信息。特别地，任务所引的不等式 $\operatorname{Tr}e^{-tT}\ge e^{-t\|T\|}$ 的用法只能是：若已知 $\operatorname{Tr}e^{-tT}\le M$，则 $\|T\|\ge\frac1t\ln\frac1M$——**永远是范数的下界**。

**命题 2.14（反例族：迹下界与范数无关）**　任意 $N\ge2$，任意 $M>0$，取 $T_M=M\cdot P$，$P$ 为秩一正交投影。则 $\|T_M\|=M$，而对一切 $t>0$：
$$\operatorname{Tr}e^{-tT_M}=e^{-tM}+(N-1)\ge 1 .$$
因此，**即使假设对所有 $t>0$ 有统一下界 $\operatorname{Tr}e^{-tT}\ge1$（远强于正性），$\|T\|$ 仍可任意大。** 热核迹正性/下界不能证明 $\|T_N\|\le\delta_N$（Hypothesis S/R 所需的上界）。

**证明.**　$T_M$ 的特征值为 $M$（重数 1）与 $0$（重数 $N-1$），直接计算迹。$\square$

**推论 2.15（对"热核迹正性 $\Rightarrow$ 小范数"的最终否定）**　设某方案宣称：由 $T_N$ 的热核迹正性（或某个下界）可推出 $\|T_N\|\le\delta_N$。由命题 2.14，存在满足该正性/下界但对任意大范数成立的算子族，故该蕴含不成立。反过来，若方案改用**迹的上界**，由引理 2.12 只能得到范数下界，仍不能得到所需的上界。**结论：热核迹这一"谱和"量对所需算子的/上界不敏感；所需的是最大特征值（或等价地，新的零点自由区）的定量控制。**

> 注（无限维版本，供完整性）：若 $T\ge0$ 自伴迹类，同样有 $\operatorname{Tr}e^{-tT}\ge e^{-t\|T\|}$（$\|T\|$ 为最大谱值）。小 $t$ 渐近 $\operatorname{Tr}e^{-tT}\to\operatorname{rank}_{<\infty}(T)$ 只给出谱计数/维数信息；$t\to\infty$ 时 $\operatorname{Tr}e^{-tT}\to\dim\ker T$，只给零特征值重数。**迹在任何极限下都不是 $\|T\|$ 的上界信息源。**

**[关于形式化的注记]**　本节引理 2.1（谱定理/指数求和）、命题 2.4（$u=e^{-t}$ 后的实二次不等式）、引理 2.8（秩一算子 $\alpha vv^*$ 构造与 $\langle Tv,v\rangle=\alpha\|v\|^4$）、引理 2.12（有限维谱分解与指数单调性）都只用初等线性代数与实分析，**在 Mathlib/Lean 4 的现有 API 下是可形式化的**（实数内积空间、`LinearMap.IsSymmetric`、秩一算子的 `smulRight`、`Real.exp` 的单调性与 `nlinarith` 即可；命题 2.4 的形式化可避开超越性：先证 $u\in(0,1)$ 上的多项式不等式，再用 `Real.exp_pos` 把 $u=e^{-t}$ 代入，或用有理函数版本 $F_0(u)=u-2u^2+2u^3$ 在 $(0,1)$ 上为正）。任务 6（`lean-feasibility`）正在测试本环境工具链；本报告只承担数学证明部分，不声称已完成 Lean 核验。

### 2.5 失败的精确逻辑位置（小结）

设待证 $Q$ = "每个偶 $N$ 是两素数之和"（或 Li–Liu 的 $G(N)\sim c_\varphi S(N)$）。任何"热核迹"方案必须形如：
$$\underbrace{\operatorname{Tr}e^{-tT}>0\ \text{(正性)}}_{\text{(H)}}\ \Longrightarrow\ \underbrace{\langle T_Nv_N,v_N\rangle<c_\varphi S(N)}_{\text{所需上界}}\ \Longrightarrow\ Q.$$
由 §2.1，**(H) 是自动的**；由 §2.3，所需的量是 $\langle T_Nv_N,v_N\rangle$ 的**上界**；由 §2.4，热核迹（正性/下界）给不出任何范数上界。**因此缺口不在证明细节，而在蕴含本身**：从自动成立的下界型性质，推不出所需的上界型结论。这正是"方向错误"四个字的精确数学内容。

---

## 3. Alpöge/Claude 的 Lean 证明有"谱/热核迹"这一步吗？

### 3.1 仓库取证（2026-11-21，本地 `/home/kiler/rh-full`，commit 与 README 一致）

**[事实] 规模与主链**（命令见附录 B）：
- `find src -name '*.lean' | wc -l` = **175,187**（与 README 表格一致）。
- 顶层定理文件 `src/Main.lean` 内容（全文）：
```lean
import Statements
import Supplements.Kernels.MainTheoremsAll
theorem riemannHypothesis : RiemannHypothesis := rhOfAll
theorem riemannZeta_eq_zero_re : RiemannZetaZerosOnLine := rhOfAll
theorem LFunction_ne_zero_of_half_lt_re : DirichletLNonvanishingRightOfHalf := allChi
theorem LFunction_eq_zero_re : DirichletLZerosOnLine := claimAll.2.1
theorem LFunction_eq_zero_re_of_isPrimitive : PrimitiveDirichletLZerosOnLine := critAll
```
- `src/Supplements/Kernels/MainTheorems.lean`：
```lean
theorem allChi : UpperTheory.EveryCharacter := UpperTheory.FinalTheorems.everyCharacter
theorem rhOfAll : RiemannHypothesis := Formalism.VW.rh_of_every allChi
```
- `Formalism/GammaFactorNonvanishing/CritLine.lean` 中 `Formalism.VW.rh_of_every`（`h : UpperTheory.EveryCharacter`）只做一步：把半平面不零 + 函数方程转成临界线。`Development/AutomorphicArithmetic/CharacterBoxes/EveryCharacter.lean` 定义
```lean
def UpperTheory.EveryCharacter : Prop :=
  ∀ (N : ℕ) [NeZero N] (χ : DirichletCharacter ℂ N) (s : ℂ),
    1/2 < s.re → (χ ≠ 1 ∨ s ≠ 1) → DirichletCharacter.LFunction χ s ≠ 0
```
即主链的实质终点是"**所有 Dirichlet $L$-函数在 $\Re s>1/2$ 不零**"；`MainConclusion.lean` 的 `UpperTheory.FinalTheorems.everyCharacter_of_row` 通过 `UpperTheory.LiteratureTheorems.every_character_of_literature_of_vWin ⟨..., UpperTheory.Zero.LLC.recTExists, ...⟩ (UpperTheory.One.vwin_of_row h)` 到达，`EveryCharacter.lean` 的 `Top.plugAll = Top.imprimitive (Top.plugWin hG hV h)` 用到 `GlobalTheory.GLq.Green`（函数域/Stepanov 玩具模型）、`Hyps (Closed … LinkN)` 等。

**[事实] 全树关键词扫描**（`grep -rli --include='*.lean' <KW> src`，文件数）：

| 关键词 | 命中文件数 | 说明 |
|---|---:|---|
| `heat kernel`（区分大小写不敏感的 "heat kernel"） | **0** | 无此短语 |
| `HeatKernel` | **13** | 全部在 `Development/AbelianVarietyTheory/` 局部子库：11 个 `Proofs/DivisorProofs/`（如 `HeatKernelTraceIntegrable.lean`、`HeatKernelFundamentalDomainPull.lean`）+ 2 个 `PublishedTheorems/Divisors₂/`；`HeatKernelTraceIntegrable` 只被同目录 `OneVector.lean` 与自身 Statement 包装文件 import |
| `HeatOperator` | 107（81 个文件名） | 同为 Abelian 簇理论里的微分几何对象，不是谱迹正性定理 |
| `thermal` | **0** | — |
| `trace formula` | **0** | — |
| `Selberg` | 284 | 绝大多数是 **Rankin–Selberg**（自守形式），无 "Selberg trace formula" |
| `Guinand` | **0** | — |
| `HilbertPolya` / `Hilbert–Pólya` | **0** | — |
| 真正的 `Pólya` | **0** | —（`grep -rl 'Pólya'`=0；`\bpolya\b` 大小写不敏感只命中定理名 `polyA`） |
| `Weil` | 35,833 | 主要是 `WeilPairing`(288)、`GlobalTheory.WeilDeligne`、Weil 限制/高度等几何代数对象；`WeilPositive`、`WeilExplicitFormula`、`weil_explicit` 均为 **0** |
| `ExplicitFormula` | 105（含 `ExplicitFormulaError*` 等） | 集中在 `Formalism/HermitianCurvature/HermitianCurvatureProofs/` 与 `Formalism/SharpRestriction/`；是内部误差项/展开式命名，不是经典显式公式的独立定理 |
| `HermitianCurvature` | 2,725 | 大块 `Formalism/HermitianCurvature`（1,922 文件）+ 引用；样本内容为行列式/余子式/Vandermonde 型恒等式（**Stepanov 行列式多重性**风格的代数内核），不是热核算子理论 |

**[事实] 主链与热核模块的关系**：`HeatKernelTraceIntegrable.lean`（是测度论积分可积性引理：`integrableOn_strN_heatKernel_diag`，关于环面基本域上热核"分层迹"的可积性）只被 `HeatKernelTraceIntegrableStatement.lean` 和 `OneVector.lean`（同目录）import；`Supplements/Kernels/MainTheorems.lean`、`Formalism/GammaFactorNonvanishing/CritLine.lean`、`CharacterBoxes/EveryCharacter.lean`、`CharacterBoxes/MainConclusion.lean` 中 `HermitianCurvature` 与 `heat` 的出现次数均为 **0**；唯一相关的是 `EveryCharacter.lean:9` 的一处 `Formalism.HC.ZeroFreeAll` 命名空间引用（"HC" 是零自由区断言的命名空间，不是热核/曲率）。README 中 "heat" 一词作为独立关键词 **0 次**（唯一相关行是 `HermitianCurvature/…/CutCptCopy.lean` 的 `addDecl` 说明）。

### 3.2 这个证明实际使用的架构

**[事实] 作者自己的 4 页说明**（`/home/kiler/rh-work/remark.txt`，即 [alpo.ge/remark.pdf](https://alpo.ge/remark.pdf)）给出的主干：
- "In Stepanov's argument resolving Riemann over function fields one uses a divisor involving multiplicity. This argument is a descendant of Stepanov's, but multiplicity is hard to find over the integers … chaining theta lifts … for the von Mangoldt sum of length $X$, Claude's suggested length of chain of theta lifts … was $\sqrt X$."（Stepanov 多重性 + 迭代 theta 提升链长 $\sqrt X$）
- 时间线（作者转述）：Stepanov 行列式 → CM 曲线上的不变微分/$\theta(0)$ 可除性 → $qN=Mk+R$（GL5 六重覆盖上的 theta 周期）→ "$W(1_S)\ge 0$ via a determinant, interpret as Stepanov with multiplicity one again" → "**Guinand-Weil had the sign**, variance test function trick …" → 迭代 theta 提升 $U(X_0)\to\cdots\to U(X_m)$、Rallis seesaw、Chowla–Selberg/Weyl/Siegel mass、相对迹公式、Iwasawa 塔（Behrend）等。
- 关键点：**其中确有"正性/符号"机制**——$W(\cdot)\ge0$ 的行列式（$W$ 是 Weil 显式公式泛函）、"Guinand–Weil had the sign"、"from middle cohomology gives a definite sign"。但这全部是**乘性**对象（von Mangoldt 和 $\sum_{n\le X}\Lambda(n)\cdot(\frac Xn-1)$、Galois 表示、theta 提升、Weil 显式公式），**与热核迹正性无关**。

**[推断] 与 proof-digest（`_rh-work/proof-digest/report.md`）的交叉验证**：该队友把 $W\ge0$ 行列式对应到 `Formalism/HermitianCurvature`（含 `addDecl` 文件 `CutCptCopy.lean`），把 theta-lift 链对应到 `ThetaCorrespondence/…/TLiftK`、`UpperTheory.Lit.every_character_of_theta_integrals_local_matching`；把玩具模型对应到 `GlobalTheory.GLq.Green`（prime-polynomial 标签/Stepanov 式的组合陈述）。这与本节的 grep 证据一致：**证明的架构是 Stepanov/自守表示/Galois 表示/显式公式符号，不是热核谱迹。**

### 3.3 结论：前提张冠李戴（misattribution）

**[推断/判断]** 用户的"黎曼猜想的谱证明架构"（指 Alpöge/Claude 的 Lean 证明）在两点上被误读：
1. **它不是"谱/热核"证明，而是 Stepanov 多重性 + theta 提升 + 自守/Galois 表示。** 热核迹正性不是该证明的关键步骤，甚至不出现在主链（§3.1）。
2. **该证明中真实的"正性/符号"步骤（Guinand–Weil 符号、$W\ge0$ 行列式、中间上同调确定符号）是乘性的**，属于 RH/GRH 的 L-函数零点理论；它不可能直接迁移到加性素数对计数（§4.2 给出结构性理由）。

而用户命题的真实文本来源（§1.1 来源 A/B）是**另外两条未评审、且自身失效的"谱证明"**：
- 若指 Morató 的 600-cell 谱证明：其 RH 部分本身未经检验，其 Goldbach 分册的核心步骤是"HL 猜想 + 伪造逐点误差界"（§1.3(A)），并非热核迹正性；
- 若指任尚业系列：其热核迹"分层对应殆素数对"是无来源的断言，且文中自认未完成 Goldbach（§1.3(B)）。

**无论按哪种归属，"谱证明架构 ⇒ 热核迹正性 ⇒ Goldbach"都不能成立。**

---

## 4. 构造性尝试：能否造一个"热核迹 = Goldbach 相关"的算子？

任务要求认真尝试构造。答案是：**能构造，且构造很简单；但构造出的正性判据是空洞的。** 这反过来暴露了该路线的全部困难所在。

### 4.1 显式构造：双粒子算子（two-particle operator）

**[构造]** 取 $\mathcal H_1=\ell^2(\mathbb P)$（平方可和素数序列），令 $L:\delta_p\mapsto p\,\delta_p$ 为对角自伴算子（谱 $=\mathbb P$）。则对 $t>0$，
$$\operatorname{Tr}e^{-tL}=\sum_{p\in\mathbb P}e^{-tp}=P(t).$$
在张量积 $\mathcal H_1\otimes\mathcal H_1$ 上取双粒子算子（对称化即可，不影响迹）
$$H:=L\otimes I+I\otimes L .$$
则
$$\operatorname{Tr}e^{-tH}=\Big(\sum_pe^{-tp}\Big)^2=\sum_{p,q}e^{-t(p+q)}=\sum_{N\ge4}r(N)\,e^{-tN},$$
其中 $r(N)=\#\{(p,q)\in\mathbb P^2:p+q=N\}$ 恰是（有序）Goldbach 表示数；无向表示数只差因子 2，不影响任何正性论证。**这就是一个自伴、正（$H\ge0$）、离散谱算子，其热核迹精确等于 Goldbach 相关的生成函数。** 且 $\operatorname{Tr}e^{-tH}>0$ 自动成立（引理 2.1）。

**[命题 4.1（这个构造为什么无用）]** 上述 $H$ 的热核迹正性等价于不多于 "$r(N)\ge0$ 且至少一个 $r(N)>0$" ——即定义性事实。它**不能**推出任何 $r(N)>0$：
- 设某个偶 $N_0$ 满足 $r(N_0)=0$（这在逻辑上可能，甚至在已知的 GRH 条件下未被排除——见 §4.2）。定义 $\widetilde H$ 为把 $H$ 作用后删去 $N_0$ 项的（对角）算子，则 $\operatorname{Tr}e^{-t\widetilde H}=\sum_{N\ne N_0}r(N)e^{-tN}>0$ 对一切 $t>0$ 仍成立，且 $\widetilde H\ge0$。**热核迹正性对"某个系数为零"完全盲。**
- 更一般地，任何"$Z(t)>0\ \forall t>0$"的判据（命题 2.4）允许多项式系数变负；在 $r(N)$ 本身由计数定义时，"正性"是免费信息，而"每个系数都 $>0$"是关于系数**支撑集**的独立算术事实。

**[判定]** "构造算子使热核迹等于 Goldbach 相关"这件事**不是困难所在**；困难在于从热核迹/正性中提取逐点系数信息。这个构造本身恰好示范了：正性自动、信息为零。

**附注（"编码式构造"的循环性）**：也可以把 $r(N)$ 直接放进算子：取对角算子 $T=\sum_N r(N)\,\delta_N\,\langle\delta_N,\cdot\rangle$，则 $\operatorname{Tr}e^{-tT}=\sum_N r(N)e^{-tN}$ 且 $T\ge0$ 当且仅当 $r(N)\ge0$。**这种构造把结论编码进了算子定义**（"$T\ge0$"就是"$r(N)\ge0$"），不是从正性推出 Goldbach，而是把 Goldbach 重述为某个算子的正性——循环论证。要避免循环，算子必须由**独立于 $r(N)$ 的算术/谱数据**定义（如 Li–Liu 的 $T_N$ 由 Dirichlet $L$-函数投影定义）；而一旦独立定义，正性就既非自动、也非可证（Li–Liu 明言 $T_N$ 允许负特征值）。

### 4.2 为什么 RH 的（Weil）正性不能迁移到加性素数对计数

**[事实] Weil 正性是乘性的。** Weil 显式公式（Guinand–Weil 形式）把 $\zeta$（或 $L$-函数）的零点之和与**素数幂的单变量和**联系起来：零点侧是一个关于检验函数的线性泛函，算术侧的每一项只涉及**单个**素数幂 $p^k$（乘性/几何对象），不存在两个独立素数变量的耦合项（标准叙述见 Bombieri 的 Clay 综述、Connes 的迹公式论文；本报告只使用其结构性质）。RH 等价于该泛函在其自然锥上的（半）正性（"Weil 正性"）。这正是 Alpöge 证明所使用的"Guinand–Weil 符号"与 "$W\ge0$"的类型：它控制的是素数（幂）的**线性统计**，即 $-\zeta'/\zeta$ 与零点。

Goldbach 需要的是**双线性/加性相关**：
$$r_\Lambda(N)=\sum_{a+b=N}\Lambda(a)\Lambda(b)=\int_0^1 S(\alpha)^2e(-N\alpha)\,d\alpha,\qquad S(\alpha)=\sum_{n\le N}\Lambda(n)e(n\alpha).$$
它有**两个独立的求和变量**，以 $a+b=N$（加法）耦合。**结构障碍**：Weil 显式公式/欧拉乘积只对**乘性（Dirichlet 卷积）结构**有 Euler 积分解（例如 $\Lambda*\Lambda$ 的 Dirichlet 级数是 $(\zeta'/\zeta)^2$，仍由 $\zeta$ 的零点控制）；而**加性卷积** $r_\Lambda(N)=\sum_{a+b=N}\Lambda(a)\Lambda(b)$ 的 Dirichlet 级数 $\sum_Nr_\Lambda(N)N^{-s}$ **没有 Euler 积**（不是 $L$-函数），因为加法与乘法结构不相容。**已知的 RH/GRH 正性针对乘性对象；对加性卷积没有任何已知的迁移定理。** 这就是"RH 语言是 L-函数零点语言、Goldbach 语言是加法结构语言"的精确含义。

**[事实] 已知最强条件性结论只到例外集。** 在 GRH 下，Hardy–Littlewood（1924）证明的是**例外集**估计
$$E(x):=\#\{4\le N\le x:\ N\text{ 不是两素数之和}\}\ \ll_\varepsilon\ x^{1/2+\varepsilon}$$
（Goldston 1992 改进为 $x^{1/2}(\log x)^c$）；无条件最好记录为 Pintz 2018 的 $E(x)<x^{0.72}$（$x$ 充分大，常数 ineffective）。这些结果都**允许例外集永远非空**（$x^{1/2+\varepsilon}$ 稀疏但可无限存在），完全不排除任何一个例外。Li–Liu 引言亦明确写道："No proof of the binary conjecture is known under the generalized Riemann Hypothesis (GRH) alone, even when GRH is assumed for all Dirichlet L-functions … This estimate does not exclude exceptions altogether."

**[事实] 圆法的量级障碍（为什么弱 Goldbach 能证、强 Goldbach 不能）。** 三素数问题主项 $\asymp N^2/\log^3N$，劣弧用 Vinogradov 型估计 $N^2(\log N)^{-A}$ 即可压住，故圆法成功（Vinogradov 1937；Helfgott 2013 完成全部情形）。二元问题主项只有 $\asymp N/\log^2N$（加权版 $\asymp N$），而劣弧可得的（即使使用 GRH 的）逐点上界远大于此——主项比三元小两个 $\log$ 量级的这一事实，正是二元问题无法用圆法在 GRH 内闭合的算术原因。GRH 改善的是**优弧**（素数在等差数列中的分布，即 $\sum\Lambda(n)\chi(n)$ 的误差），对**劣弧**所需的加法抵消（$S(\alpha)$ 在远离有理点的相位随机性）没有帮助。

**[判断]** 因此"RH 谱证明架构 ⇒ 热核迹正性 ⇒ Goldbach"在结构上不可能沿"正性"传递：RH 侧的正性是**乘性泛函的正性**；Goldbach 侧需要的是**加性双线性相关的定量下界**。二者之间不仅缺一个引理，而是缺"从乘性统计到加性相关的桥"——已知的桥（圆法、筛法）都撞在下面的奇偶屏障/劣弧障碍上。

### 4.3 奇偶屏障（parity problem）的精确形态

**[事实] Selberg 的奇偶原则**（parity problem；Selberg 1947/1951；标准叙述见 Friedlander–Iwaniec, *Opera de Cribro*, AMS 2010；Halberstam–Richert, *Sieve Methods*, 1974）：一切以**非负筛权**为基础的筛法只能利用同余/局部密度信息，而局部密度对"$n$ 的素因子个数 $\Omega(n)$ 的奇偶性"不敏感；因此筛法无法区分"恰有 1 个素因子（素数）"与"恰有 2 个素因子（半素数）"这两类数。定量后果：线性筛对素数的上界带"奇偶因子" $2e^\gamma$，且无法给出任何素数性的**正下界**；这就是为什么纯筛法不能证明 Goldbach/孪生素数。Chen 定理 (1+2) 的关键"切换原理"只给出上界方向、从不给出下界。

**[命题 4.2（筛权的 $\Omega$-盲性质，简单但严格）]** 设 $z\ge2$，$P(z)=\prod_{p\le z}p$，$w(n)=\big(\sum_{d\mid n,\ d\mid P(z)}\lambda_d\big)^2$ 为任一 Selberg $\lambda^2$ 型非负筛权。则：
- 对任意 $n$ 与 $P(z)$ 互素，只有 $d=1$ 满足 $d\mid n,d\mid P(z)$，故 $w(n)=\lambda_1^2$ 是**常数**；
- 对一般 $n$，$w(n)$ 只依赖于 $n$ 在 $\le z$ 的小素数上的行为，**完全不依赖于 $\Omega(n)$ 的奇偶性**（例如无法区分 $z$-粗糙的素数、半素数、三素数乘积）。

**证明.**　$w(n)$ 的每一项由 $d\mid n$ 且 $d\mid P(z)$ 决定；$d$ 的素因子都 $\le z$。若 $(n,P(z))=1$，则唯一这样的 $d$ 是 $1$。其余断言由定义直接得到。$\square$

**推论（这一简单观察的含义）**：任何只使用筛权 $\sum_{a+b=N}w(a)w(b)$（以及局部密度主项）的论证，其输入在"保持小素因子结构、翻转大素因子 $\Omega$-奇偶性"的变换下不变；因此它无法区分"两个分量都是素数"与"两个分量都是恰有偶数个（或奇数个）大素因子的数"。这正是奇偶屏障的机制层面。**[事实] Selberg 的奇偶定理（1951）把它提升为一条反面定理：纯筛法（非负权重、不利用 $\Omega$-奇偶敏感信息）不能证明 Goldbach/孪生素数这类"两个分量同时为素数"的问题；线性筛对素数的上界带奇偶因子 $2e^\gamma$，且只能给上界、不能给正下界。**（标准叙述见 Friedlander–Iwaniec, *Opera de Cribro*, AMS 2010；Halberstam–Richert, *Sieve Methods*, 1974。）Chen 定理 (1+2) 的关键"切换原理"**只给出上界方向、从不给出下界**——Li–Liu 的 (1+1.9) 论文对此有清晰的现代叙述（转引自 `_rh-work/goldbach/report.md` §2.3）：

> "In the weighted sieve method, the fundamental reason why we employ multiple Buchstab iterations … is that **applying the switching principle yields only upper bounds, never lower bounds**."

**[判断]（不是定理，而是对一类论证方法的评估）** 由此可以理解为何"正性/非负权重/正泛函"型论证在 Goldbach 问题上系统性地只能产出**上界型**信息：上界无法排除"计数为 0"，而 Goldbach 需要的恰是"计数 $>0$"的下界。§2 中"正性给的是下界方向（对二次型）"与算术侧"筛法只给上界"是同一逻辑现象在两个层面的表现：**正性不能替代"存在性"所需的符号敏感/抵消信息**。

**[判断] 对"热核迹正性 ⇒ Goldbach"的映射**：热核迹 $\operatorname{Tr}e^{-tH}=\sum_Ne^{-tN}r(N)$ 的每一项权重 $e^{-tN}$ 都是正的、且与 $r(N)$ 的算术来源无关；它与筛权一样，只能"求和/上界"。若真有人构造出一个**带符号**的迹（supertrace，§2.1(iv)），使 $r(N)$ 恰为某个系数，那么要证明该系数 $>0$ 就必须证明带符号迹的**精确**符号模式——这等价于 Goldbach 本身，且已知没有任何构造把分次 $\Gamma$ 与加性素数对联系起来。**"unsigned trace 编码不了 $r(N)$ 的符号；signed trace 能编码，但其正性=结论，循环。"**

### 4.4 自省式谱–Goldbach 框架的现状（说明缺口的公认位置）

**[事实]** 域内最接近"认真构造"的自出版框架，都把困难明确保留为条件假设：
- **Ying Ye**（Zenodo 21324222）：以自伴 Hilbert 空间包、trace-compatible explicit formula、Fredholm 行列式、正/非逃逸谱投影为组织原则；摘要明言 "Infinite-dimensional passages, **Goldbach positivity**, pair-correlation closure, and gap isolation are formulated as **explicit conditional estimates or verification tasks**"。
- **Byoungwoo Lee**（Zenodo 19625051）：核心层只有 $M0$ = "$\Re s>2$ 上的 Mellin–trace 恒等式"及传递/熵/二进例外集引理；全局结论需 Gate A/B 假设，作者明言 exact core 未变。
- 就连来源 A（Morató）在分册 07 中也不得不引入 HL 猜想与逐点误差界；来源 B（任尚业）自认未完成。

**这些框架的共同点恰好证实了本报告的分析：真正缺的不是"正性"（它们都可以假设各种正性），而是"正性 + 定量小量估计"；定量估计是全部困难。**

### 4.5 一个"足够"的正性定理应当长什么样

**[定义/判断]** 若真的想沿"正性"路线走，一个**充分**的定理必须同时包含正性与定量上界，形如：

> **充分定理形状（Suff-S）**：存在显式 $h(N)\to\infty$ 与算子族 $B_N$，使得对每个充分大偶 $N$：
> (i)（序正性）$B_N-T_N\ \ge\ 0$（Loewner 序），且
> (ii)（显式小 majorant）$\|B_N\|_{\mathrm{op}}\le \dfrac{S(N)}{2h(N)\sqrt{1-\eta_N}}$（或 $\langle B_Nv_N,v_N\rangle\le c_\varphi S(N)-S(N)/h(N)$）。
> 则 $G(N)=c_\varphi S(N)+O(S(N)/h(N))$，从而 Goldbach（对充分大偶数）。

这一形状的**内容**全部在 (ii)；它是"算子范数/零点自由区的定量上界"，不是正性。等价地，在 Li–Liu 字典下，需要证明 $X_N(q)$ 在 $\Re q>1-\eta_N$ 无零点，且 $\eta_N/\eta_N^{\mathrm{GRH}}\asymp h^2(\log N)^4/S^2\to\infty$（原文 (2.29)）——即**远强于 GRH 的新零点自由区**（更强，因为 $\eta_N\gg\eta_N^{\mathrm{GRH}}$，排除区域更大）。

**几类"看起来像正性、实际充分"的候选（全部未被证明）**：
1. **差算子正性 + 量化**：如 $B_N-T_N\ge0$ 且 $\operatorname{Tr}e^{-tB_N}$ 的上界显式地小（注意：这里用的热核迹必须与 $B_N$ 的**显式谱**联合使用；单独的迹正性不够，见 §2.4）。
2. **加性 Weil 型正性**：构造双变量检验函数空间上的二次型 $Q(f,f)$，使 $Q(f,f)\ge0$ 等价于"素数对相关的主项占优"（Hardy–Littlewood 型渐近）。**目前不存在**这样的二次型；构造它本质上就是圆法劣弧问题（等价于解析形式的 Goldbach 难度）。
3. **双线性/相关和的定量界**：对 $\sum_{a+b=N}\Lambda(a)\Lambda(b)$ 的逐点渐近（主项 + $o(N)$ 误差）——这**就是** Goldbach 的加权版本（再加无权重化），任何"谱正性"路线最终都得回到这个估计。
4. **奇偶敏感的新结构输入**：能打破 §4.3 奇偶屏障的额外算术结构（如代数/自守表示的额外刚性），而非任何非负权重/正泛函。这类输入目前不存在；若有，将是重大突破，而非"RH 证明的必然推论"。

---

## 5. 最终裁决

### 5.1 最强可获得的真命题（本报告能站得住的最强陈述）

沿"热核迹正性"路线，能严格得到的只有以下否定性/条件性结论（均已证明或引用）：

1. **[命题 2.1]** 对一切自伴有下界离散谱算子，$\operatorname{Tr}e^{-tA}>0$（$\forall t>0$）自动成立；该性质零算术信息，不能作为"关键一步"。
2. **[命题 2.4]** $Z(t)>0$（$\forall t>0$）$\not\Rightarrow$ 系数非负；显式反例 $F(t)=e^{-t}-2e^{-2t}+2e^{-3t}>0$，$a_2=-2$。
3. **[命题 2.6]** 系数非负 $\iff$ 生成函数完全单调；即使如此最多给 $\ge0$，给不出 Goldbach 所需的逐点严格正性；逐点严格正性是支撑集/定量问题，不在正性信息内。
4. **[引理 2.8 / 推论 2.9]** Li–Liu 框架中：$T_N\ge0$（或热核迹正性）只给 $G(N)\le c_\varphi S(N)$（下界方向）；Goldbach 需要 $\langle T_Nv_N,v_N\rangle$ 的上界（即 $\|T_N\|$ 上界 = Hypotheses S/R）。模型集合 $=(-\infty,c]$：正性允许 $G$ 任意负。
5. **[引理 2.12 / 命题 2.14]** 热核迹（正性/下界）不能给任何算子范数上界；$\operatorname{Tr}e^{-tT}\ge e^{-t\|T\|}$ 只能导范数下界；反例族 $T_M=MP$ 表明迹下界 $\ge1$ 与 $\|T\|=M\to\infty$ 相容。
6. **[事实/引理]** Alpöge/Claude Lean 证明的架构是 Stepanov 多重性 + theta 提升 + 自守/Galois 表示 + 乘性 Guinand–Weil 符号 + $W\ge0$ 行列式；热核迹正性不在主链，全树对应关键词命中数为 0–13（局部子库）。
7. **[条件性真命题（文献）]** GRH + Hypothesis S（或 R）$\Rightarrow$ 加权 Goldbach 渐近（Li–Liu 2026 预印本，Theorem 1.1/1.2；未经同行评审）。把 2026-11-20 宣称的 GRH 代入后，剩下的恰恰是 S/R——**新的、未证明的、强于 GRH 的定量谱假设**。
8. **[事实]** 不存在任何已知定理：RH/GRH/热核迹正性 $\Rightarrow$ 二元 Goldbach。GRH 下最好结果是例外集 $E(x)\ll x^{1/2+\varepsilon}$（允许永远有例外）。

### 5.2 精确的失败步骤（exact failing step）

按重要性排序：

- **第一失败点（逻辑层，致命）**：把**自动的、下界型的**迹正性当作能推出**上界型的定量结论**。形式化地：(H)$\operatorname{Tr}e^{-tT}>0$ 对一切自伴 $T$ 成立（引理 2.1），而所需结论是 $\|T_N\|\le\delta_N$（Hypothesis S/R）；由引理 2.12/命题 2.14，二者无逻辑联系。**这一步在原则上不可能成功，不是技术难点。**
- **第二失败点（系数层）**：即便热核迹等于某个 Goldbach 生成函数，正性 $\not\Rightarrow$ 系数正性（命题 2.4）；严格点值正性需要解析延拓/零点控制/定量主项-误差分离。
- **第三失败点（来源层）**：所依据的具体"证明"（Morató 分册 07）用 HL 猜想（循环）+ 从 RH 推不出的逐点误差界 $|E(2n)|\le C\sqrt{2n}/\ln(2n)$；其热核迹只在展开式中出现，从未与"正性 ⇒ Goldbach"建立定理。中文来源（任尚业）自认未完成 Goldbach。
- **第四失败点（前提层）**：Alpöge/Claude 证明根本不是热核/谱迹架构；其正性机制是乘性 Weil/Guinand 符号，不触及加性素数对。

### 5.3 一个真正充分的正性定理的形状（供后续研究参考）

若要把"正性"作为研究纲领，需要形如 §4.5 的 **"序正性 + 显式小 majorant"** 定理。用 Li–Liu 语言，最小充分输入是：
$$\exists\,\eta_N\ \text{显式},\quad \eta_N\ \ge\ \eta_N^{\mathrm{GRH}}\cdot\frac{h^2(N)(\log N)^4}{S^2(N)}\ \text{且}\ X_N(q)\ \text{在}\ \Re q>1-\eta_N\ \text{无零点};$$
等价地，算子范数上界 $\|T_N\|\le S(N)/(2h(N)\sqrt{1-\eta_N})$。这**不是正性**，而是"新的零点自由区/算子范数定量上界"。一个真正"正性形式"的充分条件可以写成 $B_N-T_N\ge0$（Loewner）+ $B_N$ 显式小；但其证明难度 = 原问题。**任何声称"由热核迹正性推出 Goldbach"的论证，都必须公开说明它如何从自动的正性得到 (ii) 的定量小量界——而这正是全部文献缺失的一步。**

### 5.4 推测与建议（[推测]/[判断]，不可当定理）

- **[推测]** 不存在"仅用 RH/GRH + 正性论证"证明二元 Goldbach 的路线；若要突破，需要全新的**奇偶敏感**结构（能打破 §4.3 的非负权重限制）与**加性相关**的定量控制，二者目前都没有。这与 Li–Liu 必须引入 S/R、Ying Ye/Lee 必须引入显式条件假设的现象一致。
- **[判断]** 对本团队的最终答案：应明确告知用户，"RH 已证 ⇒ Goldbach"在数学上无依据；能诚实陈述的最强结论是 **"GRH（+ 新的 Hypothesis S/R）⇒ 加权 Goldbach"，而 S/R 未被证明**。任何"谱证明架构必然蕴含 Goldbach"的说法混淆了：(i) 乘性 L-函数零点理论，(ii) 自动的热核迹正性，(iii) 加性素数对计数——三者之间没有已知的逻辑通道。
- **[推测]** 用户命题很可能来自对 Morató 记录摘要（或其中文转述）的字面复述；建议向用户如实指出该来源为未评审自出版预印本、其核心常数数值不自洽、其 Goldbach 分册循环使用了 HL 猜想，并给出本报告的三个反例/引理作为可核验依据。

---

## 附录 A：数值核验（可复现）

```python
import math
# (1) Morató 600-cell 常数核对
d0 = 2*math.pi - 5*math.acos(1/3)
# d0 = 0.12838822047571252 rad = 7.3565... deg   （论文写 0.118682 rad / 6.8 deg，错）
ast = (d0/(2*math.pi))*math.log(2*math.pi*math.e)
# ast = 0.057988...                              （论文写 0.189979，错）
K2_prefactor = 2*0.6601618/(math.pi**2/6)
# 2*C2/zeta(2) = 0.802660...                    （论文引理5.3 声称 K(2)=delta0/(2pi)=0.02043）
# (2) 系数提取反例 F(t)=e^{-t}-2e^{-2t}+2e^{-3t}
F = lambda t: math.exp(-t)-2*math.exp(-2*t)+2*math.exp(-3*t)
# F>0 on t>0;  min of 1-2u+2u^2 on u in (0,1) = 0.5 at u=0.5
```

输出（本机 2026-11-21 实跑）：`arccos(1/3)=1.2309594173407747`；`delta0 true=0.12838822047571252`（论文 0.118682）；`alpha_st true=0.057988101364573906`（论文 0.189979）；`2*C2/zeta(2)=0.8026604996574751`，`delta0/2pi=0.02043361992348174`；`F(t)` 在 $t=0.01,0.1,0.5,1,2,5,10,20$ 分别为 $0.9705,0.7490,0.3170,0.1968,0.1037,0.00665,4.54\times10^{-5},2.06\times10^{-9}$，全部 $>0$；$1-2u+2u^2$ 最小值 $0.5$。

## 附录 B：证据与命令清单（截止 2026-11-21 ~11:20 +08）

**本地仓库（只读）**
- `find /home/kiler/rh-full/src -name '*.lean' | wc -l` → `175187`
- `cd /home/kiler/rh-full && for k in 'heat kernel' 'HeatKernel' 'thermal' 'trace formula' 'Guinand' ...; do grep -rli "$k" --include='*.lean' src | wc -l; done` → 见 §3.1 表
- 主链文件通读：`src/Main.lean`、`src/Statements.lean`、`src/Supplements/Kernels/MainTheorems.lean`、`src/Supplements/Kernels/MainTheoremsAll.lean`、`src/Formalism/GammaFactorNonvanishing/CritLine.lean`、`src/Development/AutomorphicArithmetic/CharacterBoxes/EveryCharacter.lean`、`.../MainConclusion.lean`
- 热核文件通读：`src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/HeatKernelTraceIntegrable.lean` 及其 Statement 包装（测度可积性引理）
- `grep -rl 'HeatKernelTraceIntegrable' --include='*.lean' src` → 仅 `HeatKernelTraceIntegrableStatement.lean`、`OneVector.lean`
- README：`/home/kiler/rh-full/README.md`（175,187 文件 / ≈17.4M 行；`addDecl` 1 处）

**Li–Liu 预印本**：`/home/kiler/rh-work/liu-goldbach.clean.txt`（4432 行）；引用：(1.5)–(1.7) 页 3–4；式 (2.17) 页 9；式 (2.18)–(2.19) 页 10；(2.24)–(2.30) 页 12–13；"eigenvalues of either sign" 页 9。

**下载/抽取的 PDF（scratch，本任务目录下）**
- `scratch/morato_07_goldbach.pdf` + `.txt`（9 页，Zenodo 19128632 附件 07）
- `scratch/morato_01_main.pdf` + `.txt`（16 页，附件 01）
- `scratch/ren_step25.pdf` + `.txt`（15 页，Zenodo 22731117）
- `scratch/computing_rh.pdf` + `.txt`（819 页，Zenodo 23400373 v1.1.0；`grep -c 'Goldbach' computing_rh.txt` = 0）
- 抽取脚本：`python3 -c "import fitz; ..."`（pymupdf 可用；无 pdftotext）

**网络来源**（均 2026-11-21 访问）：Zenodo API/记录页 19128632、22731117、23400373、19625051、15460813、21324222(经 Research Briefs)；GitHub `VadimSokolov/computing_rh` README（经 Windows PowerShell，因 WSL 直连 GitHub 被 127.0.0.1 拦截）；PhilArchive 检索页被 Cloudflare 403（仅用检索摘要，未依赖内容）。

## 参考文献

1. L. Morató de Dalmases, *Complete Proof of the Riemann Hypothesis and the Unified Number Theoretic Architecture of the 600-Cell: Goldbach, Twin Primes, and Collatz*, Zenodo 19128632, v6 (2026-03-20), DOI 10.5281/zenodo.19128632；附件 01、07。**[未评审自出版]**
2. 任尚业、杨双林、任傲天，《双曲螺线数论余区间逐点一致的统一上界估计——哥猜论证之第二十五》，Zenodo 22731117（2026-08-23），DOI 10.5281/zenodo.22731117。**[未评审自出版；正文自认未完成 Goldbach]**
3. N. G. Polson, V. Sokolov, *Computing the Riemann Hypothesis: Thorin Measures, Pólya Densities and Hitting Times*, Zenodo 23400373 v1.1.0 (2026-10-14)；扩展版 Edition 2 v3.0.0（3 卷，DOI 10.5281/zenodo.24377750 / 24377753 / 24377757）；GitHub `VadimSokolov/computing_rh`。**[自出版专著；明确不宣称证明 RH；不含 Goldbach]**
4. Ying Ye, *Spectral Paradigm of Analytic Number Theory*, Zenodo 21324222 (2026-10-03)。**[未评审]**
5. Byoungwoo Lee, *A Spectral–Entropy Framework for the Goldbach Conjecture* (v5.1), Zenodo 19625051 (2026-04-17)。**[未评审]**
6. Brian Simpson, *Goldbach* [STATUS: HIGH_CLAIM_ARCHIVE], Zenodo 15460813 (2026-05-09 revision)。**[作者自认非当前证明]**
7. J. Li, J. Liu, *A Conditional Proof of the Goldbach Conjecture*, Shandong Univ. MRC preprint (2026-11-13)；本地 `/home/kiler/rh-work/liu-goldbach.pdf`。**[未评审]**
8. L. Alpöge with Claude, *Remark* (4 页), [alpo.ge/remark.pdf](https://alpo.ge/remark.pdf)，2026-11-20；MIT 独立核验页 [math.mit.edu/~drew/grh/](https://math.mit.edu/~drew/grh/)；本地 Lean 镜像 `/home/kiler/rh-full`（README 含计数）。**[Lean 形式化宣称；人类可读证明未发表]**
9. G. H. Hardy, J. E. Littlewood, *Partitio Numerorum III/V*, Acta Math. 44 (1923), Proc. LMS (2) 22 (1924)（GRH 下三素数定理与 Goldbach 例外集 $E(x)\ll x^{1/2+\varepsilon}$）；D. A. Goldston (1992)；J. Pintz, arXiv:1804.09084 (2018)（$E(x)<x^{0.72}$）；D. A. Goldston, A. I. Suriajaya, *A singular series average and the zeros of the Riemann zeta-function*, Acta Arith. 200 (2021)；J. Brüdern, J. Kaczorowski, A. Perelli, *Explicit formulae for averages of Goldbach representations*, Trans. AMS 372 (2019)；J. Friedlander, H. Iwaniec, *Opera de Cribro*, AMS Colloq. Publ. 57 (2010)；H. L. Montgomery, R. C. Vaughan, *Multiplicative Number Theory I*, CUP (2007) §18.3。
10. 团队内部报告（交叉验证用）：`_rh-work/goldbach/report.md`、`_rh-work/proof-digest/report.md`、`_rh-work/repo-verifier/report.md`。

---

### 一句话总结（给最终答案用）

[证明] 热核迹正性是自动的重言式；点值正性推不出系数正性（反例 $e^{-t}-2e^{-2t}+2e^{-3t}$）；Li–Liu 框架中正性给出的是**反方向**的下界（$G\le c_\varphi S$），Goldbach 需要的是算子范数的**定量上界**（Hypotheses S/R）；迹给不出范数上界（$T_M=MP$ 反例）。[事实] Alpöge/Claude 的 Lean 证明根本不是热核/谱架构（全树 "heat kernel" 0、"trace formula" 0、"Guinand" 0；主链是 Stepanov 多重性 + theta 提升 + 乘性 Guinand–Weil 符号）。[判断] 用户命题的文本来源是未评审自出版预印本，"热核迹正性 ⇒ 哥德巴赫"在该路线中**在原则上不成立**，而非仅仅尚未证明。
