# Lean/RH 状态复核、Mathlib 哥德巴赫调查、以及"RH ⇒ Goldbach"攻击路线的 Lean 可形式化性评估

- 报告人：teammate `lean-feasibility`（shared task board **task-6**）
- 时间：2026-11-21 11:05–11:20 CST（= 2026-11-21 03:05–03:20 UTC）
- 机器：WSL Ubuntu（user kiler），16 核 / **15 GiB RAM**，Linux FS ≈ 948 GB 空闲，D: ≈ 120 GB 空闲
- 结论标记：**【事实】**= 有命令输出/一手页面证据；**【推测】**= 工程估计
- 交付物：本文件 + `lean-check/`（可复跑的 standalone `.lean` 与输出）+ `/home/kiler/rh-work/lean-test/evidence/`（原始证据）

---

## 0. TL;DR（中文要点）

1. **RH 验证页没有更新。** 2026-11-21T03:05:54Z 抓取的 `https://math.mit.edu/~drew/grh/` 页面与本地 02:16Z / 02:20Z 快照**逐字节相同**（sha256 `de7153ec…62307`），页面仍写 "Page last updated 2026-11-20 22:05 UTC"。两个未完成项状态不变：**`lake comparator`（端到端）仍 running；Lean default / paranoid kernel replay of the export 仍 running（单线程、无结论）**。其余检查全部 pass/accept。**【事实】**
2. **本地镜像 `/home/kiler/rh-full` 未变**：HEAD = `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`，工作区干净；tracked 文件 175,192、`.lean` **175,187**、总行数 **17,374,215** —— 与 README/既有记录一致。**【事实】**
3. **Mathlib 没有哥德巴赫猜想的形式化语句。** 在精确 pin 的 Mathlib（commit `0df444a360eaa60ab8c11dca51a86af692955474`，tag v4.33.1，即 RH 证明所用版本）全库 9,030 个文件中，`goldbach`（不分大小写）只有 **2 处**：`Mathlib/NumberTheory/Fermat.lean:98` 的 *Goldbach's theorem*（Fermat 数两两互素）与 `docs/references.bib` 的书信集条目；**没有** `Goldbach` 猜想、Chen 定理、Hardy–Littlewood、singular series、circle method 的形式化。**【事实】**
4. **Mathlib 有 `RiemannHypothesis`**：`Mathlib/NumberTheory/LSeries/RiemannZeta.lean:185`，定义与 MIT 页面引用逐字一致。**【事实】**
5. **Onboarding 结果：Lean 工具链成功自举并在本机跑通。** WSL 内 github 域名被 hosts 劫持到 127.0.0.1；PowerShell 直连 GitHub 能通但只有 ~0.1 MB/s；改用 `https://gh-proxy.com/` 从 WSL 拉 GitHub release，达到 13.2 MB/s。下载官方 `lean-4.36.0-linux.zip`（946,865,949 B，与 GitHub API 列出的 asset 大小完全一致，sha256 `92a996be…902a`），用 `python3 zipfile` 解压（系统无 zstd/unzip），`chmod` 后：**`Lean (version 4.36.0, x86_64-unknown-linux-gnu, commit 611c117bfaf7b7ae1cfcf246ce6fba31e8f509e9, Release)`**。**【事实】**
6. **两个 standalone（不依赖 Mathlib）的 Lean 检查真实跑通、exit=0、无 sorry：**
   - `no_go_int.lean`：`{c − t : t ≥ 0} = (−∞, c] ∩ ℤ`，外加"结果可以任意负"的例子；axioms 仅 `[propext, Quot.sound]`。
   - `no_go_rat.lean`：**rank-one 正性方向引理**（ℚ 上）：`∀ c v : ℚ, v ≠ 0 → ∀ x, (∃ t ≥ 0, x = c − t·v²) ↔ x ≤ c`；仅用 `Init.Data.Rat.Lemmas`；axioms 仅 `[propext, Classical.choice, Quot.sound]`。
   这两条是我们 no-go 分析（task-5 报告）中"正性方向引理"的忠实退化影子，用于证明：**T ≥ 0 只能给出 x ≤ c，永远不能证明 x > 0（Goldbach 需要的方向）**。**【事实】**
7. **Alpöge/Claude 的证明架构不是 spectral/heat-kernel 的。** [事实] 全库中 thermal = 0 文件；`heat kernel` 精确短语 = 0；`HeatKernel` 标识符仅 **13** 个文件（占 175,187 的 0.0074%），全部在 `Development/AbelianVarietyTheory/Proofs/DivisorProofs/`（`IsHeatKernel` 定义在 `.../PublishedTheorems/Divisors₂/IsTorsionFormPoint.lean:93`），是 Abel 簇/周期域上除子理论里的局部工具；而 `SiegelWeil` 出现在 **6,860** 个文件、`theta lift` 2,480、`HermitianCurvature` 2,725、`Weil` 3,216、`spectral` 3,082。从 `Main.lean` 出发的 import 闭包 = **175,184 / 175,187 个模块（99.998%）**，即整个库几乎全部都在主定理闭包里。证明主体 = 自守表示/theta 提升/Siegel–Weil 公式/局部 Langlands + Hermitian curvature + positivity 的机器，**不是** 用户设想的"热核迹正性"谱架构。**【事实】**
8. **总判定**：本环境能产出的是 **tiny standalone Lean 引理**（已产出并验证），**不可能**产出与"RH ⇒ Goldbach"有关的正式定理。把 Li–Liu 条件链形式化并得到"Hypothesis S ⇒ Goldbach 渐近"的可 Lean 检查定理，量级估计 **10 万–30 万行新 Lean、60–160 人月（约 5–13 人年）**【推测】，且 S/R 本身不是 GRH 的推论（论文自己给出的 GRH 可用界 `(log N)²` 远大于所需的 `δ_N = √(S(N)(log N)³/N)`，见论文 (2.24)(2.27)–(2.30)）。

---

## 1. RH Lean 验证状态复核（`https://math.mit.edu/~drew/grh/`）

### 1.1 抓取与比对（命令 + 原始输出）

```bash
$ cd /home/kiler/rh-work/mit && date -u +"FETCH_AT_UTC=%Y-%m-%dT%H:%M:%SZ"
FETCH_AT_UTC=2026-11-21T03:05:54Z
$ curl -sS -m 20 -o grh_page_1130.html "https://math.mit.edu/~drew/grh/"
page fetched 12782 bytes
$ sha256sum grh_page_1130.html grh_page.html grh_page_now.html
de7153ec1b22acab193a99824d427d41050e2c0d2c4374ec518d52fc0de62307  grh_page_1130.html
de7153ec1b22acab193a99824d427d41050e2c0d2c4374ec518d52fc0de62307  grh_page.html        # 02:16Z 快照
de7153ec1b22acab193a99824d427d41050e2c0d2c4374ec518d52fc0de62307  grh_page_now.html   # 02:20Z / 11:04 CST 快照
# 03:15:22Z 再次抓取（final）：
de7153ec1b22acab193a99824d427d41050e2c0d2c4374ec518d52fc0de62307  grh_page_final.html
```

**答案：页面没有更新。** 页面自身仍声明 "Page last updated 2026-11-20 22:05 UTC"；在本报告抓取时（03:05Z 与 03:15Z，距其 22:05Z 约 5–5.2 小时）内容逐字节未变。

