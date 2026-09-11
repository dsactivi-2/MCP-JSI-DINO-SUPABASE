-- GATE B2 DRAFT. NO DATABASE APPROVAL EXISTS.
-- Target alias: dino_crm_discovery_target_01
-- Prerequisite: Gate B1 reviewed and separately approved as PASS.
-- Names, types, relationships, flags, size classes, and row estimates only.
-- Source scope: crm, crm_api, and crm_auth only.

BEGIN TRANSACTION READ ONLY;
SET LOCAL statement_timeout = '5s';
SET LOCAL lock_timeout = '1s';
SET LOCAL idle_in_transaction_session_timeout = '15s';
SET LOCAL search_path = pg_catalog, information_schema;

-- SQL-GATE-B2-001: approved discovery schemas
SELECT
  'SQL-GATE-B2-001' AS query_id,
  namespace.nspname AS schema_name,
  pg_catalog.pg_get_userbyid(namespace.nspowner) AS schema_owner
FROM pg_catalog.pg_namespace AS namespace
WHERE namespace.nspname IN ('crm', 'crm_api', 'crm_auth')
ORDER BY schema_name
LIMIT 5001;

-- SQL-GATE-B2-002: relations, structural flags, size classes, and row estimates
SELECT
  'SQL-GATE-B2-002' AS query_id,
  namespace.nspname AS schema_name,
  relation.relname AS relation_name,
  relation.relkind,
  pg_catalog.pg_get_userbyid(relation.relowner) AS relation_owner,
  relation.relpersistence,
  relation.relrowsecurity,
  relation.relforcerowsecurity,
  relation.relispopulated,
  relation.reltuples::bigint AS estimated_rows,
  CASE
    WHEN pg_catalog.pg_total_relation_size(relation.oid) < 1048576
      THEN 'LT_1_MIB'
    WHEN pg_catalog.pg_total_relation_size(relation.oid) < 10485760
      THEN 'FROM_1_TO_LT_10_MIB'
    WHEN pg_catalog.pg_total_relation_size(relation.oid) < 104857600
      THEN 'FROM_10_TO_LT_100_MIB'
    WHEN pg_catalog.pg_total_relation_size(relation.oid) < 1073741824
      THEN 'FROM_100_MIB_TO_LT_1_GIB'
    ELSE 'GE_1_GIB'
  END AS total_size_class
FROM pg_catalog.pg_class AS relation
JOIN pg_catalog.pg_namespace AS namespace
  ON namespace.oid = relation.relnamespace
WHERE relation.relkind IN ('r', 'p', 'v', 'm', 'f', 'S')
  AND namespace.nspname IN ('crm', 'crm_api', 'crm_auth')
ORDER BY schema_name, relation_name
LIMIT 5001;

-- SQL-GATE-B2-003: columns and structural type flags
SELECT
  'SQL-GATE-B2-003' AS query_id,
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
  AND namespace.nspname IN ('crm', 'crm_api', 'crm_auth')
ORDER BY schema_name, relation_name, ordinal_position
LIMIT 5001;

-- SQL-GATE-B2-004: constraints and relationship identifiers without definitions
SELECT
  'SQL-GATE-B2-004' AS query_id,
  namespace.nspname AS schema_name,
  relation.relname AS relation_name,
  constraint_entry.conname AS constraint_name,
  constraint_entry.contype,
  constraint_entry.convalidated,
  constraint_entry.condeferrable,
  constraint_entry.condeferred,
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
WHERE namespace.nspname IN ('crm', 'crm_api', 'crm_auth')
ORDER BY schema_name, relation_name, constraint_name
LIMIT 5001;

-- SQL-GATE-B2-005: RLS table flags without policy expressions
SELECT
  'SQL-GATE-B2-005' AS query_id,
  namespace.nspname AS schema_name,
  relation.relname AS relation_name,
  relation.relrowsecurity,
  relation.relforcerowsecurity,
  pg_catalog.count(policy.oid) AS policy_count
FROM pg_catalog.pg_class AS relation
JOIN pg_catalog.pg_namespace AS namespace
  ON namespace.oid = relation.relnamespace
LEFT JOIN pg_catalog.pg_policy AS policy
  ON policy.polrelid = relation.oid
WHERE relation.relkind IN ('r', 'p')
  AND namespace.nspname IN ('crm', 'crm_api', 'crm_auth')
GROUP BY
  namespace.nspname,
  relation.relname,
  relation.relrowsecurity,
  relation.relforcerowsecurity
ORDER BY schema_name, relation_name
LIMIT 5001;

-- Empty results do not prove absence of grants to other roles.
-- SQL-GATE-B2-006: explicit table and view grant names and flags
SELECT
  'SQL-GATE-B2-006' AS query_id,
  'ROLE_VISIBLE_ONLY' AS coverage,
  table_schema,
  table_name,
  grantor,
  grantee,
  privilege_type,
  is_grantable
FROM information_schema.table_privileges
WHERE table_schema IN ('crm', 'crm_api', 'crm_auth')
ORDER BY table_schema, table_name, grantee, privilege_type
LIMIT 5001;

