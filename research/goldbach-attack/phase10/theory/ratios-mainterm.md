# Phase-10：GWX 的 M_q 是 CFZ 标准 Ratios recipe 的自然特化，还是额外外推？

> kernel-theorist，task-35。日期：2026-11-21。
> 对象：G-W-X（Gou–Wang–Xu, arXiv:2611.18825）Hypothesis 1.1 的主项
> `M_q(a,b;s,t)=φ*(q)Z_q(a,b;s,t)+H_q(a,b)Z_q(1−b,1−a;s,t)`。
> 核心问题：这是 **CFZ 2008 标准 Ratios recipe 对本原 Dirichlet L 族的自然特化（含复合导子、奇偶分辨）**，还是**额外外推/加强**？——决定 H_Ratios 的"可信度/主流性"。
> 标注：**[证明]/[推导]/[事实]/[推测]**。关键源：本地 `phase7/lit/gwx.txt`（GWX 全文提取）；phase-8 `phase8/lit/ratios-status.md`；URL 访问 2026-11-21。
> 关键 GWX 原文（后文逐条引用）：`M_q(a,b;s,t)=φ*(q)Z_q(a,b;s,t)+H_q(a,b)Z_q(1−b,1−a;s,t)`；`Z_q=ζ_q(a+b)ζ_q(c+d)/(ζ_q(a+d)ζ_q(b+c))·A_q`；`H_q=Σ_{e=0,1}M_e(q)X_{q,e}(a)X_{q,e}(b)`（X 在原始 shifts a,b；GWX line ~6990）；`X_{q,e}(w)=(q/π)^{1/2−w}Γ((1−w+e)/2)/Γ((w+e)/2)`。（对应任务消息中的记号 c=s,d=t。）

---

## 0. 裁决（先给 Lead）

**MATCH（标准特化）+ 一处受控外推（复合导子）。** 详细：
1. **两项结构（对角项 + FE-反射项）完全是 CFZ 2008 标准 recipe 的结构**：GWX 原文（§3.1 附近）："In the ratios recipe [CFZ08], the first main term comes from the diagonal and the second from applying the functional equation to both numerator L-functions. The sum of the products of the two functional equation factors is H_q." 这与 CFZ08 的 2/2 recipe（对角 + 分子 FE 交换）**逐项一致**。**[事实]**
2. **prime q：GWX 明说它就是 Wang–Xu [WX25, Conjecture 2.1]**（原文 line 12640+："For prime q, this uses the two terms of Wang–Xu [WX25, Conjecture 2.1], with the exact primitive parity counts in the archimedean coefficient."）。所以对 prime q，H_Ratios = Wang–Xu 猜想（CFZ recipe 的 prime-conductor 特化）+ **精确奇偶计数**（见 §1.3），**不是新假设**。**[事实]**
3. **composite q：GWX 明确承认这是他们的扩展**："We assume the formula for composite as well as prime conductors. Wang–Xu [WX25] formulate their conjecture for prime conductors."（line 7340+）以及"The hypothesis uses the exact coefficient and covers composite conductors as well."（line 12640+）。所以 **复合导子部分是 H_Ratios 唯一的非文献性外推**；其"自然性"依据是：CFZ recipe 是**对任意族按局部 Euler 因子逐素构造**的通用处方（recipe 不依赖 q 素性或族大小），而 `ζ_q`, `A_q`, `M_e(q)` 恰好是"primitive χ mod q"族的局部结构（§2）。**[推导/推测]**
4. **可信度评估**：H_Ratios = **"标准 CFZ recipe 的 composite-conductor 自然扩展"**，不是对平均类型的加强（仍然是 2/2 ratios 的 power saving，ω_D 任意小、与 GRH 并列）。风险集中在复合 q 的局部因子/计数是否正确；但这**可被已知矩/数值检验**（§4/§5），且 GWX 的 parity twist 只依赖 Lemma 3.1 的形式（两项结构），不依赖具体的复合局部因子细节之外的强度。**判定：主流性强（CFZ recipe 是该领域标准猜想语言）；复合部分应标为"自然的插值延伸"，在正式引用时需注明"GWX extension of WX25/CFZ08 to composite conductors"。**

---

## 1. 逐项对照（CFZ recipe vs GWX M_q）

