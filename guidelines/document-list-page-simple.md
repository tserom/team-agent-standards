# 单据列表页简洁规范（公司仓）

实现或修改 **BsSulaQueryTable 单据列表**（含汇总↔明细双视图）时遵守。个人项目无 bssula 列表则忽略本条。

人读完整版：`docs/standards/document-list-page-simple.md`  
查询表 config：`docs/skills/bssula-query-table/`  
双视图细节真源：kb `domains/company-react/tab-query-sync.md`（2026-08-05 定稿 remount-init）  
`useEffect`：`guidelines/use-effect-prefer-events.md`

## 范围

| 管 | 不管 |
|----|------|
| 查询、状态行操作、跳转增/编/详、双视图带查询 | 新增/编辑/详情 Form；列表内大弹窗业务链；自动生单补偿 UI |

成功标准：**能查、能切视图、能按状态点行操作、能进详情/编辑**。

## 目录与 `index`（MUST）

```text
XxxOrder/
  index.tsx              # 只组壳：config、切视图、接线
  config/listFields|listColumns|detailFields|detailColumns
  utils/statusActions.ts # 一状态一函数 + 步骤注释
  services/*Api.ts       # L1/L3 + call-map
```

| `index` 允许 | `index` 禁止 |
|--------------|--------------|
| 组装 config、Tabs remount 壳、挂 statusActions / push / 导出 | 大段 request、列大数组内联、业务 Modal 主机、详情 Tab、第三张业务表 |

软上限：`index` ~200 行（双视图 ~300）；超了先拆 `tabQuerySync`。  
**反例**：维修单列表整页复制（可参考双视图思路，勿抄业务堆叠）。

## 复杂度（MUST / MUST NOT）

**MUST**：Skill 写 config；`qp-*` 公开字段；行操作进 `statusActions`；成功只 `refreshTable`（+ 角标）；跳转只用声明字段；工具栏克制 + `code`；单表不预埋 Tab。

**MUST NOT**：列表挂绑码/跨单 Modal 链；重写整段 `formProps` 做默认查询（用 `initialValues` + `rules`）；列表当详情；列表补偿自动生单。

**行操作白名单**：详情、编辑、提交、审核/驳回、撤回、反审核、作废；PRD 写明且停在本单的入口（如「分类处理」→ **跳详情**）。禁止在列表行内分类录入/分类 Excel/生下游单。

## 双视图（有则 MUST）

| 挂法 | 模式 |
|------|------|
| `Tabs` + `destroyInactiveTabPane` | **A · remount-init**（默认） |
| 条件渲染只挂一张表 | **B · requestParamsRef + initialValues** |

模式 A 最小集：无 `forceRender`；`key`+token 重挂；离开 seed `initialValues`；`onChange` → `scheduleApply` 单次 refresh；列表仅首次可 `autoInit`。细节与 reuse 对比见 kb `tab-query-sync.md`。

## PR 勾选

- [ ] 目录/`index` 职责是否按上表？
- [ ] 行操作是否 ⊆ 白名单且在 `statusActions`？
- [ ] 双视图是否 remount-init（或模式 B），且对照过 kb？
- [ ] 新增 `useEffect` 是否符合 `use-effect-prefer-events`？
- [ ] 是否未整页抄维修单？
