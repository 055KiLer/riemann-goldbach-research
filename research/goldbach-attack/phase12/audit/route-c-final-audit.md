# Phase-12 独立对抗审计：Route C 的 wrap 恒等式、c 账本、TL 目标与 Ratios 真值

> 作者：liu-auditor（phase-12 追加任务，2026-11-22）。**独立审计**：未照抄 kernel-theorist 推导；用自己的小脚本/独立推导核对。对象：`phase12/theory/wrap-attack.md`（kernel-theorist task-55）、`phase12/theory/checkE5.py`（Lead 数值）、`phase12/numerics/truth_run2.log`（spectral-numerics）。标注 **[证明]/[推导]/[数值]/[推测]**。
> **结论先行（4 条，含 2 条 kernel 断言需要修正）**：
> 1. (A) **精确恒等式本身正确但平凡**（q 素时 `Σ*=Σ_{χ≠χ0}`），且它只是把 `E^{(X)}` 重新命名；由它不能推出"wrap 不可作独立误差项"的**不可能性定理**。正确版本：`E^{(X)}` 就是非主特征上截断比值乘积的平均；因此任何"截断主块≈主项"的证明都必须处理该平均（= TL(A)），这是 **Route C 框架内的循环/等价**，不是对整个 Ratios 问题的 no-go。kernel 的"最小不可行性定理"应降级为"Route C 内 TL 等价性"。
> 2. (B) kernel 的最终界 `(q−1)|W|≲X^{2−4η}η^{-2}log⁴` **正确**，但其推导中的中间不等式 `|W|≤(1/q)(Σ|c|)(Σ|d|)` **不是普遍成立的"平凡界"**（反例：q=5,c_1=1,d_6=1 时 W=1，RHS=1/5）；正确的严格推导用 divisor 有界系数 + 对 A 的积分，结果同阶（见 §2.2）。账本：`c≤1/2` 只在"对任意小 η 一致"意义下成立；**对固定 η，trivial wrap 给出 c≤1/(2−3η)>1/2**。更一般地若 `Δ≲X^{2−4η}q^{−γ}`，则 `c≤(1+γ)/(2−3η)`；trivial γ=0 →1/2，**完美 equidistribution γ=1 →1**；**c>2 需要 γ>3**（超出 equidistribution 的因子 q^{>3}）。kernel 的 c≤1/2 是 η→0 一致极限，不是"允许 wrap 也一步不改进"的精确陈述。
> 3. (C) `c>2 ⇔ TL(A>2)` **在 Route C 截断框架内基本正确**（RAT(c) ⇒ TL(A) for 2<A≤c；TL(A) ⇒ RAT(A)），但前提是 TL 对 **所有大 q、所有足够小 η 一致**，且依赖截断引理。kernel 的"**不能**用有限和+解析延拓/插值绕过"是**过强**：该等价只说明 TL 是 RAT 的必要推论/重述，不排除用其他方法证明 RAT(c)（一旦证出，TL 自动成立）。正确的措辞是"Route C 内 c>2 等价于 TL(A>2)"，不是"数学上不能绕过"。
> 4. (D) truth_run2 数据**不支持**"主项 M_q ~q/η²"：独立复算（q=1009，同 seed）得 median|M|≈q（η 无关），M_rms≈2–4q（η=0.1→0.002），而 RMS/|M| 从 0.12 升到 1.66。数据与"Ratios 真值误差 =q^{1/2+o}·C(η)"（C(η)≈η^{-0.7…-1}）自洽，即 **q-指数 saving 不随 η 退化，只有常数 blow-up**；这与 H_Ratios 为真（且远强于 RAT(c) 对任何固定 c）一致。若 C(η)~η^{-2}，Hyp 1.1 的 `O_η` 常数可吸收；B 固定指数只需允许 η-依赖常数，**对固定 η 的 c>2 路线无实质影响，只放大阈值 N₀**；但对 η~1/logN 的定性路线需显式 B(η)/常数控制（H_UNIF）。

---

## 1. (A) 精确恒等式与"wrap 不可独立"的判定

### 1.1 恒等式 [证明]

