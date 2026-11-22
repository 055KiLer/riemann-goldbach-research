# Repo forensics 报告：riemann-hypothesis-lean 仓库完整性与"作弊构造"静态审计

任务：task-1（Repo forensics）。执行者：repo-verifier。日期：2026-11-21（Asia/Shanghai）。
对象：`/home/kiler/Windows-D/Rieman/riemann-hypothesis-lean`（D: 盘镜像，git HEAD `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`，2 commits，作者 CocoSgt 镜像）
替代工作副本：Lead 在 Linux 原生盘提供的完整干净 clone `/home/kiler/rh-full`（HEAD 同 commit，`git status --porcelain` = 0）。
作者原始档案：`https://alpo.ge/lean.tar.gz.part01..part14`（本报告中已下载、拼接并与 clone 逐字节比对）。

---

## 0. TL;DR / 结论速览

| 问题 | 结论 |
|---|---|
| 镜像内容是否 = 作者 alpo.ge 原始档案？ | **是，已逐字节验证。** 14 分片拼接 = 239,275,554 bytes，sha256 = `9631b4f020199e580ba86178cb56c6e9b09f690c2369a80dc4334aa93f49c7fc`（与 README/MIT 页一致）；解包树与 `/home/kiler/rh-full/src` **175,187 个文件全部逐字节相同**（`diff -r` 零差异），3 个根配置文件 sha256 也一致。镜像只多出 README.md、.gitignore 两个文件。 |
| 计数是否与 README 一致？ | **完全一致。** 175,192 tracked files / 175,187 个 `.lean` / 17,374,215 行 / 1,030,531,854 bytes。README 的分目录表逐行对上。 |
| 是否有 sorry / admit / axiom / unsafe / native_decide / ofReduceBool 等作弊构造？ | **静态文本扫描全部为 0**（与 README 自报一致）；`addDecl` 仅 1 个文件 2 行（经审读为"复制已有定理并改名"的 kernel 内合法元编程）；22 个 macro/elab 文件与 16 个 `run_tac` 文件逐个抽查，均为普通 tactic 简写或 revert/assign 辅助，未发现伪造证明。 |
| Main.lean 的头条定理真的是 Mathlib 的 `RiemannHypothesis` 吗？ | **是。** Main.lean 的 `riemannHypothesis : RiemannHypothesis` 直接使用 Mathlib 定义（pinned commit `0df444a3…` 的 `Mathlib/NumberTheory/LSeries/RiemannZeta.lean` 第 185 行的定义已独立抓取原文核对）；全树对 `RiemannHypothesis`/`riemannZeta` 的本地重定义数 = 0。另 4 条 Dirichlet L 陈述在 `Statements.lean`（16 行）中定义，语义与名字相符，已逐行核对。 |
| 这份源码单独能否"机械地"证明 RH？ | 源码文本本身不能证明任何东西——必须编译 + kernel 检查。**独立第三方 Andrew Sutherland（MIT）页面的检查结果显示**：175,187 模块全部编译；5 条主定理 `#print axioms` 只依赖 `propext / Classical.choice / Quot.sound`；leanchecker 重放 175,187/175,187 通过；nanoda、con-leche 两个独立 kernel 接受导出证明；con-leche `--compare` 确认 5 条定理"由解推出"；lean4lean 175,187/175,187 通过（5 个加大 fuel）。我在本地**没有**复现编译/kernel 重放（无 Lean 工具链，17.4M 行 + Mathlib 不可行），只核对了该页面产物的 SHA256 与文本。 |
| 红旗？ | **未发现"证明作弊"类红旗。** 但有一批**AI 批量生成/元编程痕迹**（非 soundness 问题，但影响"这是一份人类可读证明"的判断）：394 个含 U+2082 `₂` 的非 ASCII 路径、136,003/175,187（77.6%）文件直接 `import Mathlib`、20,937 个文件 ≤10 行（中位数 58 行）、168 个 `…Cpt` 复制名、54 个 `…Admitted` 文件名、命名空间 `…Cusp.Fake`、33 个文件使用 `allowUnsafeReducibility`、大量 `proofterm` 堆叠。这些全部被逐类检查过，均不构成 soundness 漏洞。 |

**一句话：** 就"这份镜像是不是作者档案的原样副本"和"树里有没有常见的通过 `sorry/axiom/语句替换` 造假的痕迹"两个问题而言，答案分别是"是"和"没有"；就"它是否真的证明了 RH"而言，本地静态审计只能确认**证明链路的语句是真的、连接环节是常规数学论证**，是否成立取决于编译/kernel 检查与 Mathlib 定义——这部分我没有独立复现，但第三方页面报告了完整的 kernel 级通过结果（其页面产物 sha256 我已逐一核对，除一个未下载完的大文件）。

---

## 1. 环境、方法、命令

- WSL Ubuntu（user kiler），16 cores / 15GB RAM；`/home/kiler/Windows-D` 是 Windows D: 的 9p-like 挂载（175k 小文件操作慢）。
- 仓库原生 checkout 因 Windows 长路径问题长期无法完成（D: 盘上 `git status --porcelain` 一度显示 175,198 条 staged deletion、仅 140,731/175,187 个 `.lean` 落盘）。按 Lead 指示**未**在 D: 仓库执行任何写操作；改用 Lead 提供的干净 clone `/home/kiler/rh-full` 做全部读/扫/统计，并在 D: 仓库只做 `git ls-tree`/`git show HEAD:` 只读核对。
- 工具：`rg` 在 WSL 中不存在，通过 `apt-get download ripgrep`（无需 root）+ `dpkg -x` 解到 `/tmp/rg-pkg/usr/bin/rg`（15.1.0）使用；其余 `git`、`python3`、`curl`、`tar`、`sha256sum`。
- github.com 在 WSL 内被解析到 127.0.0.1，故 Mathlib pinned 源码经 Windows PowerShell `Invoke-WebRequest` 从 raw.githubusercontent.com 抓取；alpo.ge 与 math.mit.edu 在 WSL 内直连可用。

关键命令（均已实际执行，输出要点见下文各节；原始输出存 `logs/`）：

| # | 命令（节选） | 输出/结论 |
|---|---|---|
| 1 | `git -C /home/kiler/rh-full log --oneline -3; git status --porcelain \| wc -l` | `7cbf7a0c3`、`0fb9869c6`；dirty=0 |
| 2 | `git ls-tree -r HEAD \| wc -l` | **175,192** tracked files |
| 3 | `find src -name '*.lean' \| wc -l` | **175,187** |
| 4 | `find src -name '*.lean' -print0 \| xargs -0 cat \| wc -l` | **17,374,215** 行 |
| 5 | `find src -name '*.lean' -print0 \| xargs -0 wc -l \| (sum)` | 同上 17,374,215（两种方法一致） |
| 6 | `du -sb src` | **1,030,531,854 bytes**（apparent；因 17.5 万小文件，`du -sh` 磁盘占用 ≈1.4G） |
| 7 | `cat parts{01..14} > lean.tar.gz; sha256sum` | 239,275,554 bytes；`9631b4f0…c7fc` = 声称值 |
| 8 | `tar -xzf` 后 `diff -r /tmp/rh-verify/lean/src /home/kiler/rh-full/src` | 退出码 0，**0 行差异**（全部 175,187 文件逐字节相同；路径列表也完全一致） |
| 9 | `rg -n '…' src`（29 个模式，见 §4） | 见扫描表 |
| 10 | `sha256sum -c SHA256SUMS`（MIT 页 @2026-11-20） | 全部 16 个小/中文件哈希 **OK**（audit.log、comparator.json、Audit.lean、project-oleans.sha256、全部 log）；仅 solution/challenge.ndjson（7.7GB/47MB）未下载 |

