#!/usr/bin/env python3
"""Prepare and validate source-grounded repository walkthroughs."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from story_model import StoryError, prepare_story, read_story, repository_snapshot, source_path, validate_language_coverage, validate_structure, write_story


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    inspect = commands.add_parser("inspect", help="Read repository revision and sanitized origin without executing it")
    inspect.add_argument("--repo", type=Path, required=True)
    scan = commands.add_parser("scan", help="Inventory components and static Python imports for agent review")
    scan.add_argument("--repo", type=Path, required=True)
    scan.add_argument("--path", action="append", dest="paths", help="Repository-relative file or directory; repeat to limit scope")
    scan.add_argument("--include-tests", action="store_true")
    scan.add_argument("--output", "-o", type=Path, required=True)
    build = commands.add_parser("build", help="Build portable HTML from a prepared graph")
    build.add_argument("story", type=Path)
    build.add_argument("--output", "-o", type=Path, required=True)
    build.add_argument("--all-languages", action="store_true", help="Require complete explanations in English, Czech, German, French and Spanish")
    build.add_argument("--ordered", action="store_true", help="Require authored input-to-output phases with parallel components on the same level")
    for name in ("prepare", "validate"):
        command = commands.add_parser(name, help="Check story references against the specified local checkout")
        command.add_argument("story", type=Path)
        command.add_argument("--repo", type=Path, required=True)
        command.add_argument("--all-languages", action="store_true", help="Require complete explanations in all five bundled languages")
        command.add_argument("--ordered", action="store_true", help="Require authored mechanism phases in presentation.levels")
        if name == "prepare":
            command.add_argument("--output", "-o", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "inspect":
            print(json.dumps(repository_snapshot(args.repo), ensure_ascii=False, indent=2))
            return 0
        if args.command == "scan":
            from inventory import scan_repository
            graph = scan_repository(args.repo, args.paths, include_tests=args.include_tests)
            root = args.repo.resolve()
            if any(args.output.resolve() == source_path(root, item["path"]) for item in graph["analysis"]["inventory"]):
                raise StoryError("output would overwrite an inventoried source file; choose an artifact path")
            write_story(args.output, graph)
            print(json.dumps({"status": "indexed", "components": len(graph["nodes"]), "static_import_edges": len(graph["edges"]), "scope": graph["analysis"]["scope"], "behavioral_analysis": "requires coding-agent review"}, indent=2))
            return 0
        data = read_story(args.story)
        if args.all_languages:
            data = validate_language_coverage(data)
        if args.ordered:
            data = validate_structure(data)
            if not data['presentation'].get('levels'):
                raise StoryError('Ordered explanation needs presentation.levels: inputs first, parallel components together, outputs last')
        if args.command == "build":
            from builder import build_html, write_html
            if args.output.resolve() == args.story.resolve():
                raise StoryError("HTML output must differ from the graph JSON")
            write_html(args.output, build_html(data))
            print(json.dumps({"status": "built", "output": str(args.output), "format": "portable-html"}))
            return 0
        story = prepare_story(data, args.repo)
        if args.command == "prepare":
            root = args.repo.resolve()
            if any(args.output.resolve() == source_path(root, s["path"]) for s in story["sources"]):
                raise StoryError("output would overwrite a referenced source file; choose an artifact path")
            write_story(args.output, story)
        print(json.dumps({"status": "valid", "scope": "structure, files, line ranges and fingerprints; not semantic correctness", "nodes": len(story["nodes"]), "steps": len(story["steps"]), "sources": len(story["sources"]), "repo": story["repo"]}, ensure_ascii=False, indent=2))
        return 0
    except (StoryError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
