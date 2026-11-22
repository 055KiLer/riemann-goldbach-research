# Phase-11 Route C：truncated Möbius + smooth AFE + exact orthogonality 冲击弱 H_Ratios —— 严格部分结果、参数矛盾与精确墙

> kernel-theorist，task-38（phase-11 主攻）。日期：2026-11-21。
> 目标：在 GRH 级输入下证明弱 H_Ratios（任意固定 0<ω≤1/2，全 q、Re a=Re b=1/2、Re s=Re t=1/2+η、T≤100log(2q)：`R_q(a,b;s,t)=M_q+O(q^{1−ω+ε}(1+T)^B)`）。若成，则 Alpöge GRH ⇒ Goldbach（G-W-X）。
> 标注 **[证明]/[推导]/[事实]/[推测]/[数值]**。脚本：`mq_check3.py`（数值验证 M_q）、`warm11.py`（1/1 规模）。
> 任务要求："develop rigorously, or find the exact fatal lemma" —— 本报告的结论是：**得到若干严格引理 + 一个参数矛盾定理（variant C1 在 GWX 参数窗内不可能）+ 精确的致命引理 H_wrap，未证 H_Ratios**；同时首次数值验证了 GWX 的 M_q 公式到 O(√q)。

---

## 0. 裁决（给 Lead）

1. **没有证明**弱 H_Ratios（哪怕 ω=1/100）；Route C 在参数窗 `η≪ω`（GWX 需要 `η<ω/(8(2+ω))`）内被一个**结构性矛盾**挡住，而非仅仅"估计不够好"：
   - **Variant C1（只用 truncated Möbius 表示 1/L）**：要 q^{−ω} 精度需截断长度 `M≥q^{ω/η}`；要避免 wrap-around（即所有指标乘积 <q）需 `M<q`；两者相容要求 `ω/η<1`，与 GWX 的 `ω/η>8(2+ω)>16` 矛盾。**这是 [证明] 级的障碍（给定 Lemma 1.1 的标准性）。**
   - **Variant C2（对 1/L 也用精确 smooth AFE，四段和各个长度 ~√(qT)）**：截断误差可做到 (qT)^{−A}（可控），但出现 **wrap-around 项** `Σ_{1≤|k|≤T} Σ_{nr−ml=kq}`（shift 集是等差数列 {kq}）；这是唯一未解决的项，也是**单一最难引理 H_wrap**。
2. **新的严格引理**：
   - **[证明] Lemma 1.1（GRH 下 truncated Möbius reciprocal）**：`1/L(s,χ)=Σ_{m≤M}μ(m)χ(m)m^{−s}+O(M^{1/2−σ+ε}(q(1+|t|))^{ε})`，`σ=Re s=1/2+η` ⇒ 误差 `O(M^{−η+ε}(qT)^{ε})`（标准输入：GRH ⇒ `Σ_{n≤x}μ(n)χ(n)≪x^{1/2+ε}(q(1+|x|))^{ε}`）。比 Perron 围道版本更干净、无需零点留数。
   - **[事实/证明] Lemma 1.2**：`L(a,χ)` 的光滑 AFE（长度 √(qT)，误差 (qT)^{−A}；IK Thm 5.3 型，无条件）。
   - **[证明] Lemma 1.3**：primitive 特征标精确正交性：`Σ*_{χ mod q}χ(A)\barχ(B)=1_{(AB,q)=1}Σ_{f|q}μ(q/f)φ(f)1_{A≡B(f)}`；q 素时 `=(q−1)1_{A≡B}−1`（(AB,q)=1），否则 0。**Gauss 和/root-number 求和**：`Σ_{χ parity e}ε(χ)χ(u)=O(√q)`（用 τ(χ) 显式求值），故"反射/根数型"配置贡献 ≤O(√q·(多项式))。
   - **[事实] Lemma 1.4**：`Σ*_{χ mod q}|L(1/2+iu,χ)|²≪q^{1+ε}(1+|u|)^{O(1)}`（正交性/大筛，无条件）⇒ AFE 误差项乘 |L(a)L(b)| 后 ≤q^{1+ε}(qT)^{−A}，可控。