目录/行数逐项（`find ... | xargs wc -l` 聚合）：

| Path | `.lean` files（实测） | README 声称 | Lines（实测） | README 声称 |
|---|---:|---:|---:|---:|
| `src/Development/` | 141,928 | 141,928 | 12,232,663 | 12.2 M |
| `src/Formalism/` | 18,254 | 18,254 | 3,200,748 | 3.2 M |
| `src/GroundTheory/` | 8,507 | 8,507 | 1,119,138 | 1.1 M |
| `src/ReciprocityTheory/` | 3,845 | 3,845 | 563,016 | 563 K |
| `src/CompanionTheory/` | 2,027 | 2,027 | 194,218 | 194 K |
| `src/PositivityTheory/` | 449 | 449 | 55,130 | 55 K |
| `src/Lemmata/` | 167 | 167 | 9,232 | 9 K |
| `src/Supplements/` | 3 | 3 | 22 | 22 |
| `src/BuildAid/` | 5 | 5 | 20 | 20 |
| `src/Statements.lean` + `src/Main.lean` | 2 | 2 | 16 + 12 | — |
| **Total** | **175,187** | **175,187** | **17,374,215** | **≈17.4 M** |

> 计数陷阱：用 `git ls-tree -r HEAD --name-only | grep -c '\.lean$'` 只会得到 **174,793**，因为 git 默认对含非 ASCII 的路径加双引号（394 个含 `₂` U+2082 的路径），这些行以 `"` 而不是 `.lean` 结尾。用 `-z` 或 `-c core.quotePath=false` 才是 175,187。README 的 175,187 是正确的。

源码文件大小统计：min 1 行 / p25=17 / **median 58** / mean 99.18 / p75=132 / max 17,981（`Formalism/HermitianCurvature/HermitianCurvatureProofs/IsAdmissibleSplittingCharPairMulTwist.lean`）。≤10 行 20,937 个（12.0%）；≤20 行 49,487（28.2%）；≤50 行 80,928（46.2%）；≤100 行 116,195（66.3%）。

---

## 2. 来源（provenance）验证：镜像 = 作者档案

**步骤与结果（全部实测）：**

1. `curl` 下载 `https://alpo.ge/lean.tar.gz.part01..part14`（并发 14 路，Cloudflare，HTTP 200）。分片大小：13×18,000,000 + 5,275,554 = **239,275,554 bytes**，与 README/MIT 页声称一致。
2. `cat parts{01..14} > lean.tar.gz` → `sha256sum` = **`9631b4f020199e580ba86178cb56c6e9b09f690c2369a80dc4334aa93f49c7fc`**，逐字符等于 README 与 MIT 页面的声称值。
3. `tar -tzf` 条目数 = **175,190** = `lean/` 下 3 个根文件（lake-manifest.json、lakefile.toml、lean-toolchain）+ 175,187 个 `lean/src/**.lean`；**没有** README.md / .gitignore。
4. 解包到 `/tmp/rh-verify/lean`（原生文件系统）后：
   - `find src -name '*.lean'` = 175,187；
   - 路径集合与 `/home/kiler/rh-full/src` **完全相同**（`diff` 路径列表 0 差异，各 175,187 行）；
   - `diff -r /tmp/rh-verify/lean/src /home/kiler/rh-full/src` → **退出码 0，无任何差异**（即 archive 中每个文件与 clone 中同路径文件逐字节相同）。
5. 根配置文件（archive ↔ git HEAD）sha256 三方核对：

| 文件 | archive sha256 | git HEAD 工作区 sha256 | 结果 |
|---|---|---|---|
| lake-manifest.json | `fee57ee9…bbe4774` | 同 | MATCH |
| lakefile.toml | `b831ad8c…ddec4c` | 同 | MATCH |
| lean-toolchain | `3aac669c…f5db71` | 同 | MATCH |

6. `/home/kiler/rh-full` 的 HEAD commit id 与 D: 镜像仓库相同（`7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`），且 `git status --porcelain = 0` → 工作区内容 = git HEAD tree = archive 内容。镜像新增文件只有 `README.md`（sha256 `2c613919…cf89`）与 `.gitignore`（`637cfc01…bc86a3`），与 README 自述"只加了 README 和 .gitignore"一致。

**结论：** 从 alpo.ge 抓到的 14 个分片 → 拼接 sha256 → 解包树 → 与本地 clone 全量逐字节 diff，四步全部吻合。**该 clone 的 `src/` 就是 2026-11-21 时点 alpo.ge 发布的原始 Lean 源码，未发现任何篡改/夹带。**（无法核验的是：alpo.ge 域名与实际作者身份的绑定、以及档案发布时间戳——这超出仓库取证范围。）

---

## 3. 顶层定理链与"语句真伪"核验

### 3.1 五个头条定理（`src/Main.lean`，12 行，全文）

```lean
import Statements
import Supplements.Kernels.MainTheoremsAll

theorem riemannHypothesis : RiemannHypothesis := rhOfAll
theorem riemannZeta_eq_zero_re : RiemannZetaZerosOnLine := rhOfAll
theorem LFunction_ne_zero_of_half_lt_re : DirichletLNonvanishingRightOfHalf := allChi
theorem LFunction_eq_zero_re : DirichletLZerosOnLine := claimAll.2.1
theorem LFunction_eq_zero_re_of_isPrimitive : PrimitiveDirichletLZerosOnLine := critAll
```

- **`RiemannHypothesis` 是 Mathlib 的定义**（不是本仓库定义）。我通过 Windows 网络抓取了 pinned commit `0df444a360eaa60ab8c11dca51a86af692955474` 的 `Mathlib/NumberTheory/LSeries/RiemannZeta.lean`（12,306 bytes，https://raw.githubusercontent.com/leanprover-community/mathlib4/0df444a3…/Mathlib/NumberTheory/LSeries/RiemannZeta.lean），第 185-186 行原文：

  ```lean
  def RiemannHypothesis : Prop :=
    ∀ (s : ℂ) (_ : riemannZeta s = 0) (_ : ¬∃ n : ℕ, s = -2 * (n + 1)) (_ : s ≠ 1), s.re = 1 / 2
  ```

  全树搜索 `^\s*(def|abbrev|theorem|opaque|axiom)\s+RiemannHypothesis\b` / `riemannZeta\b` → **0 处本地重定义**（`logs/scan_*`），因此 Main.lean 中的名字只能解析到 Mathlib。MIT audit.log 亦记录 `RiemannHypothesis : declared in module Mathlib.NumberTheory.LSeries.RiemannZeta`、`riemannZeta : declared in module Mathlib.NumberTheory.LSeries.RiemannZeta`。
