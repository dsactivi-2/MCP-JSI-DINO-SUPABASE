# Domenski kontekst: pretraga CRM kandidata

Recruiter treba pronaći relevantne kandidate u CRM-u s približno 200.000 zapisa
koristeći B/H/S, njemački ili engleski. Obim je projektna procjena
(DURCH DISCOVERY ZU PRÜFEN), ne potvrđen broj zapisa. Upit opisuje poslovne
kriterije poput
zanimanja, iskustva, lokacije, jezika, vještina i dostupnosti. Prikaz rezultata
treba omogućiti ljudsku procjenu prikladnosti kandidata.

## Rječnik

<!-- markdownlint-disable MD013 -->

| Pojam | Značenje u ovom projektu |
| --- | --- |
| Kandidat | Osoba predstavljena CRM zapisom; nije generirani profil. |
| Recruiter | Korisnik koji pretražuje kandidate i pregledava poklapanja. |
| Profil kandidata | Podaci o jednom kandidatu, u opsegu dozvoljenom korisniku. |
| Filter | Strukturirani kriterij pretrage, npr. zanimanje ili minimalno iskustvo. |
| Ausbildungsberuf | Formalno zanimanje/obrazovna kvalifikacija kandidata; više takvih zanimanja može odgovarati široj potrebi klijenta. Kontrolisana CRM lista i njeni ID-ovi su ARBEITSANNAHME / DURCH DISCOVERY ZU PRÜFEN. |
| Berufssuchprofil | Imenovana, verzionirana i kontrolisana grupa Ausbildungsberufe, Erfahrungsberufe i Tätigkeitsarten za širu potrebu klijenta; članovi ostaju samostalno pretraživi i mogu pripadati većem broju profila. |
| Relevante Berufserfahrung | VORLÄUFIGER VORSCHLAG: trajanje stručno odgovarajućih radnih perioda. Cijela Q8.5 je OFFEN, uključujući izbor ukupnog ili relevantnog iskustva i način obračuna; ovo nije potvrđena definicija. |
| Aktiver Filter | Korisnik ga je izričito naveo ili potvrdio u pregledu; nenavedena kategorija je neaktivna i ne ograničava rezultat. |
| Profilverwaltungs-MCP | Interna upravljačka granica za nacrte, provjeru i verzionirano objavljivanje Berufssuchprofila; odvojena je od read-only Runtime-Such-MCP-a. |
| Kanonski model | Dogovoreni domenski pojmovi na koje se mapira stvarna shema. |
| Taksonomija | Verzija odobrenih pojmova, identifikatora i višejezičnih sinonima. |
| Dokaz poklapanja | Podatak koji objašnjava zbog čega kandidat zadovoljava filter. |
| Dostupnost | Status spremnosti kandidata uz podatak o vremenu potvrde. |
| Svježina | Koliko je podatak aktuelan prema autoritativnom izvoru i vremenu. |
| Tenant | Autorizacijski opseg; njegovo stvarno postojanje i mapiranje tek se utvrđuju. |
| Discovery | Odobreni read-only postupak utvrđivanja sheme i kvaliteta podataka. |

<!-- markdownlint-enable MD013 -->

Rječnik opisuje poslovne koncepte, ne fizičke tabele, kolone ili postojeće role.
Nepoznate vrijednosti i neslaganja izvora ostaju otvorena do audita i odluke
odgovornog vlasnika.

## Izvori detalja

- [Stanje projekta](docs/project.md) prati fazu, otvorene uslove i naredni cilj.
- [Implementacijski brief](docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md)
  definira zahtjeve i kriterije prihvata.
- [ADR-0001](docs/decisions/0001-controlled-query-boundary.md) definira
  prihvaćenu arhitekturnu granicu.
- [ADR-0002](docs/decisions/0002-search-design-interview.md) čuva potvrđene i
  otvorene odluke aktivnog design intervjua.
- [Discovery runbook](docs/runbooks/schema-discovery.md) određuje postupak
  provjere nepoznatih činjenica.
- [ADR-0004](docs/decisions/0004-automated-database-development.md) i
  [runbook automatizacije](docs/runbooks/database-development-automation.md)
  određuju kako se nakon discoveryja SQL piše, provjerava, optimizira i pušta.
