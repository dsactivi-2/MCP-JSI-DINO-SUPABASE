from pathlib import Path
import re

CRM_ROOT = Path('/Users/activi/Downloads/crm-master-3')
DUMP = Path('/Users/activi/Downloads/crm-master-3/databaseDump/dump_20260226_081150.sql')
FALLBACK_DUMP = Path('/Users/activi/Downloads/dump_20260226_081150.sql')
REPORT = Path('/private/tmp/dino-crm-step2-search-wiring.md')
STATUS = Path('/private/tmp/dino-crm-step2-search-wiring.status')

SEARCH_FILES = [
    CRM_ROOT / 'src/crm/kandidati.php',
    CRM_ROOT / 'src/crm/ssdata_search.php',
    CRM_ROOT / 'src/crm/search.php',
    CRM_ROOT / 'src/crm/bot_search.php',
]
FILTER_DIR = CRM_ROOT / 'src/crm/components/Kandidati'


def req_keys(text):
    keys = set()
    for name in ('GET', 'POST', 'REQUEST'):
        needle = chr(36) + '_' + name + '['
        i = 0
        while True:
            j = text.find(needle, i)
            if j < 0:
                break
            k = j + len(needle)
            if k < len(text) and text[k] in (chr(39), chr(34)):
                q = text[k]
                n = text.find(q, k + 1)
                if n > k + 1:
                    keys.add(text[k + 1:n])
            i = j + 1
    return sorted(keys)


TABLE_RE = re.compile(r"\b(idk_[a-z0-9_]+)\b", re.I)
CREATE_RE = re.compile(r'^CREATE TABLE(?: IF NOT EXISTS)? `([A-Za-z0-9_]+)`', re.I)
COL_RE = re.compile(r'^\s+`([A-Za-z0-9_]+)`\s+([A-Za-z0-9]+)')


def fail(msg):
    STATUS.write_text('FAIL\n' + msg + '\n', encoding='utf-8')
    raise SystemExit(msg)


def dump_path():
    if DUMP.is_file() and not DUMP.is_symlink():
        return DUMP
    if FALLBACK_DUMP.is_file() and not FALLBACK_DUMP.is_symlink():
        return FALLBACK_DUMP
    fail('CRM dump dump_20260226_081150.sql not found')


def extract_php(path):
    text = path.read_text(encoding='utf-8', errors='replace')
    keys = req_keys(text)
    tables = sorted(set(TABLE_RE.findall(text)))
    return keys, tables, path.stat().st_size


def extract_columns(dump, wanted):
    wanted = {w.lower() for w in wanted}
    current = None
    cols = {}
    with dump.open('r', encoding='utf-8', errors='replace') as f:
        for line in f:
            if current is None:
                m = CREATE_RE.match(line.strip())
                if m and m.group(1).lower() in wanted:
                    current = m.group(1)
                    cols[current] = []
                continue
            if line.strip().upper().startswith('INSERT'):
                current = None
                continue
            if line.startswith(')') or line.lstrip().startswith(') ENGINE'):
                current = None
                if len(cols) == len(wanted):
                    break
                continue
            cm = COL_RE.match(line)
            if cm:
                cols[current].append(cm.group(1))
    return cols


def main():
    STATUS.write_text('FAIL\n', encoding='utf-8')
    if not CRM_ROOT.is_dir():
        fail('CRM_ROOT missing')
    dump = dump_path()
    php_blocks = []
    all_tables = set()
    for path in SEARCH_FILES:
        if not path.is_file():
            fail('missing ' + str(path))
        keys, tables, size = extract_php(path)
        all_tables.update(tables)
        php_blocks.append((path, size, keys, tables))
    filters = []
    if FILTER_DIR.is_dir():
        filters = sorted(p.name for p in FILTER_DIR.iterdir() if p.is_file())
    cols = extract_columns(dump, all_tables)
    lines = [
        '# CRM-Suchverdrahtung Schritt 2',
        '',
        'Stand: 2026-09-12',
        'Status: ENTWURF — nur Namen aus Code und CREATE TABLE. Keine Dump-Zeilen.',
        '',
        'CRM-Pfad: ' + str(CRM_ROOT),
        'Dump: ' + str(dump),
        'Dump-Bytes: ' + str(dump.stat().st_size),
        'Datenbank in diesem Lauf: keine Verbindung, kein INSERT gelesen.',
        '',
        '## 1. Suchdateien',
        '',
        '| Datei | Bytes | Request-Felder | Tabellen im Code |',
        '| --- | --- | --- | --- |',
    ]
    for path, size, keys, tables in php_blocks:
        key_s = ', '.join(keys) if keys else 'keine'
        tab_s = ', '.join(tables) if tables else 'keine'
        lines.append('| `' + path.name + '` | ' + str(size) + ' | ' + key_s + ' | ' + tab_s + ' |')
    lines += [
        '',
        '## 2. Filter-Komponenten',
        '',
    ]
    if filters:
        for name in filters:
            lines.append('- `' + name + '`')
    else:
        lines.append('- keine')
    lines += [
        '',
        '## 3. Tabellen aus dem Code, Spalten nur aus CREATE TABLE',
        '',
        '| Tabelle | Spalten (Namen) | Note |',
        '| --- | --- | --- |',
    ]
    for table in sorted(all_tables, key=str.lower):
        match = next((n for n in cols if n.lower() == table.lower()), None)
        if match:
            col_s = ', '.join(cols[match])
            note = 'BELEGT DURCH RPC-KOPF' if False else 'BELEGT DURCH SCHEMAEXPORT'
            note = 'BELEGT DURCH DUMP-DDL'
        else:
            col_s = '—'
            note = 'OFFEN / nicht im Dump-DDL'
        lines.append('| `' + table + '` | ' + col_s + ' | ' + note + ' |')
    lines += [
        '',
        '## 4. R1-Hinweis',
        '',
        'Interne Vermittler-Rollen sehen Kontakte. Kunde erst nach Einstellungsfreigabe.',
        'Dieses Script gibt keine Werte aus Dump-INSERT aus.',
        '',
        'result=PASS',
        '',
    ]
    REPORT.write_text('\n'.join(lines), encoding='utf-8')
    STATUS.write_text('PASS\n', encoding='utf-8')
    print(REPORT.read_text(encoding='utf-8'))


if __name__ == '__main__':
    main()
