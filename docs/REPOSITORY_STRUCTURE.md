# team-agent-standards · 仓库职能与目录说明

本仓库为团队 **跨项目、跨 Agent** 的协作规范真源。业务仓库只放**本项目专用**规则；可复用的约定集中在本仓库维护、构建、再复制到各项目。

---

## 1. 本仓库做什么 / 不做什么

| 做 | 不做 |
|----|------|
| 全团队通用的编码行为、Git/MR、回复格式、API 分层等 | 某个业务域的双表接口清单（放业务仓库 OpenSpec / `*-api-call-map.md`） |
| 从 `guidelines/*.md` **构建** Cursor / Claude / Copilot 等产物 | 替代业务项目的 `config/routes`、页面实现 |
| 人读长文、一页纸、评审清单（`docs/`） | 在业务仓库长期手改 `generated/` 里的 `.mdc`（会漂移） |

---

## 2. 目录职能一览

```text
team-agent-standards/
├── guidelines/              # ★ Agent 规则真源（唯一应改的规则正文）
├── docs/
│   ├── REPOSITORY_STRUCTURE.md   # 本文件：仓库职能
│   ├── other-agents.md           # 各 Agent 构建与复制命令
│   ├── standards/                # 人读长文、决策表、一页纸（非构建真源）
│   └── skills/                   # 可复用 Skill 模板（需手动复制到业务项目）
├── templates/               # 构建时拼接的 header（AGENTS.md、CLAUDE 等）
├── cursor-manifest.json     # Cursor：guideline → .mdc 映射（alwaysApply、globs）
├── agent-manifest.json      # 各 Agent 产物路径与 installTo
├── scripts/build.py         # 构建入口
├── generated/<agent-id>/    # 构建产物（git 忽略，勿当真源编辑）
├── CHANGELOG.md
└── README.md
```

### `guidelines/*.md`（真源）

- **职能**：给 AI 读的**短而硬**的约束（MUST/NOT、决策表、清单）。
- **命名**：`kebab-case.md`，如 `api-layering.md`、`git-commit-mr.md`。
- **长度**：建议单文件可控在一屏～数屏；过长拆到 `docs/standards/` 并在 guideline 里链过去。
- **变更后**：改 `cursor-manifest.json`（若新增）→ `python3 scripts/build.py cursor`（及其它 Agent）→ 复制到业务项目。

### `docs/standards/*.md`（人读配套）

- **职能**：评审、培训、飞书粘贴用的**完整版**（案例、§变更记录、Mermaid）。
- **与 guidelines 关系**：guideline = Agent 执行摘要；standards = 人读真源细节。二者内容冲突时，**以 guidelines + 合并后的 MR 为准**，并同步改两处。

### `docs/skills/`（Skill 模板，可选）

- **职能**：可跨项目复用的 `SKILL.md` 模板（如某类表格、脚手架流程）。
- **注意**：当前 **未** 接入 `build.py`；采纳后由业务项目在 `.cursor/skills/` 引用或复制。见 `docs/skills/README.md`。

### `cursor-manifest.json`

- **职能**：定义每条 Cursor 规则的 `output` 文件名、`guideline` 源文件、`description`、`alwaysApply`、`globs`。
- **新增团队规则必改此文件**，否则 `build.py cursor` 不会产出对应 `.mdc`。

### `generated/`

- **职能**：构建输出；**禁止**作为编辑真源。
- **同步**：`cp -R generated/cursor/rules → 业务项目/.cursor/rules/`。

### 业务项目内应保留什么

| 路径 | 放什么 |
|------|--------|
| `.cursor/rules/*-业务名*.mdc` | 本仓库/本域专用（如双表速查、OpenSpec 交互） |
| `.cursor/skills/` | 项目或从 `team-agent-standards/docs/skills` 复制的 Skill |
| `docs/standards/`（可选） | 从本仓库复制的长文副本，或仅链到 team 仓库 |

---

## 3. 什么内容应「晋升」到本仓库

适合晋升：

- 在 **≥2 个业务项目** 重复出现的约定，或明确「全前端适用」。
- 新总结的 **决策表 / MUST-NOT**（如 API L0–L3）。
- 统一的 **PR 回复、Git/MR、React 可读性** 等。

保留在业务项目：

- 单需求 OpenSpec、`interactions/*-api-call-map.md`。
- 单页面的 BsSulaQueryTable 字段说明、路由菜单。
- 与单一后端接口强绑定的文案。

---

## 4. 新增一条团队规范的流程

1. 在 `guidelines/` 新增或修改 `.md`。
2. 若需人读长文，在 `docs/standards/` 补充（可选）。
3. 编辑 `cursor-manifest.json` 增加 rule 条目（`output`、`guideline`、`alwaysApply`、`globs`）。
4. `python3 scripts/build.py cursor`（及团队在用的其它 Agent id）。
5. 更新 `CHANGELOG.md`。
6. MR 合并后，各业务项目执行复制命令并提交。
7. 若创建了 Skill 模板，放在 `docs/skills/<name>/` 并更新 `docs/skills/README.md`。

---

## 5. 与 Cursor User Rules 的关系

- **不要**把团队通用规则只放在本机 `~/.cursor/rules`（无法版本化、同事不同步）。
- 真源在本仓库；本机与各项目的 `.cursor/rules` 均视为 **构建副本**。

---

## 6. 维护人速查

| 我想… | 去… |
|--------|-----|
| 改 Agent 必遵约束 | `guidelines/` |
| 改飞书/评审长文 | `docs/standards/` |
| 加 Cursor 规则文件 | `cursor-manifest.json` + build |
| 加可安装 Skill 模板 | `docs/skills/` |
| 查复制到项目的命令 | `README.md`、`docs/other-agents.md` |
