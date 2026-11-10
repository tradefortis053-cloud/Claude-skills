# Skill 54 — Carbon Offset Checkout

**Category E:** B2B SaaS, Lending & Credit

> A checkout that measures grams of CO2 and grows a tree on the receipt.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `54` |
| **Slug** | `skill-54-carbon-offset-checkout` |
| **Category** | B2B SaaS, Lending & Credit |
| **Output file** | `output/skill-54-carbon-offset-checkout.html` |
| **Timeline length** | 16s (16,000 ms) at 1x speed |
| **Accent pair** | `#10B981` primary, `#06B6D4` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #54`
- `Run skill-54-carbon-offset-checkout`
- `Build the carbon offset checkout explainer`
- A natural-language request whose intent matches: _Show carbon-aware checkout: footprint estimation, offset pricing, contribution capture and verification record._

### Objective

Show carbon-aware checkout: footprint estimation, offset pricing, contribution capture and verification record.

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
| **Scene 1: Order Summary** | 0.0s - 3.5s | A $96 order is itemized and a footprint line appears. |
| **Scene 2: Footprint Estimate** | 3.5s - 8.0s | Shipping, packaging and product emissions break down. |
| **Scene 3: Offset Toggle** | 8.0s - 12.5s | A $0.71 offset covers 14.2 kg at $50 per tonne. |
| **Scene 4: Receipt and Tree** | 12.5s - 16.0s | The receipt records the contribution and a tree vector draws. |

### Scene 1 — Order Summary

**Timing window:** `0.0s - 3.5s`

**Narration subtitle:**

> A $96 order is itemized and a footprint line appears.

**On-screen elements:** Order card with three items, a footprint row in mono grams of CO2.

**Animation physics:** The footprint figure counts from 0 to 14.2 kg; the row gains a leaf glyph that fades in at completion.

### Scene 2 — Footprint Estimate

**Timing window:** `3.5s - 8.0s`

**Narration subtitle:**

> Shipping, packaging and product emissions break down.

**On-screen elements:** A three-segment horizontal bar labeled SHIPPING, PACKAGING, PRODUCT with a total.

**Animation physics:** Segments grow left to right at 120ms offsets; a total rule draws beneath and the grams count in.

### Scene 3 — Offset Toggle

**Timing window:** `8.0s - 12.5s`

**Narration subtitle:**

> A $0.71 offset covers 14.2 kg at $50 per tonne.

**On-screen elements:** Offset toggle with a price chip, a per-tonne rate note, and a contribution summary.

**Animation physics:** The toggle flips with a 6% knob overshoot; the price chip counts in; the rate note fades in second.

### Scene 4 — Receipt and Tree

**Timing window:** `12.5s - 16.0s`

**Narration subtitle:**

> The receipt records the contribution and a tree vector draws.

**On-screen elements:** Receipt card with an offset line, a tree glyph drawing via strokes, a registry reference.

**Animation physics:** The tree trunk draws first, then branches at 60ms stagger, then leaves fill at 12% opacity; the registry ID types last.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Footprint bar** | Emissions breakdown | Three stacked segments with a shared baseline and mono kg labels |
| **Leaf glyph** | Carbon marker | Simple leaf path with a single midrib stroke |
| **Offset toggle** | Opt-in | Compact track with a price chip anchored to the right |
| **Tree** | Offset symbol | Trunk plus 7 branches drawn with stroke-dasharray, 3 leaf clusters filled |
| **Registry reference** | Verification | Mono string with a verified badge and a project name |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- Fee arithmetic must hold: 14.2 kg at $50 per tonne equals $0.71, rounded consistently.
- The tree draws from trunk outward; leaves appear only after their branch completes.
- Offset pricing is transparent per tonne; opaque 'green fees' are the failure mode this skill avoids.
- Colours stay in the emerald-cyan family; avoid using green for both offsets and success states in the same scene.

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
  'A $96 order is itemized and a footprint line appears.',
  'Shipping, packaging and product emissions break down.',
  'A $0.71 offset covers 14.2 kg at $50 per tonne.',
  'The receipt records the contribution and a tree vector draws.'
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
const CARBON = { order: 96.00, items: 3, footprintKg: 14.2, breakdown: { shipping: 6.4, packaging: 2.1, product: 5.7 }, ratePerTonne: 50, offsetCost: 0.71, project: 'Verified Reforestation - Western Ghats', registryId: 'VCS-2291-4471' };
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

Rounding is the trap here: 0.0142 tonnes x $50 is $0.71, and reviewers will check. Compute the fee from the same rounded footprint shown on screen.

---

**Previous:** [Embedded Insurance](skill-53-embedded-insurance.md) | **Next:** [AI Financial Copilot](skill-55-ai-financial-copilot.md) | **Index:** [README](../README.md)
