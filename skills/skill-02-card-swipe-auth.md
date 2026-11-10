# Skill 02 — Card Swipe Authorization

**Category A:** Payment Flows & Transactions

> An isometric tap to a POS terminal, then an issuer decision in 900 milliseconds.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `02` |
| **Slug** | `skill-02-card-swipe-auth` |
| **Category** | Payment Flows & Transactions |
| **Output file** | `output/skill-02-card-swipe-auth.html` |
| **Timeline length** | 18s (18,000 ms) at 1x speed |
| **Accent pair** | `#4F46E5` primary, `#10B981` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #02`
- `Run skill-02-card-swipe-auth`
- `Build the card swipe authorization explainer`
- A natural-language request whose intent matches: _Visualize the four-party card authorization model: cardholder, merchant terminal, acquirer, and issuer rules engine, ending in an approval with an auth code._

### Objective

Visualize the four-party card authorization model: cardholder, merchant terminal, acquirer, and issuer rules engine, ending in an approval with an auth code.

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
| **Scene 1: Tap the Terminal** | 0.0s - 4.0s | The card hovers into the reader and the terminal wakes up. |
| **Scene 2: Authorization Request** | 4.0s - 8.5s | The terminal packages the cryptogram and routes it to the issuer. |
| **Scene 3: Issuer Rules Engine** | 8.5s - 13.5s | Three checks run in parallel: cryptogram, velocity, available balance. |
| **Scene 4: Approved** | 13.5s - 18.0s | The checkmark draws, the auth code prints and the card lifts away. |

### Scene 1 — Tap the Terminal

**Timing window:** `0.0s - 4.0s`

**Narration subtitle:**

> The card hovers into the reader and the terminal wakes up.

**On-screen elements:** Isometric card at rotate(-18deg, skewY(8deg)), POS body, NFC glyph, $42.80 order chip.

**Animation physics:** Card translates 90px along a diagonal with a 600ms cubic-bezier(0.16,1,0.3,1); on contact the terminal LED turns indigo and a ripple expands.

### Scene 2 — Authorization Request

**Timing window:** `4.0s - 8.5s`

**Narration subtitle:**

> The terminal packages the cryptogram and routes it to the issuer.

**On-screen elements:** Request envelope traveling a 3-hop rail: terminal -> acquirer -> issuer.

**Animation physics:** Hop markers light sequentially at 25%, 55% and 85% of the scene; the envelope leaves a 320ms fading trail.

### Scene 3 — Issuer Rules Engine

**Timing window:** `8.5s - 13.5s`

**Narration subtitle:**

> Three checks run in parallel: cryptogram, velocity, available balance.

**On-screen elements:** Vertical check stack with 28px status dots and mono labels.

**Animation physics:** Each row resolves on a staggered 260ms delay; a dot fills emerald and the label swaps from PENDING to PASS.

### Scene 4 — Approved

**Timing window:** `13.5s - 18.0s`

**Narration subtitle:**

> The checkmark draws, the auth code prints and the card lifts away.

**On-screen elements:** Stroke-drawn checkmark, printed receipt sliding out of the POS, auth code in mono.

**Animation physics:** Checkmark path traces over 420ms; receipt slides 64px on a spring; approval flash decays over 500ms.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Isometric card** | The payment instrument | Rounded rect 220x140 with a gradient face, a chip rect, and two hairline stripes |
| **POS terminal** | Merchant acceptance point | Rounded rect 180x220, 12px corner radius, screen with a 3-row mono log |
| **Routing rail** | Four-party authorization path | Polyline with rounded joins plus three circular hop nodes |
| **Rules engine stack** | Issuer decisioning | Three 300x44 pills with a leading status dot and mono value column |
| **Success checkmark** | Approval signal | Two-segment path totalling about 120 units, stroke-dasharray animated to zero |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- Contact ripple expands 0 -> 2.4x scale while opacity falls 0.5 -> 0 over 700ms.
- Hop lighting is driven by progress bands, never by chained setTimeout calls.
- The rules stack uses an 80ms stagger per row and cubic-bezier(0.65,0,0.35,1).
- Approval flash is a radial gradient whose opacity decays linearly against the last 3 seconds only.

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
  'The card hovers into the reader and the terminal wakes up.',
  'The terminal packages the cryptogram and routes it to the issuer.',
  'Three checks run in parallel: cryptogram, velocity, available balance.',
  'The checkmark draws, the auth code prints and the card lifts away.'
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
const AUTH = { merchant: 'Kettle & Co.', amount: 42.80, currency: 'USD', entry: 'CONTACTLESS', acquirer: 'NORTH_ACQ', issuer: 'MERIDIAN_BANK', authCode: 'A7K2Q9', latencyMs: 920 };
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

Keep the isometric projection consistent across all scenes. Use one SVG viewBox and transform the whole group rather than re-projecting individual shapes.

---

**Previous:** [P2P Instant Transfer](skill-01-p2p-transfer.md) | **Next:** [Split Bill](skill-03-split-bill.md) | **Index:** [README](../README.md)
