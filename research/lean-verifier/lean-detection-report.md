# Lean 检测怎么做 —— riemann-hypothesis-lean 环境审计 + 可执行验证方案

- 报告人：teammate `lean-verifier`（shared task **task-2**）
- 时间：2026-11-21 16:40–17:00 CST（= 08:40–09:00 UTC）
- 机器：WSL2 Ubuntu（MagicBook-HP），16 核，**15 GiB RAM**（报告时 available ≈ 9.4 GiB，另有并发 python 数值任务 `model.py` 占 ~5–6 GiB），Linux 根分区 936 GB 空闲，D: 111 GB 空闲
- 证据约定：**【实测】**= 本报告作者亲自执行并贴出输出；**【引用】**= 前序 teammate / MIT 页面 / 仓库 README 的一手证据；**【推测】**= 工程估计，未经实测
- 交付物：本文件 + 实测产物（`~/rh-work/lean-test/lean33-probe/`、`~/rh-work/lean-test/lean33/`、`/tmp/grh_page_final2.html`）
- 约束遵守：**目标仓库 D:\Rieman\riemann-hypothesis-lean 全程只读**；所有安装只写 `$HOME` 与 `/tmp`；未改 Windows 注册表；未杀他人进程；未启动全量构建。

---

## 0. TL;DR（先回答三个问题）

### 0.1 "Lean 检测怎么做"——一张表看清五层

| 层 | 做什么 | 能证明什么 | 本机可行性 | 缺什么 | 耗时量级 |
|---|---|---|---|---|---|
| L0 环境 | toolchain / Mathlib / 缓存就绪 | 检测的前提 | ✅ 可做（本报告已实测到一半） | — | 分钟~小时 |
| La **语句层** | `lake build Statements`（`Statements.lean` 只 `import Mathlib`） | 5 条主**语句**能在官方 Mathlib 定义下通过 elaboration | ✅ **本机可做** | 仅缺 Mathlib olean 缓存（~3 GB 下载） | 30–90 分钟（含准备） |
| Lb **构建层** | `lake build Main`（全量 17.4M 行 / 175,187 文件） | **证明**真的编译通过 | ❌ **本机不可行** | 50–100+ GB RAM 级别机器、数小时~数天 | 云机器数小时起 |
| Lc **公理审计** | 编译后 `#print axioms <5 定理>` + `leanchecker` 重放 | 证明不依赖 `sorryAx`/自定义 axiom | ❌ 本机不可行（依赖 Lb 全部 oleans；或第三方 export 重放需 ~50–100 GB RAM） | 全量 oleans / 大内存机 | 云机器分钟级（重放） |
| Ld **源码层** | `sorry/admit/axiom/unsafe/...` 文本扫描 | 没有**明显**作弊痕迹（不构成证明） | ✅ **本机已完成** | — | 分钟级 |
| Le **独立判据** | 干净环境重编译 + 无作弊 + 哈希对作者归档 + 独立 kernel（leanchecker/nanoda/con-leche/lean4lean） | 社区级可信度 | ⚠️ 哈希/文本可比对；kernel 级需大机器 | 大内存机 + 作者/第三方 export | 见 §2.5 |

**一句话结论：本机只能做"轻量检测"（Ld 静态扫描 + La 语句层，后者准备 30–90 分钟）；Lb/Lc/Le 的 kernel 级重放本机 15 GB RAM 不可能完成，只能引用第三方（MIT/Deicyde）结果并核对哈希。**

### 0.2 对 Lead 三条已知事实的复核与修正

1. **"WSL 里装了 Lean"——不成立。** 【实测】WSL 侧 `~/.elan` 不存在，`lean / lake / elan` 均不在 PATH，`/home/kiler` 下无系统级 Lean 安装。用户看到的"已装 Lean"来自三处混淆，见 §1.2。
2. **Windows 侧 elan 是 VSCode 扩展 14:45 自动装的外壳，toolchain 为空是下载失败所致。** 【实测】复读了 `7-Lean Editor.log` 的完整命令与报错：`elan toolchain install leanprover/lean4:v4.33.1` → SSL schannel `CRYPT_E_NO_REVOCATION_CHECK` 失败。详见 §1.3、§3。
3. **MIT 页面"仍未更新"——已过时，需更正。** 【实测】本报告 08:47Z 抓取 `https://math.mit.edu/~drew/grh/`（16,544 B，sha256 `bbffa73c…b348`，旧快照 `de7153ec…2307`/12,782 B），页面已写 **"Page last updated 2026-11-21 04:20 UTC"**，新增 **Robin/Lagarias 算术后果独立交叉检查**（详见 §2.5、§6.4）；主检查多数 pass，`lake comparator` 与 **Lean default/paranoid kernel 对 export 的重放仍在 running**。

### 0.3 本报告的实测增量（都是在本次会话里真跑出来的）

- 【实测】用 `gh-proxy.com` 在 WSL 下载 **官方 Lean v4.33.1 linux toolchain**（896,280,645 B，25.4 s，**35.3 MB/s**），解压 12.6 s → **3.1 GB**，`lean --version` = `Lean (version 4.33.1, x86_64-unknown-linux-gnu, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6, Release)`，**与 MIT 页记录的 Lean v4.33.1 commit `819816b2` 完全一致**。
- 【实测】v4.33.1 独立 kernel 小实验通过（`#print axioms` → 无公理，exit 0）。
- 【实测】对目标仓库源码直接跑该 toolchain：`src/Statements.lean:1:0: error: unknown module prefix 'Mathlib'` —— 精确证明"只有 toolchain 不够，还缺 Mathlib oleans"。
- 【实测】`lake build Statements` 在项目骨架上正确解析 `lakefile.toml` 并开始拉取 Mathlib（走已配置的 gh-proxy 重写）。
- 【实测】目标仓库静态扫描：**175,187 个 `.lean`、17,374,215 行；`sorry/admit/axiom/unsafe/constant/opaque/native_decide/ofReduceBool/skipKernelTC` 全部 0 文件**；`addDecl` 1 文件；`maxHeartbeats 0` 4 文件；与 README 自报一致。仓库无 `.lake`、无 oleans（HEAD `7cbf7a0c…`，与 `~/rh-full` 克隆一致）。
- 【实测】Windows 侧 `gh-proxy.com` 可直接 HEAD 到 `lean-4.33.1-windows.zip`（**200，842,456,015 B**）→ 给出 Windows 原生修复路径。

---

## 1. 环境审计表（WSL / Windows / VSCode 三处真实状态）

### 1.1 总表

