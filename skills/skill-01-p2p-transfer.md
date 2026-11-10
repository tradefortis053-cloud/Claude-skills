# Skill 01 — P2P Instant Transfer

**Category A:** Payment Flows & Transactions

> Two avatar nodes passing $250.00 across a glowing instant rail in under four seconds.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `01` |
| **Slug** | `skill-01-p2p-transfer` |
| **Category** | Payment Flows & Transactions |
| **Output file** | `output/skill-01-p2p-transfer.html` |
| **Timeline length** | 16s (16,000 ms) at 1x speed |
| **Accent pair** | `#4F46E5` primary, `#10B981` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #01`
- `Run skill-01-p2p-transfer`
- `Build the p2p instant transfer explainer`
- A natural-language request whose intent matches: _Show a peer-to-peer transfer end to end: recipient selection, rail choice, packet in flight through a compliance checkpoint, and bilateral settlement with updated balances._

### Objective

Show a peer-to-peer transfer end to end: recipient selection, rail choice, packet in flight through a compliance checkpoint, and bilateral settlement with updated balances.

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
| **Scene 1: Recipient Selected** | 0.0s - 3.2s | Maya types @arjun, enters $250.00 and sees the live fee preview read $0.00. |
| **Scene 2: Rail Selection** | 3.2s - 6.6s | Three rails light up. Instant wins on latency, so the engine commits the route. |
| **Scene 3: Packet In Flight** | 6.6s - 11.4s | The payment packet crosses the rail and clears a compliance checkpoint without a hold. |
| **Scene 4: Settlement** | 11.4s - 16.0s | Both balances update and a receipt with a reference ID slides in. |

### Scene 1 — Recipient Selected

**Timing window:** `0.0s - 3.2s`

**Narration subtitle:**

> Maya types @arjun, enters $250.00 and sees the live fee preview read $0.00.

**On-screen elements:** Left avatar node with orbital ring, handle input chip, amount field with tabular-nums counter.

**Animation physics:** Type the handle one glyph at a time on a 40ms stagger; counter eases 0 -> 250 with cubic-bezier(0.16,1,0.3,1); avatar ring pulses once on completion.

### Scene 2 — Rail Selection

**Timing window:** `3.2s - 6.6s`

**Narration subtitle:**

> Three rails light up. Instant wins on latency, so the engine commits the route.

**On-screen elements:** Three stacked rail chips (Instant, Card, Bank) with latency badges, one selected with indigo glow.

**Animation physics:** Stagger chip opacity 0 -> 1 across 180ms; selected chip scales 1 -> 1.03 with a 3px outer glow; badged text flips to 'under 4s'.

### Scene 3 — Packet In Flight

**Timing window:** `6.6s - 11.4s`

**Narration subtitle:**

> The payment packet crosses the rail and clears a compliance checkpoint without a hold.

**On-screen elements:** Cubic bezier rail path, glowing packet with trail, shield checkpoint at the midpoint.

**Animation physics:** Animate stroke-dashoffset from totalLength to 0; place packet with getPointAtLength; shield ring flashes emerald for 240ms at 62% progress.

### Scene 4 — Settlement

**Timing window:** `11.4s - 16.0s`

**Narration subtitle:**

> Both balances update and a receipt with a reference ID slides in.

**On-screen elements:** Two balance chips, receipt card with reference ID, success checkmark stroke.

**Animation physics:** Counters tween to new totals; receipt translates 24px upward with spring damping 24; checkmark draws over 400ms.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Avatar nodes** | Source and destination identities | Two 64px circles, 1.5px stroke, gradient fill at 8% opacity, dashed orbital ring at 40% opacity |
| **Payment rail** | The transfer path | Quadratic bezier, 3px stroke, linecap round, dash pattern 6 8 for the idle state |
| **Packet** | Value in motion | 12px radial-gradient orb plus a 40px blurred halo filter |
| **Compliance checkpoint** | Risk gate on the route | Shield path with 1.5px stroke, sits at bezier midpoint, pulses on clearance |
| **Receipt card** | Settlement proof | Rounded rect 320x180, glass fill, hairline border, mono reference line |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- Route draw uses stroke-dashoffset tied to a normalized 0.18 -> 0.62 slice of the master timeline.
- Packet position derives from the same progress value, so scrubbing backward rewinds it exactly.
- Avatar settle uses a damped spring (stiffness 220, damping 24) instead of a CSS transition.
- Caption crossfade is 200ms opacity with a 20ms upward translate, easing cubic-bezier(0.65,0,0.35,1).

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
  'Maya types @arjun, enters $250.00 and sees the live fee preview read $0.00.',
  'Three rails light up. Instant wins on latency, so the engine commits the route.',
  'The payment packet crosses the rail and clears a compliance checkpoint without a hold.',
  'Both balances update and a receipt with a reference ID slides in.'
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
const TRANSFER = { sender: 'Maya R.', recipient: '@arjun', amount: 250.00, currency: 'USD', fee: 0.00, rail: 'INSTANT', latency: '3.2s', ref: 'TXN-8F42QK' };
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

This skill is the reference implementation for the flagship demo. Keep the controls bar identical to demos/stripe-flow-explainer.html so both feel like one product.

---

**Previous:** _Start of series_ | **Next:** [Card Swipe Authorization](skill-02-card-swipe-auth.md) | **Index:** [README](../README.md)
