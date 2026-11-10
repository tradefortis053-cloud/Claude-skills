# Skill 33 — End-to-End Encryption

**Category D:** Security, Compliance & KYC

> A readable amount that turns to noise in transit and reassembles at the destination.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `33` |
| **Slug** | `skill-33-end-to-end-encryption` |
| **Category** | Security, Compliance & KYC |
| **Output file** | `output/skill-33-end-to-end-encryption.html` |
| **Timeline length** | 17s (17,000 ms) at 1x speed |
| **Accent pair** | `#06B6D4` primary, `#4F46E5` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #33`
- `Run skill-33-end-to-end-encryption`
- `Build the end-to-end encryption explainer`
- A natural-language request whose intent matches: _Show E2E encryption: key exchange, plaintext to ciphertext at the sender, cipher transport, and decryption at the receiver._

### Objective

Show E2E encryption: key exchange, plaintext to ciphertext at the sender, cipher transport, and decryption at the receiver.

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
| **Scene 1: Plaintext** | 0.0s - 3.5s | The sender composes a transfer of $2,400 to a known beneficiary. |
| **Scene 2: Key Exchange** | 3.5s - 7.5s | Ephemeral keys cross the channel and a shared secret is derived. |
| **Scene 3: Ciphertext** | 7.5s - 12.5s | The payload scrambles into blocks mid-flight. |
| **Scene 4: Decrypted** | 12.5s - 17.0s | The receiver decrypts and the original amount reappears unchanged. |

### Scene 1 — Plaintext

**Timing window:** `0.0s - 3.5s`

**Narration subtitle:**

> The sender composes a transfer of $2,400 to a known beneficiary.

**On-screen elements:** Composer card with a readable amount and memo line, a padlock at 40% opacity.

**Animation physics:** The padlock lifts and fills as the scene ends; amount text stays perfectly legible until encryption begins.

### Scene 2 — Key Exchange

**Timing window:** `3.5s - 7.5s`

**Narration subtitle:**

> Ephemeral keys cross the channel and a shared secret is derived.

**On-screen elements:** Two key glyphs traveling toward each other, a shared-secret node in the middle, a derivation formula chip.

**Animation physics:** Key glyphs meet at center with a 180ms ease; the shared node pulses once and shows a truncated fingerprint.

### Scene 3 — Ciphertext

**Timing window:** `7.5s - 12.5s`

**Narration subtitle:**

> The payload scrambles into blocks mid-flight.

**On-screen elements:** Paylaod orb transforming into a 3x4 block grid of hex characters, an intermediary node unable to read it.

**Animation physics:** Characters resolve per block at 40ms intervals; the intermediary node shows a blind-eye glyph and a 'no key' label.

### Scene 4 — Decrypted

**Timing window:** `12.5s - 17.0s`

**Narration subtitle:**

> The receiver decrypts and the original amount reappears unchanged.

**On-screen elements:** Receiver card, the same amount restored, a checksum line confirming integrity.

**Animation physics:** Hex blocks resolve back into text; a checksum row crossfades to emerald; the padlock closes and holds.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Composer card** | Sender surface | 360x160 with an amount field, memo line and a send button |
| **Key glyphs** | Cryptographic keys | Two key silhouettes with 6-tooth bit patterns, mirrored |
| **Cipher blocks** | Encrypted payload | 3x4 grid of 28x28 rounded rects with mono hex pairs |
| **Intermediary node** | Untrusted hop | Circle with a blind-eye glyph and a muted border |
| **Integrity checksum** | Tamper evidence | Mono line with a check glyph and a 6-character digest |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- The scrambled state must use the same character count as the plaintext, so the viewer senses a transformation rather than a replacement.
- Keys meet at center with mirrored easing so neither side appears dominant.
- The intermediary hop gets a visible 'no key' state; silence here implies the middle can read traffic.
- Decryption lands on exactly the original amount, digit for digit.

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
  'The sender composes a transfer of $2,400 to a known beneficiary.',
  'Ephemeral keys cross the channel and a shared secret is derived.',
  'The payload scrambles into blocks mid-flight.',
  'The receiver decrypts and the original amount reappears unchanged.'
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
const E2E = { sender: 'Maya R.', receiver: 'Arjun S.', amount: 2400, currency: 'USD', cipher: 'AES-256-GCM', keyExchange: 'X25519', intermediaryHops: 1, checksum: '9f3ad1', decryptMs: 2 };
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

This skill pairs well with 13 and 36 for a security series. Keep the cipher suite labels in the same mono style across all three.

---

**Previous:** [Zero-Knowledge Proof](skill-32-zero-knowledge-proof.md) | **Next:** [AML Fraud Radar](skill-34-aml-fraud-radar.md) | **Index:** [README](../README.md)