| 环境 | 检查项 | 实测状态 | 证据/命令 |
|---|---|---|---|
| **WSL Ubuntu** | `~/.elan` | ❌ 不存在 | `ls -la ~/.elan` → No such file |
| | `lean / lake / elan` 命令 | ❌ 都没有 | `which lean lake elan` → 空 |
| | `~/.bashrc` 里的 lean PATH | ❌ 无 | `grep -i elan ~/.bashrc` → 无 |
| | 系统级 Lean | ❌ 无 | `/usr/local/bin`、`/usr/bin` 无 lean |
| | **非标准路径的手装 toolchain** | ✅ **有 2 套**（前序会话 + 本次） | `~/rh-work/lean-test/lean4/lean-4.36.0-linux/bin/{lean,lake}`；`~/rh-work/lean-test/lean33/lean-4.33.1-linux/bin/{lean,lake}`（本次装，见 §5） |
| | Mathlib | ✅ 4.36.0 已构建（`.lake` 2.8–3.1 GB）；4.33.1（仓库 pin）**只有源码**，无 oleans | `~/rh-work/lean-test/mathlib36/`、`~/rh-work/lean-test/mathlib4-src/` |
| | CPU / RAM / 磁盘 | 16 核；15 GiB（available 6–9 GiB 波动）；根分区 936 G 空闲；D: 111 G 空闲 | `nproc; free -h; df -h` |
| | Remote-WSL server | ❌ `~/.vscode-server` 不存在 | `ls ~/.vscode-server` → No such file（注：这是 **Windows 用户目录**下的检查，见下） |
| **Windows** | `C:\Users\GU178\.elan` | ✅ 存在（14:46 创建），elan **4.4.0** 已装 | `bin/` 有 `elan.exe/lake.exe/lean.exe/leanc.exe/leanchecker.exe/...`（均为 6,090,752 B 的同一程序硬链接） |
| | `toolchains/` | ❌ **空** | `ls .elan/toolchains` → 空 |
| | `settings.toml` | `default_toolchain = "leanprover/lean4:stable"`，`version = "12"` | `cat .elan/settings.toml` |
| | `known-projects` | 内容一行：`\\?\D:\Rieman\riemann-hypothesis-lean` | `cat .elan/known-projects` |
| | `tmp/` | 空（16:38 被清理，与 Lead 触发 `lean.exe` 尝试一致） | `ls .elan/tmp` → 空 |
| | 系统 hosts | 🔴 **"Steam++" 加速器把 50 个域名（含 github.com、raw.githubusercontent.com、api.github.com、objects.githubusercontent.com、release-assets.githubusercontent.com、huggingface.co…）全部劫持到 `127.0.0.1`** | `grep -A55 "Steam++ Start" C:\Windows\System32\drivers\etc\hosts` |
| | Windows 侧 Lean 可执行 | ❌ 无可用 toolchain（`lean.exe` 是 elan 的转发器，找 toolchain 失败；Lead 已实测 download 失败） | — |
| **VSCode（Windows 原生）** | Lean 扩展 | ✅ `leanprover.lean4@0.0.242`（14:45 安装） | `ls C:\Users\GU178\.vscode\extensions` |
| | settings | `"lean4.alwaysAskBeforeInstallingLeanVersions": false` | `C:\Users\GU178\AppData\Roaming\Code\User\settings.json` 末行 |
| | Remote-WSL 扩展 | ❌ **未安装**（扩展列表：eide/code-runner/lean4/中文包/python/cpp/jupyter/tombi…，无 `ms-vscode-remote.remote-wsl`） | `ls ~/.vscode/extensions` |
| | `~/.vscode-server` | ❌ 不存在 → **从未用 Remote-WSL 打开过** | `ls C:\Users\GU178\.vscode-server` → No such file |
| | 当前 VSCode 进程 | ❌ Code 已关闭（实测 `Get-Process Code` 计数 = 0） | PowerShell 实测 |
| | workspaceStorage 活动 | 最新目录 `3d453656774a0a07e6c04dc8b0989bc7`（`workspace.json` = `file:///d%3A/Rieman`），`state.vscdb` mtime **16:02**（窗口/扩展宿主在该时刻退出） | `ls -lat .../workspaceStorage` |
| | Lean 扩展输出日志 | ✅ 日志存在，含完整失败链（§1.3） | `.../logs/20261121T144340/window1/exthost/output_logging_*/7-Lean Editor.log` |

### 1.2 "WSL 里装了 Lean"这一说法为什么是误会（三个来源）

1. **Windows 上的 `.elan` 目录**：`C:\Users\GU178\.elan` 是 **Windows 侧**、VSCode 扩展 14:45 自动装的，不在 WSL 里。用户若在资源管理器/WSL 里看到它（WSL 通过 `/mnt/c` 也能看到），容易误以为"Lean 装好了"。
2. **VSCode 里扩展 + "Lean" 字样面板**：扩展装好 ≠ toolchain 装好 ≠ language server 能跑。本机扩展装了，但 toolchain 下载失败（§1.3）。
3. **WSL 里确实有 Lean 二进制，但是前序 agent 手动解压的、不在 PATH、不在 `~/.elan`**：`/home/kiler/rh-work/lean-test/lean4/lean-4.36.0-linux/bin/`（11:11 由前序会话从 gh-proxy 下载 zip 解压）。本次又新增 v4.33.1（§5）。这类"野生 toolchain"不是标准安装：没有 elan、不在 PATH、VSCode 找不到、`lake` 也不会自动用它。

> 核实话术：**"WSL 从没有通过标准方式（elan）安装过 Lean；Windows 侧 VSCode 扩展自动装过 elan 外壳，但 toolchain 下载失败、目录为空。现在能用的是两个手动解压到非标准路径的官方 toolchain（4.36.0 前序装的、4.33.1 本次装的）。"**

### 1.3 VSCode 扩展为什么现在必然不能工作（完整证据链，来自 Lean Editor 日志）

日志原文（`C:\Users\GU178\AppData\Roaming\Code\logs\20261121T144340\window1\exthost\output_logging_20261121T144346\7-Lean Editor.log`，14:45 起）：

```text
d:\Rieman\riemann-hypothesis-lean> lean --version
=> Operation failed. Exit code: -4058.                      # Windows 找不到 lean.exe（扩展首次检查失败）

> try { $installCode = (Invoke-WebRequest -Uri "https://elan.lean-lang.org/elan-init.ps1" ...).Content
        $installer = ScriptBlock::Create(...); $rc = & $installer -NoPrompt 1 -DefaultToolchain leanprover/lean4:stable; exit $rc }
info: downloading installer to C:\Users\GU178\AppData\Local\Temp\
info: default toolchain set to 'leanprover/lean4:stable'

d:\Rieman\riemann-hypothesis-lean> elan --version
elan 4.4.0 (3cc76985a 2026-11-18)                            # 扩展自动装 elan 成功

> elan toolchain install leanprover/lean4:v4.33.1
warning: could not check for elan self-update: error during download
info: downloading https://releases.lean-lang.org/lean4/v4.33.1/lean-4.33.1-windows.tar.zst
error: could not download file from 'https://releases.lean-lang.org/lean4/v4.33.1/lean-4.33.1-windows.tar.zst'
       to 'C:\Users\GU178\.elan\tmp\y5anykpdovixwv3q_file'
info: caused by: error during download
info: caused by: [35] SSL connect error (schannel:
        next InitializeSecurityContext failed:
        CRYPT_E_NO_REVOCATION_CHECK (0x80092012) - 吊销服务器无法检查吊销状态)
=> Operation failed. Exit code: 1.
```

