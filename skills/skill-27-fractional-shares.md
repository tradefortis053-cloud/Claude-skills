# Skill 27 — Fractional Shares

**Category C:** Wealth, Trading & Analytics

> One share of a $1,240 stock shattering into 240 affordable hexagons.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `27` |
| **Slug** | `skill-27-fractional-shares` |
| **Category** | Wealth, Trading & Analytics |
| **Output file** | `output/skill-27-fractional-shares.html` |
| **Timeline length** | 15s (15,000 ms) at 1x speed |
| **Accent pair** | `#4F46E5` primary, `#06B6D4` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #27`
- `Run skill-27-fractional-shares`
- `Build the fractional shares explainer`
- A natural-language request whose intent matches: _Show share fractionalization: slicing a whole share into proportional units, distributing them to retail buyers, and re-aggregating ownership._

### Objective

Show share fractionalization: slicing a whole share into proportional units, distributing them to retail buyers, and re-aggregating ownership.

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
| **Scene 1: Whole Share** | 0.0s - 3.0s | A single share sits at $1,240 with a lock icon indicating unaffordability. |
| **Scene 2: Slicing** | 3.0s - 7.5s | The share shatters into a hex grid of proportional units. |
| **Scene 3: Distribution** | 7.5s - 11.5s | Units fly out to five retail buyers in proportion to their budgets. |
| **Scene 4: Re-aggregated** | 11.5s - 15.0s | The distributed units shown back together prove ownership equals one full share. |

### Scene 1 — Whole Share

**Timing window:** `0.0s - 3.0s`

**Narration subtitle:**

> A single share sits at $1,240 with a lock icon indicating unaffordability.

**On-screen elements:** Large hexagon at center, price callout, a lock glyph, a $50 budget chip.

**Animation physics:** Hexagon rotates 0 -> 12deg while settling; the lock glyph pulses twice and dissolves at the end of the scene.

### Scene 2 — Slicing

**Timing window:** `3.0s - 7.5s`

**Narration subtitle:**

> The share shatters into a hex grid of proportional units.

**On-screen elements:** 19 hexagons in a honeycomb, each 1/19 of the whole, a slicing radial wipe.

**Animation physics:** A radial wipe from center-out reveals the grid over 700ms; each hex lands with a 20ms stagger.

### Scene 3 — Distribution

**Timing window:** `7.5s - 11.5s`

**Narration subtitle:**

> Units fly out to five retail buyers in proportion to their budgets.

**On-screen elements:** Five buyer nodes with budget chips, allocator arcs, share counts at 4 decimals.

**Animation physics:** Arcs draw outward at 90ms offsets; each buyer's share counter increments as its arc lands.

### Scene 4 — Re-aggregated

**Timing window:** `11.5s - 15.0s`

**Narration subtitle:**

> The distributed units shown back together prove ownership equals one full share.

**On-screen elements:** Hexes returning to the grid, a 1.0000 share total, a custody note.

**Animation physics:** Hexes return along the same arcs in reverse; the total counter ticks to exactly 1.0000 and holds.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Hexagon grid** | Fractional units | 19 hexagons generated from axial coordinates, 2px gaps, 1px strokes |
| **Lock glyph** | Barrier to entry | Padlock path 36px tall at 60% opacity |
| **Buyer nodes** | Retail participants | Five 44px circles with initials and mono budget chips |
| **Allocator arcs** | Distribution | Five curved paths with gradient strokes and small arrowheads |
| **Total counter** | Ownership proof | Mono 40px with 4 decimals and a smaller 'shares' label |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- Fractional quantities must sum to exactly 1.0000 after rounding; distribute the remainder to the largest allocation.
- Hexagon geometry is computed from axial coordinates at load, then reused for both explosion and return.
- The slicing wipe is radial and monotonic; it must not pulse or reverse mid-animation.
- Return arcs use the identical path objects as the outbound arcs so the round trip is provably symmetric.

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
  'A single share sits at $1,240 with a lock icon indicating unaffordability.',
  'The share shatters into a hex grid of proportional units.',
  'Units fly out to five retail buyers in proportion to their budgets.',
  'The distributed units shown back together prove ownership equals one full share.'
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
const FRACTIONAL = { ticker: 'BRK.A', sharePrice: 1240.00, budget: 50.00, units: 19, buyers: [{ name: 'Maya', budget: 200, shares: 0.1613 }, { name: 'Arjun', budget: 150, shares: 0.1210 }, { name: 'Lena', budget: 300, shares: 0.2419 }, { name: 'Tom', budget: 100, shares: 0.0806 }, { name: 'Priya', budget: 490, shares: 0.3952 }] };
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

Total shares must read exactly 1.0000. Fractional-share demos that land on 0.9999 look like a rounding bug in production.

---

**Previous:** [Tax-Loss Harvesting](skill-26-tax-loss-harvesting.md) | **Next:** [Order Book Depth](skill-28-order-book-depth.md) | **Index:** [README](../README.md)
