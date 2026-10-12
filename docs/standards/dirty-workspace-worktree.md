# 功能分支一律 worktree；主工作区挂基线

配套 Agent 短规则：`guidelines/dirty-workspace-worktree.md`。

## 背景

主工作区（Cursor 日常打开的那个 checkout）适合长期挂产品线基线（如 `release-tx`），不宜在上面反复 `switch` 功能分支：

- 另一个 Agent / 并行会话可能正在主区改
- 上次改完可能忘了 commit
- 仅本地调试用的 proxy / 环境开关（公司前端常见：`config/proxy.ts`）
- 功能分支与基线切换频繁时，容易把无关 diff 带到错误分支

**默认**：新功能分支一律 `git worktree` 旁路开发。  
**例外（所见即所得）**：脏路径集合**恰好**是调试 proxy 时，可 discard/stash 清掉 proxy，**然后仍开 worktree**做功能——不要仅为 proxy 脏就改回「主区开功能分支」。

## 决策

```mermaid
flowchart TD
  A[开始改代码 / 开功能分支] --> B{git status 干净?}
  B -->|是| G[git worktree: 基线建功能分支]
  B -->|否| D{脏路径恰好仅为调试 proxy?}
  D -->|是| E[短问 discard 或 stash] --> G
  D -->|否或不确定| F[不动主工作区]
  F --> G
  G --> H[在 worktree 内改 → commit → push → MR]
  H --> I[合入后: list + 汇报可清项; 不代删]
```

「恰好仅为调试 proxy」判定：未提交文件集合是 `config/proxy.ts`（或同仓约定的仅代理配置路径），**不含**其它业务文件。混合脏 → 不动主区，直接 worktree。

## 示例

| 场景 | 做法 |
|---|---|
| `git status` 干净，工单 IKFMUZ 铁血现场 | `git fetch` → `.worktrees/…` 从 `origin/release-tx` 开 `feature/release-tx-…-IKFMUZ-…`，在 worktree 改；主区保持基线 |
| 仅 `M config/proxy.ts`（本地代理指向） | 短问 discard vs stash → 处理后仍开 worktree；**不要**回主区开功能分支 |
| 主工作区有未提交业务 diff，又要开新铁血单 | 留着主工作区不动；worktree 从 `origin/release-tx` 开新分支做新单 |
| `proxy.ts` + 其它业务文件一起脏 | 按「其它脏」→ worktree；勿把业务半成品当 proxy 扔掉 |
| 看不清未提交是什么 | 问用户；问之前默认 worktree |
| MR 已合入 | Agent `worktree list` 标出可清项；**人**定期手动 `remove` |

## MUST / MUST NOT

| MUST | MUST NOT |
|---|---|
| 动手前看 `git status` | 在主工作区为新需求 `switch -c` 功能分支 |
| 新功能分支一律 worktree；主区挂基线 | 对非「仅 proxy」脏文件擅自 stash / discard |
| 仅 proxy 路径脏 → discard/stash 后再开 worktree | 仅为 proxy 脏就改回主区开分支 |
| 脏且非仅 proxy → 不动主区 + worktree | 默认从 `master`/`main` 开铁血单 |
| worktree 功能分支基于正确产品线基线 | 在主工作区硬切分支「带走」未确认归属的改动 |
| MR target = 该基线 | Agent 擅自 `worktree remove` / 定时硬删 |
| 合入后 list + 汇报可清项；清理靠人工定期检查 | 在有未提交改动 / 未推送 commit 时删 worktree |

## 清理条件（磁盘）

同时满足才可删附属 worktree（**由人执行**，或人明确点名后 Agent 代删）：

1. 已合进目标基线（或确认不再需要该 checkout）
2. worktree 内无未提交改动
3. 无未推送提交（相对 upstream ahead=0，或提交已在远端/基线）

### 何时去检查（触发）

事件驱动汇报 + 人工定期清理；不靠每日定时硬删：

| 触发 | Agent / 人 |
|---|---|
| 用户确认 MR 已合入 / finishing 该分支 | Agent **立刻** `worktree list`，标出满足条件的可清项；**不**自动 `remove` |
| 准备 `git worktree add` 开新目录前 | 先扫现有 list；有积压则提醒，仍不代删 |
| 人工定期检查（推荐） | 人按门槛决定 `remove`；需要时可让 Agent 只做清点 |

```bash
git worktree list
# 对每个附属路径：干净？ ahead=0？已在基线？ → 人决定是否 remove
git worktree remove .worktrees/<名>   # 人工或明确授权后
git worktree prune
```

## 与其它规范的关系

- 合代码、连续 commit 文案：`guidelines/git-commit-mr.md`
- Superpowers `using-git-worktrees`：隔离目录创建细节可参照；**是否**开 worktree 以本决策表为准（默认一律开）
- kb 工作流镜像：`~/Mycodes/kb/domains/workflow/dirty-workspace-worktree.md`（与 `company-git-branch` 拼接）
