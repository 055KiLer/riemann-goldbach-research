# Phase-12 Lean 报告：no-wrap 正交性与 wrap 计数恒等式的机器验证（task-54）

- **执行**：teammate `lean-feasibility`，2026-11-22 19:36–20:45 CST
- **环境**：Lean v4.36.0（commit `611c117…`）+ Mathlib **v4.36.0**（tag commit `fc4f59e577feb1a4956671bc04ac18aaaf8cd842`），`/home/kiler/rh-work/lean-test/mathlib36/mathlib4-4.36.0`
- **结论**：两个 Lean 文件均 **EXIT CODE: 0**、**无 sorry**、公理仅 `[propext, Classical.choice, Quot.sound]`；phase-11 交付文件未改动。

## 0. TL;DR

| 类别 | 交付 | 结果 |
|---|---|---|
| no-wrap 正交性 | `phase12/lean/nowrap.lean`（197 行，6 定理） | ✅ EXIT 0 |
| wrap 计数恒等式 | `phase12/lean/wrap.lean`（158 行，3 定理 + 1 定义） | ✅ EXIT 0 |
| 日志 | `phase12/lean/nowrap_wrap.output.txt` | 含两个 `[EXIT CODE: 0]` 与全部 `#print axioms` |
| sorry | — | **0** |
| 公理 | — | 全部 `[propext, Classical.choice, Quot.sound]`（`nat_mod_eq_iff_dvd_sub` 仅 `[propext]`） |

## 1. `nowrap.lean`：no-wrap 正交性（对应 plan §1.2）

已机器验证的定理（`#check` 原文见日志）：

```
Phase12.star_apply_eq_inv (χ : DirichletCharacter ℂ q) (a : ZMod q) :
    star (χ a) = (χ a)⁻¹
Phase12.char_orthogonality_conj (A B : ZMod q) (hB : IsUnit B) :
    ∑ χ, χ A * star (χ B) = if A = B then ↑q.totient else 0
Phase12.nonprincipal_orthogonality_conj (A B : ZMod q) (hA : IsUnit A) (hB : IsUnit B) :
    ∑ χ with χ ≠ 1, χ A * star (χ B) = (if A = B then ↑q.totient else 0) - 1
Phase12.isPrimitive_iff_ne_one_of_prime (hq : q.Prime) (χ : DirichletCharacter ℂ q) :
    χ.IsPrimitive ↔ χ ≠ 1
Phase12.primitive_orthogonality_conj (hq : q.Prime) (A B : ZMod q) (hA : IsUnit A) (hB : IsUnit B) :
    ∑ χ with χ.IsPrimitive, χ A * star (χ B) = (if A = B then ↑q.totient else 0) - 1
Phase12.totient_prime (hq : q.Prime) : q.totient = q - 1
```

**数学意义**：
- 第二正交关系（全 χ）：`Σ_χ χ(A)\bar χ(B) = φ(q)·1_{A=B}`（单位 `A,B`；`\bar χ(B) = star (χ B)`）。
- 减去主特征 `χ = 1`：`Σ_{χ≠1} χ(A)\bar χ(B) = φ(q)·1_{A=B} − 1`。对素数 `q` 即任务中的
  **no-wrap 恒等式** `(q−1)·[A=B] − 1`（用 `Nat.totient_prime` 转换；`A,B<q`、`gcd(AB,q)=1` 时
  `A,B` 自动是可逆元，且 `A≡B (mod q) ⇔ A=B`）。
- **primitive 版本**：任务担心 Mathlib 缺 primitive API —— 实际 **v4.36.0 已有**
  `DirichletCharacter.conductor`、`IsPrimitive`、`primitiveCharacter`、`changeLevel` 等（phase-11 报告也记录过）。
  本文件证明了 **素数 q 时 `χ ≠ 1 ↔ χ.IsPrimitive`**（conductor ∣ q 且 `conductor=1 ↔ χ=1`），
  故 `Σ_{χ primitive} χ(A)\barχ(B) = Σ_{χ≠1} … = (q−1)[A=B] − 1`。
  因此在素数、无 wrap（`X²<q`，`A,B<q`）区域，no-wrap 正交性是**完全机器验证**的。
- 证明链：`star (χ a) = (χ a)⁻¹`（`MulChar.star_apply'` + `MulChar.inv_apply_eq_inv'`）；
  `(χ B)⁻¹ = χ(B⁻¹)`（单位 `B`）；`χ A·χ(B⁻¹)=χ(A·B⁻¹)`；再用 Mathlib 的一阶正交性
  `DirichletCharacter.sum_characters_eq`；`A·B⁻¹=1 ↔ A=B`。

## 2. `wrap.lean`：wrap 计数恒等式（对应 plan §1.3）

```
Phase12.card_pairs_mod_eq (_hq : 0 < q) (S T : Finset ℕ)
    (hS : ∀ a ∈ S, a < q) (hT : ∀ b ∈ T, b < q) :
    #((S.product T).filter (fun p => p.1 % q = p.2 % q)) = #(S ∩ T)
Phase12.residueSum (q M : ℕ) (c : ℕ → ℂ) (r : ℕ) : ℂ    -- C_r = Σ_{A<M, A≡r} c_A
Phase12.wrap_identity (hq : 0 < q) (c d : ℕ → ℂ) :
    ∑ A ∈ range M, ∑ B ∈ (range M).filter (fun B => B % q = A % q ∧ B ≠ A), c A * d B
      = (∑ r ∈ range q, residueSum q M c r * residueSum q M d r)
        - ∑ A ∈ range M, c A * d A
Phase12.nat_mod_eq_iff_dvd_sub (a b : ℕ) :
    a % q = b % q ↔ (q : ℤ) ∣ ((a : ℤ) - (b : ℤ))
```

