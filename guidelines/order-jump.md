# 单据单号统一跳转（orderJump）

实现或修改**公司仓**前端里「点业务单号进详情」时遵守。个人项目无微前端子应用单据体系则忽略。

人读完整版（前缀表、案例）：`docs/standards/order-jump.md`  
事实与踩坑真源（可同步）：kb `domains/company-react/order-jump.md`  
实现真源（stock-front）：`src/pages/InventoryCenter/StoreManagement/common/orderJump.ts` → `jumpToOrderDetail`

菜单进列表页 ≠ 单号进详情：菜单见宿主搜菜单 / `menu-config-and-nav`；单号走本文。

## 选型（命中即停）

| 数据形态 | 做法 |
|----------|------|
| 只有业务单号（`DBCK…` / `ODR…` / `JYD…` 等） | **`jumpToOrderDetail('', orderNo, record)`** |
| 后端 `targetDetailPath` 等 path **已联调确认正确** | 可用 path |
| 行上有可靠 `relationRecordType` 数字码（库存流水等） | 可用既有 `jumpToInventory`；**同一列不要混两套** |

关联单据 Tab、报表、可视化弹窗点单号：默认 orderJump。

## MUST / MUST NOT

| ✅ MUST | ❌ MUST NOT |
|---------|-------------|
| 新单据类型在 **orderJump 加前缀分支**，业务列只调入口 | 在清洗/维修/报表列复制一套 DBCK/ODR path |
| 跨子应用用 `window.$wujie.props.jump`，pathname 带 `/stock` `/distribution` 等宿主前缀 | 子应用 `history.push` 拼其它微应用 path |
| 查 id 的请求带 `x-biz-code`（`getResourceCode()`） | 未验证就信后端下发的详情 path |
| 改前缀/path 时同步 `docs/standards/order-jump.md`（及 kb 镜像） | 把 `window.open` 测试宿主域名当生产写死不改 |

## 调用

```ts
import { jumpToOrderDetail } from '@/pages/InventoryCenter/StoreManagement/common/orderJump';

jumpToOrderDetail('', orderNo, record);
```

未匹配前缀时函数静默 return；调用方宜 `message.warning('暂不支持跳转该单据')`。

## PR 勾选

- [ ] 点单号是否走 `jumpToOrderDetail`（或已论证的 path / `jumpToInventory`）？
- [ ] 新前缀是否只改 orderJump + 文档表，而非散落在列 render？
- [ ] 跨应用是否 wujie `jump`？
