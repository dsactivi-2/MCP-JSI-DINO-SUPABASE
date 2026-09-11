-- GATE B1 V2 DRAFT. NO DATABASE APPROVAL EXISTS.
-- Target alias: dino_crm_discovery_target_01
-- PostgreSQL 15-18. Run only through the Gate B execution mechanism.
-- Every returned finding row is fail-closed and requires STOP.
-- psql boundary_token is launcher-generated and contains no target data.

BEGIN TRANSACTION READ ONLY;
SET LOCAL statement_timeout = '5s';
SET LOCAL lock_timeout = '1s';
SET LOCAL idle_in_transaction_session_timeout = '15s';
SET LOCAL search_path = pg_catalog, information_schema;

-- SQL-GATE-B1-001: observe target and both active identities
\echo __GATE_B1_BOUNDARY__|:boundary_token|BEGIN|SQL-GATE-B1-001
SELECT
  'SQL-GATE-B1-001' AS query_id,
  pg_catalog.current_database() AS observed_database_name,
  session_user AS session_identity,
  current_user AS current_identity,
  pg_catalog.current_setting('server_version_num') AS server_version_num,
  pg_catalog.current_setting('transaction_read_only') AS transaction_read_only,
  pg_catalog.pg_is_in_recovery() AS is_replica;
\echo __GATE_B1_BOUNDARY__|:boundary_token|END|SQL-GATE-B1-001

-- SQL-GATE-B1-002: fail immediately on target or identity mismatch
\echo __GATE_B1_BOUNDARY__|:boundary_token|BEGIN|SQL-GATE-B1-002
SELECT
  'SQL-GATE-B1-002' AS query_id,
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
  END AS identity_guard;
\echo __GATE_B1_BOUNDARY__|:boundary_token|END|SQL-GATE-B1-002

-- SQL-GATE-B1-003: inspect attributes of both identities
\echo __GATE_B1_BOUNDARY__|:boundary_token|BEGIN|SQL-GATE-B1-003
WITH identities AS (
  SELECT 'session_user'::text AS identity_kind, session_user::name AS role_name
  UNION
  SELECT 'current_user'::text AS identity_kind, current_user::name AS role_name
)
SELECT
  'SQL-GATE-B1-003' AS query_id,
  identities.identity_kind,
  role_entry.rolname,
  role_entry.rolsuper,
  role_entry.rolinherit,
  role_entry.rolcreaterole,
  role_entry.rolcreatedb,
  role_entry.rolcanlogin,
  role_entry.rolreplication,
  role_entry.rolbypassrls,
  role_entry.rolconnlimit
FROM identities
JOIN pg_catalog.pg_roles AS role_entry
  ON role_entry.rolname = identities.role_name
WHERE role_entry.rolsuper
  OR role_entry.rolcreaterole
  OR role_entry.rolcreatedb
  OR role_entry.rolreplication
  OR role_entry.rolbypassrls
ORDER BY identities.identity_kind, role_entry.rolname
LIMIT 5001;
\echo __GATE_B1_BOUNDARY__|:boundary_token|END|SQL-GATE-B1-003

-- SQL-GATE-B1-004: complete direct and inherited parent-role graph
\echo __GATE_B1_BOUNDARY__|:boundary_token|BEGIN|SQL-GATE-B1-004
WITH RECURSIVE identity_roots AS (
  SELECT 'session_user'::text AS identity_kind, role_entry.oid AS root_oid
  FROM pg_catalog.pg_roles AS role_entry
  WHERE role_entry.rolname = session_user

  UNION

  SELECT 'current_user'::text AS identity_kind, role_entry.oid AS root_oid
  FROM pg_catalog.pg_roles AS role_entry
  WHERE role_entry.rolname = current_user
),
membership_graph AS (
  SELECT
    identity_roots.identity_kind,
    identity_roots.root_oid,
    membership.roleid,
    membership.member,
    membership.admin_option,
    1 AS inheritance_depth,
    ARRAY[membership.member, membership.roleid] AS visited
  FROM identity_roots
  JOIN pg_catalog.pg_auth_members AS membership
    ON membership.member = identity_roots.root_oid

  UNION ALL

  SELECT
    membership_graph.identity_kind,
    membership_graph.root_oid,
    membership.roleid,
    membership.member,
    membership.admin_option,
    membership_graph.inheritance_depth + 1,
    membership_graph.visited || membership.roleid
  FROM membership_graph
  JOIN pg_catalog.pg_auth_members AS membership
    ON membership.member = membership_graph.roleid
  WHERE NOT membership.roleid = ANY(membership_graph.visited)
)
SELECT
  'SQL-GATE-B1-004' AS query_id,
  membership_graph.identity_kind,
  root_role.rolname AS root_identity,
  CASE
    WHEN membership_graph.inheritance_depth = 1 THEN 'DIRECT'
    ELSE 'INHERITED'
  END AS membership_kind,
  membership_graph.inheritance_depth,
  parent_role.rolname AS reachable_role,
  membership_graph.admin_option,
  parent_role.rolsuper,
  parent_role.rolcreaterole,
  parent_role.rolcreatedb,
  parent_role.rolreplication,
  parent_role.rolbypassrls
