# Phase-11 Part A：GWX 定理 1.1 的最小充分假设 H_Ratios^min

> 作者：liu-auditor（task-37，2026-11-21/22）。本文件只写 phase11/theory；未读 kernel-theorist 的 Route C 笔记（保持独立性）。
> 依据：phase-8 审计 `phase8/audit/gwx-audit.md`、Gou–Wang–Xu arXiv:2611.18825v1 全文（本地 `phase7/lit/gwx_pdf.txt`、`gwx.txt`）、phase-10 报告（若存在）。标注：**[事实]**=论文原文/定义；**[推导]**=本报告论证；**[推测]**=判断。
> 另：本文件 §5 专门回答 Lead 的 follow-up 疑问（cxy0714 2026-11-16 的"close reading"称 parity-twist 平均不是标准 RC_D 的直接推论、需要 Hypothesis 1.1 未明确写出的额外一致性假设）。

---

## 0. 结论速览

1. **[推导] H_Ratios^min（最终推荐版，boxed）**：存在固定 $0<\omega_D\le1/2$、$\eta_0>0$、$B\ge0$，使得对每个 $0<\eta<\eta_0$、每个 $\varepsilon>0$、每个整数 $q>1$ 且 $\varphi^*(q)>0$（复合导子允许），
   $$\boxed{\ \sum_{\chi\bmod q}^{*}\frac{L(a,\chi)L(b,\bar\chi)}{L(s,\chi)L(t,\bar\chi)}=\mathcal M_q(a,b;s,t)+O_{\eta,\varepsilon}\bigl(q^{1-\omega_D+\varepsilon}(1+T)^B\bigr)\ }$$
   一致于 $\Re a=\Re b=\frac12$、$\Re s=\Re t=\frac12+\eta$、$T:=\max\{|\Im a|,|\Im b|,|\Im s|,|\Im t|\}\le 100\log(2q)$；其中 $\mathcal M_q=\varphi^*(q)Z_q+H_qZ_q(1-b,1-a;s,t)$ 是 §1.2 的精确两项主项（parity-resolved），$Z_q,H_q$ 见 §1.2；误差在分子移位 $a,b$ 的固定半径圆盘上全纯。
   **加上 GRH**（所有 primitive Dirichlet L 与 ζ），即得 GWX Theorem 1.1：
   $$\sum_{m+n=N}\Lambda(m)\Lambda(n)=N\mathfrak S(N)+O_\varepsilon(N^{1-\omega_D+\varepsilon})\quad(\forall\varepsilon>0,\ \text{所有充分大偶数 }N).$$
   **任何固定 $\omega_D>0$ 足够**；若要 $\omega_D=1/2$ 得 $O(N^{1/2+\varepsilon})$。
2. **[推导] 六项 weakening 的结论**（详见 §4 表）：
   - (i) **不需要**比"所有 $q$ 逐点"更弱：任何 $\varphi^*(q)>0$ 的 $q$ 都会作为某个偶数 $N$ 的 primitive conductor 出现（$q$ odd⇒$N=2q$；$4\mid q$⇒$N=q$），所以逐点 in $q$ 已是本质最小；但可以去掉 $v_2(q)=1$ 的情况（见 (vi)）。
   - (ii) **可以**把"逐点 + 误差全纯"弱化为"分子移位 $(u,v)$ 盘上的 $L^2$ 平均界"：GWX 的 §3.6 三线插值只需要临界线上的逐点界（boundary $\Re\xi=0$）+ GRH（boundary $\Re\xi=1/8$）；而 §3.2/§3.5 的 Cauchy 求导可由 $F_q=q^{-1}(R_q-\mathcal M_q)$ 自身的全纯性与盘上 $L^2$ 界（mean-value/Cauchy）推出。**不需要 H1.1 在圆盘内部逐点值。**
   - (iii) **$\omega_D(q)$ 随 $q$ 变、只要 $\omega_D(q)\log q\to\infty$ 且单调（或对 $q\mid N$ 有 $\omega_D(q)\ge\omega_D(N)/2$）就够——但只够定性 Goldbach（误差 $o(N)$）**；要得到固定幂次 saving $N^{1-\omega_D+\varepsilon}$ 必须固定 $\omega_D>0$。且"可数多个 $\eta$ 各自常数 $O_{\eta,\varepsilon}$"的表述本身**不足以**令 $\eta=\eta(N)\to0$；需要额外的一致性条款 **H_UNIF**：$O_{\eta,\varepsilon}\le C(\varepsilon)\eta^{-A}$（例如 $\le e^{A/\varepsilon}\eta^{-A}$；任何多项式/次指数控制都够）。这是 (iii) 的真正限制（详见 §4.3）。
   - (iv) 实际所需 T 范围只有 $T\le(10+o(1))\log(2q)$（Lemma 3.1 中 $|\Im s|,|\Im t|\le10\log2q$；三线插值矩形边界 $\Im\xi\le80\log2q$ 需要 numerator height $\le90\log2q$），**100 是宽松的**；可以换成 $T\le(10+10^{-2})\log(2q)$（或保留 100 无害）。
   - (v) **精确 parity 主项 $\mathcal M_q$ 不能完全换成 $\varphi^*/2$ 近似**：主项差别 $O(q^\varepsilon)$ 虽在误差 $q^{1-\omega_D+\varepsilon}$ 之内（$\omega_D\le1$），但 $\varphi^*/2$ 近似可能破坏 $F_q$ 在 $a+b=1$ 的可去奇点/全纯性（§4.5）；保留精确 $\mathcal M_q$ 是安全的极小形式。若愿意加一条"近似主项给出的 $F_q$ 全纯"假设，则可用 $\varphi^*/2$ 版本（[推测]）。
   - (vi) $v_2(q)=1$（q≡2 mod 4）时 primitive character 个数 $\varphi^*(q)=0$（因为 $(\mathbb Z/2m)^*\cong(\mathbb Z/m)^*$，odd m ⇒ 每个特征都由 m 诱导，conductor 不可能是 $2m$），Hypothesis 1.1 的求和为空、主项为零——**纯 vacuous，可以删去该 clause**。这也影响 $N\equiv2\bmod4$ 时最大的有效 $q$ 只有 $N/2$ 量级。
