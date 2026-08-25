# API 列表排序参数：`sorter`

设计或修改列表、导出、后台管理**排序**时，默认使用受限排序参数：

```text
sorter=<direction>-<field>
```

**人类可读完整版**：`docs/standards/api-list-sorter-params.md`  
与 [`api-query-predicate-params.md`](api-query-predicate-params.md) 并列：**筛选走 `qp-*`，排序走 `sorter`**，分页仍用 `page` / `pageSize`。

---

## 基本约定

| 段 | 含义 | 例子 |
|---|---|---|
| `direction` | `asc` 升序 / `desc` 降序 | `desc` |
| `field` | **公开 API 字段名**（camelCase） | `orderDate`、`createdAt` |

示例：

```text
sorter=desc-orderDate
sorter=asc-createdAt
```

v1 **仅单字段**；缺省 `sorter` 时后端用接口登记的默认排序；前端 `*Api.ts` 应显式传同名默认值。

---

## 字段名规则

`sorter` 的 `field` 必须用公开 API 字段名；后端白名单映射 DB 列：

```text
orderDate -> order_date
createdAt -> created_at
```

禁止传数据库列名或 SQL 片段。

---

## 边界

| 参数 | 用途 |
|---|---|
| `qp-*` | 筛选 |
| `sorter` | 排序 |
| `page` / `pageSize` | 分页 |

不要把排序塞进 `qp-*`；不要与 `sortBy` / `orderBy` 等多套命名并存。

---

## 后端 MUST / MUST NOT

| ✅ MUST | ❌ MUST NOT |
|---|---|
| 每接口维护 `field -> column` 白名单 | 把客户端 `field` 直接拼 SQL |
| 未知 field、非法 direction、格式错误 → **400** | v1 多 `sorter` 或逗号多列 |
| 缺省 `sorter` 使用文档声明的默认 | 各接口默认不一致却不写文档 |

---

## 前端 MUST

- 每个列表 export 声明 `DEFAULT_*_SORTER` 常量，`list*` 默认带上 `sorter`。
- 查询表单筛选值与排序分离：**筛选无默认值**不等于**排序无默认值**。

---

## PR 勾选

- [ ] `field` 是否都是公开 API 字段名？
- [ ] 后端是否白名单 + 400？
- [ ] 缺省默认是否与文档、前端常量一致？
- [ ] 排序是否独立于 `qp-*` 与分页？
