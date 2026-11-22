# Phase-10 报告：GWX 路线最弱输入的数值与理论核查

> **【phase-11b 数值修正，2026-11-21 23:55】本报告 §1 的复合导子数值检验有实现 bug，须以修正版为准。**
> phase-10 的 `mainterm.Aprod` 用 mask `(PRIMES % q != 0)`（测试 "q∤p"）代替正确的 "p∤q"，把整除 q 的素数错误地计入 A_q。对素数 q 无影响（故 §1 素数结论保留），但复合/ramified q 的 |E−M| 数值被系统性污染。phase-11b 修正 mask 后：q=2^e（e=8..18，40 shifts）RMS/√q = 2.1–5.0（原来 2.31→49.16），拟合 α=0.537±0.032（sqrt 标度），**"ramified 无 saving 异常"消失**；GWX (3.2) 主项（A_q over p∤q，ζ_q 每个不同素数一次）本身正确。修正后的复合导子表见 `phase11/numerics/ramified-crosscheck.md`（spectral-numerics）。**结论方向不变：H_Ratios 误差 ~q^{1/2+o(1)} 在全部导体类上数值成立。**

> 2026-11-21 21:10。任务：检验 GWX（Gou–Wang–Xu, arXiv:2611.18825）路线唯一非文献性输入——**复合导子的 parity-resolved Ratios 主项 M_q**。
> 参与：liu-auditor（GWX 归约审计，phase-8）、kernel-theorist（CFZ 主项对照，task-35）、spectral-numerics（复合 q 数值检验，task-34）。
> 标签：[数值]/[推导]/[证明]/[事实]。**所有结论非证明。**

---

## 0. 结论

1. **GWX 归约经独立审计为正确**（liu-auditor，`phase8/audit/gwx-audit.md`）：Theorem 1.1（GRH + H_Ratios ⇒ Goldbach）的证明逐步重建全部对上，未发现致命数学错误；唯一实质额外输入 = **复合导子、精确 parity-resolved 主项的 Ratios 平均**。
2. **H_Ratios 的主项 = CFZ 2008 标准 recipe 的自然特化**（kernel-theorist，`phase10/theory/ratios-mainterm.md`）：两项结构（对角 + 仅分子函数方程反射）、`ζ_q`、`A_q`、`H_q=Σ_e M_e(q)X_{q,e}(a)X_{q,e}(b)` 均是自然求值；prime q 即 Wang–Xu Conjecture 2.1（文献），composite q 是 GWX 明确承认的唯一外推；极限自洽性 `s→a,t→b ⇒ M_q→φ*(q)` 解析通过。
3. **数值检验通过**（spectral-numerics，`phase10/numerics/ratios-composite.md`）：23 个导子（q=53…2003，含 prime 与多种复合/平方因子 q），H_Ratios 主项与 `E_q=Σ*_{χ mod q primitive} L(a,χ)L(b,χ̄)/(L(s,χ)L(t,χ̄))` 匹配；`|E_q−M_q|/√q` 素数 3.9–11.1、复合 0.3–2.7，**无随 q 增长趋势**；复合 q 与同尺度素数行为一致，无 composite 特有失效；**无系统性 parity 偏差**（even/odd 权重对调后误差显著变差；删 H_q 后误差放大 5–18×）。
4. 因此：H_Ratios 的可信度 = 标准 CFZ 猜想级别；composite 部分应严格表述为 "CFZ08/WX25 composite-conductor extension (GWX 2026)"。**Goldbach 归约链 = Alpöge GRH（已声明、官方验证未完成）+ H_Ratios ⇒ Goldbach**，唯一剩余障碍是证明该 Ratios 猜想（复合导子版、任意固定 ω_D>0、uniform shifts）。

---

## 1. 数值检验（task-34）细节

- 方法：mpmath Hurwitz ζ + 精确 primitive 字符表；`L(u,χ)=q^{−u}Σ_{a∈(Z/q)^*}χ(a)ζ(u,a/q)`；q=53…2003 共 23 个（含 60,120,720,900,1000,1260,1680,2000 等），6 组 shifts × η∈{0.1,0.2}；对 H_Ratios 公式做 4 种转录变体比较。
- **最佳变体**（=phase-8 审校 boxed 形式）：`|E_q−M_q|/√q`：素数 q 3.9–11.1、复合 q 0.3–2.7；相对误差 `|E−M|/|M|`：q≥720 时 0.06–0.75（q=1000: 0.23；q=1009: 0.057；q=2000: 0.35）。
- **变体仲裁**：唯一支持 `H_q=Σ_e M_e(q)X_{q,e}(a)X_{q,e}(b)` 与 `Z_q` 分母 `(a+d)(b+c)`（+对应 A_q）；phase-9 文档里的 `X_{q,e}(1−b)X_{q,e}(1−a)` 写法在全部 23 个 q 上误差更大（不随 q 降）；swap-Z 同样失败。
- **共轭问题（重要修正）**：E_q 必须是 `L(a,χ)L(b,χ̄)/(L(s,χ)L(t,χ̄))`（GWX 原文/(3.3)）；无共轭版本不匹配（rel 0.06–6.5，移位相关大偏差）。之前 task 文字漏写共轭，已修正。
- **parity 检验**：even/odd 的 M_e 权重对调后误差显著变大（correct-vs-swapped：各 20/23 个 q 正确分配更好；even 最多改善 ~10×，odd 2–4×；q=503 even: 0.14 vs 0.88；q=1000: 0.23 vs 1.68；q=2003: 0.12 vs 2.57）；残差 even/odd 无系统偏向。**H_q 项必需**（删掉后误差放大 5–18×）。用 φ*/2 近似代替精确 M_e 的误差 0.16–0.55，与本征误差同量级 ⇒ 本数据无法分辨精确 M_e vs φ*/2。
- **最大相对偏差**：出现在最小 q 与接近 Z_q 小分母的移位（q=60: 4.53；q=503 一组小分母移位 |E−M|/√q 最大 41.6）；是移位依赖的常数放大，非随 q 增长；一般移位 |E−M|/√q=O(1)，与 H_Ratios 的 `q^{1−ω_D}(1+T)^B` 尺度（ω_D=1/2）定性一致（本数据不能定 ω_D 精确值）。
- **澄清**：(a) **v2(q)=1 的 q（如 30,42,210,330）不存在导子恰为 q 的本原特征** ⇒ E_q=0、φ*=0、M_q=0，两边恒等；有意义的复合导子须 4|q 或 q 奇（本报告覆盖 60/84/105/120/140/165/360/420/720/900/1000/1008/1260/1680/2000）。这不威胁 G-W-X（其求和只遍历 φ*(q)≠0 的 q|N），但 H_Ratios "每个整数 q>1" 在这些 q 上 vacuous。(b) phase-8 的 `check_parity.py` 曾把 principal 特征计入 primitive，不能复现审计报告的 "~1e−31"；primitive-only 独立实现把 (3.3) 复现到 **1.5×10⁻¹⁵** —— 审计结论不变，数值证据应以修正脚本重记。
- **caveats**：q≤2003、|Im|≤2（远小于 H_Ratios 的 T≤100log2q）；未直接检验 `a+b=1` 可去极点邻域与圆盘全纯性。