### 1.2 当前页面的精确状态（原文表格摘录）

页面 Summary（原文）："... the five headline theorems depend only on the three standard axioms, every module has been replayed through the Lean kernel, two independently written kernels, nanoda and con-leche, accept the full exported proof, and lean4lean accepts every compiled module. con-leche's `--compare` mode ... confirms all five theorems against the challenge. **The `lake comparator` run and the Lean-kernel replay of the export are still in progress.**"

页面检查表（原文，节选关键行）：

| Check | Result | Detail |
|---|---|---|
| All 175,187 modules compile (Lean v4.33.1, Mathlib v4.33.1) | pass | zero errors; finished 16:43:21 UTC |
| `#print axioms` for the five theorems in `Main.lean` | pass | `propext`, `Classical.choice`, `Quot.sound` only (`audit.log`) |
| No axioms declared outside Lean core | pass | 15 axioms in the environment, all in `Init` |
| Mathlib files identical to the official cache | pass | 8,322 Mathlib + 378 dependency `.olean` files, byte for byte |
| `leanchecker` kernel replay of every module | pass | 175,187 of 175,187; zero rejections; finished about 18:17 UTC |
| Challenge export equals the one published by Deicyde/riemann-hypothesis CI | match | sha256 `bd484ac9…b2b9` |
| nanoda (independent Rust kernel) on the full export | accepts | exit 0 at 19:05:45 UTC; 27 min 42 s on 80 threads (`nanoda.log`) |
| **Lean default kernel and Lean paranoid kernel on the export** | **running** | **single-threaded; no verdict yet** |
| **`lake comparator` (Lean v4.36.0) end to end** | **running** | **statement comparison and axiom check already passed in one run; kernels in progress** |
| con-leche master (`cd2eceab`) on the full export | accepts | 1,468,418 declarations accepted in `--verified` mode; exit 0 at 21:19:04 UTC |
| con-leche `--compare` (branch `compare`, `5dc36dc1`) | accepts | all five theorems "justified by the solution"; 51,692 challenge declarations accepted; exit 0 at 21:19:12 UTC |
| lean4lean (`67f63b0c`, Lean v4.33.1) on compiled files | pass | 175,187 of 175,187; finished about 21:55 UTC; 175,182 default, 5 with raised step limit |
| con-leche and con-ron bundled with Lean v4.36.0 | declined | exit 2, **not a rejection**: older binaries don't support one reflexive inductive type |
| lean4lean bundled with Lean v4.36.0 | not applicable | cannot read a v4.33 core library (`unknown constant 'Decidable.intro'`) |

页面还给出关键 provenance（原文）：源归档 `lean.tar.gz` = alpo.ge 的 14 个 part 拼接，239,275,554 bytes，sha256 `9631b4f0…c7fc`；Lean v4.33.1 (commit `819816b2`)；Mathlib tag v4.33.1 (`0df444a3`)；两个 caveats：**构建在无沙箱云机器上、以直接调用 `lean` 而非 `lake build` 的方式编译**（77 模块样本与 lake build 逐字节一致，全套未比对）；export 因此具有相同 unsandboxed provenance。

### 1.3 官方校验文件是否变化（下载比对）

```bash
$ for f in audit.log comparator.json SHA256SUMS nanoda.log; do
    curl -sS -m 20 -o "final_$f" "https://math.mit.edu/~drew/grh/$f"
    echo "$f sha256=$(sha256sum final_$f | cut -d' ' -f1)"; done
audit.log         sha256=0a1473fce6eed840011f4a76b1c51558fc6f03edd1e6bd1ee542e6c738d87a62
comparator.json   sha256=8ea890e6ccda9cf3983ada343af18a41d12542036875a3936e7925ed5b1582ff
SHA256SUMS        sha256=d8496902f492eeb0274460e525071cc30803bba7817d59b27c874f5a25317373
nanoda.log        sha256=d4c5360b02d8dd885150c1cc28b616cb6fb5bf5b20d142558d79a7b15ae9d9df
```

与 02:16Z / 02:20Z 抓到的同批文件逐字节相同（`cmp` 验证 `audit.log`、`comparator.json`、`SHA256SUMS`；`nanoda.log` 的本地旧副本已被其他 teammate 覆盖/清理，但其 sha256 与 `SHA256SUMS` 中登记的 `d4c5360b…9df` 及 02:05Z 抓取的 `now_nanoda.log` 完全一致；见 `/home/kiler/rh-work/lean-test/evidence/mit/`）。`SHA256SUMS` 内容（原文）：

```
61a8938ad5f5e57397c1c0e3b954916af546d9004ade01c3555744a681b05381  solution.ndjson.zst
c24ef99dab3556a52c7fb886e03cf22a242f3b96f82ae4cc40539e5d2f678ac6  challenge.ndjson.zst
8ea890e6ccda9cf3983ada343af18a41d12542036875a3936e7925ed5b1582ff  comparator.json
0a1473fce6eed840011f4a76b1c51558fc6f03edd1e6bd1ee542e6c738d87a62  audit.log
5d54e164c67969da6169bd9a4d5b990ae9e7a7ffe16345dcebef257b0227d346  Audit.lean
375cbee2fc3fc0f5088ef2e6dc9a5ac5530924310dc62422ec65aac9dc4c1d25  project-oleans.sha256
d4c5360b02d8dd885150c1cc28b616cb6fb5bf5b20d142558d79a7b15ae9d9df  nanoda.log
23e27eacb9e8378569474cc185c0e98f6b995b4db0f8df88fd48a921084fed02  con-leche-master.log
5a068bf55f24904eea9f05eda947c63d43bdee3c6ab0490e43943a3bd9af1f6e  con-leche-compare.log
86fbcad86db64c02ebd540861b05db4ae7d98f6c504a17ada0fa12e3fe878cbf  con-leche-bundled-4.36.log
16a76d9a8282fff5a5daad72797b60d4ce0fe93e1ce633bd92573fffd87680f1  con-ron-bundled-4.36.log
d2612cd1efeeb40f1c7df282ede78685469b4cc7075757c749b90a5f5059878a  lean4lean-raised-fuel.log
a12a614cf71d456d22f0877071eec366d1d6a4b268f095620eaf75c1a24af35c  lean4lean-default-fuel-timeouts.log
5ea74b912147c5c93cc2b6d70cc727cf908df2f62ac6a20480a3fa02f6be244e  solution.ndjson
bd484ac9886a96f26b1d9a7a59ebd45b7a70d102c015d4f31f9302bbdd6ab2b9  challenge.ndjson
```

**结论【事实】**：截至 2026-11-21T03:15Z，官方页面/校验文件无任何更新；`lake comparator` 端到端与 Lean default/paranoid kernel replay of the export 仍处于 running，尚无 verdict。其余 9 项检查 pass/accept。（注：两项 running 都是单线程、在 7.7 GB 压缩 / 61.6 GB 解压的 export 上跑，耗时以小时计是合理的；本机只有 15 GiB RAM，远不足以复跑 —— 复跑需要 ~100 GB RAM、~70 GB 磁盘，见页面 "Check it yourself"。）

