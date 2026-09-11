#!/usr/bin/env python3
"""Q10.2h catalog audit; no routine calls, raw files, or production mutations."""

import configparser
import json
from pathlib import Path
import runpy
import secrets
import subprocess
import sys

from definer_audit import MAX_BYTES, need, reject_duplicates, summarize

BASE = runpy.run_path(str(Path(__file__).with_name("check-public-definers.py")))
HELPERS = {"lo_create", "lo_creat", "lo_from_bytea", "lo_put", "lo_import",
           "lo_unlink", "lowrite", "lo_truncate", "lo_truncate64"}
PHASE = "initialization"

DEPENDENCIES = """
, edges AS MATERIALIZED (
  SELECT DISTINCT d.refclassid AS parent_class, d.refobjid AS parent_oid,
    CASE WHEN d.classid='pg_rewrite'::regclass THEN 'pg_class'::regclass
      ELSE d.classid END AS child_class,
    CASE WHEN d.classid='pg_rewrite'::regclass THEN rw.ev_class
      ELSE d.objid END AS child_oid
  FROM pg_depend d LEFT JOIN pg_rewrite rw
    ON d.classid='pg_rewrite'::regclass AND rw.oid=d.objid
  WHERE d.refclassid IN ('pg_proc'::regclass,'pg_class'::regclass)
    AND d.classid IN ('pg_proc'::regclass,'pg_rewrite'::regclass)
), walk(classid, oid, depth) AS (
  SELECT 'pg_proc'::regclass::oid, oid, 0 FROM bounded
  UNION
  SELECT e.child_class, e.child_oid, w.depth+1
  FROM walk w JOIN edges e ON e.parent_class=w.classid AND e.parent_oid=w.oid
  WHERE w.depth<4 AND NOT(e.child_class=w.classid AND e.child_oid=w.oid)
), nodes AS MATERIALIZED (
  SELECT classid, oid, min(depth) AS depth FROM walk
  GROUP BY classid,oid HAVING min(depth)>0
), node_rows AS (
  SELECT n.oid::bigint AS oid, n.depth,
    CASE WHEN n.classid='pg_proc'::regclass THEN 'routine' ELSE 'relation' END AS class,
    CASE WHEN n.classid='pg_proc'::regclass THEN p.prokind::text ELSE c.relkind::text END AS kind,
    EXISTS(SELECT 1 FROM aclexplode(COALESCE(ns.nspacl,acldefault('n',ns.nspowner))) a
      WHERE a.grantee=0 AND a.privilege_type='USAGE') AS public_lookup,
    CASE WHEN n.classid='pg_proc'::regclass THEN
      EXISTS(SELECT 1 FROM aclexplode(COALESCE(p.proacl,acldefault('f',p.proowner))) a
        WHERE a.grantee=0 AND a.privilege_type='EXECUTE')
    ELSE
      EXISTS(SELECT 1 FROM aclexplode(COALESCE(c.relacl,acldefault('r',c.relowner))) a
        WHERE a.grantee=0 AND a.privilege_type='SELECT')
      OR EXISTS(SELECT 1 FROM pg_attribute at, LATERAL aclexplode(at.attacl) a
        WHERE at.attrelid=c.oid AND at.attnum>0 AND NOT at.attisdropped
          AND a.grantee=0 AND a.privilege_type='SELECT')
    END AS public_access
  FROM nodes n
  LEFT JOIN pg_proc p ON n.classid='pg_proc'::regclass AND p.oid=n.oid
  LEFT JOIN pg_class c ON n.classid='pg_class'::regclass AND c.oid=n.oid
  JOIN pg_namespace ns ON ns.oid=COALESCE(p.pronamespace,c.relnamespace)
  WHERE (SELECT count(*) FROM nodes)<=256 ORDER BY n.classid,n.oid LIMIT 256
)
"""

EXTRA = """
, 'paths', json_build_object(
  'total', (SELECT count(*) FROM nodes),
  'frontier_count', (SELECT count(*) FROM nodes WHERE depth=4),
  'other_root_dependency_count', (SELECT count(*) FROM pg_depend d
    WHERE d.refclassid='pg_proc'::regclass AND d.refobjid IN (SELECT oid FROM bounded)
      AND d.classid NOT IN ('pg_proc'::regclass,'pg_rewrite'::regclass)),
  'nodes', COALESCE((SELECT json_agg(row_to_json(n)) FROM node_rows n),'[]'::json)),
 'helpers', COALESCE((SELECT json_agg(json_build_object(
   'name', p.proname, 'oid', p.oid::bigint, 'security_definer', p.prosecdef,
   'public_execute', EXISTS(SELECT 1 FROM aclexplode(COALESCE(p.proacl,
     acldefault('f',p.proowner))) a WHERE a.grantee=0 AND a.privilege_type='EXECUTE'),
   'public_lookup', EXISTS(SELECT 1 FROM aclexplode(COALESCE(n.nspacl,
     acldefault('n',n.nspowner))) a WHERE a.grantee=0 AND a.privilege_type='USAGE')
 ) ORDER BY p.oid) FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace
 WHERE n.nspname='pg_catalog' AND p.proname IN
 ('lo_create','lo_creat','lo_from_bytea','lo_put','lo_import','lo_unlink',
  'lowrite','lo_truncate','lo_truncate64')), '[]'::json)
"""


