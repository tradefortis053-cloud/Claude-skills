# Skill 03 — Split Bill

**Category A:** Payment Flows & Transactions

> One $186.40 dinner invoice fanning out into four shares with live percentage counters.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `03` |
| **Slug** | `skill-03-split-bill` |
| **Category** | Payment Flows & Transactions |
| **Output file** | `output/skill-03-split-bill.html` |
| **Timeline length** | 16s (16,000 ms) at 1x speed |
| **Accent pair** | `#10B981` primary, `#4F46E5` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #03`
- `Run skill-03-split-bill`
- `Build the split bill explainer`
- A natural-language request whose intent matches: _Demonstrate bill splitting with unequal shares, tip apportioning, rounding guards, and per-party settlement states._

### Objective

Demonstrate bill splitting with unequal shares, tip apportioning, rounding guards, and per-party settlement states.

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
| **Scene 1: Single Invoice** | 0.0s - 3.5s | One invoice sits in the center: $186.40 with a 20% tip already applied. |
| **Scene 2: Fan Out** | 3.5s - 8.5s | The invoice splits into four party nodes along radial spokes. |
| **Scene 3: Share Math** | 8.5s - 13.0s | Each party shows its percentage and exact amount, with the rounding remainder assigned. |
| **Scene 4: Settled** | 13.0s - 16.0s | Three parties settle instantly; one is pending and shows a nudge button. |

### Scene 1 — Single Invoice

**Timing window:** `0.0s - 3.5s`

**Narration subtitle:**

> One invoice sits in the center: $186.40 with a 20% tip already applied.

**On-screen elements:** Centered invoice card, line items, total in JetBrains Mono at 40px.

**Animation physics:** Card scales 0.96 -> 1 with a 480ms spring; total counts up from 0 with tabular-nums so digits never shift.

### Scene 2 — Fan Out

**Timing window:** `3.5s - 8.5s`

**Narration subtitle:**

> The invoice splits into four party nodes along radial spokes.

**On-screen elements:** Four avatar nodes arranged on a 220px radius, connector spokes, share chips.

**Animation physics:** Spokes draw on a 60ms stagger; each node pops with scale 0.8 -> 1 and a 120ms overlap.

### Scene 3 — Share Math

**Timing window:** `8.5s - 13.0s`

**Narration subtitle:**

> Each party shows its percentage and exact amount, with the rounding remainder assigned.

**On-screen elements:** Percentage counters, amount labels, a remainder line highlighting the $0.02 absorber.

**Animation physics:** Percent values tween in lockstep so they always sum to 100.0; remainder chip pulses once when it resolves.

### Scene 4 — Settled

**Timing window:** `13.0s - 16.0s`

**Narration subtitle:**

> Three parties settle instantly; one is pending and shows a nudge button.

**On-screen elements:** Status chips (SETTLED / PENDING), a progress ring at 75%.

**Animation physics:** Settled chips swap to emerald with a 200ms crossfade; ring arc animates 0 -> 75% with a rounded cap.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Invoice card** | Pre-split state | Rounded rect 340x200, glass surface, three hairline separators |
| **Radial spokes** | Split topology | Four straight lines from center to node ring, 1.5px, 30% opacity |
| **Party nodes** | Participants | 48px circles with initials, plus a 72px dashed halo when pending |
| **Percentage counters** | Share math | JetBrains Mono 22px, tabular-nums, suffix at 60% opacity |
| **Progress ring** | Settlement status | Circle with stroke-dasharray 2*pi*r, rotated -90deg |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- All four amount counters are driven from a single scene progress value so they never drift apart.
- Fan-out uses transform-origin at the invoice center with a 40ms per-spoke delay.
- Rounding remainder reveals with a 1.08 scale pulse then settles to 1.0 over 300ms.
- Pending halo rotates at 12deg per second with a linear timing function because it is ambient motion.

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
  'One invoice sits in the center: $186.40 with a 20% tip already applied.',
  'The invoice splits into four party nodes along radial spokes.',
  'Each party shows its percentage and exact amount, with the rounding remainder assigned.',
  'Three parties settle instantly; one is pending and shows a nudge button.'
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
const BILL = { merchant: 'Osteria Nove', subtotal: 155.33, tipPct: 20, total: 186.40, parties: [{ name: 'Maya', pct: 25, due: 46.60 }, { name: 'Arjun', pct: 25, due: 46.60 }, { name: 'Lena', pct: 30, due: 55.92 }, { name: 'Tom', pct: 20, due: 37.28 }], remainderAbsorber: 'Tom', remainder: 0.02 };
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

Always render the remainder absorber explicitly. Finance reviewers look for it, and hiding rounding is the most common credibility failure in split-payment visuals.

---

**Previous:** [Card Swipe Authorization](skill-02-card-swipe-auth.md) | **Next:** [QR Scan and Pay](skill-04-qr-scan-pay.md) | **Index:** [README](../README.md)
