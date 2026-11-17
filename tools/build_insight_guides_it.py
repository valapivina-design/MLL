#!/usr/bin/env python3
"""Build Italian keyword-slug insight guides under /it/insights/.

Italian victim-intent funnel: "truffa online" is the broad anchor term
(60x bigger than specific terms), with recupero/denuncia/avvocato pages
as supporting intent pages.

  python3 tools/build_insight_guides_it.py
"""
from __future__ import annotations

import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "it" / "insights"
SITE = "https://mikelevylaw.com"
UPDATED = "17 novembre 2026"
DATE_ISO = "2026-11-17"

GUIDES = [
    {
        "slug": "truffa-online",
        "kicker": f"Truffa online · Aggiornato il {UPDATED}",
        "h1": "Truffa online: cosa fare, a chi rivolgersi e come denunciare",
        "title": "Truffa online: cosa fare e a chi rivolgersi | Mike Levy Law",
        "desc": "Truffa online: cosa fare subito, a chi rivolgersi (Polizia Postale, Carabinieri), come funziona la denuncia e il reato di truffa (art. 640 c.p.).",
        "keywords": "truffa online, truffa online cosa fare, truffa online a chi rivolgersi, denuncia truffa online, denuncia truffa polizia postale, denuncia truffa online carabinieri, truffa online reato, truffa online codice penale, art. 640 cp",
        "lead": "Vittima di una truffa online? Le prime due settimane decidono quali opzioni restano aperte: bloccare i pagamenti, conservare le prove, denunciare al canale giusto. Questa pagina riunisce cosa fare, a chi rivolgersi e come funziona il reato di truffa (art. 640 c.p.).",
        "sections": [
            (
                "Cosa fare subito",
                "<ol>"
                "<li>Bloccare ogni altro pagamento — incluse «tasse», «commissioni di sblocco» o «rimborsi anticipati».</li>"
                "<li>Conservare chat, email, estratti conto, domini esatti e numeri di riferimento.</li>"
                "<li>Contattare la banca o l'emittente della carta per richiamo bonifico o chargeback.</li>"
                "<li>Presentare denuncia (Polizia Postale o Carabinieri) con la documentazione raccolta.</li>"
                "<li>Per perdite rilevanti: valutazione riservata con un legale.</li>"
                "</ol>",
            ),
            (
                "A chi rivolgersi",
                "<ul>"
                "<li><strong>Polizia Postale (CNAIPIC / commissariato online):</strong> canale specializzato per truffe su internet; denuncia possibile anche online.</li>"
                "<li><strong>Carabinieri:</strong> qualsiasi stazione riceve la denuncia per truffa (art. 640 c.p.).</li>"
                "<li><strong>CONSOB:</strong> segnalazione per piattaforme di trading non autorizzate — non restituisce soldi, ma può oscurare il sito.</li>"
                "<li><strong>Banca / emittente carta:</strong> in parallelo, con scadenze proprie per richiami e chargeback.</li>"
                "</ul>",
            ),
            (
                "Il reato: art. 640 c.p.",
                "<p>La truffa è punita dall'art. 640 del codice penale: artifizi o raggiri per procurarsi un ingiusto profitto con danno altrui. La denuncia non restituisce direttamente il denaro, ma apre il canale investigativo (sequestri, richieste a banche ed exchange) e costituisce la base per la costituzione di parte civile nel processo.</p>",
            ),
        ],
        "faqs": [
            (
                "Truffa online: cosa fare per prima cosa?",
                "Bloccare i pagamenti e conservare le prove, in quest'ordine. Ogni ulteriore «commissione» peggiora solo il danno; le prove servono a banca, denuncia e legale.",
            ),
            (
                "Truffa online: a chi rivolgersi per la denuncia?",
                "Polizia Postale (anche online) o Carabinieri. Se la truffa riguarda investimenti o trading, aggiunga una segnalazione alla CONSOB.",
            ),
            (
                "Con la denuncia recupero i soldi?",
                "Non direttamente. Il recupero passa da chargeback, richiamo del bonifico, sequestro in sede penale o azione civile. La denuncia è il presupposto di tutto questo.",
            ),
        ],
        "related": [
            ("../recuperare-soldi-truffa/", "Recuperare soldi dalla truffa"),
            ("../avvocato-truffa-online/", "Avvocato per truffa online"),
            ("../truffa-trading-online/", "Truffa trading online"),
        ],
        "source": "insights-it-truffa-online",
    },
    {
        "slug": "recuperare-soldi-truffa",
        "kicker": f"Recupero fondi · Aggiornato il {UPDATED}",
        "h1": "Recuperare soldi truffati: bonifico, PostePay, PayPal e carta — i canali giusti",
        "title": "Recuperare soldi truffa online: bonifico, PostePay, PayPal | Mike Levy Law",
        "desc": "Recuperare soldi truffati online: richiamo del bonifico (anche istantaneo), chargeback su carta e PostePay, reclamo PayPal — il canale dipende da come ha pagato.",
        "keywords": "recuperare soldi truffa online, recuperare soldi truffati, recuperare soldi truffa bonifico, recuperare soldi truffa postepay, recuperare soldi truffa paypal, recuperare soldi truffa carta di credito, come recuperare soldi truffati con bonifico istantaneo, recupero fondi investimento, chargeback investimento, migliori società di recupero fondi",
        "lead": "Come recuperare soldi truffati dipende quasi interamente da <strong>come ha pagato</strong>: bonifico, PostePay, PayPal o carta seguono regole e scadenze diverse. La sequenza giusta fa la differenza — e il tempo è il fattore più costoso.",
        "sections": [
            (
                "Bonifico (anche istantaneo): il richiamo",
                "<p>Chieda subito alla sua banca il <strong>richiamo del bonifico</strong> e l'escalation antifrode — idealmente lo stesso giorno lavorativo. Anche per i bonifici istantanei, teoricamente irrevocabili, il tentativo immediato conta: se i fondi sono ancora presso la banca ricevente, esistono possibilità di blocco. Conservi il riferimento del richiamo.</p>",
            ),
            (
                "Carta di credito e PostePay: chargeback",
                "<p>Per pagamenti con carta (inclusa PostePay Evolution) esiste il chargeback tramite l'emittente: finestre brevi, documentazione decisiva (dominio, screenshot del prelievo rifiutato, chat). Non aspetti il «supporto» della piattaforma mentre la finestra si chiude.</p>",
            ),
            (
                "PayPal e gli altri canali",
                "<p>PayPal ha un centro risoluzioni proprio con scadenze per la contestazione. Per criptovalute non esiste storno, ma la tracciatura fino agli exchange con KYC può aprire canali formali — veda <a href=\"../truffa-criptovalute/\">truffa criptovalute</a>. Attenzione alle «migliori società di recupero fondi» che si propongono dopo la perdita: garanzie più anticipo in cripto sono lo schema della truffa di recupero.</p>",
            ),
        ],
        "faqs": [
            (
                "Posso recuperare soldi truffati con bonifico istantaneo?",
                "Il bonifico istantaneo è tecnicamente irrevocabile, ma un richiamo immediato può bloccare i fondi se non ancora movimentati dal ricevente. Agisca lo stesso giorno e conservi il riferimento; in parallelo denuncia e valutazione legale.",
            ),
            (
                "Come recuperare soldi dalla truffa con PostePay o carta?",
                "Contesti l'addebito all'emittente (chargeback) entro le scadenze del circuito, allegando dominio usato, chat e rifiuto del prelievo. Prima si agisce, meglio è.",
            ),
            (
                "Le società di recupero fondi sono affidabili?",
                "Alcuni servizi investigativi e legali sono legittimi. Chi garantisce il recupero e chiede un anticipo in criptovalute per «sbloccare» il denaro sta applicando lo schema della recovery scam: non paghi.",
            ),
        ],
        "related": [
            ("../truffa-online/", "Truffa online: cosa fare"),
            ("../avvocato-truffa-online/", "Avvocato per truffa online"),
            ("../truffa-criptovalute/", "Truffa criptovalute"),
        ],
        "source": "insights-it-recuperare-soldi-truffa",
    },
    {
        "slug": "truffa-trading-online",
        "kicker": f"Trading · Aggiornato il {UPDATED}",
        "h1": "Truffa trading online: broker truffaldini, i 250 euro e la CONSOB",
        "title": "Truffa trading online: broker truffa e recupero | Mike Levy Law",
        "desc": "Truffa trading online: come riconoscere i broker truffaldini, lo schema dei 250 euro, la segnalazione CONSOB e come recuperare soldi dal trading.",
        "keywords": "truffa trading online, broker truffa, lista broker truffaldini, broker truffaldini, truffa trading online 250 euro, truffa trading recuperare soldi, broker truffa consob, truffa forex, broker falsi, truffa trading whatsapp, piattaforma di trading falsa, app trading falsa screenshot",
        "lead": "La truffa di trading online ha un copione: 250 euro iniziali, «guadagni» sullo schermo, poi il blocco del prelievo. Qui trova i segnali, il ruolo della CONSOB e i canali reali per recuperare i soldi.",
        "sections": [
            (
                "Lo schema dei 250 euro",
                "<p>Pubblicità su social o articoli falsi con personaggi famosi, iscrizione con <strong>250 euro</strong>, un «account manager» su telefono o WhatsApp, piccoli profitti visibili, pressione per versare di più. Al primo prelievo: «tasse», «verifiche» o silenzio. Gli screenshot della app o della dashboard falsa, con data, sono prova — li conservi prima che l'account venga «chiuso».</p>",
            ),
            (
                "Lista broker truffaldini e CONSOB",
                "<p>La CONSOB pubblica le <strong>liste nere</strong> e oscura i siti non autorizzati; le liste internazionali (FCA, IOSCO I-SCAN) completano il quadro. Verifichi sempre il <strong>dominio esatto</strong> nel registro, non il nome in pubblicità: i cloni copiano marchi autorizzati. La segnalazione CONSOB non restituisce i soldi, ma documenta e oscura.</p>",
            ),
            (
                "Recuperare soldi dalla truffa trading",
                "<ol>"
                "<li>Stop pagamenti, incluse «tasse sul prelievo».</li>"
                "<li>Carta: chargeback immediato; bonifico: richiamo in banca.</li>"
                "<li>Denuncia Polizia Postale o Carabinieri + segnalazione CONSOB.</li>"
                "<li>Perdite rilevanti: <a href=\"../avvocato-truffa-online/\">valutazione legale riservata</a>.</li>"
                "</ol>"
                "<p>Se il contatto è nato su WhatsApp/Telegram, esporti le chat prima di bloccare: sono parte centrale del fascicolo.</p>",
            ),
        ],
        "faqs": [
            (
                "Come riconosco un broker truffaldino?",
                "Tre controlli in due minuti: dominio esatto nel registro CONSOB/FCA, beneficiario del pagamento (società o privato estero?), lista nera. Promesse di rendimento garantito e bonus che blocca il prelievo sono segnali di stop.",
            ),
            (
                "Ho investito solo 250 euro: vale la pena denunciare?",
                "Sì: la denuncia costa poco e alimenta indagini su scala. Il recupero economico diretto su piccoli importi è difficile, ma la denuncia documenta il caso.",
            ),
            (
                "Truffa trading via WhatsApp: cosa conservo?",
                "Chat esportate, numeri di telefono, nomi dei «consulenti», dominio della piattaforma, coordinate di pagamento. Non cancelli i gruppi prima dell'esportazione.",
            ),
        ],
        "related": [
            ("../recuperare-soldi-truffa/", "Recuperare soldi truffati"),
            ("../problemi-prelievo-broker/", "Problemi di prelievo broker"),
            ("../truffa-online/", "Truffa online: cosa fare"),
        ],
        "source": "insights-it-truffa-trading-online",
    },
    {
        "slug": "truffa-criptovalute",
        "kicker": f"Criptovalute · Aggiornato il {UPDATED}",
        "h1": "Truffa criptovalute e bitcoin: recupero, prelievi bloccati e a chi rivolgersi",
        "title": "Truffa criptovalute / bitcoin: cosa fare | Mike Levy Law",
        "desc": "Truffa criptovalute: come recuperare criptovalute, cosa fare se il prelievo è bloccato (Binance, Coinbase), a chi rivolgersi e il ruolo dell'avvocato.",
        "keywords": "truffa criptovalute, truffa bitcoin, truffa criptovalute a chi rivolgersi, come recuperare criptovalute, recuperare criptovalute rubate, avvocato criptovalute, avvocato esperto criptovalute, prelievo bloccato, binance prelievo bloccato, coinbase prelievo bloccato, truffa investimenti bitcoin",
        "lead": "Nelle truffe in criptovalute non esiste storno — ma la blockchain è pubblica. Se le monete arrivano a un exchange con KYC, si aprono canali formali. E se il «prelievo bloccato» riguarda Binance o Coinbase, la prima verifica è se sta usando davvero l'exchange o un clone.",
        "sections": [
            (
                "Come recuperare criptovalute: cosa è realistico",
                "<p>Non esiste chargeback sulle criptovalute. Esiste la tracciatura: ogni transazione è pubblica e spesso conduce a exchange con obblighi KYC. Su quei punti possono innestarsi richieste formali di autorità e legale. Successi pieni sono rari; successi parziali dipendono dal percorso dei fondi e dalla velocità.</p>",
            ),
            (
                "«Prelievo bloccato» su Binance o Coinbase: clone o exchange vero?",
                "<p>Molte vittime cercano «binance prelievo bloccato» dopo aver usato una piattaforma che <em>somigliava</em> a Binance. Verifichi: dominio esatto, app store ufficiale, log di accesso. Se il «supporto» chiede una tassa per sbloccare il prelievo, non è l'exchange vero — è lo schema della truffa. Conservi screenshot e URL esatti.</p>",
            ),
            (
                "A chi rivolgersi",
                "<ol>"
                "<li>Polizia Postale o Carabinieri — denuncia con hash delle transazioni e indirizzi wallet.</li>"
                "<li>Exchange reale (se i fondi lo hanno toccato) — tramite i canali antifrode.</li>"
                "<li><a href=\"../avvocato-truffa-online/\">Avvocato esperto in criptovalute</a> — tracciatura, richieste formali, parte civile.</li>"
                "</ol>",
            ),
        ],
        "faqs": [
            (
                "Come recuperare criptovalute rubate o truffate?",
                "Attraverso tracciatura fino a exchange regolamentati, denuncia con hash e indirizzi, ed eventuali azioni civili contro soggetti identificabili. Nessuno può garantire il recupero; chi lo garantisce è un rischio.",
            ),
            (
                "Il prelievo è bloccato su Binance/Coinbase: che faccio?",
                "Verifichi innanzitutto di essere sul sito/app ufficiale. Se sì, apra un ticket ufficiale e documenti. Se il «blocco» arriva con richiesta di pagare una commissione di sblocco, è un clone: stop pagamenti e denuncia.",
            ),
            (
                "Truffa criptovalute: a chi rivolgersi in Italia?",
                "Polizia Postale (anche online) o Carabinieri per la denuncia; CONSOB se la truffa è presentata come investimento; un avvocato per tracciatura e strategia quando l'importo è rilevante.",
            ),
        ],
        "related": [
            ("../recuperare-soldi-truffa/", "Recuperare soldi truffati"),
            ("../avvocato-truffa-online/", "Avvocato truffa online"),
            ("../truffa-romance/", "Truffa romantica e crypto"),
        ],
        "source": "insights-it-truffa-criptovalute",
    },
    {
        "slug": "avvocato-truffa-online",
        "kicker": f"Avvocato · Aggiornato il {UPDATED}",
        "h1": "Avvocato truffa online: quando serve, cosa fa, cosa costa",
        "title": "Avvocato truffa online / trading / criptovalute | Mike Levy Law",
        "desc": "Avvocato truffa online: quando conviene, cosa fa un avvocato per truffa trading e criptovalute, dalla denuncia alla parte civile — senza promesse di recupero.",
        "keywords": "avvocato truffa online, avvocato truffa trading, avvocato criptovalute, avvocato esperto criptovalute, truffa trading online a chi rivolgersi, avvocato truffa investimenti",
        "lead": "Dopo una truffa online, un avvocato serve a tre cose: strutturare le prove, scegliere i canali giusti nell'ordine giusto, e dirle con franchezza se il gioco vale la candela. Niente promesse di recupero — metodo.",
        "sections": [
            (
                "Cosa fa concretamente l'avvocato",
                "<ul>"
                "<li>Ricostruisce pagamenti, domini e controparti (originale o clone)</li>"
                "<li>Coordina chargeback, richiamo bonifico e denuncia senza bruciare scadenze</li>"
                "<li>Per criptovalute: tracciatura e richieste formali agli exchange</li>"
                "<li>Valuta la costituzione di parte civile e le azioni civili</li>"
                "<li>Confronta il suo fascicolo con segnalazioni e liste pubbliche (CONSOB, IOSCO)</li>"
                "</ul>",
            ),
            (
                "Quando conviene",
                "<p>Per importi piccoli spesso bastano banca e denuncia. Con perdite a cinque-sei cifre, pagamenti misti (carta + bonifico + cripto) o controparti internazionali, la struttura legale paga: evita errori di sequenza e identifica soggetti effettivamente perseguibili.</p>",
            ),
            (
                "Costi e primo passo",
                "<p>I costi dipendono da valore e complessità. Il primo passo è una valutazione riservata dei documenti: chiarisce se esistono canali economici prima di impegnare spese maggiori. Diffidi di chi promette il recupero garantito — avvocato o meno.</p>",
            ),
        ],
        "faqs": [
            (
                "Serve davvero un avvocato per una truffa online?",
                "Per piccoli importi, spesso no. Per perdite rilevanti o casi complessi sì: chargeback, denuncia e azioni civili hanno scadenze e presupposti diversi, e l'ordine conta.",
            ),
            (
                "Quanto costa un avvocato per truffa trading o criptovalute?",
                "Dipende dal valore e dal lavoro necessario. Una valutazione iniziale riservata serve proprio a capire se l'impegno economico è proporzionato al recupero realistico.",
            ),
            (
                "L'avvocato può garantire il recupero?",
                "No — nessuno può. Un legale serio migliora struttura, tempi e destinazione dei passaggi; le garanzie appartengono alle truffe di recupero.",
            ),
        ],
        "related": [
            ("../truffa-online/", "Truffa online: cosa fare"),
            ("../recuperare-soldi-truffa/", "Recuperare soldi truffati"),
            ("../truffa-criptovalute/", "Truffa criptovalute"),
        ],
        "source": "insights-it-avvocato-truffa-online",
    },
    {
        "slug": "problemi-prelievo-broker",
        "kicker": f"Prelievi · Aggiornato il {UPDATED}",
        "h1": "Problemi prelievo broker: perché il broker non paga e cosa fare",
        "title": "Problemi prelievo broker: broker non paga? | Mike Levy Law",
        "desc": "Problemi prelievo broker: perché il broker trattiene i fondi, prelievo bloccato, commissioni nascoste sul prelievo — schemi, scadenze e prossimi passi.",
        "keywords": "problemi prelievo broker, broker non paga, perché il mio broker trattiene i fondi, prelievo bloccato broker, commissioni nascoste prelievo, broker non regolamentati italia, come riconoscere un broker truffaldino",
        "lead": "Prelievo «in lavorazione» da settimane, poi nuove condizioni. Un problema di prelievo dal broker è spesso il primo segnale concreto che qualcosa non va. Le prossime due settimane decidono quali opzioni restano.",
        "sections": [
            (
                "Perché i prelievi falliscono davvero",
                "<p>Ritardi operativi esistono. Conta lo <strong>schema</strong>: una spiegazione datata con bonifico tracciabile è un conto; scuse che cambiano — nuove «tasse», «commissioni di sblocco», «verifiche compliance» o silenzio dopo un piccolo prelievo di prova — un altro. Le «commissioni nascoste sul prelievo» sono il segnale più tipico: nessun broker serio chiede denaro nuovo per restituire il suo.</p>",
            ),
            (
                "Cosa fare nei primi 14 giorni",
                "<ol>"
                "<li>Nessun altro pagamento — né tassa, né sblocco, né commissione.</li>"
                "<li>Richieda il prelievo per iscritto e conservi il rifiuto.</li>"
                "<li>Esporti chat, email, estratti conto e il dominio esatto.</li>"
                "<li>Banca/emittente carta: richiamo o chargeback con le scadenze.</li>"
                "<li>Verifichi il dominio nei registri CONSOB/FCA: originale o clone?</li>"
                "</ol>",
            ),
            (
                "Broker non regolamentati in Italia",
                "<p>Se il dominio non compare in nessun registro (CONSOB, FCA, CySEC con passaporto), il broker non è autorizzato in Italia — e le tutele nazionali (arbitro ACF) non si applicano. Restano chargeback, richiamo, denuncia e valutazione legale su misura.</p>",
            ),
        ],
        "faqs": [
            (
                "Perché il mio broker trattiene i fondi?",
                "Se alle richieste seguono nuove commissioni o condizioni mutevoli, è lo schema del blocco prelievo: stop pagamenti, prove al sicuro, canali bancari e denuncia in parallelo.",
            ),
            (
                "Il broker chiede una commissione per sbloccare il prelievo: pago?",
                "No. Le commissioni legittime vengono detratte dal saldo. La richiesta di un pagamento nuovo per «sbloccare» è Vorschuss — schema da truffa.",
            ),
            (
                "Come riconosco un broker truffaldino prima di depositare?",
                "Dominio esatto nel registro CONSOB, beneficiario del pagamento coerente con la società, assenza di promesse di rendimento garantito, nessun bonus che vincola il prelievo. Due minuti di verifica evitano mesi di recupero.",
            ),
        ],
        "related": [
            ("../truffa-trading-online/", "Truffa trading online"),
            ("../recuperare-soldi-truffa/", "Recuperare soldi truffati"),
            ("../avvocato-truffa-online/", "Avvocato truffa online"),
        ],
        "source": "insights-it-problemi-prelievo-broker",
    },
    {
        "slug": "truffa-romance",
        "kicker": f"Romance scam · Aggiornato il {UPDATED}",
        "h1": "Truffa romantica e crypto: come funziona e come uscirne",
        "title": "Truffa romantica crypto (romance scam): spiegazione | Mike Levy Law",
        "desc": "Truffa romantica: come funziona il romance scam che finisce su piattaforme crypto finte, come riconoscerlo e come recuperare da una truffa romance.",
        "keywords": "truffa romantica, truffa romantica crypto, truffa romance scam spiegazione, come recuperare da truffa romance, romance scam crypto, truffa sentimentale bitcoin",
        "lead": "La truffa romantica («romance scam») inizia con una relazione e finisce su una piattaforma di investimento finta — spesso crypto. Riconoscerla è difficile perché il meccanismo è emotivo, non tecnico. Uscirne richiede freddezza: stop pagamenti, prove, canali giusti.",
        "sections": [
            (
                "Spiegazione: il copione del romance scam",
                "<p>Contatto su app di incontri o social, settimane di fiducia, poi il «consiglio»: una piattaforma di trading crypto «esclusiva». Primi prelievi piccoli che funzionano, importi crescenti, poi il blocco. Il partner romantico e la piattaforma sono la stessa organizzazione — lo schema è noto come <em>pig butchering</em>.</p>",
            ),
            (
                "Segnali che è una truffa romance",
                "<ul>"
                "<li>Mai incontrato di persona; videochiamate sempre rinviate o «rotte».</li>"
                "<li>Propone investimenti o una piattaforma che «usa anche lui/lei».</li>"
                "<li>Urgenza emotiva: emergenze, opportunità a scadenza, segreti da custodire.</li>"
                "<li>Al prelievo: tasse o commissioni da pagare prima.</li>"
                "</ul>",
            ),
            (
                "Come recuperare da una truffa romance",
                "<ol>"
                "<li>Stop pagamenti e nessun confronto emotivo: documenti tutto (chat esportate, foto, profili).</li>"
                "<li>Banca/carta: chargeback o richiamo; crypto: hash e indirizzi.</li>"
                "<li>Denuncia a Polizia Postale o Carabinieri — il reato è truffa (art. 640 c.p.).</li>"
                "<li>Perdite rilevanti: valutazione legale riservata, anche per la tracciatura crypto.</li>"
                "</ol>"
                "<p>Nessuna vergogna: lo schema funziona su professionisti esatti allo stesso modo. Serve solo la sequenza giusta.</p>",
            ),
        ],
        "faqs": [
            (
                "Come funziona la truffa romantica crypto?",
                "Relazione costruita per settimane, poi la piattaforma d'investimento consigliata dal partner: profitti finti sullo schermo, blocco al prelievo, richiesta di «tasse». Partner e piattaforma sono lo stesso gruppo.",
            ),
            (
                "Posso recuperare i soldi di una truffa romance?",
                "Dipende dal canale di pagamento: chargeback per carta, richiamo per bonifico, tracciatura per crypto fino agli exchange. La denuncia con chat e prove è il presupposto. Garantire il recupero non si può.",
            ),
            (
                "Devo denunciare anche se mi vergogno?",
                "Sì. La denuncia è riservata e alimenta indagini su organizzazioni internazionali; le prove emotive (chat, promesse) sono esattamente ciò che serve agli investigatori.",
            ),
        ],
        "related": [
            ("../truffa-criptovalute/", "Truffa criptovalute"),
            ("../recuperare-soldi-truffa/", "Recuperare soldi truffati"),
            ("../truffa-online/", "Truffa online: cosa fare"),
        ],
        "source": "insights-it-truffa-romance",
    },
]

