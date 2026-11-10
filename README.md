# Universal Fintech Motion Skills

**55 production-ready motion & explanation video skills that turn any AI coding agent into a fintech motion graphics engine.**

Every skill produces a **single, self-contained `.html` file** built with HTML5, TailwindCSS (CDN), Vanilla JavaScript and inline SVG. No build step. No bundler. No dependencies. Open the file in any modern browser and a cinematic, scrubbable explanation video plays.

> Built to feel like Stripe, Linear, Wise, Vercel and Apple — not like a slide deck.

---

## Why this exists

Fintech products are hard to explain because the interesting part is invisible: clearing, netting, tokenization, dilution, dunning, FX spreads. Diagrams in a doc go stale. Screenshots can't show a packet moving through a compliance checkpoint.

This repository gives an AI agent a **complete, deterministic motion specification** for 55 fintech concepts, plus a reference engine that makes every frame a pure function of timeline progress. That single constraint is what makes the output feel like a real video editor rather than a pile of CSS animations: you can scrub backward, change speed mid-playback, pause for three minutes, and every element is exactly where it should be.

---

## Quick start

**1. Watch the flagship demo**

```bash
open demos/stripe-flow-explainer.html      # macOS
xdg-open demos/stripe-flow-explainer.html  # Linux
start demos\stripe-flow-explainer.html     # Windows
```

Or serve the repo and click through from the browser:

```bash
python3 -m http.server 8080
# http://localhost:8080/demos/stripe-flow-explainer.html
```

**2. Install the skills into your agent**

Pick the file that matches your tool and either copy it to your project root or point your agent at it:

| Agent | Config file | Notes |
| --- | --- | --- |
| Claude Code | `CLAUDE.md` | Project memory, read automatically |
| Cursor | `.cursorrules` | Also works as `.cursor/rules/*.mdc` |
| Windsurf | `.windsurfrules` | Legacy + Cascade rules |
| GitHub Copilot / Codex | `.github/copilot-instructions.md` | Repo-scoped instructions |
| Antigravity, Manus, Qoder, Jarvis, Cue, Grok | `AGENTS.md` | Cross-agent convention |
| Anything else | `.agent/master-prompt.md` | Single source of truth |
| Programmatic clients | `.agent/config.json` | Machine-readable manifest |

All of these are generated from `.agent/master-prompt.md`, so they cannot drift apart.

**3. Generate a video**

```text
Execute Skill #34
```

or

```text
Run skill-21-compound-interest-curve and save it to output/.
```

The agent reads the matching spec in `skills/`, follows its storyboard, and writes a standalone HTML file to `output/`.

---

## The 55 skills

### Category A — Payment Flows & Transactions
Consumer and merchant payment journeys: moving value between people, cards, codes and currencies.

| # | Skill | Concept |
| --- | --- | --- |
| 01 | [P2P Instant Transfer](skills/skill-01-p2p-transfer.md) | Peer-to-peer routing with compliance checkpoints |
| 02 | [Card Swipe Authorization](skills/skill-02-card-swipe-auth.md) | Four-party authorization model in 900 ms |
| 03 | [Split Bill](skills/skill-03-split-bill.md) | Unequal shares, tip apportioning, rounding guards |
| 04 | [QR Scan and Pay](skills/skill-04-qr-scan-pay.md) | Scan, decode, authorize, morph into a receipt |
| 05 | [Cross-Border FX Transfer](skills/skill-05-cross-border-fx.md) | Mid-market rate, spread and fee transparency |
| 06 | [Escrow Release](skills/skill-06-escrow-release.md) | Dual-condition custody release |
| 07 | [Subscription Recurring Billing](skills/skill-07-subscription-recurring.md) | Cycle, soft decline and the dunning ladder |
| 08 | [Refund Reversal](skills/skill-08-refund-reversal.md) | A transaction that runs backward |
| 09 | [NFC Contactless Tap](skills/skill-09-nfc-contactless.md) | Field coupling and token exchange |
| 10 | [Multi-Currency Wallet](skills/skill-10-multi-currency-wallet.md) | Stacked balances and an FX sweep |

### Category B — Banking Infrastructure & Ledgers
The pipes underneath: clearing, ledgers, liquidity, contracts, reconciliation and treasury automation.

