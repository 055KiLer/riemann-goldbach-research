# Phase-6 recheck：MIT GRH 验证页已更新（2026-11-21 09:30 UTC）——官方验证仍未完成

- 任务：team task-27（Phase-6 quick recheck）。执行者：repo-verifier。写入范围：本目录。
- **本次检查时刻：2026-11-21 11:17:47–11:31 UTC（= 19:17–19:31 CST）**。
- 基线：phase5 报告 `_rh-work/goldbach-attack/phase5/mit-recheck/report.md`（2026-11-21 08:00–08:12 UTC）。
- 证据：`mit/`（新页面+新产物+headers）、`gh/`（GitHub 最新 NOTES/commits/runs）、`news/`（tao/sciam/tsnmedia/zenodo/bing/philarchive 尝试）、`alpo/`、`*.ps1`。

---

## 0. 结论（一句话）

**MIT 页面在 2026-11-21 09:30 UTC 有了实质性更新**（上一版为 2026-11-20 22:05 UTC，间隔 **11 小时 25 分**；我方 11:17 UTC 抓取时距新版 **1 小时 47 分**）。新增了 **"Arithmetic consequences"**（与 Robin1984 组合得到 Robin/Lagarias 不等式的无假设定理性）以及一整套新通过的检查，其中 **完整 Comparator 流水线已在 Robin1984 上端到端跑通**（"Your solution is okay!"，exit 0）。

但**主证明（RH）的官方验证仍未完成**：页面仍有 **3 项 running**——(a) 主证明导出文件的 Lean default+paranoid kernel replay；(b) 主证明的 lake comparator end-to-end；(c) 组合算术导出（61.75 GB）的 lake comparator kernel 阶段（页面明说单线程、"expected to take many hours"）。**没有任何"官方验证完成"的宣告**；无 peer review/errata；`alpo.ge` 无新 note；Tao 博客无新帖；SciAm 未更新；社区 Comparator 仓库的 `verification/` 仍无结果文件。

PhilArchive 上声称 "Invalidity…" 的记录（Nielsen）**仍然无法读取**（所有路径 403 / 超时），但这轮检索**首次拿到其 PDF 的直链** `https://philpapers.org/archive/NIEIOT-2.pdf`（同样被 Cloudflare 403）。仍属未验证、不可评估的质疑记录。

---

## 1. MIT 页面：新版内容与逐项状态（2026-11-21 09:30 UTC）

### 1.1 版本/哈希/时间戳

| 项 | 旧（2026-11-20 22:05 UTC） | 新（2026-11-21 09:30 UTC） |
|---|---|---|
| `index.html` | 12,782 B，sha256 `de7153ec…2307` | **18,423 B，sha256 `9f07d2d87d29ef12ce5221397b5594ce9ff7295e21e545e97798d8cfdd83f74b`** |
| `SHA256SUMS` | 1,291 B，sha256 `d8496902…` | **2,112 B**，Last-Modified **2026-11-21 09:21:33 GMT** |
| `audit.log` / `comparator.json` / `project-oleans.sha256` | 20 Nov 19:39:50 GMT | 未变（Last-Modified 同前） |
| 页面自述 | "Page last updated 2026-11-20 22:05 UTC" | **"Page last updated 2026-11-21 09:30 UTC. Results below are as of that time and this page will be updated as the remaining checks finish."** |
| 状态计数 | 4 accepts / 2 match / 10 pass / 2 running | **10 accepts / 3 match / 16 pass / 3 running** / 1 declined / 1 n/a |

我方抓取：`Date: Sat, 21 Nov 2026 11:17:52 GMT`（index）、11:17:54（SHA256SUMS）。**新下载的 17 个新增/更新小文件全部通过新 `SHA256SUMS` 校验（OK）**；未下载的是 `solution.ndjson.zst`（7.7GB）、`challenge.ndjson.zst`（47MB）、两个 `*.ndjson` 解包文件与 `project-oleans.sha256`（28.9MB，本轮未取）。新 `SHA256SUMS` 新增条目：`ArithChallenge.lean`、`ArithSolution.lean`、`arith-audit.log`、`arith-con-leche-compare.log`、`arith-con-leche-master.log`、`arith-nanoda.log`、`robin1984-comparator-v4.33.0.log`、`robin1984-con-leche-compare.log`、`robin1984-lake-comparator-4.36.log`。

