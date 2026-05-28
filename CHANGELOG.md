# Changelog

## Unreleased

### Added

- `guidelines/api-layering.md`：API 分层（抽象/封装/复用）L0–L3 与 5 问决策；对应 Cursor 规则 `api-layering-decision.mdc`（`alwaysApply: true`）。
- `docs/standards/api-abstraction-encapsulation-reuse*.md`：完整规范与一页纸（中/英）。
- `docs/REPOSITORY_STRUCTURE.md`：本仓库职能与各目录说明。
- `guidelines/promote-to-team-standards.md` + `promote-to-team-standards.mdc`：Agent 在可复用规则/Skill 时提醒晋升团队真源。
- `docs/skills/README.md`：团队 Skill 模板目录约定。

### Changed

- README / `docs/other-agents.md`：区分 Cursor 首次安装与**增量更新**（`cp …/*.mdc`，避免覆盖项目专用 rules）。
- `build.py` 构建结束提示默认打印增量复制命令。

- 构建产物改为可见路径（如 `generated/cursor/rules/`，不再生成隐藏的 `.cursor` 目录）。
- 构建输出改为 `generated/<agent-id>/` 分目录，不再提供安装脚本。
- **方案 B**：各 Agent 产物在 `generated/<agent-id>/` 下，构建只清空该子目录。
- Git 合代码规范改为通用 MR/PR 草稿流程（不限 GitLab / `test`）。

### Added

- **工具无关真源** `guidelines/*.md`（Karpathy、React 可读性、回复文件表、Git MR）。
- `agent-manifest.json`：Agent 列表；输出目录固定为 `generated/<id>/`。
- `docs/other-agents.md`：各工具 `build.py <id>` 与复制说明。
- `scripts/build.py` / `scripts/build.sh`：统一构建入口。

### Removed

- `install-cursor.sh`、`install-agents-md.sh`、`install-all.sh`、`install-to-project.sh`。
- 手写 `rules/*.mdc` 作为真源（改为构建产物）。