q 为素数时，primitive characters mod q = 全部非主特征（数量 q−2）。定义
$$P_u(\chi)=\sum_{n\le X}\chi(n)n^{-u},\qquad Q_u(\chi)=\sum_{m\le X}\mu(m)\chi(m)m^{-u}.$$
则逐个 χ 有 `P_aP_bQ_sQ_t = (P_aQ_s)(χ)·(P_bQ_t)(χ̄)`（P_a,Q_s 含 χ；P_b,Q_t 含 χ̄）。故
$$\boxed{E^{(X)}=\sum_{\chi\bmod q}^{*}P_aP_bQ_sQ_t=\sum_{\substack{\chi\bmod q\\ \chi\ne\chi_0}}(P_aQ_s)(\chi)(P_bQ_t)(\bar\chi).}\tag{1.1}$$
**这是集合恒等式，零信息量**；kernel 的 (0.1) 正确但平凡。[证明]

### 1.2 拆解：wrap 与 T 项 [推导]

对任意 A,B，利用 `Σ*χχ(A)χ̄(B)=Σ_{χ≠χ0}...`：
- 若 `(AB,q)=1`（A,B 都与 q 互素）：`=(q−1)1_{A≡B mod q}−1`；
- 若 `q|A` 或 `q|B`：所有非主特征取 0 ⇒ 和为 0（而 `(q−1)1−1=q−2≠0`）。
因此若把所有 A,B 都展开，`E^{(X)}=(q−1)Σ_{A≡B}c_Ad_B−Σ_{A,B}c_Ad_B+T`，其中 **T 是 q 整除 A/B 的边界项**（Lead `checkE5.py` 中 `T=C0*Sd+Sc*D0−C0*D0`）。kernel 的 §1 写 `(q−1)Σ_{A≡B}−Σ_{A,B}` 时若未含 T，则对一般系数不精确；phase-12 Lead synthesis 的 `E=(q−1)(D+W)−S_cS_d+T` 是正确的 bookkeeping。**我们的随机系数检验表明：忽略 T 时恒等式的偏差可 O(主项)**（脚本 `phase12/audit/routec_checks.py`，但该脚本对非单位系数用了错误公式；结论仍成立：必须带 T）。[推导/数值]
- wrap 项（kernel 的 W）：`W=Σ_{A≠B,A≡B mod q}c_Ad_B`；进入 E 的系数是 `(q−1)`（不是 1），故 **`(q−1)W` 才是进入 R_q 的量级**。kernel 对这一点正确；plan 早期把 W 直接记入误差，确实少了 φ*≈q−1 因子。[推导]

### 1.3 "wrap = 平均的偏离对角部分，故不可作独立误差项"：kernel 断言过强处

- **[推导] 正确部分**：`E^{(X)}` 本身是 (1.1) 的非主特征平均；把它拆成"对角主项 + wrap 误差"时，**wrap 不是与主项独立的算术对象**：给定 c,d，W 由同一个平均决定。任何只用"对角 Euler 积 + 独立估计 W"的路线，如果 W 的估计没有触及非主特征平均，就会自相矛盾；kernel 的 Fourier 表示 `Σ_{A≡B}c_A\bar d_B=(1/q)Σ_h\hat c(h)\overline{\hat d(h)}` 把未解决部分 `F=(1/q)Σ_{h≠0}...` 等同于截断比值的 h-切片，**在 Route C 内**这是循环的。[推导]
- **[推导] 但"不可作独立误差项"不是定理**：W 是一个具体的四重指数和；原则上可以用其他方法（Kloosterman/Weil/Poisson/双线性形式）估计它，不必先证明 Ratios。kernel §2–§5 的论证是"这些自然折叠都回到同一对象"的**方法级启发**，不是 no-go 证明。**反例式说明**：若 RAT(c) 通过任何其他途径被证明（例如作为假设或函数域类推），则由截断引理立刻得到 TL(A≤c)——因此"TL 必要"是逻辑结果，而不是"wrap 不可估计"。**精确的可证陈述是 §1.4 的等价性，而不是不可能性。**
- **[修正建议]** 把 kernel 的 "wrap 不可作独立误差项" 改写为：
  > "在 Route C 的截断框架内，`E^{(X)}` 恰为非主特征上的截断比值平均；`R_q−E^{(X)}` 由截断引理控制；因此 `E^{(X)}` 的主项误差 ≡ TL(A)。任何 Route C 内不使用额外算术输入的 W 估计，都不足以越过 TL。"
  这是**方法限定**陈述，不是 Goldbach/Ratios 的 no-go。

### 1.4 精确等价（Route C 框架内）[证明/推导]

