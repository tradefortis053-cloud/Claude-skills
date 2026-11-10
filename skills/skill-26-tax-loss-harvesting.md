# Skill 26 — Tax-Loss Harvesting

**Category C:** Wealth, Trading & Analytics

> A red position swapped into a correlated asset while the tax bill shrinks.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `26` |
| **Slug** | `skill-26-tax-loss-harvesting` |
| **Category** | Wealth, Trading & Analytics |
| **Output file** | `output/skill-26-tax-loss-harvesting.html` |
| **Timeline length** | 18s (18,000 ms) at 1x speed |
| **Accent pair** | `#F43F5E` primary, `#10B981` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #26`
- `Run skill-26-tax-loss-harvesting`
- `Build the tax-loss harvesting explainer`
- A natural-language request whose intent matches: _Explain harvesting: realizing a loss, avoiding a wash sale with a correlated substitute, and reducing taxable gains for the year._

### Objective

Explain harvesting: realizing a loss, avoiding a wash sale with a correlated substitute, and reducing taxable gains for the year.

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
| **Scene 1: Underwater Position** | 0.0s - 4.0s | A holding sits 18% below cost basis with an unrealized loss of $4,200. |
| **Scene 2: Harvest Trigger** | 4.0s - 8.5s | The position is sold, realizing the loss. |
| **Scene 3: Correlated Swap** | 8.5s - 13.5s | Proceeds rotate into a correlated but not substantially identical fund. |
| **Scene 4: Tax Saved** | 13.5s - 18.0s | The tax bar drops by $1,050 while market exposure stays constant. |

### Scene 1 — Underwater Position

**Timing window:** `0.0s - 4.0s`

**Narration subtitle:**

> A holding sits 18% below cost basis with an unrealized loss of $4,200.

**On-screen elements:** Holding card with cost basis and market value, an underwater area chart in rose.

**Animation physics:** The chart's filled area is clipped at the cost-basis line; the loss figure counts up in rose with tabular-nums.

### Scene 2 — Harvest Trigger

**Timing window:** `4.0s - 8.5s`

**Narration subtitle:**

> The position is sold, realizing the loss.

**On-screen elements:** Sell ticket, realized loss badge, a ledger entry with a signed amount.

**Animation physics:** The sell ticket slides across the holding card; the realized badge stamps in with a 1.1 scale overshoot.

### Scene 3 — Correlated Swap

**Timing window:** `8.5s - 13.5s`

**Narration subtitle:**

> Proceeds rotate into a correlated but not substantially identical fund.

**On-screen elements:** Two fund cards side by side with a rotation arrow and a similarity chip reading 0.91 correlation.

**Animation physics:** Arrow draws between the cards over 500ms; the similarity chip resolves after the arrow completes.

### Scene 4 — Tax Saved

**Timing window:** `13.5s - 18.0s`

**Narration subtitle:**

> The tax bar drops by $1,050 while market exposure stays constant.

**On-screen elements:** Tax bar comparison before and after, wash-sale guard note, exposure continuity badge.

**Animation physics:** The tax bar shrinks over 700ms; the exposure badge stays fully lit throughout to prove continuity; hold the frame.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Underwater chart** | Unrealized position | Area path in rose at 18% opacity with a dashed cost-basis line |
| **Fund cards** | Instruments | Two 260x160 cards with ticker, name and correlation chip |
| **Rotation arrow** | Substitution | Curved arrow with a gradient stroke between card edges |
| **Tax bar** | Liability | Two stacked horizontal bars labeled BEFORE and AFTER |
| **Wash-sale guard** | Rule compliance | Shield badge with a 30-day clock icon |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- The wash-sale guard must appear before the swap completes, not after; it is the compliance point of the whole skill.
- Correlation is stated, never implied by matching colour alone.
- The tax bar uses the same scale before and after so the reduction is visually honest.
- Keep rose for the loss and emerald for the benefit, but never on the same element simultaneously.

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
  'A holding sits 18% below cost basis with an unrealized loss of $4,200.',
  'The position is sold, realizing the loss.',
  'Proceeds rotate into a correlated but not substantially identical fund.',
  'The tax bar drops by $1,050 while market exposure stays constant.'
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
const HARVEST = { position: 'VTI', costBasis: 23_400, marketValue: 19_200, unrealizedLoss: 4_200, harvested: 4_200, substitute: 'ITOT', correlation: 0.91, taxRate: 0.25, taxSaved: 1_050, washSaleDays: 30 };
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

Always label this as illustrative and not tax advice in the closing caption. The skill is educational, not a recommendation engine.

---

**Previous:** [Dividend Reinvestment](skill-25-dividend-drip.md) | **Next:** [Fractional Shares](skill-27-fractional-shares.md) | **Index:** [README](../README.md)
