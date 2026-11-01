#!/usr/bin/env python3
"""Rebuild SBL_COMMENTS for every broker in brokers.js.

Each broker gets composed, slug-specific comments (no shared full title/body
templates reused across profiles). Support replies only on important-loss
threads. Hand-curated slugs are preserved; everything else regenerates with
--force.
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

# Only these keep hand-written threads across --force rebuilds
CURATED_SLUGS = {
    "next-forrest-review",
}

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

FIRST_NAMES = [
    "Ava", "Noah", "Mia", "Liam", "Elena", "Omar", "Priya", "Hans", "Clara",
    "Luis", "Ana", "Giulia", "Kenji", "Sofia", "Marcus", "Amira", "Daniel",
    "Caroline", "Thomas", "Isabella", "Mei", "Lucas", "Hannah", "Jonas",
    "Yara", "Felix", "Nina", "Mateo", "Ines", "Ravi", "Chloe", "Erik",
    "Lara", "Hugo", "Noor", "Pavel", "Irina", "Diego", "Camille", "Owen",
    "Freya", "Soren", "Leila", "Andre", "Marta", "Viktor", "Sara", "Ian",
    "Helena", "Bruno", "Aisha", "Nils", "Vera", "Rafael", "Zoe", "Malik",
    "Petra", "Callum", "Amina", "Johan", "Lucia", "Tariq", "Emilia", "Sean",
    "Nadia", "Pierre", "Kira", "Hassan", "Olivia", "Marco", "Yusuf", "Ellen",
]

LAST_NAMES = [
    "Hayes", "Nair", "Brennan", "Whitmore", "Hassan", "Watanabe", "Mendoza",
    "Okonkwo", "Popescu", "Berg", "Vo", "Al Farsi", "Rossi", "Pretorius",
    "Chen", "Müller", "Schmidt", "García", "Costa", "Bianchi", "Novak",
    "Silva", "Kowalski", "Dubois", "Andersen", "Petrov", "Nguyen", "Okafor",
    "Lindqvist", "Moreau", "Santos", "Keller", "Iqbal", "Fernández", "Hughes",
    "Yamamoto", "Nowak", "Baptiste", "Rahman", "Olsen", "Castillo", "Murray",
    "Ibrahim", "Vogel", "Almeida", "Johansson", "Park", "Sullivan", "Kaya",
    "Weber", "Diaz", "Fischer", "Romano", "Singh", "Cohen", "Bailey", "Cruz",
]

COUNTRY_POOL = [
    "Germany", "Spain", "Italy", "France", "Brazil", "Netherlands",
    "Poland", "Romania", "Turkey", "United Kingdom", "Singapore",
    "United Arab Emirates", "Australia", "Canada", "Japan",
    "South Africa", "Mexico", "Portugal", "Chile", "Colombia",
    "Ireland", "Sweden", "Norway", "Austria", "Belgium", "New Zealand",
]

AMOUNTS = [
    "$4,200", "$7,850", "$11,400", "$18,600", "$23,900", "$31,200",
    "$42,500", "$56,000", "$68,750", "$91,000", "€3,800", "€6,450",
    "€9,200", "€14,700", "€22,100", "€37,500", "€48,900", "£2,950",
    "£5,400", "£8,750", "£12,300", "£19,800", "£27,600", "about $15k",
    "roughly €20k", "just over £9,000", "close to $50,000", "nearly €12,000",
]

CHANNELS = {
    "en": [
        "the web platform", "their mobile app", "a Telegram desk", "an account manager on WhatsApp",
        "a cold-call broker desk", "an Instagram lead form", "a recovery chat", "email support only",
    ],
    "de": [
        "die Web-Plattform", "die Mobile-App", "einen Telegram-Desk", "einen WhatsApp-Betreuer",
        "einen Telefonvertrieb", "ein Instagram-Formular", "einen Recovery-Chat", "nur E-Mail-Support",
    ],
    "es": [
        "la plataforma web", "su app móvil", "un escritorio de Telegram", "un gestor por WhatsApp",
        "un broker por llamada", "un formulario de Instagram", "un chat de recuperación", "solo soporte por email",
    ],
    "it": [
        "la piattaforma web", "la loro app", "un desk Telegram", "un manager su WhatsApp",
        "un broker telefonico", "un form Instagram", "una chat di recovery", "solo supporto email",
    ],
    "fr": [
        "la plateforme web", "leur application", "un desk Telegram", "un gestionnaire WhatsApp",
        "un courtier par appel", "un formulaire Instagram", "un chat de récupération", "support e-mail seulement",
    ],
    "pt": [
        "a plataforma web", "a app móvel", "um desk no Telegram", "um gestor no WhatsApp",
        "um broker por telefone", "um formulário no Instagram", "um chat de recovery", "só suporte por e-mail",
    ],
    "nl": [
        "het webplatform", "hun mobiele app", "een Telegram-desk", "een WhatsApp-manager",
        "een telefonische broker", "een Instagram-formulier", "een recovery-chat", "alleen e-mailsupport",
    ],
    "pl": [
        "platformę WWW", "ich aplikację", "desk Telegram", "opiekuna na WhatsApp",
        "brokera telefonicznego", "formularz Instagram", "czat recovery", "tylko e-mail",
    ],
    "ro": [
        "platforma web", "aplicația mobilă", "un desk Telegram", "un manager pe WhatsApp",
        "un broker telefonic", "un formular Instagram", "un chat de recovery", "doar suport email",
    ],
    "tr": [
        "web platformu", "mobil uygulamaları", "bir Telegram masası", "WhatsApp yöneticisi",
        "telefonla arayan broker", "Instagram formu", "recovery sohbeti", "yalnızca e-posta destek",
    ],
}

PAYMENTS = {
    "en": [
        "card deposit", "bank wire", "crypto transfer", "e-wallet top-up",
        "same-day SEPA", "USDT transfer", "Apple Pay deposit", "wire in two tranches",
    ],
    "de": [
        "Karteneinzahlung", "Banküberweisung", "Krypto-Transfer", "E-Wallet-Aufladung",
        "SEPA am selben Tag", "USDT-Transfer", "Apple-Pay-Einzahlung", "Überweisung in zwei Tranchen",
    ],
    "es": [
        "depósito con tarjeta", "transferencia bancaria", "transferencia cripto", "recarga de monedero",
        "SEPA el mismo día", "transferencia USDT", "depósito Apple Pay", "transferencia en dos tramos",
    ],
    "it": [
        "deposito con carta", "bonifico", "transfer cripto", "ricarica e-wallet",
        "SEPA same-day", "transfer USDT", "deposito Apple Pay", "bonifico in due tranche",
    ],
    "fr": [
        "dépôt par carte", "virement bancaire", "transfert crypto", "rechargement e-wallet",
        "SEPA le jour même", "transfert USDT", "dépôt Apple Pay", "virement en deux tranches",
    ],
    "pt": [
        "depósito com cartão", "transferência bancária", "transferência crypto", "carregamento e-wallet",
        "SEPA no mesmo dia", "transferência USDT", "depósito Apple Pay", "transferência em duas tranches",
    ],
    "nl": [
        "kaartstorting", "bankoverschrijving", "crypto-transfer", "e-wallet-opwaardering",
        "zelfde-dag SEPA", "USDT-transfer", "Apple Pay-storting", "overschrijving in twee tranches",
    ],
    "pl": [
        "wpłata kartą", "przelew bankowy", "transfer krypto", "doładowanie e-wallet",
        "SEPA tego samego dnia", "transfer USDT", "wpłata Apple Pay", "przelew w dwóch transzach",
    ],
    "ro": [
        "depunere cu card", "transfer bancar", "transfer crypto", "încărcare e-wallet",
        "SEPA în aceeași zi", "transfer USDT", "depunere Apple Pay", "transfer în două tranșe",
    ],
    "tr": [
        "kart yatırımı", "havale", "kripto transferi", "e-cüzdan yükleme",
        "aynı gün SEPA", "USDT transferi", "Apple Pay yatırımı", "iki dilimde havale",
    ],
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

# Composition banks: titles + sentence parts. Combined per slug so full strings rarely collide.
TITLE_HARD = {
    "en": [
        "Withdrawal stalled after deposit",
        "Account frozen when I asked for cash out",
        "Extra fees before any payout",
        "Dashboard profits never reached my bank",
        "Support loop — no real release of funds",
        "Test withdrawal worked once, then nothing",
        "Cannot move funds off the platform",
        "Locked out after requesting a transfer",
        "Still chasing a blocked payout",
        "Deposit cleared, exit never did",
        "Asked for tax fee before release",
        "Balance shows, bank never receives",
        "Manager vanished after larger request",
        "Screenshots saved — still no payout",
        "Urgent: funds stuck after “verification”",
    ],
    "de": [
        "Auszahlung nach Einzahlung blockiert",
        "Konto gesperrt bei Auszahlungswunsch",
        "Extra-Gebühren vor jeder Freigabe",
        "Gewinne nur auf dem Dashboard",
        "Support-Schleife ohne Auszahlung",
        "Kleine Testauszahlung, dann nichts",
        "Kein Zugriff auf meine Einlagen",
        "Gesperrt nach Transferanfrage",
        "Auszahlung weiter blockiert",
        "Einzahlung da — Auszahlung nicht",
        "Steuergebühr vor Freigabe verlangt",
        "Saldo sichtbar, Bank leer",
        "Betreuer weg nach größerer Anfrage",
        "Nachweise da — trotzdem keine Auszahlung",
        "Dringend: Gelder nach „Verifizierung“ stecken",
    ],
    "es": [
        "Retiro bloqueado tras el depósito",
        "Cuenta congelada al pedir el cobro",
        "Comisiones extra antes de pagar",
        "Beneficios solo en el panel",
        "Soporte da largas sin liberar fondos",
        "Retiro de prueba, luego silencio",
        "No puedo sacar el dinero",
        "Bloqueo tras pedir transferencia",
        "Sigo sin el pago prometido",
        "Entró el depósito, no la salida",
        "Pidieron tasa fiscal antes",
        "Saldo visible, banco en cero",
        "El gestor desapareció",
        "Tengo capturas — sin cobro",
        "Urgente: fondos atrapados en “verificación”",
    ],
    "it": [
        "Prelievo bloccato dopo il deposito",
        "Conto congelato alla richiesta di cash-out",
        "Commissioni extra prima del pagamento",
        "Profitti solo sul pannello",
        "Supporto che rimanda senza sbloccare",
        "Prelievo test ok, poi nulla",
        "Non riesco a spostare i fondi",
        "Blocco dopo la richiesta di bonifico",
        "Payout ancora bloccato",
        "Deposito ok — uscita no",
        "Chiesto un “tax fee” prima",
        "Saldo visibile, banca vuota",
        "Il manager è sparito",
        "Screenshot salvati — niente prelievo",
        "Urgente: fondi bloccati in “verifica”",
    ],
    "fr": [
        "Retrait bloqué après dépôt",
        "Compte gelé à la demande de sortie",
        "Frais supplémentaires avant tout paiement",
        "Profits seulement sur le tableau",
        "Support qui temporise sans libérer",
        "Petit retrait test, puis rien",
        "Impossible de sortir les fonds",
        "Verrouillage après demande de virement",
        "Paiement toujours bloqué",
        "Dépôt OK — sortie non",
        "Frais fiscaux exigés avant",
        "Solde affiché, banque vide",
        "Le gestionnaire a disparu",
        "Preuves gardées — pas de retrait",
        "Urgent : fonds coincés en “vérification”",
    ],
    "pt": [
        "Saque bloqueado após depósito",
        "Conta congelada ao pedir retirada",
        "Taxas extras antes de qualquer pagamento",
        "Lucros só no painel",
        "Suporte enrola sem liberar",
        "Saque teste ok, depois nada",
        "Não consigo tirar os fundos",
        "Bloqueio após pedir transferência",
        "Pagamento ainda preso",
        "Depósito entrou — saída não",
        "Pediram taxa fiscal antes",
        "Saldo aparece, banco zerado",
        "Gestor sumiu depois do pedido maior",
        "Prints salvos — sem saque",
        "Urgente: fundos presos na “verificação”",
    ],
    "nl": [
        "Opname geblokkeerd na storting",
        "Account bevroren bij uitvraag",
        "Extra kosten vóór uitbetaling",
        "Winst alleen op het dashboard",
        "Support blijft uitstellen",
        "Testopname werkte, daarna niets",
        "Kan fondsen niet weghalen",
        "Vergrendeld na overboekingsverzoek",
        "Uitbetaling nog geblokkeerd",
        "Storting wel — uitgang niet",
        "Belastingfee gevraagd eerst",
        "Saldo zichtbaar, bank leeg",
        "Manager verdween na groter verzoek",
        "Bewijs bewaard — geen opname",
        "Urgent: geld vast in “verificatie”",
    ],
    "pl": [
        "Wypłata zablokowana po wpłacie",
        "Konto zamrożone przy cash-out",
        "Dodatkowe opłaty przed wypłatą",
        "Zyski tylko na panelu",
        "Support przeciąga bez wypłaty",
        "Testowa wypłata, potem cisza",
        "Nie mogę wypłacić środków",
        "Blokada po wniosku o przelew",
        "Wypłata wciąż zablokowana",
        "Wpłata OK — wypłata nie",
        "Żądanie opłaty podatkowej",
        "Saldo widać, bank pusty",
        "Opiekun zniknął po większej kwocie",
        "Zrzuty mam — wypłaty nie",
        "Pilne: środki w “weryfikacji”",
    ],
    "ro": [
        "Retragere blocată după depunere",
        "Cont înghețat la cash-out",
        "Taxe extra înainte de plată",
        "Profituri doar pe panou",
        "Suport care amână fără eliberare",
        "Retragere test, apoi tăcere",
        "Nu pot muta fondurile",
        "Blocare după cerere de transfer",
        "Plata încă blocată",
        "Depunere OK — ieșire nu",
        "Au cerut taxă fiscală întâi",
        "Sold vizibil, bancă goală",
        "Managerul a dispărut",
        "Am capturi — fără retragere",
        "Urgent: fonduri blocate în “verificare”",
    ],
    "tr": [
        "Yatırımdan sonra çekim engeli",
        "Cash-out isteğinde hesap kilitlendi",
        "Ödeme öncesi ek ücret",
        "Kâr sadece panelde",
        "Destek oyalıyor, para yok",
        "Test çekimi oldu, sonra yok",
        "Fonları çıkaramıyorum",
        "Havale sonrası kilit",
        "Ödeme hâlâ bloke",
        "Yatırım girdi — çıkış yok",
        "Önce vergi ücreti istendi",
        "Bakiye var, banka boş",
        "Yönetici büyük talepte kayboldu",
        "Ekran görüntüleri var — çekim yok",
        "Acil: “doğrulama”da takılı fon",
    ],
}

TITLE_SOFT = {
    "en": [
        "Need a real-vs-clone check",
        "Unsure how to escalate this",
        "Want paperwork reviewed quietly",
        "Mixed signals on the public record",
        "Is this the genuine firm?",
        "Looking for next-step advice",
        "Domain lookalike concern",
        "Complaint path is unclear",
        "Need help reading the licence claim",
        "Statements ready — who reviews them?",
    ],
    "de": [
        "Echtfirma oder Imitat prüfen",
        "Unklar, wie ich eskaliere",
        "Unterlagen vertraulich prüfen lassen",
        "Gemischte Signale in öffentlichen Quellen",
        "Ist das die echte Firma?",
        "Rat zum nächsten Schritt",
        "Sorge wegen Domain-Lookalike",
        "Beschwerdeweg unklar",
        "Lizenzangabe prüfen lassen",
        "Belege bereit — wer schaut drauf?",
    ],
    "es": [
        "Verificar firma real vs clon",
        "No sé cómo escalar esto",
        "Revisión confidencial de papeles",
        "Señales mixtas en el registro público",
        "¿Es la empresa genuina?",
        "Consejo sobre el siguiente paso",
        "Duda por dominio similar",
        "Ruta de reclamación poco clara",
        "Ayuda con la licencia mostrada",
        "Tengo extractos — ¿quién los revisa?",
    ],
    "it": [
        "Verifica società reale vs clone",
        "Non so come escalare",
        "Revisione confidenziale documenti",
        "Segnali misti nei registri pubblici",
        "È la società genuina?",
        "Consiglio sul passo successivo",
        "Dubbio su dominio simile",
        "Percorso reclamo poco chiaro",
        "Aiuto sulla licenza mostrata",
        "Ho estratti — chi li esamina?",
    ],
    "fr": [
        "Vérifier société réelle vs clone",
        "Incertain sur l’escalade",
        "Revue confidentielle des pièces",
        "Signaux mixtes dans le public",
        "Est-ce la vraie société ?",
        "Conseil pour l’étape suivante",
        "Doute sur un domaine proche",
        "Voie de réclamation floue",
        "Aide sur la licence affichée",
        "Relevés prêts — qui les lit ?",
    ],
    "pt": [
        "Verificar empresa real vs clone",
        "Não sei como escalar",
        "Revisão confidencial dos papéis",
        "Sinais mistos no registo público",
        "É a empresa genuína?",
        "Conselho para o próximo passo",
        "Dúvida com domínio parecido",
        "Caminho de reclamação pouco claro",
        "Ajuda com a licença mostrada",
        "Extratos prontos — quem analisa?",
    ],
    "nl": [
        "Echt bedrijf vs lookalike checken",
        "Weet niet hoe te escaleren",
        "Papieren stil laten nakijken",
        "Gemengde signalen in open bronnen",
        "Is dit het echte bedrijf?",
        "Advies voor volgende stap",
        "Zorg om lookalike-domein",
        "Klachtroute onduidelijk",
        "Hulp bij getoonde licentie",
        "Afschriften klaar — wie bekijkt ze?",
    ],
    "pl": [
        "Sprawdzić firmę vs klon",
        "Nie wiem, jak eskalować",
        "Poufna ocena dokumentów",
        "Mieszane sygnały w rejestrach",
        "Czy to prawdziwa firma?",
        "Rada co do następnego kroku",
        "Obawa o podobną domenę",
        "Ścieżka reklamacji niejasna",
        "Pomoc z pokazaną licencją",
        "Mam wyciągi — kto je sprawdzi?",
    ],
    "ro": [
        "Verificare firmă reală vs clon",
        "Nu știu cum să escaladez",
        "Revizuire confidențială acte",
        "Semnale mixte în surse publice",
        "E firma autentică?",
        "Sfat pentru pasul următor",
        "Îngrijorare domeniu similar",
        "Calea de reclamație neclară",
        "Ajutor cu licența afișată",
        "Am extrase — cine le verifică?",
    ],
    "tr": [
        "Gerçek firma / taklit kontrolü",
        "Nasıl yükselteceğimi bilmiyorum",
        "Evrakları gizli inceletmek",
        "Kamuda karışık sinyaller",
        "Gerçek şirket mi?",
        "Sonraki adım için öneri",
        "Benzer alan adı endişesi",
        "Şikâyet yolu belirsiz",
        "Gösterilen lisans için yardım",
        "Ekstreler hazır — kim bakar?",
    ],
}

# Body parts: open / mid / ask — joined into unique paragraphs
BODY_HARD = {
    "en": {
        "open": [
            "I funded through {channel} after a {payment}.",
            "I put money in via a {payment} on {channel}.",
            "Started with a {payment}; activity looked normal at first on {channel}.",
            "Onboarded through {channel} and sent a {payment}.",
            "Followed instructions from {channel} and completed a {payment}.",
        ],
        "mid_imp": [
            "About {amount} is still stuck after they blocked the withdrawal and asked for more fees.",
            "Roughly {amount} never cleared to my bank once they froze the larger request.",
            "They showed green “profits,” then held back about {amount} pending a new charge.",
            "The open balance near {amount} will not move without another “release” payment.",
            "I am missing close to {amount} that still sits on-screen while payouts fail.",
        ],
        "mid": [
            "Withdrawals then stalled and chat only recycled the same checklist.",
            "A small test payout went through once; the real request never completed.",
            "Support kept pushing new verification steps without releasing funds.",
            "The manager stopped answering after I refused another fee.",
            "Every cash-out ticket closed with a delay story and no wire.",
            "I still have the chat log, receipts, and wallet/reference IDs.",
            "They cited compliance holds that never resolved into a transfer.",
        ],
        "ask": [
            "Can someone advise if a confidential review is still worth it?",
            "Who should I contact with the timeline and proof I still have?",
            "Is there a practical next step before I chase banks or police alone?",
            "Please say whether counsel can still look at this quietly.",
            "Any guidance on what to keep and where to send it?",
        ],
        "mention": [
            " This was under the {name} name.",
            " The site I used was tied to {name}.",
            " I dealt with what presented as {name}.",
            " Domain on my notes: {domain}.",
            "",
            "",
            "",
        ],
    },
    "de": {
        "open": [
            "Ich habe über {channel} mit einer {payment} eingezahlt.",
            "Einstieg über {channel}, Zahlung per {payment}.",
            "Zuerst wirkte {channel} normal nach meiner {payment}.",
        ],
        "mid_imp": [
            "Etwa {amount} stecken fest, nachdem die Auszahlung blockiert und neue Gebühren verlangt wurden.",
            "Rund {amount} kamen nie auf mein Konto, als die größere Anfrage eingefroren wurde.",
            "Auf dem Dashboard stand Gewinn, aber etwa {amount} wurden nicht freigegeben.",
        ],
        "mid": [
            "Danach blieben Auszahlungen stehen; der Chat wiederholte nur Checklisten.",
            "Eine kleine Testauszahlung klappte einmal — die echte nicht.",
            "Support verlangte neue Schritte, ohne Geld freizugeben.",
            "Der Betreuer antwortete nicht mehr, als ich weitere Gebühren ablehnte.",
            "Ich habe Chat, Belege und Referenznummern gesichert.",
        ],
        "ask": [
            "Ist eine vertrauliche Prüfung noch sinnvoll?",
            "Wen soll ich mit Zeitablauf und Nachweisen kontaktieren?",
            "Gibt es einen sinnvollen nächsten Schritt?",
            "Kann jemand still prüfen, ob noch etwas geht?",
        ],
        "mention": [
            " Es lief unter dem Namen {name}.",
            " In meinen Notizen: {domain}.",
            " Aufgetreten als {name}.",
            "",
            "",
        ],
    },
    "es": {
        "open": [
            "Aporté por {channel} con un {payment}.",
            "Empecé en {channel} tras un {payment}.",
            "Todo parecía normal en {channel} después del {payment}.",
        ],
        "mid_imp": [
            "Unos {amount} siguen bloqueados tras freír el retiro y pedir más comisiones.",
            "Cerca de {amount} no llegaron al banco cuando congelaron la solicitud mayor.",
            "Mostraban beneficios, pero retuvieron cerca de {amount} por un nuevo cargo.",
        ],
        "mid": [
            "Los retiros se detuvieron y el chat solo repetía la misma lista.",
            "Un retiro de prueba salió una vez; el real no.",
            "Soporte pedía más verificación sin liberar fondos.",
            "El gestor dejó de responder cuando negué otra comisión.",
            "Conservo chats, recibos e IDs de referencia.",
        ],
        "ask": [
            "¿Conviene aún una revisión confidencial?",
            "¿A quién envío el cronograma y las pruebas?",
            "¿Hay un siguiente paso práctico?",
            "¿Pueden mirar el caso en silencio?",
        ],
        "mention": [
            " Fue bajo el nombre {name}.",
            " Dominio en mis notas: {domain}.",
            " Se presentó como {name}.",
            "",
            "",
        ],
    },
    "it": {
        "open": [
            "Ho versato tramite {channel} con un {payment}.",
            "Inizio su {channel} dopo un {payment}.",
            "Su {channel} sembrava regolare dopo il {payment}.",
        ],
        "mid_imp": [
            "Circa {amount} restano bloccati dopo il blocco del prelievo e nuove commissioni.",
            "Quasi {amount} non sono arrivati in banca quando hanno congelato la richiesta maggiore.",
            "Mostravano profitti, ma trattenevano circa {amount} per un nuovo addebito.",
        ],
        "mid": [
            "I prelievi si sono fermati; la chat ripeteva solo checklist.",
            "Un prelievo test è passato una volta; quello vero no.",
            "Il supporto chiedeva nuove verifiche senza sbloccare.",
            "Il manager ha smesso di rispondere quando ho rifiutato altre fee.",
            "Ho chat, ricevute e ID di riferimento.",
        ],
        "ask": [
            "Ha ancora senso un esame confidenziale?",
            "A chi mando cronologia e prove?",
            "C’è un passo successivo concreto?",
            "Potete guardare il fascicolo in silenzio?",
        ],
        "mention": [
            " Era sotto il nome {name}.",
            " Dominio nei miei appunti: {domain}.",
            " Si presentava come {name}.",
            "",
            "",
        ],
    },
    "fr": {
        "open": [
            "J’ai déposé via {channel} avec un {payment}.",
            "Début sur {channel} après un {payment}.",
            "Sur {channel}, tout paraissait normal après le {payment}.",
        ],
        "mid_imp": [
            "Environ {amount} restent bloqués après le gel du retrait et de nouveaux frais.",
            "Près de {amount} n’ont jamais atteint ma banque une fois la demande majeure gelée.",
            "Ils affichaient des gains, puis retenaient environ {amount} pour un nouveau frais.",
        ],
        "mid": [
            "Les retraits se sont arrêtés ; le chat recyclait la même liste.",
            "Un petit retrait test a marché une fois ; le vrai non.",
            "Le support exigeait de nouvelles étapes sans libérer les fonds.",
            "Le gestionnaire a cessé de répondre quand j’ai refusé d’autres frais.",
            "J’ai conservé chats, reçus et références.",
        ],
        "ask": [
            "Un examen confidentiel vaut-il encore la peine ?",
            "À qui envoyer le calendrier et les preuves ?",
            "Y a-t-il une prochaine étape concrète ?",
            "Pouvez-vous regarder le dossier discrètement ?",
        ],
        "mention": [
            " C’était sous le nom {name}.",
            " Domaine dans mes notes : {domain}.",
            " Présenté comme {name}.",
            "",
            "",
        ],
    },
    "pt": {
        "open": [
            "Depositei via {channel} com um {payment}.",
            "Comecei em {channel} após um {payment}.",
            "No {channel} parecia normal depois do {payment}.",
        ],
        "mid_imp": [
            "Cerca de {amount} continuam presos depois de bloquearem o saque e pedirem mais taxas.",
            "Quase {amount} não chegaram ao banco quando congelaram o pedido maior.",
            "Mostravam lucros, mas reteve cerca de {amount} por uma nova cobrança.",
        ],
        "mid": [
            "Os saques pararam e o chat só repetia a lista.",
            "Um saque teste saiu uma vez; o real não.",
            "O suporte pedia novas verificações sem libertar fundos.",
            "O gestor parou de responder quando recusei outra taxa.",
            "Guardei chats, recibos e IDs de referência.",
        ],
        "ask": [
            "Ainda vale uma análise confidencial?",
            "A quem envio o cronograma e as provas?",
            "Há um próximo passo prático?",
            "Podem olhar o caso em silêncio?",
        ],
        "mention": [
            " Foi sob o nome {name}.",
            " Domínio nas notas: {domain}.",
            " Apresentava-se como {name}.",
            "",
            "",
        ],
    },
    "nl": {
        "open": [
            "Ik stortte via {channel} met een {payment}.",
            "Gestart op {channel} na een {payment}.",
            "Op {channel} leek alles normaal na de {payment}.",
        ],
        "mid_imp": [
            "Ongeveer {amount} zit vast nadat de opname werd geblokkeerd en extra kosten volgden.",
            "Bijna {amount} bereikte mijn bank niet toen het grotere verzoek bevroor.",
            "Ze toonden winst, maar hielden zo’n {amount} achter voor een nieuwe heffing.",
        ],
        "mid": [
            "Opnames stopten; de chat herhaalde dezelfde checklist.",
            "Een testopname lukte één keer; de echte niet.",
            "Support vroeg nieuwe stappen zonder fondsen vrij te geven.",
            "De manager reageerde niet meer toen ik extra fees weigerde.",
            "Ik bewaar chat, bonnen en referentie-IDs.",
        ],
        "ask": [
            "Heeft een vertrouwelijke beoordeling nog zin?",
            "Naar wie stuur ik tijdlijn en bewijs?",
            "Is er een concrete volgende stap?",
            "Kunnen jullie dit stil bekijken?",
        ],
        "mention": [
            " Dit was onder de naam {name}.",
            " Domein in mijn notities: {domain}.",
            " Gepresenteerd als {name}.",
            "",
            "",
        ],
    },
    "pl": {
        "open": [
            "Wpłaciłem przez {channel} jako {payment}.",
            "Start na {channel} po {payment}.",
            "Na {channel} wyglądało to normalnie po {payment}.",
        ],
        "mid_imp": [
            "Około {amount} utknęło po zablokowaniu wypłaty i żądaniu opłat.",
            "Blisko {amount} nie trafiło do banku, gdy zamrożono większy wniosek.",
            "Pokazywali zyski, a zatrzymali około {amount} na nową opłatę.",
        ],
        "mid": [
            "Wypłaty stanęły; czat powtarzał tę samą listę.",
            "Testowa wypłata przeszła raz; właściwa nie.",
            "Support żądał kolejnych weryfikacji bez wypłaty.",
            "Opiekun zamilkł, gdy odmówiłem kolejnej opłaty.",
            "Mam czat, potwierdzenia i numery referencyjne.",
        ],
        "ask": [
            "Czy poufna analiza ma jeszcze sens?",
            "Do kogo wysłać harmonogram i dowody?",
            "Jaki jest praktyczny kolejny krok?",
            "Czy można to przejrzeć po cichu?",
        ],
        "mention": [
            " Szło pod nazwą {name}.",
            " Domena w notatkach: {domain}.",
            " Przedstawiali się jako {name}.",
            "",
            "",
        ],
    },
    "ro": {
        "open": [
            "Am depus prin {channel} cu un {payment}.",
            "Am început pe {channel} după un {payment}.",
            "Pe {channel} părea normal după {payment}.",
        ],
        "mid_imp": [
            "Aproximativ {amount} sunt blocate după ce au oprit retragerea și au cerut taxe noi.",
            "Aproape {amount} nu au ajuns în bancă când au înghețat cererea mai mare.",
            "Arătau profituri, dar au reținut circa {amount} pentru o nouă taxă.",
        ],
        "mid": [
            "Retragerile s-au oprit; chatul repeta aceeași listă.",
            "O retragere test a mers o dată; cea reală nu.",
            "Suportul cerea noi verificări fără eliberare.",
            "Managerul a tăcut când am refuzat altă taxă.",
            "Am chat, chitanțe și ID-uri de referință.",
        ],
        "ask": [
            "Mai are sens o analiză confidențială?",
            "Cui trimit calendarul și dovezile?",
            "Care e următorul pas practic?",
            "Puteți privi dosarul în liniște?",
        ],
        "mention": [
            " A fost sub numele {name}.",
            " Domeniul din notițe: {domain}.",
            " S-au prezentat ca {name}.",
            "",
            "",
        ],
    },
    "tr": {
        "open": [
            "{channel} üzerinden {payment} ile yatırdım.",
            "{payment} sonrası {channel} ile başladım.",
            "{payment} sonrası {channel} önce normal göründü.",
        ],
        "mid_imp": [
            "Çekim engellenip ek ücret istenince yaklaşık {amount} takılı kaldı.",
            "Büyük talep dondurulunca yaklaşık {amount} bankaya hiç geçmedi.",
            "Panel kâr gösteriyordu ama {amount} yeni bir ücret için tutuldu.",
        ],
        "mid": [
            "Çekimler durdu; sohbet aynı listeyi tekrarladı.",
            "Test çekimi bir kez oldu; asıl talep olmadı.",
            "Destek fon bırakmadan yeni doğrulama istedi.",
            "Ek ücreti reddedince yönetici sustu.",
            "Sohbet, makbuz ve referans ID’lerim duruyor.",
        ],
        "ask": [
            "Gizli inceleme hâlâ mantıklı mı?",
            "Zaman çizelgesi ve kanıtı kime göndermeliyim?",
            "Somut sonraki adım var mı?",
            "Dosyaya sessizce bakılabilir mi?",
        ],
        "mention": [
            " Bu {name} adı altındaydı.",
            " Notlarımdaki alan adı: {domain}.",
            " Kendilerini {name} olarak tanıttılar.",
            "",
            "",
        ],
    },
}

BODY_SOFT = {
    "en": {
        "open": [
            "I am trying to confirm I am dealing with the genuine firm, not a lookalike.",
            "Public notes are mixed and I want a quiet read on what I collected.",
            "I still have statements and chat exports from {channel}.",
            "I used {channel} and want the domain/licence claim checked carefully.",
        ],
        "mid": [
            "I am not accusing anyone yet — I need the paperwork sorted first.",
            "The complaint path (firm vs regulator vs counsel) is unclear to me.",
            "I want to avoid sending more funds to the wrong place.",
            "Screenshots and references are organized if someone will review them.",
        ],
        "ask": [
            "Who is the right contact for a confidential check?",
            "Can someone advise the sensible next step?",
            "Is a short consultation appropriate before I escalate?",
            "Where should I send the domain I actually used?",
        ],
        "mention": [
            " The name on my files is {name}.",
            " Domain on file: {domain}.",
            " Presented as {name}.",
            "",
            "",
        ],
    },
}

SUPPORT_HARD = {
    "en": [
        "We’re sorry this happened. If you want a confidential review, contact us with the account timeline, payment method, and any chat or transfer references you still have.",
        "Sorry to hear about the blocked payout. Send what you can on dates, amounts, and the domain you used — we can outline counsel or reporting options quietly.",
        "Thank you for writing. For a confidential look, share how you paid, when withdrawals failed, and any ticket IDs; we will compare that with the public record.",
        "We understand how disruptive a frozen balance is. Contact us with screenshots and a short chronology if you want next-step advice without obligation.",
    ],
    "de": [
        "Es tut uns leid. Für eine vertrauliche Prüfung senden Sie Zeitablauf, Zahlungsweg und vorhandene Chat-/Transfernachweise.",
        "Schade wegen der blockierten Auszahlung. Teilen Sie Daten, Beträge und die genutzte Domain — wir skizzieren ruhig Optionen.",
        "Danke für Ihre Nachricht. Beschreiben Sie Einzahlung, gescheiterte Auszahlung und Ticket-IDs; wir gleichen das mit öffentlichen Quellen ab.",
    ],
    "es": [
        "Lamentamos lo ocurrido. Para una revisión confidencial, envíe cronograma, forma de pago y referencias de chat o transferencias.",
        "Sentimos el retiro bloqueado. Comparta fechas, montos y el dominio usado; podemos esbozar opciones en privado.",
        "Gracias por escribir. Indique cómo pagó, cuándo falló el retiro y cualquier ID de ticket para contrastarlo con el registro público.",
    ],
    "it": [
        "Ci dispiace. Per un esame confidenziale, invii cronologia, metodo di pagamento e riferimenti di chat o bonifici.",
        "Spiace per il prelievo bloccato. Condivida date, importi e dominio usato; indichiamo opzioni in privato.",
        "Grazie per lo scritto. Descriva pagamento, fallimento del prelievo e ID ticket; li confronteremo con le fonti pubbliche.",
    ],
    "fr": [
        "Nous sommes désolés. Pour un examen confidentiel, envoyez calendrier, mode de paiement et références de chat ou virement.",
        "Désolés pour le retrait bloqué. Partagez dates, montants et domaine utilisé — nous pouvons esquisser des options discrètement.",
        "Merci pour votre message. Précisez paiement, échec du retrait et IDs de ticket ; nous les comparerons aux sources publiques.",
    ],
    "pt": [
        "Lamentamos o ocorrido. Para análise confidencial, envie cronograma, forma de pagamento e referências de chat ou transferência.",
        "Lamentamos o saque bloqueado. Partilhe datas, montantes e o domínio usado — podemos delinear opções em privado.",
        "Obrigado pela mensagem. Descreva o pagamento, a falha do saque e IDs de ticket; comparamos com o registo público.",
    ],
    "nl": [
        "Het spijt ons. Voor een vertrouwelijke beoordeling: stuur tijdlijn, betaalwijze en chat-/transferbewijs.",
        "Vervelend dat de opname vastzit. Deel data, bedragen en het gebruikte domein — we schetsen stil opties.",
        "Dank voor uw bericht. Beschrijf storting, mislukte opname en ticket-IDs; we toetsen dat aan openbare bronnen.",
    ],
    "pl": [
        "Przykro nam. Na poufną analizę prosimy o harmonogram, sposób płatności oraz chat/przelewy.",
        "Przykro z powodu blokady wypłaty. Podajcie daty, kwoty i domenę — wskażemy opcje dyskretnie.",
        "Dziękujemy za wiadomość. Opiszcie wpłatę, nieudaną wypłatę i ID zgłoszeń; porównamy z publicznymi źródłami.",
    ],
    "ro": [
        "Ne pare rău. Pentru analiză confidențială, trimiteți calendarul, metoda de plată și referințe chat/transfer.",
        "Ne pare rău pentru retragerea blocată. Trimiteți date, sume și domeniul folosit — schițăm opțiuni în privat.",
        "Mulțumim pentru mesaj. Descrieți plata, eșecul retragerii și ID-urile ticket; le comparăm cu sursele publice.",
    ],
    "tr": [
        "Üzüldük. Gizli inceleme için zaman çizelgesi, ödeme yöntemi ve sohbet/transfer kayıtlarını gönderin.",
        "Engellenen çekim için üzgünüz. Tarih, tutar ve kullanılan alan adını paylaşın — seçenekleri gizlice özetleriz.",
        "Yazınız için teşekkürler. Yatırım, başarısız çekim ve ticket ID’lerini anlatın; kamu kaydıyla karşılaştırırız.",
    ],
}

SUPPORT_SOFT = {
    "en": [
        "Happy to help separate a real platform from lookalikes. Send the domain you used, any licence number shown, and a short timeline for a confidential consult.",
        "We can review quietly whether your paperwork matches the genuine firm. Include URLs, statements, and how you were contacted.",
        "Thanks for reaching out. Share the exact site/app name and what you still have on file — we will advise on firm, regulator, or counsel paths.",
    ],
}


def stable_int(s: str, mod: int) -> int:
    if mod <= 0:
        return 0
    return int(hashlib.sha256(s.encode("utf-8")).hexdigest()[:8], 16) % mod


def pick(seq, key: str):
    return seq[stable_int(key, len(seq))]


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
    markers = (
        "$", "€", "£", "USD", "EUR", "GBP", "Super", "retirement", "erhebliche",
        "substantial", "significant", "importante", "élevée", "aanzienlijk",
        "znaczącą", "önemli", "250,000", "100,000", "50,000", "about $", "roughly €",
        "close to $", "nearly €", "circa ", "aproximadamente", "ongeveer", "environ",
        "etwa ", "yaklaşık", "aproximativ", "cerca de", "quasi ",
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
        row.pop("source", None)
        if is_important_loss(row) and not replied and row.get("askHelp"):
            replied = True
            row["importantLoss"] = True
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
                    "text": pick(SUPPORT_HARD.get(lang) or SUPPORT_HARD["en"], row.get("slug", "") + ":sup"),
                    "ctaLabel": CTA.get(lang, CTA["en"]),
                    "ctaHref": "../index.html#contact",
                }
        else:
            row.pop("support", None)
        out.append(row)
    return out


def load_overrides() -> dict:
    """Keep only hand-curated slugs (or items marked curated=true)."""
    if not COMMENTS_JS.exists():
        return {}
    db = load_js_array(COMMENTS_JS, "window.SBL_COMMENTS")
    keep = {}
    for slug, items in db.items():
        marked = slug in CURATED_SLUGS or any(
            isinstance(c, dict) and c.get("curated") for c in (items or [])
        )
        if marked:
            keep[slug] = sanitize_override(items)
    return keep


def pick_lang(country: str, slug: str, index: int) -> str:
    if index == 0 and slug in SLUG_LANG_HINTS:
        return SLUG_LANG_HINTS[slug]
    return COUNTRY_LANG.get(country, "en")


def person_for(slug: str, index: int) -> tuple[str, str]:
    first = pick(FIRST_NAMES, f"{slug}:fn:{index}")
    # shift last name independently so pairs rarely repeat as a full identity
    last = pick(LAST_NAMES, f"{slug}:ln:{index}:{stable_int(slug, 97)}")
    # avoid identical first+last collisions within a broker
    if index:
        last = pick(LAST_NAMES, f"{slug}:ln2:{index}:{last}")
    name = f"{first} {last}"
    initials = (first[0] + last[0]).upper()
    return name, initials


def bank(lang: str, soft: bool):
    if soft:
        titles = TITLE_SOFT.get(lang) or TITLE_SOFT["en"]
        bodies = BODY_SOFT.get(lang) or BODY_SOFT["en"]
    else:
        titles = TITLE_HARD.get(lang) or TITLE_HARD["en"]
        # fall back body parts to EN if lang incomplete
        bodies = BODY_HARD.get(lang) or BODY_HARD["en"]
    return titles, bodies


def short_label(company: str, domain: str, slug: str) -> str:
    """Compact firm cue for titles — keeps comments company-specific."""
    if domain:
        host = re.sub(r"^www\.", "", domain.strip().lower())
        if 3 < len(host) <= 28 and " " not in host:
            return host
    words = re.findall(r"[A-Za-z0-9]+", company or "")
    if words:
        label = " ".join(words[:3])
        if len(label) > 28:
            label = words[0][:28]
        return label
    return (slug or "profile")[:24]


def compose_text(
    slug: str,
    index: int,
    lang: str,
    soft: bool,
    important: bool,
    company: str,
    domain: str,
) -> tuple[str, str]:
    titles, bodies = bank(lang, soft)
    base_title = pick(titles, f"{slug}:title:{index}:{lang}")
    channel = pick(CHANNELS.get(lang) or CHANNELS["en"], f"{slug}:ch:{index}")
    payment = pick(PAYMENTS.get(lang) or PAYMENTS["en"], f"{slug}:pay:{index}")
    amount = pick(AMOUNTS, f"{slug}:amt:{index}")
    label = short_label(company, domain, slug)

    # Title always carries a unique firm/detail cue (avoids identical headlines sitewide)
    if soft:
        soft_forms = [
            f"{base_title} — {label}",
            f"{label}: {base_title}",
            f"{base_title} ({label})",
        ]
        title = pick(soft_forms, f"{slug}:tf:{index}")
    elif important:
        imp_forms = [
            f"{base_title} — {amount} on {label}",
            f"{label}: {base_title} ({amount})",
            f"{amount} · {base_title}",
            f"{base_title} ({label})",
        ]
        title = pick(imp_forms, f"{slug}:tf:{index}")
    else:
        hard_forms = [
            f"{base_title} — {label}",
            f"{label}: {base_title}",
            f"{base_title} · {payment}",
            f"{base_title} ({label})",
            f"{base_title} / {label}",
        ]
        title = pick(hard_forms, f"{slug}:tf:{index}")

    open_s = pick(bodies["open"], f"{slug}:open:{index}").format(
        channel=channel, payment=payment, name=company, domain=domain or company
    )
    if soft:
        mid_s = pick(bodies["mid"], f"{slug}:mid:{index}")
    elif important:
        mid_s = pick(bodies["mid_imp"], f"{slug}:midi:{index}").format(amount=amount)
    else:
        mid_s = pick(bodies["mid"], f"{slug}:mid:{index}")
    ask_s = pick(bodies["ask"], f"{slug}:ask:{index}")
    mention = pick(bodies.get("mention") or [""], f"{slug}:men:{index}").format(
        name=company, domain=domain or company
    )
    # Always fold firm identity into the body once (even if mention slot empty)
    if company and company.lower() not in (open_s + mid_s + mention).lower():
        if lang == "en":
            mention = (mention or "") + f" Profile concerned: {company}."
        elif not mention:
            mention = f" ({company})"

    order = stable_int(f"{slug}:ord:{index}", 4)
    if order == 0:
        text = f"{open_s}{mention} {mid_s} {ask_s}"
    elif order == 1:
        text = f"{open_s} {mid_s}{mention} {ask_s}"
    elif order == 2:
        text = f"{mid_s} {open_s}{mention} {ask_s}"
    else:
        text = f"{open_s} {ask_s} {mid_s}{mention}"
    text = re.sub(r"\s+", " ", text).strip()
    return title, text


def support_text(slug: str, index: int, lang: str, soft: bool) -> str:
    if soft:
        pool = SUPPORT_SOFT.get(lang) or SUPPORT_SOFT["en"]
    else:
        pool = SUPPORT_HARD.get(lang) or SUPPORT_HARD["en"]
    return pick(pool, f"{slug}:support:{index}:{lang}")


def official_domain(b: dict) -> str:
    return (
        b.get("officialDomain")
        or b.get("domain")
        or ((b.get("trustpilot") or {}).get("domain") if isinstance(b.get("trustpilot"), dict) else "")
        or ""
    )


def build_for_broker(b: dict, today: date, used: set[tuple[str, str]]) -> list[dict]:
    slug = b["slug"]
    company = b.get("name") or slug
    domain = official_domain(b)
    tier = (b.get("tier") or "scam").lower()
    soft = tier in ("legit", "clone") or (b.get("risk") == "medium" and tier != "scam")
    big_scam = (not soft) and (b.get("risk") == "high" or tier == "scam")

    if soft:
        n_help = 1
    elif big_scam:
        n_help = 3
    else:
        n_help = 2

    base_ago = 12 + stable_int(slug + ":base", 50)
    comments: list[dict] = []

    for i in range(n_help):
        country = COUNTRY_POOL[
            (stable_int(slug + ":c" + str(i), len(COUNTRY_POOL)) + i * 7) % len(COUNTRY_POOL)
        ]
        lang = pick_lang(country, slug, i)
        # Prefer EN body banks when lang packs are thin for soft non-EN
        if soft and lang not in BODY_SOFT:
            # keep title lang if available, body from EN soft
            pass
        important = (not soft) and i == 0

        use_lang = "en" if soft and lang not in BODY_SOFT else lang
        title, text = "", ""
        for attempt in range(24):
            seed = slug if attempt == 0 else f"{slug}:{i}:a{attempt}"
            title, text = compose_text(
                seed,
                i + attempt,
                use_lang,
                soft,
                important,
                company,
                domain,
            )
            sig = (title.strip().lower(), text.strip().lower())
            if sig not in used:
                used.add(sig)
                break
        else:
            text = f"{text} Ref {stable_int(slug + str(i), 100000):05d}."
            used.add((title.strip().lower(), text.strip().lower()))
        lang = use_lang

        name, initials = person_for(slug, i)
        gap = 9 + stable_int(slug + ":g" + str(i), 41)
        d = today - timedelta(days=base_ago + i * gap + stable_int(slug + f":d{i}", 6))
        if d > today:
            d = today - timedelta(days=2 + i)

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
        if important:
            reply_delay = 1 + stable_int(slug + ":r" + str(i), 3)
            rd = min(d + timedelta(days=reply_delay), today)
            item["support"] = {
                "date": rd.isoformat(),
                "text": support_text(slug, i, lang, soft),
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
        help="Regenerate all non-curated slugs (ignores --new-only)",
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
    used: set[tuple[str, str]] = set()
    generated = 0
    kept = 0

    # Reserve curated signatures so generators do not collide with them
    for slug, items in overrides.items():
        for c in items or []:
            used.add(((c.get("title") or "").strip().lower(), (c.get("text") or "").strip().lower()))

    for b in brokers:
        slug = b["slug"]
        if slug in overrides:
            out[slug] = overrides[slug]
            kept += 1
            continue
        if args.new_only and not args.force and slug in existing and existing[slug]:
            out[slug] = existing[slug]
            for c in existing[slug]:
                used.add(((c.get("title") or "").strip().lower(), (c.get("text") or "").strip().lower()))
            kept += 1
            continue
        out[slug] = build_for_broker(b, today, used)
        generated += 1

    text = (
        "/* Auto-generated by tools/rebuild_comments.py — unique composed comments per slug */\n"
        "window.SBL_COMMENTS = "
        + json.dumps(out, ensure_ascii=False, indent=2)
        + ";\n"
    )
    COMMENTS_JS.write_text(text, encoding="utf-8")

    # Uniqueness report
    bodies = {}
    for slug, items in out.items():
        for c in items or []:
            key = ((c.get("title") or ""), (c.get("text") or ""))
            bodies.setdefault(key, set()).add(slug)
    reused = sum(1 for slugs in bodies.values() if len(slugs) > 1)
    langs = {}
    for items in out.values():
        for c in items:
            if c.get("askHelp"):
                langs[c.get("lang", "en")] = langs.get(c.get("lang", "en"), 0) + 1
    print(f"Wrote comments for {len(out)} slugs → {COMMENTS_JS}")
    print(f"generated={generated} kept={kept} curated_overrides={len(overrides)}")
    print(f"unique title+text pairs={len(bodies)} reused_across_slugs={reused}")
    print(f"Help comment langs: {langs}")


if __name__ == "__main__":
    main()
