> **【phase-10 数值修正，2026-11-21 21:10】** 本报告早期消息中"用 `check_parity.py` 复现 (3.3) 到 4×10⁻³¹"的数值证据有误：该脚本把 principal 特征也当 primitive 计入，不能复现。spectral-numerics 的 primitive-only 独立实现把 (3.3) 恒等式复现到 **1.5×10⁻¹⁵**；**审计结论本身不变**（仅该数值证据应以修正脚本重记）。另：复合 q 的数值检验（q=53…2003，23 个导子）支持 H_Ratios 主项（|E−M|/√q 无 q 增长趋势、无系统性 parity 偏差、H_q 项必需、复合与素数同尺度行为一致）——见 `phase10/numerics/ratios-composite.md`。

# Phase-8 审计：Gou–Wang–Xu「GRH + Ratios ⇒ Goldbach」归约的严格审计

> 审计：liu-auditor（task-31，2026-11-21）。**只写本目录**；未改动他人文件。
> 对象：H. Gou, V. Y. Wang, M. W. Xu, *Landau's problems through ratios of L-functions*, arXiv:2611.18825v1 [math.NT], 13 Nov 2026（[预印本·未评审]）。本地全文：`/home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase7/lit/gwx_pdf.txt`、`gwx.txt`（HTML 抽取，含共轭横线，本报告以 HTML 版核对公式）；PDF `gwx.pdf`。
> 标注：**[事实]** 论文原文/可核对；**[推导]/[证明]** 本报告独立重建；**[数值]** 本报告独立数值核对（代码 `phase8/audit/check_gwx.py`、`check_parity.py`）；**[推测]** 判断。
> 本文与既有 LL 审计（phase-4/5/6）使用同一套记号；LL=Li–Liu 预印本。

---

## 0. 结论速览

1. **[推导] 证明链条重建无误**：论文的机制是
   奇偶投影 (3.1) → 功能方程求 parity twist (3.3)–(3.4)（根数在 χ 与 χ̄ 之间抵消）→ 用 Ratios 猜想在临界线上插值得到 Lemma 3.1 的移位平均 (3.2) → 有理权 Mellin (3.5)–(3.8) 压住系数指数增长 → 加权和公式 (3.12)（把它化为 Σ_{q|N}φ*(q)q^{-z}D_q(z)，再用 (1.9)/(2.12) 求和）→ sharp 整函数权 (3.19)–(3.24) 精确选出 m+n=N → 素数对计数 + 素数幂剔除 ⇒ Theorem 1.1。
   我数值验证了其中所有纯代数恒等式：(3.3) 对 q=5 的 primitive 特征误差 4×10⁻³¹；(3.4) 误差 10⁻³⁶；(3.11) 误差 6×10⁻³⁶；Prop 2.1 的 (2.11)/(2.12) 在 N=6,12,30 相对误差 <5×10⁻³⁴；S(N)(1.1) 与 2C₂∏(p−1)/(p−2) 一致。**未发现符号/常数错误。**
2. **[事实+推导] 最小自足假设 H_Ratios**（=论文 Hypothesis 1.1 的内容，见 §3.1 的 boxed 陈述）：存在**固定** 0<ω_D≤1/2、η₀>0、B≥0，使对**每个** 0<η<η₀、每个 ε>0、**每个**整数 q>1（**含复合导子**），
   Σ*_{χ mod q} L(a,χ)L(b,χ̄)/[L(s,χ)L(t,χ̄)] = M_q(a,b;s,t) + O_{η,ε}(q^{1−ω_D+ε}(1+T)^B)，
   在 ℜa=ℜb=1/2、ℜs=ℜt=1/2+η、T≤100log(2q) 上一致，误差在分子移位圆盘上全纯；其中 M_q 为**精确 parity-resolved 两项主项**（φ*Z_q+H_qZ_q 反向项，H_q=Σ_e M_e(q)X_{q,e}(a)X_{q,e}(b)）。**GRH（所有 primitive Dirichlet L + ζ）** 是另一独立假设。**任何固定 ω_D>0 足够**；若只要求定性 Goldbach 可弱化为 ω_D(q)log q→∞。
   **定理（论文 Theorem 1.1）**：H_Ratios+GRH ⇒ 对每个 ε>0、所有充分大偶数 N，Σ_{m+n=N}Λ(m)Λ(n)=N·S(N)+O_ε(N^{1−ω_D+ε})；ω_D=1/2 时 O(N^{1/2+ε})<主项 ⇒ Goldbach。
3. **[事实] 唯一实质"额外输入"（非 gap，但是假设的强度所在）**：**复合导子的精确 parity-resolved 主项 M_q 是论文自己规定的假设，不是已发表定理**。§3.6 只把 prime q 情形归到 Wang–Xu [WX25, Conjecture 2.1]；对 composite conductors，Hypothesis 1.1 直接规定 "uses the exact coefficient and covers composite conductors as well"。这与通常表述的 Ratios Conjecture 相比是**加强/外推**：标准文献一般不对复合导子给出这种精确 parity 系数与对所有移位的 q^{1−ω} 均匀误差。H_Ratios 必须包含这一点。
   除此之外，我只发现两处无关紧要的表述问题（§4.2）：§3.4 qualitative sandwich 的 δ→0 与 N→∞ 次序写得草率（**不用于 Theorem 1.1 的 power-saving 证明**，§3.5 不依赖它）；Theorem 1.1 "for every even N" 应读作"充分大 N"（小 N 并入常数）。**未发现致命错误。**
