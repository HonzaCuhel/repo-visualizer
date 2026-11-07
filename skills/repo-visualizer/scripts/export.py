#!/usr/bin/env python3
"""Render the same explorer scene to PNG, SVG, GIF, MP4 or WebM."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import io
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import sys


@contextmanager
def scene(path, width, height, browser_path=None, theme=None, language=None):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as error:
        raise RuntimeError('Install export extras: uv run --with playwright --with pillow --with imageio-ffmpeg python export.py ...; then python -m playwright install chromium') from error
    with sync_playwright() as runtime:
        options = {'headless': True}
        if browser_path:
            options['executable_path'] = str(browser_path)
        browser = runtime.chromium.launch(**options)
        try:
            page = browser.new_page(viewport={'width': width, 'height': height}, device_scale_factor=1, reduced_motion='reduce')
            # Generated explorers are offline. Never load a remote resource during export.
            page.route('http://**/*', lambda route: route.abort())
            page.route('https://**/*', lambda route: route.abort())
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.goto(Path(path).resolve().as_uri(), wait_until='load')
            page.evaluate('document.body.classList.add("export-frame")')
            page.evaluate('window.repoReady')
            if theme:
                page.evaluate('(theme)=>window.repoAppearance.setTheme(theme)', theme)
            if language:
                page.evaluate('(language)=>window.repoAppearance.setLanguage(language)', language)
                page.evaluate('window.repoLocaleReady')
            page.evaluate('document.fonts.ready')
            if errors:
                raise RuntimeError('Player failed: '+ '; '.join(errors))
            yield page
        finally:
            browser.close()


def ffmpeg_binary():
    installed = shutil.which('ffmpeg')
    if installed:
        return installed
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError as error:
        raise RuntimeError('MP4/WebM need FFmpeg on PATH or the imageio-ffmpeg export extra') from error


def export_scene(source, output, *, width=1440, height=900, fps=12, at=0, browser_path=None, scenario=None, theme=None, language=None):
    source, output = Path(source), Path(output)
    if output.resolve() == source.resolve():
        raise ValueError('Export output must differ from the input HTML')
    kind = output.suffix.lower().lstrip('.')
    if kind not in {'png', 'svg', 'gif', 'mp4', 'webm'}:
        raise ValueError('Output extension must be png, svg, gif, mp4 or webm')
    if not 1 <= fps <= 60 or not 320 <= width <= 3840 or not 320 <= height <= 2160:
        raise ValueError('Use fps 1–60, width 320–3840 and height 320–2160')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='repo-visualizer-export-', dir=output.parent) as directory:
        temporary = Path(directory)
        candidate = temporary / ('output.'+kind)
        with scene(source, width, height, browser_path, theme, language) as page:
            if scenario:
                page.evaluate('(id)=>window.repoPlayer.setScenario(id)', scenario)
            if kind in {'gif', 'mp4', 'webm'}:
                page.evaluate('window.repoPlayer.setView("path")')
            duration = page.evaluate('window.repoPlayer.durationMs')
            if kind in {'svg', 'png'}:
                page.evaluate('(ms)=>window.renderAt(ms)', at)
                if kind == 'png':
                    page.screenshot(path=str(candidate), animations='disabled')
                else:
                    candidate.write_text(page.evaluate('window.repoPlayer.exportSVG()'), encoding='utf-8')
            else:
                from PIL import Image
                count = max(1, math.ceil(duration * fps / 1000))
                # Bound pathological animations rather than filling a disk silently.
                if count > 18000:
                    raise ValueError('Animation exceeds 18000 frames; narrow the graph or use a shorter path')
                if kind == 'gif' and count * width * height > 350_000_000:
                    raise ValueError('GIF exceeds the 350 megapixel memory budget; reduce width/height/fps or use MP4')
                frames = []
                for index in range(count):
                    page.evaluate('(ms)=>window.renderAt(ms)', index*1000/fps)
                    frame = page.screenshot(animations='disabled')
                    if kind == 'gif':
                        frames.append(Image.open(io.BytesIO(frame)).convert('RGB').quantize(colors=128))
                    else:
                        (temporary / f'{index:06d}.png').write_bytes(frame)
                if kind == 'gif':
                    # Palette GIF, rounded centisecond durations with no cumulative drift.
                    durations = [max(10, (round((i+1)*100/fps)-round(i*100/fps))*10) for i in range(count)]
                    frames[0].save(candidate, save_all=True, append_images=frames[1:], duration=durations, loop=0, optimize=False)
                else:
                    codec = ['-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-movflags', '+faststart'] if kind == 'mp4' else ['-c:v', 'libvpx-vp9', '-pix_fmt', 'yuv420p', '-crf', '28', '-b:v', '0']
                    command = [ffmpeg_binary(), '-v', 'error', '-y', '-framerate', str(fps), '-i', str(temporary / '%06d.png'), '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2', *codec, str(candidate)]
                    subprocess.run(command, check=True, timeout=600)
        candidate.replace(output)
    return {'output': str(output), 'format': kind, 'width': width, 'height': height, 'duration_ms': duration if kind in {'gif','mp4','webm'} else None, 'fps': fps if kind in {'gif','mp4','webm'} else None}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('html', type=Path)
    parser.add_argument('-o', '--output', type=Path, required=True)
    parser.add_argument('--width', type=int, default=1440)
    parser.add_argument('--height', type=int, default=900)
    parser.add_argument('--fps', type=int, default=12)
    parser.add_argument('--at', type=float, default=0, help='Static capture position in milliseconds')
    parser.add_argument('--scenario', help='Optional authored scenario ID')
    parser.add_argument('--theme', choices=['light', 'dark', 'system'], help='Appearance for this export')
    parser.add_argument('--language', help='Interface language; graph text changes only when a translation is supplied')
    parser.add_argument('--browser', type=Path, help='Existing Chromium-family executable; otherwise Playwright Chromium')
    args = parser.parse_args(argv)
    try:
        result = export_scene(args.html, args.output, width=args.width, height=args.height, fps=args.fps, at=args.at, browser_path=args.browser, scenario=args.scenario, theme=args.theme, language=args.language)
        print(json.dumps(result, indent=2))
        return 0
    except (RuntimeError, ValueError, OSError, subprocess.SubprocessError) as error:
        print(f'error: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