HUB_CARDS = [
    ("truffa-online/", "Ancora · Priorità", "Truffa online", "Cosa fare, a chi rivolgersi, denuncia (Polizia Postale / Carabinieri) e art. 640 c.p.", "truffa online · cosa fare · a chi rivolgersi · denuncia"),
    ("recuperare-soldi-truffa/", "Recupero · Priorità", "Recuperare soldi truffati", "Bonifico (anche istantaneo), PostePay, PayPal, carta: il canale giusto per come ha pagato.", "recuperare soldi truffa · bonifico · postepay · paypal · chargeback"),
    ("truffa-trading-online/", "Trading · Priorità", "Truffa trading online", "Broker truffaldini, schema dei 250 euro, liste CONSOB e recupero.", "broker truffa · 250 euro · consob · truffa trading whatsapp"),
    ("truffa-criptovalute/", "Crypto · Priorità", "Truffa criptovalute e bitcoin", "Recupero realistico, prelievo bloccato (Binance/Coinbase), a chi rivolgersi.", "truffa criptovalute · truffa bitcoin · prelievo bloccato"),
    ("avvocato-truffa-online/", "Avvocato", "Avvocato truffa online", "Quando conviene, cosa fa, cosa costa — trading, crypto, investimenti.", "avvocato truffa online · avvocato criptovalute"),
    ("problemi-prelievo-broker/", "Prelievi", "Problemi prelievo broker", "Perché il broker non paga, commissioni nascoste, primi 14 giorni.", "problemi prelievo broker · prelievo bloccato · broker non paga"),
    ("truffa-romance/", "Romance scam", "Truffa romantica e crypto", "Il copione del romance scam, i segnali e come uscirne con le prove giuste.", "truffa romantica · romance scam crypto"),
]


