# Skill 14 — Liquidity Pool Balancing

**Category B:** Banking Infrastructure & Ledgers

> Two reservoirs finding level through a living SVG wave.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `14` |
| **Slug** | `skill-14-liquidity-pool` |
| **Category** | Banking Infrastructure & Ledgers |
| **Output file** | `output/skill-14-liquidity-pool.html` |
| **Timeline length** | 17s (17,000 ms) at 1x speed |
| **Accent pair** | `#06B6D4` primary, `#4F46E5` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #14`
- `Run skill-14-liquidity-pool`
- `Build the liquidity pool balancing explainer`
- A natural-language request whose intent matches: _Show treasury liquidity management: a pool with two reservoirs, a transfer gate, and rebalancing when coverage thresholds are breached._

### Objective

Show treasury liquidity management: a pool with two reservoirs, a transfer gate, and rebalancing when coverage thresholds are breached.

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
| **Scene 1: Two Reservoirs** | 0.0s - 4.0s | Two tanks sit at different fill levels with a closed gate between them. |
| **Scene 2: Coverage Alert** | 4.0s - 8.5s | Reservoir B dips below its 30% coverage floor and alerts. |
| **Scene 3: Gate Opens** | 8.5s - 13.5s | Funds flow from A to B and both waves settle toward parity. |
| **Scene 4: Balanced** | 13.5s - 17.0s | Both tanks hold near the 52/48 target and the alert clears. |

### Scene 1 — Two Reservoirs

**Timing window:** `0.0s - 4.0s`

**Narration subtitle:**

> Two tanks sit at different fill levels with a closed gate between them.

**On-screen elements:** Two rounded tank outlines with animated wave fills at 78% and 34%, plus a gate valve.

**Animation physics:** Waves use two offset sine paths per tank with a 7s ambient period; fill heights ease in over 1.2s.

### Scene 2 — Coverage Alert

**Timing window:** `4.0s - 8.5s`

**Narration subtitle:**

> Reservoir B dips below its 30% coverage floor and alerts.

**On-screen elements:** Threshold line, amber warning badge, a mono coverage percentage.

**Animation physics:** Threshold line dashes on; badge scales in with a 240ms spring; number ticks down to 28.4%.

### Scene 3 — Gate Opens

**Timing window:** `8.5s - 13.5s`

**Narration subtitle:**

> Funds flow from A to B and both waves settle toward parity.

**On-screen elements:** Gate valve rotating open, particle flow, both wave heights converging.

**Animation physics:** Valve rotates 90deg over 400ms; particles flow at 18 per second; A falls and B rises with mirrored easing.

### Scene 4 — Balanced

**Timing window:** `13.5s - 17.0s`

**Narration subtitle:**

> Both tanks hold near the 52/48 target and the alert clears.

**On-screen elements:** Target bands, emerald status chip, equilibrium caption.

**Animation physics:** Alert badge crossfades away; target bands draw as dashed guides; hold a calm 800ms tail.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Tank outlines** | Reservoir boundary | Rounded rect 200x260 with an open top and a 2px stroke |
| **Wave fill** | Liquid volume | Two sine paths offset by 40px, closed to the tank base and clipped to the tank shape |
| **Gate valve** | Transfer control | Circle with a 12px handle rect and two pipe stubs |
| **Threshold line** | Coverage floor | Dashed horizontal line with a mono percentage pin at the right end |
| **Particle flow** | Capital movement | 12 small circles on a scroller that resets seamlessly at the gate exit |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- Wave phase advances with elapsed animation time, so paused playback freezes the surface exactly where it was.
- Volume is conserved: what A loses, B gains, in the same frame.
- Use a clip-path on the tank so the wave never escapes the outline.
- Alert clearance should be understated. A slow crossfade reads more trustworthy than a celebration.

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
  'Two tanks sit at different fill levels with a closed gate between them.',
  'Reservoir B dips below its 30% coverage floor and alerts.',
  'Funds flow from A to B and both waves settle toward parity.',
  'Both tanks hold near the 52/48 target and the alert clears.'
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
const POOL = { reservoirA: { name: 'Operating', balance: 4_820_000, coverage: 0.78 }, reservoirB: { name: 'Payroll', balance: 1_140_000, coverage: 0.284 }, floor: 0.30, target: { A: 0.52, B: 0.48 }, moved: 620_000 };
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

Use one currency and unit throughout. Mixing dollars and percentages in the same counter column destroys scannability.

---

**Previous:** [API and Webhook Sync](skill-13-api-webhook-sync.md) | **Next:** [Smart Contract Execution](skill-15-smart-contract-exec.md) | **Index:** [README](../README.md)
