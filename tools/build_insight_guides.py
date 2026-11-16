#!/usr/bin/env python3
"""Build keyword-slug insight guides (victim-intent funnel).

Creates /insights/<keyword-slug>/index.html pages modeled on forensicsou
guide SEO: primary keyword in URL, commercial FAQs, review deep-links, CTA.

  python3 tools/build_insight_guides.py
"""
from __future__ import annotations

import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "insights"
SITE = "https://mikelevylaw.com"

GUIDES = [
    {
        "slug": "broker-withdrawal-problem",
        "kicker": "Withdrawals · Updated November 2026",
        "h1": "Broker Withdrawal Problem? Why Your Payout Is Stalled — and What to Do",
        "title": "Broker Withdrawal Problem: Pending Payouts & Next Steps | Mike Levy Law",
        "desc": "Broker withdrawal problem? Why payouts stall for weeks, fee demands before release, and confidential options if your broker will not pay out.",
        "keywords": "broker withdrawal problem, why is my broker not paying out, broker holding my funds hostage, withdrawal pending for weeks, broker charged hidden fees to withdraw, can't withdraw from broker",
        "lead": "You click withdraw, the status flips to pending — and nothing moves for days, then weeks. A broker withdrawal problem is often the first hard signal that something is wrong. How you respond in the next two weeks can decide which options stay open.",
        "sections": [
            (
                "Why withdrawals stall",
                "<p>Operational delays happen. What matters is the <strong>pattern</strong>: one dated explanation and a trackable transfer is different from shifting excuses — new taxes, unlock fees, “compliance” payments, or silence after a small test payout worked once.</p>"
                "<p>If support keeps demanding fresh money before releasing your own balance, treat that as a red flag. Preserve every message and do not pay another fee to “release” funds.</p>",
            ),
            (
                "What to do in the first 14 days",
                "<ol>"
                "<li>Stop sending money — including tax, commission, or unlock fees.</li>"
                "<li>Export chats, emails, account statements, and the exact domain you used.</li>"
                "<li>Notify your bank or card issuer and ask about recall or chargeback windows.</li>"
                "<li>Compare the platform name in our <a href=\"../../company-broker-index/\">Company &amp; Broker Index</a>.</li>"
                "<li>Request a confidential consultation if the loss is material.</li>"
                "</ol>",
            ),
            (
                "Related broker briefs",
                "<p>These reviews often appear in stalled-withdrawal discussions — use them to match the domain you paid, not just a brand name:</p>"
                "<ul>"
                "<li><a href=\"../../company-broker-index/reviews/flowingfunded-review.html\">Flowing Funded review</a> — prop-style funding complaints</li>"
                "<li><a href=\"../../company-broker-index/reviews/mgmt-forex-review.html\">MGMT Forex review</a> — withdrawal and fee friction patterns</li>"
                "<li><a href=\"../../company-broker-index/reviews/cryptofundtrader-review.html\">CRYPTO FUND TRADER review</a> — public-warning style brief</li>"
                "</ul>",
            ),
        ],
        "faqs": [
            (
                "Why has my broker withdrawal been pending for weeks?",
                "A short delay with a clear timeline can be operational. Changing stories, new fee demands, or a freeze after a tiny test payout usually means you should stop paying and preserve evidence immediately.",
            ),
            (
                "Can a broker legally charge a new fee before I withdraw?",
                "Legitimate charges are normally deducted from the balance under disclosed terms. A demand to send new money — tax, unlock, or commission — before your own funds are released is a classic advance-fee pattern. Do not pay it.",
            ),
            (
                "Is my money gone if the broker will not pay?",
                "Not always. Card disputes, wire recalls, crypto tracing, and civil or regulatory paths depend on how you paid and how recent the transfer is. Odds fall with time — that is why early evidence and a sober assessment matter.",
            ),
        ],
        "related": [
            ("../fund-recovery-services/", "Fund recovery services"),
            ("../chargeback-investment-fraud/", "Chargeback after investment fraud"),
            ("../recover-stolen-crypto.html", "Recover stolen crypto"),
        ],
        "source": "insights-broker-withdrawal",
    },
    {
        "slug": "fund-recovery-services",
        "kicker": "Recovery scams · Updated November 2026",
        "h1": "Fund Recovery Services: What Helps — and What Is a Second Scam",
        "title": "Fund Recovery Services: Real Help vs Recovery Scams | Mike Levy Law",
        "desc": "Fund recovery services explained: lawful consultation and tracing vs recovery scams that charge upfront fees to “unlock” stolen money.",
        "keywords": "fund recovery services, recovery scam, crypto recovery service, recover stolen funds, upfront recovery fee, fake fund recovery",
        "lead": "After a loss, strangers often offer “fund recovery services” that guarantee results for an upfront fee. Some are a second scam. This guide separates lawful next steps from recovery-scam red flags.",
        "sections": [
            (
                "What legitimate help looks like",
                "<p>Real counsel or investigators review evidence, explain bank, card, crypto, regulator, and civil options, and are clear that <strong>recovery is never guaranteed</strong>. They do not ask you to send cryptocurrency to “unlock” a phantom balance.</p>"
                "<p>Mike Levy Law offers confidential consultations for material losses — evidence first, then pathway advice. We do not sell a recovery deposit product.</p>",
            ),
            (
                "Recovery-scam red flags",
                "<ul>"
                "<li>Guaranteed return of funds or “we already found your money.”</li>"
                "<li>Upfront crypto / gift-card / wire fees to release a recovery.</li>"
                "<li>Pressure to act in minutes or stay off the phone with your bank.</li>"
                "<li>Impersonation of lawyers, police, or exchanges.</li>"
                "</ul>"
                "<p>If someone contacts you unsolicited after a broker loss, assume risk until proven otherwise.</p>",
            ),
            (
                "Safer order of operations",
                "<ol>"
                "<li>Preserve wallets, chats, and payment proofs.</li>"
                "<li>Work your bank/card/exchange dispute channels.</li>"
                "<li><a href=\"../report-a-scam.html\">Report the scam</a> to the right authorities.</li>"
                "<li>Read <a href=\"../recover-stolen-crypto.html\">recover stolen crypto</a> for realistic pathways.</li>"
                "<li>Request a confidential legal consultation — not a paid “recovery unlock.”</li>"
                "</ol>",
            ),
            (
                "Related broker briefs",
                "<ul>"
                "<li><a href=\"../../company-broker-index/reviews/blue-guardian-review.html\">Blue Guardian review</a></li>"
                "<li><a href=\"../../company-broker-index/reviews/getleveraged-review.html\">Get Leveraged review</a></li>"
                "<li><a href=\"../../company-broker-index/reviews/diversyfund-review.html\">DiversyFund review</a></li>"
                "</ul>",
            ),
        ],
        "faqs": [
            (
                "Are fund recovery services legitimate?",
                "Some investigative and legal services are legitimate. Many cold-call “recovery” firms are not. Guarantees plus upfront unlock fees are strong warning signs of a recovery scam.",
            ),
            (
                "Should I pay a fee to get my money released?",
                "No. Do not pay a stranger to unlock stolen or withheld funds. That pattern is how victims lose a second time.",
            ),
            (
                "What should I do instead?",
                "Preserve evidence, contact your payment providers, file reports, and — if the loss is material — request a confidential consultation with counsel who will not demand a recovery deposit.",
            ),
        ],
        "related": [
            ("../broker-withdrawal-problem/", "Broker withdrawal problem"),
            ("../recover-stolen-crypto.html", "Recover stolen crypto"),
            ("../report-a-scam.html", "How to report a scam"),
        ],
        "source": "insights-fund-recovery",
    },
    {
        "slug": "chargeback-investment-fraud",
        "kicker": "Card disputes · Updated November 2026",
        "h1": "Chargeback for Investment Fraud: When Card Disputes Can Help",
        "title": "Chargeback Investment Fraud: Card Dispute Options | Mike Levy Law",
        "desc": "Chargeback investment fraud guide: when card disputes apply after a fake broker or trading scam, evidence banks ask for, and limits of chargebacks.",
        "keywords": "chargeback investment fraud, chargeback failed investment, credit card chargeback trading scam, dispute broker payment, card chargeback forex scam",
        "lead": "If you paid a broker or “investment” platform by credit or debit card, a chargeback can be one of the fastest tools — but only inside short windows and with the right evidence pack.",
        "sections": [
            (
                "When a chargeback may apply",
                "<p>Card networks allow disputes for services not provided, misrepresentation, or fraud in many regions. An online trading account that never pays out, or a platform that demanded unlock fees, may support a merchant dispute — your issuer decides.</p>"
                "<p>Wire transfers and pure crypto payments usually do <strong>not</strong> use the same chargeback rules; see our <a href=\"../bank-dispute-wire-transfer-scam/\">bank dispute / wire transfer</a> guide.</p>",
            ),
            (
                "Evidence banks typically want",
                "<ul>"
                "<li>Merchant name / descriptor on the statement</li>"
                "<li>Domain you used and account screenshots</li>"
                "<li>Chat or email showing fee demands or blocked withdrawals</li>"
                "<li>Police or cybercrime reference numbers when available</li>"
                "</ul>",
            ),
            (
                "Related reading &amp; reviews",
                "<ul>"
                "<li><a href=\"../deadline-for-chargeback/\">Deadline for chargeback</a></li>"
                "<li><a href=\"../../company-broker-index/reviews/axi-select-review.html\">Axi Select review</a></li>"
                "<li><a href=\"../../company-broker-index/reviews/e8-markets-review.html\">E8 Markets review</a></li>"
                "</ul>",
            ),
        ],
        "faqs": [
            (
                "Can I chargeback a trading or investment scam?",
                "Sometimes, if you paid by card and act inside your issuer’s deadline with clear evidence. Success is not guaranteed and depends on the network rules and merchant category.",
            ),
            (
                "What if the chargeback is denied?",
                "You may still have bank complaint routes, regulator reports, or civil options. Preserve the denial letter — it is useful for counsel.",
            ),
            (
                "Does a chargeback replace legal advice?",
                "No. It is a payment-network tool. A confidential consultation can help you sequence chargeback, reporting, and other pathways without missing deadlines.",
            ),
        ],
        "related": [
            ("../deadline-for-chargeback/", "Chargeback deadlines"),
            ("../broker-withdrawal-problem/", "Broker withdrawal problem"),
            ("../recover-stolen-crypto.html", "Recover stolen crypto"),
        ],
        "source": "insights-chargeback",
    },
    {
        "slug": "deadline-for-chargeback",
        "kicker": "Deadlines · Updated November 2026",
        "h1": "Deadline for Chargeback After a Trading or Investment Scam",
        "title": "Deadline for Chargeback: How Long You Have After a Scam | Mike Levy Law",
        "desc": "Deadline for chargeback after investment or trading fraud — typical windows, why speed matters, and what to file with your card issuer.",
        "keywords": "deadline for chargeback, chargeback time limit, how long to dispute card payment, chargeback window trading scam, dispute deadline investment fraud",
        "lead": "Chargeback rights expire. If a fake broker or investment site took card payments, waiting weeks can close the window even when the facts are strong.",
        "sections": [
            (
                "How long do you usually have?",
                "<p>Exact deadlines depend on your card network, issuer, and country — often measured in <strong>days to a few months</strong> from the transaction or from when you discovered the problem. Do not rely on internet averages; call your issuer and ask for the dispute deadline in writing if possible.</p>",
            ),
            (
                "What to do today",
                "<ol>"
                "<li>List every card charge tied to the platform.</li>"
                "<li>Open a dispute / fraud claim immediately.</li>"
                "<li>Attach domain, chats, and withdrawal refusal screenshots.</li>"
                "<li>Read <a href=\"../chargeback-investment-fraud/\">chargeback for investment fraud</a> for the evidence pack.</li>"
                "</ol>",
            ),
            (
                "Related broker briefs",
                "<ul>"
                "<li><a href=\"../../company-broker-index/reviews/wsfunded-review.html\">WSFunded review</a></li>"
                "<li><a href=\"../../company-broker-index/reviews/upcomers-review.html\">Upcomers review</a></li>"
                "<li><a href=\"../../company-broker-index/reviews/the-trading-pit-review.html\">The Trading Pit review</a></li>"
                "</ul>",
            ),
        ],
        "faqs": [
            (
                "Is there a universal chargeback deadline?",
                "No. Networks and issuers differ. Treat every week as expensive — ask your bank for the specific deadline that applies to your card.",
            ),
            (
                "What if I am already past the deadline?",
                "Chargeback may be closed, but bank complaints, regulator reports, and civil options can still exist. Get the denial in writing and preserve evidence.",
            ),
            (
                "Should I wait for the broker to “resolve” it first?",
                "Do not burn the chargeback window waiting on endless support tickets. Open the dispute while you still can, then continue documenting the broker’s responses.",
            ),
        ],
        "related": [
            ("../chargeback-investment-fraud/", "Chargeback investment fraud"),
            ("../bank-dispute-wire-transfer-scam/", "Bank dispute &amp; wire scams"),
            ("../broker-withdrawal-problem/", "Broker withdrawal problem"),
        ],
        "source": "insights-chargeback-deadline",
    },
    {
        "slug": "bank-dispute-wire-transfer-scam",
        "kicker": "Wires &amp; banks · Updated November 2026",
        "h1": "Bank Dispute After a Wire Transfer Scam or Fake Broker",
        "title": "Bank Dispute Wire Transfer Scam: Recalls & Next Steps | Mike Levy Law",
        "desc": "Bank dispute after a wire transfer scam or fake broker: recall requests, what banks can and cannot reverse, and evidence that helps.",
        "keywords": "bank dispute wire transfer scam, wire recall investment scam, bank transfer to fake broker, reverse wire transfer fraud, SWIFT recall scam",
        "lead": "Wires move fast and are hard to reverse. If you sent a bank transfer to a fake broker or investment pitch, a same-day or next-day recall attempt still matters — even when success rates are low.",
        "sections": [
            (
                "Act with the sending bank immediately",
                "<p>Ask for a <strong>wire recall / recall request</strong> and a fraud escalation. Provide beneficiary details, reference numbers, and why you believe the payee is fraudulent. Delays of even a few business days sharply reduce odds.</p>",
            ),
            (
                "What banks usually cannot do",
                "<p>Once funds are withdrawn by the beneficiary, banks often cannot pull money back unilaterally. That does not end the file — police reports, civil claims, and tracing can still matter — but the recall clock is separate and short.</p>",
            ),
            (
                "Related guides &amp; reviews",
                "<ul>"
                "<li><a href=\"../broker-withdrawal-problem/\">Broker withdrawal problem</a></li>"
                "<li><a href=\"../chargeback-investment-fraud/\">Chargeback investment fraud</a> (if any card legs exist)</li>"
                "<li><a href=\"../../company-broker-index/reviews/sure-leverage-funding-review.html\">Sure Leverage Funding review</a></li>"
                "<li><a href=\"../../company-broker-index/reviews/nordic-funder-review.html\">Nordic Funder review</a></li>"
                "</ul>",
            ),
        ],
        "faqs": [
            (
                "Can a bank reverse a wire to a scam broker?",
                "Sometimes if you act immediately and funds remain at the receiving bank. Many recalls fail once money is moved onward. Still request the recall and keep the reference.",
            ),
            (
                "What evidence should I give the bank?",
                "Beneficiary name and account, transfer references, the domain or app you used, chats promising returns or blocking withdrawals, and any police report number.",
            ),
            (
                "Is a failed recall the end?",
                "No. Reporting, tracing, and civil options may remain. A confidential consultation can help sequence those steps after the bank process.",
            ),
        ],
        "related": [
            ("../deadline-for-chargeback/", "Chargeback deadlines"),
            ("../fund-recovery-services/", "Fund recovery services"),
            ("../report-a-scam.html", "How to report a scam"),
        ],
        "source": "insights-wire-dispute",
    },
    {
        "slug": "sue-forex-broker",
        "kicker": "Civil options · Updated November 2026",
        "h1": "Sue a Forex Broker? When Civil Claims May Make Sense",
        "title": "Sue Forex Broker: Civil Options After Trading Losses | Mike Levy Law",
        "desc": "Sue a forex broker? When civil claims may apply after withdrawal blocks or clone sites, what evidence matters, and realistic limits.",
        "keywords": "sue forex broker, sue online broker, lawsuit against trading platform, civil claim broker scam, forex broker legal action",
        "lead": "“Can I sue my forex broker?” depends on who you actually paid, where they are, and whether a real legal person can be served. Clones of licensed brands are not the same as a dispute with a regulated firm.",
        "sections": [
            (
                "Identify the correct defendant",
                "<p>Save the exact domain, app name, company paperwork, and payment beneficiary. Many victims sue the famous brand they saw in an ad while funds went to a lookalike. Our <a href=\"../../company-broker-index/\">broker index</a> and clone-focused briefs exist to reduce that mistake.</p>",
            ),
            (
                "When civil claims are more realistic",
                "<ul>"
                "<li>Identifiable company, officers, or recoverable assets</li>"
                "<li>Clear paper trail of deposits and blocked withdrawals</li>"
                "<li>Licensed firm with ombudsman or court access in a usable forum</li>"
                "</ul>"
                "<p>Offshore shells with no attachable assets may make litigation uneconomic even when the facts are ugly. That assessment is case-specific.</p>",
            ),
            (
                "Related briefs",
                "<ul>"
                "<li><a href=\"../online-trading-forex-scams.html\">Online trading &amp; forex scams</a></li>"
                "<li><a href=\"../../company-broker-index/reviews/fintokei-review.html\">Fintokei review</a></li>"
                "<li><a href=\"../../company-broker-index/reviews/audacity-capital-review.html\">Audacity Capital review</a></li>"
                "<li><a href=\"../../company-broker-index/reviews/alinea-invest-review.html\">Alinea Invest review</a></li>"
                "</ul>",
            ),
        ],
        "faqs": [
            (
                "Can I sue an online forex broker?",
                "Possibly, if a suable defendant and forum exist. Many scam platforms are designed to be hard to sue. Identification of the real counterparty comes first.",
            ),
            (
                "Is suing better than a chargeback or recall?",
                "Use time-sensitive payment disputes first when available. Litigation is slower and costlier; it is not a substitute for missing a chargeback deadline.",
            ),
            (
                "Will Mike Levy Law take every broker case?",
                "We review material matters confidentially and are candid when a file is not economically or jurisdictionally viable. No outcome is guaranteed.",
            ),
        ],
        "related": [
            ("../broker-withdrawal-problem/", "Broker withdrawal problem"),
            ("../online-trading-forex-scams.html", "Forex &amp; trading scams"),
            ("../fund-recovery-services/", "Fund recovery services"),
        ],
        "source": "insights-sue-forex",
    },
]