3. **[推导] 对 cxy0714 疑问的裁决：所给 Hypothesis 1.1 + GRH 足够，无需任何额外一致性条款；该 doubt 不成立。** §5 逐步给出 (3.25)/(3.26) 三线插值与 (3.12) 轮廓移动所需的全部估计，指出 100 的 margin 恰好覆盖三线矩形边界（$\le90\log2q$），$|e^{\xi^2}|=e^{-(\Im\xi)^2}$ 只用于吸收 $|T|>100\log$ 的尾巴（那里用 GRH 的 $q^2(1+|T|)^D$ strip 界），误差全纯性可直接从 $R_q-\mathcal M_q$ 得到。**真正的"额外输入"不是 uniformity，而是复合导子的精确 parity 主项 $\mathcal M_q$ 这一非标准形式——但它已明确写在 Hypothesis 1.1 中（phase-8 发现）。**
4. **[推导] 最终推荐写进 H_Ratios^min 的文字**（§3）：固定 $\omega_D$ 的 boxed 版本 + 明确指出"复合导子精确 parity 主项"是非标准但显式的假设；如果要定性版本，则加 H_UNIF 并使用 $\omega_D(q)\log q\to\infty$。

---

## 1. 记号与 GWX 的主项（[事实]）

- 对 primitive χ mod q，$\chi(-1)=(-1)^e$。令
  $$X_{q,e}(w)=\Bigl(\frac{q}{\pi}\Bigr)^{1/2-w}\frac{\Gamma((1-w+e)/2)}{\Gamma((w+e)/2)},\quad h_e=X_{q,e}(1-b)X_{q,e}(1-a),$$
  $M_e(q)=\#\{\text{primitive }\chi\bmod q:\chi(-1)=(-1)^e\}$，$\varphi^*(q)=M_0(q)+M_1(q)$。
- $Z_q(a,b;c,d)=\dfrac{\zeta_q(a+b)\zeta_q(c+d)}{\zeta_q(a+d)\zeta_q(b+c)}A_q(a,b;c,d)$，$\zeta_q(s)=\zeta(s)\prod_{p\mid q}(1-p^{-s})$，
  $A_q=\prod_{p\nmid q}\frac{(1-p^{-c-d})(1-p^{-a-d}-p^{-b-c}+p^{-c-d})}{(1-p^{-a-d})(1-p^{-b-c})}$。
- **GWX 主项**（§3.6, pp.18–19）：$\mathcal M_q(a,b;s,t):=\varphi^*(q)Z_q(a,b;s,t)+H_q(a,b)Z_q(1-b,1-a;s,t)$，
  $H_q(a,b)=\sum_{e=0,1}M_e(q)X_{q,e}(a)X_{q,e}(b)$。
- GWX Hypothesis 1.1 原文（p.2，HTML 抽取确认共轭横线）：
  > "Hypothesis 1.1 (Ratios of primitive Dirichlet L-functions ($\mathrm{RC}_D(\omega_D)$)). Fix $0<\omega_D\le1/2$. There exist constants $\eta_0>0$ and $B\ge0$ such that for every fixed $0<\eta<\eta_0$ and every $\varepsilon>0$,
  > $\sum_{\chi\bmod q}^{*}\frac{L(a,\chi)L(b,\bar\chi)}{L(s,\chi)L(t,\bar\chi)}=\mathcal M_q(a,b;s,t)+O_{\eta,\varepsilon}\bigl(q^{1-\omega_D+\varepsilon}(1+T)^B\bigr)$,
  > uniformly for all conductors $q>1$, including composite conductors, and all shifts satisfying $\Re a=\Re b=\frac12$, $\Re s=\Re t=\frac12+\eta$, $T=\max\{|\Im a|,|\Im b|,|\Im s|,|\Im t|\}\le100\log(2q)$."
  > 紧接前文（p.2）：“...On the indicated disks, the errors are holomorphic in the numerator shifts.”
- **Theorem 1.1**（p.3）：GRH for Dirichlet L + RC_D(ω_D) ⇒ 对每个 ε>0 与每个偶数 N，
  $\sum_{m+n=N}\Lambda(m)\Lambda(n)=N\mathfrak S(N)+O_\varepsilon(N^{1-\omega_D+\varepsilon})$；(1.3)。

---

## 2. H_Ratios^min 的推荐形式

### 2.1 版本 A（power-saving 版，推荐作为"最小充分假设"的干净形式）

> **H_Ratios^min（固定 saving 版）**。存在常数 $0<\omega_D\le1/2$、$\eta_0>0$、$B\ge0$，使得对每个 $0<\eta<\eta_0$、每个 $\varepsilon>0$、每个整数 $q>1$ 且 $\varphi^*(q)>0$（允许复合导子），
> $$\sum_{\chi\bmod q}^{*}\frac{L(a,\chi)L(b,\bar\chi)}{L(s,\chi)L(t,\bar\chi)}
> =\mathcal M_q(a,b;s,t)+O_{\eta,\varepsilon}\bigl(q^{1-\omega_D+\varepsilon}(1+T)^B\bigr),$$
> 对所有满足 $\Re a=\Re b=1/2$、$\Re s=\Re t=1/2+\eta$、$T=\max\{|\Im a|,|\Im b|,|\Im s|,|\Im t|\}\le100\log(2q)$ 的复移位一致成立；且误差 $E_q:=R_q-\mathcal M_q$ 在分子移位 $a,b$ 的固定半径圆盘上全纯。主项 $\mathcal M_q$ 如 §1 所示（精确 parity-resolved 两项）。
> **额外独立假设：GRH**（所有 primitive Dirichlet L 与 ζ）。

**定理**：H_Ratios^min + GRH ⇒ GWX Theorem 1.1（见 §2.2 的推导映射）。实际上，**$O_{\eta,\varepsilon}(\cdot)$ 的常数只需对每个固定 η 存在**；证明最终取一个固定的小 η（由 $\omega_D,\varepsilon$ 决定），不需要 η-一致性。

