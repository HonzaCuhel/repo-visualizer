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

if __name__=='__main__':unittest.main()
