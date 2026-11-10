# Skill 21 — Compound Interest Curve

**Category C:** Wealth, Trading & Analytics

> An exponential curve that makes the last five years look nothing like the first five.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `21` |
| **Slug** | `skill-21-compound-interest-curve` |
| **Category** | Wealth, Trading & Analytics |
| **Output file** | `output/skill-21-compound-interest-curve.html` |
| **Timeline length** | 18s (18,000 ms) at 1x speed |
| **Accent pair** | `#10B981` primary, `#4F46E5` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #21`
- `Run skill-21-compound-interest-curve`
- `Build the compound interest curve explainer`
- A natural-language request whose intent matches: _Show compounding mechanics: principal, interest earned, the bend in the curve, and the drift between simple and compound growth._

### Objective

Show compounding mechanics: principal, interest earned, the bend in the curve, and the drift between simple and compound growth.

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
| **Scene 1: Principal Planted** | 0.0s - 4.0s | A $10,000 principal enters an empty 30-year chart. |
| **Scene 2: Curve Grows** | 4.0s - 11.0s | The compound curve draws year by year and the bend arrives late. |
| **Scene 3: Simple vs Compound** | 11.0s - 15.5s | A straight simple-interest line appears far below the compound curve. |
| **Scene 4: Final Value** | 15.5s - 18.0s | The 30-year endpoint locks and shows $44,677 versus $25,000. |

### Scene 1 — Principal Planted

**Timing window:** `0.0s - 4.0s`

**Narration subtitle:**

> A $10,000 principal enters an empty 30-year chart.

**On-screen elements:** Axes with year and value labels, an empty plot area, a principal chip.

**Animation physics:** Axes draw from origin outward in 500ms; the seed dot drops onto the y-axis with a 220ms spring.

### Scene 2 — Curve Grows

**Timing window:** `4.0s - 11.0s`

**Narration subtitle:**

> The compound curve draws year by year and the bend arrives late.

**On-screen elements:** Compound curve path, year markers every 5 years, a moving endpoint dot.

**Animation physics:** Path draws via dashoffset mapping to 0 -> 30 years; the endpoint dot rides getPointAtLength; labels fade in as they pass.

### Scene 3 — Simple vs Compound

**Timing window:** `11.0s - 15.5s`

**Narration subtitle:**

> A straight simple-interest line appears far below the compound curve.

**On-screen elements:** Second straight path, a shaded gap area between the two curves.

**Animation physics:** Straight line draws in 700ms; the gap area fades in from 0.0 to 0.16 opacity over 500ms.

### Scene 4 — Final Value

**Timing window:** `15.5s - 18.0s`

**Narration subtitle:**

> The 30-year endpoint locks and shows $44,677 versus $25,000.

**On-screen elements:** Endpoint callout with compound and simple totals side by side.

**Animation physics:** Counters tween to their final values on a 600ms ease-out; callout connector draws last; hold the frame.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Axes** | Chart frame | Two 1.5px lines with tick marks every 5 years and mono tick labels |
| **Compound curve** | Exponential growth | Sampled cubic polyline of 61 points generated from the formula, not hand-drawn |
| **Simple line** | Linear baseline | Straight 2-point line in muted slate at 45% opacity |
| **Gap area** | Value of compounding | Closed path between the two series with a gradient fill at 16% opacity |
| **Endpoint callout** | Result | Card with connector rule pointing to the terminal dot |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- Compute both series from the real formula (principal * (1 + r)^t) so the curve cannot contradict the labels.
- Y-axis must use a compressed scale; a linear axis makes early years unreadable on small screens.
- Curve drawing uses stroke-dasharray equal to pathLength with a matching dashoffset.
- Do not animate the curve beyond 11 seconds; the last 7 seconds are for interpretation, not motion.

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
  'A $10,000 principal enters an empty 30-year chart.',
  'The compound curve draws year by year and the bend arrives late.',
  'A straight simple-interest line appears far below the compound curve.',
  'The 30-year endpoint locks and shows $44,677 versus $25,000.'
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
const COMPOUND = { principal: 10000, annualRate: 0.05, years: 30, compoundedPerYear: 12, finalCompound: 44677.44, finalSimple: 25000.00, ruleOf72Years: 14.4 };
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

Scale the chart to the actual computed final value at load. Hard-coded axis maxima drift from the math and break credibility.

---

**Previous:** [Treasury Yield Sweep](skill-20-treasury-yield-flow.md) | **Next:** [Portfolio Rebalance](skill-22-portfolio-rebalance.md) | **Index:** [README](../README.md)
