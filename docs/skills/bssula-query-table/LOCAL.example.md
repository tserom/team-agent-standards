# LOCAL.example.md 是什么？

团队 Skill（`SKILL.md`）刻意**不写**具体仓库名、import 路径和参考页路径，以便多个前端项目共用。

`LOCAL.example.md` 只留在 **team-agent-standards** 仓库里，作用是：

1. **填空模板**：告诉同事复制成业务项目里的 `LOCAL.md` 时要写哪些字段。
2. **示例一份**：下面用「某库存项目」填了一版，新同事照着改路径即可。
3. **不进 team 的 MR 正文**：业务项目里的 `LOCAL.md` **只提交在业务仓库**，不要回传到 team（避免 team 又被某个 monorepo 绑死）。

复制命令：

```bash
cp LOCAL.example.md  # 在业务项目 .cursor/skills/bssula-query-table/ 下执行
mv LOCAL.example.md LOCAL.md   # 或直接从 team 复制后改名为 LOCAL.md
# 编辑 LOCAL.md，改成当前仓库的真实路径
```

Agent 读 Skill 时：**先读 `SKILL.md`（通用）→ 再读同目录 `LOCAL.md`（本项目）**。

---

# 以下为示例内容（复制到业务项目后改名为 LOCAL.md 并修改）

## 封装路径

| 项 | 本仓库取值 |
|----|------------|
| 页面 import | `@/components/businessComponent/BsSulaQueryTable` |
| 底层包 | `@bit-sun/business-component` → `BsSulaQueryTable` |
| 默认 `itemPath` | `stock` |

## 参考页（相对 `src/pages`）

| 场景 | 路径 |
|------|------|
| 双 Tab 列表+明细 + initialValues | `InventoryCenter/DocumentsQuery/StandardDocumentsQuery/ReceiptDeliverNotice/index.tsx` |
| 多条件二选一查询 | `InventoryCenter/StoreManagement/UniqueCodeFlowRecord/posIndex.tsx` |
| autoInit + 自定义查询 | `InventoryCenter/InventoryManagement/InventoryQueueLog/index.tsx` |
| 列表明细 Tab 同步 | `InventoryCenter/StoreManagement/OtherOut/index.tsx`、`InventoryCenter/StoreManagement/OtherIn/index.tsx` |

## 关联 Skill

- 整页脚手架：`stock-front-page-scaffold`（仅本仓库，未晋升团队）
