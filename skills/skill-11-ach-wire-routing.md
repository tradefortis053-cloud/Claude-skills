# Skill 11 — ACH, Wire and Real-Time Routing

**Category B:** Banking Infrastructure & Ledgers

> Three rails, three clocks, one clearing house.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `11` |
| **Slug** | `skill-11-ach-wire-routing` |
| **Category** | Banking Infrastructure & Ledgers |
| **Output file** | `output/skill-11-ach-wire-routing.html` |
| **Timeline length** | 19s (19,000 ms) at 1x speed |
| **Accent pair** | `#4F46E5` primary, `#10B981` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #11`
- `Run skill-11-ach-wire-routing`
- `Build the ach, wire and real-time routing explainer`
- A natural-language request whose intent matches: _Compare batch ACH, same-day ACH and real-time rails on cost, cutoff time and settlement latency using a multi-hop clearing house diagram._

### Objective

Compare batch ACH, same-day ACH and real-time rails on cost, cutoff time and settlement latency using a multi-hop clearing house diagram.

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
| **Scene 1: Origination** | 0.0s - 4.0s | Three payment files leave the originator for the clearing house. |
| **Scene 2: Batch Queue** | 4.0s - 9.5s | ACH packets queue into a batch envelope while RTP packets go straight through. |
| **Scene 3: Clearing and Settlement** | 9.5s - 14.5s | The clearing house nets positions and settles each rail at its own cadence. |
| **Scene 4: Cost and Cutoff** | 14.5s - 19.0s | A compact comparison shows fee and cutoff for each rail. |

### Scene 1 — Origination

**Timing window:** `0.0s - 4.0s`

**Narration subtitle:**

> Three payment files leave the originator for the clearing house.

**On-screen elements:** Originator block, three parallel rails labeled ACH, SAME-DAY, RTP, each with a clock badge.

**Animation physics:** Rails draw simultaneously; clock badges show 1-2 days, same day and 10 seconds respectively.

### Scene 2 — Batch Queue

**Timing window:** `4.0s - 9.5s`

**Narration subtitle:**

> ACH packets queue into a batch envelope while RTP packets go straight through.

**On-screen elements:** Batch envelope filling with 40 small packet ticks, RTP packets bypassing the queue.

**Animation physics:** Tick fill is a seeded 40-step loop at 60ms; the RTP lane visibly overtakes with a cyan streak.

### Scene 3 — Clearing and Settlement

**Timing window:** `9.5s - 14.5s`

**Narration subtitle:**

> The clearing house nets positions and settles each rail at its own cadence.

**On-screen elements:** Netting table, three settlement timestamps, receiver bank block.

**Animation physics:** Rows land with 90ms stagger; timestamps count up from zero to their final values.

### Scene 4 — Cost and Cutoff

**Timing window:** `14.5s - 19.0s`

**Narration subtitle:**

> A compact comparison shows fee and cutoff for each rail.

**On-screen elements:** Three-column comparison card with mono figures and a recommended-rail highlight.

**Animation physics:** Columns reveal left to right; the recommended cell gets a 2px indigo outline that draws on.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Originator block** | Initiating institution | 320x90 rounded rect with a mono institution label and three output ports |
| **Rail lanes** | Payment systems | Three horizontal lanes with 2px strokes and dashed center guides |
| **Batch envelope** | ACH batching | Rounded rect with a 40-cell grid and a fill-progress clip path |
| **Netting table** | Clearing logic | Four-column grid with mono values, right aligned |
| **Clock badges** | Latency | Circle with a clock face and a mono duration label beneath |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- The RTP lane must visually finish before the ACH lane shows even 20% progress; that asymmetry is the entire lesson.
- Batch fill is a clipped mask, not 40 individually animated nodes.
- Timestamps tween as integers so they never show fractional milliseconds.
- Use the same easing family across all three lanes so the comparison stays fair.

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
  'Three payment files leave the originator for the clearing house.',
  'ACH packets queue into a batch envelope while RTP packets go straight through.',
  'The clearing house nets positions and settles each rail at its own cadence.',
  'A compact comparison shows fee and cutoff for each rail.'
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
const RAILS = [{ name: 'ACH Standard', fee: 0.29, eta: '1-2 business days', cutoff: '14:45 ET' }, { name: 'Same-Day ACH', fee: 0.55, eta: 'Same day', cutoff: '12:45 ET' }, { name: 'RTP / FedNow', fee: 0.045, eta: 'Under 10 seconds', cutoff: '24/7' }];
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

Fees vary by provider. Label the figures as illustrative in the caption so the demo never reads as a rate sheet.

---

**Previous:** [Multi-Currency Wallet](skill-10-multi-currency-wallet.md) | **Next:** [Immutable Ledger](skill-12-immutable-ledger.md) | **Index:** [README](../README.md)
