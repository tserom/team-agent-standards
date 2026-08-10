# antd InputNumber 录入手感：聚焦全选

> **适用范围**：React + antd 业务页中可编辑的 `InputNumber`（表格明细、表单金额/数量等）。  
> **目标**：减少「先清 `0.00` 再输入」的摩擦，接近表格软件的改数手感。  
> **Agent 短规则真源**：`guidelines/antd-input-number-select-on-focus.md`  
> **版本**：1.0

---

## 1. 背景

antd 默认 `InputNumber` 在值为 `0` 时显示 `0` / `0.00`，聚焦后光标落在末尾。录入场景下用户几乎总是要整段替换，全选再输入更省事。

定稿交互（方案 A）：**聚焦全选**。不默认做「零显示为空」（方案 B/C），以免与存库 `0`、失焦回显纠缠。

---

## 2. 推荐实现

### 内联

```tsx
<InputNumber
  value={unitPrice}
  onFocus={(e) => {
    const el = e.target
    requestAnimationFrame(() => el.select())
  }}
  onChange={...}
/>
```

`requestAnimationFrame`（或等价的下一帧）用于避免 **mousedown → focus → mouseup** 把选区冲掉。

### 项目封装（推荐）

同仓多处使用时抽一层薄封装，例如 `SelectOnFocusInputNumber`，透传 `InputNumberProps`，在内部合并 `onFocus`。销售单范本：`l-project` `apps/sales-front/src/components/SelectOnFocusInputNumber.tsx`。

---

## 3. 边界

| 做 | 不做 |
|----|------|
| 可编辑数量/单价/金额等录入框 | 只读展示、disabled |
| 存库仍用数字 `0` | 默认可变空展示 `null`（需产品确认） |
| 有封装则优先用封装 | 为「灵活性」再加配置开关 |

---

## 4. 校验

1. 新行点进单价 → 不删 `0.00` 直接输入 → 整段覆盖。  
2. 已有真实价格（如 `6.90`）点进 → 全选，再输可覆盖。  
3. Tab 聚焦与鼠标点击均应全选。

---

## 5. 相关

- kb 短文：`kb/domains/personal-react/antd-input-number.md`
- Cursor 规则产物：`antd-input-number-select-on-focus.mdc`