### 1.4 本地镜像 `/home/kiler/rh-full` 复核

```bash
$ cd /home/kiler/rh-full
$ git rev-parse HEAD
7cbf7a0c32fca1badf05931879a37c3f8a2b03b4
$ git log -1 --format='%H %ci %s'
7cbf7a0c32fca1badf05931879a37c3f8a2b03b4 2026-11-20 23:13:33 +0800 README: credit, statements, layout, download, build and checking guide
$ git status --porcelain        # 空 = 工作区干净
$ git ls-tree -r -z --name-only HEAD | tr '\0' '\n' | wc -l          # tracked 文件
175192
$ git ls-tree -r -z --name-only HEAD | tr '\0' '\n' | grep -c '\.lean$'
175187
$ find . -name '*.lean' -not -path './.git/*' | wc -l                 # 工作区 .lean
175187
$ find . -name '*.lean' -not -path './.git/*' -print0 | xargs -0 cat 2>/dev/null | wc -l
17374215
$ du -sh /home/kiler/rh-full
1.7G
```

非 `.lean` tracked 文件只有 5 个：`.gitignore`、`README.md`、`lake-manifest.json`、`lakefile.toml`、`lean-toolchain`（其中 `lean-toolchain` = `leanprover/lean4:v4.33.1`）。**头 commit、文件数、行数与既有记录完全一致（未变）。【事实】** 未重跑任何 heavy build（本机无 100 GB RAM，且任务要求）。

---

## 2. Mathlib 调查（精确 pin 到 RH 证明所用 commit）

### 2.1 方法与来源

WSL 内 `github.com` / `api.github.com` / `raw.githubusercontent.com` 均被解析到 `127.0.0.1`（见 §4.1），无法直连。通过 Windows 侧网络取到 Mathlib **精确 pin 的源码 tarball**：

```bash
$ cd /home/kiler/rh-work/lean-test
$ time curl -sSL --retry 3 -o mathlib4-src.tar.gz \
    "https://gh-proxy.com/https://github.com/leanprover-community/mathlib4/archive/0df444a360eaa60ab8c11dca51a86af692955474.tar.gz"
DONE http:200 size:23413113 speed:3217724B/s total:7.276296s
$ sha256sum mathlib4-src.tar.gz
4906567b829fea7e354022c603aeebead7dd2f4ad1a39a91cc42ffae5de46326  mathlib4-src.tar.gz
$ tar -xzf mathlib4-src.tar.gz -C mathlib4-src --strip-components=1   # 解压后 121 MB
$ find mathlib4-src -name '*.lean' | wc -l
8852
$ cat mathlib4-src/lean-toolchain
leanprover/lean4:v4.33.1
```

tarball 顶层目录名 = `mathlib4-0df444a360eaa60ab8c11dca51a86af692955474`，与 MIT 页面 "Mathlib tag v4.33.1 (0df444a3)" **完全一致**。以下所有结论都在这个确切版本上以 `grep -rIl` 验证。

### 2.2 哥德巴赫猜想：**不存在**

```bash
$ grep -rIil -i goldbach .          # 全库 9,030 文件（8,852 .lean）
./docs/references.bib
./Mathlib/NumberTheory/Fermat.lean
$ grep -rIi -n goldbach .
./docs/references.bib:3429:  title         = {Leonhard Euler und Christian Goldbach: Briefwechsel
./Mathlib/NumberTheory/Fermat.lean:98:**Goldbach's theorem** : no two distinct Fermat numbers share a common factor greater than one.
$ find . -iname '*goldbach*'        # 文件名搜索：空
```

- `Mathlib/NumberTheory/Fermat.lean:98` 是 **Goldbach 的一个无关定理**：任意两个不同的 Fermat 数互素（`Nat.coprime_fermat`），与二素数猜想无关。
- 全库**没有** `Goldbach`、`BinaryGoldbach`、`StrongGoldbach` 等定义或命题；没有"每个大于 2 的偶数都是两素数之和"的字符串。
- 相邻课题同样缺失：`Hardy space` 0 文件；`singular series` 0；`Hardy-Littlewood` 0；`Fueter` 0；`slice regular` 0。`Hilbert–Schmidt` 只在 `docs/1000.yaml` 的"千年问题清单"标题出现 1 次；`Chen's theorem` 同；`circle method` 仅 `Mathlib/Combinatorics/KatonaCircle.lean` 的 Katona 组合圆方法（无关）；`Prime Number Theorem` 4 处（`LSeries/Nonvanishing.lean` 注释 + 文档 + `scripts/downstream_repos.yml`）。

**结论【事实】：Mathlib4 @ 0df444a3 没有哥德巴赫猜想的形式化语句 —— 连"待证猜想"的陈述都没有。**

### 2.3 `RiemannHypothesis`：存在，且就是 MIT 页面引用的那个定义

```bash
$ grep -n -A3 -B2 "def RiemannHypothesis" Mathlib/NumberTheory/LSeries/RiemannZeta.lean
184-@[wikidata Q205966]
185:def RiemannHypothesis : Prop :=
186-  ∀ (s : ℂ) (_ : riemannZeta s = 0) (_ : ¬∃ n : ℕ, s = -2 * (n + 1)) (_ : s ≠ 1), s.re = 1 / 2
```

与 MIT 页面 "What was verified" 段落引用的定义逐字一致；页面说明：*"'GRH' here means Dirichlet L-functions only."* 镜像仓库 `src/Statements.lean`（16 行，只 import Mathlib）另定义 `RiemannZetaZerosOnLine` / `DirichletLNonvanishingRightOfHalf` / `DirichletLZerosOnLine` / `PrimitiveDirichletLZerosOnLine` 四条 GRH 相关陈述。**【事实】**

### 2.4 素数计数 / PNT / 解析数论工具盘点