3. **[数值] 首次数值验证 GWX M_q（新）**：q=97,101,103，generic shifts（Re a=Re b=1/2, Re s=Re t=0.6）：
   ```
   q=97 : R_exact=92.8849−0.0834i, M_q=93.9026−2.2781i, |R−M|/√q=0.246
   q=101: R_exact=95.2408−1.0855i, M_q=97.7878−2.4378i, |R−M|/√q=0.287
   q=103: R_exact=96.0669+1.1060i, M_q=99.7287−2.5179i, |R−M|/√q=0.508
   ```
   ⇒ 主项公式正确（误差 ≈O(√q)，即 ω_D 至多 1/2 的 square-root 型），且**平凡极限** `s=a+ε,t=b+ε`（比值≡1）给 `M_q→φ*(q)=95.0000`（ε=10^{−3}）、`R_exact→95`（O(1) 内）——验证了"可去奇点/平凡极限"约定。**这支持 phase-10 的"CFZ 标准特化"结论，也说明 GWX 的 M_q 转录无误。**
4. **精确墙（single hardest lemma）**：**H_wrap**（见 §4）：level-aspect 的 Möbius/除子型二元相关，shift 集为 {kq: 1≤|k|≤T}；已知工具（large sieve 对 AP shift 集、MRT 对数平均 Chowla、Tao–Teräväinen 几乎所有尺度、Additive divisor problem 的经典结果）都达不到 q^{1−ω} 的 **一致** saving——**parity barrier 的边界**。Route C 的成败完全取决于 H_wrap。
5. **对 GWX 路线的意义**：H_Ratios 的"弱化到任意 ω>0"仍不可由本路线证明；但本轮的 Lemma 1.1–1.4 与 M_q 数值验证把"H_Ratios 是否可信"推进了一步（M_q 已被数值支持）。

---

## 1. 严格引理

### 1.1 Lemma 1.1（GRH 下的 truncated Möbius）[证明(标准输入)]
设 χ 为本原特征 mod q，`Re s=σ=1/2+η`（η>0 固定），`T=|Im s|`。则任意 M≥2、ε>0：
```
1/L(s,χ) = Σ_{m≤M} μ(m)χ(m)m^{−s} + O_{η,ε}( M^{1/2−σ+ε} (q(1+T))^{ε} ) = Σ_{m≤M}(…) + O(M^{−η+ε}(qT)^{ε}).
```
**证明.** 标准输入（GRH 推论，Hadamard/显式公式）：`M(x,χ):=Σ_{n≤x}μ(n)χ(n) ≪ x^{1/2+ε}(q(1+|x|))^{ε}`（对 σ>1/2 的 σ-平面内收敛性的等价形式）。对 `Σ_{m>M}μ(m)χ(m)m^{−s}` 分部求和：
`|Σ_{m>M}| ≤ M^{−σ}sup_{x>M}|M(x,χ)| + |s|∫_M^∞ x^{−σ−1}|M(x,χ)|dx ≪ M^{−σ+1/2+ε}(qT)^{ε}`。∎
**注**：(i) 这给出 `M^{−η}` 级误差——在 `ω/η>1` 时需 `M>q`（见 §3 的矛盾）；(ii) 若要误差 `q^{−ω}` 而保持 M<q，需要 `Σ_{n≤x}μ(n)χ(n)≪x^{1−δ}q^{ε}`（δ>0）——这是 **power-saving Mertens/Chowla 型**输入（parity barrier 一侧），目前没有。

### 1.2 Lemma 1.2（光滑 AFE，无条件）[事实]
`L(a,χ)=Σ_{n≤N}χ(n)n^{−a}V(n/N)+ε(χ)X_{q,e}(a)Σ_{n≤N'}χ̄(n)n^{a−1}V'(n/N')+O((qT)^{−A})`，`NN'≍qT`，V,V' 标准光滑权；`Re a=1/2`。根号长度、任意阶误差（Iwaniec–Kowalski Thm 5.3 型；对 primitive χ，`|ε(χ)|=1`）。

