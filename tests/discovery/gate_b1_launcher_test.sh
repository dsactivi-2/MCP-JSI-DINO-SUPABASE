#!/bin/bash

set -euo pipefail

readonly REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)"
readonly LAUNCHER="${REPO_ROOT}/scripts/discovery/run-gate-b1.sh"

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  exit 1
}

test_hash_mismatch_stops_before_psql() {
  local test_root output status
  test_root="$(mktemp -d "${TMPDIR:-/tmp}/gate-b1-test.XXXXXX")"
  test_root="$(cd "${test_root}" && pwd -P)"
  trap 'rm -rf "${test_root}"' RETURN

  mkdir -p "${test_root}/config" "${test_root}/sql" "${test_root}/bin"
  chmod 700 "${test_root}" "${test_root}/config" "${test_root}/sql" "${test_root}/bin"

  printf '%s\n' 'synthetic gate sql' >"${test_root}/sql/gate-b1.sql"
  printf '%s\n' \
    'gate_id=DISCOVERY-GATE-B1-V2-2026-09-11' \
    'target_alias=dino_crm_discovery_target_01' \
    'window_start_epoch=2000000000' \
    'window_end_epoch=2000001800' \
    'sql_sha256=ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff' \
    >"${test_root}/config/approval.attest"
  chmod 600 "${test_root}/config/approval.attest"

  printf '%s\n' '#!/bin/bash' 'printf invoked >"${GATE_B1_TEST_ROOT}/psql-invoked"' \
    >"${test_root}/bin/fake-psql"
  chmod 700 "${test_root}/bin/fake-psql"

  set +e
  output="$(
    GATE_B1_TEST_ROOT="${test_root}" \
    GATE_B1_NOW_EPOCH=2000000001 \
      "${LAUNCHER}" --test-mode 2>&1
  )"
  status=$?
  set -e

  [[ ${status} -ne 0 ]] || fail 'hash mismatch returned success'
  [[ ! -e "${test_root}/psql-invoked" ]] || fail 'fake psql was invoked'
  [[ "${output}" != *'synthetic gate sql'* ]] || fail 'sensitive test value was printed'
  [[ "${output}" == *'STOP: SQL hash mismatch'* ]] || fail 'stable stop reason missing'

  trap - RETURN
  rm -rf "${test_root}"
}

