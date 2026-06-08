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
| `initialParams` 仅业务联调约定的固定 qp（如 `qp-recordCode-eq` / `qp-sourceRecordCode-eq`） | 未经文档擅自传 `qp-recordType-eq`、`qp-deliveryType-eq` |
| L0 `extract*BatchDetailResult` 归一化分页（框架形态，见 api-layering） | UI 内联 `request` 拼 URL |
| 行类型 `*ReceiptBatchRow` + 跳转只读**本接口 VO 声明字段** | 未声明字段 `??` 链；照搬 other-in 字段名 |

**行字段**：以**本需求联调 VO** 为准（在 `API_PENDING.md` / Skill `LOCAL.md` 建字段表）。other-in `withBatch` 仅作 **UI/列结构**参考，**不得**默认字段名一致。

**详情路由**：按**业务项目** `LOCAL`（WMS 退货 vs 库存中心标准单据 + wujie `/stock` 前缀等），集中在 `*Api.ts` 或 Section 顶部常量。

**回退**：任何业务回退登记在 `API_PENDING.md` §回退登记表；实现后回复单列待确认项。

---

## 表格与列

- 组件：**`BsSulaQueryTable`**，只读（无增删改）。
- **批次自适应列**：`GET /stock/batchAttribute?pageSize=9999&qp-status-eq=1&sorter=asc-displayOrder` → `attributeCode` 转 camelCase `key`；`comKey` 就绪后 bump 以重挂载列。
- 列顺序：行号 → 业务行字段 → `batchCode`（若有）→ **batchColumns** → **收货通知单** → **收货结果单**（稿图固定列勿与 batchAttribute 重复写死）。

---

## 分层

- L1：列表 URL 一个 export/常量。
- L0：列表结果归一化、结果单码列表解析（**仅声明字段**，不发 HTTP）。
- L3：跳转通知单/结果单详情（路由来自项目 LOCAL；跨子应用用 wujie 时在 L3 集中）。

`*Api.ts` 顶部维护：**动作 → 函数 → URL → 不会调的 URL**。

---

## 参考实现（只读 Tab）

- stock-front：`OtherInReceiptBatchSection.tsx`、`useOtherInBatchGate.ts`（**勿**复制 withBatch 的 recordType/deliveryType 入参与新接口字段链）。
- storage-front 无名包裹：`ReturnPackageReceiptBatchSection` + `ReturnPackageReceiptBatchRow`（字段表示例见 team standard §4.2）。
- 交互稿：`stock-front/openspec/changes/other-in-batch-management/interactions/03-receipt-batch-tab.md`（UI/列；**接口与字段以本 guideline + 业务 API_PENDING 为准**）。
