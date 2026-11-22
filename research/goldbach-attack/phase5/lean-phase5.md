# Phase-5 Lean 形式化报告（task-18）

**日期**：2026-11-21 16:05–16:30 CST（= 08:05–08:30 UTC）
**执行**：teammate `lean-feasibility`
**结论一句话**：**Mathlib 已在 30 分钟时间盒内成功装好**（Lean v4.36.0 + Mathlib v4.36.0）；phase-5 逻辑关键的 **6 条引理全部通过 Lean 内核检查**（`lake env lean` EXIT 0，**无 sorry**，`#print axioms` 全部为 `[propext, Classical.choice, Quot.sound]`）。

---

## 0. TL;DR（给 lead）

| 项目 | 结果 |
|---|---|
| Mathlib 是否可用 | ✅ **可用**。Lean v4.36.0（commit `611c117…`）+ Mathlib **v4.36.0**（tag commit `fc4f59e577feb1a4956671bc04ac18aaaf8cd842`） |
| 形式化文件 | `_rh-work/goldbach-attack/phase5/lean/phase5_mathlib.lean`（256 行，sha256 `d7bb12ea…47fe`） |
| 验证命令 | `lake env lean phase5_mathlib.lean` → **EXIT CODE: 0**（4.6 s；完整 transcript 见同目录 `phase5_mathlib.output.txt`） |
| 通过的引理 | 6 条（另有 1 条辅助的矩阵-自伴性引理、1 条 `HypothesisR ⇒ 二次型界`、1 条 `¬HypothesisR` 反证）——见 §2 |
| 无 sorry | ✅ `grep -n "sorry"` 只匹配到注释中的 "No `sorry`" 一行，无实际 `sorry`/`axiom`/`admit` |
| 公理 | 全部 6 条定理 `#print axioms` = `[propext, Classical.choice, Quot.sound]`（与 RH 证明 export 允许的 axiom 集一致） |
| 诚实边界 | 形式化的是 **LL Prop 5.3 的抽象算子性质 + 有限维矩阵 Lemma B + R 的推论**；**未**形式化 LL 的具体边界积分算子 `T̃_N`、`L²(Γ_N)`、Hardy 迹空间 `H_N`（Mathlib 无 Hardy 空间），**未**使用任何具体数值 Rayleigh 商（未提供数据），**未**做 Nyström/求积误差分析。 |

---

## 1. Mathlib 环境搭建（30 分钟时间盒内完成）

### 1.1 起点

- Lean 工具链已在前一任务装好：`/home/kiler/rh-work/lean-test/lean4/lean-4.36.0-linux/bin/{lean,lake,leantar,…}`
  - `lean --version` → `Lean (version 4.36.0, x86_64-unknown-linux-gnu, commit 611c117bfaf7b7ae1cfcf246ce6fba31e8f509e9, Release)`
  - `lake --version` → `Lake version 5.0.0-src+611c117 (Lean version 4.36.0)`
- WSL 内 github.com 仍被 hosts 指向 127.0.0.1（`getent hosts github.com` → `127.0.0.1`），但此前验证过 `https://gh-proxy.com/` 可代理 GitHub（clone/archive/release 均可，实测 clone `--depth 1` OK）。

### 1.2 Mathlib 源码（tag v4.36.0，与 Lean 4.36.0 精确匹配）

```bash
$ cd /home/kiler/rh-work/lean-test && mkdir -p mathlib36 && cd mathlib36
$ time curl -sSL --retry 3 -o mathlib4-v4.36.0.tar.gz \
   "https://gh-proxy.com/https://github.com/leanprover-community/mathlib4/archive/refs/tags/v4.36.0.tar.gz"
http:200 size:24301595 speed:706776B/s total:34.383701s
$ tar -xzf mathlib4-v4.36.0.tar.gz          # → mathlib4-4.36.0/
$ cat mathlib4-4.36.0/lean-toolchain
leanprover/lean4:v4.36.0                     # 与已装工具链精确一致
$ python3 -c "import json;m=json.load(open('mathlib4-4.36.0/lake-manifest.json'));print([(p['name'],p['rev']) for p in m['packages']])"
# 8 个 pinned 依赖（见 §1.3）
```

### 1.3 依赖包（8 个）——绕开 lake 的 git fetch 卡死

