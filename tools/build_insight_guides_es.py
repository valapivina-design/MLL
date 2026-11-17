#!/usr/bin/env python3
"""Build Spanish keyword-slug insight guides under /es/insights/.

Spanish victim-intent funnel: "estafa online" is the broad anchor, with
recuperar/denuncia/abogado/retiro pages as supporting intent pages.
Spain + LatAm vocabulary (bróker/estafa + fraude de inversiones).

  python3 tools/build_insight_guides_es.py
"""
from __future__ import annotations

import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "es" / "insights"
SITE = "https://mikelevylaw.com"
UPDATED = "17 de noviembre de 2026"
DATE_ISO = "2026-11-17"
FREE_LINE = "La consulta es gratuita. Primero necesitamos validar su reclamación y valorar sus perspectivas y viabilidad — eso depende del nivel de pruebas. Sin garantía de recuperación."

GUIDES = [
    {
        "slug": "estafa-online",
        "kicker": f"Estafa online · Actualizado el {UPDATED}",
        "h1": "Estafa online: qué hacer, a quién acudir y cómo denunciar",
        "title": "Estafa online: qué hacer y a quién acudir | Mike Levy Law",
        "desc": "Estafa online: qué hacer de inmediato, a quién acudir (Policía Nacional, Guardia Civil), cómo denunciar y qué es un chiringuito financiero.",
        "keywords": "estafa online, estafa online que hacer, estafa online a quien acudir, denunciar estafa online, denuncia estafa policia nacional, denuncia guardia civil estafa, chiringuito financiero, fraude de inversiones",
        "lead": "¿Víctima de una estafa online? Las primeras dos semanas deciden qué opciones quedan abiertas: cortar los pagos, conservar las pruebas, denunciar en el canal correcto. Esta página reúne qué hacer, a quién acudir y cómo funciona la denuncia.",
        "sections": [
            (
                "Qué hacer de inmediato",
                "<ol>"
                "<li>Corte cualquier otro pago — incluidas «tasas», «impuestos» o «comisiones de desbloqueo».</li>"
                "<li>Conserve chats, correos, extractos bancarios, dominios exactos y referencias.</li>"
                "<li>Llame a su banco o emisor de tarjeta: devolución de transferencia o chargeback.</li>"
                "<li>Presente denuncia (Policía Nacional o Guardia Civil) con la documentación reunida.</li>"
                "<li>Para pérdidas relevantes: valoración confidencial con un abogado.</li>"
                "</ol>",
            ),
            (
                "A quién acudir",
                "<ul>"
                "<li><strong>Policía Nacional / Guardia Civil:</strong> denuncia por estafa; ambos cuerpos la reciben, también telemáticamente.</li>"
                "<li><strong>CNMV:</strong> advertencia sobre chiringuitos financieros — entidades no registradas que ofrecen inversión. No devuelve dinero, pero documenta y alerta.</li>"
                "<li><strong>Banco / emisor de tarjeta:</strong> en paralelo, con plazos propios para devoluciones y chargeback. Si no le responde, reclamación ante el Banco de España.</li>"
                "</ul>",
            ),
            (
                "Qué es un chiringuito financiero",
                "<p>Es el término que usa la CNMV para entidades que ofrecen servicios de inversión <strong>sin estar registradas</strong>: plataformas de trading, «asesores» de WhatsApp, webs clonadas de firmas reales. La CNMV publica sus advertencias cada semana. Si su «bróker» está en esa lista — o no está en ningún registro — el punto de partida es la denuncia y la vía bancaria, no más depósitos.</p>",
            ),
        ],
        "faqs": [
            (
                "Estafa online: ¿qué hago primero?",
                "Cortar los pagos y conservar las pruebas, en ese orden. Cada «tasa» adicional solo agranda la pérdida; las pruebas sirven para el banco, la denuncia y el abogado.",
            ),
            (
                "¿Dónde denuncio una estafa online?",
                "En la Policía Nacional o la Guardia Civil (también online). Si la estafa se presentó como inversión, añada una advertencia a la CNMV.",
            ),
            (
                "¿Con la denuncia recupero el dinero?",
                "No directamente. La recuperación pasa por chargeback, devolución de la transferencia, medidas judiciales o acciones civiles. La denuncia es el presupuesto de todo ello.",
            ),
        ],
        "related": [
            ("../recuperar-dinero-estafa/", "Recuperar dinero de una estafa"),
            ("../abogado-estafa-online/", "Abogado para estafa online"),
            ("../estafa-trading-broker/", "Estafa de trading y brókers"),
        ],
        "extra_sections": [
            (
                "Semana a semana: un calendario realista",
                "<p><strong>Días 1–3:</strong> cortar pagos, banco avisado, pruebas a salvo. <strong>Días 4–10:</strong> chargeback o recall iniciados, denuncia presentada. <strong>Semanas 2–6:</strong> procedimientos bancarios en marcha, trazado en cripto, comprobación de listas de la CNMV. <strong>Después:</strong> valoración civil si hay contraparte y bienes identificables. Quien sigue este orden no pierde plazos esperando que la plataforma «lo solucione internamente» — esa espera es exactamente lo que el guion necesita.</p>",
            ),
            (
                "El expediente probatorio que mueve a bancos y abogados",
                "<ol>"
                "<li>Capturas de la cuenta con URL y fecha visibles</li>"
                "<li>Cada pago: fecha, importe y beneficiario en el extracto bancario</li>"
                "<li>Solicitudes de retiro y todas las respuestas — exportadas, no solo fotografiadas</li>"
                "<li>Peticiones textuales de «impuestos» o «comisiones de liberación»</li>"
                "<li>Dominio exacto, nombre de la app y cómo la encontró</li>"
                "</ol>"
                "<p>Con este expediente un abogado valora en un día lo que sin él lleva semanas. Para el banco igual: una reclamación documentada es un caso; sin documentos, es una queja.</p>",
            ),
        ],
        "source": "insights-es-estafa-online",
    },
    {
        "slug": "recuperar-dinero-estafa",
        "kicker": f"Recuperación · Actualizado el {UPDATED}",
        "h1": "Recuperar dinero de una estafa: transferencia, tarjeta, Bizum y PayPal",
        "title": "Recuperar dinero estafa online: por vía de pago | Mike Levy Law",
        "desc": "Recuperar dinero estafado: devolución de transferencia, chargeback en tarjeta, Bizum y PayPal — el canal correcto depende de cómo pagó.",
        "keywords": "recuperar dinero estafa online, recuperar dinero estafado, como recuperar mi dinero de un broker, recuperar dinero estafa banco, recuperar transferencia estafa, recuperar dinero tarjeta estafa, recuperar dinero bizum estafa, recuperación de fondos, reembolso inversión, mejores servicios de recuperación, empresas recuperacion de fondos estafa",
        "lead": "Cómo recuperar dinero estafado depende casi por completo de <strong>cómo pagó</strong>: transferencia, tarjeta, Bizum o PayPal siguen reglas y plazos distintos. La secuencia correcta marca la diferencia — y el tiempo es el factor más caro.",
        "sections": [
            (
                "Transferencia: devolución y protocolo antifraude",
                "<p>Pida a su banco la <strong>devolución de la transferencia</strong> (recall) y la apertura de expediente de fraude — idealmente el mismo día. Si los fondos aún están en el banco destino, existen opciones de bloqueo. Guarde la referencia del recall. Si no autorizó la operación, dígalo claramente por escrito: la normativa de servicios de pago le protege más en ese caso.</p>",
            ),
            (
                "Tarjeta: chargeback. Bizum y PayPal: sus propios canales",
                "<p>Con tarjeta existe el chargeback del emisor: ventanas cortas, documentación decisiva (dominio, capturas del retiro rechazado, chats). <strong>Bizum</strong> funciona como transferencia inmediata: reclame en su banco al momento, no hay «chargeback Bizum» — la rapidez lo es todo. <strong>PayPal</strong> tiene centro de resoluciones con plazos propios para disputas.</p>",
            ),
            (
                "Criptomonedas y las «empresas de recuperación»",
                "<p>En cripto no hay devolución, pero la trazabilidad hasta exchanges con KYC abre canales formales — vea <a href=\"../estafa-criptomonedas/\">estafa criptomonedas</a>. Y cuidado con los «mejores servicios de recuperación» que aparecen tras la pérdida: la CNMV los describe como <em>recovery rooms</em> — contactan sin que usted llame, prometen el 100 % y piden dinero por adelantado. Es la segunda estafa.</p>",
            ),
        ],
        "faqs": [
            (
                "¿Cómo recuperar mi dinero de un bróker estafador?",
                "Por la vía de pago: chargeback (tarjeta), devolución de transferencia (banco), disputa PayPal, trazabilidad (cripto) — junto a la denuncia y, en importes relevantes, valoración legal. Nadie puede garantizar la recuperación.",
            ),
            (
                "Pagué por Bizum: ¿puedo recuperarlo?",
                "Bizum es una transferencia inmediata: reclame en su banco de inmediato con la denuncia en marcha. No existe un botón de devolución; cuentan las horas, no las semanas.",
            ),
            (
                "¿Son fiables las empresas de recuperación de fondos?",
                "Algunos servicios de investigación y legales son legítimos. Contacto no solicitado + promesa de recuperación total + pago por adelantado (sobre todo en cripto) es el patrón de la recovery room. No pague.",
            ),
        ],
        "related": [
            ("../estafa-online/", "Estafa online: qué hacer"),
            ("../abogado-estafa-online/", "Abogado para estafa online"),
            ("../broker-no-deja-retirar/", "El bróker no me deja retirar"),
        ],
        "extra_sections": [
            (
                "Cómo plantear la reclamación para que el banco la trate como fraude",
                "<p>Llame al número de fraude, no al soporte general. Diga literalmente: «Fui inducido con engaño a autorizar estos pagos y solicito recall inmediato y apertura de caso de fraude con número de referencia». Pida que el recall salga <strong>ese mismo día</strong>, con aviso al banco receptor. Después, confirme por escrito: un email que resume los hechos crea la traza que cuenta si la respuesta del banco acaba ante el Servicio de Reclamaciones o ante un abogado.</p>",
            ),
            (
                "Si el banco dice que no",
                "<p>Una negativa es un documento, no el final. Pida el motivo por escrito y abra reclamación formal ante el banco y, si procede, ante el Servicio de Reclamaciones del Banco de España — sobre todo si la gestión fue deficiente (sin intento de recall, sin caso de fraude abierto, respuestas contradictorias). Nada de esto garantiza la devolución; construye el expediente sobre el que se apoyan denuncia, señalamientos y posibles acciones civiles.</p>",
            ),
        ],
        "source": "insights-es-recuperar-dinero-estafa",
    },
    {
        "slug": "estafa-trading-broker",
        "kicker": f"Trading · Actualizado el {UPDATED}",
        "h1": "Estafa de trading y brókers falsos: el patrón, la CNMV y la recuperación",
        "title": "Estafa trading / estafa broker: patrón y CNMV | Mike Levy Law",
        "desc": "Estafa trading: cómo identificar una plataforma falsa, brókeres no regulados, la lista de chiringuitos de la CNMV y cómo recuperar dinero del bróker.",
        "keywords": "estafa trading, estafa broker, bróker falso, broker falso, estafa forex, cómo identificar una plataforma falsa, brókeres no regulados, plataforma de trading falsa, app de trading falsa, lista brokers estafadores cnmv, broker no regulado españa, estafa whatsapp trading, como recuperar dinero del broker",
        "lead": "La estafa de trading tiene guion: anuncio con famoso o contacto por WhatsApp, 250 € iniciales, «ganancias» en pantalla, y el bloqueo al retirar. Aquí están las señales, el papel de la CNMV y las vías reales para recuperar el dinero.",
        "sections": [
            (
                "El patrón de la plataforma falsa",
                "<p>Publicidad en redes o artículos falsos, depósito inicial pequeño, un «gestor» por teléfono o WhatsApp, primeras ganancias visibles, presión para ingresar más. Al pedir el retiro: «impuestos», «verificaciones» o silencio. Las capturas de la app o web falsa, con fecha y URL, son prueba — consérvelas antes de que la cuenta «desaparezca».</p>",
            ),
            (
                "CNMV: la lista de chiringuitos",
                "<p>La CNMV publica advertencias sobre entidades no registradas (chiringuitos financieros) y las listas internacionales (IOSCO I-SCAN) completan el cuadro. Compruebe siempre el <strong>dominio exacto</strong> en el registro, no el nombre del anuncio: los clones copian marcas autorizadas. La advertencia a la CNMV no devuelve dinero, pero documenta y alerta a otros.</p>",
            ),
            (
                "Cómo recuperar dinero del bróker",
                "<ol>"
                "<li>Cero pagos adicionales, incluidos «impuestos sobre el retiro».</li>"
                "<li>Tarjeta: chargeback inmediato; transferencia: recall en el banco.</li>"
                "<li>Denuncia ante Policía Nacional o Guardia Civil + advertencia CNMV.</li>"
                "<li>Pérdidas relevantes: <a href=\"../abogado-estafa-online/\">valoración legal confidencial</a>.</li>"
                "</ol>"
                "<p>Si el contacto nació en WhatsApp/Telegram, exporte los chats antes de bloquear: son el centro del expediente.</p>",
            ),
        ],
        "faqs": [
            (
                "¿Cómo identificar una plataforma de trading falsa?",
                "Tres comprobaciones en dos minutos: dominio exacto en el registro de la CNMV, beneficiario del pago (¿empresa registrada o cuenta de un tercero?), y lista de advertencias. Rentabilidad garantizada y bonos que bloquean el retiro son señales de alto.",
            ),
            (
                "¿Qué es un bróker no regulado?",
                "Una entidad que ofrece inversión sin registro en la CNMV ni pasaporte europeo válido. Sus reclamaciones no llegan a los mecanismos de inversores registrados: quedan vía bancaria, denuncia y acciones civiles.",
            ),
            (
                "La app muestra ganancias: ¿puedo fiarme?",
                "No. En las plataformas falsas el saldo es parte del decorado — sube mientras usted ingresa y se bloquea al retirar. El único dato real es si el dinero llegó a su banco.",
            ),
        ],
        "related": [
            ("../recuperar-dinero-estafa/", "Recuperar dinero estafado"),
            ("../como-saber-si-un-broker-es-fiable/", "Cómo saber si un bróker es fiable"),
            ("../estafa-online/", "Estafa online: qué hacer"),
        ],
        "extra_sections": [
            (
                "El recorrido típico en cifras",
                "<p>Esquema recurrente: 250 € iniciales, saldo visible que sube a 800 €, luego 5.000 € «para el siguiente nivel», un pequeño retiro de prueba que funciona como demostración de confianza — y desde el primer importe de cinco cifras empieza la fase de bloqueo. La cuenta suele acabar mostrando un múltiplo de lo ingresado: esa cifra es decorado, sirve para calcular la «comisión». El daño real es la suma de los pagos efectivamente realizados — nada más.</p>",
            ),
            (
                "Chargeback bien motivado para plataformas de trading",
                "<p>Planteé la disputa como «servicio no prestado» o misrepresentation: pagó un servicio de inversión cuya función esencial — la devolución de fondos — fue denegada. Adjunte el rechazo del retiro, no solo el ingreso. «Cambié de opinión» es motivación débil; «el comercio deniega el pago contractual y exige comisiones adicionales» está documentado. Una cronología de una página (ingreso → solicitud → rechazo → petición de comisiones) es el documento más eficaz.</p>",
            ),
        ],
        "source": "insights-es-estafa-trading-broker",
    },
    {
        "slug": "estafa-criptomonedas",
        "kicker": f"Criptomonedas · Actualizado el {UPDATED}",
        "h1": "Estafa con criptomonedas: recuperar, exchanges clonados y denuncia",
        "title": "Estafa criptomonedas / bitcoin: qué hacer | Mike Levy Law",
        "desc": "Estafa criptomonedas: recuperar criptomonedas estafadas, qué hacer si el retiro está bloqueado, clones de exchanges y a quién acudir.",
        "keywords": "estafa criptomonedas, recuperar criptomonedas estafadas, recuperar bitcoin estafa, recuperar criptomonedas, estafa criptomonedas instagram telegram, estafa binance clon, retiro bloqueado exchange, estafa deepfake inversiones, estafa inteligencia artificial inversiones",
        "lead": "En las estafas con criptomonedas no hay devolución — pero la blockchain es pública. Si las monedas llegan a un exchange con KYC, se abren canales formales. Y si el «retiro bloqueado» ocurre en lo que parece Binance o Coinbase, la primera verificación es si está en el exchange real o en un clon.",
        "sections": [
            (
                "Recuperar criptomonedas: lo realista",
                "<p>No existe chargeback en cripto. Existe la trazabilidad: cada transacción es pública y a menudo conduce a exchanges con obligaciones KYC. Sobre esos puntos pueden articularse requerimientos formales de autoridades y abogados. Los éxitos totales son raros; los parciales dependen del recorrido de los fondos y de la velocidad.</p>",
            ),
            (
                "Instagram, Telegram y los deepfakes",
                "<p>El patrón dominante llega por Instagram, Telegram o anuncios con famosos generados por IA (deepfakes): «inversión» con rendimientos semanales, beneficios ficticios, y «tasas de verificación» o «impuestos» al retirar. Ninguna inversión seria capta clientes por mensaje directo ni garantiza porcentajes. Desconfíe del contacto no solicitado — el 95 % de las fotos de «asesores» son robadas.</p>",
            ),
            (
                "A quién acudir",
                "<ol>"
                "<li>Policía Nacional o Guardia Civil — denuncia con hashes de transacción y direcciones wallet.</li>"
                "<li>CNMV — advertencia si la estafa se presentó como inversión.</li>"
                "<li>Exchange real (si los fondos lo tocaron) — canal antifraude con los hashes.</li>"
                "<li><a href=\"../abogado-estafa-online/\">Abogado</a> — trazabilidad y requerimientos formales cuando el importe es relevante.</li>"
                "</ol>",
            ),
        ],
        "faqs": [
            (
                "¿Se pueden recuperar criptomonedas estafadas?",
                "No por devolución — sí por trazabilidad hasta exchanges regulados, denuncia con hashes y posibles acciones civiles contra sujetos identificables. Quien garantice la recuperación es un riesgo en sí mismo.",
            ),
            (
                "El retiro está bloqueado en «Binance»: ¿qué hago?",
                "Verifique primero que está en la web/app oficial. Si el «soporte» pide una tasa para desbloquear el retiro, no es el exchange real: es un clon. Cero pagos y denuncia.",
            ),
            (
                "Me contactaron por Instagram/Telegram con una inversión: ¿es estafa?",
                "El contacto no solicitado con rendimientos garantizados es el patrón central de la estafa cripto actual. Compruebe la entidad en la CNMV y no envíe nada.",
            ),
        ],
        "related": [
            ("../recuperar-dinero-estafa/", "Recuperar dinero estafado"),
            ("../estafa-sentimental-criptomonedas/", "Estafa sentimental y cripto"),
            ("../abogado-estafa-online/", "Abogado para estafa online"),
        ],
        "extra_sections": [
            (
                "Qué debe contener un informe de trazado para que sirva",
                "<p>Un informe útil incluye: la cadena completa de transacciones desde su wallet, la atribución de clusters (qué direcciones pertenecen a la misma entidad), las direcciones de exchanges o servicios identificados con evidencias y una metodología documentada que resista ante investigadores y jueces. Las capturas de un explorador de bloques rara vez bastan — lo que cuenta es que el recorrido sea reproducible.</p>",
            ),
            (
                "Por qué el exchange suele ser el punto de inflexión",
                "<p>Los estafadores deben convertir tarde o temprano a moneda tradicional — y casi siempre pasan por exchanges con obligaciones KYC. Ahí hay nombres, cuentas y canales de retiro. Autoridades y abogados pueden dirigirse a esos actores; algunos exchanges congelan temporalmente ante una solicitud formal. Por eso la rapidez importa: cada semana aumenta la probabilidad de que los fondos ya estén en otra parte.</p>",
            ),
        ],
        "source": "insights-es-estafa-criptomonedas",
    },
    {
        "slug": "broker-no-deja-retirar",
        "kicker": f"Retiros · Actualizado el {UPDATED}",
        "h1": "Mi bróker no me deja retirar: por qué pasa y qué hacer",
        "title": "Broker no me deja retirar dinero: qué hacer | Mike Levy Law",
        "desc": "Mi bróker no me deja retirar: por qué el bróker retiene fondos, retiro bloqueado o pendiente, comisiones ocultas e «impuestos» para retirar — y los próximos pasos.",
        "keywords": "mi broker no me deja retirar, broker no me deja retirar dinero, por qué mi bróker no me deja retirar, retiro bloqueado broker, retiro pendiente broker, problema retiro bróker, bróker no paga, retención de fondos bróker, comisiones ocultas retiro, broker me pide impuestos para retirar, broker me da largas para retirar",
        "lead": "Retiro «en procesamiento» desde hace semanas, después nuevas condiciones. Que el bróker no le deje retirar suele ser la primera señal dura de que algo va mal. Lo que haga en los próximos 14 días decide qué opciones quedan.",
        "sections": [
            (
                "Por qué fallan de verdad los retiros",
                "<p>Los retrasos operativos existen. Lo que cuenta es el <strong>patrón</strong>: una explicación fechada con transferencia trazable es una cosa; excusas cambiantes — nuevas «tasas», «comisiones de liberación», «verificación de compliance» o silencio tras un pequeño retiro de prueba — otra muy distinta. Las comisiones ocultas en el retiro son la señal más típica: ningún bróker serio pide dinero nuevo para devolverle el suyo.</p>",
            ),
            (
                "«Pague el 20 % de impuestos para retirar»",
                "<p>Es el patrón documentado una y otra vez en reclamaciones: la plataforma exige un porcentaje del «saldo» como supuesto impuesto antes de liberar fondos. El saldo mostrado es parte del decorado. Si paga, pedirán otra cosa. No envíe nada — y guarde la petición por escrito: es prueba central para banco, denuncia y abogado.</p>",
            ),
            (
                "Qué hacer en los primeros 14 días",
                "<ol>"
                "<li>Ningún pago más — ni tasa, ni desbloqueo, ni impuesto.</li>"
                "<li>Solicite el retiro por escrito y conserve la negativa.</li>"
                "<li>Exporte chats, correos, extractos y el dominio exacto.</li>"
                "<li>Banco/emisor: recall o chargeback con sus plazos.</li>"
                "<li>Verifique el dominio en la CNMV: ¿original o clon?</li>"
                "</ol>",
            ),
        ],
        "faqs": [
            (
                "¿Por qué mi bróker no me deja retirar?",
                "Si a las solicitudes le siguen comisiones nuevas o condiciones cambiantes, es el patrón del retiro bloqueado: cero pagos, pruebas a salvo, vías bancarias y denuncia en paralelo.",
            ),
            (
                "El bróker me da largas desde hace meses: ¿qué hago?",
                "Deje de esperar al «soporte». Active chargeback/recall según cómo pagó, denuncie con la documentación y valore asesoramiento legal si el importe es relevante.",
            ),
            (
                "¿Es legal que me cobren una comisión por retirar?",
                "Las comisiones legítimas se descuentan del saldo y constan en las condiciones. Pedir un pago nuevo para «liberar» su dinero es el patrón de la estafa de anticipo. No pague.",
            ),
        ],
        "related": [
            ("../recuperar-dinero-estafa/", "Recuperar dinero estafado"),
            ("../estafa-trading-broker/", "Estafa de trading y brókers"),
            ("../abogado-estafa-online/", "Abogado para estafa online"),
        ],
        "extra_sections": [
            (
                "El calendario de escalada tras el primer rechazo",
                "<p><strong>Día 1–2:</strong> solicitud escrita de retiro con plazo. <strong>Día 3–5:</strong> banco y emisor avisados — los relojes empiezan a correr. <strong>Día 5–10:</strong> chargeback/recall iniciados, comprobación de listas de la CNMV. <strong>Día 10–14:</strong> denuncia en preparación, señalamiento a las listas y valoración legal si el importe es relevante. Cada «espere unos días más» es una victoria del guion: la plataforma gana tiempo exactamente cuando usted se lo concede.</p>",
            ),
            (
                "«Verificación de cumplimiento», «AML», «cuenta en revisión»: qué hay detrás",
                "<p>Suenan oficiales, pero en este contexto son guion: las verificaciones reales terminan con una decisión motivada, no con nuevas comisiones. Pregunta de prueba al soporte: «Indíquenme por escrito la base legal y la fecha prevista de finalización». Los departamentos reales responden. Los guiones se repiten — y esa repetición es precisamente el documento que le sirve a banco y abogado.</p>",
            ),
        ],
        "source": "insights-es-broker-no-deja-retirar",
    },
    {
        "slug": "abogado-estafa-online",
        "kicker": f"Abogado · Actualizado el {UPDATED}",
        "h1": "Abogado para estafa online: cuándo conviene, qué hace y las recovery rooms",
        "title": "Abogado estafa online / trading / criptomonedas | Mike Levy Law",
        "desc": "Abogado estafa online: cuándo conviene, qué hace un abogado de estafas de trading y criptomonedas, y cómo distinguirlo de una recovery room.",
        "keywords": "abogado estafa online, abogado criptomonedas, abogado estafa trading, abogado experto criptomonedas, denunciar broker ante cnmv, recovery room estafa, abogado fraude de inversiones",
        "lead": "Tras una estafa online, un abogado sirve para tres cosas: estructurar las pruebas, elegir los canales en el orden correcto y decirle con franqueza si el caso es viable. Sin promesas de recuperación — método.",
        "sections": [
            (
                "Qué hace concretamente el abogado",
                "<ul>"
                "<li>Reconstruye pagos, dominios y contrapartes (¿original o clon?)</li>"
                "<li>Coordina chargeback, recall y denuncia sin quemar plazos</li>"
                "<li>En cripto: trazabilidad y requerimientos formales a exchanges</li>"
                "<li>Valora acciones civiles y contra quién dirigirlas</li>"
                "<li>Contrasta su expediente con advertencias públicas (CNMV, IOSCO)</li>"
                "</ul>",
            ),
            (
                "Cuándo conviene",
                "<p>Para importes pequeños suelen bastar banco y denuncia. Con pérdidas de cinco o seis cifras, pagos mixtos (tarjeta + transferencia + cripto) o contrapartes internacionales, la estructura legal renta: evita errores de secuencia e identifica sujetos realmente perseguibles. La consulta es gratuita y sirve exactamente para valorar eso.</p>",
            ),
            (
                "Recovery rooms: la segunda estafa",
                "<p>La CNMV alerta de las <em>recovery rooms</em>: empresas que contactan sin que usted las llame (a veces comprando listas de afectados), prometen recuperar el 100 % y piden «impuestos» u «honorarios» por adelantado. Algunas dicen actuar en nombre de la CNMV o de un juzgado — falso. Un abogado serio empieza por validar su caso con documentos, nunca pidiendo un anticipo para «desbloquear» fondos.</p>",
            ),
        ],
        "faqs": [
            (
                "¿Necesito un abogado para una estafa online?",
                "Para importes pequeños, a menudo no. Para pérdidas relevantes o casos complejos sí: chargeback, denuncia y acciones civiles tienen plazos y presupuestos distintos, y el orden importa.",
            ),
            (
                "¿La consulta con el abogado es gratuita?",
                "Sí. Primero validamos su reclamación y valoramos perspectivas y viabilidad — eso depende del nivel de pruebas que tenga.",
            ),
            (
                "¿Puede un abogado garantizar la recuperación?",
                "No — nadie puede. Un abogado mejora estructura, tiempos y destino de los pasos; las garantías pertenecen a las recovery rooms.",
            ),
        ],
        "related": [
            ("../estafa-online/", "Estafa online: qué hacer"),
            ("../recuperar-dinero-estafa/", "Recuperar dinero estafado"),
            ("../estafa-criptomonedas/", "Estafa criptomonedas"),
        ],
        "extra_sections": [
            (
                "Cómo verificar a un abogado antes de que verifique su caso",
                "<ol>"
                "<li>Colegio de Abogados: ¿la persona está realmente colegiada con ese nombre?</li>"
                "<li>Despacho verificable y devolución de llamada al número público, no al que le dieron por email</li>"
                "<li>Encargo descrito por escrito — nada de porcentajes de éxito por teléfono</li>"
                "<li>Nada de anticipos en cripto ni a cuentas personales</li>"
                "</ol>"
                "<p>Los estafadores copian despachos reales hasta el membrete. La comprobación de dos minutos vale aquí igual que con el bróker.</p>",
            ),
            (
                "Qué responde la consulta gratuita, en concreto",
                "<p>La consulta es gratuita. Responde a tres preguntas: ¿existe rastro utilizable (pagos, beneficiarios, pruebas)? ¿existe contraparte alcanzable? ¿supera la recuperación realista el coste? Solo después se decide si el encargo tiene sentido económico — depende del nivel de sus pruebas, no de las promesas.</p>",
            ),
        ],
        "source": "insights-es-abogado-estafa-online",
    },
    {
        "slug": "estafa-sentimental-criptomonedas",
        "kicker": f"Estafa sentimental · Actualizado el {UPDATED}",
        "h1": "Estafa sentimental y criptomonedas: pig butchering, Tinder y cómo salir",
        "title": "Estafa sentimental criptomonedas (pig butchering) | Mike Levy Law",
        "desc": "Estafa romance: qué es la estafa romance y el pig butchering, cómo funciona la estafa de Tinder con criptomonedas y cómo recuperar dinero de una estafa romance.",
        "keywords": "estafa sentimental criptomonedas, estafa romance, qué es la estafa romance, pig butchering, matanza del cerdo estafa, estafa tinder criptomonedas, timador tinder, cómo recuperar dinero de estafa romance, estafa romantica bitcoin",
        "lead": "La estafa sentimental («romance scam») empieza con una relación y termina en una plataforma de inversión falsa — casi siempre cripto. Reconocerla es difícil porque el mecanismo es emocional, no técnico. Salir exige frialdad: cero pagos, pruebas, canales correctos.",
        "sections": [
            (
                "Qué es el pig butchering",
                "<p>Contacto en apps de citas o redes (a veces un mensaje «por error»), semanas de confianza, y entonces el «consejo»: una plataforma de inversión cripto «exclusiva». Pequeños retiros iniciales que funcionan, importes crecientes, y el bloqueo final. La pareja y la plataforma son la misma organización — los estafadores lo llaman «engordar al cerdo» antes del sacrificio. Casos documentados en España superan los 27.000 € por víctima.</p>",
            ),
            (
                "Señales de que es una estafa romance",
                "<ul>"
                "<li>Nunca se han visto en persona; videollamadas siempre fallan.</li>"
                "<li>Propone invertir en una plataforma que «también usa».</li>"
                "<li>Urgencia emocional: emergencias, oportunidades que caducan, secretos.</li>"
                "<li>Al retirar: impuestos o tasas a pagar primero.</li>"
                "</ul>",
            ),
            (
                "Cómo recuperar dinero de una estafa romance",
                "<ol>"
                "<li>Cero pagos y nada de confrontaciones emotivas: documente todo (chats exportados, fotos, perfiles).</li>"
                "<li>Banco/tarjeta: chargeback o recall; cripto: hashes y direcciones.</li>"
                "<li>Denuncia ante Policía Nacional o Guardia Civil — el delito es estafa.</li>"
                "<li>Pérdidas relevantes: valoración legal confidencial, también para trazabilidad cripto.</li>"
                "</ol>"
                "<p>Sin vergüenza: el patrón funciona igual con profesionales solventes. Solo hace falta la secuencia correcta.</p>",
            ),
        ],
        "faqs": [
            (
                "¿Cómo funciona la estafa de Tinder con criptomonedas?",
                "Relación construida durante semanas, luego la plataforma de inversión recomendada por la pareja: ganancias ficticias en pantalla, bloqueo al retirar, petición de «impuestos». Pareja y plataforma son el mismo grupo.",
            ),
            (
                "¿Puedo recuperar el dinero de una estafa romance?",
                "Depende de la vía de pago: chargeback con tarjeta, recall en transferencia, trazabilidad cripto hasta exchanges. La denuncia con chats y pruebas es el presupuesto. Garantizar la recuperación no se puede.",
            ),
            (
                "¿Debo denunciar aunque me dé vergüenza?",
                "Sí. La denuncia es confidencial y alimenta investigaciones sobre organizaciones internacionales; las pruebas emocionales (chats, promesas) son exactamente lo que necesitan los investigadores.",
            ),
        ],
        "related": [
            ("../estafa-criptomonedas/", "Estafa criptomonedas"),
            ("../recuperar-dinero-estafa/", "Recuperar dinero estafado"),
            ("../estafa-online/", "Estafa online: qué hacer"),
        ],
        "extra_sections": [
            (
                "La línea temporal emocional del pig butchering: reconocerla mientras ocurre",
                "<p><strong>Semanas 1–3:</strong> contacto diario, atenciones, nunca un encuentro. <strong>Semanas 3–6:</strong> primeras menciones a inversiones «que yo también uso». <strong>Semanas 6–10:</strong> primer depósito, pequeño retiro que funciona, confianza plena. <strong>Después:</strong> importes crecientes, bloqueo e «impuestos». Si reconoce esta secuencia en su situación actual, deténgase donde está: no hace falta más dinero para comprobar — hace falta un retiro solicitado por escrito.</p>",
            ),
            (
                "Las pruebas emocionales son pruebas legales",
                "<p>Chats románticos, promesas de futuro común, presiones afectivas: exportadas con fecha e interlocutor, demuestran la inducción — el elemento que convierte una pérdida en estafa. No borre nada por vergüenza: los investigadores leen estos guiones a diario, y lo que para usted es personal para ellos es el rasgo distintivo de la organización que la atacó.</p>",
            ),
        ],
        "source": "insights-es-estafa-sentimental",
    },
    {
        "slug": "como-saber-si-un-broker-es-fiable",
        "kicker": f"Prevención · Actualizado el {UPDATED}",
        "h1": "Cómo saber si un bróker es fiable: la verificación de dos minutos",
        "title": "Cómo saber si un bróker es fiable o está regulado | Mike Levy Law",
        "desc": "Cómo saber si un bróker es fiable: verificar el registro de la CNMV, clon vs original, señales de plataforma falsa y la comprobación de dos minutos antes de pagar.",
        "keywords": "como saber si un broker es fiable, como saber si un broker esta regulado, como saber si una plataforma de trading es falsa, broker no regulado españa, verificar broker cnmv, señales broker estafa",
        "lead": "La mayoría de estafas de bróker se evitan con dos minutos de verificación <strong>antes</strong> del primer pago: dominio en el registro, beneficiario del cobro, promesas de rendimiento. Esta es la comprobación exacta, paso a paso.",
        "sections": [
            (
                "La verificación de dos minutos",
                "<ol>"
                "<li><strong>Dominio exacto</strong> en el registro de la CNMV (no el nombre de la marca en el anuncio — el dominio).</li>"
                "<li><strong>Lista de advertencias</strong> de la CNMV y de IOSCO I-SCAN.</li>"
                "<li><strong>Beneficiario del pago:</strong> ¿la sociedad registrada o un particular/tercer país?</li>"
                "<li><strong>Prueba de retiro pequeña</strong> antes de cualquier ingreso grande.</li>"
                "</ol>",
            ),
            (
                "Clon vs original",
                "<p>Los chiringuitos copian nombre, logo y hasta número de licencia de firmas reales — y cambian una letra del dominio. Si el registro muestra otra web u otro teléfono, usted está ante un clon, aunque la página parezca idéntica. La comprobación se hace siempre desde el registro oficial, nunca desde los enlaces que le envía el «asesor».</p>",
            ),
            (
                "Señales de plataforma falsa",
                "<ul>"
                "<li>Rendimiento garantizado o porcentajes semanales fijos.</li>"
                "<li>Bonos que vinculan su depósito a condiciones de retiro.</li>"
                "<li>Contacto no solicitado (WhatsApp, Telegram, Instagram, anuncios con famosos).</li>"
                "<li>«Impuestos» o «tasas» a pagar antes de retirar.</li>"
                "</ul>"
                "<p>Si ya pagó y reconoce estas señales: <a href=\"../estafa-online/\">qué hacer ante una estafa online</a> y <a href=\"../recuperar-dinero-estafa/\">vías para recuperar el dinero</a>.</p>",
            ),
        ],
        "faqs": [
            (
                "¿Cómo sé si un bróker está regulado en España?",
                "Buscando el dominio exacto en el registro de la CNMV. Si no aparece — o aparece otra web distinta — no está autorizado para ofrecer inversión en España, diga lo que diga su página.",
            ),
            (
                "El bróker tiene número de licencia: ¿es seguro?",
                "No necesariamente: los números se copian. Verifíquelo en el registro de la autoridad emisora y compruebe que el dominio coincide exactamente con el registrado.",
            ),
            (
                "¿Qué hago si ya deposité en una plataforma sospechosa?",
                "Pida un retiro pequeño por escrito y documente la respuesta. Si aparecen tasas o excusas, cero pagos adicionales, pruebas a salvo y active las vías bancarias y la denuncia cuanto antes.",
            ),
        ],
        "related": [
            ("../estafa-trading-broker/", "Estafa de trading y brókers"),
            ("../broker-no-deja-retirar/", "El bróker no me deja retirar"),
            ("../estafa-online/", "Estafa online: qué hacer"),
        ],
        "extra_sections": [
            (
                "Las cinco comprobaciones que no fallan, en orden",
                "<ol>"
                "<li><strong>CNMV:</strong> registros oficiales y lista de chiringuitos — el nombre exacto y el dominio</li>"
                "<li><strong>Regulador declarado:</strong> verificación en la web del regulador, no en el PDF que le envían</li>"
                "<li><strong>Dominio:</strong> antigüedad y clonación (¿meses de vida con «10 años de experiencia»?)</li>"
                "<li><strong>Retiro de prueba:</strong> antes de cualquier importe serio</li>"
                "<li><strong>Búsqueda inversa:</strong> dominio + «estafa», «withdrawal problem», «CNMV»</li>"
                "</ol>"
                "<p>Si una sola falla, la respuesta está dada. Las cinco juntas tardan menos de una hora — y es la hora mejor invertida antes de cualquier inversión.</p>",
            ),
            (
                "Si ya está dentro: verificar no es traicionar",
                "<p>Muchos afectados posponen la comprobación por miedo a confirmar sus sospechas — y la plataforma cuenta con ello. Haga el test hoy: solicite un retiro parcial por escrito y compruebe el dominio en la lista de chiringuitos de la CNMV. El resultado no empeora su situación; la documenta. Y esa documentación es exactamente lo que necesita para actuar antes de que cierren el telón.</p>",
            ),
        ],
        "source": "insights-es-broker-fiable",
    },
]

