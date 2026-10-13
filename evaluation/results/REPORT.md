# DeepSeek Flash comparison — 13 October 2026

This is one bounded run on the fictional RiverWatch archive. It compares the frozen original and model-generated compressed files with the same five questions, using `deepseek-v4.1-flash` through DigitalOcean Serverless Inference.

## Observed measurements

| Measure | Original archive | Compressed archive |
| --- | ---: | ---: |
| Candidate prompt tokens | 4,359 | 3,124 |
| Candidate completion tokens | 735 | 814 |
| Average candidate latency | 2.467 s | 2.610 s |
| Archive size | 3,743 bytes | 2,177 bytes |

The measured candidate prompt reduction was **1,235 tokens, or 28.33%**. The archive itself was 41.84% smaller in bytes. Byte reduction is not a token or cost measurement. The compressed run used more completion tokens and was slightly slower in this single sequential trial, so we cannot claim total cost or latency savings yet.

## Manual answer review

All five outputs answered the questions in a usable way. Both versions correctly handled the warm-up exclusion, the corrected Sensor A recommendation, the low-turbidity Sensor B exception, the conditional 23 October purchasing deadline, and the missing battery-life evidence. The compressed answer to the low-turbidity question omitted the supporting 1.2/0.9 and high-group values, so the shorter archive preserved the decision but less of the evidence detail.

The repository's lexical marker score is included in the JSON as a debugging signal. It penalizes valid paraphrases and is not a semantic accuracy score. No native DigitalOcean judge or separate LLM judge was used in this run.

## Reproducibility and limits

- Candidate: `deepseek-v4.1-flash`; temperature 0; maximum 1,024 output tokens.
- Ten candidate calls total: five questions against each archive.
- Synthetic five-row dataset; this demonstrates a workflow, not general model or compression effectiveness.
- Compression was model-generated and LLMLingua-inspired; it was not the LLMLingua implementation.
- Pricing, total cost and compression-generation overhead are not included because the account rate and the first compression call were not captured in this result.
- The failed earlier 256-token attempt produced no result file; provider charges, if any, must be checked in DigitalOcean usage rather than inferred.

Raw outputs and per-row metrics are in [`deepseek-v4.1-flash-20261013-retry.json`](deepseek-v4.1-flash-20261013-retry.json).