### 1.1 对角项 Z_q —— 与 CFZ recipe 的"算术因子"一致 [推导]
GWX：`Z_q=ζ_q(a+b)ζ_q(c+d)/(ζ_q(a+d)ζ_q(b+c))·A_q`，`ζ_q(s)=ζ(s)∏_{p|q}(1−p^{−s})`（即 `Σ_{(n,q)=1}n^{−s}`），
`A_q=∏_{p∤q}[(1−p^{−c−d})(1−p^{−a−d}−p^{−b−c}+p^{−c−d})]/[(1−p^{−a−d})(1−p^{−b−c})]`。
**配对来源**（CFZ 对角项的标准推导）：把四个 L 展开成 Dirichlet 级数
`L(a,χ)=Σ_n χ(n)n^{−a}`, `L(b,χ̄)=Σ_m χ̄(m)m^{−b}`, `1/L(c,χ)=Σ_r μ(r)χ(r)r^{−c}`（形式展开，解析延拓意义下）, `1/L(d,χ̄)=Σ_l μ(l)χ̄(l)l^{−d}`，
特征标正交 `Σ*_χ χ(n)\barχ(m)χ(r)\barχ(l) = Σ_{f|q}μ(q/f)φ(f)·1_{nr≡ml (f)}`（对 `(nmrl,q)=1`）。**对角主项**取"精确配对"（去掉同余约束、保留主项）：
- 配对 `n↔r`（χ(n)χ(r)）⇒ `n^{-a-c}`；
- 配对 `m↔l`（χ̄(m)χ̄(l)）⇒ `m^{-b-d}`；
- 配对 `n↔m`（χ(n)χ̄(m)）⇒ `n^{-a-b}`；
- 配对 `r↔l`（χ(r)χ̄(l)）⇒ `r^{-c-d}`；
- 交叉配对 `n↔l`（χ(n)χ̄(l)，n≡l）⇒ `n^{-a-d}`；`m↔r`（χ̄(m)χ(r)，m≡r）⇒ `m^{-b-c}`。
GWX 的 `Z_q` 的 ζ 因子恰是 `ζ_q(a+b)ζ_q(c+d)/(ζ_q(a+d)ζ_q(b+c))` 的**组合**（分母的 `a+d, b+c` 对应交叉配对，分子的 `a+b, c+d` 对应"同一 L 的共轭配对"），而 `A_q` 是 `p∤q` 的局部修正（`p|q` 时 χ 的局部因子平凡，故 `A_q` 只乘 `p∤q`，而 `ζ_q` 已用 `∏_{p|q}(1−p^{−s})` 吸收 `p|q` 的 ζ 因子）。**这与 CFZ recipe 的"局部因子逐素构造"完全同型**（CFZ 的 A 因子正是这种分子/分母组合）。**逐项 MAP ✓**。
（`A_q` 的具体局部因子形式：分子 `(1−p^{−c−d})(1−p^{−a−d}−p^{−b−c}+p^{−c−d})`、分母 `(1−p^{−a−d})(1−p^{−b−c})` 是 CFZ 比值因子的标准形态——它使 `Z_q` 在 `s=a,t=b` 退化时给出 1，见 §4.1。**[推导]**）

### 1.2 交换项 Z_q(1−b,1−a;s,t) —— CFZ 的"FE-反射项" [事实/推导]
CFZ recipe 第二项来自把**两个分子 L 的函数方程**用于 `L(a,χ)L(b,χ̄)`：`L(a,χ)L(b,χ̄)=X_{q,e}(a)X_{q,e}(b)L(1−a,χ̄)L(1−b,χ)`（root number 抵消；GWX §3.1 原文："For a primitive character χ of parity e, the functional equations for χ and χ̄ give L(1−b,χ)L(1−a,χ̄)=h_e L(a,χ)L(b,χ̄), since the root numbers cancel"）。**分母 L(s,χ)L(t,χ̄) 不反射**——因为 `Re s,Re t=1/2+η>1/2`（在"分母无零点/可展"一侧），且 GWX 原文明确："the second from applying the functional equation to both numerator L-functions"——**这正是 CFZ recipe 的标准做法**。交换项里 `Z_q(1−b,1−a;s,t)` 只反射分子 shifts（`a→1−b, b→1−a`），分母保持 `s,t` ✓。**[事实/推导]**
注：GWX §3.1 的 parity twist 正是利用这两个项：`R=R_0+R_1`，`R∨=h_0R_0+h_1R_1`，故 `Σ_χχ(−1)… = [2R∨−(h_0+h_1)R]/(h_1−h_0)`——**这要求 CFZ recipe 的两项结构在奇偶分解下正确，是配方内容而非额外假设**。

