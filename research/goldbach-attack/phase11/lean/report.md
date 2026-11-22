# Phase-11 Lean 报告：GWX 奇偶投影恒等式 (3.1) 的机器验证

- **执行**：teammate `lean-feasibility`（task-43），2026-11-21 23:09–00:10 CST
- **环境**：Lean v4.36.0（commit `611c117…`）+ Mathlib **v4.36.0**（tag commit `fc4f59e577feb1a4956671bc04ac18aaaf8cd842`），位于 `/home/kiler/rh-work/lean-test/mathlib36/mathlib4-4.36.0`
- **结论一句话**：**GWX (3.1) 已在 Mathlib 中完整机器验证**（单位假设形式，等价于 `gcd(mn,N)=1`）：`lake env lean` **EXIT CODE: 0**、无 sorry、7 条审计定理公理全部 `[propext, Classical.choice, Quot.sound]`。(B) 的 `Σ_{q|N} φ*(q) = φ(N)` **未能** 机器验证：Mathlib v4.36.0 有 conductor/primitive/changeLevel 基础设施，但**缺少** primitive 字符计数与按 conductor 的分解定理（详见 §4）。

## 0. TL;DR

| 目标 | 结果 |
|---|---|
| (A) GWX (3.1) | ✅ **完全机器验证**（`parity_projection` / `parity_projection_coprime`，见 §2） |
| (C) `χ(−1)χ(m)=χ(−m)`、`‖χ(−1)‖=1` 等 | ✅ 已验证（所有 `m : ZMod N`，无需单位假设） |
| (B) `Σ_{q\|N} φ*(q)=φ(N)` | ❌ 未验证（Mathlib 缺 primitive 字符计数；只验证了 `Nat.card (DirichletCharacter ℂ N) = φ(N)` 这一 Mathlib 已有事实的包装） |
| 验收 | ✅ `EXIT CODE: 0`，无 sorry，公理仅 `[propext, Classical.choice, Quot.sound]` |
| 交付文件 | `phase11/lean/parity.lean`（209 行，9,120 B，sha256 `5ec649bd7872a959a6cd1332a9738d600a2ab77825b6a05cc062adaf2aed4db7`）；`phase11/lean/parity.output.txt`（验证 transcript）；本报告 |

---

## 1. 待证命题（任务原文）与形式化陈述

任务：(A) 对 `N ≥ 1`，`m n ∈ ℤ`，`gcd(mn,N)=1`：

```
(1/φ(N)) · Σ_{χ : DirichletCharacter (ZMod N) ℂ} χ(−1)·χ(m)·(χ(n))^{-1}
   =  1     若 N ∣ (m+n)
   =  0     否则
```

**Lean 中的精确陈述**（`parity.lean`，namespace `GWXParity`，逐字来自验证输出）：

```lean
theorem parity_projection {N : ℕ} [NeZero N] (m n : ℤ)
    (_hm : IsUnit ((m : ZMod N))) (hn : IsUnit ((n : ZMod N))) :
    1 / ↑N.totient * ∑ χ, χ (-1) * χ ↑m * (χ ↑n)⁻¹
      = if ↑N ∣ m + n then 1 else 0

theorem parity_projection_coprime {N : ℕ} [NeZero N] (m n : ℤ)
    (hm : IsCoprime (↑N) m) (hn : IsCoprime (↑N) n) :
    1 / ↑N.totient * ∑ χ, χ (-1) * χ ↑m * (χ ↑n)⁻¹
      = if ↑N ∣ m + n then 1 else 0
```

