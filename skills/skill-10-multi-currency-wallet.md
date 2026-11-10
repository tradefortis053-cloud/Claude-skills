# Skill 10 — Multi-Currency Wallet

**Category A:** Payment Flows & Transactions

> Glass cards fanning out to reveal EUR, USD, GBP and JPY balances at once.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `10` |
| **Slug** | `skill-10-multi-currency-wallet` |
| **Category** | Payment Flows & Transactions |
| **Output file** | `output/skill-10-multi-currency-wallet.html` |
| **Timeline length** | 16s (16,000 ms) at 1x speed |
| **Accent pair** | `#4F46E5` primary, `#06B6D4` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #10`
- `Run skill-10-multi-currency-wallet`
- `Build the multi-currency wallet explainer`
- A natural-language request whose intent matches: _Show a unified multi-currency wallet: stacked balances, live conversion into a base currency, and an FX sweep that consolidates idle balances._

### Objective

Show a unified multi-currency wallet: stacked balances, live conversion into a base currency, and an FX sweep that consolidates idle balances.

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
| **Scene 1: Stacked Wallet** | 0.0s - 3.5s | Four glass cards sit perfectly stacked and then fan open. |
| **Scene 2: Balances** | 3.5s - 8.0s | Each card displays its native balance and its base-currency equivalent. |
| **Scene 3: FX Sweep** | 8.0s - 12.5s | Idle EUR and GBP balances sweep into USD to cover a payment. |
| **Scene 4: One Number** | 12.5s - 16.0s | The wallet collapses back to a single consolidated balance. |

### Scene 1 — Stacked Wallet

**Timing window:** `0.0s - 3.5s`

**Narration subtitle:**

> Four glass cards sit perfectly stacked and then fan open.

**On-screen elements:** Four overlapping rounded rects with currency glyphs, 12px vertical offsets.

**Animation physics:** Cards fan to rotate(-12, -4, 4, 12) with 60ms stagger on a spring; total balance chip stays fixed.

### Scene 2 — Balances

**Timing window:** `3.5s - 8.0s`

**Narration subtitle:**

> Each card displays its native balance and its base-currency equivalent.

**On-screen elements:** Per-card native amount plus a smaller USD equivalent line.

**Animation physics:** Counters tween on a 500ms ease-out; equivalents crossfade 120ms after each native count finishes.

### Scene 3 — FX Sweep

**Timing window:** `8.0s - 12.5s`

**Narration subtitle:**

> Idle EUR and GBP balances sweep into USD to cover a payment.

**On-screen elements:** Conversion arrows arcing between cards, rate chips, a consolidated total.

**Animation physics:** Arcs draw from each source card into the USD card at 140ms offsets; source balances decrement as the destination increments.

### Scene 4 — One Number

**Timing window:** `12.5s - 16.0s`

**Narration subtitle:**

> The wallet collapses back to a single consolidated balance.

**On-screen elements:** Cards restack, total counter at 44px mono, base currency chip.

**Animation physics:** Cards return to the stacked position; the total counts from the pre-sweep value to the consolidated one.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Wallet cards** | Currency containers | Four 300x180 rounded rects with glass fills and 1px hairline borders |
| **Currency glyphs** | Denomination | Circle badge with a mono three-letter code, no flag emoji |
| **FX arcs** | Conversion paths | Quadratic beziers between card centers with arrowheads |
| **Consolidated total** | Single source of truth | Mono 44px figure with tabular-nums and a smaller currency suffix |
| **Rate chips** | Conversion transparency | Pill with rate text and a 10% opacity indigo fill |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- Fan transforms use transform-origin at the card base, not the center, so the stack looks hinged.
- Balance updates are conserved: total value must not change during the sweep, only distribution.
- Card depth uses a 6px shadow ladder rather than blur, which stays crisp on low-DPI screens.
- Collapse uses a 400ms ease-in-out and must complete before the total counter animates.

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
  'Four glass cards sit perfectly stacked and then fan open.',
  'Each card displays its native balance and its base-currency equivalent.',
  'Idle EUR and GBP balances sweep into USD to cover a payment.',
  'The wallet collapses back to a single consolidated balance.'
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
const WALLET = { base: 'USD', balances: { EUR: 1240.50, USD: 860.00, GBP: 410.20, JPY: 58000 }, rates: { 'EUR/USD': 1.087, 'GBP/USD': 1.271, 'JPY/USD': 0.0067 }, consolidateFor: 'Vendor payout' };
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

Currency glyphs beat flag emoji. Emoji rendering differs across platforms and breaks visual consistency in a premium fintech UI.

---

**Previous:** [NFC Contactless Tap](skill-09-nfc-contactless.md) | **Next:** [ACH, Wire and Real-Time Routing](skill-11-ach-wire-routing.md) | **Index:** [README](../README.md)
