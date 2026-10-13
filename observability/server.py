"""Loopback-only, read-only observability. No keys, dependencies or paid calls."""
import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
STATIC = Path(__file__).with_name('static')


def snapshot(root):
    runs = []
    for directory in sorted((root / 'evaluation/results').glob('llmlingua-*'), reverse=True):
        result = directory / 'result.json'
        trace = directory / 'trace.jsonl'
        harness = directory / 'opencode.jsonl'
        calls = [dict(json.loads(file.read_text()), context=file.stem.rsplit('-', 1)[0],
                      question_index=int(file.stem.rsplit('-', 1)[1]))
                 for label in ('original', 'compressed')
                 for file in sorted(directory.glob(label + '-[1-5].json'))]
        compression = directory / 'compression.json'
        runs.append({'id': directory.name, 'result': json.loads(result.read_text()) if result.exists() else None,
            'calls': calls,
            'compression': json.loads(compression.read_text()) if compression.exists() else None,
            'trace': [json.loads(line) for line in trace.read_text().splitlines() if line.strip()] if trace.exists() else [],
            'harness': [json.loads(line) for line in harness.read_text().splitlines() if line.startswith('{')] if harness.exists() else []})
    platform = root / 'evaluation/results/digitalocean-observability.json'
    return {'runs': runs, 'platform': json.loads(platform.read_text()) if platform.exists() else None}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        route = urlsplit(self.path).path
        try:
            if route == '/api/observability':
                body, content = json.dumps(snapshot(ROOT)).encode(), 'application/json'
            elif route in ('/', '/app.js', '/style.css'):
                file = STATIC / {'/': 'index.html', '/app.js': 'app.js', '/style.css': 'style.css'}[route]
                body = file.read_bytes()
                content = {'/': 'text/html', '/app.js': 'text/javascript', '/style.css': 'text/css'}[route]
            else:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header('Content-Type', content + '; charset=utf-8')
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Content-Security-Policy', "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self'; connect-src 'self'; frame-ancestors 'none'")
            self.end_headers()
            self.wfile.write(body)
        except (OSError, ValueError):
            self.send_error(503, 'Evidence is updating; refresh shortly')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=7777)
    args = parser.parse_args()
    print(f'Open http://localhost:{args.port}', flush=True)
    ThreadingHTTPServer(('127.0.0.1', args.port), Handler).serve_forever()
