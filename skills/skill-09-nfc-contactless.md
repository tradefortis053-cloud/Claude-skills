# Skill 09 — NFC Contactless Tap

**Category A:** Payment Flows & Transactions

> Concentric radio waves bridging a phone and a reader in 400 milliseconds.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `09` |
| **Slug** | `skill-09-nfc-contactless` |
| **Category** | Payment Flows & Transactions |
| **Output file** | `output/skill-09-nfc-contactless.html` |
| **Timeline length** | 14s (14,000 ms) at 1x speed |
| **Accent pair** | `#06B6D4` primary, `#10B981` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #09`
- `Run skill-09-nfc-contactless`
- `Build the nfc contactless tap explainer`
- A natural-language request whose intent matches: _Visualize near-field communication: field generation, inductive coupling at 13.56 MHz, tokenized data exchange, and instant approval._

### Objective

Visualize near-field communication: field generation, inductive coupling at 13.56 MHz, tokenized data exchange, and instant approval.

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
| **Scene 1: Field On** | 0.0s - 3.5s | The phone wakes and emits a 4cm near field. |
| **Scene 2: Proximity** | 3.5s - 7.0s | The reader enters the field and the two devices couple. |
| **Scene 3: Token Exchange** | 7.0s - 11.0s | A device token, never the PAN, crosses the gap. |
| **Scene 4: Tap Complete** | 11.0s - 14.0s | The reader beeps, the terminal shows $7.20 paid and the waves retract. |

### Scene 1 — Field On

**Timing window:** `0.0s - 3.5s`

**Narration subtitle:**

> The phone wakes and emits a 4cm near field.

**On-screen elements:** Phone silhouette, three concentric arc groups expanding from the antenna region.

**Animation physics:** Each wave group expands 0 -> 1.6x scale while opacity falls 0.6 -> 0 over 900ms, staggered 160ms.

### Scene 2 — Proximity

**Timing window:** `3.5s - 7.0s`

**Narration subtitle:**

> The reader enters the field and the two devices couple.

**On-screen elements:** Reader rectangle sliding in, matching wave arcs, a 4cm distance indicator.

**Animation physics:** Reader translates 120px over 700ms; the distance ruler collapses from 4cm to 0 with a mono label ticking down.

### Scene 3 — Token Exchange

**Timing window:** `7.0s - 11.0s`

**Narration subtitle:**

> A device token, never the PAN, crosses the gap.

**On-screen elements:** Small packet labeled TOKEN-9F2A traversing the gap with a shield glyph.

**Animation physics:** Packet travels 60px in 300ms; shield pulses once on arrival; a mono caption confirms PAN never left the device.

### Scene 4 — Tap Complete

**Timing window:** `11.0s - 14.0s`

**Narration subtitle:**

> The reader beeps, the terminal shows $7.20 paid and the waves retract.

**On-screen elements:** Green reader LED, amount chip, retracting wave groups.

**Animation physics:** Waves reverse their expansion; chip lands with a 1.06 scale overshoot over 240ms.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Near-field arcs** | RF energy | Three concentric partial arcs at 0.3, 0.6 and 0.9 radii, rounded caps |
| **Phone** | Initiator device | Rounded rect 90x180 with a notch and an antenna region highlighted |
| **Card reader** | Acceptor device | Rounded rect 140x170 with a screen and a status LED circle |
| **Token packet** | Secured payload | 16x16 rounded square with a mono label and a trailing gradient |
| **Distance ruler** | Physical proximity | Horizontal line with two end caps and a mono measurement label |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- Wave stagger is 160ms with 900ms life; three groups are enough, more reads as noise.
- All wave animation stops precisely when playback pauses.
- The distance ruler uses an ease-out curve so the final centimetres feel quick.
- Keep the frequency label 13.56 MHz visible in the scene caption for technical credibility.

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
  'The phone wakes and emits a 4cm near field.',
  'The reader enters the field and the two devices couple.',
  'A device token, never the PAN, crosses the gap.',
  'The reader beeps, the terminal shows $7.20 paid and the waves retract.'
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
const NFC = { device: 'iPhone 15', reader: 'Verifone P400', amount: 7.20, currency: 'EUR', frequency: '13.56 MHz', rangeCm: 4, token: 'TOKEN-9F2A', latencyMs: 400 };
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

Do not draw a literal PAN in this skill. The entire point is that the token crosses the gap instead.

---

**Previous:** [Refund Reversal](skill-08-refund-reversal.md) | **Next:** [Multi-Currency Wallet](skill-10-multi-currency-wallet.md) | **Index:** [README](../README.md)
