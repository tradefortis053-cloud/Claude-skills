# Skill 06 — Escrow Release

**Category A:** Payment Flows & Transactions

> A vault that only opens when both parties turn their keys green.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `06` |
| **Slug** | `skill-06-escrow-release` |
| **Category** | Payment Flows & Transactions |
| **Output file** | `output/skill-06-escrow-release.html` |
| **Timeline length** | 17s (17,000 ms) at 1x speed |
| **Accent pair** | `#4F46E5` primary, `#10B981` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #06`
- `Run skill-06-escrow-release`
- `Build the escrow release explainer`
- A natural-language request whose intent matches: _Show conditional escrow: funds locked, delivery proof from the buyer, acceptance from the seller, then simultaneous release._

### Objective

Show conditional escrow: funds locked, delivery proof from the buyer, acceptance from the seller, then simultaneous release.

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
| **Scene 1: Funds Locked** | 0.0s - 4.0s | The vault seals with a $12,500 balance inside and two unlit condition keys. |
| **Scene 2: Condition One** | 4.0s - 8.5s | The buyer uploads delivery proof and the first key turns emerald. |
| **Scene 3: Condition Two** | 8.5s - 13.0s | The seller confirms acceptance and the second key turns green. |
| **Scene 4: Release** | 13.0s - 17.0s | Both keys align, the door opens and funds split: 95% seller, 5% fee. |

### Scene 1 — Funds Locked

**Timing window:** `0.0s - 4.0s`

**Narration subtitle:**

> The vault seals with a $12,500 balance inside and two unlit condition keys.

**On-screen elements:** Vault door SVG with radial bolts, a mono balance plate, two key slots at 30% opacity.

**Animation physics:** Door bolts rotate 0 -> 45deg on an 80ms stagger; a lock pulse travels around the door rim once per 2s.

### Scene 2 — Condition One

**Timing window:** `4.0s - 8.5s`

**Narration subtitle:**

> The buyer uploads delivery proof and the first key turns emerald.

**On-screen elements:** Document glyph flying into the left key slot, checkbox resolving.

**Animation physics:** Document translates 160px on a bezier with a 30% opacity trail; key rotates 90deg with a 180ms spring.

### Scene 3 — Condition Two

**Timing window:** `8.5s - 13.0s`

**Narration subtitle:**

> The seller confirms acceptance and the second key turns green.

**On-screen elements:** Mirrored interaction on the right side with an acceptance signature stroke.

**Animation physics:** Signature path draws over 520ms; the second key mirrors the first with identical easing for symmetry.

### Scene 4 — Release

**Timing window:** `13.0s - 17.0s`

**Narration subtitle:**

> Both keys align, the door opens and funds split: 95% seller, 5% fee.

**On-screen elements:** Vault opening, two fund streams, settlement ledger row.

**Animation physics:** Door rotates open on the y-axis over 700ms; streams travel on mirrored arcs; ledger row slides in last.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Vault** | Custody of funds | Outer circle 120px radius, inner door with 8 bolts around a 60px hub |
| **Condition keys** | Dual authorization | Two key silhouettes built from a circle plus a notched rect, mirrored across center |
| **Document glyph** | Delivery proof | Rect with a folded corner and three text lines |
| **Fund streams** | Release distribution | Two tapered paths with gradient fill from indigo to emerald |
| **Ledger row** | Audit trail | Table row 520x40 with four mono columns |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- Both conditions must be state-driven booleans derived from progress, not from click state.
- Key rotation eases with a springy overshoot of 6 degrees before settling.
- The door uses a CSS 3D transform on an SVG group with perspective 800px.
- Only the final release stage may use emerald; earlier stages stay indigo so green still means go.

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
  'The vault seals with a $12,500 balance inside and two unlit condition keys.',
  'The buyer uploads delivery proof and the first key turns emerald.',
  'The seller confirms acceptance and the second key turns green.',
  'Both keys align, the door opens and funds split: 95% seller, 5% fee.'
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
const ESCROW = { dealId: 'ESC-2291', amount: 12500, currency: 'USD', buyer: 'Northwind Labs', seller: 'Sable Studio', milestones: ['Delivered', 'Accepted'], platformFeePct: 5, releaseEta: 'Instant' };
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

Never animate release before both condition checks complete, even when scrubbing quickly. Clamp stage transitions to progress thresholds.

---

**Previous:** [Cross-Border FX Transfer](skill-05-cross-border-fx.md) | **Next:** [Subscription Recurring Billing](skill-07-subscription-recurring.md) | **Index:** [README](../README.md)
