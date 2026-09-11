-- SECURITY-REVIEW ONLY. DO NOT EXECUTE WITHOUT THE SEPARATE USER APPROVAL.
-- Prerequisite: 00-identity-and-privilege-gate.sql completed without STOP.
-- Scope: PostgreSQL 15-18 catalog metadata only; no candidate table reads.

BEGIN TRANSACTION READ ONLY;
SET LOCAL statement_timeout = '5s';
SET LOCAL lock_timeout = '1s';
SET LOCAL idle_in_transaction_session_timeout = '15s';
SET LOCAL search_path = pg_catalog, information_schema;

-- SQL-META-001: non-system schemas
SELECT
  namespace.nspname AS schema_name,
  pg_catalog.pg_get_userbyid(namespace.nspowner) AS schema_owner
FROM pg_catalog.pg_namespace AS namespace
WHERE namespace.nspname NOT IN ('pg_catalog', 'information_schema')
  AND namespace.nspname NOT LIKE 'pg_toast%'
  AND namespace.nspname NOT LIKE 'pg_temp_%'
ORDER BY schema_name
LIMIT 10000;

-- SQL-META-002: relations and estimated size
SELECT
  namespace.nspname AS schema_name,
  relation.relname AS relation_name,
  relation.relkind,
  pg_catalog.pg_get_userbyid(relation.relowner) AS relation_owner,
  relation.relpersistence,
  relation.relrowsecurity,
  relation.relforcerowsecurity,
  relation.reltuples::bigint AS estimated_rows,
  pg_catalog.pg_total_relation_size(relation.oid) AS total_bytes
FROM pg_catalog.pg_class AS relation
JOIN pg_catalog.pg_namespace AS namespace
  ON namespace.oid = relation.relnamespace
WHERE relation.relkind IN ('r', 'p', 'v', 'm', 'f', 'S')
  AND namespace.nspname NOT IN ('pg_catalog', 'information_schema')
  AND namespace.nspname NOT LIKE 'pg_toast%'
  AND namespace.nspname NOT LIKE 'pg_temp_%'
ORDER BY schema_name, relation_name
LIMIT 10000;

-- SQL-META-003: columns without default-expression bodies
SELECT
  namespace.nspname AS schema_name,
  relation.relname AS relation_name,
  attribute.attnum AS ordinal_position,
  attribute.attname AS column_name,
  pg_catalog.format_type(
    attribute.atttypid,
    attribute.atttypmod
  ) AS data_type,
  attribute.attnotnull AS not_null,
  attribute.atthasdef AS has_default,
  attribute.attidentity AS identity_kind,
  attribute.attgenerated AS generated_kind
FROM pg_catalog.pg_attribute AS attribute
JOIN pg_catalog.pg_class AS relation
  ON relation.oid = attribute.attrelid
JOIN pg_catalog.pg_namespace AS namespace
  ON namespace.oid = relation.relnamespace
WHERE attribute.attnum > 0
  AND NOT attribute.attisdropped
  AND relation.relkind IN ('r', 'p', 'v', 'm', 'f')
  AND namespace.nspname NOT IN ('pg_catalog', 'information_schema')
  AND namespace.nspname NOT LIKE 'pg_toast%'
  AND namespace.nspname NOT LIKE 'pg_temp_%'
ORDER BY schema_name, relation_name, ordinal_position
LIMIT 20000;

-- SQL-META-004: constraints and key relationships without row values
SELECT
  namespace.nspname AS schema_name,
  relation.relname AS relation_name,
  constraint_entry.conname AS constraint_name,
  constraint_entry.contype,
  constraint_entry.convalidated,
  constraint_entry.conkey AS local_attribute_numbers,
  referenced_namespace.nspname AS referenced_schema,
  referenced_relation.relname AS referenced_relation,
  constraint_entry.confkey AS referenced_attribute_numbers,
  constraint_entry.confupdtype,
  constraint_entry.confdeltype
FROM pg_catalog.pg_constraint AS constraint_entry
JOIN pg_catalog.pg_class AS relation
  ON relation.oid = constraint_entry.conrelid
JOIN pg_catalog.pg_namespace AS namespace
  ON namespace.oid = relation.relnamespace
