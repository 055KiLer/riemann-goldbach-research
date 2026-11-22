# Phase-7 文献调研：R 路线之后，binary Goldbach 的替代路线

> 作者：goldbach-researcher（task-30）。日期：2026-11-21 20:42–21:50（Asia/Shanghai）。URL 访问日期 2026-11-21。
> 背景：phase-6 数值裁决认为 Li–Liu 的 Hypothesis R 在有限模型中持续失败（raw ratio>1 at N=1e7, 6e7；a≈1.5–1.9），LL 路线（GRH+R⇒Goldbach）渐近上很可能不可用。本报告调研并评估替代路线。
> 标注：**[事实]** 已证/已发表；**[预印本主张]** 未评审；**[推导]**；**[推测]**；**[检索结果]** 未找到/弱证据。所有"对 Goldbach 给出什么"都以 binary（强）Goldbach 为终点。

---

## 0. 五条要点（已先发 lead）

1. **存在一个不依赖 pair correlation/R 的完整条件性 Goldbach 路线**：Gou–Wang–Xu（arXiv:2611.18825, 2026-11-13）Theorem 1.1：**GRH + 本原 Dirichlet L 的 Ratios Conjecture** `RC_D(ω_D)` ⇒ 对每个偶数 N、每个 ε>0，
   `Σ_{m+n=N} Λ(m)Λ(n) = N·𝔖(N) + O_ε(N^{1−ω_D+ε})`。
   取 ω_D=1/2 得 `O(N^{1/2+ε})` < 主项，⇒ **所有充分大偶数都是两素数之和**。这正是 phase-4/5 中 H_Gold 的量级目标，但输入换成了 Ratios Conjecture（CFZ 2008）而非 R。
2. **函数域无条件版本给出蓝图与精确障碍**：G-W-X Theorem 1.5：固定奇素数幂 q>10^200，对任意首一 N（deg d≥3）**无条件** `Σ_{F∈M_{d−1}}Λ(F)Λ(N−F)=q^{d−1}𝔖_q(N)+O_q(q^{23d/24})`。机制 = Sawin–Shusterman Type I/II 分解 →（I）平方自由等差数列中素数分布水平 >1/2（Sawin, Acta Math. 233 (2024)）；（II）**两点 Möbius 相关**用 cohomological sieve（Wan–Zhang Betti 界、Das–Howe 代数筛、判别式上同调、扭曲 Chowla）。到 ℤ 恰好卡在这两点：(I) ℤ 上水平>1/2 属 EH 型开放问题；(II) ℤ 上两点 Chowla/μ 相关即 parity barrier，且无 Frobenius/Weil 上同调、von Mangoldt 和没有 factorization-function 对应。
3. **其它非 R 路线都只到 almost-all / (1+1.x)**：圆法+GRH+新指数和（MPR `N^{19/24}`；Guth–Maynard 大值/零点密度）⇒ `E(X)≪X^{7/12+ε}`（无条件依赖零无半平面）或 GRH 下 `E(X)≪X^{1/2+ε}`——仍是例外集，密度-1 不足以证 Goldbach（phase-6 已证）。EH+加权筛 ⇒ (1+1.4)（Li–Liu）。Gallagher larger sieve 只给稀疏集上界，无 Goldbach 应用。Green–Tao 线性方程定理原文明确排除“binary cases such as the twin prime or Goldbach conjectures”（因不满足“no two forms affinely related”），transference 不能覆盖二元 ΛΛ。Hooley 型条件：未找到能推出全 N 二元 Goldbach 的已知定理。
4. **Alpöge 证明的新算术推论对 Goldbach 无帮助**：MIT 页 “Arithmetic consequences” 只有 Robin/Lagarias 不等式（经 kimihiro64/Robin1984 合并；均为 RH 等价判据，非新定量输入）。Zenodo 阅读指南（Manvir Jaswal, DOI 10.5281/zenodo.24410057, 54 页）确认 archive 核心结论是**定性** `ZeroFreeAll`（所有本原 ψ：L(s,ψ)≠0 for Re s>1/2），链由 Galois 表示/局部参数/VWin（Tate–Shafarevich 界）三输入构成；**没有显式零无区、没有定量 L'/L 或 S(t) 界**。
5. **推荐两条最值得攻击的路线（均非 R）**：
   - **路线 A（Ratios Conjecture 路线）**第一步引理：证明 `RC_D(ω_D)`（本原 Dirichlet L 族，允许 ω_D>0 的 power-saving 误差；或 G-W-X Appendix A 的弱化定性版本）；函数域已有 Sawin 2024 的 harmonic-family 先例。一旦成立即得 Theorem 1.1 的 Goldbach。
   - **路线 B（两点 Möbius/Chowla 相关路线）**第一步引理：对 ℤ 证明 power-saving 两点 Chowla/twisted Chowla 的平均形式（如 `Σ_{h≤H}|Σ_{n≤X}μ(n)μ(n+h)|² = o(HX²)` 或 `Σ_{h≤H}|Σ_{n≤X}Λ(n)Λ(n+h)−𝔖(h)X|²` 的相应平均），这正是 G-W-X 用上同调拿到的 (II)、也是 parity barrier 的核心；已知最好是对数平均 Chowla（Matomäki–Radziwiłł–Tao 2015）。

