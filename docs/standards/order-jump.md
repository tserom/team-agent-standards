# 单据单号统一跳转（orderJump）· 人读完整版

> Agent 短规则：`guidelines/order-jump.md`  
> kb 镜像：`~/Mycodes/kb/domains/company-react/order-jump.md`（事实/踩坑可两边同步）  
> 实现真源：`stock-front` → `src/pages/InventoryCenter/StoreManagement/common/orderJump.ts`  
> 导出：`jumpToOrderDetail(orderType, orderNo, record)`  
> 版本：2026-08-29

---

## 1. 问题

各列表、关联单据、流水里「点单号进详情」若在页面复制 path，会出现：

- DBCK / ODR / JYD 路由不一致、漏查 id
- 子应用 `history.push` 跳到别的微应用 path，丢宿主壳
- 后端 `targetDetailPath` 错误仍被优先使用（清洗单关联单据曾踩坑）

统一入口：按**单号前缀**分支，需要时查接口拿 id，再用 wujie `jump`。

---

## 2. 与菜单跳转的分工

| 能力 | 入口 |
|------|------|
| 侧栏 / 搜菜单进**列表页** | 宿主菜单树 + `handleMenuPush`（见 kb `menu-config-and-nav.md`） |
| 业务**单号**进详情 | **orderJump**（本文） |
| 子应用路由 | 各仓 `config/routes.ts`；详情常 `hideInMenu` |

另：`jumpToInventory(record, text)`（`stock-front/src/utils/utils.ts`）按 `relationRecordType` 数字码跳转，与 orderJump **并存**——按行数据选型，同一列不要混用。

---

## 3. 调用约定

```ts
import { jumpToOrderDetail } from '@/pages/InventoryCenter/StoreManagement/common/orderJump';

jumpToOrderDetail('', relationNo, record);
```

| 参数 | 说明 |
|------|------|
| `orderNo` | **主依据**：trim 后 `startsWith` 前缀 |
| `record` | 可选：`id` / `recordId` / `relationRecordId` / `noticeId`；来源 `sourceRecordCode` / `relationRecordCode` |
| `orderType` | 多数分支未用；可传 `''` 或关系类型文案 |
| 跳转载体 | 优先 `$wujie.props.jump({ pathname, query })`；无 wujie 时 `window.open` 宿主 hash（实现内测试域名，换环境需改） |

查 id 的请求头：`x-biz-code: getResourceCode()`。

---

## 4. 前缀 → 目标（维护表）

改代码时同步改本表。

| 单号前缀 | 单据 | 是否先查接口 | 目标 path 形态（摘要） |
|----------|------|--------------|------------------------|
| `WZ` | 物资凭证 | 否 | `/settle/.../material_asset_voucher/view/{id}/{no}` |
| `ADE` | 收发差异 | 否 | `/distribution/.../receipt-delivery-diff/view/{no}/{id}/{src}` |
| `DON` | 收发货通知 | 是 `GET /stock/rwNoticeRecord/one` | stock 标准单据查询 · 通知详情 |
| `RR` | 收发货结果 | 是 `GET /stock/rwResultRecord` | stock 标准单据查询 · 结果详情 |
| `DBCK` | 调拨单 | 是 `GET /drp-ops/inOutOrder/listNoPage`；`allocateType==20` → 跨组织 out | `transfer-issueDoc[-out]/view/{id}/{no}` |
| `JYD` | 销售 / 采购 | 先销售再采购 | `sales-slip` 或 `purchase-sub-order` |
| `JYTD` | 销售退 / 采购退 | 先销退再采退 | `sales-chargeback` 或 `purchase-return` |
| `RO` | 零售订单 | 是（仍以单号拼 path） | retail `sales-order-list/view/{no}` |
| `RC` | 零售退单 | 是 | retail `retail-chargeback/view/{no}` |
| `RA`/`RB`/`WA`/`WD`/`CA`/`CB`/`CD`/`CE`/`RD` | 门店零售 POS | 是 `GET /pos-ops/posTicketOrder` | marketing `store-sales-order-list/view/{id}/{no}` |
| `ODR` | 其他出入库 | 是 `GET /stock/ohterRwFrontRecord/one`；`deliveryType===0` 入否则出 | `otherIn` / `otherOut` |
| `AJ` | 库存调整 | 是 `GET /stock/adjust?qp-recordType-eq=30` | `inventory-adjustment-doc/view/{id}/{no}` |

未匹配：函数直接 `return`；UI 宜提示「暂不支持跳转该单据」。

---

## 5. MUST / MUST NOT

| ✅ MUST | ❌ MUST NOT |
|---------|-------------|
| 新类型在 orderJump 加分支，列只调入口 | 各业务页复制 DBCK/ODR path |
| 跨子应用 wujie `jump` + 宿主前缀 path | 子应用 `history.push` 拼其它应用 |
| 查 id 带 `x-biz-code` | 未联调就信 `targetDetailPath` |
| 同步本表与 kb 镜像 | 测试宿主 `window.open` 基址当生产永久写死 |

---

## 6. 参考调用

- 清洗单关联单据：`CleaningOrder/config/relatedOrderColumns.tsx`
- 历史原型：`oms-domain-spec` 曾有同名文件；**以 stock-front 当前 `orderJump.ts` 为准**

---

## 7. CR 清单

- [ ] 点单号是否 orderJump（或已论证 path / `jumpToInventory`）？
- [ ] 新前缀是否只改 orderJump + 本文前缀表？
- [ ] 跨应用是否 wujie `jump`？
- [ ] 文档与代码前缀是否一致？
