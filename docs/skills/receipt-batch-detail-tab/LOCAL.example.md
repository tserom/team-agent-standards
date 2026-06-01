# LOCAL.example — 复制为业务项目 `.cursor/skills/receipt-batch-detail-tab/LOCAL.md`

| 项 | 填写 |
|----|------|
| 列表 L1 URL | 例：`GET /stock/reverseRecord/receiptBatchDetail`（**以联调文档为准**） |
| sourceRecordCode | 例：无名包裹路由参数 `code`（包裹单号） |
| 收货通知单路由 | 例：`/returnsManagement/warehousingNotice/view/:id/:code` |
| 收货结果单路由 | 例：`/returnsManagement/receiptResult/view/:id/:code` |
| 本域 Section | 例：`src/pages/ReceivingManagement/ReturnPackage/components/ReturnPackageReceiptBatchSection.tsx` |

**禁止**在本文件写 `qp-recordType-eq`、`qp-deliveryType-eq`。
