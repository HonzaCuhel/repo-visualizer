from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'skills/repo-visualizer/scripts'))
from hyperframes_export import composition

class AdapterTests(unittest.TestCase):
    def test_preserves_document_and_bridges_deterministic_scene(self):
        original='<!doctype html><html><head><title>Original</title></head><body class="player"><main>Original graph</main></body></html>'
        result=composition(original,12000,960,608,10,'x</script><script>bad()</script>')
        self.assertIn('<main>Original graph</main>',result)
        self.assertIn('data-duration="12.0"',result)
        self.assertIn('window.__hf.buildReady.repoVisualizer=ready',result)
        self.assertIn('window.renderAt(seconds*1000)',result)
        self.assertNotIn('<script>bad()',result)
        self.assertEqual(result.count('<body'),1)
        self.assertEqual(result.count('</body>'),1)

    def test_video_caches_only_layout_and_keeps_the_same_scene(self):
        document='<body><script id="layout-engine">Math.random();</script><script id="repo-data" type="application/json">{"nodes":[{"id":"a"}]}</script><script>window.renderAt=sharedScene</script><script id="interaction-script">requestAnimationFrame(tick)</script></body>'
        layout={'id':'root','children':[{'id':'a','x':10,'y':20}]}
        result=composition(document,1200,960,640,10,layout=layout)
        self.assertNotIn('Math.random()',result)
        self.assertNotIn('requestAnimationFrame',result)
        self.assertIn('window.renderAt=sharedScene',result)
        self.assertIn('"nodes":[{"id":"a"}]',result)
        self.assertIn('"x":10,"y":20',result)

    def test_rejects_incomplete_document_or_invalid_timing(self):
        for html,duration in [('<main>fragment</main>',12000),('<body></body>',0),('<body></body>',float('nan'))]:
            with self.assertRaises(ValueError):composition(html,duration,960,608,10)

if __name__=='__main__':unittest.main()
