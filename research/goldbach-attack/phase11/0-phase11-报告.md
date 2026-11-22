# Phase-11 报告：攻击唯一剩余缺口 H_Ratios —— Route C 的结构性判定、移位区域弱 Ratios 定理、误差项数值验证与 H_Ratios^min

> 2026-11-21（phase-11 + phase-11b）。**目标**：在 phase-10 把 Goldbach 归约为 "GRH（Alpöge/Claude，已声明）+ H_Ratios（GFZ/WX25 型 Ratios 猜想的复合导子加强版）" 之后，尝试**证明 H_Ratios**（任何固定 ω_D>0 的 power saving 都足以完成 GWX 定理）。
> 参与：liu-auditor、kernel-theorist、spectral-numerics、heat-kernel-critic、goldbach-researcher、proof-digest、repo-verifier、lean-feasibility、Lead。全部文件在 `_rh-work/goldbach-attack/phase11/`。
> 标签：[事实]/[证明]/[推导]/[数值]/[推测]/[预印本]。**没有任何 H_Ratios 的证明；本阶段的结论是"边界刻画"。**

---

## 0. 结论速览（10 条）

1. **H_Ratios 仍是唯一缺口**，本阶段没能证明它；但被**完全刻画**：临界线（η→0）情形 ↔ 已知的 parity barrier 类障碍（H_wrap），而**离开临界线固定距离 η 的移位区域，Ratios 可以被证明**（Lead §4：saving ω<η/2 的弱 Ratios 定理 + Euler 积恒等式数值验证）。
2. **Route C（截断 Möbius + AFE + 精确正交性）被证明在 GWX 参数窗内结构性不可行**（kernel-theorist Prop 3.1；liu-auditor 独立审计同意）：精度要求 M≥q^{ω/η}、避免 wrap 要求 M<q^{1/2}T^{−1/2}，相容需 ω/η<1/2；而 GWX 的插值/轮廓机制需要 ω/η>16 ⇒ 矛盾，与估计好坏无关。
3. **临界线情形的精确墙 = H_wrap**：`Σ_{1≤|k|≤T}Σ_{n,r,m,l: nr−ml=kq}c(n,r)d(m,l)̄ ≪ q^{1−ω}`（additive-divisor 型移位相关，μ 权，shift 集合 {kq}）；trivial/Cauchy–Schwarz 给 ≫q，MRT/Tao–Teräväinen 只有 h-平均/对数平均/几乎所有尺度，无一致 power saving ⇒ 与 Chowla/零点对相关同级（parity barrier 一侧）。
4. **H_Ratios 的误差项在全部导体类上数值成立**（[数值]）：素数 q=1e3…1e6：RMS/√q 平坦（6.95–11.27），拟合 **α=0.562±0.011**；修正 A_q 后 ramified 类：2^e **α=0.537±0.032**、3^e 0.528±0.017、5^e 0.549、7^e 0.489、混合 4p/8p/9p **0.553±0.025**；无 q 级系统主项遗漏（signed mean ~1/√n）；T 依赖多项式 B=0.43±0.18。**即 ω_D≈1/2 的 q^{1/2+o(1)} 误差在数值上成立。**
5. **重要修正（phase-11b）**：phase-10/11 早期报告的"ramified 无 saving 异常"是**代码 bug**（A_q 的 mask 用 `q∤p` 而非 `p∤q`），不是 GWX 的错误。修正后异常消失；GWX (3.2) 主项（A_q over p∤q、ζ_q 每个不同素因子一次、H_q=Σ_e M_e X_e(a)X_e(b)）在 composite/ramified q 上也正确。phase-10 复合导子数值表已重算（|E−M|/√q 仍 O(1)，多数改进）。
6. **H_Ratios^min 已精确化**（liu-auditor）：等价于 GWX Hypothesis 1.1 的实质内容；逐点 in q 本质必需；可弱化为"临界线逐点 + 分子移位盘上 L² 平均界"；ω_D(q)log q→∞ 只对定性 Goldbach 足够且需要额外 H_UNIF；T≤90log(2q) 足够；保留精确 M_q；v2(q)=1 为 vacuous。**cxy0714 的"缺少 uniform 条款"疑问不成立**（三线插值高度 90log<100log、误差全纯性可由 GRH 结构提供；唯一非标准是复合导子精确主项，已写在假设内）。
7. **GWX 归约不受影响**：Theorem 1.1 的条件链仍是 "GRH + H_Ratios ⇒ Goldbach"，本阶段没有发现 GWX 的错误；唯一 exposure 是 composite conductor 的精确主项重组没有在论文中写出（[推测] exposition 完整性建议，不是 gap）。
8. **Lean**：GWX (3.1) parity projection 恒等式已**完整机器验证**（`lake env lean` exit 0；7 条定理公理均为 `[propext, Classical.choice, Quot.sound]`；Mathlib v4.36.0）。`Σ_{q|N}φ*(q)=φ(N)` 因 Mathlib 缺 primitive-character 计数/conductor 分解未完成（精确缺口清单已记录）。
9. **状态**：MIT GRH 页 2026-11-21 12:55 UTC 又更新一版（只扩文字+GRH scope，检查表仍 3 项 running，无新产物）；上游 repo/archive 无变化；无 peer review；PhilArchive 质疑仍 403 不可读。档案内部含**以 theorem 证明的定量机器**（Siegel 下界、Siegel–Walfisz、Dirichlet/ζ 零自由区、显式公式显式常数、L'/L 上界、零点计数、零密度、均方），**但无 moments/ratios/family averages/pair correlation**（旧结论"无任何量化内容"需按此修正）。
10. **下一阶段方向**：H_wrap 最小特例（q 素、|Im|≤1、O(1) 个 shift k）作为难度标尺；Baluyot–Čech 2025（arXiv:2501.12529）的 conductor-aspect MD 猜想框架（但仅 q-平均/光滑/shift 小范围）；函数域 2/2 Ratios（Bui–Florea–Keating 2023 仅 quadratic 族）；持续跟踪官方 RH 验证与 2026 新文献。