- 系数域：`ℂ`；`χ : DirichletCharacter ℂ N` 即 `MulChar (ZMod N) ℂ`（Mathlib 定义 `abbrev DirichletCharacter R n := MulChar (ZMod n) R`）。
- `IsUnit ((m : ZMod N))` 等价于 `gcd(m,N)=1`（`ZMod.isUnit_intCast_iff_isCoprime`）；`parity_projection_coprime` 直接用 `IsCoprime (N : ℤ) m` 与 `IsCoprime (N : ℤ) n` 表述，正好对应 `gcd(mn,N)=1`。
- 任务写的 `χ̄(n)`（复共轭）与 Lean 里的 `(χ n)⁻¹` 在单位 `n` 处等价：`‖χ(n)‖=1`（见 (C) 系列与 `Complex.inv_eq_conj`）；本文件采用**逆形式**（更直接，且对 ℂ 的 `Field` 结构无需额外单位模长引理）。
- 额外说明（诚实）：证明实际只用到 `hn`（`n` 为单位）；`m` 为单位假设在证明中未被使用（恒等式对任意 `m`、单位 `n` 都成立）。为忠实于 GWX 的 `gcd(mn,N)=1` 陈述，保留两个单位假设（`_hm` 以下划线开头命名以避免未使用变量警告）。

## 2. 证明结构（对应 GWX (3.1) 的奇偶投影论证）

1. **消去 χ(−1)**：`χ(−1)·χ(m) = χ((−1)·m) = χ(−m)`（由 `MulChar` 的乘法性，对**所有** `m : ZMod N` 成立，无需单位假设）——见 `chi_neg_one_mul_apply`。
2. **反演单位**：`n` 为单位 ⇒ `χ(n⁻¹) = (χ(n))⁻¹`（`χ(n⁻¹)·χ(n) = χ(1) = 1`）——证明中 `hn_inv_eq`。
3. **合并**：每项 `χ(−1)χ(m)χ(n)⁻¹ = χ(a)`，其中 `a := ((−1)·m)·n⁻¹ ∈ ZMod N`。
4. **特征正交性**：使用 Mathlib 定理（`Mathlib/NumberTheory/DirichletCharacter/Orthogonality.lean`）
   `DirichletCharacter.sum_characters_eq (R := ℂ) a : ∑ χ, χ a = if a = 1 then ↑N.totient else 0`。
5. **零点条件化**：`a = 1 ↔ (N : ℤ) ∣ (m+n)`。这是 `parity.lean` 里手写的引理 `ha_iff`：
   - ←：由 `N ∣ m+n` 得 `↑(m+n) = 0 ∈ ZMod N`（`ZMod.intCast_zmod_eq_zero_iff_dvd`），故 `m = −n`，代入 `a = ((−1)·(−n))·n⁻¹ = n·n⁻¹ = 1`（用 `ZMod.mul_inv_of_unit`）；
   - →：两边乘 `n` 得 `(−1)·m = n`，即 `−m = n`，故 `m+n = 0 ∈ ZMod N`，再用 `ZMod.intCast_zmod_eq_zero_iff_dvd`。
6. **除以 φ(N)**：`φ(N) ≠ 0`（`Nat.totient_pos`；`N ≥ 1` 因 `[NeZero N]`），`(1/φ)·φ = 1`（`field_simp`），零情形 `(1/φ)·0 = 0`。

## 3. 已机器验证的定理清单（`#check` 原文 + 公理）

```
GWXParity.chi_neg_one_mul_apply {N : ℕ} (χ : DirichletCharacter ℂ N) (m : ZMod N) :
    χ (-1) * χ m = χ (-m)
GWXParity.chi_neg_one_sq {N : ℕ} (χ : DirichletCharacter ℂ N) : χ (-1) ^ 2 = 1
GWXParity.norm_chi_neg_one {N : ℕ} (χ : DirichletCharacter ℂ N) : ‖χ (-1)‖ = 1
GWXParity.sum_characters_eq_complex {N : ℕ} [NeZero N] (a : ZMod N) :
    ∑ χ, χ a = if a = 1 then ↑N.totient else 0
GWXParity.parity_projection {N : ℕ} [NeZero N] (m n : ℤ)
    (_hm : IsUnit ↑m) (hn : IsUnit ↑n) :
    1 / ↑N.totient * ∑ χ, χ (-1) * χ ↑m * (χ ↑n)⁻¹ = if ↑N ∣ m + n then 1 else 0
GWXParity.parity_projection_coprime {N : ℕ} [NeZero N] (m n : ℤ)
    (hm : IsCoprime (↑N) m) (hn : IsCoprime (↑N) n) :
    1 / ↑N.totient * ∑ χ, χ (-1) * χ ↑m * (χ ↑n)⁻¹ = if ↑N ∣ m + n then 1 else 0
GWXParity.card_dirichletCharacter {N : ℕ} [NeZero N] :
    Nat.card (DirichletCharacter ℂ N) = N.totient
```

