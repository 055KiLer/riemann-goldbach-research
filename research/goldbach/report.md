# RH/GRH 能否推出哥德巴赫猜想？——现状、逻辑边界与研究前沿（2026-11-21）

**任务**：回答用户问题「在（新近被宣称证明的）黎曼猜想的基础上去证明哥德巴赫猜想」。
**作者**：goldbach-researcher（Team task-3）
**完成时间**：2026-11-21（Asia/Shanghai）
**范围**：二元（强）哥德巴赫猜想；RH/GRH 与其逻辑关系；2026 年 11 月前后新进展；计算证据。
**所有 URL 的访问日期均为 2026-11-21**，除非另行注明。

> **诚信声明**：本报告不包含、也不会包含任何伪造的“由 RH 推出哥德巴赫”的证明。下文严格区分：
> **[事实]** 已证明/已同行评审/可独立核验；**[预印本主张]** 2026 年新发布、尚未经同行评审；**[假设/猜想]** 未被证明；**[研究方向]** 只是思路，不是结果。

---

## 0. 30 秒结论（给 Lead 直接引用）

**[事实] 截至目前（2026-11-21），数学上没有已知定理能从 RH 或 GRH 推出二元哥德巴赫猜想。** 这一点在最新文献中有白纸黑字的确认：山东大学李嘉旻、刘建亚 2026-11-13 的《A Conditional Proof of the Goldbach Conjecture》引言写道：

> “No proof of the binary conjecture is known under the generalized Riemann Hypothesis (GRH) alone, even when GRH is assumed for all Dirichlet L-functions.”

即 **仅假设 GRH（哪怕对所有 Dirichlet L-函数）也推不出二元哥德巴赫**。RH/GRH 对哥德巴赫问题真正可陈述的贡献是：① 1923 年 Hardy–Littlewood 在 GRH 下证明了三素数定理（后被 Vinogradov 无条件化，2013 年 Helfgott 完成全部情形）；② 1924 年 Hardy–Littlewood 在 GRH 下给出**例外集**估计 E(x) ≪ x^{1/2+ε}（“几乎所有偶数都是两素数之和”，但无法排除任何一个例外），Goldston (1992) 改进到 x^{1/2}(log x)^c。这两条都不是二元哥德巴赫的证明。

**2026 年的新变化**（本场景世界）：刘建亚团队给出了**第一个条件性二元哥德巴赫证明**，但代价是除 GRH 外还需**两个新的“附加谱假设”（Hypothesis S 或更强的 Hypothesis R）**，且论文明确论证 GRH 本身只能给出更弱的谱零点排除区、**不足以推出这两个假设**（见 §3）。因此，即使用 2026-11-20 宣称的 GRH 定理把 GRH 条件消去，剩下的仍是两个未证明的新假设——**二元哥德巴赫依然开放**。谁要是声称“RH 已证，所以哥德巴赫自动成立”，那在逻辑上就是错的。

---

## 1. 二元哥德巴赫猜想：2026-11 的精确现状

### 1.1 问题

**二元（强）哥德巴赫猜想**：每个偶数 N ≥ 4 都是两个素数之和。
等价形式（加权、去掉小素数干扰）：令

  G(N) = (1/N) Σ_{n+m=N, (nm,N)=1} Λ(n)Λ(m) φ(n/N)φ(m/N)，

Hardy–Littlewood 猜想为 G(N) ~ c_φ S(N)，其中 S(N) 是哥德巴赫奇异级数（见 §3.1 定义）。
本报告统一用 E(x) 表示 ≤ x 的“哥德巴赫例外偶数”（不能写成两素数之和的偶数）之个数。

### 1.2 无条件结果（严格已证）

| 结果 | 作者/年份 | 精确陈述 | 状态 |
|---|---|---|---|
| 三素数（弱）Goldbach，充分大 | Vinogradov 1937 | 每个充分大奇数 = 三个素数之和 | **[事实]** 无条件 |
| 三素数 Goldbach，全部 | Helfgott 2013/2014 | 每个奇数 n > 5 都是三个素数之和 | **[事实]** 已完整证明（arXiv:1312.7748；Helfgott–Platt 数值验证覆盖到解析阈值以下） |
| (1+2) Chen 定理 | 陈景润 1966 宣布 / 1973 发表 | 每个充分大偶数 N = p + P₂（P₂ 至多两个素因子）；定量 D_{1,2}(N) ≥ 0.67·C(N)·N/log²N，常数后经多人改进至 0.899（Wu） | **[事实]** 无条件 |
| (1+1.9)，2026 新前沿 | Jiamin Li & Jianya Liu, arXiv:2606.05224v2 (2026-06-01, v2 2026-08-08) | 每个充分大偶数 N = p + rq，其中 p,q 素数，r=1 或素数且 r ≤ q^{0.9}；据作者/中文报道称，这是定量意义上第一次越过 Chen 的 (1+2) 边界，但离 (1+1) 仍有实质距离。若假设 Elliott–Halberstam 猜想，指数可改进为 1.4 | **[预印本主张]** 66 页 arXiv 预印本，未见同行评审记录（截至 2026-11-21） |
| 几乎所有偶数 | van der Corput 1937; Čudakov 1938; Estermann 1938 | E(x) ≪_A x/(log x)^A 对任意 A | **[事实]** 无条件 |
| 例外集定量上界（无条件最优） | Montgomery–Vaughan 1975; Chen–Liu 1989; Li 2000; Lu 2010; **Pintz 2018** | E(x) ≪ x^{1−δ}（M–V，δ>0 可计算）；Li: x^{0.914}；Lu: x^{0.879}；**Pintz: E(x) < x^{0.72}（X 充分大，常数 ineffective）** | **[事实]** 无条件；Pintz 2018（arXiv:1804.09084）是当前记录的公开文献值 |
| Hardy–Littlewood 渐近猜想 | Hardy–Littlewood 1923 | D_{1,1}(N) ~ 2C(N)·N/log²N（C(N) 为奇异级数因子） | **[猜想]** 仍开放；蕴含二元 Goldbach（因为主项正） |

> 结论：**二元哥德巴赫猜想至今开放**。(1+1.9) 是 2026 年无条件结果的新前沿，但 “1+1.9” ≠ “1+1”；从筛法角度看，它把 Chen 的指数 2 推进到 1.9，方向对，但仍隔着筛法的结构性障碍（见 §2.3）。

### 1.3 计算验证（证据，不是证明）

