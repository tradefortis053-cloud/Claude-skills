# Skill 44 — Payroll Distribution

**Category E:** B2B SaaS, Lending & Credit

> One treasury branching to fifty employees in a single orchestrated wave.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `44` |
| **Slug** | `skill-44-payroll-distribution` |
| **Category** | B2B SaaS, Lending & Credit |
| **Output file** | `output/skill-44-payroll-distribution.html` |
| **Timeline length** | 16s (16,000 ms) at 1x speed |
| **Accent pair** | `#4F46E5` primary, `#10B981` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #44`
- `Run skill-44-payroll-distribution`
- `Build the payroll distribution explainer`
- A natural-language request whose intent matches: _Show bulk payroll disbursement: funding, batch validation, parallel payouts, and per-employee reconciliation status._

### Objective

Show bulk payroll disbursement: funding, batch validation, parallel payouts, and per-employee reconciliation status.

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
| **Scene 1: Treasury Funds** | 0.0s - 3.5s | The company treasury shows $284,600 ready for the August payroll run. |
| **Scene 2: Batch Validation** | 3.5s - 7.5s | The batch passes three validation gates before sending. |
| **Scene 3: Parallel Payout** | 7.5s - 12.5s | Fifty payments fan out simultaneously across three rails. |
| **Scene 4: Reconciled** | 12.5s - 16.0s | 49 succeed, 1 is pending bank verification, and the batch reconciles. |

### Scene 1 — Treasury Funds

**Timing window:** `0.0s - 3.5s`

**Narration subtitle:**

> The company treasury shows $284,600 ready for the August payroll run.

**On-screen elements:** Treasury card, payroll run ID, a funding status badge, 50-employee count.

**Animation physics:** The funding badge flips from PENDING to FUNDED with a 200ms crossfade; the amount counts in.

### Scene 2 — Batch Validation

**Timing window:** `3.5s - 7.5s`

**Narration subtitle:**

> The batch passes three validation gates before sending.

**On-screen elements:** Three gates: balance check, duplicate check, tax withholding check.

**Animation physics:** Gates light in sequence at 400ms intervals; each returns a green pass chip that stays visible.

### Scene 3 — Parallel Payout

**Timing window:** `7.5s - 12.5s`

**Narration subtitle:**

> Fifty payments fan out simultaneously across three rails.

**On-screen elements:** Central treasury node, 50 satellite employee nodes in a radial fan, rail color coding.

**Animation physics:** Arcs draw in a radial sweep from top to bottom over 1.4s; satellites activate in 8ms waves rather than one by one.

### Scene 4 — Reconciled

**Timing window:** `12.5s - 16.0s`

**Narration subtitle:**

> 49 succeed, 1 is pending bank verification, and the batch reconciles.

**On-screen elements:** 49 emerald nodes, 1 amber node, a reconciliation summary and a retry action.

**Animation physics:** The amber node pulses twice; the summary counts 49/50; the retry chip fades in and holds.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Treasury node** | Funding source | 96px rounded square with a building glyph and a mono balance below |
| **Employee satellites** | Recipients | 50 circles radius 8 on two concentric rings at r=180 and r=260 |
| **Payout arcs** | Disbursement | 50 curves from center to satellites in three rail hues |
| **Validation gates** | Pre-flight checks | Three rounded rects with a check slot and a lock glyph |
| **Reconciliation summary** | Outcome | Card with three counters: paid, pending, failed |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- Fifty simultaneous arc draws must be batched by angle band, roughly 8 arcs per 120ms, or the browser will drop frames.
- Satellite activation uses an 8ms cascade, which reads as simultaneous without the cost of 50 independent transitions.
- Never render 50 individual DOM nodes with separate SVG filters; use one group filter and per-node opacity.
- The pending node must remain visible in the final frame; a perfect 50/50 result is less credible than 49/50.

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
  'The company treasury shows $284,600 ready for the August payroll run.',
  'The batch passes three validation gates before sending.',
  'Fifty payments fan out simultaneously across three rails.',
  '49 succeed, 1 is pending bank verification, and the batch reconciles.'
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
const PAYROLL = { runId: 'PR-2026-08', employees: 50, gross: 284_600, rails: ['ACH', 'RTP', 'Local'], paid: 49, pending: 1, failed: 0, totalPaid: 278_420, retryEta: 'Next window 02:00' };
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

Performance is the risk here. Cap animated elements near 80 and reuse a single path template rather than creating 50 unique curves.

---

**Previous:** [Invoice Factoring](skill-43-invoice-factoring.md) | **Next:** [Expense Receipt OCR](skill-45-expense-receipt-ocr.md) | **Index:** [README](../README.md)
