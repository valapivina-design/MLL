#!/usr/bin/env python3
"""Generate static, crawlable SEO brief pages for every broker review.

Writes company-broker-index/reviews/<slug>.html in the standard Mike Levy Law
brief layout (profile, risk meter, inception/reports timeline, writeup, FAQ,
case CTA) with full title/meta/H1/JSON-LD so search engines index without JS.
Interactive extras remain on review.html (canonical → these static briefs).

  python3 tools/build_reviews_seo.py
"""
from __future__ import annotations

import json
import re
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BROKERS_JS = ROOT / "company-broker-index" / "data" / "brokers.js"
OUT_DIR = ROOT / "company-broker-index" / "reviews"
SITE = "https://mikelevylaw.com"
YEAR = date.today().year
DATE_LABEL = date.today().strftime("%B %Y")


def as_of_label(b: dict) -> str:
    raw = (b.get("updated") or "")[:10]
    try:
        return date.fromisoformat(raw).strftime("%B %Y")
    except ValueError:
        return DATE_LABEL


def resolve_risk(b: dict) -> str:
    raw = ((b.get("tags") or {}).get("risk") or b.get("risk") or "high")
    r = str(raw).lower().strip()
    return r if r in ("low", "medium", "high") else "high"


def extract_inception_year(blurb: str) -> str | None:
    s = blurb or ""
    patterns = [
        r"(?:established|founded|launched|incorporated|formed|opened|started|since)\s+(?:in\s+)?((?:19|20)\d{2})",
        r"((?:19|20)\d{2})[-\s]?(?:registered|vintage|founded)",
        r"(?:registered|dating\s+from|operating\s+since)\s+(?:in\s+)?((?:19|20)\d{2})",
        r"\b(?:est\.?|est)\s*((?:19|20)\d{2})\b",
    ]
    for pat in patterns:
        m = re.search(pat, s, re.I)
        if m:
            return m.group(1)
    return None


def extract_reports_year(blurb: str, updated: str) -> str:
    s = blurb or ""
    patterns = [
        r"(?:collapsed|collapse|bankruptcy|warning|alert|complaint|dissolved|unreachable|fee.?demand)[^\d]{0,48}((?:19|20)\d{2})",
        r"((?:19|20)\d{2})[^\d]{0,24}(?:collapse|bankruptcy|warning|alert|complaint)",
        r"(?:in|since|from)\s+((?:19|20)\d{2})[^\d]{0,20}(?:complaint|report|alert|warning)",
    ]
    years = []
    for pat in patterns:
        for m in re.finditer(pat, s, re.I):
            years.append(m.group(1))
    if years:
        return min(years)
    if updated and re.match(r"^\d{4}", updated):
        return updated[:4]
    return str(YEAR)


def format_short_date(iso: str) -> str:
    raw = (iso or "")[:10]
    try:
        return date.fromisoformat(raw).strftime("%b %d, %Y")
    except ValueError:
        return raw or ""


def build_timeline(b: dict) -> list[dict]:
    """Inception → reports started → last brief update. Prefer curated timeline."""
    curated = b.get("timeline") or []
    if isinstance(curated, list) and len(curated) >= 2:
        return curated
    blurb = scrub_indexed(b.get("blurb") or "")
    updated = (b.get("updated") or "")[:10]
    upd_year = updated[:4] if updated[:4].isdigit() else str(YEAR)
    risk = resolve_risk(b)
    inception = b.get("inception") or extract_inception_year(blurb)
    reports = str(b.get("reportsStarted") or extract_reports_year(blurb, updated))
    # Keep chronological order when both known
    points: list[dict] = []
    if inception:
        points.append(
            {
                "year": str(inception),
                "event": "Inception / brand first appears in public materials",
                "tone": "blue",
            }
        )
    else:
        points.append(
            {
                "year": "—",
                "event": "Inception date not verified in sources reviewed",
                "tone": "blue",
            }
        )
    report_tone = "alert" if risk == "high" else "brown"
    report_event = (
        "Public complaints / alerts appear in the record"
        if risk == "high"
        else "Public reports and service complaints appear in the record"
    )
    # Avoid duplicate year+similar if reports == inception
    if reports and inception and str(reports) == str(inception):
        points.append(
            {
                "year": str(reports),
                "event": "Same period: public reports begin to surface",
                "tone": report_tone,
            }
        )
    else:
        points.append({"year": str(reports), "event": report_event, "tone": report_tone})
    points.append(
        {
            "year": upd_year,
            "event": "Brief last updated"
            + (f" · {format_short_date(updated)}" if updated else ""),
            "tone": "brown" if risk != "high" else "alert",
        }
    )
    return points[:3]


