---
name: bssula-query-table
description: >-
  Bit-Sun BsSulaQueryTable 查询列表 config 轻量索引：remoteDataSource、fields、columns、
  initialValues、rules、ref、converter。切换视图保留查询仅选型表，细节见知识库
  tab-query-sync.md。Use when BsSulaQueryTable, 列表/明细模式, refreshTable,
  切换视图保留查询, Segmented, remount-init.
disable-model-invocation: false
---

# BsSulaQueryTable（团队通用）

## 何时读本 Skill

凡涉及以下任一项，**先读本文件再写代码**（不要凭记忆猜 bssula / Sula 查询表 API）：

- 页面或 Modal 中的 `BsSulaQueryTable` / `SulaQueryTable`
- `config` / `detailConfig` 传给 `<BsSulaQueryTable {...config} />`
- Tab 下双表（列表模式 + 明细模式）
- **同一页 Segmented / 条件渲染切换多张 `BsSulaQueryTable`，切换后查询条件要保留**
- 查询区 `fields`、`initialValues`、`rules`、`formProps`
- `tableRef.current?.tableRef?.current?.refreshTable()` 等 ref 链

整页路由、菜单、Form 页脚手架见各业务项目的 **page-scaffold** 类 Skill；本 Skill 只管 **查询表 config**。

## 业务项目落地（复制本 Skill 后补一行）

各仓库封装路径不同，在业务项目 `.cursor/skills/bssula-query-table/` 旁可放 `LOCAL.md`（可选），至少写明：

| 项 | 示例（按项目替换） |
|----|-------------------|
| 页面 import 路径 | `@/components/businessComponent/BsSulaQueryTable` |
| 底层包 | `@bit-sun/business-component` 的 `BsSulaQueryTable` |
| `itemPath` 等默认 props | 如 `stock`、`oms` |
| 参考页路径 | 本仓库内 2～3 个典型列表页相对路径 |

Agent 写代码时 **以业务项目 LOCAL.md 或首个同类页面为准**，不要假设固定 monorepo 名。

## 典型分层

| 层级 | 说明 |
|------|------|
| 项目封装 | 常包一层 `PageHeaderWrapper`、`access`；`needPageHeader: false` 时直出内层表 |
| 业务组件 | `@bit-sun/business-component` 的 `BsSulaQueryTable` |

```tsx
import BsSulaQueryTable from '<项目封装路径>';

const tableRef = useRef<any>(null);

const config = {
  tableCode: 'your-table-code', // 列设置持久化
  fields: [/* 查询项 */],
  columns: [/* 列 */],
  remoteDataSource: { url, method, convertParams, converter },
  initialValues: { /* 查询表单默认值 */ },
  actionsRender: [/* 工具栏 */],
  rowKey: 'id',
};

<BsSulaQueryTable {...config} forwardedRef={tableRef} needPageHeader={false} />
```

## config 常用键

| 键 | 用途 |
|----|------|
| `remoteDataSource` | 列表接口；`convertParams` 常链通用 `tableConvertParamsType` + 业务函数 |
| `converter` | 把 `{ items, total }` 转成 `{ list, total }`（或项目封装的 `handleConvertResponse`） |
| `fields` | 查询表单；参数名 `qp-字段-like/eq/in`、日期 `qp-a-ge*fullDate*qp-b-le` |
| `initialValues` | **查询区默认值**（见下） |
| `columns` | 列；`key` 与接口字段一致；`render` / `dictionaryCode` |
| `actionsRender` | 工具栏按钮（导出、新增等） |
| `formProps` | **仅**在默认查询按钮不够用时覆盖（见下） |
| `rowSelection` / `summaryList` / `statusMapping` | 按页 |
| `autoInit: false` | 禁止挂载自动查；需用户点查询（配合自定义校验） |

## Ref 与刷新

```ts
// 刷新列表
tableRef?.current?.tableRef?.current?.refreshTable();

// 读查询条件（导出、批量）
tableRef?.current?.formRef?.current?.getFieldsValue();
```

## 查询默认值与必填（推荐写法）

| 点 | 不推荐 | 推荐 |
|----|--------|------|
| 默认时间 | 无 / 只在 action 里写 | `config.initialValues` |
| 必填 | 重写整段 `formProps` + 自定义 `validator` + `setFields` | `fields[].rules: [{ required: true, message: '…' }]` |
| 查询按钮 | 自己拼 `refreshTable` | 用默认「查询」（会校验 `rules`） |

**示例：默认近 7 天创建时间 + 备注模糊查**

```ts
const CREATE_TIME_FIELD = 'qp-createTime-ge*fullDate*qp-createTime-le';

function getDefaultCreateTimeRange() {
  return [moment().subtract(6, 'days').startOf('day'), moment().endOf('day')];
}

const config = {
  initialValues: {
    [CREATE_TIME_FIELD]: getDefaultCreateTimeRange(),
  },
  fields: [
    {
      name: CREATE_TIME_FIELD,
      label: '开始时间',
      field: {
        type: 'rangepicker',
        props: { format: 'YYYY/MM/DD', placeholder: ['开始时间', '结束时间'] },
      },
      rules: [{ required: true, message: '请输入此查询条件' }],
    },
    {
      name: 'qp-remark-like',
      label: '备注',
      field: {
        type: 'input',
        props: { placeholder: '请输入', allowClear: true, maxLength: 100 },
      },
    },
  ],
};
```