---

## 1. 背景与替代路线的判据

phase-6 的结论（供本报告使用，不重新论证）：

- **[数值/审计结论，引用 phase-6 报告]** far-N 有限模型 raw ratio>1 在 N=1e7 与 6e7 多配置出现；b≈1（‖Q_N‖≍logN），但 κ_eff 随 N 上升，ratio 不衰减 ⇒ **R 在有限模型中持续失败，渐近上可能为假**；且“R 只在密度-1 集合成立”不足以推出 Goldbach（phase-6 audit 的反例证明）。
- 因此替代路线必须要么 **(i) 对每个 N 给出直接渐近/正下界**（不是 almost-all），要么 **(ii) 给出一个全新的、不依赖跨 χ 四阶相关的机制**。

本报告按三个角度组织：(§2) 函数域→ℤ 的精确机制与障碍；(§3) 其它已知路线逐条评估；(§4) Alpöge 证明的可用性；(§5) 推荐。

---

## 2. 函数域 → ℤ：Gou–Wang–Xu 的机制与阻碍

### 2.1 ℤ 上的条件性 Goldbach（Ratios Conjecture 路线）

**来源**：H. Gou, V. Y. Wang, M. W. Xu, *Landau's problems through ratios of L-functions*, arXiv:2611.18825（2026-11-13；46 页；作者单位：山东大学/中研院/清华-YMSC-BIMSA）。

**Ratios Conjecture（Dirichlet 族，原文 Hypothesis 1.1）**：

> **Hypothesis 1.1 (Ratios of primitive Dirichlet L-functions (RC_D(ω_D))).** Fix 0<ω_D≤1/2. There exist constants η_0>0 and B≥0 such that for every fixed 0<η<η_0 and every ε>0,
> `Σ*_{χ mod q} L(a,χ)L(b,χ)/(L(s,χ)L(t,χ)) = M_q(a,b;s,t) + O_{η,ε}( q^{1−ω_D+ε}(1+T)^B )`,
> uniformly for all conductors q>1, including composite conductors, and all shifts satisfying ℜa=ℜb=1/2, ℜs=ℜt=1/2+η, `T=max{|ℑa|,|ℑb|,|ℑs|,|ℑt|}≤100 log(2q)`. The starred sum is over primitive characters modulo q. The saving ω_D is independent of η.

（Ratios Conjecture 的原始形式：J. B. Conrey, D. W. Farmer, M. R. Zirnbauer, *Autocorrelation of ratios of L-functions*, Commun. Number Theory Phys. 2 (2008) 593–636, arXiv:0711.0718。）

**定理（ℤ 上 Goldbach，原文 Theorem 1.1）**：

> **Theorem 1.1 (Goldbach).** Assume GRH for Dirichlet L-functions, and `RC_D(ω_D)`. For every ε>0 and every even N, we have
> `Σ_{m+n=N} Λ(m)Λ(n) = N·𝔖(N) + O_ε(N^{1−ω_D+ε})`.
> 其中 `𝔖(N)=∏_p σ_p(N)`，`σ_p(N)=p/(p−1)` 若 p|N，`=p(p−2)/(p−1)^2` 若 p∤N（原文 (1.1)）。

**为何这推出 binary Goldbach [推导]**：取 ω_D=1/2，误差 `O(N^{1/2+ε})`；主项 `N𝔖(N)`，而 𝔖(N) ≥ c>0（N 偶数时），故 N 充分大时 `Σ_{m+n=N}Λ(m)Λ(n) > 0`，即存在素数对 m+n=N。**这是“对每个 N”的渐近公式，不是 almost-all。**

**证明机制（§3 “Goldbach from character ratios”）**：
- 用 mod N 字符正交把“m+n=N”投影出来：原文 (3.1)
  `1_{N|m+n} = (1/φ(N)) Σ_{χ mod N} χ(−1)χ(m)χ(n)`。
- 注意 **χ(−1) 因子（parity twist）**：标准 Ratios Conjecture 是**不带** χ(−1) 的（同时对偶/奇特征平均）；作者用 L-函数的函数方程，从**两个 untwisted ratios 平均**中解出 parity-weighted 平均（Lemma 3.1、§3.1：“Applying the two functional equations gives a second linear combination of the sums over even and odd characters. The root numbers cancel because the characters are conjugate.”）。
- 然后对 L'/L 型 Dirichlet 级数（von Mangoldt 系数）做 Mellin 反演/求和，主项给出 Goldbach 奇异级数 𝔖(N)；误差 `q^{1−ω_D+ε}` 经插值传到 N^{1−ω_D+ε}。
- **依赖**：GRH（用于函数方程/零点/误差；脚注说可把 Ratios Conjecture 表述为不依赖 GRH 的形式）+ Ratios Conjecture（核心）。

