# Phase-5 recheck：外部验证状态快照（MIT GRH 页 / 镜像 / 公开新闻）

- 任务：team task-20（Phase-5 quick recheck）。执行者：repo-verifier。
- 检查时间：**2026-11-21 16:00–16:12 CST（= 2026-11-21 08:00–08:12 UTC）**。
- 交付目录（本任务唯一写入范围）：`_rh-work/goldbach-attack/phase5/mit-recheck/`。
- 抓取工具：WSL `curl`（general internet 可用；github.com 不可达）、Windows PowerShell `Invoke-WebRequest`（访问 github.com/raw.githubusercontent.com/wordpress）、`web_search`/`web_fetch`（第三方页面）。
- 原始证据：`mit/`（页面+产物+headers）、`gh/`（GitHub API/README/NOTES JSON+md）、`news/`（Tao 博客、36kr、PhilArchive 尝试、wayback 尝试）、`logs/`、`*.ps1`（Windows 抓取脚本）。

---

## 0. 结论（一句话）

**"已声明、官方完整验证尚未完成"这一判断不变。** MIT 页面自 `2026-11-20 22:05 UTC` 后 **没有任何更新**（字节级相同，已 10 小时无新内容）；官方 `lake comparator` 与 Lean paranoid kernel 对导出证明的重放 **仍标记为 running**，社区 Comparator 仓库 `verification/NOTES.md` 也仍写 "Comparator's output will be added here when the run finishes"。

但过去 ~10 小时出现了**增强性**新证据：**第二个、在无网络 sandbox 中完成的完整独立构建**（LUMI 超算，Aapo Lipponen）：175,187/175,187 模块 0 错误，`Main.olean`/`Statements.olean` 的 sha256 与 Sutherland 公布的完全相同；并给出了证明依赖审计：`riemannHypothesis` 实际使用 146,437/175,187 项目模块（83.6%），292 个被抽查声明全部只依赖 3 条标准 axiom。这些**不支持**"已完成官方验证"，但显著增加了"形式化证明本身可复现、无 sorry/axiom"的独立证据。

另需注意的新出现项：PhilArchive 上有一篇标题为 **"Invalidity of the Alpoge Proposed Proof of the Riemann Hypothesis"**（作者 Jenny Lorraine Nielsen）的记录/预印本（`https://philarchive.org/rec/NIEIOT-2`）。该站被 Cloudflare 防护，正文在我方所有抓取路径均为 403（web_fetch 亦 403；Wayback 超时），**未能读取内容，无法评估其严肃性，也未见它被任何方面引用/回应**。目前只能作为"待跟踪的未验证质疑"记录，不能当作反证，也不能忽略。

---

## 1. MIT 页面复核（https://math.mit.edu/~drew/grh/）

### 1.1 抓取与字节比对

| 文件 | 本次抓取（2026-11-21 08:00 UTC）sha256 | 与 2026-11-20 存档对比 |
|---|---|---|
| `index.html`（12782 B） | `de7153ec1b22acab193a99824d427d41050e2c0d2c4374ec518d52fc0de62307` | **完全相同**（5 小时前存档同哈希） |
| `audit.log`（2062 B） | `0a1473fce6eed840011f4a76b1c51558fc6f03edd1e6bd1ee542e6c738d87a62` | 相同 |
| `comparator.json`（460 B） | `8ea890e6ccda9cf3983ada343af18a41d12542036875a3936e7925ed5b1582ff` | 相同 |
| `SHA256SUMS`（1291 B） | `d8496902f492eeb0274460e525071cc30803bba7817d59b27c874f5a25317373` | 相同 |
| `project-oleans.sha256`（28,865,695 B） | `375cbee2fc3fc0f5088ef2e6dc9a5ac5530924310dc62422ec65aac9dc4c1d25` | 相同（对 SHA256SUMS 校验 OK） |

HTTP 头给出的资源修改时间（Apache `Last-Modified`，UTC）：

- `index.html`：无 `Last-Modified`（PHP 动态页），但内容哈希与 2026-11-20 的存档完全相同；
- `audit.log`、`comparator.json`、`project-oleans.sha256`：`Fri, 20 Nov 2026 19:39:50 GMT`；
- `SHA256SUMS`：`Fri, 20 Nov 2026 21:59:00 GMT`。

### 1.2 页面自述状态

页面原文（`index.html` 顶部）：

