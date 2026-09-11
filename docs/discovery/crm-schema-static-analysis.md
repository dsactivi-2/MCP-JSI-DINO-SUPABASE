# Statička analiza CRM schema izvoza

Status: **PASS_WITH_GAPS**

Datum analize: 2026-09-11

## 1. Scope i izvor

Analiziran je lokalni Schema Visualizer izvoz pod internim aliasom `crm_schema_visualizer_export_01`. Izvor je tretiran kao nepouzdan podatak i nije kopiran u repozitorij. Oznaka sheme `crm` dolazi iz korisničkog scopea; sam izvoz ne prikazuje schema-qualified nazive, pa pripadnost svakog objekta shemi ostaje **DURCH DISCOVERY ZU PRÜFEN**.

## 2. Sigurnosni preflight

- `BELEGT DURCH SCHEMAEXPORT`: datoteka postoji, običan je ASCII/UTF-8 tekst, ima 113.547 bajtova i 3.121 liniju.
- `BELEGT DURCH SCHEMAEXPORT`: automatizirani scan nije našao vjerovatne tokene/ključeve, connection stringove, privatne URL-ove, podatkovne redove, e-mail vrijednosti, telefonske vrijednosti ni CV/freetext vrijednosti; svaka kategorija ima 0 pogodaka.
- Izlaz preflighta sadržavao je samo kategorije i brojnosti, bez vrijednosti.

## 3. Sažetak

- `BELEGT DURCH SCHEMAEXPORT`: 100 potpunih `Table` blokova i 1104 kolona.
- `BELEGT DURCH SCHEMAEXPORT`: svih 100 prikazanih tabela ima po jedan označeni primary key; nema označenih unique, foreign-key ni identity/sequence constrainta.
- `BELEGT DURCH SCHEMAEXPORT`: 84 ne-primary kolone završavaju na `id`/`ids`, ali nijedna nije dokazana kao foreign key.
- `BELEGT DURCH SCHEMAEXPORT`: RLS sekcija sadrži 188 naziva objekata i 374 policy reda; 88 policy naziva nemaju odgovarajući `Table` blok u izvozu.
- `DURCH DISCOVERY ZU PRÜFEN`: izvoz je zato strukturno nepotpun i ne može dokazati puni broj tabela, sve relacije, RLS enable/force stanje, efektivna prava, indekse, viewove, funkcije ili triggere.
- Domenski je klasificirano 65 tabela; 35 ostaje tehnički ili fachlich nejasno.

## 4. Tabelleninventar nach Fachbereichen

Nazivi su fizički beleg, ali svako fachlich grupisanje je `ARBEITSANNAHME`, jer semantika nije potvrđena sadržajem ni vlasnikom podataka.

### Kandidatenstamm (7)

`idk_dak_kandidati`, `idk_kandidati`, `idk_kandidati_reject_reasons`, `idk_nd_kandidata`, `idk_nd_kandidata_biljeske`, `idk_nd_kandidata_status_log`, `idk_nd_kandidati_ciscenje`

### Kontaktdaten (4)

`idk_contacts`, `idk_contacts_info`, `idk_kandidat_kontakt_info`, `idk_nd_ustanove_kontakti`

### Dokumente und Verträge (8)

`idk_documents`, `idk_kandidat_cv`, `idk_kandidati_contracts`, `idk_korisni_dokumenti`, `idk_nd_kandidata_dokumenti`, `idk_nd_ugovori`, `idk_nd_ustanove_tip_dokumenta`, `idk_nostrifikovane_diplome`

### Ausbildung und Qualifikationen (3)

`idk_kampanje_dipl`, `idk_kandidat_akademija`, `idk_kandidat_edukacija`

### Berufserfahrung (1)

`idk_kandidat_radno_iskustvo`

### Tätigkeiten (1)

`idk_kandidat_pozicija`

### Fähigkeiten (1)

`idk_kandidat_vjestine`

### Sprachen (4)

`idk_candidate_language_logs`, `idk_candidate_verified_languages`, `idk_glossa_log`, `idk_kandidat_jezici`

### Standorte (0)

Nema potpunog `Table` bloka u izvozu.

### Gruppen und Berufssuchprofile (2)

`idk_kandidati_grupe`, `idk_nalog_profil`

### Verfügbarkeit und Status (5)

`idk_duration_per_status`, `idk_kandidat_status`, `idk_kandidat_status_prijave`, `idk_log_kandidat_statusi`, `idk_nedostupan_log`

### Partner, Mandanten und Benutzer (20)

`idk_api_clients`, `idk_clients`, `idk_clients_stats`, `idk_companies`, `idk_companies_info`, `idk_employees`, `idk_employees_info`, `idk_employees_reports`, `idk_jobstep_partners`, `idk_jobstep_partners_pregledi`, `idk_link_projects`, `idk_module_permissions`, `idk_modules`, `idk_nalog_financije`, `idk_nalog_smjer`, `idk_partner_companies`, `idk_partner_meetings`, `idk_partner_notification`, `idk_partner_notification_logs`, `idk_partner_notification_status`

### Audit und Historie (9)

`idk_agenti_activity`, `idk_analitika`, `idk_bot_obavijesti`, `idk_log_statusi_prijave`, `idk_logs`, `idk_messenger_obavijesti`, `idk_nalozi_log`, `idk_notification`, `idk_notifications`

### Technische oder unbekannte Tabellen (35)

`idk_appointment_invite_links`, `idk_chat_question`, `idk_chat_type`, `idk_email_text`, `idk_ipwhitelist`, `idk_kandidat_de`, `idk_kandidat_financije`, `idk_kandidat_projekcije`, `idk_kategorije`, `idk_kategorije_provizija`, `idk_korisni_linkovi`, `idk_link_generator`, `idk_link_generator_rel`, `idk_messages`, `idk_messages_users`, `idk_nalozi`, `idk_nalozi_blokovi_prijave`, `idk_nalozi_opis`, `idk_nalozi_rate`, `idk_nd_cron_export`, `idk_nd_cron_settings`, `idk_nd_limiti`, `idk_nd_menadzeri_statistike`, `idk_nd_naplata_preko`, `idk_nd_poste`, `idk_nd_rate`, `idk_nd_termini`, `idk_nd_ustanove`, `idk_nd_ustanove_biljeske`, `idk_nd_ustanove_skola`, `idk_nd_ustanove_skole_smjerovi`, `idk_notes`, `idk_obracuni`, `idk_ostatci_obracuna`, `idk_otherdata`

## 5. Kandidatenbezogene Tabellen und Beziehungen

- `idk_kandidati` je `ARBEITSANNAHME` za centralnu Kandidatentabelle: izvoz belegt tabelu, primary key `kandidat_id` i širok skup identitetskih, statusnih, lokacijskih, obrazovnih i partnerskih kolona.
- Kandidatenbezogene Strukturkandidaten su `idk_kandidat_edukacija`, `idk_kandidat_radno_iskustvo`, `idk_kandidat_jezici`, `idk_kandidat_vjestine`, `idk_kandidat_status`, `idk_kandidat_status_prijave`, `idk_kandidat_akademija`, `idk_kandidat_cv`, `idk_kandidat_de`, `idk_kandidat_financije`, `idk_kandidat_projekcije`, `idk_kandidati_contracts` i `idk_kandidati_grupe`.
- `idk_kandidat_radno_iskustvo.kri_kandidat_id`, `idk_kandidat_edukacija.ke_kandidat_id`, `idk_kandidat_vjestine.kv_kandidat_id` i slične ID-kolone su samo `ARBEITSANNAHME` za veze prema kandidatu; izvoz ne belegt foreign-key constraints ni kardinalnost.
- `idk_kandidat_pozicija` ima višejezične nazivkolone, source i active marker, ali nema kandidat-ID; veza prema iskustvu ili kontroliranoj pozicijskoj listi je `OFFEN`.
- `idk_kandidati_grupe` belegt grupni katalog, ali izvoz ne prikazuje članstvo kandidata u grupi. Moguća višestruka dodjela je `DURCH DISCOVERY ZU PRÜFEN`.
- Alternativni ili legacy kandidatski skupovi `idk_dak_kandidati`, `idk_nd_kandidata` i `idk_nd_kandidati_ciscenje` sadrže osjetljive kandidatkolone; autoritativnost i međusobno mapiranje su `OFFEN`.

## 6. Mehrsprachige und kontrollierte Felder

- `BELEGT DURCH SCHEMAEXPORT`: 37 kolona u 14 tabela imaju eksplicitne jezičke sufikse poput `_de`, `_en`, `_rs`, `_it` ili `_ba`.
- Primjeri su nazivi/opisi u `idk_kandidat_pozicija`, `idk_kandidat_edukacija`, `idk_kandidat_radno_iskustvo`, `idk_kandidat_jezici`, `idk_kandidat_vjestine` i `idk_partner_notification_logs`.
- `BELEGT DURCH SCHEMAEXPORT`: 151 kolona u 75 tabela imaju status/source/type/group/position slična imena. Da li predstavljaju kontrolirane domene, njihove dozvoljene vrijednosti i lookup veze ostaje `DURCH DISCOVERY ZU PRÜFEN`.
- Policy-only nazivi poput `idk_struke`, `idk_profil_kriterij`, `idk_pp_city` i `idk_pp_regions` signaliziraju moguće lookup/profil/lokacijske objekte, ali bez kolona nisu strukturno analizabilni.

## 7. Sensible Bereiche und Release-1-Ausschlüsse

