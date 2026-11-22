# Riemann–Goldbach 研究笔记（2026-11）

> **状态：未证明 Goldbach 猜想；未产生超越现有数学的无条件新定理；所有内容未经同行评审。**
> 本仓库保存的是 2026-11-21 ～ 11-22 由 DSH Agent Team 生成的研究笔记、审计报告、形式化代码与数值实验摘要；
> 仅供备份、复现与进一步审计，**不得作为已确立的数学结论引用**。

## 这个仓库是什么

一次针对两个对象的核查与攻击尝试：

1. **Alpöge / Claude 声称的黎曼猜想（RH）与 Dirichlet-L GRH 的 Lean 4 形式化证明**（2026-11-20 发布于 alpo.ge）；
2. **Goldbach 猜想的证明尝试**：Li–Liu（2026-11-13）条件性路线、Gou–Wang–Xu（arXiv:2611.18825）的 GRH + Ratios 路线，以及若干替代/否定性尝试。

仓库包含：研究/审计报告、Lean 形式化代码、可复现的 Python 实验脚本、关键小结果数据、MIT 核验页的小型证据，以及来源/状态说明。
**不包含**：第三方论文 PDF/HTML、RH 镜像的 17.4M 行源码、大型数值缓存（约 15.6GB 的 `.npy/.c64`）、作者原始归档分片（239MB 的 `lean.tar.gz` 等）。这些均可从报告给出的链接/哈希重新获取。

## 核心结论（先看这 4 条）

1. **RH/GRH 声称**：本地镜像与 alpo.ge 原始档案逐字节一致（sha256 `9631b4f0…c7fc`）；MIT 核验页截至 2026-11-22 04:35 UTC 显示大部分检查通过，但**仍有 3 项 running**（主证明 paranoid kernel replay、主证明 `lake comparator`、组合导出 comparator），**无同行评审**。
2. **Li–Liu 路线**：其核心假设 R 在有限模型数值意义上持续被反证（raw ratio > 1 到 N = 6×10⁷），并在一个未证的低相关假设下可推出 R 渐近为假；**有限模型不构成证明**。
3. **GWX/Ratios 路线**：独立审计确认“GRH + 2/2 Ratios ⇒ Goldbach”归约无致命错误；缺口被定位为 **level-aspect 2/2 Ratios 的任意固定 q-幂 power saving**（本仓库中的 `RAT_sym/der(c>2)` / residue-covariance 表述）。
4. **我们自己**：没有证明 Goldbach，没有证明 RAT/H_Ratios，没有给出新的无条件定理；产出主要是**核查、否定性结果、精确化缺口、新数值证据与 Lean 形式化骨架**。详见 `research/goldbach-attack/phase12/0-phase12-报告.md`。

## 目录

```
README.md / STATUS.md / PROVENANCE.md / NOTICE.md / LICENSE / MANIFEST.sha256
research/
  ├── 黎曼猜想与哥德巴赫_完整报告.md          # 总报告
  ├── repo-verifier/ …                        # 来源与静态审计
  ├── proof-digest/ …                         # RH 证明 digest
  ├── goldbach/ …                             # 文献核查
  ├── lean-verifier/ …                        # Lean 检测方案
  └── goldbach-attack/ …                      # 9+3 个 phase 的攻击/审计/数值/Lean
evidence/
  ├── mit/                                    # MIT 核验页的小型证据（audit.log 等）
  └── scans/                                  # 全树静态扫描的 0 命中证据
```

## 快速复现（Lean）

本仓库不包含 Mathlib；需要本地已装 **Lean 4.36.0 + Mathlib 4.36.0**：

```bash
export PATH=/path/to/lean-4.36.0-linux/bin:$PATH
cd /path/to/mathlib4-4.36.0
lake env lean /path/to/repo/research/goldbach-attack/phase12/lean/nowrap.lean   # EXIT 0
lake env lean /path/to/repo/research/goldbach-attack/phase12/lean/wrap.lean     # EXIT 0
```

- `nowrap.lean` / `wrap.lean`：no-wrap 正交性与 wrap 计数恒等式（组合恒等式，不是新数论）。
- `phase5/lean/phase5_mathlib.lean`、`phase6/lean/dictionary.lean`：Rayleigh 商、零-范数字典等逻辑链的形式化。
- 更完整的 Lean 检测方案见 `research/lean-verifier/lean-detection-report.md`。

## 快速复现（Python）

脚本依赖 `numpy`、`mpmath`；各 phase 目录内的 `.py` 可直接运行，具体参数见对应报告。注意：部分数值脚本需要大量内存/时间，且依赖本地生成的缓存；本仓库只包含小型结果数据，不含大缓存。

## 重要声明

- **这些是工作笔记，不是论文。** 多处标记 `[推导]/[推测]/[待核]`；过程中发生过自我纠错（例如 phase-4 结论撤回、A_q mask bug、memmap 伪影、c=1 账本修正等）。
- **第三方内容未在本仓库重新分发**：Alpöge/Claude 的 Lean 源码见 [CocoSgt/riemann-hypothesis-lean](https://github.com/CocoSgt/riemann-hypothesis-lean) 与 [alpo.ge](https://alpo.ge/)；MIT 核验页见 [math.mit.edu/~drew/grh](https://math.mit.edu/~drew/grh/)；GWX/Li–Liu/WX/BFK 等文献见各报告引用。
- 许可：**本团队编写的代码采用 MIT（见 `LICENSE`）；本团队编写的文字/报告采用 CC BY 4.0**。第三方名称、引文归原作者。
- 本仓库默认私有；如需公开分享，请自行评估其中未验证结论与第三方引用的风险。

## 来源与版本

见 `PROVENANCE.md`。核心版本：Lean v4.33.1（RH 仓库 pin）/ Lean v4.36.0（形式化检查）；Mathlib v4.33.1（`0df444a3…`）/ v4.36.0。