HUB_CARDS = [
    ("estafa-online/", "Ancla · Prioridad", "Estafa online", "Qué hacer, a quién acudir, denuncia (Policía Nacional / Guardia Civil) y chiringuito financiero.", "estafa online · qué hacer · a quién acudir · denuncia"),
    ("recuperar-dinero-estafa/", "Recuperación · Prioridad", "Recuperar dinero de una estafa", "Transferencia, tarjeta, Bizum y PayPal: el canal correcto según cómo pagó.", "recuperar dinero estafa · bizum · chargeback · transferencia"),
    ("estafa-trading-broker/", "Trading · Prioridad", "Estafa de trading y brókers", "Plataformas falsas, brókeres no regulados, lista de chiringuitos de la CNMV.", "estafa trading · estafa broker · bróker falso · cnmv"),
    ("estafa-criptomonedas/", "Cripto · Prioridad", "Estafa criptomonedas", "Recuperación realista, clones de exchange, Instagram/Telegram y deepfakes.", "estafa criptomonedas · recuperar bitcoin · estafa instagram"),
    ("broker-no-deja-retirar/", "Retiros · Prioridad", "Mi bróker no me deja retirar", "Retención de fondos, «impuestos» para retirar y los primeros 14 días.", "broker no deja retirar · retiro bloqueado · comisiones ocultas"),
    ("abogado-estafa-online/", "Abogado", "Abogado para estafa online", "Cuándo conviene, qué hace y cómo distinguirlo de una recovery room.", "abogado estafa online · abogado criptomonedas"),
    ("estafa-sentimental-criptomonedas/", "Romance", "Estafa sentimental y cripto", "Pig butchering, Tinder y cómo salir con las pruebas correctas.", "estafa sentimental · pig butchering · estafa tinder"),
    ("como-saber-si-un-broker-es-fiable/", "Prevención", "Cómo saber si un bróker es fiable", "La verificación de dos minutos: registro CNMV, clon vs original, señales.", "broker fiable · broker regulado · plataforma falsa"),
]


