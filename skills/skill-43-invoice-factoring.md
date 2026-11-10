# Skill 43 — Invoice Factoring

**Category E:** B2B SaaS, Lending & Credit

> A 90-day invoice converting into 85% working capital today.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `43` |
| **Slug** | `skill-43-invoice-factoring` |
| **Category** | B2B SaaS, Lending & Credit |
| **Output file** | `output/skill-43-invoice-factoring.html` |
| **Timeline length** | 17s (17,000 ms) at 1x speed |
| **Accent pair** | `#4F46E5` primary, `#10B981` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #43`
- `Run skill-43-invoice-factoring`
- `Build the invoice factoring explainer`
- A natural-language request whose intent matches: _Explain factoring and invoice financing: receivables aging, advance rate, discount fee, and settlement when the customer pays._

### Objective

Explain factoring and invoice financing: receivables aging, advance rate, discount fee, and settlement when the customer pays.

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
| **Scene 1: Invoice Aging** | 0.0s - 4.0s | A $120,000 invoice sits at net-90 with an aging bar in amber. |
| **Scene 2: Advance Rate** | 4.0s - 9.0s | The funder advances 85% immediately and holds 15% in reserve. |
| **Scene 3: Discount Fee** | 9.0s - 13.0s | A 2.5% fee is disclosed against the reserve. |
| **Scene 4: Settled on Day 90** | 13.5s - 17.0s | The customer pays, the reserve releases and the books close. |

### Scene 1 — Invoice Aging

**Timing window:** `0.0s - 4.0s`

**Narration subtitle:**

> A $120,000 invoice sits at net-90 with an aging bar in amber.

**On-screen elements:** Invoice card with terms NET 90, an aging bar, a cash gap indicator.

**Animation physics:** The aging bar fills over 1.2s across the 90-day span; the cash gap indicator pulses amber twice.

### Scene 2 — Advance Rate

**Timing window:** `4.0s - 9.0s`

**Narration subtitle:**

> The funder advances 85% immediately and holds 15% in reserve.

**On-screen elements:** Advance figure $102,000, reserve $18,000, a split bar with 85/15 segments.

**Animation physics:** The split bar divides at 85% with a 240ms spring; both figures count in parallel on the same progress value.

### Scene 3 — Discount Fee

**Timing window:** `9.0s - 13.0s`

**Narration subtitle:**

> A 2.5% fee is disclosed against the reserve.

**On-screen elements:** Fee chip $3,000, effective annualized cost note, a net settlement preview.

**Animation physics:** The fee chip slides out of the reserve segment; the annualized note fades in with a smaller type step.

### Scene 4 — Settled on Day 90

**Timing window:** `13.5s - 17.0s`

**Narration subtitle:**

> The customer pays, the reserve releases and the books close.

**On-screen elements:** Day-90 marker, reserve release arrow, net cash $117,000, a reconciled badge.

**Animation physics:** The day-90 marker travels the aging bar; the reserve arrow reverses the earlier path; reconciled badge lands last.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Invoice card** | Receivable | 360x180 with invoice number, customer, amount and terms |
| **Aging bar** | Time to payment | Horizontal bar with 30/60/90 ticks and an amber fill |
| **Split bar** | Advance vs reserve | Single bar with an 85/15 cut and a divider tick |
| **Reserve release** | Deferred cash | Curved arrow from reserve to operating balance |
| **Reconciled badge** | Closure | Emerald badge with a check glyph and a settlement date |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- Advance plus reserve must equal the invoice total exactly.
- The fee is drawn from the reserve, not from the invoice, and the visual must show that path.
- The annualized cost of 2.5% over 90 days is roughly 10% APR; show it so the comparison is honest.
- The reserve release uses a mirrored path to the advance so the round trip is legible.

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
  'A $120,000 invoice sits at net-90 with an aging bar in amber.',
  'The funder advances 85% immediately and holds 15% in reserve.',
  'A 2.5% fee is disclosed against the reserve.',
  'The customer pays, the reserve releases and the books close.'
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
const FACTORING = { invoice: 120_000, customer: 'Meridian Retail', termsDays: 90, advanceRate: 0.85, advance: 102_000, reserve: 18_000, feePct: 0.025, fee: 3_000, netSettled: 117_000, effectiveApr: 0.101 };
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

Annualize the fee on screen. A 2.5% fee over 90 days is roughly a 10% annual cost, and hiding that is the deceptive pattern.

---

**Previous:** [BNPL Installments](skill-42-bnpl-installments.md) | **Next:** [Payroll Distribution](skill-44-payroll-distribution.md) | **Index:** [README](../README.md)
