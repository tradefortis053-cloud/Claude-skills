# Skill 37 — Role-Based Access Control

**Category D:** Security, Compliance & KYC

> An approval chain that stops a $250,000 payout until the right three people sign.

---

## 1. Skill Identity & Trigger

| Field | Value |
| --- | --- |
| **Skill ID** | `37` |
| **Slug** | `skill-37-role-based-access` |
| **Category** | Security, Compliance & KYC |
| **Output file** | `output/skill-37-role-based-access.html` |
| **Timeline length** | 17s (17,000 ms) at 1x speed |
| **Accent pair** | `#4F46E5` primary, `#10B981` secondary |

### Trigger Commands

Any of the following must fire this skill:

- `Execute Skill #37`
- `Run skill-37-role-based-access`
- `Build the role-based access control explainer`
- A natural-language request whose intent matches: _Show RBAC plus approval policy: role assignment, permission scope, dual control on large payouts, and an audited approval chain._

### Objective

Show RBAC plus approval policy: role assignment, permission scope, dual control on large payouts, and an audited approval chain.

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
| **Scene 1: Team Hierarchy** | 0.0s - 4.0s | A four-node org tree loads with roles attached to each node. |
| **Scene 2: Payout Initiated** | 4.0s - 8.5s | An initiator submits a $250,000 vendor payout. |
| **Scene 3: Approval Chain** | 8.5s - 13.5s | Two approvers must sign; one attempts an out-of-policy approval and is blocked. |
| **Scene 4: Released** | 13.5s - 17.0s | Both approvals land and the payout releases with a full audit trail. |

### Scene 1 — Team Hierarchy

**Timing window:** `0.0s - 4.0s`

**Narration subtitle:**

> A four-node org tree loads with roles attached to each node.

**On-screen elements:** Tree with connectors, role chips ADMIN, APPROVER, INITIATOR, VIEWER.

**Animation physics:** Nodes appear top-down over 500ms; connectors draw after their endpoints exist; role chips fade in 120ms later.

### Scene 2 — Payout Initiated

**Timing window:** `4.0s - 8.5s`

**Narration subtitle:**

> An initiator submits a $250,000 vendor payout.

**On-screen elements:** Payout card with amount, vendor, and a policy badge reading DUAL APPROVAL REQUIRED.

**Animation physics:** The policy badge pulses rose twice; the payout card cannot advance until the first approval lands.

### Scene 3 — Approval Chain

**Timing window:** `8.5s - 13.5s`

**Narration subtitle:**

> Two approvers must sign; one attempts an out-of-policy approval and is blocked.

**On-screen elements:** Two approval slots, a blocked attempt card with a 403 message, an audit log line.

**Animation physics:** The blocked attempt rebounds 3px and greys out; the audit line appends with a mono timestamp.

### Scene 4 — Released

**Timing window:** `13.5s - 17.0s`

**Narration subtitle:**

> Both approvals land and the payout releases with a full audit trail.

**On-screen elements:** Two green approval badges, a release rail to the vendor, three audit rows.

**Animation physics:** Badges flip to approved at 200ms intervals; the release rail draws in 600ms; audit rows fill last.

### Scene Hand-off Rules

- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.
- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.
- The step indicator text is `Step N of 4: <Scene Name>` and must update exactly at the boundary fraction.
- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.

---

## 3. SVG Vector Blueprint

| Vector | Purpose | Construction |
| --- | --- | --- |
| **Org tree** | Hierarchy | Four 64px nodes with orthogonal connectors and rounded joints |
| **Role chips** | Permissions | Compact pills with uppercase role names and a leading dot |
| **Policy badge** | Control requirement | Rose-outlined pill with a lock glyph and uppercase label |
| **Approval slots** | Dual control | Two 200x64 slots with avatar, role and status line |
| **Audit rows** | Trail | Three mono rows with timestamp, actor and action columns |

### SVG Implementation Notes

- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio="xMidYMid meet"` so the artwork scales with the container.
- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.
- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.
- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.

---

## 4. Animation Physics

- The blocked approval must occur before the successful chain, so the rule is demonstrated rather than asserted.
- A single approval can never release the payout, at any scrub position.
- Role chips keep fixed widths across states to prevent layout shift when statuses change.
- The audit trail is the quiet hero: it appears last, stays still, and never animates out.

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
  'A four-node org tree loads with roles attached to each node.',
  'An initiator submits a $250,000 vendor payout.',
  'Two approvers must sign; one attempts an out-of-policy approval and is blocked.',
  'Both approvals land and the payout releases with a full audit trail.'
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
const RBAC = { payout: 250_000, vendor: 'Helios Freight', policy: 'dual approval over $100k', roles: ['ADMIN', 'APPROVER', 'INITIATOR', 'VIEWER'], blockedAttempt: { actor: 'initiator', code: 403, reason: 'self-approval' }, approvals: 2, auditRows: 3 };
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

Include the self-approval block. It is the most common real-world control failure and the most instructive moment in the skill.

---

**Previous:** [Tokenization Vault](skill-36-tokenization-vault.md) | **Next:** [PCI DSS Shield](skill-38-pci-dss-shield.md) | **Index:** [README](../README.md)