- `BELEGT DURCH SCHEMAEXPORT`: postoje kolone čija imena označavaju ime/prezime, identifikacijske brojeve, pasoš, datum rođenja, adresu, e-mail, telefon, lozinku/token/PIN, CV, sliku, bilješke, opise, dokumente i ugovore.
- `idk_kandidati`, `idk_dak_kandidati`, `idk_nd_kandidata`, `idk_nd_kandidati_ciscenje`, `idk_kandidat_kontakt_info`, `idk_kandidat_cv`, dokumentne/ugovorne tabele i freetext/bilješke ostaju izvan svakog Release-1 outputa.
- Posebno se ne smiju izložiti credential-like schema površine kao `idk_api_clients.client_token` i `idk_kandidati.kandidat_password`; izvoz ne sadrži njihove vrijednosti.
- Pravni osnov i dozvoljenost obrade dobi/Geburtsdatum ostaju `OFFEN` i ne mogu se zaključiti iz fizičke kolone.

## 8. Relevanz für den Runtime-Such-MCP

`ARBEITSANNAHME`: za kasniji kontrolirani Search-RPC prvo treba evaluirati minimalni projekcijski sloj nad `idk_kandidati` te kandidat-bezogene strukture za pozicije, iskustvo, obrazovanje, jezike, vještine, status i grupe. Nijedan fizički naziv se ovim ne usvaja kao javni MCP ugovor. Kontakt, CV, ugovor, bilješka i drugi freetext moraju biti isključeni iz Releasea 1. Stvarne veze, selektivnost, kvaliteta, tenant scope i potrebni indeksi čekaju Gate B.

## 9. Relevanz für den getrennten Profilverwaltungs-MCP

`idk_nalog_profil` belegt samo profil-sličnu tabelu vezanu za `nalog_id`; njena semantika nije dokaz za Berufssuchprofil. `idk_profil_kriterij` i `idk_struke` pojavljuju se samo kao policy nazivi bez table definicije. Zato model draft/published verzija, kontroliranih Ausbildungs-/Erfahrungsberufe/Tätigkeiten i many-to-many članstva ostaje `OFFEN`. Prihvaćena odvojena trust boundary iz ADR-0003 ostaje nepromijenjena.

## 10. Fehlende Evidenz

- Nema row counta, uzorka podataka, data-quality metrike ni dokaza autoritativnosti.
- Nema foreign-key, unique, check, default ni identity/sequence detalja osim 100 označenih primary keyeva.
- Nema index definicija ili usage statistike.
- Nema schema-qualified naziva, view/materialized-view, function/RPC ni trigger inventara.
- RLS policy redovi su prikazani, ali RLS enabled/forced stanje, potpuni policy scope, role inheritance, grants i efektivna prava nisu dokazani.
- Tenant/partner/user semantika i izolacija nisu dokazani.
- Export je nepotpun: 88 policy-referenciranih objekata nema kolonski inventar.

## 11. Empfohlene nächste Discovery-Schritte

1. Redigirani izvještaj ljudski pregledati i potvrditi prioritet kandidatskih tabela.
2. Zasebno pribaviti schema-only izvoze za `crm_api` i `crm_auth`, svaki s vlastitim preflightom.
3. `auth`, `crm_audit`, `graphql`, `extensions` i `firstschema` zadržati izvan scopea do posebne freigabe.
4. Pripremiti Gate-B metadaten-discovery za schema-qualified objekte, constraints, indekse, RLS enabled/forced, policies, grants, funkcije i triggere.
5. Tek nakon Gate-B evidencije i korisničkih odluka izvesti kanonski Searchvertrag i Berufssuchprofil model.

## 12. Izvršne sigurnosne granice

Tokom ove analize nije uspostavljena nikakva Supabase/PostgreSQL veza, nije izvršen SQL, nije korišten Supabase-Plugin/MCP, nije promijenjena baza ili eksterni sistem i nije napravljen Git commit.

## Dodatak A – Potpuni strukturni inventar

Svaka tabela i kolona ispod je `BELEGT DURCH SCHEMAEXPORT`. `PK` označava izričito prikazani primary key, `NULL` prikazanu nullability, a `NOT NULL` odsustvo oznake `Nullable` u izvozu; posljednje je ograničeno formatom izvoza i treba potvrdu. `ID-Kandidat` nije FK dokaz.

### `idk_agenti_activity`

`id` `int4` (PK, NOT NULL); `employee_id` `int4` (NOT NULL, ID-Kandidat); `activity_status` `int4` (NULL); `activity_pocetak` `timestamp` (NULL); `activity_kraj` `timestamp` (NULL); `activity_ukupno` `time` (NULL); `activity_aktivan` `int4` (NOT NULL).

### `idk_analitika`

`analizika_id` `int4` (PK, NOT NULL); `analitika_rating` `int4` (NULL); `analitika_datum` `timestamp` (NULL).

### `idk_api_clients`

`client_id` `int4` (PK, NOT NULL); `client_name` `varchar` (NOT NULL); `client_token` `varchar` (NOT NULL).

### `idk_appointment_invite_links`

`id` `int4` (PK, NOT NULL); `candidate_id` `int4` (NOT NULL, ID-Kandidat); `interview_id` `int4` (NOT NULL, ID-Kandidat); `link_status` `int4` (NOT NULL); `date_sent` `timestamp` (NULL); `date_open` `timestamp` (NULL); `date_confirmed` `timestamp` (NULL); `date_archived` `timestamp` (NULL); `send_key` `varchar` (NOT NULL); `sent_days_before` `int4` (NULL); `counter_sent` `int4` (NOT NULL).

### `idk_bot_obavijesti`

`bo_id` `int4` (PK, NOT NULL); `bo_kandidat_id` `int4` (NOT NULL, ID-Kandidat); `bo_nalog_id` `int4` (NOT NULL, ID-Kandidat); `bo_poslana` `int4` (NOT NULL); `bo_odgovor` `int4` (NULL).

### `idk_candidate_language_logs`

`cll_id` `int4` (PK, NOT NULL); `cll_candidate_id` `int4` (NOT NULL, ID-Kandidat); `cll_cvl_id` `int4` (NOT NULL, ID-Kandidat); `cll_status` `int4` (NOT NULL); `cll_date` `timestamp` (NULL); `cll_employee_id` `int4` (NOT NULL, ID-Kandidat); `cll_days_count` `int4` (NULL).

### `idk_candidate_verified_languages`

`cvl_id` `int4` (PK, NOT NULL); `cvl_status` `int4` (NOT NULL); `cvl_active` `int4` (NOT NULL); `cvl_course1_started` `date` (NULL); `cvl_course1_ended` `date` (NULL); `cvl_course2_started` `date` (NULL); `cvl_course2_ended` `date` (NULL); `cvl_motive_start` `date` (NULL); `cvl_motive_end` `date` (NULL); `cvl_exam_date` `date` (NULL); `cvl_certificate_path` `text` (NULL); `cvl_certificate_upload_date` `timestamp` (NULL); `cvl_certficate_creation_date` `date` (NULL); `cvl_certificate_expiration_date` `date` (NULL); `cvl_last_updated` `timestamp` (NULL).

### `idk_chat_question`

`id` `int4` (PK, NOT NULL); `type` `text` (NOT NULL); `question_order` `int4` (NULL); `question` `text` (NOT NULL); `answer` `text` (NULL); `parentquestion` `int4` (NULL); `deletedat` `timestamp` (NULL).

### `idk_chat_type`

`id` `int4` (PK, NOT NULL); `name` `varchar` (NOT NULL).

### `idk_clients`

`client_id` `int4` (PK, NOT NULL); `client_name` `varchar` (NULL); `client_country` `varchar` (NULL); `client_region` `varchar` (NULL); `client_city` `varchar` (NULL); `client_address` `varchar` (NULL); `client_pp` `int4` (NULL); `client_telephone` `varchar` (NULL); `client_email` `varchar` (NULL); `client_origin` `int4` (NOT NULL); `client_recommendation` `int4` (NULL); `client_recommendation_company` `int4` (NULL); `client_fc_or_sales` `int4` (NOT NULL); `client_fc_status` `int4` (NOT NULL); `client_sales_status` `int4` (NOT NULL); `client_manager` `int4` (NULL); `client_sales_manager` `int4` (NULL); `client_datum_zvanja` `date` (NULL); `client_contract` `int4` (NOT NULL); `client_description` `text` (NULL).

### `idk_clients_stats`

`id` `int4` (PK, NOT NULL); `client_id` `int4` (NULL, ID-Kandidat); `status` `int4` (NULL); `fc_or_sales` `int4` (NULL); `date` `timestamp` (NULL); `zaposlenik_id` `int4` (NULL, ID-Kandidat); `stats_desc` `text` (NULL).

### `idk_companies`

`company_id` `int4` (PK, NOT NULL); `company_name` `varchar` (NOT NULL); `company_type` `varchar` (NULL); `company_idnum` `varchar` (NULL); `company_taxnum` `varchar` (NULL); `company_ceo` `int4` (NULL); `company_contact` `int4` (NULL); `company_address` `varchar` (NULL); `company_zipcode` `varchar` (NULL); `company_city` `varchar` (NULL); `company_state` `varchar` (NULL); `company_country` `varchar` (NULL); `company_info` `text` (NULL); `company_inote` `text` (NULL); `company_logo` `varchar` (NULL); `company_contact_type` `varchar` (NULL); `company_datetime` `timestamp` (NULL); `company_status` `int4` (NULL); `company_origin` `int4` (NOT NULL); `company_reccomendation` `int4` (NULL); `company_size` `varchar` (NULL); `js_partner_id` `int4` (NULL, ID-Kandidat); `company_message` `text` (NULL); `company_total_workers_required` `int4` (NULL); `company_professions` `text` (NULL).

### `idk_companies_info`

`comi_id` `int4` (PK, NOT NULL); `comi_group` `int4` (NOT NULL); `comi_title` `varchar` (NOT NULL); `comi_data` `varchar` (NOT NULL); `comi_primary` `int4` (NOT NULL); `comi_companyid` `int4` (NOT NULL).

### `idk_contacts`