test_valid_fake_run_writes_minimized_manifest() {
  local test_root sql_hash target_hash output status manifest raw_output
  test_root="$(mktemp -d "${TMPDIR:-/tmp}/gate-b1-test.XXXXXX")"
  test_root="$(cd "${test_root}" && pwd -P)"
  trap 'rm -rf "${test_root}"' RETURN

  mkdir -p \
    "${test_root}/config" \
    "${test_root}/sql" \
    "${test_root}/bin" \
    "${test_root}/raw"
  chmod 700 \
    "${test_root}" \
    "${test_root}/config" \
    "${test_root}/sql" \
    "${test_root}/bin" \
    "${test_root}/raw"

  printf '%s\n' 'synthetic gate sql' >"${test_root}/sql/gate-b1.sql"
  sql_hash="$(shasum -a 256 "${test_root}/sql/gate-b1.sql")"
  sql_hash="${sql_hash%% *}"
  target_hash="$(printf '%s' 'test_target' | shasum -a 256)"
  target_hash="${target_hash%% *}"

  printf '%s\n' \
    'status=GRANTED' \
    'gate_id=DISCOVERY-GATE-B1-V2-2026-09-11' \
    'target_alias=dino_crm_discovery_target_01' \
    'window_start_epoch=2000000000' \
    'window_end_epoch=2000001800' \
    "sql_sha256=${sql_hash}" \
    'retention_delete_authorized=true' \
    'retention_seconds=86400' \
    >"${test_root}/config/approval.attest"
  chmod 600 "${test_root}/config/approval.attest"

  printf '%s\n' \
    'target_alias=dino_crm_discovery_target_01' \
    'expected_database_name=TEST_DATABASE' \
    "target_fingerprint_sha256=${target_hash}" \
    'connection_service=dino_crm_discovery_target_01' \
    'created_at_epoch=1999999000' \
    'responsible_person=TEST_OWNER' \
    >"${test_root}/config/target.attest"
  chmod 600 "${test_root}/config/target.attest"

  printf '%s\n' \
    '[dino_crm_discovery_target_01]' \
    'host=TEST_TARGET' \
    'dbname=TEST_DATABASE' \
    'user=TEST_IDENTITY' \
    'sslmode=require' \
    'connect_timeout=5' \
    >"${test_root}/config/pg_service.conf"
  chmod 600 "${test_root}/config/pg_service.conf"
  printf '%s\n' 'SYNTHETIC_CREDENTIAL_RECORD' >"${test_root}/config/pgpass"
  chmod 600 "${test_root}/config/pgpass"

  {
    printf '%s\n' '#!/bin/bash' 'set -euo pipefail'
    printf '%s\n' \
      'test_root="${PGPASSFILE%/config/pgpass}"' \
      'printf "invoked\\n" >"${test_root}/psql-invoked"' \
      'boundary_token=' \
      'for argument in "$@"; do' \
      '  case "${argument}" in' \
      '    --set=boundary_token=*) boundary_token="${argument#--set=boundary_token=}" ;;' \
      '  esac' \
      'done' \
      'for query_number in 001 002 003 004 005 006 007 008 009 010 011; do' \
      '  query_id="SQL-GATE-B1-${query_number}"' \
      '  printf "__GATE_B1_BOUNDARY__|%s|BEGIN|%s\\n" "${boundary_token}" "${query_id}"' \
      '  if [[ "${query_number}" != 005 ]]; then' \
      '    printf "%s,%s\\n" "${query_id}" "SENSITIVE_FAKE_VALUE"' \
      '  fi' \
      '  printf "__GATE_B1_BOUNDARY__|%s|END|%s\\n" "${boundary_token}" "${query_id}"' \
      'done'
  } >"${test_root}/bin/fake-psql"
  chmod 700 "${test_root}/bin/fake-psql"

  set +e
  output="$(
    GATE_B1_TEST_ROOT="${test_root}" \
    GATE_B1_NOW_EPOCH=2000000001 \
      "${LAUNCHER}" --test-mode 2>&1
  )"
  status=$?
  set -e

  manifest="${test_root}/raw/DISCOVERY-GATE-B1-V2-2026-09-11/gate-b1-manifest.json"
  raw_output="${test_root}/raw/DISCOVERY-GATE-B1-V2-2026-09-11/gate-b1.out"
  if [[ ${status} -ne 0 ]]; then
    [[ "${output}" != *'SENSITIVE_FAKE_VALUE'* ]] || fail 'valid fake run leaked result data'
    fail "valid fake run returned failure: ${output}"
  fi
  [[ -f "${test_root}/psql-invoked" ]] || fail 'fake psql was not invoked'
  [[ -f "${manifest}" && -f "${raw_output}" ]] || fail 'run artifacts missing'
  [[ "${output}" != *'SENSITIVE_FAKE_VALUE'* ]] || fail 'sensitive fake output reached terminal'
  [[ "$(<"${manifest}")" != *'SENSITIVE_FAKE_VALUE'* ]] || fail 'manifest contains result data'
  [[ "$(<"${manifest}")" == *'"status":"PASS"'* ]] || fail 'manifest is not PASS'
  [[ "$(<"${manifest}")" == *'"SQL-GATE-B1-005":0'* ]] || fail 'null-row query boundary was not preserved'
  [[ "$(stat -f '%Lp' "$(dirname "${manifest}")")" == '700' ]] || fail 'raw directory mode is not 0700'
  [[ "$(stat -f '%Lp' "${manifest}")" == '600' ]] || fail 'manifest mode is not 0600'
  [[ "$(stat -f '%Lp' "${raw_output}")" == '600' ]] || fail 'raw output mode is not 0600'

  trap - RETURN
  rm -rf "${test_root}"
}

