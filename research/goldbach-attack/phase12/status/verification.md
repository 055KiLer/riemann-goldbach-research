# Phase-12 状态刷新：MIT 2026-11-22 04:35 UTC 版 / 上游 / arXiv / 新闻（含与 phase-11 diff）

- 任务：team task-48（repo-verifier）。检查窗口：**2026-11-22 11:36–11:52 UTC（= 19:36–19:52 CST）**；按 Lead 指示在 20:01 CST 时间盒收口，**未完成的检查在 §6 明确标注**。
- 基线：`../phase11/status/verification.md`（2026-11-21 15:09–15:49 UTC，对应 MIT 页 11-21 12:55 UTC 版）。
- 证据目录（本目录）：`mit/`（页面+产物+headers+表格抽取）、`snapshots/`（多次 index.html 快照）、`gh/`（GitHub API/README/NOTES）、`news/`（alpo/Tao/Lean blog/PhilArchive/Zenodo）、`arxiv/`、`logs/`。
- 说明：Lead 于 **11:29 UTC** 实抓到的页面版本与我方 **11:36:43 / 11:39:40 / 11:42:37 UTC** 三次快照**完全一致**（index.html sha256 相同），页面在检查窗口内稳定。
- 按要求"多抓几次并记录 UTC 时间戳"：T0 **2026-11-22T11:36:43Z**、T1 **T11:39:40Z**、T3 **T11:42:37Z**；三次 `index.html` 均为 27,222 B、sha256 `01a43fc8defab818d878bfa8fd900d7563073db3dbc6f150ad73baec0fe388a7`；paranoid.log 三次均 HTTP 404。

---

## 1. 结论速览（可以宣称 / 不能宣称）

**可以宣称（有本次实抓证据）：**
1. MIT GRH 验证页现版本自述 **last updated 2026-11-22 04:35 UTC**（我方 T0–T3 抓取稳定；Lead 11:29 UTC 抓取同版）。
2. 相对 11-21 12:55 UTC 版，**新增 8 行检查/说明**（§2），其中关键新通过项：**独立 sandbox（bubblewrap，无网络、源码只读）`lake build Main` exit 0（2026-11-21T18:07:21Z 完成）**；**该 sandbox 内导出的 solution.ndjson 与已发布导出逐字节 identical**（61,570,595,788 bytes，sha256 `5ea74b912147c5c93cc2b6d70cc727cf908df2f62ac6a20480a3fa02f6be244e`，2026-11-21T19:32:56Z 完成）；**sandbox olean manifest 175,186/175,187 与已发布 manifest 相同（唯一差异文件为非确定性编译）**；**con-ron（Rust 版 con-leche）`--compare` accept**：主证明 exit 0 @ **2026-11-21T23:02:33Z**、组合算术导出 exit 0 @ **2026-11-21T23:15:58Z**。
3. SHA256SUMS 更新：**3,078 B，sha256 `3c902adefbaf5471db0384b7f5eb1233d1c1a2efcc6a2f8a439754e58dd84042`，Last-Modified 2026-11-22 04:09:51 GMT**；新增条目（sandbox-*、con-ron-*、explicit-statements、deps 等）与本次下载文件的 sha256 **逐一校验通过**（已下载的 15 个新/相关小文件全部 OK）。
4. **paranoid.log 仍 HTTP 404**（T0/T1/T3 三次），`comparator.log`/`lake-comparator.log`/`comparator-main.log`/`leanchecker-paranoid.log` 亦 404 → **主证明的 Lean default+paranoid kernel replay 与 lake comparator 仍无公开结果文件**。
5. 上游原档未变：`alpo.ge` 主页 11,625 B（Riemann/Lean/Claude/remark/GRH/guide 关键词 0 命中）；`remark.pdf` 245,114 B sha256 `3fc97784b71ddd44ff8aa0a177e99622a1c61b13cfa843a0989ee4a7a0cfeb8d`（未变）；本地镜像 `/home/kiler/rh-full` HEAD `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`、dirty=0、175,192 tracked / 175,187 `.lean`；本地保存的 archive sha256 重算 = `9631b4f0…c7fc`，与 MIT 页 Provenance 的 Source archive sha256 一致。GitHub `CocoSgt/riemann-hypothesis-lean` `pushed_at` 仍 **2026-11-20T15:13:36Z**，无新 commit/release。
6. 社区 Comparator 仓库 `leanprover-community/riemann-hypothesis` 仍**没有 comparator 结果**：`verification/` 现 5 个文件（CACHE.md 11,139 / CI-RUNNERS.md 618 / NOTES.md 20,783 / PORTABLE-CACHE.md 4,091 / static-scan.txt 2,588，无 results/logs）；NOTES 末尾原句仍为 "## Results — The build is in progress. The exports' checksums, Comparator's output, the exact command lines and the machine details will be added to this folder."（另首段 "Comparator's output will be added here when the run finishes."）。**注意：NOTES 新增披露社区仓库的 `src/` 已被后续 PR 修改**（"mainly by deleting files the proof does not use and by shortening proofs"），原档对应首 commit `40e56bab`；**社区仓库 HEAD ≠ alpo.ge 原始档案**（但 MIT 的检查对象是原始档案/其导出，不是社区 HEAD）。
7. 预印本：`arXiv:2611.18825`（Gou–Wang–Xu）**仍 v1**（2026-11-13T18:55:46Z）；`arXiv:2610.32672`（SeungJu Lee）**仍 v2**（v2 2026-11-03T12:27:02Z）；`au:Alpoge` 最新仍 2026-09-15，无 2026-11-20 后新条目；arXiv 检索 2026-11-20～11-23 与 "Alpoge" 相关新论文 0 条。

