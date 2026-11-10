# Skill 39 — Device Fingerprinting

**Category D:** Security, Compliance & KYC

> Twenty browser signals collapsing into one stable hash.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `39` |
| **Slug** | `skill-39-device-fingerprinting` |
| **Category** | Security, Compliance & KYC |
| **Output file** | `output/skill-39-device-fingerprinting.html` |
| **Timeline length** | 16s (16,000 ms) at 1x speed |
| **Accent pair** | `#06B6D4` primary, `#4F46E5` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #39`
- `Run skill-39-device-fingerprinting`
- `Build the device fingerprinting explainer`
- A natural-language request whose intent matches: _Explain device fingerprinting for fraud prevention: signal collection, entropy, hashing, stability over time, and privacy constraints._

### Objective

Explain device fingerprinting for fraud prevention: signal collection, entropy, hashing, stability over time, and privacy constraints.

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
| **Scene 1: Signals Collected** | 0.0s - 4.5s | Twenty attributes enter from around the device frame. |
| **Scene 2: Entropy Weighting** | 4.5s - 8.5s | High-entropy signals glow brighter than generic ones. |
| **Scene 3: Hash Merges** | 8.5s - 12.5s | All signals fold into a single fingerprint hash. |
| **Scene 4: Stability Check** | 12.5s - 16.0s | The same device returns and matches the stored fingerprint with 97% confidence. |

### Scene 1 — Signals Collected

**Timing window:** `0.0s - 4.5s`

**Narration subtitle:**

> Twenty attributes enter from around the device frame.

**On-screen elements:** Phone frame at center, 20 labled signal chips orbiting inward, collection progress ring.

**Animation physics:** Chips orbit at radius 240 and converge inward over 1.6s with 70ms stagger; the progress ring fills to 20/20.

### Scene 2 — Entropy Weighting

**Timing window:** `4.5s - 8.5s`

**Narration subtitle:**

> High-entropy signals glow brighter than generic ones.

**On-screen elements:** Signal chips at varying opacity and size, entropy bars behind three highlighted signals.

**Animation physics:** Entropy bars grow on a 300ms ease; low-entropy chips desaturate to 45% opacity.

### Scene 3 — Hash Merges

**Timing window:** `8.5s - 12.5s`

**Narration subtitle:**

> All signals fold into a single fingerprint hash.

**On-screen elements:** A converging funnel, mono hash string typing out, a 32-character digest.

**Animation physics:** Signals stream into the funnel and vanish; the hash types at 18ms per character and locks with a bracket.

### Scene 4 — Stability Check

**Timing window:** `12.5s - 16.0s`

**Narration subtitle:**

> The same device returns and matches the stored fingerprint with 97% confidence.

**On-screen elements:** Two hash rows side by side with a match badge, a 30-day stability ribbon.

**Animation physics:** The second hash appears as an exact duplicate; the match badge scales in; the stability ribbon draws across the timeline.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Signal chips** | Entropy sources | 20 pills with a label and a 4px leading icon dot |
| **Convergence funnel** | Aggregation | Trapezoid path with 3 internal guides |
| **Hash string** | Identity digest | Mono 14px, 32 characters, grouped in fours |
| **Match badge** | Confidence | Emerald pill with a check glyph and a percentage label |
| **Stability ribbon** | Persistence | Horizontal ribbon with day ticks over a 30-day span |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- Signal chips must not rotate individually; the whole ring rotates and chips translate inward for performance.
- Entropy is visualised with size and opacity, not just colour, so it survives greyscale.
- The two hashes in the stability scene must be character-identical.
- Add a privacy caption: fingerprinting is consent-gated and purpose-limited in regulated markets.

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
  'Twenty attributes enter from around the device frame.',
  'High-entropy signals glow brighter than generic ones.',
  'All signals fold into a single fingerprint hash.',
  'The same device returns and matches the stored fingerprint with 97% confidence.'
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
const FINGERPRINT = { signals: ['userAgent', 'timezone', 'screen', 'canvas', 'webgl', 'fonts', 'audio', 'plugins', 'hardwareConcurrency', 'deviceMemory', 'touchPoints', 'language', 'colorDepth', 'pixelRatio', 'platform', 'doNotTrack', 'storage', 'battery', 'networkType', 'webdriver'], highEntropy: ['canvas', 'webgl', 'fonts'], hash: 'a91f-3c7e-08b4-d52a', confidence: 0.97, stabilityDays: 30 };
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

Always include the consent and purpose-limitation note. Fingerprinting without that framing reads as surveillance.

---

**Previous:** [PCI DSS Shield](skill-38-pci-dss-shield.md) | **Next:** [Instant Card Freeze](skill-40-instant-card-freeze.md) | **Index:** [README](../README.md)
