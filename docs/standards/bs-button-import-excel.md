# 公司列表页 Excel 导入接入指南（`bs-buttonImportExcel`）

> 晋升自知识库 `kb/domains/company-react/bs-button-import-excel.md`（2026-08-07）。  
> Agent 短规则：`guidelines/bs-button-import-excel.md`。  
> **仅公司存量体系**（bssula 自定义插件）；个人项目禁止引入。

事实对照：各子应用 `plugins/CustomPlugin/Render/BsButtonImportExcel/`；样例含 HOLD 单策略、寻源指定 SKU、retail-front 评论列表抖音导入。

---

## 1. 先选型（命中即停）

| 场景 | 用什么 | 不要用 |
|------|--------|--------|
| 列表工具栏、oms-ops `excelImport` 或同类「上传 → 成功数/失败数/结果文件」 | **`bs-buttonImportExcel`** | 再抄一整页 Steps 导入 |
| 导入是主流程、多类型、要独立路由/历史 | 独立导入页（`CommonImport` / 自建 Steps） | 硬塞进 `actionsRender` 小按钮 |
| 极简同步导入、只要 Upload + L1 API、与本页其它 Modal 统一风格 | 自定义 Modal | 为省事再造一套 Steps |

多数 **oms-ops `/excelImport/...`** 列表导入 → 选 **`bs-buttonImportExcel`**。

---

## 2. `bs-buttonImportExcel` 是什么

Sula 自定义 Render 插件（各子应用 `plugins/CustomPlugin/Render/BsButtonImportExcel/`）：

1. 工具栏按钮打开 Modal  
2. Modal 内 `ModalImport`：两步（上传 → 结果）  
3. 上传成功后解析 `response.data` 的 `count` / `failedNum` / `successNum` / `url`，并调用表格 `refreshTable`

上传控件走 antd `Upload`，`action` 指向导入接口；鉴权 header 由插件内 `handleRequestHeader` 注入。

---

## 3. 列表页最小配置（推荐模板）

放在 `BsSulaQueryTable` 的 `actionsRender` 里：

```ts
{
  type: 'bs-buttonImportExcel',
  // code: 'OMS_xxx_Import', // 有权限码时挂上
  props: {
    modalButtonParams: {
      type: 'primary',
      children: '导入',
    },
    ModalParams: {
      width: '80%',
      title: '导入',
    },
    ModalImportParams: {
      title: '导入',
      actionMethod: 'get', // 仅影响「下载模版」请求 method
      documentName: '某某导入模版.xlsx',
      actionUrl: '/oms-ops/excelImport/importXxx', // 上传接口
      DownLoadUrl: '/oms-ops/excelImport/getXxxTemplate', // 模版接口
      maxSize: 20,
      isNeedDownloadTemplate: true,
      isNeedDownloadResult: true,
      isDownloadTemplateNeedAjax: true,
      isUrlDownFile: false, // false=模版按 blob 下载；true=接口返回 URL 再 downFile
      // ruleList: ['1、……'], // 可选；不传用默认一句提示
    },
  },
},
```

**真实例子（retail-front）**

| 页面 | actionUrl | DownLoadUrl |
|------|-----------|-------------|
| HOLD 单策略 | `/oms-ops/holdOrderPolicy/importHoldOrderPolicy` | `.../importDownloadHoldOrderPolicyTemplate` |
| 寻源指定 SKU | `/oms-ops/seekConfigScope/importSeekConfigSku?...` | `.../importSkuTemplate` |
| 评论列表抖音 | `/oms-ops/excelImport/importDouyinOrderComment` | `.../importDouyinOrderCommentTemplate` |

路径示例：`retail-front/src/pages/CommentManagement/CommentList/index.tsx`。

---

## 4. `ModalImportParams` 字段速查

| 字段 | 含义 | 默认/注意 |
|------|------|-----------|
| `actionUrl` | 上传地址（Upload `action`） | 必填；一般为 POST multipart |
| `DownLoadUrl` | 模版下载地址 | 与 `isNeedDownloadTemplate` 联用 |
| `actionMethod` | **下载模版** 的 HTTP method | 常见 `'get'`；**不是**上传 method |
| `documentName` | 模版/结果本地文件名 | 含 `.xlsx` |
| `maxSize` | 上传大小上限（MB） | 常见 `20` |
| `actionAccept` | 接受扩展名 | 默认 `.xlsx,.xls` |
| `isNeedDownloadTemplate` | 是否展示「下载导入模板」 | 列表导入通常 `true` |
| `isNeedDownloadResult` | 结果步是否「下载导入结果」 | 后端有 `url` 时 `true` |
| `isDownloadTemplateNeedAjax` | 模版是否走 request | `true` 调接口；`false` 则 `DownLoadUrl` 当直链 |
| `isUrlDownFile` | ajax 后如何落盘 | `false`：`responseType:'blob'` + `downFileByBuffer`；`true`：JSON 里取 URL 再 `downFile` |
| `ruleList` | 导入规则文案数组 | 空则默认一句「请严格遵守模版…」 |
| `title` | 弹层内大标题 | 与 `ModalParams.title` 可同文案 |
| `refreshTable` | 成功后刷新 | **插件自动从表格 ctx 注入**，页面不用传 |

---

## 5. 后端约定（前端依赖）

上传成功且业务成功时，插件读：

```ts
response.data = {
  count,       // 提交条数
  failedNum,   // 失败条数
  successNum,  // 成功条数
  url,         // 结果文件地址（可空）；有则「下载导入结果」可用
}
```

`handleError(response)` 为真才算成功并 `refreshTable()`。字段名以现网 `ImportResVo` 为准；若后端字段不同，要么改后端对齐，要么不要硬套本插件。

模版下载两种常见形态：

1. **blob 流**（`isUrlDownFile: false`）— excelImport 模版接口多数如此  
2. **返回可下载 URL**（`isUrlDownFile: true`）— 如部分 `getDownloadLink` 类接口  

---

## 6. 其它导入方式（对照，少用再选）

| 方式 | 代表 | 何时用 |
|------|------|--------|
| 独立路由 + `CommonImport` / UploadModal | 仓阈值 `warehouse-threshold/import.tsx` | 导入页是独立菜单能力 |
| 自建大 Steps 页 | 零售单 / 平台单导入 | 多类型、复杂校验、导入历史 |
| 自定义 Modal + `Upload.Dragger` + L1 | 客户信用等级 `ImportCreditModal` | 无标准结果文件、要控 UI |
| `ImportExcelModal` 配置化 Modal | 门店零售单 | 项目内已封装、参数可配时复用 |

**默认**：列表一个按钮 → **`bs-buttonImportExcel`**。不要无故新开导入路由。

---

## 7. 接入检查清单

- [ ] 已确认后端是 excelImport 风格（成功数 + 可选结果 url）  
- [ ] `actionUrl` / `DownLoadUrl` 与文档一致（含网关前缀如 `/oms-ops`）  
- [ ] 模版下载：blob 用 `isUrlDownFile: false`；URL 用 `true`  
- [ ] `documentName` 带扩展名  
- [ ] 需要权限时补 `code`  
- [ ] 导入成功后列表会刷新（依赖表格 ctx，勿拆到无 table 的纯 Form 页硬套）  
- [ ] 插件路径以**本仓** `plugins/.../BsButtonImportExcel` 为准（子应用可能有拷贝）  

---

## 相关

- Agent 短规则：`guidelines/bs-button-import-excel.md`  
- BsSulaQueryTable Skill：`docs/skills/bssula-query-table/SKILL.md`  
- 知识库镜像：`kb/domains/company-react/bs-button-import-excel.md`  
