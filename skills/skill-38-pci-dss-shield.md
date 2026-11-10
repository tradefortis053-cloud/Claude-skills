# Skill 38 — PCI DSS Shield

**Category D:** Security, Compliance & KYC

> Four defensive layers deflecting hostile traffic while valid carts pass through.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `38` |
| **Slug** | `skill-38-pci-dss-shield` |
| **Category** | Security, Compliance & KYC |
| **Output file** | `output/skill-38-pci-dss-shield.html` |
| **Timeline length** | 17s (17,000 ms) at 1x speed |
| **Accent pair** | `#4F46E5` primary, `#F43F5E` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #38`
- `Run skill-38-pci-dss-shield`
- `Build the pci dss shield explainer`
- A natural-language request whose intent matches: _Explain defense in depth: segmenting cardholder data, layered controls, traffic filtering, and the passing of a compliant request._

### Objective

Explain defense in depth: segmenting cardholder data, layered controls, traffic filtering, and the passing of a compliant request.

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
| **Scene 1: Cardholder Zone** | 0.0s - 4.0s | A protected zone is drawn around the payment service. |
| **Scene 2: Four Layers** | 4.0s - 9.0s | Firewall, WAF, encryption and tokenization layers stack in front of the zone. |
| **Scene 3: Hostile Traffic** | 9.0s - 13.5s | Attack packets hit the layers and are deflected with visible force. |
| **Scene 4: Valid Request** | 13.5s - 17.0s | A legitimate checkout request passes all four layers and succeeds. |

### Scene 1 — Cardholder Zone

**Timing window:** `0.0s - 4.0s`

**Narration subtitle:**

> A protected zone is drawn around the payment service.

**On-screen elements:** Boundary rect with a gradient border, zone label CDE, three inner service nodes.

**Animation physics:** The boundary draws clockwise over 900ms; service nodes fade in after the border closes.

### Scene 2 — Four Layers

**Timing window:** `4.0s - 9.0s`

**Narration subtitle:**

> Firewall, WAF, encryption and tokenization layers stack in front of the zone.

**On-screen elements:** Four vertical layer panels with labels, each with a distinct icon and a 2px separator.

**Animation physics:** Layers slide in from the left at 140ms intervals; each settles with a 4px spring.

### Scene 3 — Hostile Traffic

**Timing window:** `9.0s - 13.5s`

**Narration subtitle:**

> Attack packets hit the layers and are deflected with visible force.

**On-screen elements:** Six rose packets bouncing off layer surfaces, a deflection counter, an alert chip.

**Animation physics:** Packets travel 180ms to the surface and rebound at 40% velocity; each deflect increments the counter.

### Scene 4 — Valid Request

**Timing window:** `13.5s - 17.0s`

**Narration subtitle:**

> A legitimate checkout request passes all four layers and succeeds.

**On-screen elements:** One indigo packet traversing all four layers, a green pass chip, a response 200 in mono.

**Animation physics:** The packet decelerates at each layer by 15% then re-accelerates; a 200 response lands in emerald; hold.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Protected zone** | CDE boundary | Rounded rect with a 2px gradient stroke and a subtle inner glow |
| **Layer panels** | Defense in depth | Four 120x260 panels stacked with 16px gaps and icon glyphs |
| **Attack packets** | Hostile traffic | 6px rose circles with a short tail and a rotation hazard glyph |
| **Pass packet** | Legitimate request | Indigo packet with a check glyph and a soft trail |
| **Deflection counter** | Effectiveness | Mono counter with a small rose accent rule |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- Deflections use a physically plausible rebound: the angle mirrors and speed drops to 40%.
- The valid packet visibly decelerates through each layer, implying inspection cost.
- Only one packet may be green at a time, and only in the final scene.
- Hostile packets never reach the inner zone, at any frame.

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
  'A protected zone is drawn around the payment service.',
  'Firewall, WAF, encryption and tokenization layers stack in front of the zone.',
  'Attack packets hit the layers and are deflected with visible force.',
  'A legitimate checkout request passes all four layers and succeeds.'
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
const PCI = { zone: 'Cardholder Data Environment', layers: ['Edge Firewall', 'WAF', 'Field Encryption', 'Tokenization'], blocked: 6, passed: 1, responseMs: 41, scope: 'PCI DSS v4.0', segmentedFrom: 'corporate network' };
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

Do not claim certification. Say 'designed for PCI DSS scope reduction', which is what a layered diagram can actually support.

---

**Previous:** [Role-Based Access Control](skill-37-role-based-access.md) | **Next:** [Device Fingerprinting](skill-39-device-fingerprinting.md) | **Index:** [README](../README.md)
