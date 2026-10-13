# Source and adaptation

Reference: [ShenSeanChen/waku-agent](https://github.com/shenseanchen/waku-agent), inspected at commit `4b69b321324750f231fdfd72a83b38ad7301dcc3`.

The workspace sidebar, separate observability/evaluation views, expandable per-step trace, shared time axis and read-only stdlib HTTP approach informed this implementation. The HTML escaping helper in `static/app.js` is adapted from `waku/ops/static/js/util.js`; the MIT notice is retained in `WAKU-LICENSE.txt`.

This is an adaptation for OpenCode and research experiments, not the complete Waku runtime or an exact replica. Its memory, tool integrations, judges and chat backend are not implemented here. Waku's separately restricted design-system files, marks and product branding are not copied. Our layout styling and research-specific data rendering are authored for this project.

Compression uses the actual [Microsoft LLMLingua](https://github.com/microsoft/LLMLingua) library, version 0.2.2, and its documented LLMLingua-2-small checkpoint. [LLMLingua-2 paper](https://aclanthology.org/2024.findings-acl.57/). The experiment records the downloaded checkpoint revision and installed versions. No upstream benchmark scores are asserted.