**第一次尝试失败**：直接 `lake exe cache get` 时，lake 自己用 `git fetch --tags --force --filter=tree:0` 拉依赖，经 gh-proxy 时在 `plausible` 上卡住约 5 分钟无进展（进程树：`git remote-https origin https://gh-proxy.com/...plausible`）。**改为手工预置依赖**：对每个依赖执行
`git init; git remote add origin https://gh-proxy.com/<url>; git fetch --depth 1 origin <rev>; git checkout FETCH_HEAD`，全部 8 个在 **98 秒**内完成（每个 1–20 s）：

```
== plausible : 054b228ce0ac61d767c6e71ba73a24728f191b72
   OK 054b228ce0ac61d767c6e71ba73a24728f191b72
== LeanSearchClient : 4fb58e749ef3fc0395fe274f6cab70c2ea85f1c9
   OK 4fb58e749ef3fc0395fe274f6cab70c2ea85f1c9
== importGraph : 8370c640afcd1cc3fb1cb9bf1560cc66eafee5e0
   OK 8370c640afcd1cc3fb1cb9bf1560cc66eafee5e0
== proofwidgets : 2f0f3520daeac2d9310ff25b7a877a0e5cdaa203
   OK 2f0f3520daeac2d9310ff25b7a877a0e5cdaa203
== aesop : 66ff77cf0c4c898799e4b94d14db55f7a02d0c5a
   OK 66ff77cf0c4c898799e4b94d14db55f7a02d0c5a
== Qq : ff055a2fcc835935e0ae607339b455a5f5896b4b
   OK ff055a2fcc835935e0ae607339b455a5f5896b4b
== batteries : b4b25a3886a16daacaf6615c2eea7170a6e8f458
   OK b4b25a3886a16daacaf6615c2eea7170a6e8f458
== Cli : 50810f72af7618bee62fe9800dc26e806c188703
   OK 50810f72af7618bee62fe9800dc26e806c188703
real    1m38.048s
```

（`git config --global url."https://gh-proxy.com/https://github.com/".insteadOf "https://github.com/"` 已设；lake 打印的 "remote URL changed" 只是提示 manifest 里记录的 URL 与本地 remote 不同，无影响。）

### 1.4 预编译 Mathlib oleans（无需从源码构建 8.5k 文件）

用 Lake 的官方缓存工具（自 `cache.mathlib.org`，成功）：

```bash
$ lake build cache            # 61 jobs, Build completed successfully
$ time lake exe cache get Mathlib.Tactic \
     Mathlib.Analysis.InnerProductSpace.Projection.Basic Mathlib.Analysis.InnerProductSpace.Adjoint \
     Mathlib.Analysis.CStarAlgebra.Matrix Mathlib.Analysis.Normed.Operator.Basic
Using cache from leanprover-community/mathlib4.
Attempting to download 3272 file(s) from leanprover-community/mathlib4 cache at https://cache.mathlib.org/mathlib4-master
Downloaded: 3272 file(s) [attempted 3272/3272 = 100%]
Still decompressing downloaded files...
Decompressed 3272 file(s)
real    1m1.182s
# 之后补 1 个缺的 olean（Analysis/Matrix/Hermitian）：
$ lake exe cache get Mathlib.Analysis.Matrix.Hermitian …   # 1 file, 15.7s
```

结果：`.lake/build` **2.8 GB**（含 Mathlib + 依赖 oleans；依赖本身 build 目录合计 330 MB），`find .lake/build -name '*.olean' | wc -l` = 2997+。**全程约 8 分钟**（远在 30 分钟 Mathlib 时间盒内）。

环境小坑（记录备查）：

- `⟪x, y⟫_ℝ` 记号属于 **`open scoped InnerProductSpace`**（不是 `RealInnerProductSpace`；Defs.lean 里是 `scoped[InnerProductSpace] notation … "⟫_" 𝕜`）。
- `*ᵥ`（矩阵乘向量）是 **`open scoped Matrix`** 的 scoped 记号；`⬝ᵥ` 是全局记号。
- `Matrix.toEuclideanCLM` 的隐式参数需显式给出：`Matrix.toEuclideanCLM (n := n) (𝕜 := ℝ) C`。
- 直接 `lean file.lean` + `LEAN_PATH` 与 `lake env lean file.lean` 均可；正式验证用后者。

