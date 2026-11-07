from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import package_skill

class PackageTests(unittest.TestCase):
    def fixture(self,root):
        skill=root/'skills/repo-visualizer'
        for name in package_skill.FILES:
            path=skill/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text('fixture '+name)
        return skill

    def test_inventory_is_complete_deterministic_and_excludes_private_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);skill=self.fixture(root)
            (skill/'private.json').write_text('private fixture')
            (root/'.env').write_text('fixture secret')
            with patch('package_skill.ROOT',root):
                one=package_skill.package(root/'one.zip');two=package_skill.package(root/'two.zip')
            self.assertEqual(one['sha256'],two['sha256'])
            with zipfile.ZipFile(one['file']) as archive:
                self.assertEqual(set(archive.namelist()),{'repo-visualizer/'+n for n in package_skill.FILES})
                self.assertNotIn(b'private fixture',b''.join(archive.read(n) for n in archive.namelist()))

    def test_incomplete_or_symlinked_skill_cannot_replace_an_existing_archive(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);skill=self.fixture(root);output=root/'good.zip';output.write_bytes(b'existing')
            missing=skill/'assets/player.js';missing.unlink()
            with patch('package_skill.ROOT',root):
                with self.assertRaisesRegex(ValueError,'Incomplete'):package_skill.package(output)
                self.assertEqual(output.read_bytes(),b'existing')
                outside=root/'outside.js';outside.write_text('external');missing.symlink_to(outside)
                with self.assertRaisesRegex(ValueError,'symlink'):package_skill.package(output)
                self.assertEqual(output.read_bytes(),b'existing')

if __name__=='__main__':unittest.main()
