# STATUS — 事实清单与状态（截至 2026-11-22 20:02 +08:00）

## 1. Alpöge/Claude RH+GRH Lean 声称

| 项 | 状态 |
|---|---|
| 来源 | 本地镜像 = alpo.ge 14 分片拼接（239,275,554 B；sha256 `9631b4f0…c7fc`），逐字节一致 |
| 规模 | 175,187 个 `.lean` / 17,374,215 行 / 1,030,531,854 B |
| 工具链 | `leanprover/lean4:v4.33.1`；Mathlib pin `0df444a360eaa60ab8c11dca51a86af692955474` |
| MIT 核验页 | 2026-11-22 04:35 UTC 版：175,187 模块编译通过；5 条主定理仅 `propext/Classical.choice/Quot.sound`；leanchecker/nanoda/con-leche/lean4lean 通过；LUMI 无网络沙箱重建 + 导出逐字节一致；**3 项仍 running**（paranoid replay、主证明 lake comparator、组合导出 comparator） |
| 同行评审 | **无** |
| 结论 | “已声明、官方验证接近完成但未闭环”，不能宣称“已验证的 RH 证明” |

## 2. Goldbach 尝试

| 路线 | 状态 |
|---|---|
| Li–Liu（2026-11-13，未上 arXiv） | 条件性归约；其 Hypothesis R 在有限模型 raw ratio > 1 到 N=6×10⁷；在未证 H_cov^low 下可推 R 渐近为假；**无 Goldbach 证明** |
| GWX（arXiv:2611.18825 v1） | GRH + 2/2 Ratios ⇒ Goldbach；独立审计确认归约无致命错误；缺口 = level-aspect 2/2 Ratios |
| 替代/否定性尝试 | 热核正性方向无效；密度 1 结果不能推出 Goldbach；pair correlation 不足以覆盖全部大偶数；显式公式只给对 n 的平均 |
| 本仓库自己的条件性表述 | `GRH + RAT_sym/der(c>2) ⇒ Goldbach`；RAT(c) 与 residue-covariance 估计等价；“任意固定 q-幂 saving 就够”；方法级边界 c≤1/2；**均为未证条件** |

## 3. 我们没有做什么

- 没有证明 Goldbach；没有证明 RAT/H_Ratios；没有证明/推翻 RH 或 GRH；
- 没有产生新的无条件数学定理；没有提出可替代的新数学工具；
- 没有复现全量 kernel 级检查（本机 15GB RAM 不可行），只引用并核验了第三方页面的可下载产物。