---

## 1. 文献与状态（phase-11：goldbach-researcher task-39、proof-digest task-40、repo-verifier task-41）

### 1.1 WX25 与 Ratios over ℚ 的已知最强状态
- **[事实] WX25 = Wang–Xu, "Harper's beyond square-root conjecture", IMRN 2025 no.18 rnaf279, arXiv:2405.04094v2。** Conjecture 2.1 只覆盖**素数导体** r 的 Dirichlet 特征族（χ≠χ0），误差 `O((1+T)^ε r^{−ω})`；**WX25 没有证明任何情形**（Thm 1.2 是 GRH+Ratios 条件性的）。GWX Hypothesis 1.1 是把 WX25 外推到**所有 primitive 导体（含复合）**并指定 ω_D 的强化版。
- **[事实] 2024–2026 无一般 Dirichlet 族 2/2 Ratios 的新定理。** 最强已知仍是：Čech (Trans. AMS 377 (2024) 9113) 实特征、单 shift、受限、GRH 条件；Gao–Zhao 2022–24 二次/三次/四次族、单 shift、受限、GRH 条件；Bui–Florea–Keating (Trans. AMS 376 (2023)) 函数域 **quadratic** 族 2/2 Ratios（分母 shift Re≫g^{−1/4+ε}）；Sawin (Acta 233 (2024)) 是 F_q[t] 上 squarefree progressions 的 level of distribution（G-W-X 函数域部分的输入），**不是** Dirichlet 族 Ratios 的证明。
- **[事实] Baluyot–Čech arXiv:2501.12529 (2025)** 首次研究 "all even primitive Dirichlet characters of conductor ≤Q" 的 conductor-aspect MD，k=2 对象形式上就是 q-平均 2/2 ratio 形状；但只做到极点/留数 + 单个 L 的函数方程 + **对亚纯延拓提出猜想**；且 shift 需 |s−1/2|≪1/log Q、是光滑 q-平均 ⇒ 距 GWX 的固定 η、逐 q 一致还差三关（O4/O5）。
- **[事实] 一般 primitive 族缺"额外函数方程"**：二次族靠 theta/二次互反延长 MDs；General primitive Dirichlet 族无对应物（Saha 2017 摘要直接作证 "seems difficult to obtain such a translation formula…"）。这是 phase-9 裁决的核心结构障碍。
- **[事实] 条件性 binary Goldbach 路线只有两条**：GWX（GRH+RC_D(ω_D)）与 Li–Liu（GRH+Hypothesis S/R）；**没有找到比 H_Ratios+GRH 更弱的不同条件路线**。GRH 单独只给例外集 E(x)≪x^{1/2+ε}（almost-all）；EH/BV/BFI 只到 (1+2)/(1+1.9)/(1+1.4)；Chowla/Lindelöf/Hooley 均未知蕴含 binary Goldbach。'GRH-alone hope' 在 WX25 中指的是 Harper 猜想（一点 λ 矩），不是 Ratios，不能绕到 2/2。
- **[事实] 2026 新文**：Lee arXiv:2610.32672 v2 (2026-11-03) 覆盖所有固定正偶数间隔、弱化 ratios 假设、改进误差；GWX 仍 v1（2026-11-13，另有 Hexagon deposit）；无引用/评审/勘误（Semantic Scholar 为空；唯一外部评论 cxy0714 是未核验 AI 辅助综述，其"缺少 uniformity"疑问被 liu-auditor 否定）。

