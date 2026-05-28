# API Layering Decision · One-Pager (v1.0)

> Full spec: `api-abstraction-encapsulation-reuse.md` · For `*Api.ts` / `services` in any project

---

## 30-second model

| | What | How |
|---|------|-----|
| **Reuse** | Math, parse list, build params | **L0** — no HTTP |
| **Encapsulate** | One URL | **L1** — required baseline |
| **Encapsulate** | One user action | **L3** — one export + step comments |
| **Abstract** | Multi-step flow | **L2** — rare; **identical side effects only** |

**Rule of thumb**: wrap every URL; one function per action; no universal `sync`.

---

## Layers

```
L3  Action entry     submitOrder / changeBatchCode   ← one product sentence = one function
L2  Orchestration    syncAandB (use sparingly)      ← extract only if ≥3 entries, same steps + effects
L1  Single URL       postAdjustBatch                ← one function per endpoint (required)
L0  Utilities        normalizeList / calcTotal      ← reuse freely
```

---

## New feature: 5 questions (stop at first match)

| # | Question | Yes → |
|---|----------|-------|
| 1 | Params / parsing / math only? | **L0** |
| 2 | Exactly **one** HTTP call? | **L1** |
| 3 | New user-visible action? | **New L3** (do not extend old `sync*`) |
| 4 | Already ≥3 L3s with **same steps and side effects**? | Consider **L2** |
| 5 | This path needs **extra or fewer** URLs vs others? | **Do not** extend L2 → **new L3** |

**Orchestration check**: does the **main aggregate quantity** change? need **compensation APIs** (saveOrUpdate / rebalance)?  
→ unchanged and no compensation → **no** generic `sync` / **no** default rebalance.

---

## MUST / MUST NOT

| ✅ MUST | ❌ MUST NOT |
|---------|-------------|
| All HTTP in `*Api.ts` | UI/columns chaining adjust + PATCH |
| One L3 per action + step comments | Third boolean flag on L2 for one scenario |
| Action index (action → fn → URLs) | `request` inside L0 |
| New L2 documents URLs **called / not called** | “Any sub-table change goes through one sync” |

---

## Split signals (any one)

- Callers need a long comment to pass `options`  
- New scenario → `if (purpose === …)` in L2  
- Network tab shows URLs **not in PRD**  
- Docs say “except for scenario A…”  
- Different refresh/rollback, same function  

---

## PR checklist (4 items)

- [ ] L0/1/3? passed 5-question table?  
- [ ] L2 changed? side-effect table updated?  
- [ ] Options only for one scenario → separate L3?  
- [ ] call-map / file header index updated?  

---

*Paste into Lark/Notion or print A4 single-sided.*