### 2.2 从 H_Ratios^min 到 Theorem 1.1 的推导映射（[推导]，逐步对应 GWX）

1. **字符展开**（GWX (3.1)，p.12）：对 $(mn,N)=1$，$1_{N\mid m+n}=\varphi(N)^{-1}\sum_{\chi\bmod N}\chi(-1)\chi(m)\bar\chi(n)$。
2. **parity twist**（GWX (3.3)–(3.4)，p.13）：令 $R_q,R^\vee,h_e$ 如 §1；由两个功能方程得 $L(1-b,\chi)L(1-a,\bar\chi)=h_eL(a,\chi)L(b,\bar\chi)$（根数 $\varepsilon(\chi)\varepsilon(\bar\chi)=1$），故
   $$\sum^*_{\chi\bmod q}\chi(-1)\frac{L(a,\chi)L(b,\bar\chi)}{L(s,\chi)L(t,\bar\chi)}=\frac{2R_q(1-b,1-a;s,t)-(h_0+h_1)R_q(a,b;s,t)}{h_0-h_1}.$$
   **这一步不需要任何 Ratios 假设**（纯功能方程 + 代数）。
3. **Lemma 3.1 插值**（GWX §3.6, pp.18–19）：在 GRH 与 H_Ratios^min 下对 $F_q(a,b)=q^{-1}(R_q-\mathcal M_q)$ 在三线矩形 $0\le\Re\xi\le1/8$、$|\Im\xi|\le80\log(2q)$ 上做三线插值：
   - boundary $\Re\xi=0$：分子在临界线，H_Ratios^min 直接给出 $|F_q|\ll q^{-\omega_D+\varepsilon}(1+T)^B$，其中 $T\le10\log(2q)+80\log(2q)+O(1)<100\log(2q)$（细节 §5）；
   - boundary $\Re\xi=1/8$：GRH 给 $|F_q|\ll q^{2+\varepsilon}(1+|T|)^D$（GWX (3.25)）；
   - 垂直边/无穷尾巴：$|e^{\xi^2}|=e^{-(\Im\xi)^2}$ 吸收，$|T|>100\log2q$ 的尾部用 GRH strip 界。
   得 $|F_q|\ll q^{-\omega_D+8(\eta+r)(2+\omega_D)+\varepsilon}$（(3.26)），取 $\omega=\omega_D-8(\eta+r)(2+\omega_D)>2\eta$ 得 **(3.2)**：
   $$R_q(a,b;s,t)=\varphi^*(q)Z_q+H_qZ_q(1-b,1-a;s,t)+O(q^{1-\omega+\varepsilon}(1+|\Im s|+|\Im t|)^B),$$
   对 $(a,b)=(s+u,t+v)$ 与 $(1-t-v,1-s-u)$ 都成立，误差在 $u,v$ 盘上全纯。**所用 Ratios 输入仅是 H_Ratios^min 在临界线 $\Re a=\Re b=1/2$ 上的点值界；其余由 GRH + 三线插值给出。**（这是 §5 详证的要点，也是 cxy0714 doubt 的答案。）
4. **有理权与集成误差**（GWX §3.2–3.3）：用 (3.5) 的 $f_j$ 的 Gamma 衰减压住 $(h_0+h_1)/(h_0-h_1)$ 的指数增长，Cauchy 求导后用 (3.7) 得每个 q 的集成误差 $O(q^{1-\omega+\varepsilon})$（(3.8)）。此步只用 (3.2) 的误差全纯性/盘上界，**不需要 H_Ratios^min 的额外 clause**。
5. **加权和 (3.12)**：$W(u,v)$ 满足增长/衰减条件时，
   $$N^{-\lambda-\mu}\sum_{N\mid m+n}\Lambda\Lambda\,W=N^{1-\lambda-\mu}\sum_{k\ge1}S(kN)F(k)+O_\varepsilon(N^{1-\omega+2\eta+\varepsilon}),\tag{3.12}$$
   其中 $F(x)=\int_0^xW(u,x-u)du$。证明：用 (3.1) 分组到 $q\mid N$，主项用 (3.10)/(3.11)/(3.13)，q>1 有限 Euler 因子消极点后移到 $\Re z=3/2$ 并用 Prop 2.1 的 (1.9)/(2.12)；q=1 的 principle residue 抵消。误差项 $=\frac{N^{2\sigma}}{\varphi(N)}\sum_{q\mid N}q^{1-\omega+\varepsilon}\cdot O(1)=O(N^{1-\omega+2\eta+\varepsilon})$（$\sigma=1/2+\eta$）。
   **此处需要 Ratios 误差对所有 $q\mid N$ 逐点可用；由于所有 $\varphi^*(q)>0$ 的 q 都出现，逐点 in q 是本质的（weakening (i) 的结论）。**
6. **sharp weight**（GWX §3.5）：$w(v)=e^{20(1-v)}(\sin\pi(v-1)/\pi(v-1))^2$，$W(u,v)=u^{-\lambda}v^{-\mu}w(u+v)$，$0\le\lambda,\mu\le\omega$。因 $w(k)=0\ (k=2,3,\dots)$、$w(1)=1$，得 (3.20) 精确选择 $m+n=N$；由 (3.12) 得 (3.24)：
   $$\sum_{m+n=N}\frac{\Lambda(m)\Lambda(n)}{m^\lambda n^\mu}=S(N)N^{1-\lambda-\mu}B(1-\lambda,1-\mu)+O_\varepsilon(N^{1-\omega+2\eta+\varepsilon}).$$
7. **prime pair 计数 + 素数幂剔除**（GWX p.18）：对 (3.24) 在 $[0,\omega]^2$ 积分，主项 $S(N)\int_0^NK_\omega(t)K_\omega(N-t)dt$；proper prime powers $O(N^{1/2}\log^2(2N))$ 被 $N^{1-\omega+\varepsilon}$ 吸收；再以 $\int_2^{N-2}\frac{dt}{\log t\log(N-t)}$ 替换主项（误差 $O(N^{1-\omega+\varepsilon})$，因 $S(N)\ll N^\varepsilon$）。最后取 $\omega\to\omega_D$、$\eta\to0$ 使误差 $O_\varepsilon(N^{1-\omega_D+\varepsilon})$。**$S(N)\ge2C_2>1$ 保证主项 > 误差。** ∎