### 1.2 官方验证与上游状态（repo-verifier task-41，检查窗口 2026-11-21 15:09–15:49 UTC）
- **[事实]** MIT 页 12:55 UTC 更新（20,460 B，sha256 e4648882…）：逐条列出五定理 + 新 scope 段（"GRH" = Dirichlet L-functions：所有模与所有特征；Dedekind/Hecke/automorphic 不在检查范围），删除旧 caveat；**检查表仍 3 项 running**（主证明 kernel replay、主证明 lake comparator、组合算术导出 comparator）；`paranoid.log`/`comparator.log` 404；`SHA256SUMS` 自 09:21:33 GMT 未变。**不可宣称官方验证完成/peer review。**
- **[事实]** 本地 /home/kiler/rh-full HEAD 7cbf7a0c3…、upstream pushed_at 2026-11-20T15:13:36Z、仅 1 release、README 哈希一致；alpo.ge part01 哈希与已存分片相同 ⇒ 2026-11-20 22:05 UTC 后无新内容。
- **[事实] 量化内容修正**：档案内部含**以 theorem 证明的定量机器**：`Formalism/ZeroFreeRegion/FinalZFR.lean` `zeroFreeRegion`；`LandauZeroFreeBounds/NoZeroComplex.lean` `zFRDirichlet`（含显式形式 1−c/log(q(|im|+2))）；`FinalSiegel.lean` `siegelLower`；`SiegelWalfiszAPOfSiegelLower.lean` `siegelWalfisz`；显式公式带显式常数（ExplZeta/ExplChi/LogDerOne/ZeroCount）；零密度 `zero_density_box`；均方 `rankin_mean_square` 等。**但没有 pair correlation/moments of ζ,L/ratios/family averages** ⇒ 不能由此得到新的定量零点分布定理。公开最终结论仍只是定性 RH/GRH + Robin/Lagarias 不等式。
- **[事实]** 批评：PhilArchive Nielsen "Invalidity…" 仍 403；Lean 社区博客 "Lean verification of the Riemann Hypothesis" 三路抓取失败（未读）；Tao 博客无新帖（评论 31→61）。

---

## 2. H_Ratios^min（liu-auditor task-37，`phase11/theory/minimal-hypothesis.md`）