> "Andrew Sutherland (MIT), checks run with Claude Code. **Page last updated 2026-11-20 22:05 UTC.** Results below are as of that time and this page will be updated as the remaining checks finish."

表格中仍为 **running** 的两行（原文）：

> "| Lean default kernel and Lean paranoid kernel on the export | **running** | single-threaded; no verdict yet |"
>
> "| lake comparator (Lean v4.36.0) end to end | **running** | statement comparison and axiom check already passed in one run; kernels in progress |"

其余行（pass/accepts/match 等）与 2026-11-20 22:05 时完全一致，例如：175,187 模块编译 pass；5 条主定理 `#print axioms` → `propext, Classical.choice, Quot.sound`；leanchecker 175,187/175,187；nanoda accepts；con-leche master/`--compare` accepts；lean4lean 175,187/175,187（5 个加 fuel）。**无新增章节、无新增结果文件。**

### 1.3 探测新文件（防止"页面未更新但已上传结果"）

对以下常见结果文件名做了 HEAD 探测，全部 **HTTP 404**：`comparator.log`、`paranoid.log`、`kernel-replay.log`、`export-replay.log`、`comparator-output.txt`、`results.json`、`update.html`。→ 截至 2026-11-21 08:00 UTC，**官方 comparator / paranoid replay 没有公布完成结果**。

**与已知状态对比：** 一致，无变化。页面时间戳仍是 `2026-11-20 22:05 UTC`；到本次检查时已过去约 **10 小时 00 分**未再更新。

---

## 2. 本地镜像与作者站点复核

### 2.1 本地镜像 `/home/kiler/rh-full`（Lead 的干净 clone）

```
$ git log -1 --format='%H%n%ci%n%s'
7cbf7a0c32fca1badf05931879a37c3f8a2b03b4
2026-11-20 23:13:33 +0800
README: credit, statements, layout, download, build and checking guide
```

- `git status --porcelain` = **0**（工作区干净）；
- `git ls-tree -r HEAD | wc -l` = **175,192**；`.lean` 文件（`-z` 原始路径）= **175,187**；磁盘 `.lean` = 175,187；总行数 = **17,374,215**；
- 两个仓库 ref（`refs/heads/main`、`refs/remotes/origin/main`）均指向 `7cbf7a0c3…`；tag `v2026-11-20` = `0fb9869c6…`；`git count-objects`: in-pack 178,798。
- **结论：本地镜像未变。**
- 上游 GitHub 镜像 `CocoSgt/riemann-hypothesis-lean`（经 Windows 网络查 GitHub API，2026-11-21 08:01 UTC）：`pushed_at = 2026-11-20T15:13:36Z`，最近两个 commit 就是 `7cbf7a0c32`（15:13:33Z）和 `0fb9869c6e`（14:59:12Z）→ **上游也没有新提交**。注意该仓库的 `updated_at` 显示 2026-11-21T07:59:44Z 只是 star/元数据更新，不是代码更新。

### 2.2 alpo.ge（作者站点）

- 抓取 `https://alpo.ge/`（11,625 B，HTTP 200）：页面是他的个人主页（论文列表/履历）。**全文关键词扫描 "Riemann/riemann/RH/Lean/Claude/AI/remark/GRH" 全部为 0 次命中**——即截至检查时，主页上**没有**关于 RH 证明/Lean 档案的新 note 或更新链接（`remark.pdf` 并不从主页链接）。
- 已知产物仍可访问，且内容未变（用 ETag/sha256 判定，站点对任意路径都可能返回 200 HTML，故不能用状态码判定存在性）：
  - `https://alpo.ge/remark.pdf`：245,114 B；本地副本 `/home/kiler/rh-work/remark.pdf` sha256 = **`3fc97784b71ddd44ff8aa0a177e99622a1c61b13cfa843a0989ee4a7a0cfeb8d`**，与社区验证仓库 `leanprover-community/riemann-hypothesis` 的 `verification/NOTES.md` 记录的公告 sha256 **完全相同** → 未检测到新版/修订版 note（至少与 2026-11-20 社区记录的那一版一致；我方此前的副本也是同一份）。
  - `https://alpo.ge/lean.tar.gz.part01`：ETag `"b116580303b65e25529dae6e694a3bab"`，与 2026-11-21 早些时候/2026-11-20 抓取时相同；14 分片拼接 sha256 仍为 `9631b4f0…c7fc`（239,275,554 B，此前已验证）。
- **结论：作者站点未检测到新 note/update/errata。**

---

## 3. 公开新闻与新出现的独立验证（2026-11-20 之后）