| 课题 | Mathlib 现状（路径） | 证据 |
|---|---|---|
| 素数计数函数 | `Mathlib/NumberTheory/PrimeCounting.lean`：`Nat.primeCounting`（π）、`Nat.primeCounting'`、`Nat.primesBelow`、`Nat.primesLE`；单调性 + 上界 | 10,196 B |
| Chebyshev 函数 | `Mathlib/NumberTheory/Chebyshev.lean`：`Chebyshev.psi`（Σ Λ）、`Chebyshev.theta`（Σ log p）、Chebyshev 上下界、Costa–Pereira 不等式；注释称部分由 **PrimeNumberTheoremAnd** 项目 upstream（Kontorovich et al.） | 38,375 B |
| **完整 PNT** | **不在 Mathlib**（只有 Chebyshev 阶的初等界；完整 PNT 在独立项目 PrimeNumberTheoremAnd） | 文本 + 注释 |
| Bertrand 假设 | `Mathlib/NumberTheory/Bertrand.lean` | — |
| von Mangoldt | `Mathlib/NumberTheory/ArithmeticFunction/VonMangoldt.lean`：`ArithmeticFunction.vonMangoldt`（Λ）、`vonMangoldt_sum`、Möbius 反演表达 | 6,639 B |
| Selberg 筛 | `Mathlib/NumberTheory/SelbergSieve.lean`：上界筛框架、Λ² 筛、主项对角化 | 18,731 B |
| 几乎素数 | `Mathlib/NumberTheory/AlmostPrime.lean`：`Nat.IsAlmostPrime k n`、`Nat.IsSemiprime`、`IsAtMostAlmostPrime` | 3,162 B |
| 素数倒数和发散 | `Mathlib/NumberTheory/SumPrimeReciprocals.lean`（Erdős 证明） | 6,616 B |
| Abel 求和 | `Mathlib/NumberTheory/AbelSummation.lean` | 22,772 B |
| Dirichlet L 函数 | `Mathlib/NumberTheory/LSeries/{Basic,Dirichlet,DirichletContinuation,AbstractFuncEq,HurwitzZeta,…}.lean`（21 个文件）；`DirichletCharacter/{Basic,Bounds,GaussSum,Orthogonality}.lean`；`LSeries/Nonvanishing.lean`（`LFunction_ne_zero_of_one_le_re`；PNT/AP 的前置）；`LSeries/PrimesInAP.lean`（**Dirichlet 素数等差数列定理**，用 von Mangoldt residue class + L′/L 线性组合）；`LSeries/Deriv.lean`（L 级数可微/导数）；`LSeries/ZetaZeros.lean`（ζ 零点集离散/闭，紧集内有限） | 见左 |
| 复分析/积分变换 | `Mathlib/Analysis/MellinTransform.lean`、`Mathlib/Analysis/MellinInversion.lean`（`mellin_inversion`）、`Mathlib/Analysis/Complex/CauchyIntegral.lean`、`PhragmenLindelof.lean`、`Hadamard.lean`、`Mathlib/Analysis/SpecialFunctions/Gamma/Beta.lean`（`Complex.betaIntegral`、Γ·Γ=Γ·Β、反射公式）、Fourier 反演 | 见左 |
| Hilbert 空间算子 | `Mathlib/Analysis/InnerProductSpace/Positive.lean`（`IsPositive`：自伴 + `0 ≤ re⟪Tx,x⟫`）；`Mathlib/Analysis/InnerProductSpace/Spectrum.lean`：**紧自伴算子谱定理**（`orthogonalComplement_iSup_eigenspaces_eq_bot`、`finite_dimensional_eigenspace`；文件 TODO 明确写着 "Spectral theory for bounded self-adjoint operators" 未做） | 见左 |
| **Hardy 空间 H²** | **0** —— 无 Hp 空间理论 | grep |
| **Hilbert–Schmidt 范数/迹类** | **0** —— 无 HS 算子、无 trace class | grep |
| 奇异级数 | **0** | grep |
| 四元数分析（slice-regular / Fueter） | **0**（只有代数四元数 `Mathlib/Algebra/Quaternion.lean` 与作为赋范代数的 `Mathlib/Analysis/Quaternion.lean`，无四元数解析函数论） | grep |
| GRH 条件化的 L′/L 估计、显式公式、零点密度 | **0**（无 Guinand–Weil 显式公式，无显式零点计数） | grep |

---

## 3. Li–Liu 条件链 vs Mathlib：ingredients 清单与工程量估计

论文：Jiamin Li & Jianya Liu, *A Conditional Proof of the Goldbach Conjecture*（本地 PDF `/home/kiler/rh-work/liu-goldbach.pdf`，抽取文本 `liu-goldbach.clean.txt`，4,432 行）。以下"论文位置"按 clean 文本行号 / 章节号引用。

### 3.1 逐项对照

| # | 论文所需 ingredient | 论文位置（证据） | Mathlib 现状 | 需新写量级（估计【推测】） |
|---|---|---|---|---|
| 1 | Dirichlet 精确投影（奇数特征正交性 + 有限投影） | §2.1.1（L275–333）；§3.1–3.2（L985–1140） | 部分：`DirichletCharacter/Orthogonality.lean`、`ZMod`、特征和 | 2–6k 行 |
| 2 | Mellin 反演（垂直线上积分、contour shift、L′/L 的留数/解析延拓） | §2.1.2（L334–377）；§2.5.1（L836–881）；§7.1（L3114+） | 部分：`MellinInversion.lean` 只有基本反演；**Mathlib 无留数定理**（`residue` 仅在 LSeries 文件内部实现中出现），无竖线积分的 contour shift 框架 | 5–15k 行 |
| 3 | Beta 模型与 Γ 因子分解（continued Beta model、X₁(s)、反射/加倍公式） | §2.2（L408–524）；§4（L1331–1691） | 部分：`Complex.betaIntegral`、Γ 反射/加倍公式在 `Gamma/Beta.lean`；论文的特制 continued Beta 模型需另建 | 2–5k 行 |
| 4 | **Hardy 空间 H²(S_N)（竖直条带）、边界迹、Fourier–Laplace 表示** | §2.3.2（L548–620）；§5.1–5.2（L1790–1930）；Lemma 5.2（L1878） | **完全缺失**（Hardy space = 0） | 15–40k 行 |
| 5 | 自伴/正算子、紧算子、**Hilbert–Schmidt 范数** 与 HS 积分算子 | §2.3.2（L583）；§5.3（L1930–2034，HS 范数、谱定理使用） | 部分：紧自伴谱定理已有（`InnerProductSpace/Spectrum.lean`）；HS 范数/核的平方可积性理论**缺失** | 5–15k 行 |
| 6 | 谱乘积 X_N(q) 与**四元数 slice-regular 函数**、零点分类（临界线 vs 实对） | §2.4.1–2.4.2（L629–750）；§6.1–6.2（L2184–2401） | **完全缺失**（Fueter/slice-regular = 0；四元数只有代数） | 10–30k 行（可从复系数重写以省 50%？仍需自建形式化） |
| 7 | Dirichlet L 的 **L′/L** 及 GRH 下的解析估计（对数导数均值、零点-free 区域） | §2.4.3（L751–776）；§3.3（L1141–1261）；§6.4（L2483–3068） | **基本缺失**：L 函数连续/整函数在 Mathlib 有，但 GRH-条件的 L′/L 界、显式公式、零点的显式估计都没有 | 30–100k 行（最大头） |
| 8 | von Mangoldt 和、素数幂、序列/级数一致收敛与误差项 | §1.2（L93–260）；§7.1.3（L3395+） | 部分：von Mangoldt 定义、Chebyshev ψ/θ 初等界；AP 中的 Λ 与 L′/L 关系在 `PrimesInAP.lean`；但所需带权、带误差的和需重建 | 5–15k 行 |
| 9 | Goldbach 奇异级数 S(N)、局部密度、欧拉乘积 | §1.2（L70–92）；§2.2（L468–505）；§8（L3711+） | **缺失**（singular series = 0），但数学上是初等欧拉乘积 | 2–5k 行 |
| 10 | 二次型恒等式 `G(N)=c_φS(N)−⟨T_Nv_N,v_N⟩`、Riesz 向量范数一致界、Cauchy–Schwarz 主估计 | §2.3.3（L600–620）；§2.5.2（L882–934）；§7.2（L3425–3638） | 需要 4+5+8 的组合 | 10–25k 行 |
| 11 | 假设 S/R 的精确表述 + 最终从带权计数到"每个大偶数都是两个素数之和"（去除素数幂、小 N 处理） | §2.4.4（L777–830）；§7.3（L3639–3710） | 缺失（含 Goldbach 陈述本身，见 §2.2） | 3–8k 行 |
| 12 | 均匀性 in N（N→∞ 一致常数、h(N) 任意慢增、奇异级数 S(N)≍loglog N 的界） | (2.26)–(2.30)；§8 | 缺失 | 含在 7+11 |