**Boxed（= GWX Hypothesis 1.1 的实质内容）**：存在固定 0<ω_D≤1/2、η₀>0、B≥0，使对每个 0<η<η₀、每个 ε>0、每个整数 q>1 且 φ*(q)>0，
```
Σ*_{χ mod q} L(a,χ)L(b,χ̄)/(L(s,χ)L(t,χ̄)) = M_q(a,b;s,t) + O_{η,ε}( q^{1−ω_D+ε}(1+T)^B ),
```
一致于 Re a=Re b=1/2、Re s=Re t=1/2+η、T≤100log(2q)，误差在分子移位盘上全纯；`M_q=φ*Z_q+H_qZ_q(1−b,1−a;s,t)`（H_q=Σ_e M_e X_{q,e}(a)X_{q,e}(b)，Z_q=ζ_q(a+b)ζ_q(s+t)/(ζ_q(a+t)ζ_q(b+s))·A_q，A_q over p∤q，ζ_q(s)=ζ(s)∏_{p|q}(1−p^{−s})）。**加 GRH ⇒ GWX Thm 1.1：Σ_{m+n=N}ΛΛ=N𝔖(N)+O(N^{1−ω_D+ε})；任何固定 ω_D>0 足够，ω_D=1/2 最优。**

六项 weakening 结论：
| 条款 | 是否可弱化 |
|---|---|
| (i) 逐点 in q（每个 φ*(q)>0 的 q 都是某偶数 N 的 conductor：q odd⇒N=2q，4\|q⇒N=q） | **本质必需**，无实质减弱 |
| (ii) 全纯误差 + 点态界 | 可弱化为"临界线逐点 + 分子移位盘上 L² 平均界"（三线插值只用临界线；Cauchy 求导由 F_q 全纯 + mean value） |
| (iii) ω_D(q)log q→∞ | 只对**定性** Goldbach 足够，且需额外 H_UNIF（误差常数对 η 的多项式控制）；原始"每个固定 η 各自 O_{η,ε}"不足以令 η=η(N)→0；固定 ω_D 版无需此项 |
| (iv) T≤100log(2q) | 实际只需 T≤(90+o(1))log(2q)（三线矩形边界 10log+L=90log），100 有余量 |
| (v) 精确 M_q vs φ*/2 近似 | φ*/2 近似差 O(q^ε) 虽在误差内，但可能破坏 F_q 在 a+b=1 的可去奇点/全纯性 ⇒ 保留精确 M_q 最安全 |
| (vi) v2(q)=1 的 q | φ*(q)=0（(Z/2m)*≅(Z/m)*，无 primitive conductor 2m），求和空、M_q=0，纯 vacuous，可删 |

**cxy0714 疑问裁决：不成立。** Hypothesis 1.1 + GRH 足够，无需额外 uniformity clause；三线插值边界高度 90log<100log 恰在 T 界内；ξ=1/8 用 GRH 凸性 + 1/L 界；>100log 尾巴用 GRH strip 界 × e^{−Im ξ²}；误差全纯性甚至非必需（仅为 Cauchy 求导方便）。唯一"非标准"是**复合导子的精确 parity-resolved 主项**，它已明确写在 H1.1 中（phase-8 已指出），不是 missing clause。

---

## 3. 误差项数值验证（phase-11：spectral-numerics task-36/44、heat-kernel-critic task-42；全部 [数值]）

### 3.1 方法
- 新 fast 管线：CRT 分解的 character DFT（素数 q：primitive root dlog 的 1D FFT；p^e：local cyclic；2^e：Z/2×Z/2^{e−2}；squarefree 混合：多维 FFT）；Hurwitz ζ 用 numpy 向量化 Euler–Maclaurin（N≈20,K≈10），与 mpmath dps=30 校验 <1e-10；M_q 用 mpmath ζ + numpy Euler 积（primes≤1e6）。
- 独立校验：heat-kernel-critic 自己代码（mpmath Hurwitz，自写字符群，T T^H=φI 1e-9、#primitive 公式全部吻合、L vs 直接 Dirichlet 级数 1e-10–1e-14）复现同样的误差尺度；spectral 的 fresh char-by-char mpmath 与 fast 管线 |ΔE|/|E|≤1.7e−14。

### 3.2 主结果（修正 A_q 后；RMS over shifts）
| 导体类 | q 范围 | RMS/√q | 拟合 α（RMS∝q^α） |
|---|---|---|---|
| 素数（60 shifts） | 1009–1002241 | 6.95, 7.58, 7.60, 7.61, 7.85, 7.78, 9.88, 10.93, 11.27（×993 in q 仅 ×1.62） | **0.562±0.011** |
| squarefree 大素因子 | 101·103–1009·1013 | 7.5–13.3 | ≈0.56 |
| 2^e | e=8…18 | 2.10,5.04,2.89,3.45,3.97,3.70,4.22,2.91,3.63,4.29,3.87 | **0.537±0.032** |
| 3^e | e=7…12 | 3.76,3.46,3.65,4.38,4.23,3.98 | 0.528±0.017 |
| 5^e / 7^e | — | — | 0.549±0.082 / 0.489±0.139 |
| 混合 ramified 4p/8p/9p | q=4036…999981 | 2.57–5.06 | **0.553±0.025** |