**不能宣称：**
1. **不能宣称官方验证完成**：页面仍 **3 项 running**（见 §2 原文）：(a) 主证明导出上的 Lean default+paranoid kernel replay；(b) 主证明 `lake comparator` end-to-end；(c) 组合算术导出的 `lake comparator`（62 GB 导出、单线程、预计多小时）。页面 Summary 原句仍为 "The lake comparator run and the Lean-kernel replay of the export are still in progress."
2. 不能宣称 peer review / 期刊发表 / Clay 认可；未见任何 errata/retraction/官方"完成"声明。
3. 不能宣称数学正确性（形式化 kernel 检查 ≠ 人类数学审查）；不能宣称"GRH"为一般 GRH——MIT 页 scope 明文仅 Dirichlet L-functions，Dedekind/Hecke/自守 L 函数不在其中。
4. 不能宣称社区仓库 HEAD 的内容已被验证（其 src 已被 PR 修改；验证对象是原始档案/其导出）。
5. 不能把 Zenodo 新预印本中"已由 Lean/Mathlib 社区认证"的说法当作官方结论（该文自述为阅读指南，且官方验证仍未完成）。
6. 本地**未**独立复核的项：sandbox manifest 与已发布 manifest 的逐字节 diff（文件 28,865,695 B，下载在时间盒内未完成）、61.5 GB 导出比对、paranoid/comparator 结果文件（不存在）、Tao/Lean 社区博客最新正文（网络不可达）、PhilArchive Nielsen 正文（仍 403）。

---

## 2. 与 phase-11 版（MIT 页 2026-11-21 12:55 UTC）逐项 diff

