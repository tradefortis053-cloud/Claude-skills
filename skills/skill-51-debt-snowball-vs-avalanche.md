# Skill 51 — Debt Snowball vs Avalanche

**Category E:** B2B SaaS, Lending & Credit

> Two payoff strategies racing to zero with different curves and the same finish line.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `51` |
| **Slug** | `skill-51-debt-snowball-vs-avalanche` |
| **Category** | B2B SaaS, Lending & Credit |
| **Output file** | `output/skill-51-debt-snowball-vs-avalanche.html` |
| **Timeline length** | 19s (19,000 ms) at 1x speed |
| **Accent pair** | `#4F46E5` primary, `#10B981` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #51`
- `Run skill-51-debt-snowball-vs-avalanche`
- `Build the debt snowball vs avalanche explainer`
- A natural-language request whose intent matches: _Compare debt snowball and avalanche: ordering by balance versus rate, total interest paid, and payoff time under both._

### Objective

Compare debt snowball and avalanche: ordering by balance versus rate, total interest paid, and payoff time under both.

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
| **Scene 1: Debt Loaded** | 0.0s - 3.5s | Four debts load with balances and APRs. |
| **Scene 2: Snowball Starts** | 3.5s - 8.5s | The snowball pays the smallest balance first regardless of rate. |
| **Scene 3: Avalanche Starts** | 8.5s - 13.5s | The avalanche targets the highest APR first. |
| **Scene 4: Finish Line** | 13.5s - 19.0s | Both reach zero; the avalanche saves $1,340 and 3 months. |

### Scene 1 — Debt Loaded

**Timing window:** `0.0s - 3.5s`

**Narration subtitle:**

> Four debts load with balances and APRs.

**On-screen elements:** Four debt cards with balance and APR, a total balance of $28,400.

**Animation physics:** Cards stack in at 80ms intervals; the total counts up and locks with a mono summary line.

### Scene 2 — Snowball Starts

**Timing window:** `3.5s - 8.5s`

**Narration subtitle:**

> The snowball pays the smallest balance first regardless of rate.

**On-screen elements:** Left payoff track, debt cards ordered by balance ascending, cross-out stamps.

**Animation physics:** Cards cross out sequentially at 500ms intervals; each cross-out shrinks the balance to zero.

### Scene 3 — Avalanche Starts

**Timing window:** `8.5s - 13.5s`

**Narration subtitle:**

> The avalanche targets the highest APR first.

**On-screen elements:** Right payoff track, debt cards ordered by APR descending, an interest-saved counter.

**Animation physics:** Parallel progress with the snowball, but the interest counter runs lower; both tracks share the same time axis.

### Scene 4 — Finish Line

**Timing window:** `13.5s - 19.0s`

**Narration subtitle:**

> Both reach zero; the avalanche saves $1,340 and 3 months.

**On-screen elements:** Two race lanes converging to zero, a comparison card with months and interest.

**Animation physics:** Lane markers land at different months on the same axis; the comparison card reveals both figures side by side and holds.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Debt cards** | Obligations | Four 220x80 cards with balance, APR and a status stamp area |
| **Payoff tracks** | Strategy lanes | Two horizontal lanes with month ticks and a zero line |
| **Cross-out stamp** | Debt cleared | Rotated -8deg uppercase outline stamp with a 1.5px stroke |
| **Race markers** | Progress | Circular markers that traverse their lane based on remaining balance |
| **Comparison card** | Outcome | Three-row table: months, total interest, interest saved |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- Both lanes share one time axis; different time scales would invalidate the comparison entirely.
- Snowball visually clears cards faster at the start, which is the honest psychological benefit.
- The avalanche's interest saving is the counterweight and must appear in the same frame as the finish.
- Number of months and interest must come from the simulated amortization, not estimates.

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
  'Four debts load with balances and APRs.',
  'The snowball pays the smallest balance first regardless of rate.',
  'The avalanche targets the highest APR first.',
  'Both reach zero; the avalanche saves $1,340 and 3 months.'
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
const DEBT = { totalBalance: 28_400, debts: [{ name: 'Store Card', balance: 1_200, apr: 0.2699 }, { name: 'Credit Card', balance: 6_400, apr: 0.2249 }, { name: 'Auto Loan', balance: 8_800, apr: 0.0695 }, { name: 'Student Loan', balance: 12_000, apr: 0.051 }, snowballMonths: 34, avalancheMonths: 31, snowballInterest: 4_890, avalancheInterest: 3_550 };
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

Simulate the amortization properly, at least monthly, including minimum payments. Both lanes must reconcile to the same total paid.

---

**Previous:** [Customs and Trade Finance](skill-50-customs-trade-finance.md) | **Next:** [Chargeback Dispute Flow](skill-52-chargeback-dispute-flow.md) | **Index:** [README](../README.md)