**机制拆解**：
- 扩展激活后按 `lean-toolchain`（`leanprover/lean4:v4.33.1`）要求安装 toolchain；
- `releases.lean-lang.org` 的 URL 302 到 `github.com/leanprover/lean4/releases/...`；而 Windows 的 hosts 被 Steam++ 改写了 GitHub 域名，且 elan 用 Windows 原生 TLS（schannel），对 `release-assets.githubusercontent.com`/CDN 做证书吊销检查（OCSP/CRL）时失败 → `CRYPT_E_NO_REVOCATION_CHECK`；
- 结果：`C:\Users\GU178\.elan\toolchains\` 空；language server 无 toolchain 可启动 → InfoView/Problems 永远不会有 Lean 内容；
- 且**扩展跑在 Windows 本地**（无 Remote-WSL、无 `~/.vscode-server`），所以它连 WSL 里现有的两个 toolchain 也看不见（即使看见了也无法跨 WSL 用 Windows 二进制路径）。

> 补充【实测】：elan self-update 也是同一类网络错误（"could not check for elan self-update"），说明不是单次偶发。

### 1.4 网络真相（WSL，实测于 08:41Z）

| 端点 | 结果 | 说明 |
|---|---|---|
| `https://github.com` | ❌ 连不上（DNS 解析到 **127.0.0.1**，端口 443 拒绝） | Windows hosts 的 Steam++ 段被 WSL 继承（WSL 内 `/etc/hosts` 没有该条目，但 Windows 侧 DNS 代理返回 127.0.0.1） |
| `raw.githubusercontent.com` / `objects.githubusercontent.com` / `release-assets.githubusercontent.com` | ❌ 同上 | 同上 |
| `https://releases.lean-lang.org/...` | 302 → `github.com/...`，最终 ❌ | 只"半通"：能拿重定向但不能下载 |
| `https://elan.lean-lang.org/elan-init.sh` | ✅ 200（9,823 B） | 官方安装脚本可下；脚本内部 `ELAN_UPDATE_ROOT="https://github.com/leanprover/elan/releases"` → 真安装会卡在 GitHub |
| **`https://gh-proxy.com/https://github.com/...`** | ✅ **200，35.3 MB/s**（896 MB / 25.4 s） | **本机的 GitHub 下载正解**（前序会话已写入全局 git 重写，本次复核仍在：`url.https://gh-proxy.com/https://github.com/.insteadof https://github.com/`） |
| `https://ghproxy.net/...` | ✅ 200（速度不如 gh-proxy） | 备用 |
| `https://cache.mathlib.org/` | 404（根路径正常，说明服务可达） | Mathlib 缓存主入口 |
| `https://lakecache.blob.core.windows.net/mathlib4-master/` | 404/400（根路径；Azure 容器存在与否需具体 blob） | Mathlib cache 的 Azure 后端，网络可达 |
| `https://leanprover-community.github.io` | ❌ 连接 reset | 同上 GitHub 域名被劫持 |
| 系统代理 | ❌ 无 `http_proxy/https_proxy`；WSL 侧 172.17.192.1 / 127.0.0.1 常见 Clash 端口（7890/7897/1080…）全 closed | 当前没有可用代理客户端 |
| Windows 侧 `gh-proxy` | ✅ PowerShell HEAD `lean-4.33.1-windows.zip` = **200，842,456,015 B** | Windows 原生修复路线可行（§4.3） |

---

## 2. Lean 检测的正确分层方法论（含可直接复制的命令）

**为什么不能一步到位**：Lean 的可信度 = `kernel 接受` × `语句是想要的语句` × `没有绕过 kernel 的构造`。这三个属性由不同层级的检查覆盖；而全量构建的代价（17.4M 行 + Mathlib）让"一上来 `lake build Main`"在本机不可行。正确顺序：**先便宜的把关（Ld/La），再贵的（Lb/Lc），最后对第三方结果做哈希级比对（Le）**。

> 下面命令假定工具链用本次已装好的路径。先做一次 L0：
> ```bash
> export PATH=$HOME/rh-work/lean-test/lean33/lean-4.33.1-linux/bin:$PATH
> lean --version    # 期望：Lean (version 4.33.1, x86_64-unknown-linux-gnu, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6, Release)
> lake --version    # 期望：Lake version 5.0.0-src+819816b (Lean version 4.33.1)
> cd /home/kiler/Windows-D/Rieman/riemann-hypothesis-lean
> git rev-parse HEAD                 # 期望：7cbf7a0c32fca1badf05931879a37c3f8a2b03b4
> sha256sum lean-toolchain lakefile.toml   # 期望：3aac669c…f5db71 / b831ad8c…ddec4c（与镜像记录一致）
> ```

### 2.1 La 语句层：`lake build Statements`（只依赖 Mathlib，本机可做）

**它检查什么**：`src/Statements.lean` 只有 16 行、只 `import Mathlib`，定义 4 个 Prop（`RiemannZetaZerosOnLine` 等）；`Main.lean` 的 5 条 theorem 里第 1 条直接是 Mathlib 的 `RiemannHypothesis`。编译 `Statements` 目标 = **用官方 Mathlib 定义验证"语句本身"类型正确、没被改写**，不验证证明。这是性价比最高的一层语义检查。

**前置**：Mathlib（commit `0df444a360eaa60ab8c11dca51a86af692955474`，tag v4.33.1）的 olean 缓存。**仓库本身没有 `.lake`，所以必须先取 Mathlib**。

```bash
# 0) 为保持 D: 仓库只读，把仓库复制到 WSL 的 ext4 盘（1.7 GB，约 10–20 s）
cp -a /home/kiler/Windows-D/Rieman/riemann-hypothesis-lean "$HOME/rh-work/rh-check"
cd "$HOME/rh-work/rh-check"
export PATH=$HOME/rh-work/lean-test/lean33/lean-4.33.1-linux/bin:$PATH

# 1) 拉 pinned Mathlib + 8 个依赖（lake 会走已配置的 gh-proxy git 重写；首次约 5–20 分钟）
lake update            # 或直接 lake build Statements，lake 会自动 fetch 依赖
# 2) 下载官方预编译 Mathlib olean 缓存（Azure/lakecache；约 1.5–3 GB，10–30 分钟量级）
lake exe cache get
# 3) 编译语句层（只有一个模块，但需加载 Mathlib oleans）
time lake build Statements 2>&1 | tee /tmp/build-Statements.log
```

**预期输出**：`Build completed successfully.` / 末尾 `✔ [xxxx/xxxx] Built Statements (xxs)`，exit 0。
**耗时量级**【推测】：首次准备 30–90 分钟（依赖 clone + cache 下载 + Mathlib 加载）；之后每次 <2 分钟。
**失败怎么办**：
- `error: unknown module prefix 'Mathlib'` → Mathlib 还没 fetch/cache（见本次实测 §5-E3）；
- `lean version mismatch` / `expected v4.33.1` → PATH 里是别的 lean（4.36.0 混入）；确认 `lean --version`；
- `cache get` 403/超时 → 网络问题；重试、或 `--cache-from=master,legacy`、或检查 `cache.mathlib.org` / Azure 连通性；
- OOM（cache get 一般不会）→ 本机有并发 python 任务时先暂停；cache get 主要吃磁盘/网络。

