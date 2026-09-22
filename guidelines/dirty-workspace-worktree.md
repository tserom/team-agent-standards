# 脏工作区：优先 worktree，慎用 stash / discard

开始改代码或开功能分支前，先判断**当前主工作区**（日常打开的那个 checkout）是否干净。与 [`git-commit-mr.md`](git-commit-mr.md) 配合：合代码仍只推功能分支并建 MR/PR；本条管**未提交现场怎么处理**。

人读完整版：`docs/standards/dirty-workspace-worktree.md`  
kb 工作流/踩坑（公司前端习惯拼接）：`~/Mycodes/kb/domains/workflow/dirty-workspace-worktree.md`

---

## 决策表（命中即停）

| 主工作区状态 | MUST | MUST NOT |
|---|---|---|
| **干净**（无未提交改动） | 在主工作区切到正确基线 → 开功能分支 → 改代码 → commit → push → MR | 为「仪式感」无故开 worktree |
| **仅调试用 proxy 改动**，且用户确认可丢/可暂存 | 可 `git stash`，或按用户指示 discard，再按「干净」走 | 把业务半成品误当成 proxy |
| **其它未提交改动**（别的 agent / 忘了交 / 半成品 / **不确定**） | **不动**主工作区脏文件；用 `git worktree` 另开目录，基于目标基线建功能分支，在那边改、交、提 MR | `git stash`、discard、硬切分支带走/冲掉未提交改动 |

**不确定是不是 proxy** → 先问用户一句，**默认按「其它未提交」走 worktree**。

---

## 基线分支（开 worktree / 开功能分支时）

按需求线选基线，**不要**默认仓库 `master` / `main`：

| 线索 | 基线（示例） |
|---|---|
| 铁血 / `TX*` / `release-tx-*` 工单 | 最新 `origin/release-tx` |
| 爱唯 / `aiwei-*` | 对应 `aiwei-*` 基线 |
| 用户明确指定 | 听用户的 |

功能分支命名与团队现有约定一致（如 `feature/release-tx-22-<作者>-<工单号>-简述`）。

---

## Worktree 要点

- 目的：保护主工作区未提交现场；同一仓库另一目录 + 另一分支。
- 目录：项目已有 `.worktrees/` / `worktrees/` 则用之；否则 `.worktrees/`，且必须被 gitignore。
- 已在 linked worktree 内：不要再套一层；直接在该隔离目录继续。
- 优先平台原生 worktree 工具；否则 `git worktree add`。
- 完成后：在 worktree 功能分支 commit → push → MR（target = 所选基线）。

---

## PR 勾选

- [ ] 动手前是否看过 `git status`？
- [ ] 脏且非「已确认可丢的 proxy」时，是否用了 worktree 而非 stash/discard？
- [ ] 功能分支是否基于正确产品线基线（如铁血 → `release-tx`）？