create_valid_case() {
  local sql_hash target_hash
  CASE_ROOT="$(mktemp -d "${CASE_TEMPLATE:-${TMPDIR:-/tmp}/gate-b1-test.XXXXXX}")"
  CASE_ROOT="$(cd "${CASE_ROOT}" && pwd -P)"
  mkdir -p \
    "${CASE_ROOT}/config" \
    "${CASE_ROOT}/sql" \
    "${CASE_ROOT}/bin" \
    "${CASE_ROOT}/raw"
  chmod 700 \
    "${CASE_ROOT}" \
    "${CASE_ROOT}/config" \
    "${CASE_ROOT}/sql" \
    "${CASE_ROOT}/bin" \
    "${CASE_ROOT}/raw"

  printf '%s\n' 'synthetic gate sql' >"${CASE_ROOT}/sql/gate-b1.sql"
  sql_hash="$(shasum -a 256 "${CASE_ROOT}/sql/gate-b1.sql")"
  sql_hash="${sql_hash%% *}"
  target_hash="$(printf '%s' 'test_target' | shasum -a 256)"
  target_hash="${target_hash%% *}"

  printf '%s\n' \
    'status=GRANTED' \
    'gate_id=DISCOVERY-GATE-B1-V2-2026-09-11' \
    'target_alias=dino_crm_discovery_target_01' \
    'window_start_epoch=2000000000' \
    'window_end_epoch=2000001800' \
    "sql_sha256=${sql_hash}" \
    'retention_delete_authorized=true' \
    'retention_seconds=86400' \
    >"${CASE_ROOT}/config/approval.attest"
  printf '%s\n' \
    'target_alias=dino_crm_discovery_target_01' \
    'expected_database_name=TEST_DATABASE' \
    "target_fingerprint_sha256=${target_hash}" \
    'connection_service=dino_crm_discovery_target_01' \
    'created_at_epoch=1999999000' \
    'responsible_person=TEST_OWNER' \
    >"${CASE_ROOT}/config/target.attest"
  printf '%s\n' \
    '[dino_crm_discovery_target_01]' \
    'host=TEST_TARGET' \
    'dbname=TEST_DATABASE' \
    'user=TEST_IDENTITY' \
    'sslmode=require' \
    'connect_timeout=5' \
    >"${CASE_ROOT}/config/pg_service.conf"
  printf '%s\n' 'SYNTHETIC_CREDENTIAL_RECORD' >"${CASE_ROOT}/config/pgpass"
  chmod 600 "${CASE_ROOT}/config/"*.attest
  chmod 600 "${CASE_ROOT}/config/pg_service.conf" "${CASE_ROOT}/config/pgpass"
}