LEFT JOIN pg_catalog.pg_class AS referenced_relation
  ON referenced_relation.oid = constraint_entry.confrelid
LEFT JOIN pg_catalog.pg_namespace AS referenced_namespace
  ON referenced_namespace.oid = referenced_relation.relnamespace
WHERE namespace.nspname NOT IN ('pg_catalog', 'information_schema')
  AND namespace.nspname NOT LIKE 'pg_toast%'
  AND namespace.nspname NOT LIKE 'pg_temp_%'
ORDER BY schema_name, relation_name, constraint_name
LIMIT 20000;

-- SQL-META-005: row-level security policies
SELECT
  namespace.nspname AS schema_name,
  relation.relname AS relation_name,
  relation.relrowsecurity,
  relation.relforcerowsecurity,
  policy.polname AS policy_name,
  policy.polpermissive,
  policy.polcmd,
  ARRAY(
    SELECT CASE
      WHEN role_oid = 0 THEN 'PUBLIC'
      ELSE pg_catalog.pg_get_userbyid(role_oid)
    END
    FROM unnest(policy.polroles) AS role_oid
  ) AS policy_roles,
  pg_catalog.pg_get_expr(
    policy.polqual,
    policy.polrelid
  ) AS using_expression,
  pg_catalog.pg_get_expr(
    policy.polwithcheck,
    policy.polrelid
  ) AS check_expression
FROM pg_catalog.pg_class AS relation
JOIN pg_catalog.pg_namespace AS namespace
  ON namespace.oid = relation.relnamespace
LEFT JOIN pg_catalog.pg_policy AS policy
  ON policy.polrelid = relation.oid
WHERE relation.relkind IN ('r', 'p')
  AND namespace.nspname NOT IN ('pg_catalog', 'information_schema')
  AND namespace.nspname NOT LIKE 'pg_toast%'
  AND namespace.nspname NOT LIKE 'pg_temp_%'
ORDER BY schema_name, relation_name, policy_name
LIMIT 20000;

-- SQL-META-006: visible explicit table and view grants
SELECT
  table_schema,
  table_name,
  grantor,
  grantee,
  privilege_type,
  is_grantable
FROM information_schema.table_privileges
WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
ORDER BY table_schema, table_name, grantee, privilege_type
LIMIT 20000;

-- SQL-META-007: routine signatures and security properties, never source bodies
SELECT
  namespace.nspname AS routine_schema,
  routine.proname AS routine_name,
  routine.prokind,
  pg_catalog.pg_get_function_identity_arguments(routine.oid) AS arguments,
  pg_catalog.pg_get_function_result(routine.oid) AS result_type,
  pg_catalog.pg_get_userbyid(routine.proowner) AS routine_owner,
  routine.prosecdef AS security_definer,
  routine.provolatile AS volatility,
  routine.proparallel AS parallel_safety
FROM pg_catalog.pg_proc AS routine
JOIN pg_catalog.pg_namespace AS namespace
  ON namespace.oid = routine.pronamespace
WHERE namespace.nspname NOT IN ('pg_catalog', 'information_schema')
  AND namespace.nspname NOT LIKE 'pg_toast%'
  AND namespace.nspname NOT LIKE 'pg_temp_%'
ORDER BY routine_schema, routine_name, arguments
LIMIT 20000;

-- SQL-META-008: visible explicit routine grants
SELECT
  routine_schema,
  routine_name,
  specific_name,
  grantor,
  grantee,
  privilege_type,
  is_grantable
FROM information_schema.routine_privileges
WHERE routine_schema NOT IN ('pg_catalog', 'information_schema')
ORDER BY routine_schema, routine_name, grantee
LIMIT 20000;

-- SQL-META-009: indexes and definitions
SELECT
  table_namespace.nspname AS table_schema,
  table_relation.relname AS table_name,
  index_relation.relname AS index_name,
  index_entry.indisunique,
  index_entry.indisprimary,
  index_entry.indisvalid,
  index_entry.indisready,
  index_entry.indisreplident,
  pg_catalog.pg_relation_size(index_relation.oid) AS index_bytes,
  pg_catalog.pg_get_indexdef(index_relation.oid) AS index_definition
