# team-agent-standards

比升前端 · AI 协作规范真源。**方案 B**：各 Agent 在 `generated/<agent-id>/` 下生成**可见**目录，复制到业务项目时再放到 `.cursor` 等工具要求的路径。

| 层级 | 说明 |
|------|------|
| **`guidelines/*.md`** | 唯一真源 |
| `cursor-manifest.json` | Cursor → `.mdc` |
| `agent-manifest.json` | 构建路径与 `installTo` 对照 |
| `generated/<id>/` | 构建产物（git 忽略） |

## 构建

```bash
python3 scripts/build.py --list
python3 scripts/build.py cursor    # -> generated/cursor/rules/
python3 scripts/build.py claude    # -> generated/claude/CLAUDE.md
```

## 同步到业务项目（Cursor 示例）

```bash
python3 scripts/build.py cursor
mkdir -p /path/to/your-project/.cursor
cp -R generated/cursor/rules /path/to/your-project/.cursor/
```

其它 Agent 见 [docs/other-agents.md](docs/other-agents.md)；`build` 结束时会打印对应命令。

## 修改规则

1. 改 `guidelines/*.md` 并 MR。
2. 对使用中的 Agent 执行 `build.py <id>`。
3. 复制到业务项目。

## 远程仓库

https://github.com/tserom/team-agent-standards
