from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills/repo-visualizer/scripts"))
from inventory import scan_repository
from story_model import prepare_story, StoryError


class InventoryTests(unittest.TestCase):
    def test_scan_is_pinned_to_the_bytes_it_indexed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "app.py").write_text("value = 1\n")
            graph = scan_repository(root)
            (root / "app.py").write_text("value = 2\n")
            with self.assertRaises(StoryError):
                prepare_story(graph, root)

    def test_static_cycles_are_kept_without_running_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "pkg").mkdir()
            (root / "pkg/__init__.py").write_text("# package\n")
            (root / "pkg/a.py").write_text("from . import b\nraise RuntimeError('do not execute')\ndef action():\n    b.reply()\n")
            (root / "pkg/b.py").write_text("from .a import action\ndef reply():\n    action()\n")
            graph = scan_repository(root)
            names = {node["id"]:node["label"] for node in graph["nodes"]}
            links = {(names[e["from"]], names[e["to"]], e["relation"]) for e in graph["edges"]}
            self.assertIn(("pkg/a.py", "pkg/b.py", "imports"), links)
            self.assertIn(("pkg/b.py", "pkg/a.py", "imports"), links)
            ready = prepare_story(graph, root)
            self.assertEqual(ready["steps"], [])
            function = next(f for item in graph["analysis"]["inventory"] if item["path"]=="pkg/a.py" for f in item["symbols"] if f["name"]=="action")
            self.assertEqual(function["call_candidates"], ["b.reply"])

    def test_src_aliases_external_imports_and_other_languages_are_explicit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "backend/app").mkdir(parents=True)
            (root / "backend/app/a.py").write_text("from app.b import reply\nimport external_provider\n")
            (root / "backend/app/b.py").write_text("def reply():\n    return 'ok'\n")
            (root / "view.tsx").write_text("export function View() { return null; }\n")
            graph = scan_repository(root)
            self.assertEqual(len(graph["edges"]), 1)
            self.assertFalse(graph["analysis"]["complete_behavioral_analysis"])
            self.assertTrue(any(i["import"]=="external_provider" for i in graph["analysis"]["unresolved_imports"]))
            typescript = next(i for i in graph["analysis"]["inventory"] if i["path"]=="view.tsx")
            self.assertIn("Agent review required", typescript["edge_analysis"])

    def test_scope_skips_generated_dependencies_and_does_not_follow_symlinks(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as outside:
            root = Path(tmp)
            (root / "real.py").write_text("value = 1\n")
            (root / "node_modules").mkdir()
            (root / "node_modules/vendor.py").write_text("value = 2\n")
            (root / "test_real.py").write_text("value = 3\n")
            external = Path(outside) / "outside.py"; external.write_text("value = 4\n")
            (root / "link.py").symlink_to(external)
            graph = scan_repository(root)
            self.assertEqual([n["label"] for n in graph["nodes"]], ["real.py"])


if __name__ == "__main__":
    unittest.main()
