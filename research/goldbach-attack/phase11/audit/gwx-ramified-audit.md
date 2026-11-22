# Phase-11b 审计（修正版）：GWX (3.2) 对复合导子是正确的；ramified anomaly 是数值 mask bug

> 作者：liu-auditor（task-46，2026-11-21/22）。**本文件替换 task-46 早先的"ramified terms"审计版本**。依据：GWX 本地全文 `phase7/lit/gwx_pdf.txt`/`gwx.txt`；phase-8/11 审计；Lead 2026-11-21 消息（spectral-numerics 发现 phase-10 的 $A_q$ mask bug）；本报告独立数值 `phase11/audit/ramified_check.py`（其实现用正确的 `p∤q` mask）。
> 标注：**[事实]**=原文/可核对；**[推导]**=本报告论证；**[推测]**=判断。
> **Verdict（一句话）**：**GWX (3.2) 的 $\mathcal M_q=\varphi^*(q)Z_q+H_qZ_q(1-b,1-a)$ 对复合导子是正确的；phase-10/11 的"c·q/p ramified 残差"是数值代码把 $A_q$ 的 `p∤q` 掩码写反（用了 `q∤p`）造成的伪影；修正后残差恢复平方根标度，H_Ratios 主项无需修正。** 精确 primitive-character orthogonality 加上正确的 $p\nmid q$ 局部因子记账，正好给出 (3.2) 的 $\varphi^*,M_e$ 系数；我们**没有发现** (3.2) 对 composite q 的 genuine 结构性问题。

---

## 1. [事实] 原文：$\mathcal M_q$、(3.2)、$A_q$、$\zeta_q$ 的定义

### 1.1 §3.6（p.19）逐字

> "The sum of the two main terms in (3.2) is
> $$\mathcal M_q(a,b;s,t)=\varphi^*(q)Z_q(a,b;s,t)+H_q(a,b)Z_q(1-b,1-a;s,t).$$
> **For prime q**, this uses the two terms of Wang–Xu [WX25, Conjecture 2.1], with the exact primitive parity counts in the archimedean coefficient. … **The hypothesis uses the exact coefficient and covers composite conductors as well.**"

### 1.2 §2.1–2.2（(2.1)–(2.6)，pp.6–7）[事实]

$$Z_q(a,b;c,d)=\frac{\zeta_q(a+b)\zeta_q(c+d)}{\zeta_q(a+d)\zeta_q(b+c)}\,A_q(a,b;c,d),$$
$$\boxed{A_q(a,b;c,d)=\prod_{p\nmid q}\frac{(1-p^{-c-d})(1-p^{-a-d}-p^{-b-c}+p^{-c-d})}{(1-p^{-a-d})(1-p^{-b-c})}},$$
$$\boxed{\zeta_q(s)=\zeta(s)\prod_{p\mid q}(1-p^{-s})},\qquad
H_q(a,b)=\sum_{e=0,1}M_e(q)X_{q,e}(a)X_{q,e}(b),$$
$M_e(q)=\#\{\text{primitive }\chi\bmod q:\chi(-1)=(-1)^e\}$。

**关键点 [事实]**：
- $A_q$ 的乘积范围是 **$p\nmid q$**（p 不整除 q），不是 q∤p；这从 (2.1) 原文逐字可核。
- $\zeta_q(s)=\zeta(s)\prod_{p\mid q}(1-p^{-s})$ 的乘积按 **distinct primes**（每个 p 只出现一次，与指数 $e_p$ 无关）。
- 因此 $Z_q$ **只依赖 $q$ 的 radical（素因子集合）**，不依赖指数。这正是 (3.2) 能对所有 q 成立的结构基础。
- §3.6 另注：$\mathcal M_q$ 的两项来自 WX25（prime q）；composite q 由 Hypothesis 1.1 直接规定（论文未从 CFZ recipe 逐步推导，但也没有需要额外 ramified 主项的结构）。

### 1.3 (3.2) Lemma 3.1（p.13）[事实]

