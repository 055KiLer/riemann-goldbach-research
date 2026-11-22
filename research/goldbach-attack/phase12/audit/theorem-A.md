# Phase-12 审计：定理 A（GRH + RAT(c>2) ⇒ Goldbach）、c≈1 账本、最弱输入

> 作者：liu-auditor（task-51，2026-11-22）。只写本目录。依据：phase-12/0-plan.md §1.2/§1.3/§1.4；GWX 本地全文 `phase7/lit/gwx_pdf.txt`（行号如下）；phase-11 `shifted-region-lead.md`、`0-phase11-报告.md`。标注 **[证明]/[推导]/[待核]/[推测]**。
> **结论先行（发现 2 个需要 Lead 立即修正的问题）**：
> 1. **【重要，需修正 RAT(c) 定义】** plan §1.2 的 RAT(c) 只写了分子 $\Re a,b\approx1/2+\eta$ 的**直接构型**，但 GWX §3.1–§3.5 同时需要**反射构型** $(a,b)=(1-t-v,1-s-u)$（$\Re a,b\approx1/2-\eta$）：见 gwx_pdf.txt 行 932（Lemma 3.1 明写 both）、行 1014（$E$ 与 $E^\vee$）、行 973（$R^\vee$ 主项）。同时需要**盘上全纯/一致**与对 $u,v$ 的混合导数（行 1063–1068、1347、1450），不能只给 $\Re a$ 区间。**修正后的 RAT(c) 记为 RAT_sym/der(c)**（§1.1）。
> 2. **【重要，§1.3 c≈1 账本错误】** plan §1.3 的 wrap 平凡界 $W\ll X^2/q$ 漏了正交性系数 $\varphi^*(q)\asymp q$（归一化错配）。正确为：单侧 wrap 和 $S\ll X^2/(q\eta^{O(1)})$，**对 $R_q$ 的贡献**是 $\varphi(q)S\asymp X^2/\eta^{O(1)}(\log)^{O(1)}$。正确账本：
>    $$q^{1+\varepsilon}X^{-\eta}+X^{2}\eta^{-O(1)}(\log)^{O(1)}\le q^{1-\omega},\quad \omega=\eta A,\ X=q^A$$
>    ⇒ $A\le 1/(2+\eta)\approx1/2$，即 **c≈1/2，没有从 1/2 改进到 1**。phase-11 的 no-wrap c=1/2 仍是 trivial-wrap 下的精确极限（wrap 平凡界不提供任何增益）。**c≈1 撤回。**
> 3. **[待核，影响 §1.3 基线]** phase-11 移位区域证明 step 1 把 $L(u,\chi)$ 的截断误差写成 $X^{1/2-\sigma}=X^{-\eta}$，其引用的 "Pólya–Vinogradov + Abel" 实际只给 $q^{1/2}X^{-1/2-\eta}$；要得到 $X^{-\eta}q^{o(1)}$ 需 Perron + GRH 的临界线 Lindelöf 型界 $L(1/2+it,\chi)\ll q^{o(1)}$（或等价输入）。该输入若成立，则 $q^{1+\varepsilon}X^{-\eta}$ 成立；否则基线还要下降。详见 §2.2。
> **正面结论**：(a) 若正确假设 RAT_sym/der(c)，§3.2–§3.5 确实**不再需要** §3.6 三点插值；c>2 时定理 A 成立，Goldbach 误差 $N^{1-(c-2)\eta+\varepsilon}$（取固定小 η；需 $c\eta\le1/2+\eta$、$(c-2)\eta\le1/2$ 等常数条件）。(c) c>2 阈值正确，但 truncation 路线的 wrap 缺口比 plan 写的更大：**正确 trivial gap 在 A=2 时是 $q^{3+2\eta}$（非 $q^{2}$）**。(d)(e) 见 §3–§4。

---

## 1. 定理 A 的精确化与审计

### 1.1 修正后的 RAT 假设（RAT_sym/der(c)，**取代** plan §1.2 的 RAT(c)）