**与 phase-4/5 的关系 [推导]**：Theorem 1.1 的结论正是 H_Gold（加权二元 HL 渐近，误差 < 主项）；它不需要 pair correlation、不需要跨 χ 四阶零点相关，只需要 Ratios Conjecture 的**族平均比值**信息。这是目前已知“最完整、假设最干净”的条件性 Goldbach 路线。

### 2.2 函数域上的无条件 Goldbach（Theorem 1.5/1.6）

**Setting**：`F_q[T]`，q 奇素数幂；`M_j` = 次数 j 的首一多项式集合；`Λ(P^j)=deg P` 对首一素多项式 P。奇异级数 `𝔖_q(D)=∏_{P|D}(1−|P|^{−1})^{−1} ∏_{P∤D}(1−1/(|P|−1)^2)`（原文 (1.7)）。

> **Theorem 1.5 (Polynomial Goldbach).** Fix an odd prime power q>10^200. Uniformly over monic N of degree d≥3, we have
> `Σ_{F∈M_{d−1}} Λ(F)Λ(N−F) = q^{d−1}𝔖_q(N) + O_q(q^{23d/24})`.

> **Theorem 1.6 (Polynomial prime pairs).** Fix an odd prime power q>10^200. For n≥1, uniformly over 0≠h∈F_q[T] of degree less than n,
> `Σ_{F∈M_n} Λ(F)Λ(F+h) = q^n𝔖_q(h) + O_q(q^{23n/24})`.

**Status [预印本主张]**：定理是**无条件**的（函数域），但 q 固定且充分大（>10^200），误差 `q^{23d/24}` 远小于主项 `q^{d−1}`。作者说明：在 Sawin–Shusterman [SS22a] 的先行结果下，主项渐近只对 q=p、p² 是新的；误差项可能对其他 q 也是新的。

**证明机制（§1.5 原文摘述）**：
1. 用 Sawin–Shusterman [SS22a, §6] 的 **Type I/II 除子分解**把问题化为两类输入：
   - **(I) 平方自由等差数列中素数分布水平 >1/2**：用 Sawin, *Square-root cancellation for sums of factorization functions over squarefree progressions in F_q[t]*, Acta Math. 233 (2024) 285–418（arXiv:2102.09730）。
   - **(II) 两点 Möbius 相关（two-point Möbius correlations）**：用受 Twisted Chowla 工作（Anderson–Chow–Dietmann–Hokken–Koymans–Lemke Oliver–Sawin–Shusterman, arXiv:2608.22297）启发的筛法论证。
2. (II) 的微妙点：本文 q 固定而 [ACD+26] 取 q→∞；为此需要**固定正特征下的 Betti 数界与上同调筛**：
   - Betti 数界：Wan–Zhang, *Betti number bounds for varieties and exponential sums*, Adv. Math. 490 (2026) 110852（arXiv:2501.12623）；早期 Katz 的工作对大 q 也可用。
   - 判别式补集的参数化/低次参数化：受 Sawin–Shusterman [SS25, App. B] 启发。
   - **Das–Howe 代数筛框架**（*Cohomological and motivic inclusion–exclusion*, Compos. Math. 160 (2024) 2228–2283）把平方自由多项式空间（判别式补集）退化到可计算 signed homology 的空间；在正特征中退化到“适当 resultant 的补集”，使某些导数与某些多项式解耦，从而 signed homology 在次数线性范围内可计算且消失（即得到所需相消）。
3. 结论：`23d/24` 指数 = 与整数情形 `N^{19/24}` 的 minor-arc 指数相似的“余项指数”（作者未直接这样类比，这是我们 [推导]）。

### 2.3 到 ℤ 的精确障碍（逐条）