| # | Skill | Concept |
| --- | --- | --- |
| 11 | [ACH, Wire and Real-Time Routing](skills/skill-11-ach-wire-routing.md) | Three rails, three clocks, one clearing house |
| 12 | [Immutable Ledger](skills/skill-12-immutable-ledger.md) | Append-only blocks with tamper evidence |
| 13 | [API and Webhook Sync](skills/skill-13-api-webhook-sync.md) | Signed events and idempotent handling |
| 14 | [Liquidity Pool Balancing](skills/skill-14-liquidity-pool.md) | Coverage floors and rebalancing waves |
| 15 | [Smart Contract Execution](skills/skill-15-smart-contract-exec.md) | IF/THEN gates and state mutation |
| 16 | [Automated Reconciliation](skills/skill-16-automated-reconciliation.md) | Auto-matching and exception routing |
| 17 | [Virtual Card Issuance](skills/skill-17-virtual-card-issuance.md) | Wireframe to metal in one timeline |
| 18 | [Open Banking OAuth](skills/skill-18-open-banking-oauth.md) | Consent, handshake, scoped access |
| 19 | [Micro-Investing Round-Up](skills/skill-19-micro-investing-roundup.md) | Spare change into fractional shares |
| 20 | [Treasury Yield Sweep](skills/skill-20-treasury-yield-flow.md) | Overnight sweeps and payroll recall |

### Category C — Wealth, Trading & Analytics
Portfolios, markets and analytics: growth curves, allocation, market microstructure and long-term investing.

| # | Skill | Concept |
| --- | --- | --- |
| 21 | [Compound Interest Curve](skills/skill-21-compound-interest-curve.md) | Exponential growth vs a linear baseline |
| 22 | [Portfolio Rebalance](skills/skill-22-portfolio-rebalance.md) | Drift, bands and corrective trades |
| 23 | [Candlestick Formation](skills/skill-23-candlestick-formation.md) | OHLC anatomy and volume context |
| 24 | [Robo-Advisor Allocation](skills/skill-24-robo-advisor-allocation.md) | One risk slider, many portfolios |
| 25 | [Dividend Reinvestment](skills/skill-25-dividend-drip.md) | DRIP and compounding share count |
| 26 | [Tax-Loss Harvesting](skills/skill-26-tax-loss-harvesting.md) | Loss realization and wash-sale guards |
| 27 | [Fractional Shares](skills/skill-27-fractional-shares.md) | One share into 240 affordable units |
| 28 | [Order Book Depth](skills/skill-28-order-book-depth.md) | Bid/ask walls and imbalance |
| 29 | [Net Worth Aggregator](skills/skill-29-net-worth-aggregator.md) | Assets and liabilities into one number |
| 30 | [Dollar-Cost Averaging](skills/skill-30-dca-simulator.md) | Periodic buys against volatility |

### Category D — Security, Compliance & KYC
Trust and control: identity, cryptography, fraud detection, access policy and defensive architecture.

| # | Skill | Concept |
| --- | --- | --- |
| 31 | [Biometric KYC](skills/skill-31-biometric-kyc.md) | Document capture to verified badge |
| 32 | [Zero-Knowledge Proof](skills/skill-32-zero-knowledge-proof.md) | Proving a claim without the witness |
| 33 | [End-to-End Encryption](skills/skill-33-end-to-end-encryption.md) | Plaintext to cipher and back |
| 34 | [AML Fraud Radar](skills/skill-34-aml-fraud-radar.md) | Streaming monitor and anomaly quarantine |
| 35 | [2FA TOTP Countdown](skills/skill-35-2fa-totp-countdown.md) | Six digits on a 30-second clock |
| 36 | [Tokenization Vault](skills/skill-36-tokenization-vault.md) | PAN in, token out, never back |
| 37 | [Role-Based Access Control](skills/skill-37-role-based-access.md) | Dual control and self-approval blocks |
| 38 | [PCI DSS Shield](skills/skill-38-pci-dss-shield.md) | Four layers, one valid request |
| 39 | [Device Fingerprinting](skills/skill-39-device-fingerprinting.md) | Twenty signals into one hash |
| 40 | [Instant Card Freeze](skills/skill-40-instant-card-freeze.md) | Frost across a virtual card |

### Category E — B2B SaaS, Lending & Credit
Business money: credit, payroll, expenses, equity, revenue operations and the AI copilot layer.

