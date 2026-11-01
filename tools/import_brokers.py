#!/usr/bin/env python3
"""Import / merge broker index data into Mike Levy Law.

Sources (any combination):
  - forensicsou js/brokers-data.js  (default path, fields n/s/t/d)
  - --source PATH   another brokers-data.js
  - --json PATH     JSON array of Mike Levy Law–shaped broker objects
  - --jsonl PATH    one JSON object per line (site or forensic shape)
  - tools/inbox/*.json|*.jsonl   drop files here; --inbox picks them up

Default mode is --merge: add new slugs, refresh base fields from source,
preserve curated enrichments (aliases, clones, timeline, fundFlow, …).

  python3 tools/import_brokers.py --all
  python3 tools/import_brokers.py --merge --json tools/inbox/batch.json
  python3 tools/import_brokers.py --replace --all   # full rebuild from source
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from datetime import date, timedelta
from pathlib import Path

FORENSIC = Path("/Users/user/Documents/forensicsou-main 4")
STIRLING = Path("/Users/user/Desktop/STIRLING")
OUT_DIR = STIRLING / "company-broker-index" / "data"
INBOX = STIRLING / "tools" / "inbox"
DEFAULT_LIMIT = 60

# Survives merge/replace-from-source so hand edits are not wiped
# clones: only domains we also index, or that appear in documented stories — never invented lookalikes
CURATED_KEYS = (
    "aliases",
    "clones",
    "officialDomain",
    "timeline",
    "fundFlow",
    "kw_extra",
    "tags",
    "caseType",
    "category",
)

COUNTRIES = [
    "South Korea", "Singapore", "United Arab Emirates", "Malaysia", "Thailand",
    "Vietnam", "Philippines", "Indonesia", "Japan", "Taiwan",
    "India", "Nigeria", "Kenya", "Ghana", "South Africa",
    "Brazil", "Mexico", "Chile", "Colombia", "Poland",
    "Romania", "Czech Republic", "Portugal", "Spain", "Italy",
    "Germany", "Netherlands", "Sweden", "Norway", "Australia",
    "New Zealand", "Canada", "United Kingdom", "United States", "Ireland",
    "Hong Kong", "Saudi Arabia", "Qatar", "Egypt", "Turkey",
]


def stable_int(s: str, mod: int) -> int:
    return int(hashlib.sha256(s.encode("utf-8")).hexdigest()[:8], 16) % mod


def load_js_assign(path: Path, assign: str):
    text = path.read_text(encoding="utf-8")
    m = re.search(rf"{re.escape(assign)}\s*=\s*(\{{.*\}}|\[.*\])\s*;?\s*$", text, re.S)
    if not m:
        raise SystemExit(f"Could not parse {path}")
    return json.loads(m.group(1))


def write_js_assign(path: Path, assign: str, value, header: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"{header}\n{assign} = {json.dumps(value, ensure_ascii=False, indent=2)};\n",
        encoding="utf-8",
    )


def load_forensic_array(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    m = re.search(r"=\s*(\[.*\])\s*;?\s*$", text, re.S)
    if not m:
        raise SystemExit(f"Could not parse forensic array in {path}")
    return json.loads(m.group(1))


def load_tp_map(research_dir: Path) -> dict[str, dict]:
    path = research_dir / "_review_tp2.jsonl"
    out: dict[str, dict] = {}
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        o = json.loads(line)
        slug = o.get("slug")
        if slug and o.get("ok"):
            out[slug] = o
    return out


def tier_to_stirling(tier: str) -> dict:
    if tier == "scam":
        return {"status": "active", "category": "brokers", "caseType": "standard", "risk": "high"}
    if tier == "dead":
        return {"status": "closed", "category": "companies", "caseType": "standard", "risk": "high"}
    if tier in ("clone", "impersonation"):
        return {"status": "review", "category": "brokers", "caseType": "standard", "risk": "high"}
    return {"status": "review", "category": "brokers", "caseType": "standard", "risk": "medium"}


_SLUG_MARKET = {
    "au": "Australia",
    "uk": "United Kingdom",
    "us": "United States",
    "de": "Germany",
    "fr": "France",
    "es": "Spain",
    "it": "Italy",
    "nl": "Netherlands",
    "nz": "New Zealand",
    "sg": "Singapore",
    "hk": "Hong Kong",
    "ae": "United Arab Emirates",
    "ca": "Canada",
    "jp": "Japan",
    "in": "India",
    "za": "South Africa",
    "ie": "Ireland",
    "ch": "Switzerland",
    "pl": "Poland",
    "br": "Brazil",
    "mx": "Mexico",
    "pt": "Portugal",
    "se": "Sweden",
    "no": "Norway",
    "dk": "Denmark",
    "fi": "Finland",
    "be": "Belgium",
    "at": "Austria",
    "th": "Thailand",
    "my": "Malaysia",
    "ph": "Philippines",
    "vn": "Vietnam",
    "id": "Indonesia",
    "tw": "Taiwan",
    "tr": "Turkey",
    "kr": "South Korea",
    "eu": "European Union",
}

# Multi-market brands: regional hostname / "Brand AU" means brand + market, not a new company
_KNOWN_REGIONAL = {
    "binance": ("Binance", "binance.com"),
    "bybit": ("Bybit", "bybit.com"),
    "coinbase": ("Coinbase", "coinbase.com"),
    "kraken": ("Kraken", "kraken.com"),
    "okx": ("OKX", "okx.com"),
    "bitget": ("Bitget", "bitget.com"),
    "kucoin": ("KuCoin", "kucoin.com"),
    "etoro": ("eToro", "etoro.com"),
    "revolut": ("Revolut", "revolut.com"),
    "santander": ("Santander", "santander.com"),
    "fxpro": ("FxPro", "fxpro.com"),
    "ferratum": ("Ferratum", "ferratum.com"),
    "bitcoin": ("Bitcoin.com", "bitcoin.com"),
    "betano": ("Betano", "betano.com"),
    "rabobank": ("Rabobank", "rabobank.com"),
    "plus500": ("Plus500", "plus500.com"),
    "pepperstone": ("Pepperstone", "pepperstone.com"),
    "exness": ("Exness", "exness.com"),
    "oanda": ("OANDA", "oanda.com"),
    "avatrade": ("AvaTrade", "avatrade.com"),
    "xm": ("XM", "xm.com"),
    "ig": ("IG", "ig.com"),
}

_COUNTRY_SUFFIX = re.compile(
    r"^(?P<brand>.+?)[\s,/-]+(?P<label>"
    r"Australia|United Kingdom|UK|United States|USA|US|Germany|DE|France|FR|"
    r"Spain|ES|Italy|IT|Netherlands|NL|New Zealand|NZ|Singapore|SG|Hong Kong|HK|"
    r"Canada|CA|UAE|AE|Japan|JP|India|IN|South Africa|ZA|Ireland|IE|Switzerland|CH|"
    r"Thailand|TH|Malaysia|MY|Portugal|PT|Poland|PL|Sweden|SE|Belgium|BE|Austria|AT|"
    r"Brazil|BR|Mexico|MX|Turkey|TR|Philippines|PH|Vietnam|VN|Indonesia|ID|Taiwan|TW|"
    r"European Union|EU"
    r")$",
    re.I,
)


def location_for(slug: str, domain: str = "") -> str:
    """Prefer market hints from slug/domain (e.g. binance-com-au → Australia)."""
    s = (slug or "").lower()
    d = (domain or "").lower()
    codes = "|".join(sorted(_SLUG_MARKET.keys(), key=len, reverse=True))
    m = re.search(
        rf"(?:^|-)({codes})(?:-com|-co)?-review$",
        s,
    )
    if not m:
        m = re.search(
            r"-(?:com|co)-(au|uk|us|nz|sg|hk|ae|za)-review$",
            s,
        )
    if not m and s.endswith("-co-uk-review"):
        return "United Kingdom"
    if m:
        return _SLUG_MARKET.get(m.group(1), COUNTRIES[stable_int(slug + ":loc", len(COUNTRIES))])
    if d.endswith(".com.au") or d.endswith(".net.au") or d.endswith(".au"):
        return "Australia"
    if d.endswith(".co.uk") or d.endswith(".org.uk") or d.endswith(".uk"):
        return "United Kingdom"
    for code, loc in _SLUG_MARKET.items():
        if d.endswith("." + code):
            return loc
    return COUNTRIES[stable_int(slug + ":loc", len(COUNTRIES))]


_LABEL_TO_LOC = {
    "UK": "United Kingdom",
    "US": "United States",
    "USA": "United States",
    "DE": "Germany",
    "FR": "France",
    "ES": "Spain",
    "IT": "Italy",
    "NL": "Netherlands",
    "NZ": "New Zealand",
    "SG": "Singapore",
    "HK": "Hong Kong",
    "CA": "Canada",
    "AE": "United Arab Emirates",
    "UAE": "United Arab Emirates",
    "JP": "Japan",
    "IN": "India",
    "ZA": "South Africa",
    "IE": "Ireland",
    "CH": "Switzerland",
    "EU": "European Union",
    "AU": "Australia",
    "TH": "Thailand",
    "MY": "Malaysia",
    "PT": "Portugal",
    "PL": "Poland",
    "SE": "Sweden",
    "BE": "Belgium",
    "AT": "Austria",
    "BR": "Brazil",
    "MX": "Mexico",
    "TR": "Turkey",
    "PH": "Philippines",
    "VN": "Vietnam",
    "ID": "Indonesia",
    "TW": "Taiwan",
    "KR": "South Korea",
}


def _label_location(label: str) -> str | None:
    if not label:
        return None
    mapped = _LABEL_TO_LOC.get(label.upper())
    if mapped:
        return mapped
    if len(label) > 3:
        return label
    return None


def _slug_has_market(slug: str, domain: str = "", name: str = "") -> bool:
    s = (slug or "").lower()
    d = (domain or name or "").lower()
    codes = "|".join(sorted(_SLUG_MARKET.keys(), key=len, reverse=True))
    if re.search(rf"(?:^|-)({codes})(?:-com|-co)?-review$", s):
        return True
    if re.search(r"-(?:com|co)-(au|uk|us|nz|sg|hk|ae|za)-review$", s) or s.endswith("-co-uk-review"):
        return True
    if re.search(rf"\.(?:com\.)?({codes})\b", d):
        return True
    return False


def peel_regional_name(name: str, slug: str = "", domain: str = "") -> tuple[str, str | None, list[str], str | None]:
    """Turn 'Binance Australia' / 'bybit.nl' into brand + market location + aliases.

    Returns (name, location_or_None, aliases_to_add, official_domain_or_None).
    Does not treat corporate 'SA' (Société Anonyme) as Saudi Arabia.
    """
    raw = (name or "").strip()
    if not raw or raw.lower().startswith("impersonation"):
        return raw, None, [], None

    host = re.sub(r"^https?://", "", raw, flags=re.I).split("/")[0].strip().lower()
    host = re.sub(r"^www\.", "", host)

    for kb, (brand, official_dom) in _KNOWN_REGIONAL.items():
        # bybit.nl / bitcoin.com.au / santander.pt
        if re.fullmatch(rf"{re.escape(kb)}(?:\.com)?\.[a-z]{{2}}(?:\.[a-z]{{2}})?", host):
            loc = location_for(slug, domain or host)
            return brand, loc, [raw], official_dom

    m = _COUNTRY_SUFFIX.match(raw)
    if not m:
        return raw, None, [], None

    brand_part = m.group("brand").strip(" -–—|,")
    label = m.group("label")
    if not brand_part or len(brand_part) < 2:
        return raw, None, [], None
    # never peel corporate SA (Société Anonyme / Sociedad Anónima)
    if label.upper() == "SA":
        return raw, None, [], None

    label_loc = _label_location(label)
    if len(label) <= 3 and label.upper() not in _LABEL_TO_LOC:
        return raw, None, [], None

    brand_key = re.sub(r"[\s_.-]+", "", brand_part).lower()
    known = None
    for kb, (brand, official_dom) in _KNOWN_REGIONAL.items():
        if brand_key == kb or brand_key == re.sub(r"[\s_.-]+", "", brand).lower():
            known = (brand, official_dom)
            break

    # Short codes on unknown brands are noisy (e.g. "@Better Tr", "Foo SA")
    # Only peel them for known multi-market brands or common market tags with evidence.
    common_tags = {"UK", "UAE", "USA", "US", "EU", "AU", "DE", "FR", "NL", "NZ", "SG", "HK"}
    if len(label) <= 3 and not known:
        if label.upper() not in common_tags:
            return raw, None, [], None
        if not _slug_has_market(slug, domain, raw) and label.upper() not in {"UK", "UAE", "USA", "EU"}:
            return raw, None, [], None

    if known:
        brand, official_dom = known
        loc = label_loc
        if _slug_has_market(slug, domain, raw):
            loc = location_for(slug, domain) or label_loc
        return brand, loc, [raw], official_dom

    loc = label_loc
    if _slug_has_market(slug, domain, raw):
        loc = location_for(slug, domain) or label_loc
    return brand_part, loc, [raw], None


def normalize_slug(raw: str) -> str:
    s = (raw or "").strip().lower()
    if not s:
        raise ValueError("empty slug")
    if not s.endswith("-review") and s != "ftx":
        # allow either form; forensic source usually includes -review
        pass
    return s


def from_forensic_row(b: dict, tp_map: dict, today: date) -> dict:
    slug = normalize_slug(b["s"])
    meta = tier_to_stirling(b.get("t") or "scam")
    tp = tp_map.get(b["s"]) or tp_map.get(slug)
    updated = today - timedelta(days=stable_int(slug, 120))
    domain = b.get("domain") or ""
    name, peeled_loc, aliases, official = peel_regional_name(b["n"], slug, domain)
    loc = peeled_loc or location_for(slug, domain)
    row = {
        "slug": slug,
        "name": name,
        "domain": domain or (official or ""),
        "tier": b.get("t") or "scam",
        "blurb": b.get("d") or "",
        "location": loc,
        "status": meta["status"],
        "category": meta["category"],
        "caseType": meta["caseType"],
        "risk": meta["risk"],
        "updated": updated.isoformat(),
        "tags": {
            "regId": "",
            "regulator": "",
            "product": "broker",
            "allegation": "",
            "assetClass": "",
            "risk": meta["risk"],
        },
        "trustpilot": (
            {"title": tp["title"], "domain": tp.get("domain", "")} if tp else None
        ),
    }
    if aliases:
        row["aliases"] = aliases
    if official:
        row["officialDomain"] = official
    return row


def from_stirling_row(o: dict, today: date) -> dict:
    """Accept a full or partial site broker object."""
    if not o.get("slug") and o.get("s"):
        return from_forensic_row(o, {}, today)
    slug = normalize_slug(o["slug"])
    tier = o.get("tier") or "scam"
    meta = tier_to_stirling(tier)
    domain = o.get("domain") or ""
    raw_name = o.get("name") or slug.replace("-", " ").title()
    name, peeled_loc, peel_aliases, official = peel_regional_name(raw_name, slug, domain)
    row = {
        "slug": slug,
        "name": name,
        "domain": domain or (official or ""),
        "tier": tier,
        "blurb": o.get("blurb") or o.get("d") or "",
        "location": o.get("location") or peeled_loc or location_for(slug, domain),
        "status": o.get("status") or meta["status"],
        "category": o.get("category") or meta["category"],
        "caseType": o.get("caseType") or meta["caseType"],
        "risk": o.get("risk") or meta["risk"],
        "updated": o.get("updated") or today.isoformat(),
        "tags": o.get("tags")
        or {
            "regId": "",
            "regulator": "",
            "product": "broker",
            "allegation": "",
            "assetClass": "",
            "risk": o.get("risk") or meta["risk"],
        },
        "trustpilot": o.get("trustpilot"),
    }
    if peel_aliases and "aliases" not in o:
        row["aliases"] = peel_aliases
    if official and "officialDomain" not in o:
        row["officialDomain"] = official
    for k in CURATED_KEYS:
        if k in o and o[k] is not None:
            row[k] = o[k]
    return row


def merge_broker(existing: dict | None, incoming: dict, *, preserve_curated: bool) -> dict:
    if not existing:
        return incoming
    out = dict(existing)
    # Refresh base identity / tier fields from incoming
    for k in (
        "name",
        "domain",
        "tier",
        "blurb",
        "location",
        "status",
        "category",
        "caseType",
        "risk",
        "updated",
        "trustpilot",
    ):
        if incoming.get(k) not in (None, ""):
            # Don't blank a curated domain with empty incoming
            if k == "domain" and not incoming.get("domain") and existing.get("domain"):
                continue
            if k == "location" and existing.get("location") and incoming.get("location") == location_for(
                incoming["slug"], incoming.get("domain") or ""
            ):
                # keep existing location if incoming is only the default and we already set one
                continue
            out[k] = incoming[k]
    if preserve_curated:
        for k in CURATED_KEYS:
            if k in existing and existing[k] not in (None, "", [], {}):
                out[k] = existing[k]
            elif k in incoming and incoming[k] not in (None, "", [], {}):
                out[k] = incoming[k]
    else:
        for k in CURATED_KEYS:
            if k in incoming:
                out[k] = incoming[k]
    # tags: shallow merge
    tags = dict(existing.get("tags") or {})
    tags.update({k: v for k, v in (incoming.get("tags") or {}).items() if v not in (None, "")})
    if tags:
        out["tags"] = tags
    return out


def ftx_seed() -> dict:
    return {
        "slug": "ftx",
        "name": "FTX Trading Ltd",
        "aliases": ["FTX", "FTX.com", "Alameda Research"],
        "domain": "ftx.com",
        "officialDomain": "ftx.com",
        "tier": "scam",
        "blurb": "a crypto exchange that collapsed in 2022 amid bankruptcy proceedings and related civil and criminal matters.",
        "location": "Bahamas",
        "status": "active",
        "category": "companies",
        "caseType": "class-action",
        "risk": "high",
        "updated": "2024-11-12",
        "tags": {
            "regId": "FTX-INDEX-001",
            "regulator": "multi-jurisdiction",
            "product": "crypto-exchange",
            "allegation": "customer-fund-misuse",
            "assetClass": "digital-assets",
            "risk": "high",
        },
        "trustpilot": None,
    }


def collect_incoming(
    *,
    forensic_path: Path | None,
    tp_map: dict,
    today: date,
    limit: int | None,
    json_paths: list[Path],
    jsonl_paths: list[Path],
    use_inbox: bool,
) -> list[dict]:
    incoming: list[dict] = []

    if forensic_path and forensic_path.exists():
        raw = load_forensic_array(forensic_path)
        with_tp = [b for b in raw if b.get("s") in tp_map]
        rest = [b for b in raw if b.get("s") not in tp_map]
        ordered = with_tp + rest
        if limit is not None:
            ordered = ordered[:limit]
        for b in ordered:
            incoming.append(from_forensic_row(b, tp_map, today))

    paths = list(json_paths) + list(jsonl_paths)
    if use_inbox and INBOX.exists():
        for path in sorted(INBOX.glob("*.json")) + sorted(INBOX.glob("*.jsonl")):
            name = path.name.lower()
            if name.startswith("example.") or name.endswith(".example") or ".example." in name:
                continue
            paths.append(path)

    for path in paths:
        if not path.exists():
            print(f"skip missing {path}")
            continue
        if path.suffix == ".jsonl":
            for line in path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                incoming.append(from_stirling_row(json.loads(line), today))
        else:
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict) and "brokers" in data:
                data = data["brokers"]
            if not isinstance(data, list):
                raise SystemExit(f"{path} must be a JSON array (or {{brokers: [...]}})")
            for o in data:
                # forensic-shaped objects inside JSON
                if "s" in o and "n" in o and "slug" not in o:
                    incoming.append(from_forensic_row(o, tp_map, today))
                else:
                    incoming.append(from_stirling_row(o, today))

    return incoming


def main() -> None:
    ap = argparse.ArgumentParser(description="Import/merge brokers into Mike Levy Law")
    ap.add_argument("--limit", type=int, default=None, help="Cap forensic source rows")
    ap.add_argument("--all", action="store_true", help="Import full forensic source")
    ap.add_argument(
        "--merge",
        action="store_true",
        default=True,
        help="Merge into existing brokers.js (default)",
    )
    ap.add_argument(
        "--replace",
        action="store_true",
        help="Rebuild list from sources only (still preserves curated keys on overlap)",
    )
    ap.add_argument(
        "--source",
        type=Path,
        default=FORENSIC / "js" / "brokers-data.js",
        help="forensicsou-style brokers-data.js",
    )
    ap.add_argument("--no-forensic", action="store_true", help="Skip default forensic source")
    ap.add_argument("--json", type=Path, action="append", default=[], help="Site JSON array")
    ap.add_argument("--jsonl", type=Path, action="append", default=[], help="JSONL brokers")
    ap.add_argument(
        "--inbox",
        action="store_true",
        help=f"Also ingest {INBOX}/*.json and *.jsonl",
    )
    ap.add_argument(
        "--skip-comments",
        action="store_true",
        help="Only update brokers.js (comments later)",
    )
    ap.add_argument(
        "--comments-all",
        action="store_true",
        help="Rebuild comments for every slug (default: new slugs only)",
    )
    args = ap.parse_args()

    today = date.today()
    research = args.source.parent.parent / "research" if args.source else FORENSIC / "research"
    tp_map = load_tp_map(research if research.exists() else FORENSIC / "research")

    limit = None
    if not args.all and args.limit is None and not args.json and not args.jsonl and not args.inbox:
        limit = DEFAULT_LIMIT
    elif args.limit is not None and not args.all:
        limit = args.limit

    forensic_path = None if args.no_forensic else args.source
    incoming = collect_incoming(
        forensic_path=forensic_path,
        tp_map=tp_map,
        today=today,
        limit=limit,
        json_paths=args.json,
        jsonl_paths=args.jsonl,
        use_inbox=args.inbox,
    )

    brokers_path = OUT_DIR / "brokers.js"
    existing_list: list[dict] = []
    if brokers_path.exists() and not args.replace:
        existing_list = load_js_assign(brokers_path, "window.SBL_BROKERS")
    by_slug = {b["slug"]: b for b in existing_list}

    if "ftx" not in by_slug:
        by_slug["ftx"] = ftx_seed()

    added = 0
    updated = 0
    for row in incoming:
        slug = row["slug"]
        if slug in by_slug:
            by_slug[slug] = merge_broker(by_slug[slug], row, preserve_curated=True)
            updated += 1
        else:
            by_slug[slug] = row
            added += 1

    # Stable order: ftx first, then previous order, then new slugs alpha
    ordered_slugs = []
    if "ftx" in by_slug:
        ordered_slugs.append("ftx")
    for b in existing_list:
        if b["slug"] != "ftx" and b["slug"] in by_slug and b["slug"] not in ordered_slugs:
            ordered_slugs.append(b["slug"])
    for slug in sorted(by_slug.keys()):
        if slug not in ordered_slugs:
            ordered_slugs.append(slug)

    brokers = [by_slug[s] for s in ordered_slugs]
    write_js_assign(
        brokers_path,
        "window.SBL_BROKERS",
        brokers,
        "/* Auto-generated by tools/import_brokers.py — merge-safe; curated fields preserved */",
    )
    print(f"Brokers total={len(brokers)} added={added} touched={updated} → {brokers_path}")

    try:
        subprocess.check_call(
            ["python3", str(STIRLING / "tools" / "build_sitemap.py")],
            cwd=str(STIRLING),
        )
    except Exception as exc:  # noqa: BLE001 — sitemap is SEO hygiene, not import-critical
        print(f"Warning: sitemap rebuild failed: {exc}")

    if args.skip_comments:
        print("Skipped comments (--skip-comments)")
        return

    cmd = ["python3", str(STIRLING / "tools" / "rebuild_comments.py")]
    if not args.comments_all:
        cmd.append("--new-only")
    subprocess.check_call(cmd, cwd=str(STIRLING))


if __name__ == "__main__":
    main()