### 2.2 Lb 构建层：`lake build Main`（全量，本机不可行）

**它检查什么**：5 条主定理的证明项从源码编译、通过 elaborator+kernel。

```bash
cd "$HOME/rh-work/rh-check"      # 注意：不要在 D: 仓库里跑（会写 .lake）
export PATH=$HOME/rh-work/lean-test/lean33/lean-4.33.1-linux/bin:$PATH
nproc; free -g                   # 本机 16 核 / 15 GiB
# 强烈建议不要在本机全量跑；若坚持，先限并发 + 监控：
time lake build Main --jobs=4 2>&1 | tee /tmp/build-Main.log
# 另一个窗口监控： watch -n5 'free -g; pgrep -c lean'
```

**规模事实**【实测+引用】：175,187 个 `.lean`、17,374,215 行；`Main` 的 import 闭包 ≈ 175,184/175,187 模块（前序审计用 import 图算出）；`lakefile.toml` 全局 `maxHeartbeats = 4000000`、`--tstack=400000`——**`lean --help` 实测 `--tstack=num` 是"thread stack size in Kb"**，即每条编译线程栈上限 400 MB，16 并发仅栈就 6.4 GB，还没算 elaboration 本身。
**预期输出（成功）**：`Build completed successfully.`，全部 library Built。
**耗时量级**【推测】：需要 50–100+ GB RAM 的机器；16 核可能 10 小时–数天；本机 15 GB 很可能中途 OOM/被 kill（`Killed`、exit 137）。
**失败怎么办**：
- `Killed`/exit 137 → OOM，减小 `--jobs`、加 swap 无济于事（不要靠 swap；SSD 会写爆），换大内存机；
- `unknown constant`/`declaration uses 'sorry'` → 可能是仓库存疑信号（本机静态扫描 0 sorry，若出现要人工查）；
- 超时 → 分库段构建：`lake build Development`、`lake build Formalism`…（注意 `defaultTargets` 比 `Main` 大，README 特别提醒）；
- 想省时：**不要本机全量**，直接用第三方结果 + 哈希比对（§2.5）。

### 2.3 Lc 公理审计：`#print axioms` / kernel 重放（依赖 Lb 的产物）

**它检查什么**：编译后的环境里，5 条主定理的**传递依赖公理集**。干净结果只有 3 条标准公理；出现 `sorryAx`、`Lean.ofReduceBool`、自定义 `axiom` 就是红灯。

```bash
cd "$HOME/rh-work/rh-check"      # 必须在 lake build Main 成功之后
export PATH=$HOME/rh-work/lean-test/lean33/lean-4.33.1-linux/bin:$PATH
cat > Check.lean <<'EOF'
import Main

#print axioms riemannHypothesis
#print axioms riemannZeta_eq_zero_re
#print axioms LFunction_ne_zero_of_half_lt_re
#print axioms LFunction_eq_zero_re
#print axioms LFunction_eq_zero_re_of_isPrimitive
EOF
lake env lean Check.lean 2>&1 | tee /tmp/print-axioms.log
```

**预期输出**（MIT `audit.log` 与 README 均记录）：
```text
'riemannHypothesis' depends on axioms: [propext, Classical.choice, Quot.sound]
...（其余 4 条同理，且只允许这三条）
```
**其他辅助检查**：
- 环境里 axiom 总数：MIT 页称 "15 axioms in the environment, all in Init"；本地可用 `#print axioms` + 对比，或写脚本遍历 `Lean.Environment`（超出一页范围，可参考 MIT audit.log）。
- kernel 重放（推荐）：`leanchecker`（与 Lean 同发行版）重放编译产物；更独立的用 `lean4checker`/`nanoda`/`con-leche`/`lean4lean`。命令形态举例：`lake env leanchecker Main` 或对 export 文件用外部 checker（见 §2.5）。
**耗时量级**：`#print axioms` 秒级；leanchecker 单线程重放 175k 模块在 MIT 机器上约 43 分钟（16:43→18:17 UTC 推断）；本机 15 GB 内存**无法**完成 export 级重放（MIT 页明说 checker 需要 ~100 GB RAM / 70 GB disk；con-leche 需 ~50 GB RAM）。
**失败怎么办**：oleans 与当前 toolchain 版本不匹配 → 用生成它们的同一 toolchain 重放；`unknown module` → LEAN_PATH 没设好，用 `lake env`。

### 2.4 Ld 源码层静态扫描（本机已完成，秒级~分钟级）

```bash
# 在 WSL 里对仓库副本（ext4 上快很多；D: 上 grep 也行但慢数倍）
cd "$HOME/rh-full"    # = 与 D: 仓库同 HEAD 的克隆；或 cd D: 仓库
git grep -I -l -E '\bsorry\b'               -- '*.lean'
git grep -I -l -E 'sorryAx'                 -- '*.lean'
git grep -I -l -E '\badmit\b'               -- '*.lean'
git grep -I -l -E '^\s*axiom\s'             -- '*.lean'
git grep -I -l -E '\bunsafe\b'              -- '*.lean'
git grep -I -l -E 'implemented_by|@\[extern' -- '*.lean'
git grep -I -l -E '^\s*(opaque|constant)\s' -- '*.lean'
git grep -I -l -E 'native_decide|ofReduceBool' -- '*.lean'
git grep -I -l -E 'mkSorry|admitGoal|mkSyntheticSorry|skipKernelTC' -- '*.lean'
git grep -I -l -E 'maxHeartbeats\s+0'       -- '*.lean'
git grep -I -l -E '^\s*(scoped\s+)?(macro|elab)\b' -- '*.lean'
git grep -I -l 'addDecl'                    -- '*.lean'
```

**本次实测结果**（rh-full @ `7cbf7a0c`，与 D: 仓库 HEAD 相同；`git grep` 精确扫 175,187 个 .lean）：

| 模式 | 文件数 |
|---|---:|
| `\bsorry\b` / `sorryAx` / `\badmit\b` | **0 / 0 / 0** |
| `^\s*axiom\s`（声明）/ 任意 `\baxiom\b` | **0 / 0** |
| `unsafe` / `implemented_by` / `@[extern]` / `opaque` / `constant` 声明 | **0 / 0 / 0 / 0 / 0** |
| `native_decide` / `ofReduceBool` / `mkSorry|admitGoal|mkSyntheticSorry|skipKernelTC` | **0 / 0 / 0** |
| `#eval` / `#exit` / `set_option debug` | **0 / 0 / 0** |
| `addDecl` | **1**（`Formalism/HermitianCurvature/HermitianCurvatureProofs/CutCptCopy.lean`；前序审计读源码确认是"复制已有声明改名"，仍走 kernel） |
| `maxHeartbeats 0` | **4**（`PoitouTateDuality/PtfsShaFinal.lean`、`CutMainCpt.lean`、`UniformizerClauseOfAdmitted.lean`、`UniformizerClauseOfAdmittedAlt.lean`） |
| `macro/elab`（行首，宽口径） | 30 文件；`run_tac` 16 文件（README 自报"22 个 custom macro/elab"——**口径差异**：我含 scoped 与全部行首；差异不是造假信号） |
| 总文件 / 总行数 | **175,187 / 17,374,215**（`git grep -c '^'` 求和，实测） |
| `.lake` 构建产物 | **不存在**（D: 仓库与 rh-full 均无） |

