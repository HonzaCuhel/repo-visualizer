from pathlib import Path
import json,os,sys,tempfile,unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'skills/repo-visualizer/scripts'))
from builder import build_html,write_html
from story_model import prepare_story,validate_structure,StoryError,read_story

def fixture(root):
 (root/'source.py').write_text('value = 1\n')
 return prepare_story(dict(schema_version=1,title='Sample',question='How?',language='cs',sources=[dict(id='s',path='source.py',start=1,end=1)],groups=[dict(id='outer',label='Outer'),dict(id='inner',label='Inner',parent='outer')],nodes=[dict(id='a',label='Alpha',group='inner',source_ids=['s']),dict(id='b',label='Beta',group='inner',source_ids=['s']),dict(id='c',label='Gamma',group='outer',source_ids=['s'])],edges=[dict(id='ab',**{'from':'a','to':'b'},label='calls',source_ids=['s']),dict(id='ba',**{'from':'b','to':'a'},label='retry',source_ids=['s']),dict(id='bc',**{'from':'b','to':'c'},label='returns',source_ids=['s'])]),root)

class LocalizationModelTests(unittest.TestCase):
 def test_translations_cannot_rewrite_topology_or_evidence(self):
  with tempfile.TemporaryDirectory() as directory:
   graph=fixture(Path(directory));graph['translations']={'en':{'nodes':{'a':{'label':'First'}}}}
   self.assertEqual(validate_structure(graph)['nodes'][0]['label'],'Alpha')
   for field in ['source_ids','id','kind']:
    graph['translations']={'en':{'nodes':{'a':{field:'changed'}}}}
    with self.assertRaises(StoryError):validate_structure(graph)
   graph['translations']={'en':{'edges':{'ab':{'from':'c'}}}}
   with self.assertRaises(StoryError):validate_structure(graph)

@unittest.skipUnless(os.environ.get('REPO_VISUALIZER_BROWSER'),'Set REPO_VISUALIZER_BROWSER for browser integration')
class LocalizationBrowserTests(unittest.TestCase):
 def setUp(self):
  from playwright.sync_api import sync_playwright
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.runtime=sync_playwright().start();self.browser=self.runtime.chromium.launch(executable_path=os.environ['REPO_VISUALIZER_BROWSER']);self.page=self.browser.new_page(viewport={'width':1440,'height':1000},reduced_motion='reduce');self.errors=[];self.page.on('pageerror',lambda e:self.errors.append(str(e)));self.page.route('http://**/*',lambda r:r.abort());self.page.route('https://**/*',lambda r:r.abort())
 def tearDown(self):
  self.browser.close();self.runtime.stop();self.tmp.cleanup()
 def open(self,graph):
  path=self.root/'graph.html';write_html(path,build_html(graph));self.page.goto(path.as_uri());self.page.evaluate('window.repoReady');return path
 def test_locale_switch_keeps_graph_evidence_selection_and_offline_download(self):
  graph=fixture(self.root);graph['summary']='Full detailed context. '+('More detail. '*35);graph['overview']={'lead':'A concise introduction.','path':[{'node_id':'a','label':'Frontend'}]};graph['repo']['commit']='abcdef0123456789abcdef0123456789abcdef01';graph['translations']={'en':{'nodes':{'a':{'label':'First component'}}}};self.open(graph)
  self.assertEqual(self.page.locator('#page-description').inner_text(),'A concise introduction.');self.assertEqual(self.page.locator('#intro-metadata code').inner_text(),'abcdef0');self.assertTrue(self.page.locator('#intro-details').is_visible());self.assertEqual(self.page.locator('#overview-path button').count(),1);self.assertEqual(self.page.locator('#code-tab').inner_text(),'Kód');self.assertEqual(self.page.locator('#page-title').inner_text(),'Sample')
  self.page.evaluate('repoPlayer.selectNode("a")');self.page.locator('#language-select').select_option('en');self.page.evaluate('window.repoLocaleReady')
  self.assertEqual(self.page.locator('#selection-title').inner_text(),'First component');self.assertEqual(self.page.evaluate('repoPlayer.graph.sources[0].excerpt'),graph['sources'][0]['excerpt'])
  self.assertEqual(self.page.evaluate('repoPlayer.graph.edges.map(e=>[e.from,e.to])'),[['a','b'],['b','a'],['b','c']])
  self.page.locator('#theme-select').select_option('dark');self.assertEqual(self.page.evaluate('document.documentElement.dataset.theme'),'dark')
  svg=self.page.evaluate('repoPlayer.exportSVG()');self.assertIn('data-theme="dark"',svg);self.assertIn('--paper:#10141b',svg.replace(' ',''))
  with self.page.expect_download() as download:self.page.evaluate('repoPlayer.export("html")')
  out=self.root/'copy.html';download.value.save_as(out);self.page.goto(out.as_uri());self.page.evaluate('window.repoReady');self.assertEqual(self.page.evaluate('document.documentElement.dataset.theme'),'dark');self.assertEqual(self.page.locator('#selection-title').inner_text(),'First component');self.assertEqual(self.errors,[])
 def test_custom_language_and_untrusted_translation_are_plain_text(self):
  graph=fixture(self.root);graph['language']='fr';graph['ui_strings']={'languageName':'Français','code':'Code source','openSource':'Ouvrir la source','map':'Carte <img src=x onerror="window.PWNED=1">'};self.open(graph)
  self.assertEqual(self.page.locator('#code-tab').inner_text(),'Code source');self.assertIsNone(self.page.evaluate('window.PWNED'));self.assertEqual(self.page.locator('[data-view=map] img').count(),0);self.assertEqual(self.page.locator('#language-select').input_value(),'fr');self.assertEqual(self.errors,[])
 def test_nested_group_edges_attach_to_their_actual_components(self):
  self.open(fixture(self.root))
  failures=self.page.evaluate('''()=>{const errors=[];for(const g of document.querySelectorAll('.graph-edge')){const edge=repoPlayer.graph.edges.find(e=>e.id===g.dataset.edge);const paths=g.querySelectorAll('.edge-line');for(const [path,which,id] of [[paths[0],0,edge.from],[paths[paths.length-1],1,edge.to]]){const p=path.getPointAtLength(which?path.getTotalLength():0),point=new DOMPoint(p.x,p.y).matrixTransform(path.getScreenCTM()),rect=document.querySelector('.graph-node[data-node="'+id+'"] rect').getBoundingClientRect();if(point.x<rect.x-3||point.x>rect.right+3||point.y<rect.y-3||point.y>rect.bottom+3)errors.push({edge:edge.id,id,x:point.x,y:point.y,rect:{x:rect.x,y:rect.y,w:rect.width,h:rect.height}})}}return errors}''')
  self.assertEqual(failures,[]);self.assertEqual(self.errors,[])

if __name__=='__main__':unittest.main()
