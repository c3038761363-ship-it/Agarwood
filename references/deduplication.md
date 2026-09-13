# Lfind Cross-run Deduplication

Use this reference before accepting any candidate when GoodJob supplies an existing-lead export or when a local history ledger is enabled.

## Deterministic key order

Build one stable `dedupKey` per company using the strongest available identity signal:

1. `domain:<normalized official domain>`
2. `email:<normalized company email>` or `phone:<digits with country code>`
3. `namecountry:<normalized legal/trading name>|<normalized country>`

Normalize case, whitespace, punctuation, URL protocol, `www.`, phone separators, and common legal suffixes. Keep the original company name, phone, email, and URL in the opportunity; normalization is only for matching.

## Matching rules

- Exact domain match is a duplicate even if the trading name differs.
- Exact company email or phone match is a duplicate unless the source clearly shows a different legal entity or branch.
- Name + country is a duplicate only when the legal/trading name is unambiguous. Do not merge similar names across countries.
- Fuzzy or translated-name matching requires two supporting identity signals, such as the same domain plus address or the same phone plus legal name.
- Prefer one parent-company record with branch locations in notes unless the user explicitly requests branch-level leads.

## History behavior

- Read external GoodJob customer/lead data first. Read the canonical local `台账/seen.json` before web search and record its status in `summary.historyStatus`.
- Record every queried candidate, including skipped hits, with `dedupKey`, company, country, domain, last-seen date, last status, and source URLs. Do not store unverified personal contacts in the ledger.
- Skip an exact match when no material evidence changed and use `duplicate_existing_lead` with the matched key and last-seen date in `skipped.detail`.
- Recheck a match when it is older than 90 days or when a new source suggests a changed website, contact, role, product line, or buying signal. Emit it only as `rechecked_changed` when the new evidence is material.
- Do not update the ledger merely because a candidate was found. Only a CRM import confirmation may change `lastStatus` to `crm_imported`. Use `scripts/sync_ledger.py` after CRM confirms successful imports.
- If the ledger cannot be read or written, set `historyStatus` to `unavailable`, mark each row `history_unavailable`, and state that cross-run deduplication could not be guaranteed.

## Local ledger shape

Keep the canonical `台账/seen.json` as a small JSON file:

The older `state/seen.json` file is retained only for backward compatibility and must not be treated as the source of truth after this update.

```json
{
  "version": "goodjob-lfind-seen-v1",
  "records": [
    {
      "dedupKey": "domain:example.com",
      "company": "Example Co., Ltd.",
      "country": "Thailand",
      "domain": "example.com",
      "lastSeenAt": "2026-08-28",
      "lastStatus": "crm_imported",
      "sourceUrls": ["https://example.com/contact"]
    }
  ]
}
```

Keep the ledger append/update-only for normal runs. Do not delete history merely because a source is temporarily unavailable. The synchronization helper accepts a GoodJob result plus a CRM confirmation file, for example:

```bash
python3 scripts/sync_ledger.py \
  --result work/lfind-result.json \
  --crm-import work/crm-import-confirmed.json
```

The confirmation file may contain `{"imported": [{"dedupKey": "domain:example.com", "crmLeadId": "123"}]}`. Only entries marked imported/success/created/synced are written to the ledger.