4. **[推导] 与 LL 的 H_Gold 比较：不等价，GWX 终点更强、假设更"主流"。**
   - LL H_Gold（phase-6 形式）：固定光滑对称 ψ（支撑在 (1/3,2/3)），对每个充分大偶数 N，|G_ψ(N)−c_ψS(N)|≪δ_N=√(S/N)(logN)^{3/2}，G_ψ=(1/N)ΣΛΛψψ；H_Gold⇒Goldbach（正主项⇒至少一对）。
   - GWX+GRH ⇒ **sharp 未加权计数** ΣΛΛ=NS+O(N^{1/2+ε})，是更强的**目标**；但 sharp count 不给光滑权分布 ⇒ 不显然推出 H_Gold；H_Gold 也不给 sharp count。**两者不可互推（已知意义下），但都 ⇒ Goldbach。**
   - 假设层面：H_Ratios 是**标准型 Ratios 猜想**（单一族、无 ad hoc 算子范数/跨 χ 四阶零点相关），但需复合导子+精确 parity 主项强化；LL 的 R/S/H_Gold 是 ad hoc 的 Goldbach-强度假设。**GWX 路线在"归约到已知猜想族"意义上明显更优，是当前最有希望的路线。**
5. **[裁决]** Theorem 1.1（modulo 预印本）是一个**正确的条件性归约**。最难缺的单一输入 = **对所有 primitive 复合导子一致、带精确 parity 主项、误差 q^{1−ω_D+ε} 且对分子移位全纯的 Ratios 猜想**。GRH 若由 Alpöge/Claude 兑现，则只剩 H_Ratios；这条路不依赖 Li–Liu 的 R/S、也不依赖跨 χ 四阶零点相关（与 lead 的 phase-7 判断一致，本报告逐步核对了"不需要 pair correlation"这一点：所有相关性都被 Ratios 猜想的平均所吸收）。

---

## 1. 论文身份与 Theorem 1.1 的原文

**[事实]** 标题/作者/日期：*Landau's problems through ratios of L-functions*, Haozhe Gou, Victor Y. Wang, Max Wenqiang Xu, arXiv:2611.18825v1, 13 Nov 2026（预印本，CC BY 4.0）。

**[事实] Theorem 1.1（p.3 逐字）**：
> "**Theorem 1.1 (Goldbach).** Assume GRH for Dirichlet L-functions, and RC_D(ω_D). For every ε>0 and every even N, we have
> Σ_{m+n=N}Λ(m)Λ(n) = N𝔖(N) + O_ε(N^{1−ω_D+ε}). (1.3)"

**[事实] 开头动机/footnote 1（p.1）**：
> "Strictly speaking we also assume GRH, but as in Lee's work, it is possible to formulate the Ratios Conjecture in a way that does not require GRH."

**[事实] §1.2 结尾（p.3）**：
> "Hypothesis 1.1 assumes the formula for all primitive conductors and specifies the exponent ω_D. The case ω_D=1/2 is the square-root error bound for this family. **Any fixed ω_D>0 suffices for Theorem 1.1.**"

**[事实] §1.4 对 Goldbach 证明的概述（p.4）**：
> "For Goldbach, summing over primitive conductors gives the exact projection (and this will be proved in Proposition 2.1) … Additive support then isolates h=N."
> "For the Goldbach problem, character orthogonality introduces χ(−1). Applying the functional equations to both numerator factors gives a second untwisted ratios average, with numerator arguments (1−b,1−a). The two averages together determine the difference between the even and odd contributions. The coefficients in this linear combination can grow exponentially when the imaginary parts of the numerator arguments are large and of opposite signs. Rational product weights give sufficient Mellin decay to control this growth…"

**[事实] singular series 定义（1.1）**：S(h)=∏_p σ_p(h)，σ_p(h)=p/(p−1)（p|h），p(p−2)/(p−1)²（p∤h）；odd h 时 S(h)=0；even h 时为正的 Hardy–Littlewood 奇异级数。我们核对了它与 LL 的 2C₂∏_{p|N,p>2}(p−1)/(p−2) 完全一致。

---

## 2. 证明的逐步重建（含 GRH / RC_D 的精确使用点）

### Step 0. 奇偶投影与 primitive-conductor 求和恒等式（§2、§3 开头；p.7、p.12）

- **[事实] (3.1)（p.12）**：对 (mn,N)=1，
  $$1_{N\mid m+n}=\frac1{\varphi(N)}\sum_{\chi\bmod N}\chi(-1)\chi(m)\overline{\chi(n)}.$$
  （PDF 抽取漏了共轭横线；HTML 版确认右侧为 χ(−1)χ(m)\barχ(n)。）
- **[事实] Prop 2.1（p.7）**：对 ℜz>1，
  $$D_q(z)=\sum_{h\ge1}K_q(h)(h/q)^{-z},\qquad K_q(h)=\frac{q}{\varphi(q)^2}c_q(h)S_q(h),\tag{2.11}$$
  $$\sum_{q\mid N}\varphi^*(q)K_q(h)=\varphi(N)S(h)\mathbf 1_{N\mid h}\qquad(\forall N,h)\tag{2.12}$$
  从而 $ \frac1{\varphi(N)}\sum_{q\mid N}\varphi^*(q)q^{-z}D_q(z)=\sum_{N\mid h}S(h)h^{-z}$（(1.9)）。
  **[数值]** 我独立验证 (2.12)：N=6,12,30、h≤2N，最大相对误差 <5×10⁻³⁴（脚本 `check_gwx.py`）。**这是整条路线中"求和 over primitive conductors 恢复 Goldbach 奇异级数"的关键恒等式，正确。**
- 这一步**不需要** GRH，也不需要 Ratios；是纯代数/初等数论。

### Step 1. GRH 的第一次使用：把 Λ 展开成 L'/L，并把轮廓移到固定半平面（§2.6、§3.3；p.11、p.15）