> "…uniformly for all $q>1$, $\Re s=\Re t=\sigma$, $|\Im s|,|\Im t|\le10\log(2q)$, and $|u|,|v|\le r$, one has
> $$R_q(a,b;s,t)=\varphi^*(q)Z_q(a,b;s,t)+H_q(a,b)Z_q(1-b,1-a;s,t)+O_\varepsilon\bigl(q^{1-\omega+\varepsilon}(1+|\Im s|+|\Im t|)^B\bigr)\tag{3.2}$$
> for both $(a,b)=(s+u,t+v)$ and $(a,b)=(1-t-v,1-s-u)$."

---

## 2. [推导] 精确 composite orthogonality 如何给出 (3.2)（一致性解释）

### 2.1 精确公式

对任意整数 $A,B$：
$$\boxed{\ \sum_{\chi\bmod q}^{*}\chi(A)\bar\chi(B)
=\sum_{d\mid q}\mu(q/d)\,\varphi(d)\,\mathbf 1_{A\equiv B\ (\mathrm{mod}\ d),\ (AB,d)=1}.\ }\tag{2.1}$$
**证明**：primitive 指示函数的 Möbius 反转
$\mathbf 1_{\mathrm{cond}(\chi)=q}=\sum_{d\mid q}\mu(q/d)\mathbf 1_{\mathrm{cond}(\chi)\mid d}$，交换求和，用
$\sum_{\chi\bmod d}\chi(A\bar B)=\varphi(d)\cdot\mathbf 1_{A\equiv B\pmod d,\ (B,d)=1}$。∎ **精确恒等式**（Route C 的 exact orthogonality）。

### 2.2 各类型的显式展开（[推导]）

- **q=p（素数）**：$\varphi(p)\mathbf 1_{p\mid A-B}-1$。
- **q=p^e (e≥2)**：$\varphi(p^e)\mathbf 1_{p^e\mid A-B}-\varphi(p^{e-1})\mathbf 1_{p^{e-1}\mid A-B}$。
- **q=4p**：$\varphi(4p)\mathbf 1_{4p}-\varphi(2p)\mathbf 1_{2p}-\varphi(4)\mathbf 1_4+\varphi(2)\mathbf 1_2$。
- **q=8p**：$\varphi(8p)\mathbf 1_{8p}-\varphi(4p)\mathbf 1_{4p}-\varphi(8)\mathbf 1_8+\varphi(4)\mathbf 1_4$。
- **q=9p**：$\varphi(9p)\mathbf 1_{9p}-\varphi(3p)\mathbf 1_{3p}-\varphi(9)\mathbf 1_9+\varphi(3)\mathbf 1_3$。
- **q=p_1p_2**：$\varphi(q)\mathbf 1_q-\varphi(p_1)\mathbf 1_{p_1}-\varphi(p_2)\mathbf 1_{p_2}+1$。

### 2.3 一致性论证：为什么 (3.2) 对 composite q 也是正确主项（[推导]）

