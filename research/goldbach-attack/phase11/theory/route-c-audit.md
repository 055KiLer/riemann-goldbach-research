# Phase-11 Part B：Route C 的独立保守审计（truncated Möbius + smooth AFE + exact orthogonality）

> 作者：liu-auditor（task-37，2026-11-21/22）。**本文件为独立审计**：未阅读 kernel-theorist 的 Route C 笔记（`phase11/theory/lead-route-c.md`、`c1_*.py` 等均未打开）；仅依据 task-37 的公开描述与标准解析数论自行重建。
> 标注：**[推导]** 本报告推理；**[事实]** 标准已知结果/可核对；**[推测]** 判断。timebox 100 min 内完成的保守审计，不声称是完全的"no-go theorem"。
> 结论一句话：**Route C 的"截断 Möbius 引理"在 GRH 下是成立的（且 q^ε 一致），但它迫使截断长度 $X\gtrsim q^{2\omega/\eta}$；随后在"精确正交性"步骤出现的 wrap-around 双线性相关（模 q 的 AP 双线性型），其仅有的 GRH 级别界（大筛/第二矩）给出 $\gtrsim L=q^{1/2+2\omega/\eta}$ 的规模，远大于目标误差 $q^{1-\omega}$——两者矛盾不可调和。**这是 Route C 的**精确致命引理**。它需要的是一个 Type II/Chowla 型双线性相关估计，**不被 GRH 蕴含**，本质上等价于 Ratios 猜想/奇偶障碍（parity barrier）。所以 Route C 用"仅 GRH 级别输入"没有机会闭合；它至多把 H_Ratios 归约到另一个同等困难的相关性猜想上，属于循环。根数/Gauss 和项可以精确求出、不是致命点；主项匹配 M_q 未在 Route C 中建立（次要问题）。

---

## 0. 结论速览（给 Lead 的 boxed 答案）

> **Route C verdict（保守审计）**
> 1. **截断 Möbius 引理本身成立**：在 GRH 下，对每个固定 $\eta>0$、$\varepsilon>0$、所有 primitive χ mod q、$|t|\le T$，
>    $$1/L(1/2+\eta+it,\chi)=\sum_{n\le X}\mu(n)\chi(n)n^{-1/2-\eta-it}+O_\varepsilon\bigl(X^{-\eta/2}(q(1+|t|))^\varepsilon\bigr),$$
>    要得到 $q^{-\omega}$ 的逐点误差需 $X\ge q^{2\omega/\eta+\varepsilon}$。**引理不是致命点，但它把截断长度推到远超 $q$ 的量级。**
> 2. **致命点 = "精确正交性"后的 wrap-around 双线性型**：展开 AFE × 截断 Möbius 后，核心求和是
>    $$\Sigma_*:=\sum_{\chi\bmod q}^{*}U(\chi)V(\bar\chi),\qquad U(\chi)=\sum_{A\le L}u_A\chi(A),\ V(\chi)=\sum_{B\le L}v_B\bar\chi(B),$$
>    其中 $L\asymp R X$，$R\asymp(qT)^{1/2}$（AFE 长度），$X\ge q^{2\omega/\eta}$（Möbius 截断长度）。精确正交性（q prime）给出 $\Sigma_*=\varphi(q)\sum_{A\equiv B(q)}u_A\bar v_B-\sum_{A=B}u_A\bar v_B$；**GRH 级别能拿到的唯一通用界是大筛/Cauchy**：
>    $$|\Sigma_*|\le(q+L)\|u\|_2\|v\|_2\asymp(q+L)\cdot\frac{\log q}{\eta}\ \asymp\ q^{1/2+2\omega/\eta}\,\frac{\log q}{\eta}.$$
>    而 Ratios 的误差目标是 $q^{1-\omega}$（主项 $\varphi^*Z_q$ 是 $q^{1+o(1)}$ 量级）。两者要求
>    $$q^{1/2+2\omega/\eta+o(1)}\ll q^{1-\omega}\iff \frac{2\omega}{\eta}\le\frac12-\omega+o(1),$$
>    但三线插值要求 $\eta\ll\omega$（GWX 的 $\omega=\omega_D-8(\eta+r)(2+\omega_D)$ 需 $\omega_D>20\eta$），故 $2\omega/\eta\gg1\gg1/2-\omega$：**矛盾。没有任何 $X,\eta$ 的选择能同时满足截断误差和 wrap-around 控制。**
>    $\Rightarrow$ 必须用**远强大筛**的估计：对 $A\equiv B\pmod q$、$A\ne B$ 的双线性 μ/Λ 系数相关（Type II/Chowla 型）；这是已知的 parity barrier 类深问题，**不被 GRH 蕴含**，且它正是 H_Ratios 所编码的信息。**Route C 循环，且用 GRH-only 输入无机会。**
> 3. **根数项/Gauss 和**：可精确算出（$\tau(\chi)$ 展开），不构成独立致命点；cross terms 带 $q^{-1/2}$ 因子，甚至有利。
> 4. **主项是否匹配 $\mathcal M_q$**：未在 Route C 中建立，且有 factor/reflection 项不匹配的风险；但由于 2 已经致命，主项问题只是次要的。
> 5. **最终**：Route C 不能作为 GWX H_Ratios 的"GRH 级证明"；它若要闭合，必须假设一个至少与 H_Ratios 等价的 Type II 相关输入 ⇒ **循环，无独立价值**。GWX 路线仍以"H_Ratios 为假设"的状态成立；Route C 的失败不削弱 GWX 的条件性归约。

