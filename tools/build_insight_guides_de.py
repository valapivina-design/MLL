#!/usr/bin/env python3
"""Build German keyword-slug insight guides under /de/insights/.

German victim-intent funnel: primary keyword in URL ("anlagebetrug geld
zurück", "anlagebetrug anwalt", ...), commercial FAQs, CTA to consultation.

  python3 tools/build_insight_guides_de.py
"""
from __future__ import annotations

import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "de" / "insights"
SITE = "https://mikelevylaw.com"
UPDATED = "17. November 2026"
DATE_ISO = "2026-11-17"

GUIDES = [
    {
        "slug": "anlagebetrug-geld-zurueck",
        "kicker": f"Anlagebetrug · Aktualisiert {UPDATED}",
        "h1": "Anlagebetrug: Geld zurück — realistische Wege nach einem Anlagebetrug",
        "title": "Anlagebetrug Geld zurück: Optionen & nächste Schritte | Mike Levy Law",
        "desc": "Anlagebetrug Geld zurück: Chargeback, Überweisungsrückruf, Krypto-Tracing und anwaltliche Prüfung — was nach einem Anlagebetrug realistisch hilft.",
        "keywords": "anlagebetrug geld zurück, geld zurück nach anlagebetrug, anlagebetrug geld zurückholen, anlagebetrug rückbuchung, anlagebetrug schadensersatz",
        "lead": "Anlagebetrug Geld zurück — dafür gibt es kein Patentrezept, aber eine sinnvolle Reihenfolge: Zahlungsweg prüfen, Fristen sichern, Beweise sammeln, dann Bank-, Karten-, Krypto- oder zivilrechtliche Wege prüfen. Zeit ist der teuerste Faktor.",
        "sections": [
            (
                "Welche Zahlungswege Chancen eröffnen",
                "<p><strong>Kredit-/Debitkarte:</strong> Chargeback ist oft das schnellste Werkzeug — innerhalb kurzer Fristen und mit sauberer Beweismappe. <strong>Überweisung:</strong> Ein Rückruf (Recall) bei der eigenen Bank ist noch am selben oder nächsten Werktag am ehesten erfolgversprechend. <strong>Krypto:</strong> Kein Rückbuchungsrecht, aber Transaktionen sind nachverfolgbar — Tracing kann Empfängerbörsen identifizieren, an die sich Strafanzeige oder zivilrechtliche Schritte richten.</p>",
            ),
            (
                "Was Sie in den ersten 14 Tagen tun sollten",
                "<ol>"
                "<li>Keine weiteren Zahlungen — auch keine „Steuer“, „Freigabegebühr“ oder „Provision“.</li>"
                "<li>Chats, E-Mails, Kontoauszüge und die exakte Domain/App sichern.</li>"
                "<li>Bei Karte: Chargeback-Antrag bei der kartenausgebenden Bank stellen.</li>"
                "<li>Bei Überweisung: Rückruf und Fraud-Eskalation bei Ihrer Bank anfordern.</li>"
                "<li>Strafanzeige erstatten (Polizei / LKA / Online-Wache des Bundeslands).</li>"
                "<li>Bei erheblichem Verlust: vertrauliche anwaltliche Prüfung anfordern.</li>"
                "</ol>",
            ),
            (
                "Was Anwälte realistisch beisteuern",
                "<p>Wir gleichen Ihre Unterlagen mit dem öffentlichen Befund ab (Warnlisten, Klone, Zahlungsempfänger), prüfen zivilrechtliche Ansprüche und die Frage, wer überhaupt verklagt werden kann — und sagen offen, wenn ein Vorgehen wirtschaftlich nicht sinnvoll ist. Es gibt keine Garantie auf Wiedererlangung.</p>",
            ),
        ],
        "faqs": [
            (
                "Kann ich mein Geld nach Anlagebetrug zurückbekommen?",
                "Manchmal — abhängig vom Zahlungsweg, der Zeit seit der Zahlung und den Beweisen. Karten-Chargeback und schnelle Überweisungsrückrufe haben die besten kurzfristigen Chancen; danach bleiben Meldungen, Tracing und zivilrechtliche Wege. Garantiert ist nichts.",
            ),
            (
                "Was tun, wenn der Broker eine Gebühr vor der Auszahlung verlangt?",
                "Nicht zahlen. Seriöse Anbieter verrechnen Gebühren mit dem Guthaben — sie verlangen keine neue Überweisung als „Freigabe“. Das ist ein klassisches Vorschussbetrugs-Muster.",
            ),
            (
                "Lohnt sich ein Anwalt bei Anlagebetrug?",
                "Bei erheblichen Beträgen meist ja: Ein Anwalt strukturiert Beweise, prüft die richtige Gegenpartei (Original vs. Klon) und koordiniert Bank, Strafanzeige und gegebenenfalls Klage — statt Fristen verstreichen zu lassen.",
            ),
        ],
        "related": [
            ("../anlagebetrug-anwalt/", "Anlagebetrug Anwalt"),
            ("../anlagebetrug-was-tun/", "Anlagebetrug: was tun?"),
            ("../anlagebetrug-melden/", "Anlagebetrug melden / anzeigen"),
        ],
        "source": "insights-de-anlagebetrug-geld-zurueck",
    },
    {
        "slug": "anlagebetrug-anwalt",
        "kicker": f"Anwalt · Aktualisiert {UPDATED}",
        "h1": "Anlagebetrug Anwalt: Wann sich rechtliche Hilfe lohnt — und was sie kostet",
        "title": "Anlagebetrug Anwalt: Prüfung & Vorgehen | Mike Levy Law",
        "desc": "Anlagebetrug Anwalt: Wann sich ein Anwalt lohnt, was eine vertrauliche Prüfung leistet, und welche Wege (Bank, Anzeige, Klage) realistisch sind.",
        "keywords": "anlagebetrug anwalt, anwalt anlagebetrug, anwalt für anlagebetrug, anlagebetrug anwalt erfahrungen, anlagebetrug rechtsanwalt",
        "lead": "Nach Anlagebetrug suchen viele direkt einen Anwalt — richtig so. Entscheidend ist, dass die Prüfung mit Ihren Dokumenten beginnt, nicht mit Versprechen. Wir prüfen vertraulich, welche Wege (Bank, Karte, Krypto, Anzeige, Klage) in Ihrem Fall tragen.",
        "sections": [
            (
                "Was eine seriöse Ersteinschätzung enthält",
                "<ul>"
                "<li>Zahlungsweg und Datum jeder Zahlung (Karte, Überweisung, Krypto)</li>"
                "<li>Exakte Domain/App und Zahlungsempfänger — Original oder Klon?</li>"
                "<li>Öffentlicher Befund: Warnlisten (BaFin, FMA, FINMA, IOSCO), Klone, laufende Verfahren</li>"
                "<li>Fristen: Chargeback, Rückruf, Verjährung grob eingeordnet</li>"
                "<li>Realistische Einschätzung statt Erfolgsgarantie</li>"
                "</ul>",
            ),
            (
                "Woran Sie unseriöse „Hilfe“ erkennen",
                "<p>Vorsicht bei kalt akquirierenden „Recovery-Diensten“, die eine Vorauszahlung in Krypto verlangen, Erfolg garantieren oder behaupten, Ihr Geld „liege schon bereit“. Das ist häufig der zweite Betrug. Seriöse Anwälte verlangen keine „Freigabegebühr“, um Geld zu „entsperren“.</p>",
            ),
            (
                "Typische Bausteine eines Mandats",
                "<ol>"
                "<li>Beweissicherung und Chronologie</li>"
                "<li>Bank-/Karten-Dispute-Begleitung</li>"
                "<li>Strafanzeige mit verwertbarer Sachverhaltsdarstellung</li>"
                "<li>Prüfung zivilrechtlicher Ansprüche und der richtigen Beklagten</li>"
                "<li>Bei Krypto: Tracing-Optionen gegenüber Börsen/Dienstleistern</li>"
                "</ol>",
            ),
        ],
        "faqs": [
            (
                "Brauche ich bei Anlagebetrug einen Anwalt?",
                "Bei kleineren Beträgen reichen oft Bank-Dispute und Strafanzeige. Bei fünfstelligen Verlusten, komplexen Zahlungsketten oder Krypto ist anwaltliche Struktur meist sinnvoll — insbesondere, um Fristen und die richtige Gegenpartei nicht zu verfehlen.",
            ),
            (
                "Was kostet ein Anwalt für Anlagebetrug?",
                "Das hängt von Umfang und Gegenstandswert ab. Eine vertrauliche Ersteinschätzung klärt zuerst, ob sich weitere Schritte wirtschaftlich lohnen — bevor größere Kosten entstehen.",
            ),
            (
                "Kann ein Anwalt die Rückzahlung garantieren?",
                "Nein. Niemand kann das seriös. Ein Anwalt erhöht die Qualität und Reihenfolge der Schritte — Garantien sind ein Warnsignal.",
            ),
        ],
        "related": [
            ("../anlagebetrug-geld-zurueck/", "Anlagebetrug: Geld zurück"),
            ("../krypto-betrug-anwalt/", "Krypto-Betrug Anwalt"),
            ("../anlagebetrug-erkennen/", "Anlagebetrug erkennen"),
        ],
        "source": "insights-de-anlagebetrug-anwalt",
    },
    {
        "slug": "krypto-betrug-geld-zurueck",
        "kicker": f"Krypto-Betrug · Aktualisiert {UPDATED}",
        "h1": "Krypto-Betrug: Geld zurück — Chancen nach einem Krypto-Investmentbetrug",
        "title": "Krypto Betrug Geld zurück: Chancen & Wege | Mike Levy Law",
        "desc": "Krypto Betrug Geld zurück: Was nach einem Krypto-Betrug realistisch ist — Tracing, Börsen-Meldung, Anzeige und anwaltliche Prüfung der Chancen.",
        "keywords": "krypto betrug geld zurück, krypto betrug chancen geld zurück, krypto betrug geld zurückholen, bitcoin betrug geld zurück, krypto scam geld zurück",
        "lead": "Bei Krypto-Betrug gibt es keine Rückbuchung — aber die Blockchain ist öffentlich. Ob Geld zurückfließt, hängt davon ab, wohin die Coins liefen und ob eine regulierte Börse oder ein identifizierbarer Dienstleister im Pfad liegt.",
        "sections": [
            (
                "Warum Tracing der Ausgangspunkt ist",
                "<p>Jede Transaktion ist nachvollziehbar. Ziel ist, Auszahlungspunkte zu finden: Börsen mit KYC, Zahlungsdienstleister, Mixer-Grenzfälle. An diese Stellen können Strafverfolgung und zivilrechtliche Anfragen anknüpfen. Tracing ersetzt keine Anzeige — es macht sie verwertbarer.</p>",
            ),
            (
                "Sofort-Schritte nach einem Krypto-Betrug",
                "<ol>"
                "<li>Transaktions-Hashes, Wallet-Adressen und Plattform-Domain sichern.</li>"
                "<li>Keine „Steuer“ oder „Gas-Fee“ zur Auszahlung mehr zahlen.</li>"
                "<li>Falls auch Karte/Überweisung im Spiel war: <a href=\"../anlagebetrug-geld-zurueck/\">Chargeback/Rückruf</a> prüfen.</li>"
                "<li>Strafanzeige mit Hashes und Adressen erstatten.</li>"
                "<li>Bei erheblichem Verlust: vertrauliche Prüfung (Tracing, zivilrechtliche Optionen).</li>"
                "</ol>",
            ),
            (
                "Realistische Erwartungen",
                "<p>Volle Wiedererlangung ist die Ausnahme, nicht die Regel. Teilerfolge entstehen dort, wo Coins regulierte Börsen berühren oder Verantwortliche identifizierbar werden. Wer Garantien verspricht, ist selbst ein Risiko.</p>",
            ),
        ],
        "faqs": [
            (
                "Kann man bei Krypto-Betrug Geld zurückbekommen?",
                "Es gibt keine Rückbuchung wie bei Karte. Chancen entstehen über Tracing bis zu regulierten Börsen, Strafverfolgung und — wo möglich — zivilrechtliche Ansprüche. Die Chancen hängen stark vom Einzelfall ab.",
            ),
            (
                "Die Plattform verlangt eine Gebühr für die Auszahlung — zahlen?",
                "Nein. „Steuer“, „Mining-Fee“ oder „Freigabe“ vor der Auszahlung ist ein Vorschussbetrugs-Muster. Zahlen Sie nichts weiter.",
            ),
            (
                "Lohnt sich eine Anzeige bei Krypto-Betrug?",
                "Ja — sie ist Voraussetzung dafür, dass Ermittler Börsen und Dienstleister anschreiben können. Mit Hashes und Adressen wird die Anzeige deutlich verwertbarer.",
            ),
        ],
        "related": [
            ("../krypto-betrug-anwalt/", "Krypto-Betrug Anwalt"),
            ("../bitcoin-geld-zurueckholen/", "Bitcoin zurückholen"),
            ("../anlagebetrug-melden/", "Betrug melden / anzeigen"),
        ],
        "source": "insights-de-krypto-betrug-geld-zurueck",
    },
    {
        "slug": "krypto-betrug-anwalt",
        "kicker": f"Anwalt · Aktualisiert {UPDATED}",
        "h1": "Krypto-Betrug Anwalt: Prüfung, Tracing und Durchsetzung nach Krypto-Betrug",
        "title": "Krypto Betrug Anwalt: Prüfung & Tracing | Mike Levy Law",
        "desc": "Krypto Betrug Anwalt: vertrauliche Prüfung, Blockchain-Tracing, Anzeige und zivilrechtliche Optionen nach einem Krypto-Scam — ohne Erfolgsversprechen.",
        "keywords": "krypto betrug anwalt, krypto anwalt, anwalt krypto betrug, krypto anwalt münchen, krypto anwalt berlin, krypto anwalt köln, krypto anwalt in der nähe, bitcoin betrugsfälle anwalt",
        "lead": "Ein Anwalt für Krypto-Betrug verbindet drei Dinge: Beweisstruktur, Blockchain-Tracing und die richtige Adresse für Anzeige oder Klage. Gerade bei Krypto verschenken Betroffene oft Monate mit Tickets bei der Scam-Plattform — während Börsen-Daten veralten.",
        "sections": [
            (
                "Was der Anwalt konkret prüft",
                "<ul>"
                "<li>Wallet-Pfade: von Ihrer Einzahlung bis zu Auszahlungspunkten</li>"
                "<li>Berührungspunkte mit KYC-Börsen und Zahlungsdienstleistern</li>"
                "<li>Plattform-Hintergrund: Warnlisten, Klone, verantwortliche Entitäten</li>"
                "<li>Fiat-Anteile: Karten- oder Überweisungsbeine mit eigenen Fristen</li>"
                "</ul>",
            ),
            (
                "Standort spielt eine Rolle — aber nicht die Hauptrolle",
                "<p>Viele suchen „Krypto Anwalt München / Berlin / Köln / in der Nähe“. Für den Fall zählt weniger die Kanzleiadresse als die Frage, wo Schädiger, Börsen und Gerichtsstände liegen. Eine Mandatierung ist standortübergreifend möglich; wichtig ist, dass die Prüfung Ihren Zahlungspfad korrekt abbildet.</p>",
            ),
            (
                "Abgrenzung zu Recovery-Scams",
                "<p>„Wir holen Ihre Bitcoin zurück — Vorkasse in USDT“ ist kein Angebot, sondern der zweite Betrug. Anwaltliche Arbeit beginnt mit Prüfung und Ehrlichkeit über Erfolgsaussichten — nie mit einer „Freigabegebühr“.</p>",
            ),
        ],
        "faqs": [
            (
                "Was kann ein Krypto-Anwalt erreichen?",
                "Struktur und Hebel: verwertbare Anzeige, Tracing bis zu regulierten Stellen, gegebenenfalls zivilrechtliche Ansprüche gegen identifizierbare Parteien. Eine Rückzahlungsgarantie gibt es nicht.",
            ),
            (
                "Muss der Anwalt in meiner Stadt sein?",
                "Nein. Entscheidend sind Erfahrung mit Krypto-Fällen und die Fähigkeit, Börsen und Gerichtsstände international einzuordnen.",
            ),
            (
                "Wann lohnt sich der Anwalt bei Krypto-Betrug?",
                "Bei erheblichen Beträgen, gemischten Zahlungswegen (Fiat + Krypto) oder wenn Börsen involviert sind, die auf formale Anfragen reagieren.",
            ),
        ],
        "related": [
            ("../krypto-betrug-geld-zurueck/", "Krypto-Betrug: Geld zurück"),
            ("../anlagebetrug-anwalt/", "Anlagebetrug Anwalt"),
            ("../anlagebetrug-melden/", "Betrug melden / anzeigen"),
        ],
        "source": "insights-de-krypto-betrug-anwalt",
    },
    {
        "slug": "bitcoin-geld-zurueckholen",
        "kicker": f"Bitcoin · Aktualisiert {UPDATED}",
        "h1": "Bitcoin zurückholen: Was nach einem Bitcoin-Betrug wirklich möglich ist",
        "title": "Bitcoin Geld zurückholen: Realistische Wege | Mike Levy Law",
        "desc": "Bitcoin Geld zurückholen: Transaktionen sind final — aber nicht unsichtbar. Tracing, Börsen-Meldung und Anzeige als realistische Wege.",
        "keywords": "bitcoin geld zurückholen, bitcoin zurückholen, btc betrug geld zurück, bitcoin transaktion rückgängig, bitcoin scam geld zurück",
        "lead": "Bitcoin-Transaktionen sind technisch final — ein „Zurückbuchen“ gibt es nicht. Was es gibt: eine öffentliche Spur. Ob sie zu Geld führt, hängt davon ab, ob die Coins eine regulierte Börse oder einen identifizierbaren Dienstleister erreichen.",
        "sections": [
            (
                "Was nicht funktioniert",
                "<p>Kein Chargeback, kein „Support“ der Blockchain, kein technisches Zurückholen durch Dritte. Wer genau das gegen Gebühr anbietet, betreibt in der Regel Recovery-Betrug.</p>",
            ),
            (
                "Was funktionieren kann",
                "<ol>"
                "<li>Hashes und Empfängeradressen sichern.</li>"
                "<li>Tracing bis zu Börsen/Dienstleistern mit KYC.</li>"
                "<li>Strafanzeige mit verwertbarer Transaktionshistorie.</li>"
                "<li>Formale Anfragen an Börsen durch Ermittler/Anwalt.</li>"
                "<li>Fiat-Beine (Karte/Überweisung) separat prüfen — dort gelten eigene Fristen.</li>"
                "</ol>",
            ),
            (
                "Zeitfaktor",
                "<p>Börsen speichern Daten nicht ewig, und Coins werden weiter bewegt. Wochen zählen — nicht Monate.</p>",
            ),
        ],
        "faqs": [
            (
                "Kann man eine Bitcoin-Transaktion rückgängig machen?",
                "Nein. Final heißt final. Möglich ist nur, die Spur zu verfolgen und an regulierten Punkten anzusetzen (Börse, Dienstleister, Strafverfolgung).",
            ),
            (
                "Lohnt sich Tracing bei kleinen Beträgen?",
                "Meist nicht wirtschaftlich. Bei fünfstelligen Verlusten ist eine professionelle Einschätzung eher sinnvoll.",
            ),
            (
                "Was ist mit „Recovery Services“, die meine BTC zurückholen?",
                "Garantien plus Vorkasse in Krypto sind das Kernmuster des Recovery-Betrugs. Nicht zahlen.",
            ),
        ],
        "related": [
            ("../krypto-betrug-geld-zurueck/", "Krypto-Betrug: Geld zurück"),
            ("../krypto-betrug-anwalt/", "Krypto-Betrug Anwalt"),
            ("../anlagebetrug-was-tun/", "Anlagebetrug: was tun?"),
        ],
        "source": "insights-de-bitcoin-geld-zurueckholen",
    },
    {
        "slug": "trading-betrug-geld-zurueck",
        "kicker": f"Trading-Betrug · Aktualisiert {UPDATED}",
        "h1": "Trading-Betrug: Geld zurück — nach Fake-Brokern und Trading-Plattformen",
        "title": "Trading Betrug Geld zurück: Wege & Fristen | Mike Levy Law",
        "desc": "Trading Betrug Geld zurück: Auszahlung blockiert, „Steuer“ vor Payout, Support weg — Chargeback, Rückruf und anwaltliche Prüfung nach Trading-Betrug.",
        "keywords": "trading betrug geld zurück, trading plattform betrug geld zurück, broker betrug geld zurück, online trading betrug geld zurück, trading scam geld zurück",
        "lead": "Beim Trading-Betrug sieht das Konto gut aus — bis zur Auszahlung. Dann kommen „Steuern“, „Compliance“ oder Funkstille. Welche Wege offenstehen, entscheidet sich am Zahlungsweg und an der Geschwindigkeit Ihrer Reaktion.",
        "sections": [
            (
                "Das typische Muster",
                "<p>Kleine Testauszahlung klappt, große nicht. Neue Gebühren vor dem Payout. Der „Account Manager“ drängt zu weiteren Einzahlungen. Domain und Empfänger wechseln. All das ist Beweismaterial — sichern Sie es, bevor Accounts gelöscht werden.</p>",
            ),
            (
                "Reihenfolge der Gegenmaßnahmen",
                "<ol>"
                "<li>Keine weiteren Zahlungen, keine „Freigabegebühren“.</li>"
                "<li>Karte: Chargeback sofort beantragen.</li>"
                "<li>Überweisung: Rückruf bei der eigenen Bank anfordern.</li>"
                "<li>Krypto: Hashes sichern, Tracing-Optionen prüfen.</li>"
                "<li>Strafanzeige erstatten; Warnlisten (BaFin/FMA/FINMA) prüfen.</li>"
                "<li>Erheblicher Verlust: <a href=\"../anlagebetrug-anwalt/\">vertrauliche anwaltliche Prüfung</a>.</li>"
                "</ol>",
            ),
            (
                "Klon oder reguliertes Original?",
                "<p>Viele Trading-Scams kopieren Namen lizenzierter Firmen. Gegen wen Sie vorgehen müssen, hängt davon ab, wer Ihr Geld tatsächlich erhielt — die Rechnung und der Kontoauszug sind wichtiger als das Logo auf der Webseite.</p>",
            ),
        ],
        "faqs": [
            (
                "Wie bekomme ich Geld von einer betrügerischen Trading-Plattform zurück?",
                "Über den Zahlungsweg: Chargeback bei Karte, Rückruf bei Überweisung, Tracing bei Krypto — flankiert von Strafanzeige und, bei erheblichen Beträgen, anwaltlicher Prüfung.",
            ),
            (
                "Die Plattform verlangt 10 % „Steuer“ vor Auszahlung — normal?",
                "Nein. Das ist das bekannteste Vorschussbetrugs-Signal im Trading-Bereich. Zahlen Sie nichts weiter.",
            ),
            (
                "Ist mein Geld nach Monaten noch zu retten?",
                "Schwieriger, aber nicht automatisch hoffnungslos. Chargeback-Fristen sind dann meist vorbei; Anzeige, Tracing und zivilrechtliche Wege bleiben — mit realistischer Einschätzung.",
            ),
        ],
        "related": [
            ("../anlagebetrug-geld-zurueck/", "Anlagebetrug: Geld zurück"),
            ("../online-betrug-geld-zurueckfordern/", "Online-Betrug: Geld zurückfordern"),
            ("../anlagebetrug-melden/", "Betrug melden / anzeigen"),
        ],
        "source": "insights-de-trading-betrug-geld-zurueck",
    },
    {
        "slug": "anlagebetrug-was-tun",
        "kicker": f"Sofortmaßnahmen · Aktualisiert {UPDATED}",
        "h1": "Anlagebetrug: was tun? Die ersten 14 Tage entscheiden",
        "title": "Anlagebetrug was tun: Sofortmaßnahmen | Mike Levy Law",
        "desc": "Anlagebetrug was tun: Schritt-für-Schritt nach dem Verdacht — Zahlungen stoppen, Beweise sichern, Bank, Anzeige und anwaltliche Prüfung.",
        "keywords": "anlagebetrug was tun, was tun bei anlagebetrug, anlagebetrug sofortmaßnahmen, anlagebetrug erkannt was jetzt, investment betrug was tun",
        "lead": "Der Verdacht steht im Raum — Auszahlung blockiert, neue Gebühren, Druck vom „Berater“. Was Sie in den ersten 14 Tagen tun (und lassen), entscheidet, welche Optionen danach noch offen sind.",
        "sections": [
            (
                "Sofort stoppen",
                "<ul>"
                "<li>Keine weiteren Einzahlungen — auch keine „letzte Gebühr“.</li>"
                "<li>Kommunikation nicht löschen, sondern exportieren (Chat, Mail, Anrufprotokoll).</li>"
                "<li>Konto bei der Plattform nicht selbst schließen — Screenshots vorher.</li>"
                "</ul>",
            ),
            (
                "Beweismappe bauen",
                "<ol>"
                "<li>Domain/App, Registrierungsdatum, Ansprechpartner</li>"
                "<li>Alle Zahlungen: Datum, Betrag, Empfänger, Referenz</li>"
                "<li>Auszahlungsanfragen und Ablehnungen (Screenshots mit Datum)</li>"
                "<li>Werbeversprechen (Rendite, „Garantie“, Bonus)</li>"
                "</ol>",
            ),
            (
                "Parallel handeln",
                "<p>Bank und Kartenherausgeber kontaktieren (Dispute/Rückruf), <a href=\"../anlagebetrug-melden/\">Strafanzeige erstatten</a>, und bei erheblichem Verlust eine <a href=\"../anlagebetrug-anwalt/\">vertrauliche anwaltliche Prüfung</a> anfordern. Nicht serienmäßig warten, bis der „Support“ sich meldet — Fristen laufen.</p>",
            ),
        ],
        "faqs": [
            (
                "Was ist der allererste Schritt bei Anlagebetrug?",
                "Zahlungen stoppen und Beweise sichern — in dieser Reihenfolge. Jede weitere „Gebühr“ erhöht nur den Schaden.",
            ),
            (
                "Soll ich die Plattform konfrontieren?",
                "Kurz und schriftlich, ohne neue Zahlungen. Erwarten Sie keine Lösung — dokumentieren Sie die Antworten für Bank, Anzeige und Anwalt.",
            ),
            (
                "Wann zur Polizei, wann zum Anwalt?",
                "Anzeige immer — sie kostet nichts und schafft die Basis für Ermittlungen. Ein Anwalt lohnt sich bei erheblichen Beträgen oder komplexen Zahlungswegen zusätzlich.",
            ),
        ],
        "related": [
            ("../anlagebetrug-geld-zurueck/", "Anlagebetrug: Geld zurück"),
            ("../anlagebetrug-melden/", "Anlagebetrug melden / anzeigen"),
            ("../anlagebetrug-erkennen/", "Anlagebetrug erkennen"),
        ],
        "source": "insights-de-anlagebetrug-was-tun",
    },
    {
        "slug": "anlagebetrug-melden",
        "kicker": f"Melden & anzeigen · Aktualisiert {UPDATED}",
        "h1": "Anlagebetrug melden und anzeigen: wo, wie, mit welchen Unterlagen",
        "title": "Anlagebetrug melden / anzeigen: Stellen & Unterlagen | Mike Levy Law",
        "desc": "Anlagebetrug melden und anzeigen: Polizei, Online-Wache, BaFin — welche Stelle zuständig ist und welche Unterlagen die Anzeige verwertbar machen.",
        "keywords": "anlagebetrug melden, anlagebetrug anzeigen, anlagebetrug anzeige erstatten, krypto betrug melden, krypto betrug polizei melden, scam melden polizei, scam melden deutschland, anlagebetrug bafin melden",
        "lead": "Eine gute Anzeige ist mehr als „ich wurde betrogen“. Mit Zahlungsbelegen, Domain und Kommunikation wird aus dem Verdacht ein verwertbarer Vorgang — für Polizei, Staatsanwaltschaft und gegebenenfalls BaFin.",
        "sections": [
            (
                "Wo melden?",
                "<ul>"
                "<li><strong>Polizei / Online-Wache des Bundeslands:</strong> Strafanzeige — jederzeit, auch online.</li>"
                "<li><strong>Staatsanwaltschaft:</strong> direkt oder über die Polizei.</li>"
                "<li><strong>BaFin:</strong> Hinweis auf unerlaubte Finanz-/Anlagegeschäfte (kein Schadensersatz, aber Warnwirkung).</li>"
                "<li><strong>Verbraucherzentrale:</strong> Dokumentation und Musterfälle.</li>"
                "<li><strong>Bank/Kartenherausgeber:</strong> parallel — eigene Fristen für Dispute/Rückruf.</li>"
                "</ul>",
            ),
            (
                "Unterlagen, die zählen",
                "<ol>"
                "<li>Zahlungsnachweise mit Empfänger, IBAN/Wallet, Referenz</li>"
                "<li>Exakte Domain/App und Zeitpunkt der Registrierung</li>"
                "<li>Chats/E-Mails: Renditeversprechen, Auszahlungsverweigerung, Gebührenforderungen</li>"
                "<li>Chronologie auf einer Seite</li>"
                "</ol>",
            ),
            (
                "Was eine Anzeige bewirkt — und was nicht",
                "<p>Die Anzeige ermöglicht Ermittlungen und Anfragen an Banken/Börsen. Sie erstattet Ihr Geld nicht direkt zurück — Rückflüsse laufen über Bankwege, Pfändung oder zivilrechtliche Schritte. Beides zusammen ergibt das sinnvolle Paket.</p>",
            ),
        ],
        "faqs": [
            (
                "Wo kann ich Anlagebetrug anzeigen?",
                "Bei jeder Polizeidienststelle oder der Online-Wache Ihres Bundeslands. Zusätzlich lohnt ein Hinweis an die BaFin, wenn unerlaubte Anlagegeschäfte im Raum stehen.",
            ),
            (
                "Kann ich Krypto-Betrug bei der Polizei melden?",
                "Ja. Bringen Sie Transaktions-Hashes, Wallet-Adressen und die Plattform-Domain mit — das macht die Anzeige für Ermittler verwertbar.",
            ),
            (
                "Bringt die BaFin-Meldung mein Geld zurück?",
                "Nein — die BaFin warnt und untersagt, erstattet aber keinen Schadensersatz. Für Rückflüsse sind Bank-Dispute, Rückruf und gegebenenfalls zivilrechtliche Schritte zuständig.",
            ),
        ],
        "related": [
            ("../anlagebetrug-was-tun/", "Anlagebetrug: was tun?"),
            ("../anlagebetrug-geld-zurueck/", "Anlagebetrug: Geld zurück"),
            ("../krypto-betrug-geld-zurueck/", "Krypto-Betrug: Geld zurück"),
        ],
        "source": "insights-de-anlagebetrug-melden",
    },
    {
        "slug": "online-betrug-geld-zurueckfordern",
        "kicker": f"Online-Betrug · Aktualisiert {UPDATED}",
        "h1": "Online-Betrug: Geld zurückfordern — die Wege nach Zahlungsart",
        "title": "Online Betrug Geld zurückfordern: Wege nach Zahlungsart | Mike Levy Law",
        "desc": "Online Betrug Geld zurückfordern: Chargeback, Überweisungsrückruf, Krypto-Tracing und Anzeige — welcher Weg zu Ihrer Zahlungsart passt.",
        "keywords": "online betrug geld zurück, online betrug geld zurückfordern, internet betrug geld zurück, online scam geld zurück, geld zurückfordern betrug",
        "lead": "„Online betrogen — Geld zurück?“ Die Antwort hängt fast vollständig davon ab, <strong>wie</strong> Sie gezahlt haben. Karte, Überweisung und Krypto folgen völlig verschiedenen Regeln und Fristen.",
        "sections": [
            (
                "Karte (Kredit/Debit): Chargeback",
                "<p>Der stärkste kurzfristige Hebel. Beantragen Sie den Dispute bei der kartenausgebenden Bank — mit Domain, Screenshots und Auszahlungsverweigerung. Fristen sind kurz; „erst mal abwarten“ ist die teuerste Strategie.</p>",
            ),
            (
                "Überweisung: Rückruf und Bank-Eskalation",
                "<p>Fordern Sie bei Ihrer Bank einen Rückruf (Recall) und eine Fraud-Eskalation an — idealerweise am selben oder nächsten Werktag. Ist das Geld beim Empfänger abgehoben, bleiben Anzeige und zivilrechtliche Wege.</p>",
            ),
            (
                "Krypto: Tracing statt Rückbuchung",
                "<p>Keine Rückbuchung — dafür eine öffentliche Spur. Hashes sichern, Tracing bis zu KYC-Börsen, Anzeige mit verwertbarer Historie. Details: <a href=\"../krypto-betrug-geld-zurueck/\">Krypto-Betrug: Geld zurück</a>.</p>",
            ),
        ],
        "faqs": [
            (
                "Kann ich Geld aus einem Online-Betrug zurückfordern?",
                "Ja — über den passenden Zahlungsweg und die zuständigen Stellen. Ob etwas zurückfließt, hängt von Frist, Beweisen und der Erreichbarkeit der Gegenseite ab. Garantien gibt es nicht.",
            ),
            (
                "Was ist schneller: Anzeige oder Chargeback?",
                "Beides parallel. Der Chargeback hat harte Fristen; die Anzeige schafft die Ermittlungsgrundlage. Keines ersetzt das andere.",
            ),
            (
                "Lohnt sich ein Anwalt bei Online-Betrug?",
                "Bei erheblichen Beträgen oder gemischten Zahlungswegen meist ja — die <a href=\"../anlagebetrug-anwalt/\">vertrauliche Prüfung</a> klärt das wirtschaftlich Sinnvolle, bevor Kosten entstehen.",
            ),
        ],
        "related": [
            ("../anlagebetrug-geld-zurueck/", "Anlagebetrug: Geld zurück"),
            ("../trading-betrug-geld-zurueck/", "Trading-Betrug: Geld zurück"),
            ("../anlagebetrug-melden/", "Betrug melden / anzeigen"),
        ],
        "source": "insights-de-online-betrug-geld-zurueckfordern",
    },
    {
        "slug": "anlagebetrug-erkennen",
        "kicker": f"Prävention · Aktualisiert {UPDATED}",
        "h1": "Anlagebetrug erkennen: die Muster, bevor Sie zahlen",
        "title": "Anlagebetrug erkennen: Warnsignale & Muster | Mike Levy Law",
        "desc": "Anlagebetrug erkennen: Rendite-„Garantien“, Gebühren vor Auszahlung, Klon-Firmen, Zeitdruck — die Muster, mit denen Anlagebetrug arbeitet.",
        "keywords": "anlagebetrug erkennen, krypto betrug erkennen, trading betrug erkennen, anlagebetrug warnsignale, investment scam erkennen, fake broker erkennen",
        "lead": "Anlagebetrug ist selten clever getarnt — er ist konsequent. Dieselben fünf Muster tauchen in fast jedem Fall auf. Wer sie vor der ersten Zahlung erkennt, spart sich den zweiten Abschnitt dieses Weges: das Zurückholen.",
        "sections": [
            (
                "Die fünf Kernmuster",
                "<ul>"
                "<li><strong>Rendite-„Garantie“:</strong> feste Prozente pro Woche/Monat, „risikofrei“.</li>"
                "<li><strong>Gebühr vor Auszahlung:</strong> „Steuer“, „Freigabe“, „Provision“ als neue Zahlung.</li>"
                "<li><strong>Persönlicher „Berater“:</strong> WhatsApp/Telegram, Druck, Vertraulichkeitstaktik.</li>"
                "<li><strong>Klon-Identität:</strong> Name einer echten Firma, andere Domain, anderes Konto.</li>"
                "<li><strong>Zeitdruck:</strong> Bonus, „letzte Plätze“, drohende Kontosperrung.</li>"
                "</ul>",
            ),
            (
                "Zwei-Minuten-Prüfung vor jeder Zahlung",
                "<ol>"
                "<li>Exakte Domain notieren und mit der Registrierung der behaupteten Firma abgleichen.</li>"
                "<li>Warnlisten prüfen: BaFin, FMA, FINMA, IOSCO I-SCAN.</li>"
                "<li>Zahlungsempfänger prüfen: Firma oder Privatperson/Drittland?</li>"
                "<li>Test: kleine Auszahlung <em>vor</em> größerer Einzahlung verlangen.</li>"
                "</ol>",
            ),
            (
                "Wenn es schon passiert ist",
                "<p>Kein Grund für Scham — die Muster funktionieren bei Profis genauso. Dann gilt: <a href=\"../anlagebetrug-was-tun/\">was tun in den ersten 14 Tagen</a> und <a href=\"../anlagebetrug-geld-zurueck/\">realistische Wege zum Geld zurück</a>.</p>",
            ),
        ],
        "faqs": [
            (
                "Woran erkenne ich Anlagebetrug am schnellsten?",
                "An zwei Signalen: garantierte Rendite und der Forderung nach neuer Zahlung vor der Auszahlung. Eines davon reicht als Stopp-Signal.",
            ),
            (
                "Die Plattform hat eine Regulierungsnummer — dann ist sie sicher?",
                "Nicht automatisch. Nummern werden kopiert. Prüfen Sie die Nummer im Register der Behörde — und ob die Domain dort exakt hinterlegt ist.",
            ),
            (
                "Sind „KI-Trading-Bots“ mit Tagesrendite seriös?",
                "Produkte mit festen Tages-/Wochenrenditen aus „KI-Trading“ sind ein Kernmuster aktueller Anlagebetrugs-Kampagnen. Skepsis ist angebracht; Warnlisten prüfen.",
            ),
        ],
        "related": [
            ("../anlagebetrug-was-tun/", "Anlagebetrug: was tun?"),
            ("../anlagebetrug-anwalt/", "Anlagebetrug Anwalt"),
            ("../krypto-betrug-geld-zurueck/", "Krypto-Betrug: Geld zurück"),
        ],
        "source": "insights-de-anlagebetrug-erkennen",
    },
    {
        "slug": "betrug-mit-kryptowaehrung",
        "kicker": f"Kryptowährung · Aktualisiert {UPDATED}",
        "h1": "Betrug mit Kryptowährung: sechsstelliger Schaden — was jetzt trägt",
        "title": "Betrug mit Kryptowährung: Wege bei hohem Schaden | Mike Levy Law",
        "desc": "Betrug mit Kryptowährung — auch bei sechsstelligem Schaden: Tracing, Börsen, Anzeige und anwaltliche Durchsetzung nach Krypto-Betrug.",
        "keywords": "betrug mit kryptowährung, betrug kryptowährung sechsstelliger schaden, krypto-betrug, betrug kryptowährung, kryptowährung scam, betrug mit bitcoin",
        "lead": "Bei Betrug mit Kryptowährung im sechsstelligen Bereich ändert sich die Kalkulation: Tracing, formale Anfragen an Börsen und koordinierte straf- und zivilrechtliche Schritte werden wirtschaftlich — und Geschwindigkeit entscheidet über Datenlage und Spurenqualität.",
        "sections": [
            (
                "Warum sechsstellige Schäden anders behandelt werden",
                "<p>Ab dieser Größenordnung lohnt professionelles Blockchain-Tracing fast immer, Staatsanwaltschaften priorisieren anders, und zivilrechtliche Schritte gegen identifizierbare Mittäter oder Dienstleister werden rechnbar. Voraussetzung: saubere Beweislage ab Tag eins.</p>",
            ),
            (
                "Die tragenden Bausteine",
                "<ol>"
                "<li>Vollständige Transaktionshistorie: Hashes, Adressen, Zeitstempel, Plattform-Domain</li>"
                "<li>Tracing bis zu KYC-Börsen und Zahlungsdienstleistern</li>"
                "<li>Strafanzeige mit verwertbarer Darstellung — nicht nur „Betrug im Internet“</li>"
                "<li>Formale Anfragen an Börsen durch Ermittler oder Anwalt</li>"
                "<li>Fiat-Anteile (Karte/Überweisung) parallel über <a href=\"../anlagebetrug-geld-zurueck/\">Chargeback/Rückruf</a> prüfen</li>"
                "</ol>",
            ),
            (
                "Typische Fallen bei großen Schäden",
                "<p>Gerade sechsstellig Geschädigte werden von Recovery-Betrügern gezielt erneut kontaktiert — „wir haben Ihre Coins lokalisiert“. Zweites Warnsignal: Plattformen, die eine „Steuer“ von 10–20 % auf den angezeigten Kontostand verlangen. Beides ist Vorschussbetrug. Keine weiteren Zahlungen.</p>",
            ),
        ],
        "faqs": [
            (
                "Lohnt sich Vorgehen bei sechsstelligem Krypto-Schaden?",
                "Meist ja — Tracing, Ermittlungsdruck auf Börsen und zivilrechtliche Optionen werden bei dieser Höhe wirtschaftlich. Eine vertrauliche Prüfung klärt die konkreten Ansatzpunkte Ihres Falls.",
            ),
            (
                "Kann man bei Betrug mit Kryptowährung Geld zurückbekommen?",
                "Nicht über Rückbuchung — aber über Tracing zu regulierten Börsen, Ermittlungen und gegebenenfalls zivilrechtliche Ansprüche. Teilerfolge sind realistisch; Garantien sind es nicht.",
            ),
            (
                "Die Plattform zeigt Gewinne, verlangt aber „Steuer“ vor Auszahlung — was tun?",
                "Nicht zahlen. Der angezeigte Kontostand ist bei dieser Masche Teil der Täuschung. Beweise sichern und den Fall prüfen lassen — jede weitere Zahlung erhöht nur den Schaden.",
            ),
        ],
        "related": [
            ("../krypto-betrug-geld-zurueck/", "Krypto-Betrug: Geld zurück"),
            ("../krypto-betrug-anwalt/", "Krypto-Betrug Anwalt"),
            ("../anlagebetrug-melden/", "Betrug melden / anzeigen"),
        ],
        "source": "insights-de-betrug-mit-kryptowaehrung",
    },
    {
        "slug": "broker-auszahlung-problem",
        "kicker": f"Auszahlung · Aktualisiert {UPDATED}",
        "h1": "Broker Auszahlung Problem: warum Ihr Geld nicht ausgezahlt wird — und was hilft",
        "title": "Broker Auszahlung Problem: Geld nicht ausgezahlt | Mike Levy Law",
        "desc": "Broker Auszahlung Problem? Warum der Broker nicht auszahlt, Geld zurückhält oder die Auszahlung ewig dauert — Muster, Fristen und nächste Schritte.",
        "keywords": "broker auszahlung problem, geld nicht ausgezahlt, warum zahlt mir mein broker nicht aus, broker hält geld zurück, auszahlung dauert zu lange, broker zahlt nicht aus, forex broker auszahlung gesperrt, ist dieser broker seriös, nicht regulierte broker deutschland",
        "lead": "Die Auszahlung steht auf „pending“ — seit Wochen. Dann kommen neue Bedingungen. Ein Broker-Auszahlungsproblem ist oft das erste harte Signal, dass etwas nicht stimmt. Was Sie in den nächsten 14 Tagen tun, entscheidet, welche Optionen offen bleiben.",
        "sections": [
            (
                "Warum Auszahlungen wirklich scheitern",
                "<p>Operative Verzögerungen gibt es. Entscheidend ist das <strong>Muster</strong>: eine datierte Erklärung mit nachverfolgbarer Überweisung ist etwas anderes als wechselnde Ausreden — neue „Steuern“, „Freigabegebühren“, „Compliance-Zahlungen“ oder Funkstille, nachdem eine kleine Testauszahlung einmal klappte.</p>",
            ),
            (
                "Was Sie in den ersten 14 Tagen tun sollten",
                "<ol>"
                "<li>Keine weiteren Zahlungen — keine „Steuer“, kein „Unlock“, keine „Provision“.</li>"
                "<li>Chats, Mails, Kontoauszüge und die exakte Domain sichern.</li>"
                "<li>Bank/Kartenherausgeber informieren und Rückruf/Chargeback-Fristen erfragen.</li>"
                "<li>Regulierung prüfen: steht die Domain im BaFin-/FMA-/FINMA-Register — oder ist es ein Klon?</li>"
                "<li>Bei erheblichem Betrag: <a href=\"../anlagebetrug-anwalt/\">vertrauliche anwaltliche Prüfung</a>.</li>"
                "</ol>",
            ),
            (
                "„Ist dieser Broker seriös?“ — der Zwei-Minuten-Check",
                "<p>Prüfen Sie die exakte Domain im Register der zuständigen Behörde (nicht den Firmennamen in der Werbung), den Zahlungsempfänger auf Ihrem Kontoauszug, und Warnlisten. Nicht regulierte Broker mit Sitz außerhalb der EU sind kein Automatismus für Betrug — aber ohne Register-Eintrag zur Domain ist Vorsicht Pflicht.</p>",
            ),
        ],
        "faqs": [
            (
                "Warum zahlt mir mein Broker nicht aus?",
                "Kurze, klar begründete Verzögerungen kommen vor. Wechselnde Begründungen, neue Gebührenforderungen oder ein Einfrieren nach einer kleinen Testauszahlung sind klassische Warnsignale — Zahlungen stoppen und Beweise sichern.",
            ),
            (
                "Mein Broker hält mein Geld zurück — was zuerst?",
                "Schriftlich Auszahlung verlangen (Beweis), Bank/Kartenherausgeber kontaktieren, Auszahlungsverweigerung dokumentieren. Nicht auf neue Gebührenangebote eingehen.",
            ),
            (
                "Wie erkenne ich, ob mein Broker reguliert ist?",
                "Domain (nicht nur Firmenname) im BaFin-, FMA- oder FINMA-Register suchen. Steht die Domain dort nicht, ist sie keine regulierte Filiale — egal was die Webseite behauptet.",
            ),
        ],
        "related": [
            ("../geld-zurueck-broker/", "Geld zurück vom Broker"),
            ("../trading-betrug-geld-zurueck/", "Trading-Betrug: Geld zurück"),
            ("../anlagebetrug-erkennen/", "Anlagebetrug erkennen"),
        ],
        "source": "insights-de-broker-auszahlung-problem",
    },
    {
        "slug": "geld-zurueck-broker",
        "kicker": f"Rückholung · Aktualisiert {UPDATED}",
        "h1": "Geld zurück vom Broker: Rückholhilfe nach Betrug — seriös oder zweite Falle?",
        "title": "Geld zurück Broker: Rückholhilfe Betrug erkennen | Mike Levy Law",
        "desc": "Geld zurück vom Broker: Wie Sie Ihr Geld vom Broker zurückbekommen, was Rückholhilfe kostet — und woran Sie unseriöse Rückhol-Dienste erkennen.",
        "keywords": "geld zurück broker, wie bekomme ich mein geld vom broker zurück, rückholhilfe betrug, kosten für rückholhilfe, geld zurückholen broker, rechtsanwalt anlagebetrug, broker geld zurückfordern",
        "lead": "Nach dem Verlust kommt das zweite Angebot: „Wir holen Ihr Geld zurück.“ Ein Teil davon ist der nächste Betrug. Diese Seite trennt die echten Wege (Chargeback, Rückruf, Anwalt) von der Rückholhilfe-Falle.",
        "sections": [
            (
                "Die echten Wege zum Geld zurück",
                "<ul>"
                "<li><strong>Chargeback</strong> bei Kartenzahlung — schnell, aber fristgebunden.</li>"
                "<li><strong>Überweisungsrückruf</strong> über die eigene Bank — je früher, desto besser.</li>"
                "<li><strong>Strafanzeige</strong> — Basis für Ermittlungen und Bankanfragen.</li>"
                "<li><strong>Anwaltliche Prüfung</strong> — Beweisstruktur, richtige Gegenpartei, zivilrechtliche Optionen.</li>"
                "</ul>"
                "<p>Details: <a href=\"../anlagebetrug-geld-zurueck/\">Anlagebetrug: Geld zurück</a>.</p>",
            ),
            (
                "Rückholhilfe-Betrug: die Muster",
                "<ul>"
                "<li>Kaltakquise: Anruf oder Mail kurz nach Ihrem Verlust — woher haben die Ihre Daten?</li>"
                "<li>Vorkasse in Krypto, Gutscheinen oder Überweisung als „Freigabegebühr“.</li>"
                "<li>Erfolgsgarantie oder „Ihr Geld liegt bereits bereit“.</li>"
                "<li>Ausweis als Anwälte, Polizei oder Behörde — mit gefälschten Dokumenten.</li>"
                "</ul>"
                "<p>Seriöse Hilfe beginnt mit Prüfung Ihrer Unterlagen — nie mit einer Vorauszahlung zum „Entsperren“.</p>",
            ),
            (
                "Was kostet seriöse Rückholhilfe?",
                "<p>Anwaltliche Arbeit orientiert sich an Gegenstandswert und Aufwand; eine Ersteinschätzung klärt zuerst, ob sich weitere Schritte lohnen. Pauschale „Rückhol-Preise“ mit Garantie sind ein Warnsignal, kein Angebot.</p>",
            ),
        ],
        "faqs": [
            (
                "Wie bekomme ich mein Geld vom Broker zurück?",
                "Über den Zahlungsweg: Chargeback (Karte), Rückruf (Überweisung), Tracing (Krypto) — flankiert von Strafanzeige und, bei erheblichen Beträgen, anwaltlicher Prüfung. Ohne Garantie, aber in der richtigen Reihenfolge.",
            ),
            (
                "Sind Rückholhilfe-Dienste seriös?",
                "Einige Ermittlungs- und Beratungsleistungen sind es. Kaltakquise mit Vorkasse und Garantieversprechen ist das Kernmuster des Recovery-Betrugs — nicht zahlen.",
            ),
            (
                "Lohnt sich ein Rechtsanwalt bei Anlagebetrug?",
                "Bei erheblichen Beträgen meist ja: Er strukturiert Beweise, identifiziert die richtige Gegenpartei und koordiniert Bank, Anzeige und Klage — statt Fristen verstreichen zu lassen.",
            ),
        ],
        "related": [
            ("../anlagebetrug-anwalt/", "Anlagebetrug Anwalt"),
            ("../anlagebetrug-geld-zurueck/", "Anlagebetrug: Geld zurück"),
            ("../broker-auszahlung-problem/", "Broker Auszahlung Problem"),
        ],
        "source": "insights-de-geld-zurueck-broker",
    },
    {
        "slug": "bonusrfalle-hebelprodukte",
        "kicker": f"Bonus & Hebel · Aktualisiert {UPDATED}",
        "h1": "Bonusfalle Forex und Hebelprodukte-Betrug: warum der Bonus Ihre Auszahlung sperrt",
        "title": "Bonusfalle Forex & Hebelprodukte Betrug: Erklärung | Mike Levy Law",
        "desc": "Bonusfalle Forex erklärt: Wie Broker-Boni die Auszahlung sperren, Storno des Bonus verlangen — und was bei Hebelprodukte-Betrug zu tun ist.",
        "keywords": "bonusfalle, bonusfalle forex erklärung, storno bonus broker, forex broker auszahlung gesperrt, hebelprodukte betrug, broker bonus auszahlung gesperrt, bonus betrug forex",
        "lead": "„50 % Bonus auf Ihre Einzahlung!“ — und plötzlich ist Ihr eigenes Geld gesperrt. Die Bonusfalle ist einer der häufigsten Mechanismen, mit dem Forex- und CFD-Plattformen Auszahlungen blockieren. So funktioniert sie — und so kommen Sie heraus.",
        "sections": [
            (
                "Wie die Bonusfalle funktioniert",
                "<p>Der Bonus kommt mit „Umsatzbedingungen“, die im Kleingedruckten stehen: z. B. 30–50-faches Handelsvolumen, bevor <em>irgendeine</em> Auszahlung möglich ist — einschließlich Ihrer eigenen Einzahlung. Genau darin liegt die Sperre: Ihr Guthaben ist an Bedingungen gekettet, die praktisch unerfüllbar sind.</p>",
            ),
            (
                "Storno des Bonus verlangen",
                "<ol>"
                "<li>Schriftlich (E-Mail + Ticket) verlangen: Bonus stornieren, Bonusbedingungen für nichtig erklären, Auszahlung der Einzahlung.</li>"
                "<li>Ablehnung dokumentieren — sie ist Beweismaterial für Bank, Anzeige und Anwalt.</li>"
                "<li>Keine weiteren Trades „zum Freispielen“ — das erhöht nur den Verlust.</li>"
                "<li>Chargeback-Fristen bei Kartenzahlung parallel prüfen — nicht auf die Bonus-Diskussion warten.</li>"
                "</ol>",
            ),
            (
                "Hebelprodukte-Betrug: das größere Bild",
                "<p>Bei unregulierten Plattformen ist der Bonus oft nur der Anfang: manipulierte Kurse, „Slippage“, Zwangsliquidation und anschließende Auszahlungssperre gehören zum selben Muster. Prüfen Sie, ob die Domain überhaupt reguliert ist — und sichern Sie Screenshots, bevor das Konto „gelöscht“ wird. Mehr: <a href=\"../trading-betrug-geld-zurueck/\">Trading-Betrug: Geld zurück</a>.</p>",
            ),
        ],
        "faqs": [
            (
                "Kann ein Broker meine Auszahlung wegen eines Bonus sperren?",
                "Bei unseriösen Plattformen genau dafür ist der Bonus da. Regulierte Anbieter müssen Bedingungen transparent machen; das nachträgliche Verketten Ihrer Einzahlung mit Bonusbedingungen ist ein bekanntes Missbrauchsmuster.",
            ),
            (
                "Kann ich den Bonus stornieren lassen?",
                "Verlangen Sie es schriftlich und dokumentieren Sie die Antwort. Ob rechtlich durchsetzbar, hängt von Vertrag und Anbieter ab — die schriftliche Ablehnung ist auf jeden Fall verwertbares Beweismaterial.",
            ),
            (
                "Soll ich erst die Umsatzbedingungen erfüllen?",
                "Nein. Weiteres Traden „zum Freispielen“ ist genau das Ziel der Falle — es verwandelt einen auszahlbaren Rest in einen Totalverlust. Stoppen, dokumentieren, Bank- und Rechtswege prüfen.",
            ),
        ],
        "related": [
            ("../trading-betrug-geld-zurueck/", "Trading-Betrug: Geld zurück"),
            ("../broker-auszahlung-problem/", "Broker Auszahlung Problem"),
            ("../geld-zurueck-broker/", "Geld zurück vom Broker"),
        ],
        "source": "insights-de-bonusrfalle-hebelprodukte",
    },
]

