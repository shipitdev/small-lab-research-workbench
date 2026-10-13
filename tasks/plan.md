# Implementation plan: cloud research workbench

Updated 13 October 2026. Tasks and completion evidence live in todo.md. The simple explanation lives in ../WALKTHROUGH.md.

## Goal

Give a small research team a cloud agent that prepares a reproducible experiment: shorten a research archive, then check whether answers from the shorter archive retain the important evidence. This demonstrates a workflow, not scientific validation of compression.

## Current architecture

Mac → SSH → OpenCode on one DigitalOcean Droplet → DigitalOcean serverless inference via router:general for agent work. A repository-owned evaluator calls one fixed model ID for the measured comparison.

Native DigitalOcean Evaluations can separately compare original and compressed documents, using a fixed candidate and judge. They are optional platform evidence; the repository evaluator is the reproducible project artifact. The research agent receives real exports afterward to help write the report.

The user chose the Marketplace Droplet. This supersedes the earlier Hermes/Harness Runtime plan. We manage this server; do not pitch it as fully infrastructure-free. No GPU, custom UI, database or second agent is required.

## Context audit — 13 October 2026

The original flow is preserved: research request → agent prepares files → native evaluation → manual failure inspection → agent report → local exports. Deployment changed to OpenCode on a Droplet. Archive review found two date omissions and a mistaken integrity note; keep these visible. Check actual hosting balance/size and router policy before promising cost optimization. Native Evaluations is next, not another hosting migration.

## Ordered work

1. Recover the existing workspace over SSH. Verify binary location, completed processes and files before restarting anything.
2. Check source integrity against the local original. Preserve every recovered artifact. Inspect compression for losses, unsupported claims and missing dates. Repair input transfer and regenerate only if needed, retaining the first run as evidence.
3. Freeze the source versions and save hashes, actual configuration identifiers, notes and any available usage. Never export credentials. Character/byte savings are not model-token savings.
4. Confirm the exact fixed DeepSeek model slug and key scope. Run the repository evaluator once with identical questions and generation settings. Keep router:general for operational tasks, but disable dynamic routing in the measured comparison.
5. Optionally prepare the five held-out references for native Evaluations. If used, run Original and Compressed with identical questions, answer instructions, candidate, judge, generation settings, metric and threshold. Prefer Ground Truth Faithfulness with references. Export raw answers/results and manually inspect critical facts.
6. Write a short report and demo walkthrough from observed results. Separate compression overhead, candidate usage and judging cost. Export artifacts before removing resources; destroying the Droplet stops its compute billing, powering it off does not.

## Checkpoints

- Workspace: SSH and inference work; actual file tools work; no duplicate agent job.
- Inputs: verified original and frozen compressed version; no reference-answer leakage.
- Evaluation: source is the only intentional difference; real results and configuration are preserved.
- Demo: every claim has evidence; limitations and missing measurements are clear.

## Risks and decisions

| Risk | Response |
| --- | --- |
| Web-console transfer altered source | Compare exact bytes before using the first compression run |
| Router selects expensive models | Bound calls; inspect native usage; do not promise guaranteed savings |
| Agent mislabels information as invented | Compare its output with source manually |
| Native Evaluations access/schema unknown | Inspect official docs and account; never invent uploader fields |
| Tiny fictional dataset | Label synthetic; show workflow, not general accuracy |
| Agent runs as root | Use only approved synthetic files; avoid arbitrary installs or unrelated paths |
| Credentials in configuration | Read/export only explicitly non-secret fields |

No resources will be destroyed as part of this plan without a separate instruction. No account credit balance or router policy has been verified.
