---
name: receipt-batch-detail-tab
description: >-
  详情页商品区增加「收货批次明细」Tab：STOCKBATCH_ENABLED 门控、BsSulaQueryTable 只读、
  新列表接口（仅 qp-sourceRecordCode-eq）、batchAttribute 自适应列、
  列尾收货通知单/收货结果单 Link（字段与 other-in 一致）。
  Use when implementing receipt batch tab on detail pages (WMS, inventory center).
disable-model-invocation: false
---

# 收货批次明细 Tab

## 何时读本 Skill

- 详情页「商品列表」要拆 **商品明细** + **收货批次明细** Tab
- 需接 **批次总开关**、**批次自适应列**、通知单/结果单跳转
- 后端提供**新列表接口**（不是 `/stock/rwNoticeRecordDetail/withBatch`）

先读团队 guideline：`guidelines/receipt-batch-detail-tab.md`  
BsSulaQueryTable config：[`bssula-query-table`](../bssula-query-table/SKILL.md)

## 业务项目 LOCAL.md（必建）

在 `.cursor/skills/receipt-batch-detail-tab/LOCAL.md` 写明：

| 项 | 示例 |
|----|------|
| 列表 L1 URL | `GET /stock/???`（联调前 `RECEIPT_BATCH_DETAIL_URL_TBD`） |
| `qp-sourceRecordCode-eq` 取值 | 包裹 `recordCode` / 入库单 `recordCode` |
| 收货通知单详情路由模板 | `/returnsManagement/warehousingNotice/view/:id/:code` |
| 收货结果单详情路由模板 | `/returnsManagement/receiptResult/view/:id/:code` |
| 参考 Section 路径 | 本项目 `*ReceiptBatchSection.tsx` |

## 实施步骤

### 1. 批次门控 Hook

复制收窄 `useOtherInBatchGate` → `useXxxBatchGate`：

- `STOCKBATCH_ENABLED` → `isAllowBatch`
- `/stock/batchAttribute` → `batchColumns`, `comKey`

复制 `parseBatchTotalSwitchEnabled`（`batchTotalSwitch.ts`）若项目尚无。

### 2. *Api.ts（L1 + L0）

```ts
// L1 — 新列表 URL（LOCAL 填真实 path）
export const RECEIPT_BATCH_DETAIL_URL = 'TBD';

// L0 — 与 other-in extractReceiptBatchDetailResult 相同
export function extractReceiptBatchDetailResult(ctx) { ... }
```

`remoteDataSource.initialParams` **仅**：

```ts
{ 'qp-sourceRecordCode-eq': recordCode }
```

**不要**加 `qp-recordType-eq`、`qp-deliveryType-eq`。

### 3. Section 组件

对齐 `OtherInReceiptBatchSection`：

- `BsSulaQueryTable` + 四文本 `fields`（按稿）
- `columns = baseColumns + batchColumns + linkColumns`
- `extractResultRecords` / `goReceiptNotice` / `goReceiptResult` — 字段名与 other-in 一致，**路由用 LOCAL**

### 4. Tab 容器

- Tab1：原商品明细表（迁入，不改 URL）
- Tab2：`isAllowBatch && <ReceiptBatchSection recordCode={code} comKey={comKey} batchColumns={batchColumns} />`
- `forwardRef` → `refreshTable()` 刷新两个表

### 5. 自检

- [ ] 批次关：无收货批次 Tab
- [ ] 列表请求无 recordType/deliveryType
- [ ] 通知单/结果单 Link 可点
- [ ] `*Api.ts` 入口索引已更新

## 参考文件（stock-front）

- `src/pages/InventoryCenter/StoreManagement/OtherIn/components/OtherInReceiptBatchSection.tsx`
- `src/pages/InventoryCenter/StoreManagement/OtherIn/hooks/useOtherInBatchGate.ts`
- `openspec/changes/other-in-batch-management/interactions/03-receipt-batch-tab.md`（UI；**接口以 team guideline 为准**）