- **另外 4 条语句**定义在 `src/Statements.lean`（16 行，仅 `import Mathlib`），我逐行核对了数学含义：
  - `RiemannZetaZerosOnLine`：ζ 的非平凡零点实部 = 1/2（排除 `s=-2(n+1)` 与 `s=1`）——与 Mathlib `RiemannHypothesis` 定义同构（MIT 的 `Audit.lean` 中有编译过的 `example : RiemannZetaZerosOnLine = RiemannHypothesis := rfl`）。
  - `DirichletLNonvanishingRightOfHalf`：∀ N [NeZero N] χ s，`1/2 < Re s → (χ≠1 ∨ s≠1) → LFunction χ s ≠ 0`（= GRH 的右半平面形式）。
  - `DirichletLZerosOnLine` / `PrimitiveDirichletLZerosOnLine`：临界带内 Dirichlet L 零点在 `Re s = 1/2`（后者限 primitive χ）。
  - 这些恰好是"GRH for Dirichlet L-functions"的标准表述。注意：MIT 页面明确说明 **"GRH" here means Dirichlet L-functions only**，不是一般化的 GRH；报告/转述时不要扩大。

### 3.2 证明项链（从 Main.lean 向下 3 层，逐文件读过全文）

```
Main.lean
├─ Statements.lean                          (16 行，只有定义)
└─ Supplements/Kernels/MainTheoremsAll.lean (3 行)
   └─ Supplements/Kernels/MainTheoremsCritical.lean (4 行: import MainTheorems + 3 个 SmallClassNumbers 模块)
      └─ Supplements/Kernels/MainTheorems.lean       (16 行, 核心装箱)
         ├─ Formalism/GammaFactorNonvanishing/CritLine.lean (32 行)
         │    Formalism.VW.gammaFactor_ne_zero / critLine / rh_of_every
         ├─ Development/AutomorphicArithmetic/CharacterBoxes/ClaimStrip.lean (104 行)
         │    Claim.factor_ne_zero / prim_zero / gamma_ne_zero / prim_reflect / strip / zeta / zeta_iff
         └─ Development/AutomorphicArithmetic/CharacterBoxes/MainConclusion.lean (14 行)
              UpperTheory.FinalTheorems.everyCharacter
              = everyCharacter_of_row (UpperTheory.Gal.Int.galoisLocalGlobalStrong_recParameter)
```

核心装箱文件 `MainTheorems.lean` 全文（16 行）：

```lean
import Formalism.GammaFactorNonvanishing.CritLine
import Development.AutomorphicArithmetic.CharacterBoxes.ClaimStrip
import Development.AutomorphicArithmetic.CharacterBoxes.MainConclusion
open Complex DirichletCharacter
theorem allChi : UpperTheory.EveryCharacter := UpperTheory.FinalTheorems.everyCharacter
theorem rhOfAll : RiemannHypothesis := Formalism.VW.rh_of_every allChi
theorem critAll (N) [NeZero N] (χ) (hχ : χ.IsPrimitive) (s) (h0) (h1) (hz) : s.re = 1/2 :=
  Formalism.VW.critLine allChi N χ hχ s h0 h1 hz
theorem claimAll : Claim.HalfPlane ∧ Claim.Strip ∧ Claim.Zeta :=
  ⟨allChi, Claim.strip allChi, Claim.zeta allChi⟩
```

**关键中间命题（已核对定义/语句，非转述）：**

- `UpperTheory.EveryCharacter`（`CharacterBoxes/EveryCharacter.lean` 第 13-14 行）定义就是：
  `∀ (N) [NeZero N] (χ : DirichletCharacter ℂ N) (s), 1/2 < s.re → (χ ≠ 1 ∨ s ≠ 1) → DirichletCharacter.LFunction χ s ≠ 0`
  —— 和 `Statements.lean` 的 `DirichletLNonvanishingRightOfHalf` **字面同一个命题**。也就是说 `Main.lean` 中 `LFunction_ne_zero_of_half_lt_re` 是直接由同一命题搬过来的。
- `Claim.HalfPlane` / `Claim.Strip` / `Claim.Zeta`（`CharacterBoxes/HalfPlane.lean`）分别就是上面 GRH 右半平面、Dirichlet L 临界线、ζ 临界线三个命题；`ClaimStrip.lean:102` 的 `theorem zeta_iff : Zeta ↔ RiemannHypothesis := Iff.rfl`。
- `Formalism/VW` 命名空间没有单独文件，定义在 `Formalism/GammaFactorNonvanishing/` 两个文件中：
  - `RhOfRight.lean`（62 行）：`rh_of_right (hz : ∀ s, 1/2 < Re s → s ≠ 1 → riemannZeta s ≠ 0) : RiemannHypothesis`。证明方式是标准函数方程论证：对 `Re s < 1/2` 的情况用 `riemannZeta_one_sub` + `completedRiemannZeta_one_sub` 把 ζ(s)=0 转成 ζ(1-s)=0（与假设 `hz` 矛盾），`> 1/2` 直接由 `hz`，`=1/2` 即结论。**逐行读毕，是真正的数学证明，无占位/替换。**
  - `CritLine.lean`（32 行）：`gammaFactor_ne_zero`、`critLine`（由 `EveryCharacter` 推 primitive Dirichlet L 临界线，用到 completed L 函数函数方程与 gamma factor 非零）、`rh_of_every`（χ=1 的 L 函数 = ζ，再套 `rh_of_right`）。
  - `ClaimStrip.lean`（104 行）：`factor_ne_zero`（Euler 因子在 Re>0 不为零）、`prim_zero`（非本原 χ 的零点也是本原 character 的零点）、`prim_reflect`（函数方程反射）、`gamma_ne_zero`、`strip`（`HalfPlane ⇒ Strip`）、`zeta`（`HalfPlane ⇒ Zeta`）。数学上是标准的解析数论 reduction；无 `sorry`。
- `MainConclusion.lean:10`：`UpperTheory.FinalTheorems.everyCharacter := UpperTheory.FinalTheorems.everyCharacter_of_row UpperTheory.Gal.Int.galoisLocalGlobalStrong_recParameter`
- `RowSrc.lean`（8 行）：`galoisLocalGlobalStrong_recParameter : UpperTheory.GalStar.Row0b recT := galoisRepresentations_of_thetaLift UpperTheory.TP.K.tLiftK`
- `GaloisRepresentationsOfThetaLift.lean`：`galoisRepresentations_of_thetaLift (up : TLiftK) : Row0b recT := galoisLocalGlobalStrong_of_geometry_lift Geo.geoOne_holds up`
- `geoOne_holds : GeoOne := geometric_realization_of_weight_one weight_one_geometric_realization`（`IntegralStructures/GeometricFlagBases/WeightOneGeometricRealization.lean:11`）。

**小结（语句层面）：** 从 `Main.riemannHypothesis` 到 `RiemannHypothesis` 的路径只经过约 10 个短桥接文件（合计约 1,300 行），全部为可读、常规的函数方程/character 归约论证。真正的数学重担全部压在 `Development/…` 的 12.2M 行里（主要在 `Development/AbelianVarietyTheory/Proofs` 等），那部分无法在此次审计中逐行做"人类可读"的数学审查；但同样地，**语句替换攻击通常发生在桥接层或语句定义处，这两处已确认干净**。

