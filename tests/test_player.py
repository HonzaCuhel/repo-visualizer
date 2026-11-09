from pathlib import Path
import json
import os
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/repo-visualizer/scripts'))
from builder import build_html,write_html
from story_model import prepare_story,read_story

@unittest.skipUnless(os.environ.get('REPO_VISUALIZER_BROWSER'),'Set REPO_VISUALIZER_BROWSER for browser integration')
class PlayerTests(unittest.TestCase):
    def setUp(self):
        from playwright.sync_api import sync_playwright
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        self.runtime=sync_playwright().start();self.browser=self.runtime.chromium.launch(executable_path=os.environ['REPO_VISUALIZER_BROWSER'])
        self.page=self.browser.new_page(viewport={'width':1440,'height':900},reduced_motion='reduce');self.errors=[];self.requests=[]
        self.page.on('pageerror',lambda e:self.errors.append(str(e)))
        self.page.route('https://**/*',lambda route:(self.requests.append(route.request.url),route.abort()))
        self.page.route('http://**/*',lambda route:(self.requests.append(route.request.url),route.abort()))

    def tearDown(self):
        self.browser.close();self.runtime.stop();self.tmp.cleanup()

    def open(self,graph,landing=False):
        if landing:
            import shutil
            assets=self.root/'assets';assets.mkdir(exist_ok=True)
            shutil.copy2(ROOT/'skills/repo-visualizer/assets/fonts/AtkinsonHyperlegibleNext.ttf',assets)
        out=self.root/'graph.html';write_html(out,build_html(graph,landing=landing));self.page.goto(out.as_uri());self.page.evaluate('window.repoReady');return out

    def test_public_graph_is_offline_interactive_and_seekable(self):
        graph=read_story(ROOT/'examples/stack-diagram/graph.json');self.open(graph)
        self.assertEqual(self.page.locator('.graph-node').count(),len(graph['nodes']))
        self.assertEqual(self.page.locator('.graph-edge').count(),len(graph['edges']))
        self.page.get_by_role('button',name='Icon assets',exact=True).click()
        self.assertEqual(self.page.locator('#selection-title').inner_text(),'Icon assets')
        self.page.locator('#code-tab').click()
        self.assertIn('for f in sorted(icondir.iterdir())',self.page.locator('#source-content pre').inner_text())
        self.assertIn('#L36-L41',self.page.locator('#source-content a').get_attribute('href'))
        self.page.get_by_role('button',name='Focus',exact=True).click()
        self.assertGreater(self.page.locator('.is-dimmed').count(),0)
        self.page.get_by_role('button',name='Path',exact=True).click()
        first=self.page.evaluate('window.renderAt(0)');last=self.page.evaluate('window.renderAt(11000)')
        self.assertNotEqual(first['nodeIds'],last['nodeIds'])
        self.assertGreater(self.page.locator('.graph-edge.is-active').count(),0)
        again=self.page.evaluate('window.renderAt(0)');self.assertEqual(first,again)
        self.page.locator('#component-search').fill('nothing-matches-this')
        self.assertTrue(self.page.locator('#no-components').is_visible())
        self.page.locator('#component-search').fill('')
        self.assertEqual(self.page.locator('.component-item').count(),len(graph['nodes']))
        self.assertFalse(self.page.evaluate('repoPlayer.isPlaying'))
        self.assertEqual(self.requests,[]);self.assertEqual(self.errors,[])

    def test_downloaded_html_reopens_offline_with_working_controls(self):
        graph=read_story(ROOT/'examples/stack-diagram/graph.json');self.open(graph,landing=True)
        with self.page.expect_download() as download:
            self.page.evaluate('repoPlayer.export("html")')
        offline=self.root/'offline';offline.mkdir()
        saved=offline/'downloaded.html';download.value.save_as(saved)
        self.page.goto(saved.as_uri());self.page.evaluate('window.repoReady')
        self.assertNotIn('src:url(assets/AtkinsonHyperlegibleNext.ttf)',saved.read_text())
        self.assertTrue(self.page.evaluate('[...document.fonts].filter(f=>f.family==="Atkinson").every(f=>f.status==="loaded")'))
        self.assertFalse(self.page.locator('body').evaluate('(e)=>e.classList.contains("export-busy")'))
        self.assertEqual(self.page.locator('.wordmark .brand-mark').count(),1)
        self.assertEqual(self.page.locator('#brand-style').count(),1)
        self.assertEqual(self.page.locator('.site-header > .install-button').evaluate('(e)=>getComputedStyle(e).fontSize'),'13px')
        self.assertEqual(self.page.locator('.site-header .theme-switch').evaluate('(e)=>getComputedStyle(e).borderRadius'),'20px')
        self.assertEqual(self.page.locator('#language-menu [role=option]').count(),5)
        self.page.locator('#language-toggle').click()
        self.page.locator('#language-menu [data-language-choice=cs]').click()
        self.assertEqual(self.page.evaluate('repoAppearance.language'),'cs')
        self.page.locator('#language-toggle').click()
        self.page.locator('#language-menu [data-language-choice=en]').click()
        self.assertEqual(self.page.evaluate('repoAppearance.language'),'en')
        self.page.get_by_role('button',name='Icon assets',exact=True).click()
        self.assertEqual(self.page.locator('#selection-title').inner_text(),'Icon assets')
        self.assertEqual(self.requests,[]);self.assertEqual(self.errors,[])

    def test_complex_topology_and_hostile_labels_survive_without_code_execution(self):
        source=self.root/'fixture.py';source.write_text("raise RuntimeError('target must never execute')\n")
        label='</script><img src=x onerror="window.PWNED=1">'
        graph=prepare_story(dict(schema_version=1,title=label,question='Complex topology?',default_view='focus',sources=[dict(id='s',path='fixture.py',start=1,end=1)],groups=[dict(id='outer',label='Outer'),dict(id='inner',label='Inner',parent='outer')],nodes=[dict(id='a',label=label,group='inner',source_ids=['s']),dict(id='b',label='B',group='outer',source_ids=['s']),dict(id='c',label='Disconnected',source_ids=['s'])],edges=[dict(id='ab',**{'from':'a','to':'b'},label='calls',source_ids=['s']),dict(id='ab2',**{'from':'a','to':'b'},label='updates',source_ids=['s']),dict(id='ba',**{'from':'b','to':'a'},label='retry',source_ids=['s']),dict(id='self',**{'from':'b','to':'b'},label='repeat',source_ids=['s'])]),self.root)
        self.open(graph)
        self.assertEqual(self.page.locator('.graph-node').count(),3);self.assertEqual(self.page.locator('.graph-edge').count(),4)
        self.assertEqual(self.page.locator('.graph-group').count(),2)
        self.assertEqual(self.page.evaluate('repoPlayer.view'),'focus')
        self.assertTrue(self.page.locator('.graph-node[data-node="c"]').evaluate('(e)=>e.classList.contains("is-dimmed")'))
        self.assertIsNone(self.page.evaluate('window.PWNED'))
        self.assertIn(label,self.page.locator('#selection-title').inner_text())
        self.assertEqual(self.page.evaluate('repoPlayer.graph.edges.map(e=>e.id)'),['ab','ab2','ba','self'])
        self.assertEqual(self.page.evaluate('repoPlayer.graph.steps'),[])
        self.assertIn('not execution order',self.page.locator('#tour-note').inner_text())
        self.assertFalse(self.page.locator('#diagram').get_attribute('viewBox').find('NaN')>=0)
        self.assertEqual(self.errors,[])

    def test_shared_flow_bands_route_real_edges_and_expanded_download_restores_workspace(self):
        source=self.root/'fixture.py';source.write_text('value = 1\n')
        names=['gateway','a','b','c','root','state']
        pairs=[('a','b'),('b','c'),('c','a'),('a','b'),('b','b'),('gateway','a'),('gateway','b'),('gateway','b'),('c','state'),('state','a'),('gateway','state'),('state','state')]
        graph=prepare_story(dict(schema_version=1,title='A real topology fixture',question='How are shared services reused?',presentation={'layout':'flow','top':['gateway'],'bottom':['state']},sources=[dict(id='s',path='fixture.py',start=1,end=1)],nodes=[dict(id=n,label=n,caption='Shared responsibility' if n in ('gateway','state') else 'A short responsibility caption',source_ids=['s']) for n in names],edges=[dict(id='e'+str(i),**{'from':a,'to':b},label='relationship '+str(i),source_ids=['s']) for i,(a,b) in enumerate(pairs)]),self.root)
        self.open(graph)
        self.assertEqual(self.page.locator('#diagram').get_attribute('data-layout'),'flow')
        self.assertEqual(self.page.locator('.shared-band').count(),2)
        self.assertEqual(self.page.locator('.graph-node').count(),6)
        self.assertEqual(self.page.locator('.graph-edge').count(),len(pairs))
        # Check actual rendered endpoints and sampled paths, including parallel,
        # cyclic, shared-to-shared, self and disconnected components.
        issues=self.page.evaluate("""()=>{const issues=[],rects=new Map([...document.querySelectorAll('.graph-node')].map(e=>{let m=e.transform.baseVal.consolidate().matrix,r=e.querySelector('rect');return [e.dataset.node,{x:m.e,y:m.f,w:+r.getAttribute('width'),h:+r.getAttribute('height')}]}));const attached=(p,r)=>((Math.abs(p.x-r.x)<1||Math.abs(p.x-r.x-r.w)<1)&&p.y>=r.y-1&&p.y<=r.y+r.h+1)||((Math.abs(p.y-r.y)<1||Math.abs(p.y-r.y-r.h)<1)&&p.x>=r.x-1&&p.x<=r.x+r.w+1);for(const e of repoPlayer.graph.edges){let paths=document.querySelector('[data-edge="'+e.id+'"]').querySelectorAll('.edge-line');let first=paths[0],last=paths[paths.length-1];if(!attached(first.getPointAtLength(0),rects.get(e.from))||!attached(last.getPointAtLength(last.getTotalLength()),rects.get(e.to)))issues.push(e.id+' endpoint');for(const path of paths)for(let i=2;i<path.getTotalLength()-2;i+=4){const p=path.getPointAtLength(i);for(const [id,r]of rects)if(id!==e.from&&id!==e.to&&p.x>r.x+1&&p.x<r.x+r.w-1&&p.y>r.y+1&&p.y<r.y+r.h-1)issues.push(e.id+' crosses '+id)}}return [...new Set(issues)]}""")
        self.assertEqual(issues,[])
        self.page.locator('#expand-diagram').click()
        self.page.wait_for_function('document.querySelector("#diagram-dialog").open && !document.querySelector("#expand-diagram").disabled')
        with self.page.expect_download() as download:self.page.evaluate('repoPlayer.export("html")')
        saved=self.root/'expanded-download.html';download.value.save_as(saved)
        self.page.goto(saved.as_uri());self.page.evaluate('repoReady')
        self.assertEqual(self.page.locator('#workspace > .graph-pane').count(),1)
        self.assertFalse(self.page.locator('#diagram-dialog').evaluate('(e)=>e.open'))
        self.page.locator('#expand-diagram').click();self.page.wait_for_function('!document.querySelector("#expand-diagram").disabled')
        self.page.locator('#expand-diagram').press('Escape');self.page.wait_for_function('!document.querySelector("#diagram-dialog").open && !document.querySelector("#expand-diagram").disabled')
        self.assertEqual(self.page.evaluate('document.activeElement.id'),'expand-diagram')
        self.assertEqual(self.errors,[])

    def test_auto_flow_respects_geometry_cycles_and_resize(self):
        source=self.root/'fixture.py';source.write_text('value = 1\n')
        def make(cycle=False):
            return prepare_story(dict(schema_version=1,title='Simple chain',question='How does the chain work?',sources=[dict(id='s',path='fixture.py',start=1,end=1)],nodes=[dict(id=n,label=n,caption='A short explanation',source_ids=['s'])for n in ['a','b','c']],edges=[dict(id='ab',**{'from':'a','to':'b'},source_ids=['s']),dict(id='bc',**{'from':'b','to':'c'},source_ids=['s'])]+([dict(id='ca',**{'from':'c','to':'a'},source_ids=['s'])]if cycle else [])),self.root)
        self.open(make());self.assertEqual(self.page.locator('#diagram').get_attribute('data-layout'),'flow')
        self.page.set_viewport_size({'width':390,'height':900});self.page.wait_for_function('document.querySelector("#diagram").dataset.layout==="layered"')
        self.page.set_viewport_size({'width':1440,'height':900});self.page.wait_for_function('document.querySelector("#diagram").dataset.layout==="flow"')
        self.open(make(True));self.assertEqual(self.page.locator('#diagram').get_attribute('data-layout'),'layered')
        self.assertEqual(self.page.locator('.node-caption').count(),3)
        self.assertEqual(self.errors,[])

    def test_mobile_expansion_has_readable_text_and_explicit_fit_is_respected(self):
        self.page.set_viewport_size({'width':390,'height':844})
        self.open(read_story(ROOT/'examples/whisper/decoder-loop.json'))
        self.page.locator('#expand-diagram').click()
        self.page.wait_for_function('document.querySelector("#diagram-dialog").open && !document.querySelector("#expand-diagram").disabled')
        scale=self.page.locator('#diagram').evaluate('(e)=>{let m=e.getScreenCTM();return Math.hypot(m.a,m.b)}')
        self.assertGreaterEqual(14*scale,12)
        self.assertTrue(self.page.locator('#diagram-hint').is_visible())
        self.page.evaluate('renderAt(9000)')
        visible=self.page.locator('.graph-node[data-node=logits] .node-title').evaluate('(e)=>{let t=e.getBoundingClientRect(),s=document.querySelector("#diagram").getBoundingClientRect();return t.top>=s.top&&t.bottom<=s.bottom&&t.left>=s.left&&t.right<=s.right}')
        self.assertTrue(visible)
        self.page.locator('#zoom-fit').click()
        overview=self.page.locator('#diagram').get_attribute('viewBox')
        self.page.evaluate('renderAt(0)');self.page.wait_for_timeout(180)
        self.assertEqual(self.page.locator('#diagram').get_attribute('viewBox'),overview)
        self.assertTrue(self.page.locator('#diagram-hint').is_hidden())
        self.page.locator('#expand-diagram').press('Escape')
        self.page.wait_for_function('!document.querySelector("#diagram-dialog").open && !document.querySelector("#expand-diagram").disabled')
        self.assertEqual(self.page.locator('#workspace > .graph-pane').count(),1)
        self.assertEqual(self.errors,[])

    def test_ordered_phases_align_parallel_nodes_and_keep_the_entire_expanded_workspace(self):
        (self.root/'fixture.py').write_text('value = 1\n')
        levels=[['input'],['a','b','detached'],['join'],['output']]
        ids=['output','b','join','input','a','detached']
        pairs=[('input','a'),('input','b'),('a','join'),('b','join'),('join','output'),('join','a'),('b','b'),('a','join')]
        graph=prepare_story(dict(schema_version=1,title='Parallel request',question='How does the request finish?',presentation={'levels':levels},sources=[dict(id='s',path='fixture.py',start=1,end=1)],nodes=[dict(id=identity,label='A deliberately longer branch title that wraps'if identity=='b'else identity,caption='A responsibility',kind='input'if identity=='input'else 'output'if identity=='output'else 'process',source_ids=['s'])for identity in ids],edges=[dict(id='e'+str(index),**{'from':a,'to':b},label='relationship '+str(index),source_ids=['s'])for index,(a,b)in enumerate(pairs)]),self.root)
        self.open(graph)
        for width in (390,768,1440):
            self.page.set_viewport_size({'width':width,'height':1000})
            self.assertEqual(self.page.locator('#diagram').get_attribute('data-layout'),'ordered')
            positions=self.page.evaluate('Object.fromEntries(repoPlayer.layout.children.map(n=>[n.id,{y:n.y,h:n.height}]))')
            for row in levels:
                self.assertLess(max(positions[i]['y']for i in row)-min(positions[i]['y']for i in row),0.01)
            for first,second in zip(levels,levels[1:]):
                self.assertLess(max(positions[i]['y']+positions[i]['h']for i in first),min(positions[i]['y']for i in second))
        self.assertEqual(self.page.locator('#component-list button').evaluate_all('(items)=>items.map(item=>item.dataset.node)'),[i for row in levels for i in row])
        self.assertEqual(self.page.locator('#component-list [data-level="1"] .component-order').all_text_contents(),['2','2','2'])
        self.page.evaluate("repoPlayer.setScenario('tour');renderAt(2400)")
        self.assertEqual(self.page.locator('.graph-node.is-selected').get_attribute('data-node'),'a')
        self.page.locator('#expand-diagram').click();self.page.wait_for_function('document.querySelector("#diagram-dialog").open&&!document.querySelector("#expand-diagram").disabled')
        self.assertEqual(self.page.locator('#diagram-dialog #workspace').count(),1)
        for selector in ('.component-pane','.graph-pane','.inspector'):
            self.assertTrue(self.page.locator('#diagram-dialog '+selector).is_visible())
        self.page.locator('#component-list [data-node=b]').click();self.page.locator('#inspect-expanded').click()
        self.assertTrue(self.page.locator('#diagram-dialog').evaluate('(element)=>element.open'))
        self.assertGreater(self.page.locator('#source-content pre').count(),0)
        self.assertEqual(self.page.locator('.graph-node.is-selected').get_attribute('data-node'),'b')
        with self.page.expect_download()as download:self.page.evaluate("repoPlayer.export('html')")
        output=self.root/'complete-workspace.html';download.value.save_as(output);self.page.goto(output.as_uri());self.page.evaluate('repoReady')
        self.assertEqual(self.page.locator('#workspace').count(),1)
        self.assertEqual(self.page.locator('#diagram-dialog #workspace').count(),0)
        self.assertFalse(self.page.locator('#diagram-dialog').evaluate('(element)=>element.open'))
        self.page.locator('#expand-diagram').click();self.page.wait_for_function('!document.querySelector("#expand-diagram").disabled');self.page.locator('#close-workspace').click();self.page.wait_for_function('!document.querySelector("#diagram-dialog").open&&!document.querySelector("#expand-diagram").disabled')
        self.assertEqual(self.page.evaluate('document.activeElement.id'),'expand-diagram')
        self.assertEqual(self.errors,[])

    def test_cached_flow_video_scene_preserves_shared_band_typography(self):
        from hyperframes_export import composition
        source=self.open(read_story(ROOT/'examples/whisper/decoder-loop.json'))
        self.page.evaluate("document.body.classList.add('export-frame');repoPlayer.setView('path')")
        layout=self.page.evaluate('repoPlayer.layout')
        self.assertIn('typography',layout)
        output=self.root/'composition.html'
        output.write_text(composition(source.read_text(),12000,1440,900,8,layout=layout))
        self.page.goto(output.as_uri());self.page.evaluate('window.__hf.buildReady.repoVisualizer')
        self.assertEqual(self.page.locator('.shared-band').count(),2)
        self.assertEqual(self.page.locator('.graph-node').count(),7)
        self.assertEqual(self.page.locator('.graph-edge').count(),7)
        overflow=self.page.evaluate("""()=>[...document.querySelectorAll('.shared-band')].some(n=>{let r=n.querySelector('rect').getBBox();return [...n.querySelectorAll('text')].some(t=>{let b=t.getBBox();return b.y<0||b.y+b.height>r.height+1||b.x<0||b.x+b.width>r.width+1})})""")
        self.assertFalse(overflow)
        self.page.evaluate('window.__timelines.root.seek(9)')
        self.assertGreater(self.page.locator('.graph-edge.is-active').count(),0)
        self.assertEqual(self.errors,[])

if __name__=='__main__':unittest.main()
