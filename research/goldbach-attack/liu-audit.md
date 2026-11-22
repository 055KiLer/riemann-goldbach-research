# 李嘉旻–刘建亚《A Conditional Proof of the Goldbach Conjecture》深度审计与 Hypotheses S/R 攻击报告

审计人：liu-auditor（数学研究审计，独立复核）
日期：2026-11-21（CST）
对象：Jiamin Li & Jianya Liu, *A Conditional Proof of the Goldbach Conjecture*, 63 页，山东大学数学国家高层次人才培养中心（MRC）线上发布，发布日期 2026-11-13；本地文件 `/home/kiler/rh-work/liu-goldbach.pdf`（文本抽取 `/home/kiler/rh-work/liu-goldbach.txt`、`liu-goldbach.clean.txt`）。
方法：全文通读 + 关键公式回原 PDF 渲染核对（页 3、10、11、34、35、50、60）+ 关键恒等式独立重新推导 + 数值附录独立复算 + 文献检索（2026-11-21 11:05–11:20 CST）。
标记约定：**【事实】**＝有出处/可核对的事实；**【推导】**＝本报告独立推导并给出过程；**【推测】**＝判断/估计，非定理。

> 引用说明：文本抽取会丢失共轭横线、分母括号和式号位置（例如 $\overline{\Psi_N(\sigma+iy)}$ 的横线、$\frac{\delta_N}{2\sqrt{\eta(1-\eta)}}$ 的分式归属）。凡关键公式，本报告均回 PDF 原页核对后引用，必要时注明"按 PDF 排版还原"。

---

## 0. 结论速览（供 Lead 使用）

1. **【事实+推导】论文核心链条（GRH ⇒ 算子 $T_N$ 的精确二次型恒等式 ⇒ S/R ⇒ Goldbach 渐近）经我们逐式独立复核，内部是自洽的；没有找到致命数学错误。** 我们独立重推了零–范数字典、$\beta$-积分的模型恒等式 (2.32)–(2.33)、$\Gamma$ 分解 (4.4)、二次型恒等式 (7.17)（含共轭细节）、以及 $N=30030$ 的数值附录：Goldbach 无序素数对 = **905**（与论文一致；有序 1810），$\mathbb S(30030)\approx5.1212553$，$\delta_{30030}\approx0.4323102409$，$\alpha_N=1/\log N\approx0.09699366$，均与论文一致。
2. **【事实】论文自己明确承认"只有 GRH 不够"**：GRH 只能给出 $\|T_N\|\le\|T_N\|_{HS}\ll(\log N)^2$（Theorem 6.2 / (2.24)），其零自由宽度仅为 $\eta_N^{GRH}\asymp \mathbb S(N)/(N\log N)$（(2.25)）；论文原文（p.12）："This available norm bound is too large to make the Goldbach error smaller than its main term; S and R impose the required improvement." 以及（p.4）："In fact, GRH alone already gives a zero-free region for $X_N$ of the same form. Its width, however, falls short of that required by Hypothesis S…"。
3. **【推导】精确差距**：要证明 Hypothesis R 需 $\|T_N\|\le\delta_N$，而从 GRH 的三角形不等式路线得到的只是 $(\log N)^2$，其比值
   $$\frac{(\log N)^2}{\delta_N}=\sqrt{\frac{N}{\mathbb S(N)}}\;(\log N)^{1/2}.$$
   例：$N=10^{10}$ 时约 $4.2\times10^{5}$；$N=10^{20}$ 约 $5.9\times10^{10}$；$N=10^{100}$ 约 $1.3\times10^{51}$。要证明 Hypothesis S（任给缓慢增长的 $h$）需 $\|T_N\|\le \mathbb S/(2h\sqrt{1-\eta_N})$，相对 GRH 的三角不等式界需改进约 $2h(\log N)^2/\mathbb S$ 倍；S 要求的零自由宽度相对 GRH 宽度放大 $h^2(\log N)^4/\mathbb S^2$ 倍（即 (2.29)）。这些改进**都只能来自 $P_N,D_N,K_N$ 三部分之间的巨大相消**，论文明言其估计"do not measure cancellation between the components"（p.12）。
4. **【推导+推测】对 S/R 的攻击：目前已知技术都停在同一个墙前，而且我们发现单点下界路线连"证伪 R"都做不到。** 我们用 (5.8) 在 $s=2\alpha+i\gamma$（$\gamma$ 为某奇特征 L 零点纵坐标）得到
   $$\|T_N\|\ \ge\ \frac{4\log N}{\varphi(N)(1+\gamma^2)},$$
   而利用 Rosser–Schoenfeld 型下界 $\varphi(N)\ge N/(e^\gamma\log\log N)$（渐近意义）可证该下界与 $\delta_N$ 之比 $\to0$，故**不能**由此推翻 R。Alpöge/Claude 的 RH/GRH 证明（其 Lean 目录结构是 Stepanov 乘性 + theta 提升链 + 自守/正性理论，见 `/home/kiler/rh-full/src`：`Development/WeilBound`、`Formalism/SharpRestriction`、`PositivityTheory/…ThetaLifts…`；见第 8 节 grep 结果）只覆盖**乘性 L 函数零点**，与本文 S/R 所需的**加性素数对相关的算子范数**没有已知桥梁。**Alpöge 的证明只能兑现论文的 GRH(N) 假设，不能兑现 S/R；因此"Alpöge ⇒ 无条件 Goldbach（经本文路线）"不成立。**
