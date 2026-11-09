#!/usr/bin/env python3
"""Erzeugt die komplette Seite immoheute.at als statische HTML-Dateien.

Aufruf (im Ordner _quelle):  python3 build.py
Schreibt direkt in die Repository-Wurzel: Startseite, Rechner, Ratgeber, Rechtliches, sitemap.xml, llms.txt.
"""
import html, json, re, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "_quelle" / "ratgeber"
SITE = "https://immoheute.at"
NAME = "immoheute"
STAND = "2026-11-09"

# Reihenfolge = Reihenfolge auf der Übersicht
ARTIKEL = [
    dict(handle="immobilienertragsteuer",
         h1="Immobilienertragsteuer 2026: So berechnen Sie die ImmoESt",
         seo="Immobilienertragsteuer 2026 berechnen | immoheute",
         desc="ImmoESt in Österreich: 30 % vom Gewinn, Altvermögen 4,2 % (ab 2027 6 %), Hauptwohnsitzbefreiung, Erbschaft und Rechenbeispiele.",
         kurz="Neu- und Altvermögen, Befreiungen, Erbschaft und zwei Rechenbeispiele.",
         thema="Steuern", published=STAND, modified=STAND),
    dict(handle="immoest-2027-altvermoegen",
         h1="ImmoESt ab 2027: Altvermögen wird teurer – noch 2026 verkaufen?",
         seo="ImmoESt 2027: Altvermögen 6 % statt 4,2 % | immoheute",
         desc="Ab 1.1.2027 steigt die ImmoESt für Altvermögen von 4,2 % auf 6 %. Wer betroffen ist, was es in Euro kostet und ob sich ein Verkauf 2026 lohnt.",
         kurz="Was sich für Altvermögen ändert, wer betroffen ist und was ein Verkauf 2026 spart.",
         thema="Steuern", published=STAND, modified=STAND),
]

AUTOR = {"@type": "Person", "name": "Anton Scharmitzer", "honorificPrefix": "Mag.",
         "jobTitle": "Herausgeber, Betriebswirt", "url": f"{SITE}/impressum/"}
ORG = {"@type": "Organization", "@id": f"{SITE}/#organization", "name": "immoheute", "url": f"{SITE}/",
       "logo": f"{SITE}/icon.svg", "description": "Unabhängiger Ratgeber für private Immobilienverkäufer in Österreich.",
       "areaServed": {"@type": "Country", "name": "Österreich"}}
WEBSITE = {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/", "name": "immoheute",
           "inLanguage": "de-AT", "publisher": {"@id": f"{SITE}/#organization"}}

LOGO = ('<svg width="34" height="34" viewBox="0 0 34 34" aria-hidden="true"><rect width="34" height="34" rx="9" fill="var(--accent)"/>'
        '<path d="M8 17l9-7 9 7M11 15.5V25h12v-9.5M15 25v-5h4v5" fill="none" stroke="var(--accent-ink)" stroke-width="2.2" '
        'stroke-linecap="round" stroke-linejoin="round"/></svg>')

def header(current=""):
    def a(href, text):
        cur = ' aria-current="page"' if href == current else ""
        return f'<a href="{href}"{cur}>{text}</a>'
    return ('<header class="site"><div class="w">'
            f'<a class="logo" href="/">{LOGO}<span>immoheute<span style="color:var(--accent)">.at</span></span></a>'
            '<nav class="main" aria-label="Hauptnavigation">'
            + a("/ratgeber/", "Ratgeber") + a("/immoest-rechner/", "ImmoESt-Rechner") + a("/#fragen", "Häufige Fragen")
            + '</nav></div></header>')

FOOTER = ('<footer class="site"><div class="w"><p>immoheute.at bietet allgemeine Informationen rund um den privaten Immobilienverkauf in Österreich. '
          'Die Inhalte ersetzen keine Steuer- oder Rechtsberatung. © 2026 immoheute.at</p>'
          '<nav aria-label="Fußzeile"><a href="/ratgeber/">Ratgeber</a><a href="/immoest-rechner/">ImmoESt-Rechner</a>'
          '<a href="/impressum/">Impressum</a><a href="/datenschutz/">Datenschutz</a></nav>'
          '</div></footer>')

def head(title, desc, url, ogtype, graph, robots="index, follow, max-snippet:-1, max-image-preview:large", extra=""):
    ld = ""
    if graph:
        ld = ('<script type="application/ld+json">\n'
              + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False) + "\n</script>")
    return f"""<!doctype html>
<html lang="de-AT">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#0E5A52">
<link rel="icon" href="/icon.svg" type="image/svg+xml">
<link rel="preload" href="/fonts/pjs.woff2" as="font" type="font/woff2" crossorigin>
<meta property="og:type" content="{ogtype}">
<meta property="og:locale" content="de_AT">
<meta property="og:site_name" content="immoheute">
<meta property="og:title" content="{html.escape(title.replace(' | immoheute', ''))}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/styles.css">
{extra}{ld}
</head>"""

def seite(title, desc, path, graph, body, current="", ogtype="website", robots=None, extra=""):
    url = SITE + path
    kw = {} if robots is None else {"robots": robots}
    return head(title, desc, url, ogtype, graph, extra=extra, **kw) + f"""
<body>
{header(current)}
<main>
{body}
</main>
{FOOTER}
</body>
</html>
"""

def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()

def faq_aus(body):
    teil = body.split("<h2>Häufige Fragen</h2>", 1)
    if len(teil) < 2:
        raise SystemExit("FAQ-Abschnitt fehlt")
    faq_html = teil[1].split("<h2", 1)[0]
    paare = re.findall(r"<h3>(.*?)</h3>\s*<p>(.*?)</p>", faq_html, re.S)
    if not 3 <= len(paare) <= 6:
        raise SystemExit(f"FAQ braucht 3–6 Fragen, gefunden {len(paare)}")
    return [(strip_tags(q), strip_tags(a)) for q, a in paare]

