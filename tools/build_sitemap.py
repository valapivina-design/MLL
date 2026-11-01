#!/usr/bin/env python3
"""Build sitemap.xml (+ optional chunk files) for Mike Levy Law SEO indexing.

  python3 tools/build_sitemap.py
"""
from __future__ import annotations

import re
import json
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://mikelevylaw.com"
BROKERS_JS = ROOT / "company-broker-index" / "data" / "brokers.js"
OUT = ROOT / "sitemap.xml"
CHUNK_DIR = ROOT
MAX_URLS_PER_FILE = 45000


STATIC_PAGES = [
    ("/", "1.0", "weekly"),
    ("/company-broker-index/", "0.9", "daily"),
    ("/company-broker-index/sitemap.html", "0.6", "weekly"),
    ("/insights/", "0.85", "weekly"),
    ("/insights/crypto-scams.html", "0.8", "monthly"),
    ("/insights/scam-wallets.html", "0.8", "monthly"),
    ("/insights/ponzi-investment-scams.html", "0.8", "monthly"),
    ("/insights/digital-forensics.html", "0.8", "monthly"),
    ("/insights/report-a-scam.html", "0.8", "monthly"),
    ("/insights/recover-stolen-crypto.html", "0.8", "monthly"),
    ("/insights/online-trading-forex-scams.html", "0.8", "monthly"),
    ("/insights/pig-butchering-whatsapp-scams.html", "0.8", "monthly"),
    ("/legal/privacy-policy.html", "0.4", "yearly"),
    ("/legal/terms-of-use.html", "0.4", "yearly"),
    ("/legal/disclaimer.html", "0.4", "yearly"),
    ("/legal/cookie-policy.html", "0.3", "yearly"),
]


def load_brokers() -> list[dict]:
    text = BROKERS_JS.read_text(encoding="utf-8")
    m = re.search(r"window\.SBL_BROKERS\s*=\s*(\[.*\])\s*;?\s*$", text, re.S)
    if not m:
        raise SystemExit("Could not parse SBL_BROKERS")
    return json.loads(m.group(1))


def url_entry(loc: str, lastmod: str | None, priority: str, changefreq: str) -> str:
    parts = [
        "  <url>",
        f"    <loc>{escape(loc)}</loc>",
    ]
    if lastmod:
        parts.append(f"    <lastmod>{escape(lastmod)}</lastmod>")
    parts.append(f"    <changefreq>{changefreq}</changefreq>")
    parts.append(f"    <priority>{priority}</priority>")
    parts.append("  </url>")
    return "\n".join(parts)


def write_urlset(path: Path, entries: list[str]) -> None:
    body = "\n".join(entries)
    path.write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}\n"
        "</urlset>\n",
        encoding="utf-8",
    )


