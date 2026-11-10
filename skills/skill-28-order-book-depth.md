# Skill 28 — Order Book Depth

**Category C:** Wealth, Trading & Analytics

> Bid and ask walls breathing around a price that refuses to sit still.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `28` |
| **Slug** | `skill-28-order-book-depth` |
| **Category** | Wealth, Trading & Analytics |
| **Output file** | `output/skill-28-order-book-depth.html` |
| **Timeline length** | 17s (17,000 ms) at 1x speed |
| **Accent pair** | `#10B981` primary, `#F43F5E` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #28`
- `Run skill-28-order-book-depth`
- `Build the order book depth explainer`
- A natural-language request whose intent matches: _Explain market microstructure: bid-ask spread, depth ladder, imbalance, and how a large order walks the book._

### Objective

Explain market microstructure: bid-ask spread, depth ladder, imbalance, and how a large order walks the book.

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
| **Scene 1: Book Snapshot** | 0.0s - 4.0s | Ten levels of bids and asks populate around a mid price of $184.20. |
| **Scene 2: Live Updates** | 4.0s - 8.5s | Sizes flicker as orders are added and pulled at the top of book. |
| **Scene 3: Imbalance** | 8.5s - 12.5s | Bid depth outweighs ask depth three to one and the price starts to lean. |
| **Scene 4: Large Order Walks** | 12.5s - 17.0s | A market buy sweeps four ask levels and the spread widens. |

### Scene 1 — Book Snapshot

**Timing window:** `0.0s - 4.0s`

**Narration subtitle:**

> Ten levels of bids and asks populate around a mid price of $184.20.

**On-screen elements:** Two ladder columns, depth bars scaled to size, spread gutter in the center.

**Animation physics:** Rows appear from the inside out at 60ms intervals; the spread gutter draws a mono measurement line.

### Scene 2 — Live Updates

**Timing window:** `4.0s - 8.5s`

**Narration subtitle:**

> Sizes flicker as orders are added and pulled at the top of book.

**On-screen elements:** Depth bars resizing, flashing size deltas in green and rose.

**Animation physics:** Each update flashes for 120ms then decays over 400ms; new rows insert with a 6px vertical slide.

### Scene 3 — Imbalance

**Timing window:** `8.5s - 12.5s`

**Narration subtitle:**

> Bid depth outweighs ask depth three to one and the price starts to lean.

**On-screen elements:** A balance meter tilting toward bids, an imbalance ratio of 3.1x, mid price ticking up.

**Animation physics:** Meter tilt follows the ratio with 220ms smoothing; the mid ticker rolls its last digit per tick.

### Scene 4 — Large Order Walks

**Timing window:** `12.5s - 17.0s`

**Narration subtitle:**

> A market buy sweeps four ask levels and the spread widens.

**On-screen elements:** Order ticket of 2,400 shares, ask rows consumed sequentially, new spread measurement.

**Animation physics:** Rows fade and collapse in sequence at 160ms; depth bars shrink to zero; the spread gutter re-measures with a 300ms ease.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Depth ladder** | Book structure | 20 rows across two columns with 1px separators and right-aligned mono sizes |
| **Depth bars** | Liquidity | Background rects scaled to cumulative size at 14% opacity |
| **Spread gutter** | Bid-ask spread | Central 60px column with a bracket and a mono measurement |
| **Balance meter** | Imbalance | Horizontal seesaw with a sliding fulcrum and a ratio label |
| **Order ticket** | Aggressive order | Compact card with side, quantity and estimated fill |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- Depth bars are cumulative, not per-level; per-level bars misrepresent book shape.
- Mid price updates only after both sides finish their row insertions.
- The imbalance meter must not tilt faster than the underlying ratio changes.
- Flash decays are essential; without them rapid updates become strobe-like and unwatchable.

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
  'Ten levels of bids and asks populate around a mid price of $184.20.',
  'Sizes flicker as orders are added and pulled at the top of book.',
  'Bid depth outweighs ask depth three to one and the price starts to lean.',
  'A market buy sweeps four ask levels and the spread widens.'
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
const ORDER_BOOK = { symbol: 'AAPL', mid: 184.20, spreadCents: 2, bidDepth: 48_200, askDepth: 15_400, imbalance: 3.13, order: { side: 'BUY', qty: 2400, type: 'MARKET' }, levels: 10 };
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

Cap live update frequency at roughly 2 per second. Real tick data is unreadable at video speed and reads as visual noise.

---

**Previous:** [Fractional Shares](skill-27-fractional-shares.md) | **Next:** [Net Worth Aggregator](skill-29-net-worth-aggregator.md) | **Index:** [README](../README.md)
