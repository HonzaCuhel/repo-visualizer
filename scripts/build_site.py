#!/usr/bin/env python3
"""Build the public, static showcase from an attributed public-source graph."""
import json
from pathlib import Path
import shutil
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/repo-visualizer/scripts'))
from builder import build_html,write_html
from story_model import read_story,write_story

def build():
    graph=read_story(ROOT/'examples/stack-diagram/graph.json')
    # The landing question is the portable builder; the separate PNG renderer
    # stays available in the full example, rather than elongating this scope.
    graph['nodes']=[n for n in graph['nodes'] if n.get('group')=='build']
    ids={n['id'] for n in graph['nodes']}
    graph['edges']=[e for e in graph['edges'] if e['from'] in ids and e['to'] in ids]
    graph['groups']=[g for g in graph['groups'] if g['id']=='build']
    graph['steps']=[s for s in graph['steps'] if all(i in ids for i in s['node_ids'])]
    graph['scenarios']=[dict(id='builder',label='Build a portable diagram',step_ids=[s['id'] for s in graph['steps']])]
    refs={r for n in graph['nodes'] for r in n['source_ids']}|{r for e in graph['edges'] for r in e['source_ids']}|{r for s in graph['steps'] for r in s['source_ids']}
    graph['sources']=[s for s in graph['sources'] if s['id'] in refs]
    graph['uncertainties']=['Static source analysis at a pinned revision; not a recorded execution.','The separate PNG renderer, icon fetcher and sharing service are outside this focused example.','Source: caru-ini/stack-diagram, MIT, copyright 2026 caru-ini.']
    translated=json.loads((ROOT/'site-src/demo-cs.json').read_text())
    for field in ('nodes','edges','groups','steps'):
        allowed={item['id'] for item in graph[field]}
        translated[field]={key:value for key,value in translated[field].items() if key in allowed}
    translated['scenarios']={'builder':{'label':'Sestavit přenositelný diagram'}}
    translated['uncertainties'][1]='Samostatné vykreslení PNG, stahování ikon a sdílecí služba jsou mimo rozsah této zaměřené ukázky.'
    graph['translations']={'cs':translated}
    write_story(ROOT/'examples/stack-diagram/portable-builder.json',graph)
    site=ROOT/'site';assets=site/'assets';assets.mkdir(parents=True,exist_ok=True)
    shutil.copy2(ROOT/'skills/repo-visualizer/assets/fonts/AtkinsonHyperlegibleNext.ttf',assets)
    shutil.copy2(ROOT/'skills/repo-visualizer/assets/fonts/OFL-AtkinsonHyperlegibleNext.txt',assets)
    document=build_html(graph,landing=True)
    document=document.replace('</head>', '<meta name="description" content="Understand how a repository works. Explore source-grounded component graphs and export HTML, GIF and video with an open skill for Codex and Claude Code.">\n<link rel="icon" href="favicon.svg" type="image/svg+xml">\n<meta property="og:title" content="Repo Visualizer — understand how the code works">\n<meta property="og:description" content="A component graph you can explore, verify against source, and share as HTML or video.">\n<meta property="og:image" content="https://HonzaCuhel.github.io/repo-visualizer/media/poster.png">\n<meta property="og:url" content="https://HonzaCuhel.github.io/repo-visualizer/">\n<style id="site-style">'+(ROOT/'site-src/site.css').read_text()+'</style>\n</head>',1)
    hero='<div class="hero-actions landing-only"><a class="hero-install" href="#install"><span data-site="heroInstall">Install skill</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v12m-5-5 5 5 5-5M4 17v4h16v-4"/></svg></a><a class="hero-explore" href="#workspace" data-site="heroExplore">Explore the graph</a></div><p class="hero-meta landing-only" data-site="heroMeta">Codex + Claude Code · Open source · Local exports</p>'
    document=document.replace('</section>',hero+'\n</section>',1)
    document=document.replace('</main>', (ROOT/'site-src/sections.html').read_text()+'\n</main>',1)
    document=document.replace('</body>','<script id="site-locales" type="application/json">'+(ROOT/'site-src/locales.json').read_text().replace('<','\\u003c')+'</script><script id="site-script">'+(ROOT/'site-src/site.js').read_text()+'</script>\n</body>',1)
    write_html(site/'index.html',document)
    write_html(site/'portable-builder.html',build_html(graph))
    full=read_story(ROOT/'examples/stack-diagram/graph.json')
    full['translations']={'cs':json.loads((ROOT/'site-src/demo-cs.json').read_text())}
    write_html(site/'full-pipeline.html',build_html(full))
    (site/'.nojekyll').touch()
    (site/'favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><g fill="white" stroke="%232164c7" stroke-width="1.5"><path d="M12 7v4M5 11h14M5 11v4M19 11v4"/><rect x="8" y="2" width="8" height="5" rx="1"/><rect x="1" y="15" width="8" height="6" rx="1"/><rect x="15" y="15" width="8" height="6" rx="1"/></g></svg>'.replace('%23','#'))
    print('Built public landing page and offline example')
if __name__=='__main__':build()
