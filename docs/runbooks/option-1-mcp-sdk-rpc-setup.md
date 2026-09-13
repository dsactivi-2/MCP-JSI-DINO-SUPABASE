<!-- markdownlint-disable MD013 -->
# Runbook: Option 1 lokal installieren (MCP SDK v2 + Zod + Postgres-RPC)

Datum: 2026-09-12

Status: Evaluations-Setup. Kein AUTO-02-Stack, kein Produktiv-Deploy, kein
Gate B, kein Zugriff auf das CRM mit echten Kandidaten.

Grundlage: [Top-3-Vergleich](../research/mcp-autowire-top3-vergleich.md),
[SDK-Plan](../planning/sdk-integration-plan.md),
[ADR-0001](../decisions/0001-controlled-query-boundary.md).

Offizielle Installationsquellen (gelesen 2026-09-12):
[MCP TS SDK README](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/README.md),
[First server](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/get-started/first-server.md),
[Serve with Express](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/serving/express.md),
[Require authorization](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/serving/authorization.md),
npm `@modelcontextprotocol/server@2.0.0`.

## 1. Was diese Anleitung ist und was nicht

Sie richtet **Option 1** ein: drei MCP-Tools, Zod prüft JSON, **eine**
parametrisierte PostgreSQL-Funktion führt die Suche aus. Das LLM sieht
keinen SQL-String und keine Tabellennamen.

Sie richtet **nicht** ein:

- Verbindung zum Produktionsprojekt / Pooler / Discovery-Rolle
- `crm_api.search_candidates` (Signatur mit E-Mail/Telefon)
- Supabase-Developer-Plugin
- OAuth-Issuer (AUTH-01 bleibt OFFEN)
- echte Taxonomie, Berufssuchprofile, Q8.5-Erfahrungsrechnung

Das Verzeichnis liegt **außerhalb** dieses Dokumentationsrepos. Hier gibt
es noch keinen genehmigten App-Scaffold.

## 2. Architektur, die ihr installiert

```text
MCP-Client (stdio lokal oder HTTP)
  → Express /mcp  (optional requireBearerAuth)
  → createMcpHandler: frische McpServer-Instanz pro Request
  → registerTool + Zod (search_candidates | get_candidate_profile | get_filter_options)
  → App-Validator (unbekannte Felder, cap ≤ 50)
  → pg: SELECT * FROM crm_search_eval.search_candidates_v1($1::jsonb)
  → Postgres 17, SECURITY INVOKER, ohne Kontaktspalten
```

Zwei Tokens bleiben getrennt: ein MCP-Bearer (nur lokal/dev) und
`DATABASE_URL` für Postgres. Den MCP-Token nicht als DB-Passwort
weiterreichen.

## 3. Voraussetzungen

| Werkzeug | Vorgabe | Quelle |
| --- | --- | --- |
| Node.js | `>= 20` | `engines` in `@modelcontextprotocol/server` 2.0.0 |
| npm | kommt mit Node; Tutorial nutzt npm | First-server-Tutorial |
| Docker | für lokale Postgres 17 | Projekt läuft auf PG 17; nicht das CRM-Image |
| jq | optional, für lesbare curl-Ausgabe | macOS/Homebrew |

Prüfen:

```bash
node -v    # v20 oder neuer
docker version
```

Kein `@modelcontextprotocol/sdk` (das ist v1). Kein Mix aus v1- und
v2-Importen.

## 4. Isoliertes Projekt anlegen

```bash
mkdir -p "$HOME/Code/eval-crm-mcp-option1"
cd "$HOME/Code/eval-crm-mcp-option1"
npm init -y
npm pkg set type=module
npm pkg set name="eval-crm-mcp-option1"
mkdir -p src sql
```

`type=module` ist Pflicht: das SDK liefert ESM.

## 5. Pakete installieren und pinnen

HTTP-Variante (ChatGPT/Claude über URL, curl):

```bash
npm install @modelcontextprotocol/server@2.0.0 \
  @modelcontextprotocol/express \
  @modelcontextprotocol/node \
  express \
  zod \
  pg \
  tsx

npm install -D typescript @types/node @types/express @types/pg
```

Zod kommt mit dem Server-Paket, das Tutorial installiert es trotzdem
explizit, Import ist `zod/v4`.

Lockfile committen, sobald das Eval-Repo existiert. Version 2.0.0 des
Server-Pakets war am 2026-09-12 auf npm die veröffentlichte v2-Linie.

## 6. TypeScript

Datei `tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "strict": true,
    "skipLibCheck": true,
    "types": ["node"],
    "outDir": "dist",
    "rootDir": "src"
  },
  "include": ["src"]
}
```

