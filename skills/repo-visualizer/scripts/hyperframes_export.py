#!/usr/bin/env python3
"""Export an existing deterministic Repo Visualizer player with HyperFrames.

No alternate graph or React composition: the adapter seeks the shipped player.
HyperFrames 0.9.20, Node 22+, Chrome and FFmpeg/FFprobe are optional dependencies.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

from export import scene

VERSION = '0.9.20'


def composition(document, duration_ms, width, height, fps, scenario=None, layout=None):
    """Wrap a complete self-contained player; use the supported timeline-like interface."""
    if not re.search(r'<body(?:\s[^>]*)?>', document, re.I) or not re.search(r'</body\s*>', document, re.I):
        raise ValueError('Expected the complete generated explorer HTML with a body element')
    if not 0 < duration_ms <= 3_600_000:
        raise ValueError('Composition duration must be positive and at most one hour')
    if not all(type(x) is int and x > 0 for x in (width, height, fps)):
        raise ValueError('Width, height and fps must be positive integers')
    from builder import safe_json
    config = safe_json(dict(duration=duration_ms / 1000, scenario=scenario))
    # The layout was computed from the same graph in the real player. Caching
    # presentation coordinates avoids running the layout engine per worker.
    if layout is not None:
        cached = '<script id="layout-cache">window.REPO_PRECOMPUTED_LAYOUT='+safe_json(layout)+';</script>'
        document = re.sub(r'<script id="layout-engine">.*?</script>', lambda match: cached, document, count=1, flags=re.S)
    document = re.sub(r'<script id="interaction-script">.*?</script>', '', document, count=1, flags=re.S)
    # buildReady is the runtime's declared-compute barrier. ELK layout and fonts
    # must settle before a capture seeks; every frame uses the player's renderAt.
    adapter = '''<script>
(function(){
 const config=CONFIG;
 document.body.classList.add('export-frame');
 const ready=Promise.resolve(window.repoReady).then(()=>{
  if(config.scenario)window.repoPlayer.setScenario(config.scenario);
  window.repoPlayer.setView('path');
  window.renderAt(0);
 });
 window.__hf=window.__hf||{};
 window.__hf.buildReady=window.__hf.buildReady||{};
 window.__hf.buildReady.repoVisualizer=ready;
 window.__timelines=window.__timelines||{};
 window.__timelines.root={
  duration:()=>config.duration,totalDuration:()=>config.duration,
  pause(){return this},getChildren:()=>[],
  seek(seconds){window.renderAt(seconds*1000);return this}
 };
})();
</script>'''.replace('CONFIG', config)
    root=f'<div id="hf-repo-root" data-composition-id="root" data-width="{width}" data-height="{height}" data-duration="{duration_ms/1000}" data-fps="{fps}">'
    document=re.sub(r'(<body(?:\s[^>]*)?>)',lambda m:m[1]+root,document,count=1,flags=re.I)
    return re.sub(r'</body\s*>',lambda m:'</div>'+adapter+m[0],document,count=1,flags=re.I)


def launcher(command=None):
    if command:
        # Explicit executable only. No shell parsing of user paths or repository data.
        return [str(command)]
    if shutil.which('pnpm'):
        return [shutil.which('pnpm'), 'dlx', 'hyperframes@'+VERSION]
    if shutil.which('npx'):
        return [shutil.which('npx'), '--yes', 'hyperframes@'+VERSION]
    raise RuntimeError('Install Node 22+ and pnpm/npm, or pass an installed HyperFrames executable with --hyperframes')


def render(source, output, *, width=1440, height=900, fps=12, browser_path=None, scenario=None, executable=None):
    source,output=Path(source).resolve(),Path(output).resolve()
    if source == output:
        raise ValueError('Video output must differ from input HTML')
    kind=output.suffix.lower().lstrip('.')
    if kind not in {'mp4','webm','gif','mov'}:
        raise ValueError('HyperFrames output must be mp4, webm, gif or mov')
    if not 1 <= fps <= 60 or not 320 <= width <= 3840 or not 320 <= height <= 2160:
        raise ValueError('Use fps 1–60, width 320–3840 and height 320–2160')
    command=launcher(executable)
    with scene(source,width,height,browser_path) as page:
        if scenario:
            page.evaluate('(id)=>window.repoPlayer.setScenario(id)',scenario)
        duration=page.evaluate('window.repoPlayer.durationMs')
        layout=page.evaluate('window.repoPlayer.layout')
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='repo-hyperframes-',dir=output.parent) as directory:
        root=Path(directory)
        (root/'index.html').write_text(composition(source.read_text(encoding='utf-8'),duration,width,height,fps,scenario,layout),encoding='utf-8')
        candidate=root/('render.'+kind)
        subprocess.run([*command,'render',str(root),'-o',str(candidate),'--format',kind,'--fps',str(fps),'--workers','1','--low-memory-mode'],check=True,timeout=1800)
        if not candidate.is_file() or candidate.stat().st_size == 0:
            raise RuntimeError('HyperFrames returned without a nonempty output file')
        candidate.replace(output)
    return dict(output=str(output),engine='hyperframes',version=VERSION,duration_ms=duration,fps=fps)


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('html',type=Path);p.add_argument('-o','--output',type=Path,required=True)
    p.add_argument('--width',type=int,default=1440);p.add_argument('--height',type=int,default=900);p.add_argument('--fps',type=int,default=12)
    p.add_argument('--scenario');p.add_argument('--browser',type=Path);p.add_argument('--hyperframes',type=Path)
    a=p.parse_args(argv)
    try:
        print(json.dumps(render(a.html,a.output,width=a.width,height=a.height,fps=a.fps,browser_path=a.browser,scenario=a.scenario,executable=a.hyperframes),indent=2));return 0
    except (ValueError,RuntimeError,OSError,subprocess.SubprocessError) as error:
        print(f'error: {error}',file=sys.stderr);return 2


if __name__=='__main__':raise SystemExit(main())