- **结论：所有导体类 RMS|E−M| ≈ q^{1/2+o(1)}（α≈0.53–0.56，符合 ω_D=1/2）**；α≥0.9（无 power saving）在素数样本上约 2.4σ 排除；RMS/(q/p) 在修正后**递减**而非常值。
- **无缺失主项**：每 (q,η) 对 shifts 的 signed mean |mean(E−M)|/RMS ≈ 0.16 ≈ 1/√60；从未出现 O(q) 级系统项。
- **T 依赖**：q=99961, T=2,5,10,20：RMS=2843,5424,7230,6388 ⇒ (1+T)^B，B=0.43±0.18（多项式，非指数）。
- **全纯性/near-pole 探针**：Re a=1/2±1/16,±1/8 有界（555–953 vs 738）；a+b→1 残差饱和 ~500 而 |M|→3.4e4 ⇒ 可去极点一致。
- **η 依赖报警**：heat-kernel-critic 发现 η=0.02 时相对残差 1.95–7.12（q=2000）；H_Ratios 的 O_{η,ε} 允许 η 依赖，故不构成反例，但 GWX 若用 η→0 必须显式追踪 η^{−A} 常数（见 phase-11 报告 §2 的 L²/H_UNIF 讨论）。

### 3.3 重要修正：A_q mask bug（phase-11b）
- **[事实]** phase-10 代码 `mainterm.Aprod` 用 `mask=(PRIMES % q != 0)`（测试 "q∤p"）而非 "p∤q"，对 composite q 错误保留整除 q 的素数。对素数 q 不可见（相 conditions 重合），故所有素数结论不受影响；复合/ramified 早期数值被污染。
- **[数值] 修正后**：ramified 类 α 从 0.93–0.98 回到 0.53–0.55；phase-10 复合表重算（|E−M|/√q old→new）：720: 0.625→0.261；2000: 2.689→1.540；1260: 0.678→0.437；1008: 0.672→0.522；105: 0.636→0.521；140: 0.376→0.291；360: 0.837→0.574；165: 2.140→1.949；1000: 1.454→1.878（median rel 0.231→0.226）；prime 2003 不变。**phase-10 "复合主项匹配" 结论恢复并改善；"ramified H_Ratios 为假"的早期推断已撤回。**
- 另：Lead/heat-kernel-critic 的早期 ramified 检查代码也有同类 mask 缺陷（只排除 p==q），已注明。

---

## 4. Route C（截断 Möbius + AFE + 精确正交性）：能走多远（kernel-theorist task-38、liu-auditor task-37 Part B；`phase11/theory/route-c.md`、`route-c-audit.md`、Lead `lead-route-c.md`）

### 4.1 已证/已核实的引理
1. **[证明, GRH] Lemma 1.1**（kernel-theorist）：`1/L(s,χ)=Σ_{m≤M}μ(m)χ(m)m^{−s}+O(M^{1/2−σ+ε}(q(1+|t|))^ε)`，σ=1/2+η ⇒ 误差 M^{−η+ε}(qT)^ε。
2. **[事实] Lemma 1.2**：分子光滑 AFE（长度 √(qT)，误差 (qT)^{−A}）。
3. **[证明] Lemma 1.3**：primitive 特征标精确正交性（q 素 `(q−1)1_{A≡B}−1`；一般 q 用 Σ_{f|q}μ(q/f)φ(f)1_{A≡B mod f}）+ Gauss 和求值 `Σ_χ ε(χ)χ(u)=O(√q)` ⇒ 反射/根数交叉配置 ≤O(√q·polylog)。
4. **[事实] Lemma 1.4**：`Σ*|L(1/2+iu,χ)|²≪q^{1+ε}`（无条件，大筛/正交性）⇒ AFE 误差复合后可控。
5. **[推导/数值] Lead 的 C1 族平均验证**：对全部 primitive χ 取 RMS，`|1/L−P_X|` 严格按 X^{1/2−σ}=X^{−η} 衰减：q=337 拟合 −0.102/−0.254/−0.403（η=0.1/0.25/0.4，预测 −0.10/−0.25/−0.40），q=1009 −0.093/−0.240/−0.389；无 q^{1/2} 增长 ⇒ 截断基础成立。