`contact_id` `int4` (PK, NOT NULL); `contact_firstname` `varchar` (NOT NULL); `contact_lastname` `varchar` (NULL); `contact_nickname` `varchar` (NULL); `contact_dob` `date` (NULL); `contact_address` `varchar` (NULL); `contact_zipcode` `int4` (NULL); `contact_city` `varchar` (NULL); `contact_state` `varchar` (NULL); `contact_country` `varchar` (NULL); `contact_info` `text` (NULL); `contact_inote` `text` (NULL); `contact_image` `varchar` (NULL); `contact_type` `varchar` (NULL); `contact_companyid` `int4` (NOT NULL); `contact_clientid` `int4` (NULL); `contact_ownerid` `int4` (NULL); `contact_datetime` `timestamp` (NULL); `contact_status` `int4` (NOT NULL); `contact_job_title` `varchar` (NULL).

### `idk_contacts_info`

`ci_id` `int4` (PK, NOT NULL); `ci_group` `int4` (NOT NULL); `ci_title` `varchar` (NOT NULL); `ci_data` `varchar` (NOT NULL); `ci_primary` `int4` (NOT NULL); `ci_contactid` `int4` (NOT NULL).

### `idk_dak_kandidati`

`id_dak_kandidat` `int4` (PK, NOT NULL); `origin_dak_kandidat` `int4` (NULL); `tel_dak_kandidat` `varchar` (NULL); `hashedtel_idk_dak_kandidat` `text` (NULL); `telconfirm_dak_kandidat` `varchar` (NULL); `pin_dak_kandidat` `text` (NULL); `name_dak_kandidat` `varchar` (NULL); `lastname_dak_kandidat` `varchar` (NULL); `email_dak_kandidat` `varchar` (NULL); `contacttime_dak_kandidat` `timestamp` (NULL); `daypart_dak_kandidat` `int4` (NULL); `comment_dak_kandidat` `text` (NULL); `passport_dak_kandidat` `varchar` (NULL); `passporttime_dak_kandidat` `timestamp` (NULL); `contract_dak_kandidat` `varchar` (NULL); `contracttime_dak_kandidat` `timestamp` (NULL); `status_dak_kandidat` `int4` (NULL); `tipunosa_dak_kandidat` `int4` (NULL); `datumunosa_dak_kandidat` `timestamp` (NULL); `datumobrade_dak_kandidat` `timestamp` (NULL); `datumslanja_dak_kandidat` `timestamp` (NULL); `pocetakrada_dak_kandidat` `date` (NULL); `datumaktivacije_dak_kandidat` `timestamp` (NULL); `datumzavrsetka_dak_kandidat` `timestamp` (NULL); `datumstornoaktivacije_dak_kandidat` `timestamp` (NULL); `datumstornacije_dak_kandidat` `timestamp` (NULL); `company_dak_kandidat` `int4` (NULL); `nas_klijent_dak_kandidat` `int4` (NULL); `dipl_dak_kandidat` `int4` (NOT NULL); `osiguranje_dak_kandidat` `int4` (NOT NULL); `poslovnica_dak_kandidat` `int4` (NOT NULL); `rata1_dak_kandidat` `int4` (NOT NULL); `rata1_datum_dak_kandidat` `timestamp` (NULL); `rata2_dak_kandidat` `int4` (NOT NULL); `rata2_datum_dak_kandidat` `timestamp` (NULL); `manager_dak_kandidat` `int4` (NULL).

### `idk_documents`

`document_id` `int4` (PK, NOT NULL); `document_name` `varchar` (NOT NULL); `document_special_type` `int4` (NULL); `document_desc` `varchar` (NOT NULL); `document_file` `varchar` (NOT NULL); `document_icon` `varchar` (NOT NULL); `document_datetime` `timestamp` (NULL); `document_group` `int4` (NOT NULL); `document_dataid` `int4` (NOT NULL); `document_employeeid` `int4` (NOT NULL).

### `idk_duration_per_status`

`dpr_id` `int4` (PK, NOT NULL); `dpr_group` `int4` (NOT NULL); `dpr_status` `varchar` (NOT NULL); `dpr_duration` `int4` (NOT NULL); `dpr_description` `varchar` (NOT NULL); `dpr_status_name` `varchar` (NOT NULL).

### `idk_email_text`

`email_id` `int4` (PK, NOT NULL); `email_value` `varchar` (NOT NULL); `email_title` `varchar` (NOT NULL); `email_txt` `text` (NOT NULL).

### `idk_employees`

`employee_id` `int4` (PK, NOT NULL); `employee_firstname` `varchar` (NOT NULL); `employee_lastname` `varchar` (NOT NULL); `employee_email` `varchar` (NOT NULL); `employee_password` `varchar` (NOT NULL); `employee_key` `varchar` (NOT NULL); `employee_color` `varchar` (NULL); `employee_jmbg` `int8` (NULL); `employee_rfid` `varchar` (NOT NULL); `employee_position` `varchar` (NOT NULL); `employee_dob` `date` (NULL); `employee_doe` `date` (NULL); `employee_address` `text` (NOT NULL); `employee_city` `varchar` (NOT NULL); `employee_country` `varchar` (NOT NULL); `employee_info` `text` (NOT NULL); `employee_inote` `text` (NOT NULL); `employee_image` `varchar` (NOT NULL); `employee_status` `varchar` (NOT NULL); `employee_supervizor` `varchar` (NULL); `employee_dlanguage` `varchar` (NOT NULL); `employee_phone` `varchar` (NULL); `employee_warehouse` `int4` (NOT NULL); `employee_odjel` `int4` (NOT NULL); `employee_poslovnica` `int4` (NULL); `employee_nostrifikacija_diploma` `int4` (NULL); `employee_nostrifikacija_zadnji_menadzer` `int4` (NULL); `employee_nostrifikacija_zadnji_menadzer_app` `int4` (NULL); `employee_faktor_provizije_bih` `float8` (NOT NULL); `employee_faktor_provizije_srb` `float8` (NOT NULL); `employee_faktor_za_timove` `float8` (NOT NULL); `employee_team` `int4` (NOT NULL); `employee_viciuser` `varchar` (NULL); `employee_vicipass` `varchar` (NULL); `employee_reset_password` `int4` (NOT NULL); `employee_last_password_change` `timestamp` (NULL); `employee_reset_token` `varchar` (NULL); `employee_reset_token_doe` `timestamp` (NULL); `employee_dvag` `int4` (NOT NULL); `employee_makler_representative_status` `int4` (NOT NULL).

### `idk_employees_info`

`ei_id` `int4` (PK, NOT NULL); `ei_group` `int4` (NOT NULL); `ei_title` `varchar` (NOT NULL); `ei_data` `varchar` (NOT NULL); `ei_primary` `int4` (NOT NULL); `ei_employeeid` `int4` (NOT NULL).

### `idk_employees_reports`

`er_id` `int4` (PK, NOT NULL); `er_date` `date` (NULL); `er_title` `varchar` (NULL); `er_timefrom` `time` (NULL); `er_timeto` `time` (NULL); `er_projectid` `int4` (NULL); `er_nalogid` `int4` (NULL); `er_employeeid` `int4` (NOT NULL); `er_status` `int4` (NOT NULL).

### `idk_glossa_log`

`id` `int4` (PK, NOT NULL); `request` `text` (NOT NULL); `response` `text` (NOT NULL); `code` `int4` (NOT NULL); `candidate` `text` (NOT NULL); `request_endpoint` `varchar` (NOT NULL); `doe` `timestamp` (NULL).

### `idk_ipwhitelist`

`ipwl_id` `int4` (PK, NOT NULL); `ipwl_user` `varchar` (NOT NULL); `ipwl_ip` `varchar` (NOT NULL); `ipwl_added_by` `varchar` (NOT NULL); `ipwl_reason` `varchar` (NOT NULL); `ipwl_status` `int4` (NOT NULL); `ipwl_datetime` `timestamp` (NULL).

### `idk_jobstep_partners`

`jp_id` `int4` (PK, NOT NULL); `jp_imeprezime` `varchar` (NOT NULL); `jp_ime` `varchar` (NULL); `jp_prezime` `varchar` (NULL); `jp_email` `varchar` (NOT NULL); `jp_password` `varchar` (NOT NULL); `jp_lang` `varchar` (NULL); `jp_posta` `int4` (NULL); `jp_racun` `int4` (NULL); `jp_iban` `varchar` (NULL); `jp_swift` `varchar` (NULL); `jp_placanjeimeprezime` `varchar` (NULL); `jp_brtelefona` `varchar` (NULL); `jp_drzava` `varchar` (NULL); `jp_grad` `varchar` (NULL); `jp_postanskibroj` `int4` (NULL); `jp_ulica` `varchar` (NULL); `jp_provider` `varchar` (NULL); `jp_register_date` `timestamp` (NULL); `jp_fcmtoken` `varchar` (NULL); `jp_mailconfirmation_token` `varchar` (NOT NULL); `jp_confirmedaccount` `int4` (NOT NULL); `jp_position` `int4` (NULL); `jp_socialid` `text` (NULL); `jp_social_token` `text` (NULL); `jp_social_imgurl` `text` (NULL); `jp_preporuka_id` `int4` (NULL, ID-Kandidat); `jp_source` `int4` (NOT NULL); `jp_user_type` `int4` (NULL); `jp_user_permission` `int4` (NULL); `jp_partner_company` `int4` (NOT NULL); `jp_makler_id` `varchar` (NULL, ID-Kandidat); `jp_direction_number` `varchar` (NULL); `jp_region_de` `varchar` (NULL); `jp_spoken_languages` `text` (NULL); `jp_received_last_lead` `int4` (NULL); `jp_last_password_reset` `timestamptz` (NULL); `jp_makler_broj_direkcije` `varchar` (NULL); `jp_representative_employee_id` `int4` (NULL, ID-Kandidat); `jp_latest_login` `timestamp` (NULL); `jp_first_login` `timestamp` (NULL); `jp_datum_deaktivacije` `timestamp` (NULL); `jp_latest_activity` `timestamp` (NULL); `jp_tutorial_sent` `varchar` (NULL); `jp_password_reset_code` `varchar` (NULL); `jp_password_reset_datetime` `timestamptz` (NULL); `jp_password_reset_tries` `int4` (NULL); `jp_device` `varchar` (NULL); `jp_app_version` `varchar` (NULL).