def needle_xy(risk: str) -> tuple[str, str]:
    if risk == "low":
        return "40", "55"
    if risk == "medium":
        return "100", "28"
    return "168", "48"


def kind_label(b: dict) -> str:
    c = (b.get("category") or "").lower()
    if c == "online":
        return "Online"
    if c == "companies":
        return "Company"
    return "Broker"


def timeline_html(points: list[dict]) -> str:
    bits = []
    for p in points:
        tone = escape(str(p.get("tone") or "blue"))
        bits.append(
            f'<div class="t-point {tone}"><div class="dot"></div>'
            f'<div class="year">{escape(str(p.get("year") or "—"))}</div>'
            f'<div class="event">{escape(str(p.get("event") or ""))}</div></div>'
        )
    return "\n".join(bits)


def risk_label(risk: str) -> str:
    return {"low": "Low Risk", "medium": "Medium Risk"}.get(risk, "High Risk")


def load_brokers() -> list[dict]:
    text = BROKERS_JS.read_text(encoding="utf-8")
    m = re.search(r"window\.SBL_BROKERS\s*=\s*(\[.*\])\s*;?\s*$", text, re.S)
    if not m:
        raise SystemExit("Could not parse SBL_BROKERS")
    return json.loads(m.group(1))


def scrub_indexed(s: str) -> str:
    return re.sub(r"\bindexed\b", "listed", s or "", flags=re.I)


def blurb_needs_break(blurb: str) -> bool:
    s = (blurb or "").strip()
    if not s:
        return False
    if s[0].isupper():
        return True
    if re.match(r"^Platform\b", s, re.I):
        return True
    if re.match(r"^(the|a|an)\s+[\w'-]+(?:\s+[\w'-]+){0,3}\s+is\b", s, re.I):
        return True
    return False


def name_with_blurb_raw(name: str, blurb: str, fallback: str = "") -> str:
    s = (blurb or fallback or "").strip()
    if not s:
        s = "a firm under review against publicly available records."
    s = s.rstrip(".")
    if blurb_needs_break(s):
        return f"{name} — {s}"
    return f"{name} is {s}"


def name_with_blurb(name: str, blurb: str, fallback: str = "") -> str:
    return escape(name_with_blurb_raw(name, blurb, fallback))


def is_soft(b: dict) -> bool:
    t = (b.get("tier") or "").lower()
    if t in ("legit", "clone"):
        return True
    if t != "scam" and b.get("risk") in ("medium", "low"):
        return True
    return False


def aliases_of(b: dict) -> list[str]:
    primary = (b.get("name") or "").lower()
    out, seen = [], set()
    for a in b.get("aliases") or b.get("alsoKnownAs") or []:
        a = str(a or "").strip()
        if not a:
            continue
        key = a.lower()
        if key == primary or key in seen:
            continue
        seen.add(key)
        out.append(a)
    return out


def clones_of(b: dict) -> list[dict]:
    out, seen = [], set()
    for item in b.get("clones") or []:
        if isinstance(item, str):
            domain, name, note = item.strip(), item.strip(), ""
        elif isinstance(item, dict):
            domain = str(item.get("domain") or item.get("host") or "").strip()
            name = str(item.get("name") or item.get("label") or domain).strip()
            note = str(item.get("note") or "").strip()
        else:
            continue
        if not domain or domain.lower() in seen:
            continue
        seen.add(domain.lower())
        out.append({"domain": domain, "name": name or domain, "note": note})
    return out