> **RAT_sym/der(c)**（$c>0$）：对每个足够小的固定 $\eta>0$（$\eta<\min\{\eta_0,1/(4c),1/6\}$），存在 $B\ge0$，使对每个 $q>1$（$\varphi^*(q)>0$；$v_2(q)=1$ 时 vacuous）、每个 $s,t$ with $\Re s=\Re t=1/2+\eta$、$|\Im s|,|\Im t|\le5\log(2q)$，在**两个构型**上：
- (D) 直接：$a=s+u,\ b=t+v$，$|u|,|v|\le r:=\eta/8$（即 $|\Re a,b-(1/2+\eta)|\le r$）；
- (R) 反射：$a=1-t-v,\ b=1-s-u$（即 $|\Re a,b-(1/2-\eta)|\le r$），
以下误差的**混合导数**满足
$$\bigl|\partial_u\partial_v\bigl[R_q(a,b;s,t)-\mathcal M_q(a,b;s,t)\bigr]\bigr|\le C_{\eta,B,\varepsilon}\,q^{1-c\eta+\varepsilon}(1+T)^B,\quad T=\max|\Im a|,|\Im b|,|\Im s|,|\Im t|,$$
（对 (R) 用相应 $\mathcal M_q(1-t-v,1-s-u;s,t)$）；误差在 $|u|,|v|\le r$ 盘上全纯/一致。等价地，可直接假设 (3.2) 的磁盘一致界（更强）。
> **注**：plan 原文缺 (R)；若只假设 (D)，$R^\vee$ 无法由 $R$ 唯一决定（$R^\vee=h_0R_0+h_1R_1$ 需 parity 分解），§3.1/§3.2 的 $E^\vee$ 没有输入。

### 1.2 定理 A（[推导]，GWX §3.2–§3.5 原样搬运）

**定理 A**：GRH + RAT_sym/der(c)，$c>2$ ⇒ 所有充分大偶数 $N$：
$$\sum_{m+n=N}\Lambda(m)\Lambda(n)=N\mathfrak S(N)+O_\varepsilon\bigl(N^{1-(c-2)\eta+\varepsilon}\bigr).$$
（取固定小 $\eta$ 使 $(c-2)\eta>0$ 且 $c\eta\le1/2+\eta$、$(c-2)\eta\le1/2$；于是误差 $<$ 主项 $N\mathfrak S(N)\ge 2C_2N$。）
**证明映射**：
1. 由 RAT_sym/der(c) 在 (D)(R) 上的 (3.2) 磁盘界，**替代** GWX Lemma 3.1（行 924–943）；§3.6 整节（行 1396–1454）不再需要（其唯一功能是从 Hyp 1.1 造出 (3.2)；见 §1.3 的依赖审计）。
2. GWX §3.1 parity twist (3.3)–(3.4)（行 943–1009）不变；
3. §3.2 用 (3.2) 的 $E,E^\vee$（行 1014）与 Cauchy（行 1063–1068）得集成误差 (3.8) $O(q^{1-\omega+\varepsilon})$；此处取 $\omega=c\eta$；
4. §3.3 的 (3.12)（行 1141–1205）给误差 $O(N^{1-\omega+2\eta+\varepsilon})$（行 1181、1195）；(3.12) 对 $\omega$ 的唯一要求是 $\omega\le1/2+\eta$（行 1183 "$\sigma\le1-\omega+2\eta$"）和 $\omega>2\eta$（想得到负幂）；
5. §3.4–§3.5 的 sharp weight（行 1282–1395）：(3.24) 误差 $O(N^{1-\omega+2\eta+\varepsilon})$（行 1363），取 $\lambda=\mu=0$；
6. 素数幂 $O(N^{1/2}\log^2)$ 吸收（需 $1-\omega+2\eta\ge1/2$，即 $(c-2)\eta\le1/2$）；主项 $NS(N)\ge2C_2N$；取固定小 $\eta$ 得定理。∎

**[待核] 常数条件**：$T\le5\log(2q)+O(1)$（不是 plan 的 100log；见 §1.3）；$r=\eta/8$（比 GWX 的 $r<\min(\eta/4,(1/4-\eta)/4)$ 更紧，需 $\eta<1/6$）；$c\eta\le1/2+\eta$（即 $\eta(c-1)\le1/2$）；$(c-2)\eta\le1/2$；$c\eta<1$（误差正幂无所谓）。均可由取充分小固定 η 满足。

### 1.3 (a) 逐行核对：除 §3.6 外，(3.2)/Hyp 1.1 还有哪些使用处？——**没有别的；但需要两个构型**

