# Phase-11b（task-47 收尾）：ramified 导子的 GWX (3.2) 复核 —— 无 ramified 修正，警报是 A_q mask bug

> kernel-theorist，2026-11-22。标注 **[推导]/[数值]/[事实]**。结论：**GWX (3.2) 在复合/ramified q 上正确；无需额外 ramified 主项；phase-11 的 "ramified anomaly" 是 phase-10 的 A_q mask 数值 bug（`PRIMES % q != 0` 应为 `q % p != 0` / "p∤q"）。**

## (i) 独立数值确认（正确 mask：A_q 只乘 p∤q；ζ_q=ζ∏_{p|q}(1−p^{−s})，每个不同素数一次）
q=2^e，分子 Re a=Re b=1/2、分母 Re s=Re t=0.6，8 个随机 shift（|Im|≤1），精确字符求和 R_q（DFT with e^{+2πijk/N}：`np.fft.ifft(V)*N`）对 GWX 两项主项 M_q=φ*Z_q+H_qZ_q(1−b,1−a)：

| q | RMS\|R−M\| | RMS/√q | 错误 mask 时 RMS/√q |
|---|---|---|---|
| 2^8=256 | 32.74 | **2.05** | 1.85 |
| 2^10=1024 | 67.81 | **2.12** | 1.25 |
| 2^12=4096 | 169.93 | **2.65** | 5.15 |

正确 mask 下 RMS/√q≈2.0–2.7（与 Lead/spectral-numerics 修正后 α=0.537±0.032、RMS/√q≈2.1–5.0 一致；与素数 q 同量级）——**平方根误差，无 φ(q/p) 量级项**。脚本 `ramified_quick.py`。
（注：我的"错误 mask"复现只含一个偏置变体，值有涨落，不作为定量证据；决定性证据是团队 fresh char-by-char pipeline 的修正后拟合。）

## (ii) 为何 (3.2) 对复合 q 正确（radical-only Z_q + Möbius 反演）[推导]
1. 精确 primitive 正交性：`Σ*_{χ mod q}χ(A)\barχ(B)=1_{(AB,q)=1}Σ_{d|q}μ(q/d)φ(d)1_{A≡B mod d}`（由 `Σ_{χ mod d}χ(A)\barχ(B)=φ(d)1_{A≡B(d)}1_{(AB,d)=1}` 对导子做 Möbius 反演）。
2. 代入 R_q 得精确分解 `R_q=Σ_{d|q}μ(q/d)φ(d)D_d`，`D_d=Σ_{A≡B(d)}c_Ad_B·1_{(AB,q)=1}`（Route-C 的系数表示）。
3. 关键局部结构：对 p|q，primitive χ 在 p 处 **ramified**（χ(p)=0），因此 p|q 的局部因子**不取 generic CFZ 因子**，而由 `ζ_q=ζ∏_{p|q}(1−p^{−s})`（**每个不同素数一次**，radical 型）给出；`A_q` 在 p|q 处因子为 **1**（乘积只跑 p∤q）。于是 Z_q 在 p|q 的局部因子是 ζ_q 比值 `[(1−p^{−a−b})(1−p^{−c−d})/((1−p^{−a−d})(1−p^{−b−c}))]`，**无 A_p**。
4. 由于 `Σ_{d|q}μ(q/d)φ(d)=φ*(q)`，divisor 和精确塌缩为单一 φ*(q) 系数；反射分子/FE 配置给 H_qZ_q(1−b,1−a)。=> 形式与 (3.2) 完全一致，**不存在残留 φ(q/p) 主项**。
5. 错误 mask (`PRIMES % q != 0`) 对复合 q 会把 p|q（以及其它素数）也乘进 A_q，等于在 p|q 处插入 generic A_p^{gen}——产生一个**主项尺度**的虚假偏差（∏_{p|q}A_p^{gen}，临界线 shift 下相对偏差几个百分点），这正是"~c·φ(q/p) 残差"的来源；对素数 q 该 mask 恰巧正确（只漏掉 p=q，而 p=q 本就不该出现），所以素数/squarefree 看起来正常。liu-auditor 的精确复合正交性/radical 论证与此一致 [事实]。

## (iii) 结论与 caveat
- **无需 ramified 修正**；(3.2) 与精确 primitive 字符和在复合/ramified q 上一致到平方根级；两项 φ*/H 结构在复合 q 稳定（H_q 用精确 M_e(q) 奇偶计数，q=2^e 时 M_0=M_1=2^{e−3}）。
- **Caveat**：以上是数值+启发式论证，非证明；q≤4096、8 shifts、|Im|≤1；定理仍为猜想（RC_D 的证明难度不变）。建议 spectral-numerics 的 error-term.md 中 "ramified anomaly / H_Ratios 对所有复合 q 为假" 的段落标注 **retracted (A_q mask bug)**。phase-11 的正面结果（Lead 的移位区域弱 Ratios、kernel-theorist 的 Prop 3.1/H_wrap/Lemma 1.1–1.4、M_q 数值验证）不受影响。
