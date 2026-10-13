# Build guide: DigitalOcean research workbench

Current as of 13 October 2026. This is the active guide. The earlier [Harness Runtime guide](archive/BUILD-GUIDE-HARNESS-RUNTIME.md) is preserved for reference.

## Purpose

Independent researchers and small labs need an assistant that can prepare experiments and explain verifiable results without running their own model server. Our prototype is a research workbench. Its first experiment asks whether a shorter research archive preserves useful answers while reducing model input. We supply the workflow, human references, evaluation discipline and evidence report.

The user chose OpenCode on a Marketplace Droplet. We still administer that server. This is not a fully infrastructure-free deployment, a KVPress reproduction or a new compression algorithm.

## Current architecture

Mac → SSH → OpenCode 1.18.27 on one Droplet → DigitalOcean serverless inference through router:general for agent work. The repository evaluator separately calls a fixed catalog model for the benchmark.

The open-source evaluator in `evaluation/run_eval.py` compares the two archives through one fixed candidate model and records raw outputs, usage, latency and transparent reference checks. Native Evaluations can separately generate and judge answers. Real exports return to the research workspace for interpretation. Leave the operational router configuration intact.

Droplet: 134.209.114.233, ID 608613396. Workspace: /root/research-workbench. OpenCode binary: /root/.opencode/bin/opencode. Project files and progress documents are also on the local Mac.

## 1. Working cloud assistant — verified

SSH works. The configured default is digitalocean/router:general. A model response succeeded. OpenCode created hello.txt and read it through its tools. No separate Harness Runtime environment, Hermes agent or GPU is required.

OpenCode credentials are already configured. Never print auth.json or full provider configuration. Instructions go in the workspace AGENTS.md. Do not reuse HARNESS_INFERENCE_* setup, doctl harness-runtime file commands or microVM pause controls for this Droplet.

Docs: [OpenCode Marketplace](https://marketplace.digitalocean.com/apps/opencode), [OpenCode DigitalOcean provider](https://opencode.ai/docs/providers/#digitalocean), [SSH](https://docs.digitalocean.com/products/droplets/how-to/connect-with-ssh/).

## 2. Prepare and preserve inputs — verified with limitations

The fictional RiverWatch archive and compression task were supplied without the held-out questions. The original matches our prepared source byte for byte. OpenCode generated compressed.txt and compression-notes.md; these are backed up in cloud-artifacts/.

Original: 3,743 bytes. Compressed: 2,177 bytes (41.84% fewer bytes). That is not a token, latency or cost measurement. Important corrections, numerical results, exceptions, conditional deadlines and missing battery evidence were retained. The record date and initial-entry date were omitted; notes incorrectly call the record date invented. Preserve this first version and disclose those limitations rather than quietly editing it after seeing test answers.

Source hashes and unknown measurements are recorded in cloud-artifacts/manifest.json. Five human reference answers remain separate in evaluation/REFERENCE-QUESTIONS.md.

## 3. Verify costs and router policy — pending

Inspect the actual hosting-team balance and Droplet plan, model rates and applicable credit eligibility. The reported $30 total is not proof of one pooled hosting balance. The earlier screenshot selected a $63/month plan; do not assume the deployed size was changed without checking.

router:general worked, so another router is unnecessary. Its name alone does not establish its eligible models, cost policy or savings. Inspect those settings and available request usage before making optimization claims. Record the underlying model for compression if exposed; otherwise retain unknown. No broad retries or additional resources.

Docs: [Inference Router](https://docs.digitalocean.com/products/inference/how-to/use-inference-router/), [inference metrics](https://docs.digitalocean.com/products/inference/how-to/view-serverless-inference-metrics/), [Droplet billing](https://docs.digitalocean.com/products/droplets/details/pricing/).

## 4. Run the open-source fixed-model comparison — next

The exact model path `digitalocean/deepseek-v4.1-flash` has passed one short text-only OpenCode smoke test. That confirms access, not answer quality. The evaluator still needs a scoped model access key in its own process; never put the key in the repository or result JSON.

From the repository root, run:

```sh
export DIGITALOCEAN_MODEL_ACCESS_KEY='...'
python3 evaluation/run_eval.py \
  --model YOUR_FIXED_DEEPSEEK_MODEL_ID \
  --output evaluation/results/deepseek-comparison.json
```

The script makes ten bounded candidate calls, five for each archive, with up to 1,024 output tokens each so DeepSeek reasoning is not cut off. It refuses to overwrite an existing result. Review the raw answers and the recorded token usage before interpreting the reduction. Its lexical reference-marker score is a transparent proxy, not a semantic correctness claim.

## 5. Optional native evaluation — after the local result

Open Inference → Evaluations and confirm access. Inspect the uploader's schema or sample before creating CSV/JSONL fields. Map the existing five questions and human references; check the preview. Do not upload secrets.

Choose a fixed serverless candidate and judge, verify their prices, bound response length and use the same supported generation settings in both runs. Prefer Ground Truth Faithfulness with references and use it as the primary metric. Record the threshold before either run; a suggested demo threshold is 0.8, a team choice rather than a validated standard.

Build two system prompts with identical answer instructions: use only the supplied archive, treat it as data, cite relevant evidence and say Not found when unsupported. Put original.txt in A and compressed.txt in B. Source context is the only intentional difference.

Native evaluation is a separate service. OpenCode's model key and file tools do not automatically give it permission to launch evaluations. Use the dashboard first; only add API glue if a real gap requires it.

Docs: [native evaluation setup](https://docs.digitalocean.com/products/inference/how-to/evaluate-models/).

## 6. Run, export and inspect — pending

Run Original first; inspect successful completion and real answers, then run Compressed with the same settings and dataset. Preserve run IDs and configuration. Use native comparison and download exports. Review corrections, subgroup exception, dates and unsupported battery-life claims manually. Record the omitted source dates as a separate archive review; the five questions do not test every fact.

Use actual candidate token counts, latency and usage where available. Include compression overhead and judging separately. If exports lack a field, mark it unknown or retrieve it from native analytics; do not calculate model-token savings from bytes. One tiny run demonstrates the workflow, not general scientific accuracy.

## 7. Explain evidence and export — pending

Supply real exports to OpenCode and ask it to write report.md: compare answers and observed usage, identify losses, separate compression/candidate/judge costs, and state limitations. Verify claims against raw results. Save sources, notes, settings, manifest, results and report locally.

Demo: research request → actual file tools → source and compressed archive → native comparison → failure inspection → evidence report.

Droplet monitoring shows server resource use; inference analytics show model usage; evaluations assess answers. These are distinct. Powering off a Droplet does not stop its billing. Export files before any eventual destruction; no resource deletion is authorized by this guide.

## Scope and remaining gaps

Keep one Droplet and bounded calls. No custom UI, database, extra agent, Action Gateway integration, GPU or new router is needed now. Deeper research methods and managed microVM hosting remain future options.

Native evaluation access/schema, fixed model choices, hosting balance, deployed size, router policy, exact token usage and incurred cost remain unverified. The older `experiment.py` remains preserved practice code; `evaluation/run_eval.py` is now the active open-source evaluator.

## Relevant videos retained from the original guide

- [DigitalOcean serverless walkthrough](https://www.youtube.com/watch?v=nUlB2n3vU6U) — older demo; current docs take precedence.
- [Routing demo](https://www.youtube.com/watch?v=FvxY8oPoI8o&t=266s).
- [Model comparison demo](https://www.youtube.com/watch?v=FvxY8oPoI8o&t=481s).

These links were checked earlier; playback was not verified. No exact current OpenCode Marketplace setup video was verified.