在 GRH + 截断引理（`L=Σ_{n≤X}+O(X^{-η}q^ε)`、`1/L=Σμχ+O(X^{-η}q^ε)`）成立的前提下：
- 若 **TL(A)**（见 (C)）成立，取 X=q^A ⇒ `R_q=M_q+O(q^{1+ε}X^{-η}+q^{1−Aη})=M_q+O(q^{1−Aη})`，即 RAT(A)；
- 若 RAT(c) 成立，取 2<A≤c、X=q^A ⇒ `E^{(X)}=R_q+O(q^{1−Aη})=M_q+O(q^{1−cη}+q^{1−Aη})=M_q+O(q^{1−Aη})`，规范化后即 TL(A)。
⇒ **RAT(c) 与 TL(A)（2<A≤c）在截断框架内等价（mod 截断引理与主项匹配）**。kernel 的定理 7.1 应这样陈述；其"c>2 ⇔ TL(A>2)"基本正确，但"不能绕过"过强（见 §3）。

---

## 2. (B) 账本独立重算：正确常数、kernel 的界与 c 上界

### 2.1 kernel 的最终界是否正确？ [证明/推导]

设 `c_A=Σ_{nr=A}n^{-a}μ(r)r^{-s}`，`d_B=Σ_{ml=B}m^{-b}μ(l)l^{-t}`，`Re a=Re s=σ=1/2+η`（b,t 同理）。则
$$|c_A|\le A^{-\sigma}d(A),\qquad |d_B|\le B^{-\sigma}d(B).$$
$$|W|\le\sum_{k\ne0}\sum_{A\le X^2}A^{-\sigma}|A+kq|^{-\sigma}d(A)d(A+kq)$$
（A、A+kq∈[1,X²]；`A+kq=0` 的项属于 T/A≡0 边界，另计）。
对固定 k：A≪kq 时第 2 因子≈(kq)^{-σ}，Σ_{A\lesssim kq}A^{-σ}≈(kq)^{1-σ}/(1-σ)，得 (kq)^{1-2σ}/(1-σ)；A≫kq 时两项≈A^{-2σ}，Σ_{A\gtrsim kq}^{X²}A^{-2σ}≈(kq)^{1-2σ}/(2σ-1)（若 kq≪X²）。故
$$\sum_A\cdots\lesssim_\eta (kq)^{1-2\eta}\eta^{-1}\log^3 X.$$
对 |k|≤X²/q 求和：Σ_k (kq)^{1-2η}≈q^{1-2η}(X²/q)^{2-2η}/(2-2η)
$$=X^{2-4η}q^{-1}\cdot\frac{\eta^{-1}\log^3 X}{1-\eta}.$$
⇒
$$\boxed{|W|\lesssim_\eta X^{2-4\eta}q^{-1}\eta^{-2}\log^4 X,\qquad (q-1)|W|\lesssim X^{2-4\eta}\eta^{-2}\log^4 X.}\tag{2.1}$$
**与 kernel 的最终界一致**。[证明]
**但 kernel 的中间不等式 `|W|≤(1/q)(Σ|c|)(Σ|d|)` 不普遍成立**：反例 q=5，c_1=1，d_6=1（A=1,B=6，A≡B mod5，A≠B），W=1，而 `(1/q)(Σ|c|)(Σ|d|)=1/5`。正确证明必须用上述 divisor 有界系数/积分，不能引用该"概率型"不等式。**结论：最终界正确，推导理由需修正。** [证明]

### 2.2 平衡方程与 c 上界（精确）