公理审计（`#print axioms`，原文见 `parity.output.txt`）：

| 定理 | 公理 |
|---|---|
| `chi_neg_one_mul_apply` | `[propext, Classical.choice, Quot.sound]` |
| `chi_neg_one_sq` | `[propext, Classical.choice, Quot.sound]` |
| `norm_chi_neg_one` | `[propext, Classical.choice, Quot.sound]` |
| `sum_characters_eq_complex` | `[propext, Classical.choice, Quot.sound]` |
| `parity_projection` | `[propext, Classical.choice, Quot.sound]` |
| `parity_projection_coprime` | `[propext, Classical.choice, Quot.sound]` |
| `card_dirichletCharacter` | `[propext, Classical.choice, Quot.sound]` |

无 `sorry`/`admit`/`axiom`；`lake env lean` 退出码 0（`real 2.9s`）。审计命令与输出全文见 `phase11/lean/parity.output.txt`。

## 4. (B) 的结果与 Mathlib 缺口（精确清单）

**已验证的相邻事实**：`card_dirichletCharacter : Nat.card (DirichletCharacter ℂ N) = N.totient`——Mathlib 已有 `DirichletCharacter.card_eq_totient_of_hasEnoughRootsOfUnity`（本文件加了 ℂ 的 `HasEnoughRootsOfUnity` 实例并包装）。即“**全部** Dirichlet 字符的个数 = φ(N)”。

**未验证的目标**：`Σ_{q|N} φ*(q) = φ(N)`，其中 `φ*(q)` = 模 `q` 的 **primitive** Dirichlet 字符个数。

**Mathlib v4.36.0 已有的 primitive/conductor 基础设施**（`Mathlib/NumberTheory/DirichletCharacter/Basic.lean`）【事实】：
- `DirichletCharacter.FactorsThrough`、`conductorSet`、`conductor`（`sInf conductorSet`）、`conductor_dvd_level`、`factorsThrough_conductor`；
- `DirichletCharacter.IsPrimitive`（定义 `conductor χ = n`）、`primitiveCharacter`（`χ` 关联的 primitive 字符）、`primitiveCharacter_isPrimitive`、`changeLevel_primitiveCharacter`；
- `changeLevel`（提升 level）、`changeLevel_injective`、`conductor_changeLevel`、`conductor_inv`、`mem_conductorSet_iff_conductor_dvd`、`primitiveCharacter_changeLevel_apply` 等。

**Mathlib v4.36.0 缺少的（导致 (B) 无法直接形式化）**：
1. **没有 primitive 字符的计数**：不存在 `Nat.card {χ : DirichletCharacter R q // χ.IsPrimitive}` 的计算公式，也没有“模 q 的 primitive 字符 = φ*(q)”的定理；`grep "Nat.card.*IsPrimitive"` 在 `Mathlib/NumberTheory/DirichletCharacter/` 中为空。
2. **没有按 conductor 的字符分解/双射**：没有 `DirichletCharacter R N ≃ Σ_{q ∣ N} {χ : DirichletCharacter R q // χ.IsPrimitive}` 这样的求和分解，也没有“纤维大小 = #primitive(q)”的引理。已有的 `changeLevel`/`primitiveCharacter`/`conductor_changeLevel` 足以做这个双射的原料，但成品定理不存在。
3. **没有求和公式**：`Σ_{q|N} φ*(q) = φ(N)` 或逐 `q` 的 `#primitive(q)` 公式均不存在；`GaussSum.lean` 只在与 primitive 相关的 Gauss 和命题里提到 primitive，没有计数。
4. **容易误用的替代**：Mathlib 有经典恒等式 `Nat.sum_totient (n) : n.divisors.sum φ = n`（`Mathlib/Data/Nat/Totient.lean:163`）——它是 `Σ_{d|N} φ(d) = N`，**不是** `Σ φ*(q) = φ(N)`；两者数值不同（例如 `N=p`：`Σ_{d|p} φ(d) = p`，而 `Σ φ*(q) = 1 + (p−2) = p−1 = φ(p)`）。

