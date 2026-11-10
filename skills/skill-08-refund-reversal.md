# Skill 08 — Refund Reversal

**Category A:** Payment Flows & Transactions

> A transaction that runs backward, then settles forward again as credit.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `08` |
| **Slug** | `skill-08-refund-reversal` |
| **Category** | Payment Flows & Transactions |
| **Output file** | `output/skill-08-refund-reversal.html` |
| **Timeline length** | 15s (15,000 ms) at 1x speed |
| **Accent pair** | `#F43F5E` primary, `#10B981` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #08`
- `Run skill-08-refund-reversal`
- `Build the refund reversal explainer`
- A natural-language request whose intent matches: _Show a refund as a reversal of the original authorization: ledger entries flipping sign, the path rewinding, and the customer balance restoring._

### Objective

Show a refund as a reversal of the original authorization: ledger entries flipping sign, the path rewinding, and the customer balance restoring.

### Deliverable Requirements

- One self-contained `.html` file. No build step, no bundler, no local asset paths.
- TailwindCSS via CDN **plus** inline CSS fallbacks so the layout survives a blocked CDN.
- Inline SVG only. No external images, icon fonts or sprite sheets.
- Full `TimelineEngine` control bar: Play / Pause / Replay, scrubber, step indicator, live captions, speed toggle (`1x`, `1.5x`, `2x`), theme toggle.
- Deterministic rendering: the visual state must be a pure function of `progress` in `[0, 1]`.
- Responsive down to 390px wide; the scene must scale rather than clip.

---

## 2. Scene-by-Scene Storyboard

Scene boundaries are expressed as normalized timeline fractions so the engine can seek to any frame without drift.

| Scene | Window | Caption |
| --- | --- | --- |
| **Scene 1: Original Charge** | 0.0s - 3.5s | The capture path completes and the ledger shows a debit of $89.00. |
| **Scene 2: Reversal Triggered** | 3.5s - 7.5s | The merchant issues a refund and the timeline rewinds visibly. |
| **Scene 3: Rail Return** | 7.5s - 11.5s | Funds travel back along the issuing rail to the original card. |
| **Scene 4: Balance Restored** | 11.5s - 15.0s | The cardholder balance returns to its pre-purchase value and the ledger reconciles. |

### Scene 1 — Original Charge

**Timing window:** `0.0s - 3.5s`

**Narration subtitle:**

> The capture path completes and the ledger shows a debit of $89.00.

**On-screen elements:** Horizontal ledger with a signed amount, status chip CAPTURED, forward arrow path.

**Animation physics:** Path draws left to right; the debit row enters with a 16px X translate and settles on a spring.

### Scene 2 — Reversal Triggered

**Timing window:** `3.5s - 7.5s`

**Narration subtitle:**

> The merchant issues a refund and the timeline rewinds visibly.

**On-screen elements:** The same path redrawn right to left, amount sign flipping from -89.00 to +89.00.

**Animation physics:** Dashoffset animates in reverse; the amount text crosses through with a 180ms scaleX flip before showing the plus sign.

### Scene 3 — Rail Return

**Timing window:** `7.5s - 11.5s`

**Narration subtitle:**

> Funds travel back along the issuing rail to the original card.

**On-screen elements:** Reversed packet on the mirrored arc, three intermediary nodes lighting in reverse order.

**Animation physics:** Packet uses getPointAtLength on the same path with inverted progress; nodes light at 75%, 45%, 15%.

### Scene 4 — Balance Restored

**Timing window:** `11.5s - 15.0s`

**Narration subtitle:**

> The cardholder balance returns to its pre-purchase value and the ledger reconciles.

**On-screen elements:** Balance counter, ledger rows marked REFUNDED, reconciliation checkmark.

