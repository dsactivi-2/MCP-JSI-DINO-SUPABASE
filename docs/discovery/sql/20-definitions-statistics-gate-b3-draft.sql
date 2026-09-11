-- GATE B3 DRAFT ONLY. NOT APPROVED FOR EXECUTION.
-- Target alias: dino_crm_discovery_target_01
-- Prerequisites: Gate B1 PASS, Gate B2 reviewed, then a new explicit approval.
-- Definitions can contain literals and sensitive internal structure.
-- Statistics are derived from data or workload even when no rows are returned.
-- The schema ceiling below is not the required object allowlist.
-- Execution stays blocked until B2 identifies and approves exact objects,
-- coverage, stream markers, a launcher, and a separate approval package.

BEGIN TRANSACTION READ ONLY;
SET LOCAL statement_timeout = '5s';
SET LOCAL lock_timeout = '1s';
SET LOCAL idle_in_transaction_session_timeout = '15s';
SET LOCAL search_path = pg_catalog, information_schema;

-- SQL-GATE-B3-001
-- SENSITIVITY: RLS expressions can expose literals, role logic, column names,
-- tenant mechanisms, and internal helper-function names.
SELECT
  'SQL-GATE-B3-001' AS query_id,
  namespace.nspname AS schema_name,
  relation.relname AS relation_name,
  policy.polname AS policy_name,
  policy.polpermissive,
  policy.polcmd,
  pg_catalog.pg_get_expr(
    policy.polqual,
    policy.polrelid
  ) AS using_expression,
  pg_catalog.pg_get_expr(
    policy.polwithcheck,
    policy.polrelid
  ) AS check_expression
FROM pg_catalog.pg_policy AS policy
JOIN pg_catalog.pg_class AS relation
  ON relation.oid = policy.polrelid
JOIN pg_catalog.pg_namespace AS namespace
  ON namespace.oid = relation.relnamespace
WHERE namespace.nspname IN ('crm', 'crm_api', 'crm_auth')
ORDER BY schema_name, relation_name, policy_name
LIMIT 5001;

-- SQL-GATE-B3-002
-- SENSITIVITY: view definitions can expose literals, joins, private object
-- names, security predicates, and internal business logic.
SELECT
  'SQL-GATE-B3-002' AS query_id,
  namespace.nspname AS schema_name,
  relation.relname AS view_name,
  relation.relkind,
  'security_invoker=true' = ANY(
    COALESCE(relation.reloptions, ARRAY[]::text[])
  ) AS security_invoker,
  'security_barrier=true' = ANY(
    COALESCE(relation.reloptions, ARRAY[]::text[])
  ) AS security_barrier,
  pg_catalog.pg_get_viewdef(
    relation.oid,
    true
  ) AS view_definition
FROM pg_catalog.pg_class AS relation
JOIN pg_catalog.pg_namespace AS namespace
  ON namespace.oid = relation.relnamespace
WHERE relation.relkind IN ('v', 'm')
  AND namespace.nspname IN ('crm', 'crm_api', 'crm_auth')
ORDER BY schema_name, view_name
LIMIT 5001;

-- SQL-GATE-B3-003
-- SENSITIVITY: trigger definitions can expose literal arguments, internal
-- routine names, event behavior, and security-relevant business logic.
SELECT
  'SQL-GATE-B3-003' AS query_id,
  namespace.nspname AS schema_name,
  relation.relname AS relation_name,
  trigger_entry.tgname AS trigger_name,
  pg_catalog.pg_get_triggerdef(
    trigger_entry.oid,
    true
  ) AS trigger_definition
FROM pg_catalog.pg_trigger AS trigger_entry
JOIN pg_catalog.pg_class AS relation
  ON relation.oid = trigger_entry.tgrelid
JOIN pg_catalog.pg_namespace AS namespace
  ON namespace.oid = relation.relnamespace
WHERE NOT trigger_entry.tgisinternal
  AND namespace.nspname IN ('crm', 'crm_api', 'crm_auth')
ORDER BY schema_name, relation_name, trigger_name
LIMIT 5001;

-- SQL-GATE-B3-004
-- SENSITIVITY: index definitions can expose expression literals, partial-index
-- predicates, private column names, and search implementation details.
SELECT
  'SQL-GATE-B3-004' AS query_id,
  table_namespace.nspname AS table_schema,
  table_relation.relname AS table_name,
  index_relation.relname AS index_name,
  pg_catalog.pg_get_indexdef(index_relation.oid) AS index_definition
FROM pg_catalog.pg_index AS index_entry
JOIN pg_catalog.pg_class AS index_relation
  ON index_relation.oid = index_entry.indexrelid
JOIN pg_catalog.pg_class AS table_relation
  ON table_relation.oid = index_entry.indrelid
JOIN pg_catalog.pg_namespace AS table_namespace
  ON table_namespace.oid = table_relation.relnamespace
WHERE table_namespace.nspname IN ('crm', 'crm_api', 'crm_auth')
ORDER BY table_schema, table_name, index_name
LIMIT 5001;

-- SQL-GATE-B3-005
-- SENSITIVITY: enum labels can expose controlled internal vocabulary, status
-- values, workflow states, and taxonomy details.
SELECT
  'SQL-GATE-B3-005' AS query_id,
  namespace.nspname AS schema_name,
  type_entry.typname AS type_name,
  enum_entry.enumsortorder,
  enum_entry.enumlabel
FROM pg_catalog.pg_enum AS enum_entry
JOIN pg_catalog.pg_type AS type_entry
  ON type_entry.oid = enum_entry.enumtypid