| 项 | phase-11（11-21 12:55 UTC 版） | phase-12（11-22 04:35 UTC 版） | 变化 |
|---|---|---|---|
| `index.html` | 20,460 B，sha256 `e4648882…` | **27,222 B，sha256 `01a43fc8defab818d878bfa8fd900d7563073db3dbc6f150ad73baec0fe388a7`** | 更新 |
| 页面 last-updated | 2026-11-21 12:55 UTC | **2026-11-22 04:35 UTC** | +15h40m |
| `SHA256SUMS` | 2,112 B，sha256 `a26d92ed…`，Last-Modified 11-21 09:21:33 GMT | **3,078 B，sha256 `3c902ade…`，Last-Modified 2026-11-22 04:09:51 GMT** | 更新（新增产物条目） |
| `audit.log` | 2,062 B，sha `0a1473fc…`，LM 11-20 19:39:50 GMT | 同左（未变） | 无 |
| `comparator.json` | 460 B，sha `8ea890e6…`，LM 11-20 19:39:50 GMT | 同左（未变） | 无 |
| `paranoid.log` | 404 | **404（T0/T1/T3 三次）** | 仍无 |
| 检查表总行数 | 37 行 | **43 行**（+8 新增/改、-2 旧行被替换） | 见下 |
| running 行 | 3 行 | **3 行，文字未变**：Lean default+paranoid on export（"single-threaded; no verdict yet"）；lake comparator end to end（"statement comparison and axiom check already passed in one run; kernels in progress"）；组合导出 lake comparator（"expected to take many hours"） | 无变化 |
| 新增检查行 | — | ① Independent rebuild with `lake build Main` in a sandbox (no network, read-only source), separate machine \| **pass** \| exit 0, zero errors; finished **18:07:21 UTC on 21 November**（timeline, script）② Export made inside that sandbox vs published export \| **identical** \| **61,570,595,788 bytes, sha256 `5ea74b91…244e`**; finished **19:32:56 UTC** ③ Compiled files of sandboxed build vs manifest \| **175,186 of 175,187 identical** \| one differing module compiles non-deterministically ④ **con-ron --compare (master, 3f22699b)**: challenge vs solution \| **accepts** \| all five theorems justified; 1,468,418 solution + 51,692 challenge decls; exit 0 **23:02:33 UTC on 21 November**; 7m6s/64 threads ⑤ con-ron --compare against ArithChallenge \| **accepts** \| both theorems justified; 1,472,825 decls; exit 0 **23:15:58 UTC on 21 November**；另有 con-ron provenance 行、manifest 说明行被改写、bundled 行改写 | 新增 |
| 删/改行 | — | 删除旧 "con-leche master, above, does" 改为 "con-leche 和 con-ron built from master, above, do"；manifest 行由 "valid only for the build directory" 改为 "specific to the build directory …, and one file in it is not deterministic" | 改写 |
| 页面正文 | "What was verified" 五定理+scope；无"elaborated statement"段 | 新增 **"The elaborated statement of the Lagarias inequality"**：给出 `lagariasStmt` 的 `pp.explicit` 展开（27 个直接常量，意义依赖 1,801 个 Mathlib/core 声明；Robin 对应 2,050 个），并链接 `explicit-statements.lean/.out`、`lagarias-deps.txt`、`robin-deps.txt` | 新增 |
| Caveats | "build 未沙盒化；未与 lake build 全量比对；导出未与 sandboxed build 比对" | 改写为：沙盒 `lake build Main` 已完成且**导出逐字节一致**；新增 **非确定性 caveat**：`LocModel.olean` 同机同输入 6 次编译得到两种输出（4/6 vs 2/6），差异为自动生成的 `BBtop.eq_1` 中一个绑定变量名（38 字节）；`lean -j1` 六次一致；该竞争对应 Lean issue **#15498**，由 PR **#15499** 修复，首个 release v4.36.0；**导出不受影响**（`BBtop.eq_1` 不在 5 定理依赖中，已核对导出中不出现该名字）；**因此 manifest 文件整体 sha256 即使同一路径也不可复现，需逐文件比较** | 改写 |
| 新增下载/证据文件 | — | `sandbox-timeline.txt`、`sandbox-build.sh`、`sandbox-build-continue.sh`、`sandbox-project-oleans.sha256`（29 MB）、`con-ron-compare.log`、`arith-con-ron-compare.log`、`explicit-statements.lean/.out`、`lagarias-deps.txt`、`robin-deps.txt`、`nondet-repro.lean`；页面新增 GitHub 链接 lean4 issues #15498/#15499、con-ron repo | 新增 |

**表格 diff 方法**：解析两版 HTML 的 `<tr><td>` 为规范行后比较（phase11 37 行 → phase12 43 行；新增 8 行、旧行 2 行被改写；running 3 行文字完全一致）。

---

## 3. 本次核验的附属产物（sha256 实校）