npm-Hinweis zu `@modelcontextprotocol/server@2.0.0`: bei TypeScript ≥ 6
`"types": ["node"]` setzen, weil `Buffer` in den `.d.mts` vorkommt.

Scripts in `package.json`:

```bash
npm pkg set scripts.start="tsx --env-file=.env src/server.ts"
npm pkg set scripts.start:stdio="tsx --env-file=.env src/stdio.ts"
```

## 7. Synthetische Postgres 17 — nicht das CRM

Nur Loopback, eigenes Passwort, keine CRM-Dumps, keine OrbStack-Backups.

```bash
docker rm -f crm-mcp-eval-pg 2>/dev/null || true
docker run --name crm-mcp-eval-pg \
  --restart=no \
  -e POSTGRES_USER=eval_app \
  -e POSTGRES_PASSWORD='eval-only-local' \
  -e POSTGRES_DB=crm_mcp_eval \
  -p 127.0.0.1:55432:5432 \
  -d postgres:17

until docker exec crm-mcp-eval-pg pg_isready -U eval_app -d crm_mcp_eval
do sleep 1; done
```

Datei `sql/001_eval_search.sql` — Spielschema, **keine** echten
Kandidatenspalten:

```sql
CREATE SCHEMA IF NOT EXISTS crm_search_eval;

CREATE TABLE crm_search_eval.eval_candidate (
  candidate_id   uuid PRIMARY KEY,
  display_name   text NOT NULL,
  occupation_id  text NOT NULL,
  experience_months int NOT NULL CHECK (experience_months >= 0),
  region_code    text NOT NULL,
  language_de_level text,
  birth_date     date
);

INSERT INTO crm_search_eval.eval_candidate VALUES
  ('11111111-1111-1111-1111-111111111111', 'Eval A', 'electrician', 72, 'BY', 'B1', DATE '1995-03-01'),
  ('22222222-2222-2222-2222-222222222222', 'Eval B', 'salesperson', 240, 'BY', 'C1', DATE '1988-07-15'),
  ('33333333-3333-3333-3333-333333333333', 'Eval C', 'electrician', 24, 'BW', 'A2', DATE '1999-11-20');

CREATE OR REPLACE FUNCTION crm_search_eval.search_candidates_v1(filter jsonb)
RETURNS TABLE (
  candidate_id uuid,
  display_name text,
  occupation_id text,
  experience_months int,
  region_code text,
  match_evidence jsonb
)
LANGUAGE sql
STABLE
SECURITY INVOKER
SET search_path = crm_search_eval, pg_temp
AS $$
  SELECT
    c.candidate_id,
    c.display_name,
    c.occupation_id,
    c.experience_months,
    c.region_code,
    jsonb_build_object(
      'occupation', c.occupation_id,
      'experience_months', c.experience_months
    ) AS match_evidence
  FROM crm_search_eval.eval_candidate AS c
  WHERE
    ((filter ? 'occupationId') = false
      OR c.occupation_id = filter->>'occupationId')
    AND ((filter ? 'minExperienceMonths') = false
      OR c.experience_months >= (filter->>'minExperienceMonths')::int)
    AND ((filter ? 'regionAny') = false
      OR c.region_code IN (
        SELECT jsonb_array_elements_text(filter->'regionAny')
      ))
    AND ((filter ? 'candidateId') = false
      OR c.candidate_id = (filter->>'candidateId')::uuid)
    ORDER BY c.candidate_id
  LIMIT LEAST(
    COALESCE((filter->>'limit')::int, 50),
    50
  );
$$;

REVOKE ALL ON SCHEMA crm_search_eval FROM PUBLIC;
GRANT USAGE ON SCHEMA crm_search_eval TO eval_app;
GRANT SELECT ON crm_search_eval.eval_candidate TO eval_app;
GRANT EXECUTE ON FUNCTION crm_search_eval.search_candidates_v1(jsonb) TO eval_app;
```

Anwenden:

```bash
docker exec -i crm-mcp-eval-pg \
  psql -U eval_app -d crm_mcp_eval < sql/001_eval_search.sql
```

Die Funktion bildet **nicht** Q8.5, Taxonomie oder Freitext-Elektriker ab.
Sie zeigt nur: JSON rein, begrenzte Zeilen raus, kein Kontaktfeld.

Probe:

```bash
docker exec -i crm-mcp-eval-pg psql -U eval_app -d crm_mcp_eval -c \
"SELECT * FROM crm_search_eval.search_candidates_v1('{\"occupationId\":\"electrician\",\"minExperienceMonths\":60}'::jsonb);"
```