---

## 1. Route C 的骨架（我独立重建的形态）

目标：在 GRH 下证明 GWX Lemma 3.1 的 Ratios 平均（关键情形：分子在临界线、分母 $\Re=1/2+\eta$），即对 primitive χ mod q（q>1）：
$$R_q(a,b;s,t):=\sum_{\chi\bmod q}^{*}\frac{L(a,\chi)L(b,\bar\chi)}{L(s,\chi)L(t,\bar\chi)},\qquad \Re a=\Re b=\frac12,\ \Re s=\Re t=\frac12+\eta.$$

Route C 的做法：
1. **分子**：对 $L(a,\chi)$、$L(b,\bar\chi)$ 使用光滑近似函数方程（AFE），长度 $R\asymp(qT)^{1/2}$（$T=\max(|\Im a|,|\Im b|,|\Im s|,|\Im t|)\lesssim\log q$），
   $$L(a,\chi)=\sum_{r\le R}\frac{\chi(r)}{r^{a}}V\Bigl(\frac rR\Bigr)+\varepsilon(\chi)\Bigl(\frac q\pi\Bigr)^{1/2-a}\sum_{r\le R}\frac{\bar\chi(r)}{r^{1-a}}\bar V\Bigl(\frac rR\Bigr)+O(q^{-A}),$$
   第二项带根数 $\varepsilon(\chi)$；$L(b,\bar\chi)$ 类似带 $\varepsilon(\bar\chi)$。AFE 误差对任意固定 A 可做到 $O((qT)^{-A})$（光滑权下无条件）。
2. **分母**：用截断 Möbius
   $$1/L(s,\chi)=\sum_{m\le X}\mu(m)\chi(m)m^{-s}+E_s(\chi),\qquad 1/L(t,\bar\chi)=\sum_{n\le X}\mu(n)\bar\chi(n)n^{-t}+E_t(\chi),$$
   在 GRH 下 $E_s,E_t$ 可控（§2）。