def toc_aus(body):
    eintraege, n = [], 0
    def ersetze(m):
        nonlocal n
        attrs, text = m.group(1), m.group(2)
        if 'id="' in attrs:
            hid = re.search(r'id="([^"]+)"', attrs).group(1)
        else:
            n += 1
            hid = "a" + str(n)
            attrs = f' id="{hid}"' + attrs
        if strip_tags(text) not in ("Quellen",):
            eintraege.append((hid, strip_tags(text)))
        return f"<h2{attrs}>{text}</h2>"
    body = re.sub(r"<h2([^>]*)>(.*?)</h2>", ersetze, body)
    return body, eintraege

def datum(iso):
    d = datetime.date.fromisoformat(iso)
    monate = ["Jänner", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
    return f"{d.day}. {monate[d.month-1]} {d.year}"

def crumbs(*teile):
    out = ['<a href="/">Startseite</a>']
    for href, text in teile:
        out.append(f'<a href="{href}">{text}</a>' if href else text)
    return '<nav class="crumbs" aria-label="Brotkrumen">' + " › ".join(out) + "</nav>"

def breadcrumb_ld(*teile):
    items = [{"@type": "ListItem", "position": 1, "name": "Startseite", "item": f"{SITE}/"}]
    for i, (name, path) in enumerate(teile, start=2):
        items.append({"@type": "ListItem", "position": i, "name": name, "item": SITE + path})
    return {"@type": "BreadcrumbList", "itemListElement": items}

# ---------- Ratgeber ----------

def artikel_seite(a, alle):
    path = f"/ratgeber/{a['handle']}/"
    url = SITE + path
    body = (SRC / f"{a['handle']}.html").read_text(encoding="utf-8")
    faqs = faq_aus(body)
    body, toc = toc_aus(body)
    erster = strip_tags(re.search(r"<p>(.*?)</p>", body, re.S).group(1)).replace("Die kurze Antwort:", "").strip()
    kurz_titel = a["h1"].split(":")[0]
    graph = [
        {"@type": "Article", "@id": url + "#article", "headline": a["h1"], "description": a["desc"],
         "inLanguage": "de-AT", "datePublished": a["published"], "dateModified": a["modified"],
         "author": AUTOR, "publisher": {"@id": f"{SITE}/#organization"},
         "mainEntityOfPage": url, "image": f"{SITE}/og.png", "abstract": erster,
         "about": {"@type": "Thing", "name": kurz_titel},
         "spatialCoverage": {"@type": "Country", "name": "Österreich"}},
        ORG,
        breadcrumb_ld(("Ratgeber", "/ratgeber/"), (kurz_titel, path)),
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in faqs]},
    ]
    toc_html = "".join(f'<li><a href="#{i}">{html.escape(t)}</a></li>' for i, t in toc)
    weitere = "".join(
        f'<li><a href="/ratgeber/{b["handle"]}/">{html.escape(b["h1"])}</a><span>{html.escape(b["kurz"])}</span></li>'
        for b in alle if b["handle"] != a["handle"])
    inhalt = f"""<div class="w narrow art">
{crumbs(("/ratgeber/", "Ratgeber"))}
<p class="eyebrow">Ratgeber · {html.escape(a['thema'])}</p>
<h1>{html.escape(a['h1'])}</h1>
<p class="meta">Geprüft am {datum(a['modified'])} · Von Mag. Anton Scharmitzer</p>
<details class="toc"><summary>Inhalt</summary><ol>{toc_html}</ol></details>
<div class="prose">
{body}
<div class="autor"><p><strong>Über diesen Ratgeber:</strong> Herausgegeben von Mag. Anton Scharmitzer, Betriebswirt (Studium der Internationalen Betriebswirtschaft an der Universität Wien). Alle Zahlen und Fristen sind an den verlinkten Quellen mit Stand-Datum geprüft. Dieser Ratgeber ersetzt keine Steuer- oder Rechtsberatung. Für Ihren Einzelfall wenden Sie sich an eine Steuerberaterin, einen Notar oder eine Rechtsanwältin.</p></div>
</div>
<aside class="tools-box"><p class="eyebrow">Kostenloses Werkzeug</p><div class="row"><a class="btn primary" href="/immoest-rechner/">ImmoESt berechnen</a></div></aside>
<section class="weiter"><h2>Weitere Ratgeber</h2><ul>{weitere}</ul></section>
{newsletter_box(path)}
</div>"""
    return seite(a["seo"], a["desc"], path, graph, inhalt, current="/ratgeber/", ogtype="article")

def uebersicht(alle):
    path = "/ratgeber/"
    graph = [
        {"@type": "CollectionPage", "@id": SITE + path, "url": SITE + path, "name": "Ratgeber Immobilie verkaufen in Österreich",
         "inLanguage": "de-AT", "isPartOf": {"@id": f"{SITE}/#website"},
         "hasPart": [{"@type": "Article", "headline": a["h1"], "url": f"{SITE}/ratgeber/{a['handle']}/"} for a in alle]},
        breadcrumb_ld(("Ratgeber", path)),
    ]
    karten = "".join(
        f'<a class="card rg" href="/ratgeber/{a["handle"]}/"><p class="num">{html.escape(a["thema"])}</p>'
        f'<h2>{html.escape(a["h1"])}</h2><p>{html.escape(a["kurz"])}</p></a>' for a in alle)
    inhalt = f"""<div class="w pad-s">
{crumbs((None, "Ratgeber"))}
<p class="eyebrow">Ratgeber</p>
<h1>Immobilie verkaufen in Österreich</h1>
<p class="lead">Jede Antwort steht im ersten Absatz, jede Zahl ist an der Quelle geprüft und mit Stand-Datum versehen. Nur österreichisches Recht.</p>
<div class="grid4">{karten}</div>
<p style="margin:24px 0 0;font-size:14px;color:var(--muted)">Weitere Ratgeber zu Bewertung, Verkauf ohne Makler, Erbe und Trennung erscheinen laufend.</p>
</div>"""
    return seite("Ratgeber Immobilie verkaufen Österreich | immoheute",
                 "Ratgeber für private Immobilienverkäufer in Österreich: Immobilienertragsteuer, Altvermögen ab 2027, Befreiungen. Mit Quellen und Stand-Datum.",
                 path, graph, inhalt, current="/ratgeber/")

