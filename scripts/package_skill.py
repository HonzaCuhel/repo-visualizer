#!/usr/bin/env python3
"""Package a complete distributable skill from an explicit file inventory."""
from pathlib import Path
import argparse
import hashlib
import json
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    'SKILL.md', 'LICENSE', 'NOTICE.md', 'agents/openai.yaml',
    'scripts/story_model.py', 'scripts/inventory.py', 'scripts/repo_story.py',
    'scripts/builder.py', 'scripts/export.py', 'scripts/hyperframes_export.py',
    'references/graph-format.md', 'references/exports.md',
    'assets/player.html', 'assets/player.css', 'assets/player.js', 'assets/interaction.js',
    'assets/vendor/elk.bundled.js', 'assets/vendor/ELK-LICENSE.md', 'assets/vendor/elk-provenance.json',
    'assets/vendor/gifenc.js', 'assets/vendor/GIFENC-LICENSE.txt', 'assets/vendor/gifenc-provenance.json',
    'assets/fonts/AtkinsonHyperlegibleNext.ttf', 'assets/fonts/OFL-AtkinsonHyperlegibleNext.txt',
    'assets/fonts/AtkinsonHyperlegibleNext.ttf.provenance.json', 'assets/fonts/OFL-AtkinsonHyperlegibleNext.txt.provenance.json',
)


def package(output):
    skill = ROOT / 'skills/repo-visualizer'
    missing = [name for name in FILES if not (skill / name).is_file() or not (skill / name).stat().st_size]
    if missing:
        raise ValueError('Incomplete skill; missing required files: '+', '.join(missing))
    for name in FILES:
        path = skill / name
        if any(p.is_symlink() for p in (path, *path.parents) if p == skill or skill in p.parents):
            raise ValueError('Distribution must not contain symlinks: '+name)
    output = Path(output).resolve()
    if output == skill or skill in output.parents:
        raise ValueError('Archive output must be outside the skill directory')
    output.parent.mkdir(parents=True, exist_ok=True)
    candidate = None
    try:
        with tempfile.NamedTemporaryFile(dir=output.parent, suffix='.zip', delete=False) as stream:
            candidate = Path(stream.name)
        with zipfile.ZipFile(candidate, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
            for name in sorted(FILES):
                item = zipfile.ZipInfo('repo-visualizer/'+name, (2026,1,1,0,0,0))
                item.external_attr = 0o100644 << 16
                item.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(item, (skill / name).read_bytes())
        candidate.replace(output)
    finally:
        if candidate is not None:
            candidate.unlink(missing_ok=True)
    return {'file':str(output), 'files':len(FILES), 'sha256':hashlib.sha256(output.read_bytes()).hexdigest()}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('-o', '--output', default='dist/repo-visualizer.zip')
    args = p.parse_args()
    try:
        print(json.dumps(package(args.output), indent=2))
    except (ValueError, OSError) as error:
        print(f'error: {error}', file=sys.stderr)
        raise SystemExit(2)