Erwartung: nur Eval A (72 Monate). Eval B (Verkäufer, 240 Monate) fällt
weg — genau der Fehler, den eine naive „5 Jahre irgendwelche Erfahrung“
Suche machen würde.

## 8. Umgebung

Datei `.env` (nicht ins Git, nicht in den Chat):

```bash
DATABASE_URL=postgres://eval_app:eval-only-local@127.0.0.1:55432/crm_mcp_eval
MCP_BIND=127.0.0.1
MCP_PORT=8787
MCP_ALLOWED_HOSTS=127.0.0.1,localhost
# Nur lokales Eval. Kein Produktionsgeheimnis.
MCP_DEV_BEARER=change-me-eval-only
```

`chmod 600 .env`

`DATABASE_URL` darf kein Pooler, kein `service_role`, kein CRM-Projekt
sein.

## 9. Datenadapter

Datei `src/db.ts`:

```ts
import { Pool } from 'pg';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 4,
  idleTimeoutMillis: 10_000
});

export type SearchFilter = {
  occupationId?: string;
  minExperienceMonths?: number;
  regionAny?: string[];
  candidateId?: string;
  limit?: number;
};

export async function callSearchRpc(filter: SearchFilter) {
  const result = await pool.query(
    'select * from crm_search_eval.search_candidates_v1($1::jsonb)',
    [JSON.stringify(filter)]
  );
  return result.rows;
}
```

Kein `SELECT` auf Anwendungstabellen außer über diese eine Funktion.

## 10. Zod-Vertrag und Server

Datei `src/server.ts`:

```ts
import { createMcpExpressApp, requireBearerAuth } from '@modelcontextprotocol/express';
import { toNodeHandler } from '@modelcontextprotocol/node';
import { createMcpHandler, McpServer } from '@modelcontextprotocol/server';
import * as z from 'zod/v4';
import { callSearchRpc } from './db.js';

const searchInput = z
  .object({
    occupationId: z.string().min(1).optional(),
    minExperienceMonths: z.number().int().nonnegative().optional(),
    regionAny: z.array(z.string().min(1)).max(20).optional(),
    limit: z.number().int().min(1).max(50).optional()
  })
  .strict();

const profileInput = z.object({
  candidateId: z.string().uuid()
}).strict();

const optionsInput = z.object({
  field: z.enum(['occupationId', 'regionAny']),
  query: z.string().max(80).optional()
}).strict();

function buildServer(): McpServer {
  const server = new McpServer({
    name: 'crm-search-eval',
    version: '0.0.1'
  });

  server.registerTool(
    'search_candidates',
    {
      description:
        'Search eval candidates. Unspecified filters stay inactive. Max 50. No contacts.',
      inputSchema: searchInput
    },
    async (args) => {
      const rows = await callSearchRpc({
        occupationId: args.occupationId,
        minExperienceMonths: args.minExperienceMonths,
        regionAny: args.regionAny,
        limit: args.limit ?? 50
      });
      const page = rows.slice(0, 50);
      return {
        content: [{ type: 'text', text: JSON.stringify({ interpretedFilters: args, page }, null, 2) }]
      };
    }
  );

  server.registerTool(
    'get_candidate_profile',
    {
      description: 'Return one eval profile without contacts.',
      inputSchema: profileInput
    },
    async ({ candidateId }) => {
      const rows = await callSearchRpc({ candidateId, limit: 1 });
      const one = rows[0];
      if (!one) {
        return { content: [{ type: 'text', text: 'not found' }], isError: true };
      }
      return {
        content: [{ type: 'text', text: JSON.stringify(one, null, 2) }]
      };
    }
  );

  server.registerTool(
    'get_filter_options',
    {
      description: 'Eval catalog only, no candidate rows.',
      inputSchema: optionsInput
    },
    async ({ field, query }) => {
      const all =
        field === 'occupationId'
          ? ['electrician', 'salesperson']
          : ['BY', 'BW'];
      const q = query?.toLowerCase() ?? '';
      const options = all.filter((v) => v.includes(q)).slice(0, 20);
      return {
        content: [{ type: 'text', text: JSON.stringify({ field, options }) }]
      };
    }
  );

  return server;
}

const handler = createMcpHandler(() => buildServer());
const app = createMcpExpressApp({
  host: process.env.MCP_BIND ?? '127.0.0.1',
  allowedHosts: (process.env.MCP_ALLOWED_HOSTS ?? '127.0.0.1,localhost').split(',')
});

const verifier = {
  async verifyAccessToken(token: string) {
    if (token !== process.env.MCP_DEV_BEARER) {
      throw new Error('invalid_token');
    }
    return {
      token,
      clientId: 'eval-local',
      scopes: ['mcp'],
      expiresAt: Math.floor(Date.now() / 1000) + 3600
    };
  }
};

const auth = requireBearerAuth({
  verifier,
  requiredScopes: ['mcp']
});

const node = toNodeHandler(handler);
app.all('/mcp', auth, (req, res) => void node(req, res, req.body));

const port = Number(process.env.MCP_PORT ?? 8787);
app.listen(port, process.env.MCP_BIND ?? '127.0.0.1', () => {
  process.stdout.write(`eval MCP on http://127.0.0.1:${port}/mcp\n`);
});
```

`requireBearerAuth` sitzt vor `/mcp`. Der Verifier oben ist **nur Eval**:
ein Vergleich mit einer lokalen Zeichenkette. Produktions-MCP braucht
einen echten Issuer, Audience und JWKS laut SDK-Auth-Guide. Das SDK ist
kein Authorization Server.

Factory **pro Request** neu — so verlangt es `createMcpHandler`. Den
`pg.Pool` in `db.ts` auf Modulebene behalten, nicht in der Factory
neu öffnen.

## 11. Optional: stdio für lokale Hosts

Datei `src/stdio.ts`:

```ts
import { serveStdio } from '@modelcontextprotocol/server/stdio';
import { createMcpHandler } from '@modelcontextprotocol/server';