**它不能证明什么**：静态扫描抓不到"用元编程/自定义 elaborator 在 elaborator 层伪造证明"这类高级作弊。源码里还有 30 个 `macro/elab`、16 个 `run_tac`、1 个 `addDecl`——这些是合法机制，但**严格验证必须靠 Lb/Lc 编译 + kernel**。前序审计逐个看过这些文件并判为常规 tactic 简写/复制命令【引用】。

### 2.5 Le 独立验证判据（"怎样才算通过"清单）

对这类"声称证明大猜想"的仓库，社区级可信度需要同时满足：

| # | 判据 | 本机可做？ | 本次实测/引用结果 |
|---|---|---|---|
| 1 | **干净环境从源码全量构建通过**（不用作者任何产物；官方 toolchain + pinned Mathlib） | ❌ 需大机器 | 【引用】MIT 页："All 175,187 modules compile … pass; zero errors（Lean v4.33.1, Mathlib v4.33.1）"；【引用】caveat：用直接 `lean` 调用而非 `lake build`（77 模块样本与 lake build 逐字节相同，全量未比对） |
| 2 | **5 条主定理 `#print axioms` 只有标准 3 公理** | ❌ 依赖 1 | 【引用】MIT `audit.log`：`[propext, Classical.choice, Quot.sound]`；环境中 15 条 axiom 全在 `Init` |
| 3 | **无 `sorry/admit/axiom/unsafe` 等** | ✅ | 【实测】0（§2.4）；与 README 自报一致 |
| 4 | **语句忠实**：`RiemannHypothesis` 是 Mathlib 官方定义；4 个自定义语句与其名字相符 | ✅（文本比对） | 【实测】pinned Mathlib 源码 `Mathlib/NumberTheory/LSeries/RiemannZeta.lean` 第 185 行 `def RiemannHypothesis` 与仓库/README 引用**逐字一致**；`src/Statements.lean` 4 个定义已逐条阅读（ζ 零点在 1/2、Dirichlet L 非零/零点在 1/2） |
| 5 | **源码哈希 = 作者原始归档** | ✅ | 【实测】本地 `lean-toolchain` `3aac669c…`、`lakefile.toml` `b831ad8c…` 与前序记录一致；【引用】作者归档 `lean.tar.gz` 239,275,554 B、sha256 `9631b4f0…c7fc`（alpo.ge 14 个 part 拼接）；镜像 Releases 同值；MIT `project-oleans.sha256` 175,187 条 |
| 6 | **独立 kernel 重放**（leanchecker / nanoda / con-leche / lean4lean） | ❌ 需 50–100 GB RAM 机器 | 【引用】MIT 页：leanchecker 175,187/175,187 pass；nanoda accepts（28 min@80 线程）；con-leche master+compare accepts；lean4lean 175,187/175,187 pass；**Lean default/paranoid kernel 对 export 的重放仍 running** |
| 7 | **独立定义的算术交叉检查**（不依赖 Mathlib 的 zeta 定义） | ❌ 需构建 Robin1984 | 【实测/MIT 新页】2026-11-21 04:20 UTC 新增：与 `kimihiro64/Robin1984` 结合，得到两条无假设、不提 zeta 的除数不等式定理（Robin/Lagarias 型），`#print axioms` 只有 3 公理；Robin1984 `lake build` pass（4,435 jobs, exit 0），con-leche/nanoda/Lean paranoid 均接受 |
| 8 | **信任前提被明确** | ✅ | Lean kernel + Mathlib 定义本身是信任根；MIT 的 unsandboxed 构建 caveat 需照抄 |

**判定规则**：1–8 全部通过（或对第三方结果逐项核对哈希+原文）→ 可以写"该 Lean 仓库在 Lean/Mathlib 语义下证明了 RH 与 GRH"；任何一项红灯 → 最多写"未发现明显造假痕迹，但未独立验证"。**本机今天最多做到 3、4、5 三项。**

---

## 3. VSCode Lean 扩展实战（含当前为什么必然失败）

### 3.1 打开仓库后会发生什么（正常流程 vs 本机实际）

正常（有 toolchain + Mathlib 缓存时）：
1. 扩展激活（`onLanguage:markdown` + `onStartupFinished`，实测 package.json activationEvents）；
2. 读项目根 `lean-toolchain` → 要求 elan 的对应 toolchain；
3. 启动 `lean --server`（language server）→ InfoView 出现、Problem 面板填充、hover/go-to-def 可用；
4. 依赖 Mathlib oleans 存在时，打开 `src/Statements.lean` 秒级出结果（本机没有 oleans，即使 toolchain 就绪这里也会报 `unknown module prefix 'Mathlib'`）。

本机实际（14:45–16:02 那个 VSCode 会话）：
1. `lean --version` → **失败（exit -4058）**；
2. 自动装 elan（PowerShell 脚本，成功，elan 4.4.0）；
3. 按 `lean-toolchain` 装 v4.33.1 → **SSL 失败**；
4. 无 toolchain → language server 无法启动 → InfoView 永远空白；`toolchains/` 空。

### 3.2 面板与命令（在哪看什么）

| 位置 | 用途 |
|---|---|
| **InfoView / Lean InfoView**（右侧面板，或 `Lean: Toggle Info View`） | 光标处 goal/Tactic 状态；language server 活着时才会更新 |
| **Problems**（`Ctrl+Shift+M`） | Lean 报错/警告；toolchain 缺失的报错也会出现在这里（"cannot find lean" 类） |
| **Output**（`Ctrl+Shift+U` → 下拉选 **Lean Editor** / **Lean Server**） | 扩展日志：toolchain 检测、server 启动、异常 |
| **命令面板**（`Ctrl+Shift+P`） | `Lean: Restart File`、`Lean: Restart Server`、`Lean: Toggle Info View`、`Lake: Build`、`Lake: Clean` 等（本机扩展 0.0.242） |
| **日志磁盘位置** | `C:\Users\GU178\AppData\Roaming\Code\logs\<会话时间戳>\window1\exthost\output_logging_*\7-Lean Editor.log`；扩展宿主日志 `...\window1\exthost\exthost.log`（实测本机 lean 激活行：`ExtensionService#_doActivateExtension leanprover.lean4`） |
| **workspace 状态** | `C:\Users\GU178\AppData\Roaming\Code\User\workspaceStorage\<hash>\state.vscdb`（SQLite；`workspace.json` 记录打开的目录；hash `3d4536…` = `file:///d%3A/Rieman`） |

**怎么判断 language server 启动成功**：Output→Lean Editor 出现 `Starting Lean server` / 打印 `Lean (version …)`；InfoView 不再空白、光标处有 "no goals"/goal 列表；Problems 不再有 "lean executable not found"；`.lean` 文件顶部无红色报错。

