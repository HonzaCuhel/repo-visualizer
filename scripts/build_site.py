#!/usr/bin/env python3
"""Build the public, static showcase from an attributed public-source graph."""
import json
import base64
from pathlib import Path
import shutil
import re
import html
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/repo-visualizer/scripts'))
from builder import build_html,write_html
from story_model import read_story,write_story

def branded(document):
    mark=(ROOT/'site-src/brand-mark.svg').read_text().strip()
    icon=mark.replace('</svg>','<style>@media(prefers-color-scheme:dark){svg{color:#8bb9ff}}</style></svg>')
    data=base64.b64encode(icon.encode()).decode()
    document=document.replace('>repo-visualizer</a','>'+mark.replace('<svg ','<svg aria-hidden="true" ',1)+'<span>repo-visualizer</span></a',1)
    return document.replace('</head>','<link rel="icon" type="image/svg+xml" href="data:image/svg+xml;base64,'+data+'"><style id="brand-style">'+(ROOT/'site-src/brand.css').read_text()+'</style></head>',1)

def portable_builder_graph():
    graph=read_story(ROOT/'examples/stack-diagram/graph.json')
    # Keep the portable builder and the separate PNG renderer as two examples.
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
    return graph

def build():
    graph=read_story(ROOT/'examples/codex/agent-loop.json')
    portable=portable_builder_graph()
    site=ROOT/'site';assets=site/'assets';assets.mkdir(parents=True,exist_ok=True)
    shutil.copy2(ROOT/'skills/repo-visualizer/assets/fonts/AtkinsonHyperlegibleNext.ttf',assets)
    shutil.copy2(ROOT/'skills/repo-visualizer/assets/fonts/OFL-AtkinsonHyperlegibleNext.txt',assets)
    shutil.copy2(ROOT/'assets/plates/landscape.png',assets/'landscape.png')
    shutil.copy2(ROOT/'assets/fonts/RethinkSans.ttf',assets/'RethinkSans.ttf')
    shutil.copy2(ROOT/'assets/fonts/OFL-RethinkSans.txt',assets/'OFL-RethinkSans.txt')
    shutil.copy2(ROOT/'assets/icons/LICENSE-bootstrap-icons.txt',assets/'LICENSE-bootstrap-icons.txt')
    document=branded(build_html(graph,landing=True))
    def initial_appearance(match):
        config=json.loads(match.group(2))
        config['preference']={'theme':'light'}
        return match.group(1)+json.dumps(config,ensure_ascii=False).replace('<','\\u003c')+match.group(3)
    document=re.sub(r'(<script id="appearance-config" type="application/json">)(.*?)(</script>)',initial_appearance,document,count=1,flags=re.S)
    document=document.replace('<body class="landing">','<body class="landing"><div class="landscape landing-only" aria-hidden="true"><img src="assets/landscape.png" alt="" fetchpriority="high" decoding="async"></div>',1)
    document=document.replace('</head>', '<meta name="description" content="Understand how a repository works. Explore source-grounded component graphs and export HTML, GIF and video with an open skill for Codex and Claude Code.">\n<link rel="icon" href="favicon.svg" type="image/svg+xml">\n<meta property="og:title" content="Repo Visualizer — understand how the code works">\n<meta property="og:description" content="A component graph you can explore, verify against source, and share as HTML or video.">\n<meta property="og:image" content="https://HonzaCuhel.github.io/repo-visualizer/media/poster.png">\n<meta property="og:url" content="https://HonzaCuhel.github.io/repo-visualizer/">\n<style id="site-style">'+(ROOT/'site-src/site.css').read_text()+'</style><style id="landscape-style">'+(ROOT/'site-src/landscape.css').read_text()+'</style>\n</head>',1)
    document=document.replace('id="page-title" data-i18n="headline"','id="page-title" data-site="heroHeadline"',1)
    document=document.replace('data-i18n="subtitle"','data-site="heroSubtitle"',1)
    hero='''<div class="hero-actions landing-only"><a class="hero-install" href="#install" data-site="heroInstall">Install skill</a><a class="hero-explore" href="#workspace" data-site="heroExplore">Explore Codex</a></div><div class="hero-command landing-only"><code id="hero-command">npx skills add HonzaCuhel/repo-visualizer --skill repo-visualizer</code><button id="copy-hero" type="button" data-site-aria="copyCommand" aria-label="Copy command"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="8" y="4" width="12" height="14" rx="2"/><path d="M15 18v2H4V7h4"/></svg><span data-site="heroCopy">Copy</span></button></div><p id="hero-feedback" class="sr-only" role="status"></p>'''
    document=document.replace('</section>',hero+'\n</section>',1)
    footer_start=document.index('<footer')
    footer_end=document.index('</footer>',footer_start)
    footer=document[footer_start:footer_end]
    boundary=footer.rfind('</details>')
    footer=footer[:boundary]+'<p>GitHub icon: Bootstrap Icons · MIT.</p><pre>'+html.escape((ROOT/'assets/icons/LICENSE-bootstrap-icons.txt').read_text())+'</pre>'+footer[boundary:]
    document=document[:footer_start]+footer+document[footer_end:]
    document=document.replace('</footer>','<a class="font-credit" href="assets/OFL-RethinkSans.txt">Rethink Sans · OFL-1.1</a></footer>',1)
    document=document.replace('</main>', (ROOT/'site-src/sections.html').read_text()+'\n</main>',1)
    document=document.replace('</body>','<script id="site-locales" type="application/json">'+(ROOT/'site-src/locales.json').read_text().replace('<','\\u003c')+'</script><script id="site-script">'+(ROOT/'site-src/site.js').read_text()+'</script>\n</body>',1)
    github='<img class="github-mark" alt="" width="18" height="18" src="data:image/svg+xml;base64,'+base64.b64encode((ROOT/'assets/icons/github.svg').read_bytes()).decode()+'">'
    document=document.replace('>GitHub</a', '>'+github+'GitHub</a',1)
    document=document.replace('.landing-section,.landing-only,#site-script,#site-style,#site-locales', '.landing-section,.landing-only,#site-script,#site-style,#site-locales,#landscape-style')
    document=re.sub(r'</svg\s*>','</svg>',document)
    write_html(site/'index.html',document)
    write_html(site/'codex-shell.html',branded(build_html(read_story(ROOT/'examples/codex/graph.json'))))
    write_html(site/'codex-agent-loop.html',branded(build_html(graph)))
    write_html(site/'portable-builder.html',branded(build_html(portable)))
    full=read_story(ROOT/'examples/stack-diagram/graph.json')
    full['translations']={'cs':json.loads((ROOT/'site-src/demo-cs.json').read_text())}
    write_html(site/'full-pipeline.html',branded(build_html(full)))
    (site/'.nojekyll').touch()
    mark=(ROOT/'site-src/brand-mark.svg').read_text()
    (site/'favicon.svg').write_text(mark.replace('</svg>','<style>@media(prefers-color-scheme:dark){svg{color:#8bb9ff}}</style></svg>'))
    shutil.copy2(ROOT/'site-src/brand-mark.svg',assets/'brand-mark.svg')
    print('Built public landing page and offline example')
if __name__=='__main__':build()
