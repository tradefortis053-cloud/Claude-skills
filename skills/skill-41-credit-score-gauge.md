# Skill 41 — Credit Score Gauge

**Category E:** B2B SaaS, Lending & Credit

> A needle sweeping to 742 with the four factors that moved it.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `41` |
| **Slug** | `skill-41-credit-score-gauge` |
| **Category** | B2B SaaS, Lending & Credit |
| **Output file** | `output/skill-41-credit-score-gauge.html` |
| **Timeline length** | 17s (17,000 ms) at 1x speed |
| **Accent pair** | `#10B981` primary, `#4F46E5` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #41`
- `Run skill-41-credit-score-gauge`
- `Build the credit score gauge explainer`
- A natural-language request whose intent matches: _Explain a credit score: the 300 to 850 range, band placement, the weighted factors, and what improves the score over time._

### Objective

Explain a credit score: the 300 to 850 range, band placement, the weighted factors, and what improves the score over time.

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
| **Scene 1: Score Range** | 0.0s - 4.0s | The full 300 to 850 arc draws with band labels. |
| **Scene 2: Needle Sweeps** | 4.0s - 9.5s | The needle climbs to 742 in the Good band. |
| **Scene 3: Factor Weights** | 9.5s - 13.5s | Four weighted factors explain the score. |
| **Scene 4: Improvement Plan** | 13.5s - 17.0s | Two specific actions project a 24-point increase. |

### Scene 1 — Score Range

**Timing window:** `0.0s - 4.0s`

**Narration subtitle:**

> The full 300 to 850 arc draws with band labels.

**On-screen elements:** Semicircular gauge, five bands (Poor to Exceptional), tick labels every 100 points.

**Animation physics:** The arc draws from left to right over 900ms; band labels fade in sequentially; the needle sits at 300.

### Scene 2 — Needle Sweeps

**Timing window:** `4.0s - 9.5s`

**Narration subtitle:**

> The needle climbs to 742 in the Good band.

**On-screen elements:** Needle from 300 to 742, a live numeric readout, a glow trail behind the needle.

**Animation physics:** The needle follows a damped spring with visible deceleration; the readout counts in lockstep; the trail decays over 300ms.

### Scene 3 — Factor Weights

**Timing window:** `9.5s - 13.5s`

**Narration subtitle:**

> Four weighted factors explain the score.

**On-screen elements:** Four horizontal bars with weights 35%, 30%, 15%, 10% plus a 10% mix row.

**Animation physics:** Bars grow left to right at 100ms intervals; the weights sum visibly to 100% in a footer line.

### Scene 4 — Improvement Plan

**Timing window:** `13.5s - 17.0s`

**Narration subtitle:**

> Two specific actions project a 24-point increase.

**On-screen elements:** Action cards with an explicit point effect, a projected needle ghost at 766.

**Animation physics:** A ghost needle renders at 40% opacity; action cards slide in at 120ms intervals; both needles hold at the end.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Gauge arc** | Score range | Semicircle 400px wide with a 14px stroke and rounded caps |
| **Bands** | Score quality | Five arc segments with rose, amber, yellow, emerald and deep emerald fills |
| **Needle** | Current score | Tapered polygon 120px long with a 10px circular hub |
| **Factor bars** | Weights | Four 300x10 rounded bars with labels and mono percentages |
| **Projected needle** | Forecast | Ghost needle at 40% opacity with a dashed outline |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- The needle angle must be a pure function of the score, mapped across the 300 to 850 domain.
- Factor weights must sum to exactly 100% including the catch-all row.
- The projected needle is visually subordinate to the live needle; 40% opacity and dashed.
- Damped spring on the needle means roughly 3% overshoot, no more, or it reads as inaccurate instrumentation.

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
  'The full 300 to 850 arc draws with band labels.',
  'The needle climbs to 742 in the Good band.',
  'Four weighted factors explain the score.',
  'Two specific actions project a 24-point increase.'
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
const CREDIT = { score: 742, range: [300, 850], band: 'Good', factors: [{ name: 'Payment history', weight: 0.35 }, { name: 'Utilization', weight: 0.30 }, { name: 'History length', weight: 0.15 }, { name: 'Mix', weight: 0.10 }, { name: 'New credit', weight: 0.10 }], projected: 766, actions: ['Pay down 12% utilization', 'Dispute one late mark'] };
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

State the scoring model once, in mono, in a corner. Score models differ and unlabeled gauges invite arguments.

---

**Previous:** [Instant Card Freeze](skill-40-instant-card-freeze.md) | **Next:** [BNPL Installments](skill-42-bnpl-installments.md) | **Index:** [README](../README.md)