def write_html_sitemap(brokers: list[dict]) -> None:
    """Crawlable HTML listing so search engines can discover review URLs beyond the search gate."""
    rows = sorted(brokers, key=lambda b: (b.get("name") or "").lower())
    links = []
    for b in rows:
        slug = b.get("slug") or ""
        name = escape(b.get("name") or slug)
        href = escape(f"reviews/{slug}.html")
        links.append(f'      <li><a href="{href}">{name} Review</a></li>')
    html = f"""<!DOCTYPE html>
<html lang="en-US">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Company &amp; Broker Index — Full Listing | Mike Levy Law</title>
  <meta name="description" content="Full listing of company and broker review pages in the Mike Levy Law index. Each entry links to an individual review with scam/legitimacy FAQ and consultation options." />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="{SITE}/company-broker-index/sitemap.html" />
  <style>
    body {{ font-family: Georgia, serif; max-width: 900px; margin: 40px auto; padding: 0 20px; color: #2f2f2f; line-height: 1.5; }}
    .brand {{ display: inline-flex; align-items: center; gap: 10px; color: #1a2a4a; text-decoration: none; margin-bottom: 12px; }}
    .brand .logo-mark {{ width: 36px; height: 36px; color: #1a2a4a; }}
    .brand .logo-text {{ font-size: 13px; letter-spacing: 0.12em; text-transform: uppercase; line-height: 1.25; }}
    .brand .logo-text span {{ display: block; font-size: 10px; letter-spacing: 0.18em; opacity: 0.75; }}
    .crumbs {{ font-size: 13px; color: #5a5a5a; margin: 0 0 18px; }}
    h1 {{ font-size: 1.6rem; }}
    p {{ color: #5a5a5a; }}
    a {{ color: #1a2a4a; }}
    ul {{ columns: 2; column-gap: 2rem; list-style: none; padding: 0; }}
    li {{ break-inside: avoid; margin: 0.25rem 0; font-size: 0.92rem; }}
    @media (max-width: 700px) {{ ul {{ columns: 1; }} }}
  </style>
</head>
<body>
  <a class="brand" href="../" aria-label="Mike Levy Law">
    <svg class="logo-mark" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <circle cx="24" cy="24" r="22" stroke="currentColor" stroke-width="1.5" fill="rgba(26,42,74,0.06)"/>
      <path d="M24 10 L24 14 M14 20 H34 M16 20 V34 H32 V20" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
      <path d="M20 34 V28 H28 V34" stroke="currentColor" stroke-width="1.5"/>
      <path d="M18 20 C18 16 21 14 24 14 C27 14 30 16 30 20" stroke="currentColor" stroke-width="1.5" fill="none"/>
      <circle cx="24" cy="12" r="2" fill="currentColor"/>
    </svg>
    <div class="logo-text">Mike Levy<span>Law</span></div>
  </a>
  <p class="crumbs"><a href="./">Company &amp; Broker Index</a></p>
  <h1>Company &amp; Broker Index — Full Listing</h1>
  <p>{len(rows)} review pages. Search the main index for filters; this page exists so every brief remains discoverable.</p>
  <ul>
{chr(10).join(links)}
  </ul>
</body>
</html>
"""
    (ROOT / "company-broker-index" / "sitemap.html").write_text(html, encoding="utf-8")


def main() -> None:
    brokers = load_brokers()
    today = date.today().isoformat()
    static_entries = [
        url_entry(SITE + path, today, pri, freq) for path, pri, freq in STATIC_PAGES
    ]
    review_entries = []
    for b in brokers:
        slug = b.get("slug")
        if not slug:
            continue
        last = (b.get("updated") or today)[:10]
        loc = f"{SITE}/company-broker-index/reviews/{slug}.html"
        review_entries.append(url_entry(loc, last, "0.7", "monthly"))

    all_entries = static_entries + review_entries
    if len(all_entries) <= MAX_URLS_PER_FILE:
        write_urlset(OUT, all_entries)
        print(f"Wrote {OUT} ({len(all_entries)} URLs)")
    else:
        chunks = []
        chunk: list[str] = []
        files = []
        for e in all_entries:
            chunk.append(e)
            if len(chunk) >= MAX_URLS_PER_FILE:
                chunks.append(chunk)
                chunk = []
        if chunk:
            chunks.append(chunk)
        for i, ch in enumerate(chunks, 1):
            path = CHUNK_DIR / f"sitemap-{i}.xml"
            write_urlset(path, ch)
            files.append(path.name)
            print(f"Wrote {path} ({len(ch)} URLs)")
        index_body = "\n".join(
            f"  <sitemap>\n    <loc>{escape(SITE + '/' + name)}</loc>\n    <lastmod>{today}</lastmod>\n  </sitemap>"
            for name in files
        )
        OUT.write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{index_body}\n"
            "</sitemapindex>\n",
            encoding="utf-8",
        )
        print(f"Wrote sitemap index {OUT}")

    write_html_sitemap(brokers)
    print("Wrote company-broker-index/sitemap.html")

    # Keep static review SEO pages in sync when regenerating the sitemap
    try:
        import subprocess

        subprocess.check_call(
            ["python3", str(ROOT / "tools" / "build_reviews_seo.py")],
            cwd=str(ROOT),
        )
    except Exception as exc:  # noqa: BLE001
        print(f"Warning: review SEO rebuild failed: {exc}")


if __name__ == "__main__":
    main()
