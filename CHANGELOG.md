# Changelog

## Unreleased

### Added

- `guidelines/order-jump.md` + `order-jump.mdc`：公司仓点业务单号进详情优先 `jumpToOrderDetail`；禁止列内复制 path；与 `jumpToInventory` / 菜单跳转分工。
- `docs/standards/order-jump.md`：人读完整版（前缀表、CR）；kb 镜像 `domains/company-react/order-jump.md`。

### Added

- `guidelines/api-list-sorter-params.md` + `api-list-sorter-params.mdc`（`alwaysApply`）：列表排序 `sorter=<asc|desc>-<field>`，与 `qp-*` 并列；field 白名单、DefaultSorter、前后端常量一致。
- `docs/standards/api-list-sorter-params.md`：人读完整版（格式、边界、CR、l-project sales-manage 参考落地）。

### Added

- `guidelines/use-effect-prefer-events.md` + `use-effect-prefer-events.mdc`（`alwaysApply`）：能不用 `useEffect` 就不用；不得不用须先提示用户且 effect 极薄。
- `guidelines/document-list-page-simple.md` + `document-list-page-simple.mdc`：公司仓单据列表目录瘦身、复杂度预算、双视图 remount-init、行操作白名单。
- `docs/standards/document-list-page-simple.md`：人读完整版（自 stock-front 草稿晋升）。
- `docs/skills/bssula-query-table/SKILL.md`：链到上述列表规范与 useEffect 通则。

- `guidelines/table-summary-field-map.md` + `table-summary-field-map.mdc`：列表 summary / 导出合计 / 后端汇总按公开字段 key 映射，禁止 `colSpan`/下标/空串占位。
- `docs/standards/table-summary-field-map.md`：人读完整版（成因、MUST/NOT、横跨文案、CR 清单）。

### Changed

- `guidelines/react-readability.md` §2：交叉引用 `use-effect-prefer-events`。

### Added

- `guidelines/antd-input-number-select-on-focus.md` + `antd-input-number-select-on-focus.mdc`：antd 可编辑 `InputNumber` 默认聚焦全选（`requestAnimationFrame` + `select`）；优先项目封装。
- `docs/standards/antd-input-number-select-on-focus.md`：人读配套（边界、校验、销售单范本路径）。

### Changed

- `docs/skills/bssula-query-table/SKILL.md`：**切换视图**改为轻量索引（Tab 定稿 remount-init；禁 `useEffect([activeKey])`）；长文/踩坑指向知识库 `kb/domains/company-react/tab-query-sync.md`，不再在 Skill 内展开模式 B 三步长文。`LOCAL.example.md` 同步。
- `guidelines/api-layering.md` + `api-layering-decision.mdc`：§响应字段契约；禁止未声明业务字段 `??` 链；回退须登记并单列待确认；PR 勾选 +1。
- `docs/standards/api-abstraction-encapsulation-reuse.md` §3.4：响应字段契约、回退登记表、CR 清单增补（v1.1）。
- `guidelines/receipt-batch-detail-tab.md` + standard + skill：other-in 与业务域 VO 分表；`*ReceiptBatchRow`；回退登记表模板；修正「字段同 other-in」表述。
- `docs/skills/bssula-query-table/SKILL.md`：新增「切换视图保留查询条件」模式 A（Tab + pendingQueryFieldSyncRef）/ 模式 B（条件渲染 + requestParamsRef + initialValues）；`LOCAL.example.md` 补 stock-front 参考页。

### Added

- `guidelines/api-query-predicate-params.md` + `api-query-predicate-params.mdc`：API 查询谓词参数 `qp-<field>-<operator>`，统一公开 API 字段名、后端白名单映射与 v1 操作符边界。
- `docs/standards/api-query-predicate-params.md`：人读完整版（字段名规则、后端/前端契约、SQL 类比、接口文档模板、CR 清单）。
- `guidelines/receipt-batch-detail-tab.md` + `receipt-batch-detail-tab.mdc`：收货批次明细 Tab（新列表 URL、仅 `qp-sourceRecordCode-eq`、行字段同 other-in）。
- `docs/standards/receipt-batch-detail-tab.md`：人读完整版（接口差异、列、Link 字段表）。
- `docs/skills/receipt-batch-detail-tab/SKILL.md` + `LOCAL.example.md`：实现流程与业务项目 LOCAL 模板。

- `guidelines/api-layering.md`：API 分层（抽象/封装/复用）L0–L3 与 5 问决策；对应 Cursor 规则 `api-layering-decision.mdc`（`alwaysApply: true`）。
- `docs/standards/api-abstraction-encapsulation-reuse*.md`：完整规范与一页纸（中/英）。
- `docs/REPOSITORY_STRUCTURE.md`：本仓库职能与各目录说明。
- `guidelines/promote-to-team-standards.md` + `promote-to-team-standards.mdc`：Agent 在可复用规则/Skill 时提醒晋升团队真源。
- `docs/skills/README.md`：团队 Skill 模板目录约定。
- `docs/skills/bssula-query-table/SKILL.md`：BsSulaQueryTable 查询表 config 通用 Skill；`LOCAL.example.md` 供业务项目落地路径。

### Changed

- README / `docs/other-agents.md`：区分 Cursor 首次安装与**增量更新**（`cp …/*.mdc`，避免覆盖项目专用 rules）。
- `build.py` 构建结束提示默认打印增量复制命令。

- 构建产物改为可见路径（如 `generated/cursor/rules/`，不再生成隐藏的 `.cursor` 目录）。
- 构建输出改为 `generated/<agent-id>/` 分目录，不再提供安装脚本。
- **方案 B**：各 Agent 产物在 `generated/<agent-id>/` 下，构建只清空该子目录。
- Git 合代码规范改为通用 MR/PR 草稿流程（不限 GitLab / `test`）。

### Added

- **工具无关真源** `guidelines/*.md`（Karpathy、React 可读性、回复文件表、Git MR）。
- `agent-manifest.json`：Agent 列表；输出目录固定为 `generated/<id>/`。
- `docs/other-agents.md`：各工具 `build.py <id>` 与复制说明。
- `scripts/build.py` / `scripts/build.sh`：统一构建入口。

### Removed

- `install-cursor.sh`、`install-agents-md.sh`、`install-all.sh`、`install-to-project.sh`。
- 手写 `rules/*.mdc` 作为真源（改为构建产物）。