| # | Skill | Concept |
| --- | --- | --- |
| 41 | [Credit Score Gauge](skills/skill-41-credit-score-gauge.md) | A needle, four factors, one plan |
| 42 | [BNPL Installments](skills/skill-42-bnpl-installments.md) | Four payments, six weeks, honest fees |
| 43 | [Invoice Factoring](skills/skill-43-invoice-factoring.md) | 90-day receivable into working capital |
| 44 | [Payroll Distribution](skills/skill-44-payroll-distribution.md) | Treasury to fifty employees at once |
| 45 | [Expense Receipt OCR](skills/skill-45-expense-receipt-ocr.md) | Paper receipt into structured fields |
| 46 | [Revenue-Based Financing](skills/skill-46-revenue-based-financing.md) | Repayment that breathes with revenue |
| 47 | [Cap Table Dilution](skills/skill-47-cap-table-dilution.md) | Percentage down, dollars up |
| 48 | [SaaS MRR Waterfall](skills/skill-48-saas-mrr-waterfall.md) | New, expansion, churn, net ARR |
| 49 | [Usage-Based Billing](skills/skill-49-usage-based-billing.md) | Metered tiers and graduated pricing |
| 50 | [Customs and Trade Finance](skills/skill-50-customs-trade-finance.md) | Letters of credit across checkpoints |
| 51 | [Debt Snowball vs Avalanche](skills/skill-51-debt-snowball-vs-avalanche.md) | Two strategies, one finish line |
| 52 | [Chargeback Dispute Flow](skills/skill-52-chargeback-dispute-flow.md) | Evidence, arbitration, restoration |
| 53 | [Embedded Insurance](skills/skill-53-embedded-insurance.md) | A policy minted at checkout |
| 54 | [Carbon Offset Checkout](skills/skill-54-carbon-offset-checkout.md) | Grams of CO2 into a tree |
| 55 | [AI Financial Copilot](skills/skill-55-ai-financial-copilot.md) | A prompt into a cited forecast |

---

## Anatomy of a skill file

Every file in `skills/` follows the same seven-part contract, which is what makes them executable rather than aspirational:

1. **Skill identity & trigger** — ID, slug, output path, timeline length, accent pair, exact trigger phrases.
2. **Scene-by-scene storyboard** — four scenes with timing windows, narration subtitle, on-screen elements and animation physics.
3. **SVG vector blueprint** — what each vector is for and how to construct it at design scale.
4. **Animation physics** — the specific easing, stagger and conservation rules, plus shared timing constants.
5. **Narration subtitle track** — canonical caption strings as a copy-pasteable array.
6. **Reference data model** — the exact JS object that every number on screen must trace back to.
7. **Acceptance checklist** — ten pass/fail gates including reverse scrubbing, reduced motion and contrast.

---

## The engine

The core design decision: **`render(progress)` is a pure function.** Not a chain of `setTimeout`s, not a set of CSS animations that drift out of sync. Every frame is derived from one normalized value.

```js
class TimelineEngine {
  // progress ∈ [0,1] is the only mutable state that matters
  play()  { /* rAF loop, dt * speed / duration */ }
  pause() { /* cancel rAF, hold the exact frame */ }
  seek(p) { /* clamp, then render */ }
  render(progress) {
    // 1. compute sub-progress bands for each beat
    // 2. derive every position, height, opacity and number
    // 3. write to DOM
  }
}
```

Helpers that make this practical:

```js
const clamp01  = n => n < 0 ? 0 : n > 1 ? 1 : n;
const band     = (p, a, b) => clamp01((p - a) / (b - a));   // sub-animation window
const lerp     = (a, b, t) => a + (b - a) * t;
const easeOut  = t => 1 - Math.pow(1 - t, 3);
const spring   = t => 1 - Math.exp(-6 * t) * Math.cos(9 * t); // damped overshoot
```

Path drawing and packet travel both read from the same curve:

```js
path.setAttribute('pathLength', 1);
path.style.strokeDasharray  = '1 1';
path.style.strokeDashoffset = 1 - easedProgress;        // self-drawing line
const pt = path.getPointAtLength(progress * path.getTotalLength());
packet.style.transform = `translate(${pt.x}px, ${pt.y}px)`;  // travel on the line
```

Because both are derived from `progress`, scrubbing backward rewinds the packet along the same geometry and un-draws the line in perfect sync.