FROM pg_catalog.pg_index AS index_entry
JOIN pg_catalog.pg_class AS index_relation
  ON index_relation.oid = index_entry.indexrelid
JOIN pg_catalog.pg_class AS table_relation
  ON table_relation.oid = index_entry.indrelid
JOIN pg_catalog.pg_namespace AS table_namespace
  ON table_namespace.oid = table_relation.relnamespace
WHERE table_namespace.nspname NOT IN ('pg_catalog', 'information_schema')
  AND table_namespace.nspname NOT LIKE 'pg_toast%'
  AND table_namespace.nspname NOT LIKE 'pg_temp_%'
ORDER BY table_schema, table_name, index_name
LIMIT 20000;

-- SQL-META-010: non-internal trigger definitions
SELECT
  namespace.nspname AS schema_name,
  relation.relname AS relation_name,
  trigger_entry.tgname AS trigger_name,
  trigger_entry.tgenabled,
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
  AND namespace.nspname NOT IN ('pg_catalog', 'information_schema')
  AND namespace.nspname NOT LIKE 'pg_toast%'
  AND namespace.nspname NOT LIKE 'pg_temp_%'
ORDER BY schema_name, relation_name, trigger_name
LIMIT 20000;

-- SQL-META-011: aggregate relation activity statistics
SELECT
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
ORDER BY schemaname, relation_name
LIMIT 10000;

-- SQL-META-012: extensions without configuration details
SELECT
  extension.extname AS extension_name,
  extension.extversion AS extension_version,
  namespace.nspname AS schema_name
FROM pg_catalog.pg_extension AS extension
JOIN pg_catalog.pg_namespace AS namespace
  ON namespace.oid = extension.extnamespace
ORDER BY extension_name
LIMIT 1000;

-- SQL-META-013: view definitions; restricted output requiring redaction review
SELECT
  namespace.nspname AS schema_name,
  relation.relname AS view_name,
  relation.relkind,
  pg_catalog.pg_get_viewdef(
    relation.oid,
    true
  ) AS view_definition
FROM pg_catalog.pg_class AS relation
JOIN pg_catalog.pg_namespace AS namespace
  ON namespace.oid = relation.relnamespace
WHERE relation.relkind IN ('v', 'm')
  AND namespace.nspname NOT IN ('pg_catalog', 'information_schema')
  AND namespace.nspname NOT LIKE 'pg_toast%'
  AND namespace.nspname NOT LIKE 'pg_temp_%'
ORDER BY schema_name, view_name
LIMIT 10000;

-- SQL-META-014: safe planner statistics without value distributions
SELECT
  schemaname,
  tablename,
  attname AS column_name,
  inherited,
  null_frac,
  avg_width,
  n_distinct,
  correlation
FROM pg_catalog.pg_stats
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY schemaname, tablename, column_name
LIMIT 20000;

-- SQL-META-015: enum labels; restricted metadata, not candidate rows
SELECT
  namespace.nspname AS schema_name,
  type_entry.typname AS type_name,
  enum_entry.enumsortorder,
  enum_entry.enumlabel
FROM pg_catalog.pg_enum AS enum_entry
JOIN pg_catalog.pg_type AS type_entry
  ON type_entry.oid = enum_entry.enumtypid
JOIN pg_catalog.pg_namespace AS namespace
  ON namespace.oid = type_entry.typnamespace
WHERE namespace.nspname NOT IN ('pg_catalog', 'information_schema')
ORDER BY schema_name, type_name, enum_entry.enumsortorder
LIMIT 10000;

-- SQL-META-016: publication membership without replication contents
SELECT
  publication.pubname AS publication_name,
  publication.puballtables,
  publication.pubinsert,
  publication.pubupdate,
  publication.pubdelete,
  publication.pubtruncate
FROM pg_catalog.pg_publication AS publication
ORDER BY publication_name
LIMIT 1000;

SELECT
  publication_tables.pubname AS publication_name,
  publication_tables.schemaname AS schema_name,
  publication_tables.tablename AS relation_name
FROM pg_catalog.pg_publication_tables AS publication_tables
ORDER BY publication_name, schema_name, relation_name
LIMIT 10000;

ROLLBACK;