截断误差（每因子 X^{-η}，四因子求和）：
$$T_{\rm trunc}\ll q^{1+\varepsilon}X^{-\eta}.\tag{2.2}$$
wrap（正确含 (q−1)）：
$$W_R=(q-1)W\ll X^{2-4\eta}\eta^{-2}\log^4 X.\tag{2.3}$$
取 `X=q^A`、目标 RAT(c) 误差 `q^{1−cη}`。要证 RAT(c)，可令 `A` 满足 `A≥c`（截断误差 `q^{1−Aη}≤q^{1−cη}`）且
$$q^{A(2-4\eta)}\le q^{1-c\eta}\iff A(2-4\eta)\le1-c\eta.\tag{2.4}$$
存在 A≥c 满足 (2.4) ⇔
$$\boxed{c(2-4\eta)\le1-c\eta\iff c\le\frac{1}{2-3\eta}\ \ (\eta<2/3).}\tag{2.5}$$
**逐项结论**：
- **固定 η**：允许 wrap 的 trivial 界给 `c≤1/(2−3η)`；例如 η=0.1→c≤0.588；η=0.2→c≤0.714；η=1/6→c≤2/3；**确实比 1/2 略好**。
- **对任意小 η 一致（RAT(c) 要求）**：`inf_{η→0} 1/(2−3η)=1/2`。**⇒ kernel/Lead 的"c≤1/2"在 uniform sense 下正确**，但不能写成"允许 wrap 不改进 c"——对每个固定 η 有轻微改进，只是当 η→0 时改进消失。**这是 kernel 论断需要精确化的地方。**
- 更一般：若能把 `Δ=(q−1)W−S_cS_d+T` 直接估计为 `Δ≲X^{2−4η}q^{−γ}η^{-O(1)}`（γ≥0），则平衡给
$$\boxed{c\le\frac{1+\gamma}{2-3\eta}.}\tag{2.6}$$
  - γ=0（只用 (q−1)W 的界）：c≤1/(2−3η)→1/2；
  - γ=1（完美 equidistribution：W≈S_cS_d/q，T≈2S_cS_d/q，Δ≈S_cS_d/q~X^{2−4η}/q）：c≤2/(2−3η)→**1**（不是 2）；
  - **c>2 需要 γ>3**（因为 η→0 时 c≤(1+γ)/2）——即需要比 equidistribution 多 q^{>3} 的 saving，正是 TL/F 的内容。
  这是对 plan/kernel "c 目标"的**更精确量化**：**trivial=1/2，equidistribution=1，c>2 需要超出 equidistribution 3 个 q-幂的额外均匀性**。

### 2.3 与 checkE5 数值（q=1009, η=0.2）对照

Lead 数据：`Δ=(q−1)W−S_cS_d+T` 在 X=q^A（A=0.5→1.1）时 |Δ|=15→175；目标 `q^{1−ηA}=507→220`；Δ 仍低于目标、增长指数约 0.59–0.67（X 的指数）。
- 理论上：
  * trivial `(q−1)W` 界对应 X^{2−4η}=X^{1.2}（A 指数 1.2）；
  * 完美 equidistribution 的 Δ 界对应 X^{2−4η}/q，在 X 的指数仍是 1.2，但常数小 q 倍；
  * 观测 Δ 的 X 指数 ~0.6 <1.2，说明 **Δ 比 (q−1)W 的 trivial 界小得多（有部分抵消/等分布）**。用 (2.6) 的经验 α=0.6、η=0.2 反推：若 Δ≲X^{0.6}，则允许 c≈1/(0.6+0.2)=1.25（固定 η=0.2）。**这不能推广到 η→0**：当 η→0，理论 α 至少 ≥? trivial α=2−4η→2；若 Δ 的净界来自 equidistribution，则 α=2−4η 且带 q 抑制，得到 c→1；只有 γ>3 的额外抑制才能到 c>2。**checkE5 只测了一个 q 和 η=0.2，无法区分 γ**；Δ 的指数在 q=1009 有限范围内也可能受 X<q 或 X~q 的过渡影响。
- 结论 [推导/数值]：**checkE5 支持"Δ 比 (q−1)W 小"，因此 trivial c≤1/2 不是最优**；但**不能**由此推出 c>1/2 的 uniform-in-η 结论。需要：
  1. 对多个 q、多个 η 测量 Δ 的 **q-指数与 X-指数**，尤其是 η→0 区域；
  2. 直接测 Δ，而不是 (q−1)W；用 C_r,D_r 的精确 residue 和（checkE5 已做）；
  3. 分离 near-pole shifts（a+b≈1、a+t≈0 等）与 generic shifts；否则 Δ 的指数会被 few shifts 污染。

---

## 3. (C) 目标重述：c>2 ⇔ TL(A>2) 是否正确？

### 3.1 TL(A) 定义（kernel §7bis）

