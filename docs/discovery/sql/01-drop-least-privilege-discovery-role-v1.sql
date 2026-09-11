\set ON_ERROR_STOP on

-- This rollback is a separate production mutation and requires approval.
-- DROP ROLE has no CASCADE path; dependencies cause a fail-closed rollback.

BEGIN;
SET LOCAL statement_timeout = '5s';
SET LOCAL lock_timeout = '1s';
SET LOCAL idle_in_transaction_session_timeout = '15s';
SET LOCAL search_path = pg_catalog;

SELECT 1 / (
  (pg_catalog.current_database() = :'expected_database_name')::integer
) AS target_guard
\gset

SELECT 1 / (
  (EXISTS (
    SELECT 1
    FROM pg_catalog.pg_roles
    WHERE rolname = 'dino_crm_discovery_ro_v1'
  ))::integer
) AS role_presence_guard
\gset

-- Remove only the database grant created by the paired setup.
-- RESTRICT and DROP ROLE preserve unexpected dependencies as a hard failure.
REVOKE CONNECT
  ON DATABASE :"expected_database_name"
  FROM dino_crm_discovery_ro_v1 RESTRICT;

DROP ROLE dino_crm_discovery_ro_v1;

COMMIT;

\echo PASS: least-privilege discovery role removed
