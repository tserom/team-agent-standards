# API 查询谓词参数规范

> **适用范围**：列表、导出、后台管理页、状态 Tab 等需要通过 HTTP query string 表达字段筛选的接口。  
> **目标**：让前端用公开 API 字段表达筛选意图，后端通过白名单安全映射到查询条件。  
> **版本**：1.0 · 可复制到任意项目 `docs/standards/` 使用。

---

## 1. 背景

团队项目中已经出现过：

```text
qp-id-in=111,222,333
qp-status-eq=1
```

这类参数本质上是放在 HTTP query string 里的受限查询谓词协议。它类似 SQL `WHERE`、OData `$filter`、RSQL/FIQL、Django Filter/Ransack 等设计，但它不是 SQL，也不允许前端表达任意 SQL。

核心边界：

- 前端表达“筛选意图”。
- 后端拥有字段映射、类型转换、权限判断、SQL 生成和参数绑定。
- 每个接口只开放自己声明过的字段与操作符。

---

## 2. 格式

统一采用：

```text
qp-<field>-<operator>=<value>
```

| 段 | 含义 | 示例 |
|---|---|---|
| `qp` | query predicate/query parameter 前缀 | 固定 |
| `field` | 公开 API 字段名 | `id`、`createdAt`、`partyName` |
| `operator` | 后端允许的受限操作符 | `eq`、`in`、`gte` |
| `value` | query string 值，按字段类型解析 | `1`、`1,2,3`、`2026-01-01` |

示例：

```text
qp-id-eq=1
qp-id-in=1,2,3
qp-status-eq=enabled
qp-partyName-like=客户A
qp-createdAt-gte=2026-01-01
qp-createdAt-lte=2026-01-31
```

---

## 3. 字段名规则

`field` 是 API 契约的一部分，必须使用接口请求/响应里的公开字段名，默认 camelCase：

```text
qp-createdAt-gte=2026-01-01
qp-partyName-like=客户A
```

后端通过白名单映射到真实查询字段：

```text
id -> id
status -> status
partyName -> party_name
createdAt -> created_at
```

选择 API 字段名的原因：

1. URL 参数属于 API 契约，不属于数据库契约。
2. 前端不需要知道数据库列名或 ORM 字段名。
3. 后端可以在不破坏前端参数的情况下调整表结构、join、视图或计算字段。
4. 同一个 API 字段可以映射到单列、关联表列或表达式，但这个映射必须由后端显式维护。

默认禁止：

```text
qp-party_name-like=客户A
qp-created_at-gte=2026-01-01
```

除非该接口本身公开字段就是 snake_case。

---

## 4. v1 操作符

第一版只保留小集合，避免协议过早变成一门查询语言。

| Operator | 含义 | SQL 类比 | 示例 |
|---|---|---|---|
| `eq` | 等于 | `=` | `qp-id-eq=1` |
| `ne` | 不等于 | `!=` | `qp-status-ne=disabled` |
| `in` | 多值命中 | `IN (...)` | `qp-id-in=1,2,3` |
| `like` | 模糊匹配 | `LIKE` | `qp-partyName-like=客户A` |
| `gt` | 大于 | `>` | `qp-amount-gt=100` |
| `gte` | 大于等于 | `>=` | `qp-createdAt-gte=2026-01-01` |
| `lt` | 小于 | `<` | `qp-amount-lt=1000` |
| `lte` | 小于等于 | `<=` | `qp-createdAt-lte=2026-01-31` |

默认多个 `qp-*` 条件之间是 `AND` 关系。

`like` 的具体语义必须按字段声明：默认建议 contains，也可以对个别字段声明 prefix。

---

## 5. 后端契约

每个接口必须维护自己的白名单：

```text
API field + operator -> query builder action
```

示例：

```text
id + eq -> WHERE id = ?
id + in -> WHERE id IN ?
partyName + like -> WHERE party_name LIKE ?
createdAt + gte -> WHERE created_at >= ?
createdAt + lte -> WHERE created_at <= ?
```

后端解析要求：

1. 未注册字段返回 400。
2. 字段存在但不支持该 operator 返回 400。
3. 类型转换失败返回 400，例如 `qp-id-in=1,abc`。
4. `in` 使用英文逗号分隔，后端按字段类型逐项转换。
5. 空字符串是否有效由字段定义决定，默认忽略空值或返回 400，不能静默拼入 SQL。
6. 所有查询必须走参数绑定或 ORM query builder，禁止字符串拼接 SQL。
7. 字段是否可查还要受权限控制；不能因为存在 `qp-*` 就允许查询敏感字段。

---

## 6. 前端契约

前端只按 API 字段名组装参数：

```ts
const params = {
  "qp-id-in": selectedIds.join(","),
  "qp-partyName-like": partyName,
  "qp-createdAt-gte": dateRange[0],
  "qp-createdAt-lte": dateRange[1],
}
```

前端不应该：

1. 传数据库列名。
2. 拼接 SQL 片段。
3. 传未在接口文档中声明的 `qp-*` 字段。
4. 同时传语义冲突的条件，例如 `qp-id-eq=1` 和 `qp-id-in=2,3`，除非接口文档明确允许。

UI 配置、表格配置、导出动作都应使用同一套公开 API 字段名。

---

## 7. 与 SQL 的关系

这套协议很像 SQL `WHERE` 谓词：

```text
qp-id-in=1,2,3
```

后端可以翻译为：

```sql
WHERE id IN (?, ?, ?)
```

但 query string 不是 SQL 传输格式。前端表达的是筛选意图，SQL 字段、join、表达式、参数绑定都由后端控制。

---

## 8. 边界

适用：

- 列表筛选
- 导出筛选
- 管理后台表格筛选
- 状态 Tab 映射到单字段谓词
- 日期、数字、字符串范围筛选

v1 不支持：

- `OR`
- 括号
- 嵌套条件
- 任意关联路径，如 `user.company.name`
- 任意 SQL 函数
- 排序
- 分页
- 全文/多字段搜索

分页、排序、全局搜索保持自己的顶层参数：

```text
page=1
pageSize=20
sort=createdAt:desc
q=keyword
```

---

## 9. 接口文档模板

每个接口文档在筛选部分列出允许字段：

| Query Param | Type | Meaning |
|---|---|---|
| `qp-id-eq` | number | 精确筛选单个 ID |
| `qp-id-in` | number[] | 筛选多个 ID，逗号分隔 |
| `qp-status-eq` | string | 按状态筛选 |
| `qp-partyName-like` | string | 按主体名称模糊筛选 |
| `qp-createdAt-gte` | date/datetime | 创建时间起点 |
| `qp-createdAt-lte` | date/datetime | 创建时间终点 |

---

## 10. Code Review 清单

- [ ] `qp-*` 的 `field` 是否都是公开 API 字段名？
- [ ] 后端是否显式白名单 `field + operator`？
- [ ] 非法字段、非法 operator、类型转换失败是否返回 400？
- [ ] SQL 是否通过参数绑定或 query builder 生成？
- [ ] 分页、排序、全文搜索是否留在 `qp-*` 之外？
- [ ] 是否没有引入 `OR`、嵌套条件、任意路径等 v1 不支持能力？
