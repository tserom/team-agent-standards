# Gitee 工单 → 分支迭代号 · 人读完整版

> Agent 短规则：`guidelines/gitee-branch-iteration.md`  
> kb 习惯补充：`~/Mycodes/kb/domains/workflow/company-git-branch.md`  
> 版本：2026-09-22

---

## 1. 问题

开功能分支时若从**当前本地分支名**或「同仓最近最大迭代号」抄数字，会把工单挂到错误迭代（例如工单在迭代 23，本地还在 `…-22-…` 分支上工作）。

真源是 Gitee 工单上的 **`scrum_sprint`**。

---

## 2. 流程

```text
用户给链接/工单号
  → 抽出 ident（IKGB7L）
  → Gitee 企业 API / MCP 拉详情
  → scrum_sprint.title 解析数字
  → feature/<基线>-<数字>-<人名>-<工单>[-简述]
```

### 企业与项目 ID（易混）

| 字段 | 值 | 说明 |
|------|-----|------|
| 企业 path | `bitsun_1` | |
| `enterprise_id` | **12478212** | MCP / API 的企业主键 |
| URL `projects/753146` | `program_id` | **不是** enterprise_id |

### 解析示例

| `scrum_sprint.title` | 分支里的迭代段 |
|----------------------|----------------|
| `标品迭代23(0921-1007)` | `23` |
| （爱唯等偶发文案）`迭代18` | 跟仓内习惯，常写 `迭代18` |

### 失败兜底

- 401 → 先授权 MCP / token，再重试  
- 仍失败或工单未挂 sprint → **问用户**，不要猜

---

## 3. MUST / MUST NOT

| ✅ MUST | ❌ MUST NOT |
|---------|-------------|
| 有 Gitee 工单时从 `scrum_sprint.title` 取迭代 | 抄当前本地分支上的迭代数字 |
| 问清基线（`release-tx` / `aiwei-*`）再拉支 | 用「最近 feature 最大迭代」代替本工单 |
| 401/无 sprint 时问人 | 未挂 sprint 时自己编数字 |

---

## 4. 与其它约定

- 分支公式、MR 目标线：kb `company-git-branch.md`、`git-commit-mr` guideline  
- 主工作区脏文件：dirty-workspace / worktree（勿 stash 冲掉半成品）

---

## 5. CR 清单

- [ ] 分支名迭代号 = 该工单 `scrum_sprint.title` 中的数字？
- [ ] `enterprise_id` 未误用 URL 里的 program id？
- [ ] MR target = 当初拉支的基线？