| # | 函数域机制 | ℤ 上的障碍 | 精确陈述/引文 |
|---|---|---|---|
| (a) | **Frobenius/Weil 上同调**：对 F_q 上代数簇，Frobenius 特征值 + Deligne 界 + 上同调筛（Das–Howe）；signed homology 消失给出两点 μ 相关的相消 | Spec ℤ 没有 Frobenius 自同态；Weil 上同调对 ℤ 是猜想（motives/Tate），不能作为无条件工具 | G-W-X §1.5/§7；[推导] 本文 |
| (b) | **Λ 的代数对应**：函数域中 Λ(F)（次数）与 factorization functions 的除子和可通过几何/上同调计数；平方自由性由判别式控制 | ℤ 的 von Mangoldt 函数没有 factorization-function/除子和的代数结构；“平方自由模 + 判别式”没有直接算术类比 | G-W-X §1.5；[推导] |
| (c) | **(I) 水平 >1/2**：Sawin 2024 在 F_q[t] 平方自由等差数列证明平方根相消（无条件） | ℤ 上平方自由（或光滑）模的 Bombieri–Vinogradov 型水平 >1/2 是 **Elliott–Halberstam 型开放问题**；Bombieri–Friedlander–Iwaniec (1986) 只到 4/7 的**特殊模**，一般情形未知 | Sawin Acta 233 (2024)；BFI 1986；[事实] |
| (d) | **(II) 两点 μ 相关**：上同调筛证明 q 固定时的两点 Möbius 相关 | ℤ 上两点 Chowla/Möbius 相关即 **parity barrier**；即使平均版本也极难（当前最好：Matomäki–Radziwiłł–Tao 的对数平均 Chowla, Algebra & Number Theory 9 (2015) 2167–2196） | [事实]；G-W-X §1.5 |
| (e) | **Ratios Conjecture 的角色**：函数域上 Ratios Conjecture for harmonic families 已由 Sawin 2024 证明（这是他们能无条件的深层原因之一） | ℤ 上 Ratios Conjecture（CFZ 2008）是**猜想**；G-W-X 的 Theorem 1.1 把它作为假设。Lee (arXiv:2610.32672v2) 用 uniform zeta-ratios 假设证明 fixed even difference 的 prime pairs HL 渐近——同类条件性结果 | Conrey–Farmer–Zirnbauer 2008；Sawin 2024；Lee 2026 |
| (f) | q>10^200 **固定**、次数 d→∞：有“q 大”自由度（Betti 界、Katz/Deligne 只需大 q） | ℤ 没有 q→∞ 参数；所有障碍都是绝对的 | G-W-X Theorem 1.5 陈述 |
| (g) | 主项已知范围：对 q=p,p² 由 Sawin–Shusterman 2022 已知，本文新在误差/一般 q | ℤ 上完全没有对应主项定理 | G-W-X §1.3（"only new for q=p,p²"） |

**结论 [推导]**：函数域证明的“可转移部分”是一个**条件性蓝图**：若在 ℤ 上同时拥有 (I) 水平>1/2（EH 型）和 (II) 两点 Möbius 相关，则 G-W-X 的 Type I/II 框架可能给出无条件 Goldbach；而 **Ratios Conjecture 路线是绕开 (a)(b) 的另一条条件性路径**（§2.1），它不需要上同调，但需要 CFZ 猜想。

---

## 3. 其它非 pair-correlation 路线：逐条精确陈述与缺口

### 3.1 圆法 + GRH + 新指数和（minor arcs）

**已证/预印本工具**：

- **[预印本]** J. Maynard, M. Pandey, M. Radziwiłł, *Exponential sums over primes*, arXiv:2608.14777（2026-08-14）。摘要原文：
  > “Let α=a/q+ε with (a,q)=1, q≤N^{1/2} and |ε|≤1/(qN^{1/2}), and let B:=max(q,qN|ε|). We show that |Σ_{n<N}Λ(n)e(nα)| ≤ N^{o(1)}(N/B^{1/2}+N^{19/24}). This improves on the classical bound of Vinogradov from 1937, which has N^{4/5} in place of N^{19/24}.”
- **[预印本]** L. Guth, J. Maynard, *New large value estimates for Dirichlet polynomials*, arXiv:2405.20552（2024-05-31）。摘要：新的大值估计 ⇒ 零点密度 `N(σ,T)≤T^{30(1−σ)/13+o(1)}` 与长度为 `x^{17/30+o(1)}` 的短区间素数渐近。
- **[预印本]** Pintz–Althöfer, arXiv:2610.15559：用上述 19/24 得例外集 `E(X)≪X^{7/12+ε}`（条件于任一固定零无半平面 Re≤θ0<1）；在 `H_θ`（1/2≤θ≤2/3）下 `E(X)≪X^{g(θ)+ε}`，g(1/2)=1/2（即 GRH 情形 `E(X)≪X^{1/2+ε}`）。

**对 binary Goldbach 给出什么**：只给**例外集**上界。即使 GRH 成立（⇒ E(X)≪X^{1/2+ε}），仍有 `O(X^{1/2+ε})` 个例外偶数无法排除。

**剩余缺口 [推导]**：要从“almost-all”变成“all”，需要**逐 N** 的 minor-arc 估计：圆法积分中 minor arcs 的贡献必须 < 主项（约 `N/log²N`，对 ΛΛ 加权约 `N𝔖(N)` 的误差要 o(N)）。现有方法（Vinogradov / 19/24 / 大值估计）给出的量级远大于此；并且 phase-6 已证明“密度-1/例外集”型信息在逻辑上不能推出全 N Goldbach（非负性对稀疏补集无效）。**这条路在现有技术下不闭合。**

### 3.2 大筛 / Gallagher larger sieve