### 3.3 两种正确架构（当前本机两种都没落地）

**架构 A：Windows 原生 Lean（VSCode 扩展 + Windows elan + Windows toolchain）**
- 现状：elan 已装（4.4.0），toolchain 空；
- 修复：把 v4.33.1 的 **windows** 版 toolchain 放进 elan 目录（§4.3），然后 VSCode 里 `Lean: Restart Server`；
- 优点：不用 WSL；D: 路径原生。缺点：Windows 侧 TLS（schannel）下载失败，需要 gh-proxy 手工补；Mathlib 缓存/lake 构建也在 Windows 上跑（D: 是 9p 以外的 NTFS，构建性能一般）。

**架构 B：WSL 远程（推荐）**
- 需要：VSCode 装 **Remote-WSL** 扩展（`ms-vscode-remote.remote-wsl`，**当前未装**）+ WSL 内 elan/toolchain/Mathlib；然后从 WSL 里 `code /mnt/d/Rieman/riemann-hypothesis-lean` 或 VSCode `WSL: Reopen Folder in WSL`；
- 之后扩展跑在 WSL 里（`~/.vscode-server` 会出现），调用 WSL 内 `~/.elan/bin/lean`/手动 PATH 的 toolchain，Linux 构建性能好、网络走 WSL 的 gh-proxy 重写；
- 本机现状：WSL 的 lean/lake 已由本次准备好（手动路径），VSCode 侧只缺 Remote-WSL 扩展和 `~/.elan` 标准安装（可用 §4 的方式补）。

> 结论：**没有 Remote-WSL 的 VSCode 永远看不到 WSL 里的 Lean**；这就是"我在 WSL 装了（其实没装）Lean，VSCode 里打开仓库却没反应"的技术原因。

---

## 4. 修复 / 安装路线（推荐 WSL 优先；命令可直接复制）

### 4.1 路线 1（推荐）：WSL 标准安装 elan + v4.33.1 + Mathlib 缓存

**第 0 步：让 GitHub 可下载**（前序会话已配置；本次实测仍生效，若新开 shell 需重配）：
```bash
git config --global url."https://gh-proxy.com/https://github.com/".insteadOf "https://github.com/"
git config --global --get-regexp 'url\.'   # 应有输出
```

**第 1 步：装 elan**（官方脚本可达但内部指向 GitHub，需绕行）：
```bash
# 官方脚本确实能下（实测 200，9823 B），但直接 `| sh` 会在下载 elan 二进制时卡 GitHub，所以：
mkdir -p /tmp/elan && cd /tmp/elan
curl -sSL --retry 3 -o elan.tar.gz \
  "https://gh-proxy.com/https://github.com/leanprover/elan/releases/download/v4.4.0/elan-x86_64-unknown-linux-gnu.tar.gz"
tar -xzf elan.tar.gz && ls -la          # 得到 elan-init 安装器
./elan-init -y --default-toolchain none # 安装到 ~/.elan
source "$HOME/.elan/env"
```
> 说明：`elan-init` 这一步【未实测】（本报告时间盒内只做到 toolchain 手动安装）；若它仍尝试联网下载，见备选：直接手动建 `~/.elan/toolchains/leanprover--lean4---v4.33.1`（把 §5-E1 解压好的 3.1 GB 目录链接/移入），并把 toolchain bin 目录软链到 `~/.elan/bin`。

**第 2 步：toolchain（本报告已完成，可直接复用）**：
```bash
# 本次已下载并解压到：
ls ~/rh-work/lean-test/lean33/lean-4.33.1-linux/bin/{lean,lake}
export PATH=$HOME/rh-work/lean-test/lean33/lean-4.33.1-linux/bin:$PATH
lean --version   # Lean (version 4.33.1, ... commit 819816b2..., Release)
```
若要从头复现下载（25 秒）：
```bash
mkdir -p ~/rh-work/lean-test/lean33 && cd ~/rh-work/lean-test/lean33
time curl -sSL --retry 3 -o lean-4.33.1-linux.zip \
  "https://gh-proxy.com/https://github.com/leanprover/lean4/releases/download/v4.33.1/lean-4.33.1-linux.zip"
python3 -m zipfile -e lean-4.33.1-linux.zip . && chmod -R u+rwX lean-4.33.1-linux
find lean-4.33.1-linux/bin -type f -exec chmod u+x {} +
```

**第 3 步：Mathlib（v4.33.1 源码已在本地，但 oleans 要重新拿）**：
```bash
cp -a /home/kiler/Windows-D/Rieman/riemann-hypothesis-lean "$HOME/rh-work/rh-check"  # 只读仓库的副本
cd "$HOME/rh-work/rh-check"
export PATH=$HOME/rh-work/lean-test/lean33/lean-4.33.1-linux/bin:$PATH
lake update                                   # 通过 gh-proxy 拉 pinned mathlib + 8 依赖
lake exe cache get                           # 官方 olean 缓存（约 1.5–3 GB 量级）
lake build Statements                        # 语句层检测
```
> 离线备选：本地已有 `~/rh-work/lean-test/mathlib4-src/`（v4.33.1 源码，9030 文件，sha256 `4906567b…6326`）；但作为 lake 依赖最好让 lake 用 manifest 自动 fetch（源码 tarball 没有 .git，lake 校验 rev 会麻烦），或在 `~/.lake/packages/mathlib` 手工放置并接受 warning。

**第 4 步：VSCode 侧（任选）**
- 推荐：Windows VSCode 装 **Remote-WSL** 扩展 → `WSL: Reopen Folder in WSL` → 打开 `/mnt/d/.../riemann-hypothesis-lean`；扩展会自动在 WSL 里找 `~/.elan`/PATH；用 `Lean: Restart Server` 重启。
- 或不折腾 WSL：走 §4.3 Windows 原生路线。

### 4.2 资源可行性估算

| 项目 | 估算 | 依据 |
|---|---|---|
| toolchain 磁盘 | 3.1 GB | 【实测】解压后 du |
| Mathlib（v4.33.1）源码 | ~0.3 GB | 【实测】23 MB tar.gz → 9030 文件（解压后约 250 MB）【引用】 |
| Mathlib oleans（cache get 后） | ~2 共–4 GB | 【实测】4.36.0 的 `.lake` 2.8–3.1 GB（同类量级） |
| 仓库副本 | 1.7 GB | 【实测】du |
| **语句层总计** | **≈ 8–10 GB 磁盘；RAM 峰值约 2–4 GB** | ✅ 本机 15 GB 可做（避开并发 python 任务时段） |
| 全量 `lake build Main` 磁盘 | 数十 GB oleans（推测 20–60 GB） | 【推测】按 Mathlib 8.8k 文件/3 GB 外推 175k 文件；MIT `project-oleans.sha256` 28.8 MB 清单 |
| 全量构建 RAM/CPU | 50–100+ GB RAM；云机器多核数小时 | 【引用】MIT：全量检查需 ~100 GB RAM / 70 GB disk；con-leche 需 ~50 GB RAM、64–80 线程跑 4–28 分钟 |
| **全量检测结论** | **本机不可行**（内存差一个数量级） | 15 GB vs 50–100 GB |

