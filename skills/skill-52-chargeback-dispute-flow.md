# Skill 52 — Chargeback Dispute Flow

**Category E:** B2B SaaS, Lending & Credit

> Evidence in, arbitration out, funds restored, on one timeline.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `52` |
| **Slug** | `skill-52-chargeback-dispute-flow` |
| **Category** | B2B SaaS, Lending & Credit |
| **Output file** | `output/skill-52-chargeback-dispute-flow.html` |
| **Timeline length** | 18s (18,000 ms) at 1x speed |
| **Accent pair** | `#F43F5E` primary, `#10B981` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #52`
- `Run skill-52-chargeback-dispute-flow`
- `Build the chargeback dispute flow explainer`
- A natural-language request whose intent matches: _Show the dispute lifecycle: chargeback filing, merchant evidence submission, network arbitration, and outcome notification._

### Objective

Show the dispute lifecycle: chargeback filing, merchant evidence submission, network arbitration, and outcome notification.

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
| **Scene 1: Chargeback Filed** | 0.0s - 4.0s | A cardholder files a dispute for $1,240 with reason code 'not as described'. |
| **Scene 2: Merchant Evidence** | 4.0s - 9.5s | The merchant uploads tracking, delivery proof and correspondence. |
| **Scene 3: Arbitration Review** | 9.5s - 14.5s | The network reviews both sides and issues a decision. |
| **Scene 4: Funds Restored** | 14.5s - 18.0s | The decision lands, funds return to the cardholder and the case closes. |

### Scene 1 — Chargeback Filed

**Timing window:** `0.0s - 4.0s`

**Narration subtitle:**

> A cardholder files a dispute for $1,240 with reason code 'not as described'.

**On-screen elements:** Dispute card with reason code, amount, and a filed timestamp, a case ID.

**Animation physics:** The reason code types in mono; the case ID stamps with a 200ms spring; the filed chip turns amber.

### Scene 2 — Merchant Evidence

**Timing window:** `4.0s - 9.5s`

**Narration subtitle:**

> The merchant uploads tracking, delivery proof and correspondence.

**On-screen elements:** Three evidence upload tiles with file glyphs, progress rings, and a submission deadline chip.

**Animation physics:** Upload rings fill at 120ms intervals; the deadline chip counts down from 7 days in mono.

### Scene 3 — Arbitration Review

**Timing window:** `9.5s - 14.5s`

**Narration subtitle:**

> The network reviews both sides and issues a decision.

**On-screen elements:** Balanced scale graphic with evidence weights on each side, a review status ladder of three stages.

**Animation physics:** Scale tilts toward the cardholder with a 400ms settle; the ladder steps light at 400ms intervals.

### Scene 4 — Funds Restored

**Timing window:** `14.5s - 18.0s`

**Narration subtitle:**

> The decision lands, funds return to the cardholder and the case closes.

**On-screen elements:** Outcome card, restored funds arrow to the cardholder, closed status with a reason summary.

**Animation physics:** The funds arrow reverses the original charge path; the closed stamp lands with a 1.08 overshoot; hold.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Dispute card** | Case | 360x200 with reason code, amount, and a status rail |
| **Evidence tiles** | Merchant proof | Three 140x100 tiles with a paper glyph and a progress ring |
| **Deadline chip** | Time pressure | Amber pill with a mono countdown and a clock glyph |
| **Scale** | Arbitration | Central fulcrum with two weighted pans and a settling beam |
| **Outcome card** | Decision | Card with a decision label, amount restored and a closing rule |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- The deadline countdown is visible during evidence submission; deadlines are the mechanics of chargebacks.
- The scale tilts only once, slowly, and settles without oscillation.
- Funds restoration reuses the original charge path in reverse, consistent with skill 08.
- Neutral language throughout: 'decision', not 'win' or 'loss'.

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
  'A cardholder files a dispute for $1,240 with reason code \'not as described\'.',
  'The merchant uploads tracking, delivery proof and correspondence.',
  'The network reviews both sides and issues a decision.',
  'The decision lands, funds return to the cardholder and the case closes.'
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
const CHARGEBACK = { caseId: 'CB-2214', amount: 1_240, reasonCode: 'not_as_described', filedDaysAgo: 0, evidenceDeadlineDays: 7, evidence: ['Tracking', 'Delivery photo', 'Email thread'], decision: 'cardholder', restoreDays: 3, status: 'CLOSED' };
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

Pair this with skill 08 for a reversible-flows series. Both use mirrored path geometry and should share the same visual language.

---

**Previous:** [Debt Snowball vs Avalanche](skill-51-debt-snowball-vs-avalanche.md) | **Next:** [Embedded Insurance](skill-53-embedded-insurance.md) | **Index:** [README](../README.md)