grep 结果（行 880–1500 中 "Hypothesis 1.1/ (3.2)"）：
- 行 891–901：概述，说明用 FE 恢复 parity-weighted average；非使用。
- 行 924–943：Lemma 3.1 陈述；行 928=(3.2)；行 932 **both $(a,b)=(s+u,t+v)$ and $(a,b)=(1-t-v,1-s-u)$**；行 936–939 解释"These are two choices of numerator arguments in the untwisted Ratios Conjecture"。**⇒ 直接与反射两个构型都必须假设。**
- 行 973：用 (3.2) 写 R 与 $R^\vee$ 的主项（$R^\vee$ 的系数 $M_0h_0+M_1h_1$）——再次需要 (R) 构型。
- 行 1014：$E,E^\vee$=对 R 和 $R^\vee$ 应用 (3.2) 的误差；代入 (3.3) 得 $(2E^\vee-(h_0+h_1)E)/(h_0-h_1)$。
- 行 1063–1068：Cauchy 公式 in $u,v$；Ratios 仅在 $|\Im s|,|\Im t|\le5\log(2q)$ 使用（行 1068）；外部用 GRH 的 signed 界。**⇒ T 只需 $\le5\log(2q)+r$，不是 100log。**
- 行 1144、1181、1183、1195：(3.12) 误差 $N^{1-\omega+2\eta+\varepsilon}$；$\sigma\le1-\omega+2\eta$ 唯一涉及 ω 的约束（$\omega\le1/2+\eta$）。
- 行 1231、1363：(3.14)/(3.24) 同误差。
- 行 1347：$|\Im s|,|\Im t|\le5\log(2q)$ 上用 Cauchy 处理 weighted error in (3.3)（直接用到 (3.2) 在盘上的全纯/导数界）。
- 行 1396–1454：§3.6 证明 Lemma 3.1；其中 Hyp 1.1 只在行 1441（三线插值 boundary $\Re\xi=0$）被用。**⇒ 若直接假设 (3.2)，整节 §3.6 可删；r=η/8、loss $8(\eta+r)(2+\omega_D)$ 全部消失。**
- 其它行（§3.1、§3.3 的 principal character/Euler factor、§3.4 的近似、§3.5 的 sharp weight）只用 GRH、代数恒等式、Prop 2.1/(2.12)，**不直接使用 Hypothesis 1.1 的"临界线分母"构型**。
- **结论 [证明]**：(a) 成立——除 Lemma 3.1（由 §3.6 从 Hyp 1.1 造）外，(3.2) 只在 §3.2/§3.5 的误差处理与主项替换处被使用；**前提是把 (3.2) 在 (D) 与 (R) 两个构型、且磁盘上全纯地假设**（plan RAT(c) 缺 (R)，需修）。**没有隐藏的"临界线分子"依赖。**

---

## 2. (b) 审计 plan §1.3 的 c≈1 账本

### 2.1 独立推导（标注 [推导]）

沿用 phase-11 Lead 移位区域构造（`shifted-region-lead.md` §1）：
- 四个因子 $L(a,\chi),L(b,\bar\chi),1/L(s,\chi),1/L(t,\bar\chi)$ 截断到长 $X$；$\Re a=\Re b=\Re s=\Re t=\sigma=1/2+\eta$。
- per-factor 误差：$L(u,\chi)$：$\Delta_L\ll X^{1/2-\sigma}(qT)^{O(1)}=X^{-\eta}(qT)^{O(1)}$（**正确证明需 Perron+GRH 临界线界，见 §2.3**）；$1/L(u,\chi)$：Lemma 1.1 $\Delta\ll X^{-\eta+\varepsilon}(qT)^\varepsilon$。
- 四因子展开：单因子误差 × 其它三因子点值 $\ll X^{-\eta}q^{o(1)}$；对 $\chi$ 求和 $\asymp q$ ⇒ 总截断误差
  $$T_{\rm trunc}\ll q^{1+\varepsilon}X^{-\eta}(1+T)^C.\tag{2.1}$$
- 无 wrap（$X^2<q$ ⇒ $A,B<q$）：正交性给**精确**
  $$E^{(X)}=\varphi^*(q)\sum_{A\le X^2}c_Ad_A+\Bigl[\sum_Ac_Ad_A-\bigl(\sum_Ac_A\bigr)\bigl(\sum_Bd_B\bigr)\Bigr],$$
  主项 $\varphi^*Z_q$；Euler 积恒等式 $S:=\sum c_Ad_A=Z_q$（up to $p|q$/$X$ 修正），误差 ≤ 主项。取 $X=q^{\omega/\eta}$，$X^2<q$ ⇒ $\omega/\eta<1/2$：**c=1/2**（phase-11 结论）。**[推导]**

### 2.2 允许 wrap 的**正确**账本（发现 plan 错误）

