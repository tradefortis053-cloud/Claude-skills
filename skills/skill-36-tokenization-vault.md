# Skill 36 — Tokenization Vault

**Category D:** Security, Compliance & KYC

> A 16-digit PAN going in and a harmless token coming out.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `36` |
| **Slug** | `skill-36-tokenization-vault` |
| **Category** | Security, Compliance & KYC |
| **Output file** | `output/skill-36-tokenization-vault.html` |
| **Timeline length** | 16s (16,000 ms) at 1x speed |
| **Accent pair** | `#4F46E5` primary, `#06B6D4` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #36`
- `Run skill-36-tokenization-vault`
- `Build the tokenization vault explainer`
- A natural-language request whose intent matches: _Show card tokenization: PAN capture inside a secure boundary, token generation, and downstream use where the real PAN never appears._

### Objective

Show card tokenization: PAN capture inside a secure boundary, token generation, and downstream use where the real PAN never appears.

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
| **Scene 1: PAN Entry** | 0.0s - 3.5s | The card number is entered inside a hardened input field. |
| **Scene 2: Into the Vault** | 3.5s - 7.5s | The PAN travels into an isolated vault that never returns it. |
| **Scene 3: Token Generated** | 7.5s - 11.5s | A format-preserving token emerges with the same shape but no value. |
| **Scene 4: Token in Use** | 11.5s - 16.0s | A merchant charges the token and never touches the PAN. |

### Scene 1 — PAN Entry

**Timing window:** `0.0s - 3.5s`

**Narration subtitle:**

> The card number is entered inside a hardened input field.

**On-screen elements:** Input field with a shield boundary, digits masked after the fourth, a keypad hint.

**Animation physics:** Digits reveal for 300ms then mask; the shield boundary draws around the field at 60% opacity.

### Scene 2 — Into the Vault

**Timing window:** `3.5s - 7.5s`

**Narration subtitle:**

> The PAN travels into an isolated vault that never returns it.

**On-screen elements:** Vault door with concentric rings, one-way ingress arrow, a strict no-egress marker.

**Animation physics:** The ingress arrow draws once, then the vault closes with a 400ms rotation; the no-egress marker pulses once.

### Scene 3 — Token Generated

**Timing window:** `7.5s - 11.5s`

**Narration subtitle:**

> A format-preserving token emerges with the same shape but no value.

**On-screen elements:** Token string 4127 88xx xxxx 3021 in mono, format-preserving badge, scope chip.

**Animation physics:** Token characters type in at 30ms; the suffix 3021 locks with a 1.06 scale overshoot; the badge fades in.

### Scene 4 — Token in Use

**Timing window:** `11.5s - 16.0s`

**Narration subtitle:**

> A merchant charges the token and never touches the PAN.

**On-screen elements:** Merchant checkout card using the token, an authorization approval, a PAN-never-seen note.

**Animation physics:** Checkout card slides in; approval check draws; the closing note fades in over 400ms with a lock glyph.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Hardened input** | Capture surface | 320x56 field with a 1.5px shield-styled border and a lock glyph |
| **Vault** | Secure boundary | Concentric rings with a central keyhole and a sealed hatch |
| **Token string** | Substitute value | Mono 20px with grouped 4-character blocks and dimmed middle groups |
| **Merchant card** | Downstream use | 300x160 checkout panel with a token label and an approve button |
| **No-egress marker** | Vault property | Circle with a diagonal slash over an arrow pointing outward |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- The PAN must never be rendered in full, at any frame, in any state. Mask from the fifth digit onward.
- The vault closes before the token appears; concurrent motion implies the PAN became the token, which is wrong.
- The token uses format-preserving grouping so it reads as a card number without being one.
- One-way ingress and no-egress markers appear in the same scene; together they tell the whole story.

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
  'The card number is entered inside a hardened input field.',
  'The PAN travels into an isolated vault that never returns it.',
  'A format-preserving token emerges with the same shape but no value.',
  'A merchant charges the token and never touches the PAN.'
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
const TOKEN = { panMasked: '4127 88** **** 3021', token: 'tk_9f2a41c8b7e3', formatPreserving: true, scope: 'merchant: kettles-co', network: 'Visa Token Service', reuse: 'single merchant' };
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

Use a clearly invalid test BIN such as 4127 88 with masked middle groups. Never use a plausible live-looking full PAN.

---

**Previous:** [2FA TOTP Countdown](skill-35-2fa-totp-countdown.md) | **Next:** [Role-Based Access Control](skill-37-role-based-access.md) | **Index:** [README](../README.md)
