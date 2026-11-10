# Skill 55 — AI Financial Copilot

**Category E:** B2B SaaS, Lending & Credit

> A sentence typed in plain language turning into a live cash-flow forecast.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `55` |
| **Slug** | `skill-55-ai-financial-copilot` |
| **Category** | B2B SaaS, Lending & Credit |
| **Output file** | `output/skill-55-ai-financial-copilot.html` |
| **Timeline length** | 19s (19,000 ms) at 1x speed |
| **Accent pair** | `#4F46E5` primary, `#06B6D4` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #55`
- `Run skill-55-ai-financial-copilot`
- `Build the ai financial copilot explainer`
- A natural-language request whose intent matches: _Show an AI copilot workflow: natural-language intent, tool calls against real financial data, a generated forecast chart, and cited assumptions._

### Objective

Show an AI copilot workflow: natural-language intent, tool calls against real financial data, a generated forecast chart, and cited assumptions.

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
| **Scene 1: Prompt** | 0.0s - 3.5s | The user types: 'What does cash runway look like if hiring slows by 30%?' |
| **Scene 2: Tool Calls** | 3.5s - 9.0s | Three tool calls fire against ledger, payroll and forecast data. |
| **Scene 3: Forecast Chart** | 9.0s - 14.5s | The chart draws two paths: current plan and slowed hiring. |
| **Scene 4: Cited Answer** | 14.5s - 19.0s | The answer states 22 months and cites every assumption behind it. |

### Scene 1 — Prompt

**Timing window:** `0.0s - 3.5s`

**Narration subtitle:**

> The user types: 'What does cash runway look like if hiring slows by 30%?'

**On-screen elements:** Prompt bar with a caret, a submit chip, and a small model badge.

**Animation physics:** Characters type at 26ms; the caret blinks at 530ms intervals; the submit chip lights when the last character lands.

### Scene 2 — Tool Calls

**Timing window:** `3.5s - 9.0s`

**Narration subtitle:**

> Three tool calls fire against ledger, payroll and forecast data.

**On-screen elements:** Three call chips with names, a response time in mono, and a progress state.

**Animation physics:** Chips fan out from the prompt at 120ms intervals; each resolves with a 180ms crossfade and a mono latency figure.

### Scene 3 — Forecast Chart

**Timing window:** `9.0s - 14.5s`

**Narration subtitle:**

> The chart draws two paths: current plan and slowed hiring.

**On-screen elements:** Dual-line forecast chart with a shaded runway area, month axis, and an intersection marker at the runway end.

**Animation physics:** Both paths draw over 1.2s at 120ms offset; the shaded area fades in; the runway marker drops onto the intersection point.

### Scene 4 — Cited Answer

**Timing window:** `14.5s - 19.0s`

**Narration subtitle:**

> The answer states 22 months and cites every assumption behind it.

**On-screen elements:** Answer card with a headline figure, three assumption rows with source tags, and a confidence note.

**Animation physics:** The headline counts to 22 months; assumption rows reveal at 140ms intervals; source tags land last with a small link glyph.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Prompt bar** | Input surface | Rounded rect with a caret, an inline submit button and a model badge |
| **Tool chips** | System calls | Three 160x56 chips with a name, status dot and mono latency |
| **Forecast paths** | Outcomes | Two polylines generated from monthly data with gradient area fills |
| **Runway marker** | Intersection | Vertical dashed line with a down-arrow head and a mono month label |
| **Assumption rows** | Citations | Three rows with label, value and a source tag pill |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- The forecast curve must be generated from the stated assumptions at load, not drawn by hand to look plausible.
- Tool calls complete before the chart begins, so causality is preserved.
- The answer's headline number must match the chart's runway marker exactly.
- Assumptions and sources are part of the answer, not an afterthought. They render in the same final frame.

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
  'The user types: \'What does cash runway look like if hiring slows by 30%?\'',
  'Three tool calls fire against ledger, payroll and forecast data.',
  'The chart draws two paths: current plan and slowed hiring.',
  'The answer states 22 months and cites every assumption behind it.'
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
const COPILOT = { prompt: 'What does cash runway look like if hiring slows by 30%?', tools: [{ name: 'ledger.query', ms: 84 }, { name: 'payroll.model', ms: 132 }, { name: 'forecast.run', ms: 240 }], cashOnHand: 4_200_000, burn: 191_000, runwayMonths: 22, slowedRunwayMonths: 29, assumptions: [{ label: 'Current burn', value: '$191k/mo', source: 'Ledger' }, { label: 'Hiring plan', value: '-30%', source: 'Payroll' }, { label: 'Revenue growth', value: '4% MoM', source: 'Forecast' }] };
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

This is the skill that most needs visible sourcing. An AI finance answer without cited assumptions is a liability, not a demo.

---

**Previous:** [Carbon Offset Checkout](skill-54-carbon-offset-checkout.md) | **Next:** _End of series_ | **Index:** [README](../README.md)