### 3.1 新增：LUMI 超算上的第二个独立、无网络 sandbox 完整构建

仓库：`https://github.com/aapolipponen/rh-lean-check-lumi`（运行者 Aapo Lipponen；GitHub API：created_at `2026-11-20T19:24:46Z`，pushed_at `2026-11-20T23:59:33Z`）。README 关键内容（原样转述）：

- Status（README 原文）："**compile complete (updated 2026-11-20 22:30 UTC)** … All 175,187 modules compile, with no Lean error. `Main.lean` finished at 22:21 UTC on 20 November 2026. The audit of statements, axioms and dependencies is running; this section will be updated when it ends."
- "each `lean` process in a **no-network sandbox**"；"Archive: 14 parts from alpo.ge, concatenated sha256 `9631b4f0…c7fc`"。
- 静态扫描："no `axiom`, `sorry`, `admit` or `native_decide` in the source"。
- **Olean 跨构建一致性**：`Main.olean` sha256 **`9146dfb4148e24d2252e04c50742f3e49dd126dfcc5006d10bf5f873ddf796ad`** 和 `Statements.olean` sha256 **`f8e0aed3c2d69390b6dd3bb24e13aa25e043a02ca42f021e3f6e4ec8b57fd6b1`**，与 Andrew Sutherland 公布的哈希 **identical**。
- 构建细节：前 94%（164,776 模块）用 48 分钟（8 个 LUMI-C 节点），剩余 6% 因机器/内存限制重试，718 次基础设施重试、**没有一次 Lean error**；总计约 3,500 core-hours（编译本身约 900）。import 深度 **203 层**。
- **依赖审计**（README 中 "How much of the archive the proof uses"；对应 commit `82d91dbbd0`，2026-11-20T23:56:59Z）：`riemannHypothesis` 依赖 **146,437 / 175,187 个项目模块（83.6%）**、1,478,219 个常量、5,081 个 Mathlib 模块；**28,750 个项目模块被 `Main` import 但证明未使用**。292 个声明（5 条主定理 + 243 条 `UpperTheory.LiteratureTheorems.*` + 主要内部步骤）逐个检查：**全部只依赖 `propext`、`Classical.choice`、`Quot.sound`**，243 条文献定理全部被 RH 证明触达。
- 局限（README 原文）："**Kernel replay (`leanchecker`) of every module — not run by us.** Done by Sutherland"; "Second, independent kernel — not run by us. nanoda pass reported by Sutherland; con-leche pass reported by Szymon Teżewski on the Lean Zulip"。
- 该仓库另有 `docs/`：对档案结构的人工/AI agent 阅读指南，含"105 个命名的经典定理及其形式语句是否名副其实的裁决表"，并明确"不是 referee report，不为数学背书"。

→ **意义：MIT caveat 中"build 是 unsandboxed"这一点得到部分补强（第二个 build 是 sandboxed 且 olean 哈希一致），但官方 Comparator 与 paranoid kernel replay 仍未完成。**

### 3.2 社区 Comparator 仓库（Deicyde → 现 `leanprover-community/riemann-hypothesis`）

GitHub API（2026-11-21 08:01 UTC）：`full_name = leanprover-community/riemann-hypothesis`（即已知的 Deicyde 仓库），created `2026-11-20T14:47:49Z`，**pushed_at `2026-11-21T08:00:10Z`**（仍在高频更新：242 stars / 46 forks；本次抓取到 171 个 workflow run，最近 8 个均 success，为 "Publish CI cache / checks / Build PR" 等基础设施任务，最新 commit `23aebbb302` 2026-11-21T08:00:10Z "Retain manual PR build caches after the PR head advances (#24)"）。

`verification/NOTES.md`（本任务抓取）关键内容：