---

## 4. 反作弊静态扫描（全树 rg，175,187 文件，1.03GB 源码）

扫描在 `/home/kiler/rh-full/src` 上进行（= alpo.ge 原档，见 §2），结果文件保存在 `logs/`。README 的"镜像时静态扫描表"逐项对照：

| 模式 | README 自报 | 我实测（文件数 / 命中行） | 位置/说明 |
|---|---:|---:|---|
| `sorry`（词边界） | 0 | **0 / 0** | — |
| `sorryAx` | —（README 未列） | **0 / 0** | — |
| `admit`（词边界） | 0 | **0 / 0** | 注：全树有 3,322 行含标识符 `admitted`（1,479 文件），那是作者自定义的**假设谓词** `def admitted … : Prop`，不是 admit tactic；`\badmit\b` 为 0 |
| `axiom`（任意出现） | 0 | **0 / 0** | 连注释/字符串里都没有 |
| `constant` 声明 | 0 | **0**（`^\s*(private\|protected)? constant\b`） | 词面 `constant` 35 处全是 `h.constant`/`PreconnectedSpace.constant` 之类的标识符使用，无声明 |
| `opaque` | 0 | **0 / 0** | — |
| `unsafe` | 0 | **0 / 0** | — |
| `implemented_by` | 0 | **0 / 0** | — |
| `@[extern]` | 0 | **0 / 0** | — |
| `native_decide` | 0 | **0 / 0** | — |
| `Lean.ofReduceBool` | —（README 只在 axiom 检查提） | **0 / 0** | — |
| `addDecl` | 1 文件 | **1 文件 / 2 行** | `Formalism/HermitianCurvature/HermitianCurvatureProofs/CutCptCopy.lean:78,82`（详见 §4.1） |
| `set_option maxHeartbeats 0` | 4 文件 | **4 文件 / 4 行** | `CutMainCpt.lean:944`、`SharpRestriction/LevelLetterCocycles/UniformizerClauseOfAdmittedAlt.lean:51`、`…/UniformizerClauseOfAdmitted.lean:48`、`Development/WeilBound/…/PoitouTateDuality/PtfsShaFinal.lean:26` |
| `#eval` | —（README 未列） | **0 / 0** | — |
| 自定义 `macro`/`elab`/`syntax`（声明行） | 22 文件 | **22 文件 / 26 行** | 22 个文件全部列出并抽查；均为 tactic 简写（详见 §4.2） |
| `run_tac` | —（README 未列） | **16 文件 / 32 行** | 详见 §4.3；均为 `first` 分支里 revert-all / assign 目标的小工具 |
| `partial def` | —（README 未列） | **2 文件** | `CutCptCopy.lean:41`（`go`），`Formalism/LocalToGlobal/NumberFieldFamilies/OwnStruct.lean:18`（`copyAt`）——均为 metaprogram 辅助函数，不参与定理证明 |
| `mkSorry` / `admitGoal` / `mkSyntheticSorry` | — | **0 / 0** | 元编程伪造 sorry 的 API 未被使用 |
| `trustCompiler` / `ofReduceNat` | — | **0 / 0** | — |
| `debug.skipKernelTC` / 任何 `debug.*` option | — | **0 / 0** | 无 kernel-skip 类调试选项 |
| `set_option` 总数 | — | **75,196 文件 / 88,137 行** | 选项名分布见下；无任何 soundness 相关选项 |
| `partial`/`unsafe` 声明 | — | 0 | — |

`set_option` 选项名分布（top）：`maxHeartbeats` 57,556；`autoImplicit` 11,203；`maxSynthPendingDepth` 7,478；`synthInstance.maxHeartbeats` 7,381；`backward.isDefEq.respectTransparency` 1,879；linter 类（unusedSectionVars / unusedVariables / unusedSimpArgs / …）约 2,000+；`allowUnsafeReducibility` **37 处 / 33 文件**（README 未列，见 §7 讨论）；`maxRecDepth` 34；其余为 `pp.*`、`hygiene`、`quotPrecheck` 等无害选项。**没有** `debug.skipKernelTC`、`debug.*`、`set_option kernel.*` 之类。

### 4.1 `addDecl` 文件（`CutCptCopy.lean`，91 行）——逐行读过

机制：该文件是一个 `elab "cpt_copy_thms" : command` 元编程命令。它从 `roots`/`manual`/`special` 列表给出的定理名出发，沿"使用到的常量"递归地找出需要复制的定义/定理闭包（`go` 函数），对每个声明执行：

```lean
addDecl (.defnDecl { d with name := n', type := subst tainted d.type, value := subst tainted d.value })
addDecl (.thmDecl  { t with name := n', type := subst tainted t.type, value := subst tainted t.value })
```

`subst` 只把表达式里的常量名按 `mapName` 改名（`suffixed` 给名字加 `Cpt` 后缀，`special` 用显式映射表）。**它不创造新数学内容**：复制出来的定理 = 原定理的语句/证明把内部常量重命名；`addDecl` 走 kernel 类型检查（Lean 的 `addDecl` 对 theorem 会做 kernel check）。调用点仅 1 处：`CutMainCpt.lean:945` 的 `cpt_copy_thms`（其后同文件/下游文件使用 `…Cpt` 变体名，例如 `ThmPActualCpt`、`block_growth_bound_of_…_dataCpt`；共有 168 个路径/名字含 `Cpt`）。**判定：不是 soundness 漏洞，但这是一处"程序化批量生成声明"的 scaffold，说明树里有机器生成的复制层。** README 对此的说明（"a command that copies existing declarations under new names; addDecl still goes through the kernel"）是准确的。

### 4.2 22 个自定义 macro/elab 文件——逐个看过声明行与上下文

