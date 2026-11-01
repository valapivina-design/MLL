#!/usr/bin/env python3
"""Rebuild SBL_COMMENTS for every broker in brokers.js.

Rules (from forensicsou sample + Mike Levy Law litigation voice):
  - Trustpilot: keep public rating title when present (source=trustpilot)
  - Scam / high risk: help-seeking comments; Support replies 1–3 days later
  - Legit / uncertain: simpler “need advice” comments (not hard scam language)
  - When comment country maps to DE/ES/IT/FR/PT/NL/PL/RO/TR: write comment
    AND Support reply in that language
  - Preserve manual overrides (e.g. next-forrest Trustpilot victim text)
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import date, timedelta
from pathlib import Path

ROOT = Path("/Users/user/Desktop/STIRLING")
BROKERS_JS = ROOT / "company-broker-index" / "data" / "brokers.js"
COMMENTS_JS = ROOT / "company-broker-index" / "data" / "comments.js"

COUNTRY_LANG = {
    "Germany": "de",
    "Austria": "de",
    "Switzerland": "de",
    "Spain": "es",
    "Mexico": "es",
    "Chile": "es",
    "Colombia": "es",
    "Italy": "it",
    "France": "fr",
    "Portugal": "pt",
    "Brazil": "pt",
    "Netherlands": "nl",
    "Belgium": "nl",
    "Poland": "pl",
    "Romania": "ro",
    "Turkey": "tr",
}

# Brokers with known non-English victim / complaint footprint → force one comment in that lang
SLUG_LANG_HINTS = {
    "next-forrest-review": "de",
    "betano-review": "de",
    "ovb-willemot-review": "de",
    "monaxa-review": "es",
    "winprofx-review": "es",
    "grand-markets-review": "es",
    "fliptrade-group-review": "pt",
    "mbfx-review": "pt",
    "intrade24-review": "de",
}

NAMES = [
    ("Caroline Hayes", "CH"),
    ("Priya Nair", "PN"),
    ("Thomas Brennan", "TB"),
    ("Daniel Whitmore", "DW"),
    ("Amira Hassan", "AH"),
    ("Kenji Watanabe", "KW"),
    ("Sofia Mendoza", "SM"),
    ("Lucas Okonkwo", "LO"),
    ("Elena Popescu", "EP"),
    ("Marcus Berg", "MB"),
    ("Hannah Vo", "HV"),
    ("Omar Al Farsi", "OA"),
    ("Isabella Rossi", "IR"),
    ("Noah Pretorius", "NP"),
    ("Mei Lin Chen", "ML"),
    ("Hans Müller", "HM"),
    ("Clara Schmidt", "CS"),
    ("Luis García", "LG"),
    ("Ana Costa", "AC"),
    ("Giulia Bianchi", "GB"),
]

# Important-loss threads (we reply only to these)
IMPORTANT = {
    "en": (
        "Lost a large deposit and cannot withdraw",
        "I put in a substantial sum after months of “profits” on the dashboard. When I tried to withdraw, the account was frozen and they demanded extra fees. The amount still stuck is significant for my family. Please help — is a confidential review still possible?",
    ),
    "de": (
        "Hoher Verlust — Auszahlung blockiert",
        "Ich habe eine erhebliche Summe eingezahlt. Die Auszahlung wurde blockiert und es wurden zusätzliche Gebühren verlangt. Für meine Familie ist der Betrag existenziell. Bitte helfen Sie — ist eine vertrauliche Prüfung noch möglich?",
    ),
    "es": (
        "Pérdida importante — no puedo retirar",
        "Deposité una suma importante tras ver “beneficios” en el panel. Al retirar, congelaron la cuenta y pedían más comisiones. Es una cantidad grave para mi familia. ¿Pueden revisar el caso de forma confidencial?",
    ),
    "it": (
        "Perdita importante — prelievo bloccato",
        "Ho versato una somma rilevante. Il prelievo è bloccato e chiedono ulteriori commissioni. Per la mia famiglia è un importo serio. Potete valutare il fascicolo in modo confidenziale?",
    ),
    "fr": (
        "Perte importante — retrait bloqué",
        "J’ai déposé une somme importante. Le retrait est bloqué et l’on exige de nouveaux frais. Pour ma famille, le montant est grave. Pouvez-vous examiner le dossier de façon confidentielle ?",
    ),
    "pt": (
        "Perda significativa — saque bloqueado",
        "Depositei um valor elevado. O saque foi bloqueado e pedem taxas extras. Para a minha família o montante é grave. É possível uma análise confidencial?",
    ),
    "nl": (
        "Groot verlies — opname geblokkeerd",
        "Ik heb een aanzienlijk bedrag gestort. Opnames zijn geblokkeerd en er worden extra kosten gevraagd. Voor mijn gezin is dit ernstig. Kunnen jullie het dossier vertrouwelijk beoordelen?",
    ),
    "pl": (
        "Duża strata — wypłata zablokowana",
        "Wpłaciłem znaczną kwotę. Wypłata została zablokowana i żądają dodatkowych opłat. Dla mojej rodziny to poważna strata. Czy możliwa jest poufna analiza?",
    ),
    "ro": (
        "Pierdere importantă — retragere blocată",
        "Am depus o sumă importantă. Retragerea e blocată și cer taxe suplimentare. Pentru familia mea suma e gravă. Puteți analiza confidențial dosarul?",
    ),
    "tr": (
        "Büyük kayıp — çekim engellendi",
        "Önemli bir tutar yatırdım. Çekim engellendi ve ek ücret istendi. Ailem için ciddi bir tutar. Gizli bir inceleme mümkün mü?",
    ),
}

# Help-seeking (scam / high risk) — no Support reply unless marked important
HELP = {
    "en": [
        (
            "Could not withdraw my funds",
            "I deposited money and everything looked fine until withdrawals stopped working. Support kept delaying. I feel scammed. Is there anything I can still do?",
        ),
        (
            "Promised safety that was not there",
            "They advertised safety and protection. I only found out how exposed I was when I could not get my money out. What documents should I keep?",
        ),
        (
            "Still waiting on answers",
            "I still have screenshots and bank transfers. Does anyone know if claims are still open, and who I should contact?",
        ),
        (
            "Account locked after small test withdrawal",
            "They let a tiny withdrawal through once. The larger request never completed. Chat logs and wallet IDs are saved.",
        ),
    ],
    "de": [
        (
            "Auszahlung nicht möglich",
            "Ich habe eingezahlt und alles wirkte seriös, bis die Auszahlung nicht mehr funktionierte. Der Support hat nur hingehalten. Ich fühle mich betrogen. Bitte helfen Sie — gibt es noch etwas, das ich tun kann?",
        ),
        (
            "Dokumente sichern — bitte um Rat",
            "Mir wurde Sicherheit versprochen. Als ich auszahlen wollte, kamen nur neue Gebührenforderungen. Welche Unterlagen sollte ich aufbewahren, und wen kann ich kontaktieren?",
        ),
    ],
    "es": [
        (
            "No puedo retirar mis fondos",
            "Deposé dinero y todo parecía bien hasta que los retiros dejaron de funcionar. El soporte solo daba largas. Me siento estafado. Por favor ayuden — ¿hay algo que aún pueda hacer?",
        ),
        (
            "Sigo esperando respuestas",
            "Todavía tengo capturas y transferencias bancarias. ¿Alguien sabe si aún se pueden presentar reclamaciones y a quién debo contactar?",
        ),
    ],
    "it": [
        (
            "Non riesco a prelevare",
            "Ho depositato e tutto sembrava a posto finché i prelievi non hanno più funzionato. Il supporto rimandava continuamente. Mi sento truffato. Per favore aiutatemi — c’è ancora qualcosa che posso fare?",
        ),
    ],
    "fr": [
        (
            "Impossible de retirer mes fonds",
            "J’ai déposé de l’argent et tout semblait correct jusqu’à ce que les retraits cessent de fonctionner. Le support ne faisait que temporiser. Je me sens arnaqué. Aidez-moi — que puis-je encore faire ?",
        ),
    ],
    "pt": [
        (
            "Não consigo sacar meus fundos",
            "Depositei e tudo parecia bem até os saques pararem de funcionar. O suporte só atrasava. Sinto-me lesado. Por favor ajudem — ainda há algo que eu possa fazer?",
        ),
    ],
    "nl": [
        (
            "Kan mijn geld niet opnemen",
            "Ik heb gestort en alles leek in orde totdat opnames niet meer werkten. Support bleef uitstellen. Ik voel me opgelicht. Help alsjeblieft — is er nog iets dat ik kan doen?",
        ),
    ],
    "pl": [
        (
            "Nie mogę wypłacić środków",
            "Wpłaciłem pieniądze i wszystko wyglądało dobrze, aż wypłaty przestały działać. Support tylko zwlekał. Czuję się oszukany. Proszę o pomoc — czy mogę jeszcze coś zrobić?",
        ),
    ],
    "ro": [
        (
            "Nu pot retrage fondurile",
            "Am depus bani și totul părea în regulă până când retragerile au încetat să funcționeze. Suportul tot amâna. Mă simt înșelat. Vă rog ajutați-mă — mai pot face ceva?",
        ),
    ],
    "tr": [
        (
            "Paramı çekemiyorum",
            "Para yatırdım, her şey yolunda görünüyordu ta ki çekimler çalışmayı bırakana kadar. Destek sürekli oyaladı. Dolandırıldığımı hissediyorum. Lütfen yardım edin — hâlâ yapabileceğim bir şey var mı?",
        ),
    ],
}

SUPPORT = {
    "en": "We’re sorry to hear what happened. If you would like a confidential review of your situation, please contact us and share what you can about your account and timeline.",
    "de": "Es tut uns leid, was Ihnen widerfahren ist. Wenn Sie eine vertrauliche Prüfung Ihres Falls wünschen, kontaktieren Sie uns bitte und schildern Sie Konto sowie Zeitablauf.",
    "es": "Lamentamos lo ocurrido. Si desea una revisión confidencial de su caso, contáctenos y comparta lo que pueda sobre su cuenta y el cronograma.",
    "it": "Ci dispiace per quanto accaduto. Se desidera un esame confidenziale della sua situazione, ci contatti e condivida quanto può su conto e tempistica.",
    "fr": "Nous sommes désolés pour ce qui vous est arrivé. Pour un examen confidentiel de votre dossier, contactez-nous et précisez le compte et le calendrier.",
    "pt": "Lamentamos o ocorrido. Se quiser uma análise confidencial do seu caso, contacte-nos e partilhe o que puder sobre a conta e o cronograma.",
    "nl": "Het spijt ons wat u is overkomen. Wilt u een vertrouwelijke beoordeling van uw zaak, neem dan contact op en deel wat u kunt over rekening en tijdlijn.",
    "pl": "Przykro nam z powodu tej sytuacji. Jeśli chce Pan/Pani poufnej analizy sprawy, prosimy o kontakt i opis konta oraz harmonogramu.",
    "ro": "Ne pare rău pentru ce s-a întâmplat. Dacă doriți o analiză confidențială, contactați-ne și descrieți contul și calendarul.",
    "tr": "Başınıza gelene üzüldük. Durumunuzun gizli bir incelemesini isterseniz bizimle iletişime geçin; hesap ve zaman çizelgenizi paylaşın.",
}

CTA = {
    "en": "Contact us for a consultation →",
    "de": "Kontakt für eine Beratung →",
    "es": "Contáctenos para una consulta →",
    "it": "Contattaci per una consulenza →",
    "fr": "Contactez-nous pour une consultation →",
    "pt": "Contacte-nos para uma consulta →",
    "nl": "Neem contact op voor een consult →",
    "pl": "Skontaktuj się w sprawie konsultacji →",
    "ro": "Contactați-ne pentru o consultație →",
    "tr": "Görüşme için bize ulaşın →",
}

# Softer comments for legit / uncertain (not accusing the firm of fraud)
SOFT = {
    "en": [
        (
            "Need help verifying this is the real company",
            "I saw mixed public reviews and want to make sure I am dealing with the genuine firm, not a lookalike. Who should I contact for a confidential check of my paperwork?",
        ),
        (
            "Unsure how to escalate a complaint",
            "I still have statements and chat logs. I’m not sure whether this belongs with the firm’s complaints team, a regulator, or counsel. Can someone advise the next step?",
        ),
    ],
    "de": [
        (
            "Hilfe bei der Prüfung der echten Firma",
            "Ich sehe gemischte Bewertungen und möchte sichergehen, dass ich mit dem echten Unternehmen spreche — nicht mit einer Imitation. Wen kann ich für eine vertrauliche Prüfung kontaktieren?",
        ),
    ],
    "es": [
        (
            "Necesito verificar si es la empresa real",
            "Vi reseñas mixtas y quiero confirmar que trato con la firma genuina, no con un clon. ¿A quién debo contactar para una revisión confidencial?",
        ),
    ],
    "it": [
        (
            "Serve verifica che sia la società vera",
            "Ho letto recensioni miste e voglio assicurarmi di parlare con la società reale, non con un clone. Chi posso contattare per un controllo confidenziale?",
        ),
    ],
    "fr": [
        (
            "Besoin de vérifier que c’est la vraie société",
            "J’ai vu des avis mitigés et je veux m’assurer de traiter avec la vraie société, pas une imitation. Qui contacter pour une vérification confidentielle ?",
        ),
    ],
    "pt": [
        (
            "Preciso confirmar se é a empresa real",
            "Vi avaliações mistas e quero garantir que trato com a empresa genuína, não com um clone. A quem posso pedir uma verificação confidencial?",
        ),
    ],
    "nl": [
        (
            "Hulp bij controleren of dit het echte bedrijf is",
            "Ik zie gemengde reviews en wil zeker weten dat ik met het echte bedrijf te maken heb, niet met een lookalike. Wie kan ik vertrouwelijk om advies vragen?",
        ),
    ],
    "pl": [
        (
            "Potrzebuję potwierdzenia, że to prawdziwa firma",
            "Widzę mieszane opinie i chcę mieć pewność, że mam do czynienia z prawdziwą firmą, a nie z klonem. Do kogo mogę się zwrócić o poufną weryfikację?",
        ),
    ],
    "ro": [
        (
            "Am nevoie să verific dacă e firma reală",
            "Am văzut recenzii mixte și vreau să fiu sigur că vorbesc cu firma reală, nu cu un clon. Pe cine pot contacta pentru o verificare confidențială?",
        ),
    ],
    "tr": [
        (
            "Gerçek şirket mi diye kontrol etmem lazım",
            "Karışık yorumlar gördüm; bakalike değil gerçek firma ile mi muhatap olduğumu doğrulamak istiyorum. Gizli bir kontrol için kime başvurmalıyım?",
        ),
    ],
}

SOFT_SUPPORT = {
    "en": "Happy to help you sort real-platform issues from lookalikes. Contact us with the domain you used, any licence number shown, and your timeline for a confidential consultation.",
    "de": "Gern helfen wir, echte Plattform und Imitate zu trennen. Kontaktieren Sie uns mit der genutzten Domain, einer angegebenen Lizenznummer und Ihrem Zeitablauf für eine vertrauliche Beratung.",
    "es": "Con gusto le ayudamos a distinguir la plataforma real de imitaciones. Contáctenos con el dominio usado, cualquier número de licencia y su cronograma para una consulta confidencial.",
    "it": "Siamo lieti di aiutarla a distinguere la piattaforma reale dalle imitazioni. Contattaci con il dominio usato, eventuali numeri di licenza e la tempistica per una consulenza confidenziale.",
    "fr": "Nous pouvons vous aider à distinguer la vraie plateforme d’une imitation. Contactez-nous avec le domaine utilisé, tout numéro de licence et votre calendrier pour une consultation confidentielle.",
    "pt": "Podemos ajudar a distinguir a plataforma real de imitações. Contacte-nos com o domínio usado, qualquer número de licença e o cronograma para uma consulta confidencial.",
    "nl": "Wij helpen graag echt van lookalike te scheiden. Neem contact op met het gebruikte domein, eventueel licentienummer en uw tijdlijn voor een vertrouwelijk consult.",
    "pl": "Chętnie pomożemy odróżnić prawdziwą platformę od imitacji. Prosimy o kontakt z użytą domeną, ewentualnym numerem licencji i harmonogramem — konsultacja poufna.",
    "ro": "Vă putem ajuta să deosebiți platforma reală de imitații. Contactați-ne cu domeniul folosit, orice număr de licență și calendarul — consultație confidențială.",
    "tr": "Gerçek platform ile taklitleri ayırmanıza yardımcı oluruz. Kullandığınız alan adı, varsa lisans numarası ve zaman çizelgenizle bize ulaşın — gizlilik içinde danışma.",
}


def stable_int(s: str, mod: int) -> int:
    return int(hashlib.sha256(s.encode("utf-8")).hexdigest()[:8], 16) % mod


def load_js_array(path: Path, assign: str):
    text = path.read_text(encoding="utf-8")
    m = re.search(rf"{re.escape(assign)}\s*=\s*(\{{.*\}}|\[.*\])\s*;?\s*$", text, re.S)
    if not m:
        raise SystemExit(f"Could not parse {path}")
    return json.loads(m.group(1))


def is_important_loss(c: dict) -> bool:
    if c.get("importantLoss"):
        return True
    text = (c.get("text") or "") + " " + (c.get("title") or "")
    # Material-loss signals (amounts / Super / retirement) — reply only these
    markers = (
        "$", "€", "£", "USD", "EUR", "GBP", "Super", "retirement", "erhebliche",
        "substantial", "significant", "importante", "élevée", "aanzienlijk",
        "znaczącą", "önemli", "250,000", "100,000", "50,000",
    )
    return any(m in text for m in markers)


def sanitize_override(items: list) -> list:
    """Drop source labels from UI data; keep Support only on important losses."""
    out = []
    replied = False
    for c in items:
        if (c.get("name") or "").lower().startswith("trustpilot"):
            continue
        if "trustpilot" in (c.get("title") or "").lower():
            continue
        if "trustpilot" in (c.get("text") or "").lower() and not c.get("askHelp"):
            continue
        row = dict(c)
        row.pop("source", None)  # never surface origin on the page
        if is_important_loss(row) and not replied and row.get("askHelp"):
            replied = True
            row["importantLoss"] = True
            # keep existing support or attach default EN if missing
            if not row.get("support"):
                lang = row.get("lang") or "en"
                reply_d = row.get("date") or date.today().isoformat()
                try:
                    d0 = date.fromisoformat(reply_d)
                    rd = min(d0 + timedelta(days=2), date.today())
                except ValueError:
                    rd = date.today()
                row["support"] = {
                    "date": rd.isoformat(),
                    "text": SUPPORT.get(lang, SUPPORT["en"]),
                    "ctaLabel": CTA.get(lang, CTA["en"]),
                    "ctaHref": "../index.html#contact",
                }
        else:
            row.pop("support", None)
        out.append(row)
    return out


def load_overrides() -> dict:
    """Keep hand-curated victim threads (real review text), sanitized for frontend."""
    if not COMMENTS_JS.exists():
        return {}
    db = load_js_array(COMMENTS_JS, "window.SBL_COMMENTS")
    keep = {}
    for slug, items in db.items():
        curated = any(
            c.get("askHelp") and is_important_loss(c) and c.get("name") not in ("Trustpilot record",)
            for c in items
        )
        if slug == "next-forrest-review" or curated:
            keep[slug] = sanitize_override(items)
    return keep


def pick_lang(country: str, slug: str, index: int) -> str:
    if index == 0 and slug in SLUG_LANG_HINTS:
        return SLUG_LANG_HINTS[slug]
    return COUNTRY_LANG.get(country, "en")


def build_for_broker(b: dict, today: date) -> list[dict]:
    slug = b["slug"]
    tier = (b.get("tier") or "scam").lower()
    soft = tier in ("legit", "clone") or (b.get("risk") == "medium" and tier != "scam")
    big_scam = (not soft) and (b.get("risk") == "high" or tier == "scam")
    bodies = SOFT if soft else HELP
    support_map = SOFT_SUPPORT if soft else SUPPORT
    comments: list[dict] = []

    # Do NOT publish rating-platform snapshots on the frontend.
    # Research sources stay in brokers.js (trustpilot field) for editors only.

    if soft:
        n_help = 1
    elif big_scam:
        n_help = 4  # more voices on large / clear scam files
    else:
        n_help = 2

    base_ago = 18 + stable_int(slug + ":base", 40)
    country_pool = [
        "Germany", "Spain", "Italy", "France", "Brazil", "Netherlands",
        "Poland", "Romania", "Turkey", "United Kingdom", "Singapore",
        "United Arab Emirates", "Australia", "Canada", "Japan",
        "South Africa", "Mexico", "Portugal", "Chile", "Colombia",
    ]
    for i in range(n_help):
        country = country_pool[(stable_int(slug + ":c" + str(i), len(country_pool)) + i * 5) % len(country_pool)]
        lang = pick_lang(country, slug, i)
        important = (not soft) and i == 0  # one important-loss reply per scam file
        if important:
            title, text = IMPORTANT.get(lang) or IMPORTANT["en"]
        else:
            pack = bodies.get(lang) or bodies["en"]
            title, text = pack[stable_int(slug + str(i), len(pack)) % len(pack)]
        name, initials = NAMES[(stable_int(slug + ":n" + str(i), len(NAMES)) + i) % len(NAMES)]
        gap = 11 + stable_int(slug + ":g" + str(i), 37)
        d = today - timedelta(days=base_ago + i * gap)
        if d > today:
            d = today - timedelta(days=3 + i)
        item = {
            "name": name,
            "initials": initials,
            "country": country,
            "date": d.isoformat(),
            "title": title,
            "text": text,
            "lang": lang,
            "askHelp": True,
            "importantLoss": important,
        }
        # Support replies only on important losses — never every comment
        if important:
            reply_delay = 1 + stable_int(slug + ":r" + str(i), 3)
            rd = min(d + timedelta(days=reply_delay), today)
            item["support"] = {
                "date": rd.isoformat(),
                "text": support_map.get(lang, support_map["en"])
                if soft
                else SUPPORT.get(lang, SUPPORT["en"]),
                "ctaLabel": CTA.get(lang, CTA["en"]),
                "ctaHref": "../index.html#contact",
            }
        comments.append(item)

    comments.sort(key=lambda c: c["date"], reverse=True)
    return comments


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser(description="Rebuild SBL_COMMENTS")
    ap.add_argument(
        "--new-only",
        action="store_true",
        help="Keep existing comment threads; only generate for slugs that are missing",
    )
    ap.add_argument(
        "--force",
        action="store_true",
        help="Regenerate all non-override slugs (ignores --new-only)",
    )
    args = ap.parse_args()

    today = date.today()
    brokers = load_js_array(BROKERS_JS, "window.SBL_BROKERS")
    existing: dict[str, list] = {}
    if COMMENTS_JS.exists():
        try:
            existing = load_js_array(COMMENTS_JS, "window.SBL_COMMENTS")
        except SystemExit:
            existing = {}
    overrides = load_overrides()
    out: dict[str, list] = {}
    generated = 0
    kept = 0
    for b in brokers:
        slug = b["slug"]
        if slug in overrides:
            out[slug] = overrides[slug]
            kept += 1
            continue
        if args.new_only and not args.force and slug in existing and existing[slug]:
            out[slug] = existing[slug]
            kept += 1
            continue
        out[slug] = build_for_broker(b, today)
        generated += 1

    text = (
        "/* Auto-generated by tools/rebuild_comments.py — multilingual help + Support; overrides preserved */\n"
        "window.SBL_COMMENTS = "
        + json.dumps(out, ensure_ascii=False, indent=2)
        + ";\n"
    )
    COMMENTS_JS.write_text(text, encoding="utf-8")
    langs = {}
    for items in out.values():
        for c in items:
            if c.get("askHelp"):
                langs[c.get("lang", "en")] = langs.get(c.get("lang", "en"), 0) + 1
    print(f"Wrote comments for {len(out)} slugs → {COMMENTS_JS}")
    print(f"generated={generated} kept={kept} overrides={len(overrides)}")
    print(f"Help comment langs: {langs}")


if __name__ == "__main__":
    main()
