# Skill 50 — Customs and Trade Finance

**Category E:** B2B SaaS, Lending & Credit

> A cargo ship unlocking a letter of credit at each supply-chain checkpoint.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `50` |
| **Slug** | `skill-50-customs-trade-finance` |
| **Category** | B2B SaaS, Lending & Credit |
| **Output file** | `output/skill-50-customs-trade-finance.html` |
| **Timeline length** | 19s (19,000 ms) at 1x speed |
| **Accent pair** | `#06B6D4` primary, `#4F46E5` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #50`
- `Run skill-50-customs-trade-finance`
- `Build the customs and trade finance explainer`
- A natural-language request whose intent matches: _Show trade finance documentation: letter of credit issuance, checkpoint-based document release, and payment on bill of lading._

### Objective

Show trade finance documentation: letter of credit issuance, checkpoint-based document release, and payment on bill of lading.

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
| **Scene 1: Letter of Credit** | 0.0s - 4.5s | An importer's bank issues an LC for $480,000 to a supplier abroad. |
| **Scene 2: Voyage** | 4.5s - 10.5s | A ship travels a route across four checkpoints. |
| **Scene 3: Document Release** | 10.5s - 15.5s | Each checkpoint unlocks one required document. |
| **Scene 4: Payment Released** | 15.5s - 19.0s | All documents verified means funds release to the supplier. |

### Scene 1 — Letter of Credit

**Timing window:** `0.0s - 4.5s`

**Narration subtitle:**

> An importer's bank issues an LC for $480,000 to a supplier abroad.

**On-screen elements:** LC document card with terms, issuing bank and beneficiary, a seal glyph.

**Animation physics:** The document slides in and the seal stamps with a 1.1 scale overshoot; the amount counts in.

### Scene 2 — Voyage

**Timing window:** `4.5s - 10.5s`

**Narration subtitle:**

> A ship travels a route across four checkpoints.

**On-screen elements:** Route polyline across a simplified map, ship vector, four checkpoint nodes with labels.

**Animation physics:** The ship moves along the path via getPointAtLength; the route draws ahead by 8% so it never looks like the ship is ahead of the path.

### Scene 3 — Document Release

**Timing window:** `10.5s - 15.5s`

**Narration subtitle:**

> Each checkpoint unlocks one required document.

**On-screen elements:** Four document chips unlocking sequentially: invoice, packing list, bill of lading, certificate of origin.

**Animation physics:** Each chip flips from locked to released with a 180ms crossfade; the lock glyph rotates open 90deg.

### Scene 4 — Payment Released

**Timing window:** `15.5s - 19.0s`

**Narration subtitle:**

> All documents verified means funds release to the supplier.

**On-screen elements:** Full document set, verification badge, payment rail to the supplier, a final LC status CLOSED.

**Animation physics:** The verification badge draws; the payment rail travels the reverse of the voyage path; status flips to CLOSED and holds.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Map plate** | Trade geography | Simplified landmass paths at 12% fill with a dotted route overlay |
| **Ship** | Cargo movement | Top-down vessel outline 44x20 with a wake path trailing behind |
| **Checkpoint nodes** | Customs stages | 24px circles with a flag glyph and a mono stage label |
| **Document chips** | Required paperwork | 120x40 cards with a lock glyph and a document-type label |
| **Payment rail** | Settlement | Gradient path from the issuing bank to the supplier |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- The ship leads the path draw by exactly 8%, which reads as motion along a route rather than a race.
- Documents unlock only at their specific checkpoint; batching them together destroys the causal story.
- The wake trails 60px behind the ship and fades over 500ms.
- Payment travels the reverse route to close the loop geometrically.

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
  'An importer\'s bank issues an LC for $480,000 to a supplier abroad.',
  'A ship travels a route across four checkpoints.',
  'Each checkpoint unlocks one required document.',
  'All documents verified means funds release to the supplier.'
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
const TRADE = { lcAmount: 480_000, currency: 'USD', importer: 'Northline Trading', supplier: 'Andes Components', checkpoints: ['Port of Loading', 'Transit', 'Customs', 'Destination Port'], documents: ['Commercial Invoice', 'Packing List', 'Bill of Lading', 'Certificate of Origin'], incoterm: 'CIF', voyageDays: 34 };
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

Keep the geography schematic. Accurate coastlines invite scrutiny of projection errors that are irrelevant to the explanation.

---

**Previous:** [Usage-Based Billing](skill-49-usage-based-billing.md) | **Next:** [Debt Snowball vs Avalanche](skill-51-debt-snowball-vs-avalanche.md) | **Index:** [README](../README.md)