- **[事实] Gallagher 的 larger sieve**（*A larger sieve*, Acta Arith. 18 (1971) 77–81）：若集合 A⊂[1,N] 在模每个素数 p≤N 时只占至多 ν(p) 个剩余类，则 |A| 的上界形如
  `|A| ≲ N·(Σ_{p≤N} ν(p)log p/p) / (Σ_{p≤N} ν(p)log p − log N)`（在分母正时；精确形式见 Gallagher 原文/标准文献）。
  应用：证明某些稀疏整数集的界（如素数元组、广义 Ramanujan 素数等），**没有**已知的 binary Goldbach 应用。
- 相关：[检索结果] 未找到 “larger sieve ⇒ Goldbach” 的定理；larger sieve 是上界工具，不能产生两素数之和的正下界。

### 3.3 almost-all 结果（已有精确陈述）

- **[事实]** van der Corput/Čudakov/Estermann 1937–38：`E(X)≪_A X/(log X)^A`；
- **[事实]** Montgomery–Vaughan 1975：`E(X)≪X^{1−δ}`（某计算 δ>0）；后续显式 δ：Chen–Liu 0.05、Li 0.079→X^{0.914}、Lu X^{0.879}、Pintz X^{0.72}、Zhao (arXiv:2511.05631) X^{7/10}；
- **[事实，GRH 下]** `E(X)≪_ε X^{1/2+ε}`（Hardy–Littlewood 1924；Goldston 1992 log 改进；2026 年 Bhowmik–Grimmelt survey arXiv:2607.27282 Thm 3.1 与 Pintz–Althöfer Thm 3 给出精确形式）；
- **[推导]** 全部是 almost-all；不能推出 Goldbach（phase-6 audit 的密度-1 反例）。

### 3.4 Elliott–Halberstam / Hooley 型条件

- **[事实] Elliott–Halberstam 猜想（EH）**：素数在等差数列中的分布水平可到 `1−ε`；已知 Bombieri–Vinogradov 给 `1/2`（平均意义）。
- **[预印本主张] EH 的已知 Goldbach 后果**：Li–Liu, *Theorem (1+1.9)*, arXiv:2606.05224v2：无条件 (1+1.9)（`N=p+rq, r≤q^{0.9}`）；**在 EH 下改进为 (1+1.4)**（摘要原文：“Assuming the Elliott–Halberstam Conjecture, the exponent 1.9 can be improved to 1.4.”）。仍不是 (1+1)。
- **[检索结果] Hooley 型条件**：未找到“某 Hooley 型假设 ⇒ 全 N 二元 Goldbach”的已知定理。文献中 Hooley 的工作主要在短区间素数、素数多项式等方向；与 binary Goldbach 的已知联系是间接的（经几乎-all/指数和），没有可引用的完整蕴含。**建议 Lead 不要把 Hooley 型条件列为可行的 Goldbach 路线。**
- **剩余缺口**：EH 只控制素数在 AP 中的分布（“major arcs”信息），不触及两点 ΛΛ 相关的 parity 核心；从 1.4 到 1 没有已知路径。

### 3.5 加性组合 / transference 原理

- **[事实] Green–Tao, *Linear equations in primes*, Ann. of Math. 171 (2010) 1755–1850**（arXiv:math/0606088）原文（引言，逐字）：
  > “In this paper we (conditionally) verify this asymptotic under the assumption that no two of the affine-linear forms ψ_1,…,ψ_t are affinely related; **this excludes the important ‘binary’ cases such as the twin prime or Goldbach conjectures**, but does allow one to count ‘non-degenerate’ configurations such as arithmetic progressions.”
- 即：Green–Tao 的 finite-complexity 线性方程理论**明确排除**二元 Goldbach/孪生素数。transference 原理（Green 2005；Green–Tao 2008 “The primes contain arbitrarily long arithmetic progressions”）处理的是“素数中的多变量组态”，对二元 ΛΛ 不适用；parity barrier 是同一障碍的另一面（见 phase-1/5/6 报告；Friedlander–Iwaniec, *Opera de Cribro*, AMS 2010）。

### 3.6 熵方法

- **[检索结果]** Tao 的 entropy decrement 方法（及后续）用于证明素数中模式/线性方程的存在性（与 Green–Tao 框架配合），没有已知的 binary Goldbach 应用；就其现有形式不能给出两点 ΛΛ 的正下界。**[推测]** 熵方法若要有用，必须先在某种意义下越过 parity barrier，这与 §3.4/§3.5 的困难同源。

### 3.7 Ratios Conjecture 路线（本报告中唯一“完整”的条件性路线）

见 §2.1。它不属于 pair-correlation，也不需要跨 χ 四阶零点相关；只需要 **族平均比值** 的 power-saving 误差。与 Lee 的 twin-prime 工作（arXiv:2610.32672v2：从 restricted uniform 2/2 zeta-ratios 公式证明 fixed even difference 的 HL 渐近；Ratios 误差 `O(U^{ϑ+ε})`, `1/2≤ϑ<(39−√177)/32`；RH 下误差可改善）同一思想。

**缺口**：Ratios Conjecture 在 ℤ 上未证；它比 RH 强吗？至少它蕴含许多 pair-correlation 型结论。函数域上由 Sawin 2024 对 harmonic families 证明，是唯一已知的“接近”证据。

