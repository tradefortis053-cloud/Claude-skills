# Skill 49 — Usage-Based Billing

**Category E:** B2B SaaS, Lending & Credit

> An API meter ticking up and sliding between pricing tiers in real time.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `49` |
| **Slug** | `skill-49-usage-based-billing` |
| **Category** | B2B SaaS, Lending & Credit |
| **Output file** | `output/skill-49-usage-based-billing.html` |
| **Timeline length** | 16s (16,000 ms) at 1x speed |
| **Accent pair** | `#4F46E5` primary, `#06B6D4` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #49`
- `Run skill-49-usage-based-billing`
- `Build the usage-based billing explainer`
- A natural-language request whose intent matches: _Explain metered billing: usage counters, tiered pricing blocks, graduated rate application, and the projected invoice._

### Objective

Explain metered billing: usage counters, tiered pricing blocks, graduated rate application, and the projected invoice.

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
| **Scene 1: Usage Meter** | 0.0s - 3.5s | The meter starts at 0 and ticks up as API calls arrive. |
| **Scene 2: Tier Ladder** | 3.5s - 8.5s | The usage crosses 100k and enters the second pricing block. |
| **Scene 3: Graduated Pricing** | 8.5s - 13.0s | The invoice breaks into per-tier line items rather than one blended rate. |
| **Scene 4: Projected Invoice** | 13.0s - 16.0s | The month projects to $2,650.00 with the overage clearly separated. |

### Scene 1 — Usage Meter

**Timing window:** `0.0s - 3.5s`

**Narration subtitle:**

> The meter starts at 0 and ticks up as API calls arrive.

**On-screen elements:** Circular usage meter, live call counter, a mono rate of calls per second.

**Animation physics:** The counter increments in bursts of 3 to 5 with a 60ms cadence; the meter arc fills proportionally.

### Scene 2 — Tier Ladder

**Timing window:** `3.5s - 8.5s`

**Narration subtitle:**

> The usage crosses 100k and enters the second pricing block.

**On-screen elements:** Four tier bands with unit prices, a marker crossing tier boundaries.

**Animation physics:** The marker slides along the ladder; on each boundary crossing the band under it brightens for 200ms and the effective rate updates.

### Scene 3 — Graduated Pricing

**Timing window:** `8.5s - 13.0s`

**Narration subtitle:**

> The invoice breaks into per-tier line items rather than one blended rate.

**On-screen elements:** Four line items with usage per tier, unit price and subtotal, a blended effective rate.

**Animation physics:** Each line item grows in as its threshold is passed; the blended rate recomputes and re-renders each frame.

### Scene 4 — Projected Invoice

**Timing window:** `13.0s - 16.0s`

**Narration subtitle:**

> The month projects to $2,650.00 with the overage clearly separated.

**On-screen elements:** Invoice summary, base commit $2,000, overage $650, projected total, a note on volume discount eligibility.

**Animation physics:** The summary sheet slides up 24px on a spring; totals count in; the discount hint fades in last.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Usage meter** | Consumption | Circle r=110 with a 10px stroke, dasharray mapped to the tier cap |
| **Tier ladder** | Pricing blocks | Four horizontal bands with boundary ticks and mono unit prices |
| **Line items** | Invoice composition | Four rows with usage, unit price, and right-aligned subtotal |
| **Projection sheet** | Invoice | Card with a base commit row, overage row and total rule |
| **Rate ticker** | Live throughput | Mono counter with a small sparkline of the last 60 samples |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- Graduated pricing means each tier's rate applies only within that tier; never multiply total usage by the top rate.
- The invoice total must equal the sum of rendered line items, computed not hard-coded.
- Tier boundary crossers pulse once and settle; repeated flashing makes the ladder feel unstable.
- Use 4-decimal unit prices to keep small tiers visually meaningful.

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
  'The meter starts at 0 and ticks up as API calls arrive.',
  'The usage crosses 100k and enters the second pricing block.',
  'The invoice breaks into per-tier line items rather than one blended rate.',
  'The month projects to $2,650.00 with the overage clearly separated.'
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
const USAGE = { calls: 1_200_000, tiers: [{ upTo: 100_000, rate: 0.005 }, { upTo: 500_000, rate: 0.003 }, { upTo: 1_000_000, rate: 0.0015 }, { upTo: null, rate: 0.001 }], baseCommit: 2_000, overage: 650, projected: 2_650, effectiveRate: 0.0022 };
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

Graduated and volume pricing are different models. Label which one is being shown, or the invoice math will be challenged.

---

**Previous:** [SaaS MRR Waterfall](skill-48-saas-mrr-waterfall.md) | **Next:** [Customs and Trade Finance](skill-50-customs-trade-finance.md) | **Index:** [README](../README.md)
