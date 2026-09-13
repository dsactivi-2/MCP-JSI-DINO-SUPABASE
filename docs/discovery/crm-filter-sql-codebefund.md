<!-- markdownlint-disable MD013 -->
# Codebefund: Filter-SQL der Hauptsuche

Stand: 2026-09-13

Quelle: `serversidedata.php` case `lista_kandidata`. Keine Datensätze.
Q22: altes CRM. A aus Q20: wie die Maske wirklich rechnet.

## Ablauf

1. `kandidati.php?page=list_ajax` sammelt POST-Filter.
2. DataTables ruft `serversidedata.php?page=lista_kandidata` auf.
3. Jeder Filter wird zu einem SQL-Stück. Leer → `1` (keine Einschränkung).
4. Alle Stücke hängen mit **AND**.
5. Ohne Archiv-Cookie: `kandidat_status != 3`. Mit Cookie: nur Status 3.
   Formularfilter fallen im Archiv-Zweig weg; PHP hängt
   Führerschein-Klassen und Suchbox danach trotzdem an.

Das entspricht Q8: ungenannte Filter sind tot. Mehrere Kategorien: UND.

## Immer-Joins (PHP-Ist, kein R1-Soll)

Auch wenn die Filter Gruppe und Status **aus** sind, hängt `lista_kandidata`
Liste-SQL und Zähl-SQL fest:

`INNER JOIN idk_kandidati_grupe` auf `kandidat_group = kg_id`
und `INNER JOIN idk_kandidat_status` auf `kandidat_status = status_id`.

Ohne passende Nachschlagezeile (`kg_id` / `status_id`) fällt der Kandidat
in der **alten** Suche raus. Das ist PHP-Ist, nicht der R1-Vertrag.

R1 kopiert dieses INNER JOIN **nicht**. Kandidaten ohne Gruppen- oder
Bearbeitungszeile bleiben sichtbar (ADR-0002 Q18, 2026-09-13). Ein gesetzter
Gruppen- oder Status-Filter gilt weiter.

## Filterlogik (PHP, nicht modernisiert)

| Filter | Wenn gesetzt | Sonst |
| --- | --- | --- |
| Alter | `YEAR(now) - YEAR(geburt)` nur wenn **od und do** gesetzt | aus |
| Führerschein ja | `kandidat_vozacka_dozvola` enthält `Da` | aus |
| Führerschein-Klasse | LIKE auf `kandidat_vozacka_kategorija`; B zieht höhere Klassen mit | aus |
| Radno iskustvo | ID hat mindestens eine Zeile in `idk_kandidat_radno_iskustvo` | aus |
| Deutsch A1–C2 | `idk_kandidat_jezici`, Name ähnlich Njemacki, `kj_slusanje` = Stufe **oder höher** | `svi`/leer = aus |
| Deutsch ohne Wissen | `kj_slusanje` BEZ ZNANJA | |
| Deutsch keine Info | Kandidat hat keine Deutsch-Zeile mit A1–C2/BEZ ZNANJA | |
| Englisch | analog, Name ähnlich Engleski | |
| Gruppe | `kandidat_group IN (...)` | aus |
| Status | `kandidat_status IN (...)` | aus |
| Status prijave | `IN (...)`; Wert 0 schließt auch NULL ein | aus |
| Staatsangehörigkeit | ein Wert EU → `kandidat_drzavljanstvo_vrsta` wie EU%; NON-EU → nicht EU% oder NULL; beide → kein Filter | |
| Boravak EU | `boravak_eu LIKE` die Auswahl | aus |
| Schule ohne Smjer | `ke_naziv LIKE %schule%` → IDs | aus |
| Smjer | `ke_naziv_kvalifikacije LIKE` exakt den Smjer | Schule- **und** Struke-Bedingung fallen weg |
| Struke ohne Smjer | Struke → `idk_skole_smjerovi.ss_naziv` → gleiche Smjer-Suche | aus |
| Quelle | `kandidat_porijeklo IN`; Partner (6) nimmt 7 mit | aus |
| DIPL-Status | Join `idk_nd_kandidata`; 0 = kein DIPL oder Status in Liste | aus |
| Nostrifikation | Join `idk_nostrifikovane_diplome.full_recognition`; 3 = NULL oder in Liste | aus |

Zusätzlich die **Suchbox** der Tabelle (nicht das Filterformular): Name,
Statusname, Gruppe, **E-Mail, Mobilnummer**.

## Trefferliste (SELECT)

Unter anderem: ID, Name, Geburt, Geschlecht, JMBG, Bearbeitung, Messenger,
Bild, E-Mail, Mobil, Eingangszeit, Bewerbungs-URL, Gruppe, Herkunft,
CV/Profil-Flags, Gruppenname, Nalog-Name, Statusname.

Q4: interne Rollen dürfen Kontakte sehen. Discovery speichert keine Werte.

## Modernisieren später (nicht jetzt umbauen)

- Alter nur über Jahreszahl, nicht volles Alter.
- Deutsch nur Hör-Feld `kj_slusanje`, Tippfehler doppeltes B1 in A1-Zweig.
- Erfahrung nur „hat Jobzeile“, keine Jahre.
- Struke nur über Schul-Smjer, nicht occupation.
- SQL wird im PHP zusammengebaut (kein parametrisiertes Stück je Filter).

Q21/Q22: dokumentieren, beim MCP neu und sicher bauen. Kein 1:1-Copy.

## Als Nächstes

B7 und C 4–9 sind gelesen. JSON-Filter-Entwurf geprüft:
[crm-json-filter-draft.md](crm-json-filter-draft.md).
Bericht-Audit 2026-09-13 ausgeführt. JSON bleibt Entwurf.
Nächster Schritt: Nutzer nennt den Auftrag. Kein MCP-Scaffold ohne Freigabe.