**原则：** 不要为「默认值 / 单字段必填」去重写 `formProps.actionsRender`，除非要做 **rules 表达不了的** 逻辑（例如「吊牌码与来源单号至少填一个」）。

**自定义查询链示例（多条件二选一、autoInit）**

```ts
formProps: {
  actionsRender: [
    {
      type: 'button',
      props: { type: 'primary', children: '查询' },
      action: [
        (ctx) => {
          /* 自定义判断，失败 return Promise.reject() */
        },
        { type: 'validateQueryFields', resultPropName: '$queryFieldsValue' },
        { type: 'refreshTable', args: [{ current: 1 }, '#{result}'] },
      ],
    },
    {
      type: 'button',
      props: { children: '重置' },
      action: ['resetFields', { type: 'resetTable', args: [false] }],
    },
  ],
},
```

## 列表 + 明细双表（Tab）

```ts
const detailConfig = {
  ...config,
  tableCode: 'xxx-detail',
  remoteDataSource: { /* 明细接口 */ },
  columns: detailColumns,
};
```

- `...config` 可继承 `fields`；明细只换 `columns` / `remoteDataSource` / `tableCode`。
- **切换要带查询条件**：见下节（细节以知识库为准，本 Skill 不展开长文）。

## 切换视图保留查询条件（轻量索引）

> **细节 / 踩坑 / 定稿写法真源**：维护者知识库  
> `~/Mycodes/kb/domains/company-react/tab-query-sync.md`  
> Agent 实现或排障时：**先读该 kb 文**，再对照业务项目 `LOCAL.md` 参考页。本 Skill 只保留选型与禁令。

| 场景 | 推荐 |
|------|------|
| Tab「列表 / 明细」 | **A · remount-init**（`destroyInactiveTabPane` + seed `initialValues` + `onChange` 里 `scheduleApply` 单次 refresh；优先不用 `useEffect([activeKey])`） |
| Segmented 等条件渲染只挂一张表 | **B · `requestParamsRef` + `initialValues`** |

单据列表目录/复杂度/行操作白名单：团队 `guidelines/document-list-page-simple.md`（人读 `docs/standards/document-list-page-simple.md`）。  
`useEffect` 通则：`guidelines/use-effect-prefer-events.md`。

**MUST NOT**

- 默认用 `useEffect([activeKey])` 隐式串「回填 + 请求」（能 `onChange`+schedule 就不用；例外见 prefer-events）
- Tab 侧默认 `autoInit` 空查一遍再同步查一遍（两次 loading）
- 模式 B 只靠 `convertParams` 偷塞条件、不配 `initialValues`
- 把完整 playbook 写进业务页注释代替维护 kb
- 整页复制维修单列表当新单据模板（见 document-list-page-simple）

**参考页**：一律见业务项目 `LOCAL.md`（勿在本 Skill 写死仓库路径）。

## convertParams / 查询参数

- 通用：项目内的 `handleDealFormSearchField`、`handleConvertParams` 等
- 日期范围在 `convertParams` 里常格式化为 `YYYY-MM-DD 00:00:00` / `23:59:59`
- 模糊：`qp-remark-like` 等 `like` 后缀

## converter 与分页

- 分页列表：接口 `{ items, total }` → `{ list, total }`（数组 + 数字）
- **无分页全量**：`converter` 必须返回 **`list` 为数组**；若返回对象且未包成数组，易出现 `rawData.some is not a function`
- 关分页：在 `tableProps` / 组件 props 里设 `pagination: false`（以 `@bit-sun/business-component` 文档为准）；`remoteDataSource` 仍要写对 `converter`

## 权限

- 工具栏 / 操作列：项目约定的 `code` + `isPermissionColumn: true`
- 链接：`authFn('<权限码>')` + `disabled`

## 场景对照（在业务仓库找同类页）

| 场景 | 在本项目搜索 |
|------|----------------|
| 双 Tab 列表+明细 | `detailConfig` + `Tabs` + 两个 `BsSulaQueryTable` |
| Tab 切换保留查询（模式 A · remount-init） | 见 LOCAL.md + kb `tab-query-sync.md` |
| Segmented 切换保留查询（模式 B） | 见 LOCAL.md + kb `tab-query-sync.md` |
| 查询必填（多条件二选一） | `validateQueryFields` + 自定义 `formProps.actionsRender` |
| `autoInit: false` + 自定义查询 | `autoInit` + 自定义查询按钮 action |
| 默认 `initialValues` | `initialValues` + `rangepicker` |

## 自检

- [ ] 是否用了 `initialValues` 而不是重写查询按钮做默认？
- [ ] 必填是否用 `fields[].rules`，而非多余 `formProps`？
- [ ] `converter` 的 `list` 是否为数组？
- [ ] 双表是否 `...config` 继承查询区？
- [ ] **切换视图要保留查询**：先读 kb `tab-query-sync.md`；Tab → remount-init；条件渲染 → 模式 B？
- [ ] ref 是否为 `tableRef.current?.tableRef?.current`？
- [ ] import 是否用了**本项目**封装路径（见 LOCAL.md）？