def official_domain(b: dict) -> str:
    return (
        b.get("officialDomain")
        or b.get("domain")
        or ((b.get("trustpilot") or {}).get("domain") if isinstance(b.get("trustpilot"), dict) else "")
        or ""
    )


def dedupe_kw(parts: list[str]) -> str:
    seen, out = set(), []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        key = p.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(p)
    return ", ".join(out)


def keywords(b: dict, soft: bool) -> str:
    low = (b.get("name") or "").lower()
    dom = official_domain(b)
    parts = [
        f"{low} review",
        f"is {low} a scam",
        f"is {low} legit",
        f"is {low} a legit broker",
        f"{low} scam",
        f"{low} complaints",
    ]
    if soft:
        parts += [dom, f"{low} login", f"fake {low}", f"{low} clone", f"{low} support", f"report {low}"]
    else:
        parts += [
            f"{low} withdrawal",
            dom,
            f"{low} investigation",
            f"{low} reddit",
            f"report {low}",
        ]
    for a in aliases_of(b):
        al = a.lower()
        parts += [
            f"{al} review",
            f"is {al} a scam",
            f"is {al} legit",
            f"is {al} a legit broker",
            f"{al} scam",
            f"{al} complaints",
            f"report {al}",
        ]
    for c in clones_of(b):
        d = c["domain"].lower()
        n = (c["name"] or d).lower()
        parts += [f"{d} review", f"is {d} a scam", f"fake {n}", f"{d} clone", f"{d} scam", f"report {d}"]
    if b.get("kw_extra"):
        parts.append(str(b["kw_extra"]))
    return dedupe_kw([p for p in parts if p])


def clip(s: str, n: int = 160) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) <= n:
        return s
    cut = s[: n - 1]
    sp = cut.rfind(" ")
    if sp > 100:
        cut = cut[:sp]
    return re.sub(r"[.,;:\s]+$", "", cut) + "…"


def faqs(b: dict) -> list[tuple[str, str]]:
    n = b.get("name") or "this firm"
    soft = is_soft(b)
    dom = official_domain(b) or "the listed domain"
    blurb = scrub_indexed(b.get("blurb") or "a firm we have reviewed against publicly available records.")
    process = (
        "How does your process work?",
        "We begin with a confidential look at the date, how you paid, and any statements or screenshots you still have. We then compare that timeline with the public record and outline counsel, regulator, or reporting options. We do not replace your bank, card scheme, or the police.",
    )
    if soft:
        items = [
            (
                f"Is {n} a scam?",
                f"We do not treat {n} as a fraud finding on this page alone. The firm appears in public records as a real business. Many complaints under this name still turn out to involve lookalike sites or ordinary service disputes — send the domain you used if you want that sorted confidentially.",
            ),
            (
                f"Is {n} a legit broker?",
                f"The company itself appears genuine. That is not the same as every website using the name. Type {dom} yourself and compare it character by character with any link you were sent.",
            ),
            (
                f"Is {n} regulated?",
                (
                    f"Available records note: {(b.get('tags') or {}).get('regulator')}. Confirm the exact entity on your statement against the regulator’s public register."
                    if (b.get("tags") or {}).get("regulator")
                    else "Confirm the entity named on your account agreement against the public register of the claimed regulator. A licence for one group company does not automatically cover another."
                ),
            ),
            (
                f"I lost money to someone claiming to be {n} — is that the real company?",
                "Often it is not. Impersonators borrow names, logos, even licence numbers. Keep every message, receipt, URL and wallet address, then contact us if you want next steps reviewed.",
            ),
            (
                f"How do I check the {n} site I used is genuine?",
                f"Type {dom} yourself — do not follow a link from an advert, email or message. If the domain differs by even one character, you were not dealing with the firm described on this page.",
            ),
            process,
        ]
    else:
        items = [
            (
                f"Is {n} a legit broker?",
                f"Screen balances are not the same as a payout you control. {name_with_blurb_raw(n, blurb)}. Share the date and how you paid if you want a confidential consultation on next steps.",
            ),
            (
                f"Can you close my {n} account, or have the person who phoned me call again?",
                f"Mike Levy Law is not affiliated with this broker. We do not hold an account at {n} and cannot impersonate their staff or reopen a login for you.",
            ),
            (
                f"{n} says I must pay a tax or fee before withdrawing — should I?",
                "No. Real firms deduct legitimate charges from the balance or disclose them in statements — they do not usually demand a separate “tax” or “release” payment to a personal wallet before you can leave.",
            ),
            (
                "What do you do with what I send?",
                "We review it confidentially against the public record and outline counsel, regulator, or reporting options. We are not a bank, card scheme, or police substitute.",
            ),
            process,
        ]
    for a in aliases_of(b)[:2]:
        items.insert(
            1,
            (
                f"What is the connection between {a} and {n}?",
                f"{a} appears in materials connected with {n} — for example a prior brand, trading style, or name on paperwork. If your documents use either label, we review them as part of the same matter.",
            ),
        )
    for c in clones_of(b)[:3]:
        off = official_domain(b) or "the official domain you type yourself"
        items.append(
            (
                f"What should I know about {c['domain']}?",
                f"{c['domain']} does not match the official {n} site ({off}). Sites that borrow a trusted name are a common risk. If you paid through {c['domain']}, keep the URL, date, and payment method.",
            )
        )
    return items


