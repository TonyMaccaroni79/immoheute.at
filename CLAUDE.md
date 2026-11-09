# immoheute.at – Arbeitsanleitung

Ratgeber-Seite für private Immobilienverkäufer in Österreich (Erbe, Trennung, Verkleinern, Anlage). Betreiber: FRABANTO AUSTRIA GmbH, Mag. Anton Scharmitzer. Sprache: Deutsch (Österreich), Sie-Form, sachlich. Die Domain hatte früher ein Immobilienportal; Inhalte bleiben beim Thema Immobilien.

## Aufbau
- Repository-Wurzel = veröffentlichte Seite (statische HTML-Dateien) + `vercel.json`. Vercel baut nichts; erzeugte Seiten werden mitgeliefert.
- ALLE Seiten erzeugt `_quelle/build.py` (Startseite, Rechner, Ratgeber, Impressum, Datenschutz, 404, sitemap.xml, llms.txt). Nie die erzeugten HTML-Dateien direkt bearbeiten. Bauen: `cd _quelle && python3 build.py`.
- Ratgeber: Text in `_quelle/ratgeber/<handle>.html`, Metadaten (h1, SEO-Titel ≤ 60 Zeichen, Beschreibung ≤ 155 Zeichen, thema, published, modified) in der Liste `ARTIKEL`. Article-, FAQ- und Breadcrumb-Schema entstehen automatisch.
- Artikel-Aufbau: erster Absatz `<strong>Die kurze Antwort:</strong>` (2–4 Sätze), H2 als Fragen, mindestens eine Tabelle oder Checkliste, `<h2>Häufige Fragen</h2>` mit 3–6 `<h3>` + genau einem `<p>`, am Ende `<h2>Quellen</h2>` mit Prüfdatum.
- ImmoESt-Rechner: Logik in `berechne()` (ohne DOM) im Skript `RECHNER_JS`. Nach jeder Änderung die Prüfwerte rechnen: 400.000 € Altvermögen = 16.800 € (2026) / 24.000 € (2027); Umwidmung nach 1987 = 72.000 / 84.000 €; Neuvermögen 400.000 − 250.000 − 20.000 = 39.000 €.
- Schrift lokal in `/fonts/pjs.woff2`; keine Google Fonts, keine Fremd-Skripte, keine Cookies.
- Auf `*.vercel.app` liefert `vercel.json` `X-Robots-Tag: noindex`; erst die echte Domain wird indexiert.
- Neue Seite: in `build.py` (Sitemap/llms.txt) ergänzen, danach IndexNow anpingen: `https://api.indexnow.org/indexnow?url=<neue URL>&key=9063091d8362479e64a881aec0c7f2a5`.

## Hosting-Regel (Vercel Hobby)
- Solange das Projekt im Gratis-Plan läuft: keine Preise, Kaufbuttons, Makler-/Lead-Formulare, Werbung oder Affiliate-Links. Kommerzielle Teile (Verkaufs-Fahrplan, Makler-Bewertung, Energieausweis-Angebote) erst nach Umzug auf Hetzner oder Vercel Pro.

## Inhaltliche Regeln
- Jede Zahl, Frist und Voraussetzung an der Quelle prüfen (ris.bka.gv.at, bmf.gv.at, oesterreich.gv.at, Steuerberatungs- und Kanzlei-Publikationen als Zweitquelle) und mit Prüfdatum angeben. Nicht gefundene Werte weglassen.
- Keine Einzelfall-Steuerberatung. Hinweis „ersetzt keine Steuer- oder Rechtsberatung“.
- Österreich-spezifisch schreiben (keine Spekulationsfrist, Altvermögen, Hauptwohnsitzbefreiung) und deutsche Irrtümer richtigstellen.
- Wichtige Frist: Altvermögen-Pauschale steigt für Verkäufe ab 1.1.2027 (4,2 % → 6 %, 18 % → 21 %). Ab 2027 Texte und Rechner auf den neuen Stand bringen.

## Themenliste Ratgeber (nach Priorität, erledigte streichen)
1. ~~Immobilienertragsteuer 2026~~ – erledigt 09.11.2026
2. ~~ImmoESt ab 2027: Altvermögen~~ – erledigt 09.11.2026
3. Geerbte Wohnung verkaufen: Ablauf, Verlassenschaft, Steuer
4. Wohnung verkaufen ohne Makler
5. Haus bewerten lassen: Online, Makler oder Gutachter
6. Energieausweis beim Verkauf: Pflicht, Kosten, Gültigkeit
7. Immobilie bei Scheidung: verkaufen, übernehmen oder vermieten
8. Unterlagen-Checkliste Hausverkauf
9. Bieterverfahren
10. Grundstück verkaufen: Umwidmung und Steuer
