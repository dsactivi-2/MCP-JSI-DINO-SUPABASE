#!/bin/bash

set -euo pipefail

readonly GATE_ID='DISCOVERY-GATE-B1-V3-RO-2026-09-12'
readonly TARGET_ALIAS='dino_crm_discovery_ro_v1'
readonly REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)"
readonly LAUNCHER_PATH="${REPO_ROOT}/scripts/discovery/run-gate-b1-v3-ro.sh"
readonly PROD_SQL_PATH="${REPO_ROOT}/docs/discovery/sql/00-identity-and-privilege-gate-b1-v2.sql"
readonly PROD_SQL_SHA256='0f586d02a663f9df543a7b7c1b8efde876c2b96d6079cd79e02c3a7359710317'
readonly PROD_CONFIG_ROOT='/Users/activi/Library/Application Support/Activi/discovery-targets'
readonly PROD_TARGET_ATTEST="${PROD_CONFIG_ROOT}/${TARGET_ALIAS}.target"
readonly PROD_APPROVAL_ATTEST="${PROD_CONFIG_ROOT}/${TARGET_ALIAS}.approval"
readonly PROD_SERVICE_FILE="${PROD_CONFIG_ROOT}/${TARGET_ALIAS}.pg_service.conf"
readonly PROD_CREDENTIAL_FILE="${PROD_CONFIG_ROOT}/${TARGET_ALIAS}.pgpass"
readonly PROD_RAW_PARENT='/Users/activi/Library/Application Support/Activi/discovery-raw/dino_crm_discovery_target_01'
readonly PROD_PSQL='/opt/homebrew/bin/psql'
readonly PYTHON_BIN='/opt/homebrew/bin/python3'
readonly STREAM_GUARD="${REPO_ROOT}/scripts/discovery/gate_b1_stream_guard.py"
readonly STREAM_GUARD_SHA256='b3c4fbe8053641ef93e70c126dbc7e5fe10892af3cc41743e5c7c9c0ce5252b7'
readonly WINDOW_SECONDS=1800
readonly RETENTION_SECONDS=86400
LOCK_DIR=''
EXPECTED_UID="$(id -u)"

stop() {
  printf 'STOP: %s\n' "$1" >&2
  exit 1
}

cleanup_lock() {
  if [[ -n "${LOCK_DIR}" ]]; then
    rmdir "${LOCK_DIR}" 2>/dev/null || true
  fi
}

read_config_value() {
  local file="$1" wanted_section="$2" wanted_key="$3" source_label="$4"
  local line section='' key value found=''

  while IFS= read -r line || [[ -n "${line}" ]]; do
    [[ -n "${line}" && "${line}" != \#* && "${line}" != \;* ]] || continue
    if [[ -n "${wanted_section}" && "${line}" == \[*\] ]]; then
      section="${line#\[}"
      section="${section%\]}"
      continue
    fi
    [[ -z "${wanted_section}" || "${section}" == "${wanted_section}" ]] || continue
    [[ "${line}" == *=* ]] || continue
    key="${line%%=*}"
    value="${line#*=}"
    if [[ "${key}" == "${wanted_key}" ]]; then
      [[ -z "${found}" ]] || stop "duplicate ${source_label} key"
      found="${value}"
    fi
  done <"${file}"

  [[ -n "${found}" ]] || stop "missing ${source_label} key"
  printf '%s' "${found}"
}

read_attest_value() {
  read_config_value "$1" '' "$2" 'attestation'
}

validate_kv_schema() {
  local file="$1" label="$2" allowed_keys="$3"
  local line key seen='|'

  while IFS= read -r line || [[ -n "${line}" ]]; do
    [[ -n "${line}" && "${line}" != \#* ]] || continue
    [[ "${line}" == *=* ]] || stop "${label} schema invalid"
    key="${line%%=*}"
    [[ "${key}" =~ ^[a-z][a-z0-9_]*$ ]] || stop "${label} schema invalid"
    case "|${allowed_keys}|" in
      *"|${key}|"*) ;;
      *) stop "${label} schema invalid" ;;
    esac
    case "${seen}" in
      *"|${key}|"*) stop "${label} schema invalid" ;;
    esac
    seen="${seen}${key}|"
  done <"${file}"
}

validate_service_schema() {
  local file="$1" line section_count=0 section='' key seen='|'
  local allowed_keys='host|dbname|user|sslmode|connect_timeout'

  while IFS= read -r line || [[ -n "${line}" ]]; do
    [[ -n "${line}" && "${line}" != \#* && "${line}" != \;* ]] || continue
    if [[ "${line}" == \[*\] ]]; then
      section="${line#\[}"
      section="${section%\]}"
      section_count=$((section_count + 1))
      [[ "${section}" == "${TARGET_ALIAS}" && ${section_count} -eq 1 ]] || stop 'connection service schema invalid'
      continue
    fi
    [[ "${section}" == "${TARGET_ALIAS}" && "${line}" == *=* ]] || stop 'connection service schema invalid'
    key="${line%%=*}"
    case "|${allowed_keys}|" in
      *"|${key}|"*) ;;
      *) stop 'connection service schema invalid' ;;
    esac
    case "${seen}" in
      *"|${key}|"*) stop 'connection service schema invalid' ;;
    esac
    seen="${seen}${key}|"
  done <"${file}"
  [[ ${section_count} -eq 1 ]] || stop 'connection service schema invalid'
}

