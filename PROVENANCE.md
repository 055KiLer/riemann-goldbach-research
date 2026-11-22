# PROVENANCE / 来源与版本

## 1. RH 形式化证明镜像（第三方）

- 上游镜像：`https://github.com/CocoSgt/riemann-hypothesis-lean`
- HEAD commit：`7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`（2 commits，tag `v2026-11-20`）
- 作者原始归档：`https://alpo.ge/lean.tar.gz.part01 … part14` 拼接，239,275,554 B
- 归档 sha256：`9631b4f020199e580ba86178cb56c6e9b09f690c2369a80dc4334aa93f49c7fc`
- 工具链：`leanprover/lean4:v4.33.1`；Mathlib pin：`0df444a360eaa60ab8c11dca51a86af692955474`（= Mathlib tag v4.33.1）
- 原始作者：Levent Alpöge（与 Claude 合作）；镜像由 CocoSgt 维护。本仓库不复制其源码，只保留审计报告/摘录与链接。

## 2. 第三方核验页（外部数据，非本仓库作者结论）

- Andrew Sutherland (MIT) 核验页：`https://math.mit.edu/~drew/grh/`
- 本仓库 `evidence/mit/` 中的产物对应页面 2026-11-22 04:35 UTC 版；页面后续可能更新。
- 页面 caveats：构建在无沙箱云机上直接调用 `lean`、仅 77 模块样本与真实 `lake build` 比对、导出 comparative 检查等；详见报告。

## 3. 本仓库使用的环境

- Lean v4.36.0（commit `611c117bfaf7b7ae1cfcf246ce6fba31e8f509e9`）
- Mathlib v4.36.0（tag commit `fc4f59e577feb1a4956671bc04ac18aaaf8cd842`）
- Python 3.14 / numpy / mpmath（实验脚本）
- 所有 Lean 检查：`lake env lean`，无 `sorry`，`#print axioms` 仅 `propext/Classical.choice/Quot.sound`

## 4. 文献（仅引用，未包含 PDF 原文）

- Gou–Wang–Xu, arXiv:2611.18825 v1（2026-11-13）
- Wang–Xu, IMRN 2025 no.18, arXiv:2405.04094v2
- Li–Liu, *A Conditional Proof of the Goldbach Conjecture*, Shandong Univ. MRC, 2026-11-13（未上 arXiv）
- Bui–Florea–Keating, Trans. AMS 376 (2023) 4453–4510（函数域 2/2）
- Baluyot–Čech, arXiv:2501.12529（2025）
- 其他见 `research/goldbach-attack/**` 报告内引用。

## 5. 生产时间

2026-11-21 ～ 2026-11-22（Asia/Shanghai）；仓库初始提交 2026-11-22。