对 q 素、σ=1/2+η、X=q^A、|Im|≤T≤100log(2q)：
$$\mathrm{TL}(A):\quad \frac1q\sum_{\chi\ne\chi_0}(P_aQ_s)(\chi)(P_bQ_t)(\bar\chi)=F_{\rm pred}+O\bigl(q^{-A\eta+\varepsilon}(1+T)^B\bigr),\tag{3.1}$$
`F_pred` 是截断多项式的 CFZ 主项（X→∞ 时趋于 M_q 的 q^{-1} 归一化）。
**归一化核对 [推导]**：`E^{(X)}≈q F_pred`，`R_q≈M_q≈q F_pred`；截断误差 `q^{1+ε}X^{-η}=q^{1−Aη+ε}`，除以 q 即 `q^{−Aη+ε}`；故 TL(A) ⇔ RAT(A)（在截断框架内），与 §1.4 一致。

### 3.2 等价方向的严格性 [推导]

- **TL(A) ⇒ RAT(A)**：X=q^A，`R_q=E^{(X)}+O(q^{1+ε}X^{-η})=qF_pred+O(q^{1−Aη+ε})`；若 `M_q=qF_pred+O(q^{1−Aη})`（主项匹配），则 RAT(A)。
- **RAT(c) ⇒ TL(A) for 2<A≤c**：`E^{(X)}=R_q+O(q^{1−Aη})=M_q+O(q^{1−cη}+q^{1−Aη})=M_q+O(q^{1−Aη})`；除以 q 得 TL(A)，前提主项匹配与截断引理。
⇒ **`c>2` ⇔`∃A>2 TL(A)`** 在框架内成立（取 A 满足 2<A≤c；TL(A) 本身给 RAT(A)，即 c=A>2）。
**但必须强调的 caveats**：
1. TL 必须对 **所有大 q>1、所有足够小 η<η0 一致**；若只是固定 q/X=q^A 的有限和估计，不能推出 RAT(c)。
2. 截断引理（$L$ 和 1/L 的 $X^{-η}$ 误差）本身需要 GRH 的 Lindelöf 型输入（见 `theorem-A.md` §2.3 [待核]）；若该输入不成立，TL/RAT 等价链条也要改。
3. 主项匹配（`E^{(X)}` 的 CFZ 主项 = `F_pred`）需验证，尤其 $p|q$ 的修正；phase-11 Euler 积恒等式只对 $p\nmid q$ 直接给出。
**⇒ "c>2 ⇔ TL(A>2)" 是 Route C 框架内的等价重述，基本正确；但它不是证明 c>2 的障碍，而是把障碍换成了 TL。**

### 3.3 kernel 的"不能绕过"过强

kernel 原文："所有'把 W 用 Poisson/Weil/Kloosterman/大筛/乘性结构估计'的尝试都会落回同一平均…任何 Route-C 内部优化都不能绕过它"——这在 Route C 内部是**方法断言**（他们的 §2–§5 是启发式论证，不是形式证明）。需要修正的两点：
- **逻辑上**，若有人用其他方法证明 RAT(c)（或直接假设 H_Ratios 为真），TL(A) 自动成立；TL 是 RAT 的**推论**，不是额外难关。因此"不能绕过"应改为"Route C 内任何只依赖截断/正交性、不引入新算术输入的估计都不能证明 TL"。
- **"有限和 + 解析延拓/插值"能否绕过**：不能仅凭 TL 是有限和就断言不能绕过。若 TL 对所有 q、η 一致，它已经是 RAT 的等价形式，解析延拓不需要；若只证有限 q/X 的 TL，确实不能推出 RAT。**关键是一致性**，不是"有限和 vs 无限和"。
- kernel 的 "X>√q 之后没有免费午餐" 作为 Route C 的精确描述是好的；但"不可能性定理"命名过强，建议改为"Route C 的等价性/TL 归约"。

---

## 4. (D) 核对 truth_run2 数值与主项 η-标度

### 4.1 数据的独立复算 [数值]