### 4.2 结构性不可能（Prop 3.1，[证明]）
- 精度要求：要 q^{−ω} 误差需 M≥q^{ω/η}；避免 wrap（所有指标乘积<q）需 M<q^{1/2}T^{−1/2} ⇒ 相容需 ω/η<1/2−o(1)。
- GWX 应用需要有效 saving `ω_D−8(η+r)(2+ω_D)>0` ⇒ η<ω/16 ⇒ ω/η>16。**尖锐矛盾**；强行 M≫q 时 wrap 共振项 ~q^{ω/(2η)−1/4+ε}，在 ω/η≥16 时 ~q^{7.75}，失控。⇒ 无论估计好坏，"用足够长 Möbius 精确表示 1/L"这一步在 GWX 参数窗内原理上走不通。
- liu-auditor 独立审计：正交性后的核心是 wrap-around 双线性型 Σ*_χ U(χ)V(χ̄)；GRH 级唯一可用的大筛/Cauchy 界 ≈q^{1/2+2ω/η}(log q)/η，与目标 q^{1−ω} 需 2ω/η≤1/2−ω 而插值要求 η≪ω ⇒ 无解；闭合需 Type II/Chowla 型估计，与 H_Ratios 同级 ⇒ 循环。

### 4.3 精确墙 H_wrap（[推导]）
variant C2（1/L 也用精确 AFE）的唯一未解决项：
```
W = Σ_{1≤|k|≤T} Σ_{n,r,m,l≥1, nr−ml=kq} c(n,r)d(m,l)̄ ≪ q^{1−ω+ε}(1+T)^B,
```
四段长度 ~√(qT)、系数为光滑权（分母段含 μ）。trivial/Cauchy–Schwarz 给 ≫q；对 shift 集 {kq} 的大筛给 (T+√(qT))·L² 界，远大于 q^{1−ω}；MRT/Tao–Teräväinen 只有 h-平均/对数平均/几乎所有尺度，无对 {kq} 的一致 power saving；`nr−ml=kq` 是 additive-divisor 型移位相关（shift 尺度 ~kq 与变量平方 ~qT 同阶 = 最难区域）且系数含 μ。唯一可见入口（Poisson/双曲线分解到 Weil/Kloosterman 和 + `Σ_{n≡ξ mod q}μ(n)` 的 power-saving Mertens）本身是 parity-barrier 一侧。**精确墙陈述：弱 H_Ratios ⇐（Lemma 1.1–1.4 全部成立的前提下）H_wrap；H_wrap 与 phase-9 的 MDs 缺口、phase-7 的 H_cov^low 同类（level-aspect 二元相关/零点统计 power saving）。**

### 4.4 数值探针（heat-kernel-critic task-42B；[数值]）
- E^{(X)}（把 1/L 换成 P_X）**收敛到 E_q**（尾指数 θ≈η…1.4η，符合 naive X^{−η}），而不是直接到 M_q；|E_X−M_q| 降到 |E_q−M_q|（H_Ratios 残差本身）后振荡回升 ⇒ **Route C 无法绕过 H_Ratios 残差**。
- **公式陷阱**：任务式的 `conj(P_t(χ))` 在 Im t≠0 时收敛到 L(t̄,χ̄) 的比值而非目标 L(t,χ̄)；须对 χ̄ 直接展开 P_t 再乘 P_s(χ)·P_t(χ̄)（修正后恢复收敛：斜率 −0.38/−0.35）。结论：即使修正，终点仍是 E_q/M_q 的 H_Ratios 残差，不是绕过通道。

