# LOCAL.example — 复制为业务项目 `.cursor/skills/receipt-batch-detail-tab/LOCAL.md`

## 接口

| 项 | 填写 |
|----|------|
| 列表 L1 URL | 例：`GET /stock/reverseRecord/detail/withBatch` |
| 固定 qp | 例：`qp-recordCode-eq` = 包裹单号 `recordCode` |

## 行类型与跳转字段（本接口 VO，禁止 ?? 猜字段）

| 用途 | 字段名 |
|------|--------|
| 行类型 export 名 | 例：`ReturnPackageReceiptBatchRow` |
| 通知单跳转 id | 例：`id` |
| 通知单跳转 code | 例：`inRecordCode` |
| 结果单号（逗号拆） | 例：`resultRecordCode` |
| 结果单 id | 无则写明「路由 :id 空串，待联调确认」 |

## 路由

| 项 | 填写 |
|----|------|
| 收货通知单路由 | 例：`/inventory-center/.../receipt-deliver-notice/view/:id/:code/:deliveryType/:sourceRecordCode` |
| 收货结果单路由 | 例：同上 result 路径 |
| 跨子应用 | 例：wujie `jump({ pathname: '/stock' + path })` |

## 本域实现

| 项 | 填写 |
|----|------|
| Section 路径 | 例：`src/pages/.../ReturnPackageReceiptBatchSection.tsx` |
| *Api.ts | 例：`returnPackageReceiptBatchApi.ts` |

## §回退登记表（有则填，无则写「无」）

| 位置 | 回退内容 | 性质 | 待确认 |
|------|----------|------|--------|
| | | 框架 / 宿主 / 业务缺口 / 展示 | |

**禁止**在本文件写未联调确认的 `qp-recordType-eq`、`qp-deliveryType-eq`。