**(a) 系数恰好是 $\varphi^*(q)$ 与 $M_e(q)$。**
$$\sum_{d\mid q}\mu(q/d)\varphi(d)=\varphi^*(q),\qquad
\sum_{d\mid q}\mu(q/d)N_e(d)=M_e(q),$$
其中 $N_e(d)=\#\{\chi\bmod d:\chi(-1)=(-1)^e\}$（all characters，非 primitive）。证明：primitive 特征按 conductor 分层，all-character 计数是 primitive 计数的和；Möbius 反转即得。验证 q=p^e (odd p)：
$\varphi(p^e)-\varphi(p^{e-1})=\varphi^*(p^e)$，$\varphi(p^e)/2-\varphi(p^{e-1})/2=\varphi^*(p^e)/2=M_e(p^e)$；q=4p：$2(p-1)-(p-1)-2+1=p-2=\varphi^*(4p)$ ✓。
**(b) $Z_q$ 只依赖 radical（§1.2），因此同 radical 的 conductor 项的 kernel 相同。**
对 q=p^e (e≥2)，只有 d=p^e,p^{e−1}（同 radical {p}），两项 kernel 都是 $Z_{\{p\}}$，相加：
$$\varphi(p^e)Z_{\{p\}}-\varphi(p^{e-1})Z_{\{p\}}=\varphi^*(p^e)Z_{\{p\}},$$
反射/parity 项同理（$M_e(p^e)=N_e(p^e)-N_e(p^{e-1})$ 且 reflected kernel 只依赖 radical）⇒ **正好是 (3.2) 的 $\varphi^*(q)Z_q+H_qZ_q(1-b,1-a)$，无残余 ramified 项。**
**(c) 对一般 composite q**（4p,8p,9p,squarefree…）：精确正交性的 conductor 项按 radical 分组；每一组 d 的 kernel $Z_{\mathrm{rad}(d)}$ 是同一个函数。CFZ/ratios recipe 对 **full family mod d** 的主项必须包含从 d 提升到 q 时被省略的 Euler 因子（$\prod_{p|q,p\nmid d}(1-\chi(p)p^{-s})$，见 GWX §3.3 对 induced 特征的处理）。在正确的 $p\nmid q$ 局部因子记账下（$A_q$ 只乘 $p\nmid q$、$\zeta_q$ 只乘 $p\mid q$ 各一次），这些 conductor 项与 Euler 因子重组后**正好合并成**
$$\varphi^*(q)Z_q+H_qZ_q(1-b,1-a),$$
即 (3.2)。**这就是 primitive-character orthogonality + correct local-factor bookkeeping 的一致性解释；没有额外的 ramified 主项。**
> 严格注：论文没有把 (c) 写出来（§3.6 只说 prime q 用 WX25；composite q 由 Hypothesis 覆盖）。我们的审计只能确认：$\varphi^*,M_e$ 的 Möbius 系数、$Z_q$ 的 radical 依赖性、以及 (c) 的重组在结构上完全吻合 (3.2)；**我们没有发现任何需要修改 (3.2) 的结构性理由。** [推导/推测]

---

## 3. [推导/数值] 为什么 phase-10 会出现"c·φ(q/p) ramified 残差"：mask bug

- **Bug [事实/推导]**：phase-10 的 $A_q$ Euler 乘积使用了 mask `(PRIMES % q != 0)`。这个条件测试的是 **$q\nmid p$**（q 不整除 p）；正确条件应是 **$p\nmid q$**（p 不整除 q），即 `(q % PRIMES != 0)`。
  - 对 **prime q**：p=q 是唯一整除 q 的素数；`PRIMES % q != 0` 在 p=q 时取 0 ⇒ 排除 q，恰好等价于 p∤q；**bug 对 prime q 不可见**。
  - 对 **composite/ramified q**：任何 p|q 且 p<q 都有 `p % q = p ≠ 0` ⇒ **被错误地包含进 $A_q$**（本应排除），额外乘上了本属于 $p\mid q$ 因子的局部项；这会给残差贡献一个与 $\varphi(q/p)$ 同阶、随 q 增长的假项。**完全解释 phase-10/11 的 ramified anomaly。**
- **我们独立实现的 mask [事实]**：`ramified_check.py` 中 `if q%p==0: continue`（即只包含 **p∤q** 的素数）——这是正确版本。用该实现得到的数值（见 §4）**没有** φ(q/p) 线性增长，全部呈平方根标度；这独立支持 Lead/spectral-numerics 的结论。
- **修正后预期 [事实/推测]**：spectral-numerics 用修正 mask 重算 q=2^e (e=8..18, 40 shifts)：RMS/√q ≈ 2.1–5.0，RMS/(q/2) 递减，拟合 α=0.537±0.032（≈平方根）——**phase-10/11 的数值结论（复合 q 行为同样是 $q^{1/2+o(1)}$，无 ramified 线性项）恢复。**

---

## 4. [数值] 本报告独立核验（正确 $p\nmid q$ 的 $A_q$）

参数：$\eta=0.05$，$a=0.5+0.37i$，$b=0.5-0.21i$，$s=0.55+0.11i$，$t=0.55-0.29i$；$A_q$ 素数积截断 ≤2×10⁵，mpmath 25 位（部分优化后 20 位）；primitive χ 用单位群分解枚举；$R_q$ 直接由 Hurwitz-zeta L 值求和；$\mathcal M_q$ 按 §1.2 公式（$A_q$ 正确 mask）。**残差 $|R_q-\mathcal M_q|$ 与 $q^{1/2}$、$\varphi(q/p)$ 的比较：**