- **[事实] (2.21)**：在共同零自由半平面 ℜs>β 上，对 primitive χ，
  $$\frac{L'}{L}(\sigma+it,\chi)\ll_{\sigma-\beta}\log(2q(2+|t|)).\tag{2.21}$$
  RH/GRH 给 β=1/2；还用到 1/L 的多项式界（由零自由区积分得到）。
- **[事实] §3.3（3.12）证明中的轮廓移动**：从绝对收敛线 ℜs=ℜt=5/4 出发；含"被省略 Euler 因子"的项移到 ℜ=λ+ε/4 或 µ+ε/4；其余 primitive L'/L 移到 ℜ=σ=1/2+η 并用 (2.21) 控制。**GRH 在这里不可少**（决定可移到 1/2+η 并给 log 界）。q=1（principal）的 ζ'/ζ 双极点在 s=t=1 给 residue $N^{2-\lambda-\mu}W(1,1)/\varphi(N)$，随后与 q=1 积分在 z=1 的极点 residue 精确抵消（(3.12) 证明）。
- **[事实] 一个技术点**：对 χ mod N（可能非本原）与 primitive χ* mod q（q|N），
  $L'/L(s,\chi_N)=L'/L(s,\chi^*)-\sum_{p|N,p\nmid q}\chi(p)\log p/(p^s-\chi(p))$；被省略因子的项按上述轮廓移动后贡献 $O_\varepsilon(N^{\sigma+\varepsilon})$，在 (3.12) 中被 $N^{2\eta}$ 因子吸收。

### Step 2. 功能方程的 parity twist（§3.1；p.13）

- **【推导】公式 (3.3)**：令 $R_q(a,b;s,t)=\sum^*_{\chi\bmod q}\frac{L(a,\chi)L(b,\bar\chi)}{L(s,\chi)L(t,\bar\chi)}$，$R^\vee=R_q(1-b,1-a;s,t)$，$h_e=X_{q,e}(1-b)X_{q,e}(1-a)$。对 primitive χ（parity e）用 χ 与 χ̄ 的两个功能方程：
  $$L(1-b,\chi)L(1-a,\bar\chi)=\varepsilon(\chi)\varepsilon(\bar\chi)X_{q,e}(1-b)X_{q,e}(1-a)L(a,\chi)L(b,\bar\chi)=h_e L(a,\chi)L(b,\bar\chi),$$
  因为 $|\varepsilon(\chi)|=1$ 且 $\varepsilon(\bar\chi)=\overline{\varepsilon(\chi)}$ ⇒ 根数积=1。于是若 $R=R_0+R_1$、$R^\vee=h_0R_0+h_1R_1$，则
  $$\sum^*_{\chi\bmod q}\chi(-1)\frac{L(a,\chi)L(b,\bar\chi)}{L(s,\chi)L(t,\bar\chi)}=\frac{2R^\vee-(h_0+h_1)R}{h_0-h_1}.\tag{3.3}$$
- **[事实] (3.4)**：$h_0-h_1=-4q^z(2\pi)^{-z-1}\Gamma(a)\Gamma(b)\sin(\pi z/2)$，$z=a+b-1$；且 $(h_0+h_1)/(h_0-h_1)=-\cos(\pi(a-b)/2)/\sin(\pi z/2)$（在 σ=1/2+η 附近有指数增长，§3.2 处理）。
- **[数值]** q=5、primitive 特征 {quad,χ,χ̄}、两组随机移位：直接计算 parity 加权和与 (3.3) 右端，差 ~4×10⁻³¹；**(3.4) 差 ~10⁻³⁶**。**奇偶 twist 与其系数完全正确。**

### Step 3. 从临界线 Ratios 到移位平均：三线插值（§3.6、Lemma 3.1；p.13、pp.18–19）

- **[事实] Lemma 3.1（3.2）（p.13）**：在 GRH + Hypothesis 1.1 下，对某个 $2\eta<\omega\le1/2$，uniformly q>1、|ℑs|,|ℑt|≤10log(2q)、|u|,|v|≤r，
  $$R_q(a,b;s,t)=\varphi^*(q)Z_q(a,b;s,t)+H_q(a,b)Z_q(1-b,1-a;s,t)+O_\varepsilon\bigl(q^{1-\omega+\varepsilon}(1+|\Im s|+|\Im t|)^B\bigr)\tag{3.2}$$
  对 $(a,b)=(s+u,t+v)$ 与 $(a,b)=(1-t-v,1-s-u)$ 都成立；$H_q(a,b)=\sum_{e=0,1}M_e(q)X_{q,e}(a)X_{q,e}(b)$。
- **【推导】Lemma 3.1 的证明机制**：令 $F_q(a,b)=q^{-1}(R_q(a,b;s,t)-\mathcal M_q(a,b;s,t))$，在 $|\Re a-1/2|,|\Re b-1/2|\le1/8$ 全纯（在 GRH 下由 (3.25) 的 $q^2(1+\text{heights})^D$ 多项式界保证；near $a+b=1$ 的 apparent pole 可去）。对 $e^{\xi^2}F_q(\tfrac12+i\Im a+\frac{\Re a-1/2}{\eta+r}\xi,\dots)$ 在 $0\le\Re\xi\le1/8$ 用三线定理：$\Re\xi=0$（分子在临界线）用 Hypothesis 1.1 得 $O(q^{-\omega_D+\varepsilon})$；$\Re\xi=1/8$ 用 (3.25) 得 $O(q^{2+\varepsilon})$；于是
  $$|F_q(a,b)|\ll q^{-\omega_D+8(\eta+r)(2+\omega_D)+\varepsilon}\tag{3.26}$$
  （注意：三线宽度是 1/8，插值指数是 $8\xi(2+\omega_D)$——我们核对后确认 (3.26) 的因子 8 正确，不是笔误）。取 $\omega=\omega_D-8(\eta+r)(2+\omega_D)>2\eta$ 即得 Lemma 3.1。
- **[推导] 这里 RC_D 只用于临界线（ℜa=ℜb=1/2）**；ℜs=ℜt=1/2+η 的移位平均是插值出来的。所需 T 范围：$\Re\xi=0$ 上分子高度 ≤$10\log2q+80\log2q$，分母高度 ≤10log2q，均 <100log2q ⇒ 恰在 Hypothesis 1.1 范围内。**因此 H_Ratios 中 T≤100log(2q) 的界是必要且足够的。**
- **[事实] GRH 的第二次使用**：(3.25) 中分子凸性界 + 分母 $1/L(1/2+\eta+it,\chi)\ll q^\varepsilon$（由 GRH 零自由区积分）；以及 $|F_q|$ 的 strip 全纯。

### Step 4. 有理权 Mellin 与集成误差（§3.2；pp.13–15）

- **[事实] (3.5)–(3.7)**：用 $f_j(u)=u^j/(1+u)^{A+j}$，其 Mellin 变换 (3.6) 含两个 Gamma 因子；一个抵消 (3.3) 系数的指数增长 $e^{\pi T/2}$，另一个提供指数衰减。由 Stirling 与 (3.4) 得 (3.7)：
  $$\Bigl|\frac{\tilde f(s)\tilde g(t)}{h_0-h_1}\Bigr|+\Bigl|\frac{(h_0+h_1)\tilde f(s)\tilde g(t)}{h_0-h_1}\Bigr|\ll_{f,g,\eta,r}(1+|\Im s|+|\Im t|)^C e^{-c(|\Im s|+|\Im t|)}.$$
- **[事实]** 对每个 q 得到集成误差 $O_{f,g,\varepsilon}(q^{1-\omega+\varepsilon})$（(3.8)）。**这是"用有理权压住 parity 系数指数增长"的关键；我们复核了量级：$|h_0-h_1|^{-1}\sim e^{-\pi|y|/2}$、W 的 gamma 因子给 $e^{-\pi(|x|+|y|)/2}$，乘积确实指数衰减。**

### Step 5. 加权和公式 (3.12) 与主项（§3.3；pp.15–17）

- **【推导】(3.12)**：对满足增长/衰减条件的 W(u,v)，
  $$N^{-\lambda-\mu}\sum_{m,n\ge1,\,N\mid m+n}\Lambda(m)\Lambda(n)W(m/N,n/N)
  =N^{1-\lambda-\mu}\sum_{k\ge1}S(kN)F(k)+O_\varepsilon(N^{1-\omega+2\eta+\varepsilon}),\tag{3.12}$$
  $F(x)=\int_0^xW(u,x-u)du$。证明：用 (3.1) 展开，按 primitive conductor q|N 分组；**主项来自 Ratios 的 (3.10)（$\Delta(q)P_q(z)+[M_0X_0(s)X_0(t)-M_1X_1(s)X_1(t)]C_q(z)$）经恒等式 (3.11) 和内层 Mellin–Barnes (3.13) 化成 $(N/q)^zD_q(z)\tilde F(z)$**；q>1 的有限 Euler 因子消去 D_q 在 z=1 的极点，轮廓移到 3/2 并用 (1.9) 变回 $\sum_{N|h}S(h)$；q=1 的极点 residue 与 principal-character 项抵消。误差：集成 Ratios 误差 $\sum_{q|N}q^{1-\omega+\varepsilon}\cdot N^{2\sigma-1}$（$\sigma=1/2+\eta$）$=O_\varepsilon(N^{1-\omega+2\eta+\varepsilon})$。
- **[数值]** 我们独立验证 (3.11)（$[X_0(s)X_0(t)-X_1(s)X_1(t)]\Xi(z)/2=q^{-z}\Gamma(1-s)\Gamma(1-t)/\Gamma(1-z)$）到 6×10⁻³⁶；(3.4) 到 10⁻³⁶；(2.12) 到 5×10⁻³⁴；**未见符号/常数错误**。
- **[事实] 恒等式 (3.13)**：$\frac1{2\pi i}\int_{(\sigma)}W(s,1+z-s)\frac{\Gamma(1-s)\Gamma(s-z)}{\Gamma(1-z)}ds=\tilde F(z)$，$\Re z=2\eta$；由 Mellin–Barnes 公式 $(u+v)^{z-1}$ 与 W 的双重 Mellin 变换得到（我们核对了变量与收敛条件 $\Re z<\sigma<1$）。
- **[事实] 奇异级数**：$S(N)\ge2C_2>1$（even N，因 p=2 的局部因子为 2，其余 ≥1 或 ∏(1−1/(p−1)²)）；$S(N)\ll_\varepsilon N^\varepsilon$（$N/\varphi(N)\ll\log\log N$）。**这两条保证 (3.12) 的主项 $NS(N)$ 严格大于误差 $N^{1-\omega+\varepsilon}$（对充分大 N）。**

### Step 6. Sharp weight：精确选 m+n=N（§3.5；p.18）

- **[事实] (3.19)–(3.24)**：取 $w(v)=e^{20(1-v)}(\sin\pi(v-1)/\pi(v-1))^2$（$w(1)=1,w(k)=0$ for integers $k\ge2$），$W(u,v)=u^{-\lambda}v^{-\mu}w(u+v)$，$0\le\lambda,\mu\le\omega$。则
  $$N^{-\lambda-\mu}\sum_{N\mid m+n}\Lambda\Lambda\,W=\sum_{m+n=N}\frac{\Lambda(m)\Lambda(n)}{m^\lambda n^\mu}.\tag{3.20}$$
  $W$ 的双重 Mellin 变换 (3.22) $=\frac{\Gamma(s-\lambda)\Gamma(t-\mu)}{\Gamma(s+t-\lambda-\mu)}\tilde w(s+t-\lambda-\mu)$，由 (3.21) 有 $|\tilde w(b+iy)|\ll e^{-|y|}$ 及 $|W(s,t)|\ll(1+|x|+|y|)^Ce^{-|x|-|y|}$（我们核对了指数衰减：$\Gamma$ 比值的指数与 $\sin^{-1}$ 的指数相消，$\tilde w$ 给出 $e^{-|x+y|}$；总体上对 $|x|+|y|$ 指数衰减，足以抵消 (3.3) 的 $e^{\pi T/2}$）。
  于是 (3.12) 给
  $$\sum_{m+n=N}\frac{\Lambda(m)\Lambda(n)}{m^\lambda n^\mu}=S(N)N^{1-\lambda-\mu}B(1-\lambda,1-\mu)+O_\varepsilon(N^{1-\omega+2\eta+\varepsilon}).\tag{3.24}$$
  （$F(k)=0(k\ge2),F(1)=B(1-\lambda,1-\mu)$；主项来自 $k=1$。）
- **[事实] 素数对计数（p.18）**：对 (3.24) 在 $[0,\omega]^2$ 上积分，主项 $=S(N)\int_0^NK_\omega(t)K_\omega(N-t)dt$；素数部分差 $O(N^{1-\omega})$；proper prime powers 贡献 $O(N^{1/2}\log^2(2N))$，被 $N^{1-\omega+\varepsilon}$ 吸收（因 $1/2\le1-\omega$，$\omega\le1/2$）。最终
  $$\#\{(p_1,p_2):p_1+p_2=N\}=S(N)\int_2^{N-2}\frac{dt}{\log t\,\log(N-t)}+O_\varepsilon(N^{1-\omega+2\eta+\varepsilon}).$$
  取 λ=µ=0 即 Theorem 1.1 的 von Mangoldt 形式。**(3.24) 的误差与 λ,µ 一致，积分不损失。**

### 小结：GRH 与 RC_D 的角色（[推导]）

| 输入 | 使用位置 | 必要性 |
|---|---|---|
| **GRH（primitive Dirichlet L，含 ζ）** | (2.21) 移到 ℜ=1/2+η；三线插值中的 (3.25) 多项式界与 $1/L$ 界；q=1/ζ 的 contour/residue；尾巴积分 | 不可少（当前证明） |
| **RC_D(ω_D)（Hypothesis 1.1）** | 仅用于 Lemma 3.1 中**分子在临界线、分母 ℜ=1/2+η、T≤100log(2q)** 的平均；之后通过三线插值/全纯性得到所有需要的移位平均 | 不可少；ω_D 任何固定正数都行 |
| **不需要** | 跨 χ 四阶零点相关、pair correlation、LL 的 R/S、算子范数估计 | **论文的 parity twist + primitive-conductor 求和 + Ratios 平均完全替代了它们** |

---

## 3. 最小自足假设 H_Ratios 的精确陈述

### 3.1 H_Ratios（可检验的干净形式；等价于论文 Hypothesis 1.1）

> **H_Ratios**。存在常数 $0<\omega_D\le1/2$、$\eta_0>0$、$B\ge0$，使得对每个 $0<\eta<\eta_0$、每个 $\varepsilon>0$、每个整数 $q>1$（复合导子允许），平均
> $$\sum_{\chi\bmod q}^{*}\frac{L(a,\chi)L(b,\bar\chi)}{L(s,\chi)L(t,\bar\chi)}=\mathcal M_q(a,b;s,t)+O_{\eta,\varepsilon}\bigl(q^{1-\omega_D+\varepsilon}(1+T)^B\bigr)$$
> 对所有移位
> $$\Re a=\Re b=\tfrac12,\quad \Re s=\Re t=\tfrac12+\eta,\quad T:=\max\{|\Im a|,|\Im b|,|\Im s|,|\Im t|\}\le100\log(2q)$$
> 一致成立，且误差在分子移位 $a,b$ 的固定半径圆盘上全纯。这里（令 $\varphi^*(q)=\#\{\text{primitive }\chi\bmod q\}$，$M_e(q)=\#\{\text{primitive }\chi\bmod q:\chi(-1)=(-1)^e\}$，$H_q(a,b)=\sum_{e=0,1}M_e(q)X_{q,e}(a)X_{q,e}(b)$，$X_{q,e}(w)=(q/\pi)^{1/2-w}\Gamma((1-w+e)/2)/\Gamma((w+e)/2)$）
> $$\mathcal M_q(a,b;s,t)=\varphi^*(q)Z_q(a,b;s,t)+H_q(a,b)Z_q(1-b,1-a;s,t),$$
> $$Z_q(a,b;c,d)=\frac{\zeta_q(a+b)\zeta_q(c+d)}{\zeta_q(a+d)\zeta_q(b+c)}A_q(a,b;c,d),\quad \zeta_q(s)=\zeta(s)\prod_{p|q}(1-p^{-s}),$$
> $$A_q(a,b;c,d)=\prod_{p\nmid q}\frac{(1-p^{-c-d})(1-p^{-a-d}-p^{-b-c}+p^{-c-d})}{(1-p^{-a-d})(1-p^{-b-c})}.$$
> （在可去奇点处取解析延拓。）

**定理 (GWX Thm 1.1)**：$\mathrm{H\_Ratios}+\mathrm{GRH}\Rightarrow$ 对每个 $\varepsilon>0$、所有充分大偶数 $N$，
$$\sum_{m+n=N}\Lambda(m)\Lambda(n)=N\mathfrak S(N)+O_\varepsilon(N^{1-\omega_D+\varepsilon})$$
（$\mathfrak S$ 为 (1.1) 的奇异级数；等价于 LL 的 $2C_2\prod_{p|N,p>2}(p-1)/(p-2)$）。取 $\omega_D=1/2$ 得 $O(N^{1/2+\varepsilon})$，故所有充分大偶数 Goldbach。

### 3.2 关于"任何 ω_D>0 都够"的复核（[推导]）

论文 §1.2 断言 "Any fixed ω_D>0 suffices for Theorem 1.1"。我们逐步核对：证明中有效 saving 是
$$\omega=\omega_D-8(\eta+r)(2+\omega_D)>2\eta;$$
只要 $\omega_D$ 固定正，取 η,r 足够小可使 ω>0 且 ω>2η；最终误差 $N^{1-\omega+2\eta+\varepsilon}$，再取 $\omega_D-\omega+2\eta<\varepsilon/2$ 得 $N^{1-\omega_D+\varepsilon}$。**任何固定 ω_D>0 确实足够；常数随 ω_D→0（和 ε→0）变差，但定理允许。**
**可弱化性 [推测/推导]**：若只要求定性 Goldbach（主项 $NS(N)$ 为正即可），可取 $\omega_D(q)\to0$ 但 $\omega_D(q)\log q\to\infty$（例如 $1/\log\log q$），使误差 $N^{1-\omega_D+o(1)}=N e^{-\omega_D\log N+o(\log N)}=o(N)$（只要 ω_D log N→∞，因为 q≤N 及 divisors 的 q 需一致；需对 q|N 的最坏 q=N 要求 ω_D(N)logN→∞）。H_Ratios 用**固定** ω_D 是最干净的形式；论文未讨论此弱化。

### 3.3 GRH 的最小形式

- 证明需要：(i) 对**所有** primitive χ（任意导子 q>1）在 ℜs>1/2 的零点不存在（GRH）以得 (2.21) 与 1/L 的 q^ε 界；(ii) ζ 的 RH（principal character q=1 的 contour/residue；GRH 通常包含 ζ，或显式加 RH）；(iii) 高度范围 |t|≤~100log q。**不需要 GRH 在 q,N 上的统一显式常数**（标准的 implicitly-uniform 版本足够；常数可依赖 ε,η0,B,ω_D）。
- 论文 footnote 1 说 Ratios 可以表述成不需要 GRH 的形式（如 Lee 的工作）；但本文 Goldbach 证明实际用了 GRH 的轮廓移动（§3.3, §3.6; (2.21)）。**H_Ratios+GRH 是论文实际使用的最小组合。**

---

## 4. Gap / 错误审计

### 4.1 唯一实质性的"额外输入"：复合导子的精确 parity-resolved 主项

- **[事实]** §3.6（pp.18–19）原文：
  > "For prime q, this uses the two terms of Wang–Xu [WX25, Conjecture 2.1], with the exact primitive parity counts in the archimedean coefficient. On the critical line, replacing the two counts by φ*(q)/2 changes that coefficient by O(1)… This removes the pole of the reflected kernel, and the change in the main term is O_{η,ε}(q^ε) at the logarithmic heights in Hypothesis 1.1. **The hypothesis uses the exact coefficient and covers composite conductors as well.**"
  > "Hypothesis 1.1 assumes the formula for all primitive conductors and specifies the exponent ω_D."
- **[推导] 评价**：这不是证明中的 gap（Hypothesis 1.1 明确把它作为假设），但它使 H_Ratios **强于**通常文献中"Ratios Conjecture for Dirichlet L-functions"的表述：
  1. **复合导子 q**：Wang–Xu [WX25] 只对素数导子表述 Ratios；论文把它外推到所有复合 q，并需要主项在复合 q 时仍由 Z_q/H_q 精确给出（包括精确的 $M_e(q)$ parity 计数，而不是 φ*/2 近似）。
  2. **精确 archimedean parity 系数**：H_q 需要精确的 $M_e(q)$；若只用 φ*/2 近似，$\Delta(q)$ 项和 $M_0X_0X_0-M_1X_1X_1$ 的分解会变，主项会改变；论文说变化为 $O(q^\varepsilon)$——相对于误差 $q^{1-\omega+\varepsilon}$ 是小的（ω≤1），所以**近似主项可能也够用**，但论文的假设采用精确形式。真正必须的是：**复合 q 的 Ratios 平均在临界线附近以 q^{1-\omega+\varepsilon} 的均匀误差成立，且主项与 CFZ recipe 一致**。
  3. **误差在分子移位上全纯**：用于 Cauchy/三线插值；Ratios 文献通常讨论误差大小但不一定强调全纯性；这里作为假设的一部分。
- **【结论/推测】** H_Ratios 是"Ratios 型"猜想（不是 ad hoc Goldbach 假设）：主项结构有 CFZ recipe 依据，prime q 情形有 WX25 文献支持，function-field 情形有 Sawin 等的 Ratios 结果作类比。因此这个额外输入是**可信但未被证明的**；它是本路线最脆弱、也是唯一非"论文内部可推导"的部分。

### 4.2 次要问题（不影响 Theorem 1.1）

1. **[事实] §3.4 qualitative sandwich 的次序草率**（pp.16–17）：在 cutoffs $f_\pm$ 的夹逼中，含有 $m<\delta N$ 或 $n<\delta N$ 的项；其相对主项的大小 ~$\delta\log N/S(N)$，需要 $\delta\log N/S(N)\to0$ 才能让 $\delta\to0$；论文写"letting δ→0 gives the qualitative asymptotic"没有说明 δ 可取 $(\log N)^{-1/2}$ 之类。**但 §3.4 只用于 qualitative formula (3.18)，Theorem 1.1 的 power-saving 证明在 §3.5 直接用 (3.12)+sharp weight，不经过 sandwich。** 因此这是 exposition gap，不是定理 1.1 的 gap。
2. **[事实] Theorem 1.1 "for every even N" 的渐近语义**：误差 $O_\varepsilon(N^{1-\omega_D+\varepsilon})$ 对小 N 无法 dominate；作为渐近陈述应读作"所有充分大 N（小 N 并入常数）"。常数可依赖 ε,ω_D,η0,B；论文 §1.2 说"implied constants may depend on fixed ratios parameters"。标准、无害。
3. **[事实] q=1/principal character**：Ratios 猜想本身不对 q=1 表述；论文用 ζ 的显式 contour/residue 处理 principal 项，并用 (1.9) 保证与 q=1 极点抵消。我们核对了 residue 的符号/因子：双重 residue $N^{2-\lambda-\mu}W(1,1)/\varphi(N)$ 与 q=1 积分的 residue（$N^{1-\lambda-\mu}\cdot N\cdot\tilde F(1)/\varphi(N)$，$\tilde F(1)=W(1,1)$）精确抵消 ✓（其中 W(1,1)=∫∫W(u,v)dudv 是双重 Mellin 逆变换约定下的值）。
4. **[事实] N 与 q 的耦合**：证明中只出现 q|N；Ratios 假设对所有 q>1 一致；高度 ≤100 log(2q) ≤100log(2N)。**不存在"q≫N"或隐藏的 N-q 耦合。**
5. **[推导] 奇异级数**：even N 时 $S(N)=2\prod_{p|N,p>2}\frac{p}{p-1}\prod_{p\nmid N,p>2}\frac{p(p-2)}{(p-1)^2}\ge 2C_2>1$；$S(N)\ll N^\varepsilon$（$N/\varphi(N)\ll\log\log N$）。故主项 $\ge 2C_2N$ 严格大于 $N^{1-\omega_D+\varepsilon}$（充分大 N）。N 多/少素因子都不影响（只影响常数/次主项）。
6. **[推导] 素数幂**：prime powers 对未加权计数贡献 $O(N^{1/2}\log^2(2N))$，误差 $N^{1-\omega+\varepsilon}$（$\omega\le1/2$ ⇒ $1/2\le1-\omega$）吸收 ✓。
7. **[推导] 未发现** contour/truncation 问题：三线插值的宽度 1/8、指数因子 8 已核对；有理权的 Gamma 衰减压住 $e^{\pi T/2}$；sharp weight 的 $w$ 是整函数、指数衰减，满足 (3.21)(3.22)；$W(s,t)$ 的指数衰减由 $\Gamma$ 比值与 $\tilde w$ 组合给出；$D_q$ 的 pole 只在 z=1（q>1 被 Euler 因子消去）、q=1 的 residue 精确抵消。

### 4.3 本报告的独立数值核对（[数值]）

| 恒等式 | 检查 | 结果 |
|---|---|---|
| (3.3) parity twist | q=5 的 primitive chars（quad,χ,χ̄），两组随机复数移位，直接算 L 值/Hurwitz zeta | 差 4×10⁻³¹ |
| (3.4) h₀−h₁ | q=7，两组 (a,b) | 差 10⁻³⁶ |
| (3.11) gamma 恒等式 | q=7，两组 (s,t) | 差 6×10⁻³⁶ |
| (2.12)/Prop 2.1 | N=6,12,30；h≤2N；S_q(h) 用 Euler 乘积（素数≤30000） | 最大相对误差 <5×10⁻³⁴ |
| S(N) (1.1) vs 2C₂∏ | N=30030,40022,60022 | 完全一致（到截断精度） |

脚本：`phase8/audit/check_gwx.py`、`phase8/audit/check_parity.py`。**这些检查覆盖了 parity twist/主项系数/奇异级数三处最易出符号错误的地方；未发现错误。**

---

## 5. 与 Li–Liu 的 H_Gold 比较

### 5.1 定义（[事实]）

- **LL H_Gold(ψ)**（phase-6 形式）：固定非零光滑对称 ψ∈C_c^∞((1/3,2/3))，对每个充分大偶数 N，
  $$G_\psi(N):=\frac1N\sum_{m+n=N}\Lambda(m)\Lambda(n)\psi(m/N)\psi(n/N)=c_\psi S(N)+O_\psi(\delta_N),\qquad \delta_N=\sqrt{S(N)/N}(\log N)^{3/2}.$$
  H_Gold(ψ)⇒Goldbach（主项正 ⇒ 至少一对表示）。
- **GWX H_Ratios+GRH** ⇒ 未加权 sharp 计数 $\sum_{m+n=N}\Lambda\Lambda=N\mathfrak S(N)+O(N^{1-\omega_D+\varepsilon})$，ω_D=1/2 时 $O(N^{1/2+\varepsilon})$。⇒ Goldbach。

### 5.2 强弱比较（[推导]/[事实]）

| | LL H_Gold | GWX H_Ratios+GRH |
|---|---|---|
| 结论对象 | 固定光滑权、沿 m+n=N 的加权和 | 未加权 sharp 计数 |
| 结论强度 | 光滑加权渐近（误差 $N^{-1/2}(\log N)^{3/2}\sqrt S$） | 未加权 sharp 渐近（误差 $N^{-1/2+\varepsilon}$） |
| 是否 ⇒ Goldbach | 是（正主项 ⇒ 至少一对） | 是（误差<主项） |
| 假设性质 | ad hoc Goldbach-强度假设（LL 的 R/S 是算子范数猜想） | 标准型 Ratios 猜想（需复合导子+精确 parity 主项强化）+ GRH |
| 已知蕴含 | 不显然 ⇒ sharp count；也未被 H_Ratios 蕴含（光滑权 vs sharp count） | 不显然 ⇒ H_Gold；也未被 H_Gold 蕴含 |
| 文献基础 | 无（新概念） | Ratios Conjecture（CFZ08；WX25 素数导子；function field/Sawin）；GRH 若 Alpöge 成立可兑现 |

- **[推导] 不等价**：sharp count 与光滑加权 count 是不同统计量；彼此没有已知的、无额外损失（如显式 interval 均匀性）的蕴含。**两者都 ⇒ Goldbach，但已知不互推。**
- **[推测] 假设可信度**：H_Ratios 是"一个标准族猜想的加强版"，而 LL 的 R/S/H_Gold 是 ad hoc 的 Goldbach-强度假设。**GWX 路线在"归约到已知猜想族"的意义上明显更优；这也是 lead 判断"当前最有希望路线"的根据，我们的审计支持这一点。**
- **注意**：H_Ratios 的复合导子精确主项是"标准 conjectures 之外"的强化；若未来发现复合 q 的 M_q 系数不对，GWX 路线需要修正（但机制本身仍可能通过 φ*/2 近似/修正主项保留，因为主项误差 O(q^ε) 相对 q^{1−ω+ε} 是小的）。

---

## 6. 裁决与建议（给 Lead）

1. **【裁决】Theorem 1.1（modulo 预印本）是一个正确的条件性归约。** 我们逐步重建了证明（奇偶 twist→Ratios 插值→有理权 Mellin→加权和恒等式→sharp weight→素数对），核对了所有纯代数恒等式（数值到 1e−31~1e−36），未发现致命错误。**它不是"LL 路线的变形"，而是完全不同的机制：不需要 LL 的 R/S、不需要跨 χ 四阶零点相关、不需要算子范数；所有相关性被 Ratios 猜想的平均吸收。**
2. **【最难缺的单一输入】**：H_Ratios —— **对所有 primitive 复合导子一致、带精确 parity-resolved 主项、误差 q^{1−ω_D+ε}（任何固定 ω_D>0，最好 1/2）、对分子移位全纯、高度至 100log(2q) 的 Ratios 猜想**。prime q 情形有 Wang–Xu [WX25]；复合 q 的精确主项是外推（§3.6 作为假设），是整条路线最脆弱、也是唯一非论文内部可推导的部分。若 H_Ratios 成立、GRH 由 Alpöge/Claude 兑现，则 Goldbach 对所有充分大偶数成立。
3. **【与 LL 比较】**：H_Ratios+GRH 与 H_Gold 不可互推；前者终点更强（sharp count）、假设更"主流"；后者是 ad hoc 光滑加权假设。**建议把 GWX 路线作为主攻方向**：
   - 近期可做：(a) 核查/形式化复合导子的 M_q 系数（从 CFZ recipe / function-field 类比 / WX25 的 prime 情形推广）；(b) 明确 H_Ratios 在文献中的最强已知形式（WX25 的 prime conductor 版本、Conrey–Farmer–Zirnbauer、Sawin 的 function field 结果），评估复合 q 的难度；(c) 尝试用 Alpöge 的 GRH formalization 兑现 GRH 部分（如果验证通过）。
   - 不建议再投入 LL 的 R/S（除非有新的算子想法）；LL 的精确恒等式仍是有趣的框架，但其谱假设是非标准的、且 phase-6 的密度-1 分析表明即使成立也不能省去全 N 要求。
4. **[推测] H_Ratios 的可信度**：作为 Ratios 猜想的加强版，它比 LL 的 R/S 更"有据可依"（有 WX25 素数情形、CFZ recipe、function field 类比）；但 over Q 的 Ratios Conjecture 本身是深猜想（目前没有任何族的完整证明，除 function field 情形）。**因此 GWX 路线把 Goldbach 归约到一个深但标准的猜想上——这是目前最干净的归约，但仍不是无条件证明。**

---

## 7. 引用（逐字/公式号）

**GWX 原文**（本地 `phase7/lit/gwx.pdf` / `gwx_pdf.txt` / `gwx.txt`）：
- Hypothesis 1.1（p.2）；Theorem 1.1（p.3）；(1.3)。
- §1.2 "Any fixed ω_D>0 suffices for Theorem 1.1."（p.3）。
- §1.4 Goldbach 证明概述（p.4）。
- (3.1)（p.12）；(3.2) Lemma 3.1（p.13）；(3.3)(3.4)（p.13）；(3.5)–(3.7)（pp.13–14）；(3.8)（p.14）；(3.10)(3.11)（p.14–15）；(3.12)（p.15）；(3.13)（p.16）；(3.14)（p.16）；(3.18)（p.17）；(3.19)–(3.24)（p.18）；§3.6（pp.18–19）；Prop 2.1 (2.11)(2.12)（p.7）；(2.21)（p.11）；Appendix A（p.39）；footnote 1（p.1）。
- 论文 URL：arXiv:2611.18825（<https://arxiv.org/abs/2611.18825>）。

**外部文献**（本报告引用/对照）：
- J. B. Conrey, D. W. Farmer, M. R. Zirnbauer, *Autocorrelation of ratios of L-functions*, arXiv:0708.2575（CFZ08，Ratios Conjecture）—— 论文引用 [CFZ08]。
- V. Y. Wang, M. W. Xu（WX25），论文引用：prime conductor 的 Ratios Conjecture 2.1。
- W. Sawin 等 function-field Ratios 进展（论文引用 [Saw24] 等）。
- 若需判断 GWX 与 LL 的 GRH 共享：LL 所需 GRH(N) 即 primitive Dirichlet L（导子整除 N）的标准 GRH，与 GWX 的 GRH 相同层级；Alpöge/Claude Lean 证明（若验证）可同时兑现两者（MIT 验证页 <https://math.mit.edu/~drew/grh/>）。

---

## 8. 复现与文件

- 报告：本文件。
- 数值核对脚本：`phase8/audit/check_gwx.py`、`phase8/audit/check_parity.py`；运行 `python3 check_gwx.py`（mpmath，~1 分钟内）。
- 论文全文（只读引用，未修改）：`phase7/lit/gwx.pdf`、`gwx_pdf.txt`、`gwx.txt`。
- 本报告未重跑论文的解析证明（人手逐步核对）；数值核对只覆盖代数值恒等式（(3.3),(3.4),(3.11),(2.12),(1.1)），不覆盖 Ratios 猜想的真假。

### 附录：一句话总结

> GWX Theorem 1.1 的证明是**正确的条件性归约**：GRH 只用于轮廓移动/零点自由界，核心算术输入是**对所有 primitive 复合导子一致、带精确 parity-resolved 主项的 Ratios 猜想（H_Ratios）**；它与 LL 的 H_Gold 不等价（前者给 sharp 未加权计数、后者给光滑加权计数），但在"归约到标准猜想族"意义上 GWX 路线明显更优。当前 Goldbach 最缺的单一输入 = H_Ratios；GRH 可能已被 Alpöge/Claude 的 Lean 证明兑现（待验证），而 H_Ratios 仍是未证明的深猜想。