- 数据来源与哈希：announcement `remark.pdf` sha256 `3fc97784…`（与本地副本一致）；archive 14 分片 sha256 `9631b4f0…c7fc`；challenge export sha256 `bd484ac9886a96f26b1d9a7a59ebd45b7a70d102c015d4f31f9302bbdd6ab2b9`。
- **"Comparator's output will be added here when the run finishes."** ← 截至抓取时 **官方 Comparator 结果尚未写入**。
- 源码统计：175,187 `.lean`、1,030,531,854 B、17,374,215 行（其中非空 15,531,759）；"**There are no comments.**"；818,755 个 `theorem`/`lemma`、242,067 个 `def`/`abbrev`/`structure`/`class`/`instance`/`inductive`；所有文件在 `Main` import 闭包内。
- 静态扫描：无 `axiom`/`sorry`/`admit`/`native_decide`/`implemented_by`/`extern`/`unsafe`/`opaque`/`debug.*`/`skipKernelTC`；notation 均 local/scoped；源码不读写文件/进程/环境。
- 元编程清单（更正自 issue #2）：BuildAid D1–D5 加 deny-list 名；`CutCptCopy.lean` 用 `addDecl` 复制已有声明（"so the kernel checks every copy"）；`Imports.lean` 定义 `kexactB`——"elaborates a term and assigns it to the goal **without the elaborator checking that its type matches**. It is used, through small macros, in 67 files"；`kcopy`/`#kcopy_probe` 同类；`run_tac` 出现 33 次（31 次 revert-all 再 exact，2 次短块）；1 个 `@[positivity]` extension。并给出 soundness 论证：这些地方 kernel 是唯一检查者，"That is sound, because the kernel checks every declaration…"。
- **Lean 版本风险说明**（值得在最终报告中引用）：项目 build 用 Lean **v4.33.1**；NOTES 列出该版本包含/不包含的 kernel 修复，明确写 **不包含 4.34.1 的 runtime 修复 #15241、#15289**，"which the release notes say could potentially be turned into a proof of `False` in the official kernel with deliberately constructed input"；"kernels not built on the Lean runtime are unaffected"；因此判题用 **Lean v4.36.0** + 独立 checker。
- 另注：该服务器对任意路径返回 200 HTML，**不能用 HTTP 状态码判断文件是否存在**，须看拼接 sha256。

### 3.3 Terence Tao 博客（一手来源，2026-11-20T17:19:00Z）

URL：`https://terrytao.wordpress.com/2026/11/20/unforced-euler-singularity-unforced-navier-stokes-singularity-and-the-generalized-riemann-hypothesis/`
（本任务经 Windows PowerShell 抓取成功；`"datePublished":"2026-11-20T17:19:00+00:00"`；31 条评论。）

其中 RH 段落原文：

> "Levent Alpöge, using an internal AI model, has generated an (enormous) Lean-only proof of the Generalized Riemann Hypothesis. [This Lean Zulip thread](...) is probably the best place to follow the efforts to verify the proof and extract the strategy of proof (which, from very initial analysis, appears to use the full power of modern developments on the Langlands program and arithmetic geometry). **(UPDATE: the moderators of the Lean thread are now focusing the discussion on the Lean-related aspects of the proof only.)** I imagine the digestion process will take some time, though in this case at least we have a human author to communicate with to assist with this task."

Lean Zulip 线程 URL（从博客提取）：
`https://leanprover.zulipchat.com/#narrow/channel/113488-general/topic/Discussion.3A.20Alp.C3.B6ge.20Proves.20the.20Riemann.20Hypothesis`

→ Tao 没有宣布验证完成；"消化过程需要时间"。Tao 本人**没有**对数学正确性表态。

### 3.4 新闻/科普（二手）

- **Scientific American**，`https://www.scientificamerican.com/article/the-ai-riemann-hypothesis-proof-is-almost-certainly-true-independent-mathematicians-attest/`：`"datePublished":"2026-11-20T16:00:00-05:00"`（= 21:00 UTC），页面 `updated_at_date_time` = `2026-11-20T21:47:41Z`；meta description："Researchers are **near to completing** their verification of a claimed solution to the most important unsolved problem in math"。→ 与"未完成官方验证"一致。
- **36kr/智东西**（英文版，`https://eu.36kr.com/en/p/4078708897092744`，页面标注发布时间 `2026-11-21 09:06`，北京时间）：转述 Tao 博客、Kontorovich 表态（"I am actually more confident that the proof will succeed…"）、**Deng Yu（邓煜）**："I will not even glance at it before I reach 500 pages"；并引 Clay 规则：千禧年问题需要正式发表、至少 2 年验证、被数学界广泛接受。称"目前数学界仍在尝试验证正确性并梳理核心思想"。
- **TechCrunch**（2026-11-20）：标题提到 "and a human did, too" —— 指同日另一组人类数学家的相关声明（Euler/NS or RH-related，详见 task-2；与本次核验状态无关）。
- **LessWrong linkpost / Moneycontrol / Clarín / Indian Express / Telegraph India**：均为 2026-11-20 或 21 日的转述，无新验证结果。

