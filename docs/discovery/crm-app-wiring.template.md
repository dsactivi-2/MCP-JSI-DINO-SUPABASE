<!-- markdownlint-disable MD013 -->
# CRM-Suchverdrahtung

Stand: YYYY-MM-DD

Status: ENTWURF — Vorlage. Noch kein Befund.

Diese Datei ist die leere Output-Vorlage aus
[crm-source-wiring-capture.md](../runbooks/crm-source-wiring-capture.md).
Schritt-für-Schritt-Plan:
[crm-wiring-human-plan.md](../runbooks/crm-wiring-human-plan.md).
Arbeitskopie außerhalb Git: `/private/tmp/dino-crm-app-wiring.md`.
Redigierte Fassung erst nach Secret-/PII-Check hierher kopieren und die
Kopfzeile `Status` auf `PASS_WITH_GAPS` oder `FAIL` setzen.

CRM-Pfad: /absoluter/pfad

Stack: OFFEN

Git-Revision CRM: unbekannt

Datenbank in diesem Lauf: keine

## 1. Suchmasken

| Maske (UI-Name) | Datei / Symbol | Ruft | Kontakte im Ergebnis | Note |
| --- | --- | --- | --- | --- |
| | | RPC oder SQL-Name | ja/nein | |

Hauptsuche laut Code: OFFEN

## 2. Feldkarte

| UI-Label | Code-Symbol | RPC-Argument | Physisch (Tabelle.spalte) | Schicht | Note |
| --- | --- | --- | --- | --- | --- |
| | | | | Ausbildungsberuf / Erfahrungsberuf / Tätigkeitsart / Erfahrung / Ort / Sprache / Skill / Alter / Status / Freitext / sonst | |

## 3. RPC-Karte

| Schema.funktion | Argumente (ohne Werte) | Von Maske | Kontaktfelder | Note |
| --- | --- | --- | --- | --- |
| | | | ja/nein | |

Nicht wrappen: `crm_api.search_candidates`, falls Kontakt in der Signatur.

## 4. Beruf und Erfahrung

| Frage | Befund | Note |
| --- | --- | --- |
| Kann die Hauptsuche Ausbildung ohne Erfahrung setzen? | | |
| Kann sie Erfahrung ohne Ausbildung setzen? | | |
| Tätigkeitsart getrennt? | | |
| Welches Feld zählt Dauer? | Akte / Lebenslauf-Liste / beide / OFFEN | |
| Berufssuchprofil = welche Tabelle? | occupation-Hierarchie / idk_kandidat_pozicija / idk_nalog_profil / OFFEN | |

## 5. R1-Ausschluss in der alten Suche

| Fläche | Vorkommen in Maske/RPC | Folge |
| --- | --- | --- |
| E-Mail / Telefon | | nicht in JSON-Filter, nicht in MCP-Output |
| CV-Text | | |
| Notizen | | |

## 6. Lücken

- OFFEN:
- DURCH DISCOVERY ZU PRÜFEN:
- ARBEITSANNAHME:

## 7. Nicht entschieden (bewusst leer)

JSON-Filter, MCP-Tools, Ranking, Auth. Erst nach Abnahme von Abschnitt 1–4.
