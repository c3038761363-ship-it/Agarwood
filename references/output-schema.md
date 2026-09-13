# Agarwood Prospecting Output Schema

Default output is a single JSON object. If the user explicitly asks for a table/CSV/Excel, the agent may transform the same fields after qualification.

```json
{
  "version": "agarwood-prospect-v1",
  "summary": {
    "target": "short target description",
    "markets": ["Australia"],
    "productFamilies": ["agarwood incense", "incense burners"],
    "customerTypes": ["distributor", "wholesaler"],
    "requestedCount": 10,
    "rawFound": 0,
    "accepted": 0,
    "skipped": 0,
    "historyStatus": "loaded | initialized | unavailable | external_only",
    "ledgerPath": "台账/seen.json",
    "noResultReason": ""
  },
  "opportunities": [
    {
      "company": "Company name",
      "country": "Country",
      "website": "https://official.example",
      "customerType": "distributor | wholesaler | brand | retailer | importer | other",
      "business": "What the company sells/does",
      "relevantProductsObserved": ["incense", "sandalwood"],
      "fitScore": 0,
      "priority": "priority_A | priority_B | review_needed",
      "fitReasons": ["Evidence-backed reason"],
      "productGaps": ["Gap or complementary opportunity"],
      "recommendedProducts": ["agarwood incense sticks", "coil incense burner"],
      "outreachAngles": ["Specific non-generic development angle"],
      "contact": "Department/person or empty string",
      "contactInfo": {
        "email": "",
        "phone": "",
        "whatsapp": ""
      },
      "keyContacts": [],
      "confidence": 0,
      "uncertainPoints": [],
      "dedupKey": "domain:example.com",
      "dedupStatus": "new | rechecked_changed | history_unavailable",
      "lastSeenAt": "",
      "nextAction": "Concrete next sales action",
      "sources": [
        {
          "url": "https://source.example/page",
          "title": "Source title",
          "sourceType": "official | registry | trade_show | reputable_directory | search_result | social_public | weak",
          "evidence": "What this source confirms",
          "fields": ["identity", "business", "contact", "product"]
        }
      ]
    }
  ],
  "skipped": [
    {
      "company": "Skipped company",
      "reason": "duplicate | no_contact | wrong_business | weak_evidence | inactive | marketplace_only | wrong_market | other",
      "detail": "Concrete explanation",
      "sourceUrl": ""
    }
  ],
  "failures": [
    {
      "stage": "search | verification | extraction | timeout | configuration",
      "reason": "What failed",
      "suggestion": "How to adjust"
    }
  ]
}
```

Rules:
- An accepted opportunity requires a confirmed business identity, meaningful industry fit, and at least one source-backed public company contact method.
- Do not guess email addresses, websites, WhatsApp numbers, people, or product availability.
- `fitScore` follows `agarwood-icp.md`.
- `recommendedProducts` must be tied to observed catalog/business evidence.
- `outreachAngles` must be specific enough to support a personalized development email; avoid generic claims such as "we offer high quality and good price".
- Every accepted company must have at least one source; prefer an official source plus one independent source when practical.