FROM membership_graph
JOIN pg_catalog.pg_roles AS root_role
  ON root_role.oid = membership_graph.root_oid
JOIN pg_catalog.pg_roles AS parent_role
  ON parent_role.oid = membership_graph.roleid
ORDER BY
  membership_graph.identity_kind,
  membership_graph.inheritance_depth,
  parent_role.rolname
LIMIT 5001;
\echo __GATE_B1_BOUNDARY__|:boundary_token|END|SQL-GATE-B1-004

-- SQL-GATE-B1-005: database ownership, CREATE, and TEMP findings
\echo __GATE_B1_BOUNDARY__|:boundary_token|BEGIN|SQL-GATE-B1-005
WITH identities AS (
  SELECT 'session_user'::text AS identity_kind, session_user::name AS role_name
  UNION
  SELECT 'current_user'::text AS identity_kind, current_user::name AS role_name
)
SELECT
  'SQL-GATE-B1-005' AS query_id,
  identities.identity_kind,
  identities.role_name,
  database_entry.datdba = role_entry.oid AS is_database_owner,
  pg_catalog.has_database_privilege(
    identities.role_name,
    pg_catalog.current_database(),
    'CREATE'
  ) AS can_create,
  pg_catalog.has_database_privilege(
    identities.role_name,
    pg_catalog.current_database(),
    'TEMP'
  ) AS can_create_temp
FROM identities
JOIN pg_catalog.pg_roles AS role_entry
  ON role_entry.rolname = identities.role_name
CROSS JOIN pg_catalog.pg_database AS database_entry
WHERE database_entry.datname = pg_catalog.current_database()
  AND (
    database_entry.datdba = role_entry.oid
    OR pg_catalog.has_database_privilege(
      identities.role_name,
      pg_catalog.current_database(),
      'CREATE'
    )
    OR pg_catalog.has_database_privilege(
      identities.role_name,
      pg_catalog.current_database(),
      'TEMP'
    )
  )
ORDER BY identities.identity_kind
LIMIT 5001;
\echo __GATE_B1_BOUNDARY__|:boundary_token|END|SQL-GATE-B1-005

-- SQL-GATE-B1-006: schema ownership or CREATE findings
\echo __GATE_B1_BOUNDARY__|:boundary_token|BEGIN|SQL-GATE-B1-006
WITH identities AS (
  SELECT 'session_user'::text AS identity_kind, session_user::name AS role_name
  UNION
  SELECT 'current_user'::text AS identity_kind, current_user::name AS role_name
)
SELECT
  'SQL-GATE-B1-006' AS query_id,
  identities.identity_kind,
  identities.role_name,
  namespace.nspname AS schema_name,
  namespace.nspowner = role_entry.oid AS is_schema_owner,
  pg_catalog.has_schema_privilege(
    identities.role_name,
    namespace.oid,
    'CREATE'
  ) AS can_create
FROM identities
JOIN pg_catalog.pg_roles AS role_entry
  ON role_entry.rolname = identities.role_name
CROSS JOIN pg_catalog.pg_namespace AS namespace
WHERE namespace.nspname NOT IN ('pg_catalog', 'information_schema')
  AND namespace.nspname NOT LIKE 'pg_toast%'
  AND namespace.nspname NOT LIKE 'pg_temp_%'
  AND (
    namespace.nspowner = role_entry.oid
    OR pg_catalog.has_schema_privilege(
      identities.role_name,
      namespace.oid,
      'CREATE'
    )
  )
ORDER BY identities.identity_kind, schema_name
LIMIT 5001;
\echo __GATE_B1_BOUNDARY__|:boundary_token|END|SQL-GATE-B1-006

