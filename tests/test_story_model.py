from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "skills/repo-visualizer/scripts"
sys.path.insert(0, str(SCRIPTS))
from story_model import StoryError, prepare_story, repository_snapshot, validate_structure


def draft():
    return {
        "schema_version": 1, "title": "A small cache", "question": "What happens on a cache miss?",
        "sources": [{"id": "handler", "path": "handler.py", "start": 1, "end": 3}],
        "nodes": [
            {"id": "lookup", "label": "Look up key", "source_ids": ["handler"]},
            {"id": "result", "label": "Return result", "kind": "output", "source_ids": ["handler"]},
        ],
        "edges": [{"id": "return", "from": "lookup", "to": "result", "source_ids": ["handler"]}],
        "steps": [{"id": "read", "title": "Read the cache", "description": "The handler looks up a key and returns a value.", "node_ids": ["lookup"], "edge_ids": ["return"], "source_ids": ["handler"]}],
    }


class StoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.file = self.root / "handler.py"
        self.file.write_text("def lookup(cache, key):\n    value = cache.get(key)\n    return value\n", encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_prepare_captures_actual_source_without_altering_input(self):
        raw = draft()
        story = prepare_story(raw, self.root)
        source = story["sources"][0]
        self.assertEqual(source["sha256"], hashlib.sha256(self.file.read_bytes()).hexdigest())
        self.assertEqual(source["excerpt"], self.file.read_text().rstrip("\n"))
        self.assertNotIn("sha256", raw["sources"][0])
        self.assertEqual(source["revision"], "working-tree")
        self.assertIsNone(story["repo"]["commit"])
        self.assertEqual(story["scenarios"][0]["step_ids"], ["read"])

    def test_revalidation_detects_source_drift(self):
        story = prepare_story(draft(), self.root)
        self.assertEqual(prepare_story(story, self.root), story)
        self.file.write_text("def lookup(cache, key):\n    return None\n# changed\n")
        with self.assertRaisesRegex(StoryError, "changed"):
            prepare_story(story, self.root)

    def test_rejects_fabricated_excerpt(self):
        raw = draft()
        raw["sources"][0]["excerpt"] = "this was never in the repository"
        with self.assertRaisesRegex(StoryError, "excerpt"):
            prepare_story(raw, self.root)

    def test_rejects_missing_file_and_out_of_range_lines(self):
        for values in ({"path": "missing.py"}, {"end": 100}, {"start": 0}, {"start": True}, {"start": 3, "end": 1}):
            with self.subTest(values=values):
                raw = draft()
                raw["sources"][0].update(values)
                with self.assertRaises(StoryError):
                    prepare_story(raw, self.root)

    def test_source_cannot_escape_via_path_or_symlink(self):
        with tempfile.TemporaryDirectory() as outside:
            outside_file = Path(outside) / "private.py"
            outside_file.write_text("outside\n")
            (self.root / "escape.py").symlink_to(outside_file)
            for path in ("../private.py", str(outside_file), "escape.py", "C:\\outside\\private.py"):
                raw = draft()
                raw["sources"][0]["path"] = path
                with self.subTest(path=path), self.assertRaises(StoryError):
                    prepare_story(raw, self.root)

    def test_references_and_evidence_are_not_implicitly_trusted(self):
        cases = []
        unknown = draft(); unknown["edges"][0]["to"] = "invented"; cases.append(unknown)
        unknown = draft(); unknown["edges"][0]["to"] = ["invented"]; cases.append(unknown)
        unknown = draft(); unknown["steps"][0]["source_ids"] = ["invented"]; cases.append(unknown)
        unknown = draft(); unknown["nodes"][0]["source_ids"] = []; cases.append(unknown)
        unknown = draft(); unknown["nodes"][0]["evidence"] = "runtime"; cases.append(unknown)
        unknown = draft(); unknown["steps"][0]["duration_ms"] = True; cases.append(unknown)
        unknown = draft(); unknown["scenarios"] = [{"id": "missing", "label": "Missing", "step_ids": ["invented"]}]; cases.append(unknown)
        for raw in cases:
            with self.subTest(raw=raw), self.assertRaises(StoryError):
                validate_structure(raw)

    def test_inference_is_explicit_and_requires_a_reason(self):
        raw = draft()
        raw["nodes"][0].update(evidence="inferred", source_ids=[], reason="The provider implementation is external.")
        story = prepare_story(raw, self.root)
        self.assertEqual(story["nodes"][0]["evidence"], "inferred")
        del raw["nodes"][0]["reason"]
        with self.assertRaisesRegex(StoryError, "reason"):
            validate_structure(raw)

    def test_graph_preserves_cycles_parallel_edges_and_disconnected_components(self):
        raw = draft()
        del raw["steps"]
        raw["nodes"].append({"id": "external", "label": "Separate module", "source_ids": ["handler"]})
        raw["edges"].extend([
            {"id": "retry", "from": "result", "to": "lookup", "relation": "retries", "source_ids": ["handler"]},
            {"id": "audit", "from": "lookup", "to": "result", "relation": "emits", "source_ids": ["handler"]},
        ])
        story = prepare_story(raw, self.root)
        self.assertEqual(story["default_view"], "map")
        self.assertEqual(story["steps"], [])
        self.assertEqual(story["scenarios"], [])
        self.assertEqual([(e["from"],e["to"]) for e in story["edges"]], [("lookup","result"),("result","lookup"),("lookup","result")])
        self.assertEqual(len(story["nodes"]), 3)

    def test_nested_component_groups_have_valid_acyclic_parentage(self):
        raw = draft()
        raw["groups"] = [{"id": "app", "label": "Application"}, {"id": "cache", "label": "Cache", "parent": "app"}]
        raw["nodes"][0]["group"] = "cache"
        self.assertEqual(prepare_story(raw, self.root)["groups"], raw["groups"])
        raw["groups"][0]["parent"] = "cache"
        with self.assertRaisesRegex(StoryError, "cycle"):
            validate_structure(raw)
        raw["groups"][0].pop("parent")
        raw["groups"][1]["parent"] = "missing"
        with self.assertRaisesRegex(StoryError, "unknown group"):
            validate_structure(raw)

    def test_labels_remain_data_and_no_target_code_runs(self):
        raw = draft()
        raw["nodes"][0]["label"] = '</script><img src=x onerror="alert(1)">'
        self.file.write_text("raise RuntimeError('must never execute')\n# source\n# only\n")
        story = prepare_story(raw, self.root)
        self.assertEqual(story["nodes"][0]["label"], raw["nodes"][0]["label"])

    def test_commit_change_during_capture_is_rejected(self):
        first = {"name": "fixture", "commit": "a"*40, "dirty": False, "url": None}
        last = {**first, "commit": "b"*40}
        with patch("story_model.repository_snapshot", side_effect=[first, last]):
            with self.assertRaisesRegex(StoryError, "changed while capturing"):
                prepare_story(draft(), self.root)

    def test_git_links_match_only_unchanged_source_and_strip_credentials(self):
        env = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
        def git(*args):
            return subprocess.run(["git", "-C", str(self.root), *args], env=env, check=True, capture_output=True, text=True).stdout
        git("init", "-b", "main")
        git("add", "handler.py")
        git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-m", "Fixture")
        git("remote", "add", "origin", "https://fixture-user:fixture-password@github.com/example/fixture.git?unused=true")
        story = prepare_story(draft(), self.root)
        source = story["sources"][0]
        self.assertIn("/blob/", source["url"])
        self.assertEqual(story["repo"]["url"], "https://github.com/example/fixture")
        self.assertNotIn("fixture-password", json.dumps(story))
        self.file.write_text(self.file.read_text()+"# local change\n")
        changed = prepare_story(draft(), self.root)
        self.assertEqual(changed["sources"][0]["revision"], "working-tree")
        self.assertNotIn("url", changed["sources"][0])
        self.assertTrue(changed["repo"]["dirty"])
        wrong = draft(); wrong["repo"] = {"commit": "0"*40}
        with self.assertRaisesRegex(StoryError, "commit"):
            prepare_story(wrong, self.root)

    def test_cli_does_not_overwrite_good_output_on_invalid_input(self):
        input_file = self.root / "story.json"
        output_file = self.root / "grounded.json"
        input_file.write_text(json.dumps(draft()))
        command = [sys.executable, str(SCRIPTS / "repo_story.py"), "prepare", str(input_file), "--repo", str(self.root), "-o", str(output_file)]
        good = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(good.returncode, 0, good.stderr)
        original = output_file.read_bytes()
        bad = draft(); bad["sources"][0]["end"] = 100
        input_file.write_text(json.dumps(bad))
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(output_file.read_bytes(), original)
        self.assertIn("exceed", result.stderr)

    def test_cli_cannot_replace_a_source_with_its_generated_story(self):
        input_file = self.root / "story.json"
        input_file.write_text(json.dumps(draft()))
        before = self.file.read_bytes()
        result = subprocess.run([sys.executable, str(SCRIPTS / "repo_story.py"), "prepare", str(input_file), "--repo", str(self.root), "-o", str(self.file)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.file.read_bytes(), before)
        self.assertIn("overwrite a referenced source", result.stderr)


if __name__ == "__main__":
    unittest.main()