对素数 $q$（一般 q 用 divisor 公式，主项系数仍 $\varphi^*(q)\asymp q$），$X^2>q$：
- 正交性：$\sum^*_\chi\chi(A)\bar\chi(B)=\varphi^*(q)\mathbf1_{A\equiv B\bmod q}+(1_{A\equiv B}-1)$（$A,B$ 与 q 互素；见 GWX §3.1 及我们 phase-11b 报告）。
- 于是 $E^{(X)}=\varphi^*(q)\sum_{A\equiv B}c_Ad_B+[\sum_{A\equiv B}c_Ad_B-\sum_{A,B}c_Ad_B]$；**wrap 对 $R_q$ 的贡献**是
  $$W_R=\varphi^*(q)\sum_{A\ne B,\,A\equiv B(q)}c_Ad_B.$$
- 系数（$\Re a=\Re s=\sigma$）：$c_A=\sum_{rm=A}r^{-a}\mu(m)m^{-s}$，$|c_A|\le A^{-1/2-\eta}d(A)$；$|d_B|\le B^{-1/2-\eta}d(B)$。
- 单侧和：
  $$S_{\rm wrap}:=\sum_{A\ne B,A\equiv B(q)}|c_A||d_B|
  \le\sum_{1\le|k|\le X^2/q}\sum_{A\le X^2} A^{-1/2-\eta}|A-kq|^{-1/2-\eta}d(A)d(A-kq).$$
  对固定 $k$，内和 $\asymp\eta^{-O(1)}(\log X)^{O(1)}$（$\sum_A A^{-1-2\eta}\asymp1/(2\eta)$；边界项给 log 因子）；乘 $k$ 的个数 $X^2/q$：
  $$S_{\rm wrap}\ll \eta^{-O(1)}(\log X)^{O(1)}\,\frac{X^2}{q}. \tag{2.2}$$
  即 plan 的 $W\ll X^2/q\cdot\eta^{-O(1)}(\log)$ 是**未乘 $\varphi^*$ 的单侧和** $S_{\rm wrap}$。
- **但对 $R_q$ 的贡献**是 $\varphi^*(q)S_{\rm wrap}\asymp q\cdot X^2/q=X^2$（$\eta^{-O(1)}$ 常数），不是 $X^2/q$。
- 正确账本：$X=q^A$，$\omega=\eta A$，两误差：
  $$T_{\rm trunc}=q^{1-\eta A+\varepsilon},\qquad W_R\ll X^2\eta^{-O(1)}(\log)^{O(1)}=q^{2A}\eta^{-O(1)}(\log)^{O(1)}.$$
  要求两者 $\le q^{1-\omega}=q^{1-\eta A}$：
  $$\text{trunc: 自动（差 }q^\varepsilon\text{）};\qquad
  \text{wrap: }2A\le1-\eta A\iff A\le\frac1{2+\eta}\approx\frac12. \tag{2.3}$$
  **⇒ 允许 wrap 且用平凡界，c 仍是 $\approx1/2$，没有任何改进。**
  若做归一化（除以 $\varphi^*$）：$T_{\rm trunc}/\varphi^*\ll q^{\varepsilon}X^{-\eta}$，$W_R/\varphi^*\ll X^2/(q\eta^{O(1)})=q^{2A-1}\eta^{-O(1)}$；目标 $q^{-\omega}=q^{-\eta A}$；同样 $2A-1\le-\eta A\Rightarrow A\le1/(2-\eta)\approx1/2$。**两种归一化都给 c≤1/2。**
- **[推测] plan 的 c≈1 来源**：把 $S_{\rm wrap}=X^2/q$ 直接与**未归一化**的 $q^{1-\omega}$ 比较（或用 $W_R$ 与 $q^{-\omega}$ 比较），归一化/正交性系数 $\varphi^*\asymp q$ 被漏掉，导致 $2A-1\le1-\eta A\Rightarrow A\le2/(2+\eta)\approx1$。**这是 §1.3 的实质性算术错误；请 Lead 立即修正。**

### 2.3 [待核] 截断误差 $q^{1+\varepsilon}X^{-\eta}$ 的合法性