**数学意义**：
- `card_pairs_mod_eq`：`S,T ⊆ [0,q)` 时同余对 = 对角对 = `S∩T` 的大小（no-wrap 的计数核心）。
- `wrap_identity`：**wrap 记账恒等式**——"同残类总配对 − 对角"：
  `Σ_{A≡B (mod q), A≠B} c_A d_B = Σ_r C_r D_r − Σ_A c_A d_A`。这正是 plan §1.3 把 wrap 和
  `W` 写成 residue 分组和再减去对角项的形式；`C_r,D_r` 就是按残类分组的和。
- `nat_mod_eq_iff_dvd_sub`：residue 形式 `A%q=B%q` ↔ `kq` 差集形式 `q ∣ (A−B)`
  （即 `A−B=kq`）。这是 plan §1.3 中 `W = Σ_{k≠0} Σ_{nm−rl=kq} …` 与 residue 分组公式之间的
  **算术桥**（把 "差是 q 的倍数" 化为 "同余类相同"）。
- 证明：内层 `filter (B%q=A%q ∧ B≠A) = (filter B%q=A%q).erase A`，用
  `Finset.sum_erase_add`；再按 `A ↦ A%q` 用 `Finset.sum_fiberwise_of_maps_to` 重排为 `Σ_r C_r D_r`。

## 3. 与 plan 的对应 & 诚实边界

- **对应**：`nowrap.lean` = plan §1.2 的 no-wrap 正交性（截断 `X²<q`、`c=1/2` 区域所用）；
  `wrap.lean` = plan §1.3 的 wrap 记账（`W` 的 residue 形式 = 总同残类配对 − 对角）。这些是
  常数追逐的**有限、可审计**骨架。
- **它们本身不证明 H_Ratios / c>2**：`c>2` 需要 `W` 的解析估计
  `W ≪ q^{1−ηA+ε}`（wrap 平凡界差 power），那是解析数论内容，不在本 Lean 文件范围；
  本文件证明的是**组合恒等式**（记账/正交性），不产生新的数论估计。
- **task 第 3 项（完整 W 的 2-vs-2 形式）**：本次只做了桥（`nat_mod_eq_iff_dvd_sub`）与一般
  单变量 wrap 恒等式（`c_A d_B`）。完整的 `W = Σ_{k≠0} Σ_{nm−rl=kq} c(n,m)d(r,l)` 需要对
  `(n,m,r,l)` 的有限截断、k 的有界范围做二重 Finset 求和与重排——结构与本文件的 `wrap_identity`
  相同，属于**可直接扩展**的工作（估计 1–2 人日），本次时间盒内未做，不虚报。
- **Mathlib 缺口**：本次无阻塞。实操中遇到的两个小障碍（已绕过）：
  1. v4.36.0 的 big-operator 语法是 `∑ x ∈ s, f x`（`∑ x in s` 不支持；最初 parse 失败的原因）；
  2. Mathlib 没有 `DecidableEq (DirichletCharacter ℂ q)` 实例（filter 特征需要），本文件在 section 内
     用 `attribute [local instance] Classical.decEq Classical.propDecidable` 解决。
  除此之外 `MulChar.star_apply'`、`DirichletCharacter.sum_characters_eq`、`Nat.ModEq`、
  `Finset.sum_fiberwise_of_maps_to`、`Finset.sum_erase_add` 等全部现成可用。
- **公理**：`#print axioms` 全部 `[propext, Classical.choice, Quot.sound]`（`nat_mod_eq_iff_dvd_sub`
  仅 `[propext]`），无 `sorryAx`。

## 4. 复现命令

```bash
MATHLIB=/home/kiler/rh-work/lean-test/mathlib36/mathlib4-4.36.0
export PATH=/home/kiler/rh-work/lean-test/lean4/lean-4.36.0-linux/bin:$PATH
cd "$MATHLIB"
lake env lean /home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase12/lean/nowrap.lean  # EXIT 0
lake env lean /home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase12/lean/wrap.lean    # EXIT 0
```

## 5. 交付文件

| 文件 | 行数 | sha256 | 说明 |
|---|---|---|---|
| `phase12/lean/nowrap.lean` | 197 | `5f780165fcb40c299c9c64826dc7f1dde26a41533ff6ff08f32a98b930420906` | no-wrap 正交性 6 定理 |
| `phase12/lean/wrap.lean` | 158 | `da13496ecc6256fb3aeaa6dc3f57477603f5d331a89f476c86d69720af89b3b9` | wrap 计数 3 定理 + 定义 |
| `phase12/lean/nowrap_wrap.output.txt` | — | — | 两文件 `lake env lean` 完整日志（两个 EXIT 0） |
| `phase12/lean/report.md` | 本文件 | — | 报告 |
