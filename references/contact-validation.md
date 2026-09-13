# Lfind Contact and Person Validation

Use this reference whenever a GoodJob result includes company contacts, procurement people, decision makers, WhatsApp, or LinkedIn.

## Company contact evidence

Prefer sources in this order:

1. The company's official website, contact page, product page, quotation page, or official PDF.
2. An official registry, chamber, tender portal, or trade-show exhibitor record.
3. A reputable business directory that clearly identifies the company.
4. A public search-result snippet only when the underlying page is accessible or the snippet clearly shows the company/value relationship.

For every accepted company contact, preserve the exact public value and record:

- `status`: `source_confirmed` only when the exact value appears in the cited source; use `conflicting` when sources disagree and `unverified` when the relationship is unclear.
- `sourceUrl`, `sourceTitle`, and `sourceType`.
- `evidence`: a concise page label or context such as “official contact page lists Sales: sales@example.com”. Do not invent or reconstruct hidden values.
- `checkedAt`: the lookup date in `YYYY-MM-DD` format when known.

Do not treat a guessed email pattern, a company-domain assumption, a marketplace seller name, or an unlabeled phone number as proof. A phone number may be copied exactly, but it must remain a phone value unless the source explicitly labels it WhatsApp or WhatsApp Business.

## Procurement and decision-maker discovery

Only add a `keyContacts` entry when a public source connects the person's exact name to the company and states a business role. Useful role terms include Procurement, Purchasing, Sourcing, Supply Chain, Buyer, Commercial, Sales Director, Product Manager, Automation Manager, and Engineering Manager. A generic employee listing is not enough to call someone a buyer.

Allowed public sources include official team/contact pages, public tender or procurement documents, trade-show exhibitor catalogs, chamber pages, and public LinkedIn profile pages or search snippets that are visible without login. Do not log in, bypass access controls, scrape private profiles, or collect personal data unrelated to the business purpose.

For each person, verify independently:

- `name` and `role` from the cited source;
- `linkedinUrl` only when the exact public profile URL is visible;
- `whatsapp` only when the exact number is explicitly labeled WhatsApp/WhatsApp Business;
- `email` or `phone` only when the exact public business value is shown.

If the source provides a name but not a role, keep the person only as an unverified lead or omit the entry; never upgrade the person to “purchaser” by inference. If no reliable person is found, return an empty `keyContacts` array and state “no public procurement/decision contact found” in `uncertainPoints` or `personFinding.evidence`.

## Confidence guidance

- 80–100: company identity, country, business fit, website, and company contact are strongly supported; a person may still be absent.
- 55–79: useful category-fit prospect, but Longtec/TR200H relationship or a key field remains unproven.
- Below 55: retain only when the candidate is still actionable and the uncertainty is explicit.

Never increase confidence merely because a LinkedIn profile or phone number exists; confidence reflects identity, role, source quality, and fit together.

## Contact-first qualification

For normal prospecting, contactability is the primary gate and buying intent is a secondary ranking signal. A well-matched distributor with a published company email or phone can be accepted as `review_needed` even when no tender or open purchase notice exists. Keep the distinction explicit:

- `published`: the value is visible in a public source;
- `cross_source`: the same value is independently confirmed in two sources;
- `reachability_unchecked`: no email delivery or phone call was performed;
- `invalid_or_bounced`: an authorized outreach or verification attempt failed.

Never report `reachability_unchecked` as a successful contact. If no public company channel is available, the candidate should normally be skipped rather than padded into the accepted list.