---

## 4. Alpöge 证明的新算术推论：对 Goldbach 是否有用？

### 4.1 MIT 页 “Arithmetic consequences”

- **[事实]** 2026-11-21 09:30 UTC 版 MIT 页（https://math.mit.edu/~drew/grh/）新增：把主证明与 kimihiro64/Robin1984（commit acab1a3，独立形式化的 Robin/Lagarias 判据）合并，得到两个**无假设、不提及 ζ** 的定理：
  - `robin_inequality : ∀ n > 5040, σ(n) < e^γ n log log n`；
  - `lagarias_inequality : ∀ n > 0, σ(n) ≤ H_n + e^{H_n} log H_n`。
- 这两条是 **RH 的等价判据**（Robin 1984、Lagarias 2002），属于“验证 ζ 的定义/算术后果一致性”的交叉检验，**不是新的定量分析输入**（对 Goldbach 无用）。

### 4.2 Zenodo 阅读指南（Manvir Jaswal, DOI 10.5281/zenodo.24410057）

- **[预印本/阅读指南]** 54 页 PDF，2026-11-21 创建；描述 Alpöge Lean 形式化：五条定理；核心链：
  - 主定理 (b) 归约为 `ZeroFreeAll`：所有本原 ψ（含平凡）满足 `L(s,ψ)≠0` for `Re s>1/2`（CB/Imprimitive.lean:5；TGC/ExplicitFormulaErrorOfHostConditions.lean:18）；
  - 三输入：Galois 表示（Row0b IsRecT）、GL_n 有限位局部参数、**VWin：Tate–Shafarevich 群（Tate twists）的长度上界**；
  - 中间件：theta lift 链、slope inequality、covolume/orthogonality、Kato Euler system、U(3) 自守形式同余等。
- **关键结论 [事实/阅读]**：archive 的最终陈述是**定性的零无半平面**（`ZeroFreeAll`）；**没有**显式零无区（没有 `π(x)` 误差的显式常数）、**没有**定量 L'/L 界、**没有** S(t)（辐角）界。Jaswal 的“bound for Tate–Shafarevich groups”是证明内部输入，不是可用的经典定量推论。
- [推测] 即使形式化证明将来被提取出显式常数，按 phase-6 alpoege-scan 的结论，也不足以给出跨 χ 四阶矩/pair correlation；对 Goldbach 的 R/H_Gold 路线没有直接帮助。

---

## 5. 结论：推荐的两条路线（都不是 R 路线）

### 路线 A：Ratios Conjecture 路线（首推）

**理由**：唯一已知能对**每个**偶数 N 给出渐近公式（从而 Goldbach）的非 pair-correlation 路线；假设是单一、明确、有文献积累的猜想（CFZ 2008）；函数域上已有 Sawin 2024 的无条件版本作“可行性证据”；G-W-X 已把实现该路线的完整链条写出（§3：parity twist + Mellin + 误差插值）。**它也是 H_Gold 的最自然替代**（phase-4/5 的 H_Gold 正是 Theorem 1.1 的结论）。

**第一步技术引理（具体）**：
> 证明 `RC_D(ω_D)` 的本原 Dirichlet 情形（甚至只需要 q 为素数、ω_D 任意固定正数、误差均匀到 `|ℑ|≤100 log(2q)`）：即
> `Σ*_{χ mod q} L(1/2+a,χ)L(1/2+b,χ)/(L(1/2+η+is,χ)L(1/2+η+it,χ))`
> `= M_q(a,b;s,t) + O_ε(q^{1−ω_D+ε})`，`ω_D>0` 固定。
> 更实际的第一小步：对**素数模 q** 证明 2/2 ratios 的 power-saving（可参考 Lee 的 restricted zeta-ratios 版本、Wang–Xu 的 prime-conductor 猜想），或先证明 G-W-X Appendix A 的弱化定性版本（其 Theorem 1.1 只需 ω_D>0）。

**判据**：若只能证 ω_D 很小的版本，误差 N^{1−ω_D+ε} 仍 < N，足以得到充分大 N 的 Goldbach。**因此这条路线对假设的“强度”要求比 R 温和**（只要任何固定 power saving，而非 N^{1/2}），这是它最大的吸引力。**[推导]**

### 路线 B：两点 Möbius / Chowla 相关路线（函数域蓝图的 ℤ 版）

**理由**：函数域证明把“无条件 Goldbach”精确归约到 (I) 水平>1/2 + (II) 两点 μ 相关（§2.2）。路线 B 直接攻击 (II)——parity barrier 的核心，也是筛法/圆法所有路线共同的墙。若能证明 (II) 的强平均形式，再加上已知/可证的 (I)（Bombieri–Vinogradov 型 + BFI 的 4/7 特殊模可能足够，或更强的 EH 型），则按 G-W-X 框架有希望得到 ℤ 上的无条件 Goldbach（[推测]，因为 ℤ 版框架尚未写出）。

