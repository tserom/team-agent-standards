# team-agent-standards

比升前端 · AI 协作规范真源。**方案 B**：各 Agent 产物在 `generated/<agent-id>/` 下，构建时只清空该子目录，互不影响。

| 层级 | 说明 |
|------|------|
| **`guidelines/*.md`** | 唯一真源 |
| `cursor-manifest.json` | Cursor → `.mdc` |
| `agent-manifest.json` | Agent 列表与输出文件名 |
| `generated/<id>/` | 构建产物（git 忽略） |

## 构建

```bash
python3 scripts/build.py --list
python3 scripts/build.py cursor    # -> generated/cursor/.cursor/
python3 scripts/build.py claude    # -> generated/claude/CLAUDE.md
```

可先 build 多个 Agent，它们会分别留在 `generated/cursor/`、`generated/claude/` 等目录中。

## 同步到业务项目

```bash
python3 scripts/build.py cursor
cp -R generated/cursor/.cursor /path/to/your-project/
```

其它 Agent 见 [docs/other-agents.md](docs/other-agents.md)。

## 修改规则

1. 改 `guidelines/*.md` 并 MR。
2. 对使用中的 Agent 执行 `build.py <id>`。
3. 从 `generated/<id>/` 复制到业务项目。

## 远程仓库

https://github.com/tserom/team-agent-standards