**关键点**：整条推导中 H_Ratios^min 只在第 2 步之后用于三线插值的临界线边界；其它所有步骤只需 GRH 与代数恒等式（(3.3),(3.4),(3.11),(3.13),(2.12),(1.9) 均为已核对的恒等式）。

---

## 3. H_Ratios^min 的精确陈述（最终推荐写入报告/论文的版本）

> **H_Ratios^min（最终版）**
> 存在 $0<\omega_D\le1/2$、$\eta_0>0$、$B\ge0$，使得对每个 $0<\eta<\eta_0$、每个 $\varepsilon>0$、每个整数 $q>1$ 且 $\varphi^*(q)>0$，有
> $$\boxed{\ \sum_{\chi\bmod q}^{*}\frac{L(a,\chi)L(b,\bar\chi)}{L(s,\chi)L(t,\bar\chi)}
> =\varphi^*(q)Z_q(a,b;s,t)+H_q(a,b)Z_q(1-b,1-a;s,t)+O_{\eta,\varepsilon}\bigl(q^{1-\omega_D+\varepsilon}(1+T)^B\bigr)\ }$$
> 对所有 $\Re a=\Re b=1/2$、$\Re s=\Re t=1/2+\eta$、$T\le100\log(2q)$ 成立；误差在分子移位盘上全纯。**非标准处（必须显式保留）**：主项的精确 parity-resolved 形式（复合导子、$M_e(q)$ 计数、$H_q$）——这是比"标准 Ratios Conjecture"多出来的一项，不是 uniformity 问题。
> **再加 GRH**（all primitive Dirichlet L, ζ）。
> 结论：GWX Theorem 1.1；特别 $\omega_D=1/2$ 时误差 $O_\varepsilon(N^{1/2+\varepsilon})$，所有充分大偶数 Goldbach。

### 3.1 若只要定性 Goldbach 的弱化版（可选，需加一致性条款）

> **H_Ratios^{min,qual}**：存在非增函数 $\omega_D:(1,\infty)\to(0,1/2]$ 使 $\omega_D(q)\log q\to\infty$（如 $1/\log\log q$），且存在 $\eta_0,B$、**以及常数控制 $C(\varepsilon,\eta)=O(\varepsilon^{-A}\eta^{-A})$（H_UNIF，多项式型）**，使对每个 $0<\eta<\eta_0$、每个 $\varepsilon>0$、每个 $q$ 如上有
> $$\sum^*_\chi \frac{L(a,\chi)L(b,\bar\chi)}{L(s,\chi)L(t,\bar\chi)}=\mathcal M_q+O\bigl(C(\varepsilon,\eta)q^{1-\omega_D(q)+\varepsilon}(1+T)^B\bigr).$$
> 则 H_Ratios^{min,qual}+GRH ⇒ 误差 $O(N^{1-\omega_D(N)/2+o(1)})=o(N)$（取 $\eta=\eta(N):=\omega_D(N)/40$），故 Goldbach 对所有充分大偶数成立。
> **注意**：原始 H1.1 只说"对每个固定 η 存在 $O_{\eta,\varepsilon}$"，未给 $C(\varepsilon,\eta)$ 的多项式界；因此"$\omega_D(q)\log q\to\infty$ 的弱化"**不能**从原始 H1.1 直接推出，必须显式加 H_UNIF。这是 (iii) 的真正限制。

---

## 4. 六个 weakening 的逐项审计（表 + 说明）

| # | 原始 Hypothesis 1.1 clause | 是否必需？ | H_Ratios^min 的处理 |
|---|---|---|---|
| (i) | 对**所有** primitive conductors $q>1$（含 composite）一致性 | 本质必需（点值 in q） | 可限制到 $\varphi^*(q)>0$ 的 q；每个这样的 q 都是某偶数 N 的 conductor（$q$ odd ⇒ $N=2q$；$4\mid q$ ⇒ $N=q$），故无实质减弱 |
| (ii) | 误差逐点 + 在分子 disk 上全纯 | 可弱化为 $L^2$ 盘平均界 + $F_q$ 自动全纯 | 三线插值只用临界线逐点界；Cauchy 求导由 $F_q$ 全纯 + 盘上 $L^2$/mean-value 即可（见 §4.2） |
| (iii) | 固定 $\omega_D>0$（且 saving 独立于 η） | **固定 $\omega_D$ 版本必需**；变 $\omega_D(q)$ 需额外 H_UNIF | 见 §4.3；定性版可 $\omega_D(q)\log q\to\infty$，但需多项式型 η-常数控制 |
| (iv) | $T\le100\log(2q)$ | 宽松，实际只需 $\approx10\log(2q)$（三线矩形边界需 $\approx90\log2q$） | 可写 $T\le(10+o(1))\log2q$；保留 100 无害 |
| (v) | 精确 parity-resolved 主项 $\mathcal M_q$ | 安全最小形式；$\varphi^*/2$ 近似**有条件**可行 | 保留精确 $\mathcal M_q$；若用近似，需额外假设近似主项在 $a+b=1$ 可去/全纯（§4.5）[推测] |
| (vi) | $q>1$ 全部 | $v_2(q)=1$ 时 $\varphi^*(q)=0$，纯 vacuous | 删去该 clause（no effect）；对 $N\equiv2\bmod4$，有效最大 q 为 $N/2$（细节 §4.6） |

### 4.1 (i) 逐点 in q vs 只用 $q\mid N$ 的特定权重

- **[推导]** GWX (3.12) 的误差是 $\sum_{q\mid N}q^{1-\omega+\varepsilon}$ 型；若只对每个 N 给出"加权和"误差、而无逐 q 界，则当 N 取为单个大除数情形（$N=2q$，q odd；或 $N=q$，$4\mid q$）即可反推出该 q 的界（因为加权和中 q 项占主导，其它除数项至多 O(q^{1−ω}τ) 但可分离），所以逐点 in q 是本质的。**结论：无实质 weakening**（除了去掉 vacuous q）。
- 但注意：不需要对所有**奇数** q 之外的东西；只需 $\varphi^*(q)>0$ 的 q（见 (vi)）。