def writeup_html(b: dict) -> str:
    n = b.get("name") or "this firm"
    soft = is_soft(b)
    dom = official_domain(b) or "the domain associated with this brand"
    loc = b.get("location") or "its stated jurisdiction"
    blurb = scrub_indexed(
        b.get("blurb") or "a trading or investment firm we have reviewed against publicly available records."
    )
    parts: list[str] = []
    if soft:
        parts.append(
            f"<h2>About this {escape(n)} review</h2>"
            f"<p>{escape(n)} appears as a real business in the public records we examined. That does not mean every site using the name is genuine — lookalike domains and service complaints are often confused. This review helps separate a dispute with the real platform from impersonation, and when a confidential consultation may help. If you are asking whether {escape(n)} is a scam, or whether {escape(n)} is a legit broker, verify the domain character by character before any further deposits.</p>"
            f"<h2>Regulation and legitimacy</h2>"
            f"<p>{name_with_blurb(n, blurb)}. Confirm the entity on your statements against the regulator’s register, and type <strong>{escape(dom)}</strong> yourself rather than following a message link.</p>"
            f"<h2>Complaints and impersonation risk</h2>"
            f"<p>Reports about {escape(n)} often mix ordinary support issues with losses on fake sites that borrow the brand. Preserve chat logs, receipts, and URLs. We can review that paperwork confidentially and outline counsel or reporting options.</p>"
        )
    else:
        parts.append(
            f"<h2>About this {escape(n)} review</h2>"
            f"<p>{name_with_blurb(n, blurb)}. As of {escape(as_of_label(b))}, public reporting linked to {escape(dom)} and activity associated with {escape(loc)} includes patterns such as stalled withdrawals, unexpected fee demands before payout, or similar friction. Clients often ask whether {escape(n)} is a scam or a legitimate broker; the answer turns on the domain you used and the documents you still hold.</p>"
            f"<h2>Withdrawals, fees, and what to keep</h2>"
            f"<p>A licence you verified yourself and a payout that reaches an account you control is one picture. A dashboard balance plus a new “tax” or “compliance” payment before you can leave is another. If you paid through {escape(dom)}, retain the date, method, and any message that demanded an extra fee.</p>"
            f"<h2>If you cannot withdraw</h2>"
            f"<p>Accounts that allow a small test payout and then freeze larger requests are a recurring pattern in {escape(n)} complaint threads. Contact Mike Levy Law for a confidential consultation — we compare what you send with the public record and advise on litigation or reporting pathways.</p>"
        )
    als = aliases_of(b)
    if als:
        parts.append(
            f"<h2>Related names and prior brands</h2>"
            f"<p>This review centres on <strong>{escape(n)}</strong>. The labels below also appear in filings, dashboards, or client paperwork connected with the same matter.</p>"
        )
        for a in als:
            parts.append(
                f"<h2>{escape(a)} review</h2>"
                f"<p>Materials referring to {escape(a)} are commonly part of the same {escape(n)} storyline. Clients sometimes ask whether {escape(a)} is a scam, or whether {escape(a)} is a legit broker; the practical question is which domain took the funds and what evidence remains.</p>"
            )
    cls = clones_of(b)
    if cls:
        off = official_domain(b)
        parts.append(
            f"<h2>Lookalike domains</h2>"
            f"<p>Alongside related names, some websites imitate {escape(n)} branding. Those addresses are not the official site"
            + (f" (<strong>{escape(off)}</strong>)" if off else "")
            + ".</p>"
        )
        for c in cls:
            parts.append(
                f"<h2>{escape(c['domain'])} review</h2>"
                f"<p>{escape(c['name'])} has been noted as a lookalike in connection with {escape(n)}. Where people ask whether {escape(c['domain'])} is a scam, the safer working assumption is that any domain other than the official site warrants careful review before further payments.</p>"
            )
    return "\n".join(parts)


