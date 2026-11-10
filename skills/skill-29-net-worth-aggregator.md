# Skill 29 — Net Worth Aggregator

**Category C:** Wealth, Trading & Analytics

> Every account on one screen, liabilities subtracting instead of hiding.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `29` |
| **Slug** | `skill-29-net-worth-aggregator` |
| **Category** | Wealth, Trading & Analytics |
| **Output file** | `output/skill-29-net-worth-aggregator.html` |
| **Timeline length** | 16s (16,000 ms) at 1x speed |
| **Accent pair** | `#10B981` primary, `#F43F5E` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #29`
- `Run skill-29-net-worth-aggregator`
- `Build the net worth aggregator explainer`
- A natural-language request whose intent matches: _Show net worth computation: linking accounts, summing assets, subtracting liabilities, and tracking the month-over-month delta._

### Objective

Show net worth computation: linking accounts, summing assets, subtracting liabilities, and tracking the month-over-month delta.

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
| **Scene 1: Link Accounts** | 0.0s - 4.0s | Four accounts connect with a verified badge each. |
| **Scene 2: Assets Rise** | 4.0s - 8.0s | Checking, brokerage, retirement and property sum into total assets. |
| **Scene 3: Liabilities Subtract** | 8.0s - 12.5s | Credit card and mortgage appear in rose and subtract from the total. |
| **Scene 4: One Number** | 12.5s - 16.0s | The net worth figure locks in with a 3.2% month-over-month delta. |

### Scene 1 — Link Accounts

**Timing window:** `0.0s - 4.0s`

**Narration subtitle:**

> Four accounts connect with a verified badge each.

**On-screen elements:** Four institution cards with logo glyphs, connection status, loading shimmer.

**Animation physics:** Shimmer sweeps left to right twice; each card flips to a verified state with a 180ms crossfade.

### Scene 2 — Assets Rise

**Timing window:** `4.0s - 8.0s`

**Narration subtitle:**

> Checking, brokerage, retirement and property sum into total assets.

**On-screen elements:** Asset stack with individual values, a running subtotal, emerald accent rules.

**Animation physics:** Values count in on a 500ms ease-out with 100ms stagger; the subtotal resolves last.

### Scene 3 — Liabilities Subtract

**Timing window:** `8.0s - 12.5s`

**Narration subtitle:**

> Credit card and mortgage appear in rose and subtract from the total.

**On-screen elements:** Liability rows below with minus signs, a subtraction rail, subtotal moving downward.

**Animation physics:** The subtraction rail sweeps downward over 600ms; the running total animates down while assets stay fixed.

### Scene 4 — One Number

**Timing window:** `12.5s - 16.0s`

**Narration subtitle:**

> The net worth figure locks in with a 3.2% month-over-month delta.

**On-screen elements:** Large mono net worth figure, MoM delta chip, a small sparkline of the last 6 months.

**Animation physics:** Final counter lands on an exact value; the delta chip slides in from the right with a 200ms spring; sparkline draws in 500ms.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Institution cards** | Connected sources | 160x96 rounded rects with a logo glyph, name and status dot |
| **Asset stack** | Positive balances | Row stack with 2px emerald rules on the left edge |
| **Subtraction rail** | Liability math | Vertical rail with a downward arrow and a minus operator glyph |
| **Net worth figure** | Single truth | Mono 56px with tabular-nums and a currency symbol at 60% size |
| **MoM sparkline** | Trend | Six-point polyline with a soft area fill and an endpoint dot |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- The running total must equal assets minus liabilities at every frame, computed rather than tweened independently.
- Liability rows never use the same green as assets, even at low opacity.
- Negative values use a true minus sign, not a hyphen.
- The final number is the primary type on screen; everything else shrinks by at least one step.

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
  'Four accounts connect with a verified badge each.',
  'Checking, brokerage, retirement and property sum into total assets.',
  'Credit card and mortgage appear in rose and subtract from the total.',
  'The net worth figure locks in with a 3.2% month-over-month delta.'
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
const NET_WORTH = { assets: [{ name: 'Checking', value: 18_400 }, { name: 'Brokerage', value: 96_200 }, { name: '401(k)', value: 212_800 }, { name: 'Home', value: 540_000 }], liabilities: [{ name: 'Credit Card', value: 4_150 }, { name: 'Mortgage', value: 318_600 }], totalAssets: 867_400, totalLiabilities: 322_750, netWorth: 544_650, momDelta: 0.032 };
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

This is the skill where tabular-nums matters most. A shifting net worth figure during counting looks like a rendering defect.

---

**Previous:** [Order Book Depth](skill-28-order-book-depth.md) | **Next:** [Dollar-Cost Averaging](skill-30-dca-simulator.md) | **Index:** [README](../README.md)