write_fake_psql() {
  local scenario="$1"
  {
    printf '%s\n' '#!/bin/bash' 'set -euo pipefail'
    printf 'scenario=%q\n' "${scenario}"
    printf '%s\n' \
      'test_root="${PGPASSFILE%/config/pgpass}"' \
      'count=0' \
      'if [[ -f "${test_root}/psql-invocations" ]]; then read -r count <"${test_root}/psql-invocations"; fi' \
      'printf "%s\\n" "$((count + 1))" >"${test_root}/psql-invocations"' \
      'boundary_token=' \
      'required_flags=0' \
      'for argument in "$@"; do' \
      '  case "${argument}" in' \
      '    -X|--no-psqlrc|--no-password|--set=ON_ERROR_STOP=on|--csv|--tuples-only) required_flags=$((required_flags + 1)) ;;' \
      '    --set=boundary_token=*) boundary_token="${argument#--set=boundary_token=}" ;;' \
      '    --set=expected_database_name=TEST_DATABASE) : ;;' \
      '    --file=*) : ;;' \
      '    *) exit 64 ;;' \
      '  esac' \
      'done' \
      '[[ ${required_flags} -eq 6 && -n "${boundary_token}" ]] || exit 64' \
      'case "${scenario}" in' \
      '  hang)' \
      '    sleep 2' \
      '    ;;' \
      '  client_error)' \
      '    exit 7' \
      '    ;;' \
      '  sql_error)' \
      '    printf "__GATE_B1_BOUNDARY__|%s|BEGIN|SQL-GATE-B1-001\\n" "${boundary_token}"' \
      '    printf "SYNTHETIC_SQL_FAILURE\\n"' \
      '    exit 3' \
      '    ;;' \
      '  sentinel)' \
      '    printf "__GATE_B1_BOUNDARY__|%s|BEGIN|SQL-GATE-B1-001\\n" "${boundary_token}"' \
      '    row=1' \
      '    while [[ ${row} -le 5001 ]]; do' \
      '      printf "SQL-GATE-B1-001,%s\\n" "${row}"' \
      '      row=$((row + 1))' \
      '    done' \
      '    ;;' \
      '  query_bytes)' \
      '    printf "__GATE_B1_BOUNDARY__|%s|BEGIN|SQL-GATE-B1-001\\n" "${boundary_token}"' \
      '    /opt/homebrew/bin/python3 -c '\''import sys; sys.stdout.write("SQL-GATE-B1-001," + "X" * (2 * 1024 * 1024) + "\n")'\''' \
      '    ;;' \
      '  total_bytes)' \
      '    for query_number in 001 002 003 004 005 006 007 008 009 010 011; do' \
      '      query_id="SQL-GATE-B1-${query_number}"' \
      '      printf "__GATE_B1_BOUNDARY__|%s|BEGIN|%s\\n" "${boundary_token}" "${query_id}"' \
      '      /opt/homebrew/bin/python3 -c '\''import sys; sys.stdout.write(sys.argv[1] + "," + "X" * 1200000 + "\n")'\'' "${query_id}"' \
      '      printf "__GATE_B1_BOUNDARY__|%s|END|%s\\n" "${boundary_token}" "${query_id}"' \
      '    done' \
      '    ;;' \
      '  happy)' \
      '    for query_number in 001 002 003 004 005 006 007 008 009 010 011; do' \
      '      query_id="SQL-GATE-B1-${query_number}"' \
      '      printf "__GATE_B1_BOUNDARY__|%s|BEGIN|%s\\n" "${boundary_token}" "${query_id}"' \
      '      if [[ "${query_number}" != 005 ]]; then' \
      '        printf "%s,%s\\n" "${query_id}" "SENSITIVE_FAKE_VALUE"' \
      '      fi' \
      '      printf "__GATE_B1_BOUNDARY__|%s|END|%s\\n" "${boundary_token}" "${query_id}"' \
      '    done' \
      '    ;;' \
      '  *) exit 65 ;;' \
      'esac'
  } >"${CASE_ROOT}/bin/fake-psql"
  chmod 700 "${CASE_ROOT}/bin/fake-psql"
}

run_case() {
  set +e
  RUN_OUTPUT="$(
    GATE_B1_TEST_ROOT="${CASE_ROOT}" \
    GATE_B1_NOW_EPOCH="${CASE_NOW_EPOCH:-2000000001}" \
    GATE_B1_TEST_TIMEOUT_SECONDS="${CASE_TIMEOUT_SECONDS:-60}" \
    GATE_B1_TEST_EXPECTED_UID="${CASE_EXPECTED_UID:-$(id -u)}" \
      "${LAUNCHER}" --test-mode 2>&1
  )"
  RUN_STATUS=$?
  set -e
}

replace_config_value() {
  local file="$1" key="$2" value="$3"
  perl -pi -e "s/^${key}=.*\$/${key}=${value}/" "${file}"
}

