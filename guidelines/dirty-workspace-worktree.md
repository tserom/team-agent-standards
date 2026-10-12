# 功能分支一律 worktree；主工作区挂基线

开功能分支 / 动手改需求代码前：主工作区（日常打开的那个 checkout）**保持产品线基线**；新功能分支一律用 `git worktree` 旁路。与 [`git-commit-mr.md`](git-commit-mr.md) 配合：合代码仍只推功能分支并建 MR/PR；本条管**在哪改、怎么开分支、何时汇报可清理项**。

人读完整版：`docs/standards/dirty-workspace-worktree.md`  
kb 工作流/踩坑（公司前端习惯拼接）：`~/Mycodes/kb/domains/workflow/dirty-workspace-worktree.md`

---

## 决策表（命中即停）

| 主工作区状态 | MUST | MUST NOT |
|---|---|---|
| **干净**（无未提交改动） | `git worktree add`：从正确基线建功能分支 → 在 worktree 内改 → commit → push → MR；主区继续挂基线 | 在主工作区 `switch -c` / 直接改功能分支 |
| **仅调试用 proxy**（脏路径集合恰好是代理配置，公司前端常见：`config/proxy.ts`） | **默认**可 `git stash` 或 discard（短问 discard vs stash，或按用户当场指示）；然后仍按上行走 worktree。**不必**再问「算不算 proxy」 | 把业务半成品误当成 proxy；仅为 proxy 脏就改回「主区开功能分支」 |
| **其它未提交改动**（别的 agent / 忘了交 / 半成品 / **混合脏** / **不确定**） | **不动**主工作区脏文件；`git worktree` 另开目录，基于目标基线建功能分支，在那边改、交、提 MR | `git stash`、discard、硬切分支带走/冲掉未提交改动 |

**判定**：未提交路径**恰好**为上述 proxy 文件 → 按「仅 proxy」行处理完 proxy，再开 worktree。若还含其它路径、或看不清 → **默认 worktree**（可先问一句）。

口诀：**功能旁路做；主区挂基线；只有 proxy 能扔；可清只汇报。**

---

## 基线分支（开 worktree / 开功能分支时）

按需求线选基线，**不要**默认仓库 `master` / `main`：

| 线索 | 基线（示例） |
|---|---|
| 铁血 / `TX*` / `release-tx-*` 工单 | 最新 `origin/release-tx` |
| 爱唯 / `aiwei-*` | 对应 `aiwei-*` 基线 |
| 用户明确指定 | 听用户的 |

功能分支命名与团队现有约定一致（如 `feature/release-tx-<迭代号>-<作者>-<工单号>-简述`）。  
**迭代号**：有 Gitee 工单时从工单 `scrum_sprint` 读取，见 [`gitee-branch-iteration.md`](gitee-branch-iteration.md)；禁止抄当前本地分支。

---

## Worktree 要点

- 目的：主工作区稳定挂基线；功能开发隔离在旁路目录 + 旁路分支。
- 目录：项目已有 `.worktrees/` / `worktrees/` 则用之；否则 `.worktrees/`，且必须被 gitignore。
- 已在 linked worktree 内：不要再套一层；直接在该隔离目录继续。
- 优先平台原生 worktree 工具；否则 `git worktree add`。
- 完成后：在 worktree 功能分支 commit → push → MR（target = 所选基线）。

### 清理门槛（人删时须同时满足）

1. MR 已合入基线（或确认不再需要该 checkout）
2. 该 worktree **无未提交改动**
3. **无未推送提交**（相对 upstream ahead=0，或提交已在远端/基线）

勿在脏 / 有未推送 commit 时删。

### 清理：Agent 只汇报，不代删

| 何时 | Agent MUST | Agent MUST NOT |
|---|---|---|
| 用户说 MR **已合入** / finishing 分支 / 「合到 release-tx 了」 | `git worktree list`，标出**满足门槛、可清**的路径与分支 | `git worktree remove` / `prune`（除非用户明确点名「删掉 xxx」） |
| **新建** worktree **之前** | `git worktree list`；若有明显可清项，在回复里提醒积压 | 为「腾地方」自动 `remove` |
| 用户要求定期检查 / 清点 worktree | 列出全部附属 worktree + 是否满足清理门槛 | 定时硬删、批量静默删除 |

不要靠每日定时硬删 worktree（易误伤「当天未 commit」的目录）。清理以**人工定期检查**为主。

---

## PR 勾选

- [ ] 动手前是否看过 `git status`？
- [ ] 新功能分支是否在 worktree 内（主区未直接 `switch -c`）？
- [ ] 仅 `config/proxy.ts`（或同类仅代理配置）脏时，是否已 discard/stash 后再开 worktree？
- [ ] 脏且非「仅 proxy」时，是否未动主区、已用 worktree？
- [ ] 功能分支是否基于正确产品线基线（如铁血 → `release-tx`）？
- [ ] 合入后是否只汇报可清项、未擅自 `worktree remove`？
- [ ] 开新 worktree 前是否扫过 list 并提醒积压（仍不代删）？