### `idk_jobstep_partners_pregledi`

`jpp_id` `int4` (PK, NOT NULL); `jpp_partnerid` `varchar` (NOT NULL); `jpp_nalogid` `int4` (NOT NULL); `jpp_pregledi_count` `int4` (NOT NULL).

### `idk_kampanje_dipl`

`kd_id` `int4` (PK, NOT NULL); `kd_naziv` `varchar` (NOT NULL); `kd_skraceni_naziv` `varchar` (NULL); `kd_poruka_kampanje` `text` (NULL); `kd_jezik_forme` `varchar` (NOT NULL); `kd_drzava` `varchar` (NOT NULL); `kd_broj_pregleda` `int4` (NOT NULL); `kd_broj_prijavljenih` `int4` (NOT NULL); `kd_datum_kreiranja` `timestamp` (NULL); `kd_troskovi` `float8` (NULL); `kd_status` `int4` (NOT NULL); `kd_slike` `text` (NULL); `kd_category` `varchar` (NOT NULL).

### `idk_kandidat_akademija`

`ka_id` `int4` (PK, NOT NULL); `ka_kandidat_id` `int4` (NOT NULL, ID-Kandidat); `ka_nalog_id` `int4` (NOT NULL, ID-Kandidat); `ka_status` `int4` (NOT NULL); `ka_date_from` `date` (NULL); `ka_date_to` `date` (NULL); `ka_note` `text` (NULL); `ka_rating` `int4` (NULL).

### `idk_kandidat_cv`

`kcv_id` `int4` (PK, NOT NULL); `kcv_kandidatid` `int4` (NULL); `kcv_ba` `varchar` (NULL); `kcv_de` `varchar` (NULL).

### `idk_kandidat_de`

`kde_id` `int4` (PK, NOT NULL); `kde_kandidat_id` `int4` (NULL, ID-Kandidat); `kde_prijava_na` `varchar` (NULL); `kde_spol` `varchar` (NULL); `kde_drzavljanstvo` `varchar` (NULL); `kde_vozacka` `varchar` (NULL).

### `idk_kandidat_edukacija`

`ke_id` `int4` (PK, NOT NULL); `ke_orderid` `int4` (NOT NULL); `ke_datumod` `date` (NULL); `ke_datumdo` `date` (NULL); `ke_aktuelno` `int4` (NOT NULL); `ke_smjer_id` `int4` (NULL, ID-Kandidat); `ke_naziv_kvalifikacije` `varchar` (NOT NULL); `ke_naziv_kvalifikacije_de` `varchar` (NULL); `ke_skola_id` `int4` (NULL, ID-Kandidat); `ke_naziv` `varchar` (NULL); `ke_naziv_de` `varchar` (NULL); `ke_grad` `varchar` (NULL); `ke_grad_de` `varchar` (NULL); `ke_drzava` `varchar` (NULL); `ke_opis` `text` (NULL); `ke_opis_de` `text` (NULL); `ke_kandidat_id` `int4` (NOT NULL, ID-Kandidat); `ke_vrsta_obrazovanja` `varchar` (NULL); `ke_prikaz_pp` `int4` (NOT NULL).

### `idk_kandidat_financije`

`kf_id` `int4` (PK, NOT NULL); `nalog_id` `int4` (NOT NULL, ID-Kandidat); `projekt_id` `int4` (NULL, ID-Kandidat); `kandidat_id` `int4` (NOT NULL, ID-Kandidat); `kf_datum` `date` (NULL); `kf_datum_stvarni` `date` (NULL); `kf_nalog_rata_id` `int4` (NULL, ID-Kandidat); `kf_type` `int4` (NOT NULL); `kf_iznos` `float8` (NOT NULL); `kf_placeno` `int4` (NULL); `kf_datum_fakturisanja` `date` (NULL); `kf_datum_placanja` `date` (NULL); `kf_status` `int4` (NULL); `kf_zamjena_id` `int4` (NULL, ID-Kandidat).

### `idk_kandidat_jezici`

`kj_id` `int4` (PK, NOT NULL); `kj_naziv` `varchar` (NOT NULL); `kj_naziv_de` `varchar` (NULL); `kj_slusanje` `varchar` (NOT NULL); `kj_slusanje_de` `varchar` (NULL); `kj_citanje` `varchar` (NOT NULL); `kj_citanje_de` `varchar` (NULL); `kj_govorna_interakcija` `varchar` (NOT NULL); `kj_govorna_interakcija_de` `varchar` (NULL); `kj_govorna_produkcija` `varchar` (NOT NULL); `kj_govorna_produkcija_de` `varchar` (NULL); `kj_pisanje` `varchar` (NOT NULL); `kj_pisanje_de` `varchar` (NULL); `kj_kandidatid` `int4` (NOT NULL); `kj_ustanova` `int4` (NULL).

### `idk_kandidat_kontakt_info`

`kki_id` `int4` (PK, NOT NULL); `kki_orderid` `int4` (NULL); `kki_grupa` `int4` (NOT NULL); `kki_naziv` `varchar` (NOT NULL); `kki_naziv_de` `varchar` (NULL); `kki_podatak` `varchar` (NULL); `kki_kandidat_id` `int4` (NOT NULL, ID-Kandidat); `kki_primary` `int4` (NOT NULL).

### `idk_kandidat_pozicija`

`kp_id` `int4` (PK, NOT NULL); `kp_ime` `varchar` (NULL); `kp_ime_de` `varchar` (NULL); `kp_ime_en` `varchar` (NULL); `kp_ime_rs` `varchar` (NULL); `kp_opis` `text` (NULL); `kp_created_by` `int4` (NULL); `kp_source` `int4` (NOT NULL); `kp_active` `int4` (NOT NULL).

### `idk_kandidat_projekcije`

`kandidat_id` `int4` (PK, NOT NULL); `proracunati_pocetak_rada` `date` (NULL).

### `idk_kandidat_radno_iskustvo`

`kri_id` `int4` (PK, NOT NULL); `kri_order` `int4` (NULL); `kri_darum_od` `date` (NULL); `kri_datum_do` `date` (NULL); `kri_aktuelno` `int4` (NOT NULL); `kri_pozicija` `varchar` (NOT NULL); `kri_pozicija_de` `varchar` (NULL); `kri_pozicija_en` `varchar` (NULL); `kri_naziv` `varchar` (NOT NULL); `kri_naziv_de` `varchar` (NULL); `kri_grad` `varchar` (NULL); `kri_grad_de` `varchar` (NULL); `kri_drzava` `varchar` (NULL); `kri_adresa` `varchar` (NULL); `kri_telefon` `varchar` (NULL); `kri_email` `varchar` (NULL); `kri_web` `varchar` (NULL); `kri_opis` `text` (NULL); `kri_opis_de` `text` (NULL); `kri_kandidat_id` `int4` (NOT NULL, ID-Kandidat); `kri_prikaz_pp` `int4` (NOT NULL).

### `idk_kandidat_status`

`id` `int4` (PK, NOT NULL); `status_id` `int4` (NULL, ID-Kandidat); `status_naziv` `varchar` (NULL).

### `idk_kandidat_status_prijave`

`status_id` `int4` (PK, NOT NULL); `status_naziv` `varchar` (NOT NULL); `status_aktivan` `int4` (NOT NULL); `rezervisanje` `int4` (NOT NULL); `redoslijed_statusa` `int4` (NULL).

### `idk_kandidat_vjestine`

`kv_id` `int4` (PK, NOT NULL); `kv_naziv` `varchar` (NOT NULL); `kv_naziv_de` `text` (NULL); `kv_grupa` `int4` (NOT NULL); `kv_opis` `text` (NOT NULL); `kv_opis_de` `text` (NULL); `kv_kandidat_id` `int4` (NOT NULL, ID-Kandidat).

### `idk_kandidati`