| 范围 | 作者/年份 | 状态 |
|---|---|---|
| 每个偶数 4 ≤ n ≤ 4×10^18 | Oliveira e Silva, Herzog, Pardi, *Math. Comp.* 83 (2014), 2033–2060 | **[事实/同行评审]** 公开基准；这是目前最权威、可审计的验证记录 |
| [4×10^18, 4×10^18 + 10^15]（即到 4.001×10^18） | I. Llorente-Saguer, Zenodo 23346739, 2026-10-13（预印本，单作者，独立研究者） | **[预印本主张]** “fail-closed” GPU 实现，论文围绕“这一个 bit 的可靠性证据”展开；方法学论文，非数学进展 |
| 计算前沿 ~4.0043247639×10^18（2026-10-07 显示值） | “Gridbach”分布式浏览器计算项目 (gridbach.com) | **[未经同行评审的众包主张]**；被上述 2026 预印本引用 |
| 4×10^18 – 6×10^18 | Gosar, Das, Pardasani（据 Llorente-Saguer 转引） | **[未经审计的主张]**：使用概率素性检验，无存档运行记录 |
| 到 9×10^18 | Sankei, Njagi, Mutembei（期刊文章，据 Llorente-Saguer 转引） | **[未经审计的主张]**：无存档运行记录，无法核验 |
| 4 ≤ n ≤ 10^7 | 本报告 §5 的 Python 程序 | **[证据]** 0 失败（见 §5） |

> 诚实说明：计算验证无论做到多大，都**不能证明**猜想（需要覆盖无穷多个偶数）。4×10^18 是同行评审的公开记录；2026 年更高数字均为未经评审/未审计的主张，不能当作“已证明到 9×10^18”。另外，2026 年网络上（Zenodo、preprints.org 等）出现多个声称“完整证明 Goldbach”的预印本，**均未见任何同行评审或权威核验，本报告不予采用**（仅作存在性说明，例：Zenodo records 20024763 / 23634560，标题均为 “A Complete Proof of the Goldbach Conjecture”；未核验、不背书）。这是本领域经典的“crank 论文”高发区，必须警惕。

### 1.4 2026 年 11 月的真正“前沿图景”

按时间线：

1. **2026-06-01**：Li & Liu 在 arXiv 发布 **Theorem (1+1.9)**：无条件越过 Chen 的 1+2，到 1+1.9；在 Elliott–Halberstam 下到 1+1.4。据论文与中文报道，这是筛法路线 60 年来**第一次跨过 1+2 边界**（“1+1.9”），但仍不是 1+1。
2. **2026-11-13**：Li & Liu 在山东大学数学国家高层次人才培养中心（MRC）发布 **《A Conditional Proof of the Goldbach Conjecture》**（63 页 PDF，PDF 创建时间戳 2026-11-13 03:06 +08），宣称**首个对一切充分大偶数成立的二元哥德巴赫条件性证明**；条件 = GRH（Dirichlet L-函数）+ 两个附加谱假设之一。**注意：该文并未上 arXiv（2026-11-21 检索 arXiv 标题/作者均无此文），只有校方页面 PDF；未见同行评审。**
3. **2026-11-20**：Levent Alpöge（Anthropic）宣称与 Claude 一起证明了 **RH 与 GRH**，并给出 Lean 4 形式化；MIT Andrew Sutherland 的核验页面 https://math.mit.edu/~drew/grh/ 显示：源码编译通过、五条主定理只依赖三条标准公理、leanchecker / nanoda / con-leche 等独立内核接受全部导出证明；**该页面明确写着“GRH here means Dirichlet L-functions only”**。截至页面最后更新（2026-11-20 22:05 UTC），Lean 默认内核重放和 `lake comparator` 仍在进行。**尚未经过人类同行评审。**
4. **2026-11-20 前后**：另有 A. M. Masullo 的“The Music of the Primes”宣称证明 RH+GRH；Scientific American 以 “Dueling claims of Riemann hypothesis proofs emerge” 报道两份竞争性声明；PhilArchive 上有 Jenny Lorraine Nielsen 的预印本 **《A Failure of Uniform Boundedness in Masullo’s Proposed Proof of the Generalized Riemann Hypothesis》**，**指控 Masullo 的证明有缺陷**（该指控本身亦未经同行评审）。**[预印本主张]**
5. 2026-11-21（今天）：**二元哥德巴赫仍未解决**；Li–Liu 的条件性证明 + Alpöge 的 GRH 宣称，合起来仍然**不构成**无条件证明（理由见 §3）。

---

## 2. RH/GRH 与哥德巴赫：逻辑关系（本报告的核心）

### 2.1 直接答案

**没有任何已知定理给出 “RH ⇒ 二元 Goldbach” 或 “GRH ⇒ 二元 Goldbach”。**

支撑这一点的最直接、最新的书面陈述来自 2026 年的两篇论文作者本人：

- Li & Liu（2026-11-13，条件性证明，§1.1 引言，原文）：
  > “No proof of the binary conjecture is known under the generalized Riemann Hypothesis (GRH) alone, even when GRH is assumed for all Dirichlet L-functions. Under this hypothesis, Hardy and Littlewood [6] obtained the classical exceptional-set bound E(x) ≪_ε x^{1/2+ε} for every ε > 0, … **This estimate does not exclude exceptions altogether.**”
- Pintz（2018，arXiv:1804.09084，Goldbach 例外集当前记录保持者）：
  > “The first non-trivial, although conditional, estimate for the exceptional set … was achieved by Hardy and Littlewood [8] in 1924. They showed under the Generalized Riemann Hypothesis (GRH) the estimate E(X) ≪_ε X^{1/2+ε} … This result is apart from the substitution of X^ε by log^c X by Goldston [6] even today the best conditional result on GRH.”

也就是说：**GRH 在二元哥德巴赫问题上已知的最好“推论”只是例外集 ≪ x^{1/2+ε}**（“几乎所有”），不是“全部”。至于“RH 单独”（不对 Dirichlet L-函数加 GRH）则连这个都给不了太多——因为二元哥德巴赫的圆法处理需要所有模数的 Dirichlet L-函数信息。

### 2.2 为什么？圆法图景（可给聪明外行讲的版本）

把“N 是不是两个素数之和”写成 Fourier/圆法积分（von Mangoldt 加权）：

  r_Λ(N) = Σ_{p₁+p₂=N} log p₁ log p₂ = ∫₀¹ S(α)² e(−Nα) dα，  S(α) = Σ_{n≤N} Λ(n)e(nα)。

