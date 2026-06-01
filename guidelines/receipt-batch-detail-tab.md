# 详情页 · 收货批次明细 Tab（批次总开关）

在业务详情「商品/明细」区增加 **收货批次明细** 只读 Tab 时**默认遵守**。与 [bssula-query-table](../docs/skills/bssula-query-table/SKILL.md)、[api-layering.md](api-layering.md) 配合。

**人读完整版**（列、字段、跳转、参考实现）：`docs/standards/receipt-batch-detail-tab.md`  
**实现流程 Skill**：`docs/skills/receipt-batch-detail-tab/SKILL.md`

---

## 显示条件

| 条件 | 表现 |
|------|------|
| `STOCKBATCH_ENABLED` = false | **不展示**收货批次明细 Tab；原明细表可单独或放在「商品明细」Tab |
| `STOCKBATCH_ENABLED` = true | **商品明细** + **收货批次明细** 并列 Tab |

开关：`GET /basic/configParam/relation/group?qp-configCode-eq=STOCKBATCH_ENABLED&qp-type-in=10&qp-configPriority-ne=0` → `parseBatchTotalSwitchEnabled`（与 stock-front `batchTotalSwitch.ts` 一致）。

---

## 收货批次列表接口（2026-06 团队约定）

| ✅ MUST | ❌ MUST NOT |
|---------|-------------|
| 使用**业务域新列表 URL**（L1 常量，联调前可 `TBD`） | 默认沿用 `/stock/rwNoticeRecordDetail/withBatch`（其他入库旧路径；新需求已废弃） |
| `initialParams` 仅 **`qp-sourceRecordCode-eq`** = 来源单号（如包裹单号 `recordCode`） | 传 `qp-recordType-eq`、`qp-deliveryType-eq` |
| L0 `extract*BatchDetailResult` 归一化分页 | UI 内联 `request` 拼 URL |
| 用户查询区 `fields` 叠加 `qp-spuCode-eq` 等 | 把 recordType/deliveryType 写进业务 OpenSpec 必填 |

**行数据**：通知单/结果单字段名与 **other-in 收货批次明细**响应一致（`recordCode`、`recordId`/`noticeRecordId`/`id`；`resultRecordCodeList`/`resultRecordCodes`/单值/逗号串 + 对应 `*IdList`）。列尾 Link + `extractResultRecords` 复用 stock-front `OtherInReceiptBatchSection` 逻辑。

**详情路由**：按**业务项目** `LOCAL`（WMS 退货 vs 库存中心标准单据），集中在 `*Api.ts` 或 Section 顶部常量。

---

## 表格与列

- 组件：**`BsSulaQueryTable`**，只读（无增删改）。
- **批次自适应列**：`GET /stock/batchAttribute?pageSize=9999&qp-status-eq=1&sorter=asc-displayOrder` → `attributeCode` 转 camelCase `key`；`comKey` 就绪后 bump 以重挂载列。
- 列顺序：行号 → 业务行字段 → `batchCode`（若有）→ **batchColumns** → **收货通知单** → **收货结果单**（稿图固定列勿与 batchAttribute 重复写死）。

---

## 分层

- L1：列表 URL 一个 export/常量。
- L0：列表结果归一化、结果单码列表解析（不发 HTTP）。
- L3：跳转通知单/结果单详情（`history.push`，路由来自项目 LOCAL）。

`*Api.ts` 顶部维护：**动作 → 函数 → URL → 不会调的 URL**。

---

## 参考实现（只读 Tab）

- stock-front：`OtherInReceiptBatchSection.tsx`、`useOtherInBatchGate.ts`（**勿**复制 withBatch 的 recordType/deliveryType 入参到新需求）。
- 交互稿：`stock-front/openspec/changes/other-in-batch-management/interactions/03-receipt-batch-tab.md`（UI/列；接口以本 guideline 为准）。