3. **代入**：$R_q=\sum^*_\chi [L(a,\chi)P_s(\chi)]\,[L(b,\bar\chi)P_t(\bar\chi)]+\text{误差项}$，其中 $P_s(\chi)=\sum_{m\le X}\mu(m)\chi(m)m^{-s}$。
4. **展开成 Dirichlet 多项式**：$U(\chi):=L(a,\chi)P_s(\chi)\approx\sum_{A\le L}u_A\chi(A)$，$V(\chi):=L(b,\bar\chi)P_t(\bar\chi)\approx\sum_{B\le L}v_B\bar\chi(B)$，其中 $L=RX$，系数
   $$u_A=\sum_{rm=A}a_r\mu(m)m^{-s},\qquad v_B=\sum_{sn=B}b_s\mu(n)n^{-t}$$
   （$a_r$ 是 AFE 直接/反射项的系数，含 $r^{-a},r^{a-1}$ 与权函数）。
5. **精确正交性**：对 primitive χ mod q（q prime 为最干净情形）
   $$\Sigma_*:=\sum_{\chi\bmod q}^{*}U(\chi)V(\bar\chi)=\varphi(q)\sum_{A\equiv B\ (q)}u_A\bar v_B-\sum_{A=B}u_A\bar v_B.$$
   目标：把 $\Sigma_*$ 的主项算成 $\mathcal M_q$（或至少其可辨识部分），误差 $O(q^{1-\omega+\varepsilon})$。
6. 比较主项 $\mathcal M_q$，处理素数幂/低阶项，完成 Ratios 的"初等"证明——**这就是 Route C**。

**结论预告 [推导]**：步骤 2 可做；步骤 3 的截断误差**不能**由第二/第四矩控制（§3：Möbius 多项式的第二矩在长度 $X\gg q$ 上即需 AP 双线性相关）；步骤 5 的**第二项（wrap-around，$A\equiv B\bmod q$、$A\ne B$）也不可控**（§4）；二者是同一致命点的两化身；步骤 1 的根数项可精确处理（§5）；步骤 5 的主项匹配未建立但次要（§6）。

---

## 2. 截断 Möbius 引理：在 GRH 下成立，且 q^ε 一致（不是致命点）

**[事实/推导] Lemma (truncated Möbius under GRH).** 设 χ 为 primitive mod q，$s=1/2+\eta+it$，$\eta\in(0,1/2)$，$T\ge1$，$|t|\le T$。对任意 $X\ge1$ 与 $\varepsilon>0$，
$$1/L(s,\chi)=\sum_{n\le X}\mu(n)\chi(n)n^{-s}+O_\varepsilon\bigl(X^{-\eta/2}(qT)^\varepsilon\bigr).$$
**证明思路 [推导]**：Perron 公式（$c=1+\eta/2$）：
$$\sum_{n\le X}\mu(n)\chi(n)n^{-s}=\frac1{2\pi i}\int_{(c)}\frac{1}{L(w,\chi)}\frac{X^{w-s}}{w-s}\,dw.$$
把轮廓移到 $\Re w=\frac12+\frac\eta2$（GRH 下 $1/L(w,\chi)$ 在该竖直线上全纯，且 $L(w,\chi)\neq0$；$w=1$ 的 ζ 极点在 $q>1$ 时被 Euler 因子消去），得
$$\sum_{n\le X}\mu(n)\chi(n)n^{-s}=\frac1{L(s,\chi)}+O\Bigl(X^{1/2+\eta/2-\sigma}\cdot\sup_{\Re w=1/2+\eta/2}|1/L(w,\chi)|\cdot\log T\Bigr),$$
其中 $\sigma=\Re s=1/2+\eta$，指数 $1/2+\eta/2-(1/2+\eta)=-\eta/2$；在 GRH 下
$$\sup_{\Re w=1/2+\eta/2,\ |\Im w|\le T}|1/L(w,\chi)|\ll_\varepsilon(qT)^\varepsilon$$
（由标准零自由区/局部零点展开；$w$ 与零点距离 $\ge\eta/2$）。证毕。$\square$
**要得到 $q^{-\omega}$ 的误差**（逐点、供 Cauchy/三线使用）：令 $X^{-\eta/2}(qT)^\varepsilon\ll q^{-\omega}$，得
$$X\ \ge\ q^{2\omega/\eta}(qT)^{2\varepsilon/\eta}.\tag{2.1}$$
若 $\eta$ 固定（如 $\eta=1/10$）则 $X=q^{20\omega}$ 是多项式但巨大；若 $\eta\to0$（如 GWX 插值中可取 $\eta$ 很小），$X$ 是指数级 $e^{2\omega(\log q)^2/\eta}$。
**结论**：截断 Möbius 引理**在 GRH 下成立且 q^ε 一致**，不是 Route C 的致命点；但 (2.1) 是不可协商的长度要求，迟早要与后面的正交性/大筛要求冲突（§4）。

