#!/usr/bin/env bash
# Step 1: lock CRM source paths. Metadata only. Never read dump SQL bodies.
set -euo pipefail

CRM_ROOT="/Users/activi/Downloads/crm-master-3"
DUMP_FILE="/Users/activi/Downloads/crm-master-3/databaseDump/2024_10_28.sql"
DINO_ROOT="/Users/activi/Documents/ChatGPT/Dino problem baza crm"
REPORT="/private/tmp/dino-crm-step1-source-lock.txt"
STATUS_FILE="/private/tmp/dino-crm-step1-source-lock.status"

echo PASS > "$STATUS_FILE"

fail() {
  echo FAIL > "$STATUS_FILE"
}

{
  echo "step=1-source-lock"
  echo "started_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "crm_root=$CRM_ROOT"
  echo "dump_file=$DUMP_FILE"
  echo "dino_root=$DINO_ROOT"
  echo "report=$REPORT"
  echo "dump_sql_body=not_read"
  echo

  if [[ -d "$CRM_ROOT" ]]; then
    echo "crm_root_exists=yes"
  else
    echo "crm_root_exists=no"
    echo "MISSING_DIR $CRM_ROOT"
    fail
  fi

  if [[ -d "$CRM_ROOT/src/crm" ]]; then
    echo "src_crm_exists=yes"
  else
    echo "src_crm_exists=no"
    echo "MISSING_DIR $CRM_ROOT/src/crm"
    fail
  fi

  if [[ -d "$DINO_ROOT" ]]; then
    echo "dino_root_exists=yes"
  else
    echo "dino_root_exists=no"
    echo "MISSING_DIR $DINO_ROOT"
    fail
  fi

  echo
  echo "[search_files]"
  while IFS= read -r path; do
    if [[ -f "$path" ]]; then
      size=$(stat -f "%z" "$path")
      sha=$(shasum -a 256 "$path" | awk '{print $1}')
      echo "OK size=$size sha256=$sha path=$path"
    else
      echo "MISSING path=$path"
      fail
    fi
  done <<PATHS
$CRM_ROOT/src/crm/kandidati.php
$CRM_ROOT/src/crm/ssdata_search.php
$CRM_ROOT/src/crm/search.php
$CRM_ROOT/src/crm/bot_search.php
$CRM_ROOT/docker-compose.yml
PATHS

  echo
  echo "[filter_dir]"
  filter_dir="$CRM_ROOT/src/crm/components/Kandidati"
  if [[ -d "$filter_dir" ]]; then
    echo "filter_dir_exists=yes"
    while IFS= read -r path; do
      size=$(stat -f "%z" "$path")
      echo "OK size=$size path=$path"
    done < <(find "$filter_dir" -maxdepth 1 -type f | LC_ALL=C sort)
  else
    echo "filter_dir_exists=no"
    fail
  fi

  echo
  echo "[dump_metadata]"
  if [[ ! -e "$DUMP_FILE" ]]; then
    echo "dump_exists=no"
    fail
  elif [[ -L "$DUMP_FILE" ]]; then
    echo "dump_exists=yes"
    echo "dump_symlink=yes"
    echo "dump_symlink_is_blocked=yes"
    fail
  elif [[ ! -f "$DUMP_FILE" ]]; then
    echo "dump_exists=yes"
    echo "dump_regular_file=no"
    fail
  else
    dump_size=$(stat -f "%z" "$DUMP_FILE")
    dump_mode=$(stat -f "%Lp" "$DUMP_FILE")
    dump_sha=$(shasum -a 256 "$DUMP_FILE" | awk '{print $1}')
    dump_file_type=$(file -b "$DUMP_FILE")
    echo "dump_exists=yes"
    echo "dump_symlink=no"
    echo "dump_regular_file=yes"
    echo "dump_bytes=$dump_size"
    echo "dump_mode=$dump_mode"
    echo "dump_sha256=$dump_sha"
    echo "dump_file_type=$dump_file_type"
    echo "dump_locked_this_step=yes"
    if [[ "$dump_size" -lt 1000 ]]; then
      echo "dump_size_implausible=yes"
      fail
    fi
  fi

  echo
  echo "[git_isolation]"
  if git -C "$DINO_ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    if git -C "$DINO_ROOT" ls-files --error-unmatch "databaseDump/2024_10_28.sql" >/dev/null 2>&1; then
      echo "dump_tracked_in_dino=yes"
      fail
    else
      echo "dump_tracked_in_dino=no"
    fi
  else
    echo "dino_git=missing"
    fail
  fi

  echo
  echo "finished_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "result=$(cat "$STATUS_FILE")"
} > "$REPORT"

cat "$REPORT"
if [[ "$(cat "$STATUS_FILE")" != "PASS" ]]; then
  exit 1
fi