- **优弧（major arcs）**：α 接近分母小的有理数 a/q。这里 S(α) 的行为由**素数在等差数列中的分布**决定——这正是 GRH 管的地方（GRH ⇒ 强 PNT-AP、无 Siegel 零点）。优弧贡献出主项（≈ 奇异级数 × N，对应 N/log²N 的素数对个数）。
- **劣弧（minor arcs）**：α 的“分母”大。这里需要 S(α) 的**随机式抵消**。这是加性结构问题，不是 L-函数零点问题；GRH 对它提供不了足够强的控制。
- **关键量级障碍**：二元哥德巴赫（去掉 von Mangoldt 权重后的）素数对个数主项大小是 **N/log²N**（加权积分的主项则是 ≍N）；而劣弧积分的平凡/目前可得上界（即便用上 GRH 能给出的最好逐点估计和 L² 方法）远大于此。三元问题的主项是 N²/log³N，劣弧用 Vinogradov 型估计（N²/(log N)^A）就能压住，所以圆法成功；二元问题主项比三元小了一个 log²N 量级，圆法分离不开，**这正是“弱 Goldbach 能证、强 Goldbach 不能证”的算术原因**。
- GRH 只描述“素数整体/按模分布的误差”（乘性信息），而二元哥德巴赫问的是“素数集合的**加法**结构：P+P 是否覆盖所有偶数”。这两类信息之间没有已知的一般推理通道。**用类比说**：一个集合可以密度极均匀、素数在等差数列中分布极好，但它与自己的和集是否覆盖每个偶数，仍是另一个问题；RH 保证的是前者的误差最小。**（注：此段是量级直觉说明，不是形式化论证；但“GRH 不足”这一结论有文献原文支持。）**
- 另外，Tao 在五素数论文（arXiv:1201.6656）中也指出：即便是**三素数**的圆法证明，其劣弧估计也受 Siegel 零点问题限制（“one cannot hope to obtain a bound for S(x,α) better than x√(φ(q))/q without making progress on the Siegel zero problem”）；而这些都还只是与素数在 AP 中分布相关的那一半困难。二元问题的困难在其之外。

### 2.3 筛法路线与“奇偶屏障”（parity problem）

**[事实] 这是另一条独立障碍，RH 对此完全无能为力。**

- Selberg 筛法的经典**奇偶问题（parity problem）**：筛法（Brun/Selberg 型，权重非负）本质上只能给出“某集合中素数个数”的上界，无法区分“有偶数个素因子”与“有奇数个素因子”的数；因此纯筛法**无法证明**哥德巴赫类型（要求两个因子同时恰为素数）或孪生素数猜想。标准文献：Friedlander & Iwaniec, *Opera de Cribro*, AMS Colloq. Publ. 57 (2010)（哥德巴赫/孪生问题的筛法极限讨论）、Halberstam & Richert, *Sieve Methods* (1974)。
- Chen 定理 (1+2) 的关键是 **switching principle（切换原理）**（Chen 1966/1973；Fouvry–Grupp 1986 等）：先证明 N−p 要么是素数要么是两个素数乘积，再切换再筛——但它**只能给出上界方向的估计，从不给出下界**。2026 年 Li–Liu 的 (1+1.9) 论文 §8.1/§8.2.1 对此有非常清晰的现代说明：
  > “In the weighted sieve method, the fundamental reason why we employ multiple Buchstab iterations … is that **applying the switching principle yields only upper bounds, never lower bounds**.”
- 因此，(1+2) → (1+1) 的“最后一步”不是把某个误差再压小 0.1，而是**改变信息的类型**：要么找到越过 parity 屏障的新机制（额外的算术/谱结构输入），要么用完全不同的方法。RH/GRH 是不含“加法信息”的 L-函数零点命题，不能越过这个屏障。**这是“为什么 RH 不能推出 Goldbach”的最简答案。**

### 2.4 GRH 究竟能推出哪些与 Goldbach 有关的精确结论（逐条核实）

| # | 条件性陈述 | 来源/年份 | 现状 |
|---|---|---|---|
| (a) | **GRH ⇒ 每个充分大奇数 = 三个素数之和**（三素数定理的条件性证明） | Hardy & Littlewood, *Partitio Numerorum* III, Acta Math. 44 (1923), 1–70 | **[事实]** 历史性结果；1937 年 Vinogradov 去掉 GRH；Helfgott 2013 完成全部奇数 n>5。今日仅具历史意义 |
| (b) | **GRH ⇒ 二元 Goldbach 例外集 E(x) ≪_ε x^{1/2+ε}**；Goldston (1992) 改进为 E(x) ≪ x^{1/2}(log x)^c | Hardy & Littlewood, *Partitio Numerorum* V, Proc. LMS (2) 22 (1924), 46–56；Goldston, Amalfi Conf. Proc. (1992), 115–155 | **[事实]**（GRH 下）。**只给出“几乎所有”，无法排除任何例外**。标准教科书参考：Montgomery & Vaughan, *Multiplicative Number Theory I: Classical Theory*, CUP 2007, §18.3 “Conditional estimates”（见 MathOverflow 501900 的说明） |
| (c) | **仅 GRH ⇒ 二元 Goldbach 对一切充分大偶数成立** | —— | **[不存在]**：无此定理。Li–Liu 2026 明确写“No proof … known under GRH alone” |
| (d) | **GRH + Hypothesis S（或更强的 R） ⇒ 二元 Goldbach 对一切充分大偶数成立**（且给出素数对数量 ≫ S(N)N/log²N，素数都落在 [N/3, 2N/3]） | Li & Liu, 2026-11-13（条件性证明，Theorem 1.1/1.2） | **[预印本主张]** 这是**唯一已知的**“GRH + 额外假设 ⇒ 二元 Goldbach”的条件性定理；额外假设见 §3.1 |
| (e) | **Hardy–Littlewood 渐近猜想（比 GRH 强得多）⇒ 二元 Goldbach** | Hardy–Littlewood 1923 | **[事实]**（显然：主项正即可推出 N 充分大时表示数 > 0）；但 HL 猜想本身比 GRH 强，且远未证明 |
| (f) | **Elliott–Halberstam 猜想 + 加权筛 ⇒ (1+1.4)**（不是 1+1） | Li & Liu, arXiv:2606.05224v2（2026） | **[预印本主张]**；EH 是“素数在 AP 中分布水平达到 1−ε”的猜想。它把 1+1.9 推到 1+1.4，仍不是 1+1 |
| (g) | **Montgomery 对相关猜想 / Chowla 猜想 / Hooley 假设等 ⇒ 二元 Goldbach？** | —— | **未发现已知蕴含**。本报告检索了相关文献与讨论（含 MathOverflow），没有找到“由这些标准假设推出二元哥德巴赫”的定理；任何这类说法都应视为未证实 |

