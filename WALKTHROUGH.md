# What we are building, in simple words

“A small research lab can give a cloud agent its documents, ask it to prepare an experiment, and check the results using DigitalOcean's evaluation tools. The model runs through a managed API instead of a lab-owned model server.”

## Our example

A fictional lab compares two water sensors. Its notebook contains an early recommendation, a later correction, an exception and a conditional deadline. We ask the agent to shorten the notebook. Then we ask the same five questions using the long and short versions. We want to see whether the shorter document still supports the right answers.

## Who does what

- The Droplet is our rented cloud computer.
- OpenCode is the assistant running on it. It reads and writes the experiment files.
- Serverless inference supplies the model; we do not load model weights onto the Droplet.
- router:general chooses a model for the assistant's operational requests. Savings are not yet measured.
- The repository evaluator sends the same questions to both archives through one fixed model. DigitalOcean native Evaluations can provide an optional second judge view.
- We supply the research recipe, human references and review of the evidence.

## What has happened

1. Created a Droplet and configured OpenCode's DigitalOcean model access.
2. Connected router:general and received a real response.
3. Asked the agent to create hello.txt and read it back. Both file tools succeeded.
4. Loaded a synthetic research document without its held-out answer key.
5. The agent created compressed.txt and compression-notes.md.
6. Switched from the browser console to SSH. SSH now works. OpenCode lives at /root/.opencode/bin/opencode, so remote commands should use that full path.
7. Ran one short text-only request through `digitalocean/deepseek-v4.1-flash`; it returned the expected response. This verifies model access, not research quality.
8. Ran the fixed-model evaluator against all five questions for both archives. It measured 4,359 versus 3,124 candidate prompt tokens: 28.33% fewer tokens for the compressed archive. We manually reviewed the answers; the compressed answer to the low-turbidity question kept the decision but omitted supporting numbers. The full evidence report is in `evaluation/results/REPORT.md`.

## Where we are now

The original matches the prepared source exactly. The compressed document is 2,177 bytes versus 3,743 bytes: 41.84% smaller in bytes. The fixed DeepSeek comparison measured 28.33% fewer candidate prompt tokens, but the compressed run used more completion tokens and was slightly slower in this single trial. It retains the important measurements and purchasing conditions, but drops the record date and initial-entry date. Its notes wrongly call the record date invented; that date really exists in the source. We preserved this first run and recorded the limitation. Native evaluations have not run yet.

## What is now ready

`evaluation/run_eval.py` is the open-source benchmark. It keeps the operational router and research candidate separate: OpenCode may use `router:general`, while the benchmark must use one exact model ID, such as the DeepSeek Flash slug shown in the Model Catalog. It records raw answers, API token usage, latency, prompt-token reduction and transparent reference-marker checks. Its tests run offline, so they spend no credits.

## What comes next

DigitalOcean Analyze now visibly shows real account telemetry: 10,068 input and 13,259 output tokens over the last seven days. A recent DeepSeek card shows 2,859 input and 3,158 output tokens. These are dashboard/account observations, not exclusively our benchmark. The observation is saved in `evaluation/results/digitalocean-observability.json`; no native judge evaluation has run.

Future evaluator exports now include exact submitted messages, source SHA-256 hashes, UTC submission timestamps, provider model/response IDs, and a request ID when returned. Old results retain their original evidence and cannot retrospectively acquire missing IDs.

Verify the account's actual usage and price → optionally compare in native Evaluations → decide whether a stronger semantic judge is needed → explain what was preserved or lost and what the calls actually cost.

## What we can honestly pitch today

“Our cloud agent is connected and can work with files. It prepared a compressed research archive and ran a fixed DeepSeek comparison. The shorter archive used 28.33% fewer candidate prompt tokens, while manual review exposed the evidence detail it dropped.”

This is a Droplet prototype: we still manage the server. The study is fictional. We have not proved lower total cost or equal answer quality, and the metric proxy is not a semantic judge.

Update this file after each verified milestone. Keep planned steps and observed results separate.

## Decision after checking the original plan

We are keeping the original research workflow. Only hosting changed: OpenCode on a Droplet replaces the managed microVM. The fixed-model evaluator is now the reproducible GitHub artifact; native Evaluations remain optional DigitalOcean evidence. We still need to verify the exact model slug, key scope, deployed server price and router policy. We do not need another router or more infrastructure.
