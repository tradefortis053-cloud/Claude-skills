# Skill 04 — QR Scan and Pay

**Category A:** Payment Flows & Transactions

> A scanner frame locks onto a QR code, resolves it, and morphs into a digital receipt.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `04` |
| **Slug** | `skill-04-qr-scan-pay` |
| **Category** | Payment Flows & Transactions |
| **Output file** | `output/skill-04-qr-scan-pay.html` |
| **Timeline length** | 15s (15,000 ms) at 1x speed |
| **Accent pair** | `#06B6D4` primary, `#10B981` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #04`
- `Run skill-04-qr-scan-pay`
- `Build the qr scan and pay explainer`
- A natural-language request whose intent matches: _Show merchant QR acceptance: scan, decode, amount confirmation, authorization, and receipt generation from a single morphing container._

### Objective

Show merchant QR acceptance: scan, decode, amount confirmation, authorization, and receipt generation from a single morphing container.

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
| **Scene 1: Scanner Online** | 0.0s - 3.0s | The viewfinder opens and four corner brackets snap to a QR code. |
| **Scene 2: Decode** | 3.0s - 7.5s | QR modules resolve into a merchant identity and an amount. |
| **Scene 3: Confirm and Authorize** | 7.5s - 11.5s | The user confirms and the payment clears in one pass. |
| **Scene 4: Receipt Morph** | 11.5s - 15.0s | The scanner frame morphs into a receipt with a scannable reference. |

### Scene 1 — Scanner Online

**Timing window:** `0.0s - 3.0s`

**Narration subtitle:**

> The viewfinder opens and four corner brackets snap to a QR code.

**On-screen elements:** Phone frame, dimmed camera plate, four L-shaped brackets, laser sweep line.

**Animation physics:** Brackets translate inward 16px on an 80ms stagger; the sweep line loops vertically at 1.2s per pass with an ease-in-out.

### Scene 2 — Decode

**Timing window:** `3.0s - 7.5s`

**Narration subtitle:**

> QR modules resolve into a merchant identity and an amount.

**On-screen elements:** 25x25 module grid, resolving into a merchant chip and a $18.50 amount row.

**Animation physics:** Modules fade out in a diagonal wave from 0 -> 1.2s; merchant text types in mono at 24ms per character.

### Scene 3 — Confirm and Authorize

**Timing window:** `7.5s - 11.5s`

**Narration subtitle:**

> The user confirms and the payment clears in one pass.

**On-screen elements:** Confirm sheet, biometric glyph, three-step authorization ticks.

**Animation physics:** Sheet translates upward 120px on a spring; ticks land at 120ms intervals; button label swaps CONFIRM -> PAID.

### Scene 4 — Receipt Morph

**Timing window:** `11.5s - 15.0s`

**Narration subtitle:**

> The scanner frame morphs into a receipt with a scannable reference.

**On-screen elements:** Same rounded rect morphing from camera aspect to receipt aspect, itemized lines.

**Animation physics:** Animate width, height and corner radius together over 600ms; module grid cross-fades to receipt text.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Viewfinder brackets** | Scan target | Four L-paths with 3px stroke and rounded caps at the four corners |
| **Laser sweep** | Scanning motion | Gradient-filled rect 2px tall with a soft blur, clipped to the viewfinder |
| **QR matrix** | Encoded payload | Deterministic 25x25 rect grid generated from a seeded PRNG, not a static image |
| **Receipt** | Post-payment artifact | Rounded rect with a mono line stack and a reference hash |
| **Morph container** | Continuity device | One SVG rect whose x, y, width, height and rx are all interpolated |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- Generate QR modules once on load and toggle opacity per module; never rewrite the DOM during playback.
- The morph interpolates geometry with cubic-bezier(0.16,1,0.3,1) to keep the shape legible mid-flight.
- Laser sweep is ambient and uses linear timing, gated by scene progress so it stops when paused.
- Success state uses emerald plus a 240ms halo, not a colour flash, to avoid looking like an error.

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
  'The viewfinder opens and four corner brackets snap to a QR code.',
  'QR modules resolve into a merchant identity and an amount.',
  'The user confirms and the payment clears in one pass.',
  'The scanner frame morphs into a receipt with a scannable reference.'
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
const QR_PAY = { merchant: 'Blue Tokai Coffee', amount: 18.50, currency: 'INR', method: 'UPI_QR', vpa: 'bluetokai@okhdfcbank', ref: 'QR-4M8X2P', settledIn: '1.8s' };
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

Use a seeded PRNG for the QR pattern so every render, replay and screenshot produces the identical matrix.

---

**Previous:** [Split Bill](skill-03-split-bill.md) | **Next:** [Cross-Border FX Transfer](skill-05-cross-border-fx.md) | **Index:** [README](../README.md)
