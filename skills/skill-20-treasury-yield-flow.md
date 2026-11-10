# Skill 20 — Treasury Yield Sweep

**Category B:** Banking Infrastructure & Ledgers

> Idle cash sweeping into yield overnight and returning before payroll.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `20` |
| **Slug** | `skill-20-treasury-yield-flow` |
| **Category** | Banking Infrastructure & Ledgers |
| **Output file** | `output/skill-20-treasury-yield-flow.html` |
| **Timeline length** | 18s (18,000 ms) at 1x speed |
| **Accent pair** | `#4F46E5` primary, `#10B981` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #20`
- `Run skill-20-treasury-yield-flow`
- `Build the treasury yield sweep explainer`
- A natural-language request whose intent matches: _Show automated treasury sweeps: idle balance detection, money market allocation, accrual, and liquidity recall before obligations._

### Objective

Show automated treasury sweeps: idle balance detection, money market allocation, accrual, and liquidity recall before obligations.

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
| **Scene 1: Idle Cash Detected** | 0.0s - 4.0s | A $3.2M operating balance sits idle past its buffer. |
| **Scene 2: Sweep to Yield** | 4.0s - 9.5s | The excess sweeps into a money market fund at 5.1% APY. |
| **Scene 3: Overnight Accrual** | 9.5s - 14.5s | Interest accrues hour by hour while the clock runs at night. |
| **Scene 4: Recall for Payroll** | 14.5s - 18.0s | Funds are recalled before the payroll run and the buffer is restored. |

### Scene 1 — Idle Cash Detected

**Timing window:** `0.0s - 4.0s`

**Narration subtitle:**

> A $3.2M operating balance sits idle past its buffer.

**On-screen elements:** Operating account card, a buffer threshold band, an idle amount highlight.

**Animation physics:** Threshold band pulses amber once; the idle segment of the balance bar separates with an 8px rise.

### Scene 2 — Sweep to Yield

**Timing window:** `4.0s - 9.5s`

**Narration subtitle:**

> The excess sweeps into a money market fund at 5.1% APY.

**On-screen elements:** Sweep arrow into a yield bucket, APY chip, fund name in mono.

**Animation physics:** Sweep travels over 800ms with a tapered gradient; the APY chip ticks from 0.0% to 5.1%.

### Scene 3 — Overnight Accrual

**Timing window:** `9.5s - 14.5s`

**Narration subtitle:**

> Interest accrues hour by hour while the clock runs at night.

**On-screen elements:** Clock arc from 22:00 to 06:00, accrual micro-bars, a running interest counter.

**Animation physics:** Accrual bars grow at 1 bar per 160ms; interest counter increments in hundredths with tabular-nums.

### Scene 4 — Recall for Payroll

**Timing window:** `14.5s - 18.0s`

**Narration subtitle:**

> Funds are recalled before the payroll run and the buffer is restored.

**On-screen elements:** Recall arrow back to operating, payroll calendar chip, buffer at 100%.

**Animation physics:** Recall arrow reverses the sweep path; buffer refills to its threshold line; a green check closes the loop.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Account card** | Liquidity source | 380x160 with a balance figure and a threshold band overlay |
| **Sweep arrow** | Automated transfer | Tapered path with a gradient from indigo to emerald and a rounded head |
| **Yield bucket** | Investment destination | Cylinder form with an APY chip and a fill level |
| **Clock arc** | Overnight window | 270-degree arc with hour ticks and a moving marker |
| **Payroll chip** | Obligation | Calendar glyph with a mono date and amount |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- Sweep and recall must use mirrored path geometry so the round trip reads as one system.
- Interest accrual is small on purpose; show hundredths so the value is visible without exaggeration.
- The clock arc advances 22:00 to 06:00 across the scene, then stops exactly at the end frame.
- Buffer restoration uses an ease-out so the refill feels like a completed obligation, not a race.

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
  'A $3.2M operating balance sits idle past its buffer.',
  'The excess sweeps into a money market fund at 5.1% APY.',
  'Interest accrues hour by hour while the clock runs at night.',
  'Funds are recalled before the payroll run and the buffer is restored.'
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
const TREASURY = { operatingBalance: 3_200_000, bufferTarget: 2_400_000, swept: 800_000, apy: 0.051, fund: 'Prime MMF', overnightInterest: 111.78, payrollDue: '06:00', recalled: 800_000 };
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

Keep the APY visibly labelled as illustrative. Yields move and a stale number invites complaints.

---

**Previous:** [Micro-Investing Round-Up](skill-19-micro-investing-roundup.md) | **Next:** [Compound Interest Curve](skill-21-compound-interest-curve.md) | **Index:** [README](../README.md)
