\set ON_ERROR_STOP on

-- Production mutation for Q10.2b/Q10.2o. Own gate. No password in this file.
-- Password is set afterwards interactively; never in Git or chat.

BEGIN;
SET LOCAL statement_timeout = '30s';
SET LOCAL lock_timeout = '2s';
SET LOCAL idle_in_transaction_session_timeout = '90s';
SET LOCAL search_path = pg_catalog;

SELECT 1 / ((current_setting('server_version_num')::integer
  BETWEEN 170000 AND 179999)::integer) AS tested_version_guard
\gset

SELECT 1 / (
  (pg_catalog.current_database() = :'expected_database_name'
   AND session_user = :'expected_user')::integer
) AS identity_guard
\gset

SELECT 1 / (
  (NOT EXISTS (
    SELECT 1
    FROM pg_catalog.pg_roles
    WHERE rolname = 'dino_crm_discovery_ro_v1'
  ))::integer
) AS role_absence_guard
\gset

CREATE ROLE dino_crm_discovery_ro_v1
  LOGIN
  NOINHERIT
  NOSUPERUSER
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION
  NOBYPASSRLS
  CONNECTION LIMIT 1
  PASSWORD NULL;

REVOKE ALL PRIVILEGES
  ON DATABASE :"expected_database_name"
  FROM dino_crm_discovery_ro_v1;

GRANT CONNECT
  ON DATABASE :"expected_database_name"
  TO dino_crm_discovery_ro_v1;

ALTER ROLE dino_crm_discovery_ro_v1
  SET default_transaction_read_only = 'on';
ALTER ROLE dino_crm_discovery_ro_v1
  SET statement_timeout = '5s';
ALTER ROLE dino_crm_discovery_ro_v1
  SET lock_timeout = '1s';
ALTER ROLE dino_crm_discovery_ro_v1
  SET idle_in_transaction_session_timeout = '15s';
ALTER ROLE dino_crm_discovery_ro_v1
  SET search_path = pg_catalog, information_schema;


-- Evaluate the fixed new role explicitly; the creator need not SET ROLE.

WITH active_role AS (
  SELECT role_entry.*
  FROM pg_catalog.pg_roles AS role_entry
  WHERE role_entry.rolname = 'dino_crm_discovery_ro_v1'
),
effective_findings AS (
  SELECT 1 AS finding
  FROM active_role
  WHERE rolsuper
    OR rolinherit
    OR rolcreaterole
    OR rolcreatedb
    OR NOT rolcanlogin
    OR rolreplication
    OR rolbypassrls
    OR rolconnlimit <> 1

  UNION ALL

  SELECT 1
  FROM active_role
  WHERE pg_catalog.has_database_privilege(
      'dino_crm_discovery_ro_v1',
      pg_catalog.current_database(),
      'CREATE'
    )
    OR pg_catalog.has_database_privilege(
      'dino_crm_discovery_ro_v1',
      pg_catalog.current_database(),
      'TEMP'
    )

  UNION ALL

  SELECT 1
  FROM pg_catalog.pg_namespace AS namespace_entry
  JOIN active_role
    ON TRUE
  WHERE namespace_entry.nspowner = active_role.oid
    OR pg_catalog.has_schema_privilege(
      'dino_crm_discovery_ro_v1',
      namespace_entry.oid,
      'CREATE'
    )

  UNION ALL

  SELECT 1
  FROM pg_catalog.pg_class AS relation_entry
  JOIN active_role
    ON TRUE
  WHERE relation_entry.relkind IN ('r', 'p', 'v', 'm', 'f')
    AND (
      relation_entry.relowner = active_role.oid
      OR pg_catalog.has_table_privilege(
        'dino_crm_discovery_ro_v1',
        relation_entry.oid,
        'INSERT,DELETE,TRUNCATE,REFERENCES,TRIGGER,MAINTAIN'
      )
      -- Updating this exact built-in view is session-local SET, not data DML.
      OR (
        relation_entry.oid <> 'pg_catalog.pg_settings'::pg_catalog.regclass
        AND pg_catalog.has_table_privilege(
          'dino_crm_discovery_ro_v1', relation_entry.oid, 'UPDATE'
        )
      )
    )

  UNION ALL

  SELECT 1
  FROM pg_catalog.pg_attribute AS attribute_entry
  JOIN pg_catalog.pg_class AS relation_entry
    ON relation_entry.oid = attribute_entry.attrelid
  WHERE relation_entry.relkind IN ('r', 'p', 'v', 'm', 'f')
    AND attribute_entry.attnum > 0
    AND NOT attribute_entry.attisdropped
    AND (
      pg_catalog.has_column_privilege(
        'dino_crm_discovery_ro_v1', relation_entry.oid, attribute_entry.attnum, 'INSERT'
      )
      OR (
        relation_entry.oid <> 'pg_catalog.pg_settings'::pg_catalog.regclass
        AND pg_catalog.has_column_privilege(
          'dino_crm_discovery_ro_v1', relation_entry.oid, attribute_entry.attnum, 'UPDATE'
        )
      )
    )

  UNION ALL

  SELECT 1
  FROM pg_catalog.pg_class AS sequence_entry
  JOIN active_role
    ON TRUE
  WHERE sequence_entry.relkind = 'S'
    AND (
      sequence_entry.relowner = active_role.oid
      OR pg_catalog.has_sequence_privilege(
        'dino_crm_discovery_ro_v1',
        sequence_entry.oid,
        'USAGE,UPDATE'
      )
    )

  UNION ALL

  SELECT 1
  FROM pg_catalog.pg_proc AS routine_entry
  JOIN active_role
    ON TRUE
  WHERE routine_entry.proowner = active_role.oid
    OR (
      routine_entry.prosecdef
      AND pg_catalog.has_function_privilege(
        'dino_crm_discovery_ro_v1',
        routine_entry.oid,
        'EXECUTE'
      )
    )

  UNION ALL

  SELECT 1
  FROM pg_catalog.pg_auth_members AS membership
  JOIN active_role
    ON membership.member = active_role.oid
      OR membership.roleid = active_role.oid
  WHERE membership.member = active_role.oid
    OR NOT (
      membership.roleid = active_role.oid
      AND membership.member = (
        SELECT oid FROM pg_catalog.pg_roles WHERE rolname = current_user
      )
      AND membership.admin_option
      AND NOT membership.inherit_option
      AND NOT membership.set_option
      AND (
        membership.grantor = (
          SELECT oid FROM pg_catalog.pg_roles WHERE rolname = current_user
        )
        OR EXISTS (
          SELECT 1 FROM pg_catalog.pg_roles AS grantor
          WHERE grantor.oid = membership.grantor AND grantor.rolsuper
        )
      )
    )
)
SELECT 1 / (
  ((EXISTS (SELECT 1 FROM active_role)
    AND NOT EXISTS (SELECT 1 FROM effective_findings)
  ))::integer
) AS least_privilege_guard
\gset

SELECT 1 / (
  (EXISTS (
    SELECT 1
    FROM pg_catalog.pg_db_role_setting AS role_setting
    JOIN pg_catalog.pg_roles AS role_entry
      ON role_entry.oid = role_setting.setrole
    WHERE role_entry.rolname = 'dino_crm_discovery_ro_v1'
      AND role_setting.setdatabase = 0
      AND role_setting.setconfig @> ARRAY[
        'default_transaction_read_only=on',
        'statement_timeout=5s',
        'lock_timeout=1s',
        'idle_in_transaction_session_timeout=15s',
        'search_path=pg_catalog, information_schema'
      ]::text[]
  ))::integer
) AS role_settings_guard
\gset

COMMIT;
