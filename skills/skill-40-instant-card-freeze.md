# Skill 40 — Instant Card Freeze

**Category D:** Security, Compliance & KYC

> Frost crawling across a virtual card the instant the toggle flips.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `40` |
| **Slug** | `skill-40-instant-card-freeze` |
| **Category** | Security, Compliance & KYC |
| **Output file** | `output/skill-40-instant-card-freeze.html` |
| **Timeline length** | 15s (15,000 ms) at 1x speed |
| **Accent pair** | `#06B6D4` primary, `#4F46E5` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #40`
- `Run skill-40-instant-card-freeze`
- `Build the instant card freeze explainer`
- A natural-language request whose intent matches: _Show card controls: instant freeze, declining authorization attempts, and unfreeze with state sync across channels._

### Objective

Show card controls: instant freeze, declining authorization attempts, and unfreeze with state sync across channels.

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
| **Scene 1: Toggle** | 0.0s - 3.0s | The freeze toggle flips on with a tactile response. |
| **Scene 2: Frost Spreads** | 3.0s - 7.5s | Frost grows across the card from the edges inward. |
| **Scene 3: Attempt Declined** | 7.5s - 11.5s | An authorization attempt hits the frozen card and is declined. |
| **Scene 4: Unfreeze** | 11.5s - 15.0s | The toggle flips back and the frost retreats to reveal an active card. |

### Scene 1 — Toggle

**Timing window:** `0.0s - 3.0s`

**Narration subtitle:**

> The freeze toggle flips on with a tactile response.

**On-screen elements:** Toggle switch at 64x36, a haptic pulse ring, a status label updating.

**Animation physics:** The knob slides 28px on a spring with 6% overshoot; the pulse ring expands once at 300ms.

### Scene 2 — Frost Spreads

**Timing window:** `3.0s - 7.5s`

**Narration subtitle:**

> Frost grows across the card from the edges inward.

**On-screen elements:** Card face with a noise-textured frost overlay, feathered noise crystals along the border, a temperature glyph.

**Animation physics:** Frost mask scales from 0 -> 1 with a texture reveal over 900ms; a 40px blur on the leading edge fades out as it fills.

### Scene 3 — Attempt Declined

**Timing window:** `7.5s - 11.5s`

**Narration subtitle:**

> An authorization attempt hits the frozen card and is declined.

**On-screen elements:** POS attempt card, a rose decline chip with code 62 (restricted card).

**Animation physics:** The attempt chip enters and immediately bounces off with a 3px rebound; the decline code appears in mono.

### Scene 4 — Unfreeze

**Timing window:** `11.5s - 15.0s`

**Narration subtitle:**

> The toggle flips back and the frost retreats to reveal an active card.

**On-screen elements:** Toggle returning, frost retracting, ACTIVE status, a state-synced badge across app and wallet.

**Animation physics:** Frost retreats over 600ms from the center outward; the card face brightens by 4% luminance; the sync badge ticks in.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Virtual card** | Controlled instrument | 380x240 rounded rect with a fine grain overlay and a metallic edge |
| **Frost overlay** | Frozen state | Noise mask with 6 crystal clusters along the perimeter and a 40px feathered edge |
| **Toggle** | Control | Track with 2px inner shadow and a knob with a subtle gradient |
| **Decline chip** | Blocked attempt | Rose pill with a mono code and a cross glyph |
| **Sync badge** | Cross-channel state | Two overlapping device glyphs with a link icon and a check |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- Frost growth must originate at the card edges, not the center; that is what reads as freezing.
- Declines use rose plus a numeric code, never rose alone, so the reason is explicit.
- Unfreeze is faster than freeze to signal restored usability.
- The toggle is interactive and must drive the same state variable used by the frost mask.

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
  'The freeze toggle flips on with a tactile response.',
  'Frost grows across the card from the edges inward.',
  'An authorization attempt hits the frozen card and is declined.',
  'The toggle flips back and the frost retreats to reveal an active card.'
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
const FREEZE = { card: 'Virtual Visa - 4821', status: 'FROZEN', declineCode: '62', reason: 'restricted card', attemptsBlocked: 1, syncChannels: ['App', 'Apple Wallet', 'Google Pay'], unfreezeMs: 600 };
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

Frost is a texture problem, not a gradient problem. Use layered noise with a feathered mask; a simple white radial gradient looks like fog, not ice.

---

**Previous:** [Device Fingerprinting](skill-39-device-fingerprinting.md) | **Next:** [Credit Score Gauge](skill-41-credit-score-gauge.md) | **Index:** [README](../README.md)
