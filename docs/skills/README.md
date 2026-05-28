# 团队 Skill 模板（`docs/skills/`）

## 职能

存放可跨业务项目复用的 **Cursor Agent Skill**（`SKILL.md`）模板。与 `guidelines/` 区别：

| | `guidelines/` | `docs/skills/` |
|---|----------------|----------------|
| 产物 | 经 `build.py` 生成 `.mdc` / `AGENTS.md` 等 | **不**参与构建，需手动复制或 submodule |
| 形态 | 规则、约束、决策表 | 任务流程、工具链、领域 playbook |
| 安装 | `cp generated/cursor/rules/…` | `cp -R docs/skills/foo 业务项目/.cursor/skills/foo` |

## 目录约定

```text
docs/skills/
  README.md           # 本说明
  <skill-name>/
    SKILL.md          # Skill 正文（与 Cursor skill 格式一致）
```

## 何时晋升到此处

- 多个项目会用到同一套**操作步骤**（如 BsSulaQueryTable、页面脚手架）。
- 内容偏「怎么做」而非「禁止做什么」（禁止类放 `guidelines/`）。

## 采纳后

1. 在本目录新增 `<skill-name>/SKILL.md` 并 MR。
2. 在业务项目 `.cursor/skills/` **按目录**复制，例如 `cp -R docs/skills/<skill-name> 项目/.cursor/skills/`（勿 `cp -R docs/skills/` 整目录，以免覆盖项目自有 skill）。
3. 在 `CHANGELOG.md` 记录。