### 4.2 (ii) 点值 vs $L^2$ 盘平均

- **【推导】** GWX Lemma 3.1 的证明 = 三线插值。三线定理的输入只有：
  (a) $\Re\xi=0$ 边界：$|F_q|\le q^{-\omega_D+\varepsilon}(1+T)^B$（来自 H_Ratios^min 的**临界线点值**）；
  (b) $\Re\xi=1/8$ 边界：$|F_q|\ll q^{2+\varepsilon}(1+|T|)^D$（来自 GRH，GWX (3.25)）；
  (c) 垂直边/尾巴：$e^{\xi^2}$ 与 GRH strip 界。
  因此**逐点 H1.1 只在临界线被用**；不需要圆盘内部的逐点值。
- 之后 §3.2/§3.5 需要 Cauchy 公式对 $u,v$ 求导。设 $F_q(a,b)=q^{-1}(R_q-\mathcal M_q)$ 在目标点附近全纯（$R_q$ 由 L-函数/分母（GRH 下无零点）给出；$\mathcal M_q$ 为解析延拓）。若 H_Ratios 只给"在分子移位盘上 $L^2$ 平均 $\le q^{2-2\omega_D+\varepsilon}(1+T)^{2B}$"，则 mean-value inequality 给出
  $$|F_q(a,b)|\le C_r\Bigl(\frac1{\pi r^2}\int_{|u|^2+|v|^2\le r^2}|F_q(a+u,b+v)|^2\,dudv\Bigr)^{1/2}\ll_r q^{1-\omega_D+\varepsilon}(1+T)^B,$$
  再对 $u,v$ 用 Cauchy 得导数界（常数只依赖 r）；**故 (ii) 可以弱化为盘上 $L^2$ 平均界**。原始 H1.1 的"逐点 + 全纯"是充分而非必要。
- **[事实] 但注意**：GWX 自己的证明并不需要这个 weakening；保留"逐点 + 全纯"更简单、也是论文 Hypothesis 的写法。H_Ratios^min 可写成"逐点（临界线）+ 全纯"，这已是论文形式；若要弱化，可用 $L^2$ 版本。

### 4.3 (iii) $\omega_D(q)\log q\to\infty$ 是否足够？——**只对定性 Goldbach 足够，且需 H_UNIF**

- **[推导] 定性版推导**：设 $\omega(q)$ 非增、$\omega(q)\log q\to\infty$。取 $\eta=\eta(N):=c_0\,\omega(N)$（$c_0$ 小，比如 $1/40$），$r=\eta/8$。则对每个 $q\mid N$，因为 $\omega(q)\ge\omega(N)$，
  $$\omega_{\rm eff}(q)=\omega(q)-8(\eta+r)(2+\omega(q))\ge \omega(q)/2\ge\omega(N)/2>2\eta.$$
  于是 (3.12) 误差
  $$O\Bigl(\frac{N^{2\sigma}}{\varphi(N)}\sum_{q\mid N}q^{1-\omega_{\rm eff}(q)+\varepsilon}\Bigr)
  =O\Bigl(N^{2\eta+\varepsilon}\cdot \tau(N)N^{1-\omega(N)/2+\varepsilon}\Bigr)
  =O\bigl(N^{1-\omega(N)/2+2\eta+2\varepsilon}\bigr)=o(N),$$
  因为 $2\eta=\omega(N)/20$，且 $\omega(N)\log N\to\infty$。主项 $NS(N)\ge2C_2N$ 故 Goldbach 对所有充分大偶数成立。
- **【推导】真正的问题**：上式中 $O(N^{2\eta+\varepsilon})$ 吸收时使用了 (3.26) 的常数；原始 Hypothesis 1.1 的误差常数 $O_{\eta,\varepsilon}$ 对 η **没有显式控制**。由于 $\eta=\eta(N)=c_0\omega(N)\to0$，若常数如 $e^{1/\eta}$，则 $N^{2\eta}e^{1/\eta}$ 可能是 $N^{c_0\omega(N)+o(1)}$ 还是爆炸取决于常数形式；若常数是 $\eta^{-A}$（多项式），则 $N^{2\eta}\eta^{-A}=N^{c_0\omega(N)}\cdot(\log N)^{A}$（因为 $\omega(N)\sim(\log N)^{-1+o(1)}$ 之类），仍为 $N^{o(1)}$（只要 $c_0\omega(N)\log N\to0$？等等：$N^{2\eta}=e^{2c_0\omega(N)\log N}$；若 $\omega(N)\log N\to\infty$，则 $2c_0\omega(N)\log N\to\infty$，$N^{2\eta}$ 会爆炸！**这是关键**：$N^{2\eta}$ 是增长因子，不是小量。在 (3.12) 的误差里，$N^{2\eta}$ 来自 Mellin 因子 $N^{2\sigma}$；要让它 ≤$N^{1-\omega(N)/2}$，需要 $2\eta=\omega(N)/20$ 确实小于 $\omega(N)/2$，但相比主项 $N$，$N^{2\eta}/N = N^{-\omega(N)/2+\omega(N)/20}$，即相对误差 $N^{-0.45\omega(N)}$；因为 $\omega(N)\log N\to\infty$，$N^{-0.45\omega(N)}\to0$ ✓（不是 $N^{2\eta}$ 爆炸，而是相对于主项 $N$ 是小的）。所以只要常数多项式型，整体相对主项 $N^{-0.45\omega(N)+2\varepsilon}$·(log)^A→0 ✓。**结论：$\omega(q)\log q\to\infty$ 足够定性 Goldbach，前提是 H_UNIF（常数多项式型 in 1/η, 1/ε）。**
- **【事实/推导】原始 H1.1 没有 H_UNIF**：它说"for every fixed η... O_{η,ε}"，即常数可任意依赖 η。因此**不能**直接取 $\eta=\eta(N)\to0$；只有固定 $\omega_D$ 的版本（§3 boxed）是原文直接支持的。**这就是 (iii) 的精确结论**。
- **【推测】** 实际 Ratios 文献中的误差常数很可能是多项式型（来自 Cauchy/Stirling），H_UNIF 不算强假设；但作为"最小自足假设"必须显式写出，否则变量-ω 弱化不成立。