`kandidat_id` `int4` (PK, NOT NULL); `kandidat_check` `varchar` (NOT NULL); `kandidat_ime` `varchar` (NOT NULL); `kandidat_prezime` `varchar` (NOT NULL); `kandidat_prijava_na` `varchar` (NOT NULL); `kandidat_spol` `varchar` (NULL); `kandidat_djevojackoprezime` `varchar` (NULL); `kandidat_jmbg` `varchar` (NULL); `kandidat_brojlk` `varchar` (NULL); `kandidat_broj_pasosa` `varchar` (NULL); `kandidat_datumrodjenja` `date` (NULL); `kandidat_mjestorodjenja` `varchar` (NULL); `kandidat_drzavljanstvo_vrsta` `varchar` (NULL); `kandidat_drzavarodjenja` `varchar` (NULL); `kandidat_drzavljanstvo` `varchar` (NULL); `kandidat_bracnostanje` `varchar` (NULL); `kandidat_bracnostanjeod` `date` (NULL); `kandidat_adresa` `text` (NULL); `kandidat_grad` `varchar` (NULL); `kandidat_pbroj` `int4` (NULL); `kandidat_drzava` `varchar` (NULL); `kandidat_email` `varchar` (NULL); `kandidat_mobitel` `varchar` (NULL); `kandidat_vozacka_dozvola` `varchar` (NULL); `kandidat_vozacka_kategorija` `varchar` (NULL); `kandidat_korisnickoime` `varchar` (NULL); `kandidat_password` `varchar` (NULL); `kandidat_slika` `varchar` (NOT NULL); `kandidat_status` `int4` (NOT NULL); `kandidat_status_messenger` `int4` (NOT NULL); `kandidat_datetime` `timestamp` (NULL); `kandidat_visitedurl` `int4` (NULL); `kandidat_group` `int4` (NOT NULL); `kandidat_mailsent` `int4` (NOT NULL); `datum_termina` `date` (NULL); `kandidat_bio_na_terminu` `int4` (NULL); `datum_aplikacije` `date` (NULL); `kandidat_procjenatermina` `int4` (NULL); `kandidat_viza` `int4` (NULL); `kandidat_viza_vrijedi_od` `date` (NULL); `kandidat_viza_vrijedi_do` `date` (NULL); `boravak_eu` `varchar` (NULL); `kandidat_status_prijave` `int4` (NULL); `kandidat_zaposlen_kod` `int4` (NULL); `cv_ba` `int4` (NULL); `cv_de` `int4` (NULL); `profile_ba` `int4` (NOT NULL); `profile_de` `int4` (NOT NULL); `kandidat_datum_ugovora` `date` (NULL); `kandidat_datum_ugovora_mjesec` `date` (NULL); `kandidat_datum_pocetakrada` `date` (NULL); `kandidat_datum_pocetakrada_mjesec` `date` (NULL); `kandidat_potencijalni_pocetak_rada` `varchar` (NULL); `kandidat_dogovoreni_pocetak_rada` `date` (NULL); `kandidat_potvrden_pocetak_rada` `int4` (NULL); `kandidat_partnerid` `int4` (NULL); `kandidat_partner_status` `int4` (NULL); `kandidat_poslan_sms` `varchar` (NULL); `kandidat_sms_id` `varchar` (NULL, ID-Kandidat); `kandidat_pogledao_link_prijave` `int4` (NOT NULL); `kandidat_poslan_dipl` `int4` (NOT NULL); `povezan_na_dipl` `int4` (NOT NULL); `kandidat_porijeklo` `int4` (NOT NULL); `struka_sa_prijave` `int4` (NULL); `kandidat_nalog_id` `int4` (NULL, ID-Kandidat); `kandidat_latest_reserved_time` `timestamp` (NULL); `kandidat_ppa_partner_id` `int4` (NULL, ID-Kandidat); `kandidat_pp_lokacija` `varchar` (NULL); `kandidat_pp_pozicija` `varchar` (NULL); `kandidat_pp_plata` `varchar` (NULL); `kandidat_pp_povezao_user_id` `int4` (NULL, ID-Kandidat); `kandidat_pp_razlog_odbijanja` `varchar` (NULL); `kandidat_pp_datum_prihvatanja` `date` (NULL); `kandidat_dipl_id` `int4` (NOT NULL, ID-Kandidat); `kandidat_ima_nostrifikaciju` `int4` (NULL); `kandidat_glossa` `int4` (NOT NULL); `kandidat_tf_status` `int4` (NULL); `kandidat_iskustvo_u_struci` `int4` (NULL); `kandidat_iskustvo_u_struci_trajanje` `int4` (NULL); `kandidat_termin_za_vizu` `int4` (NULL); `tf_reserved_agent` `int4` (NULL); `kandidat_nacin_odlaska` `int4` (NOT NULL); `kandidat_bracno_stanje` `int4` (NOT NULL); `kandidat_dostavljen_ugovor_jobstepu` `int4` (NULL); `kandidat_zeljena_regija` `int4` (NULL); `kandidat_zeljeni_grad` `int4` (NULL); `kandidat_partner_lead_status` `int4` (NULL); `zaduzeni_makler_id` `int4` (NULL, ID-Kandidat); `zaduzen_makleru_datum` `timestamp` (NULL); `zaduzeni_makler_reminder_datum` `date` (NULL); `kandidat_nivo_obrazovanja` `int4` (NULL); `kandidat_partner_lead_biljeska` `text` (NULL); `kandidat_destinacija_grad` `varchar` (NULL); `kandidat_destinacija_postanski_broj` `varchar` (NULL); `assigned_to_makler` `int4` (NULL); `kandidat_paralelno_zb` `int4` (NOT NULL); `kandidat_pogresan_broj` `int4` (NOT NULL); `kandidat_nedostupan` `int4` (NOT NULL); `kandidat_atu_paket` `int4` (NULL).

### `idk_kandidati_contracts`

`kc_id` `int4` (PK, NOT NULL); `kc_file_name` `varchar` (NULL); `kc_candidate_id` `int4` (NOT NULL, ID-Kandidat); `kc_source` `int4` (NOT NULL); `kc_user_id` `int4` (NOT NULL, ID-Kandidat); `kc_upload_time` `timestamp` (NULL); `kc_nalog_id` `int4` (NOT NULL, ID-Kandidat); `kc_partner_id` `int4` (NULL, ID-Kandidat); `kc_signed` `int4` (NOT NULL); `kc_visibility_status` `int4` (NOT NULL).

### `idk_kandidati_grupe`

`kg_id` `int4` (PK, NOT NULL); `kg_title` `varchar` (NOT NULL); `kg_title_de` `varchar` (NULL); `kg_title_it` `varchar` (NULL); `kg_date` `timestamp` (NULL); `kg_employeeid` `int4` (NOT NULL); `kg_status` `int4` (NOT NULL).

### `idk_kandidati_reject_reasons`

`krr_id` `int4` (PK, NOT NULL); `krr_reason_id` `int4` (NOT NULL, ID-Kandidat); `krr_candidate_id` `int4` (NOT NULL, ID-Kandidat); `krr_nalog_id` `int4` (NOT NULL, ID-Kandidat); `krr_partner_id` `int4` (NULL, ID-Kandidat); `krr_apointment_id` `int4` (NULL, ID-Kandidat); `krr_description` `text` (NULL); `krr_source` `int4` (NOT NULL); `krr_done_by` `int4` (NOT NULL); `krr_date` `timestamp` (NULL); `krr_last_status` `int4` (NOT NULL).

### `idk_kategorije`

`kategorija_id` `int4` (PK, NOT NULL); `kategorija_naziv` `text` (NULL).

### `idk_kategorije_provizija`

`kp_id` `int4` (PK, NOT NULL); `kp_naziv` `varchar` (NOT NULL); `kp_iznos` `float8` (NOT NULL); `kp_iznos_rs` `float8` (NOT NULL); `kp_faktorizacija` `int4` (NOT NULL); `kp_tip_id` `int4` (NOT NULL, ID-Kandidat); `kp_status` `int4` (NOT NULL); `kp_odjeli` `text` (NULL); `kp_vrsta` `int4` (NOT NULL); `kp_employee_id` `int4` (NULL, ID-Kandidat).

### `idk_korisni_dokumenti`

`kd_id` `int4` (PK, NOT NULL); `kd_naziv` `varchar` (NOT NULL); `kd_detaljni_opis` `text` (NULL); `kd_file` `varchar` (NOT NULL); `kd_icon` `varchar` (NOT NULL); `kd_datetime` `timestamp` (NULL); `kd_employee_id` `int4` (NOT NULL, ID-Kandidat); `kd_status` `int4` (NOT NULL).

### `idk_korisni_linkovi`

`kl_id` `int4` (PK, NOT NULL); `kl_naziv` `text` (NOT NULL); `kl_detaljni_opis` `text` (NULL); `kl_link` `text` (NOT NULL); `kl_datetime` `timestamp` (NULL); `kl_employee_id` `int4` (NOT NULL, ID-Kandidat); `kl_status` `int4` (NOT NULL).

### `idk_link_generator`

`lg_id` `int4` (PK, NOT NULL); `lg_link_prijave` `varchar` (NULL); `idk_urlimg_prijave` `varchar` (NULL); `lg_url` `varchar` (NOT NULL); `lg_desc` `varchar` (NOT NULL); `lg_status` `int4` (NOT NULL); `lg_employeeid` `int4` (NOT NULL); `lg_datetime` `timestamp` (NULL); `lg_project` `int4` (NULL); `lg_nalogid` `int4` (NULL); `lg_language` `varchar` (NULL); `lg_troskovi` `float8` (NULL); `lg_broj_pregleda` `int4` (NOT NULL); `lg_partner_app` `int4` (NOT NULL).

### `idk_link_generator_rel`

`lr_id` `int4` (PK, NOT NULL); `lr_lgid` `int4` (NOT NULL); `lr_groupid` `int4` (NOT NULL).

### `idk_link_projects`

`lp_id` `int4` (PK, NOT NULL); `lp_linkid` `int4` (NOT NULL); `lp_projectid` `int4` (NOT NULL).

### `idk_log_kandidat_statusi`

`lks_id` `int4` (PK, NOT NULL); `lks_kandidat_id` `int4` (NOT NULL, ID-Kandidat); `lks_status_obrade` `int4` (NOT NULL); `lks_status_messenger` `int4` (NOT NULL); `lks_datetime` `timestamp` (NULL); `lks_employee_id` `int4` (NULL, ID-Kandidat); `lks_broj_dana` `int4` (NULL); `lks_link_id` `int4` (NULL, ID-Kandidat).

### `idk_log_statusi_prijave`

`lsp_id` `int4` (PK, NOT NULL); `lsp_kandidat_id` `int4` (NOT NULL, ID-Kandidat); `lsp_projekt_id` `int4` (NULL, ID-Kandidat); `lsp_status_prijave_id` `int4` (NOT NULL, ID-Kandidat); `lsp_employee_id` `int4` (NULL, ID-Kandidat); `lsp_izvor` `int4` (NOT NULL); `lsp_datetime` `timestamp` (NULL); `lsp_broj_dana` `int4` (NULL).

### `idk_logs`

`log_id` `int4` (PK, NOT NULL); `log_employeeid` `int4` (NOT NULL); `log_desc` `text` (NOT NULL); `log_date` `timestamp` (NULL); `log_type` `int4` (NOT NULL).

### `idk_messages`

`message_id` `int4` (PK, NOT NULL); `message_subject` `varchar` (NOT NULL); `message_text` `text` (NOT NULL); `message_sentid` `int4` (NOT NULL); `message_status` `int4` (NOT NULL); `message_datetime` `timestamp` (NULL).

