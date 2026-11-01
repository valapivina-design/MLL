# Mike Levy Law Company & Broker Index — Review Engine

Adapted from the forensicsou (`build_reviews.py`) broker-review SEO engine, with Mike Levy Law litigation messaging, Support replies, timed comments, and multilingual help threads.

## Files

| Path | Role |
|------|------|
| `data/brokers.js` | Searchable broker/company index (`window.SBL_BROKERS`) |
| `data/comments.js` | Per-slug comments (`window.SBL_COMMENTS`) |
| `js/review-engine.js` | Renders `review.html?company=<slug>` + SEO + FAQ |
| `review.html` | Brief shell |
| `../tools/import_brokers.py` | Merge/import brokers (forensic source, JSON, inbox) |
| `../tools/rebuild_comments.py` | Comments; `--new-only` for incremental adds |
| `../tools/inbox/` | Drop `*.json` / `*.jsonl` batches to merge |

## SEO properties (observed from forensicsou sample)

Per review page, `applySeo()` sets:

| Property | Scam / high-risk pattern | Legit / uncertain pattern |
|----------|--------------------------|---------------------------|
| `<title>` | `{Name} Review {Year} — Company & Broker Index \| Mike Levy Law` | `{Name} Review {Year} — Regulation, Complaints & Clone Warnings \| Mike Levy Law` |
| `meta description` | `{Name} review ({Month Year}): is {Name} a scam? Is {Name} a legit broker? Our assessment of {domain} — documented issues, withdrawal complaints, regulator checks, and how to request a consultation.` | Same question pair + “company is real / complaints under review / clones” framing |
| `meta keywords` | `{low} review, is {low} a scam, is {low} legit, is {low} a legit broker, {low} scam, {low} complaints, {low} withdrawal, {domain}, {low} investigation, {low} reddit, report {low}` | Swap withdrawal/investigation for `{low} login, fake {low}, {low} support` |
| `robots` | `index, follow, max-image-preview:large` | same |
| `author` | Mike Levy Law | same |
| `canonical` | `…/review.html?company={slug}` | same |
| `hreflang` | `en` + `x-default` (same URL until localized folders exist) | same |
| Open Graph | `og:type=article`, `og:site_name`, `og:locale=en_GB`, title/desc/url | same |
| Twitter | `summary_large_image` + title/desc | same |
| JSON-LD `@graph` | `BreadcrumbList` + `Article` + `FAQPage` | same |
| Optional | `HowTo` for consultation process (litigation-adapted) | same |

Optional broker fields: `kw_extra`, `domain`, `trustpilot.title` (appended into keywords / description).

### Crawl / indexing

| Asset | Role |
|-------|------|
| `/robots.txt` | Allow crawl; points to sitemap |
| `/sitemap.xml` | Home, index, insights, every static review URL |
| `/company-broker-index/reviews/<slug>.html` | **Canonical** SEO brief (same brief layout: risk meter, inception/reports timeline, writeup, FAQ, case CTA + Article/Review/FAQPage JSON-LD) — no JS required |
| `/company-broker-index/brief.css` | Shared brief stylesheet for static SEO reviews |
| `/company-broker-index/review.html?company=<slug>` | Interactive brief extras (comments); `rel=canonical` → static reviews URL |
| `/company-broker-index/sitemap.html` | HTML full listing (search gate bypass for crawlers) |
| Bare `review.html` (no `?company=`) | `noindex` — not a unique page |

Rebuild after broker imports:

```bash
python3 tools/build_reviews_seo.py   # static review HTML
python3 tools/build_sitemap.py       # also rebuilds review SEO pages
```

### Keyword rules

