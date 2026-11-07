"""Build a source-indexed component inventory without importing target code.

Python imports are resolved statically. Other languages are inventoried for the
coding agent to interpret; absence of an extracted edge never means no coupling.
"""
from __future__ import annotations

import ast
from collections import defaultdict
import hashlib
import os
from pathlib import Path

from story_model import StoryError, repository_snapshot, source_path

CODE_SUFFIXES = {".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".go", ".rs", ".java", ".rb", ".php", ".cs", ".swift", ".kt"}
SKIP_DIRS = {".git", ".work", "node_modules", ".venv", "venv", "dist", "build", "__pycache__", ".next", ".cache", "vendor"}


def _id(prefix, *parts):
    return prefix + "-" + hashlib.sha256("\0".join(map(str, parts)).encode()).hexdigest()[:16]


def _module(path):
    parts = list(Path(path).with_suffix("").parts)
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def _aliases(path):
    canonical = _module(path)
    aliases = {canonical}
    parts = canonical.split(".")
    for marker in ("src", "backend", "lib", "python"):
        if marker in parts:
            index = parts.index(marker) + 1
            if index < len(parts):
                aliases.add(".".join(parts[index:]))
    return aliases


def _function_name(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _function_name(node.value)
        return base + "." + node.attr if base else node.attr
    return None


def _symbols(tree):
    result = []
    def visit(body, parents=()):
        for node in body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                name = ".".join((*parents, node.name))
                item = {"name": name, "kind": "class" if isinstance(node, ast.ClassDef) else "function", "start": node.lineno, "end": node.end_lineno}
                if not isinstance(node, ast.ClassDef):
                    # Candidates only: a method name is not proof of its receiver's type.
                    calls = {_function_name(n.func) for n in ast.walk(node) if isinstance(n, ast.Call)}
                    item["call_candidates"] = sorted(c for c in calls if c)
                result.append(item)
                visit(node.body, (*parents, node.name))
            elif hasattr(node, "body") and isinstance(node.body, list):
                visit(node.body, parents)
    visit(tree.body)
    return result


def scan_repository(repository, paths=None, *, include_tests=False):
    root = Path(repository).resolve(strict=True)
    selected = []
    if paths:
        for relative in paths:
            pure = Path(relative)
            if pure.is_absolute() or ".." in pure.parts:
                raise StoryError("scan paths must be repository-relative")
            target = (root / pure).resolve(strict=True)
            try:
                target.relative_to(root)
            except ValueError as error:
                raise StoryError("scan path escapes the repository") from error
            if target.is_file():
                selected.append(target)
            else:
                selected.extend(_walk(target, include_tests))
    else:
        selected = list(_walk(root, include_tests))
    files = sorted({p.relative_to(root).as_posix() for p in selected if p.suffix in CODE_SUFFIXES})
    sources, nodes, edges, inventory, warnings = [], [], [], [], []
    source_ids, captured_hashes, edge_ids = {}, {}, set()
    trees, node_ids, module_index = {}, {}, defaultdict(set)
    def source(relative, start, end):
        key = (relative, start, end)
        if key not in source_ids:
            key_id = _id("source", *key)
            source_ids[key] = key_id
            sources.append({"id": key_id, "path": relative, "start": start, "end": end, "sha256": captured_hashes[relative]})
        return source_ids[key]
    for relative in files:
        path = source_path(root, relative)
        if path.stat().st_size > 8_000_000:
            warnings.append(f"Skipped large source: {relative}")
            continue
        try:
            raw = path.read_bytes()
            text = raw.decode("utf-8")
        except (UnicodeError, OSError):
            warnings.append(f"Skipped unreadable text: {relative}")
            continue
        lines = text.splitlines()
        if not lines:
            continue
        captured_hashes[relative] = hashlib.sha256(raw).hexdigest()
        key = _id("module", relative)
        node_ids[relative] = key
        item = {"path": relative, "language": "python" if path.suffix == ".py" else path.suffix.lstrip("."), "sha256": captured_hashes[relative], "symbols": []}
        description = "Source module. Inspect its implementation to explain its responsibilities."
        if path.suffix == ".py":
            try:
                tree = ast.parse(text, filename=relative)
                trees[relative] = tree
                item["symbols"] = _symbols(tree)
                doc = ast.get_docstring(tree)
                if doc:
                    description = doc.split("\n\n", 1)[0].replace("\n", " ")
                for alias in _aliases(relative):
                    module_index[alias].add(relative)
            except (SyntaxError, RecursionError) as error:
                warnings.append(f"Python syntax could not be indexed: {relative}: {type(error).__name__}")
        else:
            item["edge_analysis"] = "Agent review required; no language-specific relationships extracted."
        nodes.append({"id": key, "label": relative, "kind": "module", "description": description, "source_ids": [source(relative, 1, min(len(lines), 8))]})
        inventory.append(item)
    unresolved = []
    for relative, tree in trees.items():
        current = _module(relative).split(".")
        package = current if relative.endswith("/__init__.py") else current[:-1]
        for node in ast.walk(tree):
            candidates = []
            if isinstance(node, ast.Import):
                candidates = [(alias.name, [alias.name]) for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    if node.level > len(package):
                        unresolved.append({"path": relative, "line": node.lineno, "import": "."*node.level+(node.module or ""), "reason": "relative import exceeds the package"})
                        continue
                    base = package[:len(package)-node.level+1]
                    base += node.module.split(".") if node.module else []
                    module = ".".join(base)
                else:
                    module = node.module or ""
                for alias in node.names:
                    member = module + "." + alias.name if module else alias.name
                    candidates.append((member, [member, module]))
            for imported, choices in candidates:
                matches = set()
                for choice in choices:
                    matches = module_index.get(choice, set())
                    if matches:
                        break
                if len(matches) != 1:
                    unresolved.append({"path": relative, "line": node.lineno, "import": imported, "reason": "external or unresolved" if not matches else "ambiguous local module"})
                    continue
                target = next(iter(matches))
                if target == relative:
                    continue
                edge_id = _id("import", relative, node.lineno, target)
                if edge_id in edge_ids:
                    continue
                edge_ids.add(edge_id)
                edges.append({"id": edge_id, "from": node_ids[relative], "to": node_ids[target], "relation": "imports", "label": "imports", "source_ids": [source(relative, node.lineno, node.end_lineno)]})
    if not nodes:
        raise StoryError("No readable code components found in the selected scope")
    return {
        "schema_version": 1,
        "title": root.name + " component inventory",
        "question": "Which source modules exist and how do their Python imports connect?",
        "summary": "A static component inventory for the coding agent to refine into the repository's behavioral graph.",
        "repo": repository_snapshot(root),
        "default_view": "map",
        "nodes": nodes, "edges": edges, "sources": sources,
        "uncertainties": ["Import edges are static dependencies, not executed calls. Other-language and dynamic relationships require agent review.", *warnings],
        "analysis": {"scope": "static-python-imports-and-cross-language-file-inventory", "complete_behavioral_analysis": False, "inventory": inventory, "unresolved_imports": unresolved},
    }


def _walk(root, include_tests):
    for directory, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not (not include_tests and d in {"tests", "test", "__tests__"}))
        for name in sorted(files):
            path = Path(directory) / name
            if not include_tests and (name.startswith("test_") or ".test." in name or ".spec." in name):
                continue
            if path.suffix in CODE_SUFFIXES and not path.is_symlink():
                yield path
