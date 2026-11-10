# Skill 12 — Immutable Ledger

**Category B:** Banking Infrastructure & Ledgers

> Cryptographic blocks locking in sequence while hash strings type themselves out.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `12` |
| **Slug** | `skill-12-immutable-ledger` |
| **Category** | Banking Infrastructure & Ledgers |
| **Output file** | `output/skill-12-immutable-ledger.html` |
| **Timeline length** | 18s (18,000 ms) at 1x speed |
| **Accent pair** | `#06B6D4` primary, `#4F46E5` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #12`
- `Run skill-12-immutable-ledger`
- `Build the immutable ledger explainer`
- A natural-language request whose intent matches: _Show append-only ledger mechanics: hashing transaction batches, chaining each block to its predecessor, and detecting tampering._

### Objective

Show append-only ledger mechanics: hashing transaction batches, chaining each block to its predecessor, and detecting tampering.

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
| **Scene 1: Transaction Pool** | 0.0s - 4.0s | Four pending transactions settle into a mempool line. |
| **Scene 2: Block Sealed** | 4.0s - 9.0s | The pool batches, a merkle root is computed and a hash types out. |
| **Scene 3: Chain Link** | 9.0s - 14.0s | Each block references the previous hash and the chain extends. |
| **Scene 4: Tamper Detected** | 14.0s - 18.0s | One block is altered and every downstream link invalidates in red. |

### Scene 1 — Transaction Pool

**Timing window:** `0.0s - 4.0s`

**Narration subtitle:**

> Four pending transactions settle into a mempool line.

**On-screen elements:** Four transaction chips with mono IDs and amounts, a pending queue rail.

**Animation physics:** Chips drop into the pool with a 70ms stagger and a 6px settle bounce.

### Scene 2 — Block Sealed

**Timing window:** `4.0s - 9.0s`

**Narration subtitle:**

> The pool batches, a merkle root is computed and a hash types out.

**On-screen elements:** Block card with nonce, merkle root, timestamp and a typing hash line.

**Animation physics:** Hash types at 22ms per hex character; the block border draws from 0 -> full perimeter over 800ms.

### Scene 3 — Chain Link

**Timing window:** `9.0s - 14.0s`

**Narration subtitle:**

> Each block references the previous hash and the chain extends.

**On-screen elements:** Three blocks linked by prev-hash connector rails.

**Animation physics:** Connector draws between blocks on a 200ms stagger; each new block inherits a 1-block vertical offset.

### Scene 4 — Tamper Detected

**Timing window:** `14.0s - 18.0s`

**Narration subtitle:**

> One block is altered and every downstream link invalidates in red.

**On-screen elements:** Altered block with a diff highlight, downstream hashes flashing rose, invalid banner.

**Animation physics:** The tamper sweep travels right at 1 block per 300ms; affected blocks shift 2px and desaturate, then the banner slides in.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Transaction chips** | Ledger inputs | 120x36 pills with mono ID and right-aligned amount |
| **Block card** | Ledger unit | 260x200 rounded rect with a 3-row mono field stack |
| **Hash text** | Integrity proof | JetBrains Mono 12px, 0.2em tracking, truncated to 16 hex characters |
| **Chain connectors** | Linked structure | 1.5px lines with a mid-arrow marker between block edges |
| **Tamper highlight** | Invalidation | Rose overlay rect with a 1px inset border and a diagonal hatch pattern |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- Typed hashes must be deterministic per block index so replay produces identical strings.
- Only one hash types at a time; concurrent typing destroys legibility.
- Tamper propagation is a rightward sweep with a fixed 300ms per block, never a global flash.
- After invalidation, hold the state for the final 600ms instead of looping, so the consequence lands.

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
  'Four pending transactions settle into a mempool line.',
  'The pool batches, a merkle root is computed and a hash types out.',
  'Each block references the previous hash and the chain extends.',
  'One block is altered and every downstream link invalidates in red.'
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
const LEDGER = { blockHeight: 841_207, txCount: 4, prevHash: '0000a3f1c9d2', merkleRoot: '7e4b90cc12af', nonce: 18423, algorithm: 'SHA-256', finality: 'probabilistic' };
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

Say 'append-only with tamper evidence' rather than 'unhackable'. Precision protects the demo from technical criticism.

---

**Previous:** [ACH, Wire and Real-Time Routing](skill-11-ach-wire-routing.md) | **Next:** [API and Webhook Sync](skill-13-api-webhook-sync.md) | **Index:** [README](../README.md)
