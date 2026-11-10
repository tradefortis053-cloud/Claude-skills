# Skill 16 — Automated Reconciliation

**Category B:** Banking Infrastructure & Ledgers

> Two columns of numbers snapping together with green connector lines.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `16` |
| **Slug** | `skill-16-automated-reconciliation` |
| **Category** | Banking Infrastructure & Ledgers |
| **Output file** | `output/skill-16-automated-reconciliation.html` |
| **Timeline length** | 18s (18,000 ms) at 1x speed |
| **Accent pair** | `#10B981` primary, `#F43F5E` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #16`
- `Run skill-16-automated-reconciliation`
- `Build the automated reconciliation explainer`
- A natural-language request whose intent matches: _Show reconciliation between internal ledger and bank statement: auto-matching, exception surfacing, and a final balanced state._

### Objective

Show reconciliation between internal ledger and bank statement: auto-matching, exception surfacing, and a final balanced state.

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
| **Scene 1: Two Sources** | 0.0s - 4.0s | Internal ledger and bank statement load in parallel columns. |
| **Scene 2: Auto Match** | 4.0s - 10.0s | The engine matches nine of ten rows with green connector lines. |
| **Scene 3: Exception** | 10.0s - 14.5s | One row has a 2-cent difference and is routed to review. |
| **Scene 4: Balanced** | 14.5s - 18.0s | The exception resolves and both totals agree exactly. |

### Scene 1 — Two Sources

**Timing window:** `0.0s - 4.0s`

**Narration subtitle:**

> Internal ledger and bank statement load in parallel columns.

**On-screen elements:** Two scrolling columns with mono amounts, dates and reference IDs.

**Animation physics:** Columns populate top-down on a 40ms stagger; scroll offset syncs so rows align horizontally.

### Scene 2 — Auto Match

**Timing window:** `4.0s - 10.0s`

**Narration subtitle:**

> The engine matches nine of ten rows with green connector lines.

**On-screen elements:** Connector arcs between matching rows, match confidence badges at 100%.

**Animation physics:** Arcs draw left to right in 180ms each with a 90ms stagger; matched rows gain a subtle emerald left border.

### Scene 3 — Exception

**Timing window:** `10.0s - 14.5s`

**Narration subtitle:**

> One row has a 2-cent difference and is routed to review.

**On-screen elements:** Amber row pair, a delta chip reading +0.02, a review queue slot.

**Animation physics:** Non-matching pair shakes 2px horizontally once, then lifts into the exception tray over 400ms.

### Scene 4 — Balanced

**Timing window:** `14.5s - 18.0s`

**Narration subtitle:**

> The exception resolves and both totals agree exactly.

**On-screen elements:** Two total rows converging to the same figure, a reconciled stamp.

**Animation physics:** Both totals count to the identical value; stamp lands with a 240ms spring and a 1px rule underline.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Ledger column** | Internal records | 380x420 panel with 10 rows, mono right-aligned amounts |
| **Statement column** | External records | Mirrored panel with slightly different row ordering to imply messy source data |
| **Connector arcs** | Match linkage | Cubic beziers drawn across the gutter with a 1.5px emerald stroke |
| **Delta chip** | Discrepancy | Pill with signed value and amber fill at 12% opacity |
| **Reconciled stamp** | Closure | Rotated -6deg rounded outline with uppercase tracking 0.16em |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- Row scroll must be synchronized between columns; independent scrolling breaks the matching metaphor.
- Match arcs animate only after both endpoint rows are fully visible.
- The exception shake happens exactly once, 2px amplitude, 120ms total.
- Final totals must be numerically identical, computed from the data array rather than hard-coded.

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
  'Internal ledger and bank statement load in parallel columns.',
  'The engine matches nine of ten rows with green connector lines.',
  'One row has a 2-cent difference and is routed to review.',
  'The exception resolves and both totals agree exactly.'
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
const RECON = { ledgerTotal: 284_915.42, statementTotal: 284_915.42, rows: 10, autoMatched: 9, exceptions: [{ ref: 'INV-8841', delta: 0.02, reason: 'FX rounding' }], matchRate: '90%' };
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

Compute totals live from the row data. Reviewers do add the columns up, and a mismatch destroys trust instantly.

---

**Previous:** [Smart Contract Execution](skill-15-smart-contract-exec.md) | **Next:** [Virtual Card Issuance](skill-17-virtual-card-issuance.md) | **Index:** [README](../README.md)
