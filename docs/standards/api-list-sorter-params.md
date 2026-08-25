# API 列表排序参数规范

> **适用范围**：列表、导出、后台管理页等需要 HTTP query 表达**排序**的接口。  
> **目标**：与 `qp-*` 筛选并列，用公开 API 字段表达排序意图，后端白名单映射到 `ORDER BY`。  
> **版本**：1.0 · 2026-08-25

---

## 1. 背景

列表接口通常需要三类 query 参数：

| 类别 | 参数 | 职责 |
|---|---|---|
| 筛选 | `qp-<field>-<operator>` | 字段谓词（AND） |
| 排序 | `sorter` | 单字段 asc/desc |
| 分页 | `page` / `pageSize` | 窗口 |

若排序硬编码在 Repository（如一律 `updated_at DESC`），会出现：

- 业务日期与展示顺序不一致（销售单按修改时间而非 `orderDate`）。
- 前后端对「默认顺序」无共同语言。

本规范固定 **`sorter=<direction>-<field>`** 形态，与 [api-query-predicate-params.md](./api-query-predicate-params.md) 对称。

---

## 2. 格式

```text
sorter=<direction>-<field>
```

| 段 | 允许值 | 示例 |
|---|---|---|
| `direction` | `asc` / `desc` | `desc` |
| `field` | 接口 JSON 公开字段名 | `orderDate`、`createdAt` |

示例：

```text
sorter=desc-orderDate
sorter=asc-createdAt
```

**v1 限制**：仅支持**一个** `sorter` 参数、**一个**字段；不支持 `sorter=a,b` 或多 key。

---

## 3. 字段映射

后端维护白名单 `apiField -> dbColumn`，例如：

```text
orderDate  -> order_date
createdAt  -> created_at
updatedAt  -> updated_at
```

- 客户端 **MUST NOT** 传 `order_date` 等 DB 列名。
- 服务端 **MUST NOT** 把未白名单字段拼进 `ORDER BY`。

---

## 4. 缺省与默认

| 行为 | 约定 |
|---|---|
| 请求**无** `sorter` 或空字符串 | 使用该接口文档登记的 **DefaultSorter** |
| 非法 `sorter` | **400**，message 说明 field/direction/format |
| 前端列表页 | `*Api.ts` 定义 `DEFAULT_*_SORTER`，与后端 Default 一致并默认传入 |

**筛选默认值**与**排序默认值**分开：查询表单可以「无默认筛选」；排序仍应有明确默认（常见：业务日期或创建时间 **desc**）。

---

## 5. 后端实现要点

1. 解析：`ParseSorter(ctx, fieldWhitelist, defaultSpec)` → `{ column, direction }`。
2. `ORDER BY` 只使用白名单 `column` + `ASC`/`DESC` 字面量。
3. 每个列表 Handler 登记：可排字段表 + DefaultSorter。
4. 与 `qp.Apply` 组合顺序：`WHERE`（qp）→ `ORDER BY`（sorter）→ `LIMIT/OFFSET`（分页）。

参考实现（l-project sales-manage）：`apps/sales-manage/internal/pkg/qp/sorter.go`。

---

## 6. 前端实现要点

1. `export const DEFAULT_XXX_SORTER = 'desc-orderDate'`（与后端 Default 一致）。
2. `listXxx(query)` 中：`sorter: query.sorter ?? DEFAULT_XXX_SORTER`。
3. 导出拉全量复用同一 `listXxx`，自动继承排序。
4. UI 未提供排序控件时，仍传默认 `sorter`，不依赖后端隐式行为。

---

## 7. 接口登记模板

### `GET /api/v1/example/items`

| 可排 field | DefaultSorter |
|---|---|
| `orderDate`, `createdAt`, `updatedAt` | `desc-orderDate` |

---

## 8. 与 `qp-*` 边界（再强调）

`qp-*` 的 guideline 已规定排序不在谓词内。统一使用 **`sorter`** 作为排序参数名，避免 `sort` / `sortBy` / `orderBy` 混用。

---

## 9. Code Review 勾选

- [ ] `field` 都是公开 API 字段名？
- [ ] 后端白名单 + 非法 → 400？
- [ ] DefaultSorter 文档化且与前端常量一致？
- [ ] 排序独立于 `qp-*` 与分页？
- [ ] Repository 无未文档化的硬编码 `Order(...)`？

---

## 10. 参考落地（l-project sales-manage）

| 接口 | 可排字段 | Default |
|---|---|---|
| `GET /api/v1/sale/orders` | `orderDate`, `createdAt`, `updatedAt` | `desc-orderDate` |
| `GET /api/v1/sale/orders/invoice-candidates` | 同上 | `desc-orderDate` |
| `GET /api/v1/sale/invoice-docs` | `createdAt`, `updatedAt` | `desc-createdAt` |

前端：`apps/sales-front/src/services/salesOrderApi.ts`、`invoiceDocApi.ts`。
