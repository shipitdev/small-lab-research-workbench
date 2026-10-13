# Actual LLMLingua-2 experiment: observed result

Completed 13 October 2026. Five synthetic RiverWatch questions, each asked with the original and LLMLingua-2-compressed archive through fixed `deepseek-v4.1-flash`. Both sides use temperature 0 and a 4,096-token output allowance. OpenCode inspection is separate from the ten-call benchmark.

| Measurement | Original | Compressed |
|---|---:|---:|
| Provider input tokens | 4,359 | 2,524 |
| Provider output tokens, including reasoning | 622 | 7,817 |
| Provider reasoning tokens (subset of output) | 402 | 7,499 |
| Total measured request duration | 10.03s | 100.92s |
| Compressor tokenizer tokens | 772 | 407 |
| Archive bytes | 3,743 | 1,999 |

Input reduction: **42.10%**. Compressor computation: **1.9441s**, plus **4.3169s** loading its cached checkpoint. These timings are one CPU/DigitalOcean trial, not a benchmark distribution or causal speedup measurement. Cache usage differs between runs. Total billed cost is unavailable; fewer input tokens did not imply better total token usage.

Manual review:

- Both answers retain 40 paired samples and the exclusion of eight. The compressed answer weakens the direct explanation tying exclusion to incomplete warm-up.
- Both choose Sensor A overall with 3.1 versus 4.0 NTU.
- Both retain the low-turbidity exception favoring B. The compressed answer includes 0.9 versus 1.2 NTU; the original answer omits those supporting numbers.
- Both give 23 October. **The compressed answer omits the required permissions-by-18-October condition**, so it does not fully answer the question.
- Both correctly decline to calculate battery life from missing measurements.

Conclusion: the real compression method saves candidate input tokens in this example, but the shortened context causes substantially more reasoning and loses a condition. This prototype exposes that tradeoff; it does not demonstrate equivalent answer quality or cost/speed savings.

The failed earlier 1,024-token trial is retained separately. References were loaded only after compressor output was written. This is a method reproduction/application study using an official checkpoint, not a reproduction of LLMLingua-2's original published benchmark scores.