### 4.5 Lead 的正面结果：移位区域弱 Ratios 定理（`phase11/theory/shifted-region-lead.md`；[推导]）
**定理（草图）**：q 素，Re a=Re b=Re s=Re t=1/2+η（0<η≤1/4），|Im|≤T。则在 GRH 下，对任意固定 0<ω<η/2，
```
R_q(a,b;s,t) = φ*(q) Z_q(a,b;s,t) + O(q^{1−ω+ε}(1+T)^C),
```
其中 H_q 反射项被自动吸收（相对大小 q^{−2η}）。**推导骨架**：(1) 四个因子都用截断 Dirichlet 级数（分子 Re>1/2 绝对/条件收敛；分母用 Lemma 1.1），误差 `q^{1+ε}X^{−η}(1+T)^C`；(2) 对全部 primitive χ 用精确正交性；X²<q 时 A≡B ⇔ A=B，得**精确** `E^{(X)} = φ*(q)Σ_{A≤X²}c_Ad_A + [Σ_A c_Ad_A−(Σc)(Σd)]`；(3) **Euler 积恒等式**：`Σ_{A≥1}c_Ad_A = ∏_p (1−p^{−a−t}−p^{−b−s}+p^{−s−t})/(1−p^{−a−b}) = Z_q`（与 CFZ 的 Z_q 在 p∤q 逐 Euler 因子完全相同；p|q 差 O(p^{−1−2η})，乘 φ* 后 ≤q^{−2η}）；(4) 取 X=q^{ω/η}<q^{1/2}（no-wrap），误差账本得 ω<η/2。**[数值] 验证**（`shifted_check.py`，q=1009/211，mpmath 全 primitive 求和）：主项恒等式 |φ*S−φ*Z| = 2.4e−4/2.5e−3/1.7e−4；R_q 与 CFZ M_q 吻合到 0.9–2.0%（~q^{−1/2} 级）；σ=0.6 时 H 项相对大小 ~q^{-2η} 显著（0.46）与"内部吸收"分析一致。
**η-权衡 ⇒ 不能完成 GWX**：GWX 的 (3.12) 移到 σ=1/2+η 放大 N^{2η}，要求有效 saving ω>2η；本方法最大 ω<η/2 ⇒ 对每个 η 差 ≥4 倍指数（与 Prop 3.1 的 ω/η<1/2 vs >16 一致）。**意义**：这是"离终点距离"的精确度量 —— 用 GRH 级工具可以把 Ratios 推到临界线外任意近，但 saving 随距离线性退化到 0；要拿到与距离无关的 saving，必须新输入（Type II/零点相关/Ratios 本身）。

---

## 5. Lean（lean-feasibility task-43；`phase11/lean/`）

- **[证明·机器验证] GWX (3.1) 完全验证**：`parity_projection`（对单位为假设）与 `parity_projection_coprime`（IsCoprime ⇔ gcd(mn,N)=1）：`(1/φ(N))Σ_χ χ(−1)χ(m)χ(n)⁻¹ = 1_{N|m+n}`。`lake env lean` **EXIT CODE 0**，无 sorry，7 条审计定理公理均为 `[propext, Classical.choice, Quot.sound]`；Mathlib v4.36.0。证明链：χ(−1)χ(m)=χ(−m) → χ(n)⁻¹=χ(n⁻¹)（n 单位）→ 每条化为 χ(a)（a=(−1)mn⁻¹）→ Mathlib 特征正交性 `DirichletCharacter.sum_characters_eq` → 手证 a=1 ⇔ N|(m+n)（ZMod.intCast_zmod_eq_zero_iff_dvd）→ 除以 φ(N)。
- **[证明] 附带**：χ(−1)χ(m)=χ(−m)（对所有 m，无需单位假设）、χ(−1)²=1、‖χ(−1)‖=1。
- **[事实] Mathlib 缺口**：`Nat.card {χ // IsPrimitive}` 公式、按 conductor 的分解双射 `DirichletCharacter R N ≃ Σ_{q|N}{primitive mod q}`、`Σ_{q|N}φ*(q)=φ(N)` 未完成（1–3 人日可补；注意 `Nat.sum_totient` 是 Σφ(d)=N，不同于 Σφ*(q)=φ(N)）。

