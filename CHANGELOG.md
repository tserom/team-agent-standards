# Changelog

## Unreleased

### Changed

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