### 2.5 常见误区，逐条反驳

1. **“RH 说明素数分布最规则，所以偶数一定能写成两素数之和”——错。**
   RH 只给“素数计数误差最小”，这是关于 π(x) 与 AP 分布的全局/乘性信息；不能推出加法覆盖。文献中“GRH 下只能得到几乎所有偶数”正是这一事实的体现（§2.4(b)）。
2. **“既然 RH 已经被证明了，哥德巴赫当然跟着成立”——错。**
   RH 是定理 ⇒ 所有“RH ⇒ X”的定理变成无条件定理 X。但文献中**不存在** “RH ⇒ 二元 Goldbach”这样的定理（§2.1、§2.4(c)）。新证明改变的是假设的真值，不改变“假设与结论之间有无推导链”这个逻辑事实。
3. **“GRH 下几乎所有的偶数都满足，所以剩下的只是技术问题”——错。**
   “排除最后一个例外”恰恰是全部困难所在：E(x) ≪ x^{1/2+ε} 意味着例外集可能永远非空；所有已知方法（包括 2026 年 Li–Liu）都无法在 GRH 内把例外集压成空集。Li–Liu 必须**增加新的谱假设**才行——这本身最有力地说明 GRH 不够。
4. **“网上有人发了证明”——需极谨慎。**
   2026 年 Zenodo/preprints.org 上有多篇“Goldbach 完整证明”预印本，均无同行评审、无核验、无权威背书。本报告不采用（见 §1.3 说明）。

---

## 3. 2026 年的新东西到底改变了什么？

### 3.1 Li–Liu 条件性定理：精确陈述（把 Lead 需要的“两个谱假设”钉死）

**论文**：Jiamin Li & Jianya Liu, *A Conditional Proof of the Goldbach Conjecture*, 63 页，2026-11-13 发布于山东大学 MRC（PDF 创建时间 2026-11-13 03:06 +08；未见 arXiv 版本；未见同行评审）。
**页面**：https://mrc.sdu.edu.cn/english/info/1018/1514.htm （英文）/ http://mrc.sdu.edu.cn/info/1018/2193.htm （中文）
**本地副本**（Lead 提供）：`/home/kiler/rh-work/liu-goldbach.pdf`（文本抽取 `liu-goldbach.clean.txt`）。

**框架**：固定非负对称光滑权 φ ∈ C_c^∞(ℝ)，supp φ ⊂ [1/3, 2/3]，φ(u)=φ(1−u)；定义加权哥德巴赫相关量

  G(N) = (1/N) Σ_{n+m=N, (nm,N)=1} Λ(n)Λ(m) φ(n/N) φ(m/N)， c_φ = ∫₀¹ φ²(u)du，

以及奇异级数 S(N) = 2C₂ Π_{p|N, p>2} (p−1)/(p−2)，C₂ = Π_{p>2}(1 − 1/(p−1)²)。

**GRH(N)**（论文的定义，比全局 GRH 弱、逐 N 陈述）：每个整除 N 的本原 Dirichlet L-函数的每个非平凡零点实部为 1/2。

**构造**：用奇 Dirichlet 特征标的正交性把 G(N) 精确投影；扣掉对角项与 Beta 函数模型后，在 GRH(N) 下残差定义出 Hardy 空间上一个**紧自伴 Hilbert–Schmidt 算子 T_N**；得到精确二次型恒等式 c_φ S(N) − G(N) = ⟨T_N v_N, v_N⟩，故 |G(N) − c_φ S(N)| ≤ ‖T_N‖·‖v_N‖²。由 T_N 的谱（特征值 μ_j(N)）定义四元数变量的对称谱函数

  X_N(q) = Π_j ( 1 − 4μ_j²(N) / (δ_N² q(1−q)) )， q ∈ ℍ（四元数）， δ_N = √(S(N)/N)·(log N)^{3/2}。

X_N 的零点位置控制 ‖T_N‖。两个附加假设（原文）：

> **Hypothesis S.** 事先固定一个正函数 h(N) → ∞，使得最终 η_N := h²(N)(log N)³/(N S(N)) ≤ 1/4。对每个充分大、满足 GRH(N) 的偶数 N，函数 X_N(q) 在 ℜq > 1 − η_N 内无零点。
>
> **Hypothesis R.** 对每个充分大、满足 GRH(N) 的偶数 N，X_N(q) 的每个零点的实部都等于 1/2。

**定理**：

> **Theorem 1.1**：假设对所有充分大偶数 N 有 GRH(N)，并假设 Hypothesis S（给定 h），则 G(N) = c_φ S(N) + O_φ(S(N)/h(N))。特别地 G(N) ~ c_φ S(N)。
>
> **Theorem 1.2**：假设对所有充分大偶数 N 有 GRH(N)，并假设 Hypothesis R，则 G(N) = c_φ S(N) + O_φ( √(S(N)/N)(log N)^{3/2} )。
>
> 两个定理都推出：每个充分大的偶数 N 都有 ≫_φ S(N)·N/(log N)² 个有序表示 N = p₁ + p₂，且两个素数都在 [N/3, 2N/3] 内。

**关键：GRH 本身推不出 S 或 R。** 论文 §2.4.3 给出 GRH 单独能得到的算子范数界 ‖T_N‖ ≪ (log N)²，对应谱零点排除区

  ℜq > 1 − η_N^{GRH}，  η_N^{GRH} ≍ S(N)/(N log N)，

而 Hypothesis S 需要的宽度是 η_N = h²(log N)³/(N S(N))；两者之比

  η_N / η_N^{GRH} ≍ h²(N)(log N)⁴ / S²(N) → ∞   （用 S(N) ≪ log log N）。

原文（§1，先于定理）：
> “In fact, GRH alone already gives a zero-free region for X_N of the same form. Its width, however, falls short of that required by Hypothesis S, so the resulting estimate is not strong enough to make the Goldbach error o(S(N)).”

也就是说，**S/R 是严格强于 GRH 的新假设**，不是 GRH 的推论，也不是任何已知标准猜想的推论（论文没有声称它们由别的东西推出；见 §4.1）。

