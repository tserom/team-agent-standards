# 其他 Agent 配置说明

规范真源在 `guidelines/*.md`。采用 **方案 B**：每个 Agent 对应 `generated/<agent-id>/`；构建产物使用**可见目录名**（无 `.cursor` 等隐藏文件夹），复制到业务项目时再放到工具要求的路径。

```bash
python3 scripts/build.py --list
python3 scripts/build.py cursor
python3 scripts/build.py claude
```

## 目录结构（构建产物，访达可见）

```text
generated/
  cursor/rules/*.mdc
  claude/CLAUDE.md
  copilot/github/copilot-instructions.md
  agents-md/AGENTS.md
  windsurf/windsurfrules
  cline/clinerules
  aider/CONVENTIONS.md
  continue/continue/rules/team-standards.md
```

## Agent 与复制命令

| 命令 | 工具 | 构建产物 | 复制到业务项目 |
|------|------|----------|----------------|
| `build.py cursor` | Cursor | `generated/cursor/rules/` | 见下方示例 |
| `build.py claude` | Claude Code | `generated/claude/CLAUDE.md` | `cp generated/claude/CLAUDE.md 项目根/` |
| `build.py copilot` | GitHub Copilot | `generated/copilot/github/...` | `mkdir -p 项目/.github && cp ... 项目/.github/` |
| `build.py agents-md` | Copilot Agent / Codex 等 | `generated/agents-md/AGENTS.md` | `cp ... 项目根/` |
| `build.py windsurf` | Windsurf | `generated/windsurf/windsurfrules` | `cp ... 项目/.windsurfrules` |
| `build.py cline` | Cline | `generated/cline/clinerules` | `cp ... 项目/.clinerules` |
| `build.py aider` | Aider | `generated/aider/CONVENTIONS.md` | `cp ... 项目根/` |
| `build.py continue` | Continue | `generated/continue/continue/rules/` | `mkdir -p 项目/.continue && cp -R generated/continue/continue 项目/.continue` |

`build.py <id>` 执行后会打印该 Agent 的完整 `cp` 命令。

## 示例（Cursor）

```bash
python3 scripts/build.py cursor

mkdir -p /path/to/your-app/.cursor
cp -R generated/cursor/rules /path/to/your-app/.cursor/
```

## 注意

- 若本地仍有旧版 `generated/cursor/.cursor/`，重新 build 一次即可，或手动删除。
- 业务专用规则仍放在各业务仓库。

## 更新流程

1. 改 `guidelines/*.md` 并合并。
2. 对使用中的 Agent 分别 `build.py <id>`。
3. 按打印的复制命令同步到业务项目并提交。