---

## 2. 形式化内容与验证

### 2.1 最终验证命令与输出（`phase5_mathlib.output.txt`，原文）

```
# Phase-5 Lean verification transcript
# $ lean --version
Lean (version 4.36.0, x86_64-unknown-linux-gnu, commit 611c117bfaf7b7ae1cfcf246ce6fba31e8f509e9, Release)
# $ lake --version
Lake version 5.0.0-src+611c117 (Lean version 4.36.0)
# Mathlib: tag v4.36.0, commit fc4f59e577feb1a4956671bc04ac18aaaf8cd842
# lean-toolchain: leanprover/lean4:v4.36.0

$ lake env lean /home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase5/lean/phase5_mathlib.lean

abs_rayleigh_le_opNorm.{u_1} {H : Type u_1} [NormedAddCommGroup H] [InnerProductSpace ℝ H] (T : H →L[ℝ] H) (v : H) :
  |⟪T v, v⟫_ℝ| ≤ ‖T‖ * ‖v‖ ^ 2
selfAdjoint_inner_eq_starProjection.{u_1} {H : Type u_1} [NormedAddCommGroup H] [InnerProductSpace ℝ H]
  [CompleteSpace H] (T : H →L[ℝ] H) (hT : IsSelfAdjoint T) (M : Submodule ℝ H) [M.HasOrthogonalProjection]
  (hTM : ∀ (x : H), T x ∈ M) (v : H) : ⟪T v, v⟫_ℝ = ⟪T (M.starProjection v), M.starProjection v⟫_ℝ
transfer_rayleigh_unit_le.{u_1} {H : Type u_1} [NormedAddCommGroup H] [InnerProductSpace ℝ H] [CompleteSpace H]
  (T : H →L[ℝ] H) (hT : IsSelfAdjoint T) (M : Submodule ℝ H) [M.HasOrthogonalProjection] (hTM : ∀ (x : H), T x ∈ M)
  (v : H) (hv : ‖v‖ = 1) : |⟪T v, v⟫_ℝ| ≤ ‖T‖
hypothesisR_implies_abs_rayleigh_le.{u_1} {H : Type u_1} [NormedAddCommGroup H] [InnerProductSpace ℝ H] (T : H →L[ℝ] H)
  (δ : ℝ) (hR : HypothesisR T δ) (v : H) (hv : ‖v‖ = 1) : |⟪T v, v⟫_ℝ| ≤ δ
rayleigh_gt_refutes_R.{u_1} {H : Type u_1} [NormedAddCommGroup H] [InnerProductSpace ℝ H] (T : H →L[ℝ] H) (δ : ℝ)
  (v : H) (hv : ‖v‖ = 1) (h : δ < ⟪T v, v⟫_ℝ) : ¬HypothesisR T δ
matrix_rayleigh_gt_implies_norm_gt.{u_1} {n : Type u_1} [Fintype n] [DecidableEq n] (C : Matrix n n ℝ) (hC : C.IsSymm)
  (v : EuclideanSpace ℝ n) (hv : ‖v‖ = 1) (δ : ℝ) (h : δ < v.ofLp ⬝ᵥ C *ᵥ v.ofLp) : δ < ‖C‖
'abs_rayleigh_le_opNorm' depends on axioms: [propext, Classical.choice, Quot.sound]
'selfAdjoint_inner_eq_starProjection' depends on axioms: [propext, Classical.choice, Quot.sound]
'transfer_rayleigh_unit_le' depends on axioms: [propext, Classical.choice, Quot.sound]
'hypothesisR_implies_abs_rayleigh_le' depends on axioms: [propext, Classical.choice, Quot.sound]
'rayleigh_gt_refutes_R' depends on axioms: [propext, Classical.choice, Quot.sound]
'matrix_rayleigh_gt_implies_norm_gt' depends on axioms: [propext, Classical.choice, Quot.sound]
[EXIT CODE: 0]
```

### 2.2 引理清单与对应的 phase-5 逻辑

设 `H` 为实 Hilbert 空间（`NormedAddCommGroup` + `InnerProductSpace ℝ` + `CompleteSpace`），`T : H →L[ℝ] H`，`M : Submodule ℝ H` 带 `HasOrthogonalProjection`，`P_M = M.starProjection`。