**数值证据（论文附录 B，仅有限模型，不是证明）**：N = 30030 = 2·3·5·7·11·13，φ(N)=5760；用特征积分+有限修正恢复出 30030 的**恰好 905 个无序哥德巴赫表示**（=1810 有序），与直接枚举一致。有限谱模型用 2562 个节点（边界竖线高度 40、网格 1/16）、素数截断 2×10^5 近似，得到 ‖C‖/δ_N ≈ 0.826864 < 1，从而**该有限模型**的零点全部落在 ℜq=1/2 上。作者明确声明这**不能**证明 Hypothesis R（原文：“they do not certify Hypothesis R for T_{30030,1}”），也未给出全算子的截断/离散误差界。

### 3.2 把 Alpöge 的 GRH 定理代入 Li–Liu：还剩什么？

**逻辑链**（本报告的分析，非论文原文）：

1. Alpöge/Claude 的定理（若最终被接受）给出 **GRH for all Dirichlet L-functions**（MIT 页面：“GRH here means Dirichlet L-functions only”）。这恰好覆盖 Li–Liu 的 GRH(N)（N 的本原 Dirichlet L-函数是全体 Dirichlet L-函数的一部分）。
2. 于是 Li–Liu 的两个定理可以重写为：
   - **Hypothesis S ⇒ 二元哥德巴赫**（对所有充分大偶数）——若 S 中的 h 可选；
   - **Hypothesis R ⇒ 二元哥德巴赫**（对所有充分大偶数），且带显式误差项。
3. 但 **Hypothesis S 和 R 至今没有任何证明**；它们既不是 GRH 的推论（§3.1 的量级论证），也不是其他已知定理的推论。并且它们在文档里被作者称为“附加谱假设”，R 被作者称为 “the stronger, ultimate conjecture”。
4. 所以：**即使用 2026-11-20 的 GRH 定理，二元哥德巴赫仍然需要两个全新的、未证明的数学命题。** 这正是“在 RH 的基础上证明 Goldbach”在 2026 年能走到的最远处——**仍差两个假设**。
5. **公开讨论情况（截至 2026-11-21）**：我们在中英文网络上检索后，**没有发现**有人在 Alpöge/Claude 的 RH 公告（2026-11-20）之后公开讨论“新 GRH 定理能否闭合 Li–Liu 条件性证明”这个问题——从时间上看也很自然：Li–Liu 条件性论文发布于 2026-11-13，比 RH 公告早 7 天，其写作时 GRH 仍是假设；而论文作者自己论证 GRH 不足以推出 S/R（§3.1）。网络上关于 Li–Liu 论文的公开讨论主要是中文科普/论坛（见 §7 引用 12），其标题与结论也都明确说“哥德巴赫没被攻克/论文没有证明哥德巴赫”。因此，“用新 GRH 定理消去 Li–Liu 的 GRH 条件、只剩 S/R”这一逻辑后果，是**本报告自己的分析**，而非已有公开文献的报道；请 Lead 引用时注明这是逻辑推论。

**回答 Lead 的问题“这两个谱假设是否独立/是否被新 GRH 定理蕴含？”**：
- **不被蕴含**（论文自己证明 GRH 给的区域严格更窄，比值 → ∞）；
- **也不已知独立**：只是“未被证明、未被反驳”，并且是作者新引入的针对特定算子 T_N 的陈述；
- 它们与 GRH 的关系类似（但不等同）“某个 Hilbert–Pólya 算子的 RH”：Hypothesis R 要求 X_N 的所有谱零点落在临界线 ℜq=1/2 上；Hypothesis S 只要求一个宽度比 GRH 推导宽得多的无零点区。论文还指出：被排除的零点是“靠近端点的实对”，其位置与 **Siegel 零点** 类比（“The excluded zeros are real pairs near the endpoints; the Siegel-zero analogy concerns their location, without asserting uniqueness, simplicity, or repulsion.”）。

### 3.3 哪些“GRH 条件结果”会变成无条件？（仅限与 Goldbach 相关）

如果 Alpöge/Claude 的 GRH 定理被数学界接受，那么经典的“GRH ⇒ …”定理自动升级。与哥德巴赫相关的有：

1. **[真升级] 例外集**：E(x) ≪_ε x^{1/2+ε}（Hardy–Littlewood 1924）与 Goldston (1992) 的 E(x) ≪ x^{1/2}(log x)^c 变成**无条件**。这会把目前最优无条件的 Pintz (2018) x^{0.72} 改进到 x^{1/2+o(1)}——这是 2026 年 RH 定理对哥德巴赫问题**唯一真实的、可陈述的“新无条件定理”**。但它仍然只是“几乎所有偶数”，离二元哥德巴赫差得远。
2. **[无新内容] 三素数定理的 GRH 版本**：早已被 Vinogradov/ Helfgott 无条件化，无所谓。
3. **[部分升级] Li–Liu 条件性定理**：GRH 条件被消去（见 §3.2），但留下 S/R；不是无条件证明。
4. **[无升级] 二元哥德巴赫本身**：因为不存在“GRH ⇒ 二元 Goldbach”的定理可升级（§2.1）。
5. 其他大量 GRH 条件结果（如“least prime in AP”、“Linnik 常数”的 GRH 版本、若干特征和估计）会升级，但与二元哥德巴赫无直接关系；而且 Alpöge 的 Lean 证明目前没有给出显式常数，对“显式”版本的结果帮助有限。

### 3.4 对计算验证的影响

- **直接验证二元 Goldbach 不需要 RH/GRH**：它就是逐个偶数找 p 使 N−p 为素数；RH 不改变验证范式，也不会自动把 4×10^18 的验证“推得更远”。
- RH/GRH 型显式界可用于**间接**证明某区间必有素数（Helfgott–Platt 对三素数定理的数值验证就用了 RH 数值验证来构造“短区间含素数”），但这类技巧用于二元问题需要的是“每个偶数附近有素数对”，RH 给不了。
- Alpöge 的形式化证明目前是“存在性”的，未提供可计算的显式误差常数；即便提供，也只是把“已知所有偶数到 4×10^18 成立”这类有限陈述的条件性证明变得不需要 GRH，不能变成对所有偶数成立。
- 所以：**GRH 的新证明对二元哥德巴赫的计算机验证没有实质推进**；2026 年把记录往后推（4.001×10^18、~9×10^18 等主张）靠的是算力/工程，不是 RH。