def page_html(b: dict) -> str:
    n = b.get("name") or b.get("slug") or "Company"
    slug = b.get("slug") or ""
    soft = is_soft(b)
    dom = official_domain(b) or "listed domain"
    als = aliases_of(b)
    cls = clones_of(b)
    kw = keywords(b, soft)
    as_of = as_of_label(b)
    if soft:
        title = f"{n} Review {YEAR} — Regulation, Complaints & Clone Warnings | Mike Levy Law"
        desc = f"{n} review ({as_of}): is {n} a scam? Is {n} a legit broker? Real company signals, clone warnings, complaints, and confidential consultation."
    else:
        title = f"{n} Review {YEAR} — Company & Broker Index | Mike Levy Law"
        desc = f"{n} review ({as_of}): is {n} a scam? Is {n} a legit broker? Assessment of {dom} — withdrawals, complaints, regulator checks, consultation."
    extra = ""
    if als:
        extra += " Also: " + ", ".join(als[:3]) + "."
    if cls:
        extra += " Lookalikes: " + ", ".join(c["domain"] for c in cls[:3]) + "."
    desc = clip(desc + extra, 160)
    canon = f"{SITE}/company-broker-index/reviews/{escape(slug)}.html"
    interactive = f"../review.html?company={escape(slug)}"
    faq_list = faqs(b)
    faq_html = "\n".join(
        f"<details{' open' if i == 0 else ''}><summary>{escape(q)}</summary><p>{escape(a)}</p></details>"
        for i, (q, a) in enumerate(faq_list)
    )
    blurb = scrub_indexed(b.get("blurb") or "a firm under review against publicly available records.")
    updated = (b.get("updated") or date.today().isoformat())[:10]
    org = {
        "@type": ["Organization", "LegalService"],
        "@id": f"{SITE}/#organization",
        "name": "Mike Levy Law",
        "url": f"{SITE}/",
        "email": "info@mikelevylaw.com",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "1395 Brickell Ave, Suite 800",
            "addressLocality": "Miami",
            "addressRegion": "FL",
            "postalCode": "33131",
            "addressCountry": "US",
        },
    }
    item_reviewed = {
        "@type": "Organization",
        "name": n,
    }
    if official_domain(b):
        item_reviewed["url"] = "https://" + official_domain(b).replace("https://", "").replace("http://", "")
    graph = [
        org,
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "Company & Broker Index",
                    "item": f"{SITE}/company-broker-index/",
                },
                {"@type": "ListItem", "position": 3, "name": f"{n} Review", "item": canon},
            ],
        },
        {
            "@type": "WebPage",
            "@id": canon,
            "url": canon,
            "name": f"{n} Review",
            "description": desc,
            "isPartOf": {"@id": f"{SITE}/#website"},
            "about": item_reviewed,
            "inLanguage": "en-US",
            "dateModified": updated,
        },
        {
            "@type": "Article",
            "headline": f"{n} Review",
            "alternativeHeadline": title,
            "description": desc,
            "keywords": kw,
            "inLanguage": "en-US",
            "dateModified": updated,
            "datePublished": updated,
            "author": {"@id": f"{SITE}/#organization"},
            "publisher": {"@id": f"{SITE}/#organization"},
            "image": f"{SITE}/hero-books.jpg",
            "mainEntityOfPage": {"@type": "WebPage", "@id": canon},
            "about": item_reviewed,
        },
        {
            "@type": "Review",
            "name": f"{n} Review",
            "url": canon,
            "dateModified": updated,
            "author": {"@id": f"{SITE}/#organization"},
            "publisher": {"@id": f"{SITE}/#organization"},
            "itemReviewed": item_reviewed,
            "reviewBody": f"{n} — {blurb} This page is informational and does not constitute a finding of liability.",
            "inLanguage": "en-US",
        },
        {
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a},
                }
                for q, a in faq_list
            ],
        },
        {
            "@type": "HowTo",
            "name": "Confidential consultation process",
            "description": "How Mike Levy Law reviews a potential loss matter.",
            "step": [
                {
                    "@type": "HowToStep",
                    "position": 1,
                    "name": "Free initial look",
                    "text": "Send the date, how you paid, and any chat or screenshot.",
                },
                {
                    "@type": "HowToStep",
                    "position": 2,
                    "name": "Record review",
                    "text": "We compare your timeline to the public record and available notices.",
                },
                {
                    "@type": "HowToStep",
                    "position": 3,
                    "name": "Next-step advice",
                    "text": "We advise on counsel, regulator, or reporting pathways. We do not replace the bank or police.",
                },
            ],
        },
    ]
    if als:
        graph[3]["alternateName"] = als  # Article
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    loc = escape(b.get("location") or "")
    risk = resolve_risk(b)
    nx, ny = needle_xy(risk)
    points = build_timeline(b)
    tl_html = timeline_html(points)
    kind = kind_label(b)
    updated_fmt = format_short_date(updated)
    badge = (
        '<span class="verified-badge flagged">'
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true">'
        '<path d="M12 9v4M12 17h.01"/><path d="M10.3 4.3L2.8 18a2 2 0 0 0 1.7 3h15a2 2 0 0 0 1.7-3L13.7 4.3a2 2 0 0 0-3.4 0z"/>'
        "</svg> High Attention</span>"
        if risk == "high"
        else '<span class="verified-badge">'
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true">'
        '<path d="M20 6L9 17l-5-5"/></svg> On File</span>'
    )
    contact = (
        f"../../index.html?source=review-seo-{escape(slug)}"
        f"&amp;company={escape(n)}&amp;slug={escape(slug)}"
        f"&amp;matter=Broker+%2F+Investment+Platform+Dispute#contact"
    )
    return f"""<!DOCTYPE html>
<html lang="en-US">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(desc)}" />
  <meta name="keywords" content="{escape(kw)}" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <meta name="author" content="Mike Levy Law" />
  <link rel="canonical" href="{canon}" />
  <link rel="alternate" hreflang="en" href="{canon}" />
  <link rel="alternate" hreflang="x-default" href="{canon}" />
  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="Mike Levy Law" />
  <meta property="og:locale" content="en_US" />
  <meta property="og:title" content="{escape(title)}" />
  <meta property="og:description" content="{escape(desc)}" />
  <meta property="og:url" content="{canon}" />
  <meta property="og:image" content="{SITE}/hero-books.jpg" />
  <meta property="article:modified_time" content="{escape(updated)}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{escape(title)}" />
  <meta name="twitter:description" content="{escape(desc)}" />
  <meta name="twitter:image" content="{SITE}/hero-books.jpg" />
  <script type="application/ld+json">{ld}</script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700&family=Playfair+Display:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../brief.css" />
</head>
<body>
  <header class="report-top">
    <div class="report-top-inner">
      <div class="brand-line">
        <a href="../../index.html" class="brand" aria-label="Mike Levy Law">
          <svg class="logo-mark" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
            <circle cx="24" cy="24" r="22" stroke="currentColor" stroke-width="1.5" fill="rgba(255,255,255,0.06)"/>
            <path d="M24 10 L24 14 M14 20 H34 M16 20 V34 H32 V20" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M20 34 V28 H28 V34" stroke="currentColor" stroke-width="1.5"/>
            <path d="M18 20 C18 16 21 14 24 14 C27 14 30 16 30 20" stroke="currentColor" stroke-width="1.5" fill="none"/>
            <circle cx="24" cy="12" r="2" fill="currentColor"/>
          </svg>
          <div class="logo-text">Mike Levy<span>Law</span></div>
        </a>
      </div>
      <div class="seo-kicker">Brief</div>
      <div class="report-heading-row">
        <h1>{escape(n)} Review</h1>
        <form class="top-search" action="../index.html" method="get" role="search">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
            <circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/>
          </svg>
          <input type="search" name="q" placeholder="Enter Broker Name or Registration ID..." aria-label="Search index" />
        </form>
      </div>
    </div>
  </header>

  <main class="page">
    <a class="back-link" href="../index.html">← Back to Company &amp; Broker Index</a>

    <section class="profile-card">
      <div class="profile-top">
        <div>
          <p class="company-name">{escape(n)}</p>
          <p class="company-sub">Company profile · {escape(kind)}{f" · {loc}" if loc else ""}{f" · Updated {escape(updated_fmt)}" if updated_fmt else ""}</p>
          {badge}
        </div>
        <div class="risk-block" role="img" aria-label="Risk score: {escape(risk_label(risk))}, as of {escape(updated_fmt)}">
          <h3>Risk Score</h3>
          <div class="gauge-wrap" aria-hidden="true">
            <svg viewBox="0 0 200 120">
              <path d="M20 100 A80 80 0 0 1 70 28" fill="none" stroke="#8b7055" stroke-width="18" stroke-linecap="butt"/>
              <path d="M70 28 A80 80 0 0 1 130 28" fill="none" stroke="#c4a35a" stroke-width="18" stroke-linecap="butt"/>
              <path d="M130 28 A80 80 0 0 1 180 100" fill="none" stroke="#6b3a3a" stroke-width="18" stroke-linecap="butt"/>
              <circle cx="100" cy="100" r="7" fill="#1a2a4a"/>
              <line x1="100" y1="100" x2="{nx}" y2="{ny}" stroke="#1a2a4a" stroke-width="3" stroke-linecap="round"/>
            </svg>
          </div>
          <div class="risk-label {escape(risk)}">{escape(risk_label(risk))}</div>
          <p class="risk-asof">{f"As of {escape(updated_fmt)}" if updated_fmt else ""}</p>
        </div>
      </div>
      <div class="profile-bottom" style="grid-template-columns:1fr">
        <div class="panel">
          <div class="panel-title">Inception &amp; reports</div>
          <div class="timeline">
            <div class="timeline-line" aria-hidden="true"></div>
            <div class="timeline-points">
{tl_html}
            </div>
          </div>
        </div>
      </div>
    </section>

    <div class="writeup-wrap">
      <div class="section-kicker">Brief analysis</div>
      <article class="writeup">
{writeup_html(b)}
      </article>
    </div>

    <section class="faq-block" aria-labelledby="faq-heading">
      <div class="section-kicker">Guidance</div>
      <h2 id="faq-heading">Frequently asked questions</h2>
      <p class="faq-lead">Straight answers on legitimacy, withdrawals, fees, and how a confidential consultation works.</p>
      <div class="faq">
{faq_html}
      </div>
    </section>

    <aside class="case-review-panel" style="max-width:100%;margin:0 0 40px">
      <h3>Need a case review?</h3>
      <a class="cta-btn" href="{contact}">Request a case review</a>
    </aside>

    <div class="closing">
      <p class="summary"><strong>Summary:</strong> {escape(n)} — {escape(blurb)} This page is informational and does not constitute a finding of liability.{f" Profile last updated {escape(updated_fmt)}." if updated_fmt else ""}</p>
      <p class="note">Informational only. Does not create an attorney-client relationship.
        <a href="../../legal/privacy-policy.html">Privacy Policy</a> ·
        <a href="../../legal/terms-of-use.html">Terms of Use</a> ·
        <a href="../../legal/disclaimer.html">Disclaimer</a>
      </p>
    </div>
  </main>

  <footer class="site-footer">
    <div class="site-footer-inner">
      <div class="site-footer-grid">
        <div>
          <div class="site-footer-brand">Mike Levy Law<span>Litigation</span></div>
          <p>Premier dispute-resolution counsel for businesses, professionals, and individuals in contested civil and investment matters.</p>
        </div>
        <div>
          <h4>Firm</h4>
          <ul>
            <li><a href="../../index.html">Home</a></li>
            <li><a href="../index.html">Company &amp; Broker Index</a></li>
            <li><a href="{interactive}">Interactive tools</a></li>
            <li><a href="{contact}">Contact</a></li>
          </ul>
        </div>
        <div>
          <h4>Legal</h4>
          <ul>
            <li><a href="../../legal/privacy-policy.html">Privacy Policy</a></li>
            <li><a href="../../legal/terms-of-use.html">Terms of Use</a></li>
            <li><a href="../../legal/disclaimer.html">Disclaimer</a></li>
            <li><a href="../../legal/cookie-policy.html">Cookie Policy</a></li>
          </ul>
        </div>
        <div>
          <h4>Contact</h4>
          <ul>
            <li>1395 Brickell Ave, Suite 800</li>
            <li>Miami, FL 33131 · USA</li>
            <li><a href="mailto:info@mikelevylaw.com">info@mikelevylaw.com</a></li>
          </ul>
        </div>
      </div>
      <div class="site-footer-bottom">
        <p class="disclaimer">Informational only. Not legal advice. No attorney-client relationship from using this brief.</p>
        <p>&copy; MLL 2026</p>
      </div>
    </div>
  </footer>
</body>
</html>
"""