合计粗估【推测】：**新写 10 万–30 万行 Lean，60–160 人月 ≈ 5–13 人年**（熟悉 Mathlib 的 1–2 名专家；若允许大量 AI 辅助，可能压缩 20–50%，但不改变数量级）。对照：Mathlib 本身 1,500 万+ 行、汇聚全球贡献者多年；PrimeNumberTheoremAnd 项目仅覆盖 PNT 及其周边就耗时数年。**这还不含** 证明 Hypotheses S/R（论文的核心未解输入；见 §3.3）。

### 3.2 数学上真正"最小可 Lean 检查"的引理（本任务已选并验证）

把 §3.1 的差距全部压缩后，攻击路线的核心否证只依赖一条初等引理（task-5 报告中的 positivity-direction lemma）：

> 设 H 为实内积空间，v ≠ 0，c ∈ ℝ。则
> `{ c − ⟨Tv, v⟩ : T : H → H 自伴, T ≥ 0 } = (−∞, c]`。

因此 **T ≥ 0 只能把 `c − ⟨Tv,v⟩` 往下推，永远不能证明 Goldbach 所需的 `⟨Tv,v⟩ < c`（即 `G(N) > 0`）**。这条引理本身可以直接在 Lean/Mathlib 里形式化（用 `InnerProductSpace`、`ContinuousLinearMap.IsPositive`；Mathlib 里 `IsPositive` 已要求自伴，且已有 `c • 1` 型正算子的正性），估计 **100–300 行、约 1–2 周**（有 Mathlib olean cache 的前提下）。

本报告实际跑通的是它的**忠实退化影子**（见 §4；core Lean，无 Mathlib）：
- `no_go_int.lean`：ℤ 上 `{c − t : t ≥ 0} = (−∞, c]`；
- `no_go_rat.lean`：ℚ 上 rank-one 版本 `{c − t·v² : t ≥ 0} = {x : x ≤ c} (v ≠ 0)`（1 维时自伴 T = 乘以 t，T ≥ 0 ⇔ t ≥ 0，⟨Tv,v⟩ = t·v²）。

另一条 task-5 的 rigorous lemma ——"生成函数正值不蕴含系数正值"的反例 `F(t)=e^{−t}−2e^{−2t}+2e^{−3t} > 0 (t>0) 但 a₂<0` ——**不能**在本机的 core-only 工具链里检查，因为它需要 `Real.exp`/`ℝ`（Mathlib）。在 Mathlib 下这条反例是初等的（约 50–150 行，1–3 天）。多项式影子（`1−2t+2t²` 判别式）也可在 ℚ 上形式化，但价值低于直接做 Real.exp 版本，故本次未做。

### 3.3 为什么"GRH 已证"不能替代 Hypotheses S/R（引用论文原文）

论文自己给出的 GRH 可用界是 (2.24)：`‖T_N‖ ≤ ‖T_N‖_HS ≪ (log N)²`（§2.4.3, L751–776），由此只能得到零免区 (2.25) `η_N^GRH ≍ S(N)/(N log N)`；而 Goldbach 渐近所需的是 (2.26)–(2.27)：

```
|G(N) − c_φS(N)| / (c_φS(N))  ≪_φ  sqrt( (log N)^3 / (N η_N S(N)) )
N η_N S(N) / (log N)^3  → ∞
```

即需要把可用零免宽度提升约 `η_N/η_N^GRH ≍ h²(N)(log N)^4 / S²(N) → ∞`（(2.29)），其中 h(N) 可任意慢增。Hypothesis S/R 正是关于谱乘积 X_N(q) 零点位置的额外断言（(2.28)：S(N;h) ⇔ ‖T_N‖ ≤ S(N)/(2h(N)√(1−η_N))；(2.30)：R(N) ⇔ ‖T_N‖ ≤ δ_N，δ_N² = S(N)(log N)³/N）。**GRH（现在被声称已证）只提供 holomorphy 和 (log N)² 的 baseline，远不足以推出 S/R。**这与 task-4（Li–Liu 审计）和 task-5（热核路线否证）的结论一致。

---

## 4. Lean 工具链实测（time-boxed，真实输出）

### 4.1 先验检查：本机原本没有 Lean

```bash
$ which lean lake elan zstd unzip rg        # 全部为空
(empty above = absent)
$ ls -d ~/.elan 2>/dev/null                 # 空（不存在）
$ ls /opt                                   # 只有 opencode
opencode
$ tar --version | head -1                   # GNU tar 1.35（但系统无 zstd，--zstd 不可用）
$ python3 -c "import zstandard"             # ModuleNotFoundError: No module named 'zstandard'
```

网络（WSL 内）：

```bash
$ getent hosts github.com api.github.com raw.githubusercontent.com
127.0.0.1       github.com
127.0.0.1       api.github.com
127.0.0.1       raw.githubusercontent.com
$ curl -sS -m 10 -o /dev/null -w "mit:%{http_code} %{time_total}s\n" https://math.mit.edu/~drew/grh/
mit:200 1.334682s        # 普通互联网可达；仅 github 系列被劫持
```

Windows 侧 PowerShell（`/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe`）可访问 GitHub API：

```powershell
$ Invoke-RestMethod -Uri 'https://api.github.com/repos/leanprover/lean4/releases/latest'
TAG=v4.36.0
PUBLISHED=2026-11-16T15:45:27Z
ASSET: lean-4.36.0-linux.zip | 946865949 | https://github.com/leanprover/lean4/releases/download/v4.36.0/lean-4.36.0-linux.zip
ASSET: lean-4.36.0-linux.tar.zst | 607649028 | ...  # 需要 zstd，本机没有
...
```

但 **PowerShell 直连 GitHub 下载太慢**：两个文件并行时单个约 93–147 KB/s（实测 03:06:58→03:07:18 由 2,781,184 B → 4,796,416 B，即 ~100 KB/s；947 MB 需 ~2.6 小时，超出时间盒）。改用**国内可用的 GitHub 代理**（WSL 内直连）：

```bash
$ timeout 15 curl -sSL -r 0-20971519 -o /tmp/speedtest.bin \
   "https://gh-proxy.com/https://github.com/leanprover/lean4/releases/download/v4.36.0/lean-4.36.0-linux.zip"
# 代理忽略 Range，15s 内下载 119,566,336 B（≈8 MB/s）
$ # 完整下载（最终版本）：
$ time curl -sSL --retry 3 -o lean-4.36.0-linux.zip \
   "https://gh-proxy.com/https://github.com/leanprover/lean4/releases/download/v4.36.0/lean-4.36.0-linux.zip"
DONE http:200 size:946865949 speed:13200900B/s total:71.727375s
real    1m11.735s
$ sha256sum lean-4.36.0-linux.zip
92a996be487b48e1c2f2985be6b150490475c94d02f5a5e26665a9dab780902a  lean-4.36.0-linux.zip
# 946,865,949 B 与 GitHub API 列出的 asset 大小逐字节一致
```

