# Skill 31 — Biometric KYC

**Category D:** Security, Compliance & KYC

> A face mesh that scans, liveness-checks and becomes a verified badge.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `31` |
| **Slug** | `skill-31-biometric-kyc` |
| **Category** | Security, Compliance & KYC |
| **Output file** | `output/skill-31-biometric-kyc.html` |
| **Timeline length** | 18s (18,000 ms) at 1x speed |
| **Accent pair** | `#4F46E5` primary, `#10B981` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #31`
- `Run skill-31-biometric-kyc`
- `Build the biometric kyc explainer`
- A natural-language request whose intent matches: _Show identity verification: document capture, biometric liveness detection, face match scoring, and verification issuance._

### Objective

Show identity verification: document capture, biometric liveness detection, face match scoring, and verification issuance.

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
| **Scene 1: Document Capture** | 0.0s - 4.5s | A passport is framed, deskewed and read by OCR. |
| **Scene 2: Liveness Check** | 4.5s - 9.5s | The camera prompts a blink and a head turn, then passes liveness. |
| **Scene 3: Face Match** | 9.5s - 14.0s | The selfie and document photo are compared with a 99.2% confidence score. |
| **Scene 4: Verified Badge** | 14.0s - 18.0s | The mesh collapses into a verified badge with an audit trail entry. |

### Scene 1 — Document Capture

**Timing window:** `0.0s - 4.5s`

**Narration subtitle:**

> A passport is framed, deskewed and read by OCR.

**On-screen elements:** Document in a viewfinder with corner brackets, detected field boxes appearing.

**Animation physics:** Brackets snap inward; field boxes draw one at a time at 120ms; OCR text types into mono fields.

### Scene 2 — Liveness Check

**Timing window:** `4.5s - 9.5s`

**Narration subtitle:**

> The camera prompts a blink and a head turn, then passes liveness.

**On-screen elements:** Face silhouette with a 480-point mesh, prompt chips, a liveness progress ring.

**Animation physics:** Mesh vertices fade in on a radial wave over 900ms; prompt chips swap at 1.4s intervals; the ring completes in emerald.

### Scene 3 — Face Match

**Timing window:** `9.5s - 14.0s`

**Narration subtitle:**

> The selfie and document photo are compared with a 99.2% confidence score.

**On-screen elements:** Side-by-side faces, a matching bracket, a confidence arc at 99.2%.

**Animation physics:** The confidence arc sweeps 0 -> 99.2% over 700ms while the number counts in parallel.

### Scene 4 — Verified Badge

**Timing window:** `14.0s - 18.0s`

**Narration subtitle:**

> The mesh collapses into a verified badge with an audit trail entry.

**On-screen elements:** Badge with a check glyph, KYC status VERIFIED, audit trail timestamp.

**Animation physics:** Mesh vertices converge to the badge center over 500ms; the badge pops with a 240ms spring; audit line fades in last.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Document frame** | Capture target | Rounded rect with four corner brackets and a slight perspective skew |
| **Face mesh** | Biometric landmarks | Grid of 480 small dots sampled on an elliptical face surface, 1px radius |
| **Liveness ring** | Liveness progress | Circle r=90 with a 6px stroke and rounded dash caps |
| **Confidence arc** | Match score | 270-degree arc with a gradient from cyan to emerald |
| **Verified badge** | Outcome | Shield path 96px tall with a check glyph and an outer glow |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- Generate mesh vertices once and animate opacity only; moving 480 nodes individually drops frames on mid-range hardware.
- Liveness prompts must change in a fixed order so the sequence is auditable.
- Confidence is displayed to one decimal and never rounds to 100%.
- The mesh-to-badge morph should fade the mesh out while the badge scales in; do not attempt per-vertex interpolation.

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
  'A passport is framed, deskewed and read by OCR.',
  'The camera prompts a blink and a head turn, then passes liveness.',
  'The selfie and document photo are compared with a 99.2% confidence score.',
  'The mesh collapses into a verified badge with an audit trail entry.'
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
const KYC = { document: 'Passport', country: 'IND', ocrFields: ['Name', 'DOB', 'Document No.'], liveness: 'passed', prompts: ['Blink', 'Turn left', 'Look ahead'], faceMatch: 0.992, status: 'VERIFIED', auditId: 'KYC-9F31C', reviewMs: 1400 };
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

Never fabricate a real-looking passport number or a photoreal face. Use abstract silhouettes and masked fields.

---

**Previous:** [Dollar-Cost Averaging](skill-30-dca-simulator.md) | **Next:** [Zero-Knowledge Proof](skill-32-zero-knowledge-proof.md) | **Index:** [README](../README.md)