### 1.3 archimedean 因子 H_q 与 M_e(q)（唯一需要仔细看的"加强点"）[事实]
`H_q(a,b)=Σ_{e=0,1}M_e(q)X_{q,e}(a)X_{q,e}(b)`（GWX 原文 line ~6990 的精确形式：**X 在原始分子 shift a,b 处**；与 §3.1 的 `h_e=X_e(1−b)X_e(1−a)=(X_e(a)X_e(b))^{-1}` 互为倒数，一致），`M_e(q)`=primitive χ mod q 的 parity e 计数，`φ*(q)=M_0+M_1`。
- **这是 Σ*_χ X_{q,e}(a)X_{q,e}(b) 的精确求值**（利用 X 只依赖 parity e 与 q）；CFZ recipe 里对应的"archimedean 因子"本来就是族平均 `E_χ[X(a,χ)X(b,χ̄)]`，所以**用精确 M_e(q) 是正确求值，不是加强假设**。**[推导]**
- **prime q**：q 奇素时 `M_0=M_1=(q−1)/2=φ*/2`，故精确计数与 `φ*/2` 一致（GWX 原文："On the critical line, replacing the two counts by φ*(q)/2 changes that coefficient by O(1)"——对 prime q 实际差 0；对 composite q 差 `Δ(q)=M_0−M_1`）。**[事实]**
- **composite q**：`M_e(q)` 有显式公式（按 CRT/导子分解：`q=∏p^{a_p}`，primitive χ 的 parity 由其原特征 parity 与模 4/8 条件决定；`Δ(q)≠0`，如 `q≡2 mod 4` 时只有偶特征? 需按标准公式核对），`Δ(q)` 是 composite 结构的主要"新东西"；GWX 用它**移除 reflected kernel 的极点**（原文："This removes the pole of the reflected kernel... The hypothesis uses the exact coefficient and covers composite conductors as well."）。**[事实/推导]**
- **`ζ_q` 的复合形式**：`ζ_q(s)=Σ_{(n,q)=1}n^{−s}` 正是"primitive χ mod q ⇒ χ(n)=0 for (n,q)>1"的直接后果（L 的 Dirichlet 级数只含与 q 互素的 n）；**这是复合导子的正确局部结构，不是外推**。**[证明]**

### 1.4 小结（term-by-term）
| 成分 | CFZ recipe 标准？ | 复合导子？ | 结论 |
|---|---|---|---|
| 两项结构（对角+分子FE交换） | ✓（CFZ08 / WX25） | 不变 | 标准 |
| `Z_q` 的 ζ 因子配对（a+b,c+d 分子；a+d,b+c 分母） | ✓（局部因子逐素构造） | `ζ_q=ζ∏_{p|q}` 正确 | 标准 |
| `A_q`（p∤q 局部因子） | ✓（CFZ 比值因子形态） | p\|q 局部因子平凡 | 标准 |
| `H_q`（archimedean） | ✓（=族平均 X 因子） | 精确 `M_e(q)`、`Δ(q)≠0` | 自然加强求值 |
| 全 q（含复合）的**声明** | ✗（WX25 仅 prime） | —— | **GWX 的受控外推** |

---

## 2. 函数域类比：复合导子的主项形式是否被支持？[事实/推导]
- **G-W-X Thm 1.5（函数域，无条件）**：对固定奇素数幂 `q>10^{200}`、任意首一 `N`（deg≥3），
  `Σ_{F∈M_{d−1}}Λ(F)Λ(N−F)=q^{d−1}𝔖_q(N)+O_q(q^{23d/24})`。
  其主项 = **局部密度乘积（singular series）** × `q^{d−1}`；机制是 Sawin 的 factorization-function 估计（平方自由 AP 中素数分布，水平 θ=5/6）+ 判别式上同调（两点 Möbius 相关）。