（备选：`ghproxy.net` 实测被限速（15 s 仅 884 KB），`gh-proxy.com` 可用；`ggfast.top` 不可达；`cdn.jsdelivr.net` 在 WSL 内 TLS 被 reset。最终全部走 `gh-proxy.com`。）

### 4.2 解压与运行

系统无 `zstd`、无 `unzip`；用 `python3 zipfile`（zip asset 946 MB → 3.3 GB，18901 entries，15.6 s），再补可执行位（zip 解压丢 exec 位）：

```bash
$ python3 - <<'EOF'
import zipfile, time
z = zipfile.ZipFile('lean-4.36.0-linux.zip'); z.extractall('lean4')
EOF
entries: 18901, extracted in 15.6s
$ cd lean4/lean-4.36.0-linux
$ chmod -R u+rwX . && chmod u+x bin/lean bin/lake
$ ./bin/lean --version
Lean (version 4.36.0, x86_64-unknown-linux-gnu, commit 611c117bfaf7b7ae1cfcf246ce6fba31e8f509e9, Release)
```

**工具链自举成功，总耗时约 5–6 分钟（下载 72 s + 解压 16 s），远在 25 分钟时间盒内。**

### 4.3 Core-only Lean 检查（无 Mathlib）—— 两个真实通过的文件

> 关键约束：`lean` 发行版自带 `Init`/`Std`/`Lean` 库的 oleans，但**没有 Mathlib**。因此只能检查只依赖 core 的数学。我们选择同时验证两条与 no-go 分析直接相关的引理。

#### (a) `no_go_int.lean` —— ℤ 上正性方向引理（含"可以任意负"）

```lean
theorem positivity_direction_int (c x : Int) :
    (∃ t : Int, 0 ≤ t ∧ x = c - t) ↔ x ≤ c := by
  constructor
  · rintro ⟨t, ht, rfl⟩
    omega
  · intro hx
    exact ⟨c - x, by omega, by omega⟩

theorem positivity_direction_no_upper_bound (c : Int) :
    ∃ t : Int, 0 ≤ t ∧ c - t < 0 := by
  exact ⟨if 0 ≤ c then c + 1 else 1, by omega, by omega⟩
```

真实运行输出（`lean-check/no_go_int.output.txt`）：

```
$ ./lean4/lean-4.36.0-linux/bin/lean check/no_go_int.lean
positivity_direction_int (c x : Int) : (∃ t, 0 ≤ t ∧ x = c - t) ↔ x ≤ c
positivity_direction_no_upper_bound (c : Int) : ∃ t, 0 ≤ t ∧ c - t < 0
'positivity_direction_int' depends on axioms: [propext, Quot.sound]
'positivity_direction_no_upper_bound' depends on axioms: [propext, Quot.sound]
[exit=0]
```

#### (b) `no_go_rat.lean` —— ℚ 上 rank-one 正性方向引理（`v ≠ 0`，`t·v²`）

完整文件见 `lean-check/no_go_rat.lean`（3,123 B，sha256 `88fe18f2…8700`），只 `import Init.Data.Rat.Lemmas`。核心定理：

```lean
theorem positivity_direction_rat (c v : Rat) (hv : v ≠ 0) :
    ∀ x : Rat, (∃ t : Rat, 0 ≤ t ∧ x = c - t * (v * v)) ↔ x ≤ c
```

真实运行输出（`lean-check/no_go_rat.output.txt`）：

```
$ ./lean4/lean-4.36.0-linux/bin/lean check/no_go_rat.lean
positivity_direction_rat (c v : Rat) (hv : v ≠ 0) (x : Rat) : (∃ t, 0 ≤ t ∧ x = c - t * (v * v)) ↔ x ≤ c
'positivity_direction_rat' depends on axioms: [propext, Classical.choice, Quot.sound]
'rat_mul_self_nonneg' depends on axioms: [propext, Classical.choice, Quot.sound]
[exit=0]
```

**解释**：这正是"1 维时 `{c − ⟨Tv,v⟩ : T 自伴, T ≥ 0} = (−∞, c]`"（`v ≠ 0` 时 T 是数乘 t，T ≥ 0 ⇔ t ≥ 0，⟨Tv,v⟩ = t·v²）。它严格地说明：正性（T ≥ 0）只给出上界以外的"下界方向"，不能推出 `G(N) = c_φS(N) − ⟨T_Nv_N,v_N⟩ > 0`。**两条检查都由 Lean 4.36.0 内核真实通过（exit=0），无 sorry（axiom 列表中无 `sorryAx`）。**

**诚实的边界**：
- 我们检查的是 ℝ 上内积空间引理的 **ℚ/ℤ 退化影子**，不是完整版；完整版需要 Mathlib 的 `InnerProductSpace`/`ContinuousLinearMap.IsPositive`，约 100–300 行，本次未做（需要 Mathlib oleans）。
- 未构建 Mathlib（build 需数小时；下载 olean cache ≈ 6–8 GB、还要配 lake 工程，超出 25 分钟时间盒且与"tiny check"目标不符）。
- 未运行 comparator / nanoda 等官方检查（需 ~100 GB RAM、7.7 GB 压缩 export、数小时；本机 15 GiB RAM，且任务明确不重跑 heavy build）。
- 没有做出任何关于"RH export 内核正确"的新判断；该判断只能引用 MIT 页面 + 官方 hash 文件（本报告 §1）。

### 4.4 产物与哈希

| 文件 | 大小 | sha256 |
|---|---|---|
| `lean-check/no_go_int.lean` | 1,546 B | `50d0ce5fdbcca0c7efd74498326a912c270548af40b805f8c33ac7b0583ed017` |
| `lean-check/no_go_rat.lean` | 3,123 B | `88fe18f2e0593e3c4d8466bcc3a030250b53faab92c028520aededc72c618700` |
| `lean-check/no_go_int.output.txt` | 373 B | `e0d86b69…5b9d0c1c` |
| `lean-check/no_go_rat.output.txt` | 351 B | `edc39221…d80ba2c0` |
| `lean-4.36.0-linux.zip`（工具链，Linux FS） | 946,865,949 B | `92a996be487b48e1c2f2985be6b150490475c94d02f5a5e26665a9dab780902a` |
| `mathlib4-src.tar.gz`（survey 用） | 23,413,113 B | `4906567b829fea7e354022c603aeebead7dd2f4ad1a39a91cc42ffae5de46326` |

工具链解压在 `/home/kiler/rh-work/lean-test/lean4/lean-4.36.0-linux/`（3.3 GB）；原始证据在 `/home/kiler/rh-work/lean-test/evidence/`（`mit/`, `mathlib/`, `rh_repo/`, `lean/`）。

---

## 5. 架构检查：Alpöge/Claude 的证明是"谱/热核"还是"自守/正性"？

### 5.1 关键词统计（`grep -rIil` over `/home/kiler/rh-full/src`，175,187 个 .lean 文件；原始日志 `evidence/rh_repo/arch_results.txt`）

