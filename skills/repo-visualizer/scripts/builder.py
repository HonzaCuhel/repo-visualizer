"""Assemble the local player, graph and vendored layout engine into portable HTML."""
from __future__ import annotations

import base64
import hashlib
import html
import json
from pathlib import Path
import re
import tempfile

from story_model import StoryError, validate_structure

ASSETS = Path(__file__).resolve().parent.parent / 'assets'


def safe_json(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':')).replace('&', '\\u0026').replace('<', '\\u003c').replace('>', '\\u003e').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')


def build_html(data, *, landing=False):
    story = validate_structure(data)
    for source in story['sources']:
        if not isinstance(source.get('excerpt'), str) or not re.fullmatch(r'[a-f0-9]{64}', source.get('sha256', '')):
            raise StoryError('build needs prepared source excerpts and fingerprints; run prepare first')
        expected = hashlib.sha256(source['excerpt'].encode('utf-8')).hexdigest()
        if source.get('excerpt_sha256') != expected:
            raise StoryError('source excerpt fingerprint does not match; run prepare against the repository')
        # Only the builder's pinned GitHub permalink is navigable. All source text is data.
        source.pop('url', None)
        commit = source.get('commit', '')
        origin = story['repo'].get('url', '') or ''
        if source.get('revision') == 'commit' and re.fullmatch(r'[a-f0-9]{40,64}', commit) and re.fullmatch(r'https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', origin):
            from urllib.parse import quote
            source['url'] = f"{origin}/blob/{commit}/{quote(source['path'], safe='/')}#L{source['start']}-L{source['end']}"
    template = (ASSETS / 'player.html').read_text(encoding='utf-8')
    mark = (ASSETS / 'brand-mark.svg').read_text(encoding='utf-8').strip()
    icon = mark.replace('</svg>', '<style>@media(prefers-color-scheme:dark){svg{color:#8bb9ff}}</style></svg>')
    replacements = {
        '@@BRAND_MARK@@': mark.replace('<svg ', '<svg aria-hidden="true" ', 1),
        '@@BRAND_CSS@@': (ASSETS / 'brand.css').read_text(encoding='utf-8'),
        '@@FAVICON@@': 'data:image/svg+xml;base64,' + base64.b64encode(icon.encode('utf-8')).decode(),
        '@@APPEARANCE@@': (ASSETS / 'appearance.js').read_text(encoding='utf-8'),
        '@@BODY_CLASS@@': 'landing' if landing else 'standalone',
        '@@UI_CONFIG@@': safe_json({'language': story['language'], 'ui_strings': story.get('ui_strings', {}), 'content_languages': [story['language'], *story.get('translations', {})], 'landing': landing}),
        '@@LOCALES@@': safe_json({language: json.loads((ASSETS / 'locales' / (language+'.json')).read_text(encoding='utf-8')) for language in ('en', 'cs', 'de', 'fr', 'es')}),
        '@@LANG@@': html.escape(story['language'], quote=True),
        '@@TITLE@@': html.escape(story['title']),
        '@@STORY@@': safe_json(story),
        '@@CSS@@': (ASSETS / 'player.css').read_text(encoding='utf-8'),
        '@@INTERACTION@@': (ASSETS / 'interaction.js').read_text(encoding='utf-8'),
        '@@JS@@': (ASSETS / 'player.js').read_text(encoding='utf-8'),
        '@@ELK@@': (ASSETS / 'vendor/elk.bundled.js').read_text(encoding='utf-8').replace('</script', '<\\/script'),
        '@@GIFENC@@': (ASSETS / 'vendor/gifenc.js').read_text(encoding='utf-8').replace('</script', '<\\/script'),
        '@@GIF_LICENSE@@': html.escape((ASSETS / 'vendor/GIFENC-LICENSE.txt').read_text(encoding='utf-8')),
        '@@FONT_URL@@': 'assets/AtkinsonHyperlegibleNext.ttf' if landing else 'data:font/ttf;base64,'+base64.b64encode((ASSETS / 'fonts/AtkinsonHyperlegibleNext.ttf').read_bytes()).decode(),
        '@@FONT@@': base64.b64encode((ASSETS / 'fonts/AtkinsonHyperlegibleNext.ttf').read_bytes()).decode(),
        '@@FONT_LICENSE@@': html.escape((ASSETS / 'fonts/OFL-AtkinsonHyperlegibleNext.txt').read_text(encoding='utf-8')),
        '@@ELK_LICENSE@@': html.escape((ASSETS / 'vendor/ELK-LICENSE.md').read_text(encoding='utf-8')),
        '@@LANDING@@': 'true' if landing else 'false',
        '@@PLAYER_LICENSE@@': html.escape((ASSETS.parent / 'LICENSE').read_text(encoding='utf-8')),
        '@@SOURCE_LICENSE@@': html.escape(story.get('source_license') or 'No repository license text was included. Source excerpts retain their original authorship and permissions.'),
    }
    # One pass: placeholder-looking repository strings must not be interpreted as templates.
    return re.sub(r'@@[A-Z_]+@@', lambda match: replacements[match.group()], template)


def write_html(path, document):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = None
    try:
        with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=path.parent, prefix=path.name+'.', suffix='.tmp', delete=False) as stream:
            tmp = Path(stream.name)
            stream.write(document)
        tmp.replace(path)
    finally:
        if tmp is not None:
            tmp.unlink(missing_ok=True)