-- SQL-GATE-B1-007: relation ownership or table-level write findings
\echo __GATE_B1_BOUNDARY__|:boundary_token|BEGIN|SQL-GATE-B1-007
WITH identities AS (
  SELECT 'session_user'::text AS identity_kind, session_user::name AS role_name
  UNION
  SELECT 'current_user'::text AS identity_kind, current_user::name AS role_name
)
SELECT
  'SQL-GATE-B1-007' AS query_id,
  identities.identity_kind,
  identities.role_name,
  namespace.nspname AS schema_name,
  relation.relname AS relation_name,
  relation.relkind,
  relation.relowner = role_entry.oid AS is_relation_owner,
  pg_catalog.has_table_privilege(
    identities.role_name,
    relation.oid,
    'INSERT'
  ) AS can_insert,
  pg_catalog.has_table_privilege(
    identities.role_name,
    relation.oid,
    'UPDATE'
  ) AS can_update,
  pg_catalog.has_table_privilege(
    identities.role_name,
    relation.oid,
    'DELETE'
  ) AS can_delete,
  pg_catalog.has_table_privilege(
    identities.role_name,
    relation.oid,
    'TRUNCATE'
  ) AS can_truncate,
  pg_catalog.has_table_privilege(
    identities.role_name,
    relation.oid,
    'TRIGGER'
  ) AS can_trigger
FROM identities
JOIN pg_catalog.pg_roles AS role_entry
  ON role_entry.rolname = identities.role_name
CROSS JOIN pg_catalog.pg_class AS relation
JOIN pg_catalog.pg_namespace AS namespace
  ON namespace.oid = relation.relnamespace
WHERE relation.relkind IN ('r', 'p', 'v', 'm', 'f')
  AND namespace.nspname NOT IN ('pg_catalog', 'information_schema')
  AND namespace.nspname NOT LIKE 'pg_toast%'
  AND namespace.nspname NOT LIKE 'pg_temp_%'
  AND (
    relation.relowner = role_entry.oid
    OR pg_catalog.has_table_privilege(
      identities.role_name,
      relation.oid,
      'INSERT'
    )
    OR pg_catalog.has_table_privilege(
      identities.role_name,
      relation.oid,
      'UPDATE'
    )
    OR pg_catalog.has_table_privilege(
      identities.role_name,
      relation.oid,
      'DELETE'
    )
    OR pg_catalog.has_table_privilege(
      identities.role_name,
      relation.oid,
      'TRUNCATE'
    )
    OR pg_catalog.has_table_privilege(
      identities.role_name,
      relation.oid,
      'TRIGGER'
    )
  )
ORDER BY identities.identity_kind, schema_name, relation_name
LIMIT 5001;
\echo __GATE_B1_BOUNDARY__|:boundary_token|END|SQL-GATE-B1-007

-- SQL-GATE-B1-008: effective column-level INSERT or UPDATE findings
\echo __GATE_B1_BOUNDARY__|:boundary_token|BEGIN|SQL-GATE-B1-008
WITH identities AS (
  SELECT 'session_user'::text AS identity_kind, session_user::name AS role_name
  UNION
  SELECT 'current_user'::text AS identity_kind, current_user::name AS role_name
)
SELECT
  'SQL-GATE-B1-008' AS query_id,
  identities.identity_kind,
  identities.role_name,
  namespace.nspname AS schema_name,
  relation.relname AS relation_name,
  attribute.attname AS column_name,
  pg_catalog.has_column_privilege(
    identities.role_name,
    relation.oid,
    attribute.attnum,
    'INSERT'
  ) AS can_insert,
  pg_catalog.has_column_privilege(
    identities.role_name,
    relation.oid,
    attribute.attnum,
    'UPDATE'
  ) AS can_update
FROM identities
CROSS JOIN pg_catalog.pg_attribute AS attribute
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
  AND (
    pg_catalog.has_column_privilege(
      identities.role_name,
      relation.oid,
      attribute.attnum,
      'INSERT'
    )
    OR pg_catalog.has_column_privilege(
      identities.role_name,
      relation.oid,
      attribute.attnum,
      'UPDATE'
    )
  )
ORDER BY
  identities.identity_kind,
  schema_name,
  relation_name,
  column_name
LIMIT 5001;
\echo __GATE_B1_BOUNDARY__|:boundary_token|END|SQL-GATE-B1-008

