# Skill 13 — API and Webhook Sync

**Category B:** Banking Infrastructure & Ledgers

> A JSON payload leaving a code pane and landing as a live mobile notification.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `13` |
| **Slug** | `skill-13-api-webhook-sync` |
| **Category** | Banking Infrastructure & Ledgers |
| **Output file** | `output/skill-13-api-webhook-sync.html` |
| **Timeline length** | 17s (17,000 ms) at 1x speed |
| **Accent pair** | `#4F46E5` primary, `#06B6D4` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #13`
- `Run skill-13-api-webhook-sync`
- `Build the api and webhook sync explainer`
- A natural-language request whose intent matches: _Explain event-driven integration: an API request, a signed webhook delivery, idempotency handling, and the resulting UI update._

### Objective

Explain event-driven integration: an API request, a signed webhook delivery, idempotency handling, and the resulting UI update.

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
| **Scene 1: API Call** | 0.0s - 4.0s | A POST request builds in the code pane with syntax highlighting. |
| **Scene 2: Signed Webhook** | 4.0s - 9.0s | The event serializes and travels to the merchant endpoint with an HMAC signature. |
| **Scene 3: Idempotent Handling** | 9.0s - 13.0s | A duplicate delivery arrives and is safely ignored via the idempotency key. |
| **Scene 4: UI Updates** | 13.0s - 17.0s | The mobile screen flips from Pending to Paid with the exact webhook amount. |

### Scene 1 — API Call

**Timing window:** `0.0s - 4.0s`

**Narration subtitle:**

> A POST request builds in the code pane with syntax highlighting.

**On-screen elements:** Code card with line numbers, method badge POST, endpoint, JSON body.

**Animation physics:** Lines reveal one at a time at 90ms; the POST badge pulses once when the request fires.

### Scene 2 — Signed Webhook

**Timing window:** `4.0s - 9.0s`

**Narration subtitle:**

> The event serializes and travels to the merchant endpoint with an HMAC signature.

**On-screen elements:** Payload orb labeled payment_intent.succeeded, a signature chip, a delivery rail.

**Animation physics:** Orb travels the rail over 900ms; a 200 response chip lands with a 1.05 scale overshoot.

### Scene 3 — Idempotent Handling

**Timing window:** `9.0s - 13.0s`

**Narration subtitle:**

> A duplicate delivery arrives and is safely ignored via the idempotency key.

**On-screen elements:** Two identical payloads, one marked DUPLICATE, a dedupe shield.

**Animation physics:** Second payload arrives with 60% opacity and is stamped DUPLICATE over 180ms.

### Scene 4 — UI Updates

**Timing window:** `13.0s - 17.0s`

**Narration subtitle:**

> The mobile screen flips from Pending to Paid with the exact webhook amount.

**On-screen elements:** Phone frame, status pill transition, amount row, timestamp.

**Animation physics:** Pill crossfades amber to emerald over 200ms; the amount row does a single 4px rise.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Code pane** | Developer surface | 560x300 rounded rect with a 24px gutter strip and mono 12px lines |
| **Payload orb** | Event object | Gradient circle 28px with an outer 60px blurred glow |
| **Delivery rail** | Transport | Dashed horizontal layer with three waypoint dots |
| **Dedupe shield** | Idempotency | Shield path 36px tall with a check glyph inside |
| **Phone frame** | End consumer surface | Rounded rect 260x520 with a 24px screen radius |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- JSON lines reveal on a fixed 90ms cadence and never reflow the pane height mid-animation.
- The duplicate payload must be visibly dimmer but identical in content, so dedupe reads correctly.
- Webhook latency label ticks from 0ms to 142ms during transit.
- Prefer mono for all identifiers, keys and amounts; sans for commentary labels.

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
  'A POST request builds in the code pane with syntax highlighting.',
  'The event serializes and travels to the merchant endpoint with an HMAC signature.',
  'A duplicate delivery arrives and is safely ignored via the idempotency key.',
  'The mobile screen flips from Pending to Paid with the exact webhook amount.'
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
const WEBHOOK = { event: 'payment_intent.succeeded', id: 'evt_1Qx8Zk2e', idempotencyKey: 'idem_7c31ab', amount: 49.00, currency: 'USD', deliveredIn: '142ms', signature: 't=1731,v1=8f9c...' };
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

Show the idempotency key explicitly. It is the single most useful detail for engineers evaluating the demo.

---

**Previous:** [Immutable Ledger](skill-12-immutable-ledger.md) | **Next:** [Liquidity Pool Balancing](skill-14-liquidity-pool.md) | **Index:** [README](../README.md)