### 4.4 (iv) 实际 T 范围

- **[推导]** Lemma 3.1 的输入：$|\Im s|,|\Im t|\le10\log(2q)$、$|u|,|v|\le r$。三线插值矩形 $|\Im\xi|\le L:=80\log(2q)$；boundary $\Re\xi=0$ 的 numerator imaginary parts：
  $$|\Im a|\le10\log2q+r+L\le10\log2q+r+80\log2q<100\log2q,$$
  分母 $|\Im s|,|\Im t|\le10\log2q$。故 H1.1 的 $T\le100\log2q$ **恰好够用，且有余量**。**若想收紧**：可证只需 $T\le(90+o(1))\log2q$；甚至 $L$ 可取 $60\log2q$（Gaussian 尾巴 $e^{-3600(\log2q)^2}$ 仍极小），给出 $T\le(70+o(1))\log2q$。H_Ratios^min 保留 100 最安全。
- 在 (3.12) 轮廓移动中 Ratios 只用于 $|\Im s|,|\Im t|\le5\log2q$ 的 box 内（§3.5），更小；box 外由 GRH 的 signed 界 + $W$ 指数衰减控制。

### 4.5 (v) $\varphi^*/2$ 近似主项是否足够？

- **[事实]** GWX §3.6（pp.18–19）：
  > "...replacing the two counts by $\varphi^*(q)/2$ changes that coefficient by $O(1)$, by the bound for $\Delta(q)$ and $|X_{q,e}(a)|=|X_{q,e}(b)|=1$. After taking out the common factor $(q/\pi)^{1-a-b}$, which has modulus one on the critical line, the difference is independent of $q$ and vanishes on $a+b=1$. Cauchy's estimate for the gamma factors bounds its quotient by $a+b-1$ polynomially in the heights. **This removes the pole of the reflected kernel, and the change in the main term is $O_{\eta,\varepsilon}(q^\varepsilon)$ at the logarithmic heights in Hypothesis 1.1.** The hypothesis uses the exact coefficient and covers composite conductors as well."
- **[推导]** 若用 $\varphi^*/2$ 近似（即 $\Delta(q)=M_0-M_1=0$ 的版本），主项改变 $\le O(q^\varepsilon)$；相对于 Ratios 误差 $q^{1-\omega_D+\varepsilon}$，因为 $\omega_D\le1/2<1$，有 $q^\varepsilon\ll q^{1-\omega_D+\varepsilon}$。数值上**近似主项在最终误差中可忽略**。但 §3.6 同时指出"精确系数移除了 reflected kernel 的极点"：$\varphi^*/2$ 近似可能破坏 $F_q=q^{-1}(R_q-\mathcal M_q^{\rm approx})$ 在 $a+b=1$ 的可去性/全纯性，从而三线插值不适用。**因此 (v) 不是无条件的 weakening；H_Ratios^min 保留精确 $\mathcal M_q$ 最安全。** [推测] 若加上"近似主项给出的 $F_q$ 在 strip 全纯/可去"这一条，则可用近似（但这几乎等价于要求 $\Delta$ 项的结构，未必更弱）。
- **结论**：保留精确 $\mathcal M_q$；$q^\varepsilon$ 观察意味着主项只需"差 $O(q^\varepsilon)$"，但**解析结构（全纯/可去）也必须匹配**。

### 4.6 (vi) $v_2(q)=1$ 的 vacuous 情形

- **[推导]** 若 $q=2m$，m odd，则 $(\mathbb Z/2m)^*\cong(\mathbb Z/m)^*$；任何 mod $2m$ 的 Dirichlet 特征都由 mod $m$ 的特征诱导，conductor 整除 $m<2m$，故不存在 conductor 为 $2m$ 的 primitive 特征：$\varphi^*(2m)=0$（可用 $\sum_{d\mid q}\mu(q/d)\varphi(d)$ 验证：$q=6,10,14$ 均为 0）。因此 Hypothesis 1.1 对 $v_2(q)=1$ 的 $q$ 求和为空、$\mathcal M_q=0$，**纯 vacuous**；H_Ratios^min 可直接删去这些 $q$。
- **[推导] 对 N 的影响**：若 $v_2(N)=1$（$N\equiv2\bmod4$），N 的所有 primitive conductor 因子都是奇数（因为任何 $q\mid N$ 若 $v_2(q)=1$ 则 $\varphi^*(q)=0$），故有效 $q$ 只到 $N/2$（N 的奇部）；这是 (i)/(iii) 中"最大 q"的常数改善，不影响结论。
- 若 $4\mid q$ 或 $q$ odd，则 $\varphi^*(q)>0$（标准公式），这些 q 都必须保留。

---

## 5. 回答 follow-up：cxy0714 的"额外一致性"疑问是否成立？

**结论：[推导] 不成立。所给 Hypothesis 1.1（+前文的"errors holomorphic on disks"）+ GRH 已足够推出 Lemma 3.1 的 (3.25)/(3.26) 与 (3.12) 的轮廓移动；不需要任何未写出的 uniformity 假设。** 逐步如下。

### 5.1 三线插值所需的一切（对应 GWX §3.6, pp.18–19）