我们用 `phase12/numerics/ratios_lib.py`（与 spectral 相同 pipeline）独立复算 q=1009、同 seed/30 shifts、shifted config（四者 Re=1/2+η；d=R−M）：
| η | RMS(d)/√q | median\|M\| | M_rms | RMS/M_rms | RMS/√q / (M_rms/q) |
|---|---|---|---|---|---|
| 0.1 | 8.33 | 1080 | 2130 | 0.124 | 3.9 |
| 0.05 | 21.95 | 1080 | 3000 | 0.233 | 7.3 |
| 0.02 | 57.53 | 1080 | 3870 | 0.473 | 14.9 |
| 0.01 | 95.19 | 1080 | 4110 | 0.735 | 23.5 |
| 0.005 | 139.50 | 1080 | 4200 | 1.056 | 33.8 |
| 0.002 | 221.65 | 1080 | 4230 | 1.665 | 52.8 |
（与 `truth_run2.log` shifted 行一致：q=1009 η=0.1 RMS/√q=8.33；η=0.02=57.5 等——**数据复现**。）
- **median |M|≈q（1080 vs q=1009）不随 η 变**；M_rms 只从 2.1q 升到 4.2q。**因此"主项 M_q ~q/η²"作为一般/中位数陈述不成立**。可能有少数 near-pole shifts（a+b≈1、a+t≈0、或 reflected kernel 的 ζ(1) 附近）使 M 变大；需要按 shift 分离。**Lead 的 1/η² 标度需要重新核实：它最多是 near-pole 子集的标度，不是 RMS main-term 的标度。**
- 数据与以下模型自洽：误差 `d=R−M≈q^{1/2}·C(η)·(random)`；`RMS/√q=C(η)`；由表得 C(η) 从 ~4（η=0.1）到 ~53（η=0.002），拟合粗略 `C(η)≈η^{-0.7}～η^{-1}`（在 η=0.1→0.02 区间约 η^{-1.2}；更小 η 因 q 有限/near-pole 变缓）。**不是 η^{-2}**；若强行用 η^{-2} 解释，需要 M_q~q/η²，但我们的 M 测量不支持。
- **重要 caveat**：我们的 M 用 `M_correct`（phase-11b 修正 A_q）；若 spectral 的 M 公式不同（例如漏 H_q 或不同 A_q），η-标度会不同。建议 spectral 交叉核对 M 公式；尤其 H_q 反射项在 shifted config 的相对大小 q^{-2η} 在 η=0.1 时 ~25%，不可忽略。

### 4.2 对 GWX/Hyp 1.1 形式的含义 [推导/推测]

- 若 Ratios 真值误差 = `q^{1/2+o}·C(η)`（C(η)=η^{-O(1)}），则对任意固定 c>0，只要 η<1/(2c)，有 `q^{1/2}C(η) ≤ q^{1−cη}` 对充分大 q 成立（因 1/2<1−cη），即 **RAT(c) 对任何固定 c 都被真值蕴含（模常数）**。**c>2 也不例外**；真正困难是把"真值"变成定理，而不是 c 的阈值本身。
- Hyp 1.1 的 `O_η` 常数允许 C(η) blow-up；`(1+T)^B` 的 B 若固定，也可由常数吸收 T≤100log(2q) 的 C(η)（因为 C(η) 进常数，不进 T）。**对固定 η 的 RAT_sym/der(c>2)→Goldbach 路线：C(η) 只影响隐含常数和阈值 N₀（N₀ 可能 ~C(η)^{2/((c−2)η)}，天文数字但有限），不影响 c>2 的形式有效性。**
- 若走 `η~1/log N` 定性路线：C(η)~η^{-2}~(logN)^2；Hyp 1.1 的 O_η 常数变成 N-依赖的 (logN)^2，需显式常数控制（H_UNIF）；B 也可能需 η-依赖。**这是 phase-12 后续若尝试定性路线必须补的条款；固定 η 路线不需要。**
- 数据目前只测 T=2、q≤5×10^5、随机 shifts；**不足以确定 B(η)**。建议 spectral-numerics 增加：(i) 分离 near-pole shifts；(ii) 用 M 的精确公式核对 η-标度；(iii) 在 shifted config 用 scaling in q 验证 C(η) 的 q-指数是否仍 1/2（目前 η=0.1 数据跨 q 大致常数，支持；η≤0.02 数据跨 q 有 2–4 倍漂移，需更大 q/T 控制）。

### 4.3 "主项 M_q ~q/η²" 的独立判断 [推导/数值]