### `idk_messages_users`

`mu_id` `int4` (PK, NOT NULL); `mu_messageid` `int4` (NOT NULL); `mu_employeeid` `int4` (NOT NULL); `mu_status` `int4` (NOT NULL).

### `idk_messenger_obavijesti`

`mo_id` `int4` (PK, NOT NULL); `mo_kandidat_id` `int4` (NOT NULL, ID-Kandidat); `mo_tip` `int4` (NOT NULL); `mo_datum_slanja` `timestamp` (NULL).

### `idk_module_permissions`

`mp_id` `int4` (PK, NOT NULL); `mp_name` `varchar` (NOT NULL); `mp_employees` `varchar` (NULL).

### `idk_modules`

`module_id` `int4` (PK, NOT NULL); `module_name` `varchar` (NOT NULL); `module_status` `int4` (NOT NULL); `module_desc` `text` (NOT NULL).

### `idk_nalog_financije`

`nf_id` `int4` (PK, NOT NULL); `nf_nalog_id` `int4` (NOT NULL, ID-Kandidat); `nf_datum_aktiviranja` `date` (NULL); `nf_type` `int4` (NULL); `nf_broj_rate` `int4` (NULL); `nf_iznos` `float8` (NOT NULL); `nf_placeno` `int4` (NOT NULL); `nf_datum_fakturisanja` `date` (NULL); `nf_datum_placanja` `date` (NULL); `nf_desc` `varchar` (NULL).

### `idk_nalog_profil`

`id` `int4` (PK, NOT NULL); `naziv` `varchar` (NOT NULL); `zaposlenik` `int4` (NOT NULL); `status` `int4` (NOT NULL); `prioritet` `int4` (NOT NULL); `doe` `timestamptz` (NOT NULL); `nalog_id` `int4` (NOT NULL, ID-Kandidat).

### `idk_nalog_smjer`

`id` `int4` (PK, NOT NULL); `nalog_id` `int4` (NOT NULL, ID-Kandidat); `smjer_id` `int4` (NOT NULL, ID-Kandidat).

### `idk_nalozi`

`nalog_id` `int4` (PK, NOT NULL); `kompanija_id` `int4` (NULL, ID-Kandidat); `employee_id` `int4` (NULL, ID-Kandidat); `nalog_broj` `varchar` (NULL); `nalog_naziv` `varchar` (NULL); `nalog_opis` `text` (NULL); `nalog_kreirano` `timestamptz` (NOT NULL); `nalog_datum_potpisa_naloga` `date` (NULL); `nalog_status` `int4` (NULL); `nalog_marketing_menadzer` `int4` (NULL); `nalog_ugovor` `varchar` (NULL); `nalog_potrebno_kandidata` `int4` (NULL); `nalog_provizija` `float8` (NULL); `nalog_provizija_po_plati` `float8` (NULL); `nalog_broj_rata` `int4` (NULL); `nalog_procenat_avansa` `int4` (NULL); `nalog_placa_nostrifikaciju` `int4` (NOT NULL); `nalog_nacin_nostrifikacije` `int4` (NULL); `nalog_provizija_nostrifikacija` `float8` (NULL); `nalog_broj_rata_nostrifikacija` `int4` (NULL); `nalog_firma_fakturisanja` `int4` (NULL); `nalog_placena_prva_rata` `int4` (NOT NULL); `nalog_financije` `int4` (NOT NULL); `nalog_akademija` `int4` (NOT NULL); `nalog_provizija_akademija` `int4` (NULL); `nalog_nacin_akademija` `int4` (NULL); `nalog_broj_dana_akademija` `int4` (NULL); `nalog_partner_active` `int4` (NOT NULL); `nalog_partner_provizija` `float8` (NULL); `pristup_poslodavcima` `int4` (NOT NULL); `partneri_pp` `int4` (NOT NULL); `nalog_prioritet` `int4` (NULL); `nalog_slanje_na_glosu` `int4` (NOT NULL); `nalog_dospijece` `int4` (NOT NULL); `nalog_smjerovi_kriterij` `int4` (NOT NULL); `nalog_js_partner_id` `int4` (NULL, ID-Kandidat); `nalog_partner_app_title` `varchar` (NULL); `nalog_partner_app_location` `varchar` (NULL); `nalog_partner_app_until` `timestamp` (NULL); `nalog_partner_app_salary` `varchar` (NULL); `nalog_poslodavac_trazi_jezik` `int4` (NOT NULL); `nalog_poslodavac_koristi_pp` `int4` (NOT NULL); `offers_and_benefits_of_employers` `text` (NULL).

### `idk_nalozi_blokovi_prijave`

`nbp_id` `int4` (PK, NOT NULL); `nbp_nalogid` `int4` (NOT NULL); `nbp_vozacka` `varchar` (NOT NULL); `nbp_vozacka_kategorija` `varchar` (NULL); `nbp_visoko_obr` `int4` (NOT NULL); `nbp_dodatno_obr` `int4` (NOT NULL); `nbp_korak4` `int4` (NOT NULL); `nbp_njemacki_jezik` `varchar` (NOT NULL); `nbp_ostali_jezici` `varchar` (NOT NULL); `nbp_korak7` `int4` (NOT NULL); `nbp_slika` `int4` (NOT NULL); `nbp_diploma` `int4` (NOT NULL); `nbp_pripravnicki` `int4` (NOT NULL); `nbp_strucni` `int4` (NOT NULL); `nbp_jezik_cert` `int4` (NOT NULL); `nbp_struka` `varchar` (NULL); `nbp_iskustvo_u_struci` `int4` (NOT NULL); `nbp_iskustvo_u_struci_trajanje` `int4` (NULL); `nbp_kandidat_starost_od` `int4` (NULL); `nbp_kandidat_starost_do` `int4` (NULL).

### `idk_nalozi_log`

`n_log_id` `int4` (PK, NOT NULL); `n_log_nalogid` `int4` (NOT NULL); `n_log_employeeid` `int4` (NOT NULL); `n_log_status` `int4` (NOT NULL); `n_log_vrijeme` `timestamptz` (NOT NULL).

### `idk_nalozi_opis`

`no_id` `int4` (PK, NOT NULL); `no_lang` `varchar` (NOT NULL); `no_nalogid` `int4` (NOT NULL); `no_nalognaziv` `varchar` (NOT NULL); `no_nalogopis` `text` (NOT NULL).

### `idk_nalozi_rate`

`nr_id` `int4` (PK, NOT NULL); `nr_nalog` `int4` (NOT NULL); `nr_rata` `int4` (NOT NULL); `nr_procenat` `int4` (NULL); `nr_vrijeme_placanja` `varchar` (NULL); `nr_datum` `date` (NULL); `nr_mjeseci_nakon` `int4` (NULL).

### `idk_nd_cron_export`

`id_c` `int4` (PK, NOT NULL); `type_c` `int4` (NULL); `result_c` `text` (NULL); `datetime_c` `timestamp` (NULL); `date_c` `date` (NULL); `sending_type_c` `int4` (NULL); `sent_to_employees_c` `text` (NULL); `download_employees_c` `text` (NULL); `settings_id` `int4` (NULL, ID-Kandidat).

### `idk_nd_cron_settings`

`id_s` `int4` (PK, NOT NULL); `type_s` `int4` (NULL); `status_s` `int4` (NULL); `employees_s` `text` (NULL); `control_employees_s` `text` (NULL); `candidate_status_s` `int4` (NULL); `status_days_s` `int4` (NULL); `communication_days_s` `int4` (NULL); `start_day_s` `timestamp` (NULL); `end_day_s` `timestamp` (NULL).

### `idk_nd_kandidata`

