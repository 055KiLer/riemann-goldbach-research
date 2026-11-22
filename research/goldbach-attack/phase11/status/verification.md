# Phase-11 状态复核：官方 RH 验证仍未完成；上游无变化；量化内容需修正旧结论

- 任务：team task-41（Phase-11 status，repo-verifier，仅报告、无重编译）。
- 检查窗口：**2026-11-21 15:09–15:49 UTC（= 23:09–23:49 CST）**。
- 基线：phase6 报告 `_rh-work/goldbach-attack/phase6/mit-recheck/report.md`（2026-11-21 11:17–11:31 UTC）。
- 证据目录：`_rh-work/goldbach-attack/phase11/status/{mit,gh,news,arxiv,logs}`；本报告所有 URL/时间戳均为实抓。

---

## 0. 六行摘要

1. **官方验证仍未完成**：MIT 页 `last updated 2026-11-21 12:55 UTC`（比 09:30 UTC 版更新，但只是文字扩充/scope 说明；检查表逐行未变），**仍 3 项 running**：主证明 Lean default+paranoid kernel replay、主证明 lake comparator、组合算术导出 lake comparator。无 `paranoid.log`/`comparator.log`（404）；`SHA256SUMS` 自 09:21:33 GMT 未变；无新产物。
2. **上游无变化**：本地 `/home/kiler/rh-full` HEAD = `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`（2026-11-20T15:13:33Z），dirty=0；GitHub `CocoSgt/riemann-hypothesis-lean` `pushed_at 2026-11-20T15:13:36Z`，仅 1 个 release（v2026-11-20，2026-11-20T15:05:56Z），README sha256 与本地相同 → **2026-11-20 22:05 UTC 之后无新 commit/release/README**。`alpo.ge` 主页 11,625 B 无 RH/Lean/Claude 关键词；`remark.pdf` sha256 `3fc97784…` 未变；新抓 part01 sha256 `86974b1c…` 与已存分片**完全相同**（档案未变）；无 reader's-guide 类新文件（该服务器对任意路径回退 homepage HTML）。
3. **量化内容：旧结论"无量化内容"需要修正为"最终定理是定性的，但档案内部含大量量化解析数论机器（且以 theorem 形式给出）"**：Siegel 下界（`siegelLower : SiegelLower`）、Siegel–Walfisz（`siegelWalfisz : SiegelWalfisz`）、Dirichlet L 零自由区（`zFRDirichlet : ZFRDirichlet`）、ζ 经典零自由区（`zeroFreeRegion : ZeroFreeRegion`）、显式公式带显式误差常数（`ExplZeta`/`ExplChi`）、L'/L 上界（`LogDerOne`）、零点计数（`ZeroCount`）、零密度盒（`ZeroDensityBox`/`ZeroDensityBound`）、GL3 均方（`GL3MeanSquares` 目录）。但**无 pair correlation（0 命中）、无 ζ/L 的 moments、无 ratios conjecture、无 L 函数 family averages**；最终公开输出只有定性 RH/GRH + MIT 页所列 Robin/Lagarias 不等式。
4. **批评/新闻**：PhilArchive Nielsen "Invalidity of the Alpoge Proposed Proof" 仍 **403 不可读**（rec/PDF/philpapers 全部 403）；另检索到 Nielsen 的 "Invalidity of Masullo's Proof" 及另一篇 "A Formal Completed Proof That the RH Has One Address…"——说明该平台有未审阅 RH 上传，均不能作为有效批评/证据。**Lean 社区博客 "Lean verification of the Riemann Hypothesis"**（`https://leanprover-community.github.io/blog/posts/riemann-hypothesis/`）存在但本轮 WSL/Windows/web_fetch 三路抓取均失败（github.io 被重置/超时），未能读取——建议有访问权限者补读。Tao 博客无新帖（同一 2026-11-20 帖，评论数 31→61）。
5. **预印本更新**：`arXiv:2611.18825`（Gou–Wang–Xu, *Landau's problems through ratios of L-functions*）**仍 v1 单版本**（2026-11-13T18:55:46Z，46 页），无更新/撤回；`arXiv:2610.32672`（SeungJu Lee）**v2**（v1 2026-10-23，v2 2026-11-03T12:27:02Z，16 页；注释称覆盖所有固定正偶数间隔、弱化 ratios 假设、改进误差），无 v3。**Li–Liu  preprint 未能定位**（arXiv 作者/日期查询无匹配；检索到的 "Failure of the Li-Liu spectral hypothesis R under Dirichlet GRH" 挂在 hexagonmath.org/pdf/2611.00788v1，而 arXiv 2611.00788 实为无关 ML 论文 → 该 hexagonmath 文档不是 arXiv 论文，疑为不可靠来源，不能作为 Li–Liu 更新依据）。`arXiv au:Alpoge` 最近条目为 2026-09-15，无 2026-11-20 后新预印本。
6. **不能宣称**：官方 comparator/paranoid replay 完成、peer review、独立证实"数学正确"。当前可说的最强表述：MIT 页（12:55 UTC 版）显示官方验证"仅余 3 项 running"，且 Comparator 流水线已在 Robin1984 上端到端通过；主证明导出仍未被官方 comparator/Lean paranoid kernel 宣布通过。