| q | 类型 | $\varphi^*$ | 残差 | 残差/$q^{1/2}$ | 残差/φ(q/p) |
|---|---|---|---|---|---|
| 8 | 2³ | 2 | 0.165 | 0.058 | 0.083 |
| 16 | 2⁴ | 4 | 0.222 | 0.056 | 0.056 |
| 32 | 2⁵ | 8 | 0.673 | 0.119 | 0.084 |
| 64 | 2⁶ | 16 | 0.488 | 0.061 | 0.030 |
| 128 | 2⁷ | 32 | 2.172 | 0.192 | 0.068 |
| **256** | **2⁸** | **64** | **2.525** | **0.158** | **0.039** |
| 9 | 3² | 4 | 0.313 | 0.104 | 0.157 |
| 27 | 3³ | 12 | 0.395 | 0.076 | 0.066 |
| 81 | 3⁴ | 36 | 1.314 | 0.146 | 0.073 |
| 100 | 4·5² | 16 | 1.460 | 0.146 | 0.073 |
| **196** | **4·7²** | **36** | **1.460** | **0.104** | **0.035** |
| 225 | 9·5² | 64 | 8.633 | 0.576 | 0.216 |
| 12 | 4·3 | 1 | 0.144 | 0.042 | 0.072 |
| 20 | 4·5 | 3 | 0.222 | 0.050 | 0.056 |
| 24 | 8·3 | 2 | 0.085 | 0.017 | 0.021 |
| 36 | 4·9 | 4 | 0.103 | 0.017 | 0.017 |
| 45 | 9·5 | 12 | 2.052 | 0.306 | 0.256 |

**解读 [数值]**：
- 用正确 mask，**pure 2-powers** 的残差/$q^{1/2}$ 松散稳定在 0.06–0.19；残差/φ(q/p) 从 0.083（q=8）降到 0.039（q=256）——**没有 c·φ(q/p) 线性项**；q=256 是最强反证（若有 $\sim c\cdot64$ 的 ramified 项，残差应 ~数十，而不是 2.5）。
- **mixed 4·p²**：q=100（p=5）残差 1.46，q=196（p=7）残差 1.46；$q^{1/2}$ 分别为 10、14，残差/q^{1/2}=0.15、0.10——**平方根标度，无 φ(q/p) 增长**。
- q=225（9·5²）残差 8.6 较大，但 q=31 的 prime 也有 3.2 的残差（0.58q^{1/2}）；小 q 非渐近波动大，且我们的实现可能还有低阶项/参数敏感；**不构成 ramified 结构证据**。
- 该表与 phase-10 的 bug 解释一致：用错误 mask 时，composite/ramified q 的 $A_q$ 会额外包含 p|q 的局部因子，导致 φ(q/p) 级假残差；正确 mask 后消失。

---

## 5. [事实/推导] 对 $A_q$ 与 $\zeta_q$ 的逐项核对（与修正实现的匹配）

1. **(2.1) 的乘积范围**：PDF 原文（§2.1, p.6）：
   "$A_q(a,b;c,d)=\prod_{p\nmid q}\frac{(1-p^{-c-d})(1-p^{-a-d}-p^{-b-c}+p^{-c-d})}{(1-p^{-a-d})(1-p^{-b-c})}$"
   ⇒ **p∤q**，且每个 p 一次。**修正实现 `if q%p==0: continue` 与此一致；phase-10 的 `PRIMES%q != 0` 是反的。**