| # | Lean 引理 | 类型（简化） | 对应逻辑/用途 |
|---|---|---|---|
| A0 | `abs_rayleigh_le_opNorm` | `|⟪T v, v⟫_ℝ| ≤ ‖T‖ * ‖v‖^2` | 任意有界算子的 Rayleigh 商绝对界（Cauchy–Schwarz + 算子范数），**不需要自伴** |
| A1 | `selfAdjoint_inner_eq_starProjection` | self-adjoint `T`，`range(T) ⊆ M` ⇒ `⟪T v, v⟫ = ⟪T (P_M v), P_M v⟫` | **LL Prop 5.3 的抽象核心**：“T̃_N range ⊆ H_N ⇒ 二次型只依赖 P_H v”（即 `T̃_N = T_N ⊕ 0` 的二次型层面内容） |
| A2 | `selfAdjoint_eq_starProjection_comp` | 同上条件 ⇒ `T v = P_M (T (P_M v))` | 算子层面的 `T = P_M ∘ T ∘ P_M` |
| A3 | `transfer_rayleigh_unit_le` | 同上，`‖v‖ = 1` ⇒ `|⟪T v, v⟫| ≤ ‖T‖` | **Lemma A（transfer）**：任意单位 v 的 Rayleigh 商被算子范数控制；配 `≥ 0` 与 `⟪T(Pv),Pv⟫` 得 `≤ ‖T_N‖·‖P_H v‖² ≤ ‖T_N‖` |
| A3′ | `transfer_rayleigh_unit_le_of_le_norm` | 再加 `‖T‖ ≤ ‖T_M‖` ⇒ `|⟪T v,v⟫| ≤ ‖T_M‖` | `T = T_M ⊕ 0` 时 `‖T‖ = ‖T_M‖`，即任务书 Lemma A 的 `‖T_M‖` 版本 |
| C | `hypothesisR_implies_abs_rayleigh_le` | `HypothesisR T δ`（定义为 `‖T‖ ≤ δ`）⇒ 任意单位 v：`|⟪T v,v⟫| ≤ δ` | **Lemma C / R ⇒ 二次型界**：R 成立时所有 Rayleigh 商都被 δ_N 压住（与我们直接 Goldbach 数值远小于 δ 相容的方向） |
| crux | `rayleigh_gt_refutes_R` | `‖v‖ = 1`，`δ < ⟪T v, v⟫` ⇒ `¬ HypothesisR T δ` | **phase-5 逻辑关键点**：有限模型（Nyström 压缩）算出的单位向量 Rayleigh 商 `λ̃ > δ_N` ⇒ `‖T_N‖ > δ_N` ⇒ Hypothesis R 在该 N 处为假 |
| B | `matrix_rayleigh_gt_implies_norm_gt` | `C : Matrix n n ℝ` 对称、`v` 单位、`δ < vᵀ C v` ⇒ `δ < ‖C‖`（`‖·‖` 为 `Matrix.Norms.L2Operator` 的 L2 算子范数） | **Lemma B（有限维矩阵版）**：Hermitian 矩阵的 Rayleigh 商下界 ⇒ 算子范数下界 |
| B′ | `matrix_rayleigh_gt_implies_opNorm_gt`（同文件，辅助） | 同上 ⇒ `δ < ‖Matrix.toEuclideanCLM C‖`（不经矩阵范数作用域） | 矩阵 ↔ `EuclideanSpace` 连续线性算子的桥接 |
| — | `isSymm_toEuclideanCLM_isSelfAdjoint`（辅助） | `C.IsSymm` ⇒ `IsSelfAdjoint (toEuclideanCLM C)` | 说明“实对称 ↔ 自伴算子”，使 Lemma B 的假设与 Lemma A 的自伴假设衔接 |

**证明思路（A1）**：令 `w = v − P_M v ∈ Mᗮ`。由 `T` 自伴且 `range(T) ⊆ M`，
`⟪T w, T w⟫ = ⟪w, T(T w)⟫ = 0`（`T(T w) ∈ M`，`w ⊥ M`），故 `T w = 0`，即 `T(P_M v) = T v`；再用自伴性与实内积对称性把 `⟪T v, v⟫` 化为 `⟪T(P_M v), P_M v⟫`。**A3** 再用 `P_M` 是压缩（`‖P_M v‖ ≤ ‖v‖`）与 A0。**B** 用 `Matrix.inner_toEuclideanCLM` 把二次型写成 `⟪C v, v⟫`，再用 A0 与 `Matrix.l2_opNorm_toEuclideanCLM : ‖toEuclideanCLM C‖ = ‖C‖`。**crux** 用 `δ < ⟪Tv,v⟫ ≤ |⟪Tv,v⟫| ≤ ‖T‖·1`。

