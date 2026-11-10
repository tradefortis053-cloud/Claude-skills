# Skill 17 — Virtual Card Issuance

**Category B:** Banking Infrastructure & Ledgers

> A card that draws itself out of strokes, then fills with metal.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `17` |
| **Slug** | `skill-17-virtual-card-issuance` |
| **Category** | Banking Infrastructure & Ledgers |
| **Output file** | `output/skill-17-virtual-card-issuance.html` |
| **Timeline length** | 16s (16,000 ms) at 1x speed |
| **Accent pair** | `#4F46E5` primary, `#06B6D4` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #17`
- `Run skill-17-virtual-card-issuance`
- `Build the virtual card issuance explainer`
- A natural-language request whose intent matches: _Show instant virtual card issuance: provisioning request, card number generation in a secure enclave, and activation in the wallet._

### Objective

Show instant virtual card issuance: provisioning request, card number generation in a secure enclave, and activation in the wallet.

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
| **Scene 1: Provisioning Request** | 0.0s - 4.0s | A request fires from the app to the issuer with a spend limit policy. |
| **Scene 2: Wireframe Draw** | 4.0s - 9.0s | The card outline draws itself stroke by stroke. |
| **Scene 3: Metal Fill** | 9.0s - 13.0s | Gradients flood the wireframe and the PAN suffix resolves. |
| **Scene 4: Ready to Spend** | 13.0s - 16.0s | The card lands in the wallet with a success state and expiry. |

### Scene 1 — Provisioning Request

**Timing window:** `0.0s - 4.0s`

**Narration subtitle:**

> A request fires from the app to the issuer with a spend limit policy.

**On-screen elements:** Request card, policy chip reading $2,000 monthly, issuer endpoint mono line.

**Animation physics:** Request line traces left to right in 500ms; the policy chip stamps in with a 1.08 scale overshoot.

### Scene 2 — Wireframe Draw

**Timing window:** `4.0s - 9.0s`

**Narration subtitle:**

> The card outline draws itself stroke by stroke.

**On-screen elements:** Card frame, chip, contactless glyph and number grid drawn via dashoffset.

**Animation physics:** Each of five strokes draws sequentially at 260ms; the number grid reveals as masked dots in a 4x4 layout.

### Scene 3 — Metal Fill

**Timing window:** `9.0s - 13.0s`

**Narration subtitle:**

> Gradients flood the wireframe and the PAN suffix resolves.

**On-screen elements:** Linear gradient fill from slate to indigo with a moving specular highlight.

**Animation physics:** Fill opacity animates 0 -> 1 over 600ms; the specular sweep crosses once at 45deg over 900ms.

### Scene 4 — Ready to Spend

**Timing window:** `13.0s - 16.0s`

**Narration subtitle:**

> The card lands in the wallet with a success state and expiry.

**On-screen elements:** Card in wallet stack, ACTIVE chip, last four digits and expiry.

**Animation physics:** Card translates into the stack; ACTIVE chip crossfades from PENDING; hold the final frame.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Card frame** | Instrument outline | Rounded rect 380x240 with 18px radius and a 2px stroke |
| **Chip** | EMV element | Rounded rect 44x32 with three internal division lines |
| **Contactless glyph** | Tap capability | Four nested arcs rotated 90deg in the card's upper right |
| **PAN mask** | Sensitive data | 16 dots in a 4x4 mono grid; only the last four render as digits |
| **Metal gradient** | Premium fill | Linear gradient 135deg from #1E293B through #4F46E5 to #06B6D4 |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- Stroke drawing must complete before any fill animation begins; overlapping them looks like a render glitch.
- Masked PAN reveals only the last four digits, and that reveal is the emotional payoff.
- Specular sweep runs on a composited gradient transform, never by animating background position on a large element.
- The final card sits at a 6-degree tilt for depth, matching the wallet stack angle in skill 10.

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
  'A request fires from the app to the issuer with a spend limit policy.',
  'The card outline draws itself stroke by stroke.',
  'Gradients flood the wireframe and the PAN suffix resolves.',
  'The card lands in the wallet with a success state and expiry.'
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
const VIRTUAL_CARD = { program: 'Visa Commercial', last4: '4821', expiry: '09/29', spendLimit: 2000, period: 'monthly', status: 'ACTIVE', createdIn: '1.4s' };
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

Never render a full 16-digit PAN, even a fake one. Use the last four only; it is both safer and more realistic.

---

**Previous:** [Automated Reconciliation](skill-16-automated-reconciliation.md) | **Next:** [Open Banking OAuth](skill-18-open-banking-oauth.md) | **Index:** [README](../README.md)