---

## 6. 项目最终状态（phase-11 结束时）

**归约链（唯一已知最佳）**：
```
Alpöge/Claude GRH（Dirichlet L；已声明、大量检查通过；官方 comparator/paranoid kernel replay 仍未完成、无 peer review）
   +  H_Ratios（GFZ/WX25 型 2/2 Ratios 的复合导子 + 精确 parity 主项 + 任意固定 ω_D>0 的 q^{1−ω_D+ε} power saving）
   ⇒  Goldbach（GWX Theorem 1.1，归约经独立审计正确；本 phase 未发现 GWX 错误）
```
- **H_Ratios 状态**：未证明；数值上误差项 ~q^{1/2+o(1)} 在素数/squarefree/ramified 全部导体类成立（α≈0.53–0.56），主项（含 composite 精确 M_q）经修正 A_q 后在 q≤2000 复算通过；是标准型猜想（CFZ recipe 的复合外推 + WX25 素数情形），但 over ℚ 无任何族的完整 Ratios 证明。
- **为什么难（精确墙）**：临界线（η→0）情形 ↔ H_wrap / wrap-around AP 双线性型（additive-divisor 移位相关 + μ 权），与 Chowla/零点对相关/parity barrier 同级；GRH 级输入不能解决。
- **能证的极限**：移位区域 Re=1/2+η 的弱 Ratios（saving ω<η/2，η-tradeoff 与 GWX 需求差 ≥4 倍指数）；这说明"精确缺口"是 η→0 的临界线极限，不是任意正 η。
- **若 H_Ratios 被证明**（任何固定 ω_D>0）：GWX ⇒ 所有充分大偶数 Goldbach（ω_D=1/2 给 O(N^{1/2+ε})）；GRH 部分若官方验证完成则条件性进一步减弱。
- **其余成果**：LL/R 路线被排除（R 渐近为假，ratio→常数≈1.2）；GWX 归约/GWX 主项全面核实；A_q mask 修正使 composite 数值结论恢复；GWX (3.1) Lean 机器验证；最小假设 H_Ratios^min；官方状态/文献/MDs 报告更新。

---

## 7. 文件索引（phase-11）
- 报告：本文件；`phase11/lit/ratios-2026-survey.md`（WX25/GWX/Lee/条件路线）、`phase11/lit/mds-22-survey.md`（MDs/函数域）、`phase11/status/verification.md`（官方验证/上游/批评）。
- 理论：`phase11/theory/minimal-hypothesis.md`（H_Ratios^min）、`phase11/theory/route-c.md`（Route C 构造尝试 + Prop 3.1 + H_wrap）、`phase11/theory/route-c-audit.md`（独立审计）、`phase11/theory/lead-route-c.md`（Lead 结构分析 + C1 数值）、`phase11/theory/shifted-region-lead.md`（移位区域弱 Ratios 定理 + 数值验证）、`phase11/audit/gwx-ramified-audit.md`（composite 主项审计：正确，异常为 bug）。
- 数值：`phase11/numerics/error-term.md`（误差指数，含 erratum banner）、`phase11/numerics/ramified-crosscheck.md`（A_q 修正 + 全类 α + phase-10 复算）、`phase11/audit/error-replication.md`（独立复制 + Route C 探针）、代码与 cache（`numerics/*.py`、`numerics/cache/`、`audit/scripts/`）。
- Lean：`phase11/lean/parity.lean` + `report.md`（GWX (3.1) 机器验证）。
- 关键外部文献：GWX arXiv:2611.18825（v1）；WX25 arXiv:2405.04094v2；CFZ arXiv:0711.0718；Čech arXiv:2110.04409；Gao–Zhao arXiv:2404.05081 等；Lee arXiv:2610.32672v2；Baluyot–Čech arXiv:2501.12529；Bui–Florea–Keating Trans. AMS 376 (2023)；Sawin Acta 233 (2024)；Alpöge MIT 验证页 https://math.mit.edu/~drew/grh/（2026-11-21 12:55 UTC 版）。
