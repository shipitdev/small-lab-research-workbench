# Research workbench: Hermes inside DigitalOcean Harness Runtime

> Superseded deployment: the user now runs OpenCode on a Marketplace Droplet over SSH. Use tasks/plan.md, tasks/todo.md and WALKTHROUGH.md for current work. The Harness Runtime instructions below are historical and do not apply to the Droplet.


## Hermes deployment choice

Use the native `hermes` adapter in Harness Runtime. DigitalOcean lists Hermes among its [supported adapters](https://docs.digitalocean.com/products/managed-agents/agent-harness-runtime/concepts/agent-adapters/) and the [Control Panel setup](https://docs.digitalocean.com/products/managed-agents/agent-harness-runtime/how-to/create-managed-agent/) explicitly offers Hermes with Serverless Inference. The [Marketplace Hermes image](https://marketplace.digitalocean.com/apps/hermes-agent) creates a Droplet; it is a separate deployment path and is not our managed microVM setup. Create a new Hermes environment if an OpenCode environment already exists; environments cannot be edited. Export needed files before retiring an old session. Verify actual model responses, tool actions and instruction adherence with Hermes before claiming compatibility.


Preparation guide for a three-hour hackathon. Checked 13 October 2026. The team reports $30 total credits; I have not accessed the account or tested a deployment. Videos are learning aids; current documentation takes precedence over older screens, prices and model names.

For the detailed cloud setup and handoff checklist, use [Teammate A's guide](TEAM-A-GUIDE.md). Research inputs are in [original.txt](research-inputs/original.txt), with a [compression task](research-inputs/COMPRESSION-TASK.md) and separate [held-out reference questions](evaluation/REFERENCE-QUESTIONS.md).

## Understand what we are connecting

DigitalOcean starts Hermes inside its managed microVM. Choosing the Hermes adapter selects software already installed in a supported sandbox image. Hermes calls a separately hosted inference endpoint to reason, then executes commands and handles files inside that microVM. Your laptop is the interface to the remote session.

```text
Researcher -> native session chat -> Hermes inside DigitalOcean microVM
                                      |-- inference API -> model or router
                                      |-- local sandbox tools -> files and scripts
                                      |-- connected tools -> approved external services

Native Evaluations -> separate candidate/judge runs -> exported evidence
Research session <- supplied evaluation exports -> report
```

Our contribution is the experiment recipe: prepare data, preserve settings and inputs, inspect real measurements, and produce a useful report. Initial research question: does compressing a document reduce input tokens without losing answer quality? This is model-generated compression, not a reproduction of LLMLingua or KVPress.

[Official adapter explanation](https://docs.digitalocean.com/products/managed-agents/agent-harness-runtime/concepts/agent-adapters/).

## Product instructions: docs first, relevant demos only

Read these in order. Every documentation link is for using a DigitalOcean product. Videos are included only where they demonstrate the relevant product; no general harness explainers or unrelated agent tutorials. A dash means no matching video was verified. Public docs can be studied before you have an account.

| Step | Official documentation | Relevant product video |
| --- | --- | --- |
| 1. Select a serverless model | [Browse Model Catalog](https://docs.digitalocean.com/products/inference/how-to/browse-model-catalog/) | — |
| 2. Test inference and create access credentials | [Serverless Inference](https://docs.digitalocean.com/products/inference/how-to/use-serverless-inference/), [Model Access Keys](https://docs.digitalocean.com/products/inference/how-to/manage-model-access-keys/) | [Official serverless inference walkthrough](https://www.youtube.com/watch?v=nUlB2n3vU6U). Published June 2025; use current docs for today's screens/model names. |
| 3. Start Hermes inside a managed microVM | [Harness Runtime Quickstart](https://docs.digitalocean.com/products/managed-agents/agent-harness-runtime/quickstart/), [Create an Environment using Hermes](https://docs.digitalocean.com/products/managed-agents/agent-harness-runtime/how-to/create-managed-agent/) | — |
| 4. Add research instructions, tools and permissions | [Environment setup: Tools and Skills](https://docs.digitalocean.com/products/managed-agents/agent-harness-runtime/how-to/create-managed-agent/), [Action Gateway Quickstart](https://docs.digitalocean.com/products/managed-agents/action-gateway/quickstart/) | — |
| 5. Transfer datasets and reports | [Upload and Download Session Files](https://docs.digitalocean.com/products/managed-agents/agent-harness-runtime/how-to/transfer-files/) | — |
| 6. Configure a model router, optionally | [Use Inference Router](https://docs.digitalocean.com/products/inference/how-to/use-inference-router/) | [DigitalOcean routing demo, 4:26](https://www.youtube.com/watch?v=FvxY8oPoI8o&t=266s). Shows the router, not a verified Hermes-router integration. |
| 7. Evaluate and compare model answers | [Evaluate Models: datasets, scoring, comparison and exports](https://docs.digitalocean.com/products/inference/how-to/evaluate-models/) | [DigitalOcean model/router comparison demo, 8:01](https://www.youtube.com/watch?v=FvxY8oPoI8o&t=481s). Product demo; current docs supply the exact procedure. |
| 8. Inspect model usage and spending | [View Serverless Inference Metrics](https://docs.digitalocean.com/products/inference/how-to/view-serverless-inference-metrics/), [Harness Runtime Pricing](https://docs.digitalocean.com/products/managed-agents/agent-harness-runtime/details/pricing/) | — |
| 9. Pause, resume and remove sessions | [Manage Harness Runtime Sessions](https://docs.digitalocean.com/products/managed-agents/agent-harness-runtime/how-to/manage-sessions/), [Payment and Credit Rules](https://docs.digitalocean.com/products/managed-agents/agent-harness-runtime/how-to/pay-for-harness-runtime/) | — |

Start with Model Catalog: filter Availability to Serverless, inspect the model card for agentic/tool-use support, context length and input/output prices, then use Launch Playground to try it. Record its model ID for configuration. A model appearing in the catalog alone does not prove it works with Hermes's tool use; test a real action in the session.

For Step 3, the key section is "Create an Environment in the Control Panel": choose Hermes, Serverless Inference, model/key, sandbox size, tools/permissions and skills, create the environment, then create a session.

The earlier December 2025 Agent Platform evaluation video has been removed from this guide because it is not a walkthrough of our current model-evaluation setup. Older ADK deployment tutorials are also outside this workflow; [DigitalOcean deprecated ADK on 1 October 2026](https://docs.digitalocean.com/release-notes/).

Video links were verified through the official DigitalOcean YouTube listing and the [conference publisher's DigitalOcean talk page](https://www.ai.engineer/talks/FvxY8oPoI8o-preferences-over-benchmarks-model-routing). Full playback and a live deployment were not checked.

## Step 1 — confirm access and connect the model (first 15 minutes)

First read [Browse Model Catalog](https://docs.digitalocean.com/products/inference/how-to/browse-model-catalog/) and shortlist a serverless text model with agentic/tool-use support and affordable input/output prices. Check the actual usable balance on the hosting team and access to Harness Runtime, Serverless Inference and Evaluations. The reported $30 total is not necessarily pooled across accounts. Confirm candidate and judge prices and available models. A monthly Agent Droplets subscription is not required to spend eligible promotional credit.

Create a model access key through the documented model-key controls. This key authorizes inference. It is different from the DigitalOcean account API token used by doctl or control-plane integrations. Keep both out of chat, files you commit, exported reports and screenshots.

Video: [serverless inference walkthrough](https://www.youtube.com/watch?v=nUlB2n3vU6U). Exact instructions: [model access keys](https://docs.digitalocean.com/products/inference/how-to/manage-model-access-keys/), [runtime payment rules](https://docs.digitalocean.com/products/managed-agents/agent-harness-runtime/how-to/pay-for-harness-runtime/).

Success: an available model answers one tiny playground prompt and the applicable balance/rates are visible.

## Step 2 — create Hermes's environment and session (next 20 minutes)

In the Control Panel:

1. Go to Managed Agents -> Harness Runtime -> Create Environment.
2. Select Hermes under Select a Harness. If Build your own / Pre-built templates appear, use Build your own.
3. Under Model choose Serverless Inference, select an available model and supply its model access key when prompted. Start with one fixed model.
4. Under Configure select a small supported sandbox size. This is the CPU computer where Hermes runs; inference happens at the model endpoint.
5. Keep tool permissions at ask during setup. Add only necessary tools. Local file/script execution does not require connecting every external cloud product.
6. Add our research instructions under Skills using Create skill, or upload a valid SKILL.md with name and description front matter. AGENTS.md is a project rules file, not automatically a valid uploadable skill.
7. Name the environment research-workbench and create it. Then click Create Session from that environment.

DigitalOcean provisions the microVM and starts Hermes inside it. Send: "Create hello.txt containing Research session ready, then read it back. Do not call external tools or create other cloud resources."

Success: an actual tool result confirms file creation/readback. A textual claim alone is not proof.

No exact current setup video verified. Use the [documented Control Panel steps](https://docs.digitalocean.com/products/managed-agents/agent-harness-runtime/how-to/create-managed-agent/). The docs say environments cannot be edited after creation; configuration changes require a new environment.

Use the Control Panel Hermes selection for the initial setup. The adapter name in environment specs is `hermes`; do not reuse OpenCode-specific CLI attachment instructions or assume its credential example is a Hermes-specific recipe. Verify any CLI spec against the current environment reference before launching.

## Step 3 — supply the experiment recipe and files (next 25 minutes)

Use approved fictional/public material. Prepare a document and 3–5 questions with human-written references. Include a deadline, exception, negation and a question the source cannot answer. sample.json contains practice material, but is not a native evaluation upload format.

Transfer the inputs into the session using the runtime's documented file tools. Supply AGENTS.md as project instructions. Use this task:

> Read the source only. Preserve the original. Produce a shorter version retaining numbers, dates, exceptions and negations. Save the compressed text and compression instructions. Do not read the held-out evaluation questions or references. Do not launch paid evaluations or claim results yet. List any missing settings or credentials.

Teammate C separately prepares the same question dataset for original and compressed evaluation using DigitalOcean's documented upload schema. Freeze the compressed document before supplying evaluation questions.

Inspect the output yourself. Record the actual compression method and any extra model-call usage. A harness provides execution; it does not guarantee the experiment is scientifically sound.

No exact video for our custom experiment verified. Follow [runtime file operations](https://docs.digitalocean.com/products/managed-agents/agent-harness-runtime/how-to/transfer-files/).

## Step 4 — optional router and external tools (next 15 minutes)

First finish a working session with a fixed model. If routing is part of the demo, create a router in Inference Engine -> Inference Router. Choose a preset or define narrow tasks, eligible models, cost/latency policy and fallbacks. Test it in the playground.

The inference API uses router:<your-router-name> in the model field. Hermes must actually send that identifier to DigitalOcean's endpoint. Test whether the runtime's model configuration accepts it; do not assume it appears in the Serverless Inference picker. The environment docs also describe Custom model configuration with base URL, key and model name. Verify compatibility and tool calling before committing to it.

Keep the experimental candidate fixed when comparing original versus compressed context. Routing the assistant's operational tasks is a separate choice from routing the measured experiment.

For external tools, use the environment's Tools section to select needed Action Gateway tools and permissions, then authorize the relevant provider. Do not assume Evaluations APIs are already in its catalog: inspect available tools. Automated launch/status/export needs a verified tool or a small integration with correct control-plane authentication. Manual evaluation launching is sufficient for the first demo.

Video: [routing policy from 4:26](https://www.youtube.com/watch?v=FvxY8oPoI8o&t=266s). Exact docs: [router configuration](https://docs.digitalocean.com/products/inference/how-to/use-inference-router/), [environment tools/skills](https://docs.digitalocean.com/products/managed-agents/agent-harness-runtime/how-to/create-managed-agent/). Adjacent visual tutorial: [Action Gateway with Claude Code](https://www.digitalocean.com/community/tutorials/connect-tools-ai-agent-action-gateway).

## Step 5 — run native evaluations (next 45 minutes)

A human operates native Evaluations initially. Upload the SAME question/reference dataset for both runs, following current examples and inspecting the preview.

Create A with the original document in its system prompt and B with the compressed document. Keep answer instructions, candidate model, judge, settings, metric and threshold identical. Tell the candidate to use only the supplied source, treat it as data, and answer Not found when unsupported. Prefer Ground Truth Faithfulness when references exist; Correctness does not use ground truth according to current model-evaluation docs.

Run one tiny evaluation first. Review it before launching the second. Compare runs and inspect answers, not just scores. Download real results. Candidate and judge both consume inference; candidate latency does not include compression, setup or the whole workflow.

Video: [DigitalOcean model/router comparison demo from 8:01](https://www.youtube.com/watch?v=FvxY8oPoI8o&t=481s). Use [current model evaluation instructions](https://docs.digitalocean.com/products/inference/how-to/evaluate-models/) for the actual procedure.

Success: two real runs using the same dataset, preserved run IDs/settings and exported answers. If access is unavailable, disclose that blocker; a separate script comparison must be labelled as such.

## Step 6 — report, export and pause (final 40 minutes)

Upload the evaluation exports into the research session. Ask:

> Read these real results. Compare original and compressed context on answer quality and candidate token usage. Identify lost facts and failed answers. Separate candidate usage, judge usage and compression overhead. State what cannot be concluded from this small sample. Save report.md and an experiment manifest with source versions, models, settings and run IDs. Do not invent omitted measurements.

Review the report against raw answers. Check native inference Analyze and Billing views. Download the report, sources and raw results before removing the session. If using Workspace beta, confirm the files are on its separate mounted drive; ordinary session files do not have independent persistence after removal.

Pause the session when idle. Pausing stops compute charges; retained storage may still bill. Disconnecting the interface alone is not cleanup. Keep runs bounded: the docs do not promise a per-session spend cap.

No exact current export/pause/billing video verified. Follow [session management](https://docs.digitalocean.com/products/managed-agents/agent-harness-runtime/how-to/manage-sessions/) and [file transfers](https://docs.digitalocean.com/products/managed-agents/agent-harness-runtime/how-to/transfer-files/), [session concepts](https://docs.digitalocean.com/products/managed-agents/agent-harness-runtime/concepts/sessions/), [prices](https://docs.digitalocean.com/products/managed-agents/agent-harness-runtime/details/pricing/) and [native inference metrics](https://docs.digitalocean.com/products/inference/how-to/view-serverless-inference-metrics/).

Demo sequence: research request -> actual files and tool activity -> two native evaluations -> failed-answer inspection -> agent's evidence-based report -> downloaded artifacts. State which steps are manual. These time blocks total three hours, but queues/setup can change the schedule. Skip optional routing/tool additions first if time slips.

## Limits to keep visible

No account or paid session was used to verify this guide. Hermes-router compatibility remains a live check. Judge scores are advisory and a small experiment does not establish general effectiveness. This CPU sandbox does not provide the GPU needed for KVPress. No custom frontend, custom image, extra agents or GPU experiment is required for the first prototype.