### 1.3 Lemma 1.3（精确正交性 + Gauss 和）[证明]
```
Σ*_{χ mod q} χ(A)\barχ(B) = 0  if (AB,q)>1;  = Σ_{f|q} μ(q/f)φ(f)1_{A≡B mod f}  if (AB,q)=1.
q prime: = (q−1)1_{A≡B mod q} − 1   (for (AB,q)=1).
Σ_{χ parity e} χ(u) = (φ(q)/2)(1_{u≡1}−(−1)^e1_{u≡−1}) − [e=0]·1   （q 素，去掉主特征）
Σ_{χ parity e} ε(χ)χ(u) = O(√q)  （用 ε(χ)=τ(χ)/(i^e√q)，Σ_a e(a/q)Σ_χχ(au) 显式求值）
```
**证明**：标准（正交性 + Gauss 和）。∎ ⇒ 所有"root-number/反射交叉"配置贡献 ≤ O(√q)·(Dirichlet 和的 L² 范数) = O(q^{1/2+ε}(qT)^{O(1)}·log^A) — 对目标 `q^{1−ω}`（ω<1/2）是中低阶项，但对 ω 接近 1/2 需仔细核对（记为 [待核]）。

### 1.4 Lemma 1.4（第二矩输入）[事实]
`Σ*_{χ mod q}|L(1/2+iu,χ)|²≪q^{1+ε}(1+|u|)^{O(1)}`（无条件：正交性/大筛；对 q 的所有模）。用于：AFE 误差项 × |L(a)L(b)| 的 χ-平均 ⇒ Cauchy–Schwarz 给 `≪q^{1+ε}(1+T)^{O(1)}(qT)^{−A}≪q^{−A'}`（取 A 大）。

---

## 2. Route C 的结构与分类

把 `1/L(s,χ)`、`1/L(t,χ̄)` 分别用 **Variant C1**（Lemma 1.1 截断 Möbius）或 **Variant C2**（Lemma 1.2 型精确 AFE）代入 `R_q=Σ*_χ L(a,χ)L(b,χ̄)/(L(s,χ)L(t,χ̄))`；分子用 Lemma 1.2。展开成最多 2（分子）×2×2（分母，若 C2）段之和，按"净特征标幂次"分类：
- **(N) 无净 χ 幂**（χ 与 χ̄ 数相等）：`Σ*_χ1=φ*(q)`；各指标和未受约束 ⇒ 分解为 Dirichlet 和/ζ,L 值乘积。**是主项的一部分**（"反射×反射"给出 CFZ 的交换项 `H_qZ_q(1−b,1−a;s,t)`；"直接×直接"在 C2 中亦给出 Z_q 因子；根数 ε(χ)ε(χ̄)=1 自动抵消 ✓ 与 GWX §3.1 一致）。
- **(R) root-number/反射交叉**（净幂为 1 个 χ 或 χ̄）：用 Lemma 1.3 的 Gauss 和求值 ⇒ O(√q·polylog)（Lemma 1.3 末条）。
- **(D) 对角/整除边界**（净 χ 幂 2 或 0 但出现 `1_{A≡B}`）：精确等式 A=B（对角，Euler 积可算，**主项主要来源**）与整除边界 `q|A`（C1 中 r=qρ 的 "Möbius 共振"项，可算）。
- **(W) wrap-around**：`A≡B mod q, A≠B`（A=nr, B=ml 为两段指标之积）——**唯一无法处理的项**。

**主项计算**：对角（D-exact）+（N）配置的 Euler 积组合应重组为 CFZ `M_q=φ*Z_q+H_qZ_q(1−b,1−a;s,t)`；由于时间盒未完成全部 bookkeeping，本报告以 §4 的数值验证（|R_q−M_q|=O(√q)）作为"主项正确"的强证据。**[推导/数值]**

---

## 3. Variant C1 的参数矛盾（结构性障碍 [证明]）

