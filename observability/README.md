# Local research observatory

From the repository root:

```sh
python3 observability/server.py
```

Open http://localhost:7777. It reads `evaluation/results/llmlingua-*/` every five seconds. It binds only to your Mac's loopback address, exposes three static files and one read-only endpoint (`GET /api/observability`), and cannot start paid model calls. No model key is sent to the browser.

In a second terminal, start a fresh real workflow:

```sh
bash scripts/demo.sh
```

This uses the existing SSH connection to the research Droplet, runs its installed CPU compressor, and syncs only that run's evidence to your Mac. `rsync` must be installed on both machines. Every run makes ten paid fixed-model DeepSeek calls plus one paid OpenCode inspection. Existing runs are retained. The operational OpenCode default router is unchanged.

The Droplet requires Python venv support and a preinstalled compressor environment:

```sh
python3 -m venv .venv-llmlingua
.venv-llmlingua/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu
.venv-llmlingua/bin/pip install -r evaluation/requirements-compression.txt
```

The tested environment and checkpoint revision are recorded in each run's `compression.json`. First use downloads the public checkpoint; later runs use its local cache. A failed run retains its trace and any completed calls; it does not pretend to be complete. The comparison cannot claim a speed or dollar improvement merely from fewer input tokens.

## Judge walkthrough (about three minutes)

1. **Overview:** “Small labs need to test research components without operating a large model server. Our cloud workspace runs the agent and a small compressor; DigitalOcean supplies DeepSeek inference.” Show the four workflow stages.
2. **Context:** Show the long notebook and actual LLMLingua-2 output. “This uses Microsoft's token-classification checkpoint. Compression happens before the evaluator loads the reference answers.” Show checkpoint revision, compressor token counts and compression time.
3. **Observability:** Expand an OpenCode event and an inference call. “We can see what actually ran, how long it took, and the provider token receipt. This is our workflow evidence, not invented agent activity.”
4. **Evaluations:** Show question 2 (corrected overall choice), question 3 (the exception and its numbers), question 4 (conditional deadline), and question 5 (missing battery evidence). Compare both answers with the reference. Missing or wrong details are visible, rather than concealed by a headline score.
5. **Overview:** Report the recorded provider input-token reduction, output usage and timings. “We reproduced the method on our synthetic example. This does not reproduce the paper's published benchmark scores.”
6. To rerun, keep the dashboard open and run `bash scripts/demo.sh` in the second terminal. Select the new UTC-named run once it appears. Its trace updates during the experiment; final results appear when all ten calls complete. Model outputs and timing may vary; identical scores are not guaranteed.

**Saved-run fallback:** The dashboard's retained completed run works without SSH or inference access. Say that it is recorded evidence. Don't imply a fresh live run if network access fails.

**DigitalOcean view:** Per-request usage comes directly from inference responses. The separate platform JSON is an earlier manual account-wide dashboard observation. It is neither live billing nor a native DigitalOcean judge evaluation.

See [source attribution](ATTRIBUTION.md) for the Waku reference and the adapted MIT helper. This is a research-focused adaptation, not the complete Waku dashboard/runtime.
