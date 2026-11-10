# Skill 32 — Zero-Knowledge Proof

**Category D:** Security, Compliance & KYC

> An age check that proves the claim without ever revealing the birthdate.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `32` |
| **Slug** | `skill-32-zero-knowledge-proof` |
| **Category** | Security, Compliance & KYC |
| **Output file** | `output/skill-32-zero-knowledge-proof.html` |
| **Timeline length** | 19s (19,000 ms) at 1x speed |
| **Accent pair** | `#4F46E5` primary, `#06B6D4` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #32`
- `Run skill-32-zero-knowledge-proof`
- `Build the zero-knowledge proof explainer`
- A natural-language request whose intent matches: _Explain ZK proofs conceptually: a claim, a witness kept private, a proof generated, and a verifier checking the proof rather than the data._

### Objective

Explain ZK proofs conceptually: a claim, a witness kept private, a proof generated, and a verifier checking the proof rather than the data.

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
| **Scene 1: The Claim** | 0.0s - 4.0s | The user asserts 'I am over 18' with no other data exposed. |
| **Scene 2: Witness Stays Private** | 4.0s - 8.5s | The private inputs are hashed locally and never leave the device boundary. |
| **Scene 3: Proof Generated** | 8.5s - 13.5s | A compact proof, not the data, crosses to the verifier. |
| **Scene 4: Verified** | 13.5s - 19.0s | The verifier checks the proof in 12ms and returns true. |

### Scene 1 — The Claim

**Timing window:** `0.0s - 4.0s`

**Narration subtitle:**

> The user asserts 'I am over 18' with no other data exposed.

**On-screen elements:** Claim card, a single boolean row, a hidden witness block shown as dots.

**Animation physics:** The claim types in mono at 28ms per character; the witness block stays visually sealed at 25% opacity.

### Scene 2 — Witness Stays Private

**Timing window:** `4.0s - 8.5s`

**Narration subtitle:**

> The private inputs are hashed locally and never leave the device boundary.

**On-screen elements:** Device boundary line, witness inputs entering a hash function, output commitment 0x7f2a.

**Animation physics:** Inputs travel inward but stop at the boundary; the commitment hash types out and then locks.

### Scene 3 — Proof Generated

**Timing window:** `8.5s - 13.5s`

**Narration subtitle:**

> A compact proof, not the data, crosses to the verifier.

**On-screen elements:** A 288-byte proof chip traversing a tunnel, five constraint gates lighting along the way.

**Animation physics:** Tunnel draws; the chip travels 1200ms; gates light at 20% intervals as the proof passes each.

### Scene 4 — Verified

**Timing window:** `13.5s - 19.0s`

**Narration subtitle:**

> The verifier checks the proof in 12ms and returns true.

**On-screen elements:** Verifier block, check mark, a mono timing figure, a privacy summary line.

**Animation physics:** Check draws over 360ms; timing counts from 0 to 12ms; the privacy line fades in and holds.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Claim card** | Statement to prove | 320x120 with a mono claim string and a boolean result row |
| **Witness block** | Private inputs | Rounded rect filled with a dot pattern to imply redaction |
| **Commitment hash** | Binding value | Mono 12px string with a leading 0x and a lock glyph |
| **Constraint gates** | Circuit checks | Five small rounded squares along the tunnel path |
| **Verifier block** | Checking party | 260x160 with a check glyph and a timing readout |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- The witness must never visually cross the device boundary. That is the whole claim of the skill.
- Gate lighting is sequential and tied to proof position, not to a timer.
- The proof chip is visibly smaller than the data blocks; size conveys succinctness.
- Avoid mathematical notation on screen beyond simple inequalities; the audience is not cryptographers.

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
  'The user asserts \'I am over 18\' with no other data exposed.',
  'The private inputs are hashed locally and never leave the device boundary.',
  'A compact proof, not the data, crosses to the verifier.',
  'The verifier checks the proof in 12ms and returns true.'
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
const ZK = { claim: 'age >= 18', witness: { birthYear: 1994, documentId: 'redacted' }, commitment: '0x7f2a9c41', proofBytes: 288, verifyMs: 12, scheme: 'Groth16', verified: true };
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

Say 'the verifier learns only that the claim is true'. Any stronger guarantee is technically inaccurate.

---

**Previous:** [Biometric KYC](skill-31-biometric-kyc.md) | **Next:** [End-to-End Encryption](skill-33-end-to-end-encryption.md) | **Index:** [README](../README.md)
