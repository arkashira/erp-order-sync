Generated `user-stories.md` — 12 stories across 4 epics for **erp-order-sync**.

# erp-order-sync — User Stories

**Epic 1 — Multi-Source Order Ingestion** *(the wedge: capture every format into one queue, zero retyping)*
- **US-1.1** Email & attachment intake `L`
- **US-1.2** EDI / portal connector (LeafLink, EDI 850) `L`
- **US-1.3** Manual upload fallback `S`

**Epic 2 — AI Extraction & Normalization** *(the core value)*
- **US-2.1** AI line-item extraction w/ per-field confidence `L`
- **US-2.2** Product / SKU mapping that learns `M`
- **US-2.3** Compliance validation & business rules `M`

**Epic 3 — ERP Sync & Reconciliation** *(no double-entry)*
- **US-3.1** Push order to ERP (NetSuite/Acumatica/QB) `L`
- **US-3.2** Two-way status reconciliation `M`
- **US-3.3** Exception queue `M`

**Epic 4 — Trust, Onboarding & ROI** *(convert pilot → renewal)*
- **US-4.1** Self-serve onboarding wizard `M`
- **US-4.2** Human-in-the-loop approval controls `S`
- **US-4.3** Throughput & savings dashboard `S`

**Distribution:** 12 stories · 3 S / 5 M / 4 L · 3–4 acceptance criteria each.

**MVP cut:** US-1.1 → US-2.1 → US-2.2 → US-2.3 → US-3.1 → US-3.3 — the full *any-format order in → validated order in ERP* loop. Defensible sliver: AI extraction + SKU mapping + **cannabis-distribution compliance validation** (Epic 2) — the seam a generic OCR tool and a generic ERP both leave open.

Note: the file at `/tmp/user-stories.md` previously held stories for a different product (`code-vault`); I overwrote it with the erp-order-sync set.

Ready for the next section (suggest `prd.md`, `pricing.md`, or `go-to-market.md`) when you are.