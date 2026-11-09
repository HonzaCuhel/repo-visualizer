from pathlib import Path
import copy,json,os,re,subprocess,sys,tempfile,unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'skills/repo-visualizer/scripts'))
from builder import build_html,write_html
from story_model import SUPPORTED_LANGUAGES,prepare_story,validate_structure,validate_language_coverage,StoryError,read_story

def fixture(root):
 (root/'source.py').write_text('value = 1\n')
 return prepare_story(dict(schema_version=1,title='Sample',question='How?',language='cs',sources=[dict(id='s',path='source.py',start=1,end=1)],groups=[dict(id='outer',label='Outer'),dict(id='inner',label='Inner',parent='outer')],nodes=[dict(id='a',label='Alpha',group='inner',source_ids=['s']),dict(id='b',label='Beta',group='inner',source_ids=['s']),dict(id='c',label='Gamma',group='outer',source_ids=['s'])],edges=[dict(id='ab',**{'from':'a','to':'b'},label='calls',source_ids=['s']),dict(id='ba',**{'from':'b','to':'a'},label='retry',source_ids=['s']),dict(id='bc',**{'from':'b','to':'c'},label='returns',source_ids=['s'])]),root)

def coverage_fixture(root):
 """Distinct display markers test coverage and rendering, not translation quality."""
 graph=fixture(root);graph.update(language='en',summary='Summary',overview={'lead':'Introduction','path':[{'node_id':'a','label':'First'},{'node_id':'b','label':'Second'}]},uncertainties=['Static interpretation.'])
 for node in graph['nodes']:node.update(description='Responsibility',caption='Short caption')
 graph['nodes'][0].update(evidence='inferred',reason='Inferred from configuration.')
 graph['edges'][0].update(evidence='inferred',reason='Indirect call.')
 graph['steps']=[dict(id='walk',title='Follow the call',description='Read the selected source.',node_ids=['a'],edge_ids=['ab'],source_ids=['s'],evidence='inferred',reason='Illustrative path.')]
 graph['scenarios']=[dict(id='main',label='A request',step_ids=['walk'])]
 fields={'nodes':['label','description','caption','reason'],'edges':['label','relation','reason'],'groups':['label'],'steps':['title','description','reason'],'scenarios':['label']}
 graph=validate_structure(graph)
 for language in ('cs','de','fr','es'):
  display={key:language+' '+graph[key]for key in ('title','question','summary')}
  display.update(uncertainties=[language+' limitation'],overview={'lead':language+' introduction','path':[{'node_id':item['node_id'],'label':language+' '+item['label']}for item in graph['overview']['path']]})
  for collection,names in fields.items():
   display[collection]={item['id']:{name:language+' '+item[name]for name in names if item.get(name)}for item in graph[collection]}
  graph.setdefault('translations',{})[language]=display
 return graph

