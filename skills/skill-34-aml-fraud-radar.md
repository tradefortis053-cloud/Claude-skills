# Skill 34 — AML Fraud Radar

**Category D:** Security, Compliance & KYC

> A radar that constantly sweeps a stream of transactions and quarantines one anomaly.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `34` |
| **Slug** | `skill-34-aml-fraud-radar` |
| **Category** | Security, Compliance & KYC |
| **Output file** | `output/skill-34-aml-fraud-radar.html` |
| **Timeline length** | 19s (19,000 ms) at 1x speed |
| **Accent pair** | `#F43F5E` primary, `#06B6D4` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #34`
- `Run skill-34-aml-fraud-radar`
- `Build the aml fraud radar explainer`
- A natural-language request whose intent matches: _Explain real-time transaction monitoring: streaming ingest, rule and model scoring, anomaly isolation, and case escalation._

### Objective

Explain real-time transaction monitoring: streaming ingest, rule and model scoring, anomaly isolation, and case escalation.

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
| **Scene 1: Stream Ingest** | 0.0s - 4.0s | Transactions stream in as a dense field of moving dots. |
| **Scene 2: Radar Sweep** | 4.0s - 8.0s | A rotating sweep beam scores each batch against AML rules. |
| **Scene 3: Anomaly Isolated** | 8.0s - 13.5s | One dot breaks pattern: $9,800 structured into three transfers. |
| **Scene 4: Quarantine** | 13.5s - 19.0s | The account is held, a case opens and a SAR review is scheduled. |

### Scene 1 — Stream Ingest

**Timing window:** `0.0s - 4.0s`

**Narration subtitle:**

> Transactions stream in as a dense field of moving dots.

**On-screen elements:** Radar circle with concentric rings, 60 transaction dots on orbital paths, a live count.

**Animation physics:** Dots spawn at the rim and decay toward center; count increments at roughly 8 per second in mono.

### Scene 2 — Radar Sweep

**Timing window:** `4.0s - 8.0s`

**Narration subtitle:**

> A rotating sweep beam scores each batch against AML rules.

**On-screen elements:** Wedge sweep with a trailing gradient, score badges appearing on dots.

**Animation physics:** The sweep rotates 360deg in 3.2s; dots flash their score as the beam passes; beam is clipped to the radar circle.

### Scene 3 — Anomaly Isolated

**Timing window:** `8.0s - 13.5s`

**Narration subtitle:**

> One dot breaks pattern: $9,800 structured into three transfers.

**On-screen elements:** A single dot turns rose and slows, expanding into a detail card with three linked amounts.

**Animation physics:** The dot pulls toward center while others dim to 30%; the detail card unfurls with a 300ms ease; structure links draw between amounts.

### Scene 4 — Quarantine

**Timing window:** `13.5s - 19.0s`

**Narration subtitle:**

> The account is held, a case opens and a SAR review is scheduled.

**On-screen elements:** Quarantine ring around the dot, case card CASE-4471, escalation ladder.

**Animation physics:** The ring closes over 400ms; the case card slides in from the right; the escalation ladder ticks through three stages and holds.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Radar** | Monitoring scope | Three concentric circles at 90, 150 and 210 radius, 1px strokes at 18% opacity |
| **Sweep beam** | Inspection | Wedge path with a conic-style gradient, clipped to the outer circle |
| **Transaction dots** | Events | 4px circles with 12% fill and a 1px stroke |
| **Anomaly card** | Case detail | 280x180 card with three amount rows and a structure link graphic |
| **Quarantine ring** | Hold | Dashed rose ring at 40% opacity with a lock glyph at the top |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- The sweep is an ambient rotation gated by scene progress so pausing freezes it cleanly.
- Only one dot may become the anomaly; competing highlights destroy the focus of the scene.
- Dimming non-relevant dots to 30% is mandatory before the detail card appears.
- Avoid naming a real regulation action as certain. Use 'review opened', not 'SAR filed'.

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
  'Transactions stream in as a dense field of moving dots.',
  'A rotating sweep beam scores each batch against AML rules.',
  'One dot breaks pattern: $9,800 structured into three transfers.',
  'The account is held, a case opens and a SAR review is scheduled.'
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
const AML = { streamRate: '8 txn/s', rules: ['structuring', 'velocity', 'geo mismatch'], anomaly: { account: 'AC-9921', amount: 9800, splits: [3200, 3300, 3300], window: '36h', score: 0.94 }, caseId: 'CASE-4471', action: 'account hold + review' };
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

This is the most sensitive skill in the set. Keep the language procedural and avoid implying guilt about a named party.

---

**Previous:** [End-to-End Encryption](skill-33-end-to-end-encryption.md) | **Next:** [2FA TOTP Countdown](skill-35-2fa-totp-countdown.md) | **Index:** [README](../README.md)
