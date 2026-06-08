# 详情页 · 收货批次明细 Tab（标准）

> 团队真源：`guidelines/receipt-batch-detail-tab.md`（Agent 摘要）  
> 实现 Skill：`docs/skills/receipt-batch-detail-tab/SKILL.md`  
> 字段契约通则：`docs/standards/api-abstraction-encapsulation-reuse.md` §3.4

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
| URL | `GET /stock/rwNoticeRecordDetail/withBatch` | **新接口，URL 以联调为准**（L1 常量） |
| 固定 qp | `qp-sourceRecordCode-eq` + `qp-recordType-eq=50` + `qp-deliveryType-eq=0` | **以联调文档为准**（无名包裹：`qp-recordCode-eq`） |
| recordType / deliveryType | 必填 | 新需求**禁止**未经文档擅自传递 |

### 3.2 查询区（用户输入）

在 `initialParams` 之外，由 `BsSulaQueryTable` `fields` 提供，常见：

| 标签 | qp 示例 |
|------|---------|
| SPU 编码 | `qp-spuCode-eq` |
| SKU 编码 | `qp-skuCode-eq` |
| SKU 名称 | `qp-skuName-like` |
| 批次编码 | `qp-batchCode-eq` |

具体后缀以后端文档为准；与商品明细 Tab 命名对齐。

### 3.3 响应归一化（L0 · 框架形态）

`extract*BatchDetailResult` 可兼容 BsSula 多层包裹与 `items` / `list` / `data`、`total` 缺失兜底——属**框架响应形态**，须在函数注释标明；**不是**业务字段回退链。

---

## 4. 行字段与列尾 Link

### 4.0 原则（先于字段表）

1. **每个业务域独立字段表**：写在 `openspec/.../API_PENDING.md` 或 `.cursor/skills/receipt-batch-detail-tab/LOCAL.md`。
2. **`*Api.ts` 定义 `*ReceiptBatchRow` 类型**，跳转函数只解构表中字段。
3. **禁止**未在表中声明的 `??` / `\|\|` 回退（尤其禁止从 other-in 照搬 `recordId ?? noticeRecordId ?? id`）。
4. **必须回退时**：登记 §4.4 回退表，MR 与 Agent 回复**单列**待确认项。

### 4.1 other-in withBatch（stock-front 已上线 · 仅该接口适用）

| 用途 | 字段 |
|------|------|
| 跳转 id | `recordId` → `noticeRecordId` → `id` |
| 展示/路由 code | `recordCode` |
| 结果单号 | `resultRecordCodeList` → `resultRecordCodes` → `resultRecordCode`（逗号拆） |
| 结果单 id | `resultRecordIdList` → `resultRecordIds` → `resultRecordId`（逗号拆） |

参考：`stock-front/.../OtherInReceiptBatchSection.tsx`。

### 4.2 无名包裹 · `GET /stock/reverseRecord/detail/withBatch`（示例）

| 用途 | 字段 |
|------|------|
| 通知单跳转 id | `id`（行 id） |
| 通知单跳转 code | `inRecordCode` |
| 结果单号 | `resultRecordCode`（英文逗号拆；**无**结果单 id 字段） |

类型示例：`ReturnPackageReceiptBatchRow`（`returnPackageReceiptBatchApi.ts`）。

### 4.3 详情路由（按项目 LOCAL）

| 项目类型 | 收货通知单（示例） | 收货结果单（示例） |
|----------|-------------------|-------------------|
| 库存中心 stock-front | `/inventory-center/.../receipt-deliver-notice/view/:id/:code/:deliveryType/:sourceRecordCode` | `/inventory-center/.../receipt-deliver-result/view/...` |
| WMS storage-front 退货 | `/returnsManagement/warehousingNotice/view/:id/:code` | `/returnsManagement/receiptResult/view/:id/:code` |
| storage → stock 子应用 | wujie `jump({ pathname: '/stock' + path })` | 同上 |

`deliveryType` / `sourceRecordCode` 路径段以业务 LOCAL 为准。

### 4.4 回退登记表（模板）

复制到 `API_PENDING.md` 或 `LOCAL.md`：

| 位置 | 回退内容 | 性质 | 待确认 |
|------|----------|------|--------|
| （例）`jumpToStockApp` | 无 wujie 时 `history.push` | 宿主环境 | 一般保留 |
| （例）`extract*BatchDetailResult` | 多层 ctx 取 list | BsSula 框架 | 一般保留 |
| （例）结果单 `:id` 空串 | 接口无结果单 id | **业务缺口** | **需联调确认** |
| （例）状态列 | `statusName` 空 → 字典 `status` | 展示兜底 | 可选 |

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
- [ ] `initialParams` 与联调文档一致
- [ ] 未擅自传 `qp-recordType-eq` / `qp-deliveryType-eq`
- [ ] `*ReceiptBatchRow` + 跳转仅声明字段；回退表已登记
- [ ] Link 跳转与解析在 Section 或 L3 集中
- [ ] `*Api.ts` 入口索引已更新

---

## 变更记录

| 日期 | 说明 |
|------|------|
| 2026-06-01 | 晋升自 storage-front 无名包裹 OpenSpec；新列表 URL 待定 |
| 2026-06-01 | 补充：禁止未声明业务字段回退链；other-in 与业务域 VO 分表；回退登记表 |
