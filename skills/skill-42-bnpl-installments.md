# Skill 42 — BNPL Installments

**Category E:** B2B SaaS, Lending & Credit

> One purchase split into four payments across six weeks, with zero interest.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `42` |
| **Slug** | `skill-42-bnpl-installments` |
| **Category** | B2B SaaS, Lending & Credit |
| **Output file** | `output/skill-42-bnpl-installments.html` |
| **Timeline length** | 16s (16,000 ms) at 1x speed |
| **Accent pair** | `#4F46E5` primary, `#10B981` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #42`
- `Run skill-42-bnpl-installments`
- `Build the bnpl installments explainer`
- A natural-language request whose intent matches: _Explain buy-now-pay-later mechanics: point-of-sale split, installment schedule, merchant discount fee, and late-fee policy._

### Objective

Explain buy-now-pay-later mechanics: point-of-sale split, installment schedule, merchant discount fee, and late-fee policy.

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
| **Scene 1: Checkout Split** | 0.0s - 4.0s | A $240 cart offers four payments of $60 at checkout. |
| **Scene 2: Installment Schedule** | 4.0s - 9.0s | Four payment nodes land across a six-week timeline. |
| **Scene 3: Merchant Fee** | 9.0s - 13.0s | The merchant pays a 4.9% discount fee and receives $228.24 today. |
| **Scene 4: Repaid** | 13.5s - 16.0s | Three payments clear and the fourth completes the schedule. |

### Scene 1 — Checkout Split

**Timing window:** `0.0s - 4.0s`

**Narration subtitle:**

> A $240 cart offers four payments of $60 at checkout.

**On-screen elements:** Checkout panel, payment options list, a highlighted 4-payment row.

**Animation physics:** The BNPL row highlights with a 1.03 scale and a 2px indigo outline; the schedule preview fades in beneath.

### Scene 2 — Installment Schedule

**Timing window:** `4.0s - 9.0s`

**Narration subtitle:**

> Four payment nodes land across a six-week timeline.

**On-screen elements:** Horizontal timeline with 4 nodes at day 0, 14, 28, 42, each with amount $60.00.

**Animation physics:** Nodes pop in chronological order at 140ms; the connecting timeline draws ahead of each node at 90% of its travel.

### Scene 3 — Merchant Fee

**Timing window:** `9.0s - 13.0s`

**Narration subtitle:**

> The merchant pays a 4.9% discount fee and receives $228.24 today.

**On-screen elements:** Two-row settlement: customer pays 4x60, merchant receives 228.24 now, fee chip 11.76.

**Animation physics:** The fee chip lifts out of the total with an 8px rise and a rose tint; the merchant net figure counts in last.

### Scene 4 — Repaid

**Timing window:** `13.5s - 16.0s`

**Narration subtitle:**

> Three payments clear and the fourth completes the schedule.

**On-screen elements:** Three settled nodes, a final PAID state, zero-interest badge throughout.

**Animation physics:** Each node ticks to settled at 200ms intervals; the zero-interest badge stays constant to reinforce the claim.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Timeline** | Installment cadence | Horizontal rail 640px wide with 4 nodes and day labels |
| **Payment nodes** | Installments | 36px circles with a mono amount beneath and a status ring |
| **Cart panel** | Purchase | 340x200 with line items and a total in mono 32px |
| **Fee chip** | Merchant cost | Rose pill with a signed percentage and an absolute figure |
| **Zero-interest badge** | Customer term | Emerald outline pill with a 0% glyph |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- The four payments must sum exactly to the purchase total.
- Merchant net plus fee must equal the purchase total, in the same currency.
- Nodes settle only in chronological order; jumping ahead breaks the repayment narrative.
- The zero-interest badge never animates or flashes. It is a constant, and constancy reads as reliability.

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
  'A $240 cart offers four payments of $60 at checkout.',
  'Four payment nodes land across a six-week timeline.',
  'The merchant pays a 4.9% discount fee and receives $228.24 today.',
  'Three payments clear and the fourth completes the schedule.'
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
const BNPL = { cart: 240.00, currency: 'USD', installments: 4, perPayment: 60.00, apr: 0, merchantFeePct: 0.049, merchantFee: 11.76, merchantNet: 228.24, scheduleDays: [0, 14, 28, 42], lateFee: 7.00 };
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

Show the merchant fee. BNPL demos that hide the merchant discount look like consumer advertising rather than explanation.

---

**Previous:** [Credit Score Gauge](skill-41-credit-score-gauge.md) | **Next:** [Invoice Factoring](skill-43-invoice-factoring.md) | **Index:** [README](../README.md)
