# Skill 18 — Open Banking OAuth

**Category B:** Banking Infrastructure & Ledgers

> A three-party handshake bridge built from Bank, Aggregator and App.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `18` |
| **Slug** | `skill-18-open-banking-oauth` |
| **Category** | Banking Infrastructure & Ledgers |
| **Output file** | `output/skill-18-open-banking-oauth.html` |
| **Timeline length** | 18s (18,000 ms) at 1x speed |
| **Accent pair** | `#4F46E5` primary, `#10B981` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #18`
- `Run skill-18-open-banking-oauth`
- `Build the open banking oauth explainer`
- A natural-language request whose intent matches: _Explain the OAuth consent flow in open banking: consent scope selection, redirect handshake, token exchange, and scoped data access._

### Objective

Explain the OAuth consent flow in open banking: consent scope selection, redirect handshake, token exchange, and scoped data access.

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
| **Scene 1: Consent Screen** | 0.0s - 4.5s | The user reviews scopes: balances, transactions and identity. |
| **Scene 2: Three-Party Handshake** | 4.5s - 10.0s | Bank, aggregator and app exchange a redirect and an auth code. |
| **Scene 3: Token Exchange** | 10.0s - 14.0s | The code is swapped for a short-lived access token in the back channel. |
| **Scene 4: Scoped Data Access** | 14.0s - 18.0s | Transactions flow into the app, limited exactly to the granted scopes. |

### Scene 1 — Consent Screen

**Timing window:** `0.0s - 4.5s`

**Narration subtitle:**

> The user reviews scopes: balances, transactions and identity.

**On-screen elements:** Consent card with three toggle rows and a scope summary footer.

**Animation physics:** Toggles flip on at 160ms intervals; the summary line counts scopes 0 -> 3.

### Scene 2 — Three-Party Handshake

**Timing window:** `4.5s - 10.0s`

**Narration subtitle:**

> Bank, aggregator and app exchange a redirect and an auth code.

**On-screen elements:** Three nodes on a bridge, numbered exchange arrows 1, 2, 3.

**Animation physics:** Arrows draw in strict numeric order at 500ms each; no arrow overlaps the next.

### Scene 3 — Token Exchange

**Timing window:** `10.0s - 14.0s`

**Narration subtitle:**

> The code is swapped for a short-lived access token in the back channel.

**On-screen elements:** Server-to-server dashed channel, token chip with 90-minute TTL, refresh token chip.

**Animation physics:** Dashed channel draws with a marching-ants offset; token chip lands and the TTL ticks down from 90:00.

### Scene 4 — Scoped Data Access

**Timing window:** `14.0s - 18.0s`

**Narration subtitle:**

> Transactions flow into the app, limited exactly to the granted scopes.

**On-screen elements:** Data rows entering the app, a scope guard badge rejecting one out-of-scope request.

**Animation physics:** Rows stream in over 1.2s; the blocked request bounces off the guard with a 3px rebound.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Bridge** | Trust path between parties | Three-pillar isometric bridge with 2px rails and 8 support ties |
| **Party nodes** | Participants | 72px rounded squares with bank, aggregator and app glyphs |
| **Exchange arrows** | Protocol steps | Numbered arcs with arrowheads, 1.5px stroke, distinct hue per step |
| **Token chip** | Credential | Pill with a mono token preview and a TTL countdown ring |
| **Scope guard** | Least privilege | Shield gate at the app boundary with a pass and a block lane |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- Numbered arrows must animate strictly in sequence; parallel arrows misrepresent the protocol.
- The token chip uses a countdown ring that decelerates visually as it approaches expiry.
- Blocked requests rebound 3px and fade over 220ms, clearly different from a smooth pass.
- Never show a raw token value in full, only a truncated mono preview.

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
  'The user reviews scopes: balances, transactions and identity.',
  'Bank, aggregator and app exchange a redirect and an auth code.',
  'The code is swapped for a short-lived access token in the back channel.',
  'Transactions flow into the app, limited exactly to the granted scopes.'
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
const OAUTH = { grant: 'authorization_code + PKCE', scopes: ['accounts.balance', 'transactions.read', 'identity.read'], tokenTtlMin: 90, refreshRotates: true, psuConsent: 'PSD2 SCA', revokedAfterDays: 90 };
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

Label the consent as revocable and time-bounded. That detail is what separates an open-banking demo from a data-scraping one.

---

**Previous:** [Virtual Card Issuance](skill-17-virtual-card-issuance.md) | **Next:** [Micro-Investing Round-Up](skill-19-micro-investing-roundup.md) | **Index:** [README](../README.md)
