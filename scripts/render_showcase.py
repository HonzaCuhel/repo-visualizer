#!/usr/bin/env python3
"""Render public showcase media from the same graph as the landing explorer.

Requires the optional export environment. Run scripts/build_site.py first.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/repo-visualizer/scripts'))
from export import export_scene


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--browser', help='Path to an existing Chromium browser')
    args = parser.parse_args()
    source = ROOT / 'site/codex-agent-loop.html'
    graph = json.loads((ROOT / 'examples/codex/agent-loop.json').read_text())
    jobs = []
    for language in ('en', 'cs'):
        for theme in ('light', 'dark'):
            suffix = ('' if language == 'en' else '-cs') + ('' if theme == 'light' else '-dark')
            for kind in ('png', 'gif', 'mp4'):
                filename = ('poster' if kind == 'png' else 'walkthrough') + suffix + '.' + kind
                jobs.append((ROOT / 'site/media' / filename, language, theme))

    def render(job):
        output, language, theme = job
        settings = dict(width=1200, height=800, fps=8, at=4800,
                        browser_path=args.browser, theme=theme, language=language)
        result = export_scene(source, output, **settings)
        provenance = {
            'kind': 'runtime-render',
            'generator': 'Repo Visualizer export.py (Playwright, Pillow, FFmpeg)',
            'settings': {key: value for key, value in settings.items() if key != 'browser_path'},
            'source_repository': graph['repo']['url'],
            'source_revision': graph['repo']['commit'],
            'source_html_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'artifact_sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
            'note': 'Source-derived graph explanation, not recorded execution. No image generation model used.',
        }
        Path(str(output) + '.provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
        print('Rendered ' + output.name, flush=True)
        return result

    with ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(render, jobs))
    export_scene(source, ROOT / 'site/downloads/component-map.svg', browser_path=args.browser)


if __name__ == '__main__':
    main()