1. Always include the question pair: `is {name} a scam` and `is {name} a legit broker`.
2. Always include `{name} review` and `{name} scam` / complaints tokens.
3. Include the live **domain** when known.
4. Append `kw_extra` from research (alerts, aliases) without duplicating tokens.
5. H1 / `<title>`: primary `{Name} Review` only.
6. **Name variants** (`aliases`): H2 = `{Alias} review`. Put “is {Alias} a scam / legit broker” in the **body** (and FAQ), not the heading.
7. **Clones** (`clones`): H2 = `{domain} review`. Scam/legitimacy phrasing in body vs `officialDomain`. Keep prose professional — no SEO scaffolding language.
   - **Only** list lookalike domains we also have a record for in this index, **or** that appear in documented victim/story material for that brand. Do not invent `*-login.com` / phishing-pattern placeholders.
8. Avoid the word **indexed** in visible page copy and badges (use “On File” / “Profile” instead).

### Writing setup (tier voice)

- **scam / high**: Direct record + help intake. Do not invent convictions. Litigation CTA, not recovery-fee cyber copy.
- **legit**: “No — real business” + clone / complaint triage. Soft comments only.
- **uncertain / medium**: Softer summary; avoid “it’s a scam” as a finding.
- **Tone**: confidential consultation · Support replies · contact form — never “firm reply” stars.

## FAQ templates (Mike Levy Law–adapted from forensicsou)

### Scam / high risk

1. `Is {Name} a legit broker?` — screen-balance vs real payout framing + blurb + “send date and how you paid.”
2. `Can you close my {Name} account, or have the person who phoned me call again?` — not affiliated; cannot close accounts or impersonate the broker.
3. `{Name} says I must pay a tax or fee before withdrawing — should I?` — No; real firms deduct from balance.
4. `What do you do with what I send?` — confidential case review for counsel pathways; not a bank/police replacement.
5. `How does your process work?` — free initial look → document timeline → advise next legal/reporting steps.

### Legit / uncertain

1. `Is {Name} a scam?` — No / not established; clones often drive “scam” searches.
2. `Is {Name} a legit broker?` — company appears real; verify domain yourself.
3. `Is {Name} regulated?` — point to public registers when known; else verify entity on statement.
4. `I lost money to someone claiming to be {Name}` — likely impersonation; preserve evidence.
5. `How do I check the {Name} site I used is genuine?` — type official domain; compare character-by-character.
6. Process FAQ (same as above).

FAQ is rendered in-page (`#faq-list`) and mirrored into `FAQPage` JSON-LD.

## Comment timing & language

- **Sources (Trustpilot / forums / etc.)**: used for research only. **Never** show platform names or “Trustpilot” badges on the frontend.
- **Big scam / high risk**: up to **4** comments; **Support replies only on important losses** (material amounts), not every thread.
- **Legit / uncertain**: 1 softer “verify real company” comment; usually **no** Support reply.
- Timing: staggered **11–47 days**; Support **+1–3 days** when present (≤ today).
- **Language**: DE/ES/IT/FR/PT/NL/PL/RO/TR when country/hint fits; Support matches that language.
- On-page SEO: H1 `{Name} Review`; H2s + meta description carry scam/legit/withdrawal intent; alias H2s use the same keyword shape for variants.
- Rebuild: `python3 tools/rebuild_comments.py` (preserves curated victim threads such as Next Forrest).

## Import / grow the index

Default is **merge-safe**: new slugs are added; curated fields (`aliases`, `clones`, `timeline`, `fundFlow`, `officialDomain`, …) on existing slugs are kept.

```bash
# Full forensic source (already done once)
python3 tools/import_brokers.py --all

# Add a JSON batch (Mike Levy Law–shaped or forensic n/s/t/d)
python3 tools/import_brokers.py --no-forensic --json path/to/batch.json

# Drop files in tools/inbox/ then:
python3 tools/import_brokers.py --no-forensic --inbox

# Comments for new slugs only (default after import)
python3 tools/rebuild_comments.py --new-only

# Force regenerate all non-curated comment threads
python3 tools/rebuild_comments.py --force
```

Inbox format: see `tools/inbox/README.md`.

Source (read-only forensic): `/Users/user/Documents/forensicsou-main 4/js/brokers-data.js`, `research/_review_tp2.jsonl`.