### 1.2 新增章节 "Arithmetic consequences"（原文要点/引文）

> "As a check that does not depend on Mathlib's definition of the zeta function, the proof was combined with kimihiro64/Robin1984 (commit acab1a3), an independent formalization of Robin's and Lagarias's criteria on the same Lean and Mathlib versions. Importing both gives two theorems about the divisor sum, with no hypotheses and no mention of zeta (ArithSolution.lean; statements alone in ArithChallenge.lean, which imports only Mathlib)."

给出的两条定理（页面原文）：

```lean
theorem robin_inequality :
    ∀ n : ℕ, 5040 < n →
      ((ArithmeticFunction.sigma 1 n : ℕ) : ℝ) <
        Real.exp Real.eulerMascheroniConstant * (n : ℝ) * Real.log (Real.log (n : ℝ))

theorem lagarias_inequality :
    ∀ n : ℕ, 0 < n →
      ((ArithmeticFunction.sigma 1 n : ℕ) : ℝ) ≤
        (harmonic n : ℝ) + Real.exp (harmonic n : ℝ) * Real.log (harmonic n : ℝ)
```

本地下载的 `ArithChallenge.lean`（1,099 B，仅 import Mathlib，两个 `sorry` 占位）与 `ArithSolution.lean`（945 B，`import Main; import Solution`，用 `Robin1984.robin_inequality_iff_riemannHypothesis.mpr riemannHypothesis` 等给出证明）已核对，与页面描述一致。`arith-audit.log`（我下载并校验）显示两条定理的 `#print axioms` = `[propext, Classical.choice, Quot.sound]`。组合导出：61,752,134,938 B，sha256 `44651dcc482a6e06e8d626994221aff638e422fded189bf856e0c31176926f0d`；其 challenge 导出 sha256 `088a57c9e7454fa5279a86a825e551828ac8431694855aadd1f6e6a6eb37bb1d`。

### 1.3 新通过的检查（页面原文关键行 + 产物 exit 时间）

| 检查 | 结果 | 关键细节（页面/日志原文） |
|---|---|---|
| Robin1984 单独 `lake build` | pass | 4,435 jobs, exit 0 |
| Robin1984 con-leche master + `--compare` | accepts | 69,293 declarations accepted；all three theorems "justified" |
| Robin1984 **未修改的 Comparator v4.33.0**（仓库自身 config） | **pass** | "nanoda accepts, Lean default kernel accepts, **'Your solution is okay!'**; exit 0 at **03:31:06 UTC**"（`robin1984-comparator-v4.33.0.log`：Elapsed **2:51:06**，Exit status 0） |
| Robin1984 **lake comparator (Lean v4.36.0) from exports** | **pass** | "Lean paranoid kernel, nanoda and Lean default kernel all accept; **'Your solution is okay!'**; exit 0 at **04:16:52 UTC**"（`robin1984-lake-comparator-4.36.log`：Elapsed **3:35:48**，Exit status 0） |
| 组合定理 robin/lagarias 编译 + `#print axioms` | pass | only `propext, Classical.choice, Quot.sound` |
| 组合导出 con-leche master | accepts | **1,472,825 declarations** accepted in `--verified` mode；exit 0 at **02:29:56 UTC** |
| 组合导出 con-leche `--compare` vs ArithChallenge | accepts | 两定理 "justified by the solution"；exit 0 at **02:29:06 UTC** |
| 组合导出 nanoda | accepts | exit 0 at **02:56:46 UTC**；33 min 46 s on 64 threads（`arith-nanoda.log`） |
| 组合导出 **lake comparator (v4.36.0)** | **running** | "statement comparison and axiom check passed; its Lean kernel stages are single-threaded on a **62 GB export** and are expected to take many hours, as for the main proof" |

**意义：** 此前 "unmodified Comparator v4.33.0 / lake comparator v4.36.0 端到端" 从未在完整实例上出结果；现在这两个完整流水线都在 Robin1984（一个独立第三方 Lean 项目，同一 Lean/Mathlib 版本）上**成功跑通并给出 "Your solution is okay!"**——即 Comparator 判题链路本身已被端到端验证。主证明本身的 comparator 仍只是"statement comparison + axiom check 已在一轮通过，kernel 阶段 running"。