- phase-11 证明 step 1 写 $L(u,\chi)=\sum_{n\le X}\chi(n)n^{-u}+O(X^{1/2-\sigma}(\log qX)^C)=O(X^{-\eta}\cdots)$，引用 "Pólya–Vinogradov/GRH 部分和 + Abel"。**但 PV 只给 $\sum_{n\le N}\chi(n)\ll q^{1/2}\log q$，Abel 给出 tail $\ll q^{1/2}\log q\,X^{-1/2-\eta}$，不是 $X^{-\eta}$。** 要得到 $X^{-\eta}q^{o(1)}$，正确路线是 Perron 公式把 $L(u,\chi)$ 的截断误差移到临界线 $\Re=1/2$，并用 GRH 下的临界线界 $L(1/2+it,\chi)\ll q^{o(1)}(1+|t|)^{O(1)}$（Lindelöf 型；是否严格由 GRH 推出需逐条核实，[待核]）。若该输入成立，则 (2.1) 成立；否则基线误差更大，c=1/2 也要下调。**建议 proof-digest/文献组核对该 GRH 推论。**
- 分母 Lemma 1.1 的 $X^{-\eta}$ 来自 GRH 的 Möbius 部分和 $\sum_{n\le x}\mu(n)\chi(n)\ll x^{1/2+\varepsilon}q^{O(1)}$ + Abel；这条更标准（[待核] 常数/uniformity）。
- 结论：plan §1.3 的 $q^{1+\varepsilon}X^{-\eta}$ 在"GFH Lindelöf 型输入 + Lemma 1.1"下可成立；**不是由 PV+Abel 直接给出**。需要修正证明文本。

---

## 3. (c) 审计 c>2 阈值与 wrap 缺口

### 3.1 c>2 从何而来（[推导]）

直接 RAT_sym/der(c)（无截断）⇒ (3.12) 误差 $N^{1-\omega+2\eta+\varepsilon}$ with $\omega=c\eta$ ⇒ $N^{1-(c-2)\eta+\varepsilon}$。要**幂次节省**且主项 $N\mathfrak S(N)$ 胜出，只需 $(c-2)\eta>0$；取固定小 η，**c>2**。这部分的 plan 逻辑正确。
常数约束：$\omega=c\eta\le1/2+\eta$（行 1183）⇒ $\eta(c-1)\le1/2$；素数幂吸收需 $(c-2)\eta\le1/2$；取 $\eta<\min(1/(4c),1/6)$ 即可。**[推导]**

### 3.2 truncation 路线的 wrap 缺口（修正 plan 的 q²）

设截断法要证 RAT(c)：取 $X=q^A$，希望 $\omega=\eta A=c\eta$ ⇒ $A=c$。A>2 ⇒ X>q²。
- 截断误差（2.1）：$q^{1-\eta A+\varepsilon}$；目标 $q^{1-\eta A}$ ✓（差 $q^\varepsilon$）。
- wrap 平凡界（正确）：$W_R\ll q^{2A}\eta^{-O(1)}(\log)^{O(1)}$；目标 $q^{1-\eta A}$。
  **要求的 wrap saving（相对平凡）**：
  $$\boxed{\ \text{need } W_R\ll q^{1-\eta A+\varepsilon}\ \Longleftrightarrow\ \text{trivial }W_R\sim q^{2A}\ \text{需额外 saving }q^{\,A(2+\eta)-1}.\ }$$
  在 $A=2$（即 $X=q^2$、目标 c=2）：额外 saving $q^{3+2\eta}$（**不是 plan 的 q²**）。
- 若按 plan 的错误 $W\sim q^{2A-1}$（单侧和，未乘 $\varphi^*$）外推：$q^{2A-1}\le q^{1-\eta A}$ ⇒ $A(2+\eta)\le2$ ⇒ $A\le2/(2+\eta)\approx1$；在 A=2：gap $q^{2+2\eta}$。**plan 的 q² 来自这个错误归一化。**
- **结论 [推导]**：c>2 阈值本身正确；但 "A=2 时差 q²" 应改为 **q^{3+2η}**（正确的、含 $\varphi^*$ 的 wrap 平凡界）。truncation 路线离 c>2 的差距比 plan 描述的**大 q^{1+?}**。

### 3.3 与已知结果的差距量化（[推导]/[推测]）

