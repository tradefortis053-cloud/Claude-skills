# Skill 45 — Expense Receipt OCR

**Category E:** B2B SaaS, Lending & Credit

> A crumpled receipt turning into structured expense fields.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `45` |
| **Slug** | `skill-45-expense-receipt-ocr` |
| **Category** | B2B SaaS, Lending & Credit |
| **Output file** | `output/skill-45-expense-receipt-ocr.html` |
| **Timeline length** | 17s (17,000 ms) at 1x speed |
| **Accent pair** | `#06B6D4` primary, `#10B981` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #45`
- `Run skill-45-expense-receipt-ocr`
- `Build the expense receipt ocr explainer`
- A natural-language request whose intent matches: _Show receipt OCR for expenses: image capture, field detection, extraction into structured data, category prediction and policy check._

### Objective

Show receipt OCR for expenses: image capture, field detection, extraction into structured data, category prediction and policy check.

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
| **Scene 1: Capture** | 0.0s - 4.0s | The camera frames a receipt and auto-crops with perspective correction. |
| **Scene 2: Field Detection** | 4.0s - 9.0s | Bounding boxes appear over vendor, date, total and tax. |
| **Scene 3: Extraction** | 9.0s - 13.5s | Text lifts from the receipt into structured form fields. |
| **Scene 4: Policy Check** | 13.5s - 17.0s | The expense is categorized, policy-checked and submitted. |

### Scene 1 — Capture

**Timing window:** `0.0s - 4.0s`

**Narration subtitle:**

> The camera frames a receipt and auto-crops with perspective correction.

**On-screen elements:** Phone viewfinder, receipt at an angle, four crop handles snapping to corners.

**Animation physics:** The crop quad deforms from screen-aligned to perspective-correct over 700ms; a subtle grid overlay appears.

### Scene 2 — Field Detection

**Timing window:** `4.0s - 9.0s`

**Narration subtitle:**

> Bounding boxes appear over vendor, date, total and tax.

**On-screen elements:** Four dashed boxes with label tags, scanning line sweeping vertically.

**Animation physics:** The scan line sweeps top to bottom twice; each box draws after the line passes it, with a 120ms delay.

### Scene 3 — Extraction

**Timing window:** `9.0s - 13.5s`

**Narration subtitle:**

> Text lifts from the receipt into structured form fields.

**On-screen elements:** Extraction ghosts flying from box to field, four form rows populating in mono.

**Animation physics:** Ghosts travel along a slight arc over 400ms; fields populate sequentially with a caret blink; confidence chips appear at 92% and above.

### Scene 4 — Policy Check

**Timing window:** `13.5s - 17.0s`

**Narration subtitle:**

> The expense is categorized, policy-checked and submitted.

**On-screen elements:** Category chip MEALS, policy status WITHIN LIMIT, submit confirmation with an amount match.

**Animation physics:** Category chip types in; the policy check flips to emerald; a final match line confirms the total equals the sum of line items.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Viewfinder** | Capture frame | Rounded rect with 4 corner brackets and a 20% dim mask outside |
| **Crop quad** | Perspective correction | Quadrilateral with draggable corner handles and hairline guides |
| **Field boxes** | Detection regions | Dashed rounded rects with label tabs anchored top-left |
| **Scan line** | OCR sweep | 2px horizontal line with a gradient glow, clipped to the receipt |
| **Form rows** | Structured output | Four rows with label, mono value and a confidence chip |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- Detection boxes appear only after the scan line has passed them; simultaneous appearance implies magic.
- Extracted values use a light typing effect at 30 characters per second, not a hard cut.
- Confidence is shown per field, and values below 90% visually flag for review.
- The final total must equal the sum of detected line items; recompute at load.

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
  'The camera frames a receipt and auto-crops with perspective correction.',
  'Bounding boxes appear over vendor, date, total and tax.',
  'Text lifts from the receipt into structured form fields.',
  'The expense is categorized, policy-checked and submitted.'
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
const OCR = { vendor: 'Harbor Provisions', date: '2026-08-14', total: 84.36, tax: 6.12, category: 'Meals', confidence: { vendor: 0.97, date: 0.94, total: 0.99, tax: 0.91 }, policy: 'within $100 limit', currency: 'USD' };
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

Keep the receipt content clearly synthetic. A real-looking receipt photo with a real vendor name can create legal friction in a demo.

---

**Previous:** [Payroll Distribution](skill-44-payroll-distribution.md) | **Next:** [Revenue-Based Financing](skill-46-revenue-based-financing.md) | **Index:** [README](../README.md)
