# Skill 46 — Revenue-Based Financing

**Category E:** B2B SaaS, Lending & Credit

> A repayment bar that breathes with revenue instead of marching on a calendar.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `46` |
| **Slug** | `skill-46-revenue-based-financing` |
| **Category** | B2B SaaS, Lending & Credit |
| **Output file** | `output/skill-46-revenue-based-financing.html` |
| **Timeline length** | 17s (17,000 ms) at 1x speed |
| **Accent pair** | `#4F46E5` primary, `#10B981` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #46`
- `Run skill-46-revenue-based-financing`
- `Build the revenue-based financing explainer`
- A natural-language request whose intent matches: _Explain RBF: an upfront advance, a fixed repayment multiple, a percentage of monthly revenue, and the true cost of capital._

### Objective

Explain RBF: an upfront advance, a fixed repayment multiple, a percentage of monthly revenue, and the true cost of capital.

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
| **Scene 1: Capital Advance** | 0.0s - 3.5s | A $500,000 advance lands with a repayment cap of $650,000. |
| **Scene 2: Revenue Share** | 3.5s - 9.0s | Each month remits 8% of revenue and the bar tracks proportionally. |
| **Scene 3: Slow Month** | 9.0s - 13.5s | A weak month means a smaller payment and a longer tail. |
| **Scene 4: Fully Repaid** | 13.5s - 17.0s | The cap is reached and the obligation ends, with the effective APR shown. |

### Scene 1 — Capital Advance

**Timing window:** `0.0s - 3.5s`

**Narration subtitle:**

> A $500,000 advance lands with a repayment cap of $650,000.

**On-screen elements:** Advance card, a repayment multiple of 1.3x, a cap amount, terms summary.

**Animation physics:** The advance amount counts in over 500ms; the 1.3x multiple chip scales in at 200ms and stays fixed.

### Scene 2 — Revenue Share

**Timing window:** `3.5s - 9.0s`

**Narration subtitle:**

> Each month remits 8% of revenue and the bar tracks proportionally.

**On-screen elements:** Monthly revenue bars rising and falling, a remittance overlay on each bar, a cumulative repaid counter.

**Animation physics:** Bars animate month by month at 320ms each; the remittance overlay grows with a 100ms lag; the cumulative counter follows.

### Scene 3 — Slow Month

**Timing window:** `9.0s - 13.5s`

**Narration subtitle:**

> A weak month means a smaller payment and a longer tail.

**On-screen elements:** A short revenue bar, a visibly small remittance, the projected payoff date moving later.

**Animation physics:** The projected date slides right with a 300ms ease; the short bar renders at 40% height with a muted tint.

### Scene 4 — Fully Repaid

**Timing window:** `13.5s - 17.0s`

**Narration subtitle:**

> The cap is reached and the obligation ends, with the effective APR shown.

**On-screen elements:** Cap reached badge, effective annualized cost 18.4%, total months 26.

**Animation physics:** The cumulative counter lands exactly on the cap; the effective-APR figure fades in last; hold.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Revenue bars** | Monthly performance | Width 28, height mapped to revenue, 4px gap, at 30% opacity base fill |
| **Remittance overlay** | Investor share | Same-width bar segment drawn from the base at 80% opacity in indigo |
| **Cumulative counter** | Progress to cap | Mono 36px with a progress bar beneath |
| **Payoff projection** | Timeline | Date chip that translates along a horizontal rule |
| **Cap badge** | Completion | Emerald badge with a check and a total figure |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- Remittance is always exactly the stated percentage of the rendered revenue bar; recompute per frame.
- The cumulative counter must stop exactly at the cap, never overshoot.
- The payoff date only moves later, never earlier, when revenue dips.
- Show effective annualized cost at the end; RBF is cheaper than equity only sometimes, and the number should speak.

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
  'A $500,000 advance lands with a repayment cap of $650,000.',
  'Each month remits 8% of revenue and the bar tracks proportionally.',
  'A weak month means a smaller payment and a longer tail.',
  'The cap is reached and the obligation ends, with the effective APR shown.'
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
const RBF = { advance: 500_000, multiple: 1.3, cap: 650_000, revenueSharePct: 0.08, months: 26, strongMonth: 210_000, weakMonth: 96_000, effectiveApr: 0.184 };
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

The effective APR is the honest counterweight to the friendly 'we only take a share' framing. Keep it in the final frame, not buried.

---

**Previous:** [Expense Receipt OCR](skill-45-expense-receipt-ocr.md) | **Next:** [Cap Table Dilution](skill-47-cap-table-dilution.md) | **Index:** [README](../README.md)