### 1.4 主证明：仍是 running 的 3 项（原文）

> "| Lean default kernel and Lean paranoid kernel on the export | **running** | single-threaded; no verdict yet |"
>
> "| lake comparator (Lean v4.36.0) end to end | **running** | statement comparison and axiom check already passed in one run; kernels in progress |"
>
> 组合导出 lake comparator：见 §1.3 最后一行。

主证明其余 16 项 pass/accepts/match 与上一版相同（编译 175,187、3 条标准 axiom、leanchecker 175,187/175,187、nanoda exit 19:05:45、con-leche 1,468,418 decls exit 21:19:04、con-leche --compare exit 21:19:12、lean4lean 175,187/175,187 等）。

### 1.5 新版 Caveats 的两个重要细化（相对 phase5 需修正/补充）

1. **`.olean` 哈希依赖构建目录**（新段 "the note below"）："In Lean v4.33.1 a compiled file stores each linter message together with the absolute path of its source file. Of our 175,187 compiled files, **98,219 contain the path** `/home/ubuntu/grh/src/lean/src/…`; the other **76,968, including `Main.olean`, contain no path**. So `project-oleans.sha256` and its sha256 can be reproduced in full only by a build whose source tree is at `/home/ubuntu/grh/src/lean`." 他们做了验证：240 模块 sample（不同机器/路径）168 个 identical、72 个不同（72 个全含该 build 路径、168 个都不含）；77 模块同目录 `lake build` vs 直接 `lean` 调用 byte-identical。"We have not compared the full set against a lake build."
   → 对 phase5 报告里"Main.olean/项目 olean 跨机构一致"的表述需要更精确：**`Main.olean` 等无路径哈希可跨机构复现；整体 manifest 只在同一绝对路径下可复现**。
2. **unsandboxed provenance 未变**：导出仍来自无 sandbox 的 build；"We have not ourselves compared its sha256 with an export made from a sandboxed lake build."（注：LUMI 的独立 sandboxed build 已报告 `Main.olean`/`Statements.olean` 哈希与 MIT 相同，见 phase5 §3.1。）

---

## 2. 其他来源：本轮抓取结果（2026-11-21 11:17–11:31 UTC）

| 来源 | 状态 | 精确事实/引文 |
|---|---|---|
| **alpo.ge** 主页 | **无更新** | 本次 11,625 B（与 phase5 相同）；关键词 Riemann/riemann/Lean/Claude/remark/GRH 命中 **0**。无新 note/update。 |
| **Tao 博客** | **无新帖** | `https://terrytao.wordpress.com/` 最新相关帖仍是 2026-11-20 的 *"Unforced Euler singularity, unforced Navier-Stokes singularity, and the Generalized Riemann Hypothesis"*（`datePublished 2026-11-20T17:19:00Z`，31 comments）；无 2026-11-21 新文/更新。 |
| **Scientific American** | **无更新** | 页面 `updated_at_date_time` 仍为 `2026-11-20T21:47:41Z`；`datePublished 2026-11-20T21:00Z`。 |
| **36kr/智东西** | 未见新文（未逐一列表页验证） | phase5 已记录 2026-11-21 09:06（北京时间）文章；本轮 36kr 列表页请求超时。 |
| **Zulip 线程** | 未能直接读取（需登录/API；未提供公开只读 JSON）| 引用的线程：`https://leanprover.zulipchat.com/#narrow/channel/113488-general/topic/Discussion.3A.20Alp.C3.B6ge.20Proves.20the.20Riemann.20Hypothesis`。仅有 Tao 博客 2026-11-20 的 UPDATE（"moderators … focusing the discussion on the Lean-related aspects"）。 |
| **GitHub `leanprover-community/riemann-hypothesis`** | **仍无 Comparator 结果** | API（2026-11-21T11:18:32Z 抓取）：`pushed_at 2026-11-21T11:17:07Z`，283 stars / 49 forks；最近 commit `8c90877cea` 11:17:07Z（CI small-runner routing），commits 全是 CI/cache 基础设施；`verification/` 目录仍只有 `CACHE.md, CI-RUNNERS.md, NOTES.md, static-scan.txt`（**无 comparator 输出/log**）。`NOTES.md` 本轮有 diff，但**只是补充 build cache/`lakefile.toml` 两处改动的说明**，仍写 "Comparator's output will be added here when the run finishes."；runs 总数 224，最近多为 success / checks in_progress。 |
| **tsnmedia.org** 文章 | 新（相对 phase5），但内容**落后于** MIT 新版 | `https://tsnmedia.org/riemann-hypothesis-lean-checks/`，`datePublished 2026-11-21T09:11:41Z`；仍按 MIT 2026-11-20 22:05 UTC 版本报道（"last updated at 22:05 UTC on 20 November"），称两个 headline runs（lake comparator、Lean-kernel replay）仍在进行；强调 "There is no journal paper, no refereeing…"；引 SciAm：Sutherland "Honestly the chance that anything is fishy here is approximately zero"，Kevin Buzzard 仍在等 "a successful comparator run"。**未反映 09:30 UTC 的新版**（该文 09:11 发布，早于新版 19 分钟）。 |
| **Zenodo 新预印本（新出现，非验证）** | 2026-11-21 发布 | *"The Riemann hypothesis for Dirichlet L-functions [after Levent Alpöge]"*，作者 **Manvir Jaswal**，DOI `10.5281/zenodo.24410057`，v1，**created 2026-11-21T05:51:35Z**，publication_date 2026-11-21，PDF 896,964 B（已下载 `news/jaswal.pdf`）。Zenodo 描述自述为 "A reader's guide to L. Alpöge's Lean 4 formalization…"：陈述 Main.lean 五条定理并沿声明链走，包括 (i) 化归为排除 1/2 右侧零点的某个不等式；(ii) 通过 **ramp sums 与 Landau 的窗口定理**的解析论证；(iii) 该不等式的来源；(iv) **Tate 扭的 Tate–Shafarevich 群**的界；并对照 Alpöge 的 20 个带日期步骤。明确说 "The theorems and their proofs are Alpöge's, and the guide is a reading of his archive." → **是阅读指南，不是独立验证，也非同行评审**。 |

