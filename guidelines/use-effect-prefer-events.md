# `useEffect`：能不用就不用

实现或修改 React 页面/组件时**默认遵守**（不限列表页）。与 [react-readability.md](react-readability.md) §2（禁止 effect 串联业务）互补：本条管「要不要写 effect、写之前先问」。

## 优先级

| 优先级 | 做法 |
|--------|------|
| **1** | 能在事件、显式调度、派生渲染、`key` 重置里完成 → **不要** `useEffect` |
| **2** | 确认不用就做不到 → **先提示用户/开发者**（理由、依赖、副作用与请求风险）→ 确认后再写 |
| **3** | 获准后：effect **极薄**（挂载就绪、订阅、cleanup）；业务进具名函数，不在 effect 里堆分支 |

口令：**能不用就不用；要用先说一声，并且里面少写逻辑。**

## MUST NOT（未获准时）

- 用 `useEffect` 跟路由 key / Tab `activeKey` / 查询 seed 隐式串「回填 + 请求」
- 在 effect 里堆业务分支、拼 params、连续多次 `setState` + 请求

## 双视图列表

公司仓 Tabs 列表/明细：优先 `onChange` + `scheduleApply`（见 kb `tab-query-sync.md`、guideline `document-list-page-simple.md`）。若必须用 effect 等实例就绪：走上方优先级 2～3。

## 自检

- [ ] 能否改成事件 / 显式调度 / `key` 重置？
- [ ] 新增 effect 是否已说明理由并经确认？
- [ ] effect 体内是否只调具名函数 + cleanup？