---

## Design system

| Token | Light | Dark |
| --- | --- | --- |
| Canvas | `#F8FAFC` | `#090D16` |
| Surface | `#FFFFFF` | `rgba(255,255,255,0.03)` |
| Border | `#E2E8F0` | `rgba(255,255,255,0.08)` |
| Text | `#0F172A` | `#F8FAFC` |
| Muted | `#64748B` | `#94A3B8` |
| Success | `#10B981` | `#34D399` |
| Primary | `#4F46E5` | `#6366F1` |
| Telemetry | `#06B6D4` | `#22D3EE` |
| Risk | `#F43F5E` | `#FB7185` |

**Type:** Inter / Plus Jakarta Sans for UI, JetBrains Mono for every figure, hash, ticker and identifier.

**Motion:** `cubic-bezier(0.16, 1, 0.3, 1)` for entries, `cubic-bezier(0.65, 0, 0.35, 1)` for symmetric moves, damped springs for tactile settles. `linear` is reserved for two honest uses only: real-time countdowns and ambient rotation.

**Numbers:** `font-variant-numeric: tabular-nums` everywhere. A counter that changes width mid-count reads as a rendering bug.

---

## Repository layout

```
.
├── README.md
├── CLAUDE.md                        # Claude Code
├── AGENTS.md                        # Antigravity, Manus, Qoder, Jarvis, Cue, Grok, Codex
├── .cursorrules                     # Cursor
├── .windsurfrules                   # Windsurf
├── .github/
│   └── copilot-instructions.md      # Copilot / Codex
├── .agent/
│   ├── config.json                  # machine-readable manifest
│   └── master-prompt.md             # single source of truth
├── skills/                          # 55 skill specifications
│   ├── skill-01-p2p-transfer.md
│   ├── ...
│   └── skill-55-ai-financial-copilot.md
├── demos/
│   └── stripe-flow-explainer.html   # flagship reference implementation
├── output/                          # generated videos land here
└── tools/
    ├── generate_skills.py           # regenerates all 55 skill files
    └── data/                        # structured source of truth for the specs
```

### Regenerating the skill files

The 55 specs are generated, not hand-maintained, so cross-cutting changes stay consistent:

```bash
python3 tools/generate_skills.py
```

Edit `tools/data/skills_*.json` to change a storyboard, add a vector or fix a caption, then regenerate. The script asserts uniqueness and completeness of all 55 IDs.

### Syncing the agent configs

After editing `.agent/master-prompt.md`, refresh the copies that agents read from the project root:

```bash
cp .agent/master-prompt.md CLAUDE.md
cp .agent/master-prompt.md AGENTS.md
cp .agent/master-prompt.md .cursorrules
cp .agent/master-prompt.md .windsurfrules
cp .agent/master-prompt.md .github/copilot-instructions.md
```

---

## Writing your own skill

Copy an existing spec and keep the seven-part contract. The parts that actually determine whether the output is good:

- **Scene windows must be normalized fractions**, not raw milliseconds. Raw timings break the moment you change the total duration.
- **State a conservation rule.** If money moves, the total must not change. If a packet travels, both endpoints must agree. Reviewers check this first.
- **Name the derived figures.** "Closing MRR equals opening plus additions minus subtractions" is testable; "show some numbers" is not.
- **Give the final frame a job.** The last 800 ms should hold on a complete, readable statement — not on a mid-transition.

---

## Quality gates

Every generated demo is expected to pass these before it ships:

- [ ] Scrubbing from 100% to 0% leaves every element exactly at its initial state
- [ ] Pause freezes all motion including ambient loops and countdowns
- [ ] `1.5x` and `2x` do not desynchronize any sub-animation
- [ ] Light and dark themes both pass 4.5:1 on body text
- [ ] Every visible number traces back to the reference data model
- [ ] The final frame holds for at least 800 ms
- [ ] No external requests beyond the Tailwind and font CDNs
- [ ] Renders correctly at 390, 768, 1280 and 1920 px
- [ ] `prefers-reduced-motion: reduce` collapses transitions to fades
- [ ] No fabricated full PANs, real document numbers or named individuals

---

## License

GPL-3.0. See [LICENSE](LICENSE).

Figures, rates and identifiers in every skill are illustrative and synthetic. Nothing here is financial, tax, or legal advice.