### PhilArchive "Invalidity…"（Nielsen）——本轮仍未读取

- 记录页/PDF：`https://philarchive.org/rec/NIEIOT-2`、检索索引新暴露的直链 `https://philpapers.org/archive/NIEIOT-2.pdf`。
- 本轮尝试与结果（2026-11-21 约 11:20–11:26 UTC）：`philarchive.org/rec/NIEIOT-2` → **403**（Cloudflare "Just a moment…"）；`/archive/NIEIOT-2` → 403；`/rec/NIEIOT-2.json` → 403；`philpapers.org/rec/NIEIOT-2` → 403；带搜索索引给出的 `__cf_chl_tk` 令牌的 PDF URL → **403**；`r.jina.ai` 文本代理 → 60s 超时；Wayback CDX API → 空/超时、Wayback 直取 → 40s 超时；Bing 查询返回无关的中文本地化结果。→ **正文/摘要/日期/作者资质均仍不可得**，无法评估。继续列为"未验证、未审阅的质疑记录"，不能当反证。

---

## 3. 对"官方验证是否完成"的当前判断

**未完成。** 依据（2026-11-21 09:30 UTC 页面版本 + 11:17 UTC 抓取）：

- 页面 **3 项 running**：主证明 Lean default+paranoid kernel replay、主证明 lake comparator end-to-end、组合算术导出 lake comparator kernel 阶段（页面明确 expected many hours）。
- 页面 **没有任何** "verification complete / all checks passed" 的表述；Summary 仍写 "The lake comparator run and the Lean-kernel replay of the export are still in progress."
- 社区 Comparator 仓库 `verification/` 仍无结果（NOTES 原句未变）；无 peer review、无 errata、无官方声明。
- 媒体报道（tsnmedia 2026-11-21 09:11 UTC）与 SciAm（2026-11-20 21:47 UTC）均未宣称完成；Tao 无新表态；alpo.ge 无新 note。