def page_html(g: dict) -> str:
    slug = g["slug"]
    canon = f"{SITE}/it/insights/{slug}/"
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
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Approfondimenti (IT)", "item": f"{SITE}/it/insights/"},
                    {"@type": "ListItem", "position": 3, "name": g["h1"], "item": canon},
                ],
            },
            {
                "@type": "Article",
                "headline": g["h1"],
                "description": g["desc"],
                "inLanguage": "it-IT",
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
<html lang="it-IT">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{escape(g["title"])}</title>
  <meta name="description" content="{escape(g["desc"])}" />
  <meta name="keywords" content="{escape(g["keywords"])}" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <meta name="author" content="Mike Levy Law" />
  <link rel="canonical" href="{canon}" />
  <link rel="alternate" hreflang="it" href="{canon}" />
  <link rel="alternate" hreflang="x-default" href="{canon}" />
  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="Mike Levy Law" />
  <meta property="og:locale" content="it_IT" />
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
      <nav class="crumbs" aria-label="Breadcrumb"><a href="../../../index.html">Home</a><span>/</span><a href="../">Approfondimenti</a><span>/</span><span>{escape(slug.replace("-", " "))}</span></nav>
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
      <h2 id="faq-h">Domande frequenti</h2>
      <p class="faq-lead">Risposte chiare su prossimi passi, scadenze e quando una valutazione riservata è utile.</p>
      <div class="faq">
{faq_html}
      </div>
    </section>
    <div class="cta-strip">
      <div>
        <strong>Richiedere una valutazione riservata?</strong>
        <p>Confrontiamo la sua documentazione con il quadro pubblico e valutiamo i canali di segnalazione o legali — senza impegno. Nessuna garanzia di recupero.</p>
      </div>
      <a href="{contact}">Richiedi una consulenza</a>
    </div>
    <p class="note">Solo informazioni. Non costituisce consulenza legale né garanzia di recupero. Il contatto non instaura alcun rapporto professionale.</p>
  </main>
  <footer class="site-footer">
    <div class="wrap-wide site-footer-inner">
      <p><a href="../">Approfondimenti (IT)</a> · <a href="../../../company-broker-index/">Indice società &amp; broker</a> · <a href="{contact}">Contatto</a> · <a href="../../../legal/privacy-policy.html">Privacy</a> · <a href="../../../legal/terms-of-use.html">Termini</a> · <a href="../../../legal/disclaimer.html">Disclaimer</a></p>
      <p>&copy; MLL 2026</p>
      <p class="footer-nap">1395 Brickell Ave, Suite 800 · Miami, FL 33131 · USA · <a href="mailto:info@mikelevylaw.com">info@mikelevylaw.com</a></p>
    </div>
  </footer>
  <script src="/js/tawk-mll.js" defer></script>
</body>
</html>
"""


def hub_html() -> str:
    canon = f"{SITE}/it/insights/"
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
                "name": "Guide sulle truffe online (Italiano)",
                "url": canon,
                "inLanguage": "it-IT",
                "description": "Guide in italiano su truffa online, truffa trading, criptovalute e recupero fondi: cosa fare, a chi rivolgersi, avvocato.",
                "hasPart": [
                    {"@type": "WebPage", "name": h2, "url": f"{SITE}/it/insights/{href}"}
                    for href, _t, h2, _p, _k in HUB_CARDS
                ],
            }
        ],
    }
    ld = json.dumps(graph, ensure_ascii=False)
    return f"""<!DOCTYPE html>
<html lang="it-IT">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Truffa online: guide, recupero soldi e avvocato | Mike Levy Law</title>
  <meta name="description" content="Truffa online, truffa trading, truffa criptovalute: recuperare soldi, a chi rivolgersi, denuncia e avvocato — guide in italiano di Mike Levy Law." />
  <meta name="keywords" content="truffa online, recuperare soldi truffati, truffa trading online, truffa criptovalute, avvocato truffa online, denuncia truffa online, broker truffa" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <meta name="author" content="Mike Levy Law" />
  <link rel="canonical" href="{canon}" />
  <link rel="alternate" hreflang="it" href="{canon}" />
  <link rel="alternate" hreflang="x-default" href="{canon}" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Mike Levy Law" />
  <meta property="og:locale" content="it_IT" />
  <meta property="og:title" content="Truffa online: guide, recupero soldi e avvocato | Mike Levy Law" />
  <meta property="og:description" content="Guide in italiano su truffa online, trading, criptovalute e recupero fondi." />
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
      <nav class="crumbs" aria-label="Breadcrumb"><a href="../../index.html">Home</a><span>/</span><span>Approfondimenti (IT)</span></nav>
    </div>
  </header>
  <main class="wrap">
    <div class="hero">
      <p class="kicker">Guide · Italiano · Aggiornato il {UPDATED}</p>
      <h1>Truffa online: recupero soldi, denuncia e avvocato</h1>
      <p class="lead">
        Parta dalla sua situazione — <strong>recuperare soldi</strong>, <strong>cosa fare</strong>,
        <strong>a chi rivolgersi</strong> o <strong>avvocato</strong> — per truffa online, trading e
        criptovalute. Scritto per chiarezza, non per promesse. Nessuna garanzia di recupero.
      </p>
    </div>

    <div class="folder-grid">
{cards}
    </div>
  </main>
  <footer class="site-footer">
    <div class="wrap-wide site-footer-inner">
      <p><a href="../../insights/">Insights (EN)</a> · <a href="../../de/insights/">Ratgeber (DE)</a> · <a href="../../company-broker-index/">Indice società &amp; broker</a> · <a href="../../index.html?source=insights-it-hub#contact">Contatto</a> · <a href="../../legal/privacy-policy.html">Privacy</a> · <a href="../../legal/disclaimer.html">Disclaimer</a></p>
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
    print("Wrote it/insights/index.html")
    for g in GUIDES:
        dest = OUT / g["slug"]
        dest.mkdir(parents=True, exist_ok=True)
        path = dest / "index.html"
        path.write_text(page_html(g), encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT)}")
    print(f"Done — {len(GUIDES)} Italian keyword guides + hub")


if __name__ == "__main__":
    main()
