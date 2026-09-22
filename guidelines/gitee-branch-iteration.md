# Gitee 工单 → 分支迭代号

开功能分支且用户给出 **Gitee 工单号 / 需求链接** 时遵守。  
人读完整版：`docs/standards/gitee-branch-iteration.md`  
事实与习惯补充：kb `domains/workflow/company-git-branch.md`

与 [`git-commit-mr.md`](git-commit-mr.md) 分工：本条只管 **迭代号从哪来**；连续 commit 序号与 MR 推送见彼文。

---

## MUST（开分支前）

1. 从链接或正文抽出工单 ident（如 `IKGB7L`；URL 形如 `...?issue=IKGB7L`）。
2. 用 Gitee 企业 MCP / API 拉工单详情：
   - `enterprise_id` = **12478212**（企业 path `bitsun_1`）
   - **不要**把 URL 里的 `projects/753146` 当成 `enterprise_id`（那是 `program_id`）
   - `get_enterprise_issue_detail`（或等价），`issue_id` = ident
3. 读返回的 **`scrum_sprint.title`**，解析迭代数字：
   - 例：`标品迭代23(0921-1007)` → **`23`**
4. 分支名：`feature/<基线>-<迭代号>-<人名>-<工单号>[-简述]`  
   例：`feature/release-tx-23-凌启睿-IKGB7L-指导销售价`
5. 401 / 未授权 → 先授权再重试；仍失败则 **问用户迭代号**，禁止瞎猜。

## MUST NOT

- 从当前本地分支名抄迭代号（如看到 `…-22-…` 就写 22）
- 用「同仓最近 feature 分支最大迭代号」代替工单归属迭代
- 工单未挂 sprint 时自己编一个数（应问用户或查排期）

## 与基线

基线仍按产品线选（铁血 → `origin/release-tx` 等）；本条只约束 sprint/迭代号来源。

## PR 勾选

- [ ] 是否已用 Gitee 工单详情确认 `scrum_sprint`？
- [ ] 分支名中的迭代号是否与 `scrum_sprint.title` 一致？
