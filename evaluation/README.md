# Open-source evaluation runner

`run_eval.py` is the repository's reproducible benchmark. It sends the same five questions to the original and compressed RiverWatch archives through the DigitalOcean OpenAI-compatible endpoint.

The measured candidate must be a fixed model ID, such as the exact DeepSeek Flash slug shown in the DigitalOcean Model Catalog. Do not use `router:general` for this comparison: routing can change the model between requests.

## Run

Keep the model access key out of files and Git. Either export it in the shell or let the script ask for it without echoing:

```sh
export DIGITALOCEAN_MODEL_ACCESS_KEY='...'
python3 evaluation/run_eval.py \
  --model deepseek-v4.1-flash \
  --output evaluation/results/deepseek-flash-$(date +%Y%m%d-%H%M%S).json
```

The script makes ten candidate calls: five questions against each context. It uses temperature 0, allows up to 1,024 output tokens so reasoning models are not truncated, and refuses to overwrite an existing result. Keep the output JSON with the model ID and settings.

## What it measures

- API-reported prompt-token counts for original and compressed contexts.
- Prompt-token reduction and byte sizes.
- Raw answers, latency and completion-token usage.
- A transparent lexical reference-marker recall and `Not found` alignment check.

The lexical score is a debugging signal, not a semantic accuracy score. Review the answers manually and use DigitalOcean's native Evaluations as optional judge evidence. The compression method remains model-generated and LLMLingua-inspired; it is not the LLMLingua implementation.

The first completed run is summarized in [REPORT.md](results/REPORT.md), with raw outputs in `results/deepseek-v4.1-flash-20261013-retry.json`.
