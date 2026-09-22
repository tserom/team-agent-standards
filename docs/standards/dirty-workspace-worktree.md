# 脏工作区与 git worktree

配套 Agent 短规则：`guidelines/dirty-workspace-worktree.md`。

## 背景

主工作区常会留下未提交改动，来源未必是「当前需求」：

- 另一个 Agent / 并行会话正在改
- 上次改完忘了 commit
- 仅本地调试用的 proxy / 环境开关

若一律 `stash` 或 discard，可能弄丢别人的半成品，或把调试改动和业务改动搅在一起。若一律在脏目录上硬切分支，又可能把无关 diff 带到错误分支。

## 决策

```mermaid
flowchart TD
  A[开始改代码 / 开功能分支] --> B{git status 干净?}
  B -->|是| C[主工作区: 正确基线 → 功能分支 → 改 → MR]
  B -->|否| D{仅调试 proxy 且用户确认可丢/可暂存?}
  D -->|是| E[stash 或 discard] --> C
  D -->|否或不确定| F[不动主工作区]
  F --> G[git worktree: 基线建功能分支]
  G --> H[在 worktree 内改 → commit → push → MR]
```

## 示例

| 场景 | 做法 |
|---|---|
| `git status` 干净，工单 IKFMUZ 铁血现场 | `git fetch` → 从 `origin/release-tx` 开 `feature/release-tx-…-IKFMUZ-…`，在主工作区改 |
| 仅改了本地 proxy 指向测试环境，用户说可以丢掉 | discard 或 stash 后，再按上条 |
| 主工作区有未提交业务 diff，又要开新铁血单 | 留着主工作区不动；`.worktrees/…` 从 `origin/release-tx` 开新分支做新单 |
| 看不清未提交是什么 | 问用户；问之前默认 worktree |

## MUST / MUST NOT

| MUST | MUST NOT |
|---|---|
| 动手前看 `git status` | 对非 proxy 脏文件擅自 stash / discard |
| 脏且非确认可丢的 proxy → worktree | 默认从 `master`/`main` 开铁血单 |
| worktree 功能分支基于正确产品线基线 | 在主工作区硬切分支「带走」未确认归属的改动 |
| MR target = 该基线 | 为干净工作区无故套 worktree |

## 与其它规范的关系

- 合代码、连续 commit 文案：`guidelines/git-commit-mr.md`
- Superpowers `using-git-worktrees`：隔离目录创建细节可参照；**是否**开 worktree 以本决策表为准
