#!/usr/bin/env python3
"""Synchronize CRM-confirmed Lfind imports into the local deduplication ledger.

The script intentionally records company-level identity only. It does not copy
keyContacts or other personal fields into the ledger.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


LEGAL_SUFFIXES = {
    "co",
    "company",
    "corporation",
    "corp",
    "inc",
    "ltd",
    "limited",
    "llc",
    "plc",
    "gmbh",
    "pte",
    "sdn",
    "bhd",
}


def norm_text(value: Any) -> str:
    text = str(value or "").casefold()
    text = re.sub(r"[^\w\u0080-\uffff]+", " ", text, flags=re.UNICODE)
    tokens = [token for token in text.split() if token not in LEGAL_SUFFIXES]
    return " ".join(tokens)


def norm_domain(value: Any) -> str:
    raw = str(value or "").strip()
    if not raw:
        return ""
    parsed = urlparse(raw if "://" in raw else f"https://{raw}")
    host = (parsed.netloc or parsed.path).split("@")[-1].split(":")[0].casefold()
    if host.startswith("www."):
        host = host[4:]
    return host.rstrip(".")


def norm_contact(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(value or "").casefold())


def derive_key(opportunity: dict[str, Any]) -> str:
    explicit = str(opportunity.get("dedupKey") or "").strip()
    if explicit:
        return explicit
    domain = norm_domain(opportunity.get("website") or opportunity.get("domain"))
    if domain:
        return f"domain:{domain}"
    info = str(opportunity.get("contactInfo") or "")
    for token in re.split(r"[;,|]", info):
        token = token.strip()
        normalized = norm_contact(token)
        if "@" in token:
            return f"email:{normalized}"
        digits = re.sub(r"\D", "", token)
        if len(digits) >= 7:
            return f"phone:{digits}"
    name = norm_text(opportunity.get("company"))
    country = norm_text(opportunity.get("country"))
    return f"namecountry:{name}|{country}"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def imported_items(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        values = payload
    elif isinstance(payload, dict):
        values = payload.get("imported") or payload.get("leads") or payload.get("records") or []
    else:
        values = []
    result: list[dict[str, Any]] = []
    for value in values:
        if isinstance(value, str):
            result.append({"dedupKey": value})
        elif isinstance(value, dict):
            status = str(value.get("status") or "imported").casefold()
            if status in {"imported", "success", "created", "synced"}:
                result.append(value)
    return result


def source_urls(opportunity: dict[str, Any]) -> list[str]:
    urls: list[str] = []
    for source in opportunity.get("sources") or []:
        if isinstance(source, dict) and source.get("url"):
            urls.append(str(source["url"]))
    report = opportunity.get("searchReport") or {}
    for source in report.get("checkedSources") or []:
        if isinstance(source, dict) and source.get("url"):
            urls.append(str(source["url"]))
    return sorted(set(urls))


def atomic_write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent), text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--result", required=True, type=Path, help="Agarwood Prospecting result JSON")
    parser.add_argument("--crm-import", required=True, type=Path, help="CRM confirmation JSON")
    parser.add_argument(
        "--ledger",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "台账" / "seen.json",
        help="Ledger path (defaults to the skill's 台账/seen.json)",
    )
    parser.add_argument("--date", default=date.today().isoformat(), help="Ledger date YYYY-MM-DD")
    args = parser.parse_args()

    result_payload = load_json(args.result)
    crm_payload = load_json(args.crm_import)
    opportunities = result_payload.get("opportunities") if isinstance(result_payload, dict) else []
    opportunities = opportunities if isinstance(opportunities, list) else []
    confirmations = imported_items(crm_payload)
    if not confirmations:
        raise SystemExit("No CRM-confirmed imported records found; ledger was not changed.")

    ledger = load_json(args.ledger) if args.ledger.exists() else {"version": "agarwood-prospect-seen-v1", "records": []}
    records = ledger.get("records") if isinstance(ledger, dict) else []
    records = records if isinstance(records, list) else []
    by_key = {str(record.get("dedupKey")): record for record in records if isinstance(record, dict) and record.get("dedupKey")}
    by_domain = {norm_domain(record.get("domain")): record for record in records if isinstance(record, dict) and norm_domain(record.get("domain"))}
    by_name_country = {
        f"{norm_text(record.get('company'))}|{norm_text(record.get('country'))}": record
        for record in records
        if isinstance(record, dict) and record.get("company")
    }

    updated = 0
    unmatched = 0
    for confirmation in confirmations:
        key = str(confirmation.get("dedupKey") or "").strip()
        opp = next((item for item in opportunities if isinstance(item, dict) and derive_key(item) == key), None)
        if opp is None and confirmation.get("domain"):
            domain = norm_domain(confirmation.get("domain"))
            opp = next((item for item in opportunities if isinstance(item, dict) and norm_domain(item.get("website")) == domain), None)
        if opp is None and confirmation.get("company"):
            match_key = f"{norm_text(confirmation.get('company'))}|{norm_text(confirmation.get('country'))}"
            opp = next((item for item in opportunities if isinstance(item, dict) and f"{norm_text(item.get('company'))}|{norm_text(item.get('country'))}" == match_key), None)
        if opp is None:
            unmatched += 1
            continue

        key = derive_key(opp)
        domain = norm_domain(opp.get("website"))
        record = by_key.get(key) or (by_domain.get(domain) if domain else None) or by_name_country.get(f"{norm_text(opp.get('company'))}|{norm_text(opp.get('country'))}")
        if record is None:
            record = {"dedupKey": key}
            records.append(record)
        record.update(
            {
                "dedupKey": key,
                "company": opp.get("company", ""),
                "country": opp.get("country", ""),
                "domain": domain,
                "lastSeenAt": args.date,
                "lastStatus": "crm_imported",
                "sourceUrls": source_urls(opp),
            }
        )
        if confirmation.get("crmLeadId") is not None:
            record["crmLeadId"] = str(confirmation["crmLeadId"])
        by_key[key] = record
        if domain:
            by_domain[domain] = record
        by_name_country[f"{norm_text(opp.get('company'))}|{norm_text(opp.get('country'))}"] = record
        updated += 1

    ledger = {"version": "agarwood-prospect-seen-v1", "records": records}
    atomic_write(args.ledger, ledger)
    print(json.dumps({"ledger": str(args.ledger), "updated": updated, "unmatched": unmatched}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

