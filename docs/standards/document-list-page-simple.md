# 单据列表页简洁规范（人读完整版）

> 团队真源：`guidelines/document-list-page-simple.md`（Agent 短规则）  
> 定稿：2026-08-13；双视图 kb：2026-08-05  
> 首个落地：stock-front 清洗单列表  
> 适用：公司仓 BsSulaQueryTable 单据列表；个人项目忽略

目标：列表页保持「成熟、可抄、别膨胀」。查询表 config 以 `docs/skills/bssula-query-table/` 为准；本文管结构、复杂度预算、双视图选型、自检。

通用 `useEffect` 已拆到 `guidelines/use-effect-prefer-events.md`（全仓适用）。

---

## 1. 适用范围

**管什么**

- 单据类列表页（单表、汇总 ↔ 明细双视图）
- 能力：查询、按状态行操作、跳转新增/编辑/详情

**不管什么**

- 新增 / 编辑 / 详情 Form 页（另开规范）
- 列表内大弹窗业务流程（绑码、跨单编排）→ 详情或独立路由
- 后端自动生单、WMS 回传 → 列表最多展示结果与跳转

**与已有文档**

| 主题 | 真源 |
|------|------|
| `BsSulaQueryTable` config | `docs/skills/bssula-query-table/` |
| 双视图切 Tab 带查询 | kb `domains/company-react/tab-query-sync.md`（2026-08-05；remount-init） |
| `useEffect` | `guidelines/use-effect-prefer-events.md` |

**反例**：`stock-front` 维修单 `RepairOrder/index.tsx`（双视图思路可参考，整页业务堆叠勿抄）。

---

## 2. 目录与 `index` 职责

### 2.1 推荐目录（双视图）

```text
XxxOrder/
  index.tsx                 # 列表页壳：挂表、切视图、接线
  create.tsx / …            # 非本规范
  config/
    listFields.tsx
    listColumns.tsx
    detailFields.tsx        # 无明细模式则省略
    detailColumns.tsx
  utils/
    statusActions.ts
    tabQuerySync.ts         # 可选；先页内，稳定后再抽公共
  services/
    xxxOrderApi.ts
  constants/
```

单表去掉 `detail*` 与 `tabQuerySync`。

### 2.2 `index` 允许 / 禁止

| 允许 | 禁止 → 放到 |
|------|-------------|
| 组装 config | 大段 request / 编排 → `services` / `statusActions` |
| 双视图壳（Tabs + remount token + seed） | 字段/列大数组内联 → `config/*` |
| 接线 statusActions、push、导出 | 业务 Modal 主机 → 详情/独立页 |
| 读 ref | 同页第三张业务表 → 新页面 |

### 2.3 体量（软约束）

| 文件 | 建议 |
|------|------|
| `index.tsx` | ~200 行；双视图 ~300；再长先拆 |
| `*Columns` | 行操作只 import action |
| `statusActions.ts` | 一状态一函数 + L3 步骤注释 |

---

## 3. 复杂度预算

成功标准：**能查、能切视图、能按状态点行操作、能进详情/编辑**。

### 3.1 MUST

1. 项目封装 `BsSulaQueryTable`；config 跟 Skill  
2. `qp-*` 公开字段；分页/排序不进 `qp-*`  
3. 行操作进 `statusActions`，不在 column 里打接口  
4. 成功只 `refreshTable`（+ 角标）  
5. 跳转只用声明字段；禁止未声明 `??` 链  
6. 工具栏克制 + `code`  
7. 双视图守 §4；单表不预埋 Tab  
8. 遵守 `use-effect-prefer-events`；双视图优先 `onChange` + `scheduleApply`

### 3.2 MUST NOT

1. 列表挂业务 Modal 链  
2. `index` 堆多个 `runXxx` 编排  
3. 重写整段 `formProps.actionsRender` 做默认查询  
4. 列表编辑主数据（开关类除外）  
5. `index` 塞详情 Tab  
6. 整页抄维修单再删减  
7. 列表做自动生单补偿/重试 UI  

### 3.3 行操作白名单

允许：详情、编辑、提交、审核/驳回、撤回、反审核、作废；PRD 写明且停在本单的入口（如分类处理 → **跳详情**）。

不允许：列表行内分类录入、分类 Excel、生下游单、改明细数量。

### 3.4 膨胀信号

| 信号 | 处理 |
|------|------|
| `index` 本模块 import 过多（~10+） | 砍越界职责 |
| PR 出现详情专用组件 | 挪详情页 |
| Tab 同步与 kb 不一致 | 改回定稿 |

---

## 4. 双视图唯一路径

细节、踩坑、**reuse vs remount 对比**：kb `tab-query-sync.md`（2026-08-05）。

| 挂法 | 模式 |
|------|------|
| `Tabs` + `destroyInactiveTabPane` | **A · remount-init**（默认） |
| 条件渲染只挂一张 | **B · requestParamsRef + initialValues** |

模式 A：无 `forceRender`；`key`+token；seed `initialValues`；`onChange` → `scheduleApply` 单次 refresh；列表仅首次可 `autoInit`。

禁止：预挂 + `forceRender` 当新页默认；两套不同步逻辑；无控制多次 refresh。

---

## 5. 自检清单

- [ ] 目录/`index` 按 §2  
- [ ] 行操作 ⊆ 白名单且在 `statusActions`  
- [ ] 无业务 Modal / 详情 Tab 进列表；未整页抄维修单  
- [ ] `useEffect` 符合 prefer-events  
- [ ] 双视图 remount-init（或模式 B）；列表接口切入 1 次  
- [ ] `initialValues` + `rules`；`qp-*` 公开字段  

---

## 变更记录

| 日期 | 说明 |
|------|------|
| 2026-08-13 | 自 stock-front 草稿晋升；拆出通用 useEffect guideline |