def page_html(g: dict) -> str:
    slug = g["slug"]
    canon = f"{SITE}/es/insights/{slug}/"
    contact = f"../../../index.html?source={escape(g['source'])}#contact"
    faq_ld = [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in g["faqs"]
    ]
    faq_html = "\n".join(
        f"<details{' open' if i == 0 else ''}><summary>{escape(q)}</summary><p>{escape(a)}</p></details>"
        for i, (q, a) in enumerate(g["faqs"])
    )
    all_sections = list(g["sections"]) + list(g.get("extra_sections", []))
    sections = "\n".join(f"<h2>{escape(h)}</h2>\n{body}" for h, body in all_sections)
    related = "\n".join(f'        <a href="{href}">{label}</a>' for href, label in g["related"])
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Inicio", "item": f"{SITE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Guías (ES)", "item": f"{SITE}/es/insights/"},
                    {"@type": "ListItem", "position": 3, "name": g["h1"], "item": canon},
                ],
            },
            {
                "@type": "Article",
                "headline": g["h1"],
                "description": g["desc"],
                "inLanguage": "es-ES",
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
<html lang="es-ES">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{escape(g["title"])}</title>
  <meta name="description" content="{escape(g["desc"])}" />
  <meta name="keywords" content="{escape(g["keywords"])}" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <meta name="author" content="Mike Levy Law" />
  <link rel="canonical" href="{canon}" />
  <link rel="alternate" hreflang="es" href="{canon}" />
  <link rel="alternate" hreflang="x-default" href="{canon}" />
  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="Mike Levy Law" />
  <meta property="og:locale" content="es_ES" />
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
      <nav class="crumbs" aria-label="Breadcrumb"><a href="../../../index.html">Inicio</a><span>/</span><a href="../">Guías</a><span>/</span><span>{escape(slug.replace("-", " "))}</span></nav>
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
      <h2 id="faq-h">Preguntas frecuentes</h2>
      <p class="faq-lead">Respuestas claras sobre próximos pasos, plazos y cuándo una valoración confidencial es útil.</p>
      <div class="faq">
{faq_html}
      </div>
    </section>
    <div class="cta-strip">
      <div>
        <strong>¿Solicitar una valoración confidencial?</strong>
        <p>{escape(FREE_LINE)}</p>
      </div>
      <a href="{contact}">Solicitar consulta</a>
    </div>
    <p class="note">Solo información. No constituye asesoramiento legal ni garantía de recuperación. El contacto no crea relación abogado-cliente.</p>
  </main>
  <footer class="site-footer">
    <div class="wrap-wide site-footer-inner">
      <p><a href="../">Guías (ES)</a> · <a href="../../../company-broker-index/">Índice de empresas y brókers</a> · <a href="{contact}">Contacto</a> · <a href="../../../legal/privacy-policy.html">Privacidad</a> · <a href="../../../legal/terms-of-use.html">Términos</a> · <a href="../../../legal/disclaimer.html">Aviso legal</a></p>
      <p>&copy; MLL 2026</p>
      <p class="footer-nap">1395 Brickell Ave, Suite 800 · Miami, FL 33131 · USA · <a href="mailto:info@mikelevylaw.com">info@mikelevylaw.com</a></p>
    </div>
  </footer>
  <script src="/js/tawk-mll.js" defer></script>
</body>
</html>
"""


def hub_html() -> str:
    canon = f"{SITE}/es/insights/"
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
                "name": "Guías sobre estafas online (Español)",
                "url": canon,
                "inLanguage": "es-ES",
                "description": "Guías en español sobre estafa online, estafa de trading, criptomonedas y recuperación de fondos: qué hacer, a quién acudir, abogado.",
                "hasPart": [
                    {"@type": "WebPage", "name": h2, "url": f"{SITE}/es/insights/{href}"}
                    for href, _t, h2, _p, _k in HUB_CARDS
                ],
            }
        ],
    }
    ld = json.dumps(graph, ensure_ascii=False)
    return f"""<!DOCTYPE html>
<html lang="es-ES">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Estafa online: guías, recuperar dinero y abogado | Mike Levy Law</title>
  <meta name="description" content="Estafa online, estafa de trading, estafa criptomonedas: recuperar dinero, a quién acudir, denuncia y abogado — guías en español de Mike Levy Law." />
  <meta name="keywords" content="estafa online, recuperar dinero estafa, estafa trading, estafa criptomonedas, abogado estafa online, denunciar estafa online, broker estafa, chiringuito financiero" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <meta name="author" content="Mike Levy Law" />
  <link rel="canonical" href="{canon}" />
  <link rel="alternate" hreflang="es" href="{canon}" />
  <link rel="alternate" hreflang="x-default" href="{canon}" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Mike Levy Law" />
  <meta property="og:locale" content="es_ES" />
  <meta property="og:title" content="Estafa online: guías, recuperar dinero y abogado | Mike Levy Law" />
  <meta property="og:description" content="Guías en español sobre estafa online, trading, criptomonedas y recuperación de fondos." />
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
      <nav class="crumbs" aria-label="Breadcrumb"><a href="../../index.html">Inicio</a><span>/</span><span>Guías (ES)</span></nav>
    </div>
  </header>
  <main class="wrap">
    <div class="hero">
      <p class="kicker">Guías · Español · Actualizado el {UPDATED}</p>
      <h1>Estafa online: recuperar dinero, denuncia y abogado</h1>
      <p class="lead">
        Empiece por su situación — <strong>recuperar dinero</strong>, <strong>qué hacer</strong>,
        <strong>a quién acudir</strong> o <strong>abogado</strong> — para estafa online, trading y
        criptomonedas. Escrito para claridad, no para promesas. Sin garantía de recuperación.
      </p>
    </div>

    <div class="folder-grid">
{cards}
    </div>
  </main>
  <footer class="site-footer">
    <div class="wrap-wide site-footer-inner">
      <p><a href="../../insights/">Insights (EN)</a> · <a href="../../de/insights/">Ratgeber (DE)</a> · <a href="../../it/insights/">Guide (IT)</a> · <a href="../../company-broker-index/">Índice de empresas y brókers</a> · <a href="../../index.html?source=insights-es-hub#contact">Contacto</a> · <a href="../../legal/privacy-policy.html">Privacidad</a> · <a href="../../legal/disclaimer.html">Aviso legal</a></p>
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
    print("Wrote es/insights/index.html")
    from depth_long import attach
    attach(GUIDES, "es")
    for g in GUIDES:
        dest = OUT / g["slug"]
        dest.mkdir(parents=True, exist_ok=True)
        path = dest / "index.html"
        path.write_text(page_html(g), encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT)}")
    print(f"Done — {len(GUIDES)} Spanish keyword guides + hub")


if __name__ == "__main__":
    main()