HUB_CARDS = [
    ("anlagebetrug-geld-zurueck/", "Geld zurück · Priorität", "Anlagebetrug: Geld zurück", "Chargeback, Rückruf, Krypto-Tracing — die realistische Reihenfolge nach Zahlungsweg.", "anlagebetrug geld zurück · geld zurückholen · rückbuchung"),
    ("anlagebetrug-anwalt/", "Anwalt · Priorität", "Anlagebetrug Anwalt", "Wann sich rechtliche Hilfe lohnt, was die vertrauliche Prüfung leistet, was sie kostet.", "anlagebetrug anwalt · rechtsanwalt · erfahrungen"),
    ("krypto-betrug-geld-zurueck/", "Geld zurück", "Krypto-Betrug: Geld zurück", "Tracing, Börsen-Meldung, Anzeige — was nach einem Krypto-Scam realistisch ist.", "krypto betrug geld zurück · chancen geld zurück"),
    ("krypto-betrug-anwalt/", "Anwalt", "Krypto-Betrug Anwalt", "Prüfung, Blockchain-Tracing und Durchsetzung — standortübergreifend.", "krypto betrug anwalt · krypto anwalt · in der nähe"),
    ("bitcoin-geld-zurueckholen/", "Bitcoin", "Bitcoin zurückholen", "Final heißt nicht unsichtbar: Hashes, Tracing, Börsen und Anzeige.", "bitcoin geld zurückholen · btc betrug geld zurück"),
    ("trading-betrug-geld-zurueck/", "Geld zurück", "Trading-Betrug: Geld zurück", "Fake-Broker, blockierte Auszahlung, „Steuer“ vor Payout — Gegenmaßnahmen.", "trading betrug geld zurück · broker betrug geld zurück"),
    ("anlagebetrug-was-tun/", "Sofort", "Anlagebetrug: was tun?", "Die ersten 14 Tage: stoppen, sichern, Bank, Anzeige, Prüfung.", "anlagebetrug was tun · sofortmaßnahmen"),
    ("anlagebetrug-melden/", "Melden", "Anlagebetrug melden / anzeigen", "Polizei, Online-Wache, BaFin — Stellen und Unterlagen für eine verwertbare Anzeige.", "anlagebetrug melden · anzeigen · scam melden polizei"),
    ("online-betrug-geld-zurueckfordern/", "Geld zurück", "Online-Betrug: Geld zurückfordern", "Der richtige Weg nach Zahlungsart: Karte, Überweisung, Krypto.", "online betrug geld zurück · zurückfordern"),
    ("anlagebetrug-erkennen/", "Prävention", "Anlagebetrug erkennen", "Die fünf Kernmuster — und die Zwei-Minuten-Prüfung vor jeder Zahlung.", "anlagebetrug erkennen · warnsignale · krypto betrug erkennen"),
    ("betrug-mit-kryptowaehrung/", "Krypto · Priorität", "Betrug mit Kryptowährung", "Sechsstelliger Schaden: Tracing, Börsen, Anzeige und Durchsetzung.", "betrug mit kryptowährung · sechsstelliger schaden · krypto-betrug"),
    ("broker-auszahlung-problem/", "Auszahlung · Priorität", "Broker Auszahlung Problem", "Warum der Broker nicht auszahlt — Muster, Fristen, erste 14 Tage.", "broker auszahlung problem · geld nicht ausgezahlt · broker hält geld zurück"),
    ("geld-zurueck-broker/", "Rückholung", "Geld zurück vom Broker", "Echte Wege vs. Rückholhilfe-Betrug — Kosten und Muster der zweiten Falle.", "geld zurück broker · rückholhilfe betrug · rechtsanwalt anlagebetrug"),
    ("bonusrfalle-hebelprodukte/", "Bonus & Hebel", "Bonusfalle Forex & Hebelprodukte", "Wie der Bonus die Auszahlung sperrt — Storno verlangen, Fristen sichern.", "bonusfalle forex · storno bonus broker · hebelprodukte betrug"),
]


