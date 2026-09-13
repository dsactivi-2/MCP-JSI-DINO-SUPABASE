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
| Recruiter | Interna pretraga Vermittlera: Sachbearbeiter, Teamleiter, Inhaber i Entwickler. Nisu Kunde ni Kandidat. |
| Vermittler | Agencija koja povezuje Kandidaten i Kunden. Interna pretraga vidi cijeli pool. |
| Kunde | Firma koja zapošljava. Nikad cijeli pool. Prvo Vorschlagsfreigabe bez kontakata, zatim Einstellungsfreigabe s kontaktima tog kandidata. |
| Entwickler | Tehnička uloga Vermittlera. U proizvodu vidi cijeli pool i sva polja uključujući kontakte. Plugin nikad na produkciju ili klon. |
| Sachbearbeiter | Interni Vermittler. Vidi cijeli pool i sva polja uključujući kontakte. |
| Teamleiter | Interni Vermittler. Vidi cijeli pool i sva polja uključujući kontakte. |
| Inhaber | Vlasnik Vermittlera. Vidi cijeli pool i sva polja uključujući kontakte; bez plugina. |
| Vorschlagsfreigabe | Nakon ugovora i konkretnog zahtjeva Kunde vidi predložene kandidate bez e-maila, telefona i ostalih kontakata. |
| Einstellungsfreigabe | Nakon zasuge/zapošljavanja predloženog kandidata Kunde dobija i kontakte tog kandidata. To je CONTACT-02. |
| Profil kandidata | Podaci o jednom kandidatu, u opsegu dozvoljenom korisniku. |
| Filter | Strukturirani kriterij pretrage, npr. zanimanje ili minimalno iskustvo. |
| Ausbildungsberuf | Formalno zanimanje/obrazovna kvalifikacija kandidata; više takvih zanimanja može odgovarati široj potrebi klijenta. Kontrolisana CRM lista i njeni ID-ovi su ARBEITSANNAHME / DURCH DISCOVERY ZU PRÜFEN. |
| Berufssuchprofil | Imenovana, verzionirana i kontrolisana grupa Ausbildungsberufe, Erfahrungsberufe i Tätigkeitsarten za širu potrebu klijenta; članovi ostaju samostalno pretraživi i mogu pripadati većem broju profila. |
| Berufserfahrung | Jedno značenje. Ako dva spremišta tvrde da su to godine iskustva, brojevi moraju biti isti; inače Aktenfeld nije ta stavka (Q8.5.1). |
| Relevante Berufserfahrung | Odgovarajući poslovi: sličan natpis i srodni nazivi. Liste prvo; KI samo prijedlog uz potvrdu (Q8.5.3–8). Preklapanja se ne sabiraju; tekući posao do danas. Zettel 2 se ne koristi. |
| Aktiver Filter | Korisnik ga je izričito naveo ili potvrdio u pregledu; nenavedena kategorija je neaktivna i ne ograničava rezultat. |
| Profilverwaltungs-MCP | Interna upravljačka granica za nacrte, provjeru i verzionirano objavljivanje Berufssuchprofila; odvojena je od read-only Runtime-Such-MCP-a. |
| Runtime-Such-MCP | Kontrolisana read-only granica za pretragu, pojedinačni profil i dozvoljene filteropcije; korisnikov identitet i dozvoljeni opseg vrijede za svaki poziv. |
| Autentificirani akter | Provjereni pozivalac; sama prijava ne daje pravo na svaki kandidat, profil ili administrativnu radnju. |
| Kanonski model | Dogovoreni domenski pojmovi na koje se mapira stvarna shema. |
| Taksonomija | Verzija odobrenih pojmova, identifikatora i višejezičnih sinonima. |
| Dokaz poklapanja | Podatak koji objašnjava zbog čega kandidat zadovoljava filter. |
| Dostupnost | Status spremnosti kandidata uz podatak o vremenu potvrde. |
| Svježina | Koliko je podatak aktuelan prema autoritativnom izvoru i vremenu. |
| Tenant | Autorizacijski opseg; njegovo stvarno postojanje i mapiranje tek se utvrđuju. |
| Ähnlichkeitssuche | Eksplicitni extra-modus „sličan ovom kandidatu“, nije default. Nije R1 must-have; isporuka nakon evaluacijskog gatea. |
| Discovery | Odobreni read-only postupak utvrđivanja sheme i kvaliteta podataka. |
| Heft (ADR-0002) | Ciljevi i izričite odluke design intervjua; nije whitelist. |
| Stara Filter-UI | Kako recruiter danas traži u PHP-CRM (`kandidati.php` Filter). |
| Codebefund | Inventar iz koda, bez tvrdnje da je to već MCP-ugovor. |
| Quellenrang | Q17: Heft i stara UI su ravnopravni; novo iz koda ne ispada. |
| Statuswechsel-Nachricht | Mail/Messenger/Erinnerung an Status; im Produkt default aus (Q20). |
| Funktionsparität | Gleiche CRM-Fähigkeiten wie im PHP, nicht 1:1-Kopie der alten SQL (Q21). |
| Status obrade | `kandidat_status` 0–8 (Na provjeri … Arhiviran). |
| Status prijave | `kandidat_status_prijave`; labele u DB, ne u PHP. |
| Messenger-status | `kandidat_status_messenger` (SMS čeka / ulogovan / odbio / profil nedovršen). |
| DIPL-status | Zasebna skala 0–7 u filteru, nije ista kao obrada. |
| JSON-Filter | Mali dozvoljeni obrazac iz teksta; Postgres traži (ADR-0001). |

<!-- markdownlint-enable MD013 -->

Rječnik opisuje poslovne koncepte, ne fizičke tabele, kolone ili postojeće role.
Nepoznate vrijednosti i neslaganja izvora ostaju otvorena do audita i odluke
odgovornog vlasnika.

## Izvori detalja

- [Stanje projekta](docs/project.md) prati fazu, otvorene uslove i naredni cilj.
- [Implementacijski brief](docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md)
  definira zahtjeve i kriterije prihvata.
- [SDK integracijski plan](docs/planning/sdk-integration-plan.md) čuva
  tehničku razradu i otvorene provjere; SDK detalji nisu domenski pojmovi.
- [ADR-0001](docs/decisions/0001-controlled-query-boundary.md) definira
  prihvaćenu arhitekturnu granicu.
- [ADR-0002](docs/decisions/0002-search-design-interview.md) čuva potvrđene i
  otvorene odluke aktivnog design intervjua.
- [Inventar CRM-Scan](docs/discovery/crm-work-inventory.md) indeksira šta je
  iz PHP-a već mapirano i šta je otvoreno.
- [Discovery runbook](docs/runbooks/schema-discovery.md) određuje postupak
  provjere nepoznatih činjenica.
- [ADR-0004](docs/decisions/0004-automated-database-development.md) i
  [runbook automatizacije](docs/runbooks/database-development-automation.md)
  određuju kako se nakon discoveryja SQL piše, provjerava, optimizira i pušta.
