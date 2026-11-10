# Skill 22 — Portfolio Rebalance

**Category C:** Wealth, Trading & Analytics

> A donut that quietly repairs itself back to target weights.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `22` |
| **Slug** | `skill-22-portfolio-rebalance` |
| **Category** | Wealth, Trading & Analytics |
| **Output file** | `output/skill-22-portfolio-rebalance.html` |
| **Timeline length** | 17s (17,000 ms) at 1x speed |
| **Accent pair** | `#4F46E5` primary, `#10B981` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #22`
- `Run skill-22-portfolio-rebalance`
- `Build the portfolio rebalance explainer`
- A natural-language request whose intent matches: _Explain drift and rebalancing: how allocation drifts with market moves, how target bands trigger a rebalance, and the resulting trades._

### Objective

Explain drift and rebalancing: how allocation drifts with market moves, how target bands trigger a rebalance, and the resulting trades.

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
| **Scene 1: Target Allocation** | 0.0s - 3.5s | The target donut settles at 60/25/15 across equities, bonds and cash. |
| **Scene 2: Drift** | 3.5s - 8.5s | Equities rally and the weights drift to 68/20/12. |
| **Scene 3: Rebalance Trades** | 8.5s - 13.5s | Two trades fire: sell equities, buy bonds and cash. |
| **Scene 4: Restored** | 13.5s - 17.0s | The donut returns to target and the status clears. |

### Scene 1 — Target Allocation

**Timing window:** `0.0s - 3.5s`

**Narration subtitle:**

> The target donut settles at 60/25/15 across equities, bonds and cash.

**On-screen elements:** Three-segment donut, legend rows with target percentages, total value in the center.

**Animation physics:** Segments sweep from 0 to their target angles over 900ms with a 60ms stagger.

### Scene 2 — Drift

**Timing window:** `3.5s - 8.5s`

**Narration subtitle:**

> Equities rally and the weights drift to 68/20/12.

**On-screen elements:** Same donut with segments morphing; drift arrows and a drift badge reading +8.0%.

**Animation physics:** Arc angles interpolate on a 1.2s ease; the drift badge counts up and turns amber past the 5% band.

### Scene 3 — Rebalance Trades

**Timing window:** `8.5s - 13.5s`

**Narration subtitle:**

> Two trades fire: sell equities, buy bonds and cash.

**On-screen elements:** Trade tickets with SELL 8% and BUY 5% / 3%, a trade cost line at 0.04%.

**Animation physics:** Tickets slide in from the donut at 120ms offsets along radial directions.

### Scene 4 — Restored

**Timing window:** `13.5s - 17.0s`

**Narration subtitle:**

> The donut returns to target and the status clears.

**On-screen elements:** Donut at 60/25/15, emerald restored chip, next review date.

**Animation physics:** Arcs interpolate back over 800ms; badge fades out; the center total is unchanged throughout to prove no value was created.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Donut segments** | Allocation | Three arcs on r=120 with a 34px stroke and rounded caps at the boundaries |
| **Legend rows** | Weights | Three rows with a colour swatch, label, and mono percentage |
| **Drift badge** | Deviation | Pill showing signed percentage, amber above threshold, slate within band |
| **Trade tickets** | Execution | Compact cards with side, asset and weight delta |
| **Center total** | Portfolio value | Mono 36px value with a smaller label |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- Segment angles must be derived from weights at every frame; never animate stroke-dasharray with hard-coded numbers.
- The center total must not change during rebalancing. Value conservation is the proof of correctness.
- The drift threshold band is 5%; show it numerically so the alert is explainable.
- Rebalance motion is deliberately calmer than the drift motion; correction should feel reassuring.

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
  'The target donut settles at 60/25/15 across equities, bonds and cash.',
  'Equities rally and the weights drift to 68/20/12.',
  'Two trades fire: sell equities, buy bonds and cash.',
  'The donut returns to target and the status clears.'
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
const REBALANCE = { total: 128_400, target: { equities: 0.60, bonds: 0.25, cash: 0.15 }, drifted: { equities: 0.68, bonds: 0.20, cash: 0.12 }, band: 0.05, tradeCostBps: 4, nextReview: 'Quarterly' };
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

Round displayed percentages to one decimal and make the three values sum to 100.0 exactly after rounding.

---

**Previous:** [Compound Interest Curve](skill-21-compound-interest-curve.md) | **Next:** [Candlestick Formation](skill-23-candlestick-formation.md) | **Index:** [README](../README.md)
