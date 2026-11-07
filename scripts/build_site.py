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
    write_story(ROOT/'examples/stack-diagram/portable-builder.json',graph)
    site=ROOT/'site';assets=site/'assets';assets.mkdir(parents=True,exist_ok=True)
    shutil.copy2(ROOT/'skills/repo-visualizer/assets/fonts/AtkinsonHyperlegibleNext.ttf',assets)
    shutil.copy2(ROOT/'skills/repo-visualizer/assets/fonts/OFL-AtkinsonHyperlegibleNext.txt',assets)
    write_html(site/'index.html',build_html(graph,landing=True))
    write_html(site/'portable-builder.html',build_html(graph))
    print('Built public landing page and offline example')
if __name__=='__main__':build()