**第一步技术引理（具体）**：
> 证明两点 Chowla 的 power-saving 平均形式，例如存在 δ>0 使
> `Σ_{h≤H} |Σ_{n≤X} μ(n)μ(n+h)|² ≪ H X² (log X)^{−δ}`（合适范围 H→∞, X→∞），
> 或 twisted 版本 `Σ_{h≤H} |Σ_{n≤X} μ(n)μ(n+h)χ(n)|²`；
> 已知最强：Matomäki–Radziwiłł–Tao 的对数平均 Chowla（2015）；本引理要求从 log-平均升级到真正的二点平均/逐点。

**判据**：这是公认的 parity barrier 核心，远超现有技术；但它是**唯一已知的、函数域证明指名的 ℤ 缺口**，因此值得作为长期目标。

### 不推荐（附理由）

- **圆法/例外集**：只能 almost-all；密度-1 不足以证 Goldbach（phase-6 反例）。
- **EH+加权筛**：只到 (1+1.4)，到 (1+1) 无路径（parity barrier）。
- **Green–Tao transference / 熵方法 / larger sieve**：原文明确排除 binary Goldbach 或只是上界工具。
- **Hooley 型条件**：未找到已知蕴含（建议不要列入路线）。
- **Alpöge 证明的新推论**：无显式零无区/L'/L/S(t)，对 Goldbach 无直接帮助。

---

## 6. 引用清单（URL/DOI，访问日期 2026-11-21）

**Ratios Conjecture / 函数域 Goldbach**
1. H. Gou, V. Y. Wang, M. W. Xu, *Landau's problems through ratios of L-functions*, arXiv:2611.18825（2026-11-13）。https://arxiv.org/abs/2611.18825（全文 HTML/PDF 已抓取核对）
2. J. B. Conrey, D. W. Farmer, M. R. Zirnbauer, *Autocorrelation of ratios of L-functions*, Commun. Number Theory Phys. 2 (2008) 593–636；arXiv:0711.0718。
3. W. Sawin, *Square-root cancellation for sums of factorization functions over squarefree progressions in F_q[t]*, Acta Math. 233 (2024) 285–418；arXiv:2102.09730。
4. W. Sawin, M. Shusterman, *On the Chowla and twin primes conjectures over F_q[T]*, Ann. of Math. (2) 196 (2022) 457–506。
5. T. C. Anderson, S. Chow, R. Dietmann, D. Hokken, P. Koymans, R. J. Lemke Oliver, W. Sawin, M. Shusterman, *The strong form of Van der Waerden's conjecture via twisted Chowla*, arXiv:2608.22297v2。
6. D. Wan, D. Zhang, *Betti number bounds for varieties and exponential sums*, Adv. Math. 490 (2026) 110852；arXiv:2501.12623。
7. R. Das, S. Howe, *Cohomological and motivic inclusion–exclusion*, Compos. Math. 160 (2024) 2228–2283；arXiv:2204.04165。
8. S. Lee, *The Hardy–Littlewood asymptotic for prime pairs of fixed even difference from a uniform zeta-ratios conjecture*, arXiv:2610.32672v2（revised 2026-11-03）。https://arxiv.org/abs/2610.32672

**指数和 / 圆法 / 例外集**
9. J. Maynard, M. Pandey, M. Radziwiłł, *Exponential sums over primes*, arXiv:2608.14777（2026-08-14）。https://arxiv.org/abs/2608.14777
10. L. Guth, J. Maynard, *New large value estimates for Dirichlet polynomials*, arXiv:2405.20552（2024-05-31）。https://arxiv.org/abs/2405.20552
11. J. Pintz, I. Althöfer, *The Goldbach exceptional set: an exponent of 7/12 and conditional refinements*, arXiv:2610.15559（2026-10-11）。https://arxiv.org/abs/2610.15559
12. G. Bhowmik, L. Grimmelt, *The exceptional set of the Goldbach problem*, arXiv:2607.27282（2026-07）。https://arxiv.org/abs/2607.27282
13. G. Zhao, *The exceptional set of Goldbach problem and Linnik's constant*, arXiv:2511.05631（2025-11；v2 2026-01-23）。https://arxiv.org/abs/2511.05631

**筛法 / transference / 组合**
14. J. Friedlander, H. Iwaniec, *Opera de Cribro*, AMS Colloq. Publ. 57 (2010)。
15. H. Halberstam, H.-E. Richert, *Sieve Methods*, Academic Press (1974)。
16. B. Green, T. Tao, *Linear equations in primes*, Ann. of Math. 171 (2010) 1755–1850；arXiv:math/0606088（§1.5 原文：excludes binary cases such as twin prime/Goldbach）。
17. B. Green, T. Tao, *The primes contain arbitrarily long arithmetic progressions*, Ann. of Math. 167 (2008) 481–547。
18. P. Gallagher, *A larger sieve*, Acta Arith. 18 (1971) 77–81。
19. K. Matomäki, M. Radziwiłł, T. Tao, *An averaged form of Chowla's conjecture*, Algebra Number Theory 9 (2015) 2167–2196。
20. J. Li, J. Liu, *Theorem (1+1.9) on the Goldbach Conjecture*, arXiv:2606.05224v2（2026-08-08）：EH ⇒ (1+1.4)。https://arxiv.org/abs/2606.05224