### 3.5 唯一"负面"新出现项：PhilArchive 的 invalidity 预印本记录（未能读取）

- 检索索引可见：**"Jenny Lorraine Nielsen, *Invalidity of the Alpoge Proposed Proof of the Riemann Hypothesis*"**，记录页 `https://philarchive.org/rec/NIEIOT-2`。
- 抓取尝试与结果（均 2026-11-21 16:02–16:11 CST）：WSL curl → Cloudflare "Just a moment..."；Windows PowerShell Invoke-WebRequest → **HTTP 403 Forbidden**；`web_fetch` 工具 → **HTTP 403**；Wayback Machine `http://archive.org/wayback/available` 超时、`web.archive.org` 抓取 90s 超时；Googlebot UA 亦被 Cloudflare 拦截。→ **正文、摘要、日期、作者资质均无法取得**。
- 因此：**不能把它当作有效反证，也不能忽略**。目前没有任何可核验内容表明它指出了具体数学错误；PhilArchive 是预印本平台，无同行评审背书。建议列入最终报告的"待跟踪/未证实质疑"清单，并尝试后续通过机构代理/邮件联系作者核实。
- 另：未检索到任何 retraction/errata/官方回应。

---

## 4. 对既有判断的影响（逐条）

| 既有判断 | 本次复核 | 变化 |
|---|---|---|
| MIT 页 last updated 2026-11-20 22:05 UTC；官方 lake comparator + paranoid kernel replay 仍在 running | **确认**：页面字节级无变化；两个 running 行仍在；探测的结果文件全部 404；~10h 无更新 | 无变化 |
| "已声明但未完成官方验证" | **确认**，且社区 Comparator 仓库 NOTES 仍写 "Comparator's output will be added here when the run finishes"；Tao/SciAm/36kr 均未宣布完成 | 无变化 |
| 本地镜像 = alpo.ge 档案且未变 | **确认**：HEAD `7cbf7a0c3…`、175,192/175,187/17,374,215、dirty=0；上游 CocoSgt 无新提交；archive 分片 ETag/sha 未变；remark.pdf 未变（sha256 `3fc97784…`） | 无变化 |
| 独立验证只有 MIT 一家（build unsandboxed） | **需更新**：新增第二个独立、**无网络 sandbox** 的完整 build（LUMI、Aapo Lipponen），175,187/175,187、0 Lean 错误，`Main.olean`/`Statements.olean` 哈希与 MIT 的完全相同；另有依赖审计（83.6% 模块、292 声明仅 3 axiom）。但其未做 leanchecker 重放；官方 Comparator/paranoid 仍未完成 | **增强，但不改变"官方未完成"** |
| 无需关注反对意见 | **需新增**：PhilArchive 出现 "Invalidity…" 预印本记录，内容不可得、未验证；应跟踪，不能当反证 | **新增待跟踪项** |
| Lean kernel 信任前提 | 社区 NOTES 给出更细的版本风险：build 用 4.33.1，**不含 4.34.1 的 runtime 修复 #15241/#15289**（理论上可构造 False，但"kernels not built on the Lean runtime are unaffected"），故判题用 4.36.0 + 独立 kernel。最终报告应把这层 caveat 写清楚，避免"kernel 已验所以万无一失"的过度声明 | **细化 caveat** |

---

## 5. 精确引文 / URL / 时间戳汇总（可复制进最终报告）