### 4.3 Windows 原生修复路线（若用户想保留 VSCode 本地形态）

1. **下载 Windows 版 toolchain（用 gh-proxy，已实测可达：HEAD 200，842,456,015 B）**：
```powershell
# PowerShell（Windows）
$u = "https://gh-proxy.com/https://github.com/leanprover/lean4/releases/download/v4.33.1/lean-4.33.1-windows.zip"
Invoke-WebRequest -Uri $u -OutFile "$env:TEMP\lean-4.33.1-windows.zip" -UseBasicParsing
# 解压（内层目录通常为 lean-4.33.1-windows/）
Expand-Archive "$env:TEMP\lean-4.33.1-windows.zip" -DestinationPath "$env:TEMP\lean33w" -Force
```
2. **放进 elan 的 toolchain 目录**（elan 命名规则：toolchain 名中 `/` 编码为 `--`，即 `leanprover--lean4---v4.33.1`）：
```powershell
$dest = "$env:USERPROFILE\.elan\toolchains\leanprover--lean4---v4.33.1"
New-Item -ItemType Directory -Force -Path $dest | Out-Null
# 把解压内容（bin/ lib/ include/ share/ …）复制进 $dest
Copy-Item "$env:TEMP\lean33w\lean-4.33.1-windows\*" $dest -Recurse -Force
& "$env:USERPROFILE\.elan\bin\lean.exe" --version   # 期望 Lean (version 4.33.1, ... windows)
```
> 该目录命名规则【已知惯例，未在本机 Windows 实测】；若 `elan show` 不识别，检查 `elan toolchain list` 输出并用 `elan default leanprover/lean4:v4.33.1` 指认。
3. 然后在 VSCode 里 `Lean: Restart Server`；Mathlib 仍跑 `lake exe cache get`（RWindows 侧网络可能仍需 gh-proxy/代理；Windows 侧 git 可配 `git config --global url."https://gh-proxy.com/https://github.com/".insteadOf ...`）。
4. 备选代理：若用户开启 Clash/系统代理，可给 elan 设 `HTTP_PROXY/HTTPS_PROXY` 后重试 `elan toolchain install`（schannel 吊销错误通常也能被代理绕开，但需真实代理可用；本机当前没有开 Clash 的端口）。

---

## 5. 本次最小实测记录（全部真实执行，结果为原始输出）

### E1. v4.33.1 官方 toolchain 下载 + 解压 + 版本验证
```text
[实测 16:44–16:46]
$ curl -sSL --retry 3 -o lean-4.33.1-linux.zip \
    "https://gh-proxy.com/https://github.com/leanprover/lean4/releases/download/v4.33.1/lean-4.33.1-linux.zip"
DONE http:200 bytes:896280645 speed:35255292B/s total:25.422584s     # 35.3 MB/s
$ python3 -m zipfile -e lean-4.33.1-linux.zip .                     # 12.6 s
$ du -sh lean-4.33.1-linux                                          # 3.1G
$ ./lean-4.33.1-linux/bin/lean --version
Lean (version 4.33.1, x86_64-unknown-linux-gnu, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6, Release)
$ ./lean-4.33.1-linux/bin/lake --version
Lake version 5.0.0-src+819816b (Lean version 4.33.1)
```
✅ **结论：本机现在有与仓库 `lean-toolchain` 完全一致的官方 Lean v4.33.1；且与 MIT 页记录的 Lean v4.33.1 commit `819816b2` 一致。**

### E2. v4.33.1 kernel 小实验（无 Mathlib）
`~/rh-work/lean-test/lean33-probe/probe.lean`：
```lean
theorem probe_add : 1 + 1 = 2 := rfl
#print axioms probe_add
theorem probe_imp (p q : Prop) (hp : p) (h : p → q) : q := h hp
#print axioms probe_imp
```
```text
[实测] $ ./bin/lean probe.lean
'probe_add' does not depend on any axioms
'probe_imp' does not depend on any axioms
[exit=0]
```
✅ toolchain 可编译、可做 `#print axioms`。

### E3. 只有 toolchain、没有 Mathlib oleans 时编译仓库语句 → 精确失败
```text
[实测] $ ./bin/lean /home/kiler/Windows-D/Rieman/riemann-hypothesis-lean/src/Statements.lean
src/Statements.lean:1:0: error: unknown module prefix 'Mathlib'
No directory 'Mathlib' or file 'Mathlib.olean' in the search path entries:
/home/kiler/rh-work/lean-test/lean33/lean-4.33.1-linux/lib/lean
[exit=1]
```
✅ 证明：**语句层检测的阻塞点就是 Mathlib oleans，而不是 toolchain**。

### E4. `lake` 能解析该项目（项目骨架实验，不动 D: 仓库）
```text
[实测] cp {lakefile.toml,lake-manifest.json,lean-toolchain,src/Statements.lean} → /tmp/lake-probe
$ lake --version
Lake version 5.0.0-src+819816b (Lean version 4.33.1)
$ timeout 12 lake build Statements
info: mathlib: cloning https://github.com/leanprover-community/mathlib4
[exit=124  # 被 timeout 终止；克隆走已配置的 gh-proxy 重写]
```
✅ lake 正确识别 `lean-toolchain`/manifest，并按 manifest 拉 pinned Mathlib —— 只差把 clone + cache get 跑完。

### E5. 网络/环境事实
见 §1.4 表（github 劫持、gh-proxy 35 MB/s、Windows gh-proxy HEAD 842 MB 等）。

### E6. 目标仓库身份与只读审计
```text
[实测] D: 仓库 HEAD = 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4（2026-11-20 23:13:33 +0800）
       ~/rh-full 克隆 HEAD 相同；.lean = 175,187；总行数 17,374,215；du 1.7G；.lake 不存在
       sha256(lean-toolchain)  = 3aac669c7a910ec2389f4e4f921b605adf6ebf2d1e0c9b9cd0be4d33f3f5db71
       sha256(lakefile.toml)   = b831ad8cac0babb7bf713433259bdfe5163e58c90734e86d71536d4e30ddec4c
```
静态扫描结果见 §2.4。

### E7. MIT 第三方核验页（08:47Z 实测）
```text
页面 sha256 = bbffa73cc8e43e952b65fc1ac01f781d0611a95df99b3bcc457e8960ca11b348（16,544 B）
"Page last updated 2026-11-21 04:20 UTC"（旧快照 2026-11-20 22:05 UTC，sha de7153ec…，12,782 B）
新增 "Arithmetic consequences"：与 kimihiro64/Robin1984 结合得到 Robin/Lagarias 型除数不等式（无假设、不提 zeta），
    组合定理 #print axioms 仅 propext/Classical.choice/Quot.sound；Robin1984 lake build pass（4,435 jobs, exit 0）。
仍 running：lake comparator（v4.36.0）end-to-end；Lean default/paranoid kernel replay of the export。
```

---

## 6. 结论与建议（按优先级）

