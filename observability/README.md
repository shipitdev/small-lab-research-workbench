# Local research observatory

From the repository root:

```sh
python3 observability/server.py
```

Open http://localhost:7777/#workflow. Leave **Follow newest run** checked: starting the bash script switches the dashboard to the new run automatically. It narrates recorded stages in plain language, shows the actual OpenCode inspection and completed candidate answers, then displays final metrics. Selecting an older run turns following off; re-enable it before your next live demo. It reads `evaluation/results/llmlingua-*/` every five seconds. It binds only to your Mac's loopback address, exposes three static files and one read-only endpoint (`GET /api/observability`), and cannot start paid model calls. No model key is sent to the browser.

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
6. To rerun, keep the dashboard open and run `bash scripts/demo.sh` in the second terminal. Enable **Follow newest run** to select the new UTC-named run automatically. Its trace updates during the experiment; final results appear when all ten calls complete. Model outputs and timing may vary; identical scores are not guaranteed.

**Saved-run fallback:** The dashboard's retained completed run works without SSH or inference access. Say that it is recorded evidence. Don't imply a fresh live run if network access fails.

**DigitalOcean view:** Per-request usage comes directly from inference responses. The separate platform JSON is an earlier manual account-wide dashboard observation. It is neither live billing nor a native DigitalOcean judge evaluation.

See [source attribution](ATTRIBUTION.md) for the Waku reference and the adapted MIT helper. This is a research-focused adaptation, not the complete Waku dashboard/runtime.

## Interactive cloud demonstration

Use this when you want to connect to the cloud, give the agent an instruction, and watch the experiment in the dashboard.

1. Start the local dashboard if it is not already running: `python3 observability/server.py`.
2. Upload the latest recipe without making inference calls: `bash scripts/demo.sh --prepare`.
3. In a local terminal, run `bash scripts/demo.sh --watch`. Leave it running; it syncs only research run directories and never starts an experiment. Stop it with Ctrl+C.
4. Open http://localhost:7777/#workflow and enable **Follow newest run**.
5. In another terminal, connect to the configured Droplet and open its agent:

```sh
ssh root@134.209.114.233
cd /root/research-workbench
/root/.opencode/bin/opencode
```

The address is the current project's Droplet; use your own authorized host if different.

Type this task into OpenCode:

```text
Run our RiverWatch research experiment using the existing tested recipe.
Compare the original archive with actual LLMLingua-2 compression through
DeepSeek, and preserve all evaluation evidence. Do not change the code,
questions, or compression settings.

Use the bash tool to start the following command exactly once in the
background, then report its PID and run directory:

run_dir="evaluation/results/llmlingua-$(date -u +%Y%m%dT%H%M%SZ)"
nohup .venv-llmlingua/bin/python evaluation/workflow.py --model deepseek-v4.1-flash --output "$run_dir" > /tmp/small-lab-demo.log 2>&1 &
echo "PID=$! RUN=$run_dir"
```

Approve OpenCode's command permission if prompted. The background process avoids keeping the agent's shell tool open for the entire experiment. This makes paid inference calls. Run one experiment at a time; `/tmp/small-lab-demo.log` is the latest launch log, while the uniquely named evidence directories are preserved.

Show the terminal's real tool action, then the dashboard's stage updates, actual inspection answer, candidate answers, and final metrics. The outer interactive agent launches the existing recipe; the workflow also runs its own archive-inspection agent call. The dashboard records that inner inspection and experiment events, not the outer terminal conversation. It does not expose private model reasoning.

The dashboard starts showing progress once the workflow writes its first event. If nothing arrives, ask OpenCode to check the reported process and `/tmp/small-lab-demo.log`; a launch acknowledgement is not proof that the experiment succeeded. The watcher reports synchronization failures and retries. Final metrics appear only when a completed `result.json` is synchronized.

## Natural-language task and session approvals

The demo's SSH user is root, so sudo is not needed. To auto-approve tool requests for this OpenCode session, start `/root/.opencode/bin/opencode --auto` in `/root/research-workbench`. Explicit deny rules still apply. This grants the session the ability to run allowed commands without stopping for prompts; it is not a sandbox. Typing “sudo approve all” into the task does not configure permissions.

A natural prompt for this prepared workflow:

```text
I have a water-sensor research notebook in research-inputs/original.txt.
Please test whether shortening it with actual LLMLingua-2 preserves the
information our lab needs, using our existing evaluation/workflow.py recipe.

You have my approval to read the research files and execute the commands
needed for this experiment. Keep the original notebook, evaluation questions,
and recipe unchanged. Use DeepSeek serverless inference for both versions.
Start one run in the background with a fresh UTC-named
 evaluation/results/llmlingua-... directory, and tell me its process ID and
run directory so I can follow the evidence in the dashboard.

Record the answers, input and output tokens, reasoning-token usage, runtime,
and evaluation evidence. Once complete, explain the tradeoffs in simple
words and identify missing details by comparing answers with the references.
Do not invent results or claim savings from input-token reduction alone.
```

Reasoning tokens are now visible both in final live metrics and beside individual completed answers when the provider reports them. They are a subset of output tokens, not extra tokens to add again and not a display of private model reasoning. Missing counts appear as unavailable rather than zero.