设目标 numerator 移位 $a=s+u$、$b=t+v$，$\Re s=\Re t=\frac12+\eta$，$|u|,|v|\le r$，$|\Im s|,|\Im t|\le10\log(2q)$，$r<\min(\eta/4,(1/4-\eta)/4)$。定义
$$F_q(a,b)=q^{-1}\bigl(R_q(a,b;s,t)-\mathcal M_q(a,b;s,t)\bigr).$$
它作为 $a,b$ 的函数在 strip $|\Re a-\frac12|,|\Re b-\frac12|\le1/8$ 上全纯：
- 分子 $L(a,\chi)L(b,\bar\chi)$ 整；
- 分母 $L(s,\chi)L(t,\bar\chi)$ 在 $\Re s=\Re t=\frac12+\eta$ 非零（GRH），且 $\Re s>1/2$ 使其逆有界；
- $\mathcal M_q$ 是 CFZ 两项主项的解析延拓（$a+b=1$ 可去；GWX §1.1/§3.6 明确定义）。**注意：这里没有用到 H1.1 的任何圆盘假设；全纯性来自 $R_q$ 和 $\mathcal M_q$ 的解析结构 + GRH。**
取三线函数 $e^{\xi^2}F_q\bigl(\frac12+i\Im a+\frac{\Re a-1/2}{\eta+r}\xi,\ \frac12+i\Im b+\frac{\Re b-1/2}{\eta+r}\xi\bigr)$，矩形 $0\le\Re\xi\le1/8$、$|\Im\xi|\le L:=80\log(2q)$。注意在 $\xi=\eta+r$（实数）处，实部 $=1/2+(\Re a-1/2)=\Re a$（对 direct 情形；反射情形 $a=1-t-v$ 时有 $\Re a-1/2=-\eta$，同样成立），虚部 $=\Im a$，即目标点。

**Boundary $\Re\xi=0$**：numerators 在临界线，$\Re a=\Re b=1/2$；imaginary parts：
$$|\Im a_{\xi=0}|=|\Im a+\frac{\Re a-1/2}{\eta+r}\Im\xi|\le10\log2q+\frac{r}{\eta+r}L\le10\log2q+L\le90\log2q;$$
同理 $|\Im b_{\xi=0}|\le90\log2q$；分母 $|\Im s|,|\Im t|\le10\log2q$。故
$$T\le90\log(2q)<100\log(2q).$$
**Hypothesis 1.1 直接适用**（对每个固定 $0<\eta<\eta_0$；此处 η 就是 Lemma 的 η，固定），给
$$|F_q|_{\Re\xi=0}\le q^{-\omega_D+\varepsilon}(1+90\log2q)^B.$$
（$|e^{\xi^2}|=e^{(\Re\xi)^2-(\Im\xi)^2}=e^{-(\Im\xi)^2}\le1$，此处不需要衰减。）

**Boundary $\Re\xi=1/8$**：numerators 实部 $=5/8$；用 GRH：
- $L(5/8+it,\chi)\ll q^{(1-5/8)/2+\varepsilon}(1+|t|)^{C}=q^{3/16+\varepsilon}(1+|t|)^C$（凸性界；或 GRH Lindelöf）；
- 分母 $1/L(1/2+\eta+it,\chi)\ll q^\varepsilon(1+|t|)^\varepsilon$（GRH 零自由区）；
- $\mathcal M_q$ 的 $Z_q$ 因子在实部 $>1$（$a+b$ 实部 $5/4$）绝对收敛，$H_q\le\varphi^*(q)\le q$；
故 $|F_q|_{\Re\xi=1/8}\ll q^{-1}\cdot q^{3/8+\varepsilon}\cdot q^\varepsilon\cdot q^{1+\varepsilon}=q^{2+\varepsilon}(1+|T|)^D$（与 (3.25) 一致；常数宽松）。

**垂直边与尾巴**：
- 垂直边 $\Re\xi=0$ 与 $1/8$ 在 $|\Im\xi|=L$ 处是端点；三线定理只用左右两条竖边（$\Re\xi=0,1/8$）的边界，不需要上下边（$|\Im\xi|=L$ 是截断，非边界；实际上三线定理用于矩形 $[0,1/8]\times[-L,L]$ 的左右边）。
- 对 $|\Im\xi|>L$ 的无穷竖边：不能直接引用 H1.1（$T>100\log2q$），但 $F_q$ 有 GRH strip 界 $|F_q|\ll q^{2+\varepsilon}(1+|\Im\xi|)^D$（由上述同样估计，实部在 strip 内），乘 $|e^{\xi^2}|=e^{-(\Im\xi)^2}$ 后尾部 $\ll q^{2+\varepsilon}L^D e^{-L^2}\ll q^{-100}$（因 $L=80\log2q$），可忽略；而且三线插值实际只需矩形，不需要无穷边。**因此无额外 H1.1 要求。**
- 三线定理（对 $e^{\xi^2}F_q$ 在矩形上）给
  $$\max_{\Re\xi\in[0,1/8]}|e^{\xi^2}F_q(\xi)|\le M_0^{1-8\Re\xi}M_{1/8}^{8\Re\xi},$$
  其中 $M_0=q^{-\omega_D+\varepsilon}(1+90\log2q)^B$、$M_{1/8}=q^{2+\varepsilon}(1+|T|)^D$。在目标 $\xi=\eta+r$ 处：
  $$|F_q|\ll q^{-\omega_D+8(\eta+r)(2+\omega_D)+\varepsilon}(1+\log2q)^{B'}=q^{-\omega+\varepsilon}(1+\log2q)^{B'},$$
  即 GWX (3.26)。取 $\omega=\omega_D-8(\eta+r)(2+\omega_D)>2\eta$（η,r 足够小；注意 $\omega_D>0$ 固定，所以总能取到）即 Lemma 3.1 的 (3.2)。
- **误差在 $u,v$ 盘上的全纯性与一致性**：$F_q$ 对 $a,b$ 全纯；strip 界在目标点邻域一致（$T$ 变化 $\le r$）；因此对 $u,v$ 用 Cauchy 得导数界；常数只依赖 $\eta,r,B,\varepsilon$，不依赖 q。**无需 H1.1 在圆盘内的逐点值。**

**结论**：三线插值只消费 H1.1 的以下内容：(a) 每个固定 η<η0；(b) 临界线 numerator + 分母 $\Re=1/2+\eta$；(c) $T\le100\log2q$；(d) 误差 $O_{\eta,\varepsilon}(q^{1-\omega_D+\varepsilon}(1+T)^B)$。**全部在 Hypothesis 1.1 中。没有 missing uniformity。**

### 5.2 (3.12) 轮廓移动所需的一切