**但有实质进展（需在最终报告体现）：**
1. MIT 页新增 "Arithmetic consequences"：用 RH 证明 + 独立 Robin1984 形式化（commit acab1a3）导出 **Robin 不等式**与 **Lagarias 不等式**（无假设、不提及 ζ）；组合导出 61,752,134,938 B（sha256 `44651dcc…`）。
2. **Comparator 判题链路首次端到端成功**（在 Robin1984 上）：unmodified Comparator v4.33.0 → "Your solution is okay!"（exit 0，**2026-11-21 03:31:06 UTC**）；lake comparator v4.36.0 from exports → paranoid kernel + nanoda + default kernel 全 accept，"Your solution is okay!"（exit 0，**04:16:52 UTC**）。
3. 组合算术包除 comparator kernel 阶段外全部通过（con-leche/nanoda/axiom audit）。
4. 上一版 ~10 小时停滞被打破：新版在 **11h25m** 后出现（2026-11-20 22:05 → 2026-11-21 09:30 UTC）。
5. `.olean` 路径依赖 caveat 的细化（Main.olean 等 76,968 个无路径文件可跨机构一致；98,219 个含绝对路径者不可）。

**预计：** 主证明 comparator 完成时间未知（页面自述 kernel 单线程、61.7GB 导出要多小时；截至 11:17 UTC 仍未宣布）。最终报告应表述为："as of 2026-11-21 09:30 UTC (page) / 11:17 UTC (our fetch)，官方验证仍未完成，但 Comparator 流水线本身已被端到端验证，主证明仅余 3 项运行中。"

---

## 4. 时间线（本轮新增，UTC）

| 时间（UTC） | 事件 |
|---|---|
| 2026-11-21 05:51:35 | Zenodo 预印本 Jaswal "The Riemann hypothesis for Dirichlet L-functions [after L. Alpöge]" 创建（v1，DOI 10.5281/zenodo.24410057） |
| 2026-11-21 09:11:41 | tsnmedia 文章发布（基于 20 日 22:05 UTC 旧版页面；称两个 headline runs 仍在进行） |
| 2026-11-21 09:21:33 | MIT 新 `SHA256SUMS` Last-Modified |
| **2026-11-21 09:30 UTC** | **MIT 页面新版 last-updated**（新增 Arithmetic consequences、Robin1984 检查、组合导出检查；3 项 running） |
| 2026-11-21 11:17:07 | GitHub leanprover-community/riemann-hypothesis 最新 commit（CI 基础设施；NOTES 仍无 comparator 结果） |
| 2026-11-21 11:17:52 | 我方抓取新版 MIT index.html（sha256 `9f07d2d8…`） |

页面/日志中记录的新检查完成时刻（均 2026-11-21 UTC）：组合 con-leche compare **02:29:06**、组合 con-leche master **02:29:56**、组合 nanoda **02:56:46**、Robin1984 unmodified Comparator **03:31:06**、Robin1984 lake comparator **04:16:52**。

---

## 5. 本次局限

- MIT index 无 `Last-Modified`，版本判定靠内容 sha256 + 页面自述时间（`9f07d2d8…`，18,423 B）。
- 未下载 7.7GB `solution.ndjson.zst`、47MB `challenge.ndjson.zst`、两个 ndjson 解包文件、28.9MB `project-oleans.sha256`；因此未复核导出级 sha256（页面值转述）。
- Zulip 线程未直接读取（登录墙/无公开 API）；Tao 博客仅主页/已知帖子。
- 36kr 列表页请求超时；未逐篇检索中文媒体。
- PhilArchive/Nielsen：6 种路径全部 403/超时，正文不可得；其记录真实性仅由搜索引擎索引佐证。
- Zenodo 预印本只读了 API 元数据/描述与 PDF 本体（896KB，未做全文 PDF 文本抽取）；它自述是 reader's guide，不是验证。
- GitHub API 快照 11:18Z，之后可能变化；未读取 CI run 具体日志（只按 NOTES/目录/run 状态判断 comparator 结果未发布）。

---

## 6. 证据文件

- `mit/`：新版 `index.html`、新 `SHA256SUMS`、`page_text.txt`（全文抽取）、全部新增/更新小文件（17 个，全部对 SHA256SUMS 校验 OK）、`hdr_*.txt`
- `gh/`：最新 `notes.md`（与 phase5 的 diff 见正文）、`repo.json`、`commits.json`、`runs.json`、`verif_dir.json`、`root_readme.md`
- `news/`：`tao_home.html`、`sciam.html`、`tsnmedia.html`（+ 抽文）、`zenodo.json`、`jaswal.pdf`、`bing.html`、`philarchive`/`philpapers` 403 页、waveback 尝试
- `alpo/index.html`
- `fetch_gh.ps1`（Windows 侧 GitHub 抓取脚本）
