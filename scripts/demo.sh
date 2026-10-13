#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
remote=root@134.209.114.233
mode=${1:-}
case "$mode" in
  ''|--prepare|--watch) ;;
  *) printf 'Usage: bash scripts/demo.sh [--prepare|--watch]\n' >&2; exit 2 ;;
esac
if [[ "$mode" == --watch ]]; then
  mkdir -p evaluation/results
  printf 'Watching cloud research evidence. Open http://localhost:7777/#workflow\nPress Ctrl+C to stop. This mode does not start an experiment.\n'
  while true; do
    rsync -az -e 'ssh -o ConnectTimeout=8 -o ServerAliveInterval=10 -o ServerAliveCountMax=2' \
      --include='/llmlingua-*/' --include='/llmlingua-*/*' --exclude='*' \
      "$remote:/root/research-workbench/evaluation/results/" evaluation/results/ \
      || printf 'Cloud sync failed; retrying in five seconds.\n' >&2
    sleep 5
  done
fi
run="llmlingua-$(date -u +%Y%m%dT%H%M%SZ)"
scp evaluation/workflow.py evaluation/run_eval.py evaluation/riverwatch-eval.jsonl "$remote:/root/research-workbench/evaluation/"
ssh "$remote" 'mkdir -p /root/research-workbench/research-inputs'
scp research-inputs/original.txt "$remote:/root/research-workbench/research-inputs/"
if [[ "$mode" == --prepare ]]; then
  printf 'Updated cloud research recipe. No inference calls started.\n'
  exit 0
fi
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
status=0
ssh "$remote" "cd /root/research-workbench && .venv-llmlingua/bin/python evaluation/workflow.py --output evaluation/results/$run" || status=$?
# Bring the terminal error event back too; a failed experiment must not look live forever.
rsync -az "$remote:/root/research-workbench/evaluation/results/$run/" "evaluation/results/$run/" || status=$?
printf '\nRun: %s\nLive workflow: http://localhost:7777/#workflow\n' "$run"
exit "$status"