`id_broj_nd_kandidata` `int4` (PK, NOT NULL); `ime_nd_kandidata` `varchar` (NULL); `prezime_nd_kandidata` `varchar` (NULL); `ulica_nd_kandidata` `varchar` (NULL); `postanski_broj_nd_kandidata` `int4` (NULL); `grad_nd_kandidata` `varchar` (NULL); `ulica_bor_nd_kandidata` `varchar` (NULL); `postanski_broj_bor_nd_kandidata` `int4` (NULL); `grad_bor_nd_kandidata` `varchar` (NULL); `mobilni_nd_kandidata` `varchar` (NULL); `email_nd_kandidata` `varchar` (NULL); `izdao_licnu_nd_kandidata` `varchar` (NULL); `jmbg_nd_kandidata` `varchar` (NULL); `broj_licne_karte_nd_kandidata` `varchar` (NULL); `skola_nd_kandidata` `int4` (NULL); `skola_smjer_nd_kandidata` `int4` (NULL); `poslodavac_nd_kandidata` `int4` (NULL); `poslodavac_nas_nd_kandidata` `int4` (NULL); `poslodavac_naziv_nas_nd_kandidata` `int4` (NULL); `poslodavac_naziv_nd_kandidata` `varchar` (NULL); `poslodavac_ulica_nd_kandidata` `varchar` (NULL); `poslodavac_postanski_broj_nd_kandidata` `int4` (NULL); `poslodavac_grad_nd_kandidata` `varchar` (NULL); `poslodavac_regija_nd_kandidata` `varchar` (NULL); `poslodavac_drzava_nd_kandidata` `varchar` (NULL); `poslodavac_ime_nd_kandidata` `varchar` (NULL); `poslodavac_prezime_nd_kandidata` `varchar` (NULL); `poslodavac_mail_nd_kandidata` `varchar` (NULL); `poslodavac_mobilni_nd_kandidata` `varchar` (NULL); `komentar_nd_kandidata` `text` (NULL); `vrijeme_kreiranja_nd_kandidata` `timestamp` (NULL); `dodao_zaposlenik_nd_kandidata` `int4` (NULL); `zaduzen_zaposlenik_nd_kandidata` `int4` (NULL); `tim_nd_kandidata` `int4` (NOT NULL); `status_nd_kandidata` `int4` (NULL); `pstatus_nd_kandidata` `int4` (NOT NULL); `idd_ustanova_nd` `int4` (NULL); `broj_zahtjeva_na_ustanovi_nd_kandidata` `varchar` (NULL); `idd_kontakt_ustanova_nd` `int4` (NULL); `tracking_number_nd_kandidata` `varchar` (NULL); `link_tracking_number_nd_kandidata` `int4` (NULL); `vrsta_ugovora_nd_kandidata` `int4` (NULL); `rata1_nd_kandidata` `int4` (NOT NULL); `rata1_vrijeme_nd_kandidata` `timestamp` (NULL); `rata2_nd_kandidata` `int4` (NOT NULL); `rata2_vrijeme_nd_kandidata` `timestamp` (NULL); `povijest_nd_kandidata` `int4` (NOT NULL); `povijest_vrsta_nd_kandidata` `int4` (NULL); `kandidat_idd` `int4` (NULL); `partner_nd_status` `int4` (NULL); `kampanja_id` `int4` (NULL, ID-Kandidat); `datum_rodjenja` `date` (NULL); `in_vici_dial` `int4` (NOT NULL); `status_pp` `int4` (NOT NULL); `vrijeme_zakaznog_poziva` `timestamp` (NULL); `status_zakaznog_poziva` `int4` (NULL); `zadnja_komunikacija` `timestamp` (NULL); `chat_slike` `text` (NULL); `vrsta_obrade` `int4` (NOT NULL); `nivo_poznavanja_jezika` `int4` (NOT NULL); `certifikat_nd_kandidata` `int4` (NOT NULL); `inbound_aktivan` `int4` (NOT NULL); `poslan_spisak_datum` `date` (NULL); `dokumentacija_kompletna_datum` `date` (NULL); `na_prevodu_datum` `date` (NULL); `prevod_zavrsen_datum` `date` (NULL); `poslana_posta_datum` `date` (NULL); `zaprimljena_dokumentacija_datum` `date` (NULL); `stigla_taksa_dopuna_datum` `date` (NULL); `placena_taksa_poslana_dopuna_datum` `date` (NULL); `zavrsen_datum` `date` (NULL).

### `idk_nd_kandidata_biljeske`

`id_biljeska_nd` `int4` (PK, NOT NULL); `id_kandidata_biljeska_nd` `int4` (NULL); `status_biljeska_nd` `int4` (NULL); `tip_biljeska_nd` `int4` (NOT NULL); `razlog_biljeska_nd` `int4` (NULL); `sadrzaj_biljeska_nd` `text` (NULL); `vrijeme_dodavanja_biljeska_nd` `timestamp` (NULL); `vrijeme_grupa_biljeska_nd` `int4` (NULL); `dodao_zaposlenik_biljeska_nd` `int4` (NULL); `predracun_id` `int4` (NULL, ID-Kandidat); `predracun_status` `int4` (NULL); `vrijeme_ponovnog_zvanja` `timestamp` (NULL); `uplata_na_datum` `timestamp` (NULL); `zadnja_inkaso_biljeska` `int4` (NOT NULL); `prilog_biljeska_nd` `text` (NULL).

### `idk_nd_kandidata_dokumenti`

`id_dokument_nd` `int4` (PK, NOT NULL); `naziv_dokument_nd` `varchar` (NULL); `naziv_dokument_ostali_nd` `varchar` (NULL); `status_dokument_nd` `int4` (NULL); `id_kandidata_dokument_nd` `int4` (NULL); `vrijeme_dodavanja_dokument_nd` `timestamp` (NULL); `dodao_zaposlenik_dokument_nd` `int4` (NULL); `tip_dokumenta` `int4` (NULL); `tip_dokumenta_status` `int4` (NOT NULL); `broj_rate` `int4` (NOT NULL).

### `idk_nd_kandidata_status_log`

`id_log_status_nd_kandidata` `int4` (PK, NOT NULL); `idd_broj_nd_kandidata` `int4` (NULL); `status_nd_kandidata` `int4` (NULL); `pstatus_nd_kandidata` `int4` (NOT NULL); `vrijeme_promjene_statusa_nd_kandidata` `timestamp` (NULL); `broj_dana_statusa_nd_kandidata` `int4` (NULL); `promjenio_zaposlenik_nd_kandidata` `int4` (NULL).

### `idk_nd_kandidati_ciscenje`

`kandidat_ciscenje_id` `int4` (PK, NOT NULL); `id_kandidata_dipl` `int4` (NOT NULL); `ime_kandidata` `varchar` (NOT NULL); `prezime_kandidata` `varchar` (NOT NULL); `hash_id_dipl` `varchar` (NOT NULL); `status_informacija` `int4` (NOT NULL); `status_pracenja` `int4` (NOT NULL); `broj_telefona` `varchar` (NOT NULL); `id_kandidata_posao` `int4` (NULL); `arhiva` `int4` (NOT NULL); `treba_prebaciti_jezik_u_dipl` `int4` (NULL); `znanje_jezika_iz_idk_kan_jezici` `varchar` (NULL); `treba_prebaciti_skolu_smjer_u_dipl` `int4` (NULL); `skola` `int4` (NULL); `smjer` `int4` (NULL).

### `idk_nd_limiti`

`lt_id` `int4` (PK, NOT NULL); `lt_emp_id` `int4` (NULL, ID-Kandidat); `lt_drzava` `varchar` (NULL); `lt_dnevni` `int4` (NOT NULL); `lt_sedmicni` `int4` (NOT NULL); `lt_mjesecni` `int4` (NOT NULL); `lt_dnevni_cnt` `int4` (NOT NULL); `lt_sedmicni_cnt` `int4` (NOT NULL); `lt_mjesecni_cnt` `int4` (NOT NULL); `lt_zadnji_dobio_bih` `int4` (NULL); `lt_zadnji_dobio_srb` `int4` (NULL); `lt_zadnji_dobio_de` `int4` (NULL); `lt_zadnji_dobio_ostalo` `int4` (NULL); `lt_campaign_category` `varchar` (NOT NULL).

### `idk_nd_menadzeri_statistike`

`id_stat` `int4` (PK, NOT NULL); `idd_broj_nd_kandidata` `int4` (NULL); `zaduzen_zaposlenik_id` `int4` (NULL, ID-Kandidat); `prethodni_zaposlenik_id` `int4` (NULL, ID-Kandidat); `vrsta_aktivnosti` `int4` (NULL); `vrijeme_aktivnosti` `timestamp` (NULL).

### `idk_nd_naplata_preko`

`id` `int4` (PK, NOT NULL); `naplata_preko` `varchar` (NOT NULL); `drzava` `varchar` (NULL); `fk_naplata_preko` `int4` (NOT NULL); `aktivno` `int4` (NOT NULL); `datum_aktivacije` `timestamp` (NULL).

### `idk_nd_poste`

`id_poste` `int4` (PK, NOT NULL); `naziv_poste` `varchar` (NULL); `link_poste` `text` (NULL).

### `idk_nd_rate`

`id_r` `int4` (PK, NOT NULL); `id_nd_kan` `int4` (NULL); `br_r` `int4` (NULL); `vr_u_r` `timestamp` (NULL).

### `idk_nd_termini`

`termin_id` `int4` (PK, NOT NULL); `termin_kandidat_id` `int4` (NULL, ID-Kandidat); `termin_vrijeme` `timestamp` (NULL); `termin_kandidat_status` `int4` (NULL); `termin_kandidat_pstatus` `int4` (NULL); `termin_status` `int4` (NULL); `termin_zaposlenik_id` `int4` (NULL, ID-Kandidat); `termin_biljeska_id` `int4` (NULL, ID-Kandidat).

### `idk_nd_ugovori`

`ug_id` `int4` (PK, NOT NULL); `ug_kandidat_id` `int4` (NOT NULL, ID-Kandidat); `ug_broj` `varchar` (NULL); `ug_vrsta` `int4` (NULL); `ug_zaposlenik_id` `int4` (NOT NULL, ID-Kandidat); `ug_token` `varchar` (NOT NULL); `ug_jezik` `varchar` (NULL); `ug_file` `varchar` (NULL); `ug_file_de` `varchar` (NULL); `ug_status` `int4` (NOT NULL); `ug_datum_arhiviranja` `timestamp` (NULL); `ug_datum_slanja` `timestamp` (NULL); `ug_datum_prihvatanja` `timestamp` (NULL); `ug_datum_odbijanja` `timestamp` (NULL); `ug_datum_otvaranja_linka` `timestamp` (NULL); `ug_ip_adresa` `varchar` (NULL); `ug_timestamp` `varchar` (NULL); `ug_razlog_odbijanja` `int4` (NULL); `ug_komentar` `text` (NULL).

### `idk_nd_ustanove`

`id_ustanove_nd` `int4` (PK, NOT NULL); `naziv_ustanove_nd` `varchar` (NULL); `ulica_ustanove_nd` `varchar` (NULL); `postanski_broj_ustanove_nd` `int4` (NULL); `grad_ustanove_nd` `varchar` (NULL); `regija_da_ne_ustanove_nd` `int4` (NULL); `naziv_regije_ustanove_nd` `varchar` (NULL); `drzava_ustanove_nd` `varchar` (NULL); `period_nostrifikacije_ustanove_nd` `int4` (NULL); `napomena_ustanove_nd` `text` (NULL); `datum_registracije_ustanove_nd` `timestamp` (NULL); `dodao_zaposlenik_ustanove_nd` `int4` (NULL).

### `idk_nd_ustanove_biljeske`

`id_biljeska_nd` `int4` (PK, NOT NULL); `id_ustanova_biljeska_nd` `int4` (NULL); `sadrzaj_biljeska_nd` `text` (NULL); `vrijeme_dodavanja_biljeska_nd` `timestamp` (NULL); `vrijeme_grupa_biljeska_nd` `int4` (NULL); `dodao_zaposlenik_biljeska_nd` `int4` (NULL).

