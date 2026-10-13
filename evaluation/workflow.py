"""A bounded, traced LLMLingua-2 experiment. Run on the research Droplet."""
import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import time
from datetime import datetime, timezone
from run_eval import load_dataset, run_comparison

ROOT = Path(__file__).resolve().parents[1]
COMPRESSOR = 'microsoft/llmlingua-2-bert-base-multilingual-cased-meetingbank'
REVISION = '5f0c82792b7ea14c6484e015b6a072009496b7f2'
ENDPOINT = 'https://inference.do-ai.run/v1/chat/completions'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    parser.add_argument('--model', default='deepseek-v4.1-flash')
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=False)
    events = out / 'trace.jsonl'
    clock = time.perf_counter()

    def emit(kind, **data):
        with events.open('a') as handle:
            handle.write(json.dumps({'kind': kind, 'at_utc': datetime.now(timezone.utc).isoformat(),
                                     'elapsed_seconds': round(time.perf_counter() - clock, 4), **data}) + '\n')
        print(kind, data.get('name', ''), flush=True)

    try:
        # Credentials stay in this process; never in a browser, trace or CLI argument.
        key = os.environ.get('DIGITALOCEAN_MODEL_ACCESS_KEY')
        if not key:
            auth = json.loads((Path.home() / '.local/share/opencode/auth.json').read_text())
            key = auth['digitalocean']['key']
        source = ROOT / 'research-inputs/original.txt'
        if not source.exists():
            source = ROOT / 'original.txt'
        original = source.read_text()
        emit('workflow_start', name='RiverWatch / LLMLingua-2', model=args.model,
             source_sha256=hashlib.sha256(original.encode()).hexdigest())
        # Give the harness only the archive. No evaluation references or compression decisions.
        start = time.perf_counter()
        emit('step_start', name='OpenCode: inspect archive')
        proc = subprocess.run(['/root/.opencode/bin/opencode', 'run', '--format', 'json',
            '-m', 'digitalocean/' + args.model,
            'Read the attached synthetic research archive. In at most 100 words identify the research task, the later correction, and the missing measurements. Do not create or modify any files.',
            '--file', str(source)],
            cwd=out, capture_output=True, text=True, timeout=180)
        (out / 'opencode.jsonl').write_text(proc.stdout)
        if proc.returncode != 0:
            raise RuntimeError('OpenCode failed; inspect its local session. No benchmark was completed.')
        parsed = [json.loads(line) for line in proc.stdout.splitlines() if line.startswith('{')]
        if not parsed or any(item.get('type') == 'error' for item in parsed):
            raise RuntimeError('OpenCode emitted no successful trace.')
        emit('step_end', name='OpenCode: inspect archive', seconds=round(time.perf_counter()-start, 4),
             events=len(parsed))
        emit('step_start', name='LLMLingua-2: load CPU checkpoint')
        start = time.perf_counter()
        from llmlingua import PromptCompressor
        import torch
        torch.set_num_threads(2)
        compressor = PromptCompressor(model_name=COMPRESSOR, use_llmlingua2=True, device_map='cpu',
                                      model_config={'revision': REVISION})
        load_seconds = time.perf_counter() - start
        emit('step_end', name='LLMLingua-2: load CPU checkpoint', seconds=round(load_seconds, 4))
        emit('step_start', name='LLMLingua-2: compress without answer key')
        start = time.perf_counter()
        compression = compressor.compress_prompt(original, rate=0.5, force_tokens=['\n'], drop_consecutive=True)
        compression_seconds = time.perf_counter() - start
        compressed = compression['compressed_prompt']
        (out / 'compressed.txt').write_text(compressed)
        metadata = {'algorithm': 'LLMLingua-2', 'checkpoint': COMPRESSOR,
            'checkpoint_revision': getattr(compressor.model.config, '_commit_hash', None),
            'packages': {name: importlib.metadata.version(name) for name in ['llmlingua', 'transformers', 'torch']},
            'device': 'cpu', 'rate': 0.5, 'force_tokens': ['\n'], 'drop_consecutive': True,
            'load_seconds': round(load_seconds, 4), 'compression_seconds': round(compression_seconds, 4),
            'upstream_output': compression}
        (out / 'compression.json').write_text(json.dumps(metadata, indent=2))
        emit('step_end', name='LLMLingua-2: compress without answer key', seconds=round(compression_seconds, 4),
             origin_tokens=compression['origin_tokens'], compressed_tokens=compression['compressed_tokens'])
        # References enter only after compression is frozen.
        rows = load_dataset(ROOT / 'evaluation/riverwatch-eval.jsonl')
        def observe(label, index, row, seconds):
            (out / f'{label}-{index}.json').write_text(json.dumps(row, indent=2))
            emit('inference', name=f'{label} / question {index}', seconds=round(seconds, 4),
                 usage=row['response']['usage'], provider_response_id=row['response'].get('provider_response_id'))
        def on_start(label, index, question):
            emit('inference_start', name=f'{label} / question {index}', question=question)
        result = run_comparison(original, compressed, rows, args.model, key, ENDPOINT,
                                observer=observe, max_tokens=4096, on_start=on_start)
        result.update(method='Actual LLMLingua-2 CPU compression, synthetic RiverWatch application experiment',
                      compression=metadata, original_context=original, compressed_context=compressed)
        result['limitations'] = 'Method reproduction, not reproduction of published benchmark scores. Synthetic five-question dataset. Lexical recall is not semantic accuracy. One trial; caching and output length affect latency and cost. Compressor tokens differ from provider tokens.'
        (out / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
        emit('workflow_end', name='Comparison saved', prompt_metrics=result['prompt_metrics'])
    except Exception as exc:
        if hasattr(exc, 'evidence'):
            (out / 'failed-response.json').write_text(json.dumps(exc.evidence, indent=2))
        emit('workflow_error', name=type(exc).__name__, message=str(exc))
        raise


if __name__ == '__main__':
    main()