- (3.12) 的误差来自 $\sum_{q\mid N}$ 的每一 q：在 $\Re s=\Re t=\sigma=1/2+\eta$ 的 Mellin 线上，用 (3.2) 的误差 $O(q^{1-\omega+\varepsilon}(1+|\Im s|+|\Im t|)^B)$，乘 $|W(s,t)|$ 后积分。GWX 用 (3.7)（有理权）或 (3.23)（sharp 权）证明
  $$\int_{(\sigma)^2}|F_q^{\rm err}(s,t)|\,|W(s,t)|\,|ds\,dt|\ll q^{1-\omega+\varepsilon}\cdot(\log2q)^{B'},$$
  其中 $F_q^{\rm err}$ 是 (3.2) 的误差（含 Cauchy 求导后的 u,v 导数）；常数只依赖权（fixed rational functions 或 fixed sharp $w$、$\lambda,\mu\in[0,\omega]$）与 $\eta,\varepsilon$。
- 求和：$\sum_{q\mid N}q^{1-\omega+\varepsilon}\ll N^{1-\omega+2\varepsilon}$（$\tau(N)\ll N^\varepsilon$）；乘 $N^{2\sigma}/\varphi(N)=N^{1+2\eta}/N^{1-\varepsilon}=N^{2\eta+\varepsilon}$；总误差 $O(N^{1-\omega+2\eta+\varepsilon})$，即 (3.12)。**唯一用到的"一致性"是 H1.1 的"uniformly for all conductors q>1"与 $(1+T)^B$（多项式，积分后只多 log 因子）；两者都在 H1.1 中。**
- 轮廓移动的其它步骤（q>1 消极点、q=1 principal residue 抵消、$\Re z=3/2$ 的绝对收敛、GRH 的 q=1 移动）全部是标准/已核对恒等式，不用 Ratios。
- **结论**：无 missing uniformity。

### 5.3 cxy0714 疑问的可能来源（为何听起来像"需要额外假设"）

1. **主项非标准**：Hypothesis 1.1 用的 $\mathcal M_q$ 是复合导子的精确 parity-resolved 两项主项；标准文献（WX25）只对 prime conductor 表述。若把"标准 RC_D"理解为"只有 φ*Z_q + H_q 的 φ*/2 版本/只对 prime q"，则 parity-twist 平均**确实不是其直接推论**——但这不是 uniformity 缺失，而是**主项形式**的超标准性，且已显式写在 H1.1 中（phase-8 已指出）。**H_Ratios^min 必须显式保留这一点（报告 §3 已 boxed）。**
2. **三线插值的 100 margin**：由于 H1.1 的 T 上界 100log 只在临界线，而三线边界需要 numerator 高度到 90log（我们算出），看起来"需要 H1.1 在大高度也成立"；但 100 覆盖 90，加上 Gaussian 处理 >100log 的尾巴（用 GRH strip 界），所以实际成立。**这是 doubt 最可能的技术来源；我们已在 §5.1 用显式常数消除。**
3. **误差全纯性**：H1.1 的"errors holomorphic on disks"是为后续 Cauchy 求导写的；三线插值本身不需要它（$F_q$ 全纯来自结构）；它对 §3.2 的 Cauchy 求导是充分的。所以它不制造额外需求。
4. **若 H1.1 只被理解为"逐点 on the line, no holomorphy"**：仍足够：$F_q$ 全纯性来自 $R_q,\mathcal M_q$ 的解析结构 + GRH；逐点误差界 + 全纯性 ⇒ 用最大值原理？不，逐点误差界只在线上，圆盘内值仍需三线插值（用 GRH 另一端）；所以全纯性不是必需，但也不缺。

**最终裁决**：**Hypothesis 1.1 + GRH 足够；不存在需要补充的 uniformity clause。** 唯一需要在 H_Ratios^min 中显式强调的"额外"是**复合导子的精确 parity-resolved 主项**（已在 H1.1 原文中，不是 missing clause）。cxy0714 的 phrase "not a direct corollary of standard RC_D" 若指主项形式，则**正确但不是 uniformity gap**；若指三线插值需要额外一致性，则**不正确**（§5.1–5.2 已逐项核验）。

---

## 6. 文献/公式索引

- GWX Hypothesis 1.1（p.2）；Theorem 1.1（p.3）；§1.1 "On the indicated disks, the errors are holomorphic in the numerator shifts"（p.2）。
- Lemma 3.1 / (3.2)（p.13）；(3.3)(3.4)（p.13）；(3.9)(3.10)(3.11)（pp.14–15）；(3.25)(3.26)（p.19）；§3.6（pp.18–19）；(3.12)（p.15）；(3.24)（p.18）；Prop 2.1 (2.11)(2.12)（p.7）；(2.21)（p.11）；Appendix A（p.39）。
- 本地全文：`phase7/lit/gwx_pdf.txt`、`gwx.txt`（HTML 版含共轭横线）。
- 本报告使用的独立数值核对见 phase-8 报告 §4.3（(3.3),(3.4),(3.11),(2.12) 全部通过）。

---

## 7. 一句话结论（给 Lead）

> **H_Ratios^min = GWX Hypothesis 1.1 本身（固定 $\omega_D>0$、精确复合导子 parity 主项、$T\le100\log2q$、误差在分子移位盘上全纯）+ GRH**；任何固定 $\omega_D>0$ 足够（$\omega_D=1/2$ 最优）。六项 weakening 中：只有 (ii) 真正可弱化为 $L^2$ 盘平均、(iv) 可收紧到 $T\approx10\log2q$、(vi) 可删去 $v_2(q)=1$ 的 vacuous q；(i) 无实质减弱；(iii) 的 $\omega_D(q)\log q\to\infty$ 只对定性 Goldbach 成立且需额外 H_UNIF（多项式型 η-常数控制）；(v) 近似主项需额外解析结构，保留精确 $\mathcal M_q$ 最安全。**cxy0714 的"missing uniformity"doubt 不成立**：Hypothesis 1.1 + GRH 的 100-log margin、全纯性、三线插值与 (3.12) 轮廓移动所需全部估计均已逐步核验；唯一"非标准"是精确 parity-resolved 复合导子主项，而它已显式写在 H1.1 中。