需要的估计（H_wrap，精确形式）：
$$\sum_{1\le|k|\le X^2/q}\ \sum_{\substack{n,r,m,l\le X\\ nr-ml=kq}} |c(n,r)\overline{d(m,l)}|\ \ll\ q^{1-\eta A+\varepsilon},\qquad X=q^A,\ A>2. \tag{3.1}$$
（$c(n,r)$ 为截断 Dirichlet 系数，含 μ。）
- **平凡/Cauchy–Schwarz**：$\gg q$（phase-11 已述），trivial 上界 $q^{2A}$；需要的 saving $A(2+\eta)-1$（A=2 时 $3+2\eta$；A=1 时 $1+\eta$ 但 c=1 不够）。
- **Bombieri–Vinogradov**：只给素数在 AP（模 $q\le x^{1/2-\varepsilon}$）的**平均**分布；这里模 q 可到 $X^{1/A}<X^{1/2}$，但对象是四变量双线性 $nr-ml=kq$（含 μ），不是线性 AP 素数，不能直接套用。
- **Chowla / MRT / Tao–Teräväinen**：给出 $\mu$ 或 $\tau$ 的**对数平均/几乎 all shift** 相关，或 additive divisor 对几乎所有 h 的渐近；对固定集合 $\{kq\}$、且要求**一致 power saving** 的 (3.1) 没有结论。这里的 saving 是 q 的幂（至少 $q^3$ 在 A=2），远强于对数 saving。
- **Additive divisor**：固定 h 的 $\sum_n\tau(n)\tau(n+h)$ 有渐近；h 的一致性只到有限范围（经典 h up to $X^{?}$ 平均），而这里 h=kq 可达 $X^2/q$，且变量是四重的 nr、ml；μ 权重进一步使其成为 Chowla/parity-barrier 级。
- **结论 [推测]**：H_wrap (3.1) 与 phase-11 的 parity barrier 同级；c>2 的 truncation 证明不可由 GRH 级工具完成。直接 RAT_sym/der(c>2) 是**更强的假设**，若被独立证明则可绕过；目前两条路都未解决。

---

## 4. (d) 最弱充分输入（plan §1.4(5)）

### 4.1 比 RAT_sym/der(c>2) 更弱但足够的输入

1. **[推导] 导数层足够；点值 $u=v=0$ 不够。** GWX §3.2/§3.5 对分子移位 $u,v$ 用 Cauchy（行 1063–1068、1347、1450），实际需要的是 $\partial_u\partial_v$ 误差在 $u=v=0$（或盘上）的界。因此 **RAT_sym/der(c)**（§1.1）已经是一个弱化：只假设混合导数误差，不假设 $E$ 的完整磁盘点值界（但需在每个 $|u|,|v|\le r$ 上给导数界/或 (3.2) 磁盘界；最干净是磁盘 (3.2)）。若只假设 $u=v=0$ 的误差点值，**不能**控制 $\partial_u\partial_v$，不足以补 §3.2。
2. **[推测/待核] 可进一步弱化到 parity-combined 导数层**：只假设组合 $\partial_u\partial_v[(2R^\vee-(h_0+h_1)R)/(h_0-h_1)]$ 的主项 (3.9) + 误差 $q^{1-c\eta+\varepsilon}$，而不分别要求 R、R∨ 的 (3.2)。这比 RAT_sym/der 弱（只需一个线性组合），且 §3.2 的误差正好是这个组合；但需重新验证 (3.9) 主项的求导/全纯细节。**这是目前能陈述的最弱充分形式，标记 [待核]。**
3. **[推导] 只需 q|N 吗？** 否——每个 $\varphi^*(q)>0$ 的 q 都会作为某偶数 N 的 primitive conductor 出现（q odd ⇒ N=2q；4|q ⇒ N=q）；且 v2(q)=1 的 q 有 $\varphi^*(q)=0$（vacuous，可删）。所以"对 q|N"与"对所有 q"无实质差别；只能删 vacuous 类。
4. **[推导] |Im|≤C 常数吗？** 否。GWX §3.2/§3.5 的 Ratios 输入在 $|\Im s|,|\Im t|\le5\log(2q)$ 上使用（行 1068、1347），外部用 GRH；分子移位再加 $r$。所以需要 $T\le5\log(2q)+O(1)$（可把 Hyp 1.1 的 100log 降到 5log+r），但**不能**降到固定常数 C（锐权重/rational weights 的 Mellin 积分需要高度到 log q）。
5. **[待核] 积分形式/光滑权重**：§3.2/§3.5 最终只把这些误差积分 against rational weights $f_j$ 与 sharp $w$；理论上可以假设"对这些特定权重的积分误差≤..."，但这会比点值/导数层更人为，也不能让证明更容易；不推荐作为"最弱输入"的候选。
6. **[推导] 主项**：必须保留**精确两项** $\mathcal M_q=\varphi^*Z_q+H_qZ_q(1-b,1-a)$（含 $H_q$ 及 parity 计数），不能只保留 $\varphi^*Z_q$；否则 (3.9)/(3.10) 的 $\Delta(q)$ 和 $M_0X_0X_0-M_1X_1X_1$ 项错。

**最弱可陈述充分输入（推荐写入 phase-12）**：RAT_sym/der(c)（§1.1），或进一步 RAT_par/der(c)（parity-combined 导数层，[待核]）。两者都比 GWX Hyp 1.1 弱：无需临界线构型、无需全移位/圆盘上的 (3.2)、T 只需 5log、只需导数层。