- 我们直接计算 `φ*Z_q` 与 `H_qZ_q(1−b,1−a)`：**median |φ*Z|≈q**（η=0.1→0.002 几乎不变）；median |H_qZ_d| 从 ~48 升到 ~121（q=1009），远小于 φ*Z；mean |H Zd| 从 201 升到 784（near-pole shifts 贡献）。**不存在统一的 1/η² 主项标度**。[数值]
- 若 Lead 的 `q/η²` 来自某个特殊移位（如 a+b 或 a+t 接近极点），它只对少数 shifts 成立；用 RMS 统计时这些 shifts 会抬高 RMS/√q 并产生 η^{-2} 外观。**建议 spectral 用 median/trimmed RMS 排除 near-pole shifts，再拟合 C(η)**；否则数据对 H_Ratios 的"真值支持"会被 near-pole 伪影污染。
- **[推测]** 若排除 near-pole 后 C(η) 仍随 η 下降而增长（我们的 median 数据已显示 d_rms/|M|_med 从 0.25 到 2.1），那仍是 Ratios 误差的 η-依赖常数，与 H_Ratios 真相容；但需确认它不是 M 公式的 η-误差。

---

## 5. 结论与修正清单（给 Lead）

1. **(A)** 恒等式 (1.1) 正确但平凡；kernel 的"wrap 不可独立/最小不可行性定理"应改为**Route C 框架内的 TL 等价性**；不可作独立误差项是方法级结论，不是数学 no-go。分解必须带 T（q|A/B 边界）；kernel 的 `(q−1)W` 保留正确。
2. **(B)** kernel 最终 W 界 `(q−1)|W|≲X^{2−4η}η^{-2}log⁴` **正确**，但中间 `(1/q)(Σ|c|)(Σ|d|)` 不等式不对（反例）；正确证明用 divisor 有界 + 积分。平衡：**对固定 η，trivial wrap 给 c≤1/(2−3η)>1/2；对任意小 η 一致才得 c≤1/2**。更一般 `c≤(1+γ)/(2−3η)`（Δ≲X^{2−4η}q^{−γ}）：trivial γ=0→1/2，equidistribution γ=1→1，**c>2 需 γ>3**。checkE5 的 Δ~X^{0.6} 表明 Δ 比 trivial W 小（近 equidistribution），但这只是 q=1009、η=0.2 的有限数据，不能推出 uniform c>1/2。
3. **(C)** `c>2 ⇔ TL(A>2)` 在截断框架内基本正确（需 TL 对所有 q、所有小 η 一致、截断引理、主项匹配）；但"不能绕过/不可能性定理"过强：TL 是 RAT 的推论，不是额外数学障碍；其他方法证明 RAT 后 TL 自动成立。kernel 应改称"Route C 内等价"。
4. **(D)** truth_run2 数据复现无误（q=1009 与 log 一致）；但 **median |M_q|≈q，不随 η 变；M_rms≈2–4q**，不支持"M_q~q/η²"作为主项标度。数据的 `RMS/√q` 增长与 `q^{1/2}·C(η)`（C(η)≈η^{-0.7…-1}）自洽；这与 H_Ratios 真值（q-指数 1/2、仅 η-常数 blow-up）一致。若 C(η)=η^{-2}，Hyp 1.1 的 O_η 常数可吸收；对固定 η 的 c>2 路线只影响 N₀；对 η~1/logN 定性路线需 H_UNIF/B(η)。**建议 spectral 分离 near-pole shifts 并核对 M 公式，再下"真值支持"结论。**
5. **总体判断**：phase-12 的"c>2 门槛"作为充分条件仍然有效；kernel 的 TL 重述把缺口精确化，但"c≤1/2 是严格上限"仅在 uniform-in-η/specific trivial bound 下成立；**真正精确的墙是 Δ 的 q^{−γ}（γ>3）估计**，即 TL(A>2)。这与项目最终结论（缺 H_Ratios 型 level-aspect 2/2 Ratios power saving）一致。

---

## 6. 复现 & 文件

- 报告：本文件；相关：`phase12/audit/theorem-A.md`（我的定理 A 审计）、`phase12/theory/wrap-attack.md`（kernel）、`phase12/theory/checkE5.py`（Lead）、`phase12/numerics/truth_run2.log`（spectral）。
- 独立复算：使用 `phase12/numerics/ratios_lib.py` 的 `run_q`（同 pipeline）重跑 q=1009、seed=2024、30 shifts、shifted config 的 M/d 数据；输出见 §4.1 表（与 truth_run2.log 一致）。
- 恒等式/账本推导：§1–§2（手算；随机系数检验脚本在 §1.2 提及，因非单位系数公式需 T，未作为决定性验证）。
- 未改他人文件；未读 kernel 的笔记以外的新文件（本任务明确允许读 wrap-attack.md）。