assert_preflight_stop() {
  local expected_reason="$1"
  [[ ${RUN_STATUS} -ne 0 ]] || fail "${expected_reason} returned success"
  [[ "${RUN_OUTPUT}" == *"STOP: ${expected_reason}"* ]] || fail "${expected_reason} stop reason missing"
  [[ ! -e "${CASE_ROOT}/psql-invocations" ]] || fail "${expected_reason} invoked fake psql"
}

test_wrong_owner_stops_before_psql() {
  create_valid_case
  write_fake_psql hang
  CASE_EXPECTED_UID=99999
  run_case

  [[ ${RUN_STATUS} -ne 0 ]] || fail 'wrong owner returned success'
  [[ "${RUN_OUTPUT}" == *'STOP: approval attestation owner mismatch'* ]] || fail 'owner stop reason missing'
  [[ ! -e "${CASE_ROOT}/psql-invocations" ]] || fail 'wrong owner invoked fake psql'

  cleanup_case
  unset CASE_EXPECTED_UID
}

test_preflight_attestation_and_path_guards() {
  create_valid_case
  write_fake_psql happy
  replace_config_value "${CASE_ROOT}/config/approval.attest" target_alias wrong_test_alias
  run_case
  assert_preflight_stop 'target alias mismatch'
  cleanup_case

  create_valid_case
  write_fake_psql happy
  chmod 644 "${CASE_ROOT}/config/target.attest"
  run_case
  assert_preflight_stop 'target attestation mode mismatch'
  cleanup_case

  create_valid_case
  write_fake_psql happy
  mv "${CASE_ROOT}/config/target.attest" "${CASE_ROOT}/config/target.real"
  ln -s "${CASE_ROOT}/config/target.real" "${CASE_ROOT}/config/target.attest"
  run_case
  assert_preflight_stop 'target attestation invalid'
  cleanup_case

  create_valid_case
  write_fake_psql happy
  replace_config_value "${CASE_ROOT}/config/target.attest" target_fingerprint_sha256 ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
  run_case
  assert_preflight_stop 'target fingerprint mismatch'
  cleanup_case
}

test_unknown_attest_and_inline_password_stop() {
  create_valid_case
  write_fake_psql happy
  printf '%s\n' 'unexpected_field=TEST_VALUE' >>"${CASE_ROOT}/config/approval.attest"
  run_case
  assert_preflight_stop 'approval attestation schema invalid'
  cleanup_case

  create_valid_case
  write_fake_psql happy
  printf '%s\n' 'password=SYNTHETIC_FORBIDDEN_VALUE' >>"${CASE_ROOT}/config/pg_service.conf"
  run_case
  assert_preflight_stop 'connection service schema invalid'
  cleanup_case
}

test_raw_time_and_lock_guards() {
  create_valid_case
  write_fake_psql happy
  mkdir -m 700 "${CASE_ROOT}/raw/DISCOVERY-GATE-B1-V2-2026-09-11"
  run_case
  assert_preflight_stop 'raw path already exists'
  cleanup_case

  CASE_TEMPLATE="${REPO_ROOT}/.scratch/gate-b1-test.XXXXXX"
  create_valid_case
  unset CASE_TEMPLATE
  write_fake_psql happy
  run_case
  assert_preflight_stop 'raw path inside repository'
  cleanup_case

  create_valid_case
  write_fake_psql happy
  CASE_NOW_EPOCH=2000001800
  run_case
  assert_preflight_stop 'time window inactive'
  cleanup_case
  unset CASE_NOW_EPOCH

  create_valid_case
  write_fake_psql happy
  replace_config_value "${CASE_ROOT}/config/approval.attest" window_end_epoch 2000001700
  run_case
  assert_preflight_stop 'invalid time window'
  cleanup_case

  create_valid_case
  write_fake_psql happy
  mkdir "${CASE_ROOT}/config/approval.attest.lock"
  run_case
  assert_preflight_stop 'discovery lock conflict'
  cleanup_case
}

