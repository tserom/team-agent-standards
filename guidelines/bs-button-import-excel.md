# 列表 Excel 导入：优先 `bs-buttonImportExcel`

在公司前端（bssula / `BsSulaQueryTable`）列表工具栏做 Excel 导入时**默认遵守**。个人项目禁止引入。

**人读完整版**（字段速查、后端约定、其它导入方式对照）：`docs/standards/bs-button-import-excel.md`  
**环境事实 / 页面样例**：知识库 `kb/domains/company-react/bs-button-import-excel.md`（可与本仓库同步）

与 [bssula-query-table](../docs/skills/bssula-query-table/SKILL.md) 配合：配置写在 `actionsRender`。

---

## 选型（命中即停）

| 场景 | ✅ 用 | ❌ 不要 |
|------|------|--------|
| 列表按钮 + oms-ops `excelImport`（或同类：成功数/失败数/结果 url） | **`type: 'bs-buttonImportExcel'`** | 再抄一整页 Steps / 独立导入路由 |
| 导入是主流程、多类型、要历史页 | 独立导入页 | 硬塞进列表小按钮 |
| 极简同步 Upload、无标准结果文件 | 自定义 Modal + L1 | 为省事硬套本插件 |

---

## MUST / MUST NOT

| ✅ MUST | ❌ MUST NOT |
|---------|-------------|
| 列表工具栏用插件配置：`actionUrl` + `DownLoadUrl` + `documentName` | 无故新开导入路由复制 Steps |
| 模版 blob 流：`isUrlDownFile: false`；接口返回 URL：`true` | 搞混 `actionMethod`（它只影响**下载模版**，不是上传 method） |
| 有权限码时挂 `code` | 假定各子应用插件路径完全一致而不看本仓 `plugins/.../BsButtonImportExcel` |
| 成功依赖表格 ctx 自动 `refreshTable` | 在无 table 的纯 Form 页硬套本插件却期望刷新 |

---

## 最小配置骨架

```ts
{
  type: 'bs-buttonImportExcel',
  // code: 'OMS_xxx_Import',
  props: {
    modalButtonParams: { type: 'primary', children: '导入' },
    ModalParams: { width: '80%', title: '导入' },
    ModalImportParams: {
      title: '导入',
      actionMethod: 'get',
      documentName: '某某导入模版.xlsx',
      actionUrl: '/oms-ops/excelImport/importXxx',
      DownLoadUrl: '/oms-ops/excelImport/getXxxTemplate',
      maxSize: 20,
      isNeedDownloadTemplate: true,
      isNeedDownloadResult: true,
      isDownloadTemplateNeedAjax: true,
      isUrlDownFile: false,
    },
  },
}
```

插件期望成功响应 `data` 含：`count` / `failedNum` / `successNum` / `url`（以现网 ImportResVo 为准）。

---

## PR 勾选

- [ ] 是否列表场景且后端为 excelImport 风格？否则是否已改选型？
- [ ] `actionUrl` / `DownLoadUrl` / `documentName` / `isUrlDownFile` 是否与联调一致？
- [ ] 权限 `code` 是否已挂（如有）？
- [ ] 是否避免无故新开导入页？
