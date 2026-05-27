# 其他 Agent 配置说明

规范真源在 `guidelines/*.md`。采用 **方案 B**：每个 Agent 对应 `generated/<agent-id>/` 目录；`build.py <id>` **只清空并重建该目录**，不会动其它 Agent。

```bash
python3 scripts/build.py --list
python3 scripts/build.py cursor
python3 scripts/build.py claude   # generated/cursor/ 仍在
```

## 目录结构

```text
generated/
  cursor/.cursor/rules/*.mdc
  claude/CLAUDE.md
  copilot/.github/copilot-instructions.md
  agents-md/AGENTS.md
  windsurf/.windsurfrules
  cline/.clinerules
  aider/CONVENTIONS.md
  continue/.continue/rules/team-standards.md
```

## Agent 与复制命令

| 命令 | 工具 | 复制到业务项目 |
|------|------|----------------|
| `build.py cursor` | Cursor | `cp -R generated/cursor/.cursor 项目根/` |
| `build.py claude` | Claude Code | `cp generated/claude/CLAUDE.md 项目根/` |
| `build.py copilot` | GitHub Copilot | `cp -R generated/copilot/.github 项目根/` |
| `build.py agents-md` | Copilot Agent / Codex 等 | `cp generated/agents-md/AGENTS.md 项目根/` |
| `build.py windsurf` | Windsurf | `cp generated/windsurf/.windsurfrules 项目根/` |
| `build.py cline` | Cline | `cp generated/cline/.clinerules 项目根/` |
| `build.py aider` | Aider | `cp generated/aider/CONVENTIONS.md 项目根/` |
| `build.py continue` | Continue | `cp -R generated/continue/.continue 项目根/` |

## 示例

```bash
python3 scripts/build.py cursor
cp -R generated/cursor/.cursor /path/to/your-app/

python3 scripts/build.py claude
cp generated/claude/CLAUDE.md /path/to/your-app/
```

## 注意

- `generated/` 根下若仍有旧版扁平文件（如 `generated/.cursor`、`generated/CLAUDE.md`），与当前方案无关，可手动删除。
- 业务专用规则仍放在各业务仓库，不放进本仓库。

## 更新流程

1. 改 `guidelines/*.md` 并合并。
2. 对使用中的 Agent 分别 `build.py <id>`。
3. 从 `generated/<id>/` 复制到业务项目并提交。