# ---------- Startseite ----------

FAQ_START = [
    ("Wie viel Steuer zahle ich beim Verkauf einer Wohnung in Österreich?",
     "In der Regel 30 % Immobilienertragsteuer auf den Gewinn. Bei Altvermögen (meist vor dem 31. März 2002 gekauft) sind es pauschal 4,2 % des Verkaufspreises, bei Verkäufen ab 1. Jänner 2027 6 %."),
    ("Wann ist der Verkauf meines Hauses steuerfrei?",
     "Wenn es seit dem Kauf mindestens zwei Jahre durchgehend oder in den letzten zehn Jahren mindestens fünf Jahre durchgehend Ihr Hauptwohnsitz war und Sie diesen aufgeben. Grund über 1.000 m² ist anteilig steuerpflichtig."),
    ("Muss ich für eine geerbte Immobilie Steuer zahlen?",
     "Für das Erbe selbst fällt keine Immobilienertragsteuer an. Verkaufen Sie die Immobilie später, zählen Kaufzeitpunkt und Anschaffungskosten der verstorbenen Person."),
    ("Was ändert sich 2027 bei der Immobilienertragsteuer?",
     "Für Altvermögen steigt die Pauschalsteuer bei Verkäufen nach dem 31. Dezember 2026 von 4,2 % auf 6 % des Verkaufspreises, bei Umwidmung nach 1987 von 18 % auf 21 %. Der Steuersatz von 30 % auf Gewinne bei Neuvermögen bleibt."),
    ("Wer berechnet die Immobilienertragsteuer?",
     "In der Regel die Notarin oder der Rechtsanwalt, der den Kaufvertrag abwickelt. Die Steuer wird im Rahmen der Selbstberechnung an das Finanzamt abgeführt."),
]

