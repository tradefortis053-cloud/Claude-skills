# Skill 47 — Cap Table Dilution

**Category E:** B2B SaaS, Lending & Credit

> Founder equity shrinking while the pie grows faster than it shrinks.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `47` |
| **Slug** | `skill-47-cap-table-dilution` |
| **Category** | B2B SaaS, Lending & Credit |
| **Output file** | `output/skill-47-cap-table-dilution.html` |
| **Timeline length** | 18s (18,000 ms) at 1x speed |
| **Accent pair** | `#4F46E5` primary, `#10B981` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #47`
- `Run skill-47-cap-table-dilution`
- `Build the cap table dilution explainer`
- A natural-language request whose intent matches: _Show dilution mechanics across rounds: pre and post-money, option pool expansion, founder dilution, and the absolute value effect._

### Objective

Show dilution mechanics across rounds: pre and post-money, option pool expansion, founder dilution, and the absolute value effect.

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
| **Scene 1: Founding Cap Table** | 0.0s - 3.5s | Two founders hold 100% split 60/40. |
| **Scene 2: Seed Round** | 3.5s - 8.0s | A $2M seed at $8M pre-money mints new shares and dilutes founders. |
| **Scene 3: Option Pool** | 8.0s - 12.5s | A 10% option pool is carved from the founders, not the investor. |
| **Scene 4: Series A** | 12.5s - 18.0s | A $6M Series A at $24M pre-money lands, and absolute value still rises. |

### Scene 1 — Founding Cap Table

**Timing window:** `0.0s - 3.5s`

**Narration subtitle:**

> Two founders hold 100% split 60/40.

**On-screen elements:** Pie with two segments, founder labels, a note that the pie equals 100%.

**Animation physics:** The pie draws clockwise over 700ms; segment labels fade in as each closes.

### Scene 2 — Seed Round

**Timing window:** `3.5s - 8.0s`

**Narration subtitle:**

> A $2M seed at $8M pre-money mints new shares and dilutes founders.

**On-screen elements:** Pie with a new investor slice at 20%, a pre/post money band, a dilution note of -12.0% and -8.0%.

**Animation physics:** The pie re-slices with a 900ms interpolation; founder labels update only after the slice settles.

### Scene 3 — Option Pool

**Timing window:** `8.0s - 12.5s`

**Narration subtitle:**

> A 10% option pool is carved from the founders, not the investor.

**On-screen elements:** An ESOP slice appearing between founders, a pool source annotation.

**Animation physics:** The ESOP slice grows from the founders' arcs specifically; a dashed leader line points to the source.

### Scene 4 — Series A

**Timing window:** `12.5s - 18.0s`

**Narration subtitle:**

> A $6M Series A at $24M pre-money lands, and absolute value still rises.

**On-screen elements:** Pie with four segments, an absolute value callout showing founder stake worth more despite lower ownership.

**Animation physics:** The pie re-slices again; the value callout counts from $4.8M to $10.1M; the caption contrasts percent versus dollars and holds.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Cap table pie** | Ownership | Circle r=150 with segments separated by 2px white gaps |
| **Investor slice** | New ownership | Arc with a distinct hue and a subtle outer ring on first appearance |
| **ESOP slice** | Option pool | Hatched fill at 20% opacity to differentiate from cash ownership |
| **Dilution annotation** | Change | Signed percentage chips anchored at segment midpoints |
| **Absolute value callout** | Dollar outcome | Card with two rows: ownership percent and dollar value |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- All segments must sum to 100.0% after every round; compute and assert at load, not just visually.
- Only the founders' arcs shrink when the pool is created, never the investor's.
- Labels fade in only after their arc stops moving, otherwise the text smears.
- The final scene must present percent and dollars together; dilution without value context is misleading.

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
  'Two founders hold 100% split 60/40.',
  'A $2M seed at $8M pre-money mints new shares and dilutes founders.',
  'A 10% option pool is carved from the founders, not the investor.',
  'A $6M Series A at $24M pre-money lands, and absolute value still rises.'
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
const CAP_TABLE = { rounds: [{ name: 'Founding', founders: [0.60, 0.40], investor: 0, esop: 0 }, { name: 'Seed', founders: [0.48, 0.32], investor: 0.20, esop: 0 }, { name: 'Seed + Pool', founders: [0.43, 0.27], investor: 0.20, esop: 0.10 }, { name: 'Series A', founders: [0.3225, 0.2025], investor: 0.275, esop: 0.20 }], founderValueStart: 4_800_000, founderValueEnd: 10_100_000 };
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

Verify every round's segments sum to 100%. Cap table demos are checked by finance people with a calculator in hand.

---

**Previous:** [Revenue-Based Financing](skill-46-revenue-based-financing.md) | **Next:** [SaaS MRR Waterfall](skill-48-saas-mrr-waterfall.md) | **Index:** [README](../README.md)
