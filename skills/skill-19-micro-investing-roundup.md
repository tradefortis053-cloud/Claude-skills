# Skill 19 — Micro-Investing Round-Up

**Category B:** Banking Infrastructure & Ledgers

> A $4.60 coffee that quietly invests its $0.40 of loose change.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `19` |
| **Slug** | `skill-19-micro-investing-roundup` |
| **Category** | Banking Infrastructure & Ledgers |
| **Output file** | `output/skill-19-micro-investing-roundup.html` |
| **Timeline length** | 15s (15,000 ms) at 1x speed |
| **Accent pair** | `#10B981` primary, `#4F46E5` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #19`
- `Run skill-19-micro-investing-roundup`
- `Build the micro-investing round-up explainer`
- A natural-language request whose intent matches: _Show spare-change investing: purchase capture, round-up calculation, batch aggregation and a fractional share purchase._

### Objective

Show spare-change investing: purchase capture, round-up calculation, batch aggregation and a fractional share purchase.

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
| **Scene 1: Coffee Purchase** | 0.0s - 3.5s | A $4.60 charge clears and the amount settles in mono. |
| **Scene 2: Round-Up Math** | 3.5s - 7.5s | The engine rounds to $5.00 and isolates the $0.40 delta. |
| **Scene 3: Batch Aggregation** | 7.5s - 11.0s | Five round-ups batch into a $2.15 weekly sweep. |
| **Scene 4: Fractional Purchase** | 11.0s - 15.0s | The batch buys 0.0214 of a share and the portfolio grows. |

### Scene 1 — Coffee Purchase

**Timing window:** `0.0s - 3.5s`

**Narration subtitle:**

> A $4.60 charge clears and the amount settles in mono.

**On-screen elements:** Merchant chip, receipt line, $4.60 amount, card glyph.

**Animation physics:** Receipt line draws in; the amount counts from 0 to 4.60 in 400ms with tabular-nums.

### Scene 2 — Round-Up Math

**Timing window:** `3.5s - 7.5s`

**Narration subtitle:**

> The engine rounds to $5.00 and isolates the $0.40 delta.

**On-screen elements:** Amount splits into $4.60 spent and $0.40 invested, a coin glyph for the remainder.

**Animation physics:** The $0.40 chip lifts out of the total with a 12px rise and separates on a spring.

### Scene 3 — Batch Aggregation

**Timing window:** `7.5s - 11.0s`

**Narration subtitle:**

> Five round-ups batch into a $2.15 weekly sweep.

**On-screen elements:** Five coin chips stacking into a weekly bucket, a running total.

**Animation physics:** Coins drop in at 120ms intervals with a 4px bounce; the bucket total counts up in step.

### Scene 4 — Fractional Purchase

**Timing window:** `11.0s - 15.0s`

**Narration subtitle:**

> The batch buys 0.0214 of a share and the portfolio grows.

**On-screen elements:** Portfolio line chart rising, shares counter at 4 decimals, position value.

**Animation physics:** Chart path draws on a 900ms ease-out; the share counter increments with a 4-decimal mono format.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Coin chips** | Spare change | 28px circles with a currency glyph and a 6px inner ring |
| **Amount split** | Allocation | Two stacked amount rows with a divider that splits outward |
| **Weekly bucket** | Aggregation | Open-top container 120x160 with a fill line |
| **Portfolio curve** | Investment growth | Polyline of 24 seeded points with a gradient area fill beneath |
| **Share counter** | Ownership | Mono 32px with 4 decimal places and a smaller ticker label |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- The split must be arithmetically visible: 4.60 + 0.40 must equal 5.00 in the rendered text at all times.
- Coin drops use a single shared easing with staggered start times.
- Chart growth is montonic; never let the seeded series dip during the purchase scene.
- Share quantity uses 4 decimals, because fractional investing lives or dies on that precision.

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
  'A $4.60 charge clears and the amount settles in mono.',
  'The engine rounds to $5.00 and isolates the $0.40 delta.',
  'Five round-ups batch into a $2.15 weekly sweep.',
  'The batch buys 0.0214 of a share and the portfolio grows.'
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
const ROUNDUP = { purchase: 4.60, rounded: 5.00, spare: 0.40, weeklyBatch: 2.15, asset: 'VTI', price: 271.40, sharesBought: 0.00792, portfolioValue: 1284.16 };
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

Verify the arithmetic against the displayed share count and price. Inconsistent numbers are the fastest way to lose a fintech audience.

---

**Previous:** [Open Banking OAuth](skill-18-open-banking-oauth.md) | **Next:** [Treasury Yield Sweep](skill-20-treasury-yield-flow.md) | **Index:** [README](../README.md)