---

## 4. 要证明哥德巴赫，真正还需要什么？

### 4.1 具体到 2026 年的两条路线

**(A) Li–Liu 路线**：需要证明 Hypothesis S（对某个增长函数 h）或更强的 Hypothesis R。具体障碍：
- X_N 是由 T_N 的谱**构造**出来的四元数函数，其零点没有已知的解析/代数控制手段；
- 论文的数值只在 N=30030 的有限维近似上验证了“零点像在临界线上”，且明确不能据此证明 R；
- 可能的想法：把 T_N 与某个已知谱理论（Hilbert–Pólya 式算子、自守谱、transfer operator 等）联系起来，从而证明其谱的对称性——**这是纯研究方向，没有任何已证结果**。
- 需要注意的是：即便 S 对某个 h 成立，也仍然需要 h(N)→∞ ——**S 本身是一个比“R 弱、但比 GRH 强”的新猜想**。

**(B) 经典筛法/圆法路线**：
- 把 (1+1.9) 改进到 (1+1)：筛法 + 分布水平（Bombieri–Vinogradov → Elliott–Halberstam 只到 1+1.4，仍不是 1+1）无法越过奇偶屏障；需要新的“加法结构”输入。
- 可能的输入：更强的双线性/三线性指数和估计（minor arcs），或把转移原理（transference principle, Green–Tao、relative Szemerédi）用于素数集——但 Green–Tao 型转移原理目前能给出的“素数内部的加法结构”结论（如任意长等差数列）**不直接给出二元 Goldbach 方程**；哥德巴赫是“两个变量、一个方程”的最难情形，恰在现有转移技术之外。**[研究方向]**
- 另一类可能：利用 2026 年 RH/GRH 证明中出现的新工具（Stepanov 式多重性、theta 提升链、Iwasawa 塔、Rallis seesaw、Bost 斜率不等式等，见 remark.pdf）。这是克劳德/阿尔波格的证明架构；**没有任何迹象表明这些工具能产生素数对的加法信息**——而且目前人类尚未消化该证明本身。**[推测/研究方向，明确不是结果]**

### 4.2 为什么“RH 语言”与“加法结构”正交（给 Lead 的解释）

- RH 是**乘性**对象：ζ（及 Dirichlet L）的零点编码素数在乘法/等差数列意义下的分布误差。
- Goldbach 是**加性**对象：P + P 的和集是否覆盖一切偶数。两个素数的“相加”在 L-函数世界中没有对应的欧拉乘积/零点语言（L-函数只“看见”乘法）。
- 历史上把两者连起来的唯一桥梁是圆法：优弧用乘性信息（GRH），劣弧需要加性抵消——而二元情形劣弧无法控制。**这就是“RH 不蕴含 Goldbach”的深层原因，不是技术细节。**
- 一个容易理解的类比：知道一个城市里人口密度分布极均匀（RH 式信息），并不能保证任意两个街区都有一条直达道路（加法覆盖）。密度均匀有助于“平均意义上”有路，但不能保证“每个目标都有”。

### 4.3 明确不是结果的东西（诚实清单）

- 任何“由 RH/GRH 单独推出二元 Goldbach”的推导：**不存在**。
- 任何“因为 RH 已证，所以 Goldbach 已证/即将被证”的论证：**无效**。
- 任何声称“Li–Liu 条件性证明 + Alpöge GRH 证明 = Goldbach 证明”的说法：**遗漏了 Hypothesis S/R**，无效。
- 本报告提出的任何“可能的想法”（§4.1）都不是结果，没有一条已经走通。

---

## 5. 计算实验（证据，非证明）

脚本：`_rh-work/goldbach/goldbach_demo.py`（本目录），运行环境 Python 3.14 / WSL Ubuntu。
方法：

1. Eratosthenes 筛到 10^7；
2. 对每个偶数 4 ≤ N ≤ 10^7，从最小素数 p 开始找使 N−p 为素数的 p（p ≤ N/2），记录失败数；
3. 对 [10^6, 10^6+4000] 窗口内的偶数计算表示数 r(N) = #{p ≤ N/2: N−p 素数}，给出 comet 式统计。

**输出（2026-11-21 实跑，3.6 秒）**：

```
[A] verified even n in [4,10000000]: failures=0
    largest minimal Goldbach prime p_min up to 10000000: 751 (first at n=3807404)
    record minima (n,p_min): [(4,2),(6,3),(12,5),(30,7),(98,19),(220,23),(308,31),
      (556,47),(992,73),(2642,103),(5372,139),(7426,173),(43532,211),(54244,233),
      (63274,293),(113672,313),(128168,331),(194428,359),(194470,383),(413572,389),
      (503222,523),(1077422,601),(3526958,727),(3807404,751)]
[B] window [1000000,1004000]: evens=2001 min r(n)=3963 max=14883 mean=6146.32
    r(n) min/25%/median/75%/max = 3963/4120/4969/8150/14883
    #n with r(n)=1: 0   #n with r(n)<=2: 0
```

**解读**：到 10^7 为止所有偶数都通过了（0 失败）；最小的“使 N−p 为素数”的 p 在 10^7 内最大只到 751（出现在 N=3,807,404），这与“绝大多数偶数只需很小的素数 p”的经验一致；10^6 附近的表示数在数千量级（r(N) ≈ 奇异级数 × N/log²N），与 Hardy–Littlewood 强度一致。
**这仅是数值证据，不能作为证明。**

---

## 6. 可直接引用给用户的 Bottom line（中文）

> **不能。** 即使接受 2026-11-20 的“RH+GRH 已被证明”这一宣称（它本身尚待人类同行评审，GRH 范围仅为 Dirichlet L-函数），**从 RH/GRH 单独推出二元哥德巴赫猜想在数学上仍然没有任何已知定理**；最新文献（李嘉旻、刘建亚，山东大学，2026-11-13 条件性证明）明确写道：仅假设 GRH（哪怕对所有 Dirichlet L-函数）也推不出二元哥德巴赫。GRH 能做的只是把“不能表示为两素数之和”的偶数压缩成稀疏例外集：E(x) ≪ x^{1/2+ε}（Hardy–Littlewood 1924；Goldston 1992 到 x^{1/2}(log x)^c）——这是“几乎所有偶数”，不是全部。2026 年的真正进展是：① 无条件 (1+1.9)（Li–Liu，arXiv，越过陈景润 1+2 边界但远未到 1+1）；② 第一个条件性二元哥德巴赫证明（Li–Liu, 2026-11-13），但条件是 GRH **加上两个未证明的附加谱假设**（Hypothesis S 或更强的 R）；论文自己证明 GRH 只能给出严格更窄的谱零点排除区，推不出 S/R。因此，把新的 GRH 定理代入后，唯一能得到的结论是“**Hypothesis S（或 R）⇒ 哥德巴赫**”——这两个谱假设仍然无人证明，二元哥德巴赫依然开放。谁若声称已由 RH 证明哥德巴赫，要么遗漏了 S/R，要么不成立；我们不会伪造这样的证明。目前二元哥德巴赫的计算验证记录是 4×10^18（Oliveira e Silva–Herzog–Pardi, Math. Comp. 2014，同行评审）；2026 年有到 4.001×10^18 及更高的未评审/未审计计算主张，但计算永远不能替代证明。

