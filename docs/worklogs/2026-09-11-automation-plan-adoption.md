# Worklog: Prihvatanje SQL i database automatizacijskog plana

Datum: 2026-09-11

Status: Dokumentacijska promjena; bez database, produkcijskog ili Linear writea

## Povod

Korisnik je nakon poređenja postojećeg implementacijskog briefa i novog
istraživanja zatražio usklađivanje dokumentacije, planova, ADR-ova i ticketa s
automatiziranim putem koji štedi najviše ponovljivog rada bez promjene
Release-1 funkcija.

## Prihvaćeno

- Supabase CLI, lokalna sintetička baza, verzionirane migracije, SQL lint,
  pgTAP, MCP contract testovi, Advisors i CI čine osnovni put nakon discoveryja
  i stack odluke.
- AI priprema SQL i testne diffove, ali nema pravo produkcijskog applyja.
- Ugrađeni Supabase/PostgreSQL monitoring prethodi dodatnim servisima.
- pganalyze se evaluira tek nakon četiri do osam sedmica reprezentativnog
  workload-a.
- Ostali alati ostaju opcije s jasnim triggerima, ne zadani Release-1 stack.

## Ažurirani artefakti

- [ADR-0004](../decisions/0004-automated-database-development.md)
- [Implementacijski brief](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md)
- [Runbook automatizacije](../runbooks/database-development-automation.md)
- [Plan ticketa](../planning/release-1-automation-tickets.md)
- [Projektni status](../project.md), [README](../../README.md),
  [CONTEXT](../../CONTEXT.md) i agentske upute

## Vanjski tracker

Read-only Linear inventar vratio je nula issuea. Osam blockers-first ticketa je
pripremljeno lokalno. Kreiranje i povezivanje u Linearu nije izvršeno jer nakon
preflighta zahtijeva zasebnu freigabe, a implementacijski ticketi ostaju
blokirani otvorenim design odlukama iz ADR-0002.