def page_html(g: dict) -> str:
    slug = g["slug"]
    canon = f"{SITE}/de/insights/{slug}/"
    contact = f"../../../index.html?source={escape(g['source'])}#contact"
    faq_ld = [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in g["faqs"]
    ]
    faq_html = "\n".join(
        f"<details{' open' if i == 0 else ''}><summary>{escape(q)}</summary><p>{escape(a)}</p></details>"
        for i, (q, a) in enumerate(g["faqs"])
    )
    sections = "\n".join(f"<h2>{escape(h)}</h2>\n{body}" for h, body in g["sections"])
    related = "\n".join(f'        <a href="{href}">{label}</a>' for href, label in g["related"])
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Start", "item": f"{SITE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Insights (DE)", "item": f"{SITE}/de/insights/"},
                    {"@type": "ListItem", "position": 3, "name": g["h1"], "item": canon},
                ],
            },
            {
                "@type": "Article",
                "headline": g["h1"],
                "description": g["desc"],
                "inLanguage": "de-DE",
                "datePublished": DATE_ISO,
                "dateModified": DATE_ISO,
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
<html lang="de-DE">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{escape(g["title"])}</title>
  <meta name="description" content="{escape(g["desc"])}" />
  <meta name="keywords" content="{escape(g["keywords"])}" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <meta name="author" content="Mike Levy Law" />
  <link rel="canonical" href="{canon}" />
  <link rel="alternate" hreflang="de" href="{canon}" />
  <link rel="alternate" hreflang="x-default" href="{canon}" />
  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="Mike Levy Law" />
  <meta property="og:locale" content="de_DE" />
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
  <link rel="stylesheet" href="../../insights/styles.css" />
  <script type="application/ld+json">{ld}</script>
</head>
<body>
  <header class="top">
    <div class="wrap-wide top-inner">
      <a class="brand" href="../../../index.html" aria-label="Mike Levy Law">
        <svg class="logo-mark" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <circle cx="24" cy="24" r="22" stroke="currentColor" stroke-width="1.5" fill="rgba(255,255,255,0.06)"/>
          <path d="M24 10 L24 14 M14 20 H34 M16 20 V34 H32 V20" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M20 34 V28 H28 V34" stroke="currentColor" stroke-width="1.5"/>
          <path d="M18 20 C18 16 21 14 24 14 C27 14 30 16 30 20" stroke="currentColor" stroke-width="1.5" fill="none"/>
          <circle cx="24" cy="12" r="2" fill="currentColor"/>
        </svg>
        <div class="logo-text">Mike Levy<span>Law</span></div>
      </a>
      <nav class="crumbs" aria-label="Breadcrumb"><a href="../../../index.html">Start</a><span>/</span><a href="../">Insights</a><span>/</span><span>{escape(slug.replace("-", " "))}</span></nav>
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
      <h2 id="faq-h">Häufige Fragen</h2>
      <p class="faq-lead">Klare Antworten zu nächsten Schritten, Fristen und wann eine vertrauliche Prüfung hilft.</p>
      <div class="faq">
{faq_html}
      </div>
    </section>
    <div class="cta-strip">
      <div>
        <strong>Vertrauliche Prüfung anfordern?</strong>
        <p>Die Ersteinschätzung ist kostenlos. Wir prüfen zunächst Ihren Anspruch sowie dessen Aussichten und Durchsetzbarkeit — das hängt vom Stand der Beweise ab. Keine Erfolgsgarantie.</p>
      </div>
      <a href="{contact}">Beratung anfordern</a>
    </div>
    <p class="note">Nur Informationen. Keine Rechtsberatung und keine Garantie auf Wiedererlangung. Eine Kontaktaufnahme begründet kein Mandatsverhältnis.</p>
  </main>
  <footer class="site-footer">
    <div class="wrap-wide site-footer-inner">
      <p><a href="../">Insights (DE)</a> · <a href="../../../company-broker-index/">Firmen- &amp; Broker-Index</a> · <a href="{contact}">Kontakt</a> · <a href="../../../legal/privacy-policy.html">Datenschutz</a> · <a href="../../../legal/terms-of-use.html">Nutzungsbedingungen</a> · <a href="../../../legal/disclaimer.html">Haftungsausschluss</a></p>
      <p>&copy; MLL 2026</p>
      <p class="footer-nap">1395 Brickell Ave, Suite 800 · Miami, FL 33131 · USA · <a href="mailto:info@mikelevylaw.com">info@mikelevylaw.com</a></p>
    </div>
  </footer>
  <script src="/js/tawk-mll.js" defer></script>
</body>
</html>
"""


def hub_html() -> str:
    canon = f"{SITE}/de/insights/"
    cards = "\n".join(
        f'''      <a class="folder" href="{href}">
        <div class="tag">{escape(tag)}</div>
        <h2>{escape(h2)}</h2>
        <p>{escape(p)}</p>
        <p class="kw">{escape(kw)}</p>
      </a>'''
        for href, tag, h2, p, kw in HUB_CARDS
    )
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "CollectionPage",
                "name": "Anlagebetrug-Ratgeber (Deutsch)",
                "url": canon,
                "inLanguage": "de-DE",
                "description": "Deutschsprachige Ratgeber zu Anlagebetrug, Krypto-Betrug und Trading-Betrug: Geld zurück, Anwalt, melden, erkennen.",
                "hasPart": [
                    {"@type": "WebPage", "name": h2, "url": f"{SITE}/de/insights/{href}"}
                    for href, _t, h2, _p, _k in HUB_CARDS
                ],
            }
        ],
    }
    ld = json.dumps(graph, ensure_ascii=False)
    return f"""<!DOCTYPE html>
<html lang="de-DE">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Anlagebetrug Ratgeber: Geld zurück, Anwalt, melden | Mike Levy Law</title>
  <meta name="description" content="Anlagebetrug, Krypto-Betrug, Trading-Betrug: Geld zurück, Anwalt, was tun, melden und erkennen — deutschsprachige Ratgeber von Mike Levy Law." />
  <meta name="keywords" content="anlagebetrug, anlagebetrug geld zurück, anlagebetrug anwalt, krypto betrug, bitcoin betrug, trading betrug, broker betrug, anlagebetrug was tun, anlagebetrug melden, anlagebetrug erkennen" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <meta name="author" content="Mike Levy Law" />
  <link rel="canonical" href="{canon}" />
  <link rel="alternate" hreflang="de" href="{canon}" />
  <link rel="alternate" hreflang="x-default" href="{canon}" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Mike Levy Law" />
  <meta property="og:locale" content="de_DE" />
  <meta property="og:title" content="Anlagebetrug Ratgeber: Geld zurück, Anwalt, melden | Mike Levy Law" />
  <meta property="og:description" content="Deutschsprachige Ratgeber zu Anlagebetrug, Krypto-Betrug und Trading-Betrug." />
  <meta property="og:url" content="{canon}" />
  <meta property="og:image" content="{SITE}/hero-books.jpg" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700&family=Playfair+Display:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../../insights/styles.css" />
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
      <nav class="crumbs" aria-label="Breadcrumb"><a href="../../index.html">Start</a><span>/</span><span>Insights (DE)</span></nav>
    </div>
  </header>
  <main class="wrap">
    <div class="hero">
      <p class="kicker">Ratgeber · Deutsch · Aktualisiert {UPDATED}</p>
      <h1>Anlagebetrug-Ratgeber: Geld zurück, Anwalt, melden</h1>
      <p class="lead">
        Beginnen Sie mit Ihrer Situation — <strong>Geld zurück</strong>, <strong>Anwalt</strong>,
        <strong>was tun</strong> oder <strong>melden</strong> — für Anlagebetrug, Krypto-Betrug und
        Trading-Betrug. Geschrieben für Klarheit, nicht für Versprechen. Keine Erfolgsgarantie.
      </p>
    </div>

    <div class="folder-grid">
{cards}
    </div>
  </main>
  <footer class="site-footer">
    <div class="wrap-wide site-footer-inner">
      <p><a href="../../insights/">Insights (EN)</a> · <a href="../../company-broker-index/">Firmen- &amp; Broker-Index</a> · <a href="../../index.html?source=insights-de-hub#contact">Kontakt</a> · <a href="../../legal/privacy-policy.html">Datenschutz</a> · <a href="../../legal/disclaimer.html">Haftungsausschluss</a></p>
      <p>&copy; MLL 2026</p>
      <p class="footer-nap">1395 Brickell Ave, Suite 800 · Miami, FL 33131 · USA · <a href="mailto:info@mikelevylaw.com">info@mikelevylaw.com</a></p>
    </div>
  </footer>
  <script src="/js/tawk-mll.js" defer></script>
</body>
</html>
"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.html").write_text(hub_html(), encoding="utf-8")
    print("Wrote de/insights/index.html")
    for g in GUIDES:
        dest = OUT / g["slug"]
        dest.mkdir(parents=True, exist_ok=True)
        path = dest / "index.html"
        path.write_text(page_html(g), encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT)}")
    print(f"Done — {len(GUIDES)} German keyword guides + hub")


if __name__ == "__main__":
    main()