### `idk_nd_ustanove_kontakti`

`id_kontakt_ustanove_nd` `int4` (PK, NOT NULL); `ime_kontakt_ustanove_nd` `varchar` (NULL); `prezime_kontakt_ustanove_nd` `varchar` (NULL); `email_kontakt_ustanove_nd` `varchar` (NULL); `broj_telefona_kontakt_ustanove_nd` `varchar` (NULL); `zaduzenje_kontakt_ustanove_nd` `text` (NULL); `idd_ustanove_nd` `int4` (NULL).

### `idk_nd_ustanove_skola`

`id_skole_ustanove_nd` `int4` (PK, NOT NULL); `skola_idd` `int4` (NULL); `idd_ustanove_nd` `int4` (NULL).

### `idk_nd_ustanove_skole_smjerovi`

`id_skole_smjer_ustanove_nd` `int4` (PK, NOT NULL); `idd_skole_ustanove_nd` `int4` (NULL); `ss_idd` `int4` (NULL).

### `idk_nd_ustanove_tip_dokumenta`

`id_tip_dokumenta_ustanove_nd` `int4` (PK, NOT NULL); `povezanost_dokumenta_ustanove_nd` `int4` (NULL); `naziv_tip_dokumenta_ustanove_nd` `varchar` (NULL); `obaveznost_dokumenta_ustanove_nd` `int4` (NULL); `idd_ustanove_nd` `int4` (NULL); `idd_skole_ustanove_nd` `int4` (NULL); `idd_skole_smjer_ustanove_nd` `int4` (NULL); `template_dokumenta_ustanove_nd` `int4` (NULL); `template_naziv_dokumenta_ustanove_nd` `varchar` (NULL).

### `idk_nedostupan_log`

`id` `int4` (PK, NOT NULL); `kandidat` `int4` (NOT NULL); `nalog` `int4` (NOT NULL); `agent` `int4` (NOT NULL); `brojac` `int4` (NOT NULL); `status` `int4` (NOT NULL); `doe` `timestamptz` (NOT NULL).

### `idk_nostrifikovane_diplome`

`id_nd` `int4` (PK, NOT NULL); `id_cand_dipl` `int4` (NULL); `id_cand_job` `int4` (NULL); `file_nd` `text` (NOT NULL); `upload_date_nd` `timestamp` (NULL); `upload_employee_id` `int4` (NULL, ID-Kandidat); `full_recognition` `int4` (NULL).

### `idk_notes`

`note_id` `int4` (PK, NOT NULL); `note_txt` `text` (NOT NULL); `note_files` `text` (NULL); `note_datetime` `timestamp` (NULL); `note_group` `int4` (NOT NULL); `note_dataid` `int4` (NOT NULL); `note_employeeid` `int4` (NOT NULL).

### `idk_notification`

`not_id` `int4` (PK, NOT NULL); `not_kandidatid` `int4` (NOT NULL); `not_text` `text` (NOT NULL); `not_url` `varchar` (NOT NULL); `not_date` `timestamp` (NULL); `not_type` `int4` (NOT NULL); `not_status` `int4` (NOT NULL).

### `idk_notifications`

`notification_id` `int4` (PK, NOT NULL); `notification_datetime` `timestamp` (NULL); `notification_title` `varchar` (NOT NULL); `notification_icon` `varchar` (NOT NULL); `notification_link` `varchar` (NOT NULL); `notification_employeeid` `int4` (NOT NULL); `notification_status` `int4` (NOT NULL).

### `idk_obracuni`

`id` `int4` (PK, NOT NULL); `employee_id` `int4` (NOT NULL, ID-Kandidat); `predracun_id` `int4` (NOT NULL, ID-Kandidat); `status_predracuna` `int4` (NOT NULL); `status_obracuna` `int4` (NOT NULL); `valuta` `varchar` (NOT NULL); `rata` `int4` (NOT NULL); `broj_rata` `int4` (NOT NULL); `vrijednost_tipa` `float8` (NOT NULL); `vrijednost_kategorije` `float8` (NOT NULL); `iznos_obracuna_bam` `float8` (NOT NULL); `iznos_obracuna_rsd` `float8` (NOT NULL); `iznos_obracuna_eur` `float8` (NOT NULL); `vrijeme_kreiranja` `timestamp` (NULL); `vrijeme_uplate` `timestamp` (NULL); `vrijeme_isplate` `timestamp` (NULL); `tip_provizije` `int4` (NOT NULL); `kategorija_provizije` `int4` (NULL).

### `idk_ostatci_obracuna`

`oo_id` `int4` (PK, NOT NULL); `oo_employee_id` `int4` (NOT NULL, ID-Kandidat); `oo_valuta` `varchar` (NOT NULL); `oo_iznos` `float8` (NOT NULL); `oo_vrijeme_kreiranja` `timestamp` (NULL); `oo_period_od` `timestamp` (NULL); `oo_period_do` `timestamp` (NULL); `oo_status` `int4` (NOT NULL).

### `idk_otherdata`

`otherdata_id` `int4` (PK, NOT NULL); `otherdata_data` `varchar` (NOT NULL); `otherdata_group` `int4` (NOT NULL).

### `idk_partner_companies`

`pc_id` `int4` (PK, NOT NULL); `pc_name` `varchar` (NOT NULL); `pc_primary_color` `json` (NULL); `pc_logo` `varchar` (NULL).

### `idk_partner_meetings`

`id` `int4` (PK, NOT NULL); `meeting_appointment` `timestamp` (NULL); `meeting_type` `varchar` (NOT NULL); `meeting_company_id` `int4` (NULL, ID-Kandidat); `meeting_employee` `int4` (NOT NULL).

### `idk_partner_notification`

`notification_id` `int4` (PK, NOT NULL); `notification_type_id` `int4` (NOT NULL, ID-Kandidat); `notification_audience` `varchar` (NOT NULL); `notification_payload` `text` (NOT NULL); `notification_sent_at` `timestamp` (NULL); `notification_created_at` `timestamp` (NULL); `notification_title` `text` (NOT NULL); `notification_content` `text` (NOT NULL); `notification_partner_id` `int4` (NULL, ID-Kandidat); `notification_action` `varchar` (NOT NULL).

### `idk_partner_notification_logs`

`id` `int4` (PK, NOT NULL); `employee_id` `int4` (NOT NULL, ID-Kandidat); `title_de` `varchar` (NOT NULL); `content_de` `varchar` (NOT NULL); `title_en` `varchar` (NOT NULL); `content_en` `varchar` (NOT NULL); `created_at` `timestamptz` (NOT NULL).

### `idk_partner_notification_status`

`status_id` `int4` (PK, NOT NULL); `partner_id` `int4` (NOT NULL, ID-Kandidat); `notification_id` `int4` (NOT NULL, ID-Kandidat); `read_at` `timestamp` (NULL); `deleted_at` `timestamp` (NULL).

## Dodatak B – Policy-only objektni nazivi

Sljedeći nazivi su `BELEGT DURCH SCHEMAEXPORT` samo kao RLS policy sekcije, ne kao potpuni table/view dokaz:

`candidate_field_change_audit`, `candidate_field_fallbacks`, `candidate_status_transition_audit`, `candidate_status_transition_rules`, `idk_partner_personal_notification_types`, `idk_partner_personal_notifications_preferences`, `idk_partner_pushnot`, `idk_partner_tutorials`, `idk_partner_uplate`, `idk_partner_user_log`, `idk_ponovne_prijave`, `idk_poslovnice`, `idk_pp_appointment_groups`, `idk_pp_appointment_hours`, `idk_pp_appointments`, `idk_pp_appointments_questions`, `idk_pp_cand_appts`, `idk_pp_cand_required_documents`, `idk_pp_city`, `idk_pp_contract_sent`, `idk_pp_document_types`, `idk_pp_documents`, `idk_pp_documents_status_logs`, `idk_pp_documents_statuses`, `idk_pp_informacije_profil`, `idk_pp_nalog_profil`, `idk_pp_nalog_required_documents`, `idk_pp_partners`, `idk_pp_permissions`, `idk_pp_question_categories`, `idk_pp_question_options`, `idk_pp_questions`, `idk_pp_ratings`, `idk_pp_regions`, `idk_pp_reminder_documents`, `idk_pp_reminder_settings`, `idk_pp_reminder_types`, `idk_pp_reminders`, `idk_pp_user_access`, `idk_pp_users`, `idk_pp_visa_incomplete`, `idk_predracuni`, `idk_profil_kriterij`, `idk_project_candidate_queue`, `idk_project_kandidati`, `idk_projects`, `idk_projects_settings`, `idk_projects_tasks`, `idk_provider_for_sending_messages`, `idk_pushnotifications`, `idk_racuni`, `idk_razlozi_odbijanja`, `idk_reject_reasons`, `idk_reminders`, `idk_ro_usluge`, `idk_sales_reminders`, `idk_settings`, `idk_skladiste`, `idk_skladiste_kategorije`, `idk_skladiste_product`, `idk_skladiste_zaposlenici`, `idk_skole`, `idk_skole_smjerovi`, `idk_sms_messages`, `idk_struke`, `idk_task_force`, `idk_tasks`, `idk_tf_agent_nalog`, `idk_tf_reservations`, `idk_tf_stats_reservations`, `idk_tf_statusi`, `idk_tf_transfered_candidates_logs`, `idk_tf_vrste`, `idk_ticketi`, `idk_ticketi_komentari`, `idk_timeline`, `idk_timovi`, `idk_tipovi_provizija`, `idk_triggerurl`, `idk_tutorijali`, `idk_validnosti_inputa`, `idk_viber_obavijesti`, `job_occupation_map`, `occupation`, `occupation_alias`, `occupation_remap_audit`, `status_project_name_rules`, `users`.