def make_query():
    source = BASE["QUERY"]
    lookup_filter = """    AND EXISTS (SELECT 1 FROM aclexplode(COALESCE(n.nspacl,
      acldefault('n',n.nspowner))) a
      WHERE a.grantee=0 AND a.privilege_type='USAGE')
"""
    need(source.count(lookup_filter) == 1)
    source = source.replace(lookup_filter, "").replace("<=256", "=2")
    source = source.replace("WITH selected", "WITH RECURSIVE selected", 1)
    head, body = source.split("\nSELECT json_build_object(", 1)
    need(body.endswith(";\nROLLBACK;\n"))
    body = "SELECT json_build_object(" + body.removesuffix(";\nROLLBACK;\n")
    return head + DEPENDENCIES + "\nSELECT json_build_object('audit', (" + body + ")" + EXTRA + ");\nROLLBACK;\n"


QUERY = make_query()


def count(value, maximum):
    need(type(value) is int and 0 <= value <= maximum)
    return value


def summarize_extended(payload, token):
    global PHASE
    PHASE = "json"
    need(len(payload) <= MAX_BYTES)
    doc = json.loads(payload, object_pairs_hook=reject_duplicates)
    PHASE = "envelope"
    need(isinstance(doc, dict) and set(doc) == {"audit", "paths", "helpers"})
    audit = doc["audit"]
    PHASE = "root_scope"
    need(isinstance(audit, dict) and audit.get("total_count") == 2)
    PHASE = "roots"
    result = summarize(json.dumps(audit).encode(), token)
    result["scope"] = "Q10.2h: two PUBLIC definers, bounded catalog dependencies, named helper ACLs"
    PHASE = "paths"
    paths = doc["paths"]
    need(isinstance(paths, dict) and set(paths) ==
         {"total", "frontier_count", "other_root_dependency_count", "nodes"})
    total = count(paths["total"], 256)
    frontier = count(paths["frontier_count"], total)
    others = count(paths["other_root_dependency_count"], 2**32-1)
    need(isinstance(paths["nodes"], list) and len(paths["nodes"]) == total)
    nodes, seen = [], set()
    for i, node in enumerate(paths["nodes"], 1):
        need(isinstance(node, dict) and set(node) ==
             {"oid", "class", "kind", "depth", "public_lookup", "public_access"})
        oid = count(node["oid"], 2**32-1)
        need(oid > 0 and node["class"] in {"routine", "relation"})
        need(node["kind"] in ({"f", "p", "w"} if node["class"] == "routine"
                             else {"r", "p", "v", "m", "f"}))
        depth = count(node["depth"], 4)
        need(depth > 0 and (node["class"], oid) not in seen)
        seen.add((node["class"], oid))
        need(type(node["public_lookup"]) is bool and type(node["public_access"]) is bool)
        nodes.append({"alias": f"D{i:03d}", **node})
    PHASE = "helpers"
    helpers, helper_oids = [], set()
    need(isinstance(doc["helpers"], list) and len(doc["helpers"]) <= 32)
    for helper in doc["helpers"]:
        need(isinstance(helper, dict) and set(helper) ==
             {"name", "oid", "public_execute", "public_lookup", "security_definer"})
        need(helper["name"] in HELPERS)
        oid = count(helper["oid"], 2**32-1)
        need(oid > 0 and oid not in helper_oids)
        helper_oids.add(oid)
        for key in ("public_execute", "public_lookup", "security_definer"):
            need(type(helper[key]) is bool)
        helpers.append(dict(helper))
    result["paths"] = {"status": "CATALOG_ONLY_INCOMPLETE", "count": total,
                       "frontier_count": frontier, "other_root_dependency_count": others,
                       "nodes": nodes}
    result["helpers"] = helpers
    result["missing_helper_names"] = sorted(HELPERS - {h["name"] for h in helpers})
    result["limitations"] += [
        "two-root count binding does not establish identity continuity across snapshots",
        "dependent nodes and minimum depth are reported without edges or root attribution",
        "catalog dependencies omit dynamic SQL and many string-body calls",
        "incoming routine/view paths stop after four levels; other dependency kinds are not traversed",
        "PUBLIC ACLs do not identify required consumers or prove absence of effective role access",
        "helper ACLs establish permission only, not production execution or all possible write paths",
    ]
    return result


def main():
    global PHASE
    if len(sys.argv) == 3 and sys.argv[1] == "--validate-stdin":
        report = summarize_extended(sys.stdin.buffer.read(MAX_BYTES+1), sys.argv[2])
    else:
        need(sys.argv[1:] == ["--approved-read-only-public-paths"])
        PHASE = "binding"
        bootstrap = runpy.run_path(str(Path(__file__).with_name("check-role-bootstrap.py")))
        command, env = bootstrap["connection_parameters"]()
        token = secrets.token_hex(16)
        command += ["-v", "audit_token=" + token]
        env["PGAPPNAME"] = "dino-public-paths-readonly"
        PHASE = "query"
        try:
            payload = BASE["collect"](command, env, QUERY, diagnose=True)
        except ValueError as error:
            if str(error).removeprefix("audit failure ") in BASE["ERROR_CLASSES"]:
                PHASE = "query_" + str(error).removeprefix("audit failure ")
            raise
        report = summarize_extended(payload, token)
        report["connections"] = 1
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, TypeError, KeyError, UnicodeError, RecursionError,
            OSError, configparser.Error, subprocess.TimeoutExpired, KeyboardInterrupt):
        print(f"STOP: extended audit rejected at {PHASE}; no raw output or retry", file=sys.stderr)
        raise SystemExit(1) from None