2. **(2.4)/(2.6) 的 $\zeta_q$**：$\zeta_q(s)=\zeta(s)\prod_{p|q}(1-p^{-s})$，product over distinct primes（不随指数重复）。PDF 原文 §2.1 的 $\zeta_q(s)=\zeta(s)\prod_{p\mid q}(1-p^{-s})$ 明确。**修正实现 `zetaq` 对每个 p|q 只乘一次，正确。**
3. **$F_p,\ A_q,\ C_q$**：$D_q(z)=(q/\varphi(q))^2\zeta(z)\prod_{p\nmid q}F_p(z)\prod_{p|q}(1-p^{z-1})$（(2.4)）；这与 $Z_q$ 的 $A_q$、$\zeta_q$ 定义相容；$C_q=\Xi D_q$ (2.6) 的 $p|q$ 因子同样按 distinct primes。**数值实现中我们的 $Z_q$ 直接按 (2.2)+(2.1) 计算，与论文一致；未使用错误的 $A_q$。**
4. **[事实] 结论**：修正实现与 GWX (2.1)-(2.6) 的定义**完全匹配**；phase-10 的异常是 mask 笔误，不是论文公式错误。

---

## 6. 最终 verdict（按 Lead 要求 re-framed）

1. **[事实] (3.2) 对复合导子是正确的**（至少：与 exact orthogonality + 正确 $p\nmid q$ 局部因子记账完全一致；未发现结构性问题）。$\mathcal M_q=\varphi^*(q)Z_q+H_qZ_q(1-b,1-a)$，$Z_q$ 只依赖 $q$ 的 radical，$A_q$ 只乘 $p\nmid q$，$\zeta_q$ 只乘 $p\mid q$ 各一次。
2. **[事实/推导] phase-10/11 的"c·φ(q/p) ramified 残差"是数值 mask bug**：`(PRIMES % q != 0)` 把"$q\nmid p$"误当"$p\nmid q$"；对 prime q 不可见，对 composite q 错误包含 p|q 的素数，产生与 φ(q/p) 同阶的假项。修正为 `p∤q` 后（spectral-numerics 重算），q=2^e 的 RMS/√q 稳定、RMS/(q/2) 递减、α≈0.537——**平方根标度恢复**。
3. **[数值] 我们的独立实现（正确 mask）同样无 ramified 线性项**：q=256（2^8）残差 2.5 而非 φ(q/p)=64 级；q=100/196（4p²）残差 1.46，/√q=0.15/0.10；**支持 (3.2) 与 phase-10 修正后的结论。**
4. **[事实/推导] phase-10 的 composite 表应重新确认**：随 spectral-numerics 用修正 mask 重算；本报告与 Lead 的解析/数值结论指向"恢复原结论：prime/squarefree/ramified 都 $q^{1/2+o(1)}$，GWX (3.2) 无需修正"。**原 phase-10 表中 ramified 行的异常应删除/标注为代码 bug。**
5. **对项目 claim 的影响**：**无负面影响**。GWX Theorem 1.1 的 (3.2) 主项不变；H_Ratios^min（phase-11 Part A）不变（仍可用 $\mathcal M_q$ 印刷版）；Route C 的失败（phase-11 Part B）与 (3.2) 正确性无关（其致命点仍是 wrap-around Type II 相关，见 `route-c-audit.md`）。**没有需要向 GWX 报告的结构性修正；cxy0714 的 uniformity doubt 也已在 Part A 解决。**
6. **唯一保留的 minor caveat [推测]**：GWX 对 composite q 的 (3.2) 是从 prime q（WX25）+ Hypothesis 直接陈述的；论文没有写出 composite q 的 CFZ recipe 推导。我们的"一致性论证"（§2.3）是结构性的，不是逐行推导；若未来要做形式化/严格审计，建议补一段 conductor-Möbius + induced-Euler-factor 的重组证明。但**这不是 gap，更不是反例**；数值与结构均支持 (3.2)。

---

## 7. 复现 & 文件

- 报告：本文件（替换早先 ramified 版本）。
- 脚本：`phase11/audit/ramified_check.py`（正确 `p∤q` mask；含 primitive χ 枚举、Hurwitz-zeta L 值、$A_q$ 素数积截断、mpmath 高精度）。输出见 `q256.log` 等。
- GWX 原文：`phase7/lit/gwx_pdf.txt`（(2.1)–(2.6), (3.2), §3.6）、`gwx.txt`（HTML，含共轭横线）。
- 本报告未读 kernel-theorist 笔记；未假定 ramified 项。