清单（`logs/scan_macro_decl.txt`）：`Theta1.lean`(ones)、`ChasePf.lean`(meq)、`ExistsRosatiGen.lean`(secTac)、`PFibreBoundV.lean`(nbt)、`Cup1CoboundaryMemBoundaries.lean`(fin_order)、`ShuffleCup1FormulaPositiveDegree.lean`(fin_order')、`FIwasawaC.lean`(fIwasawa_omega)、`CutCptCopy.lean`(cpt_copy_thms)、`RttUpperRelationsFromDescent.lean`(distrib_module)、`MulMApply.lean`(lvo)、`FaceMapCompSuccAboveCastSucc.lean`(fin_tac)、`SubsingletonRankIndicatorIff.lean`(exists_prescribed_local_data)、`CbBase.lean`(zz, evs)、`CcBase.lean`(ztac, evs)、`Change.lean`(change_aux_intm)、`NegOnePowBoundaryTermsCancel.lean`(fin_index_simp)、`NonsingularNorm.lean`(integ)、`OwnStruct.lean`(kcopy 与 `#kcopy_probe`)、`FunctionalLowerBoundOfConditionsNumeric.lean`(pos_tac, onele_tac)、`Imports.lean`(kexactB)、`IsProperOfFiniteType.lean`(lbt)、`RigidFrameSymmetricRatioSeries.lean`(jet_tac)。

- 其中 20 个是纯 tactic 简写（`macro "名字" : tactic => `(tactic| …)`），内容都是 `simp/omega/linarith/erw/positivity` 组合——标准 Lean 写法，不可能伪造证明（tactic 展开后仍须 kernel 验类型）。
- 3 个是真正的元编程：`cpt_copy_thms`（§4.1，复制已有声明）；`kcopy`（`OwnStruct.lean:53-58`，把 term 的表达式"拷贝"成目标类型对应的表达式，即 def-eq 转换辅助，`g.assign` 仍产生 kernel 可检查项）；`kexactB`（`Imports.lean:5-8`，`elab "kexactB " e:term : tactic` 就是 `exact` 的变体，`g.assign` 已合成的项）。
- 均**未**使用 `mkSorry`/`admitGoal`/`axiom`/`addDecl`（除 CutCptCopy 的复制用途外）；没有绕过 kernel 的 API。

### 4.3 `run_tac`（16 文件 / 32 行）——逐个看上下文

分两类，全部读过：
1. 16 个文件里的 `first | (run_tac Lean.Elab.Tactic.liftMetaTactic (fun g => do pure [← g.revertAll])); exact @_root_.GlobalTheory.….main` —— 只是"把所有假设 revert 后 exact 引理"的兜底分支，等价于手写 `revert_all; exact …`。
2. `ExistsGIs.lean:81` 用 `run_tac do … m.assign (← Lean.Meta.getFVarFromUserName `h)`（把目标 assign 给已有假设）；`FramesTildeGammaValues.lean:70` 用 `run_tac` 从上下文取 `famEq`/`fin`，用 `Subsingleton.elim` 造 `hfin` 后 `g.note`/`replaceMainGoal`——用于处理 instance/子类型 def-eq 繁琐处，赋给 kernel 的仍是合法证明项。
   **判定：无伪造证明；属"AI/自动化生成代码中常见的绕 elaboration 摩擦"写法。**

### 4.4 其他静态红旗排查

- 全树不存在本地重定义 `RiemannHypothesis`/`riemannZeta`（0）。
- `Main.lean` 只有 2 个 import，`Statements.lean` 只 `import Mathlib`；没有可疑的"私有导入替换"。
- 无 `#exit`、无 `@[implemented_by]`、无 `attribute [extern]`、无 `unsafe` 声明、无 `axiom`/`constant`/`opaque`。
- 无 `debug.*` 选项、无 `skipKernelTC`。
- 未发现伪造 kernel 的 `.olean`/二进制文件混入（archive 仅 175,187 个 `.lean` + 3 个配置文本；`.gitignore = .lake/ build/`）。
- 未发现指向 comparator/lean4export/nanoda 之类检查器配置或 CI 的隐藏文件（仓库根只有 README/.gitignore/lake 配置；`git ls-tree` 非 `src/` 仅 5 个文件）。

---

## 5. 结构刻画：17.4M 行是什么样的树？

### 5.1 规模与层级

- 175,187 个 Lean 文件，17,374,215 行，apparent size 1,030,531,854 bytes；平均 99.18 行/文件，**中位数 58 行**。
- 声明行（行首关键词计数，近似）：`theorem` 725,150；`lemma` 26,347；`def` 201,448；`abbrev` 12,614；`instance` 7,401；`structure` 8,185；`class` 43；`example` 4,660。合计约 1.05M 声明行。
- 最大的 5 个文件：`IsAdmissibleSplittingCharPairMulTwist.lean` 17,981 行；`Formalism/SharpRestriction/CuspSpanNormBounds/LatticeGluingRadicals.lean` 9,252；`Development/AutomorphicArithmetic/IntegralCasts/CapelliIdentities/FixPiIff.lean` 8,029；`KappaEndpoints.lean` 6,945；`UnipotentCoordinatesMeasurePreserving.lean` 6,929。
- 文件最多的子目录：`Development/AbelianVarietyTheory/Proofs` **95,418** 个文件（占全树 54%）；`Development/AutomorphicSpectrum/Proofs` 14,864；`Development/AutomorphicArithmetic` 18,431；`Formalism/LocalToGlobal` 5,501；`GroundTheory/HeightsAndTheta` 6,410。

### 5.2 import 图（对 175,187 个文件解析顶部 import 行）

- 总 import 行 909,822；**中位数 4 条/文件**，max 370（`Formalism.HermitianCurvature.HeisenbergConjugationMeasurePreserving`）。
- **136,003 个文件（77.6%）直接 `import Mathlib`（整包）**；269 个文件 import `Mathlib.*` 子模块；外部依赖只有 Mathlib（156,238 条 import 行）、Lean（12）、Batteries（3）。
- 从 `Main` 做 import 传递闭包：**可达 175,187/175,187 个本地模块（100%）、17,374,215/17,374,215 行（100%）**；最大 import 深度 43，深度 10-12 各聚集约 15,000 个模块。→ 从"编译 `lake build Main`"的意义上，**整棵树都是 Main 的依赖闭包**（这也解释了 MIT 为何是"175,187 个模块全部编译"）。但"被 import 到"≠"数学上被用"：大量文件是通过 `Imports.lean`/`Assembly.lean` 等聚合文件挂进闭包的（见下）。
- 扇入最高的模块（被最多文件 import）：`Development.AbelianVarietyTheory.Definitions.Divisors.CTSmallCone`（3,088）、`…SiegelWeilAnisotropicHermitian`（2,972）、`…DiscreteSeriesHermitianUnique`（2,518）、`Development.AbelianVarietyTheory.PublishedTheorems.AutomorphicForms₂.ExistsNormLeHeightPow`（2,460）、`ReciprocityTheory…ToroidalCompactification.UniformisationConclusion`（2,390）。这是一种"定义/接口中心 + 海量引理"的结构，不是单条干净的证明链。
- 聚合式 import 文件很多：`Imports.lean` 375 个、`Statement.lean` 86、`Development.lean` 85、`ImportsAlt.lean` 82、`Assembly.lean` 58（同名文件遍布不同目录，共 4,053 个重名 basename）；扇出最高的文件 import 了 370/321/276/232 个其他模块。这些是"目录级 import 汇总"的 AI 生成脚手架特征。

### 5.3 采样（任务要求的目录，随机抽样，显示路径 + 首个非 import 行）

| 目录 | 文件数 | 抽样路径 | 首个非 import 行 |
|---|---:|---|---|
| `Development/WeilBound/` | 7,051 | `CoreStatements/AutomorphicKernels/UnitaryDualGL/GenericUnitaryDual/CongrProd.lean` | `noncomputable section` |
| | | `RepresentationTheoryGL/SiegelWeilProof/HolomorphicContinuation/GaussianPlaneIntegrals/SecLineB.lean` | `noncomputable section` |
| `Formalism/HermitianCurvature/` | 1,922 | `HermitianCurvatureProofs/RightCapelliAsGenerators.lean` | `open Formalism.REAL Formalism.QuantumDeterminants …` |
| | | `HermitianCurvatureProofs/CutLam.lean` | `open Formalism.FourierDecayAlt` |
| `GroundTheory/` | 8,507 | `HeightsAndTheta/Heights/KleimanAmpleness/StatementsStepThreeOnW.lean` | `set_option maxSynthPendingDepth 1` |
| | | `HeightsAndTheta/Heights/ComplexAnalyticSets/StProperOpenProjectionLocalUnbranched.lean` | `set_option maxSynthPendingDepth 1` |
| `ReciprocityTheory/` | 3,845 | `ReductiveGroups/ArithmeticGeometry/ExtensionDescent/ThetaVV.lean` | `set_option autoImplicit false` |
| | | `AnalyticForms/LeviForms/ProjectiveLineSecondChartSymmOfNe.lean` | `namespace ReciprocityTheory.AnForm.P` |
| `CompanionTheory/` | 2,027 | `SpectralGeometry/LocalGlobalProofs/StableLattices/HeckeRankOneStatement.lean` | `set_option maxHeartbeats 1000000 in` |
| | | `SpectralGeometry/LocalGlobalProofs/StableLattices/ImportsExtraSide.lean` | （空：纯 import 聚合文件） |
| `PositivityTheory/` | 449 | `AutomorphicForms/PublishedInputs/JacquetLanglands/TorusKernels/PfFell.lean` | `noncomputable section` |
| | | `AutomorphicForms/PublishedInputs/RealGaloisRepresentations/IwahoriSphericalTransfer/SqrtNegMovedByInertia.lean` | `open NumberField IsDedekindDomain …` |

共性是：**没有版权头/作者注释**，文件直接从 `import`/`open`/`set_option`/`noncomputable section` 开始，一个文件塞一个小引理（中位数 58 行），符合"按自然语言证明步骤逐步生成"的形态。

### 5.4 AI 生成痕迹（定量）

1. **394 个非 ASCII 路径**：16 个目录名带 U+2082 `₂`（如 `PublishedTheorems/AutomorphicForms₂/`、`GaloisCohomology₂/`、`SiegelWeil₂/`、`Metrics₂/`），另有 7 个含 `₂` 的文件名；每个 `X₂` 目录**没有**同名 ASCII 目录（不是把旧目录改名的结果），394 个 unicode 模块全部被 import。这几乎不可能是人类命名习惯（且会破坏很多工具链；git 默认还会给这些路径加引号）。
2. **命名空间/文件名痕迹**：路径含 `Alt` 751 个、`Bis` 357、`Second` 988、`Copy` 30、`Cpt` 168、`Admitted` 54（如 `UniformizerClauseOfAdmitted.lean`、`ArcCoordinatesAdmittedOfLevels.lean`）、`Dup` 4、`Fake`（命名空间 `GlobalTheory.CompanionTheory.Ar.Cusp.Fake`，内含正常带证明的数学）；`basename` 重复 4,053 种（`Imports.lean` 375 个、`Statement.lean` 86 个…）。
3. **完全相同的文件极少**：按 sha256 分组，175,173 个不同内容，仅 **9 组 23 个文件**字节级相同（多为 1 行的 `Imports.lean`）。→ 树不是简单复制粘贴，而是"变体生成"，与 Claude 渐进式改写相符。
4. **巨型 Proofs 目录**：`Development/AbelianVarietyTheory/Proofs` 95,418 个文件/约 8M 行；很多文件是 10-50 行的小引理，说明证明被拆成碎片逐步生成。
5. **元编程脚手架**：`BuildAid/D1..D5.lean` 用 `run_cmd Lean.modifyEnv` 把 `CompanionTheory`、`CrystallineSemistableComparison`、`GlobalTheory`、`PositivityTheory`、`UpperTheory` 加入 `Lean.LibrarySuggestions.nameDenyListExt`——这是给 Lean 的自动建议/`exact?` 类工具配置"不要建议这些命名空间"的黑名单，典型的 **AI agent 编码会话留下的工具配置**（README 说其"无数学内容"，属实）。
6. **样式并不像 Mathlib**：Mathlib 文件一般有 `Copyright` 头、模块 docstring、命名规范（`Foo.bar_of_baz`）；这里大量文件无头注释、单字母变量、`Imports.lean` 聚合，命名偏长描述式（如 `ExistsNormLeHeightPow`、`EventuallyRankLeRpowOfLtOneDivFiftytwo`）。

**判定：这是一棵典型的大规模 AI 生成 Lean 开发树（"规划-拆解-海量小文件"形态），不是人类手写风格；但这属于"生成方式"证据，不构成逻辑造假证据。**

---

## 6. 独立验证证据（MIT / Andrew Sutherland 页面，2026-11-20）

来源：`https://math.mit.edu/~drew/grh/`（页面自述 "Andrew Sutherland (MIT), checks run with Claude Code. Page last updated 2026-11-20 22:05 UTC"）。我抓取了 `index.html`、`audit.log`、`SHA256SUMS`、`comparator.json`、`Audit.lean`、`project-oleans.sha256`（28,865,695 B，175,187 条编译产物清单）、`nanoda.log`、`con-leche-master.log`、`con-leche-compare.log`、`lean4lean-*.log`、`con-leche-bundled-4.36.log`、`con-ron-bundled-4.36.log`，并逐一对 `SHA256SUMS` 校验：**全部 16 个已下载文件的 sha256 均 OK**。其中 `project-oleans.sha256` = `375cbee2…1d25`，与 SHA256SUMS 及页面 Manifest of all compiled files 值一致；清单恰好 175,187 条，且 ./Main.olean 条目 = `9146dfb4148e24d2252e04c50742f3e49dd126dfcc5006d10bf5f873ddf796ad`，与页面声称的 Main.olean sha256 **逐字符相同**。未下载的仅 solution.ndjson.zst（7.7GB）与 challenge.ndjson.zst（47MB）。

页面声称的检查（原文要点，**非我的复现**）：

| 检查 | 结果 | 细节 |
|---|---|---|
| 175,187 个模块全部编译（Lean v4.33.1, Mathlib v4.33.1） | pass | zero errors；16:43:21 UTC 完成 |
| 5 条主定理 `#print axioms` | pass | 仅 `propext`, `Classical.choice`, `Quot.sound` |
| 环境中无 Lean core 之外的 axiom | pass | 环境共 15 条 axiom，全部在 `Init` |
| Mathlib 文件与官方 cache 逐字节相同 | pass | 8,322 Mathlib + 378 依赖 `.olean` |
| leanchecker kernel replay 每个模块 | pass | 175,187 / 175,187，零拒绝，约 18:17 UTC |
| challenge 导出文件与 Deicyde/riemann-hypothesis CI 发布的一致 | match | sha256 `bd484ac9…b2b9` |
| nanoda（独立 Rust kernel）对完整导出 | accepts | exit 0（27:42，80 线程） |
| Lean 默认/paranoid kernel 重放导出 | running | 页面更新时未完成 |
| `lake comparator` 端到端 | running | 语句比较与 axiom 检查已通过一轮；kernel 检查进行中 |
| con-leche master（cd2eceab）完整导出 | accepts | 1,468,418 declarations accepted；exit 0（3:15，64 线程） |
| con-leche `--compare`（5dc36dc1，Comparator 语句匹配的独立实现） | accepts | 5 条定理全部 "justified by the solution"；51,692 challenge declarations；exit 0 |
| lean4lean（67f63b0c，120k+ 模块逐模块） | pass | 175,187/175,187；其中 175,182 默认通过，5 个（`DyadicPrimeIntervals.Run1-4`、`ChebyshevPrimeBounds.SmallLoop`，都是大 `decide` 计算）超默认 step limit，提高后通过 |
| Lean v4.36.0 自带的 con-leche/con-ron | declined | exit 2（不支持证明里的一个 reflexive inductive type），非拒绝 |
| Lean v4.36.0 自带 lean4lean | not applicable | 读不了 v4.33 core library |

`audit.log` 我本地逐字节核对（sha256 `0a1473fce6…87a62` 与 SHA256SUMS 一致），关键内容：

```
RiemannHypothesis : declared in module Mathlib.NumberTheory.LSeries.RiemannZeta
riemannZeta : declared in module Mathlib.NumberTheory.LSeries.RiemannZeta
RiemannZetaZerosOnLine : declared in module Statements
DirichletLNonvanishingRightOfHalf : declared in module Statements
DirichletLZerosOnLine : declared in module Statements
PrimitiveDirichletLZerosOnLine : declared in module Statements
riemannHypothesis : declared in module Main
riemannZeta_eq_zero_re : declared in module Main
LFunction_ne_zero_of_half_lt_re : declared in module Main
LFunction_eq_zero_re : declared in module Main
LFunction_eq_zero_re_of_isPrimitive : declared in module Main
modules imported: 186200; constants: 2701132; theorems: 2084256
ALL AXIOMS IN ENVIRONMENT (15): [(Classical.choice, Init.Prelude),
 (Lean.ofReduceBool, Init.Core), (Lean.ofReduceNat, Init.Core), (Lean.trustCompiler, Init.Core),
 (Quot.lcInv, Init.Prelude), (Quot.sound, Init.Core), (isScalarObj, Init.Prelude), (lcAny, Init.Prelude),
 (lcCast, Init.Prelude), (lcErased, Init.Prelude), (lcProof, Init.Prelude), (lcUnreachable, Init.Prelude),
 (lcVoid, Init.Prelude), (propext, Init.Core), (sorryAx, Init.Prelude)]
'riemannHypothesis' depends on axioms: [propext, Classical.choice, Quot.sound]
...（其余 4 条同）
```

注意正确解读：**环境里存在 `sorryAx`/`Lean.ofReduceBool` 等 Lean core 自带的 axiom 是正常的**；关键是 5 条主定理的依赖集**不含**它们（README 的"Checked proof"一节也是这么说的）。MIT 页 caveats 原文也要照抄/转述，不要删：

- 编译在**无 sandbox** 的云机器上、直接调用 `lean`（不是 `lake build`）；77 个模块样本与真实 `lake build` 输出逐字节相同，**全量未与 lake build 比对**。
- 因此导出文件（solution.ndjson）具有同样的 unsandboxed provenance；sandboxed 构建（Deicyde protocol）的导出**尚未**做 sha256 对比。
- "A passing check shows that the formal statements, as written in Lean against Mathlib's definitions, follow from the three standard axioms according to the kernels used. It relies on those kernels and on Mathlib's definitions being what they are intended to be."
- "**GRH** here means Dirichlet L-functions only."
- 第一次构建用了错误 module root，已整体丢弃，不在这些结果里。

此外 `comparator.json` 内容（我本地文件与 SHA256SUMS 一致）给出 5 个 theorem 名与 permitted axioms：`["propext","Quot.sound","Classical.choice"]`，与 Main.lean/Statements.lean 的 5 个名字完全一致。

---

## 7. 我能验证什么 / 不能验证什么（诚实边界）

**已在本地独立验证（可复现）：**
1. 计数：175,192 tracked / 175,187 `.lean` / 17,374,215 行 / 分目录表（§1）。
2. 来源：14 分片 → 239,275,554 B → sha256 `9631b4f0…c7fc`；archive 解包树 vs clone **全量 175,187 文件逐字节相同**（`diff -r` 零差异）；根配置 3 文件 sha256 相同；镜像仅加 README/.gitignore。
3. 静态扫描：29 类模式的命中数/位置（§4），与 README 自报**逐项一致**，并补充了 README 未列的 run_tac / partial / allowUnsafeReducibility / debug options 检查（均无 soundness 问题；`allowUnsafeReducibility` 33 文件属于 Lean elaboration 选项，具体语义未在本地 Lean 源码中进一步查证，但任何 kernel 重放都会覆盖这一点）。
4. 语句：`RiemannHypothesis` 的 Mathlib 定义原文；`Statements.lean` 4 条 GRH 陈述逐行核对；全树无本地重定义；5 条 Main.lean 定理的语句与 5 个桥接文件（共约 1,300 行）逐行读过，是常规函数方程论证。
5. 深链结构：`Main → … → galoisLocalGlobalStrong_recParameter → galoisRepresentations_of_thetaLift → Geo.geoOne_holds` 等命名与语句；整树 import 闭包 = 100% 模块。
6. MIT 页面小文件的 sha256 与 SHA256SUMS 一致；页面文字、audit.log、comparator.json、各检查 log 的原文内容。

**未能/无法验证（必须明说）：**
1. **没有编译、没有 kernel 重放、没有 `#print axioms` 本地复现**：WSL 无 Lean/elan/lake，也无 Mathlib（下载 + 编译 17.4M 行 + Mathlib 需要大量时间/内存/磁盘；MIT 页面报告是数小时级、~100GB RAM）。本报告关于"证明成立"的证据全部转自 MIT 页面，未独立复现。
2. 没有下载/核验 7.7GB `solution.ndjson.zst` 与 47MB `challenge.ndjson.zst`（未做导出 sha256 比对；页面给出的 sha256 只能算"转述"）。
3. 未下载 7.7GB `solution.ndjson.zst` 与 47MB `challenge.ndjson.zst`，因此**没有**对导出证明本身做 sha256 比对（页面给出的解/挑战导出 sha256 只能算转述）。已下载并校验的 `project-oleans.sha256` 清单（175,187 条）内部自洽，且其 ./Main.olean 条目与页面声称的 `Main.olean` sha256 `9146dfb4…` 一致——但这只是「页面清单与页面声称一致」，不是由我重新编译得到。
4. 没有对 12.2M 行 `Development/` 做数学正确性/可读性审查；无法判断"这个证明是否真的证出了应该证的东西"超出 kernel 语句的层面——这一步只能靠 kernel 检查的语句忠实性 + Mathlib 定义，而这两项已在 §3/§6 覆盖。
5. 无法独立确认 alpo.ge = Levent Alpöge 本人、发布时间线、remark.pdf 与代码的一致性（remark 由 Lead 的 task-2 负责）。
6. **D: 盘原始 checkout 始终不完整**（长路径问题，Lead 的 reset 任务未能在报告前修好）；本报告用 Lead 的干净 clone `/home/kiler/rh-full`（同 HEAD commit）完成；D: 仓库未被写入。

---

## 8. 红旗 / 需要注意的点（按严重性排序）

**A. 不属于"证明作弊"，但都应向读者标注：**

1. **`addDecl` 复制元编程**（`CutCptCopy.lean` + 调用点 `CutMainCpt.lean:945`）：程序化复制已有声明并改名（168 个 `…Cpt` 名字）。kernel 合法，但意味着部分"引理"是机器复制出来的变体，不是独立证明的数学内容 → 会被计入 17.4M 行/725k theorem 的规模统计。**不违反 soundness，但夸大了"独立数学内容"的量。**
2. **`admitted` 假设谓词普遍存在**：全树 1,479 个文件 3,322 行含标识符 `admitted`（自定义 `def admitted … : Prop` 形式的"文献假设包"），54 个文件名含 `Admitted`。**这不是 `admit` tactic**（扫描 0），而是"给定这些从文献摘取的假设 hA，推出…"的接口设计；最终主定理无假设，说明这些假设包在别处被具体定理/结构填充。但阅读时容易误读，建议明确说明。
3. **`Fake` 命名空间**（`GlobalTheory.CompanionTheory.Ar.Cusp.Fake`）：名字可疑，实际内容是正常带证明的 cusp/weight 数学（101 行文件内全是真证明）。属于命名噪音，不是占位。
4. **`allowUnsafeReducibility`** 33 文件 / 37 处：README 扫描表未列。该选项只影响 elaboration 的可归约性判断，不改变 kernel 的证明检查；MIT 的 kernel 重放/导出检查已覆盖。若要 100% 静态自证，需要进一步查 Lean 源码确认语义（本地无 Lean 工具链，未做）。
5. **`partial def`** 2 处（均为 metaprogram 辅助）、**`run_tac`** 16 文件、**22 个自定义 macro/elab**：均逐一看过，结论是不伪造证明；但确实存在"用元编程绕 elaboration"的写法，属于 AI 生成痕迹。
6. **规模/结构叙事**：17.4M 行中，真正连接 RH 的桥接只有约 1,300 行（§3.2），其余是 `Development/AbelianVarietyTheory/Proofs` 等海量小引理 + 聚合 import 文件；"175,187 模块"是 **import 闭包**，不等于 175,187 个数学上必需的模块。对外表述时不要说"17.4M 行全新数学"。
7. **AI 生成形态**（§5.4）：394 个 unicode 文件名、77.6% 文件整包 `import Mathlib`、中位数 58 行、4,053 个重名 basename、`Cpt/Copy/Fake/Alt/₂` 命名——支持"Claude 生成"的说法，但也提示**代码可维护性/可审查性差**，不是人类可读的"500 页证明"。

**B. 未发现（已用多种方式检查）：** `sorry`/`admit`/`sorryAx`/`axiom`/`constant`/`opaque`/`unsafe`/`implemented_by`/`@[extern]`/`native_decide`/`Lean.ofReduceBool`/`mkSorry`/`debug.skipKernelTC`/本地重定义头条语句/伪造 import/二进制混入。

---

## 9. 最终判定（verdict）

1. **完整性/来源：通过。** 本地 clone 的 `src/` 与 alpo.ge 原始 14 分片拼接档案**逐字节一致**（239,275,554 B / sha256 `9631b4f0…c7fc`），镜像新增内容仅 README.md 与 .gitignore；计数 175,192 / 175,187 / 17,374,215 与 README 完全吻合。
2. **静态"证明作弊"扫描：通过。** 全树无 `sorry`/`admit`/`axiom`/`constant`/`opaque`/`unsafe`/`extern`/`native_decide`/`ofReduceBool`/`#eval`/伪造 sorry API/跳过 kernel 的 debug 选项；`addDecl` 仅 1 处合法复制元编程；22 个 macro/elab、16 个 run_tac 文件逐一看过无问题。与 README 自报扫描表逐项一致（并额外覆盖了其中未列的项目）。
3. **语句与链路：通过（在可审计范围内）。** `Main.lean` 的 `riemannHypothesis : RiemannHypothesis` 用的是 Mathlib 定义（pinned commit 原文件核对 + 本地无重定义 + MIT audit.log 三方一致）；4 条 GRH 陈述是标准的 Dirichlet L 表述；桥接层约 1,300 行逐行读过，是常规函数方程论证，不是语句替换/循环论证。
4. **"这份树能否机械地证明 RH？"** —— **就 Lean 形式化意义：第三方（MIT Sutherland）页面的 kernel 级检查报告是"能"**（编译通过、3 条标准 axiom、leanchecker/nanoda/con-leche/lean4lean 全过、con-leche `--compare` 5 条定理语句匹配），且该页面的产物 sha256 我已核对。但**前提是必须信任**：(a) 该页面及其运行结果（我未复现）；(b) Lean kernel/Mathlib 定义（MIT 也把这一点列为 caveat）；(c) 检查在无 sandbox 环境完成（页面自述，尚未与 sandboxed 构建比对）。**源码文本本身不构成证明**——对没有编译/kernel 重放的审计者，这只是一个"看起来没有造假、语句正确、结构合理"的候选证明。
5. **GRH 范围：** 仅为 Dirichlet L-functions（MIT 页面明确；不要扩大到一般 GRH 或"所有 L 函数"）。
6. **最重要的诚实提醒：** 17.4M 行中大量内容是机器生成的复制层/碎片引理/聚合 import；独立验证者（MIT）做的是 **kernel 级**验证，而不是**人类数学审查**；作者本人 remark 也说明后续会简化（task-2 负责）。因此正确表述是：**"在 Lean kernel 与 Mathlib 定义可信、且 MIT 页面所述检查成立的前提下，该仓库被形式化验证建立 Mathlib 的 RiemannHypothesis 及 Dirichlet-L GRH 四条陈述；它不构成人类可读的证明，也尚未经同行数学审查。"**

---

## 附录 A：本次运行的关键文件

- `report.md`（本文件）
- `logs/scan_summary.txt`：29 个扫描模式的 文件数/命中行数汇总；`logs/*.txt` 为各模式原始命中
- `logs/struct_out.txt`、`logs/struct2_out.txt`、`logs/struct3_out.txt`：import 图/闭包/重复/采样/目录统计输出
- `logs/options.txt`：`set_option` 选项名分布；`logs/root_hashes.txt`：根配置/README/.gitignore sha256；`logs/wc_all.txt`：逐文件行数
- `mit/`：`index.html`、`audit.log`、`SHA256SUMS`、`comparator.json`、`Audit.lean`、`nanoda.log`、`con-leche-*.log`、`lean4lean-*.log`、`mathlib_RiemannZeta.lean`（pinned commit 抓取）
- `archive/lean.tar.gz`：14 分片拼接后的 239,275,554 B 档案（sha256 已核）；`parts/`：14 个原始分片

## 附录 B：本报告未做的事（防止误读）

- 未编译、未跑 `#print axioms`、未跑 leanchecker/nanoda/con-leche/lean4lean/comparator（本地无工具链/依赖，且超出 ~1 小时预算）。
- 未逐行审查 `Development/` 12.2M 行数学内容。
- 未验证 remark.pdf 与代码的对应、未调查媒体/同行评审状态（Lead 的 task-2）。
- 未修改 D: 盘原仓库；所有写操作只发生在 `_rh-work/repo-verifier/`、`/tmp/`、`/home/kiler/rh-full` 只读。