5. **【推测】S/R 未必是假命题**：R 断言的加权误差 $O(\delta_N)$ 换算到素数对计数误差约 $\sqrt{\mathbb S(N)N}/\sqrt{\log N}$，只比"随机平方根涨落" $\sqrt{\#\text{pairs}}\approx\sqrt{\mathbb S N}/\log N$ 大 $\sqrt{\log N}$ 因子（推导见 §9.7）；论文 Appendix B 的有限维模型在 $N=30030$ 给出 $\|C\|/\delta_N\approx0.8269<1$（有限截断，非证明）。所以更准确的判断是：**S/R 是"可能为真但现有工具无法证明"的新型算子范数命题，而不是显然荒谬的假设。** 但证明 S/R 本身是一个与 Hardy–Littlewood 猜想同量级的新定理；本文并没有把 Goldbach 归约到更简单的问题，而是把它等价地重新编码成一个"谱范数版的加性素数对一致估计"。

---

## 1. 审计对象与版本（事实）

- **【事实】** 山东大学 MRC 官方页面（英文）：<https://mrc.sdu.edu.cn/english/info/1018/1514.htm>；中文：<http://mrc.sdu.edu.cn/info/1018/2193.htm>。两页均载明发布日期 **2026-11-13**，并给出 PDF 下载链接；摘要与论文首页 Abstract 一致。
- **【事实】** 本地 PDF 共 **63 页**（`pymupdf` 读取 `len(doc)==63`）；无 arXiv 版本被检索到（截至 2026-11-21 11:20 CST 的检索，见 §8；论文参考文献 [9] 是作者自己的另一篇 arXiv:2606.05224 "Theorem (1+1.9) on the Goldbach Conjecture"）。
- **【事实】** 论文的 GRH 假设为 **GRH(N)**（p.3）：
  > "GRH(N). *Every nontrivial zero of every primitive Dirichlet L-function whose conductor divides N has real part 1/2.*"
  注意：这只涉及 Dirichlet L 函数（偶/奇、本原、导子整除 N），不涉及其他 L 函数。
- **【事实】** Alpöge/Claude 的 Lean 证明的公开验证页（本地快照 `/home/kiler/rh-work/mit/grh_page_now.html`，页面自述最后更新 2026-11-20 22:05 UTC）写明：五个主定理包含 `DirichletLZerosOnLine`、`PrimitiveDirichletLZerosOnLine`，且明确 "**"GRH" here means Dirichlet L-functions only.**"；即 Alpöge 的结果恰好覆盖本文所需的 GRH(N)（对所有导子、本原或非本原均含）。**【事实】** 但其验证状态仍有 caveat：页面 Summary 中 "The lake comparator run and the Lean-kernel replay of the export are still in progress."（同一页面在本地 11:04 的快照 `grh_page_1130.html` / `now_*` 中，nanoda、con-leche、lean4lean 等已通过，lake comparator 与 Lean 导出重放标记为 running）。此点由 repo-verifier/proof-digest 负责，不是本报告的审计对象；本报告只记"若 Alpöge 结果成立，则本文 GRH(N) 假设成立"。

---

## 2. 逻辑链完整重建（含逐式核对）

以下把论文的证明拆成 8 个环节；除特别标记外均为 **【事实】**（论文陈述，我们已回原页核对），配合 **【推导】** 给出独立理解。页号均为 PDF 实际页码（与文本抽取的 `===== PAGE n =====` 一致）。

### 2.1 奇特征正交投影：(2.1)–(2.5)、Lemma 3.1（p.5–6、p.15–16）

- 设 $N$ 偶，$\phi\in C_c^\infty(\mathbb R)$ 非零、非负、支撑在 $[1/3,2/3]$、$\phi(u)=\phi(1-u)$。加权 Goldbach 相关量（1.3, p.2）：
  $$G(N)=\frac1N\sum_{\substack{n+m=N\\(nm,N)=1}}\Lambda(n)\Lambda(m)\phi(n/N)\phi(m/N),$$
  主项猜想为 $c_\phi\mathbb S(N)$，其中 $c_\phi=\int_0^1\phi^2$，$\mathbb S(N)=2C_2\prod_{p\mid N,p>2}\frac{p-1}{p-2}$，$C_2=\prod_{p>2}(1-\frac1{(p-1)^2})$（(1.2),(1.4)，p.2）。
- $X_N^-$ = 模 $N$ 的所有奇特征（含非本原，非单位处延拓为 0）。**Lemma 3.1（p.15–16）**：对偶数 $N\ge4$，
  $$G(N)=D(N)-P(N),\qquad D(N)=\frac1N\sum_{(n,N)=1}\Lambda^2(n)\phi^2(n/N),\quad P(N)=\frac{2}{\varphi(N)}\sum_{\chi\in X_N^-}|P_\chi|^2,\tag{2.2,2.3}$$
  $$P_\chi=\sum_n\frac{\Lambda(n)\chi(n)}{\sqrt n}\Phi(n/N),\qquad \Phi(u)=\sqrt u\,\phi(u).\tag{2.4,2.5}$$
  证明要点：正交关系
  $$\frac2{\varphi(N)}\sum_{\chi\in X_N^-}\chi(n)\overline{\chi(m)}=\mathbf 1_{(nm,N)=1}\bigl(\mathbf 1_{n\equiv m\ (N)}-\mathbf 1_{n\equiv -m\ (N)}\bigr)\tag{2.1}$$
  （**注意共轭：抽取文本漏掉了 $\overline{\chi(m)}$，PDF p.15 与推导均要求它；我们已独立验证：对 $N=5$，$n=2,m=3$ 取共轭时等式两边均为 $-1$，不取共轭则为 $+1$，故共轭不可省**）；在 $\phi$ 的支撑上有 $N/3\le n,m\le 2N/3$，故 $|n-m|\le N/3$、$2N/3\le n+m\le4N/3$，于是两个同余分别退化为 $n=m$ 与 $n+m=N$。乘 $\Lambda\Lambda\phi\phi/N$ 求和得 (2.2)。
- **【推导】核对**：$P(N)\ge0$、$G(N)\ge0$ 均显然（$|P_\chi|^2\ge0$；$G$ 的项非负），所以 $0\le P\le D$ 成立；$D(N)\ll\log N$ 由 $\Lambda^2(n)\le(\log N)\Lambda(n)$ 与 Chebyshev 界得（3.1, p.16）。此步无条件、无漏洞。

### 2.2 Mellin 化与三族分解：(2.6)–(2.8)、Prop 3.2、Lemma 3.4、Lemma 3.5（p.6、16–19）

- 解析核（2.6）：$P_N(s,z)=\frac2{\varphi(N)}\sum_{\chi\in X_N^-}g_\chi(s)g_{\bar\chi}(z)$，$g_\chi(s)=\frac{L'}L(1/2+s,\chi)$。由 $-\frac{L'}L(1/2+s,\chi)=\sum_n\Lambda(n)\chi(n)n^{-1/2-s}$ 与 Mellin 反演（2.7）得（2.8）：
  $$P(N)=\frac{1}{(2\pi i)^2}\int_{(\sigma)}\int_{(\sigma)}N^{s+z}\tilde\Phi(s)\tilde\Phi(z)P_N(s,z)\,ds\,dz,$$
  在 $\sigma>1/2$ 时无条件成立（绝对收敛），在 **GRH(N)** 下可移到 $0<\sigma\le1/9$（Lemma 3.5, p.19；水平边由 Lemma 3.4 的 $g_\chi(\sigma+it)\ll_I\log^2(N(|t|+2))$ 界与 $\tilde\Phi$ 的快速衰减控制）。
- **【事实】Prop 3.2（p.16–17）**：$\Re s,\Re z>1/2$ 时
  $$P_N(s,z)=\sum_{n,m\ge1,(nm,N)=1}\frac{\Lambda(n)\Lambda(m)}{n^{1/2+s}m^{1/2+z}}\bigl(\mathbf 1_{n\equiv m\,(N)}-\mathbf 1_{n\equiv -m\,(N)}\bigr),\tag{3.2}$$
  且在 GRH(N) 下 $P_N$ 在 $\Re s,\Re z>0$ 全纯、满足 $P_N(s,z)=P_N(z,s)$、$P_N(s,z)=P_N(\bar s,\bar z)$；$P_N(s,\bar z)$ 半正定、秩 $\le\varphi(N)/2$（Gram 表示 (2.13)）。
- **【推导】核对**：GRH(N) 下每个奇特征 L 的零点/极点位置：非平凡零点在 $u=1/2+i\gamma$ 即 $s=i\gamma$（$\Re s=0$）；本原平凡零点在 $u=-1,-3,\dots$（$\Re s<0$）；非本原额外 Euler 因子零点在 $u$ 纯虚（$\Re s=-1/2$）。故 $g_\chi$ 在 $\Re s>0$ 全纯。**（论文 p.17 有一处 u/s 记号混用的笔误：把"额外 Euler 因子零点在 u 的实部为 0"写成"$\Re s=0$"，实际应为 $\Re u=0$ 或 $\Re s=-1/2$；不影响结论，属表述瑕疵。）**
- **【事实】三族表（p.7）**：$m=n+kN$（+）、$n=m+kN$（+）、$n+m=kN$（−），$k\ge1$。权重反演后由支撑条件只有 $k=1$ 的和族存活——这是后面模型构造的动机。

### 2.3 Beta 模型与精确主项：(2.9)–(2.12)、Lemma 4.1–4.3、Prop 4.4（p.7–8、20–24）

- 三个连续积分（Lemma 4.1, p.21；$w=s+z$）：
  $$\int_0^\infty x^{-1/2-s}(x+h)^{-1/2-z}dx=h^{-w}B(1/2-s,w),$$
  $$\int_0^\infty x^{-1/2-z}(x+h)^{-1/2-s}dx=h^{-w}B(1/2-z,w),$$
  $$\int_0^h x^{-1/2-s}(h-x)^{-1/2-z}dx=h^{-w}B(1/2-s,1/2-z),$$
  符号 $+,+,-$ 组合出 $K_-(s,z)=B(1/2-s,s+z)+B(1/2-z,s+z)-B(1/2-s,1/2-z)$（(2.9)）。三项共同的局部密度是 $\mathbb S(kN)$（(1.2) 的形式；Lemma 4.1 用 $\nu_p(h)$ 计数核对，p.21）。
- 密度级数/对角级数（2.10–2.11）：
  $$D_N(w)=\sum_{(n,N)=1}\frac{\Lambda^2(n)}{n^{1+w}},\qquad \mathbb S_N(w)=\sum_{k\ge1}\frac{\mathbb S(kN)}{k^w}=\mathbb S(N)\zeta(w)\mathcal P_N(w),\quad \mathcal P_N(w)=\prod_{p>2,p\nmid N}\Bigl(1+\frac{p^{-w}}{p-2}\Bigr).$$
  **Lemma 4.3（p.22–23）**：$\mathbb S_N$ 亚纯延拓到 $\Re w>0$，唯一单极点在 $w=1$，留数 $\operatorname{Res}_{w=1}\mathbb S_N(w)=\frac{N}{\varphi(N)}$（(4.5)）；且
  $$\frac{C_2N}{\varphi(N)}\le \mathbb S(N)\le\frac{N}{\varphi(N)}\ll\log\log N,\qquad \mathbb S(N)>1.\tag{4.7}$$
- **【推导】独立核对 (4.7)**：$\mathbb S(N)=\frac{N}{\varphi(N)}\prod_{p>2,p\nmid N}\bigl(1-\frac1{(p-1)^2}\bigr)$；该乘积介于 $C_2$ 与 1 之间；又由定义本身 $\mathbb S(N)\ge2C_2>1$。$\frac{N}{\varphi(N)}\ll\log\log N$ 由 Mertens 定理/标准估计得（论文 p.23 的证明分成 $p\le y=\log N$ 与 $p>y$ 两段，思路正确；其文字"$S(N)\ge2C_2$"用的是定义式而非 (4.7) 下界，表述稍乱但结论正确）。数值核对：$2C_2=1.32032363\dots$；$N=30030$ 时 $\mathbb S=5.12125533\dots$；取前 $k$ 个素数之积的 primorial，$\mathbb S/\log\log N\to\sim1.8$–$2.1$（我们算了 $N=5\times10^5,\,6.5\times10^9,\,4.1\times10^{28},\,2.6\times10^{98}$，比值 $2.12,2.02,1.89,1.83$），与 $\mathbb S(N)\ll\log\log N$ 一致。
- **【事实】Prop 4.4（p.23–24）**：由 $\Gamma$ 反射/倍元恒等式得 (4.4) $K_-(s,z)=2^{1-w}\Gamma(w)\cos(\pi w/2)X_1(s)X_1(z)$，$X_1(s)=\frac{\Gamma((3/2-s)/2)}{\Gamma((3/2+s)/2)}$；代入 $\zeta$ 函数方程后
  $$K_N(s,z)=\mathbb S(N)\Bigl(\frac{\pi}{N}\Bigr)^{s+z}\mathcal P_N(s+z)\zeta(1-s-z)X_1(s)X_1(z)\tag{2.12}$$
  在 $\Omega=\{0<\Re s,\Re z<3/2\}$ 上全纯。
- **【推导】核对 (2.12) 的 $\pi^w$ 常数**：$\zeta(1-w)=2(2\pi)^{-w}\Gamma(w)\cos(\pi w/2)\zeta(w)$，故 $2^{1-w}\Gamma(w)\cos(\pi w/2)=\pi^w\zeta(1-w)/\zeta(w)$，于是 $K_N=N^{-w}\mathbb S(N)\zeta(w)\mathcal P_N(w)\cdot\pi^w\zeta(1-w)/\zeta(w)\,X_1X_1=\mathbb S(N)(\pi/N)^w\mathcal P_N(w)\zeta(1-w)X_1X_1$，**与 (2.12) 一致**（不是 $(2\pi/N)^w$）。另外 $\mathcal P_N(w)$ 在 $w=0$ 处有单极点（$\log\mathcal P_N(w)\sim\log\frac1{\Re w}$，与 $\mathbb S(N)\mathcal P_N(2\sigma)\sim\frac1{2\sigma}$ 一致，见 Appendix A (A.9) 附近，p.56），与 $\zeta(1-w)$ 的极点相合成 $K_N$ 在 $w=0$ 的二阶极点，但 $w=0\notin\Omega$（$\Re w>0$），不影响 $\Omega$ 上全纯性。**【事实】** 论文 p.24 只提到 $\zeta(1-s-z)$ 的极点在 $s+z=0$，未提 $\mathcal P_N(s+z)$ 也在那里有极点，但两者都在 $\Omega$ 外，结论不受影响（属省略，不是错误）。

- **【事实】Prop 4.5（p.24）**：GRH(N) 下残差
  $$E_N(s,z)=P_N(s,z)-D_N(s+z)-K_N(s,z)$$
  在 $\Omega$ 上全纯，且 $E_N(s,z)=E_N(z,s)$、$E_N(s,z)=E_N(\bar s,\bar z)$，故 $E_N(s,\bar z)$ 为 Hermitian 核。

### 2.4 残差积分与"精确"Goldbach 恒等式：(2.31)–(2.35)、Lemma 7.1–7.2、Prop 7.3（p.13、43–47）

- **【事实】** 对 $0<\sigma\le1/9$（Lemma 3.5、Lemma 7.1）：
  $$P(N)=\frac1{(2\pi i)^2}\int_{(\sigma)}\int_{(\sigma)}N^{s+z}\tilde\Phi(s)\tilde\Phi(z)P_N(s,z)\,ds\,dz,\tag{7.3}$$
  $$\frac1{(2\pi i)^2}\int_{(\sigma)}\int_{(\sigma)}N^{s+z}\tilde\Phi(s)\tilde\Phi(z)D_N(s+z)\,ds\,dz=D(N),\tag{7.5}$$
  $$I_N(\Phi):=\frac1{(2\pi i)^2}\int_{(\sigma)}\int_{(\sigma)}\tilde\Phi(s)\tilde\Phi(z)\mathbb S_N(s+z)K_-(s,z)\,ds\,dz=-c_\phi\mathbb S(N).\tag{7.6}$$
- **【推导】核对 (7.6)（这是任务点名的 "(2.32)–(2.33)"）**：把 $w=s+z$ 代入，$I_N(\Phi)=\frac1{2\pi i}\int_{(2\sigma)}\mathbb S_N(w)\widetilde{H_0}(w)dw$，其中
  $$\widetilde{H_0}(w)=\frac1{2\pi i}\int_{(\eta)}\tilde\Phi(s)\tilde\Phi(w-s)K_-(s,w-s)ds,\quad H_0(y)=2C_0(y)-J_0(y),$$
  $$C_0(y)=\int_0^\infty\phi(u)\phi(u+y)du,\quad J_0(y)=\int_0^y\phi(u)\phi(y-u)du.$$
  支撑 $C_0(k)=0\,(k\ge1)$、$J_0(k)=0\,(k\ge2)$、$J_0(1)=c_\phi$（$k$ 整数），故 $H_0(k)=0\,(k\ge2)$、$H_0(1)=-c_\phi$；又 $\widetilde{H_0}(1)=0$ 消掉 $\mathbb S_N$ 在 $w=1$ 的极点，把 $w$-围道移到 $\Re w=3/2$ 后逐项 Mellin 反演得
  $$I_N(\Phi)=\sum_{k\ge1}\mathbb S(kN)H_0(k)=\mathbb S(N)(-c_\phi)=-c_\phi\mathbb S(N).$$
  我们逐条检查了 $2C_0$ 的来源（两个正差族各贡献一个 $C_0$）、$H_0(0)=2c_\phi$（无关紧要）、$\int C_0=a_0^2/2$、$\int J_0=a_0^2$、$H_0(1)=-c_\phi$，以及 $w$-围道移动所需的绝对可积主导项（论文 p.46–47 用 $|\tilde\Phi(s)|\ll(1+|v|)^{-6}$、$|\mathbb S_N(2\sigma+it)|\ll 1+|t|$、三条 Beta 因子的一致有界性给出可积主导函数，**成立**）。**结论：(2.32)–(2.33) 正确，常数与符号均对（注意模型积分自身为 $-c_\phi\mathbb S(N)$，残差里 $K$ 前是减号，故最终 $r=P-D+c_\phi\mathbb S$，符号自洽）。**
- **【事实】Prop 7.3（p.47）**：对 $0<\sigma\le1/9$，
  $$r_\sigma(N)=\frac1{(2\pi i)^2}\int_{(\sigma)}\int_{(\sigma)}N^{s+z}\tilde\Phi(s)\tilde\Phi(z)E_N(s,z)ds\,dz=P(N)-D(N)+c_\phi\mathbb S(N),$$
  $$G(N)=c_\phi\mathbb S(N)-r_\sigma(N).\tag{7.14}$$
  $r_\sigma$ 与 $\sigma$ 无关，记作 $r(N)$。

### 2.5 Hardy 空间与紧自伴算子：(2.14)–(2.17)、Prop 5.1–5.4（p.9、25–31）

- **【事实】** 取
  $$\alpha_N=\frac1{\log N},\quad\beta=\frac18,\quad\sigma_*=\frac19,\quad\Delta_N=\beta-\alpha_N,\quad S_N=\{\alpha_N<\Re s<\beta\},$$
  $$H_N=H^2(S_N),\quad \Gamma_N=(\alpha_N+i\mathbb R)\sqcup(\beta+i\mathbb R),\quad \langle h,g\rangle_{H_N}=\int_{\Gamma_N}h(s)\overline{g(s)}\,|ds|$$
  （内积对第一个变量线性、第二个共轭；两条边界各带正弧长，无 $1/(2\pi)$ 因子），算子（2.17）
  $$(T_Nh)(s)=\int_{\Gamma_N}\frac{E_N(s,\bar z)}{(1+s)(1+\bar z)}\,h(z)\,|dz|.$$
  **Lemma 5.2** 给出 Fourier–Laplace 表示 $h=U_H\psi$、$\|h\|^2_{H_N}=\int|\psi|^2(e^{2\alpha_N\tau}+e^{2\beta\tau})d\tau$；**Prop 5.3** 证明 $T_N$ 紧、自伴、Hilbert–Schmidt，且
  $$\sum_j\mu_j^2=\|T_N\|_{HS}^2=\int_{\Gamma_N}\int_{\Gamma_N}\frac{|E_N(s,\bar z)|^2}{|1+s|^2|1+\bar z|^2}|ds||dz|.\tag{5.4}$$
  **Prop 5.4** 给出点值公式与复制核 $k_z(s)=\frac1{4\Delta_N}\csc\frac{\pi(s+\bar z-2\alpha_N)}{2\Delta_N}$、
  $$\|k_s\|^2_{H_N}=\frac1{4\Delta_N}\csc\frac{\pi(\Re s-\alpha_N)}{\Delta_N}\le\frac1{8d_N(s)},\qquad |E_N(s,\bar z)|\le\|T_N\|\frac{|1+s||1+z|}{8\sqrt{d_N(s)d_N(z)}}.\tag{5.6–5.8}$$
- **【推导】核对**：(5.6) 由 $k_z(s)=\frac1{2\pi}\int_{\mathbb R}\frac{e^{(s+\bar z)\tau}}{e^{2\alpha_N\tau}+e^{2\beta\tau}}d\tau$ 与 Beta 积分 $\int_0^\infty\frac{t^{\lambda-1}}{1+t}dt=B(\lambda,1-\lambda)=\pi/\sin(\pi\lambda)$ 得到；$\|k_s\|^2=k_s(s)$；$d_N(\sigma_*)\ge\min(1/9-1/\log N,\,1/8-1/9)\ge1/90$（$N>e^{10}$），故 (5.9) $|E_N(\sigma_*+iv,\sigma_*+it)|\ll\|T_N\|(1+|v|+|t|)^2$ 成立。**（5.8）是我们后面攻击 R 的关键工具，已独立推导，无误。**

### 2.6 显式二次型恒等式：(2.36)–(2.40)、Prop 7.4、Theorem 7.1（p.13–14、48–50）

- **【事实】** 线性泛函（2.36）$\ell_N(h)=\frac1{2\pi i}\int_{(\sigma)}N^s\tilde\Phi(s)(1+s)h(s)ds$，其 Riesz 向量 $v_N$（$\ell_N(h)=\langle h,v_N\rangle$），范数
  $$Q_N=\|v_N\|^2=\frac1{2\pi}\int_0^\infty\frac{(Nu)^{2\alpha_N}|V(u)|^2}{1+(Nu)^{-2\Delta_N}}\frac{du}{u}\le\frac{e^2}{2\pi}\int_0^\infty\frac{|V(u)|^2}{u}du\ll_\phi1,\tag{2.37,2.38}$$
  其中 $V(u)=\Phi(u)-u\Phi'(u)$（分部积分 $\widetilde V(s)=(1+s)\tilde\Phi(s)$）。**Theorem 7.1（p.50）**：
  $$r(N)=\langle T_Nv_N,v_N\rangle,\qquad |r(N)|\le Q_N\|T_N\|\ll_\phi\|T_N\|\tag{7.17}$$
  从而 $G(N)=c_\phi\mathbb S(N)-\langle T_Nv_N,v_N\rangle$，$|G(N)-c_\phi\mathbb S(N)|\ll_\phi\|T_N\|$（(7.18) = 主估计 (2.19)）。
- **【推导】独立复核 (7.17)（逐共轭核对，这是最容易出错的地方）**：由 Riesz 向量 $v_N=\frac1{2\pi}\int_{\mathbb R}\overline{\Psi_N(\sigma+iy)}\,k_{\sigma+iy}dy$（$\Psi_N(s)=N^s\tilde\Phi(s)(1+s)$，PDF p.50 确有共轭横线），及 Gram/复制核恒等式 $\langle T_Nk_z,k_s\rangle=\frac{E_N(s,\bar z)}{(1+s)(1+\bar z)}$，得
  $$\langle T_Nv_N,v_N\rangle=\frac1{(2\pi)^2}\int_{\mathbb R^2}\Psi_N(\sigma+ix)\overline{\Psi_N(\sigma+iy)}\,\frac{E_N(\sigma+ix,\sigma-iy)}{(1+\sigma+ix)(1+\sigma-iy)}dx\,dy .$$
  用 $\overline{\Psi_N(\sigma+iy)}=\Psi_N(\sigma-iy)$（$\Phi$ 实值）把 $y\mapsto-y$，得
  $$=\frac1{(2\pi)^2}\int_{\mathbb R^2}\Psi_N(\sigma+ix)\Psi_N(\sigma+iy)\frac{E_N(\sigma+ix,\sigma+iy)}{(1+\sigma+ix)(1+\sigma+iy)}dx\,dy,$$
  而 $\frac{\Psi_N(s)}{1+s}=N^s\tilde\Phi(s)$，故此式正是
  $\frac1{(2\pi i)^2}\int_{(\sigma)}\int_{(\sigma)}N^{s+z}\tilde\Phi(s)\tilde\Phi(z)E_N(s,z)ds\,dz=r(N)$。
  **结论：(7.17) 正确（符号为正），论文 p.50 的推导与本复核一致。** 再结合 (7.14) 得 $G=c_\phi\mathbb S-\langle T_Nv_N,v_N\rangle$。

### 2.7 谱函数与零–范数字典：§2.4、§6（p.10–13、32–35）

- **【事实】** $\delta_N=\sqrt{\frac{\mathbb S(N)}{N}}(\log N)^{3/2}$（(1.5)，p.3）；谱函数（p.3、p.10、p.32）
  $$X_N(q)=\prod_j\Bigl(1-\frac{4\mu_j^2(N)}{\delta_N^2}q(1-q)\Bigr),\quad q\in\mathbb H,$$
  $X_N(0)=X_N(1)=1$，$X_N(1-q)=X_N(q)$，$X_N(\bar q)=\overline{X_N(q)}$，且在通常复切片上 $X_N(q)=\det(\mathrm{Id}-\frac4{\delta_N^2}q(1-q)T_N^2)$，$T_N^2$ 迹类（Prop 6.1, p.33）。
- **零分类（Prop 6.3, p.34）**：令 $d_j=\delta_N^2/\mu_j^2(N)$，因子零点满足 $q(1-q)=d_j/4$，故
  $$\begin{cases}\Re q=\frac12,\ |\Im q|=\frac12\sqrt{d_j-1}, & d_j>1\ (\Leftrightarrow|\mu_j|<\delta_N);\\ q=\frac12\ \text{(因子二重零点)},&d_j=1;\\ q=\frac12\pm\frac12\sqrt{1-d_j},&0<d_j<1\ (\Leftrightarrow|\mu_j|>\delta_N).\end{cases}$$
  非实零点组成 $\Re q=1/2$ 上的二维球面；**实零点只来自 $|\mu_j|>\delta_N$ 的"例外对"，且只有有限多个**（因 $\sum\mu_j^2<\infty\Rightarrow\mu_j\to0$，紧性）。零点的无穷乘积不产生额外零点（Prop 6.3 的绝对收敛论证，p.34）。
- **Hypotheses（p.4、p.12）**：
  - **Hypothesis S**：预先固定 $h(N)\to\infty$，使最终
    $$\eta_N=\frac{h^2(N)(\log N)^3}{N\mathbb S(N)}\le\frac14 ;\tag{1.7}$$
    对每个满足 GRH(N) 的充分大偶数 $N$，$X_N(q)$ 在 $\Re q>1-\eta_N$ 无零点。
  - **Hypothesis R**：对每个满足 GRH(N) 的充分大偶数 $N$，$X_N$ 的每个零点的实部都是 $1/2$。
- **【推导】字典（定理 6.1, p.35）**：见 §3，本报告独立重推并确认
  $$R(N)\iff\|T_N\|\le\delta_N,\qquad X_N(q)\ne0\ (\Re q>1-\eta)\iff\|T_N\|\le\frac{\delta_N}{2\sqrt{\eta(1-\eta)}}\quad(0<\eta<1/2),$$
  以及 (2.23) $\eta(M_N)=\frac{1-\sqrt{1-\delta_N^2/M_N^2}}2$（$M_N>\delta_N$）、$\eta(M_N)(1-\eta(M_N))=\delta_N^2/(4M_N^2)$。

### 2.8 主定理证明与"从 $G$ 到素数对"（p.12–13、50–51、5）

- **【事实】** 设零自由宽度 $0<\eta_N\le1/4$，由字典与 (7.18)：
  $$\frac{|G(N)-c_\phi\mathbb S(N)|}{c_\phi\mathbb S(N)}\ll_\phi\sqrt{\frac{(\log N)^3}{N\eta_N\mathbb S(N)}}\tag{7.19}$$
  故只需 $N\eta_N\mathbb S(N)/(\log N)^3\to\infty$（(7.20) = (2.27)）。
  - **Theorem 1.1（p.4、p.51）**：GRH +  Hypothesis S（宽度 (1.7)）⇒ $G(N)=c_\phi\mathbb S(N)+O_\phi(\mathbb S(N)/h(N))$；证明用 $\|T_N\|\le\delta_N/(2\sqrt{\eta_N(1-\eta_N)})=\mathbb S/(2h\sqrt{1-\eta_N})\le\mathbb S/(\sqrt3 h)$。
  - **Theorem 1.2（p.5、p.51）**：GRH + Hypothesis R ⇒ $G(N)=c_\phi\mathbb S(N)+O_\phi\bigl(\sqrt{\mathbb S/N}(\log N)^{3/2}\bigr)$，即 $O(\delta_N)$；且 R 蕴含 S（对所有满足 $\eta_N\le1/4$ 的宽度）。
- **【事实+推导】从 $G$ 到素数对下界（p.5 §2.5.3）**：$G(N)\le\frac{(\log N)^2}{N}\#\{(p,q):p+q=N\}$（每对素数贡献 $\le(\log N)^2/N$），故有序素数对数 $\ge G(N)N/(\log N)^2\gg_\phi\mathbb S(N)N/(\log N)^2$。**须排除"素数幂对"占主导**：$n=p^k(k\ge2)$ 或 $m=q^\ell(\ell\ge2)$ 的对数至多 $O(\sqrt N\log N)$（$N$ 以内素数幂只有 $O(\sqrt N)$ 个），其贡献 $O(\sqrt N\log^3N/N)=o(1)$，而 $\mathbb S(N)N/(\log N)^2\ge N/(\log N)^2$ 发散，故主项来自真素数对；且 $p,q\in[N/3,2N/3]$ 自动成立（$p+q=N$，$p,q\ge N/3$）。此步正确。

---

## 3. 零–范数字典的独立重新推导（逐常数核对）

**【推导】** 设 $T_N=T_N^*$ 紧、$\{\mu_j\}$ 为非零实特征值（含重数），$\sum\mu_j^2<\infty$。令 $d_j=\delta_N^2/\mu_j^2>0$。因子
$$F_j(q)=1-\frac{4\mu_j^2}{\delta_N^2}q(1-q)=1-\frac{4}{d_j}q(1-q)$$
（**注意：抽取文本曾把因子读成 $1-\frac{4\mu_j^2}{\delta_N^2q(1-q)}$，系分母/分子归属误读；PDF p.3 的 (1.6) 与 p.60 的 (B.3) 附近均可确认 $q(1-q)$ 在分子一侧的乘积位置。** 我们用 PDF 渲染核对过 p.3、p.11、p.60。）零化条件为 $q(1-q)=d_j/4$。

写 $q=x+yI$（$I$ 为单位纯虚四元数），$q(1-q)=x(1-x)+y^2+(1-2x)yI$。

1. **$y\ne0$**：虚部为零 ⇒ $x=1/2$；实部 $1/4+y^2=d_j/4$ ⇒ $y^2=(d_j-1)/4$。故
   - $d_j>1$：$|y|=\frac12\sqrt{d_j-1}$，非实零点（$\Re q=1/2$ 的球面）；
   - $d_j=1$：$y=0$，即 $q=1/2$，此时因子关于 $\xi=q-1/2$ 是二阶的（$F_j=1-\frac4{d_j}(1/4-\xi^2)=4\xi^2/d_j$，因为 $q(1-q)=1/4-\xi^2$），对应"因子二重零点"；
   - $0<d_j<1$：$y^2<0$，$y$ 必须为实，得 $q=\frac12\pm\frac12\sqrt{1-d_j}$，两个实零点。
2. **$y=0$（$q$ 实）**：$q\in(0,1)$ 时 $q(1-q)\in(0,1/4]$，需 $d_j/4>0$；其他情形 $q\notin(0,1)$ 时 $q(1-q)\le0$，而 $d_j/4>0$，故无零点（与 "$X_N(x)\ge1$ for real $x\notin(0,1)$" 一致）。**故全部零点如论文分类。**
3. **$R(N)\iff\|T_N\|\le\delta_N$**：$R$ 说无"实而非 $1/2$"的零点（非实零点总在 $\Re q=1/2$）⇔ 无 $0<d_j<1$ ⇔ 无 $|\mu_j|>\delta_N$ ⇔ $\sup_j|\mu_j|\le\delta_N$ ⇔ $\|T_N\|\le\delta_N$（$T_N=0$ 的平凡情形也含在内，$\sup\varnothing$ 约定为 0）。✔
4. **宽度字典**：固定 $0<\eta<1/2$。只有例外对的大根 $\frac12+\frac12\sqrt{1-d_j}$（对应 $|\mu_j|>\delta_N$，$0<d_j<1$）可能落进半平面 $\Re q>1-\eta$（另一根 $<1/2$；$\Re=1/2$ 的非实零点不在其中，因为 $1/2<1-\eta$）。大根被排除 ⇔
   $$\frac12+\frac12\sqrt{1-\frac{\delta_N^2}{\mu_j^2}}\le1-\eta\iff\sqrt{1-\frac{\delta_N^2}{\mu_j^2}}\le1-2\eta\iff1-\frac{\delta_N^2}{\mu_j^2}\le(1-2\eta)^2=1-4\eta+4\eta^2$$
   $$\iff\frac{\delta_N^2}{\mu_j^2}\ge4\eta(1-\eta)\iff|\mu_j|\le\frac{\delta_N}{2\sqrt{\eta(1-\eta)}} .$$
   左推右：平方可逆因 $1-2\eta>0$。非例外（$|\mu_j|\le\delta_N$）自动满足该界，因为 $\frac{\delta_N}{2\sqrt{\eta(1-\eta)}}>\delta_N$（$\eta<1/2$ 时 $2\sqrt{\eta(1-\eta)}<1$）。取 $\sup$ 得字典。✔
   **【事实】** PDF p.11 确实写作 $|\mu_j|\le\frac{\delta_N}{2\sqrt{\eta(1-\eta)}}$（文本抽取把分式压平为"$\delta_N/2\sqrt{\eta(1-\eta)}$"，易误读为我们曾怀疑的"$\frac{\delta_N}{2}\sqrt{\eta(1-\eta)}$"；PDF 排版确认前者）。同理 (2.28) 的 $\|T_N\|\le\frac{\mathbb S(N)}{2h(N)\sqrt{1-\eta_N}}$ 是正确形式（把 $\eta_N=\frac{h^2(\log N)^3}{N\mathbb S}=\frac{h^2\delta_N^2}{\mathbb S^2}$ 代入 $\delta_N/(2\sqrt{\eta_N(1-\eta_N)})$ 即得）。✔
5. **宽度公式 (2.23)**：给界 $\|T_N\|\le M_N>\delta_N$，取 $\eta=\eta(M_N)$ 使 $2\sqrt{\eta(1-\eta)}=\delta_N/M_N$，解得 $\eta(M_N)=\frac{1-\sqrt{1-\delta_N^2/M_N^2}}2$；且
   $$\eta(M_N)(1-\eta(M_N))=\frac{\delta_N^2}{4M_N^2},\qquad \eta(M_N)\asymp\frac{\delta_N^2}{M_N^2}\ (\eta\le1/4).$$
   ✔（与论文 (2.23) 一致。）
6. **例外对有限性**：$\sum_j\mu_j^2<\infty\Rightarrow\mu_j\to0$，故 $\{j:|\mu_j|>\delta_N\}$ 有限；实零点全部来自这些，且 $(0,1)$ 内。✔

**【结论】** 零–范数字典（(2.23)、(2.30)、Theorem 6.1）在所有常数与不等式方向上均正确；未见符号/尺度/指标错误。唯一"疑似错误"经 PDF 核对是文本抽取造成的误读。

---

## 4. GRH 的 $\|T_N\|_{HS}\ll(\log N)^2$ 界：可信性、余量与到 $\delta_N$ 的精确差距

### 4.1 该界的内容与可信度评估（事实+推导）

**【事实】** Theorem 6.2（p.36）：GRH(N) ⇒
$$\|T_N\|\le\|T_N\|_{HS}\ll(\log N)^2\tag{6.7}$$
并由字典得到零自由区 (6.8) $X_N(q)\ne0\ (\Re q>1-\eta_N^{GRH})$，$\eta_N^{GRH}\asymp\frac{\mathbb S(N)}{N\log N}$。

证明拆成 Prop 6.5（p.40–42）：$T_N=P_N-D_N-K_N$，
$$\|P_N\|_{HS}\le \operatorname{tr}P_N\ll(\log N)^2+\alpha_N^{-2},\qquad \|D_N\|_{HS}\le\operatorname{tr}D_N\ll\alpha_N^{-2},\qquad \|K_N\|_{HS}\ll\alpha_N^{-2},$$
在 $\alpha_N=1/\log N$ 时各自 $\asymp(\log N)^2$。

**【推导】独立核对三个分量**：
- **$P_N$**：$P_N=\frac2{\varphi(N)}\sum_{\chi\in X_N^-}|f_\chi\rangle\langle f_\chi|$，$f_\chi(s)=g_\chi(s)/(1+s)$。故 $\operatorname{tr}P_N=\frac2{\varphi(N)}\sum_\chi\|f_\chi\|^2_{H_N}$，而 $\|f_\chi\|^2_{H_N}=\int_{\alpha_N+i\mathbb R}\frac{|g_\chi|^2}{|1+s|^2}dt+\int_{\beta+i\mathbb R}\cdots\asymp\int_{\mathbb R}\frac{|g_\chi(\alpha_N+it)|^2}{1+t^2}dt+\text{同}(\beta)$。论文 Lemma 6.4（p.36–40）证明
  $$\frac2{\varphi(N)}\sum_{\chi\in X_N^-}\int_{\mathbb R}\frac{|g_\chi(\sigma+it)|^2}{1+t^2}dt\ll(\log N)^2+\sigma^{-2},\qquad0<\sigma\le\beta\tag{6.9}$$
  （对 $\sigma=\alpha_N$ 即 $\ll(\log N)^2$）。我们检查了其证明的三个技术点：(i) 参考线 $\sigma_{ref}=2/\log N$ 上，用缓和的 Dirichlet 多项式 + 奇特征正交性把 $\frac2\varphi\sum_\chi|P_{\chi,X}(1/2+\sigma_{ref}+it)|^2$ 化为对角和 $\sum_n\Lambda^2(n)n^{-1-2\sigma_{ref}}\ll\sigma_{ref}^{-2}=(\log N)^2/4$（(6.11)–(6.12)）；(ii) 由零点 Poisson 核 $Q_\chi$ 的正性作 $\sigma\le\sigma_{ref}$ 的传递 $E_\chi(\sigma)\ll(\sigma_{ref}/\sigma)^2E_\chi(\sigma_{ref})+(\log N)^2$（$K=\sigma_{ref}/\sigma\le2$ 当 $\sigma=\alpha_N$）；(iii) $\sigma\ge\sigma_{ref}$ 用圆盘 $H^2$/Poisson 积分（Cayley 变换后 $\ell=\sigma-\sigma_{ref}\le\beta$，$P_1*P_\ell=P_{1+\ell}\le(1+\ell)P_1$）。**结构正确，常数可绝对。**
- **$D_N$**：$D_N$ 的核为 $\sum_{(n,N)=1}\frac{\Lambda^2(n)}{n}d_n\otimes\bar d_n$，$d_n(s)=n^{-s}/(1+s)$，正秩一和；$\operatorname{tr}D_N=\pi\bigl(\frac{D_N(2\alpha_N)}{1+\alpha_N}+\frac{D_N(2\beta)}{1+\beta}\bigr)$，而 $D_N(2\sigma)=\sum\Lambda^2(n)n^{-1-2\sigma}\ll\sigma^{-2}$（$B(u)=\sum_{n\le u}\Lambda^2(n)\ll u\log(2u)$ + 分部求和：$\int_1^\infty\log(2u)u^{-1-2\sigma}du\asymp\sigma^{-2}$）。✔
- **$K_N$**：用 (2.12) 分解 $S(N)P_N(\sigma)\ll\sigma^{-1}$（Euler 乘积逐项 $\le p^\sigma$，$\prod_{p|N}p\le N$，$N^{-\sigma}\cdot N^\sigma=1$）、$|\zeta(1-\sigma-i\tau)|\ll\sigma^{-1}(2+|\tau|)^{2\beta}$（Euler 求和；$\Re w=2\beta\le1/4$ 时 $\zeta$ 在 $1-w$ 的实部 $\ge3/4$）、Stirling 估计 $|X_1(s)|\ll(1+|\Im s|)^{-\Re s}$，得边界核平方的主导
  $$\ll\alpha_N^{-4}\frac{(2+|t-y|)^{4\beta}}{(1+t^2)(1+y^2)},$$
  其 $\mathbb R^2$ 积分 $\asymp1$（因 $4\beta=1/2<1$，$\int(1+|t-y|)^{1/2}/((1+t^2)(1+y^2))<\infty$），故 $\|K_N\|_{HS}\ll\alpha_N^{-2}$。✔
- 三角不等式：$\|T_N\|_{HS}\le\|P_N\|_{HS}+\|D_N\|_{HS}+\|K_N\|_{HS}\ll(\log N)^2$。✔

**【评估】** (2.24)/(6.7) 的可信度高：三个分量各自都是"平凡大小"（$\asymp(\log N)^2$），三角不等式无相消。**并且这个界在分量层面是紧的**：$P_N$ 的迹本身 $\asymp(\log N)^2$（我们算：对导子为 $d_\chi$ 的 $\chi$，$\int|g_\chi(\alpha_N+it)|^2/(1+t^2)dt\asymp\frac1{\alpha_N}\sum_{\gamma_\chi}\frac1{1+\gamma_\chi^2}\asymp(\log N)(\log d_\chi)$，而对模 $N$ 特征平均 $\langle\log d_\chi\rangle\asymp\log N$），故 $\operatorname{tr}P_N\asymp(\log N)^2$。所以任何想靠"更精细的迹/均方估计"改进到 $\delta_N$ 的路线必然会失败；改进必须来自 $P_N-(D_N+K_N)$ 的相消，而论文自己的话说"they do not measure cancellation between the components"（p.12）。

### 4.2 精确差距（推导）

由 $\delta_N=\sqrt{\frac{\mathbb S(N)}N}(\log N)^{3/2}$：
$$\boxed{\ \frac{(\log N)^2}{\delta_N}=\sqrt{\frac{N}{\mathbb S(N)}}\,(\log N)^{1/2}\ }\tag{GAP-R}$$

数值（取最小奇异级数 $\mathbb S_{\min}=2C_2=1.3203$ 以简化；$\mathbb S(N)$ 越大差距略小）：

| $N$ | $\log N$ | $\delta_N$ | $(\log N)^2$ | $(\log N)^2/\delta_N$ |
|---|---|---|---|---|
| $10^4$ | 9.21 | $3.21\times10^{-1}$ | 84.8 | $2.6\times10^2$ |
| $10^6$ | 13.82 | $5.90\times10^{-2}$ | 190.9 | $3.2\times10^3$ |
| $10^{10}$ | 23.03 | $1.27\times10^{-3}$ | 530 | $4.2\times10^5$ |
| $10^{20}$ | 46.05 | $3.59\times10^{-8}$ | 2121 | $5.9\times10^{10}$ |
| $10^{50}$ | 115.1 | $1.42\times10^{-22}$ | 13255 | $9.3\times10^{25}$ |
| $10^{100}$ | 230.3 | $4.02\times10^{-47}$ | 53019 | $1.3\times10^{51}$ |

（$\mathbb S(N)$ 的实际范围：$2C_2=1.3203\le\mathbb S(N)\ll\log\log N$。大 $\mathbb S$ 使差距按 $1/\sqrt{\mathbb S}$ 略降，但不改变数量级结论。）

- **【推导】Hypothesis S 的差距**：S 要求 $\|T_N\|\le\frac{\mathbb S}{2h\sqrt{1-\eta_N}}$。相对 GRH 的 $(\log N)^2$，需要改进
  $$\frac{(\log N)^2}{\mathbb S/(2h\sqrt{1-\eta_N})}=\frac{2h(\log N)^2\sqrt{1-\eta_N}}{\mathbb S}\approx\frac{2h(\log N)^2}{\mathbb S}.$$
  由于 $\mathbb S\ll\log\log N$，即使 $h$ 只缓慢增长（如 $h=\log\log N$），改进因子也 $\asymp(\log N)^2$。
- **【推导】零自由宽度的差距**：由 (2.29)，
  $$\frac{\eta_N}{\eta_N^{GRH}}\asymp\frac{h^2(\log N)^4}{\mathbb S^2}.$$
  数值（取 $\mathbb S=2C_2$，$h=\log\log N$）：$N=10^{10}$ 时 $\approx1.6\times10^{6}$；$N=10^{20}$ 时 $\approx3.8\times10^{7}$；$N=10^{100}$ 时 $\approx4.8\times10^{10}$。
- **【事实】GRH 是否改变量级**：不改变。$\eta_N^{GRH}\asymp \mathbb S/(N\log N)$ 是论文从 (2.24) 推出的**全部**内容；它比 S 所需宽度小 $h^2(\log N)^4/\mathbb S^2$ 倍。即使 RH/GRH 被完全证明，论文中的定量输入仍只有 (2.24)，因此 S/R 依旧未决。

---

## 5. 其余关键步骤复核（逐项：置信度与说明）

| 步骤 | 位置 | 复核结论 | 置信度 |
|---|---|---|---|
| 奇特征正交 (2.1)（含共轭） | p.15 | 正确（已验证 $N=5$ 反例区分共轭与否）；非单位处延拓为 0 使 $(nm,N)=1$ 条件出现 | 高 |
| $G=D-P$、$0\le P\le D$、$D\ll\log N$ | p.16 Lemma 3.1 | 正确 | 高 |
| Prop 3.2：$P_N$ 全纯、Hermitian、正半定、秩 $\le\varphi/2$ | p.16–17 | 正确（Gram 表示） | 高 |
| Lemma 3.4 (3.8)/(3.9)：$g_\chi$ 的零点展开与垂直界 | p.17–18 | 正确；我们重推 (3.8) 并确认多出的 $-\tilde e_\chi(2)$ 来自把 $L'/L(2,\chi^*)$ 换成非本原 $L'/L(2,\chi)$（$L'/L(u,\chi)=L'/L(u,\chi^*)+\tilde e_\chi(u)$） | 高 |
| Lemma 4.1 三积分与密度 $\mathbb S(kN)$ | p.21 | 正确（$\nu_p(h)$ 计数核对无误） | 高 |
| Lemma 4.2 (4.3)/(4.4) $\Gamma$ 分解 | p.21–22 | 正确（我们重推：$K_-=\frac{\Gamma(r)\Gamma(t)\Gamma(w)}{\pi}4\sin\frac{\pi r}2\sin\frac{\pi t}2\cos\frac{\pi w}2$ 与 $X_1$ 的倍元公式相乘得 (4.4)） | 高 |
| Lemma 4.3：$\mathbb S_N$ 延拓/留数 $N/\varphi(N)$/(4.6)/(4.7) | p.22–23 | 正确（留数用恒等式 $(1-\frac1{(p-1)^2})(1+\frac1{p(p-2)})=1$ 验证） | 高 |
| (2.12) 中 $(\pi/N)^w$ 常数 | p.8/p.24 | 正确（见 §2.3 推导） | 高 |
| Prop 4.4/4.5：$K_N$ 与 $E_N$ 在 $\Omega$ 全纯、对称性 | p.23–24 | 正确；论文略提 $\mathcal P_N(s+z)$ 在 $s+z=0$ 也发散，但该点在 $\Omega$ 外，不影响 | 高 |
| Lemma 5.2 Fourier–Laplace 表示 | p.28–29 | 正确（Plancherel + Cauchy–Riemann 论证标准） | 高 |
| Prop 5.3：$T_N$ 紧自伴 HS、(5.4) | p.29–30 | 正确；关键是 (5.5) 的核平方主导，我们用 $\zeta$ 函数方程的指数衰减与 $\Gamma$ 估计复核，可积性成立（常数依赖固定 $N$） | 中高 |
| Prop 5.4：(5.6)–(5.9) 复制核与点值界 | p.30–31 | 正确（我们独立算出 $\|k_s\|^2=\frac1{4\Delta}\csc\frac{\pi(\Re s-\alpha)}{\Delta}$，与 (5.7) 一致） | 高 |
| Prop 6.1：乘积收敛、Fredholm 行列式 | p.33 | 正确（$\sum\mu_j^2<\infty$ 使 $\sum|u_j|<\infty$） | 高 |
| Prop 6.2/6.3：对称性、零分类、例外有限 | p.33–34 | 正确 | 高 |
| Theorem 6.1：零–范数字典 | p.35 | 正确（§3 独立重推） | 高 |
| Lemma 6.4 (6.9)：平均对数导数界 | p.36–40 | 结构正确；这是全文技术含量最高的一步，我们核对了参考线估计、Poisson 传递与圆盘 $H^2$ 两步，未发现方向性错误；常数为绝对（未逐常数重算，属"未完全逐项验证"项） | 中高 |
| Prop 6.5：三分量 HS/迹界 | p.40–42 | 正确（见 §4.1） | 高 |
| Theorem 6.2：GRH 基线 (6.7)/(6.8) | p.36, 42 | 正确（三角不等式 + 字典） | 高 |
| Lemma 7.1/7.2：(7.2)(7.3)(7.5)(7.6) | p.44–47 | 正确（(7.6) 见 §2.3 独立复核） | 高 |
| Prop 7.4：(2.37) 泛函范数公式 | p.49 | 正确（Fourier–Laplace + Mellin 反演；$\tau=-\log(Nu)$ 换元核对） | 高 |
| Theorem 7.1：(7.17) 二次型恒等式 | p.50 | 正确（逐共轭核对，见 §2.6） | 高 |
| Lemma 7.5/定理 1.1/1.2 推导 | p.50–51 | 正确 | 高 |
| §2.5.3 素数幂剔除 | p.5、p.14 | 正确（见 §2.8） | 高 |
| Appendix A.4 固定模数障碍 | p.55–56 | 正确（Laurent 展开我们复核：$P_N(s,\bar s)=C_{N,\gamma}/\sigma^2+O_{N,\gamma}(\sigma^{-1})$，$D_N(2\sigma)=\frac1{4\sigma^2}+O_N(1)$，$K_N(s,\bar s)=-\frac1{4\sigma^2}+O_{N,\gamma}(\sigma^{-1})$；结论 $\liminf_{c\downarrow0}c\|T_{N,c}\|\ge\frac{2C_{N,\gamma}\log N}{1+\gamma^2}>0$） | 高 |

---

## 6. 是否发现真正的错误？（结论：未发现致命错误；列出瑕疵与"未逐项验证"清单）

### 6.1 我们确认不是错误、但容易被误读的点

1. **【事实】提取文本 vs PDF**：`liu-goldbach.txt` 在 (2.1) 漏 $\overline{\chi(m)}$、在 (7.17) 漏 $\overline{\Psi_N(\sigma+iy)}$、在 (1.6) 把 $q(1-q)$ 错放到分母、在 (2.22) 漏 $\overline{X_N(q)}$ 的横线、(2.30) 的分式归属失真。回原 PDF（p.3、p.11、p.15、p.35、p.50）核对后**均正确**。因此这些是抽取瑕疵，不是论文错误。
2. **【事实】p.17 u/s 记号混用**："the additional Euler-factor zeros of imprimitive characters lie on $\Re s=0$" 应为 $\Re u=0$（等价 $\Re s=-1/2$）；结论"$g_\chi$ 在 $\Re s>0$ 全纯"正确，不影响证明。
3. **【事实】p.24 省略**：只说 $\zeta(1-s-z)$ 的极点在 $s+z=0$，未提 $\mathcal P_N(s+z)$ 在此也发散；但 $w=0\notin\Omega$，结论（$K_N$ 在 $\Omega$ 全纯）正确。
4. **【事实】p.23 文字顺序**："The remaining product lies between $C_2$ and 1. Also $C_2>\prod(1-m^{-2})=1/2$, so $\mathbb S(N)\ge2C_2>1$." 严格说 $\mathbb S(N)\ge2C_2$ 用的是定义式中 $\prod_{p\mid N}\frac{p-1}{p-2}\ge1$，不是 (4.7) 的下界；结论正确，仅叙述次序略乱。
5. **【事实/推测】风格问题（不影响正确性）**：文中出现"Fueter regular""intrinsic slice-regular quaternionic function"等对证明并非必需的包装，以及引用面向大众的 Lebl 讲义原话（"There is something very special about the holomorphic category."）；§8 的叙述（twin primes/Bourgain–Gamburd–Sarnak）与主证明无关。这些**不构成数学错误**，但提示本文可能经过大量非传统写作/编辑加工（**推测**），审稿人应重点核 §6 的逐常数估计，而不是被包装分散注意力。

### 6.2 属"技术性断言、未在论文中完全展开"的点（referee 会追问，但我们未发现方向性错误）

1. **Lemma 6.4**（p.36–40）是全文最重的一步：它包含 (6.10) 的 Poisson 比较、Perron 公式 (6.12) 的围道移动（"First let the height tend to infinity, then move the left line to minus infinity"、Euler 因子零点列的局部计数与水平段避开零点）、(6.14) 的两种传递。我们核对了逻辑结构与关键不等式，但没有逐常数重算所有 $\ll$ 依赖（论文声称"implied constant is absolute"）。**建议：若要把本文作为进一步工作的基础，应先把 (6.9) 的绝对常数重写一遍。**
2. **Prop 5.3** 的"边界核算子 $\tilde T_N$ 的值域落入 Hardy 迹空间"依赖 (5.5) 的一致主导与 Morera/控制收敛论证；对固定 $N$ 成立，但常数 $\ll_N$ 依赖 $N$（文中未追求统一）。**结论不受影响（谱性质只需固定 N）。**
3. **Lemma 7.2** 的多重 Mellin 反演/Fubini 交换：论文用显式可积主导函数（$\tilde\Phi$ 的 $(1+|v|)^{-6}$ 衰减、$\mathbb S_N$ 的线性增长、Beta 因子有界）论证；我们核对后认为足够，但细节留给审稿人。
4. **Appendix B** 的有限谱模型（2562 节点、$N=30030$）**不是**对 R 的证明：论文 p.62 自己写 "Cutoff stability and pointwise high-precision checks do not bound the full operator's truncation or discretization error. The figures illustrate the finite spectral model; they do not certify Hypothesis R for $T_{30030,1}$." —— 这一自我限定正确且必要。

### 6.3 数值附录独立复核（事实）

我们用独立 Python（素数筛 + Mertens 乘积极限计算，代码见 §11）复算：
- $N=30030=2\cdot3\cdot5\cdot7\cdot11\cdot13$，$\varphi(N)=5760$；
- **无序 Goldbach 素数对（$p\le q$，$p+q=30030$）= 905**，有序 = 1810 —— 与论文 Appendix B (B.3)/(B.4) 的 905 完全一致（**我们直接枚举素数验证，独立于论文的复分析计算**）；
- $\mathbb S(30030)=5.1212553287\dots$（论文用更精确 $C_2$）、$\delta_{30030}=0.432310240854\dots$（论文 0.432310239587548，差 $<10^{-9}$，因 $C_2$ 精度）、$\alpha_N=1/\log N=0.0969936605\dots$（论文 0.09699366）——均一致；
- 论文 (B.1) 的计数公式 $r_G(N)=\frac N2J-\frac{C_{pp}}2+E$ 的结构核对：无序计数 = (有序加权/2) − 素数幂修正 + 边缘修正，自洽。
- **【事实】** 但 Appendix B 只支持"计数方法与数值实现正确"，**不支持 S/R**；有限谱模型 $\|C\|/\delta_N\approx0.8269<1$ 与有限零点都在虚轴平移线上，是 2562 维截断的观测，论文本人已声明不构成 R 的认证。

---

## 7. 文献状态（2026-11-13 之后，检索至 2026-11-21 11:20 CST）

**【事实】**
1. **官方来源**：山东大学 MRC 英文/中文新闻页（见 §1）为唯一权威发布源，含 PDF；本地 PDF 与页面摘要一致。**未检索到 arXiv 条目**（检索 "A Conditional Proof of the Goldbach Conjecture arXiv"、"Li Liu Goldbach 2026" 均只返回 MRC 页面与二手报道；作者 2026-06 的 arXiv:2606.05224 是另一篇 (1+1.9) 论文）。
2. **二手/科普报道**：
   - 数学中国论坛转帖两篇：<http://www.mathchina.com/bbs/forum.php?mod=viewthread&tid=2069463>（2026-11-15 起，9 回复）与 <http://www.mathchina.com/bbs/forum.php?mod=viewthread&tid=2069475>（2026-11-16 起，7 回复）。**技术价值：零**。前者 1# 是通俗介绍（明确说"条件证明 ≠ 已证明猜想"、"GRH 至今没有证明"），回复多为业余爱好者（用户 ysr）关于自创"全深度筛"的发言，与本文无关；后者 1# 是 AI 风格的深度解读（对论文结构描述基本准确，例如正确指出 R 是"临界线条件在谱函数层面的对应物"、有限模型不构成证明），但**没有独立专家审稿意见**。
   - 中文问答：知乎问题「继发布「1+1.9定理」后，刘建亚、李嘉旻新给出哥德巴赫猜想的首个条件性证明？这意味着什么？」<https://www.zhihu.com/question/2104680319357907490>（页面 403，无法抓取回答正文）。
   - 今日头条/163/微博等转载报道（如 <https://m.toutiao.com/article/7708062452621099560/>）。
3. **未发现任何**：正式评注/勘误/follow-up 论文、arXiv/Zenodo 上的技术批评、MathOverflow/Reddit 的技术讨论、Zulip 讨论。
4. **【事实】与 Alpöge 2026-11-20 GRH 声明的关联**：检索 "Alpöge Goldbach"、"Alpöge Riemann hypothesis Goldbach consequence" 等，**未发现**任何把两者联系起来的公开讨论；Alpöge 的 4 页 remark（本地 `/home/kiler/rh-work/remark.txt`）全文 **0 次**出现 "Goldbach"/"additive"/"twin"（我们 grep 核对）。即：**目前没有人（包括作者）声称 Alpöge 的结果能推出本文的 S/R 或使 Goldbach 无条件。**
5. **【事实】Alpöge/Claude 证明覆盖范围**：MIT 验证页写明五个定理含 `DirichletLZerosOnLine`/`PrimitiveDirichletLZerosOnLine`，且 "GRH here means Dirichlet L-functions only"。这恰好覆盖本文 GRH(N)（p.3 定义），**不多不少**。注意其验证 caveat（lake comparator/Lean 导出重放仍在进行，见 §1 引用），这不是本报告的范围。

---

## 8. Alpöge/Claude 证明的架构与本文 S/R 的关系（事实 + 分析）

**【事实】** `/home/kiler/rh-full`（Alpöge Lean 证明的镜像）的目录结构关键词 grep：
- `heat kernel`: 仅出现在 `src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/HeatKernel*` 等与主链无直接关系的文件（且 `HeatKernel` 目录属于 Abelian variety/divisor 理论），**不是**"热核谱证明"架构；
- `Weil`: 大量命中 `WeilRepresentation`、`WeilGroupCharacters`、`SiegelWeilFiniteness`、`WeilIndicatorMeasures` 等 —— 是 **Weil 表示/theta 对应/Siegel–Weil 公式** 意义下的 Weil，不是 Weil 显式公式的 positivity；
- `ThetaLift`: `src/PositivityTheory/.../KFiniteThetaLifts/...`、`src/Development/AutomorphicArithmetic/ThetaCorrespondence/...` 等，与 Alpöge remark 里"$\sqrt X$ 长度的 theta 提升链"一致；
- `Stepanov`、`explicit formula`: grep 无核心命中（`ExplicitFormula` 只出现在 `Formalism/HermitianCurvature` 等长文件名的尾部子串中）；
- 顶层陈述：`src/Statements.lean` 只定义 `RiemannZetaZerosOnLine`、`DirichletLNonvanishingRightOfHalf`、`DirichletLZerosOnLine`、`PrimitiveDirichletLZerosOnLine`；`src/Main.lean` 从 `Supplements.Kernels.MainTheorems` 取 `everyCharacter` 等。
- 目录体量（README）：`Development/` 141,928 个 `.lean`、`Formalism/` 18,254、`GroundTheory/` 8,507、`ReciprocityTheory/` 3,845、`CompanionTheory/` 2,027、`PositivityTheory/` 449、`Lemmata/` 167；主题是自守形式、L 函数、theta 提升、正性、Hermitian 曲率等。

**【分析（推导/推测）】** 该证明的数学内容是**乘性**的（L 函数零点、自守表示、theta 提升、显式公式的零点计数），它证明的是 GRH（Dirichlet L，导子任意）。本文的 S/R 却是**加性**的：$T_N$ 的核是 $g_\chi=L'/L$ 的 Gram 型二次型，其某个特定向量 $v_N$ 的二次型等于 Goldbach 误差；S/R 要求的是**对所有 Hardy 检验函数一致**的一个算子范数界（等价于加性素数对相关量的一致性估计）。**Alpöge 证明中没有任何机制产生这种加性相关的一致上界**；即使有，也不来自"零点在临界线上"这类乘性信息（这正是经典困难：GRH 只给主项，minor-arc/奇偶性问题不因 RH 消失）。**因此："Alpöge ⇒ 无条件 Goldbach"不成立；正确说法是"Alpöge ⇒ 本文的 GRH(N) 被兑现，Goldbach 仍归结为 S/R"。** 这也与论文自己的 p.4 声明一致。

---

## 9. 对 Hypotheses S/R 的具体攻击（本任务核心）

### 9.1 攻击 R-1：三角不等式 / Hilbert–Schmidt 范数

**【推导】** 已知（论文 Theorem 6.2）$\|T_N\|\le\|T_N\|_{HS}\ll(\log N)^2$；R 需 $\|T_N\|\le\delta_N$。差距 (GAP-R) $=\sqrt{N/\mathbb S}(\log N)^{1/2}$，随 $N$ 指数增长。**失败原因不是估计粗糙，而是结构性的**：$P_N$ 是正算子、$\operatorname{tr}P_N\asymp(\log N)^2$，且 $D_N$ 也为正、$\operatorname{tr}D_N\asymp(\log N)^2$，$K_N$ 的 HS 范数 $\asymp(\log N)^2$；三个分量各自的"平凡大小"都是 $(\log N)^2$。任何只用 $\|\cdot\|_{HS}$ 的路线无法低于 $(\log N)^2$。**结论：三角不等式路线走不通；必须用 $P_N$ 与 $D_N+K_N$ 之间的相消。**

### 9.2 攻击 R-2：复制核点值下界（能否证伪 R？）——**这是我们最实质的尝试**

**【推导】** 用 (5.8)：对 $S_N$ 内任意 $s,z$，
$$\|T_N\|\ge\frac{8\sqrt{d_N(s)d_N(z)}\,|E_N(s,\bar z)|}{|1+s||1+z|}.$$
取 $z=s=\sigma+i\gamma$，其中 $\rho=1/2+i\gamma$ 是某个奇特征 $\chi_0$（导子 $d\mid N$）的非平凡零点，重数 $m$，并取 $\sigma=2\alpha_N$（此时 $d_N(s)=\min(\sigma-\alpha_N,\beta-\sigma)=\alpha_N$，因 $2\alpha_N<\beta$ 对充分大 $N$）。在 $s$ 处：
- $g_{\chi_0}(s)$ 有极点 $1/(s-i\gamma)$，故 $|g_{\chi_0}(s)|^2=\frac{m^2}{\sigma^2}+O(1/\sigma)$；
- 其他 $\chi$ 与 $D_N,K_N$ 在 $\Im s=\gamma$ 附近解析或按 Appendix A.4 展开：$D_N(2\sigma)=\frac1{4\sigma^2}+O_N(1)$，$K_N(s,\bar s)=-\frac1{4\sigma^2}+O_{N,\gamma}(1/\sigma)$；
故
$$E_N(s,\bar s)=P_N(s,\bar s)-D_N(2\sigma)-K_N(s,\bar s)=\frac{2m^2}{\varphi(N)\sigma^2}+O_{N,\gamma}\Bigl(\frac1\sigma\Bigr),$$
取主项（$\sigma=2/\log N\to0$，主项 $\asymp\frac{m^2\log^2N}{\varphi(N)}$ 最终会压过误差，因误差含 $O_N$ 常数；严格化需对 $N$ 取大，此处作**推导性**估计），得
$$\|T_N\|\ \ge\ \frac{8\alpha_N\cdot\frac{2m^2}{\varphi(N)\cdot4\alpha_N^2}}{1+\gamma^2}\cdot\frac{1}{1+o(1)}
=\frac{4m^2\log N}{\varphi(N)(1+\gamma^2)}(1+o(1)).\tag{LB}$$
对固定零点（如 $3\mid N$ 时 $\chi\bmod3$ 的首个零点 $\gamma\approx8.04$，或任意 $N>2$ 的某个奇特征的首个零点，$\gamma\ll\log(\operatorname{cond})$），$m\ge1$。因此
$$\|T_N\|\ \gtrsim\ \frac{4\log N}{\varphi(N)(1+\gamma^2)} .$$
**【推导】与 $\delta_N$ 比较**：$\frac{\text{(LB)}}{\delta_N}\lesssim\frac{4\log N}{\varphi(N)(1+\gamma^2)}\cdot\frac{\sqrt{N/\mathbb S}}{\log^{3/2}N}=\frac{4\sqrt N}{\varphi(N)(1+\gamma^2)\sqrt{\mathbb S}\sqrt{\log N}}$。用标准下界 $\frac{N}{\varphi(N)}\le e^\gamma\log\log N+O(1/\log\log N)$（Rosser–Schoenfeld 型，$N\ge3$），即 $\varphi(N)\ge\frac{N}{e^\gamma\log\log N}$，得
$$\frac{\text{(LB)}}{\delta_N}\le\frac{4e^\gamma\log\log N}{\sqrt{\log N}\sqrt{\mathbb S}\,\sqrt N}\cdot\frac{1}{1+\gamma^2}\longrightarrow0 .$$
**结论（重要）**：单点复制核下界最多给出 $\sim\frac{\log N}{\varphi(N)}$ 量级，**永远小于 $\delta_N$**，所以这条路线既不能证明 R，也**不能证伪 R**。同时这揭示了 R 的"宽松度"：R 允许 $\|T_N\|$ 在 $[\frac{4\log N}{\varphi(N)(1+\gamma^2)},\,\delta_N]$ 之间；由于 $\frac{\log N}{\varphi(N)}\ll\delta_N$，R 不被零点奇异性自动违反。

**【事实】附注（论文 Appendix A.4）**：论文用同一机制证明**固定 $N$、$c\downarrow0$** 时 $c\|T_{N,c}\|\ge\frac{2C_{N,\gamma}\log N}{1+\gamma^2}>0$，即 R(N,c) 对足够小的 $c$ 失效（p.55）：这说明 S/R 对条带参数极为敏感，主文取 $c=1$ 是靠 §6.5 的"平衡"（$\alpha\asymp1/\log N$）选出的；这一附录反而是论文**诚实性**的证据（作者知道自己不能声称 R 与 c 无关）。我们对 A.4 的 Laurent 展开逐项复核无误。

### 9.3 攻击 S-1：均方/迹估计路线

**【推导】** S 要求 $\|T_N\|\le\frac{\mathbb S}{2h\sqrt{1-\eta_N}}\approx\frac{\mathbb S}{2h}$。S 所需宽度 $\eta_N$ 相对 GRH 宽度的放大倍数 $h^2(\log N)^4/\mathbb S^2$ 是巨大的；而 $\operatorname{tr}P_N\asymp(\log N)^2\gg\mathbb S$。由于 $P_N\ge0$（算子意义下正），
$$\|T_N\|=\|P_N-(D_N+K_N)\|\ge \|P_N\|-\|D_N+K_N\|,$$
但 $\|D_N+K_N\|$ 未知；仅由迹估计无法得到 $\|T_N\|$ 的上界低于 $(\log N)^2$。若想用"特征平均"改进，本质是要证明 $P_N$ 的谱在扣除 $D_N+K_N$ 后大幅塌缩——这就是 S/R 的内容本身。**路线失败位置：论文 (6.9) 的均方界已经是"Character average"能达到的最优量级 $\asymp(\log N)^2$（与迹同阶），无法跨过 $(\log N)^2\to\mathbb S/(2h)$ 的鸿沟。**

### 9.4 攻击 S/R-2：借用 Alpöge/Weil 型正性技术

**【分析】** 我们考察了三种可能的迁移：
1. **Weil 显式公式 positivity**：RH ⇔ $\sum_\rho \hat f(\rho)\ge0$ 型正性（Weil 判据），其证明对象是 $\zeta$ 的显式公式。本文的 $T_N$ 的二次型在 $v_N$ 处**精确等于** Goldbach 加权误差（这是论文的核心恒等式），若要从中推出正性/上界，正需要一个**关于素数对的显式公式**（Hardy–Littlewood 型的加性版本），而 Weil 显式公式的检验函数是**乘性**的（$\sum_n\Lambda(n)f(n)$ 型，涉及单个素数的分布），不含 $p+q=N$ 的加性约束。**不相容。**
2. **theta 提升链/自守正性**：Alpöge 证明的"$\sqrt X$ 链"是为了在 $\mathbb Z$ 上模拟 Stepanov 的重数论证以控制 L 零点，其结论是乘性 L 函数的零点位置；本文 S/R 是 $T_N$ 的算子范数，$T_N$ 的核由 $L'/L$ 的**平方/相关系**构成，其特征值对应加性相关矩阵的谱。**无已知机制把零点位置信息升级为加性相关的一致上界。**
3. **Hermitian 曲率/正性理论**：Alpöge 仓库中的 `HermitianCurvature`、`PositivityTheory` 是自守表示/周期积分语境下的正性（Weil 表示、theta 对应），不是"某个算子的 HS 范数上界"的现成工具。**结论：借用失败；论文的 S/R 与 Alpöge 的技术栈之间不存在已知桥梁。**

### 9.5 攻击 S/R-3：圆法/配对相关/显式公式的等价翻译

**【推导】** 把 S/R 翻译成关于素数对相关量的陈述。由 §2.6，$T_N$ 的边界核为
$$\frac{E_N(s,\bar z)}{(1+s)(1+\bar z)},\qquad E_N=P_N-D_N-K_N,$$
且 $P_N(s,\bar z)=\frac2{\varphi(N)}\sum_{\chi}g_\chi(s)g_{\bar\chi}(\bar z)$。对任意 $h\in H_N$（用 Fourier–Laplace 密度 $\psi$ 参数化，$h=U_H\psi$，$\|h\|^2=\int|\psi|^2(e^{2\alpha_N\tau}+e^{2\beta\tau})d\tau$），二次型 $\langle T_Nh,h\rangle$ 是 $E_N$ 的一个二重（加权）Mellin–Fourier 变换；逐项展开后，$P_N$ 项给出形如
$$\frac2{\varphi(N)}\sum_{\chi\in X_N^-}\iint \bigl(\text{对 }g_\chi\text{ 的线性泛函}\bigr)\bigl(\text{对 }g_{\bar\chi}\text{ 的共轭线性泛函}\bigr)$$
的**特征平均的二阶量**，$D_N$、$K_N$ 项给出对角/模型的显式项。因此
$$\boxed{R:\ \sup_{0\ne h\in H_N}\frac{|\langle T_Nh,h\rangle|}{\|h\|^2}\le\delta_N}$$
是一个**对所有检验函数一致的加权素数对相关量的上界**，其强度相当于 Hardy–Littlewood 渐近式的"统一误差版本"（对所有光滑权一致），属于圆法 minor-arc/奇偶性问题所在的困难层级（S 是它的一个较弱版本：右端 $\mathbb S/(2h\sqrt{1-\eta_N})$）。**已知工具（GRH + 大筛法）只能给 $(\log N)^2$ 型均方界；要到达 $\delta_N$ 或 $\mathbb S/(2h)$，需要新的一致的加性素数对相消输入。**

### 9.6 若要证明 S/R，最低限度需要什么？（可检验的精确表述）

1. **R 的充分条件（形式化）**：存在绝对常数/显式函数，使对每个满足 GRH(N) 的充分大偶数 $N$，
   $$\sup_{h\in H_N,\ \|h\|=1}\Bigl|\frac1{(2\pi)^2}\iint \bar\Phi\text{-变换后的 }E_N\text{ 核}\Big|\le\delta_N .$$
   最弱的可攻击形式：证明 $P_N$ 的"近临界线尖峰"与 $D_N+K_N$ 在算子意义下相消到 $\delta_N$ 量级；这等价于一个**加性素数对相关量的 uniform Hardy–Littlewood 定理**（对一类光滑权）。
2. **S 的充分条件**：同上，但右端换成 $\mathbb S/(2h(N)\sqrt{1-\eta_N})$，即仅需 $h\to\infty$ 的"任意慢"改进；这仍需要相消，只是量级要求比 R 弱 $\sqrt{N/\mathbb S}(\log N)^{1/2}\cdot\frac{\mathbb S}{2h\delta_N}\cdot$ 倍（即 S 比 R 弱约 $\sqrt{N\mathbb S}/(h(\log N)^{3/2})$ 倍）。
3. **不建议的路线**：任何仅用 $\|T_N\|_{HS}$、$\operatorname{tr}P_N$、逐点值、或逐项绝对值估计的路线，已被量级证据排除（§9.1、§9.3、§9.2）。
4. **可做的计算实验（我们未能完成，建议 lead 考虑后续）**：对中等 $N$（如 $N=30030$ 已有、或 $N=510510$）用更高精度/更大截断去做 Galerkin 离散，估计 $\|T_N\|/\delta_N$；但要注意截断误差无界（论文 p.62 自承），只能作启发式证据，不能证明。我们在本任务内完成了 $N=30030$ 的**计数**独立复核（905），但没有复现其 2562 维谱模型（需要其 L 值计算流水线，时间不允许）。

### 9.7 启发式：R 是否可能为真？（推测）

**【推测】** 若把"加权 Goldbach 误差"看作随机涨落：
- 加权计数主项 $c_\phi\mathbb S\sim\mathbb S$；
- 有效素数对个数 $\asymp\mathbb S N/(\log N)^2$，随机模型的相对涨落 $\asymp1/\sqrt{\#\text{pairs}}=(\log N)/\sqrt{\mathbb S N}$；
- R 断言相对误差 $\asymp\delta_N/\mathbb S=(\log N)^{3/2}/\sqrt{\mathbb S N}=\sqrt{\log N}\cdot(\log N)/\sqrt{\mathbb S N}$，即**只比随机涨落大 $\sqrt{\log N}$ 倍**。
因此 R 不是"离谱地强"：它与 Hardy–Littlewood 型随机涨落在同一量级（仅差 $\sqrt{\log N}$），并且比"最优平方根相消"（误差 $\sqrt{\#\text{pairs}}\cdot(\log N)^2/N\approx\sqrt{\mathbb S/N}\log N$）宽松。加上 Appendix B 的有限模型在 $N=30030$ 给出最大特征值 $0.357<0.432=\delta_N$，**R 在数值上看起来是可信的**。但"可信"不等于"可证"：证明 R 需要控制算子范数到 $\delta_N$，这是一个全新的、非乘性的解析数论问题；它是本文真正的未解决核心，也是本文没有把 Goldbach"变简单"的原因。

---

## 10. 判定

### 10.1 关于论文本身

- **【事实】本文是一个诚实的条件性结果**：摘要、§1.2、§8 都明确说明需要 GRH **加上** S 或 R；§2.4.3 明确说 GRH 单独不够；§8 甚至说"We do not know whether sufficiently ingenious refinements of sieve methods or the circle method can yield the Goldbach asymptotic formula. The present difficulties do not warrant excluding this possibility."（p.52）。
- **【推导】在"GRH + S/R"前提下，Theorem 1.1/1.2 的推导链是自洽的**：我们独立重推了零–范数字典、Beta 模型恒等式、二次型恒等式、$Q_N\ll1$、素数对下界；未发现致命错误。唯一"高风险"部分是 Lemma 6.4 的绝对一致性（技术性强、未完全逐常数核验），但它属于标准调和分析/围道移动技术，方向上没有错误迹象。
- **【事实+推导】它不是 GRH ⇒ Goldbach**：从 (2.24) 到 $\delta_N$ 的差距是 $\sqrt{N/\mathbb S}(\log N)^{1/2}$（R）或 $\asymp(\log N)^2/\mathbb S$（S）；没有任何已知定理能跨越。

### 10.2 关于 S/R 的可证性/真伪

- **【推导】不可能由 GRH 单独推出**（否则论文的 (2.24) 就不是最好结果——但更准确说：**没有证据**表明 GRH 蕴含 S/R；且 S/R 的强弱远超 GRH 的常规推论；若 S/R 可由 GRH 推出，则 Goldbach 就被 GRH 证明，这与"GRH 不蕴含 Goldbach"的普遍认知矛盾——尽管后者不是定理，但是本领域的强共识）。
- **【推导】S/R 不是空洞的**：R ⇔ $\|T_N\|\le\delta_N$ 是一个精确、可数值检验的命题；Appendix A.4 显示它们对条带参数敏感、**不能**由任意 $c$ 的算子族自动满足；S 依 $h$ 强弱变化。
- **【推测】S/R 大概率为真（至少不被已知下界违反）**：我们没有找到任何证伪它们的途径（§9.2 的下界远低于 $\delta_N$；数值模型支持）；但这属于"强猜想"，其证明需要新的加性素数对相消定理。
- **【推测】S/R 的证明难度与 Hardy–Littlewood 猜想同量级**：R ⇒ 加权 HL 渐近式（强误差）；反向不成立（算子范数比单个二次型强），所以 S/R 严格强于"加权 Goldbach 渐近"这一结论本身。**因此本文并没有把 Goldbach 归约到"更简单"的问题；它把难度重新编码到一个显式的算子范数命题里。**

### 10.3 对"用 Alpöge 的 RH 结果 + 本文 ⇒ Goldbach"的回答

**【事实】** Alpöge/Claude 结果 = RH + GRH（Dirichlet L，任意导子）的形式化证明（验证状态见 §1 caveat）。**【事实】** 本文的 GRH(N) 假设因此被兑现。**【事实】** 但本文还需要 S 或 R，而 Alpöge 的证明不提供任何关于 $T_N$ 算子范数的信息。**【推导+推测】** 因此：
$$\text{Alpöge 的 RH/GRH}+\text{Li–Liu}\ \not\Rightarrow\ \text{Goldbach}\quad(\text{至少目前没有逻辑通道}),$$
除非另外证明 S 或 R。**这是本任务最重要的负面结论，也是给用户的诚实回答：哥德巴赫猜想没有被这条路线"解决"；Li–Liu 把问题精确地归结为一个新的、未证明的谱假设；Alpöge 的 GRH 证明只是兑现了其中较容易的一半。**

---

## 11. 复现命令与脚本

- PDF 页渲染（核对公式）：`python3 -c "import pymupdf; d=pymupdf.open('/home/kiler/rh-work/liu-goldbach.pdf'); d[p].get_pixmap(dpi=180).save(...)"`（用到的页：3、10、11、34、35、50、60）。
- $N=30030$ 独立复算（本报告 §6.3）：

```python
N = 30030
sieve = bytearray([1])*(N+1); sieve[0]=sieve[1]=0
for i in range(2,int(N**0.5)+1):
    if sieve[i]: sieve[i*i::i]=bytearray(len(sieve[i*i::i]))
primes=[i for i in range(2,N+1) if sieve[i]]; ps=set(primes)
cnt=sum(1 for p in primes if p<=N//2 and (N-p) in ps)   # -> 905 (unordered)
# S(N) = 2*C2 * prod_{p|N} (p-1)/(p-2), C2 = 0.6601618158468696...
# -> S = 5.1212553287, delta = sqrt(S/N)*log(N)**1.5 = 0.432310240854...
```

- 可复制的数值：`delta_N` vs `(logN)^2` 差距见 §4.2 表（脚本：`(log(N)**2)/((S/N)**0.5*log(N)**1.5)`，取 $S=1.3203236$）。
- 本地 MIT 验证快照：`/home/kiler/rh-work/mit/grh_page_now.html`、`now_audit.log`、`now_comparator.json`。
- Alpöge 架构 grep：`grep -ril "ThetaLift\|WeilRepresentation\|HeatKernel" /home/kiler/rh-full/src`（详见 §8）。

---

## 12. 引用与链接

- 论文（官方）：[MRC English announcement](https://mrc.sdu.edu.cn/english/info/1018/1514.htm)；[MRC 中文公告](http://mrc.sdu.edu.cn/info/1018/2193.htm)；本地 PDF `/home/kiler/rh-work/liu-goldbach.pdf`（63 页）。
- Alpöge 公告与验证：[alpo.ge/remark.pdf](https://alpo.ge/remark.pdf)；[MIT verification page](https://math.mit.edu/~drew/grh/)（本地快照 `/home/kiler/rh-work/mit/`）。
- 作者前作：(1+1.9) 定理，[arXiv:2606.05224](https://browse-export.arxiv.org/abs/2606.05224)。
- 二手报道（仅供参考，无技术审稿价值）：[数学中国转帖 2069463](http://www.mathchina.com/bbs/forum.php?mod=viewthread&tid=2069463)；[数学中国转帖 2069475](http://www.mathchina.com/bbs/forum.php?mod=viewthread&tid=2069475)；[知乎问题](https://www.zhihu.com/question/2104680319357907490)；[今日头条](https://m.toutiao.com/article/7708062452621099560/)。
- 背景（GRH 与 Goldbach 关系的公认表述）：论文 §1.1 p.2 自己写道 "No proof of the binary conjecture is known under the generalized Riemann Hypothesis (GRH) alone, even when GRH is assumed for all Dirichlet L-functions." —— 这句话本身就否定了"GRH ⇒ Goldbach"。

---

## 附录 A：本报告用到的关键原文摘录（逐字，PDF 页码）

1. **p.3, GRH(N)**："*Every nontrivial zero of every primitive Dirichlet L-function whose conductor divides N has real part 1/2.*"
2. **p.4, Hypothesis S / R**：见 §2.7（原文见 §12 论文 PDF）。
3. **p.4（GRH 不够）**："In fact, GRH alone already gives a zero-free region for XN of the same form. Its width, however, falls short of that required by Hypothesis S, so the resulting estimate is not strong enough to make the Goldbach error o(S(N))."
4. **p.11, 零–范数字典**："Taking the supremum therefore gives the exact dictionary  XN(q) ≠ 0 (ℜq > 1 − η) ⟺ ‖TN‖ ⩽ δN/(2√(η(1 − η)))."
5. **p.12, GRH 基线**："(2.24) ‖TN‖ ⩽ ‖TN‖HS ≪ (log N)2 … This available norm bound is too large to make the Goldbach error smaller than its main term; S and R impose the required improvement."
6. **p.12（无相消）**："The character average controls the first component, positivity controls the diagonal, and the continued Beta formula controls the model. Their separate estimates each have size O((log N)2) at αN = 1/log N; they do not measure cancellation between the components."
7. **p.50, Theorem 7.1**："(7.17) r(N) = ⟨TNvN, vN⟩,  |r(N)| ⩽ QN‖TN‖ ≪φ ‖TN‖."
8. **p.52（作者不排除其他路线）**："We do not know whether sufficiently ingenious refinements of sieve methods or the circle method can yield the Goldbach asymptotic formula. The present difficulties do not warrant excluding this possibility."
9. **p.62（数值模型不认证 R）**："Cutoff stability and pointwise high-precision checks do not bound the full operator's truncation or discretization error. The figures illustrate the finite spectral model; they do not certify Hypothesis R for T30030,1."
10. **p.2（GRH 单独不够，作者原话）**："No proof of the binary conjecture is known under the generalized Riemann Hypothesis (GRH) alone, even when GRH is assumed for all Dirichlet L-functions."

---

## 附录 B：审计覆盖度声明

- 已逐式核对：§1.2–§2.5（主文逻辑链）、§3–§7 的主要引理陈述与关键推导、Appendix A.1–A.4、Appendix B.1–B.4 的数值结论。
- 未逐常数重算：Lemma 6.4 的全部隐含常数（但结构/方向已核）；Lemma 7.2 的 Fubini 主导函数逐项（已核结构）；Appendix B 的 2562 维谱模型（未复现，需其 L 值计算流水线）。
- 未做：对疑似错误的穷尽式搜索（例如把 Lemma 6.4 的每个 $\ll$ 重写为显式常数）——若后续要沿本文路线做实质推进，建议优先做这一项；我们判断它不会推翻论文，但会决定"足够大 N"的界是否原则可计算。