---

## 3. 截断误差 × 分子 AFE 的矩控制：**Cauchy–Schwarz 不够，也回到同一个致命点**

记截断误差 $E_s=1/L(s,\chi)-P_s(\chi)$、$E_t$ 同理。$R_q$ 的误差项中最危险的是
$$T_1=\sum_{\chi}^{*}E_s(\chi)L(a,\chi)L(b,\bar\chi)P_t(\bar\chi).$$
**[推导] Step 1（用逐点界 + 绝对值）**：若用 (2.1) 取 $X$ 使 $|E_s|\ll q^{-\omega}$，
$$|T_1|\le q^{-\omega}\sum_{\chi}^{*}|L(a,\chi)L(b,\bar\chi)P_t(\bar\chi)|
\le q^{-\omega}\Bigl(\sum_{\chi}^{*}|L(a,\chi)L(b,\bar\chi)|^2\Bigr)^{1/2}
\Bigl(\sum_{\chi}^{*}|P_t(\bar\chi)|^2\Bigr)^{1/2}.$$
**[事实/推导] Step 2（分子矩）**：对 prime q，Young 的四次矩给出
$$\sum_{\chi\bmod q}^{*}|L(1/2+it,\chi)|^4\ll q^{1+\varepsilon}(1+|t|)^{O(1)},$$
于是 $\sum^{*}|L(a)L(b)|^2\le(\sum^{*}|L(a)|^4)^{1/2}(\sum^{*}|L(b)|^4)^{1/2}\ll q^{1+\varepsilon}$；
分子因子 $=(\cdot)^{1/2}\ll q^{1/2+\varepsilon}$。**（general composite q 的四次矩在 level aspect 不是已知的标准结果；这是 Route C 的另一个隐藏输入，先记为 [推测] 可望而不可即。）**