| 关键词（正则，不分大小写，per-file 计数） | 命中文件数 | 备注 |
|---|---:|---|
| `thermal` | **0** | 无 |
| `heat`（子串） | 900 | 绝大多数是假阳性：`hEat` 变量、`GlobalTheory.Eat` 谓词、`Chebyshev` 等 |
| `heat[ _-]?kernel\|HeatKernel\|heatKernel` | **13** | 全部在 `Development/AbelianVarietyTheory/Proofs/DivisorProofs/`（+2 个 `PublishedTheorems/Divisors₂`） |
| `heat kernel`（精确短语） | **0** | 代码里是 `IsHeatKernel` 标识符 |
| `HermitianCurvature` | 2,725 | `src/Formalism/HermitianCurvature/` 1,922 个文件为主 |
| `Weil`（词） | 3,216 | 其中 `Siegel[ -]?Weil` 出现在 **6,860** 个文件 |
| `explicit formula`（短语） | 0（但标识符 `ExplicitFormula*` 在 105 个文件里） | 多为接口式陈述，如 `FamilyExplicitFormulaHolds`、`ExplicitFormulaDirichletZerosRightHalf` |
| `Guinand` | **0** | 无 Guinand–Weil 显式公式 |
| `positivity\|Positivity` | 22,707 | 过于泛化（多数为 Lean 的 `positivity` tactic / 命名） |
| `Stepanov` | **0** | 注意：作者 remark 说证明是 Stepanov 式（乘法/theta 链），但仓库中没有任何以 Stepanov 命名的引理 |
| `theta lift\|ThetaLift` | 2,480 | `.../ThetaLifts/...` |
| `spectral\|Spectral` | 3,082 | 泛化；含 `.../DiscreteSeries/LaplaceOperators/SpectralGap/...` |
| `vonMangoldt` | 133 | 含 `Formalism/LandauZeroFreeBounds/ExceptionalZeroBounds/*` |

`HeatKernel` 的 13 个文件中，`IsHeatKernel` 的定义在 `Development/AbelianVarietyTheory/PublishedTheorems/Divisors₂/IsTorsionFormPoint.lean:93`，类型是
`(b : E) → (u : ℝ) → (D : Set (Fl g)) → (K : ℝ → (Fin g → ℂ) → (Fin g → ℂ) → Ext (n+n+g) →L[ℂ] Ext (n+n+g)) → Prop`，
即 Abel 簇/周期域上除子理论用的核（`ContDiffOn … ∧` 平移/周期性条件），**与 RH 的谱/热核迹正性无关**；其使用样例 `integrableOn_strN_heatKernel_diag`、`HeatKernelTraceIntegrable.lean` 都是 `GlobalTheory` 下的技术引理。

### 5.2 import 闭包：几乎所有模块都在主定理闭包里

用 Python 解析全部 175,187 个 `.lean` 文件的 `^import`（含 `public import`），以 `Main`, `Statements`, `Supplements.Kernels.MainTheoremsAll` 及 `MainTheorems` 直接 import 的三个模块为根做 BFS：

```
indexed 175187 lean files, 175187 modules
CLOSURE size = 175184 modules of 175187          # 99.998%
by top dir: Development 141925, Formalism 18254, GroundTheory 8507,
            ReciprocityTheory 3845, CompanionTheory 2027, PositivityTheory 449,
            Lemmata 167, BuildAid 5, Supplements 3, Main 1, Statements 1
HeatKernel:        in-closure=4  (4 个模块名含 HeatKernel)
HermitianCurvature: in-closure=1923 (全部)
WeilBound:         in-closure=7051 (全部)
PositivityTheory:  in-closure=449 (全部)
ThetaLift:         in-closure=1321
ExplicitFormula:   in-closure=63
Stepanov:          in-closure=0
Guinand:           in-closure=0
```

即：这个 17.4M 行的巨型库**没有"装饰性填充区"可分**——从 `Main` 出发几乎能到达所有模块（AI 生成/接口化的 import 网络）。主链本身很短：

```
src/Main.lean
  import Statements
  import Supplements.Kernels.MainTheoremsAll
    import Supplements.Kernels.MainTheoremsCritical
    import Development.AutomorphicArithmetic.AutomorphicVarieties.SmallClassNumbers.CorGKOf
theorem riemannHypothesis : RiemannHypothesis := rhOfAll
  -- Supplements.Kernels.MainTheorems.lean:
  --   import Formalism.GammaFactorNonvanishing.CritLine
  --   import Development.AutomorphicArithmetic.CharacterBoxes.ClaimStrip
  --   import Development.AutomorphicArithmetic.CharacterBoxes.MainConclusion
  --   allChi := UpperTheory.FinalTheorems.everyCharacter
  --   rhOfAll := Formalism.VW.rh_of_every allChi
  --   critAll := Formalism.VW.critLine allChi ...
  --   claimAll := ⟨allChi, Claim.strip allChi, Claim.zeta allChi⟩
```

关键定义（`Development/AutomorphicArithmetic/CharacterBoxes/EveryCharacter.lean:13`，与 Mathlib 的 GRH 陈述直接挂钩）：

```lean
def UpperTheory.EveryCharacter : Prop :=
  ∀ (N : ℕ) [NeZero N] (χ : DirichletCharacter ℂ N) (s : ℂ),
    1 / 2 < s.re → (χ ≠ 1 ∨ s ≠ 1) → DirichletCharacter.LFunction χ s ≠ 0
```

主结论 `UpperTheory.FinalTheorems.everyCharacter` 由 `CharacterBoxes/MainConclusion.lean` 给出，依赖 `Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.EveryCharacterOfLiteratureOfVWin`、`AutomorphicVarieties.ModularityArgument.ThresholdArguments.DenseThresholdCases.VwinOfRow`、`Foundations.LocalLanglands.LocalCentralUnits.RecTExists`、`Foundations.GaloisRepresentations.IntegralStructures.RowSrc` 等 —— **theta 提升 / 局部 Langlands / Galois 表示 / 自守形式**；`Formalism/GammaFactorNonvanishing/CritLine.lean` 才是把 `EveryCharacter` 转成 `RiemannHypothesis` 的短链（`gammaFactor_ne_zero`、`critLine`、`rh_of_every`，各 10–30 行）。

### 5.3 判定

- **不是 heat-kernel/spectral-trace 架构**：`thermal`=0，热核词汇只在 13 个 Abel 簇除子理论文件里（0.0074%），没有"热核迹正性"作为 RH 证明的步骤。
- **是 automorphic/positivity 型**：Siegel–Weil 公式（6,860 文件）、theta lifts（2,480）、局部/全局 Langlands、Galois 表示、HermitianCurvature（2,725）、PositivityTheory（449）构成主体；与作者 remark 中"chaining theta lifts / Stepanov 的后代 / 原生自守方式"的描述吻合（`Stepanov` 字样为 0，属命名层面缺失）。
- **对用户前提的意义**："黎曼猜想的谱证明架构能'必然蕴含'哥德巴赫，其关键一步是热核迹正性"这一前提，与**这个** RH 证明的实际架构不符：该证明没有任何谱/热核迹正性步骤可作为通往 Goldbach 的桥梁；而 task-5 已独立证明，即便存在这样的正性，系数提取与算子范数上界的方向也不支持 Goldbach（见 §3.2 的引理）。

---

## 6. 总判定：这个环境能产出什么 Lean 验证产物？

### 6.1 可以（且已经）产出的

