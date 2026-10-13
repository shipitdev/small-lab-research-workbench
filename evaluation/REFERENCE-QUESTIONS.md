# Held-out evaluation questions and reference answers

All references below are manually prepared from the fictional original.txt. Keep this file with the evaluation operator while the research agent compresses the source. This is NOT a DigitalOcean upload schema: teammate C must map these entries to the current native uploader format and inspect its preview.

1. How many paired samples remain after quality control, and why were the others removed?
   Reference: 40 paired samples remain. Eight of the original 48 were excluded because both sensors were measured before the ten-minute warm-up had elapsed. The retained samples comprise 20 low-turbidity and 20 high-turbidity samples.
2. Which sensor is preferred overall after correction, and what are the error values and units?
   Reference: Sensor A is preferred for a general pilot spanning the tested range. Its corrected mean absolute error is 3.1 NTU, compared with Sensor B's 4.0 NTU, across the 40 retained paired samples. The initial provisional preference for B used warm-up readings and was superseded.
3. Does the overall recommendation also apply to water below 20 NTU?
   Reference: Not necessarily. Below 20 NTU, Sensor B has the lower mean absolute error, 0.9 NTU versus Sensor A's 1.2 NTU, so B may be preferable for a pilot restricted to that subgroup. Above or equal to 20 and up to 100 NTU, A's error is 5.0 NTU versus B's 7.1 NTU.
4. What is the final purchasing deadline, and what condition could defer it?
   Reference: The later memo sets 23 October as the final deadline, conditional on receiving all site permissions by 18 October. Later permission requires purchasing to be deferred until a revised schedule is approved. The draft 20 October date is superseded.
5. How long will Sensor B's battery last during unattended deployment?
   Reference: Not found / cannot be calculated from this archive. The 45 mA figure is only measurement-mode current. Battery capacity, duty cycle, sleep current, voltage and radio power are missing, and continuous unattended field reliability was not tested.

Scoring: use the same questions and reference answers for Original and Compressed. Keep candidate, judge, settings, metric and threshold fixed. Prefer the reference-aware Ground Truth Faithfulness metric if available. Manually inspect dates, units, correction history, exceptions and unsupported claims; judge scores alone are not conclusive.

The dataset contains five questions, so results demonstrate a workflow, not broad model accuracy. Candidate latency excludes compression and judging. No live evaluation results exist yet.