**[推导] Step 3（关键：Möbius 多项式的第二矩失控）**：
$$\sum_{\chi\bmod q}^{*}|P_t(\bar\chi)|^2
=\sum_{m,n\le X}\mu(m)\mu(n)(mn)^{-1/2-\eta}\sum_{\chi}^{*}\bar\chi(m)\chi(n).$$
用精确正交性（q prime）：$\sum^{*}\bar\chi(m)\chi(n)=\varphi(q)\mathbf 1_{m\equiv n(q)}-\mathbf 1_{m=n}$。对角部分（$m=n$）给
$$\varphi(q)\sum_{m\le X}m^{-1-2\eta}-\sum_{m\le X}m^{-1-2\eta}=\varphi(q)\cdot\frac1{2\eta}+O(1)\asymp\frac q\eta,$$
这是可接受的。但**非对角部分** $m\equiv n\pmod q$、$m\ne n$（wrap-around）是
$$\sum_{\substack{m,n\le X\\ m\equiv n(q),\,m\ne n}}\mu(m)\mu(n)(mn)^{-1/2-\eta}$$
——**又是一个 Type II/Chowla 型 AP 相关**。GRH 级别能拿到的唯一通用上界是大筛：
$$\sum_{\chi}^{*}|P_t(\bar\chi)|^2\le(q+X)\sum_{m\le X}m^{-1-2\eta}\ll\frac{q+X}{\eta}.$$
当 $X\ge q^{2\omega/\eta}\gg q$ 时这给 $\asymp X/\eta$，于是
$$|T_1|\ll q^{-\omega}\cdot q^{1/2+\varepsilon}\cdot\Bigl(\frac{X}{\eta}\Bigr)^{1/2}
=q^{1/2-\omega+\omega/\eta+\varepsilon}\eta^{-1/2},$$
**比目标 $q^{1-\omega}$ 大 $q^{\omega/\eta-1/2}$**。因为 (2.1) 的 $X$ 必然使 $X\gg q$，而 $\omega/\eta\gg1$，**Cauchy–Schwarz + 大筛绝无可能闭合**。
- **[事实] 备注**：即使假设四次矩 $\sum|L|^4\ll q^{1+\varepsilon}$（prime q 已知；composite q 不完整），上式仍差 $q^{\omega/\eta-1/2}$。**所以任务描述中的乐观设想"(2) 可以用第二矩控制"不成立**：分子第二/第四矩不是瓶颈，瓶颈是**分母 Möbius 多项式 $P_t$ 在长度 $X\gg q$ 上的第二矩**，它本身需要 AP 双线性相关估计。
- **[推导] 结论**：截断误差项**与 §4 的 wrap-around 项是同一个致命点的两个化身**：都需要
  $$\sum_{\substack{m,n\le X\\ m\equiv n(q)}}\mu(m)\mu(n)(mn)^{-1/2-\eta}\ll\frac{q}{\eta}\ (\text{或至少 }\ll q^{1-2\omega+\varepsilon})$$
  型估计，即 μ 在模 q AP 上的双线性相关。**GRH 不蕴含它。** 因此即便 §4 的 AFE 侧 wrap 项被证明可控，§3 的截断误差也照样致命。

## 4. 致命引理：精确正交性后的 wrap-around 双线性型

### 4.1 结构

假设截断误差已被控制（但 §3 表明这本身就需要致命输入），$R_q$ 的主部为
$$\sum_{\chi}^{*}U(\chi)V(\bar\chi),\quad U(\chi)=\sum_{A\le L}u_A\chi(A),\quad V(\chi)=\sum_{B\le L}v_B\bar\chi(B),\quad L=RX.$$
**精确正交性**（q prime；一般 q 用 $\sum_{d|q}\mu(q/d)$ 展开，类似）：
$$\sum_{\chi\bmod q}^{*}\chi(A)\bar\chi(B)=\begin{cases}\varphi(q)-1,&A\equiv B\pmod q,\\ -1,&A\not\equiv B\pmod q,\end{cases}\quad(\text{for }(AB,q)=1)$$
即 $\Sigma_*=\varphi(q)\sum_{A\equiv B(q)}u_A\bar v_B-\sum_{A=B}u_A\bar v_B$。第一项含 wrap-around（$A\equiv B\pmod q$，$A\ne B$）；第二项是"对角线"（可算，可能对应主项的一部分）。

### 4.2 GRH 级别可用的所有工具

- **(a) 大筛（character large sieve）**：对任意系数 $c_A$，
  $$\sum_{\chi\bmod q}^{*}\Bigl|\sum_{A\le L}c_A\chi(A)\Bigr|^2\le(q+L)\sum_{A\le L}|c_A|^2.$$
- **(b) Cauchy–Schwarz**：$|\Sigma_*|\le(\sum^*|U|^2)^{1/2}(\sum^*|V|^2)^{1/2}\le(q+L)\|u\|_2\|v\|_2$。
- 系数 $L^2$ 范数：$u_A=\sum_{rm=A}a_r\mu(m)m^{-s}$，
  $$\|u\|_2^2=\sum_{A\le L}|u_A|^2\le\Bigl(\sum_{r\le R}|a_r|^2\Bigr)\Bigl(\sum_{m\le X}|m^{-s}|^2\Bigr)\ll (\log R)\cdot\zeta(1+2\eta)\ll\frac{\log q}{\eta}.$$
  同理 $\|v\|_2^2\ll\log q/\eta$。故
  $$|\Sigma_*|\le(q+L)\frac{\log q}{\eta}\asymp L\frac{\log q}{\eta}=R X\frac{\log q}{\eta}.$$