file_mode() {
  stat -f '%Lp' "$1"
}

file_owner() {
  stat -f '%u' "$1"
}

validate_secure_file() {
  local file="$1" label="$2" file_dir physical_dir

  [[ "${file}" == /* && -f "${file}" && ! -L "${file}" ]] || stop "${label} invalid"
  file_dir="$(dirname "${file}")"
  physical_dir="$(cd "${file_dir}" && pwd -P)"
  [[ "${physical_dir}/$(basename "${file}")" == "${file}" ]] || stop "${label} uses symlink path"
  [[ "$(file_owner "${file}")" == "${EXPECTED_UID}" ]] || stop "${label} owner mismatch"
  [[ "$(file_mode "${file}")" == '600' ]] || stop "${label} mode mismatch"
}

read_service_value() {
  read_config_value "$1" "$2" "$3" 'connection service'
}

main() {
  local sql_path approval_path target_attest service_file credential_file
  local raw_parent raw_dir psql_bin test_mode='false'
  local expected_hash actual_hash hash_record approval_status approval_gate approval_alias
  local expected_launcher_hash launcher_hash_record launcher_hash
  local expected_stream_guard_hash
  local window_start window_end now retention_authorized retention_seconds
  local target_alias target_service expected_database expected_fingerprint
  local service_host service_database service_user service_sslmode service_timeout
  local normalized_host fingerprint_record actual_fingerprint
  local stream_guard_hash_record stream_guard_hash
  local launcher_timeout=60

  if [[ "${1:-}" == '--test-mode' && $# -eq 1 ]]; then
    test_mode='true'
    [[ -n "${GATE_B1_TEST_ROOT:-}" ]] || stop 'test root missing'
    [[ "${GATE_B1_TEST_ROOT}" == /* ]] || stop 'test root must be absolute'
    [[ "$(cd "${GATE_B1_TEST_ROOT}" && pwd -P)" == "${GATE_B1_TEST_ROOT}" ]] || stop 'test root uses symlink path'
    sql_path="${GATE_B1_TEST_ROOT}/sql/gate-b1.sql"
    approval_path="${GATE_B1_TEST_ROOT}/config/approval.attest"
    target_attest="${GATE_B1_TEST_ROOT}/config/target.attest"
    service_file="${GATE_B1_TEST_ROOT}/config/pg_service.conf"
    credential_file="${GATE_B1_TEST_ROOT}/config/pgpass"
    raw_parent="${GATE_B1_TEST_ROOT}/raw"
    psql_bin="${GATE_B1_TEST_ROOT}/bin/fake-psql"
    now="${GATE_B1_NOW_EPOCH:-}"
    launcher_timeout="${GATE_B1_TEST_TIMEOUT_SECONDS:-60}"
    EXPECTED_UID="${GATE_B1_TEST_EXPECTED_UID:-${EXPECTED_UID}}"
  elif [[ $# -eq 0 ]]; then
    sql_path="${PROD_SQL_PATH}"
    approval_path="${PROD_APPROVAL_ATTEST}"
    target_attest="${PROD_TARGET_ATTEST}"
    service_file="${PROD_SERVICE_FILE}"
    credential_file="${PROD_CREDENTIAL_FILE}"
    raw_parent="${PROD_RAW_PARENT}"
    psql_bin="${PROD_PSQL}"
    now="$(date +%s)"
  else
    stop 'unsupported arguments'
  fi

  validate_secure_file "${approval_path}" 'approval attestation'
  validate_kv_schema \
    "${approval_path}" \
    'approval attestation' \
    'status|gate_id|target_alias|window_start_epoch|window_end_epoch|sql_sha256|launcher_sha256|stream_guard_sha256|retention_delete_authorized|retention_seconds'
  expected_hash="$(read_attest_value "${approval_path}" 'sql_sha256')"
  expected_launcher_hash="$(read_attest_value "${approval_path}" 'launcher_sha256')"
  expected_stream_guard_hash="$(read_attest_value "${approval_path}" 'stream_guard_sha256')"
  launcher_hash_record="$(shasum -a 256 "${LAUNCHER_PATH}")"
  launcher_hash="${launcher_hash_record%% *}"
  [[ "${launcher_hash}" == "${expected_launcher_hash}" ]] || stop 'launcher hash mismatch'
  [[ -f "${sql_path}" && ! -L "${sql_path}" ]] || stop 'SQL file invalid'
  hash_record="$(shasum -a 256 "${sql_path}")"
  actual_hash="${hash_record%% *}"
  [[ "${actual_hash}" == "${expected_hash}" ]] || stop 'SQL hash mismatch'
  if [[ "${test_mode}" == 'false' ]]; then
    [[ "${actual_hash}" == "${PROD_SQL_SHA256}" ]] || stop 'compiled SQL hash mismatch'
  fi

  validate_secure_file "${target_attest}" 'target attestation'
  validate_secure_file "${service_file}" 'connection service'
  validate_secure_file "${credential_file}" 'credential file'
  [[ -x "${psql_bin}" && -f "${psql_bin}" && ! -L "${psql_bin}" ]] || stop 'psql executable invalid'
  [[ -x "${PYTHON_BIN}" && -f "${PYTHON_BIN}" ]] || stop 'python runtime invalid'
  [[ -f "${STREAM_GUARD}" && ! -L "${STREAM_GUARD}" ]] || stop 'stream guard invalid'
  stream_guard_hash_record="$(shasum -a 256 "${STREAM_GUARD}")"
  stream_guard_hash="${stream_guard_hash_record%% *}"
  [[ "${stream_guard_hash}" == "${expected_stream_guard_hash}" ]] || stop 'approved stream guard hash mismatch'
  [[ "${stream_guard_hash}" == "${STREAM_GUARD_SHA256}" ]] || stop 'stream guard hash mismatch'

  validate_kv_schema \
    "${target_attest}" \
    'target attestation' \
    'target_alias|expected_database_name|target_fingerprint_sha256|connection_service|created_at_epoch|responsible_person'
  validate_service_schema "${service_file}"

  approval_status="$(read_attest_value "${approval_path}" 'status')"
  approval_gate="$(read_attest_value "${approval_path}" 'gate_id')"
  approval_alias="$(read_attest_value "${approval_path}" 'target_alias')"
  window_start="$(read_attest_value "${approval_path}" 'window_start_epoch')"
  window_end="$(read_attest_value "${approval_path}" 'window_end_epoch')"
  retention_authorized="$(read_attest_value "${approval_path}" 'retention_delete_authorized')"
  retention_seconds="$(read_attest_value "${approval_path}" 'retention_seconds')"

  [[ "${approval_status}" == 'GRANTED' ]] || stop 'approval not granted'
  [[ "${approval_gate}" == "${GATE_ID}" ]] || stop 'gate ID mismatch'
  [[ "${approval_alias}" == "${TARGET_ALIAS}" ]] || stop 'target alias mismatch'
  [[ "${window_start}" =~ ^[0-9]+$ && "${window_end}" =~ ^[0-9]+$ && "${now}" =~ ^[0-9]+$ ]] || stop 'invalid time window'
  [[ "${EXPECTED_UID}" =~ ^[0-9]+$ ]] || stop 'invalid expected owner'
  [[ "${launcher_timeout}" =~ ^[0-9]+$ ]] || stop 'invalid launcher timeout'
  (( launcher_timeout >= 1 && launcher_timeout <= 60 )) || stop 'invalid launcher timeout'
  (( window_end - window_start == WINDOW_SECONDS )) || stop 'invalid time window'
  (( now >= window_start && now < window_end )) || stop 'time window inactive'
  [[ "${retention_authorized}" == 'true' && "${retention_seconds}" == "${RETENTION_SECONDS}" ]] || stop 'retention not authorized'

  target_alias="$(read_attest_value "${target_attest}" 'target_alias')"
  expected_database="$(read_attest_value "${target_attest}" 'expected_database_name')"
  expected_fingerprint="$(read_attest_value "${target_attest}" 'target_fingerprint_sha256')"
  target_service="$(read_attest_value "${target_attest}" 'connection_service')"
  read_attest_value "${target_attest}" 'created_at_epoch' >/dev/null
  read_attest_value "${target_attest}" 'responsible_person' >/dev/null
  [[ "${target_alias}" == "${TARGET_ALIAS}" && "${target_service}" == "${TARGET_ALIAS}" ]] || stop 'target attestation mismatch'

  service_host="$(read_service_value "${service_file}" "${TARGET_ALIAS}" 'host')"
  service_database="$(read_service_value "${service_file}" "${TARGET_ALIAS}" 'dbname')"
  service_user="$(read_service_value "${service_file}" "${TARGET_ALIAS}" 'user')"
  service_sslmode="$(read_service_value "${service_file}" "${TARGET_ALIAS}" 'sslmode')"
  service_timeout="$(read_service_value "${service_file}" "${TARGET_ALIAS}" 'connect_timeout')"
  [[ -n "${service_user}" ]] || stop 'connection service identity missing'
  [[ "${service_host}" != *,* ]] || stop 'connection service host invalid'
  case "${service_sslmode}" in
    require|verify-ca|verify-full) ;;
    *) stop 'connection service TLS invalid' ;;
  esac
  [[ "${service_timeout}" == '5' ]] || stop 'connection service timeout invalid'
  [[ "${service_database}" == "${expected_database}" ]] || stop 'database attestation mismatch'
  normalized_host="$(printf '%s' "${service_host}" | LC_ALL=C tr '[:upper:]' '[:lower:]' | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
  fingerprint_record="$(printf '%s' "${normalized_host}" | shasum -a 256)"
  actual_fingerprint="${fingerprint_record%% *}"
  [[ "${actual_fingerprint}" == "${expected_fingerprint}" ]] || stop 'target fingerprint mismatch'

  [[ "${raw_parent}" == /* && -d "${raw_parent}" && ! -L "${raw_parent}" ]] || stop 'raw parent invalid'
  [[ "$(cd "${raw_parent}" && pwd -P)" == "${raw_parent}" ]] || stop 'raw parent uses symlink path'
  [[ "$(file_owner "${raw_parent}")" == "$(id -u)" ]] || stop 'raw parent owner mismatch'
  [[ "$(file_mode "${raw_parent}")" == '700' ]] || stop 'raw parent mode mismatch'
  [[ "${raw_parent}" != "${REPO_ROOT}" && "${raw_parent}" != "${REPO_ROOT}/"* ]] || stop 'raw path inside repository'

  raw_dir="${raw_parent}/${GATE_ID}"
  [[ ! -e "${raw_dir}" && ! -L "${raw_dir}" ]] || stop 'raw path already exists'
  LOCK_DIR="${approval_path}.lock"
  mkdir "${LOCK_DIR}" 2>/dev/null || stop 'discovery lock conflict'
  trap cleanup_lock EXIT HUP INT TERM

  mkdir -m 700 "${raw_dir}"
  [[ "$(file_owner "${raw_dir}")" == "$(id -u)" && "$(file_mode "${raw_dir}")" == '700' ]] || stop 'raw directory security mismatch'

  GATE_B1_EXPECTED_DATABASE_NAME="${expected_database}" \
  PGSERVICE="${TARGET_ALIAS}" \
  PGSERVICEFILE="${service_file}" \
  PGPASSFILE="${credential_file}" \
    "${PYTHON_BIN}" "${STREAM_GUARD}" \
      --psql "${psql_bin}" \
      --sql "${sql_path}" \
      --raw "${raw_dir}/gate-b1.out" \
      --manifest "${raw_dir}/gate-b1-manifest.json" \
      --gate-id "${GATE_ID}" \
      --target-alias "${TARGET_ALIAS}" \
      --sql-sha256 "${actual_hash}" \
      --window-end-epoch "${window_end}" \
      --timeout-seconds "${launcher_timeout}"

  printf 'PASS: Gate B1 launcher completed\n'
}

main "$@"