test_psql_failures_stop_without_retry() {
  local manifest
  for scenario in client_error sql_error; do
    create_valid_case
    write_fake_psql "${scenario}"
    run_case
    manifest="${CASE_ROOT}/raw/DISCOVERY-GATE-B1-V2-2026-09-11/gate-b1-manifest.json"
    [[ ${RUN_STATUS} -ne 0 ]] || fail "${scenario} returned success"
    [[ "$(<"${CASE_ROOT}/psql-invocations")" == '1' ]] || fail "${scenario} caused retry"
    [[ "$(<"${manifest}")" == *'"status":"STOP"'* ]] || fail "${scenario} manifest is not STOP"
    [[ "${RUN_OUTPUT}" != *'SYNTHETIC_SQL_FAILURE'* ]] || fail "${scenario} leaked raw error"
    cleanup_case
  done
}

test_stream_limits_stop_fail_closed() {
  local manifest expected_reason
  for scenario in sentinel query_bytes total_bytes; do
    case "${scenario}" in
      sentinel) expected_reason='row_sentinel_5001' ;;
      query_bytes) expected_reason='query_byte_limit' ;;
      total_bytes) expected_reason='total_byte_limit' ;;
    esac
    create_valid_case
    write_fake_psql "${scenario}"
    run_case
    manifest="${CASE_ROOT}/raw/DISCOVERY-GATE-B1-V2-2026-09-11/gate-b1-manifest.json"
    [[ ${RUN_STATUS} -ne 0 ]] || fail "${scenario} returned success"
    [[ "${RUN_OUTPUT}" == *"STOP: ${expected_reason}"* ]] || fail "${scenario} stop reason missing: ${RUN_OUTPUT}"
    [[ "$(<"${CASE_ROOT}/psql-invocations")" == '1' ]] || fail "${scenario} caused retry"
    [[ "$(<"${manifest}")" == *"\"stop_reason\":\"${expected_reason}\""* ]] || fail "${scenario} manifest reason missing"
    cleanup_case
  done
}

cleanup_case() {
  rm -rf "${CASE_ROOT}"
}

test_timeout_stops_once_without_retry() {
  local manifest
  create_valid_case
  write_fake_psql hang
  CASE_TIMEOUT_SECONDS=1
  run_case
  manifest="${CASE_ROOT}/raw/DISCOVERY-GATE-B1-V2-2026-09-11/gate-b1-manifest.json"

  [[ ${RUN_STATUS} -ne 0 ]] || fail 'hanging fake psql returned success'
  [[ "${RUN_OUTPUT}" == *'STOP: launcher_timeout'* ]] || fail 'stable timeout reason missing'
  [[ "$(<"${CASE_ROOT}/psql-invocations")" == '1' ]] || fail 'timeout caused a retry'
  [[ "$(<"${manifest}")" == *'"status":"STOP"'* ]] || fail 'timeout manifest is not STOP'

  cleanup_case
  unset CASE_TIMEOUT_SECONDS
}

test_hash_mismatch_stops_before_psql
printf 'PASS: hash mismatch stops before fake psql\n'
test_valid_fake_run_writes_minimized_manifest
printf 'PASS: valid fake run writes minimized manifest\n'
test_timeout_stops_once_without_retry
printf 'PASS: timeout stops once without retry\n'
test_wrong_owner_stops_before_psql
printf 'PASS: wrong owner stops before fake psql\n'
test_preflight_attestation_and_path_guards
printf 'PASS: attestation and path guards stop before fake psql\n'
test_unknown_attest_and_inline_password_stop
printf 'PASS: strict config schemas reject unknown and inline-secret fields\n'
test_raw_time_and_lock_guards
printf 'PASS: raw, time, and lock guards stop before fake psql\n'
test_psql_failures_stop_without_retry
printf 'PASS: SQL and client failures stop without retry\n'
test_stream_limits_stop_fail_closed
printf 'PASS: stream limits stop fail-closed\n'