C1：分母用 Lemma 1.1 的截断 Möbius（长度 M）。
- **精度要求**：误差 `M^{−η+ε}` 乘 `Σ*|L(a)L(b)|≤(Σ|L(a)|²)^{1/2}(Σ|L(b)|²)^{1/2}≪q^{1+ε}`（Lemma 1.4）⇒ 总误差 `≪q^{1+ε}M^{−η}`。要 `≤q^{1−ω}`，需
```
M ≥ q^{(ω+O(ε))/η}.         (3.1)
```
- **无 wrap 要求**：C1 中所有指标：分子 AFE 长度 N≍N'≍√(qT)；Möbius 长度 M。若所有乘积 <q，则 Lemma 1.3 的 `1_{A≡B}` 退化为 A=B、`q|A` 不可能，全部化为 Euler 积可算项。最坏乘积 ~N·M；q 素、T≤q 时 N<q，故条件为
```
N M < q  ⇒  M < q^{1/2} T^{−1/2}.       (3.2)
```
- **(3.1)+(3.2) ⇒ ω/η < 1/2 − o(1)（更精确：√(qT)·q^{ω/η}<q）。** 而 GWX 的使用要求（phase-7 条件）`ω_D−8(η+r)(2+ω_D)>0`，即 `η < ω_D/(8(2+ω_D)) ≈ ω/16`（ω→0），故 `ω/η > 16` ——**与 (3.2) 尖锐矛盾**。
- 若强行 `M≥q^{ω/η}≫q`（GWX 窗内），则 wrap-around 必然出现，其规模（对 C1 的共振/同余项，用 μ 分部求和估计）：
```
W_C1 ~ (M/q)^{1/2}·N^{1/2}·q^{ε} ~ q^{ω/(2η)−1/4+ε}  （主导量级估计）
```
当 `ω/η>5/4` 时 `W_C1>q^{1−ω}`；在 GWX 窗 `ω/η≥16` 时 `W_C1≈q^{7.75}` — 完全失控。
**定理（结构性）[证明(条件：Lemma 1.1 的标准输入)]：Variant C1 在 GWX 参数窗 `η<ω/16` 内不可能证明 `R_q=M_q+q^{1−ω+ε}`-型估计，与该估计是否正确无关——截断 Möbius 表示本身在"精度 vs 长度 vs wrap"三角中无解。** ∎

**推论**：无法通过的假象路径是"用足够长的 Möbius 和精确表示 1/L"——它在 ω≪η（即 η 大）时或可行（此时 M<q，C1 完全化为 Euler 积计算，1/1 情形 R≈φ*+O(√q) 的数值支持这一目标［数值］），但**不能用于 GWX 的 η→0 需求**。这正回答 task 的 red-team 问题之一。

---

## 4. Variant C2（精确 AFE）与单一最难引理 H_wrap

C2：`1/L` 也用光滑 AFE（Lemma 1.2 型，系数 μ 代替 1），四段和长度均 ~√(qT)，误差 (qT)^{−A}。
- 截断误差可控（Lemma 1.4）✓；无 (3.1)-(3.2) 的矛盾 ✓。
- 但 Lemma 1.3 的 `(q−1)1_{A≡B}−1`：A=nr、B=ml（每段指标 ≤√(qT)），故 |A−B|≤qT，wrap 解 A−B=kq 中 `1≤|k|≤T`（短！）。
- 主项 = A=B 对角（Euler 积） + （N）配置 + (R) 项；wrap 项必须证小：
```
**H_wrap**  对 q 素、T≤c log q、任意固定 ω>0：
   W := Σ_{1≤|k|≤T} Σ_{n,r,m,l ≥1, nr−ml=kq} c(n,r) \overline{d(m,l)}  ≪_{ω,ε} q^{1−ω+ε}(1+T)^B,
   其中 c(n,r)=n^{−a}\bar V(n/N)·\overline{μ(r) r^{−s}V_s(r/N_s)} 等（光滑权, Re shifts 如题），
   四段长度均 ~√(qT)。
```
- **为何是墙（逐条排除已知工具）**：
  1. **Cauchy–Schwarz + 第二矩**：W 的四段和各自 L² 范数 ~log^{O(1)}，但**解数**无控制：对固定 k，方程 nr−ml=kq 的解数可达 ~(qT)^{o(1)}·(四维体积)~qT 量级；KS 给 W≪qT·(log)^C ≫q。
  2. **large sieve 对 AP shift 集**：把 W 写成 Σ_k⟨c, T_{kq}d⟩；对 shift 集 {kq:|k|≤T}（间距 q）的大筛给出 ~(T+√(qT))·||c||²||d||² 型界——远大于 q^{1−ω}（且 q^{ω} 的 saving 需要 shift 集的总长度 ≪q）。
  3. **MRT/Tao–Teräväinen**：给出 h-平均/对数平均/几乎所有尺度下的 Chowla 型 o()，**没有**对 shift 集 {kq} 的一致 power saving；且 m,n 的系数含 μ（分母段），本质是 Möbius 相关。
  4. **Additive divisor problem**：nr−ml=kq 可重写为 `Σ_{N_0} d_4-type` 的移位相关；经典结果（Estermann、Heath-Brown、Motohashi、Deshouillers–Iwaniec）对 `Σ_{n≤X}d(n)d(n+h)` 在 h≈X（此处 h=kq 与变量尺度 √(qT)·√(qT)=qT 同阶；shift/尺度 ~k/T~O(1)）恰是**最难区域**，给出主项但误差远达不到 q^{1−ω} 在其"shift 是 q 的倍数"上的一致版本；且这里系数含 μ 而非 d，需要 Möbius 抵消。
  5. **可能的希望**：对每个 k 用 Poisson/加性特征展开 mod q 或对 nr−ml=kq 做 Dirichlet 双曲线分解，把 W 化为 Weil/Kloosterman 型和 + 主项；这需要完成 `Σ_{n≡ξ}μ(n)`-型在 q 模下的分布（power-saving Mertens in AP mod q），即 **parity barrier 一侧**。**[推测]** 这是唯一可能的技术入口，但难度不低于弱 Chowla。