| 可产出 | 状态 | 证据 |
|---|---|---|
| 工具链（Lean 4.36.0 官方 linux release，本机可跑） | **完成** | §4.2、`lean --version` |
| 与 no-go 分析直接相关的最小 standalone 引理（ℤ/ℚ rank-one 正性方向） | **完成、exit=0、无 sorry** | §4.3、`lean-check/` |
| 完整 ℝ-内积空间版正性方向引理（Mathlib，约 100–300 行） | **未做，可做**（需 Mathlib olean cache ≈ 6–8 GB；估 1–2 周） | — |
| "生成函数正性 ⇏ 系数正性"的 Real.exp 反例（Mathlib，约 50–150 行） | **未做，可做**（1–3 天） | — |
| Mathlib 对 Goldbach 猜想的形式化 | **不存在**；若要建，仅陈述+定义约 1–2 天，但**证明**是千年级问题 | §2.2 |

### 6.2 不能产出的

- **任何"RH/GRH ⇒ Goldbach"的 Lean 定理**：Mathlib 里没有 Goldbach 陈述、没有 Li–Liu 链的任何 ingredient（Hardy 空间、Hilbert–Schmidt、奇异级数、四元数解析、显式公式等均缺失），且该蕴含关系本身在文献中被认为是错误的（GRH 给不了 minor arcs / parity barrier；见 task-3 报告）。
- **对 RH 证明的独立 kernel 复检**：官方 `lake comparator` + Lean default/paranoid kernel replay 仍在 running；本机 15 GiB RAM 远低于页面要求的 ~100 GB RAM / ~70 GB 磁盘 / 数小时单线程。
- **完整的 Li–Liu 链形式化**：约 10 万–30 万行新 Lean、60–160 人月【推测】，超出任何单次任务。即使只做 "Hypothesis S ⇒ Goldbach 渐近" 的条件版本，仍需要上表第 1–11 项的绝大部分（约 8 万–25 万行；50–130 人月），因为 S 只是"输入假设"，不是形式化捷径 —— 从带权计数到二素数表示、以及 S/R 与谱乘积零点字典的全部中间步骤都必须形式化。

### 6.3 "Hypothesis S ⇒ Goldbach 渐近"的 Lean 定理需要什么（清单）

1. **Goldbach 陈述本身**：`Nat.Goldbach` / `∀ n, Even n → 4 ≤ n → ∃ p q, p.Prime ∧ q.Prime ∧ p+q = n`（Mathlib 无，需自建；约 1–2 天）。
2. **Li–Liu 的有限投影/特征正交/Mellin 反演链**（§3.1 第 1–3 项）。
3. **Hardy 空间 H² 条带 + 边界迹 + Fourier–Laplace 表示**（Mathlib 完全缺失；最大单块之一）。
4. **Hilbert–Schmidt 算子/核理论 + 紧自伴谱定理**（谱定理有，HS 部分需自建）。
5. **四元数 slice-regular 谱乘积 X_N(q) 与零点分类**（缺失）。
6. **GRH-条件的 L′/L 估计与零免区**（Mathlib 只有 L 函数解析延拓/非零；显式公式、对数导数均值、零点计数缺失；最大块）。
7. **奇异级数/局部密度、von Mangoldt 带权和、素数幂去除、误差项与 N-均匀性**。
8. **把 Hypothesis S/R 作为显式假设参数化**（如 `(hS : ∀ᶠ N in atTop, S(N; h))`），并证明 `S(N;h) → G(N) = c_φS(N) + O_φ(S(N)/h(N))`（论文 (2.28)）——需要上述 6+7 的定量估计。
9. 若要做"无条件"版本，还必须**证明 S/R**（论文未证；GRH 不够，见 §3.3），或把它们作为 axiom —— 但那就不再是"证明 Goldbach"，只是条件定理。

**现实的时间估计【推测】**：即使假设论文数学正确且已有 Mathlib olean cache、由 1–2 名 Lean 专家 + AI 辅助全职推进，完成"Li–Liu 全链形式化"也要 **5–13 人年**；只做 §6.3 的"条件定理 + 最小依赖"也需 **约 3–8 人年**。单次 25 分钟/本次任务预算内，能诚实交付的只有 §6.1 的前两行。

---

## 7. 证据索引（可复跑）

- MIT 页面与校验文件：`/home/kiler/rh-work/lean-test/evidence/mit/`
  - `grh_page_2026-11-21T0315Z.html`（sha256 `de7153ec…62307`）
  - `grh_page_text_2026-11-21T0315Z.txt`（提取文本，233 行）
  - `final_audit.log`、`final_comparator.json`、`final_SHA256SUMS`、`final_nanoda.log`
- Mathlib 调查：`/home/kiler/rh-work/lean-test/evidence/mathlib/`
  - `goldbach_and_rh_search.txt`（命令 + Goldbach 搜索结果 + RiemannHypothesis 定义）
  - `ingredient_paths.txt`（素数计数/L 函数/复分析/算子理论文件清单）
  - 源码树：`/home/kiler/rh-work/lean-test/mathlib4-src/`（commit 0df444a3，8,852 .lean）
- RH 仓库：`/home/kiler/rh-work/lean-test/evidence/rh_repo/`
  - `rh_full_counts.txt`（commit/计数/行数命令输出）
  - `arch_results.txt`（关键词 grep 原始日志）
  - `closure_modules.txt`（175,184 个主定理闭包模块清单，5.4 MB）
  - `architecture_summary.txt`（补充计数）
- Lean 工具链与检查：`/home/kiler/rh-work/lean-test/evidence/lean/`
  - `toolchain.txt`（lean --version + zip/tarball sha256）
  - `no_go_int.output.txt`、`no_go_rat.output.txt`
- 交付目录：`/home/kiler/Windows-D/Rieman/_rh-work/goldbach-attack/lean-check/`（两个 `.lean` 与输出，可直接用 `lean` 复跑）
- 复跑命令（工具链仍在）：
  ```bash
  cd /home/kiler/rh-work/lean-test
  ./lean4/lean-4.36.0-linux/bin/lean check/no_go_int.lean   # 期望 exit=0，无错误输出
  ./lean4/lean-4.36.0-linux/bin/lean check/no_go_rat.lean   # 期望 exit=0，无错误输出
  ```
  （`lean` 对无错误文件默认静默；本报告的 output 文件里看到的两行 `#check` 与 `depends on axioms` 来自文件末尾的 `#check`/`#print axioms` 命令，是有意保留的自证。）

---

## 8. 与其他任务/报告的关系

- 本报告的 §1（RH 状态）与 task-1（repo forensics）/task-2（proof digest）交叉印证：镜像 commit/计数/行数一致；官方页面仍有两项 running。
- 本报告的 §3.3（GRH 不够）与 **task-4（Li–Liu 审计）**、**task-5（热核路线否证）** 的结论一致：RH/GRH 已证不改变 "S/R 未被证明、且不能由 GRH 推出" 这一事实；No-go 引理（§3.2）是 task-5 两条严格引理之一的 Lean 化影子。
- 本报告的 §5 直接回应用户"谱证明架构 ⇒ Goldbach / 热核迹正性"的前提：**该前提与 Alpöge/Claude 证明的实际架构不符**，且热核正性在数学上也不能给出 Goldbach 所需方向（§3.2、§4.3）。
