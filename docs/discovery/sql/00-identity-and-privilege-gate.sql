-- SECURITY-REVIEW ONLY. DO NOT EXECUTE WITHOUT THE SEPARATE USER APPROVAL.
-- Scope: PostgreSQL 15-18 identity and effective-privilege metadata only.
-- Run this file before any other discovery SQL. Every statement is read-only.

BEGIN TRANSACTION READ ONLY;
SET LOCAL statement_timeout = '5s';
SET LOCAL lock_timeout = '1s';
SET LOCAL idle_in_transaction_session_timeout = '15s';
SET LOCAL search_path = pg_catalog, information_schema;

-- SQL-GATE-001: environment and active identity
SELECT
  current_database() AS database_name,
  current_user AS current_role,
  session_user AS session_role,
  current_setting('server_version_num') AS server_version_num,
  current_setting('transaction_read_only') AS transaction_read_only,
  pg_is_in_recovery() AS is_replica;

-- SQL-GATE-002: role capabilities that can bypass the discovery boundary
SELECT
  rolname,
  rolsuper,
  rolinherit,
  rolcreaterole,
  rolcreatedb,
  rolcanlogin,
  rolreplication,
  rolbypassrls,
  rolconnlimit
FROM pg_catalog.pg_roles
WHERE rolname = current_user;

-- SQL-GATE-003: direct and inherited parent-role memberships
WITH RECURSIVE membership AS (
  SELECT
    m.roleid,
    m.member,
    m.admin_option,
    ARRAY[m.member, m.roleid] AS visited
  FROM pg_catalog.pg_auth_members AS m
  JOIN pg_catalog.pg_roles AS child_role
    ON child_role.oid = m.member
  WHERE child_role.rolname = current_user

  UNION ALL

  SELECT
    m.roleid,
    m.member,
    m.admin_option,
    membership.visited || m.roleid
  FROM pg_catalog.pg_auth_members AS m
  JOIN membership
    ON membership.roleid = m.member
  WHERE NOT m.roleid = ANY(membership.visited)
)
SELECT DISTINCT
  parent_role.rolname AS inherited_role,
  membership.admin_option
FROM membership
JOIN pg_catalog.pg_roles AS parent_role
  ON parent_role.oid = membership.roleid
ORDER BY inherited_role;

-- SQL-GATE-004: database ownership and effective database privileges
SELECT
  current_database() AS database_name,
  pg_catalog.pg_get_userbyid(database_entry.datdba) AS database_owner,
  database_entry.datdba = active_role.oid AS current_role_is_owner,
  pg_catalog.has_database_privilege(
    current_user,
    current_database(),
    'CONNECT'
  ) AS can_connect,
  pg_catalog.has_database_privilege(
    current_user,
    current_database(),
    'CREATE'
  ) AS can_create,
  pg_catalog.has_database_privilege(
    current_user,
    current_database(),
    'TEMP'
  ) AS can_create_temp
FROM pg_catalog.pg_database AS database_entry
CROSS JOIN pg_catalog.pg_roles AS active_role
WHERE database_entry.datname = current_database()
  AND active_role.rolname = current_user;

-- SQL-GATE-005: schema ownership and effective CREATE privileges
SELECT
  namespace.nspname AS schema_name,
  pg_catalog.pg_get_userbyid(namespace.nspowner) AS schema_owner,
  namespace.nspowner = active_role.oid AS current_role_is_owner,
  pg_catalog.has_schema_privilege(
    current_user,
    namespace.oid,
    'USAGE'
  ) AS can_use,
  pg_catalog.has_schema_privilege(
    current_user,
    namespace.oid,
    'CREATE'
  ) AS can_create
FROM pg_catalog.pg_namespace AS namespace
CROSS JOIN pg_catalog.pg_roles AS active_role
WHERE active_role.rolname = current_user
  AND namespace.nspname NOT IN ('pg_catalog', 'information_schema')
  AND namespace.nspname NOT LIKE 'pg_toast%'
  AND namespace.nspname NOT LIKE 'pg_temp_%'
ORDER BY schema_name
LIMIT 10000;

-- SQL-GATE-006: relation ownership and effective write-capable privileges
SELECT
  namespace.nspname AS schema_name,
  relation.relname AS relation_name,
  relation.relkind,
  pg_catalog.pg_get_userbyid(relation.relowner) AS relation_owner,
  relation.relowner = active_role.oid AS current_role_is_owner,
  pg_catalog.has_table_privilege(
    current_user,
    relation.oid,
    'INSERT'
  ) AS can_insert,
  pg_catalog.has_table_privilege(
    current_user,
    relation.oid,
    'UPDATE'
  ) AS can_update,
  pg_catalog.has_table_privilege(
    current_user,
    relation.oid,
    'DELETE'
  ) AS can_delete,
  pg_catalog.has_table_privilege(
    current_user,
    relation.oid,
    'TRUNCATE'
  ) AS can_truncate,
  pg_catalog.has_table_privilege(
    current_user,
    relation.oid,
    'TRIGGER'
  ) AS can_trigger
FROM pg_catalog.pg_class AS relation
JOIN pg_catalog.pg_namespace AS namespace
  ON namespace.oid = relation.relnamespace
CROSS JOIN pg_catalog.pg_roles AS active_role
WHERE active_role.rolname = current_user
  AND relation.relkind IN ('r', 'p', 'v', 'm', 'f')
  AND namespace.nspname NOT IN ('pg_catalog', 'information_schema')
  AND namespace.nspname NOT LIKE 'pg_toast%'
  AND namespace.nspname NOT LIKE 'pg_temp_%'
  AND (
    relation.relowner = active_role.oid
    OR pg_catalog.has_table_privilege(
      current_user,
      relation.oid,
      'INSERT'
    )
    OR pg_catalog.has_table_privilege(
      current_user,
      relation.oid,
      'UPDATE'
    )
    OR pg_catalog.has_table_privilege(
      current_user,
      relation.oid,
      'DELETE'
    )
    OR pg_catalog.has_table_privilege(
      current_user,
      relation.oid,
      'TRUNCATE'
    )
    OR pg_catalog.has_table_privilege(
      current_user,
      relation.oid,
      'TRIGGER'
    )
  )
ORDER BY schema_name, relation_name
LIMIT 10000;

-- SQL-GATE-007: executable SECURITY DEFINER routines
SELECT
  namespace.nspname AS routine_schema,
  routine.proname AS routine_name,
  pg_catalog.pg_get_function_identity_arguments(routine.oid) AS arguments,
  pg_catalog.pg_get_userbyid(routine.proowner) AS routine_owner
FROM pg_catalog.pg_proc AS routine
JOIN pg_catalog.pg_namespace AS namespace
  ON namespace.oid = routine.pronamespace
WHERE namespace.nspname NOT IN ('pg_catalog', 'information_schema')
  AND namespace.nspname NOT LIKE 'pg_toast%'
  AND namespace.nspname NOT LIKE 'pg_temp_%'
  AND routine.prosecdef
  AND pg_catalog.has_function_privilege(
    current_user,
    routine.oid,
    'EXECUTE'
  )
ORDER BY routine_schema, routine_name, arguments
LIMIT 10000;

-- SQL-GATE-008: applied session guardrails
SELECT
  current_setting('transaction_read_only') AS transaction_read_only,
  current_setting('statement_timeout') AS statement_timeout,
  current_setting('lock_timeout') AS lock_timeout,
  current_setting(
    'idle_in_transaction_session_timeout'
  ) AS idle_in_transaction_session_timeout;

ROLLBACK;