### 2.3 公理审计（`#print axioms` 原文见 §2.1）

| 定理 | 依赖公理 |
|---|---|
| `abs_rayleigh_le_opNorm` | `[propext, Classical.choice, Quot.sound]` |
| `selfAdjoint_inner_eq_starProjection` | `[propext, Classical.choice, Quot.sound]` |
| `transfer_rayleigh_unit_le` | `[propext, Classical.choice, Quot.sound]` |
| `hypothesisR_implies_abs_rayleigh_le` | `[propext, Classical.choice, Quot.sound]` |
| `rayleigh_gt_refutes_R` | `[propext, Classical.choice, Quot.sound]` |
| `matrix_rayleigh_gt_implies_norm_gt` | `[propext, Classical.choice, Quot.sound]` |

- 无 `sorry`（`grep -n "sorry\|admit"` 只命中注释里的说明文字），无自定义 `axiom`/`constant`/`native_decide`/`@[extern]`。编译本身即 Lean 内核逐条检查（`lake env lean` 退出码 0）。
- 未额外运行 `lean4checker`/`lean4lean` 对整份 olean 复检：`#print axioms` 已满足任务要求（且等价于“无 sorry 的 kernel 编译”）；如需第三方内核复检，可用 `leanchecker` 对导出的 olean 再查一遍（未做，不算已验）。

### 2.4 诚实说明：哪些**没有**做到

1. **没有形式化 LL 论文的 Prop 5.3 本体**（具体边界积分算子 `T̃_N`、`L²(Γ_N)`、Hardy 迹空间 `H_N`、其上自伴性/值域包含/湮灭 `H_N^⊥` 的具体构造）。Mathlib 无 Hardy 空间、无 Hilbert–Schmidt 理论，这一步属于 task-6 报告中“Li–Liu 全链形式化”缺口的一部分，不是本次 30 分钟能做的。本次形式化的是其**抽象算子性质**：只要某自伴 `T` 满足 `range ⊆ M`（任意带正交投影的闭子空间 `M`），A1/A2/A3 就给出 `⟨T v,v⟩ = ⟨T(P_Mv),P_Mv⟩ ≤ ‖T‖`。这正是 Prop 5.3 中“用于把 T̃_N 的二次型压到 T_N 上”的逻辑内容。
2. **`HypothesisR` 是抽象定义** `‖T‖ ≤ δ`（任务书给出的抽象形式）；没有连接到 LL 的具体 `δ_N = sqrt(S(N)(log N)^3/N)` 与 `S(N)` 的奇异级数解析表达式（那需要 Li–Liu 链的其余部分）。
3. **没有使用任何具体数值**（例如 N=30030 的有限模型 Rayleigh 商）：lead 未提供数值数据，因此矩阵版是“若 λ̃ > δ 则 …”的通用逻辑，而非具体反例。
4. **没有形式化求积/Nyström 压缩误差**（λ̃ 与 ⟨T_N v,v⟩ 之间的数值误差界），这是数值分析内容，与本次“逻辑关键点内核可检”目标正交。
5. **矩阵版的不等式其实不需要对称性**（A0 对任意算子成立；对称性只用于把 `toEuclideanCLM C` 解释为自伴算子、与 Lemma A 的假设对齐）。矩阵定理保留 `hC : C.IsSymm` 并显式用它构造 `IsSelfAdjoint`，以忠实对应任务书 Lemma B 的“实对称”假设。

---

## 3. 复现步骤（完整命令）

