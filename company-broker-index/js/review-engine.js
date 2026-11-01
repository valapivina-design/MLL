/* Mike Levy Law — review page engine
   Loads broker + comments by ?company=<slug>
   SEO: title/desc/keywords/og/twitter + BreadcrumbList/Article/FAQPage/HowTo (forensicsou pattern)
   FAQ: scam vs soft (legit) templates; Comments: TP + multilingual help; Support replies match lang
*/
(function () {
  var brokers = window.SBL_BROKERS || [];
  var commentsDB = window.SBL_COMMENTS || {};
  var params = new URLSearchParams(window.location.search);
  var hasCompanyParam = params.has("company") || params.has("slug");
  var slug = (params.get("company") || params.get("slug") || "").toLowerCase().trim();

  function findBroker(s) {
    for (var i = 0; i < brokers.length; i++) {
      if ((brokers[i].slug || "").toLowerCase() === s) return brokers[i];
    }
    return null;
  }

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function formatDate(iso) {
    if (!iso) return "";
    var d = new Date(iso + "T12:00:00");
    if (isNaN(d.getTime())) return iso;
    return d.toLocaleDateString("en-US", { day: "numeric", month: "short", year: "numeric" });
  }

  function resolveRisk(b) {
    var raw = (b && b.tags && b.tags.risk) || (b && b.risk) || "high";
    var r = String(raw).toLowerCase().trim();
    if (r === "low" || r === "medium" || r === "high") return r;
    return "high";
  }

  function riskClass(r) {
    if (r === "low") return "low";
    if (r === "medium") return "medium";
    return "high";
  }

  function riskLabel(r) {
    if (r === "low") return "Low Risk";
    if (r === "medium") return "Medium Risk";
    return "High Risk";
  }

  function setNeedle(risk) {
    var needle = document.getElementById("gauge-needle");
    if (!needle) return;
    // Gauge arc: low (left) → medium (top) → high (right)
    if (risk === "low") {
      needle.setAttribute("x2", "40");
      needle.setAttribute("y2", "55");
    } else if (risk === "medium") {
      needle.setAttribute("x2", "100");
      needle.setAttribute("y2", "28");
    } else {
      needle.setAttribute("x2", "168");
      needle.setAttribute("y2", "48");
    }
  }

  function asOfLabel(iso) {
    if (!iso) return DATE_LABEL;
    var d = new Date(String(iso).slice(0, 10) + "T12:00:00");
    if (isNaN(d.getTime())) return DATE_LABEL;
    return d.toLocaleDateString("en-US", { month: "long", year: "numeric" });
  }

  function applyRiskMeter(risk, updatedIso) {
    var label = document.getElementById("risk-label");
    var asof = document.getElementById("risk-asof");
    var wrap = document.getElementById("risk-gauge");
    if (label) {
      label.textContent = riskLabel(risk);
      label.className = "risk-label " + riskClass(risk);
    }
    setNeedle(risk);
    if (asof) {
      asof.textContent = updatedIso
        ? "As of " + formatDate(updatedIso)
        : "";
    }
    if (wrap) {
      wrap.setAttribute(
        "aria-label",
        "Risk score: " +
          riskLabel(risk) +
          (updatedIso ? ", as of " + formatDate(updatedIso) : "")
      );
    }
  }

  var SITE = "https://mikelevylaw.com";
  var YEAR = new Date().getFullYear();
  var DATE_LABEL = new Date().toLocaleDateString("en-US", {
    month: "long",
    year: "numeric",
  });
  var ORG = {
    "@type": ["Organization", "LegalService"],
    "@id": SITE + "/#organization",
    name: "Mike Levy Law",
    url: SITE + "/",
    email: "info@mikelevylaw.com",
    address: {
      "@type": "PostalAddress",
      streetAddress: "1395 Brickell Ave, Suite 800",
      addressLocality: "Miami",
      addressRegion: "FL",
      postalCode: "33131",
      addressCountry: "US",
    },
  };

  function reviewCanon(slug) {
    return SITE + "/company-broker-index/reviews/" + encodeURIComponent(slug) + ".html";
  }

  function scrubIndexed(s) {
    // Keyword rule: avoid “indexed” in visible page copy / badges
    return String(s == null ? "" : s).replace(/\bindexed\b/gi, "listed");
  }

  function dedupeKeywords(kw) {
    var parts = String(kw || "")
      .split(",")
      .map(function (p) {
        return p.trim();
      })
      .filter(Boolean);
    var seen = {};
    var out = [];
    for (var i = 0; i < parts.length; i++) {
      var key = parts[i].toLowerCase();
      if (seen[key]) continue;
      seen[key] = true;
      out.push(parts[i]);
    }
    return out.join(", ");
  }

  function clipDescription(desc, maxLen) {
    maxLen = maxLen || 160;
    var s = String(desc || "").replace(/\s+/g, " ").trim();
    if (s.length <= maxLen) return s;
    var cut = s.slice(0, maxLen - 1);
    var sp = cut.lastIndexOf(" ");
    if (sp > 100) cut = cut.slice(0, sp);
    return cut.replace(/[.,;:\s]+$/, "") + "…";
  }

  function setNoIndex() {
    setMeta(
      'meta[name="robots"]',
      "content",
      "noindex, follow"
    );
  }

  function isSoftTier(b) {
    var t = (b.tier || "").toLowerCase();
    if (t === "legit" || t === "clone") return true;
    if (t !== "scam" && (b.risk === "medium" || b.risk === "low")) return true;
    return false;
  }

  /** Blurbs that already read as full sentences should not follow "Name is …". */
  function blurbNeedsBreak(blurb) {
    var s = String(blurb || "").trim();
    if (!s) return false;
    if (/^[A-Z]/.test(s)) return true;
    if (/^Platform\b/i.test(s)) return true;
    if (/^(the|a|an)\s+[\w'-]+(?:\s+[\w'-]+){0,3}\s+is\b/i.test(s)) return true;
    return false;
  }

  function nameWithBlurbRaw(name, blurb, fallback) {
    var s = String(blurb || fallback || "").trim();
    if (!s) s = "a firm under review against publicly available records.";
    s = s.replace(/[.]+$/, "");
    if (blurbNeedsBreak(s)) return name + " — " + s;
    return name + " is " + s;
  }

  function nameWithBlurb(name, blurb, fallback) {
    return esc(nameWithBlurbRaw(name, blurb, fallback));
  }

  /** Name variants / rebrands — primary stays in H1; each alias gets H2 keyword blocks */
  function getAliases(b) {
    var raw = b.aliases || b.alsoKnownAs || [];
    if (!raw || !raw.length) return [];
    var primary = String(b.name || "").toLowerCase();
    var out = [];
    var seen = {};
    for (var i = 0; i < raw.length; i++) {
      var a = String(raw[i] || "").trim();
      if (!a) continue;
      var key = a.toLowerCase();
      if (key === primary || seen[key]) continue;
      seen[key] = true;
      out.push(a);
    }
    return out;
  }

  /**
   * Clone / lookalike sites attached to the brand.
   * Accepts strings ("fake-broker.com") or { domain, name, note }.
   */
  function getClones(b) {
    var raw = b.clones || [];
    if (!raw || !raw.length) return [];
    var out = [];
    var seen = {};
    for (var i = 0; i < raw.length; i++) {
      var item = raw[i];
      var domain = "";
      var name = "";
      var note = "";
      if (typeof item === "string") {
        domain = item.trim();
        name = domain;
      } else if (item && typeof item === "object") {
        domain = String(item.domain || item.host || "").trim();
        name = String(item.name || item.label || domain).trim();
        note = String(item.note || "").trim();
      }
      if (!domain) continue;
      var key = domain.toLowerCase();
      if (seen[key]) continue;
      seen[key] = true;
      out.push({ domain: domain, name: name || domain, note: note });
    }
    return out;
  }

  function officialDomain(b) {
    return (
      b.officialDomain ||
      b.domain ||
      (b.trustpilot && b.trustpilot.domain) ||
      ""
    );
  }

  function aliasKeywordChunk(alias) {
    var low = alias.toLowerCase();
    return (
      low +
      " review, is " +
      low +
      " a scam, is " +
      low +
      " legit, is " +
      low +
      " a legit broker, " +
      low +
      " scam, " +
      low +
      " complaints, report " +
      low
    );
  }

  function cloneKeywordChunk(clone) {
    var d = clone.domain.toLowerCase();
    var n = (clone.name || clone.domain).toLowerCase();
    return (
      d +
      " review, is " +
      d +
      " a scam, fake " +
      n +
      ", " +
      d +
      " clone, " +
      d +
      " scam, report " +
      d
    );
  }

  function buildKeywords(b, soft) {
    var low = String(b.name || "").toLowerCase();
    var dom = officialDomain(b);
    var kw;
    if (soft) {
      kw =
        low +
        " review, is " +
        low +
        " a scam, is " +
        low +
        " legit, is " +
        low +
        " a legit broker, " +
        low +
        " scam, " +
        low +
        " complaints, " +
        (dom ? dom + ", " : "") +
        low +
        " login, fake " +
        low +
        ", " +
        low +
        " clone, " +
        low +
        " support, report " +
        low;
    } else {
      kw =
        low +
        " review, is " +
        low +
        " a scam, is " +
        low +
        " legit, is " +
        low +
        " a legit broker, " +
        low +
        " scam, " +
        low +
        " complaints, " +
        low +
        " withdrawal, " +
        (dom ? dom + ", " : "") +
        low +
        " investigation, " +
        low +
        " reddit, report " +
        low;
    }
    var aliases = getAliases(b);
    for (var i = 0; i < aliases.length; i++) {
      kw += ", " + aliasKeywordChunk(aliases[i]);
    }
    var clones = getClones(b);
    for (var j = 0; j < clones.length; j++) {
      kw += ", " + cloneKeywordChunk(clones[j]);
    }
    if (b.kw_extra) kw += ", " + b.kw_extra;
    return kw;
  }

  function buildFaqs(b) {
    var n = b.name;
    var aliases = getAliases(b);
    var dom = officialDomain(b) || "the listed domain";
    var blurb = b.blurb || "a firm we have reviewed against publicly available records.";
    var soft = isSoftTier(b);
    var process = [
      "How does your process work?",
      "We begin with a confidential look at the date, how you paid, and any statements or screenshots you still have. We then compare that timeline with the public record and outline counsel, regulator, or reporting options. We do not replace your bank, card scheme, or the police.",
    ];
    var aliasFaqs = aliases.slice(0, 2).map(function (a) {
      return [
        "What is the connection between " + a + " and " + n + "?",
        a +
          " appears in materials connected with " +
          n +
          " — for example a prior brand, trading style, or name on paperwork. If your documents use either label, we review them as part of the same matter. Share the date and how you paid if you would like a confidential consultation.",
      ];
    });
    var clones = getClones(b);
    var off = officialDomain(b) || "the official domain you type yourself";
    var cloneFaqs = clones.slice(0, 3).map(function (c) {
      return [
        "What should I know about " + c.domain + "?",
        c.domain +
          " does not match the official " +
          n +
          " site (" +
          off +
          "). Sites that borrow a trusted name are a common risk. If you paid through " +
          c.domain +
          ", keep the URL, date, and payment method — that trail is what a consultation starts from.",
      ];
    });
    var faqs;
    if (soft) {
      faqs = [
        [
          "Is " + n + " a scam?",
          "We do not treat " +
            n +
            " as a fraud finding on this page alone. The firm appears in public records as a real business. Many complaints under this name still turn out to involve lookalike sites or ordinary service disputes — send the domain you used if you want that sorted confidentially.",
        ],
        [
          "Is " + n + " a legit broker?",
          "The company itself appears genuine. That is not the same as every website using the name. Type " +
            dom +
            " yourself and compare it character by character with any link you were sent.",
        ],
        [
          "Is " + n + " regulated?",
          b.tags && b.tags.regulator
            ? "Available records note: " +
              b.tags.regulator +
              ". Confirm the exact entity on your statement against the regulator’s public register."
            : "Confirm the entity named on your account agreement against the public register of the claimed regulator. A licence for one group company does not automatically cover another.",
        ],
        [
          "I lost money to someone claiming to be " + n + " — is that the real company?",
          "Often it is not. Impersonators borrow names, logos, even licence numbers. Keep every message, receipt, URL and wallet address, then contact us if you want next steps reviewed.",
        ],
        [
          "How do I check the " + n + " site I used is genuine?",
          "Type " +
            dom +
            " yourself — do not follow a link from an advert, email or message. If the domain differs by even one character, you were not dealing with the firm described on this page.",
        ],
        process,
      ];
    } else {
      faqs = [
        [
          "Is " + n + " a legit broker?",
          "A licence you verified yourself and a payout that reaches an account you own is one picture. A screen balance plus a new fee before you can leave is another. " +
            nameWithBlurbRaw(n, scrubIndexed(blurb)) +
            ". If you paid, share the date and method for a confidential consultation.",
        ],
        [
          "Can you close my " + n + " account, or have the person who phoned me call again?",
          "Mike Levy Law is not affiliated with this broker. We do not hold an account at " +
            dom +
            ". We cannot confirm a balance, close an account, or contact you as " +
            n +
            ".",
        ],
        [
          n + " says I must pay a tax or fee before withdrawing — should I?",
          "No. A genuine broker deducts fees from the balance. A fresh payment to “release” your own money is a second charge. Keep that message, then contact us if you want the file reviewed.",
        ],
        [
          "What do you do with what I send?",
          "We compare it with the public record on this page and advise on litigation and reporting pathways. We do not replace the bank, the card scheme, or the police. The first look is confidential.",
        ],
        process,
      ];
    }
    var extras = aliasFaqs.concat(cloneFaqs);
    if (extras.length) {
      faqs = [faqs[0]].concat(extras, faqs.slice(1));
    }
    return faqs;
  }

  function renderFaq(b) {
    var mount = document.getElementById("faq-list");
    if (!mount) return [];
    var faqs = buildFaqs(b);
    var html = "";
    for (var i = 0; i < faqs.length; i++) {
      html +=
        "<details" +
        (i === 0 ? " open" : "") +
        "><summary>" +
        esc(faqs[i][0]) +
        "</summary><p>" +
        esc(faqs[i][1]) +
        "</p></details>";
    }
    mount.innerHTML = html;
    return faqs;
  }

  function setMeta(sel, attr, value) {
    var el = document.querySelector(sel);
    if (!el) {
      var mName = sel.match(/^meta\[name="([^"]+)"\]$/i);
      var mProp = sel.match(/^meta\[property="([^"]+)"\]$/i);
      var l = sel.match(/^link\[rel="([^"]+)"\]$/i);
      if (mName) {
        el = document.createElement("meta");
        el.setAttribute("name", mName[1]);
        document.head.appendChild(el);
      } else if (mProp) {
        el = document.createElement("meta");
        el.setAttribute("property", mProp[1]);
        document.head.appendChild(el);
      } else if (l) {
        el = document.createElement("link");
        el.setAttribute("rel", l[1]);
        document.head.appendChild(el);
      }
    }
    if (el) el.setAttribute(attr, value);
  }

  function consultationUrl(companyName, companySlug, leadSource) {
    var q = new URLSearchParams();
    q.set("source", leadSource || "broker-review");
    if (companyName) q.set("company", companyName);
    if (companySlug) q.set("slug", companySlug);
    q.set("matter", "Broker / Investment Platform Dispute");
    return "../index.html?" + q.toString() + "#contact";
  }

  function renderComments(slugKey, companyName) {
    var mount = document.getElementById("reviews-grid");
    if (!mount) return;
    var brokerRow = findBroker(slugKey);
    var displayName = companyName || (brokerRow && brokerRow.name) || slugKey;
    var consultHref = consultationUrl(
      displayName,
      slugKey,
      "broker-support-reply"
    );
    var items = commentsDB[slugKey] || [];
    if (!items.length) {
      mount.innerHTML =
        '<p class="reviews-empty-soft">No public comments published for this profile yet.</p>';
      return;
    }
    var html = "";
    for (var i = 0; i < items.length; i++) {
      var c = items[i];
      if (
        (c.name || "").toLowerCase().indexOf("trustpilot") !== -1 ||
        (c.title || "").toLowerCase().indexOf("trustpilot") !== -1 ||
        (c.source === "trustpilot" && !c.askHelp)
      ) {
        continue; // research-only; never publish source labels on the page
      }
      var support = c.support;
      var lang = c.lang || "en";
      // Never show review-source platforms on the frontend
      html +=
        '<article class="review-card" lang="' +
        esc(lang) +
        '">' +
        '<div class="review-meta"><time datetime="' +
        esc(c.date) +
        '">' +
        esc(formatDate(c.date)) +
        "</time></div>" +
        '<h3 class="review-title">' +
        esc(c.title) +
        "</h3>" +
        '<p class="review-body">' +
        esc(c.text) +
        "</p>" +
        '<div class="review-author">' +
        '<div class="avatar">' +
        esc(c.initials || "?") +
        "</div>" +
        '<div class="review-author-text"><strong>' +
        esc(c.name) +
        "</strong><span>" +
        esc(c.country || "") +
        "</span></div></div>";

      if (support) {
        html +=
          '<div class="firm-reply" lang="' +
          esc(lang) +
          '">' +
          '<div class="firm-reply-head">' +
          '<div class="avatar firm">ML</div>' +
          "<div><strong>Mike Levy Law</strong><span>Support</span></div>" +
          "</div>" +
          "<p>" +
          esc(support.text) +
          "</p>" +
          '<a href="' +
          esc(consultHref) +
          '">' +
          esc(support.ctaLabel || "Contact us for a consultation →") +
          "</a></div>";
      }
      html += "</article>";
    }
    mount.innerHTML = html;
  }

  function applySeo(b) {
    var soft = isSoftTier(b);
    var n = b.name;
    var low = n.toLowerCase();
    var dom =
      officialDomain(b) ||
      b.domain ||
      (b.trustpilot && b.trustpilot.domain) ||
      "listed domain";
    var title;
    var desc;
    // Keyword rules: H1 / primary title signal = "{Name} Review".
    // Question pair (scam / legit broker) lives in meta description, H2s, FAQ.
    var asOf = asOfLabel(b.updated);
    if (soft) {
      title =
        n +
        " Review " +
        YEAR +
        " — Regulation, Complaints & Clone Warnings | Mike Levy Law";
      desc =
        n +
        " review (" +
        asOf +
        "): is " +
        n +
        " a scam? Is " +
        n +
        " a legit broker? Real company signals, clone warnings, complaints, and confidential consultation.";
    } else {
      title =
        n +
        " Review " +
        YEAR +
        " — Company & Broker Index | Mike Levy Law";
      desc =
        n +
        " review (" +
        asOf +
        "): is " +
        n +
        " a scam? Is " +
        n +
        " a legit broker? Assessment of " +
        dom +
        " — withdrawals, complaints, regulator checks, consultation.";
    }
    var aliases = getAliases(b);
    var clones = getClones(b);
    // Keep primary keyword pair first; append aliases only if room after clip
    var extra = "";
    if (aliases.length) {
      extra += " Also: " + aliases.slice(0, 3).join(", ") + ".";
    }
    if (clones.length) {
      extra +=
        " Lookalikes: " +
        clones
          .slice(0, 3)
          .map(function (c) {
            return c.domain;
          })
          .join(", ") +
        ".";
    }
    desc = clipDescription(desc + extra, 160);
    var kw = dedupeKeywords(buildKeywords(b, soft));
    var canon = reviewCanon(b.slug);
    var interactive =
      SITE +
      "/company-broker-index/review.html?company=" +
      encodeURIComponent(b.slug);
    var itemReviewed = { "@type": "Organization", name: n };
    if (dom && dom !== "listed domain") {
      itemReviewed.url = "https://" + String(dom).replace(/^https?:\/\//, "");
    }

    document.title = title;
    setMeta('meta[name="description"]', "content", desc);
    setMeta('meta[name="keywords"]', "content", kw);
    setMeta(
      'meta[name="robots"]',
      "content",
      "index, follow, max-image-preview:large"
    );
    setMeta('meta[name="author"]', "content", "Mike Levy Law");
    setMeta('link[rel="canonical"]', "href", canon);
    document.querySelectorAll('link[rel="alternate"][hreflang]').forEach(function (el) {
      el.setAttribute("href", canon);
    });
    setMeta('meta[property="og:type"]', "content", "article");
    setMeta('meta[property="og:site_name"]', "content", "Mike Levy Law");
    setMeta('meta[property="og:locale"]', "content", "en_US");
    setMeta('meta[property="og:title"]', "content", title);
    setMeta('meta[property="og:description"]', "content", desc);
    setMeta('meta[property="og:url"]', "content", canon);
    setMeta('meta[property="og:image"]', "content", SITE + "/hero-books.jpg");
    setMeta('meta[name="twitter:card"]', "content", "summary_large_image");
    setMeta('meta[name="twitter:title"]', "content", title);
    setMeta('meta[name="twitter:description"]', "content", desc);
    setMeta('meta[name="twitter:image"]', "content", SITE + "/hero-books.jpg");
    if (b.updated) {
      setMeta('meta[property="article:modified_time"]', "content", b.updated);
      setMeta('meta[property="article:published_time"]', "content", b.updated);
    }

    var faqs = renderFaq(b);
    var faqLd = faqs.map(function (qa) {
      return {
        "@type": "Question",
        name: qa[0],
        acceptedAnswer: { "@type": "Answer", text: qa[1] },
      };
    });
    var blurb = scrubIndexed(
      b.blurb || "a firm under review against publicly available records."
    );

    var ld = document.getElementById("seo-jsonld");
    if (ld) {
      ld.textContent = JSON.stringify({
        "@context": "https://schema.org",
        "@graph": [
          ORG,
          {
            "@type": "WebSite",
            "@id": SITE + "/#website",
            url: SITE + "/",
            name: "Mike Levy Law",
            publisher: { "@id": SITE + "/#organization" },
            inLanguage: "en-US",
          },
          {
            "@type": "BreadcrumbList",
            itemListElement: [
              {
                "@type": "ListItem",
                position: 1,
                name: "Home",
                item: SITE + "/",
              },
              {
                "@type": "ListItem",
                position: 2,
                name: "Company & Broker Index",
                item: SITE + "/company-broker-index/",
              },
              {
                "@type": "ListItem",
                position: 3,
                name: n + " Review",
                item: canon,
              },
            ],
          },
          {
            "@type": "WebPage",
            "@id": canon,
            url: canon,
            name: n + " Review",
            description: desc,
            isPartOf: { "@id": SITE + "/#website" },
            about: itemReviewed,
            inLanguage: "en-US",
            dateModified: b.updated || undefined,
            significantLink: interactive,
          },
          {
            "@type": "Article",
            headline: n + " Review",
            alternativeHeadline: title,
            description: desc,
            keywords: kw,
            inLanguage: "en-US",
            dateModified: b.updated || undefined,
            datePublished: b.updated || undefined,
            author: { "@id": SITE + "/#organization" },
            publisher: { "@id": SITE + "/#organization" },
            image: SITE + "/hero-books.jpg",
            mainEntityOfPage: { "@type": "WebPage", "@id": canon },
            about: itemReviewed,
            alternateName: aliases.length ? aliases : undefined,
            mentions: clones.length
              ? clones.map(function (c) {
                  return {
                    "@type": "WebSite",
                    name: c.name,
                    url: "https://" + c.domain.replace(/^https?:\/\//, ""),
                    description:
                      "Reported clone or lookalike domain associated with " + n,
                  };
                })
              : undefined,
          },
          {
            "@type": "Review",
            name: n + " Review",
            url: canon,
            dateModified: b.updated || undefined,
            author: { "@id": SITE + "/#organization" },
            publisher: { "@id": SITE + "/#organization" },
            itemReviewed: itemReviewed,
            reviewBody:
              n +
              " — " +
              blurb +
              " This page is informational and does not constitute a finding of liability.",
            inLanguage: "en-US",
          },
          {
            "@type": "FAQPage",
            mainEntity: faqLd,
          },
          {
            "@type": "HowTo",
            name: "Confidential consultation process",
            description:
              "How Mike Levy Law reviews a potential loss matter.",
            step: [
              {
                "@type": "HowToStep",
                position: 1,
                name: "Free initial look",
                text: "Send the date, how you paid, and any chat or screenshot.",
              },
              {
                "@type": "HowToStep",
                position: 2,
                name: "Record review",
                text: "We compare your timeline to the public record and available notices.",
              },
              {
                "@type": "HowToStep",
                position: 3,
                name: "Next-step advice",
                text: "We advise on counsel, regulator, or reporting pathways. We do not replace the bank or police.",
              },
            ],
          },
        ],
      });
    }
  }

  function extractInceptionYear(blurb) {
    var s = String(blurb || "");
    var patterns = [
      /(?:established|founded|launched|incorporated|formed|opened|started|since)\s+(?:in\s+)?((?:19|20)\d{2})/i,
      /((?:19|20)\d{2})[-\s]?(?:registered|vintage|founded)/i,
      /(?:registered|dating\s+from|operating\s+since)\s+(?:in\s+)?((?:19|20)\d{2})/i,
      /\b(?:est\.?|est)\s*((?:19|20)\d{2})\b/i,
    ];
    for (var i = 0; i < patterns.length; i++) {
      var m = s.match(patterns[i]);
      if (m) return m[1];
    }
    return "";
  }

  function extractReportsYear(blurb, updated) {
    var s = String(blurb || "");
    var patterns = [
      /(?:collapsed|collapse|bankruptcy|warning|alert|complaint|dissolved|unreachable|fee.?demand)[^\d]{0,48}((?:19|20)\d{2})/gi,
      /((?:19|20)\d{2})[^\d]{0,24}(?:collapse|bankruptcy|warning|alert|complaint)/gi,
    ];
    var years = [];
    for (var i = 0; i < patterns.length; i++) {
      var re = patterns[i];
      var m;
      while ((m = re.exec(s))) years.push(m[1]);
    }
    if (years.length) {
      years.sort();
      return years[0];
    }
    if (updated && /^\d{4}/.test(updated)) return updated.slice(0, 4);
    return String(YEAR);
  }

  function defaultTimeline(broker) {
    var updated = broker.updated || "";
    var when = formatDate(updated);
    var updYear = (updated || "").slice(0, 4) || String(YEAR);
    var risk = resolveRisk(broker);
    var blurb = scrubIndexed(broker.blurb || "");
    var inception = broker.inception || extractInceptionYear(blurb);
    var reports = String(
      broker.reportsStarted || extractReportsYear(blurb, updated)
    );
    var points = [];
    if (inception) {
      points.push({
        year: String(inception),
        event: "Inception / brand first appears in public materials",
        tone: "blue",
      });
    } else {
      points.push({
        year: "—",
        event: "Inception date not verified in sources reviewed",
        tone: "blue",
      });
    }
    var reportTone = risk === "high" ? "alert" : "brown";
    var reportEvent =
      risk === "high"
        ? "Public complaints / alerts appear in the record"
        : "Public reports and service complaints appear in the record";
    if (reports && inception && String(reports) === String(inception)) {
      points.push({
        year: String(reports),
        event: "Same period: public reports begin to surface",
        tone: reportTone,
      });
    } else {
      points.push({ year: String(reports), event: reportEvent, tone: reportTone });
    }
    points.push({
      year: updYear,
      event: "Brief last updated" + (when ? " · " + when : ""),
      tone: risk === "high" ? "alert" : "brown",
    });
    return points.slice(0, 3);
  }

  function renderTimeline(broker) {
    var tl = document.getElementById("timeline");
    var title = document.getElementById("timeline-panel-title");
    if (!tl) return;
    var curated = broker.timeline && broker.timeline.length >= 2;
    var points = curated ? broker.timeline : defaultTimeline(broker);
    if (title) {
      title.textContent = curated ? "Key events" : "Inception & reports";
    }
    tl.innerHTML = points
      .map(function (p) {
        var tone = p.tone || "blue";
        return (
          '<div class="t-point ' +
          esc(tone) +
          '"><div class="dot"></div><div class="year">' +
          esc(p.year) +
          '</div><div class="event">' +
          esc(p.event) +
          "</div></div>"
        );
      })
      .join("");
  }

  function parsePoints(str) {
    return String(str || "")
      .trim()
      .split(/\s+/)
      .map(function (pair) {
        var xy = pair.split(",");
        return { x: parseFloat(xy[0]), y: parseFloat(xy[1]) };
      })
      .filter(function (p) {
        return !isNaN(p.x) && !isNaN(p.y);
      });
  }

  function renderFundFlow(broker) {
    var flow = broker.fundFlow;
    var title = document.getElementById("fund-flow-panel-title");
    var noteEl = document.getElementById("fund-flow-note");
    var lineEl = document.getElementById("fund-flow-line");
    var peakEl = document.getElementById("fund-flow-peak");
    var endEl = document.getElementById("fund-flow-end");
    var svg = document.getElementById("fund-flow-svg");
    var labelEls = [
      document.getElementById("fund-flow-l0"),
      document.getElementById("fund-flow-l1"),
      document.getElementById("fund-flow-l2"),
    ];
    var xs = [40, 175, 275];

    function setLabels(labels) {
      for (var j = 0; j < 3; j++) {
        if (!labelEls[j]) continue;
        labelEls[j].textContent = labels[j] || "";
        labelEls[j].setAttribute("x", String(xs[j]));
      }
    }

    if (!flow || !flow.points) {
      // No curated series — do not invent multi-year fund history.
      if (title) title.textContent = "Record window";
      var when = formatDate(broker.updated) || asOfLabel(broker.updated);
      var yr = (broker.updated || "").slice(0, 4) || String(YEAR);
      if (lineEl) lineEl.setAttribute("points", "40,88 120,84 200,82 280,84 310,86");
      if (peakEl) {
        peakEl.setAttribute("cx", "200");
        peakEl.setAttribute("cy", "82");
      }
      if (endEl) {
        endEl.setAttribute("cx", "310");
        endEl.setAttribute("cy", "86");
      }
      setLabels([yr, when || yr, "Current"]);
      if (svg) {
        svg.setAttribute(
          "aria-label",
          "Record window for last profile update" +
            (when ? " on " + when : "")
        );
      }
      if (noteEl) {
        noteEl.hidden = false;
        noteEl.textContent =
          "No public fund-flow series on file. Date reflects the last profile update only — not creation date or AUM.";
      }
      return;
    }

    if (title) title.textContent = "Fund flow";
    var pts = parsePoints(flow.points);
    if (lineEl) lineEl.setAttribute("points", flow.points);

    if (pts.length) {
      var minY = pts[0];
      var last = pts[pts.length - 1];
      for (var i = 1; i < pts.length; i++) {
        if (pts[i].y < minY.y) minY = pts[i];
      }
      if (peakEl) {
        peakEl.setAttribute("cx", String(minY.x));
        peakEl.setAttribute("cy", String(minY.y));
      }
      if (endEl) {
        endEl.setAttribute("cx", String(last.x));
        endEl.setAttribute("cy", String(last.y));
      }
    }

    var labels = flow.labels || [];
    setLabels(labels);
    if (svg) {
      svg.setAttribute(
        "aria-label",
        "Fund flow chart" +
          (labels.length ? " · " + labels.join(" → ") : "")
      );
    }
    if (noteEl) {
      if (flow.note) {
        noteEl.hidden = false;
        noteEl.textContent = flow.note;
      } else {
        noteEl.hidden = true;
        noteEl.textContent = "";
      }
    }
  }

  function wireCommentForm(companyName, companySlug) {
    var companyEl = document.getElementById("comment-company");
    var slugEl = document.getElementById("comment-slug");
    var urlEl = document.getElementById("comment-page-url");
    if (companyEl) companyEl.value = companyName || "";
    if (slugEl) slugEl.value = companySlug || "";
    if (urlEl) urlEl.value = window.location.href;

    var caseCta = document.getElementById("request-case-review");
    if (caseCta) {
      caseCta.href = consultationUrl(
        companyName,
        companySlug,
        "broker-request-case-review"
      );
    }

    var form = document.getElementById("broker-comment-form");
    if (!form || form.dataset.wired === "1") return;
    form.dataset.wired = "1";

    var status = document.getElementById("comment-form-status");
    var btn = document.getElementById("comment-submit");

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (status) {
        status.textContent = "";
        status.className = "comment-form-status";
      }
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }
      if (btn) btn.disabled = true;
      if (status) status.textContent = "Sending…";

      fetch(form.action, {
        method: "POST",
        headers: { Accept: "application/json" },
        body: new FormData(form),
      })
        .then(function (res) {
          return res.json().then(function (data) {
            return { ok: res.ok, data: data };
          });
        })
        .then(function (result) {
          var data = result.data || {};
          if (result.ok && (data.code === 200 || data.status === "success")) {
            if (status) {
              status.className = "comment-form-status ok";
              status.textContent =
                "Thank you. Your comment was received and will be moderated before it appears live.";
            }
            form.reset();
            if (form.elements.form_type) form.elements.form_type.value = "comment";
            if (form.elements.lead_source)
              form.elements.lead_source.value = "broker-review-comment";
            if (companyEl) companyEl.value = companyName || "";
            if (slugEl) slugEl.value = companySlug || "";
            if (urlEl) urlEl.value = window.location.href;
          } else {
            if (status) {
              status.className = "comment-form-status err";
              status.textContent =
                (data && data.message) ||
                "We could not submit that comment. Please try again in a moment.";
            }
          }
        })
        .catch(function () {
          if (status) {
            status.className = "comment-form-status err";
            status.textContent =
              "No response from the form service. Please try again.";
          }
        })
        .finally(function () {
          if (btn) btn.disabled = false;
        });
    });
  }

  var broker = slug ? findBroker(slug) : null;

  if (!hasCompanyParam || !slug || !broker) {
    // Bare / unknown review URLs must not compete with real company pages in the index
    setNoIndex();
    document.title =
      (!hasCompanyParam || !slug
        ? "Select a Company Review"
        : "Profile Not Found") + " | Mike Levy Law";
    setMeta(
      'meta[name="description"]',
      "content",
      "Search the Mike Levy Law Company & Broker Index for a company or broker review. Each brief covers complaints, legitimacy questions, and confidential consultation options."
    );
    setMeta(
      'link[rel="canonical"]',
      "href",
      SITE + "/company-broker-index/"
    );
    var h1Missing = document.getElementById("seo-h1");
    if (h1Missing) {
      h1Missing.textContent =
        !hasCompanyParam || !slug
          ? "Company & Broker Review"
          : "Profile Not Found";
    }
    document.getElementById("company-name").textContent =
      !hasCompanyParam || !slug
        ? "Company & Broker Index"
        : slug
            .replace(/-/g, " ")
            .replace(/\b\w/g, function (c) {
              return c.toUpperCase();
            });
    document.getElementById("company-sub").textContent =
      !hasCompanyParam || !slug
        ? "Search the index to open a brief"
        : "No matching profile on file for this link";
    document.getElementById("status-badge").className = "verified-badge";
    document.getElementById("status-badge").innerHTML =
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg> On File';
    applyRiskMeter("medium", "");
    var riskAsofMissing = document.getElementById("risk-asof");
    if (riskAsofMissing) riskAsofMissing.textContent = "";
    var sum = document.querySelector(".summary");
    if (sum) {
      sum.innerHTML =
        "<strong>Summary:</strong> Use the <a href=\"./\" style=\"color:inherit;text-decoration:underline\">Company &amp; Broker Index</a> search to open a named review. Bare review links without a company parameter are not published as standalone pages.";
    }
    wireCommentForm("", "");
    return;
  }

  applySeo(broker);

  var h1 = document.getElementById("seo-h1");
  if (h1) h1.textContent = broker.name + " Review";

  document.getElementById("company-name").textContent = broker.name;
  var kind =
    broker.category === "online"
      ? "Online"
      : broker.category === "companies"
        ? "Company"
        : "Broker";
  var updatedFmt = formatDate(broker.updated);
  document.getElementById("company-sub").textContent =
    "Company profile · " +
    kind +
    (broker.location ? " · " + broker.location : "") +
    (updatedFmt ? " · Updated " + updatedFmt : "");

  var risk = resolveRisk(broker);
  applyRiskMeter(risk, broker.updated);

  var badge = document.getElementById("status-badge");
  if (risk === "high") {
    badge.className = "verified-badge flagged";
    badge.innerHTML =
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M12 9v4M12 17h.01"/><path d="M10.3 4.3L2.8 18a2 2 0 0 0 1.7 3h15a2 2 0 0 0 1.7-3L13.7 4.3a2 2 0 0 0-3.4 0z"/></svg> High Attention';
  } else {
    badge.className = "verified-badge";
    badge.innerHTML =
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg> On File';
  }

  var summary = document.querySelector(".summary");
  if (summary) {
    summary.innerHTML =
      "<strong>Summary:</strong> " +
      esc(broker.name) +
      " — " +
      esc(
        scrubIndexed(
          broker.blurb || "a firm under review against publicly available records."
        )
      ) +
      " This page is informational and does not constitute a finding of liability." +
      (updatedFmt
        ? " Profile last updated " + esc(updatedFmt) + "."
        : "");
  }

  renderTimeline(broker);
  renderFundFlow(broker);
  renderComments(broker.slug, broker.name);
  renderWriteup(broker);
  wireCommentForm(broker.name, broker.slug);

  function renderWriteup(b) {
    var mount = document.getElementById("seo-writeup");
    if (!mount) return;
    var n = b.name;
    var aliases = getAliases(b);
    var soft = isSoftTier(b);
    var dom = officialDomain(b) || "the domain associated with this brand";
    var loc = b.location || "its stated jurisdiction";
    var blurb = scrubIndexed(
      b.blurb ||
        "a trading or investment firm we have reviewed against publicly available records."
    );
    var html = "";
    if (soft) {
      html +=
        "<h2>About this " +
        esc(n) +
        " review</h2>" +
        "<p>" +
        esc(n) +
        " appears as a real business in the public records we examined. That does not mean every site using the name is genuine — lookalike domains and service complaints are often confused. This review helps separate a dispute with the real platform from impersonation, and when a confidential consultation may help. If you are asking whether " +
        esc(n) +
        " is a scam, or whether " +
        esc(n) +
        " is a legit broker, verify the domain character by character before any further deposits.</p>" +
        "<h2>Regulation and legitimacy</h2>" +
        "<p>" +
        nameWithBlurb(n, blurb) +
        ". Confirm the entity on your statements against the regulator’s register, and type <strong>" +
        esc(dom) +
        "</strong> yourself rather than following a message link. If the address differs by even one character, treat it as a different matter.</p>" +
        "<h2>Complaints and impersonation risk</h2>" +
        "<p>Reports about " +
        esc(n) +
        " often mix ordinary support issues with losses on fake sites that borrow the brand. Preserve chat logs, receipts, and URLs. We can review that paperwork confidentially and outline counsel or reporting options — we do not replace your bank or the police.</p>";
    } else {
      html +=
        "<h2>About this " +
        esc(n) +
        " review</h2>" +
        "<p>" +
        nameWithBlurb(n, blurb) +
        ". As of " +
        esc(asOfLabel(b.updated)) +
        ", public reporting linked to " +
        esc(dom) +
        " and activity associated with " +
        esc(loc) +
        " includes patterns such as stalled withdrawals, unexpected fee demands before payout, or similar friction. This page is a brief for research and intake — not a court judgment. Clients often ask whether " +
        esc(n) +
        " is a scam or a legitimate broker; the answer turns on the domain you used and the documents you still hold.</p>" +
        "<h2>Withdrawals, fees, and what to keep</h2>" +
        "<p>A licence you verified yourself and a payout that reaches an account you control is one picture. A dashboard balance plus a new “tax” or “compliance” payment before you can leave is another. If you paid through " +
        esc(dom) +
        ", retain the date, method, and any message that demanded an extra fee — those records matter more than the on-screen figure.</p>" +
        "<h2>If you cannot withdraw</h2>" +
        "<p>Accounts that allow a small test payout and then freeze larger requests are a recurring pattern in " +
        esc(n) +
        " complaint threads. If that matches your timeline, contact Mike Levy Law for a confidential consultation. We compare what you send with the public record and advise on litigation or reporting pathways.</p>";
    }
    if (aliases.length) {
      html +=
        "<h2>Related names and prior brands</h2>" +
        "<p>This review centres on <strong>" +
        esc(n) +
        "</strong>. The labels below also appear in filings, dashboards, or client paperwork connected with the same matter — for example a rebrand, trading style, or earlier corporate name. Unless a regulator treats them as separate entities, we review them together.</p>";
      for (var i = 0; i < aliases.length; i++) {
        var a = aliases[i];
        html +=
          "<h2>" +
          esc(a) +
          " review</h2>" +
          "<p>Materials referring to " +
          esc(a) +
          " are commonly part of the same " +
          esc(n) +
          " storyline — a predecessor brand, an alternate trading name, or wording still shown on statements. If you deposited under “" +
          esc(a) +
          "” or were told the business had moved to " +
          esc(n) +
          ", bring that paperwork to a consultation. Clients sometimes ask whether " +
          esc(a) +
          " is a scam, or whether " +
          esc(a) +
          " is a legit broker; the practical question is which domain took the funds and what evidence remains.</p>";
      }
    }
    var clones = getClones(b);
    var off = officialDomain(b);
    if (clones.length) {
      html +=
        "<h2>Lookalike domains</h2>" +
        "<p>Alongside related names, some websites imitate " +
        esc(n) +
        " branding. Those addresses are not the official site" +
        (off ? " (<strong>" + esc(off) + "</strong>)" : "") +
        ". Funds sent to a lookalike are a different problem from a dispute with the genuine platform.</p>";
      for (var j = 0; j < clones.length; j++) {
        var c = clones[j];
        html +=
          "<h2>" +
          esc(c.domain) +
          " review</h2>" +
          "<p>" +
          (c.name && c.name !== c.domain
            ? esc(c.name) + " (" + esc(c.domain) + ")"
            : esc(c.domain)) +
          " has been noted as a lookalike in connection with " +
          esc(n) +
          ". Always type the official address yourself" +
          (off ? " — " + esc(off) : "") +
          " — and compare it character by character. If you paid through " +
          esc(c.domain) +
          ", keep the URL, chat history, and payment trail" +
          (c.note ? ". " + esc(c.note) : "") +
          ". Where people ask whether " +
          esc(c.domain) +
          " is a scam, the safer working assumption is that any domain other than the official site warrants a careful review before further payments.</p>";
      }
    }
    mount.innerHTML = html;
  }
})();