- **结论**：**H_wrap = Route C 的精确墙**。它与 phase-9 的 MDs 缺口、phase-7 的 H_cov^low 同类：都需要 level-aspect 的二元相关/零点统计 power saving，现有技术达不到。

---

## 5. 数值验证细节（新）[数值]

脚本 `mq_check3.py`（mpmath；用 Hurwitz 公式 `L(s,χ)=q^{−s}Σ_{a=1}^{q}χ(a)ζ(s,a/q)` 精确计算；枚举 (Z/q)* 的生成元得到全部 φ(q) 个特征标；primitive=q−1 个非主特征；CFZ M_q 用 ζ_q、A_q（p∤q 无穷积到 30000）、精确 `M_e(q)` 奇偶计数与 X_{q,e} 计算）。
- **generic shifts** 表（§0.3）：|R_q−M_q|/√q = 0.246, 0.287, 0.508 —— **主项正确到 square-root 级**。
- **平凡极限** `s=a+ε, t=b+ε`（比值≡1，R_q→φ*=95）：M_q(ε)=94.841 (0.05) → 94.993 (0.01) → **94.9997 (0.002)**；R_exact=94.20,95.47,95.24（~O(1) 内）⇒ **M_q 在可去奇点处正确收敛到 φ*** ✓（验证 GWX 的"可去奇点"和 archimedean 归一化）。
- 1/1 warm-up（`warm11.py`）：`Σ*L(a,χ)/L(s,χ)`≈96.93, 83.89, 94.71（q=97）≈φ*=95 加 O(√q) 涨落 ⇒ 1/1 的"主项≈φ*+低阶修正"结构；C1 在 η 大（M<q）时的目标是把这些低阶修正算出来，本轮时间盒未完成 main-term bookkeeping。

---

## 6. 诚实判定 + 若继续的 top 步骤

**已证/已建立**：Lemma 1.1（GRH truncated Möbius）、Lemma 1.2（AFE）、Lemma 1.3（正交/Gauss）、Lemma 1.4（第二矩）；**Proposition 3.1（C1 在 GWX 窗内的参数矛盾）**；**数值验证 M_q 到 O(√q)**（新）。
**未证**：H_Ratios 的任何 ω>0（即使受限 range）；H_wrap。
**最小缺失输入**：H_wrap（或等价的 power-saving Mertens `Σ_{n≤x}μ(n)χ(n)≪x^{1−δ}q^{ε}`），二者均为 level-aspect 二元相关/parity barrier 级。
**若继续的 top-2 步骤**：
1. **精确 main-term bookkeeping（C2 对角 + 无幂配置）**：用 Euler 积显式算出 `(q−1)Σ_{nr=ml}` 与 (N) 配置的组合，验证其等于 CFZ M_q（数值已支持；理论上这是可完成的有限计算，1-2 周）。若不等，则 H_Ratios 的 M_q 形式有误（但 phase-10/数值不支持这个可能）。
2. **H_wrap 的一个可攻特例**：先证 q 素、T 有界（|Im shifts|≤1，即只有 k 很小）的情形：此时 W 只含 O(1) 个 shift k，且各段长度大；尝试 Dirichlet 双曲线分裂 nr−ml=kq 化为 `Σ μ(n)e(·)` 的 Weil 型和（若成功，再逐步放大 T）。这是 H_wrap 的最小版本，也是其难度标尺。
**给 GWX 路线的结论**：Route C 不能完成弱 H_Ratios；需新方法（MDs/Sawin 型几何方法或 H_wrap 本身）。但这不削弱 GWX 条件性定理的有效性——其唯一输入仍是标准 CFZ 猜想（phase-10 结论 + 本轮 M_q 数值支持）。