def page_html(g: dict) -> str:
    slug = g["slug"]
    canon = f"{SITE}/insights/{slug}/"
    contact = f"../../index.html?source={escape(g['source'])}#contact"
    faq_ld = [
        {
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        }
        for q, a in g["faqs"]
    ]
    faq_html = "\n".join(
        f"<details{' open' if i == 0 else ''}><summary>{escape(q)}</summary><p>{escape(a)}</p></details>"
        for i, (q, a) in enumerate(g["faqs"])
    )
    sections = "\n".join(
        f"<h2>{escape(h)}</h2>\n{body}" for h, body in g["sections"]
    )
    related = "\n".join(
        f'        <a href="{href}">{label}</a>' for href, label in g["related"]
    )
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Insights", "item": f"{SITE}/insights/"},
                    {"@type": "ListItem", "position": 3, "name": g["h1"], "item": canon},
                ],
            },
            {
                "@type": "Article",
                "headline": g["h1"],
                "description": g["desc"],
                "inLanguage": "en-US",
                "datePublished": "2026-11-16",
                "dateModified": "2026-11-16",
                "author": {"@type": "Organization", "name": "Mike Levy Law", "url": f"{SITE}/"},
                "publisher": {"@type": "Organization", "name": "Mike Levy Law", "url": f"{SITE}/"},
                "mainEntityOfPage": {"@type": "WebPage", "@id": canon},
                "keywords": g["keywords"],
            },
            {"@type": "FAQPage", "mainEntity": faq_ld},
        ],
    }
    ld = json.dumps(graph, ensure_ascii=False)
    return f"""<!DOCTYPE html>
<html lang="en-US">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{escape(g["title"])}</title>
  <meta name="description" content="{escape(g["desc"])}" />
  <meta name="keywords" content="{escape(g["keywords"])}" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <meta name="author" content="Mike Levy Law" />
  <link rel="canonical" href="{canon}" />
  <link rel="alternate" hreflang="en" href="{canon}" />
  <link rel="alternate" hreflang="x-default" href="{canon}" />
  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="Mike Levy Law" />
  <meta property="og:locale" content="en_US" />
  <meta property="og:title" content="{escape(g["title"])}" />
  <meta property="og:description" content="{escape(g["desc"])}" />
  <meta property="og:url" content="{canon}" />
  <meta property="og:image" content="{SITE}/hero-books.jpg" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{escape(g["title"])}" />
  <meta name="twitter:description" content="{escape(g["desc"])}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700&family=Playfair+Display:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../styles.css" />
  <script type="application/ld+json">{ld}</script>
</head>
<body>
  <header class="top">
    <div class="wrap-wide top-inner">
      <a class="brand" href="../../index.html" aria-label="Mike Levy Law">
        <svg class="logo-mark" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <circle cx="24" cy="24" r="22" stroke="currentColor" stroke-width="1.5" fill="rgba(255,255,255,0.06)"/>
          <path d="M24 10 L24 14 M14 20 H34 M16 20 V34 H32 V20" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M20 34 V28 H28 V34" stroke="currentColor" stroke-width="1.5"/>
          <path d="M18 20 C18 16 21 14 24 14 C27 14 30 16 30 20" stroke="currentColor" stroke-width="1.5" fill="none"/>
          <circle cx="24" cy="12" r="2" fill="currentColor"/>
        </svg>
        <div class="logo-text">Mike Levy<span>Law</span></div>
      </a>
      <nav class="crumbs" aria-label="Breadcrumb"><a href="../../index.html">Home</a><span>/</span><a href="../">Insights</a><span>/</span><span>{escape(slug.replace("-", " "))}</span></nav>
    </div>
  </header>
  <main class="wrap">
    <div class="hero">
      <p class="kicker">{escape(g["kicker"])}</p>
      <h1>{escape(g["h1"])}</h1>
      <p class="lead">{escape(g["lead"])}</p>
    </div>
    <article class="article">
{sections}
      <div class="related">
{related}
      </div>
    </article>
    <section class="faq-block" aria-labelledby="faq-h">
      <h2 id="faq-h">Frequently asked questions</h2>
      <p class="faq-lead">Straight answers on next steps, deadlines, and when a confidential consultation may help.</p>
      <div class="faq">
{faq_html}
      </div>
    </section>
    <div class="cta-strip">
      <div>
        <strong>Need a confidential review?</strong>
        <p>If this matches your situation, we can compare your records with the public pattern and advise on reporting or litigation pathways — without obligation. No recovery guarantees.</p>
      </div>
      <a href="{contact}">Request a consultation</a>
    </div>
    <p class="note">Informational only. Does not constitute legal advice or a guarantee of recovery. Contacting Mike Levy Law does not create an attorney-client relationship.</p>
  </main>
  <footer class="site-footer">
    <div class="wrap-wide site-footer-inner">
      <p><a href="../">Insights</a> · <a href="../../company-broker-index/">Company &amp; Broker Index</a> · <a href="{contact}">Contact</a> · <a href="../../legal/privacy-policy.html">Privacy</a> · <a href="../../legal/terms-of-use.html">Terms</a> · <a href="../../legal/disclaimer.html">Disclaimer</a></p>
      <p>&copy; MLL 2026</p>
      <p class="footer-nap">1395 Brickell Ave, Suite 800 · Miami, FL 33131 · USA · <a href="mailto:info@mikelevylaw.com">info@mikelevylaw.com</a></p>
    </div>
  </footer>
  <script src="/js/tawk-mll.js" defer></script>
</body>
</html>
"""


def main() -> None:
    for g in GUIDES:
        dest = OUT / g["slug"]
        dest.mkdir(parents=True, exist_ok=True)
        path = dest / "index.html"
        path.write_text(page_html(g), encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT)}")
    print(f"Done — {len(GUIDES)} keyword guides")


if __name__ == "__main__":
    main()