### 4.2 是否更可证？

- 直接 RAT_sym/der(c) 仍是 Ratios 型深猜想（临界线 $\eta\to0$ 的极限是 phase-11 的 H_wrap/parity barrier）；但它把"临界线+插值"结构完全剥离，可能让 kernel-theorist 用 Kloosterman/FE 折叠直接攻 **(D)(R) 两个固定距离构型**，而不被 §3.6 的 8(η+r)(2+ω_D) 损失卡住。**这是 phase-12 框架的正面价值**：把目标从"H_Ratios on critical line + interpolation"变为"RAT_sym/der(c>2) on two shifted configurations"，后者在 k-空间可能更容易折叠（plan §1.4(1)）。
- 但 c>2 本身仍要求 $\omega/\eta>2$ 的均匀 saving，与 phase-11 的"移位区域可证 only ω<η/2"矛盾 ⇒ 至少要比 phase-11 强 4 倍；这不是靠"绕过插值"能获得的，需要**新的 wrap/parity 输入**。**[推测]**

---

## 5. (e) GWX Appendix A 为什么排除 Goldbach

### 5.1 原文（`gwx_pdf.txt` 行 3199–3204）

> "**Appendix A. Ratios with qualitative errors.** For prime differences and quadratic values, the power-saving ratios errors in the main theorems can be weakened if only qualitative asymptotics are required. The condition ω>2η compensates for the fixed Mellin-line factor X^{2η}. Taking η of order 1/log X keeps that factor bounded. Uniform o(Q) primitive errors then give o(X) after smoothing and Mellin inversion. **The character argument continues to use a positive power saving.**"

### 5.2 解释（[推导]）

- Appendix A 的定性假设 Hypotheses 2.4/2.5 只对 **ζ（prime pairs）** 与 **Hecke（quadratic values）** 陈述；**没有**对 Dirichlet primitive family 的定性版本。
- 为什么 Goldbach 不能直接用定性 o(q)：GWX 的 Ratios 输入是按 **每个 primitive conductor q|N** 使用、再对 q 求和、除以 φ(N)（(3.12) 行 1181–1183）。若每个 q 的误差只知 $o(q)$（对每个 q 的速率依赖 q、无统一控制），则
  $$\sum_{q|N}o(q)\le N^{1-o(1)}\tau(N)$$
  不足以得 $o(N)$（τ(N) 无界）；且除以 φ(N) 后仍需一致控制。**需要的是对所有 q|N 一致的正幂 saving $q^{1-\omega}$（固定 ω>0）**，才能 $\sum_{q|N}q^{1-\omega}\le N^{1-\omega+\varepsilon}$，再乘 $N^{2\eta}$（(3.12) 的 Mellin 因子）后要求 $\omega>2\eta$。这正是 Appendix A 说 "character argument continues to use a positive power saving" 的含义：**Goldbach 的字符和/divisor sum 步骤需要正 power saving，而不是 zeta/Hecke 那种"族平均 o(Q)"。**
- 若改用 $\eta\sim1/\log N$（Appendix A 的移动线想法）并允许**定量** rate $\omega(q)\log q\to\infty$（如 $1/\log\log q$），则 $\omega>2\eta\sim2/\log N$ 可满足（因 $\omega\log N\to\infty$），Goldbach 误差 $o(N)$ 也可能成立。**但这不是 Appendix A 的定性假设**：它需要 Dirichlet 族的**带速率定性 Ratios**（phase-11 Part A 的 H_Ratios^{min,qual} + H_UNIF），GWX 没有形式化。**[推导/推测]**
- 与 c>2 路线的关系：
  * 直接 RAT_sym/der(c>2) 是**固定 η、固定正 saving** 的充分条件；c>2 阈值来自 $\omega=c\eta>2\eta$。
  * 定性-rate 路线（$\omega(q)\log q\to\infty$，$\eta\sim1/\log N$）在逻辑上**不要求 c>2**：它允许 $\omega/\eta$ 缓慢增；但需要额外的 rate/uniformity（H_UNIF）。**因此 c>2 是充分而非必要；phase-12 若把目标定为 c>2，是选择了更强的、但形式更干净的定量版本。**
  * 若目标只是"证明 Goldbach"（定性），最弱路线可能是"定量定性 Ratios + H_UNIF"（saving $\gg1/\log N$），但该输入的证明难度仍与 H_wrap/parity barrier 同级；c>2 与它是两条不同的定量充分条件。

---

## 6. 结论与需要 Lead 立即修正的事项