新 `SHA256SUMS` 中以下文件已下载并**校验 OK**：`audit.log`、`comparator.json`、`con-ron-compare.log`、`arith-con-ron-compare.log`、`explicit-statements.lean`、`explicit-statements.out`、`lagarias-deps.txt`、`robin-deps.txt`、`nondet-repro.lean`、`sandbox-build.sh`、`sandbox-timeline.txt`。另 phase-11 已核过的 `ArithChallenge.lean`/`ArithSolution.lean`/`arith-*.log`/`nanoda.log`/`con-leche-*.log`/`robin1984-*.log`/`lean4lean-*.log` 的哈希在新 `SHA256SUMS` 中未变（本目录未重复存放，phase-11 已校验）。
**未完成（时间盒）**：`sandbox-project-oleans.sha256`（28,865,695 B，SHA256SUMS 期望 sha256 `51319e37e06fd80dc16cdbe3380e13967603cc36d529389f835ca48076c24859`）下载在时间盒内只拿到部分（未完成）；`sandbox-build-continue.sh`（SHA256SUMS 期望 `3f978140…9fcc`）因服务器 SSL EOF 未取到。故页面第③行 "175,186/175,187" 与 timeline 中 manifest sha256 目前只按**页面+timeline 文本**记录，未做本地逐文件 diff。

本次读到的关键新增文本（原文要点）：
- `sandbox-timeline.txt`：phase A start **2026-11-21T10:09:36Z**（192 核 EPYC）；Mathlib+deps oleans 与 clean reference 一致；pre-sandbox `lake build Mathlib` exit 0 @ **10:09:47Z**；bwrap 沙盒（`--unshare-all`、网络不可达、源码只读、仅 .lake 可写）；多次以不同 `LEAN_NUM_THREADS` 续跑；**sandboxed lake build Main exit=0 @ 2026-11-21T18:07:21Z**；**sandboxed export exit=0 bytes=61570595788 @ 19:32:56Z**，`5ea74b91…244e` = **EXPORT SHA256 MATCHES the published export**；olean manifest 175,187 files sha256 `51319e37…4859`；identical **175,186 of 175,187**；differing 1；ALL DONE **19:33:29Z**。
- `con-ron-compare.log`：accepted 51,692 challenge decls、5 axioms justified；5 条定理逐一 "justified by the solution"；exit 0；elapsed **7:05.63**。
- `arith-con-ron-compare.log`：accepted 15,156 decls、2 axioms justified；robin/lagarias 两定理 justified；exit 0；elapsed **13:25.13**。
- `explicit-statements.out`：lagariasStmt **27** 直接常量 / closure **1,801**（defs 836, theorems-as-statements 559, inductives 179, other 227）；robinStmt **21** / closure **2,050**（955, 630, 207, 258）——与页面文字一致。

---

## 4. 上游（本次实测，UTC 时间戳）

| 目标 | 结果 | 时间 |
|---|---|---|
| 本地 `/home/kiler/rh-full` | HEAD `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`（2026-11-20T15:13:33Z）；`git status --porcelain` = **0**；tracked **175,192**；`.lean` **175,187** | 实测 2026-11-22T11:40Z |
| 本地 archive（`_rh-work/repo-verifier/archive/lean.tar.gz`）sha256 | **`9631b4f020199e580ba86178cb56c6e9b09f690c2369a80dc4334aa93f49c7fc`** = MIT 页 Provenance 的 Source archive sha256（一致） | 11:42Z |
| GitHub `CocoSgt/riemann-hypothesis-lean` | `pushed_at **2026-11-20T15:13:36Z**`；最新 commit `7cbf7a0c32`（与本地一致）；releases 仅 1 个 `v2026-11-20`（published 2026-11-20T15:05:56Z）；README sha256 与本地 README 相同 | API 抓取 11:40Z |
| GitHub `leanprover-community/riemann-hypothesis` | `pushed_at **2026-11-22T11:13:09Z**`；最新 commit `7cce738ba7`（11:08:58Z，README 链接原始来源）；**`verification/` 5 个文件、无 comparator 结果**；NOTES 末段 "Results — build is in progress"；NOTES 新增 "Comparing builds" 段（第三方复现：ishaan2006 完整 build 76,968 identical / 98,219 因绝对路径不同；export 被独立复现；Ticobit challenge export 两次一致）；并披露社区仓库 `src/` 已被 PR 修改、原始档案=commit `40e56bab` | API 抓取 11:40Z |
| `alpo.ge` | 主页 **11,625 B**；关键词 Riemann/riemann/Lean/Claude/remark/GRH/guide 各 **0**；`remark.pdf` **245,114 B，sha256 `3fc97784…eb8d`（未变）** | 11:44Z |

---

## 5. arXiv / 新闻 / 批评（本次实测）