**Alpöge/RH 状态**
21. MIT RH Lean 核验页：https://math.mit.edu/~drew/grh/（last updated 2026-11-21 09:30 UTC）。
22. M. Jaswal, *The Riemann hypothesis for Dirichlet L-functions [after Levent Alpöge]*, Zenodo, DOI 10.5281/zenodo.24410057（2026-11-21，54 页）。https://zenodo.org/records/24410057
23. L. Alpöge, *remark.pdf*（2026-11-20）。https://alpo.ge/remark.pdf

**本团队报告（引用其结论）**
24. phase-6/0-phase6-报告.md（final，2026-11-21 20:30）；phase-6/numerics/farN.md；phase-6/audit/hgold-direct.md；phase-6/adversarial/audit.md；phase-6/lit/extremes.md；phase-6/alpoege-scan/quant.md。
25. phase-5/lit/lit-and-tools.md（task-16）；phase-4/afe-attack.md、independent-audit.md（task-11/12）。

---

## 附录 A：关键原文

1. **G-W-X Theorem 1.1（Goldbach，ℤ 上条件性）**：
   > “Assume GRH for Dirichlet L-functions, and RC_D(ω_D). For every ε>0 and every even N, we have Σ_{m+n=N}Λ(m)Λ(n) = N𝔖(N) + O_ε(N^{1−ω_D+ε}).”

2. **G-W-X Theorem 1.5（函数域无条件）**：
   > “Fix an odd prime power q>10^200. Uniformly over monic N of degree d≥3, we have Σ_{F∈M_{d−1}}Λ(F)Λ(N−F) = q^{d−1}𝔖_q(N) + O_q(q^{23d/24}).”

3. **G-W-X §1.5（机制）**：
   > “The Type I/II divisor decomposition of Sawin and Shusterman [SS22a, §6] reduces the problem to a combination of (I) a level of distribution beyond 1/2 for primes in squarefree progressions, and (II) progress on two-point Möbius correlations. For (I) we use work of Sawin [Saw24], and for (II) we use a sieve-theoretic argument inspired by recent work on the Twisted Chowla Conjecture [ACD+26].”

4. **G-W-X §3（parity twist）**：
   > “Note that the factor χ(−1) in (3.1) is not present in our standard Ratios Conjecture. We therefore use the functional equations first to recover the parity-weighted average from two untwisted ratios averages.”

5. **Green–Tao（binary cases 被排除）**：
   > “In this paper we (conditionally) verify this asymptotic under the assumption that no two of the affine-linear forms ψ_1,…,ψ_t are affinely related; this excludes the important ‘binary’ cases such as the twin prime or Goldbach conjectures …”

6. **Jaswal 指南（核心链）**：
   > “ZeroFreeAll says that L(s,ψ)≠0 for every primitive character ψ, the trivial one included, and every s with Re s > 1/2 …”
   > “Part (b) follows from three inputs: Galois representations … local parameters for GL_n at the finite places … and a bound VWin for Tate–Shafarevich groups of Tate twists.”

7. **MIT 页（Arithmetic consequences）**：
   > “As a check that does not depend on Mathlib's definition of the zeta function, the proof was combined with kimihiro64/Robin1984 … Importing both gives two theorems about the divisor sum, with no hypotheses and no mention of zeta … robin_inequality … lagarias_inequality …”

---

## 附录 B：核查方式与局限

- **逐字核对**：G-W-X PDF（46 页全文抽取，Theorem 1.1/1.5/1.6、Hypothesis 1.1、§1.5、§3.1 原文）；Green–Tao arXiv:math/0606088 ar5iv HTML（binary cases 原句）；MIT 页 page_text（本地存档 + 2026-11-21 抓取）；Jaswal 指南 PDF（54 页全文抽取，ZeroFreeAll/三输入原文）；arXiv 摘要：2608.14777、2405.20552、2610.32672、2610.15559、2511.05631、2606.05224、2411.19762。
- **未逐字核对/仅据摘要或二次引用**：CFZ08 的精确主项公式 M_q；Sawin 2024 的精确定理号与条件；Wan–Zhang、Das–Howe 的定理编号；Gallagher larger sieve 的精确常数形式；Matomäki–Radziwiłł–Tao 的精确陈述；Hooley 相关文献（检索未找到可引用蕴含）。
- **局限**：WSL 下 github/Wikipedia 不可达；部分页面需登录；arXiv API 偶发限流。时间盒 60 分钟，本报告是文献调研而非证明审计；所有“路线可行性”判断均标 [推测]。
