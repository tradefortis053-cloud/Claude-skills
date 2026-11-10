# Skill 48 — SaaS MRR Waterfall

**Category E:** B2B SaaS, Lending & Credit

> New, expansion and churn stacking into one honest net ARR number.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `48` |
| **Slug** | `skill-48-saas-mrr-waterfall` |
| **Category** | B2B SaaS, Lending & Credit |
| **Output file** | `output/skill-48-saas-mrr-waterfall.html` |
| **Timeline length** | 17s (17,000 ms) at 1x speed |
| **Accent pair** | `#10B981` primary, `#F43F5E` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #48`
- `Run skill-48-saas-mrr-waterfall`
- `Build the saas mrr waterfall explainer`
- A natural-language request whose intent matches: _Explain MRR movement: new business, expansion, contraction, churn, and net new MRR building to ending ARR._

### Objective

Explain MRR movement: new business, expansion, contraction, churn, and net new MRR building to ending ARR.

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
| **Scene 1: Starting MRR** | 0.0s - 3.5s | The opening balance of $412,000 stands as a solid column. |
| **Scene 2: Additions** | 3.5s - 8.5s | New business and expansion stack upward in green. |
| **Scene 3: Subtractions** | 8.5s - 13.5s | Contraction and churn pull down in rose. |
| **Scene 4: Net ARR** | 13.5s - 17.0s | The closing bar resolves to $446,800 with net new of $34,800. |

### Scene 1 — Starting MRR

**Timing window:** `0.0s - 3.5s`

**Narration subtitle:**

> The opening balance of $412,000 stands as a solid column.

**On-screen elements:** Single bar with a mono label and a baseline grid.

**Animation physics:** The bar grows from zero in 500ms; the label counts in with tabular-nums and locks.

### Scene 2 — Additions

**Timing window:** `3.5s - 8.5s`

**Narration subtitle:**

> New business and expansion stack upward in green.

**On-screen elements:** Two stacked positive segments with labels NEW and EXPANSION, floating connector rules.

**Animation physics:** Each segment grows 0 -> full over 400ms at 200ms offsets; connector rules draw horizontally after each settles.

### Scene 3 — Subtractions

**Timing window:** `8.5s - 13.5s`

**Narration subtitle:**

> Contraction and churn pull down in rose.

**On-screen elements:** Two negative segments with labels CONTRACTION and CHURN, descending connectors.

**Animation physics:** Segments drop on a 320ms ease-in; a 1px baseline marker indicates where the bar started so the net is readable.

### Scene 4 — Net ARR

**Timing window:** `13.5s - 17.0s`

**Narration subtitle:**

> The closing bar resolves to $446,800 with net new of $34,800.

**On-screen elements:** Final bar, net new label, a growth rate of 8.4% MoM, an ARR annualization note.

**Animation physics:** The closing bar eases to its final height over 500ms; the net label fades in centered on the delta; hold.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Waterfall columns** | MRR movement | Vertical bars 56px wide with 3px gaps and rounded 2px caps |
| **Connector rules** | Continuity | Horizontal 1px dashed lines linking bar tops |
| **Value labels** | Amounts | Mono 13px centered above each column |
| **Baseline** | Zero reference | 1px line across the chart at 20% opacity |
| **Delta brace** | Net new MRR | Vertical brace spanning the net change with a mono label |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- Waterfall column heights must reconcile exactly: opening plus additions minus subtractions equals closing.
- Negative segments start from the previous cumulative top, not from the baseline.
- Connector rules draw only after the adjacent columns finish, so the eye follows the arithmetic.
- Churn is never hidden in a net number; it gets its own visible segment.

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
  'The opening balance of $412,000 stands as a solid column.',
  'New business and expansion stack upward in green.',
  'Contraction and churn pull down in rose.',
  'The closing bar resolves to $446,800 with net new of $34,800.'
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
const WATERFALL = { startMrr: 412_000, new: 38_400, expansion: 21_600, contraction: 9_200, churn: 16_000, netNew: 34_800, endMrr: 446_800, growthMoM: 0.084, endArr: 5_361_600 };
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

The reconciliation is the entire point. Compute closing from the components at load and render that, so the chart cannot lie.

---

**Previous:** [Cap Table Dilution](skill-47-cap-table-dilution.md) | **Next:** [Usage-Based Billing](skill-49-usage-based-billing.md) | **Index:** [README](../README.md)