1. MIT 页面：`https://math.mit.edu/~drew/grh/`；页面自述 **"Page last updated 2026-11-20 22:05 UTC"**；本次抓取 2026-11-21 08:00:24 UTC，`index.html` sha256 `de7153ec…2307`（与 2026-11-20 存档相同）；仍为 running 的两项：Lean default+paranoid kernel on the export；lake comparator (Lean v4.36.0) end to end。各 downloaded artifact `Last-Modified`：audit.log/comparator.json/project-oleans.sha256 = 2026-11-20 19:39:50 GMT；SHA256SUMS = 2026-11-20 21:59:00 GMT。
2. LUMI 独立验证：`https://github.com/aapolipponen/rh-lean-check-lumi`；repo created 2026-11-20T19:24:46Z，pushed 2026-11-20T23:59:33Z；README "compile complete (updated 2026-11-20 22:30 UTC)"、"175,187 of 175,187, 0 failures"、`Main.olean` sha256 `9146dfb4…96ad`（与 Sutherland 相同）、依赖审计 commit `82d91dbb` 2026-11-20T23:56:59Z（146,437/175,187 模块、292 声明仅 3 axiom）。
3. 社区 Comparator 仓库：`https://github.com/leanprover-community/riemann-hypothesis`（Deicyde 仓库现名）；pushed_at 2026-11-21T08:00:10Z；`verification/NOTES.md`："Comparator's output will be added here when the run finishes."；challenge export sha256 `bd484ac9…b2b9`；source："There are no comments."，17,374,215 行/15,531,759 非空、818,755 theorem/lemma、242,067 def/…
4. Tao 博客：`https://terrytao.wordpress.com/2026/11/20/unforced-euler-singularity-unforced-navier-stokes-singularity-and-the-generalized-riemann-hypothesis/`，`datePublished 2026-11-20T17:19:00+00:00`；原文引文见 §3.3；Lean Zulip thread：`https://leanprover.zulipchat.com/#narrow/channel/113488-general/topic/Discussion.3A.20Alp.C3.B6ge.20Proves.20the.20Riemann.20Hypothesis`。
5. SciAm：`https://www.scientificamerican.com/article/the-ai-riemann-hypothesis-proof-is-almost-certainly-true-independent-mathematicians-attest/`，published 2026-11-20T21:00Z，updated 2026-11-20T21:47:41Z，"Researchers are near to completing their verification…"。
6. 36kr/智东西：`https://eu.36kr.com/en/p/4078708897092744`，标注 **2026-11-21 09:06**；Deng Yu "I will not even glance at it before I reach 500 pages"；Clay 需 2 年验证。
7. 本地：`/home/kiler/rh-full` HEAD `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`（author date 2026-11-20T23:13:33+08:00），175,192 tracked / 175,187 .lean / 17,374,215 行，`git status` clean；上游 `CocoSgt/riemann-hypothesis-lean` pushed_at 2026-11-20T15:13:36Z。
8. alpo.ge：主页 11,625 B，关键词 "Riemann/Lean/Claude…" 0 命中；`remark.pdf` 245,114 B sha256 `3fc97784b71ddd44ff8aa0a177e99622a1c61b13cfa843a0989ee4a7a0cfeb8d`；`lean.tar.gz.part01` ETag `b116580303b65e25529dae6e694a3bab`（未变）。
9. PhilArchive：`https://philarchive.org/rec/NIEIOT-2`（Jenny Lorraine Nielsen, "Invalidity of the Alpoge Proposed Proof of the Riemann Hypothesis"）——正文 403 不可得，内容未验证。

---

## 6. 本次未能做到的（诚实边界）

- MIT 页面 `index.html` 无 HTTP `Last-Modified`，只能用内容 sha256 证明未变（不是服务器时间戳）。
- 未直接读取 Lean Zulip 线程（需登录/API）；Tao 博客是公开一手来源。
- GitHub API 快照时间 2026-11-21T08:01Z，star/run 数此后可能变化；未逐个读取 171 个 CI run 的日志，仅按 NOTES.md 与 run 名称/状态判断"Comparator 结果未发布"。
- PhilArchive 正文在 4 种抓取方式下均被 Cloudflare 拦截（403/挑战页/Wayback 超时），未评估其内容与严肃性。
- 36kr 内容为二手转述（标注了出处与时间），其英文版对 Tao/Deng/Clay 的引语可能经过翻译。
- 所有"未检出"结论都只针对本次抓取时间点；MIT 页面可能在我们检查后更新。

---

## 7. 证据文件清单

- `mit/index.html`、`mit/audit.log`、`mit/comparator.json`、`mit/SHA256SUMS`、`mit/project-oleans.sha256`、`mit/hdr_*.txt`（HTTP 头）、`mit/page_text.txt`（正文抽取）
- `gh/aapolipponen_readme.md`、`gh/aapolipponen_repo.json`、`gh/aapolipponen_commits.json`、`gh/deicyde_repo.json`、`gh/deicyde_commits.json`、`gh/deicyde_notes.md`、`gh/deicyde_verif_dir.json`、`gh/deicyde_actions_runs.json`、`gh/cocosgt_repo.json`、`gh/cocosgt_commits.json`
- `news/tao_home.html`、`news/tao_post.html`、`news/sciam.html`、`news/36kr_en.html`、`news/philarchive_*.html`（Cloudflare 挑战页）、`news/philpapers.html`
- `fetch_gh.ps1`、`fetch_gh2.ps1`、`fetch_gh3.ps1`（Windows 侧抓取脚本，供复现）
