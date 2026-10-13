# Research workbench — start here

These documents are on your local Mac. No SSH is needed to read them.

- [Simple walkthrough](WALKTHROUGH.md): what is happening, why it matters and what we can pitch.
- [Progress checklist](tasks/todo.md): completed checks and remaining tasks.
- [Implementation plan](tasks/plan.md): how we finish the experiment.
- [Open-source evaluator](evaluation/README.md): how the fixed-model comparison runs.
- [Recovered cloud outputs](cloud-artifacts/): original, compressed document, raw agent notes and manifest.

Current setup: OpenCode 1.18.27 runs on our DigitalOcean Droplet and calls serverless inference through router:general for operational work. The repository now also has a fixed-model evaluator for DeepSeek or another catalog model. SSH and agent file tools work. The original source matches our local input exactly. The first compressed document is 41.84% smaller in bytes, with date omissions recorded in the manifest. No paid benchmark has run; token, cost and answer-quality results remain unknown.

Next: confirm the exact DeepSeek model slug and key scope, run one bounded fixed-model comparison, inspect its JSON, then optionally use DigitalOcean native Evaluations for a second judge view. The walkthrough and checklist are the current progress records.

## Earlier local practice runner

The instructions below describe the preserved Python practice script, not the current Droplet workflow. Running it launches additional paid model calls; it is not required for our next step.

First slice of a researcher workbench: original context versus model-generated compressed context. This is not LLMLingua or KVPress. No dependencies beyond Python 3.

## Practice

1. In DigitalOcean, open Model Catalog/Serverless Inference. Select an inexpensive text model supporting Chat Completions; copy its exact model ID and review input/output rates.
2. Create a model access key. Keep it out of chat, files, and version control.
3. From this directory, run `python3 -m unittest -v` for the offline checks (no spending).
4. Run `python3 experiment.py --model YOUR_MODEL_ID`. It asks for the key with hidden input. Alternatively set GRADIENT_MODEL_ACCESS_KEY securely in your local environment.
5. Review result.json: answers, references, returned token usage and wall time. The sample performs seven calls: one compression and two answers for each of three questions. Maximum five questions and 12,000 source characters. Limits bound requests, not dollars.

Use a new --output filename for subsequent runs. No automatic retries. Charges incurred before a failed run remain payable. API responses, including original/compressed text, are exported locally; only use data approved for cloud processing.

## Interpreting results

Compare correctness manually before interpreting token savings. Include compression usage and time in total overhead. For prices I/O per million tokens, calculate each response cost as (prompt_tokens * I + completion_tokens * O) / 1,000,000; use current model rates and account billing, including any caching-specific rates. Original versus compressed requests execute sequentially, once; latency is illustrative, not a rigorous performance benchmark. Compression is not guaranteed to shorten text or retain facts. Temperature zero does not guarantee deterministic answers.

## AI-native cloud progression

Now: DigitalOcean serverless inference runs compression and answer generation; this script coordinates a fixed experiment locally.
Next: App Platform hosts a browser interface and backend with the key kept server-side. A managed agent can prepare a validated experiment configuration and explain results through bounded tools. Keep benchmark model selection fixed: routing between different models would confound a compression comparison. Store exports in Spaces only when hosted persistence is needed.

No managed agent, GPU provisioning, hosted UI or deployment exists in this first slice. Knowledge bases and multiple agents are unnecessary for the fixed dataset experiment.