def main() -> None:
    brokers = load_brokers()
    if OUT_DIR.exists():
        for old in OUT_DIR.glob("*.html"):
            old.unlink()
    else:
        OUT_DIR.mkdir(parents=True)
    written = 0
    for b in brokers:
        slug = b.get("slug")
        if not slug:
            continue
        # sanitize path segment
        safe = re.sub(r"[^a-zA-Z0-9._-]+", "-", slug).strip("-")
        if safe != slug:
            continue
        (OUT_DIR / f"{slug}.html").write_text(page_html(b), encoding="utf-8")
        written += 1
    index = f"""<!DOCTYPE html>
<html lang="en-US">
<head>
  <meta charset="UTF-8" />
  <title>Broker Reviews — Mike Levy Law</title>
  <meta name="robots" content="noindex, follow" />
  <link rel="canonical" href="{SITE}/company-broker-index/sitemap.html" />
  <meta http-equiv="refresh" content="0;url=../sitemap.html" />
</head>
<body>
  <p><a href="../sitemap.html">Full company &amp; broker review listing</a></p>
</body>
</html>
"""
    (OUT_DIR / "index.html").write_text(index, encoding="utf-8")
    print(f"Wrote {written} review SEO pages → {OUT_DIR}")


if __name__ == "__main__":
    main()
