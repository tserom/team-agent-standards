---
name: receipt-batch-detail-tab
description: >-
  详情页商品区增加「收货批次明细」Tab：STOCKBATCH_ENABLED 门控、BsSulaQueryTable 只读、
  新列表接口、batchAttribute 自适应列、列尾收货通知单/收货结果单 Link。
  行字段以本接口 VO 为准（*ReceiptBatchRow），禁止未声明字段 ?? 回退链。
  Use when implementing receipt batch tab on detail pages (WMS, inventory center).
disable-model-invocation: false
---

# 收货批次明细 Tab

## 何时读本 Skill

- 详情页「商品列表」要拆 **商品明细** + **收货批次明细** Tab
- 需接 **批次总开关**、**批次自适应列**、通知单/结果单跳转
- 后端提供**新列表接口**（不是 `/stock/rwNoticeRecordDetail/withBatch`）

先读团队 guideline：`guidelines/receipt-batch-detail-tab.md`  
字段契约：`guidelines/api-layering.md` §响应字段契约  
BsSulaQueryTable config：[`bssula-query-table`](../bssula-query-table/SKILL.md)

## 业务项目 LOCAL.md（必建）

在 `.cursor/skills/receipt-batch-detail-tab/LOCAL.md` 写明：

| 项 | 示例 |
|----|------|
| 列表 L1 URL | `GET /stock/reverseRecord/detail/withBatch` |
| 固定 qp | `qp-recordCode-eq` = 包裹单号 |
| **行类型名** | `ReturnPackageReceiptBatchRow` |
| **跳转字段表** | 通知单 id=`id`，code=`inRecordCode`；结果单=`resultRecordCode` |
| 收货通知单详情路由模板 | `/inventory-center/.../receipt-deliver-notice/view/:id/:code/...` |
| 收货结果单详情路由模板 | 同上 result 路径 |
| 参考 Section 路径 | 本项目 `*ReceiptBatchSection.tsx` |
| **§回退登记表** | 复制 team standard §4.4，填本项目待确认项 |

**禁止**在 LOCAL 写未联调确认的 `qp-recordType-eq`、`qp-deliveryType-eq`。

## 实施步骤

### 1. 批次门控 Hook

复制收窄 `useOtherInBatchGate` → `useXxxBatchGate`：

- `STOCKBATCH_ENABLED` → `isAllowBatch`
- `/stock/batchAttribute` → `batchColumns`, `comKey`

复制 `parseBatchTotalSwitchEnabled`（`batchTotalSwitch.ts`）若项目尚无。

### 2. *Api.ts（L1 + L0 + 行类型）

```ts
/** 本接口 VO — 跳转只读下列字段 */
export type XxxReceiptBatchRow = {
  id?: string | number;        // 注释：对应路由哪一段
  inRecordCode?: string;
  resultRecordCode?: string;
};

export const RECEIPT_BATCH_DETAIL_URL = '...'; // LOCAL

// L0 框架归一化（注释标明 BsSula 包裹形态）
export function extractReceiptBatchDetailResult(ctx) { ... }

// L0 仅声明字段，例如只拆 resultRecordCode
export function extractResultRecordCodes(record: Pick<XxxReceiptBatchRow, 'resultRecordCode'>) { ... }
```

`remoteDataSource.initialParams` **仅** LOCAL 固定 qp。

### 3. Section 组件

- `BsSulaQueryTable` + 四文本 `fields`（按稿）
- `columns = baseColumns + batchColumns + linkColumns`
- L3 跳转集中在 `*Api.ts`；**路由用 LOCAL**；**勿**复制 other-in 字段 `??` 链

### 4. Tab 容器

- Tab1：原商品明细表（迁入，不改 URL）
- Tab2：`isAllowBatch && <ReceiptBatchSection ... />`
- `forwardRef` → `refreshTable()` 刷新两个表

### 5. 自检

- [ ] 批次关：无收货批次 Tab
- [ ] 列表请求 qp 与 LOCAL 一致
- [ ] `*ReceiptBatchRow` 与跳转函数字段一致
- [ ] 回退表已填；待确认项已在 MR/回复列出
- [ ] 通知单/结果单 Link 可点
- [ ] `*Api.ts` 入口索引已更新

## 参考文件

- **UI 结构**：stock-front `OtherInReceiptBatchSection.tsx`（**勿**照搬其字段链）
- **字段示例**：storage-front `ReturnPackageReceiptBatchRow` + `API_PENDING.md`
- 交互稿：`stock-front/openspec/.../03-receipt-batch-tab.md`（UI；**接口与字段以 LOCAL 为准**）
