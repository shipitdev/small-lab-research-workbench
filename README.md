# Small Lab Research Workbench

An open-source research workflow for small labs using OpenCode and DeepSeek through DigitalOcean Serverless Inference.

The first experiment compares a fictional research archive with a model-generated compressed version. It is inspired by LLMLingua's context-efficiency question; it does not implement LLMLingua's algorithm.

## Run the evaluation

Python 3 is the only runtime dependency. Run the offline tests:

```sh
python3 -m unittest discover -s evaluation -p 'test_*.py' -v
```

Run a bounded comparison with a fixed model:

```sh
python3 evaluation/run_eval.py --model deepseek-v4.1-flash --output evaluation/results/new-run.json
```

The script asks for a model access key with hidden input, or uses `DIGITALOCEAN_MODEL_ACCESS_KEY`. Keep credentials outside the repository. Each comparison makes ten paid inference calls; existing output files are preserved.

## Evidence

- [Evaluation instructions](evaluation/README.md)
- [Comparison page](evaluation/results/comparison.html)
- [Observed results and limitations](evaluation/results/REPORT.md)
- [Raw DeepSeek outputs](evaluation/results/deepseek-v4.1-flash-20261013-retry.json)
- [DigitalOcean dashboard observation](evaluation/results/digitalocean-observability.json)
- [Original research input](research-inputs/original.txt) and [compressed archive](cloud-artifacts/compressed.txt)

The first comparison measured 28.33% fewer candidate prompt tokens. Completion usage increased and latency did not improve in this single trial. Manual review found the main decisions preserved with some supporting detail omitted. The dataset is synthetic, lexical scores are proxies, and total cost savings have not been established.

Future runs capture exact request messages, source hashes, timestamps and provider identifiers. Native DigitalOcean judge evaluations have not run. Dashboard totals are account-wide observations, not exclusively benchmark usage.

`experiment.py` is an earlier standalone practice script; `evaluation/run_eval.py` is the current evaluator.