---

## 7. 引用与核查日志

**一手/权威来源（全部 2026-11-21 访问）**

1. Jiamin Li & Jianya Liu, *A Conditional Proof of the Goldbach Conjecture*, Shandong University MRC, posted 2026-11-13, 63 pp.
   - https://mrc.sdu.edu.cn/english/info/1018/1514.htm
   - http://mrc.sdu.edu.cn/info/1018/2193.htm （中文版，摘要同）
   - 本地 PDF：`/home/kiler/rh-work/liu-goldbach.pdf`（PDF 元数据 creationDate 2026-11-13 03:06:10 +08:00；fitz 抽取 63 页）
   - 未上 arXiv（2026-11-21 arXiv API 检索标题/作者均无此文）；未见同行评审。
2. Jiamin Li & Jianya Liu, *Theorem (1+1.9) on the Goldbach Conjecture*, arXiv:2606.05224v2（v1 2026-06-01；v2 2026-08-08；66 页）
   - https://arxiv.org/abs/2606.05224
   - 摘要原文：for 1≤a≤2, Proposition (1+a): every sufficiently large even N = p + rq, r ≤ q^{a−1}, r=1 or prime, p,q primes; proven unconditionally for a=1.9; under Elliott–Halberstam, a=1.4. 另有对偶孪生结果 (1−1.75)（无条件）与 (1−1.4)（EH 下）。
3. L. Alpöge, *remark.pdf*（2026-11-20 公告，4 页）：https://alpo.ge/remark.pdf
   - 原文：“I believe I have … discovered a proof of the Riemann Hypothesis. In fact, the method easily extends much further, resolving the so-called Generalized Riemann Hypothesis, and I expect, with more time, the Extended Riemann Hypothesis too.”（GRH 宣称；并承认自己尚未掌握周边数学、未完成人类可读写作。）
4. A. Sutherland (MIT), *RH Lean proof: verification files*：https://math.mit.edu/~drew/grh/
   - 页面最后更新 2026-11-20 22:05 UTC。摘要：编译通过；五条主定理只依赖 propext/Classical.choice/Quot.sound；leanchecker 全模块重放通过；nanoda、con-leche 独立内核接受完整导出证明；`lake comparator` 与 Lean 默认内核重放仍在进行。
   - **关键原文：“GRH here means Dirichlet L-functions only.”**
5. J. Pintz, *A new explicit formula in the additive theory of primes with applications II. The exceptional set in Goldbach's problem*, arXiv:1804.09084v2 (2018)：
   - 例外集历史与 GRH 条件界 (1.2)：E(X) ≪_ε X^{1/2+ε}（Hardy–Littlewood 1924）；Goldston 1992 改进到 log^c；无条件记录：van der Corput/Čudakov/Estermann 1937–38 E(X) ≪_A X/(log X)^A；Vaughan 1972 X exp(−c√log X)；Montgomery–Vaughan 1975 X^{1−δ}；Chen–Liu 1989 δ=0.05；Li 1999 δ=0.079、2000 X^{0.914}；Lu 2010 X^{0.879}；本文 Theorem 1：E(X) < X^{0.72}（X > X₂，ineffective）。
   - https://arxiv.org/abs/1804.09084
6. H. A. Helfgott, *The ternary Goldbach conjecture is true*, arXiv:1312.7748（2013/2014）：
   - Main Theorem：每个奇数 n > 5 是三个素数之和；§1.2.1：“Hardy and Littlewood [HL23] proved that every odd number larger than a constant C is the sum of three primes, conditionally on the generalized Riemann Hypothesis.”；§1.2.2 引 Oliveira e Silva–Herzog–Pardi：所有偶数 4 ≤ n ≤ 4·10^18 是两素数之和。
   - https://arxiv.org/abs/1312.7748
7. T. Tao, *Every odd number greater than 1 is the sum of at most five primes*, arXiv:1201.6656：
   - 脚注：“the odd Goldbach conjecture is known to be true assuming the generalised Riemann hypothesis; see [9].”
   - https://arxiv.org/abs/1201.6656
8. O. e Silva, S. Herzog, S. Pardi, *Empirical verification of the even Goldbach conjecture and computation of prime gaps up to 4·10^18*, Math. Comp. 83 (2014), 2033–2060.
9. I. Llorente-Saguer, *Fail-Closed GPU Verification of the Even Goldbach Conjecture beyond 4·10^18: Method and Evidence*, Zenodo 23346739, 2026-10-13（预印本）：https://zenodo.org/records/23346739
   - 摘要称验证 [4·10^18, 4·10^18+Δ]，Δ 至 10^15，依赖 4·10^18 的已发表验证；§6 综述了 Gridbach（~4.0043×10^18，2026-10-07）、Gosar/Das/Pardasani（4–6×10^18）、Sankei/Njagi/Mutembei（至 9×10^18）等未审计主张。
10. MathOverflow 501900, “What do know about the exceptional set in Goldbach under various hypothesis”：指出 GRH 下例外集 ≈ √x，来自 ψ_χ(β) ≪ √x(1+√(βx))，并指向 Montgomery–Vaughan《Multiplicative Number Theory I》§18.3 “conditional estimates”。https://mathoverflow.net/questions/501900
11. MathOverflow 341758, “Riemann hypothesis and ternary Goldbach”；427499, “Does asymptotic Goldbach imply GRH?”（后者问的是反向关系，非本报告结论）。
12. 中文科普/讨论：*山东大学刘建亚团队发布“哥德巴赫猜想”首个条件性证明，以算子谱理论重构“1+1”*，数学中国论坛（转自“数学家”公众号 2026-11-15），2026-11-16：http://www.mathchina.com/bbs/forum.php?mod=viewthread&tid=2069475
   - 其中明确写道：“甚至广义黎曼猜想（GRH）本身也不够。在 GRH 下，Hardy 和 Littlewood 得到例外集估计……但没有任何已知方法能从中排除哪怕一个例外。”；“这篇论文没有证明哥德巴赫猜想；它的结论依赖于广义黎曼猜想和两个附加谱假设。”
