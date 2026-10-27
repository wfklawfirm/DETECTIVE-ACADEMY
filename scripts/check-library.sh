#!/usr/bin/env bash
# Authoritative fair-play check (ASP/clingo) from the research library. Needs: python3 + `pip install clingo`.
set -u
rc=0
for f in content/cases/*.json; do
  case "$f" in *.ui.json|*.scoring.json) continue;; esac
  out=$(python3 -I tools/library/13_CASE_DESIGN_REFERENCE/tools/check_case.py "$f" --json 2>&1) || rc=1
  echo "$out" | python3 -c "import sys,json
t=sys.stdin.read()
try:
  d=json.loads(t); print('$f', d.get('result'), 'publish_gate=',d.get('publish_gate'))
except Exception: print('$f ERROR', t[-300:])"
done
exit $rc