**Animation physics:** Counter counts upward from the debited value; both ledger rows emit a single emerald underline sweep.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Ledger rows** | Accounting truth | Two stacked rows with mono debit/credit columns and status chips |
| **Reversal path** | Refund routing | Single polyline reused for both directions, 3px stroke |
| **Card face** | Destination instrument | Rounded rect with masked PAN and a subtle metallic gradient |
| **Reconciliation check** | Closure state | Checkmark path plus a 560x2 underline gradient sweep |
| **Sign flip glyph** | Direction change | Text node with transform-origin center and scaleX animated through zero |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- Reversal must reuse the exact same path geometry as the original charge to read as a true rewind.
- The sign flip passes through scaleX 0 at the midpoint and never displays both signs at once.
- Rose is used for the original debit, emerald for the returned credit; avoid mixing them on one element.
- The end state is a quiet one: after reconciliation, hold still for the final 800ms rather than looping.

### Shared Timing Constants

```js
const EASE = {
  decel:  'cubic-bezier(0.16, 1, 0.3, 1)',   // Apple-style entry
  inout:  'cubic-bezier(0.65, 0, 0.35, 1)',  // symmetric transitions
  spring: { stiffness: 220, damping: 24 },   // damped settle
  // linear is reserved for ambient rotation and real-time countdowns only
};

const clamp01 = (n) => Math.min(1, Math.max(0, n));
const lerp = (a, b, t) => a + (b - a) * t;
const band = (p, start, end) => clamp01((p - start) / (end - start));
const easeOut = (t) => 1 - Math.pow(1 - t, 3);
const easeInOut = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
const springOut = (t) => 1 - Math.exp(-6 * t) * Math.cos(9 * t);
```

Use `band(progress, start, end)` for every sub-animation. It is the reason scrubbing backward works.

---

## 5. Narration Subtitle Track

These strings are the canonical captions. They render in the control bar and must not be paraphrased by the generator.

```js
const CAPTIONS = [
  'The capture path completes and the ledger shows a debit of $89.00.',
  'The merchant issues a refund and the timeline rewinds visibly.',
  'Funds travel back along the issuing rail to the original card.',
  'The cardholder balance returns to its pre-purchase value and the ledger reconciles.'
];
```

### Caption Styling

- Font: Inter or Plus Jakarta Sans, 14 px at 500 weight, 1.5 line height.
- Constrain to 2 lines maximum on desktop and 3 lines on mobile by shortening the scene copy, never by shrinking type below 13 px.
- Colour: muted slate (`#64748B`) in light mode, `#94A3B8` in dark mode. Captions are secondary to the scene, never competing.
- Reserve a fixed caption block height so scene changes never shift the control bar.

---

## 6. Reference Data Model

Bind every number on screen to this object. Do not hard-code figures inside render functions.

```js
const REFUND = { orderId: 'ORD-7719', merchant: 'Fern Supply', amount: 89.00, currency: 'USD', originalAuth: 'CAPTURED', refundStatus: 'REFUNDED', railDays: '3-5 business', reason: 'Item not received' };
```

### Data Rules

- All currency displays use `Intl.NumberFormat` with the correct locale and two decimals (or the correct precision for the asset).
- Counters use `font-variant-numeric: tabular-nums` so digits do not shift width mid-count.
- Any derived figure (totals, percentages, deltas) is computed from this object at load and asserted in a dev-only check.

---

## 7. Acceptance Checklist

- [ ] Scrubbing from 100% back to 0% leaves every element in its exact initial state.
- [ ] Pausing freezes all motion, including ambient loops and countdowns.
- [ ] Changing speed to `1.5x` or `2x` does not desynchronize any sub-animation.
- [ ] Both light and dark themes pass a 4.5:1 contrast check on body text.
- [ ] Every number on screen traces back to the `Reference Data Model`.
- [ ] The final frame holds for at least 800 ms and is a complete, readable statement.
- [ ] No `linear` easing except for real-time countdowns and ambient rotation.
- [ ] No external network requests beyond the TailwindCSS CDN.
- [ ] Renders correctly at 390 px, 768 px, 1280 px and 1920 px widths.
- [ ] `prefers-reduced-motion: reduce` collapses scene transitions to fades and disables ambient loops.

---

### Skill Notes

Reversal animations are the clearest test of a progress-driven engine. If scrubbing backward looks broken, this skill will expose it.

---

**Previous:** [Subscription Recurring Billing](skill-07-subscription-recurring.md) | **Next:** [NFC Contactless Tap](skill-09-nfc-contactless.md) | **Index:** [README](../README.md)
