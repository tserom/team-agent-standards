# 详情页 · 收货批次明细 Tab（标准）

> 团队真源：`guidelines/receipt-batch-detail-tab.md`（Agent 摘要）  
> 实现 Skill：`docs/skills/receipt-batch-detail-tab/SKILL.md`

## 1. 适用场景

业务单据详情页「商品列表 / 明细」区域，在开启库存 **批次总开关** 后，需要：

- 保留原有 **商品明细**（SKU 行）查询表；
- 增加 **收货批次明细** 只读 Tab（按批次 + 通知单维度展示）；
- 列尾跳转 **收货通知单**、**收货结果单**。

已落地参考：**stock-front 其他入库**（`OtherInReceiptBatchSection`）；**storage-front 无名包裹**（OpenSpec `unnamed-package-receipt-batch-tab`）。

---

## 2. 批次总开关

| 项 | 值 |
|----|-----|
| 配置码 | `STOCKBATCH_ENABLED` |
| 请求 | `GET /basic/configParam/relation/group?qp-configCode-eq=STOCKBATCH_ENABLED&qp-type-in=10&qp-configPriority-ne=0` |
| 解析 | `parseBatchTotalSwitchEnabled(res)`（`optionDefaultValue.valueCode`） |

Hook 模式（可复制到业务域 `useXxxBatchGate`）：

1. 拉开关 → `isAllowBatch`
2. 拉 `/stock/batchAttribute` → `batchColumns` + `comKey` bump

---

## 3. 列表接口（2026-06 更新）

### 3.1 与「其他入库旧实现」的差异

| | 其他入库（stock-front 已上线） | **新需求（无名包裹等）** |
|---|-------------------------------|-------------------------|
| URL | `GET /stock/rwNoticeRecordDetail/withBatch` | **新接口，URL 联调前未知**（L1 常量占位） |
| 固定 qp | `qp-sourceRecordCode-eq` + `qp-recordType-eq=50` + `qp-deliveryType-eq=0` | **仅** `qp-sourceRecordCode-eq` = 来源单号（包裹单号等） |
| recordType / deliveryType | 必填 | **禁止**再传 |

### 3.2 查询区（用户输入）

在 `initialParams` 之外，由 `BsSulaQueryTable` `fields` 提供，常见：

| 标签 | qp 示例 |
|------|---------|
| SPU 编码 | `qp-spuCode-eq` |
| SKU 编码 | `qp-skuCode-eq` |
| SKU 名称 | `qp-skuName-like` |
| 批次编码 | `qp-batchCode-eq` |

具体后缀以后端文档为准；与商品明细 Tab 命名对齐。

### 3.3 响应归一化（L0）

与 other-in 相同，兼容 `items` / `list` / `data` 数组及 `total`：

```ts
// 命名示例：extractReceiptBatchDetailResult
```

---

## 4. 行字段与列尾 Link（与 other-in 一致）

后端已确认：**通知单/结果单行字段名与 other-in `withBatch` 平铺响应一致**。

### 4.1 收货通知单

| 用途 | 字段（优先级） |
|------|----------------|
| 跳转 id | `recordId` → `noticeRecordId` → `id` |
| 展示/路由 code | `recordCode` |

### 4.2 收货结果单（多单）

| 用途 | 字段（优先级） |
|------|----------------|
| 单号列表 | `resultRecordCodeList` → `resultRecordCodes` → `resultRecordCode`（逗号拆） |
| id 列表 | `resultRecordIdList` → `resultRecordIds` → `resultRecordId`（逗号拆） |

展示：多个结果单号 **英文逗号** 分隔，每个为 Link。

参考实现：`stock-front/.../OtherInReceiptBatchSection.tsx` 中 `extractResultRecords`、`goReceiptNotice`、`goReceiptResult`。

### 4.3 详情路由（按项目 LOCAL）

| 项目类型 | 收货通知单（示例） | 收货结果单（示例） |
|----------|-------------------|-------------------|
| 库存中心 stock-front | `/inventory-center/.../receipt-deliver-notice/view/:id/:code/:deliveryType/:sourceRecordCode` | `/inventory-center/.../receipt-deliver-result/view/...` |
| WMS storage-front 退货 | `/returnsManagement/warehousingNotice/view/:id/:code` | `/returnsManagement/receiptResult/view/:id/:code` |

**新接口**下结果单跳转是否仍带 `deliveryType`/`sourceRecordCode` 路径段，由业务项目 LOCAL 与后端约定；字段读取仍按上表。

---

## 5. 列结构

1. **行号**（index + 1）
2. **业务列**（SKU、数量、状态等，按产品稿）
3. **批次编码** `batchCode`（空显示 `--`）
4. **批次自适应列**（`batchAttribute` 配置，勿与稿图重复写死过期日期等）
5. **收货通知单**（Link）
6. **收货结果单**（Link，多单逗号）

---

## 6. API 分层检查清单

- [ ] 新列表 URL 仅在 `*Api.ts` L1 定义一处
- [ ] `initialParams` 只有 `qp-sourceRecordCode-eq`
- [ ] 未传 `qp-recordType-eq` / `qp-deliveryType-eq`
- [ ] Link 跳转与 `extractResultRecords` 在 Section 或 L3 集中
- [ ] `*Api.ts` 入口索引已更新

---

## 变更记录

| 日期 | 说明 |
|------|------|
| 2026-06-01 | 晋升自 storage-front 无名包裹 OpenSpec；新列表 URL 待定；入参仅 sourceRecordCode；行字段与 other-in 一致 |
