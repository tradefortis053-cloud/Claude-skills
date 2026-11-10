# Skill 53 — Embedded Insurance

**Category E:** B2B SaaS, Lending & Credit

> A checkout toggle that mints a policy in under a second.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `53` |
| **Slug** | `skill-53-embedded-insurance` |
| **Category** | B2B SaaS, Lending & Credit |
| **Output file** | `output/skill-53-embedded-insurance.html` |
| **Timeline length** | 15s (15,000 ms) at 1x speed |
| **Accent pair** | `#10B981` primary, `#4F46E5` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #53`
- `Run skill-53-embedded-insurance`
- `Build the embedded insurance explainer`
- A natural-language request whose intent matches: _Show embedded insurance at checkout: coverage offer, premium calculation, instant policy issuance and claims path._

### Objective

Show embedded insurance at checkout: coverage offer, premium calculation, instant policy issuance and claims path.

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
| **Scene 1: Checkout** | 0.0s - 3.5s | A $1,899 laptop sits in the cart with an assurance row beneath. |
| **Scene 2: Toggle On** | 3.5s - 7.0s | The micro-shield toggle flips and coverage terms expand. |
| **Scene 3: Policy Issued** | 7.0s - 11.5s | A policy number is minted with an effective timestamp and a premium of $45.58. |
| **Scene 4: Claim Path** | 11.5s - 15.0s | A claim button appears with a one-tap promise and a 48-hour target. |

### Scene 1 — Checkout

**Timing window:** `0.0s - 3.5s`

**Narration subtitle:**

> A $1,899 laptop sits in the cart with an assurance row beneath.

**On-screen elements:** Checkout card, line items, an assurance row with a shield glyph and a 2.4% premium.

**Animation physics:** The assurance row highlights with a 2px indigo outline; the premium chip counts from 0.0% to 2.4%.

### Scene 2 — Toggle On

**Timing window:** `3.5s - 7.0s`

**Narration subtitle:**

> The micro-shield toggle flips and coverage terms expand.

**On-screen elements:** Toggle at 56x32, an expanding details panel with 3 coverage bullets and an exclusion note.

**Animation physics:** The panel expands from 0 to its height over 320ms; bullets fade in at 80ms intervals; the exclusion line uses a smaller, muted style.

### Scene 3 — Policy Issued

**Timing window:** `7.0s - 11.5s`

**Narration subtitle:**

> A policy number is minted with an effective timestamp and a premium of $45.58.

**On-screen elements:** Policy card with number, term, premium, and an instant-issue badge.

**Animation physics:** The policy number types at 24ms per character; the instant badge stamps in with a 180ms spring; the total updates once.

### Scene 4 — Claim Path

**Timing window:** `11.5s - 15.0s`

**Narration subtitle:**

> A claim button appears with a one-tap promise and a 48-hour target.

**On-screen elements:** Claim CTA with a subtle pulse, a 48h SLA chip, and a coverage summary line.

**Animation physics:** The CTA pulses twice at 1.04 scale; the SLA chip fades in; everything settles to a still final frame.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Shield glyph** | Protection | Shield path 40px tall with a check glyph and a 1.5px stroke |
| **Toggle** | Opt-in | Rounded track with a 24px knob and a subtle inner shadow |
| **Policy card** | Contract | 340x200 with policy number, term dates, premium and issuer line |
| **SLA chip** | Service promise | Emerald pill with a clock glyph and a mono duration |
| **Coverage summary** | Terms digest | Three-bullet block with consistent line heights |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- Premium must be computed from the cart total and the displayed rate; the arithmetic is checked by viewers.
- The exclusions line is not optional; an insurance demo without exclusions is a compliance problem.
- Instant issuance is under one second on screen; avoid a fake spinner that contradicts the promise.
- The claim CTA is the only element that pulses at the end; reduce competing motion to keep focus.

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
  'A $1,899 laptop sits in the cart with an assurance row beneath.',
  'The micro-shield toggle flips and coverage terms expand.',
  'A policy number is minted with an effective timestamp and a premium of $45.58.',
  'A claim button appears with a one-tap promise and a 48-hour target.'
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
const INSURANCE = { cart: 1_899, item: 'Laptop', premiumPct: 0.024, premium: 45.58, coverageLimit: 1_899, termMonths: 24, policyNo: 'POL-8F31-2210', issuedIn: '0.8s', slaHours: 48 };
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

Show the annualized cost too. A 2.4% premium on a $1,899 laptop is $45.58 for the term; ambiguous term lengths are the usual complaint.

---

**Previous:** [Chargeback Dispute Flow](skill-52-chargeback-dispute-flow.md) | **Next:** [Carbon Offset Checkout](skill-54-carbon-offset-checkout.md) | **Index:** [README](../README.md)
