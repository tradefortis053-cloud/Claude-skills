# Skill 24 — Robo-Advisor Allocation

**Category C:** Wealth, Trading & Analytics

> One risk slider morphing an entire asset allocation in real time.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `24` |
| **Slug** | `skill-24-robo-advisor-allocation` |
| **Category** | Wealth, Trading & Analytics |
| **Output file** | `output/skill-24-robo-advisor-allocation.html` |
| **Timeline length** | 16s (16,000 ms) at 1x speed |
| **Accent pair** | `#4F46E5` primary, `#F43F5E` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #24`
- `Run skill-24-robo-advisor-allocation`
- `Build the robo-advisor allocation explainer`
- A natural-language request whose intent matches: _Explain risk profiling: how a single risk score maps to an allocation model, expected return range and maximum drawdown tolerance._

### Objective

Explain risk profiling: how a single risk score maps to an allocation model, expected return range and maximum drawdown tolerance.

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
| **Scene 1: Risk Profile** | 0.0s - 4.0s | A five-question profile resolves to a risk score of 6 out of 10. |
| **Scene 2: Slider Moves** | 4.0s - 9.5s | The user drags from Conservative to Aggressive. |
| **Scene 3: Morphing Weights** | 9.5s - 13.5s | Equities, bonds and alternatives re-weight with each stop. |
| **Scene 4: Model Locked** | 13.5s - 16.0s | The allocation locks in with expected return and drawdown figures. |

### Scene 1 — Risk Profile

**Timing window:** `0.0s - 4.0s`

**Narration subtitle:**

> A five-question profile resolves to a risk score of 6 out of 10.

**On-screen elements:** Questionnaire summary card, five answered chips, a score gauge at 60%.

**Animation physics:** Answered chips cascade in at 80ms intervals; the gauge needle sweeps 0 -> 6 with a 220ms damped spring.

### Scene 2 — Slider Moves

**Timing window:** `4.0s - 9.5s`

**Narration subtitle:**

> The user drags from Conservative to Aggressive.

**On-screen elements:** Horizontal slider with five labelled stops, a live allocation preview stacking to the right.

**Animation physics:** Thumb follows a bezier path; allocation bars reflow continuously with 120ms smoothing so motion never snaps.

### Scene 3 — Morphing Weights

**Timing window:** `9.5s - 13.5s`

**Narration subtitle:**

> Equities, bonds and alternatives re-weight with each stop.

**On-screen elements:** Stacked horizontal bars, weight labels in mono, an expected return band chip.

**Animation physics:** Bars interpolate from current to target over 400ms per stop; text labels crossfade only after the bars settle.

### Scene 4 — Model Locked

**Timing window:** `13.5s - 16.0s`

**Narration subtitle:**

> The allocation locks in with expected return and drawdown figures.

**On-screen elements:** Locked allocation bar, return band 4.2% to 6.8%, max drawdown 18%.

**Animation physics:** Bars gain a 1px indigo outline; figures count in; hold the final state for 900ms.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Risk gauge** | Profile score | 240-degree arc with 10 tick marks and a needle path |
| **Risk slider** | User control | Track with five stop dots and a draggable thumb 18px wide |
| **Allocation bars** | Portfolio mix | Stacked rects with 2px gaps and inline mono percentage labels |
| **Return band** | Expected outcome | Horizontal band with a midpoint marker and range labels |
| **Drawdown note** | Risk disclosure | Small mono caption with a rose accent rule on the left |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- Allocation must always sum to 100%; clamp and normalize after interpolation rather than trusting raw lerps.
- The slider is a real interactive control. Pointer drag must update the render pipeline, not just CSS.
- Expected return ranges widen as risk rises; that widening is the teaching moment.
- Show maximum drawdown alongside return. Presenting upside without downside is the classic robo-advisor failure.

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
  'A five-question profile resolves to a risk score of 6 out of 10.',
  'The user drags from Conservative to Aggressive.',
  'Equities, bonds and alternatives re-weight with each stop.',
  'The allocation locks in with expected return and drawdown figures.'
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
const ROBO = { riskScore: 6, models: [{ name: 'Conservative', equities: 0.25, bonds: 0.65, alts: 0.10, ret: [0.028, 0.041], dd: 0.07 }, { name: 'Balanced', equities: 0.55, bonds: 0.35, alts: 0.10, ret: [0.038, 0.058], dd: 0.12 }, { name: 'Aggressive', equities: 0.85, bonds: 0.08, alts: 0.07, ret: [0.042, 0.068], dd: 0.18 }] };
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

Always pair the expected return with a drawdown figure in the same visual block. It is a compliance-friendly pattern and looks more premium.

---

**Previous:** [Candlestick Formation](skill-23-candlestick-formation.md) | **Next:** [Dividend Reinvestment](skill-25-dividend-drip.md) | **Index:** [README](../README.md)