13. 竞争性 RH 宣称的报道与指控（仅作背景，未采信）：
   - Scientific American, “Dueling claims of Riemann hypothesis proofs emerge”：https://www.scientificamerican.com/article/dueling-claims-of-riemann-hypothesis-proofs-emerge/
   - J. L. Nielsen, *A Failure of Uniform Boundedness in Masullo's Proposed Proof of the Generalized Riemann Hypothesis*, PhilArchive（预印本）：https://philarchive.org/rec/NIEIOM
14. 筛法/奇偶屏障标准参考：J. Friedlander & H. Iwaniec, *Opera de Cribro*, AMS Colloq. Publ. 57 (2010)；H. Halberstam & H.-E. Richert, *Sieve Methods*, Academic Press (1974)；Chen 定理原始：J. R. Chen, Kexue Tongbao 17 (1966) 385–386；Sci. Sinica 16 (1973) 157–176；switching principle：E. Fouvry & F. Grupp, J. Reine Angew. Math. 370 (1986) 101–126。

**核查日志（本报告的独立检查）**

- arXiv API `id_list=2606.05224`：确认 (1+1.9) 摘要/版本/日期（2026-11-21）。
- arXiv API `search_query=au:"Jiamin_Li"`：确认作者其他论文，**未发现** 2026-11-13 条件性 Goldbach 论文的 arXiv 版本。
- arXiv API `search_query=ti:"conditional proof of the Goldbach"`：0 条结果（确认非 arXiv）。
- `mrc.sdu.edu.cn` 英文/中文页面抓取：确认发布日期 2026-11-13、摘要原文、作者。
- `liu-goldbach.pdf` fitz 抽取：63 页，creationDate 2026-11-13 03:06:10 +08:00。
- `math.mit.edu/~drew/grh/` 抓取：确认 2026-11-20 22:05 UTC 的核验状态与 “GRH here means Dirichlet L-functions only”。
- `pintz_exceptional.pdf` 文本抽取：确认例外集历史与定理 1 的 x^0.72。
- `helfgott_ternary.pdf` 文本抽取：确认三素数主定理与 GRH 历史陈述。
- 本地 Python 实验：见 §5。
- 未采用的来源：2026 年 Zenodo/preprints.org 上的“Goldbach 完整证明”预印本（无评审、无核验）；网络论坛中未具名/无出处的“证明”帖子。

---

## 附录 A：Li–Liu 条件性论文的英文原文关键段落（方便 Lead 核对）

**Abstract（摘录）**
> “We give what is, to our knowledge, the first conditional proof of the binary Goldbach conjecture for all sufficiently large even integers, assuming the generalized Riemann hypothesis for Dirichlet L-functions together with either of two additional spectral hypotheses. … Under either spectral hypothesis together with GRH, every sufficiently large even integer N has ≫_φ S(N)N/(log N)² ordered representations as a sum of two primes in [N/3, 2N/3].”

**§1.1 引言（关键句）**
> “No proof of the binary conjecture is known under the generalized Riemann Hypothesis (GRH) alone, even when GRH is assumed for all Dirichlet L-functions. Under this hypothesis, Hardy and Littlewood [6] obtained the classical exceptional-set bound E(x) ≪_ε x^{1/2+ε} for every ε > 0, where E(x) counts the even integers 4 ≤ N ≤ x that are not sums of two primes. This estimate does not exclude exceptions altogether.”

**Hypothesis S / R 与定理（原文，见 §1.2）**
> **Hypothesis S.** Fix beforehand a positive function h(N) → ∞ such that, eventually, η_N = h²(N)(log N)³/(N S(N)) ≤ 1/4. For every sufficiently large even N satisfying GRH(N), the function X_N(q) has no zeros in ℜq > 1 − η_N.
>
> **Theorem 1.1.** Assume GRH(N) for every sufficiently large even N, and Hypothesis S with the prescribed function h. Then G(N) = c_φ S(N) + O_φ(S(N)/h(N)).
>
> **Hypothesis R.** For every sufficiently large even N satisfying GRH(N), every zero of X_N(q) has real part 1/2.
>
> **Theorem 1.2.** Assume GRH(N) for every sufficiently large even N, and Hypothesis R. Then G(N) = c_φ S(N) + O_φ(√(S(N)/N)(log N)^{3/2}).
>
> **GRH alone vs S（§1.2）**：“In fact, GRH alone already gives a zero-free region for X_N of the same form. Its width, however, falls short of that required by Hypothesis S, so the resulting estimate is not strong enough to make the Goldbach error o(S(N)).”

**数值附录（Appendix B）**
> “We recover the number of unordered Goldbach representations of 30030 … The integral value 905.0000000052 determines the exact integer 905 … both give 905 unordered pairs (1810 ordered) … It does not certify Hypothesis R for T_{30030,1}.”

---

## 附录 B：Python 程序与运行输出（可复现）

代码见本目录 `goldbach_demo.py`（内容见下），输出见 §5。

```python
# 核心部分（完整脚本见 goldbach_demo.py）
import math
N = 10**7
sieve = bytearray(b"\x01") * (N + 1); sieve[0:2] = b"\x00\x00"
for i in range(2, math.isqrt(N) + 1):
    if sieve[i]:
        start = i * i
        sieve[start::i] = b"\x00" * (((N - start) // i) + 1)
primes = [i for i in range(2, N + 1) if sieve[i]]
fails = []
for n in range(4, N + 1, 2):
    found = False
    for p in primes:
        if p > n // 2: break
        if sieve[n - p]: found = True; break
    if not found: fails.append(n)
print("failures =", len(fails))
```

**可复现命令**：

```bash
cd /home/kiler/Windows-D/Rieman/_rh-work/goldbach
python3 goldbach_demo.py
```

---

*报告结束。若 Lead 需要把某一段落翻译成给用户的最终答复，建议直接引用 §6 的 Bottom line；技术细节可引用 §3.1/§3.2 与附录 A 的原文。*