---

## 2. H_Ratios 的精确陈述（canonical，待正式引用）

存在固定 0<ω_D≤1/2、η₀>0、B≥0，使对每个 0<η<η₀、每个 ε>0、每个整数 q>1（含复合导子；v2(q)=1 时该族为空），
`Σ*_{χ mod q primitive} L(a,χ)L(b,χ̄) / [L(s,χ)L(t,χ̄)] = M_q(a,b;s,t) + O_{η,ε}(q^{1−ω_D+ε}(1+T)^B)`，
uniformly for ℜa=ℜb=1/2, ℜs=ℜt=1/2+η, T=max|ℑ·|≤100log(2q)，且在 (a,b) 的固定圆盘上全纯；
`M_q = φ*(q)Z_q(a,b;s,t) + H_q(a,b)Z_q(1−b,1−a;s,t)`，
`Z_q=ζ_q(a+b)ζ_q(c+d)/(ζ_q(a+d)ζ_q(b+c))·A_q`，`ζ_q(s)=ζ(s)∏_{p|q}(1−p^{−s})`，
`A_q=∏_{p∤q}[(1−p^{−c−d})(1−p^{−a−d}−p^{−b−c}+p^{−c−d})]/[(1−p^{−a−d})(1−p^{−b−c})]`，
`H_q(a,b)=Σ_{e=0,1}M_e(q)X_{q,e}(a)X_{q,e}(b)`，`X_{q,e}(w)=(q/π)^{1/2−w}Γ((1−w+e)/2)/Γ((w+e)/2)`，
`M_e(q)`=primitive χ mod q 中 χ(−1)=(−1)^e 的个数，φ*=M_0+M_1。
- 任意固定 ω_D>0 够（有效 saving ω=ω_D−8(η+r)(2+ω_D)>2η）；定性 Goldbach 可弱化为 ω_D(q)log q→∞。
- GRH 在 GWX 证明中用于三处：(2.21) 移轮廓、(3.25) 的 1/L 与凸性界、尾巴积分；Ratios 本身不依赖 GRH。

---

## 3. 与 H_Gold 比较（phase-8 审计）

- 不等价、不可互推：GWX+GRH 的终点是 **sharp 未加权计数** `Σ_{m+n=N}Λ(m)Λ(n)=N·S(N)+O(N^{1/2+ε})`（更强），H_Gold 是光滑加权渐近。
- 假设层面：H_Ratios 是标准型 Ratios 猜想（CFZ/WX25 + 复合导子精确 parity 主项），比 LL 的 R/S/H_Gold（ad hoc、需跨 χ 四阶零点相关）**更主流、更可陈述**。
- **GWX 路线是当前最有希望的 Goldbach 归约**；若 Alpöge GRH 验证通过，仅剩 H_Ratios。

---

## 4. 剩余缺口与下一步

1. **H_Ratios 本身**：over ℚ 无任何族的完整 Ratios 证明；函数域有 Sawin 2024 类比；phase-9 的 L1/L2（level-aspect 2/2 MDs、二阶矩/对数导数混合项）是长期研究前沿，非"范围提升"。
2. **数值**：本检验只覆盖 q≤2003、|Im|≤2；G-W-X 需要 T≤100log2q（q=2000 时 ~760）——大 shift 与圆盘全纯性未检验。
3. **v2(q)=1 的 vacuous 情形**：H_Ratios 的"每个 q"表述应加"或该族为空"的注；不影响 GWX。
4. 若继续：优先做 **L2 的 A=0 固定 shift 大筛型估计**（GRH 下可能可达），它是 L1 之前最现实的第一步；以及把 H_Ratios 作为公开的"最小假设"正式表述。

---

## 5. 文件
- `phase8/audit/gwx-audit.md`（GWX 归约审计，liu-auditor）
- `phase10/theory/ratios-mainterm.md`（CFZ 主项对照，kernel-theorist）
- `phase10/numerics/ratios-composite.md` + `cache/final_data.json` + logs（复合 q 数值，spectral-numerics）
- `phase8/lit/ratios-status.md`（gap 表，goldbach-researcher）
- `phase9/theory/ratios22.md`（MDs 可行性，kernel-theorist）
- `0-九阶段总报告.md`（项目总报告）