class LocalizationModelTests(unittest.TestCase):
 def test_ordered_cli_requires_explicit_phases_without_rewriting_legacy_graphs(self):
  with tempfile.TemporaryDirectory()as directory:
   root=Path(directory);graph=fixture(root);draft=root/'legacy.json';draft.write_text(json.dumps(graph));output=root/'explorer.html';cli=ROOT/'skills/repo-visualizer/scripts/repo_story.py'
   args=[sys.executable,str(cli),'build',str(draft),'-o',str(output)]
   failed=subprocess.run(args+['--ordered'],capture_output=True,text=True);self.assertEqual(failed.returncode,2);self.assertIn('presentation.levels',failed.stderr);self.assertFalse(output.exists())
   self.assertEqual(subprocess.run(args,capture_output=True).returncode,0)
   graph['groups']=[]
   for node in graph['nodes']:node.pop('group')
   graph['presentation']={'levels':[['a'],['b','c']]};draft.write_text(json.dumps(graph))
   complete=subprocess.run(args+['--ordered'],capture_output=True,text=True);self.assertEqual(complete.returncode,0,complete.stderr)
   draft.write_text(json.dumps({'presentation':[]}));failed=subprocess.run(args+['--ordered'],capture_output=True,text=True);self.assertEqual(failed.returncode,2);self.assertNotIn('Traceback',failed.stderr)
 def test_complete_explanation_coverage_preserves_the_canonical_graph(self):
  with tempfile.TemporaryDirectory()as directory:
   graph=coverage_fixture(Path(directory));original=copy.deepcopy(graph)
   self.assertEqual(validate_language_coverage(graph),original);self.assertEqual(graph,original)
   # Identical names/symbols are legal; this check does not guess a language from prose.
   graph['translations']['fr']['nodes']['a']['label']=graph['nodes'][0]['label']
   validate_language_coverage(graph)
   graph['language']='en-GB';validate_language_coverage(graph)
 def test_complete_mode_rejects_missing_nested_text_and_shortened_caveats(self):
  with tempfile.TemporaryDirectory()as directory:
   graph=coverage_fixture(Path(directory))
   paths=[('title',),('question',),('summary',),('nodes','a','label'),('nodes','a','caption'),('nodes','a','description'),('nodes','a','reason'),('edges','ab','label'),('edges','ab','relation'),('edges','ab','reason'),('groups','inner','label'),('steps','walk','title'),('steps','walk','description'),('steps','walk','reason'),('scenarios','main','label'),('overview','lead'),('overview','path'),('uncertainties',)]
   for path in paths:
    with self.subTest(path=path):
     value=copy.deepcopy(graph);target=value['translations']['fr']
     for key in path[:-1]:target=target[key]
     del target[path[-1]]
     with self.assertRaisesRegex(StoryError,'fr:'):validate_language_coverage(value)
   graph['translations'].pop('de')
   with self.assertRaisesRegex(StoryError,'de:'):validate_language_coverage(graph)
 def test_translated_overview_preserves_component_identity_and_order(self):
  with tempfile.TemporaryDirectory()as directory:
   graph=coverage_fixture(Path(directory));path=graph['translations']['fr']['overview']['path']
   path.reverse()
   with self.assertRaisesRegex(StoryError,'ids and order'):validate_structure(graph)
   path.reverse();path[0]['source_ids']=['s']
   with self.assertRaises(StoryError):validate_structure(graph)
   del path[0]['source_ids'];path.pop()
   with self.assertRaisesRegex(StoryError,'original component path'):validate_structure(graph)
 def test_cli_requires_all_languages_before_writing_prepare_or_build_output(self):
  with tempfile.TemporaryDirectory()as directory:
   root=Path(directory);graph=coverage_fixture(root);draft=root/'graph.json';draft.write_text(json.dumps(graph));cli=ROOT/'skills/repo-visualizer/scripts/repo_story.py'
   for command in ('prepare','build','validate'):
    output=root/(command+'.out');output.write_text('Keep existing artifact')
    args=[sys.executable,str(cli),command,str(draft),'--all-languages']
    if command!='build':args+=['--repo',str(root)]
    if command!='validate':args+=['-o',str(output)]
    complete=subprocess.run(args,capture_output=True,text=True);self.assertEqual(complete.returncode,0,complete.stderr)
    if command=='build':self.assertIn('<!doctype html>',output.read_text().lower())
    incomplete=copy.deepcopy(graph);del incomplete['translations']['es']['nodes']['a']['caption'];draft.write_text(json.dumps(incomplete));output.write_text('Keep existing artifact')
    failed=subprocess.run(args,capture_output=True,text=True);self.assertEqual(failed.returncode,2);self.assertIn('es: nodes.a.caption',failed.stderr);self.assertEqual(output.read_text(),'Keep existing artifact');draft.write_text(json.dumps(graph))
 def test_bundled_catalogs_are_complete_and_keep_format_arguments(self):
  folder=ROOT/'skills/repo-visualizer/assets/locales';base=read_story(folder/'en.json')
  for language in ['cs','de','fr','es']:
   catalog=read_story(folder/(language+'.json'));self.assertEqual(set(catalog),set(base))
   for key in base:
    self.assertTrue(catalog[key].strip());self.assertEqual(sorted(re.findall(r'\{\w+\}',catalog[key])),sorted(re.findall(r'\{\w+\}',base[key])))
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
 def test_all_five_explanations_switch_including_overview_relationships_and_inferences(self):
  graph=validate_language_coverage(coverage_fixture(self.root));self.open(graph)
  for language in SUPPORTED_LANGUAGES:
   self.page.locator('#language-toggle').click();self.page.locator('[data-language-choice='+language+']').click();self.page.evaluate('window.repoLocaleReady')
   display=graph if language=='en'else graph['translations'][language]
   self.assertEqual(self.page.locator('#page-title').inner_text(),display['title']);self.assertEqual(self.page.locator('#question').inner_text(),display['question']);self.assertEqual(self.page.locator('#page-description').inner_text(),display['overview']['lead'])
   self.assertEqual(self.page.locator('#overview-path button').all_inner_texts(),[part['label']for part in display['overview']['path']]);self.page.locator('.analysis-notes').evaluate('(element)=>element.open=true');self.assertEqual(self.page.locator('#uncertainties li').all_inner_texts(),display['uncertainties']);self.assertFalse(self.page.locator('#graph-language-note').is_visible())
   node=graph['nodes'][0]if language=='en'else display['nodes']['a'];edge=graph['edges'][0]if language=='en'else display['edges']['ab']
   self.page.evaluate('repoPlayer.selectNode("a")');self.assertEqual(self.page.locator('#selection-title').inner_text(),node['label']);self.assertIn(node['description'],self.page.locator('#selection-description').inner_text());self.assertIn(node['reason'],self.page.locator('#selection-description').inner_text());self.assertIn(node['caption'],self.page.locator('[data-node=a] .node-caption').text_content())
   self.page.evaluate('repoPlayer.selectEdge("ab")');self.assertEqual(self.page.locator('#selection-title').inner_text(),edge['label']);self.assertIn(edge['relation'],self.page.locator('#selection-meta').inner_text());self.assertIn(edge['reason'],self.page.locator('#selection-description').inner_text())
   self.assertEqual(self.page.evaluate('repoPlayer.graph.sources'),graph['sources']);self.assertEqual(self.page.evaluate('repoPlayer.graph.edges.map(e=>[e.id,e.from,e.to,e.evidence])'),[[e['id'],e['from'],e['to'],e['evidence']]for e in graph['edges']]);self.assertEqual(self.page.locator('#scenario option[value=main]').inner_text(),graph['scenarios'][0]['label']if language=='en'else display['scenarios']['main']['label'])
  with self.page.expect_download()as event:self.page.evaluate("repoPlayer.export('json')")
  output=self.root/'canonical.json';event.value.save_as(output);saved=validate_language_coverage(read_story(output));self.assertEqual(saved['language'],'en');self.assertEqual(saved['translations'],graph['translations']);self.assertEqual(saved['sources'],graph['sources'])
  self.assertEqual(self.errors,[])
 def test_locale_switch_keeps_graph_evidence_selection_and_offline_download(self):
  graph=fixture(self.root);graph['summary']='Full detailed context. '+('More detail. '*35);graph['overview']={'lead':'A concise introduction.','path':[{'node_id':'a','label':'Frontend'}]};graph['repo']['commit']='abcdef0123456789abcdef0123456789abcdef01';graph['translations']={'en':{'nodes':{'a':{'label':'First component'}}}};self.open(graph)
  self.assertEqual(self.page.locator('#page-description').inner_text(),'A concise introduction.');self.assertEqual(self.page.locator('#intro-metadata code').inner_text(),'abcdef0');self.assertTrue(self.page.locator('#intro-details').is_visible());self.assertEqual(self.page.locator('#overview-path button').count(),1);self.assertEqual(self.page.locator('#code-tab').inner_text(),'Kód');self.assertEqual(self.page.locator('#page-title').inner_text(),'Sample')
  self.page.evaluate('repoPlayer.selectNode("a")');self.page.locator('#language-toggle').click();self.page.locator('[data-language-choice=en]').click();self.page.evaluate('window.repoLocaleReady')
  self.assertEqual(self.page.locator('#selection-title').inner_text(),'First component');self.assertEqual(self.page.evaluate('repoPlayer.graph.sources[0].excerpt'),graph['sources'][0]['excerpt'])
  self.assertEqual(self.page.evaluate('repoPlayer.graph.edges.map(e=>[e.from,e.to])'),[['a','b'],['b','a'],['b','c']])
  self.page.locator('[data-theme-choice=dark]').click();self.assertEqual(self.page.evaluate('document.documentElement.dataset.theme'),'dark')
  svg=self.page.evaluate('repoPlayer.exportSVG()');self.assertIn('data-theme="dark"',svg);self.assertIn('--paper:#10141b',svg.replace(' ',''))
  with self.page.expect_download() as download:self.page.evaluate('repoPlayer.export("html")')
  out=self.root/'copy.html';download.value.save_as(out);self.page.goto(out.as_uri());self.page.evaluate('window.repoReady');self.assertEqual(self.page.evaluate('document.documentElement.dataset.theme'),'dark');self.assertEqual(self.page.locator('#selection-title').inner_text(),'First component');self.assertEqual(self.errors,[])
 def test_custom_language_and_untrusted_translation_are_plain_text(self):
  graph=fixture(self.root);graph['language']='fr';graph['ui_strings']={'languageName':'Français','code':'Code source','openSource':'Ouvrir la source','map':'Carte <img src=x onerror="window.PWNED=1">'};self.open(graph)
  self.assertEqual(self.page.locator('#code-tab').inner_text(),'Code source');self.assertIsNone(self.page.evaluate('window.PWNED'));self.assertEqual(self.page.locator('[data-view=map] img').count(),0);self.assertEqual(self.page.evaluate('repoAppearance.language'),'fr');self.assertEqual(self.errors,[])
 def test_keyboard_language_menu_icon_themes_and_persistence(self):
  self.open(fixture(self.root));toggle=self.page.locator('#language-toggle')
  toggle.focus();toggle.press('Enter');self.assertEqual(toggle.get_attribute('aria-expanded'),'true')
  self.assertEqual(self.page.evaluate('document.activeElement.dataset.languageChoice'),'cs')
  self.page.keyboard.press('ArrowDown');self.page.keyboard.press('Enter');self.page.evaluate('window.repoLocaleReady')
  self.assertEqual(self.page.evaluate('repoAppearance.language'),'de');self.assertEqual(toggle.get_attribute('aria-expanded'),'false')
  self.assertEqual(self.page.evaluate('document.activeElement.id'),'language-toggle')
  self.assertEqual(self.page.locator('#current-flag svg').count(),1)
  self.assertTrue(self.page.locator('#graph-language-note').is_visible())
  self.page.locator('[data-theme-choice=dark]').click();self.assertEqual(self.page.evaluate('document.documentElement.dataset.theme'),'dark')
  self.assertEqual(self.page.locator('.theme-switch [aria-pressed=true]').count(),1)
  self.page.reload();self.page.evaluate('window.repoReady');self.assertEqual(self.page.evaluate('repoAppearance.language'),'de');self.assertEqual(self.page.evaluate('repoAppearance.theme'),'dark')
  toggle.click();self.page.keyboard.press('Escape');self.assertEqual(toggle.get_attribute('aria-expanded'),'false')
  toggle.click();self.page.locator('#page-title').click();self.assertEqual(toggle.get_attribute('aria-expanded'),'false')
  self.page.locator('[data-theme-choice=system]').click();self.page.emulate_media(color_scheme='light');self.assertEqual(self.page.evaluate('document.documentElement.dataset.theme'),'light')
  self.page.emulate_media(color_scheme='dark');self.page.wait_for_function('document.documentElement.dataset.theme==="dark"');self.assertEqual(self.page.locator('[data-theme-choice=system]').get_attribute('aria-pressed'),'true');self.assertEqual(self.errors,[])
 def test_nested_group_edges_attach_to_their_actual_components(self):
  self.open(fixture(self.root))
  failures=self.page.evaluate('''()=>{const errors=[];for(const g of document.querySelectorAll('.graph-edge')){const edge=repoPlayer.graph.edges.find(e=>e.id===g.dataset.edge);const paths=g.querySelectorAll('.edge-line');for(const [path,which,id] of [[paths[0],0,edge.from],[paths[paths.length-1],1,edge.to]]){const p=path.getPointAtLength(which?path.getTotalLength():0),point=new DOMPoint(p.x,p.y).matrixTransform(path.getScreenCTM()),rect=document.querySelector('.graph-node[data-node="'+id+'"] rect').getBoundingClientRect();if(point.x<rect.x-3||point.x>rect.right+3||point.y<rect.y-3||point.y>rect.bottom+3)errors.push({edge:edge.id,id,x:point.x,y:point.y,rect:{x:rect.x,y:rect.y,w:rect.width,h:rect.height}})}}return errors}''')
  self.assertEqual(failures,[]);self.assertEqual(self.errors,[])

if __name__=='__main__':unittest.main()
