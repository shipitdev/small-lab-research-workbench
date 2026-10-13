# Small Lab Research Workbench

An open-source cloud research workflow for small labs: OpenCode on a DigitalOcean Droplet, actual Microsoft LLMLingua-2 compression on CPU, and DeepSeek through DigitalOcean Serverless Inference. The lab doesn't operate the large inference model.

Our prototype tests whether a shorter synthetic research notebook preserves the answers to five held-out questions. The localhost observatory shows the agent events, compressor settings, exact model contexts, token receipts, timings and side-by-side answers.

## Open the observatory

```sh
python3 observability/server.py
```

Visit http://localhost:7777. Select a retained completed LLMLingua run. No cloud credentials or dependencies are needed to inspect saved evidence.

To run a fresh paid experiment using the already configured research Droplet:

```sh
bash scripts/demo.sh
```

The script syncs new evidence while the workflow runs; the dashboard refreshes every five seconds. Each experiment makes ten fixed-model comparison calls plus an OpenCode inspection. Existing files are retained.

[Setup, complete workflow and judge demo](observability/README.md) · [Waku source attribution](observability/ATTRIBUTION.md) · [Earlier baseline evidence](evaluation/results/REPORT.md)

## What the results mean

This implements the real LLMLingua-2 method on our synthetic RiverWatch example. It does **not** reproduce the paper's published benchmark scores, which use other datasets and model settings. Provider input tokens, compressor tokenizer tokens and archive bytes are different measurements. Lower input usage alone does not establish lower total cost or latency. Reference-marker recall measures lexical overlap; inspect the answers for correctness.

The earlier model-generated compression experiment is retained separately. It measured 28.33% fewer candidate input tokens but did not use the LLMLingua algorithm. Native DigitalOcean judge evaluations have not run. The platform dashboard observation is historical and account-wide; per-call usage in new runs is captured directly from the inference API.

## Offline checks

```sh
python3 -m unittest discover -s evaluation -p 'test_*.py' -v
python3 -m unittest discover -s observability -p 'test_*.py' -v
node --check observability/static/app.js
```

Keep keys outside the repository. The observatory is loopback-only and read-only; it serves only its own static files and research evidence. `experiment.py` is an earlier practice script; `evaluation/workflow.py` is the complete current experiment.
