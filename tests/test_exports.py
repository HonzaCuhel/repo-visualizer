from pathlib import Path
import json
import os
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'skills/repo-visualizer/scripts'))
from export import export_scene, ffmpeg_binary

# A synthetic engine contract fixture, not a repository or product walkthrough.
FIXTURE='''<!doctype html><html><head><meta charset="utf-8"><style>body{margin:0;background:#fff}svg{width:320px;height:320px}</style></head><body><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 320"><rect id="moving" x="10" y="100" width="40" height="40" fill="#2365ca"/></svg><script>
window.repoReady=Promise.resolve();
window.renderAt=(ms)=>document.getElementById('moving').setAttribute('x',10+Math.min(ms,1200)/6);
window.repoPlayer={durationMs:1200,setView(){},setScenario(id){if(id!=='default')throw Error('Unknown scenario')},exportSVG:()=>new XMLSerializer().serializeToString(document.querySelector('svg'))};
renderAt(0);
</script></body></html>'''

class ExportArgumentTests(unittest.TestCase):
    def test_invalid_exports_do_not_touch_input_or_existing_output(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'input.html';path.write_text('original')
            for output,kwargs in [(path,{}),(Path(directory)/'bad.exe',{}),(Path(directory)/'a.png',{'fps':0}),(Path(directory)/'a.png',{'width':10})]:
                with self.assertRaises(ValueError):export_scene(path,output,**kwargs)
                self.assertEqual(path.read_text(),'original')

@unittest.skipUnless(os.environ.get('REPO_VISUALIZER_BROWSER'),'Set REPO_VISUALIZER_BROWSER to run the real export integration tests')
class ExportIntegrationTests(unittest.TestCase):
    def test_all_formats_decode_and_animation_changes(self):
        from PIL import Image,ImageSequence
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);source=root/'fixture.html';source.write_text(FIXTURE)
            for kind in ['png','svg','gif','mp4','webm']:
                output=root/('test.'+kind)
                receipt=export_scene(source,output,width=320,height=320,fps=5,browser_path=os.environ['REPO_VISUALIZER_BROWSER'])
                self.assertGreater(output.stat().st_size,100)
                self.assertEqual(receipt['format'],kind)
                if kind=='png':
                    with Image.open(output) as img:self.assertEqual(img.size,(320,320))
                elif kind=='svg':
                    self.assertEqual(ET.fromstring(output.read_text()).tag,'{http://www.w3.org/2000/svg}svg')
                elif kind=='gif':
                    with Image.open(output) as img:
                        frames=[frame.convert('RGB').tobytes() for frame in ImageSequence.Iterator(img)]
                        self.assertGreaterEqual(len(set(frames)),5)
                        self.assertEqual(img.info['loop'],0)
                else:
                    decoded=subprocess.run([ffmpeg_binary(),'-v','error','-i',str(output),'-f','framemd5','-'],capture_output=True,text=True,check=True)
                    hashes=[s.rsplit(',',1)[-1].strip() for s in decoded.stdout.splitlines() if not s.startswith('#')]
                    self.assertEqual(len(hashes),6)
                    self.assertGreaterEqual(len(set(hashes)),5)

    def test_failed_scene_keeps_existing_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);source=root/'bad.html';source.write_text('<script>throw Error("fixture failure")</script>')
            output=root/'good.png';output.write_bytes(b'existing')
            with self.assertRaises(RuntimeError):export_scene(source,output,width=320,height=320,browser_path=os.environ['REPO_VISUALIZER_BROWSER'])
            self.assertEqual(output.read_bytes(),b'existing')

if __name__=='__main__':unittest.main()