def startseite():
    graph = [ORG, WEBSITE,
             {"@type": "WebPage", "@id": f"{SITE}/#webpage", "url": f"{SITE}/", "name": "Immobilie verkaufen in Österreich",
              "inLanguage": "de-AT", "isPartOf": {"@id": f"{SITE}/#website"}, "dateModified": STAND,
              "mainEntity": {"@id": f"{SITE}/#faq"}},
             {"@type": "FAQPage", "@id": f"{SITE}/#faq", "inLanguage": "de-AT", "mainEntity": [
                 {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ_START]}]
    faq_html = "".join(
        f'<details class="faq"{" open" if i == 0 else ""}><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>'
        for i, (q, a) in enumerate(FAQ_START))
    karten = "".join(
        f'<a class="card rg" href="/ratgeber/{a["handle"]}/"><p class="num">{html.escape(a["thema"])}</p>'
        f'<h2>{html.escape(a["h1"])}</h2><p>{html.escape(a["kurz"])}</p></a>' for a in ARTIKEL)
    inhalt = f"""<section class="hero"><div class="w">
<div class="text">
<p class="eyebrow">Ratgeber für private Eigentümer in Österreich</p>
<h1>Wohnung oder Haus verkaufen. Ohne teure Fehler.</h1>
<p class="lead">Für alle, die geerbt haben, sich nach einer Trennung neu ordnen oder sich verkleinern: was beim Verkauf auf Sie zukommt, welche Steuer anfällt und welche Unterlagen Sie brauchen.</p>
<div class="row"><a class="btn primary" href="/immoest-rechner/">ImmoESt gratis berechnen</a><a class="btn ghost" href="/ratgeber/">Zu den Ratgebern</a></div>
<div class="ticks"><span>✓ Österreichisches Recht</span><span>✓ Quellen bei jeder Antwort</span><span>✓ Stand: November 2026</span></div>
</div>
<div class="panel">
<p class="eyebrow" style="margin-bottom:6px">Wichtig für 2026</p>
<h2>Altvermögen: Ab 2027 steigt die Steuer</h2>
<p style="margin:0 0 16px;color:var(--body)">Wer eine Immobilie verkauft, die vor dem 31. März 2002 gekauft wurde, zahlt bis Jahresende 4,2 % des Verkaufspreises. Ab 1. Jänner 2027 sind es 6 %. Das betrifft auch viele geerbte Elternhäuser.</p>
<div style="display:flex;flex-direction:column;gap:10px">
<a class="choice" href="/ratgeber/immoest-2027-altvermoegen/"><span><strong>Was die Änderung für Sie bedeutet</strong><small>Tabelle in Euro, wer betroffen ist</small></span><span aria-hidden="true">›</span></a>
<a class="choice" href="/immoest-rechner/"><span><strong>2026 und 2027 vergleichen</strong><small>Mit dem ImmoESt-Rechner</small></span><span aria-hidden="true">›</span></a>
</div>
</div>
</div></section>

<section id="lebenslagen"><div class="w pad">
<p class="eyebrow">Ihre Situation</p>
<h2 class="h2">Warum Sie verkaufen, bestimmt, worauf es ankommt</h2>
<p class="lead">Die Steuerregeln sind dieselben, die Fallstricke nicht.</p>
<div class="grid4">
<article class="card phase"><p class="num">Erbe</p><h3>Geerbte Immobilie</h3><p>Für die Steuer zählt der Kauf durch die verstorbene Person. Vor 2002 gekauft heißt meist: Altvermögen.</p><ul><li><a href="/ratgeber/immobilienertragsteuer/">ImmoESt bei geerbten Immobilien</a></li><li><a href="/ratgeber/immoest-2027-altvermoegen/">Elternhaus noch 2026 verkaufen?</a></li></ul></article>
<article class="card phase"><p class="num">Trennung</p><h3>Verkauf nach der Scheidung</h3><p>Übernimmt ein Ehegatte die Immobilie, tritt er in die Anschaffungskosten ein. Verkauft wird erst später.</p><ul><li><a href="/ratgeber/immobilienertragsteuer/">Steuer beim späteren Verkauf</a></li><li>Immobilie bei Scheidung: verkaufen oder übernehmen (in Arbeit)</li></ul></article>
<article class="card phase"><p class="num">Verkleinern</p><h3>Eigenheim verkaufen</h3><p>War die Immobilie lange genug Ihr Hauptwohnsitz, ist der Verkauf meist steuerfrei.</p><ul><li><a href="/ratgeber/immobilienertragsteuer/#a6">Hauptwohnsitzbefreiung</a></li><li>Unterlagen-Checkliste (in Arbeit)</li></ul></article>
<article class="card phase"><p class="num">Anlage</p><h3>Vermietete Wohnung</h3><p>Hier fällt fast immer ImmoESt an. Belege für Kaufnebenkosten und Sanierungen senken die Steuer.</p><ul><li><a href="/ratgeber/immobilienertragsteuer/#a3">So wird der Gewinn berechnet</a></li><li><a href="/immoest-rechner/">ImmoESt berechnen</a></li></ul></article>
</div>
</div></section>

<section id="werkzeuge"><div class="w pad-s">
<p class="eyebrow">Kostenloses Werkzeug</p>
<h2 class="h2" style="margin-bottom:40px">Klarheit in zwei Minuten</h2>
<div class="tools">
<div class="tool-hero"><h3>ImmoESt-Rechner</h3><p>Immobilienertragsteuer für Neu- und Altvermögen, mit Umwidmung, Hauptwohnsitzbefreiung und dem Vergleich Verkauf 2026 oder 2027. Mit vollständigem Rechenweg.</p><a class="btn" href="/immoest-rechner/">Jetzt berechnen</a></div>
<div class="tool-list">
<div class="card tool"><div><h3>Ratgeber mit Quellen</h3><p>Jede Zahl ist an der Quelle geprüft und mit Datum versehen.</p><a href="/ratgeber/" style="font-weight:700;font-size:15px">Zu den Ratgebern</a></div></div>
<div class="card tool"><div><h3>Häufige Fragen</h3><p>Steuer, Befreiungen, Erbe und die Änderung 2027 in kurzen Antworten.</p><a href="#fragen" style="font-weight:700;font-size:15px">Zu den Antworten</a></div></div>
</div>
</div>
</div></section>

<section><div class="w pad-s">
<p class="eyebrow">Neueste Ratgeber</p>
<h2 class="h2" style="margin-bottom:28px">Gründlich statt oberflächlich</h2>
<div class="grid4">{karten}</div>
</div></section>

<section><div class="w narrow pad-s">{newsletter_box("/")}</div></section>

<section id="fragen" aria-labelledby="faq-titel"><div class="w narrow pad">
<p class="eyebrow">Häufige Fragen</p>
<h2 id="faq-titel" class="h2" style="margin-bottom:32px">Immobilie verkaufen: die wichtigsten Antworten</h2>
<div style="display:flex;flex-direction:column;gap:12px">{faq_html}</div>
<p style="margin:16px 0 0;font-size:14px;color:var(--muted)">Quellen: Einkommensteuergesetz §§ 30–30c, Budgetbegleitgesetz 2027–2028. Details und Links in den <a href="/ratgeber/">Ratgebern</a>. Zuletzt geprüft: November 2026.</p>
</div></section>"""
    return seite("Immobilie verkaufen Österreich: Steuer & Ablauf | immoheute",
                 "Wohnung oder Haus in Österreich verkaufen: Immobilienertragsteuer, Altvermögen ab 2027, Hauptwohnsitzbefreiung, Erbe. Mit gratis ImmoESt-Rechner.",
                 "/", graph, inhalt, current="/")

# ---------- Rechner ----------

RECHNER_JS = r"""
<script>
(function(){
  'use strict';
  var eur = new Intl.NumberFormat('de-AT',{style:'currency',currency:'EUR',maximumFractionDigits:0});
  function zahl(id){ var v = parseFloat(String(document.getElementById(id).value).replace(/\./g,'').replace(',','.')); return isFinite(v) && v > 0 ? v : 0; }
  function wert(name){ var el = document.querySelector('input[name="'+name+'"]:checked'); return el ? el.value : ''; }

  // Kernberechnung ohne DOM
  function berechne(e){
    var schritte = [], hinweise = [];
    if (e.hws === 'ja') {
      return {steuer:0, schritte:['Hauptwohnsitzbefreiung: Der Verkauf ist steuerfrei.'],
              hinweise:['Grund und Boden über 1.000 m² ist anteilig steuerpflichtig. Den Hauptwohnsitz müssen Sie aufgeben.'], sub:'steuerfrei (Hauptwohnsitzbefreiung)'};
    }
    var ab2027 = e.jahr === '2027';
    var gewinn;
    if (e.art === 'alt') {
      var anteil = e.umw === 'keine' ? (ab2027 ? 0.20 : 0.14) : (ab2027 ? 0.70 : 0.60);
      gewinn = e.preis * anteil;
      schritte.push('Altvermögen: ' + Math.round(anteil*100) + ' % des Verkaufspreises gelten als Gewinn: ' + eur.format(gewinn));
      hinweise.push('Auf Antrag kann der Gewinn auch nach den allgemeinen Regeln (Verkaufspreis minus tatsächliche Anschaffungskosten) ermittelt werden. Das lohnt sich nur bei geringem Wertzuwachs.');
    } else {
      gewinn = Math.max(0, e.preis - e.ak - e.inv);
      schritte.push('Gewinn: ' + eur.format(e.preis) + ' − ' + eur.format(e.ak) + ' Anschaffungskosten − ' + eur.format(e.inv) + ' Sanierung/Zubau = ' + eur.format(gewinn));
    }
    if (e.umw === '2024') {
      var mit = Math.min(e.preis, gewinn * 1.3);
      schritte.push('Umwidmungszuschlag (+30 %, höchstens bis zum Verkaufspreis): ' + eur.format(mit));
      gewinn = mit;
    }
    var steuer = gewinn * 0.30;
    schritte.push('30 % Immobilienertragsteuer: ' + eur.format(steuer));
    var sub = e.preis > 0 ? ('entspricht ' + (steuer / e.preis * 100).toLocaleString('de-AT',{maximumFractionDigits:1}) + ' % des Verkaufspreises') : '';
    return {steuer:steuer, schritte:schritte, hinweise:hinweise, sub:sub};
  }

  function lesen(){
    return {preis:zahl('preis'), art:wert('art'), jahr:wert('jahr'), umw:document.getElementById('umw').value,
            hws:wert('hws'), ak:zahl('ak'), inv:zahl('inv')};
  }

  function zeigen(){
    var e = lesen();
    document.getElementById('neuFelder').hidden = e.art !== 'neu';
    var r = berechne(e);
    document.getElementById('total').textContent = eur.format(r.steuer);
    document.getElementById('totalSub').textContent = r.sub;
    document.getElementById('steps').innerHTML = r.schritte.map(function(s){ return '<li>' + s + '</li>'; }).join('');
    var vgl = '';
    if (e.art === 'alt' && e.hws !== 'ja') {
      var a = berechne(Object.assign({}, e, {jahr:'2026'})), b = berechne(Object.assign({}, e, {jahr:'2027'}));
      vgl = '<p><strong>Verkauf 2026:</strong> ' + eur.format(a.steuer) + ' · <strong>ab 2027:</strong> ' + eur.format(b.steuer) +
            ' · Unterschied: ' + eur.format(b.steuer - a.steuer) + '</p>';
    }
    document.getElementById('vergleich').innerHTML = vgl;
    document.getElementById('notes').innerHTML = r.hinweise.map(function(h){ return '<p class="hint" style="margin-top:10px">' + h + '</p>'; }).join('');
  }
  document.getElementById('calc').addEventListener('input', zeigen);
  document.getElementById('calc').addEventListener('change', zeigen);
  document.getElementById('calc').addEventListener('submit', function(ev){ ev.preventDefault(); zeigen(); });
  zeigen();
  window.immoest = berechne;
})();
</script>"""

def rechner():
    path = "/immoest-rechner/"
    graph = [ORG,
             {"@type": "WebApplication", "name": "ImmoESt-Rechner Österreich", "url": SITE + path,
              "applicationCategory": "FinanceApplication", "operatingSystem": "Web", "inLanguage": "de-AT",
              "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
              "description": "Berechnet die Immobilienertragsteuer in Österreich für Neu- und Altvermögen, mit Umwidmung, Hauptwohnsitzbefreiung und Vergleich 2026/2027."},
             breadcrumb_ld(("ImmoESt-Rechner", path))]
    inhalt = f"""<div class="w pad-s">
{crumbs((None, "ImmoESt-Rechner"))}
<p class="eyebrow">ImmoESt-Rechner · Stand November 2026</p>
<h1 style="font-size:clamp(32px,4.4vw,48px)">Immobilienertragsteuer berechnen</h1>
<p class="lead">Für Wohnung, Haus oder Grundstück in Österreich. Das Beispiel ist vorausgefüllt – ändern Sie einfach die Werte. Ihre Eingaben bleiben in Ihrem Browser.</p>
<div class="calc">
<form id="calc" novalidate>
<div class="card">
<div class="field"><label for="preis">Verkaufspreis</label><input id="preis" type="text" inputmode="decimal" value="400000"></div>
<div class="field"><span class="label" id="l-hws">War die Immobilie Ihr Hauptwohnsitz?</span>
<div class="seg" role="radiogroup" aria-labelledby="l-hws"><label><input type="radio" name="hws" value="nein" checked> Nein</label><label><input type="radio" name="hws" value="ja"> Ja, 2 Jahre seit Kauf oder 5 der letzten 10 Jahre durchgehend</label></div></div>
<div class="field"><span class="label" id="l-art">Wann wurde die Immobilie zuletzt gekauft?</span>
<p class="hint">Bei Erbe oder Schenkung zählt der Kauf durch die Vorbesitzerin oder den Vorbesitzer.</p>
<div class="seg" role="radiogroup" aria-labelledby="l-art"><label><input type="radio" name="art" value="alt" checked> Vor dem 31. März 2002 (Altvermögen)</label><label><input type="radio" name="art" value="neu"> Danach (Neuvermögen)</label></div></div>
<div class="field"><span class="label" id="l-jahr">Wann verkaufen Sie?</span>
<div class="seg" role="radiogroup" aria-labelledby="l-jahr"><label><input type="radio" name="jahr" value="2026" checked> Bis 31. Dezember 2026</label><label><input type="radio" name="jahr" value="2027"> Ab 1. Jänner 2027</label></div></div>
<div class="field"><label for="umw">Wurde der Grund in Bauland umgewidmet?</label>
<select id="umw"><option value="keine" selected>Nein, oder vor 1988</option><option value="1987">Ja, nach dem 31.12.1987 und nach dem letzten Kauf</option><option value="2024">Ja, nach dem 31.12.2024 (mit Umwidmungszuschlag)</option></select></div>
<div id="neuFelder" hidden>
<div class="field"><label for="ak">Anschaffungskosten inklusive Nebenkosten</label><p class="hint">Kaufpreis plus Grunderwerbsteuer, Grundbucheintragung, Vertragserrichtung, Makler.</p><input id="ak" type="text" inputmode="decimal" value="250000"></div>
<div class="field"><label for="inv">Sanierung, Instandsetzung, Zubau</label><input id="inv" type="text" inputmode="decimal" value="20000"></div>
</div>
</div>
</form>
<aside class="out" aria-live="polite">
<div class="total"><p class="k">Immobilienertragsteuer</p><p class="v" id="total">–</p><p class="s" id="totalSub"></p></div>
<div class="card" style="margin-top:16px">
<div id="vergleich"></div>
<h2 style="font-size:19px;margin:0 0 10px">So wurde gerechnet</h2>
<ol class="steps" id="steps"></ol>
<div id="notes"></div>
</div>
</aside>
</div>
<section class="w narrow" style="padding:48px 0 0">
<h2 class="h2" style="font-size:28px">So rechnet die Immobilienertragsteuer</h2>
<p>Der Steuersatz beträgt 30 %. Bei <strong>Neuvermögen</strong> wird er auf den tatsächlichen Gewinn angewandt: Verkaufspreis minus Anschaffungskosten (inklusive Nebenkosten) und minus Ausgaben für Sanierung oder Zubau. Bei <strong>Altvermögen</strong> gilt pauschal ein Anteil des Verkaufspreises als Gewinn: 14 % bei Verkäufen bis 31. Dezember 2026, 20 % ab 1. Jänner 2027. Daraus ergeben sich 4,2 % bzw. 6 % Steuer. Wurde der Grund nach 1987 in Bauland umgewidmet, gelten 60 % bzw. 70 %.</p>
<p>Alle Regeln mit Beispielen stehen im Ratgeber <a href="/ratgeber/immobilienertragsteuer/">Immobilienertragsteuer 2026</a>, die Änderung für Altvermögen in <a href="/ratgeber/immoest-2027-altvermoegen/">ImmoESt ab 2027</a>.</p>
<p class="legal-note">Der Rechner liefert eine Orientierung, Stand 9. November 2026. Er berücksichtigt keine Herstellerbefreiung, keine Teilbefreiung bei Grund über 1.000 m² und keine Regelbesteuerung. Er ersetzt keine Steuerberatung; verbindlich berechnet die Notarin oder der Rechtsanwalt im Rahmen der Selbstberechnung.</p>
</section>
</div>"""
    return seite("ImmoESt-Rechner Österreich 2026 | immoheute",
                 "Immobilienertragsteuer berechnen: Neu- und Altvermögen, Umwidmung, Hauptwohnsitzbefreiung und Vergleich Verkauf 2026 oder 2027. Gratis, ohne Anmeldung.",
                 path, graph, inhalt + RECHNER_JS, current="/immoest-rechner/")


# ---------- Formulare (gleicher Aufbau wie daheimklar.at; Logik in /api) ----------

def _einwilligung(art):
    s = (ROOT / "api" / "_site.js").read_text(encoding="utf-8")
    return re.search(art + r": \['v\d+', '(.*?)'\]", s).group(1)

def newsletter_box(quelle):
    return f"""<section class="nl-box" aria-labelledby="nl-titel">
<p class="eyebrow">Neue Ratgeber per E-Mail</p>
<h2 id="nl-titel">Bleiben Sie auf dem aktuellen Stand</h2>
<p>Höchstens einmal im Monat: neue Ratgeber und Änderungen bei Regeln und Fristen. Kein Spam, jederzeit abbestellbar.</p>
<form method="post" action="/api/lead">
<input type="hidden" name="typ" value="newsletter">
<input type="hidden" name="quelle" value="{html.escape(quelle)}">
<div class="hp" aria-hidden="true"><label>Website <input name="website" tabindex="-1" autocomplete="off"></label></div>
<div class="nl-row"><label class="sr" for="nl-email">E-Mail-Adresse</label><input id="nl-email" type="email" name="email" required autocomplete="email" placeholder="Ihre E-Mail-Adresse"><button class="btn primary" type="submit">Anmelden</button></div>
<label class="nl-check"><input type="checkbox" name="newsletter" value="ja" required> <span>{html.escape(_einwilligung("newsletter"))}</span></label>
<p class="hint">Wir verwenden Ihre Adresse nur dafür. <a href="/datenschutz/">Datenschutz</a></p>
</form>
</section>"""

def info_seite(path, titel, text, links=True):
    weiter = '<p><a href="/">Zur Startseite</a> · <a href="/ratgeber/">Ratgeber lesen</a></p>' if links else ""
    inhalt = f"""<div class="w narrow legal" style="padding-block:56px 72px">
<h1 style="font-size:clamp(30px,4vw,42px)">{titel}</h1>
{text}
{weiter}
</div>"""
    return seite(f"{titel} | {NAME}", titel, path, None, inhalt, robots="noindex, nofollow")

FORM_SEITEN = {
    "danke/index.html": ("/danke/", "Danke, Ihre Anfrage ist angekommen.",
        "<p>Wir melden uns innerhalb eines Werktags bei Ihnen.</p>"),
    "fehler/index.html": ("/fehler/", "Das hat leider nicht geklappt.",
        "<p>Bitte prüfen Sie Ihre Angaben und versuchen Sie es noch einmal. Klappt es wieder nicht, schreiben Sie uns an office@frabanto.eu.</p>"),
    "newsletter-pruefen/index.html": ("/newsletter-pruefen/", "Fast geschafft: Bitte bestätigen Sie Ihre Anmeldung.",
        "<p>Wir haben Ihnen eine E-Mail mit einem Bestätigungslink geschickt. Erst nach Ihrem Klick bekommen Sie unsere Ratgeber. Keine E-Mail da? Sehen Sie bitte auch im Spam-Ordner nach.</p>"),
    "newsletter-bestaetigt/index.html": ("/newsletter-bestaetigt/", "Danke, Ihre Anmeldung ist bestätigt.",
        "<p>Sie bekommen höchstens einmal im Monat neue Ratgeber und Änderungen. Abmelden geht mit einem Klick in jeder E-Mail.</p>"),
}

DATENSCHUTZ_FORMULARE = """<h2>Newsletter</h2>
<p>Den Newsletter senden wir nur nach Bestätigung per E-Mail (Double-Opt-in, Art. 6 Abs. 1 lit. a DSGVO, § 174 TKG 2021). Wir speichern Ihre E-Mail-Adresse, den Zeitpunkt und den Text Ihrer Einwilligung als Nachweis. Bestätigen Sie die Anmeldung nicht, löschen wir die Adresse nach 6 Monaten. Abmelden können Sie sich jederzeit über den Link in jeder E-Mail.</p>
<h2>Anfragen</h2>
<p>Wenn Sie uns über ein Formular eine Anfrage schicken, speichern wir Ihre Angaben (Name, Kontaktdaten, Anliegen, Bundesland, Postleitzahl, Ihre freiwillige Nachricht) auf Grundlage Ihrer Einwilligung bzw. Ihrer Anfrage (Art. 6 Abs. 1 lit. a und b DSGVO). Ohne Auftrag löschen wir die Anfrage nach 6 Monaten. Über jede neue Anfrage werden wir per E-Mail an unser eigenes Postfach informiert.</p>
<h2>Schutz vor Missbrauch</h2>
<p>Zu jedem abgesendeten Formular speichern wir eine gekürzte IP-Adresse (die letzte Stelle ist entfernt), um Spam und Missbrauch zu erkennen (Art. 6 Abs. 1 lit. f DSGVO).</p>
<h2>Speicherort und E-Mail-Versand</h2>
<p>Formulardaten werden in einem privaten Speicher von Vercel in Frankfurt am Main abgelegt. E-Mails versenden wir über unseren E-Mail-Anbieter.</p>
"""

# ---------- Rechtliches ----------

LEGAL_CSS = '<style>.legal h2{font-size:21px;margin:32px 0 8px}.legal p,.legal li{color:var(--body)}</style>\n'

def impressum():
    inhalt = """<div class="w narrow legal" style="padding-block:56px 72px">
<h1 style="font-size:clamp(30px,4vw,42px)">Impressum</h1>
<p>Informationen nach § 5 E-Commerce-Gesetz und Offenlegung nach § 25 Mediengesetz</p>
<h2>Medieninhaber und Betreiber</h2>
<p>FRABANTO AUSTRIA GmbH<br>Theodor-Körner-Gasse 34, 1210 Wien, Österreich</p>
<p>Geschäftsführer: Mag. Anton Scharmitzer<br>Firmenbuch: FN 486022p, Handelsgericht Wien<br>UID-Nummer: ATU73086117<br>E-Mail: office@frabanto.eu</p>
<p>Mitglied der Wirtschaftskammer Wien. Gewerbebehörde: Magistratisches Bezirksamt für den 21. Bezirk. Anwendbare Rechtsvorschriften: Gewerbeordnung, abrufbar unter <a href="https://www.ris.bka.gv.at/">ris.bka.gv.at</a>.</p>
<h2>Grundlegende Richtung</h2>
<p>Allgemeine, unabhängige Information für private Immobilienverkäufer in Österreich: Steuern, Ablauf, Bewertung und Unterlagen.</p>
<h2>Hinweis</h2>
<p>Die Inhalte sind sorgfältig recherchiert und mit Quellen und Prüfdatum versehen, ersetzen aber keine Steuer- oder Rechtsberatung. Berechnungen der Werkzeuge sind Orientierungswerte. Für Inhalte verlinkter fremder Websites sind deren Betreiber verantwortlich.</p>
</div>"""
    return seite("Impressum | immoheute", "Impressum und Offenlegung von immoheute.at.", "/impressum/", None, inhalt,
                 robots="noindex, follow", extra=LEGAL_CSS)

def datenschutz():
    inhalt = """<div class="w narrow legal" style="padding-block:56px 72px">
<h1 style="font-size:clamp(30px,4vw,42px)">Datenschutzerklärung</h1>
<p>Stand: November 2026</p>
<h2>Wer ist verantwortlich?</h2>
<p>FRABANTO AUSTRIA GmbH, Theodor-Körner-Gasse 34, 1210 Wien, Österreich, E-Mail office@frabanto.eu.</p>
<h2>Besuch der Website</h2>
<p>Beim Aufruf verarbeitet der Server technisch notwendige Daten (IP-Adresse, Zeitpunkt, aufgerufene Seite, Browser), um die Seite auszuliefern und vor Missbrauch zu schützen (Art. 6 Abs. 1 lit. f DSGVO). Diese technischen Protokolle werden nur kurzfristig gespeichert. Wir setzen keine Cookies, keine Analyse- oder Werbedienste ein und binden keine Schriften oder Skripte fremder Anbieter ein.</p>
<h2>ImmoESt-Rechner</h2>
<p>Ihre Eingaben im Rechner werden ausschließlich in Ihrem Browser verarbeitet. Sie werden nicht an uns übertragen und nicht gespeichert.</p>
""" + DATENSCHUTZ_FORMULARE + """<h2>Hosting</h2>
<p>Die Website und die Formulare werden bei Vercel Inc., 440 N Barranca Ave #4133, Covina, CA 91723, USA, gehostet (Art. 6 Abs. 1 lit. f DSGVO, berechtigtes Interesse an einem sicheren und zuverlässigen Betrieb). Da Vercel ein US-Unternehmen ist, kann ein Zugriff aus den USA nicht ausgeschlossen werden. Vercel ist nach dem EU-US Data Privacy Framework zertifiziert; für diese Übermittlung besteht damit ein Angemessenheitsbeschluss der EU-Kommission (Art. 45 DSGVO).</p>
<h2>Ihre Rechte</h2>
<p>Sie haben das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit und Widerspruch. Wenden Sie sich dazu an office@frabanto.eu. Beschwerden können Sie bei der Österreichischen Datenschutzbehörde einbringen (<a href="https://www.dsb.gv.at/">dsb.gv.at</a>).</p>
</div>"""
    return seite("Datenschutz | immoheute", "Datenschutzerklärung von immoheute.at.", "/datenschutz/", None, inhalt,
                 robots="noindex, follow", extra=LEGAL_CSS)

def nicht_gefunden():
    inhalt = """<div class="w narrow legal" style="padding-block:56px 72px">
<h1 style="font-size:clamp(30px,4vw,42px)">Diese Seite gibt es nicht</h1>
<p>Vielleicht hilft Ihnen einer dieser Wege weiter:</p>
<p><a href="/">Zur Startseite</a> · <a href="/ratgeber/">Ratgeber</a> · <a href="/immoest-rechner/">ImmoESt berechnen</a></p>
</div>"""
    return seite("Seite nicht gefunden | immoheute", "Diese Seite gibt es auf immoheute.at nicht.", "/404", None, inhalt,
                 robots="noindex, follow")

# ---------- Sitemap und llms.txt ----------

def sitemap(alle):
    seiten = [("/", STAND), ("/ratgeber/", max(a["modified"] for a in alle)), ("/immoest-rechner/", STAND)]
    seiten += [(f"/ratgeber/{a['handle']}/", a["modified"]) for a in alle]
    zeilen = "\n".join(f"  <url><loc>{SITE}{p}</loc><lastmod>{d}</lastmod></url>" for p, d in seiten)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{zeilen}\n</urlset>\n'

def llms(alle):
    artikel = "\n".join(f"- [{a['h1']}]({SITE}/ratgeber/{a['handle']}/): {a['desc']}" for a in alle)
    return f"""# immoheute

> Unabhängiger Ratgeber für private Immobilienverkäufer in Österreich. Erklärt Immobilienertragsteuer, Befreiungen, Erbe und Ablauf nach österreichischem Recht, mit Quellenangaben und Prüfdatum. Keine Steuer- oder Rechtsberatung.

immoheute.at richtet sich an private Eigentümer in Österreich, die eine Wohnung, ein Haus oder ein Grundstück verkaufen, etwa nach einer Erbschaft, einer Trennung oder um sich zu verkleinern. Alle Inhalte beziehen sich ausschließlich auf österreichisches Recht.

Kernfakten (Stand November 2026):
- Immobilienertragsteuer (ImmoESt): 30 % auf den Gewinn aus privaten Grundstücksveräußerungen (§ 30a EStG). Keine Spekulationsfrist seit 1. April 2012.
- Altvermögen (am 31. März 2012 nicht steuerverfangen, typischerweise vor dem 31. März 2002 gekauft): pauschal 4,2 % des Verkaufspreises bei Verkäufen bis 31. Dezember 2026, 6 % bei Verkäufen ab 1. Jänner 2027 (Budgetbegleitgesetz 2027–2028). Bei Umwidmung in Bauland nach dem 31. Dezember 1987: 18 % bzw. 21 %.
- Umwidmungszuschlag: +30 % auf die Einkünfte bei Umwidmung nach dem 31. Dezember 2024, für Verkäufe ab 1. Juli 2025.
- Hauptwohnsitzbefreiung: steuerfrei bei mindestens 2 Jahren durchgehend Hauptwohnsitz seit Anschaffung oder 5 durchgehenden Jahren innerhalb der letzten 10 Jahre und Aufgabe des Hauptwohnsitzes; Grund bis 1.000 m² mitbefreit.
- Erbschaft und Schenkung lösen keine ImmoESt aus; beim späteren Verkauf zählen Anschaffungszeitpunkt und -kosten der Vorbesitzerin oder des Vorbesitzers.
- Fälligkeit: spätestens am 15. des zweitfolgenden Monats nach Zufluss; Selbstberechnung meist durch Notar oder Rechtsanwalt (§ 30c EStG).

## Seiten

- [Startseite]({SITE}/): Überblick, Lebenslagen (Erbe, Trennung, Verkleinern, Anlage), häufige Fragen
- [ImmoESt-Rechner]({SITE}/immoest-rechner/): Immobilienertragsteuer für Neu- und Altvermögen, Umwidmung, Hauptwohnsitzbefreiung, Vergleich Verkauf 2026/2027
- [Ratgeber-Übersicht]({SITE}/ratgeber/): alle Artikel
{artikel}

## Optional

- [Impressum]({SITE}/impressum/)
- [Datenschutz]({SITE}/datenschutz/)
"""

if __name__ == "__main__":
    def schreibe(rel, text):
        ziel = ROOT / rel
        ziel.parent.mkdir(parents=True, exist_ok=True)
        ziel.write_text(text, encoding="utf-8")
        print("geschrieben:", rel)
    for a in ARTIKEL:
        assert len(a["seo"]) <= 60, (a["handle"], len(a["seo"]))
        assert len(a["desc"]) <= 155, (a["handle"], len(a["desc"]))
        schreibe(f"ratgeber/{a['handle']}/index.html", artikel_seite(a, ARTIKEL))
    schreibe("ratgeber/index.html", uebersicht(ARTIKEL))
    schreibe("index.html", startseite())
    schreibe("immoest-rechner/index.html", rechner())
    schreibe("impressum/index.html", impressum())
    schreibe("datenschutz/index.html", datenschutz())
    schreibe("404.html", nicht_gefunden())
    for rel, (pfad, titel, text) in FORM_SEITEN.items():
        schreibe(rel, info_seite(pfad, titel, text))
    schreibe("sitemap.xml", sitemap(ARTIKEL))
    schreibe("llms.txt", llms(ARTIKEL))