JOIN pg_catalog.pg_namespace AS namespace
  ON namespace.oid = type_entry.typnamespace
WHERE namespace.nspname IN ('crm', 'crm_api', 'crm_auth')
ORDER BY schema_name, type_name, enum_entry.enumsortorder
LIMIT 5001;

-- SQL-GATE-B3-006
-- SENSITIVITY: these values are data-derived and can reveal sparsity,
-- selectivity, width, and distribution characteristics even without raw rows.
-- Value arrays such as most_common_vals and histogram_bounds remain excluded.
SELECT
  'SQL-GATE-B3-006' AS query_id,
  'READABLE_TABLES_ONLY' AS coverage,
  schemaname,
  tablename,
  attname AS column_name,
  inherited,
  null_frac,
  avg_width,
  n_distinct,
  correlation
FROM pg_catalog.pg_stats
WHERE schemaname IN ('crm', 'crm_api', 'crm_auth')
ORDER BY schemaname, tablename, column_name
LIMIT 5001;

-- SQL-GATE-B3-007
-- SENSITIVITY: workload-derived counters and timestamps reveal access patterns,
-- table activity, maintenance behavior, and approximate live/dead row counts.
SELECT
  'SQL-GATE-B3-007' AS query_id,
  schemaname,
  relname AS relation_name,
  seq_scan,
  seq_tup_read,
  idx_scan,
  idx_tup_fetch,
  n_live_tup,
  n_dead_tup,
  last_analyze,
  last_autoanalyze
FROM pg_catalog.pg_stat_user_tables
WHERE schemaname IN ('crm', 'crm_api', 'crm_auth')
ORDER BY schemaname, relation_name
LIMIT 5001;

-- SQL-GATE-B3-008
-- SENSITIVITY: exact storage sizes can reveal internal scale, growth, and
-- concentration even though no candidate values are returned.
SELECT
  'SQL-GATE-B3-008' AS query_id,
  namespace.nspname AS schema_name,
  relation.relname AS relation_name,
  relation.relkind,
  relation.reltuples::bigint AS estimated_rows,
  pg_catalog.pg_relation_size(relation.oid) AS relation_bytes,
  pg_catalog.pg_total_relation_size(relation.oid) AS total_bytes
FROM pg_catalog.pg_class AS relation
JOIN pg_catalog.pg_namespace AS namespace
  ON namespace.oid = relation.relnamespace
WHERE relation.relkind IN ('r', 'p', 'm', 'f')
  AND namespace.nspname IN ('crm', 'crm_api', 'crm_auth')
ORDER BY schema_name, relation_name
LIMIT 5001;

-- SQL-GATE-B3-009
-- SENSITIVITY: policy role names expose authorization structure even without
-- policy expressions or row data.
SELECT
  'SQL-GATE-B3-009' AS query_id,
  namespace.nspname AS schema_name,
  relation.relname AS relation_name,
  policy.polname AS policy_name,
  CASE WHEN expanded_policy_role.role_oid = 0 THEN 'PUBLIC'
    ELSE role_entry.rolname END AS policy_role
FROM pg_catalog.pg_policy AS policy
JOIN pg_catalog.pg_class AS relation
  ON relation.oid = policy.polrelid
JOIN pg_catalog.pg_namespace AS namespace
  ON namespace.oid = relation.relnamespace
CROSS JOIN LATERAL pg_catalog.unnest(policy.polroles)
  AS expanded_policy_role(role_oid)
LEFT JOIN pg_catalog.pg_roles AS role_entry
  ON role_entry.oid = expanded_policy_role.role_oid
WHERE namespace.nspname IN ('crm', 'crm_api', 'crm_auth')
ORDER BY schema_name, relation_name, policy_name, policy_role
LIMIT 5001;

-- SQL-GATE-B3-011: routine definitions and execution settings
-- SENSITIVITY: bodies and proconfig may contain literals or secrets.
-- Restricted output and an exact object allowlist are required before use.
SELECT
  'SQL-GATE-B3-011' AS query_id,
  namespace.nspname AS routine_schema,
  routine.proname AS routine_name,
  pg_catalog.pg_get_function_identity_arguments(routine.oid) AS arguments,
  routine.prosecdef AS security_definer,
  routine.proconfig AS execution_settings,
  pg_catalog.pg_get_functiondef(routine.oid) AS routine_definition
FROM pg_catalog.pg_proc AS routine
JOIN pg_catalog.pg_namespace AS namespace
  ON namespace.oid = routine.pronamespace
WHERE routine.prokind IN ('f', 'p')
  AND namespace.nspname IN ('crm', 'crm_api', 'crm_auth')
ORDER BY routine_schema, routine_name, arguments
LIMIT 5001;

-- SQL-GATE-B3-010: confirm stable identity and guardrails before rollback
SELECT
  'SQL-GATE-B3-010' AS query_id,
  CASE
    WHEN pg_catalog.current_database() = :'expected_database_name'
      THEN 1
    ELSE (
      'database_mismatch:' || pg_catalog.current_database()
    )::integer
  END AS database_guard,
  CASE
    WHEN session_user = current_user
      THEN 1
    ELSE (
      'identity_mismatch:' || session_user || ':' || current_user
    )::integer
  END AS identity_guard,
  pg_catalog.current_setting('transaction_read_only') AS transaction_read_only,
  pg_catalog.current_setting('statement_timeout') AS statement_timeout,
  pg_catalog.current_setting('lock_timeout') AS lock_timeout,
  pg_catalog.current_setting(
    'idle_in_transaction_session_timeout'
  ) AS idle_in_transaction_session_timeout;

ROLLBACK;