**若要补全 (B) 的估计【推测】**：需 (i) 定义 `φ*(q) := Nat.card {χ : DirichletCharacter ℂ q // χ.IsPrimitive}`；(ii) 用 `primitiveCharacter` + `changeLevel` + `changeLevel_injective`/`conductor_changeLevel` 证明双射（每个 `χ mod N` ↔ 唯一的 `(q ∣ N, primitive χ₀ mod q)`）；(iii) 证明纤维基数为 #primitive(q)；(iv) 由 `Nat.card` 相加得 `Σ_{q|N} φ*(q) = Nat.card (DirichletCharacter ℂ N) = φ(N)`。Mathlib 的基础设施已让 (ii)(iii) 可行，但工作量估计 **1–3 人日**（需要 `Nat.card` 的 fiber/求和工具、`Finset` 求和与 `Fintype.card_congr` 的精细管理），本次 75 分钟盒内不做。

## 5. 诚实说明（未做/简化）

1. **χ̄(n) 的共轭形式**：本文件用 `(χ n)⁻¹`。对单位 `n` 有 `‖χ(n)‖=1`，因此逆 = 复共轭（Mathlib `Complex.inv_eq_conj` 在 `Mathlib/Analysis/Complex/Basic.lean:359` 可直接使用）；未在文件中额外走通“`χ̄ = conj`”这一层（不影响 (3.1) 的数学内容）。
2. **参数假设**：(A) 用 `n` 为单位的假设；`gm`（`m` 为单位）在证明中冗余（保留以匹配 GWX 的 `gcd(mn,N)=1`）。若去掉 `m` 的单位假设，恒等式仍成立（本文件未单独形式化该加强版）。
3. **只覆盖 (3.1) 的有限字符和部分**：没有涉及 GWX 后续的 sieve/BFMT/显式公式等；没有无限乘积、没有 LL 的算子/零点链。
4. **(B) 未完成**：如上，只验证了“全部字符数 = φ(N)”这一 Mathlib 已有事实；primitive 计数与 `Σφ*` 恒等式缺失。另 `Σ_{q|N} φ*(q) = φ(N)` 中 `φ*` 的准确定义（GWX 用 `q` 的 primitive 字符数）按 §4 定义；不同文献的 φ* 记号可能不同，本报告按“模 q 的 primitive 字符数”理解。
5. 没有运行 `lean4checker`/`lean4lean` 的整份 olean 第三方复检：`lake env lean` 本身即 Lean 内核检查，`#print axioms` 已满足任务验收要求（如需第三方内核复检可后续加做）。

## 6. 复现命令

```bash
MATHLIB=/home/kiler/rh-work/lean-test/mathlib36/mathlib4-4.36.0
export PATH=/home/kiler/rh-work/lean-test/lean4/lean-4.36.0-linux/bin:$PATH   # Lean 4.36.0
cd "$MATHLIB"
lake env lean /home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase11/lean/parity.lean
# → 7 条 #check + 7 条 #print axioms，末尾 [EXIT CODE: 0]
# 如需补 olean（本次新增 408 个）：
# lake exe cache get Mathlib.NumberTheory.DirichletCharacter.Orthogonality \
#   Mathlib.Analysis.Complex.Polynomial.Basic Mathlib.RingTheory.RootsOfUnity.AlgebraicallyClosed \
#   Mathlib.GroupTheory.Exponent
```

## 7. 交付文件

| 文件 | 大小/行数 | sha256 | 说明 |
|---|---|---|---|
| `phase11/lean/parity.lean` | 209 行 / 9,120 B | `5ec649bd7872a959a6cd1332a9738d600a2ab77825b6a05cc062adaf2aed4db7` | 主交付：GWX (3.1) + (C) 系列 + 审计命令 |
| `phase11/lean/parity.output.txt` | — | — | `lake env lean` transcript（含 `[EXIT CODE: 0]` 与 7 条公理输出） |
| `phase11/lean/report.md` | 本文件 | — | 报告 |