- **类比支持**：函数域主项是**局部因子的 Euler 乘积**（`𝔖_q(N)=∏_v 局部密度`），复合"导子"（模多项式 C 的因子）按素因子逐个进入——这与 GWX 在 ℚ 侧的 `ζ_q, A_q, M_e(q)` 的逐素结构**同型**；Sawin 的 squarefree-progression 估计也确实是"逐素因子"的。故**函数域中复合结构的局部因子化是被证明的**（但走的是完全不同的无条件机制，不是 Ratios formula）。**[事实]**
- **不能直接支持 ℚ 侧 M_q**：函数域 Thm 1.5 不经过 Ratios；它只说明"复合局部因子化"是**正确的物理**，从而 GWX 把 prime-q CFZ formula 按局部因子延拓到 composite q 是**自然的**；但 ℚ 侧的正确性仍需 Ratios 猜想本身（或数值/矩检验）。**[推导/推测]**

---

## 3. 极限自洽性检验 [推导]

### 3.1 平凡极限 s→a, t→b（比值≡1）——**GWX M_q 通过 ✓**
`R_q(a,b;a,b)=Σ*_χ 1=φ*(q)`。逐项计算（用 `c=s=a,d=t=b`）：
- `Z_q(a,b;a,b)`：分子 `ζ_q(a+b)²`、分母 `ζ_q(a+b)ζ_q(b+a)=ζ_q(a+b)²` ⇒ 比值 1；`A_q(a,b;a,b)`：分子 `(1−x)(1−x)`、分母 `(1−x)²`（`x=p^{−a−b}`）⇒ `A_q=1`。故 `Z_q=1`。
- 交换项：`Z_q(1−b,1−a;a,b)=ζ_q(2−a−b)ζ_q(a+b)/(ζ_q(1−b+b)ζ_q(1−a+a))·A_q' = ζ_q(2−a−b)ζ_q(a+b)/ζ_q(1)²·A_q'`。`ζ_q(1)` 是极点 ⇒ 该因子为 **0**（即使 `a+b=1` 时分子单极点也压不过分母双极点）。故 `H_q·0=0`。
- 合计 `M_q→φ*(q)·1=φ*(q)` ✓。**这是一个非平凡的逐项一致性检验（分子/分母配对、A_q 形态、交换项归零均正确）**。

### 3.2 矩极限（二阶矩）——定性一致，定量留待数值 [推导]
已知无条件事实：`Σ*_{χ mod q}|L(1/2+it,χ)|²` 的主项 ~ `φ*(q)·(log q + O(1))`（中央点 log q 增长；一般 t 处由 `ζ(1+2it)` 型因子控制）。GWX 的 `Z_q` 在 `a+b→1`（对应 `L(a)L(b)` 的共轭/二阶矩方向）时含 `ζ_q(a+b)` 的**单极点** ⇒ `log q` 增长，**定性一致**（`ζ_q` 的单极点来自 `(n,q)=1` 的对角 `n=m` 求和，正是二阶矩的对角主项）✓。**定量常数**（`A_q` 在 `a+b=1` 的取值、`A_q/ζ_q` 的组合）需要更仔细的矩极限（把 2/2 比值极限化为 2/2 矩），本报告时间盒内未完成；**建议 spectral-numerics（task-34）直接数值核验** `M_q` 在这两个极限的值（见 §5）。

### 3.3 parity 极限 [推导]
`Δ(q)=M_0−M_1`：prime q 为 0；composite q 一般非 0。GWX 原文说在临界线 `|X_{q,e}(a)|=1` 时用 `φ*/2` 代替精确计数使 archimedean 系数变化 `O(1)`，并"removes the pole of the reflected kernel"——说明**精确 `Δ(q)` 是 composite q 情形的实质内容**（若假设 `Δ(q)=0` 会在 reflected kernel 上出极点）。这一点在 prime q 不出现，是 composite 外推的核心风险点；可用 `Δ(q)` 的显式公式独立计算 + 数值检验。

---

## 4. 裁决与风险评估

### 4.1 裁决
```
H_Ratios = [CFZ 2008 标准 2/2 Ratios recipe 的 primitive-Dirichlet-族特化]
         + [精确 archimedean parity 计数 M_e(q)]（自然求值）
         + [composite conductors 的逐素延拓]（GWX 的扩展；文献仅有 prime q 版 WX25 Conj 2.1）
```
**即：主流语言内的"标准猜想 + 受控延拓"，不是全新类型的假设**；但严格引用时应写作：**"CFZ08/WX25 的 composite-conductor extension (GWX 2026)"**，不可声称"CFZ 2008 原文已包含复合导子"。**[事实/推导]**

