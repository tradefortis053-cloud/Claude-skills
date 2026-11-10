# Skill 15 — Smart Contract Execution

**Category B:** Banking Infrastructure & Ledgers

> IF and THEN gates lighting up as a payload walks the conditional path.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `15` |
| **Slug** | `skill-15-smart-contract-exec` |
| **Category** | Banking Infrastructure & Ledgers |
| **Output file** | `output/skill-15-smart-contract-exec.html` |
| **Timeline length** | 17s (17,000 ms) at 1x speed |
| **Accent pair** | `#4F46E5` primary, `#10B981` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #15`
- `Run skill-15-smart-contract-exec`
- `Build the smart contract execution explainer`
- A natural-language request whose intent matches: _Visualize deterministic contract logic: condition evaluation, branch selection, state mutation and an emitted event._

### Objective

Visualize deterministic contract logic: condition evaluation, branch selection, state mutation and an emitted event.

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
| **Scene 1: Invocation** | 0.0s - 3.5s | A function call enters the contract boundary with typed arguments. |
| **Scene 2: Conditional Gates** | 3.5s - 9.0s | Two IF gates evaluate and one branch is chosen. |
| **Scene 3: State Mutation** | 9.0s - 13.5s | The contract writes new state and updates the ledger entry. |
| **Scene 4: Event Emitted** | 13.5s - 17.0s | An event log entry is appended and confirmed by the network. |

### Scene 1 — Invocation

**Timing window:** `0.0s - 3.5s`

**Narration subtitle:**

> A function call enters the contract boundary with typed arguments.

**On-screen elements:** Contract outline, function signature in mono, three argument chips.

**Animation physics:** The call packet enters from the left; the contract border draws once around the full perimeter.

### Scene 2 — Conditional Gates

**Timing window:** `3.5s - 9.0s`

**Narration subtitle:**

> Two IF gates evaluate and one branch is chosen.

**On-screen elements:** Diamond gate shapes labeled IF, true and false output rails, a boolean chip.

**Animation physics:** True path turns emerald and stays lit; the false path dims to 30% and stops animating entirely.

### Scene 3 — State Mutation

**Timing window:** `9.0s - 13.5s`

**Narration subtitle:**

> The contract writes new state and updates the ledger entry.

**On-screen elements:** State variable row flipping from PENDING to SETTLED, storage slot glyph.

**Animation physics:** Row values crossfade with an 80ms overlap; storage glyph fills 0 -> 100% vertically.

### Scene 4 — Event Emitted

**Timing window:** `13.5s - 17.0s`

**Narration subtitle:**

> An event log entry is appended and confirmed by the network.

**On-screen elements:** Event log card, three confirmation dots, finality stamp.

**Animation physics:** Dots light at 200ms intervals; the stamp scales in with a 180ms spring and holds.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Contract boundary** | Execution scope | Rounded rect 420x300 with a 1.5px dashed stroke |
| **Diamond gates** | Conditional logic | Rotated squares with a centered IF label and two output ports |
| **Branch rails** | Control flow | Orthogonal polylines with rounded 8px joints |
| **State rows** | Storage mutation | 300x40 rows with key on the left in mono and value right-aligned |
| **Event log** | Observability | Card with a mono event name, indexed args and a block number |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- Only one branch may animate at a time; dimming the losing branch is a hard requirement.
- Gate evaluation flashes are 120ms, not 400ms. Logic should read as instant.
- State change uses a value crossfade, never a slide, to avoid implying a transaction in progress.
- Colour semantics are fixed: emerald true, rose false, indigo neutral path.

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
  'A function call enters the contract boundary with typed arguments.',
  'Two IF gates evaluate and one branch is chosen.',
  'The contract writes new state and updates the ledger entry.',
  'An event log entry is appended and confirmed by the network.'
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
const CONTRACT = { function: 'releaseMilestone(uint256 id)', args: { id: 2, amount: 5000, currency: 'USDC' }, condition: 'approvals >= 2', result: true, stateBefore: 'PENDING', stateAfter: 'SETTLED', event: 'MilestoneReleased(id=2)' };
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

Keep the branch graph at most two levels deep. Deeper logic needs a different skill and a slower duration.

---

**Previous:** [Liquidity Pool Balancing](skill-14-liquidity-pool.md) | **Next:** [Automated Reconciliation](skill-16-automated-reconciliation.md) | **Index:** [README](../README.md)
