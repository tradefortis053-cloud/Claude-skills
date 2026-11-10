# Skill 07 — Subscription Recurring Billing

**Category A:** Payment Flows & Transactions

> A circular calendar that bills, retries and recovers without ever leaving the loop.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `07` |
| **Slug** | `skill-07-subscription-recurring` |
| **Category** | Payment Flows & Transactions |
| **Output file** | `output/skill-07-subscription-recurring.html` |
| **Timeline length** | 18s (18,000 ms) at 1x speed |
| **Accent pair** | `#4F46E5` primary, `#F43F5E` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #07`
- `Run skill-07-subscription-recurring`
- `Build the subscription recurring billing explainer`
- A natural-language request whose intent matches: _Explain the subscription billing cycle including the invoice trigger, smart retry ladder on a soft decline, and a voluntary cancellation path._

### Objective

Explain the subscription billing cycle including the invoice trigger, smart retry ladder on a soft decline, and a voluntary cancellation path.

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
| **Scene 1: Cycle Begins** | 0.0s - 4.0s | A 12-month ring draws and the current month marker slides into place. |
| **Scene 2: Auto Charge** | 4.0s - 8.5s | The card is charged and a micro-deduction ripple fires each cycle. |
| **Scene 3: Soft Decline** | 8.5s - 13.5s | A decline hits, then a retry ladder runs D+1, D+3, D+5. |
| **Scene 4: Recovered or Cancelled** | 13.5s - 18.0s | Retry succeeds and the loop resumes, with the cancel path shown dimmed. |

### Scene 1 — Cycle Begins

**Timing window:** `0.0s - 4.0s`

**Narration subtitle:**

> A 12-month ring draws and the current month marker slides into place.

**On-screen elements:** Concentric month ring, 12 tick marks, a cardinal marker, $49 per month chip.

**Animation physics:** Ring draws with stroke-dashoffset over 1.4s; marker slides to the 4th tick using a spring.

### Scene 2 — Auto Charge

**Timing window:** `4.0s - 8.5s`

**Narration subtitle:**

> The card is charged and a micro-deduction ripple fires each cycle.

**On-screen elements:** Card chip, charge pulses radiating inward, balance ticking down.

**Animation physics:** Each monthly pulse uses a 300ms scale + opacity pair, staggered by 240ms across three simulated cycles.

### Scene 3 — Soft Decline

**Timing window:** `8.5s - 13.5s`

**Narration subtitle:**

> A decline hits, then a retry ladder runs D+1, D+3, D+5.

**On-screen elements:** Rose status chip, three retry nodes on a horizontal ladder with day labels.

**Animation physics:** Ladder nodes lock in sequence with a 200ms fade; the active node pulses in rose until it resolves.

### Scene 4 — Recovered or Cancelled

**Timing window:** `13.5s - 18.0s`

**Narration subtitle:**

> Retry succeeds and the loop resumes, with the cancel path shown dimmed.

**On-screen elements:** Emerald recovery chip, loop re-entering, dimmed cancel branch with a 40% opacity label.

**Animation physics:** Recovery chip swaps label with a crossfade; the loop arrow re-draws once to signal continuity.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Month ring** | Billing calendar | Circle r=140 with 12 radial tick lines and one cardinal marker |
| **Charge pulses** | Micro-deductions | Three concentric circles with staggered scale and opacity animations |
| **Retry ladder** | Dunning logic | Polyline with three 28px nodes and mono day labels D+1, D+3, D+5 |
| **Card chip** | Payment method | Rounded rect 160x100 with a chip rect and truncated PAN |
| **Cancel branch** | Churn path | Dashed path branching downward at 40% opacity |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- Retry nodes resolve on progress thresholds, not timers, so a scrub to 90% shows the correct ladder state.
- Loss and recovery colours stay separate: rose only for decline, emerald only for recovery.
- Ambient ring rotation runs at 6deg/s and must pause with playback.
- Charge ripples reverse their scale direction on retry to visually signal a second attempt.

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
  'A 12-month ring draws and the current month marker slides into place.',
  'The card is charged and a micro-deduction ripple fires each cycle.',
  'A decline hits, then a retry ladder runs D+1, D+3, D+5.',
  'Retry succeeds and the loop resumes, with the cancel path shown dimmed.'
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
const SUBSCRIPTION = { plan: 'Pro Annual', monthly: 49.00, currency: 'USD', cycle: 'monthly', retryLadder: [1, 3, 5], declineCode: 'soft_decline', recoveryRate: 0.72 };
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

Dunning is the most under-visualized part of billing. Give the retry ladder a full third of the runtime.

---

**Previous:** [Escrow Release](skill-06-escrow-release.md) | **Next:** [Refund Reversal](skill-08-refund-reversal.md) | **Index:** [README](../README.md)