---

## 1. 时间戳事实表

| UTC 时间 | 事实 | 来源/证据 |
|---|---|---|
| 2026-11-20 15:13:33 | 本地镜像/上游最后 commit `7cbf7a0c32`（README） | `git -C /home/kiler/rh-full log -1`；GitHub API cocosgt_commits.json |
| 2026-11-20 19:39:50 | MIT `audit.log`/`comparator.json`/`project-oleans.sha256` Last-Modified（至今未变） | `mit/hdr_*.txt` |
| 2026-11-21 09:21:33 | MIT 现 `SHA256SUMS` Last-Modified（2,112 B；sha256 `a26d92ed…`），此后未变 | `mit/hdr_SHA256SUMS.txt` |
| 2026-11-21 09:30 | MIT 页上一版 last-updated（新增 Arithmetic consequences 等） | phase6 报告 |
| **2026-11-21 12:55** | **MIT 页当前版本 last-updated**：18,423→**20,460 B**，sha256 **`e46488825acc7e4fbf3c0c744edcfaa5219f773571a9267b06df26b11f18a1a3`**；仅扩充 "What was verified"（五定理逐条+scope 段）并删除旧"first build wrong module root"caveat；**检查表逐行相同** | `mit/index.html`、`mit/page_text.txt`、diff vs phase6 |
| **2026-11-21 15:09:07** | 我方实抓 MIT 页；页面自述 "Page last updated 2026-11-21 12:55 UTC"；仍 **3 running**（原文：Lean default+paranoid on export "single-threaded; no verdict yet"；lake comparator "statement comparison and axiom check already passed in one run; kernels in progress"；组合导出 lake comparator "expected to take many hours"） | 实抓 |
| 2026-11-21 15:09:11 | `paranoid.log` HTTP **404**；无 `comparator.log`；页面链接集合与 phase6 完全相同 | 实抓 |
| 2026-11-21 15:00:01 | `leanprover-community/riemann-hypothesis` pushed_at；最新 commit `2f097b744a` 14:14:13Z；`verification/` 仍仅 `CACHE.md/CI-RUNNERS.md/NOTES.md/static-scan.txt`（无 comparator 结果）；NOTES.md 与 phase6 逐字节相同（diff 空） | GitHub API gh/*.json |
| 2026-11-21 15:12:45 | `alpo.ge` 主页 11,625 B；关键词 0；`remark.pdf` 245,114 B sha256 `3fc97784b71ddd44ff8aa0a177e99622a1c61b13cfa843a0989ee4a7a0cfeb8d`（未变）；fresh part01 sha256 `86974b1c…` = 旧存档（未变）；part15/guide.pdf 等均回退 homepage HTML | news/alpo_index.html、news/remark.pdf、news/part01_fresh.bin |
| 2026-11-21 15:20 | arXiv API：2611.18825 v1 2026-11-13T18:55:46Z；2610.32672 v2 2026-11-03T12:27:02Z；均无新版本 | arxiv/api_ids.xml、arxiv/abs_*.html |
| 2026-11-21 15:31 | Tao 博客仍只有 2026-11-20T17:19:00Z 那篇（评论数 61） | news/tao_home.html |
| 2026-11-21 15:40 | PhilArchive/PhilPapers 全路径仍 403；hexagonmath 2611.00788v1 = 非 arXiv 文档 | news/hexagon_li.html 等 |

---

## 2. 官方验证状态（详细）

**未完成。** 依据 2026-11-21 15:09 UTC 实抓的 12:55 UTC 版页面：

- 表格 **16 pass / 3 accepts 状态行 / 3 match / 1 declined / 1 n/a / 3 running**；running 三项见 §1 表，原文未变；页面 Summary 仍写 "The lake comparator run and the Lean-kernel replay of the export are still in progress."
- 主证明已完成项（自 2026-11-20/21）：175,187 模块编译 pass；`#print axioms` 仅 `propext/Classical.choice/Quot.sound`；环境 15 axioms 全在 Init；Mathlib 缓存逐字节一致；leanchecker 175,187/175,187；challenge 导出 sha `bd484ac9…` match；nanoda accept（2026-11-20 19:05:45）；con-leche 1,468,418 decls accept（21:19:04）；con-leche --compare 5 定理 justified（21:19:12）；lean4lean 175,187/175,187。
- 新版本（12:55 UTC）**新增文字澄清**：五条定理由 challenge 文件原样列出；新增 scope 段原文："**Scope. 'GRH' here means Dirichlet L-functions: all moduli and all characters. Dedekind zeta functions, Hecke L-functions and automorphic L-functions in general are not among the statements that were checked.**"；删除了 "A first build attempt used a wrong module root…" caveat；**无任何检查行状态变化**。
- 自 09:30 UTC 版以来约 3.5 小时无新检查结果；自首次发布（2026-11-20 22:05 UTC）已约 **17 小时**，官方 comparator/paranoid replay 仍未宣布完成。
- 已知可用的判题证据仍只有：Robin1984 上的完整 Comparator 流水线（v4.33.0 "Your solution is okay!" exit 0 @ 03:31:06 UTC；lake comparator v4.36.0 三 kernel accept @ 04:16:52 UTC）与组合算术包的 con-leche/nanoda 通过；**主证明导出本身未通过这些最终 checker**。

## 3. 上游/档案状态（详细）

- 本地 `/home/kiler/rh-full`：HEAD `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`，`git status --porcelain`=0（计数 175,192 tracked / 175,187 .lean / 17,374,215 行与此前一致，未做重扫改动）。
- `github.com/CocoSgt/riemann-hypothesis-lean`：`pushed_at 2026-11-20T15:13:36Z`、`updated_at 2026-11-21T15:01:12Z`（仅 star 元数据）、407 stars/65 forks；commits 最新 = `7cbf7a0c32`；releases = 1 个（`v2026-11-20`，2026-11-20T15:05:56Z）；README sha256 `2c613919744434c3499c5f75c8019f5686673bc85e2487189f619ca76980cf89` = 本地 README。→ **无更新**。
- `alpo.ge`：主页内容与 2026-11-21 早间完全相同（11,625 B；无 RH/Lean/Claude/remark/GRH/guide 关键词）；`remark.pdf` 未变（sha256 `3fc97784…`）；`lean.tar.gz.part01` 新鲜下载 sha256 `86974b1c242ca7b6748f3299df4fc64ee0f6e06c776ac964fb64888101a3de77` = 此前存档分片；part14 ETag `8a60f30a…`，part15 不存在（回退 HTML）。→ **档案与 note 均未变，无新 reader's guide**。
- `github.com/leanprover-community/riemann-hypothesis`（原 Deicyde）：`pushed_at 2026-11-21T15:00:01Z`（CI 基础设施活跃：14:14Z "ci-runner doctor: report vm.max_map_count…" 等）；`verification/` 仍 4 个文件，**无 comparator 输出**；NOTES.md 与 11:18 UTC 抓取版本 byte-identical。

## 4. 量化内容（用 file:line 证据重核，修正旧结论）

**旧结论需修正**：此前"证明无量化内容"应改为：**最终定理是定性 RH/GRH（无零区域宽度、无误差项、无 moments 等定量结论），但档案内部含大量以 theorem 证明的定量解析数论机器**，作为中间步骤（均非 axiom/sorry；依赖 MIT kernel 检查）。证据（均在 `/home/kiler/rh-full`）：

| 类别 | 证据（文件:行 + 命题） |
|---|---|
| ζ 经典零自由区 | `src/Formalism/ZeroFreeRegion/FinalZFR.lean:17` `theorem zeroFreeRegion : ZeroFreeRegion := classicalZeroFreeRegionOfBounds …` |
| Dirichlet L 零自由区（显式形如 `1 - c/log(q(|im|+2))`） | `src/Formalism/LandauZeroFreeBounds/Statement.lean:8-14` `def InRegion`/`def ZFRDirichlet : Prop`；`NoZeroComplex.lean:20,23,26,29,32` `theorem noZeroComplex/realLargeT/realSmallT/twoReal : …`、**`theorem zFRDirichlet : ZFRDirichlet`** |
| Siegel 下界 | `src/Formalism/LandauZeroFreeBounds/FinalSiegel.lean:14,17` `bqKey : BqKey`、**`siegelLower : SiegelLower`**；`SiegelWalfiszAP.lean:29-31` `def SiegelLower := ∀ ε>0, ∃ c>0, ∀ q χ real nonprincipal, c q^{-ε} ≤ ‖L χ 1‖` |
| Siegel–Walfisz（含 AP/素数字比例） | `SiegelWalfiszAP.lean:33-36` `def SiegelWalfisz`；`:38-41` `def SiegelWalfiszAP`；`:43-47` `def PrimeShareSW`；`SiegelWalfiszAPOfSiegelLower.lean:29,34` **`theorem siegelWalfisz : SiegelWalfisz := siegelWalfisz_of_siegelLower siegelLower`** |
| 显式公式（显式误差常数） | `src/Development/AbelianVarietyTheory/PublishedTheorems/AutomorphicForms₂/ExplZeta.lean:12` `def ExplZeta : Prop := ∃ C, ∀ x T ≥2, ‖ψ(x)-x+Σ_ρ x^ρ/ρ+…‖ ≤ C(log x + x/T log(xT)^2)`；`ExplChi.lean:12` 同型（Dirichlet L）；另有 `src/Formalism/PeriodIntegrals/ExplicitFormula.lean:16,26` `def ExplicitFormulaWith (C)`、`def ExplicitFormula := ∃ C>0, ExplicitFormulaWith C` |
| L'/L 上界 | `…/AutomorphicForms₂/LogDerOne.lean:12` `def LogDerOne := ∃ C, ∀ q χ primitive, ‖L'/L(χ,1) - Σ_ρ 1/(1-ρ)‖ ≤ C log(3q)`；`src/Formalism/ZetaNonvanishing/LogDerivZeroFree.lean:9` `theorem logDerivZeroFree : LogDerivZeroFree`（def: `ZetaRealNonvanish.lean:76`） |
| 零点计数 | `…/AutomorphicForms₂/ZeroCount.lean:12` `def ZeroCount := ∃ C, ∀ q χ primitive t, zsumR χ t 1 (fun _=>1) ≤ C log(q(|t|+2))` |
| 零密度 | `src/Formalism/GL3MeanSquares/GenusMeanAsymptotics/JacobiCharacterSums/CountSt.lean:7` `def ZeroDensityBox`；`CountZAll.lean:13` `theorem zero_density_box : …ZeroDensityBox`；`src/Formalism/GL3MeanSquares/SmoothedRemainderRealIntegralFormula.lean:81` `def ZeroDensityBound (σ Q)` |
| 均方（Rankin–Selberg / GL3） | `src/Development/AbelianVarietyTheory/Proofs/FoundationProofs/RankinMeanSquareCuspForm.lean:138` `theorem rankin_mean_square : …∧ ∃ C, …∑' ‖h n‖²/n^{k+s} …`；目录 `src/Formalism/GL3MeanSquares/`（含 `…/MeanSquareOfPrimeNumberTheorem.lean`、`NumericalZeroDensityBound.lean`、`HookFormulaTorsion/` 等） |
| **未发现** | pair correlation：0 命中；L 函数 moments（"second/first moment" 0 命中，moment 命中均为代数/测度语境，如 BehrendVariance/Fock space）；ratios conjecture：0 命中；L 函数 family averages：仅 6 个 automorphic "compact family average" 文件，非解析 family average |
| 最终公开"算术后果" | MIT 页 12:55 版 "Arithmetic consequences"：`robin_inequality`（σ(n) < e^γ n loglog n, n>5040）与 `lagarias_inequality`（σ(n) ≤ H_n + exp(H_n) log H_n, n≥1），由 RH 证明 + `kimihiro64/Robin1984`（acab1a3）组合得到；组合导出 sha256 `44651dcc…`；两条定理 `#print axioms` 仅 3 标准 axiom；组合导出 con-leche/nanoda accept，lake comparator 组合导出仍 running |

**量化内容结论**：档案内部**确有**强定量机器（Siegel、Siegel–Walfisz、ZFR、显式公式、L'/L、零点计数、零密度、均方），但 (a) 都是经典结果的形式化/中间步骤，未见超出经典的"新定量定理"作为公开主张；(b) 公开的最终结论仍是定性 RH/GRH，加上 Robin/Lagarias 不等式；(c) 无 pair correlation/moments/ratios/family averages。因此"RH 证明可推出新的定量零点分布结论"这一说法**不应支持**；但"档案完全没有量化内容"也**不成立**。

## 5. 批评 / 新闻（自 2026-11-21 08:00 UTC）

- **PhilArchive Nielsen "Invalidity of the Alpoge Proposed Proof"**：`https://philarchive.org/rec/NIEIOT-2` 及 `https://philpapers.org/archive/NIEIOT-2.pdf`、`/rec/NIEIOT-2` 本轮 15:37–15:40 UTC 实抓**全部 HTTP 403**（Cloudflare），正文/摘要仍不可得 → **不能当作有效反证，也不能忽略**（未验证、未审阅）。
- 检索同时出现：`Jenny Lorraine Nielsen, "Invalidity of Masullo's Proof of the Riemann Hypothesis"`（philarchive NIEIOM）与 `"A Formal Completed Proof That the Riemann Hypothesis Has One Address and Not a Sequence of Missing Pieces"`（philarchive ISLAFC-2）→ 表明 PhilArchive 上有多个未经审阅的 RH 相关上传，引用需极度谨慎。
- **Lean 社区博客** `https://leanprover-community.github.io/blog/posts/riemann-hypothesis/`（标题 "Lean verification of the Riemann Hypothesis"）在搜索结果中出现，但本轮 **WSL curl（TLS reset）、Windows PowerShell（超时）、web_fetch（fetch failed）三路均无法读取** → 未能确认其内容/日期；建议 Lead 或有人工浏览器者补读（这是本轮唯一可能改变"官方状态"叙事的未读来源）。
- **Tao 博客**：无新帖；2026-11-20T17:19:00Z 的帖子仍在，评论数由 31 → **61**（15:31 UTC 抓取），正文无更新（仍"digestion 需要时间"）。
- SciAm：未再抓（前次 2026-11-20T21:47:41Z 后无更新证据）；未见任何媒体/机构宣布"验证完成"。
- 未发现 errata/retraction/peer-review 声明。

## 6. 预印本更新

| 预印本 | 状态（2026-11-21 15:20–15:45 UTC 查询） |
|---|---|
| `arXiv:2611.18825` Gou–Wang–Xu, *Landau's problems through ratios of L-functions* | **v1 only**，2026-11-13T18:55:46Z，46 页，math.NT；无新版本/无撤回/无新 comments |
| `arXiv:2610.32672` SeungJu Lee, *The Hardy–Littlewood asymptotic for prime pairs of fixed even difference from a uniform zeta-ratios conjecture* | **v2**（v1 2026-10-23T14:14:23Z；v2 2026-11-03T12:27:02Z），16 页；comment："The result now covers all fixed positive even gaps. We also weaken the ratios assumption and improve the error bounds"；**无 v3** |
| Li–Liu preprint（Lead 提到的 2026-11-13 三篇之一） | **未能定位 arXiv ID**：arXiv API 按 Li+Liu+日期窗口 0 条；检索到的 "Failure of the Li-Liu spectral hypothesis R under Dirichlet GRH" 位于 `hexagonmath.org/pdf/2611.00788v1`（238 KB PDF；该 ID 在 arXiv 对应无关 ML 论文，故 hexagonmath 文档**不是** arXiv 记录）→ 需 Lead 提供 Li–Liu 的 arXiv ID；该 hexagonmath 项暂按不可靠来源处理，不作为更新依据 |
| Alpöge 本人 arXiv | `au:Alpoge` 最新为 2026-09-15（另有 2026-08-13 v2 "More than two thirds of the zeta zeros are simple and on the critical line"）；**无 2026-11-20 之后新预印本** |

## 7. 局限

- 未重编译/未重跑 kernel；全部"证明成立"证据转述 MIT 页面与其日志（sha256 已核的小文件）。
- MIT index 无 `Last-Modified`，版本靠内容 sha256/自述（本次 `e4648882…`，20,460 B）。
- `SHA256SUMS` 未随 12:55 页面文字更新（仍 09:21:33 版），但页面 12:55 版未新增/修改任何下载产物（链接集合相同），故不构成缺失。
- Lean 社区博客、PhilArchive 正文不可读；hexagonmath 来源不可靠；36kr/Reddit/HN/MathOverflow/Zulip 未能逐一深读（未发现可引用新表态）。
- 未下载 7.7GB `solution.ndjson.zst` / 47MB `challenge.ndjson.zst` 等大文件；未复核导出级 hash。
