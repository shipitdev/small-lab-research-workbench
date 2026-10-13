#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
remote=root@134.209.114.233
run="llmlingua-$(date -u +%Y%m%dT%H%M%SZ)"
scp evaluation/workflow.py evaluation/run_eval.py evaluation/riverwatch-eval.jsonl "$remote:/root/research-workbench/evaluation/"
ssh "$remote" 'mkdir -p /root/research-workbench/research-inputs'
scp research-inputs/original.txt "$remote:/root/research-workbench/research-inputs/"
mkdir -p "evaluation/results/$run"
# Only this run's synthetic evidence is synced. Keys and other server files stay remote.
(
  while true; do
    rsync -az "$remote:/root/research-workbench/evaluation/results/$run/" "evaluation/results/$run/" 2>/dev/null || true
    sleep 5
  done
) &
sync_pid=$!
trap 'kill "$sync_pid" 2>/dev/null || true' EXIT
ssh "$remote" "cd /root/research-workbench && .venv-llmlingua/bin/python evaluation/workflow.py --output evaluation/results/$run"
rsync -az "$remote:/root/research-workbench/evaluation/results/$run/" "evaluation/results/$run/"
printf '\nEvidence ready: %s\nDashboard: http://localhost:7777\n' "$run"