### 6.1 现在马上能做的（0 成本）
1. **Ld 静态扫描已做完**（本报告 §2.4）：0 sorry/axiom/unsafe 等，1 个 `addDecl`、4 个 `maxHeartbeats 0`；与 README 自报一致。**注意：这只说明"没有明显作弊痕迹"，不构成证明。**
2. **语句文本比对已做完**：`RiemannHypothesis` 确为 pinned Mathlib 官方定义（`RiemannZeta.lean:185`，逐字一致）；4 条自定义语句逐条读过，名字与内容相符。**
3. VSCode 当前配置**必然失败**，原因已定位（§1.3/§3）：toolchain 下载 SSL 失败 + 无 Remote-WSL。

### 6.2 值得做的下一步（30–90 分钟，推荐）
**语句层检测（La）**：按 §4.1 第 0–3 步执行，产出：
- `lake build Statements` 成功日志；
- 这将是"独立复现的**第一层语义验证**"：用官方 Mathlib 定义确认 5 条主语句成立（不是证明，是语句与定义吻合）。
- 若成功，可再对 4 条自定义语句做**语义等价**人工复核（如 `RiemannZetaZerosOnLine` 与 Mathlib `RiemannHypothesis` 的等价性可另写 lemma 用 `lake env lean` 验证）。
- 风险提示：Mathlib cache 下载 ~1.5–3 GB（>Lead 的 1 GB 单次下载阈值，**执行前请 Lead 确认**）；先暂停/避开并发 python 数值任务，避免 15 GB 内存吃紧。

### 6.3 本机做不了的（必须换机器，不要浪费时间）
- `lake build Main` 全量（17.4M 行）：50–100+ GB RAM 级，云机器数小时~数天；本机 15 GB 会 OOM。
- Lc 公理审计（依赖全量构建）、Le 的独立 kernel 重放（MIT 明说 ~100 GB RAM / 70 GB disk；con-leche ~50 GB RAM）。
- 建议：租 64–128 核 / 100–200 GB RAM / 200 GB 磁盘的云机，或用第三方（MIT/Deicyde）结果 + 哈希比对（§2.5 判据 5、8）。

### 6.4 对"RH 是否被 Lean 证明"的当前诚实判据
- **可以写**：仓库源码完整、HEAD 一致、无 sorry/axiom 等明显作弊痕迹；语句忠实于 Mathlib 定义；第三方（MIT 页面）报告了编译/kernel 级通过结果，且其核对文件哈希与本地一致。
- **不能写**：本地独立复现了编译或 kernel 检查（本机做不到）；MIT 页仍有两项 running（lake comparator、Lean default/paranoid kernel replay of export），且 MIT 自述构建是 unsandboxed、非 `lake build` 方式。
- 第三方页面已于 **2026-11-21 04:20 UTC** 更新（新增 Robin/Lagarias 算术交叉检查），请 Lead 后续引用时用新快照，不要再用 11:xx CST 的旧快照。**
- 正确表述模板："按 MIT（Sutherland）页面 2026-11-21 04:20 UTC 版本：175,187 模块编译通过、5 条主定理仅依赖 3 条标准公理、leanchecker/nanoda/con-leche/lean4lean 接受；lake comparator 与 Lean kernel export replay 仍在进行；本地独立完成的只有源码静态审计与语句文本比对（未复现编译/kernel 级检查）。"

### 6.5 对团队现状的两条澄清
1. **`~/rh-work/lean-test/lean33/` 的 16:44 下载与 16:45 解压是本人（lean-verifier）执行的**，属于 task-2 的"最小实测"，不是"另一个并发 DSH 会话"——不存在重复下载/冲突，Lead 可直接复用这套 toolchain。
2. 本报告只读目标仓库；新增写入仅：`$HOME/rh-work/lean-test/lean33*/`、`/tmp/*`、本报告文件。

---

## 附录 A：命令速查（复制即用）

```bash
# 0) 工具链
export PATH=$HOME/rh-work/lean-test/lean33/lean-4.33.1-linux/bin:$PATH
lean --version && lake --version

# 1) 静态扫描（Ld）——在 ~/rh-full 或 D: 仓库
cd ~/rh-full
git grep -I -l -E '\bsorry\b|sorryAx|\badmit\b|^\s*axiom\s|\bunsafe\b|native_decide|ofReduceBool' -- '*.lean'
git grep -I -l -E 'addDecl|maxHeartbeats\s+0|mkSorry|skipKernelTC' -- '*.lean'
git grep -c '^' -- '*.lean' | awk -F: '{s+=$NF} END {print s}'   # 17,374,215

# 2) 语句层（La）——保持 D: 仓库只读，在副本里跑
cp -a /home/kiler/Windows-D/Rieman/riemann-hypothesis-lean "$HOME/rh-work/rh-check"
cd "$HOME/rh-work/rh-check"
export PATH=$HOME/rh-work/lean-test/lean33/lean-4.33.1-linux/bin:$PATH
lake update && lake exe cache get && time lake build Statements

# 3) 构建层（Lb）——本机不要跑；云机器上：
time lake build Main --jobs=$(nproc) 2>&1 | tee build-Main.log

# 4) 公理审计（Lc）——Lb 成功后
cat > Check.lean <<'EOF'
import Main
#print axioms riemannHypothesis
#print axioms riemannZeta_eq_zero_re
#print axioms LFunction_ne_zero_of_half_lt_re
#print axioms LFunction_eq_zero_re
#print axioms LFunction_eq_zero_re_of_isPrimitive
EOF
lake env lean Check.lean

# 5) GitHub 不通时（WSL 全局）
git config --global url."https://gh-proxy.com/https://github.com/".insteadOf "https://github.com/"
# 下载任意 GitHub release 文件：https://gh-proxy.com/<原 github URL>
```

## 附录 B：证据路径

| 内容 | 路径 |
|---|---|
| 本报告 | `_rh-work/lean-verifier/lean-detection-report.md` |
| 本次下载的 v4.33.1 toolchain | `~/rh-work/lean-test/lean33/lean-4.33.1-linux/`（3.1 GB，已可执行） |
| v4.33.1 standalone probe | `~/rh-work/lean-test/lean33-probe/probe.lean`（输出已记录于 §5-E2） |
| 前序 4.36.0 toolchain + Mathlib 4.36.0 | `~/rh-work/lean-test/lean4/`、`~/rh-work/lean-test/mathlib36/`（.lake 2.8–3.1 GB） |
| 仓库 pin 的 Mathlib v4.33.1 源码 | `~/rh-work/lean-test/mathlib4-src/`（9030 文件） |
| MIT 页面最新快照 | `/tmp/grh_page_final2.html`（sha256 `bbffa73c…b348`） |
| Windows Lean 扩展失败日志 | `C:\Users\GU178\AppData\Roaming\Code\logs\20261121T144340\window1\exthost\output_logging_20261121T144346\7-Lean Editor.log` |
| Windows elan 状态 | `C:\Users\GU178\.elan\`（settings.toml / known-projects / toolchains 空） |
| 前序 phase5 Lean 报告 | `_rh-work/goldbach-attack/phase5/lean-phase5.md`（6 条引理过 kernel） |