1. **RAT(c) 定义必须改成 RAT_sym/der(c)**（§1.1）：(i) 加反射构型 $(a,b)=(1-t-v,1-s-u)$；(ii) 加 $|u|,|v|\le r$ 磁盘/全纯/一致性与混合导数层；(iii) T 从 100log 降到 $5\log(2q)+O(1)$（可保留 100log 无害）；(iv) 明确 $\mathcal M_q$ 在反射构型为 $\mathcal M_q(1-t-v,1-s-u;s,t)$（或直接用 §3.1 的 $R^\vee$ 主项）。
2. **§1.3 的 c≈1 账本撤回，改为 c≈1/2**：wrap 对 $R_q$ 的贡献是 $\varphi^*S_{\rm wrap}\asymp X^2$，不是 $X^2/q$；正确 ledger (2.3) 给 $A\le1/(2+\eta)$。**plan 中 "A≤1/(1+η/2) ⇒ c≈1" 是错误的；请修正为 "trivial wrap 不改进 c=1/2"**。相应地 phase-12 的任务表述"最后 4 倍指数缺口"仍成立（phase-11 c=1/2 vs c>2 是 4 倍），但**不能用"trivial wrap 到 c≈1"作为中间步骤**。
3. **c>2 的 wrap 缺口修正**：A=2 时正确 gap 是 $q^{3+2\eta}$（不是 $q^2$）；一般 A>2 需 wrap saving $q^{A(2+\eta)-1}$。已知 Bombieri–Vinogradov/Chowla/MRT/TT/additive divisor 均不够（见 §3.3）。
4. **[待核] phase-11 移位区域 step 1 的 $L(u,\chi)$ 截断误差 $X^{-\eta}$**：PV+Abel 不够，需要 Perron+GRH 临界线 Lindelöf 型输入；请 proof-digest/文献组核实，否则 §1.3 基线需下调。
5. **正面**：定理 A 在修正 RAT_sym/der(c) 后成立（c>2 ⇒ Goldbach，误差 $N^{1-(c-2)\eta+\varepsilon}$）；§3.6 插值可完全绕过（行 880–1500 无其他 Hyp 1.1 依赖）；最弱充分输入为 RAT_sym/der（或进一步 parity-combined 导数层，[待核]）；Appendix A 排除 Goldbach 的原因是 Goldbach 需要 uniform positive power saving per conductor，定性 o(Q) 不能求和过 q|N（§5）。
6. **建议 phase-12 修正 plan 后继续**：框架（绕过插值、把目标定为 RAT_sym/der(c>2)）是**有意义的**，但 (i) c≈1 中间目标不存在（顺序是 1/2 → 2，需直接量子跃迁）；(ii) c>2 的实质就是 H_wrap/parity barrier，phase-12 的 wrap 主攻（Kloosterman/FE 折叠）值得尝试但困难；(iii) 若只求定性，定性-rate Ratios 是更弱的逻辑目标但可能需要 H_UNIF。

---

## 7. 关键行号索引（gwx_pdf.txt）

- 行 891–901：Goldbach 推导概述（Hyp 1.1 仅用于插值）。
- 行 924–943：Lemma 3.1、(3.2)、**both 构型**（行 932）、分母/分子 disk 说明。
- 行 973–1009：R/R∨ 主项、parity twist (3.3)；行 1014：$E,E^\vee$。
- 行 1063–1068：Cauchy in u,v、Ratios 仅 $|\Im|\le5\log(2q)$。
- 行 1141–1205：(3.12)，误差行 1144/1181/1195，$\sigma\le1-\omega+2\eta$ 行 1183。
- 行 1231、1363：(3.14)/(3.24) 同误差；行 1347：5log 上的 Cauchy。
- 行 1396–1454：§3.6 插值（唯一 Hyp 1.1 使用行 1441；ω 损失行 1449）；行 1452：最终 η 选择。
- 行 3199–3204：Appendix A 定性版本原文。

## 8. 复现/说明

- 本审计未读 kernel-theorist 新笔记；未假定任何 ramified 主项（phase-11b 已确认 (3.2) 正确、ramified anomaly 为 A_q mask bug）。
- 计算均为解析推导；未运行新数值（wrap 数值由 heat-kernel-critic task-54 负责；本报告的 $X^2$ vs $X^2/q$ 是确定性的归一化算术）。
- 行号来自 `phase7/lit/gwx_pdf.txt`；外部：GWX arXiv:2611.18825v1；phase-11 `shifted-region-lead.md`；phase-12/0-plan.md。
