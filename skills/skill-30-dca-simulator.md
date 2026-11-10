# Skill 30 — Dollar-Cost Averaging

**Category C:** Wealth, Trading & Analytics

> Twelve buy markers smoothing a violent market wave into a calm average.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `30` |
| **Slug** | `skill-30-dca-simulator` |
| **Category** | Wealth, Trading & Analytics |
| **Output file** | `output/skill-30-dca-simulator.html` |
| **Timeline length** | 18s (18,000 ms) at 1x speed |
| **Accent pair** | `#4F46E5` primary, `#10B981` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #30`
- `Run skill-30-dca-simulator`
- `Build the dollar-cost averaging explainer`
- A natural-language request whose intent matches: _Contrast lump-sum and DCA entry under volatility: fixed periodic buys, average cost basis, and the smoothed entry line._

### Objective

Contrast lump-sum and DCA entry under volatility: fixed periodic buys, average cost basis, and the smoothed entry line.

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
| **Scene 1: Volatile Market** | 0.0s - 4.5s | A jagged 12-month price line draws across the chart. |
| **Scene 2: Lump Sum Entry** | 4.5s - 8.5s | A single $12,000 buy lands at an unlucky local high. |
| **Scene 3: Monthly Buys** | 8.5s - 14.5s | Twelve $1,000 buys distribute across the year. |
| **Scene 4: Average Wins** | 14.5s - 18.0s | The DCA cost basis sits below the lump-sum basis and shows a better return. |

### Scene 1 — Volatile Market

**Timing window:** `0.0s - 4.5s`

**Narration subtitle:**

> A jagged 12-month price line draws across the chart.

**On-screen elements:** Price polyline with 48 seeded points, y-axis in dollars, month labels.

**Animation physics:** Line draws over 1.8s with a 240ms ambient flicker on the endpoint dot; volatility is visible but never frantic.

### Scene 2 — Lump Sum Entry

**Timing window:** `4.5s - 8.5s`

**Narration subtitle:**

> A single $12,000 buy lands at an unlucky local high.

**On-screen elements:** One large buy marker at the peak, an entry price callout, a rose cost-basis line.

**Animation physics:** Marker drops 120px on an ease-in and bounces 4px; the cost-basis line draws horizontally and stays rose.

### Scene 3 — Monthly Buys

**Timing window:** `8.5s - 14.5s`

**Narration subtitle:**

> Twelve $1,000 buys distribute across the year.

**On-screen elements:** Twelve small markers at month intervals, each with a quantity label.

**Animation physics:** Markers appear at 140ms intervals in month order; a running average line lags behind them smoothly.

### Scene 4 — Average Wins

**Timing window:** `14.5s - 18.0s`

**Narration subtitle:**

> The DCA cost basis sits below the lump-sum basis and shows a better return.

**On-screen elements:** Two cost-basis lines converging onto the final price, a comparison callout.

**Animation physics:** Comparison callout draws a connector between the two lines; final figures count in; hold for 900ms.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Price line** | Market path | 48-point polyline from a seeded random walk with 1.8px stroke |
| **Buy markers** | Entry points | Filled circles 10px with a 24px halo for the lump sum and 16px for DCA |
| **Cost-basis lines** | Average entry | Dashed horizontal lines, rose for lump sum and indigo for DCA |
| **Month axis** | Time scale | 12 tick labels with 1px guides at 20% opacity |
| **Comparison callout** | Outcome | Card with two rows, percentages and a delta chip |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- DCA average is recomputed cumulatively after each buy; never interpolate an average from the final value.
- The lump-sum peak is chosen from the actual seeded series, not placed arbitrarily.
- Markers appear in strict chronological order and never overlap month guides.
- Use the same y-scale for both strategies so the comparison is fair.

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
  'A jagged 12-month price line draws across the chart.',
  'A single $12,000 buy lands at an unlucky local high.',
  'Twelve $1,000 buys distribute across the year.',
  'The DCA cost basis sits below the lump-sum basis and shows a better return.'
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
const DCA = { budget: 12_000, months: 12, monthly: 1_000, lumpSumEntry: 141.80, dcaAverage: 128.34, finalPrice: 136.20, lumpSumReturn: -0.0395, dcaReturn: 0.0612, asset: 'VOO' };
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

Show the losing case for DCA at least once in a variant. Skills that always prove the author's point read as marketing, not explanation.

---

**Previous:** [Net Worth Aggregator](skill-29-net-worth-aggregator.md) | **Next:** [Biometric KYC](skill-31-biometric-kyc.md) | **Index:** [README](../README.md)
