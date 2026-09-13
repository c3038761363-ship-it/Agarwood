---
name: agarwood-prospecting
description: Find, verify, qualify, deduplicate, and prioritize overseas B2B prospects for agarwood, incense, oud, aromatherapy, spiritual-fragrance products, agarwood bracelets, raw agarwood material, and incense burners using public sources. Use when the user asks to find overseas customers, distributors, wholesalers, importers, incense brands, aromatherapy businesses, oud/agarwood sellers, spiritual-goods companies, or source-backed contact information for agarwood export business. Do not use private/logged-in/CAPTCHA-gated data or guess contacts.
---

# Agarwood Prospecting

This skill is a public-source overseas B2B prospecting workflow specialized for agarwood and adjacent fragrance/incense markets.

Its job is not merely to return many company names. Its job is to produce a small, verifiable, contactable, deduplicated and prioritized pipeline that a sales operator can actually develop.

## Core principles

- Keep the original reliable prospecting backbone: search -> verify -> qualify -> contact validation -> deduplicate -> prioritize -> output.
- Optimize for relevance and contactability, not raw quantity.
- Use only public accessible business information. Never log in, bypass CAPTCHA/access controls, use leaked/private data, guess emails, or infer WhatsApp from a normal phone number.
- Prefer official company pages, official catalogs, public trade-show/exhibitor records, chambers/registries and reputable directories. Search snippets and marketplaces can discover candidates but are not sufficient proof by themselves.
- If a fact is uncertain, say so. Never fabricate product gaps, buyer identities, company scale, official domains or contact values.
- A company may be highly relevant but still be skipped if no public contact method can be source-confirmed.

## Default scope

When the user does not specify otherwise:
- accepted target per run: 10
- hard cap per run: 30 accepted companies
- raw search cap: 100 hits
- target priority: importer/distributor/wholesaler -> established brand -> established retailer
- required accepted contact: public source-backed company email, phone, or explicitly labeled WhatsApp

## Workflow

1. Parse the request into target market(s), product family, customer type, desired count, exclusions and any already-developed companies/domains.
2. Read `references/agarwood-icp.md` and translate the request into an ICP. If the user gives a narrow product (for example agarwood bracelets), weight that product more heavily rather than searching every agarwood category equally.
3. Read `references/search-playbook.md` and build multiple search routes. Do not rely on one English keyword pattern. Use direct agarwood/oud routes, incense-channel routes, adjacent fragrance routes, local-language wording and reputable trade/directory sources when useful.
4. Load external duplicate lists supplied by the user and the local `台账/seen.json` ledger. Generate deterministic deduplication keys. If history cannot be loaded, mark history as unavailable; never promise that repeats are impossible.
5. Collect roughly 3-5x the requested count, up to the raw-hit cap. Discovery evidence can be broad, but acceptance must be strict.
6. Verify each serious candidate:
   - real company/business identity
   - target country/market
   - official website/domain when available
   - actual product/business relevance
   - public source-backed business contact
   - evidence supporting the fit
7. Apply the ICP scoring from `references/agarwood-icp.md`. Reject or deprioritize companies that are only weakly adjacent, marketplace-only, inactive, irrelevant, or unsupported by credible sources.
8. Perform product-gap analysis. Compare what the candidate visibly sells with the relevant agarwood product families. Identify complementary opportunities without claiming catalog absence beyond what was actually reviewed.
9. Create 1-3 concrete `outreachAngles` for each accepted company. These should explain why that particular company may care, e.g. expanding a narrow incense range with agarwood variants, adding coil/chip burners, adding agarwood bracelets, or complementing oud/bakhoor with East Asian agarwood incense.
10. Validate contact data using `references/contact-validation.md`. Never guess email patterns. A phone number is not WhatsApp unless publicly labeled as such. Public decision makers are optional and must have both name and business role source-backed.
11. Deduplicate using `references/deduplication.md`: domain first, then exact contact, then normalized company name + country. Skip unchanged existing matches. Recheck only when meaningful new business/contact evidence exists.
12. Prepare results using `references/output-schema.md`. Default to strict JSON for machine reuse; if the user explicitly requests a human table, CSV, Excel or CRM-ready structure, transform the same verified fields without weakening the qualification rules.
13. Do not treat discovery as successful CRM import. Update the local ledger only after the user/system confirms the companies were actually accepted/imported/used. The included ledger script may be adapted for this confirmation step.

## Research quality bar

For an accepted company, aim to know:
- who they are;
- what relevant products they actually sell;
- why they fit the target ICP;
- how the user can contact them using a public business channel;
- which agarwood products are most plausible for them;
- what personalized development angle should be used;
- what remains uncertain.

A list of names without this evidence is incomplete.

## References

- ICP and scoring: `references/agarwood-icp.md`
- Search routes: `references/search-playbook.md`
- Contact/person verification: `references/contact-validation.md`
- Deduplication: `references/deduplication.md`
- Output structure: `references/output-schema.md`