- **arXiv:2611.18825**（Gou–Wang–Xu, *Landau's problems through ratios of L-functions*）：仍 **v1**，published/updated **2026-11-13T18:55:46Z**，46 页。
- **arXiv:2610.32672**（SeungJu Lee）：仍 **v2**，updated **2026-11-03T12:27:02Z**（v1 2026-10-23），16 页。
- **`au:Alpoge`**：最新条目 2026-09-15；无 2026-11-20 之后新预印本；arXiv 检索 2026-11-20～11-23 "Alpoge" 相关 **0 条**。
- **新 Zenodo 预印本**（新出现）：*"What a map identifies and the Riemann hypothesis: height averages, a reading of zero exclusion in Alpöge's proof, and a search for zeros using prime phases"*，作者 **Kokonoha**，DOI `10.5281/zenodo.24432174`，created **2026-11-22T02:40:59Z**，publication_date 2026-11-22；文中自述是帮助读者理解 Alpöge 证明的阅读笔记，并称"the validity of the proof, certified by the Lean and Mathlib communities, is not revisited"——**该表述比当前官方状态更强，不可引用为验证结论**。
- **PhilArchive Nielsen "Invalidity of the Alpoge Proposed Proof"**：`https://philarchive.org/rec/NIEIOT-2` 与 `https://philpapers.org/archive/NIEIOT-2.pdf` 本次仍 **HTTP 403**（Cloudflare）；正文/摘要仍不可得 → 未验证、不能当反证。
- **Tao 博客**：本轮 WSL（HTTP 000）与 Windows PowerShell（无法连接）均抓取失败（网络问题，非 404）；上次成功抓取（phase-11，2026-11-21 15:31 UTC）仍无新帖，2026-11-20T17:19:00Z 那篇评论数 61。
- **Lean community blog** `https://leanprover-community.github.io/blog/posts/riemann-hypothesis/`：本轮 WSL/Windows/jina 代理三路仍不可达（HTTP 000/超时）→ **未完成（时间盒），内容未知**。
- 未发现 peer review/errata/retraction/官方"验证完成"新闻。

---

## 6. 未完成项（时间盒，明确标注）

1. `sandbox-project-oleans.sha256`（29 MB）未完整下载 → 未能本地逐文件复核"175,186/175,187 identical、唯一差异 LocModel.olean"与 manifest sha256 `51319e37…`（仅记录页面+timeline 说法）。
2. `sandbox-build-continue.sh` 未取到（SSL EOF）；其 hash 按 SHA256SUMS 记录为 `3f978140…9fcc` 但未本地校验该文件。
3. 未复核 61,570,595,788 B 导出逐字节一致（需 61.5 GB 下载/比对，超出本任务范围）。
4. Tao 博客/Lean community blog 最新正文未取到（网络不可达）；PhilArchive Nielsen 正文仍 403。
5. 未重新做本地 175,187 文件与 archive 的全量 `diff -r`（phase-5 已做过全量逐字节一致；本轮只重算 archive sha256 与本地 git 状态）。
6. Li–Liu 预印本 arXiv ID 仍未定位（phase-11 已记录；hexagonmath 同名文档非 arXiv 记录）。

---

## 7. 给最终报告的"状态"表述（建议）

> As of **2026-11-22 04:35 UTC** (MIT page; our fetch T0–T3 11:36–11:42 UTC; Lead 11:29 UTC): the official verification is **still not complete** — three checks remain running: the Lean default+paranoid kernel replay of the main export, the `lake comparator` run on the main proof, and the `lake comparator` run on the combined arithmetic export (62 GB, single-threaded, expected many hours). What is new since 11-21 12:55 UTC: an **independent sandboxed `lake build Main`** (no network, read-only source) **completed with exit 0 at 2026-11-21 18:07:21 UTC**, its **export is byte-identical to the published export** (61,570,595,788 B, sha256 `5ea74b91…244e`, finished 19:32:56 UTC), its olean manifest matches 175,186/175,187 files (one non-deterministic file, explained; export unaffected), and **con-ron `--compare` accepts** both the five main theorems (23:02:33 UTC) and the Robin/Lagarias statements (23:15:58 UTC). Upstream original archive (alpo.ge) and the CocoSgt mirror are unchanged; the community Comparator repo is active but still has **no comparator output**. No peer review, no errata, no completion announcement.