- 若不用大筛而逐点用 GRH：$\sum_\chi^*|U(\chi)|^2$ 正是"水平的 second moment of a Dirichlet polynomial"；GRH 给出单点 $|L|\ll q^{1/4+\varepsilon}$ 等，但**求和后的 $L^2$ 没有任何 GRH-可得的比大筛更好的界**（大筛是已知最优通用工具；要更好需要 Ratios/Chowla 型输入）。

### 4.3 与截断长度的矛盾（**[推导]，本报告的定量核心**）

- 截断 Möbius 要求 (2.1)：$X\ge q^{2\omega/\eta}(qT)^{2\varepsilon/\eta}$ ⇒ $L=RX\ge q^{1/2}\cdot q^{2\omega/\eta}(qT)^{o(1)}$。
- 大筛/Cauchy 给 $|\Sigma_*|\lesssim L\log q/\eta=q^{1/2+2\omega/\eta+o(1)}$。
- 目标误差 $q^{1-\omega+o(1)}$。要求
  $$\frac12+\frac{2\omega}{\eta}\le1-\omega+o(1)\iff\frac{2\omega}{\eta}+\omega\le\frac12+o(1).\tag{4.1}$$
- 三线插值需要（GWX (3.26)）：$\omega=\omega_D-8(\eta+r)(2+\omega_D)>2\eta$；取 $\omega_D\le1/2$、$\eta$ 足够小，有 $\omega\ge\omega_D/2$ 且 $\omega\ll1$、$\eta\ll\omega/20$。于是 $2\omega/\eta\gg40$，而右边 $\le1/2$。**(4.1) 绝无可能成立。**
- 即使把目标误差放宽到 $q^{1-\omega'}$（$\omega'$ 更小），只要 $\omega'>0$ 固定，仍有 $2\omega/\eta\gg1/\omega$ vs $\le1/2$。**无解。**
- **【推导】结论**：在"截断 Möbius + AFE + 精确正交性"的框架内，wrap-around 双线性型无法用 GRH 级别（大筛/矩）控制到 Ratios 所需精度。要闭合，必须证明一个**远强于大筛**的估计：
  $$\Bigl|\sum_{\substack{A,B\le L\\ A\equiv B(q),\,A\ne B}}u_A\bar v_B\Bigr|\le q^{1-\omega+\varepsilon}\quad\text{with }L=q^{1/2+2\omega/\eta},\tag{4.2}$$
  其中 $u,v$ 是 $\mu$/Λ-型系数的卷积。**(4.2) 是一个 Type II（双线性）AP 相关估计**；对 $\mu$ 的双线性相关是 Chowla 型、对 Λ 是素数对型，均属 parity barrier 范畴；**(4.2) 不比 H_Ratios 弱**（它编码的正是"跨 χ 的比值平均"在最难区域的行为）。
- **循环性**：若假设 (4.2)，那么它本身就是一个"跨 χ 双线性相关"假设；用它证明 Ratios 并不会提供独立证据——**Route C 的净收益为零**。

### 4.4 精确致命引理（陈述）

> **Fatal Lemma (Route C 的致命引理，本审计形式)**：对任意固定 $0<\omega\le1/2$、$0<\eta\le\omega/20$，令 $R\asymp(qT)^{1/2}$、$X\ge q^{2\omega/\eta}$、$L=RX$；设 $u_A=\sum_{rm=A}a_r\mu(m)m^{-s}$、$v_B=\sum_{sn=B}b_s\mu(n)n^{-t}$ 为 AFE×Möbius 的 Dirichlet 卷积系数。Route C 需要
> $$\Bigl|\sum_{\chi\bmod q}^{*}U(\chi)V(\bar\chi)\Bigr|\le q^{1-\omega+\varepsilon},\qquad U=\sum_{A\le L}u_A\chi(A),\ V=\sum_{B\le L}v_B\bar\chi(B).$$
> 但 GRH 级别可用的全部工具（大筛、Cauchy、第二/第四矩）只给
> $$\Bigl|\sum_{\chi}^{*}U(\chi)V(\bar\chi)\Bigr|\le(q+L)\|u\|_2\|v\|_2\asymp q^{1/2+2\omega/\eta+o(1)}\gg q^{1-\omega},$$
> 差至少 $q^{2\omega/\eta+\omega-1/2}$（$\gg q^{40\omega-1/2}$）。**闭合该 gap 等价于一个 Type II/Chowla 型双线性 AP 相关估计，不被 GRH 蕴含，且与 Ratios 猜想同级。**
> **Route C 不能 only-GRH 完成；它至多把问题循环归约。**

---

## 5. 根数/Gauss 和项：可精确处理，不是致命点

- **[推导]** 对 primitive χ，$\varepsilon(\chi)=\tau(\chi)/(i^e\sqrt q)$，$\tau(\chi)=\sum_{u\bmod q}\chi(u)e(u/q)$。AFE 反射项中的 $\varepsilon(\chi)$（或 $\varepsilon(\bar\chi)$）在 $\sum^*_\chi$ 下可**精确**求：
  $$\sum_{\chi}^{*}\varepsilon(\chi)\chi(A)\bar\chi(B)=\frac1{i^e\sqrt q}\sum_{u\bmod q}e(u/q)\sum_\chi^*\chi(A+u)\bar\chi(B)$$
  （用 $\tau(\chi)\chi(A)=\sum_u\chi(A+u)e(u/q)$ 或等价恒等式）；再对 χ 用正交性得到 $A+u\equiv B\pmod q$ 的条件，对 $u$ 求和给出 Ramanujan 和/同余条件。**这是精确恒等式，不需要估计**；产生的项与直接项同型（仍由 $L=RX$ 的 Dirichlet 多项式组成），只是系数带 $q^{-1/2}$（Gauss 和的 $1/\sqrt q$ 归一化）。**因此根数项本身不制造新障碍；它们的误差分析回到 §4 的同一 wrap-around 双线性型**（带额外 $q^{-1/2}$，可能还稍好）。**结论：root-number 不是致命点；致命点仍是 (4.2)。**
- 特别地，AFE 的 direct×reflected 与 reflected×direct cross terms 各含一个 $\varepsilon$；reflected×reflected 含 $\varepsilon(\chi)\varepsilon(\bar\chi)=1$（与 GWX 的根数抵消相同）。核验：$\varepsilon(\chi)\varepsilon(\bar\chi)=1$ 因 $|\varepsilon|=1$ 且 $\varepsilon(\bar\chi)=\overline{\varepsilon(\chi)}$。**所以根数结构是可控的，Route C 不会因根数失败。**

---

## 6. 主项是否匹配 $\mathcal M_q$？（次要，但未建立）

- **[推测]** 主项应来自"对角线" $A=B$（primitive subtraction 项）和/或 $A\equiv B\pmod q$ 中的"$q\mid A-B$ 的主部"；经过 Euler 乘积计算，可能给出 $\varphi^*(q)Z_q$；反射项经 Gauss 和精确计算可能给出 $H_qZ_q(1-b,1-a;s,t)$。**结构上应能匹配 $\mathcal M_q$**（因为 AFE 与功能方程正是 CFZ 主项的来源），但**Route C 的描述没有给出该计算**；有 factor/reflection 项不匹配的风险（例如 $H_q$ 的 parity 计数、$X_{q,e}$ 系数、$q^{-1/2}$ 归一化）。
- **[推导]** 即使主项完全匹配，§4 的误差也足以致命；所以 Route C 的主项问题**不是重点**，但若主项因 factor 或缺失 reflection 项而不匹配，Route C 会以更早的方式失败。**当前审计 verdict：主项匹配"可能但未证明"，不足以拯救 Route C。**

---

## 7. 最终判定（给 Lead）

1. **截断 Möbius 引理：成立**（GRH 下 q^ε 一致，Perron + GRH 的 $1/L$ 界），因此"truncation lemma 本身失败"**不是** Route C 的问题。问题在**截断长度的量级要求**：$X\ge q^{2\omega/\eta}$（§2, (2.1)）。
2. **wrap-around/正交性项：无法用 GRH 级别控制**。精确致命引理 = §4.4：所需精度 $q^{1-\omega}$ 与大筛界 $q^{1/2+2\omega/\eta}$ 之间差 $q^{2\omega/\eta+\omega-1/2}$；而 $\eta\ll\omega$ 使指数 $\gg1$。要闭合需要 Type II/Chowla 型双线性 AP 相关，未被 GRH 蕴含、与 Ratios 同级 ⇒ **循环**。
3. **根数项：可精确求，不是 fatal**：$\tau(\chi)$ 展开 + 正交性给出精确 Ramanujan/同余表达式；AFA 反射项贡献带 $q^{-1/2}$，甚至有利。
4. **主项匹配 $\mathcal M_q$：未建立**；结构上可能（AFE/功能方程与 CFZ 主项同源），但 Route C 的 sketch 未给出计算；即使匹配也救不了误差。
5. **Route C 有无机会？** 在"仅 GRH + 标准矩/大筛"的框架下**没有机会**；若 kernel-theorist 有额外结构（例如用 exact orthogonality 之外的新恒等式直接消去 wrap 项，或假设 (4.2) 型 Type II 输入），那么它不再是 GRH-only，且其假设与 H_Ratios 同级/更强——**无独立价值**。
6. **对 GWX 路线的影响**：无。GWX Theorem 1.1 是"H_Ratios + GRH ⇒ Goldbach"的条件性归约；Route C 只是试图证明 H_Ratios 的一个（失败的）策略。**GWX 路线仍以 H_Ratios 为最弱已知充分假设（见 minimal-hypothesis.md）。**

---

## 8. 关键公式/量级汇总

- 截断误差：$E_s\ll X^{-\eta/2}(qT)^\varepsilon$；需要 $X\ge q^{2\omega/\eta}$。
- AFE 长度：$R\asymp(qT)^{1/2}$；总长度 $L=RX\ge q^{1/2+2\omega/\eta+o(1)}$。
- 大筛：$\sum^*_\chi|U(\chi)|^2\le(q+L)\|u\|_2^2$；$\|u\|_2^2\ll(\log q)/\eta$。
- 目标误差：$q^{1-\omega}$；大筛给出 $\gtrsim q^{1/2+2\omega/\eta}\log q/\eta$。
- 无解条件：$\frac{2\omega}{\eta}\le\frac12-\omega$ 与 $\eta\le\omega/20$ 矛盾。
- 需要的额外输入：Type II/Chowla 型估计 (4.2)，不被 GRH 蕴含，与 H_Ratios 同级。

### 复现/文件说明

- 本审计基于 task-37 的文字描述与标准解析数论推导；**未阅读** kernel-theorist 的 `phase11/theory/lead-route-c.md`、`c1_*.py`、`mq_check*.py` 等（保持独立）。
- 未运行数值实验（Route C 的失败是结构性的量级矛盾，不需要数值验证；如需，可对小 q 验证 $\Sigma_*$ 的 wrap 项大小，但那不改变指数矛盾）。
- 引用：AFE 与 character large sieve 标准参考（Iwaniec–Kowalski, *Analytic Number Theory*, Ch. 5, 7, 12）；Young 四次矩 Ann. Math. 173 (2011)；truncated Möbius/Perron 标准；GWX arXiv:2611.18825（H_Ratios 目标）。