-- SQL-GATE-B2-007: routine signatures and security flags without source bodies
SELECT
  'SQL-GATE-B2-007' AS query_id,
  namespace.nspname AS routine_schema,
  routine.proname AS routine_name,
  routine.prokind,
  pg_catalog.pg_get_function_identity_arguments(routine.oid) AS arguments,
  pg_catalog.pg_get_function_result(routine.oid) AS result_type,
  pg_catalog.pg_get_userbyid(routine.proowner) AS routine_owner,
  routine.prosecdef AS security_definer,
  routine.proleakproof AS leakproof,
  routine.provolatile AS volatility,
  routine.proparallel AS parallel_safety
FROM pg_catalog.pg_proc AS routine
JOIN pg_catalog.pg_namespace AS namespace
  ON namespace.oid = routine.pronamespace
WHERE namespace.nspname IN ('crm', 'crm_api', 'crm_auth')
ORDER BY routine_schema, routine_name, arguments
LIMIT 5001;

-- A separate reviewed catalog/owner attestation must establish completeness.
-- SQL-GATE-B2-008: explicit routine grant names and flags
SELECT
  'SQL-GATE-B2-008' AS query_id,
  'ROLE_VISIBLE_ONLY' AS coverage,
  routine_schema,
  routine_name,
  specific_name,
  grantor,
  grantee,
  privilege_type,
  is_grantable
FROM information_schema.routine_privileges
WHERE routine_schema IN ('crm', 'crm_api', 'crm_auth')
ORDER BY routine_schema, routine_name, grantee
LIMIT 5001;

-- SQL-GATE-B2-009: index names, state flags, and size classes
SELECT
  'SQL-GATE-B2-009' AS query_id,
  table_namespace.nspname AS table_schema,
  table_relation.relname AS table_name,
  index_relation.relname AS index_name,
  index_entry.indisunique,
  index_entry.indisprimary,
  index_entry.indisvalid,
  index_entry.indisready,
  index_entry.indisreplident,
  CASE
    WHEN pg_catalog.pg_relation_size(index_relation.oid) < 1048576
      THEN 'LT_1_MIB'
    WHEN pg_catalog.pg_relation_size(index_relation.oid) < 10485760
      THEN 'FROM_1_TO_LT_10_MIB'
    WHEN pg_catalog.pg_relation_size(index_relation.oid) < 104857600
      THEN 'FROM_10_TO_LT_100_MIB'
    WHEN pg_catalog.pg_relation_size(index_relation.oid) < 1073741824
      THEN 'FROM_100_MIB_TO_LT_1_GIB'
    ELSE 'GE_1_GIB'
  END AS index_size_class
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

-- SQL-GATE-B2-010: trigger names and flags without trigger definitions
SELECT
  'SQL-GATE-B2-010' AS query_id,
  namespace.nspname AS schema_name,
  relation.relname AS relation_name,
  trigger_entry.tgname AS trigger_name,
  trigger_entry.tgenabled,
  routine_namespace.nspname AS routine_schema,
  routine.proname AS routine_name
FROM pg_catalog.pg_trigger AS trigger_entry
JOIN pg_catalog.pg_class AS relation
  ON relation.oid = trigger_entry.tgrelid
JOIN pg_catalog.pg_namespace AS namespace
  ON namespace.oid = relation.relnamespace
JOIN pg_catalog.pg_proc AS routine
  ON routine.oid = trigger_entry.tgfoid
JOIN pg_catalog.pg_namespace AS routine_namespace
  ON routine_namespace.oid = routine.pronamespace
WHERE NOT trigger_entry.tgisinternal
  AND namespace.nspname IN ('crm', 'crm_api', 'crm_auth')
ORDER BY schema_name, relation_name, trigger_name
LIMIT 5001;

-- SQL-GATE-B2-011: extension names and versions without configuration
SELECT
  'SQL-GATE-B2-011' AS query_id,
  extension.extname AS extension_name,
  extension.extversion AS extension_version,
  namespace.nspname AS schema_name
FROM pg_catalog.pg_extension AS extension
JOIN pg_catalog.pg_namespace AS namespace
  ON namespace.oid = extension.extnamespace
WHERE namespace.nspname IN ('crm', 'crm_api', 'crm_auth')
ORDER BY extension_name
LIMIT 5001;

-- SQL-GATE-B2-012: publication names and structural flags
SELECT
  'SQL-GATE-B2-012' AS query_id,
  publication.pubname AS publication_name,
  publication.puballtables,
  publication.pubinsert,
  publication.pubupdate,
  publication.pubdelete,
  publication.pubtruncate
FROM pg_catalog.pg_publication AS publication
WHERE EXISTS (
  SELECT 1
  FROM pg_catalog.pg_publication_tables AS publication_tables
  WHERE publication_tables.pubname = publication.pubname
    AND publication_tables.schemaname IN ('crm', 'crm_api', 'crm_auth')
)
ORDER BY publication_name
LIMIT 5001;

-- SQL-GATE-B2-013: publication membership names
SELECT
  'SQL-GATE-B2-013' AS query_id,
  publication_tables.pubname AS publication_name,
  publication_tables.schemaname AS schema_name,
  publication_tables.tablename AS relation_name
FROM pg_catalog.pg_publication_tables AS publication_tables
WHERE publication_tables.schemaname IN ('crm', 'crm_api', 'crm_auth')
ORDER BY publication_name, schema_name, relation_name
LIMIT 5001;

-- SQL-GATE-B2-014: confirm stable identity and guardrails before rollback
SELECT
  'SQL-GATE-B2-014' AS query_id,
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
