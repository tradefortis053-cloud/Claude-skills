# Skill 25 — Dividend Reinvestment

**Category C:** Wealth, Trading & Analytics

> Dividend droplets falling back into the principal bucket to compound the share count.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `25` |
| **Slug** | `skill-25-dividend-drip` |
| **Category** | Wealth, Trading & Analytics |
| **Output file** | `output/skill-25-dividend-drip.html` |
| **Timeline length** | 16s (16,000 ms) at 1x speed |
| **Accent pair** | `#10B981` primary, `#4F46E5` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #25`
- `Run skill-25-dividend-drip`
- `Build the dividend reinvestment explainer`
- A natural-language request whose intent matches: _Show dividend mechanics and DRIP: ex-date, payment, per-share distribution, and reinvestment that increases share count._

### Objective

Show dividend mechanics and DRIP: ex-date, payment, per-share distribution, and reinvestment that increases share count.

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
| **Scene 1: Ex-Dividend Date** | 0.0s - 3.5s | A calendar marks the ex-date and the entitlement window closes. |
| **Scene 2: Dividend Declared** | 3.5s - 7.5s | The distribution is calculated at $0.24 per share across 412 shares. |
| **Scene 3: Cash Lands** | 7.5s - 11.5s | Droplets fall from the holding into the cash balance. |
| **Scene 4: DRIP Reinvests** | 11.5s - 16.0s | Cash converts back into 0.36 additional shares and the count grows. |

### Scene 1 — Ex-Dividend Date

**Timing window:** `0.0s - 3.5s`

**Narration subtitle:**

> A calendar marks the ex-date and the entitlement window closes.

**On-screen elements:** Month calendar grid, an ex-date cell highlighted, entitlement badge.

**Animation physics:** Highlight cell fills top-down over 300ms; the entitlement badge drops in with a 200ms spring.

### Scene 2 — Dividend Declared

**Timing window:** `3.5s - 7.5s`

**Narration subtitle:**

> The distribution is calculated at $0.24 per share across 412 shares.

**On-screen elements:** Per-share figure, share count, total distribution $98.88, payout ratio chip.

**Animation physics:** The multiplication builds left to right: 0.24 x 412 = 98.88 with each operand entering sequentially.

### Scene 3 — Cash Lands

**Timing window:** `7.5s - 11.5s`

**Narration subtitle:**

> Droplets fall from the holding into the cash balance.

**On-screen elements:** Stock holding card above, cash bucket below, three droplets with trails.

**Animation physics:** Droplets fall 90px on an ease-in with 140ms stagger; the cash counter increments as each lands.

### Scene 4 — DRIP Reinvests

**Timing window:** `11.5s - 16.0s`

**Narration subtitle:**

> Cash converts back into 0.36 additional shares and the count grows.

**On-screen elements:** Reinvestment arrow back to the holding, share counter 412 -> 412.36, cost basis note.

**Animation physics:** Arrow traces the reverse path; the share counter uses 2 decimals and a 300ms ease-out; a small compounding note appears.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Calendar grid** | Date context | 7x5 cell grid with 1px separators and a mono date header |
| **Holding card** | Position | 340x120 with ticker, share count and market value |
| **Cash bucket** | Distribution destination | Open-top container with a fill level and a mono balance |
| **Droplets** | Cash movement | Teardrop paths with a gradient fill and a short trailing streak |
| **Reinvestment arrow** | DRIP path | Curved arrow with a gradient stroke from emerald to indigo |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- Share count increases with each reinvestment; it must never decrease during this skill.
- Cash and share values must be mathematically linked by the stated share price.
- Droplet easing is ease-in only. Gravity accelerates, and a bouncy fall looks wrong.
- The final share count uses two decimals; the ticker label stays fixed width to prevent jitter.

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
  'A calendar marks the ex-date and the entitlement window closes.',
  'The distribution is calculated at $0.24 per share across 412 shares.',
  'Droplets fall from the holding into the cash balance.',
  'Cash converts back into 0.36 additional shares and the count grows.'
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
const DRIP = { ticker: 'SCHD', shares: 412, pricePerShare: 81.45, dividendPerShare: 0.24, totalDividend: 98.88, exDate: '2026-09-24', payDate: '2026-09-29', sharesBought: 1.21, newShares: 413.21 };
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

Recompute the share purchase from the dividend total and the share price at load. Two independent numbers almost always disagree.

---

**Previous:** [Robo-Advisor Allocation](skill-24-robo-advisor-allocation.md) | **Next:** [Tax-Loss Harvesting](skill-26-tax-loss-harvesting.md) | **Index:** [README](../README.md)