```bash
# 0) 环境（已就绪，本报告验证时所用）
LEAN=/home/kiler/rh-work/lean-test/lean4/lean-4.36.0-linux/bin/lean
LAKE=/home/kiler/rh-work/lean-test/lean4/lean-4.36.0-linux/bin/lake
MATHLIB=/home/kiler/rh-work/lean-test/mathlib36/mathlib4-4.36.0
export PATH=/home/kiler/rh-work/lean-test/lean4/lean-4.36.0-linux/bin:$PATH

# 1) 从零重建（若需要）：
#    Mathlib 源码（tag v4.36.0）：
#    curl -sSL -o mathlib4-v4.36.0.tar.gz \
#      "https://gh-proxy.com/https://github.com/leanprover-community/mathlib4/archive/refs/tags/v4.36.0.tar.gz"
#    tar -xzf mathlib4-v4.36.0.tar.gz
#    8 个 dep 用 git clone --depth 1（经 gh-proxy）+ 手工 fetch 到 .lake/packages/*
#    （脚本见本任务执行记录；核心：git init && git remote add origin https://gh-proxy.com/<url>
#      && git fetch --depth 1 origin <rev> && git checkout FETCH_HEAD）
#    cd $MATHLIB && lake build cache && lake exe cache get <需要的模块>
#    （再加：lake exe cache get Mathlib.Analysis.Matrix.Hermitian）

# 2) 验证
cd "$MATHLIB"
lake env lean /home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase5/lean/phase5_mathlib.lean
# → 应打印 6 条 #check 与 6 条 #print axioms，最后 EXIT CODE: 0

# 3) 机器可读速查
grep -n "sorry" /home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase5/lean/phase5_mathlib.lean
sha256sum /home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase5/lean/phase5_mathlib.lean
```

> 环境持久化：`$MATHLIB/.lake/build` 2.8 GB，`.lake/packages` 330 MB，位于 Linux FS（有 ~948 GB 空闲），可直接复用；下游任何需要 Mathlib v4.36.0 的任务可以 `lake env lean` 使用该 checkout。

---

## 4. 交付文件清单

目录：`/home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/phase5/lean/`

| 文件 | 大小/行数 | sha256 | 说明 |
|---|---|---|---|
| `phase5_mathlib.lean` | 256 行 / 12,741 B | `d7bb12ea20b8ffec298a873818878d3128c82403a810e349a407d9b2430447fe` | 主交付：§2 的 6 条主定理 + 4 条辅助引理（含自伴性桥接、压缩恒等式、矩阵范数桥接） + `#check`/`#print axioms` |
| `phase5_mathlib.output.txt` | 2,348 B | — | `lake env lean` 完整 transcript（含 `[EXIT CODE: 0]`） |
| `no_go_int.lean` | 1,546 B | `50d0ce5fdbcca0c7efd74498326a912c270548af40b805f8c33ac7b0583ed017` | 纯 core Lean 备援（前次任务的 no-go 整数版，已验证 exit 0） |
| `no_go_rat.lean` | 3,123 B | `88fe18f2e0593e3c4d8466bcc3a030250b53faab92c028520aededc72c618700` | 纯 core Lean 备援（rank-one 正性方向引理 ℚ 版，已验证 exit 0） |
| `no_go_int.output.txt` / `no_go_rat.output.txt` | 373 B / 351 B | — | 上述 core 文件的运行输出 |

---

## 5. 与 task-6（Lean 可行性）结论的关系

- task-6 曾判定 “Mathlib 缺 Hardy 空间/Hilbert–Schmidt 等，故 Li–Liu 全链不可形式化”——本次补充：**Mathlib + olean cache 在本机 8 分钟内可用**，普通 Hilbert 空间/自伴算子/紧自伴谱定理级别的抽象引理**可以**在 Mathlib 中快速形式化（本次 6 条引理含调试共约 25 分钟）。缺口仍然是 **Li–Liu 特有的高级分析对象**（条带 Hardy 空间、HS 范数、谱乘积、四元数解析、显式公式），这些在本 phase-5 的“逻辑关键点”上并非必需。
- 对 phase-5 结论的意义：**[内核已验证]** “自伴 + range⊆M ⇒ 二次型只依赖投影” 与 “单位 Rayleigh 商 > δ ⇒ 算子范数 > δ ⇒ ¬R” 这条推理链是无 sorry、仅标准公理的 Lean 定理；因此 “有限模型 λ̃ > δ_N 可证伪 R(N)” 这一步在逻辑/形式化层面是干净的，**剩下的不确定性完全落在数值部分**（λ̃ 与 ⟨T_N v,v⟩ 的求积误差）与 LL 具体算子/假设 S/R 的解析部分。
