<!-- markdownlint-disable MD013 -->
# CRM-Verdrahtung Wizards

Welche Datei wann, und warum nicht ein Script:
[docs/runbooks/crm-wiring-wizards.md](../../docs/runbooks/crm-wiring-wizards.md).

```bash
./crm-wiring-01-locate-and-scan.sh
```

Zustand nur unter `/private/tmp/dino-crm-wiring.env`, nicht im Projekt-`.env`.

Wizard 01 hat **keinen** 200-Zeilen-Deckel (Rescan 2026-09-13: RPC 21,
Tabellen-Fundstellen 1732, UI-Fundstellen 2487).
Die Zahl ist `wc -l` der ganzen Datei. Eine Liste mit genau 200 Zeilen
ist der alte Fehl-Lauf, kein vollständiges Ergebnis.
