# Break-Even & Unit Economics — `erp-order-sync`

> Model unit = **one active distributor account** (ERP-connected org), not seat. Cannabis distributors process bursty, multi-format inbound orders (PDF POs, email free-text, faxed sheets, EDI 850, spreadsheet attachments). Costs scale with **orders parsed**, not headcount. Assumed baseline: **median active account = 1,800 order documents/mo**, ~3.2 line-items each.

## 1. Cost per active user (monthly, USD)

| Cost driver | Basis | Volume/account/mo | Unit cost | $/account/mo |
|---|---|---|---|---|
| **LLM parse/extract** | Vision+text extraction, structured-output, 1 retry budget | 1,800 docs × ~6.5K tok in / 1.2K out | ~$0.0042/doc blended (Haiku-tier vision + Sonnet escalation on 12% low-confidence) | **$7.56** |
| **Confidence re-rank / validation** | Embedding match SKU↔catalog, dedupe | 5,760 line-items × embed | ~$0.00002/item | **$0.12** |
| **Compute (app/API/workers)** | Async queue, ERP push, webhooks | ~0.15 vCPU avg, autoscale | $0.034/vCPU-hr × 110 hr | **$3.74** |
| **Storage** | Raw docs (7-yr compliance retention) + parsed JSON + audit log | ~9.5 GB cumulative yr-1 avg | $0.023/GB-mo (S3 std-IA tiered) | **$0.22** |
| **Bandwidth** | Doc ingest + ERP API egress | ~14 GB | $0.09/GB egress (ingest free) | **$1.26** |
| **Error/human-in-loop tooling** | Support + exception-review infra amortized | flat | — | **$1.10** |
| **COGS subtotal** | | | | **≈ $14.00** |

- **Marginal cost per account ≈ $14/mo** at median volume.
- **Heavy account (8,000 docs/mo):** ~$48/mo COGS — still <15% of any paid tier.
- **Gross margin target:** 82–88% across tiers (cannabis ERP buyers tolerate premium pricing; price is anchored to order-entry labor displaced, not to compute).

> Key lever: **only 12% of docs escalate to the expensive model.** Hold that confidence-routing threshold or COGS doubles. This is the single most important number to monitor.

## 2. Pricing tiers

Anchored to **labor displaced**: 1 order-entry clerk in cannabis distribution ≈ $3,400–4,200/mo fully loaded; the tool replaces 0.4–1.5 FTE per account.

| Tier | $/mo | Doc cap | Target buyer | Features |
|---|---|---|---|---|
| **Starter** | **$299** | 750 docs/mo | Single-state micro-distributor, 1–2 ERP feeds | PDF/email/spreadsheet parse, 1 ERP connector (QuickBooks/Cova/Distru), confidence flags, manual review queue, CSV export |
| **Growth** | **$899** | 3,000 docs/mo | Multi-account distributor | Everything in Starter + EDI 850/810, 3 connectors, SKU auto-mapping, metrc/state-traceability field mapping, dup-PO detection, Slack/email exception alerts, API |
| **Scale** | **$2,400** | 12,000 docs/mo | Regional MSO / multi-state operator | Everything + unlimited connectors, SSO/RBAC, audit-grade 7-yr retention, custom field rules, dedicated parse model fine-tune, SLA 99.9%, priority support |

- **Overage:** $0.09/doc above cap (≈6.5× COGS — protects margin on volume spikes).
- **Annual:** 2 months free (16.7% discount) — push hard; cannabis cashflow is lumpy but churn drops sharply on annual.
- **No free tier.** Offer a **14-day pilot on real inbox** instead — proves accuracy on the buyer's own messy POs, which is the only thing that converts this segment.

## 3. CAC

B2B niche-vertical, founder-led + outbound. Cannabis = relationship/compliance-driven, conference-heavy, low digital-ad efficacy.

| Channel | Blended CAC | Notes |
|---|---|---|
| Founder outbound + warm intro (distro associations, ERP-vendor referrals) | **$650–1,100** | Primary motion yr-1 |
| Conference / trade (MJBizCon, state distributor assns) | **$1,400–2,200** | High-intent, slow cycle |
| ERP-marketplace co-sell (Distru, Cova, Canix) | **$400–800** | Best long-term channel — prioritize 2 integrations to unlock |

**Blended CAC range: $700–1,500.** Plan at **$1,100**.

## 4. LTV

- **Logo churn:** 2.5%/mo early → stabilize ~1.6%/mo (vertical ERP tools are sticky once order flow runs through them). Avg lifetime ≈ **50 months**.
- **ARPA:** blended **$780/mo** (mix skews Growth; ~55% Growth, 30% Starter, 15% Scale).
- **Gross margin:** 85%.

**LTV = $780 × 0.85 × 50 ≈ $33,150 per account.**

| Metric | Value |
|---|---|
| LTV : CAC | **~30:1** (target ≥3:1 — wildly healthy; signals room to spend faster on CAC) |
| CAC payback | **~1.7 months** of gross profit |

> 30:1 means you're under-investing in acquisition, not over-. The constraint is sales velocity / integration count, not economics.

## 5. Break-even users count

| Cost base (monthly) | Estimate |
|---|---|
| Fixed opex (2 FTE eng + founder draw + tooling/infra base + ERP partner fees) | **~$38,000/mo** |
| Contribution margin per account (ARPA $780 × 85%) | **$663** |

**Break-even = $38,000 ÷ $663 ≈ 58 active accounts.**

- Lean variant (founder unpaid, 1 eng, ~$19K fixed): **~29 accounts.**
- At blended ARPA, ~58 accounts is realistically reached in **9–14 months** given the integration-gated sales motion.

## 6. Path to $10K MRR

Fastest credible route — **Growth tier is the engine:**

| Scenario | Mix | Accounts | MRR |
|---|---|---|---|
| **Recommended** | 11 × Growth ($899) + 1 × Scale ($2,400) | **12** | **$12,289** |
| Pure-Growth | Growth only | **12** | **$10,788** |
| Starter-heavy (avoid) | Starter only | **34** | **$10,166** |

**Target: 12 accounts, Growth-anchored → ~$10–12K MRR.**

- Why Growth, not Starter: Starter-only needs **34 logos** for the same MRR at **2.8× the CAC spend and support load** — wrong motion for a 12% margin difference. Sell Growth as default; Starter is only a down-sell to close hesitant micro-distributors.
- **Milestones:** $10K MRR ≈ 12 accounts (months 4–6) → break-even ≈ 58 accounts (~$45K MRR) → 2 ERP-marketplace integrations live is the unlock that drops CAC and accelerates from 12 → 58.
- **Riskiest assumption to validate first:** the 12% model-escalation rate on *real* cannabis PO formats. If accuracy forces 35%+ escalation, COGS triples and Starter goes margin-negative — kill or reprice Starter before scaling.