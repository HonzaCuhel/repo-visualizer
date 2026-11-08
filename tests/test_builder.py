from pathlib import Path
import hashlib
import json
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'skills/repo-visualizer/scripts'))
from builder import build_html, safe_json
from story_model import prepare_story, StoryError

class BuilderTests(unittest.TestCase):
    def test_untrusted_labels_cannot_end_a_script_or_reenter_the_template(self):
        payload='</script><script>window.hacked=1</script>@@JS@@\u2028'
        encoded=safe_json({'title':payload})
        self.assertNotIn('</script>',encoded)
        self.assertEqual(json.loads(encoded)['title'],payload)
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'code.py').write_text('value = 1\n')
            graph=prepare_story({'schema_version':1,'title':payload,'question':'Why?', 'sources':[{'id':'s','path':'code.py','start':1,'end':1}], 'nodes':[{'id':'n','label':payload,'source_ids':['s']}]},root)
            (root/'LICENSE').write_text('MIT fixture license')
            assets=root/'assets';(assets/'fonts').mkdir(parents=True);(assets/'vendor').mkdir();(assets/'locales').mkdir()
            (assets/'player.html').write_text('<title>@@TITLE@@</title><script type="application/json">@@STORY@@</script><script>@@JS@@</script>')
            for language in ('de','fr','es'):
                (assets/'locales'/(language+'.json')).write_text('{}')
            for file,content in [('appearance.js','/*appearance*/'),('locales/en.json','{}'),('locales/cs.json','{}'),('player.css','body{}'),('player.js','/*real-player*/'),('interaction.js','/*controls*/'),('vendor/elk.bundled.js','/*elk*/'),('vendor/ELK-LICENSE.md','license'),('vendor/gifenc.js','/*gif*/'),('vendor/GIFENC-LICENSE.txt','license'),('fonts/OFL-AtkinsonHyperlegibleNext.txt','license')]:
                (assets/file).write_text(content)
            (assets/'fonts/AtkinsonHyperlegibleNext.ttf').write_bytes(b'font')
            with patch('builder.ASSETS',assets):
                output=build_html(graph)
            self.assertEqual(output.count('/*real-player*/'),1)
            self.assertNotIn('<script>window.hacked',output)
            self.assertIn('@@JS@@',output)

    def test_unprepared_graph_is_rejected(self):
        graph={'schema_version':1,'title':'demo','question':'Why?', 'sources':[{'id':'s','path':'code.py','start':1,'end':1}], 'nodes':[{'id':'n','label':'Code','source_ids':['s']}]}
        with self.assertRaisesRegex(StoryError,'prepare'):
            build_html(graph)

if __name__=='__main__':unittest.main()
