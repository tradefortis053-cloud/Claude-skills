# Skill 23 — Candlestick Formation

**Category C:** Wealth, Trading & Analytics

> OHLC candles assembling body first, wick second, volume rising underneath.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `23` |
| **Slug** | `skill-23-candlestick-formation` |
| **Category** | Wealth, Trading & Analytics |
| **Output file** | `output/skill-23-candlestick-formation.html` |
| **Timeline length** | 18s (18,000 ms) at 1x speed |
| **Accent pair** | `#10B981` primary, `#F43F5E` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #23`
- `Run skill-23-candlestick-formation`
- `Build the candlestick formation explainer`
- A natural-language request whose intent matches: _Teach candle anatomy: open, high, low, close, body direction, and the relationship between volume and price movement._

### Objective

Teach candle anatomy: open, high, low, close, body direction, and the relationship between volume and price movement.

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
| **Scene 1: Anatomy of One Candle** | 0.0s - 5.5s | A single candle is built with labelled callouts for O, H, L and C. |
| **Scene 2: Series of Candles** | 5.5s - 11.0s | Twenty candles build left to right with real OHLC values. |
| **Scene 3: Volume Bars** | 11.0s - 15.0s | Volume bars rise beneath the price panel. |
| **Scene 4: Read the Tape** | 15.0s - 18.0s | A caption reads the pattern: higher highs with falling volume. |

### Scene 1 — Anatomy of One Candle

**Timing window:** `0.0s - 5.5s`

**Narration subtitle:**

> A single candle is built with labelled callouts for O, H, L and C.

**On-screen elements:** Isolated candle at 3x scale, four callout lines with mono price labels.

**Animation physics:** Body draws from open to close over 500ms; wicks extend outward on a 180ms stagger; labels fade in after the body completes.

### Scene 2 — Series of Candles

**Timing window:** `5.5s - 11.0s`

**Narration subtitle:**

> Twenty candles build left to right with real OHLC values.

**On-screen elements:** 20 candles spaced 24px apart, alternating bullish and bearish fills.

**Animation physics:** Each candle builds in 120ms with a 60ms horizontal stagger; the last candle keeps a live pulse until the scene ends.

### Scene 3 — Volume Bars

**Timing window:** `11.0s - 15.0s`

**Narration subtitle:**

> Volume bars rise beneath the price panel.

**On-screen elements:** Volume histogram scaled to the same bar cadence, 60% height panel.

**Animation physics:** Bars grow from baseline on a 380ms ease-out, staggered with the candles so each pairs semantically.

### Scene 4 — Read the Tape

**Timing window:** `15.0s - 18.0s`

**Narration subtitle:**

> A caption reads the pattern: higher highs with falling volume.

**On-screen elements:** Annotation bracket spanning candles 12 to 20, divergence marker, a mono summary line.

**Animation physics:** Bracket draws right to left; the divergence marker pulses once; the summary line reveals by word group.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Candle body** | Open-close range | Rect with width 14 and height derived from |close - open| |
| **Wicks** | High-low range | Two 1px vertical lines above and below the body |
| **Volume bars** | Participation | Rects with 4px gaps and a 0.55 opacity fill |
| **Callout lines** | Anatomy labels | 1px leaders with 60% opacity and small terminal dots |
| **Divergence bracket** | Pattern annotation | Horizontal bracket with two down-ticks and a 1.2px stroke |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- Generate candles from a seeded OHLC series so every replay is byte-for-byte identical.
- Body is drawn before wicks; reversing that order reads as a glitch.
- Candle build time shortens from 260ms for the first candle to 90ms by the last, which implies acceleration.
- Volume bars must never exceed the price panel's left and right bounds.

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
  'A single candle is built with labelled callouts for O, H, L and C.',
  'Twenty candles build left to right with real OHLC values.',
  'Volume bars rise beneath the price panel.',
  'A caption reads the pattern: higher highs with falling volume.'
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
const CANDLES = { symbol: 'NVDA', interval: '1D', candles: 20, first: { o: 118.40, h: 121.10, l: 117.60, c: 120.35 }, last: { o: 138.20, h: 139.40, l: 135.10, c: 136.05 }, volumeNote: 'rising price, falling volume' };
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

Keep the price axis visible while candles build. A floating chart without scale looks decorative rather than financial.

---

**Previous:** [Portfolio Rebalance](skill-22-portfolio-rebalance.md) | **Next:** [Robo-Advisor Allocation](skill-24-robo-advisor-allocation.md) | **Index:** [README](../README.md)
