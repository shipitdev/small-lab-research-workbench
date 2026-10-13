# Research workbench tasks

## 1. Recover workspace — complete
- [x] SSH connection succeeds.
- [x] Locate OpenCode: /root/.opencode/bin/opencode.
- [x] Confirm original, compressed and notes files exist; no active OpenCode job observed.
- [x] Backed up files locally; original matches prepared source byte for byte.

Verification: remote inventory, process list and byte comparison. Dependencies: none. Scope: recovered files and walkthrough.

## 2. Validate and freeze compression
- [x] Reviewed corrected numbers, units, subgroup exception, purchasing conditions and missing battery-life evidence.
- [x] No source-transfer discrepancy. Preserved the first run; record-date and initial-entry-date omissions disclosed.
- [x] Saved hashes in cloud-artifacts/manifest.json; underlying model, tokens, cost and quality scores remain unknown.

Verification: local comparison and manual source review. Dependency: 1. Scope: inputs, outputs and manifest.

## Checkpoint: reliable inputs
- [x] Cloud file tools verified; original intact; compressed output reviewed with omissions disclosed; held-out answers kept separate.

## 3. Prepare native evaluation
- [ ] Verify hosting-team balance, deployed Droplet size/rate and credit eligibility.
- [ ] Inspect router:general policy and request usage; record underlying model if available.
- [ ] Verify account access and current upload schema.
- [x] Mapped five questions/references into `evaluation/riverwatch-eval.jsonl`; preview is still pending manual upload.
- [x] Added `evaluation/run_eval.py` and offline tests for the open-source fixed-model comparison.
- [x] Confirmed `digitalocean/deepseek-v4.1-flash` with one short text-only OpenCode smoke test; no benchmark result inferred.
- [ ] Provide the evaluator process a scoped model access key without writing it to disk, then record settings and prices before the ten-call run.
- [ ] Record native candidate, judge, settings, reference-aware metric and prices if the dashboard run is used.

Verification: native dataset preview and configuration. Dependency: 2. Scope: evaluation dataset/settings.

## 4. Compare the two contexts
- [ ] Run `evaluation/run_eval.py` with one fixed DeepSeek model and the same settings for both contexts.
- [ ] Optionally run native Original and Compressed evaluations using the same settings.
- [ ] Export answers and results; manually check critical facts.
- [ ] Record actual usage where available; separate compression and judge costs.

Verification: real native exports and manual review. Dependency: 3. Scope: two runs and exports.

## Checkpoint: real evidence
- [ ] No fabricated scores; comparison changes only source context; missing fields marked unknown.

## 5. Prepare report and demo
- [ ] Write findings and limitations from real evidence.
- [ ] Update WALKTHROUGH.md and copy artifacts locally.
- [ ] Provide safe cleanup instructions without deleting resources.

Verification: every pitch claim traced to an artifact. Dependency: 4. Scope: report and walkthrough.