// Dieselbe buildServer-Funktion nach src/tools.ts ziehen und hier nutzen.
// stdio eignet sich für Claude Desktop / Codex lokal, nicht für ChatGPT-HTTP.
```

Für den ersten Nachweis reicht HTTP + curl.

## 12. Start und Nachweis

```bash
set -a && source .env && set +a
npm start
```

Anderes Terminal:

```bash
TOKEN='change-me-eval-only'

curl -sS -X POST "http://127.0.0.1:8787/mcp" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

Erwartung: SSE `message` mit genau den drei Toolnamen
`search_candidates`, `get_candidate_profile`, `get_filter_options`.
Ohne Bearer: `401 invalid_token`.

Suche „Elektriker, 5 Jahre“ im Eval-Modell:

```bash
curl -sS -X POST "http://127.0.0.1:8787/mcp" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc":"2.0",
    "id":2,
    "method":"tools/call",
    "params":{
      "name":"search_candidates",
      "arguments":{
        "occupationId":"electrician",
        "minExperienceMonths":60
      }
    }
  }'
```

Erwartung: Eval A, nicht Eval B. Unbekanntes Feld im JSON muss Zod
ablehnen, bevor Postgres läuft.

## 13. Client anbinden (lokal)

HTTP-Clients (wenn sie einen URL-MCP sprechen) auf
`http://127.0.0.1:8787/mcp` mit Bearer. `Host`/`Origin` müssen zu
`MCP_ALLOWED_HOSTS` passen; `createMcpExpressApp` prüft das gegen
DNS-Rebinding.

stdio-Host (Claude Desktop o. ä.) erst nach extrahierter `buildServer`-
Funktion, Command z. B. `npx tsx src/stdio.ts`, Arbeitsverzeichnis das
Eval-Projekt, Env aus `.env`. Keine CRM-Credentials in die Client-Config.

## 14. Aufräumen

```bash
docker stop crm-mcp-eval-pg
docker rm crm-mcp-eval-pg
```

Eval-Ordner und `.env` nicht in das CRM-Dokumentationsrepo kopieren.

## 15. Was danach noch fehlt (kein GO)

- AUTH-01: echter MCP-Issuer, Audience, kein Shared-Secret-Verifier
- Downstream-DB-Identität ungleich MCP-Token
- echte Search-RPC auf kanonischem Modell nach Discovery, ohne
  Kontaktprojektion
- Taxonomie, Berufssuchprofil, Q7, Q8.5
- CI: kein `from(`, kein `query(sql)`, cap 50, Kontaktfreiheit
- AUTO-02: Package-Manager, Hosting, Pinning im CRM-Repo

Erst wenn das steht, ist Option 1 mehr als ein lokaler Nachweis.

## Quellen

- [MCP server package.json engines](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/packages/server/package.json) (node >= 20, Version 2.0.0)
- [First server](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/get-started/first-server.md)
- [Serve with Express](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/serving/express.md)
- [Serve over HTTP](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/serving/http.md)
- [Require authorization](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/serving/authorization.md)
- [npm @modelcontextprotocol/server](https://www.npmjs.com/package/@modelcontextprotocol/server)