-- SQL-GATE-B1-009: sequence ownership, UPDATE, or USAGE findings
\echo __GATE_B1_BOUNDARY__|:boundary_token|BEGIN|SQL-GATE-B1-009
WITH identities AS (
  SELECT 'session_user'::text AS identity_kind, session_user::name AS role_name
  UNION
  SELECT 'current_user'::text AS identity_kind, current_user::name AS role_name
)
SELECT
  'SQL-GATE-B1-009' AS query_id,
  identities.identity_kind,
  identities.role_name,
  namespace.nspname AS schema_name,
  sequence_entry.relname AS sequence_name,
  sequence_entry.relowner = role_entry.oid AS is_sequence_owner,
  pg_catalog.has_sequence_privilege(
    identities.role_name,
    sequence_entry.oid,
    'USAGE'
  ) AS can_use,
  pg_catalog.has_sequence_privilege(
    identities.role_name,
    sequence_entry.oid,
    'UPDATE'
  ) AS can_update
FROM identities
JOIN pg_catalog.pg_roles AS role_entry
  ON role_entry.rolname = identities.role_name
CROSS JOIN pg_catalog.pg_class AS sequence_entry
JOIN pg_catalog.pg_namespace AS namespace
  ON namespace.oid = sequence_entry.relnamespace
WHERE sequence_entry.relkind = 'S'
  AND namespace.nspname NOT IN ('pg_catalog', 'information_schema')
  AND namespace.nspname NOT LIKE 'pg_toast%'
  AND namespace.nspname NOT LIKE 'pg_temp_%'
  AND (
    sequence_entry.relowner = role_entry.oid
    OR pg_catalog.has_sequence_privilege(
      identities.role_name,
      sequence_entry.oid,
      'USAGE'
    )
    OR pg_catalog.has_sequence_privilege(
      identities.role_name,
      sequence_entry.oid,
      'UPDATE'
    )
  )
ORDER BY identities.identity_kind, schema_name, sequence_name
LIMIT 5001;
\echo __GATE_B1_BOUNDARY__|:boundary_token|END|SQL-GATE-B1-009

-- SQL-GATE-B1-010: owned routines or executable SECURITY DEFINER routines
\echo __GATE_B1_BOUNDARY__|:boundary_token|BEGIN|SQL-GATE-B1-010
WITH identities AS (
  SELECT 'session_user'::text AS identity_kind, session_user::name AS role_name
  UNION
  SELECT 'current_user'::text AS identity_kind, current_user::name AS role_name
)
SELECT
  'SQL-GATE-B1-010' AS query_id,
  identities.identity_kind,
  identities.role_name,
  namespace.nspname AS routine_schema,
  routine.proname AS routine_name,
  pg_catalog.pg_get_function_identity_arguments(routine.oid) AS arguments,
  routine.proowner = role_entry.oid AS is_routine_owner,
  routine.prosecdef AS security_definer,
  pg_catalog.has_function_privilege(
    identities.role_name,
    routine.oid,
    'EXECUTE'
  ) AS can_execute
FROM identities
JOIN pg_catalog.pg_roles AS role_entry
  ON role_entry.rolname = identities.role_name
CROSS JOIN pg_catalog.pg_proc AS routine
JOIN pg_catalog.pg_namespace AS namespace
  ON namespace.oid = routine.pronamespace
WHERE namespace.nspname NOT IN ('pg_catalog', 'information_schema')
  AND namespace.nspname NOT LIKE 'pg_toast%'
  AND namespace.nspname NOT LIKE 'pg_temp_%'
  AND (
    routine.proowner = role_entry.oid
    OR (
      routine.prosecdef
      AND pg_catalog.has_function_privilege(
        identities.role_name,
        routine.oid,
        'EXECUTE'
      )
    )
  )
ORDER BY identities.identity_kind, routine_schema, routine_name, arguments
LIMIT 5001;
\echo __GATE_B1_BOUNDARY__|:boundary_token|END|SQL-GATE-B1-010

-- SQL-GATE-B1-011: detect identity changes and re-check active guardrails
\echo __GATE_B1_BOUNDARY__|:boundary_token|BEGIN|SQL-GATE-B1-011
SELECT
  'SQL-GATE-B1-011' AS query_id,
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
\echo __GATE_B1_BOUNDARY__|:boundary_token|END|SQL-GATE-B1-011

ROLLBACK;
