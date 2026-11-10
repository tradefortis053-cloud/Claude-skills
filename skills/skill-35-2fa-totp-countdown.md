# Skill 35 — 2FA TOTP Countdown

**Category D:** Security, Compliance & KYC

> Six digits that expire in thirty seconds, with the ring closing in.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `35` |
| **Slug** | `skill-35-2fa-totp-countdown` |
| **Category** | Security, Compliance & KYC |
| **Output file** | `output/skill-35-2fa-totp-countdown.html` |
| **Timeline length** | 15s (15,000 ms) at 1x speed |
| **Accent pair** | `#4F46E5` primary, `#F43F5E` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #35`
- `Run skill-35-2fa-totp-countdown`
- `Build the 2fa totp countdown explainer`
- A natural-language request whose intent matches: _Explain TOTP two-factor authentication: shared secret, 30-second time step, HMAC derivation, and verification window tolerance._

### Objective

Explain TOTP two-factor authentication: shared secret, 30-second time step, HMAC derivation, and verification window tolerance.

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
| **Scene 1: Shared Secret** | 0.0s - 3.5s | A secret is provisioned to the phone once, shown as a masked seed and a QR glyph. |
| **Scene 2: Six Digits** | 3.5s - 8.0s | The authenticator computes a code and shows six digits. |
| **Scene 3: Time Step** | 8.0s - 12.0s | The counter reaches zero and a new code rolls in. |
| **Scene 4: Verified** | 12.0s - 15.0s | The code is accepted within the drift window and a session starts. |

### Scene 1 — Shared Secret

**Timing window:** `0.0s - 3.5s`

**Narration subtitle:**

> A secret is provisioned to the phone once, shown as a masked seed and a QR glyph.

**On-screen elements:** Masked secret string in mono, a small QR glyph, an enrolled-device row.

**Animation physics:** The secret reveals two characters at a time then re-masks; the QR glyph fades in at 40% opacity.

### Scene 2 — Six Digits

**Timing window:** `3.5s - 8.0s`

**Narration subtitle:**

> The authenticator computes a code and shows six digits.

**On-screen elements:** Six digit cells at 40px mono, a 30-second countdown ring, a copy button.

**Animation physics:** Digits land one at a time at 60ms intervals; the ring starts full and depletes clockwise with a linear sweep.

### Scene 3 — Time Step

**Timing window:** `8.0s - 12.0s`

**Narration subtitle:**

> The counter reaches zero and a new code rolls in.

**On-screen elements:** Ring empties, digits crossfade to a new set, a mono timestamp of the time step.

**Animation physics:** The ring empties over the full 30s at 1x; when it wraps, digits flip with a 180ms vertical crossfade.

### Scene 4 — Verified

**Timing window:** `12.0s - 15.0s`

**Narration subtitle:**

> The code is accepted within the drift window and a session starts.

**On-screen elements:** Verify field, check glyph, drift window of +/-1 step, session token chip.

**Animation physics:** Check draws in 300ms; the drift window shows a small bracket around the current step; session chip lands last.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Digit cells** | Code display | Six 48x64 rounded rects with 32px mono digits and hairline borders |
| **Countdown ring** | Time step | Circle r=76 with an 8px stroke, stroke-dasharray mapped to seconds remaining |
| **Secret seed** | Provisioning | Masked mono string with 6 visible characters and a copy glyph |
| **Drift bracket** | Verification tolerance | Bracket spanning three time steps, centered on the current one |
| **Session chip** | Outcome | Pill with a truncated token and an expiry label |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- The countdown ring depletes linearly because it represents real time; a bezier here would be dishonest.
- Digit rollover is a vertical crossfade, never a slide that keeps both codes legible at once.
- Drift tolerance is shown as a plus or minus one step bracket, not described only in captions.
- Cap the loop at one or two rollovers so the video does not feel like a waiting screen.

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
  'A secret is provisioned to the phone once, shown as a masked seed and a QR glyph.',
  'The authenticator computes a code and shows six digits.',
  'The counter reaches zero and a new code rolls in.',
  'The code is accepted within the drift window and a session starts.'
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
const TOTP = { digits: 6, stepSeconds: 30, algorithm: 'SHA-1', driftSteps: 1, code: '481 920', previous: '77 4 206', verifiesAt: '98.4%' };
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

Format the code in two groups of three for legibility, and keep the underlying value in a single mono string so copying still works.

---

**Previous:** [AML Fraud Radar](skill-34-aml-fraud-radar.md) | **Next:** [Tokenization Vault](skill-36-tokenization-vault.md) | **Index:** [README](../README.md)