### 4.2 风险（按重要性）
1. **composite q 的精确局部计数 `M_e(q)`/`Δ(q)` 与 `ζ_q` 的相互作用**：若局部因子在 `p|q`（不同于 `p∤q`）的处理有误，error term 可能从 `q^{1−ω}` 恶化（例如出现额外 `q^{o(1)}` 因子——对 G-W-X 的任意 ε 可吸收，故**风险有限**；但若恶化到 `q^{1−ω+c}` 则失去 arbitrary ω）。
2. **任意小 `ω_D>0` 与 `η→0` 一致性**：CFZ recipe 本身不含"arbitrary ω"；这是 G-W-X 额外要求的**一致性强度**（比通常"square-root"猜想更强）。不过 WX25 已 conjecture power saving for prime q；"arbitrary ω>0, independent of η" 是 G-W-X 的加强表述。**[事实/推测]**
3. **分母 shifts `Re s=Re t=1/2+η` 与 numerator `Re=1/2` 的混合区域**：CFZ recipe 通常按"分母在收敛域/无零点区"叙述，此处分母仅在临界线右侧 η 处；GWX 的 Lemma 3.1 用 `a=s+u`（分子实部在 (1/4,3/4)）并插值；需要确认 recipe 在该混合区域的正确性（GWX 用 GRH 保证分母无零点来支撑）。
4. **误差 `(1+T)^B` 的 B 与控制**：要求对 `T≤100log(2q)` 一致，B 有限；这比通常固定 shift 的猜想强，但"power saving in q"是主内容，`T` 多项式损失为技术性。

### 4.3 可检验预言（供 spectral-numerics task-34）
```
(P1) 平凡极限：数值计算 M_q(a,b;a,b) 应 = φ*(q)（本报告已解析验证；数值可复核）。
(P2) 二阶矩：取 (a,b) 使 L(a)L(b)/[L(s)L(t)] 的极限化为 |L(1/2+it,χ)|² 型（或直接算 Σ*|L|² 的已知 log q 主项），
     核验 Z_q 的 ζ_q(a+b) 极点系数（预测：中央点 log q 的系数与已知二阶矩主项一致）。
(P3) composite q 的 Δ(q)：对 q=2p, 4p, 8p, p² 等计算 M_0,M_1 与 GWX 公式，检查 reflected kernel 极点是否如原文所说被 exact counts 移除；
     若数值显示 M_q 与直接 χ-平均在 q^{1−ω} 量级不一致（且 ω 随 q 下降），则 composite 延拓有误。
(P4) 与 prime q 对照：q 素时应与 WX25 Conj 2.1（CFZ recipe）逐项一致（这是文献锚点）。
```

---

## 5. 结论（一句话）
**M_q 的两项结构、`Z_q` 的 ζ/A 因子、交换项的分子反射、archimedean 因子的族平均形式，全部是 CFZ 2008 Ratios recipe 的标准内容（prime q 时 = Wang–Xu Conjecture 2.1）；唯一超出文献的是 GWX 把该公式按局部 Euler 因子自然延拓到 composite conductors，并用精确 parity 计数 `M_e(q)/Δ(q)` 处理反射核极点。因此 H_Ratios 的可信度 = 标准 CFZ 猜想的可信度（主流、被广泛假设），复合导子部分应视为"自然但未验证的延拓"（风险受控、可数值检验，且对 G-W-X 的任意 ε 有缓冲）。**

## 6. 参考 URL（2026-11-21）
- GWX: arXiv:2611.18825（本地 `phase7/lit/gwx.txt`）；关键行：line 12640+（prime q 用 WX25 Conj 2.1 + exact parity counts + "covers composite conductors as well"）、line 7340+（"We assume the formula for composite as well as prime conductors. Wang–Xu formulate their conjecture for prime conductors."）、§3.1（parity twist：`R=R_0+R_1, R∨=h_0R_0+h_1R_1`）。
- CFZ08: arXiv:0711.0718（ratios recipe；GWX 引作 [CFZ08, Conjecture 5.1 and Section 6.4] 的 2/2 主项来源）。
- WX25: Wang–Xu, Conjecture 2.1（prime conductors；GWX 引 [WX25]，phase-8 已确认其存在与 prime-q 范围）。
- Sawin, Acta Math. 233 (2024) 285–418, arXiv:2102.09730（函数域 factorization functions）。
- phase-8 汇总 `phase8/lit/ratios-status.md`；phase-9 `phase9/theory/ratios22.md`（MDs 技术可行性）。
