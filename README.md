# team-agent-standards

团队 · 跨项目 AI 协作规范真源。**方案 B**：各 Agent 在 `generated/<agent-id>/` 下生成**可见**目录，复制到业务项目时再放到 `.cursor` 等工具要求的路径。

**仓库职能与目录说明** → [docs/REPOSITORY_STRUCTURE.md](docs/REPOSITORY_STRUCTURE.md)  
**何时把规则/Skill 晋升到本仓库** → `guidelines/promote-to-team-standards.md`（构建为 Cursor 规则 `promote-to-team-standards.mdc`）

| 层级 | 说明 |
|------|------|
| **`guidelines/*.md`** | 唯一真源（含 `api-layering.md`、Karpathy、React 可读性等） |
| **`docs/standards/*.md`** | API 分层等人读长文（与 `guidelines` 配套，非构建真源） |
| **`docs/skills/`** | 可复用 Skill 模板（手动复制到业务 `.cursor/skills/`） |
| `cursor-manifest.json` | Cursor → `.mdc` |
| `agent-manifest.json` | 构建路径与 `installTo` 对照 |
| `generated/<id>/` | 构建产物（git 忽略） |

## 构建

```bash
python3 scripts/build.py --list
python3 scripts/build.py cursor    # -> generated/cursor/rules/
python3 scripts/build.py claude    # -> generated/claude/CLAUDE.md
```

## 同步到业务项目（Cursor）

```bash
python3 scripts/build.py cursor
```

其它 Agent 见 [docs/other-agents.md](docs/other-agents.md)；`build` 结束时会打印复制提示。

### 首次安装（项目尚无 `.cursor/rules`）

```bash
APP=/path/to/your-project
mkdir -p "$APP/.cursor"
cp -R generated/cursor/rules "$APP/.cursor/"
```

### 增量更新（项目里已有自己的 rules）

业务项目可并存 **团队规则**（本仓库 `cursor-manifest.json` 的 `output` 文件名）与 **项目专用** `.mdc`（建议命名 `*-业务名*.mdc`，勿与团队 `output` 同名）。同步时**只复制团队那几条**，不要用 `cp -R` 盖整个目录，否则会误伤或弄乱项目专用文件。

```bash
APP=/path/to/your-project
mkdir -p "$APP/.cursor/rules"

# 默认：仅覆盖与团队同名的 .mdc，不删除其它文件
cp generated/cursor/rules/*.mdc "$APP/.cursor/rules/"

# 若本地同名文件是你手改过的团队副本、暂不想被覆盖：
# cp -n generated/cursor/rules/*.mdc "$APP/.cursor/rules/"
```

同步前建议 `ls generated/cursor/rules/` 与 `ls "$APP/.cursor/rules/"`，提交前 `git diff .cursor/rules` 确认只动了团队文件。

**Skills**（不参与 build）按目录增量复制，例如 `cp -R docs/skills/foo "$APP/.cursor/skills/"`，勿无脑 `cp -R` 整个 `docs/skills/` 以免覆盖项目自有 skill。

## 修改规则

1. 改 `guidelines/*.md` 并 MR。
2. 对使用中的 Agent 执行 `build.py <id>`。
3. 复制到业务项目。

## 远程仓库

https://github.com/tserom/team-agent-standards
