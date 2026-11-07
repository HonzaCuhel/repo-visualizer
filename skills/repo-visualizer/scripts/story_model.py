"""Source-grounded repository stories. Standard library only; never runs repo code."""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import subprocess
import tempfile
from urllib.parse import quote, urlsplit, urlunsplit


class StoryError(ValueError):
    """An actionable model or source-reference error."""


def _text(value, context, *, optional=False):
    if optional and (value is None or isinstance(value, str) and not value.strip()):
        return ""
    if not isinstance(value, str) or not value.strip():
        raise StoryError(f"{context}: expected non-empty text")
    return value.strip()


def _integer(value, context, minimum=1):
    if type(value) is not int or value < minimum:
        raise StoryError(f"{context}: expected an integer >= {minimum}")
    return value


def _records(value, context):
    if not isinstance(value, list) or not value:
        raise StoryError(f"{context}: expected a non-empty list")
    result = {}
    for item in value:
        if not isinstance(item, dict):
            raise StoryError(f"{context}: each entry must be an object")
        key = _text(item.get("id"), f"{context}.id")
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", key):
            raise StoryError(f"{context}: invalid id {key!r}")
        if key in result:
            raise StoryError(f"{context}: duplicate id {key!r}")
        item["id"] = key
        result[key] = item
    return result


def _refs(values, available, context, *, required=False):
    if not isinstance(values, list):
        raise StoryError(f"{context}: expected a list of ids")
    if required and not values:
        raise StoryError(f"{context}: at least one reference is required")
    for value in values:
        if not isinstance(value, str) or value not in available:
            raise StoryError(f"{context}: unknown reference {value!r}")
    if len(set(values)) != len(values):
        raise StoryError(f"{context}: duplicate references")


def _evidence(item, sources, context):
    kind = item.setdefault("evidence", "source")
    if kind not in ("source", "inferred"):
        raise StoryError(f"{context}.evidence: use 'source' or 'inferred'; this model does not certify runtime traces")
    _refs(item.setdefault("source_ids", []), sources, f"{context}.source_ids", required=kind == "source")
    if kind == "inferred":
        _text(item.get("reason"), f"{context}.reason")


def validate_structure(data):
    """Return a normalized copy; validate meaning references, not source interpretation."""
    if not isinstance(data, dict):
        raise StoryError("story: expected a JSON object")
    story = copy.deepcopy(data)
    if type(story.get("schema_version")) is not int or story["schema_version"] != 1:
        raise StoryError("schema_version: expected 1")
    for field in ("title", "question"):
        story[field] = _text(story.get(field), field)
    story["summary"] = _text(story.get("summary"), "summary", optional=True)
    story["source_license"] = _text(story.get("source_license"), "source_license", optional=True)
    language = story.setdefault("language", "en")
    if not isinstance(language, str) or not re.fullmatch(r"[a-zA-Z]{2,8}(?:-[a-zA-Z0-9]{1,8})*", language):
        raise StoryError("language: expected a language tag such as en or cs")
    if story.setdefault("default_view", "map") not in ("map", "focus", "path"):
        raise StoryError("default_view: expected map, focus or path")
    sources = _records(story.get("sources"), "sources")
    nodes = _records(story.get("nodes"), "nodes")
    overview = story.setdefault('overview', {})
    if not isinstance(overview, dict) or set(overview) - {'lead', 'path'}:
        raise StoryError('overview: expected a short lead and optional component path')
    if 'lead' in overview:
        _text(overview['lead'], 'overview.lead')
    if 'path' in overview:
        if not isinstance(overview['path'], list):
            raise StoryError('overview.path: expected component references')
        for entry in overview['path']:
            if not isinstance(entry, dict) or set(entry) - {'node_id', 'label'} or entry.get('node_id') not in nodes:
                raise StoryError('overview.path: use existing component ids')
            if 'label' in entry:
                _text(entry['label'], 'overview.path.label')
    raw_edges = story.setdefault("edges", [])
    if not isinstance(raw_edges, list):
        raise StoryError("edges: expected a list")
    edges = _records(raw_edges, "edges") if raw_edges else {}
    raw_steps = story.setdefault("steps", [])
    if not isinstance(raw_steps, list):
        raise StoryError("steps: expected a list; paths through the graph are optional")
    steps = _records(raw_steps, "steps") if raw_steps else {}
    raw_groups = story.setdefault("groups", [])
    if not isinstance(raw_groups, list):
        raise StoryError("groups: expected a list")
    groups = _records(raw_groups, "groups") if raw_groups else {}
    if set(groups) & set(nodes):
        raise StoryError("groups: group and component ids must be distinct")
    for key, group in groups.items():
        _text(group.get("label"), f"groups.{key}.label")
        parent = group.get("parent")
        if parent is not None and (not isinstance(parent, str) or parent not in groups):
            raise StoryError(f"groups.{key}.parent: unknown group")
    for key, group in groups.items():
        parent = group.get("parent")
        visited = {key}
        while parent is not None:
            if parent in visited:
                raise StoryError(f"groups.{key}: group nesting contains a cycle")
            visited.add(parent)
            parent = groups[parent].get("parent")
    for key, source in sources.items():
        _text(source.get("path"), f"sources.{key}.path")
        start = _integer(source.get("start"), f"sources.{key}.start")
        if _integer(source.get("end"), f"sources.{key}.end") < start:
            raise StoryError(f"sources.{key}: end precedes start")
    for key, node in nodes.items():
        node["label"] = _text(node.get("label"), f"nodes.{key}.label")
        node["description"] = _text(node.get("description"), f"nodes.{key}.description", optional=True)
        if node.setdefault("kind", "module") not in ("input", "process", "decision", "output", "external", "module", "function", "service", "store", "queue", "actor", "artifact"):
            raise StoryError(f"nodes.{key}.kind: unknown node kind")
        group = node.get("group")
        if group is not None and (not isinstance(group, str) or group not in groups):
            raise StoryError(f"nodes.{key}.group: unknown group")
        _evidence(node, sources, f"nodes.{key}")
    for key, edge in edges.items():
        for endpoint in ("from", "to"):
            if not isinstance(edge.get(endpoint), str) or edge[endpoint] not in nodes:
                raise StoryError(f"edges.{key}.{endpoint}: unknown node {edge.get(endpoint)!r}")
        edge["label"] = _text(edge.get("label"), f"edges.{key}.label", optional=True)
        edge["relation"] = _text(edge.get("relation", "relates_to"), f"edges.{key}.relation")
        _evidence(edge, sources, f"edges.{key}")
    for key, step in steps.items():
        step["title"] = _text(step.get("title"), f"steps.{key}.title")
        step["description"] = _text(step.get("description"), f"steps.{key}.description")
        _refs(step.get("node_ids"), nodes, f"steps.{key}.node_ids", required=True)
        _refs(step.setdefault("edge_ids", []), edges, f"steps.{key}.edge_ids")
        duration = _integer(step.setdefault("duration_ms", 2400), f"steps.{key}.duration_ms", 100)
        if duration > 60000:
            raise StoryError(f"steps.{key}.duration_ms: split steps longer than 60 seconds")
        _evidence(step, sources, f"steps.{key}")
    scenarios = story.setdefault("scenarios", [{"id": "default", "label": "Walkthrough", "step_ids": list(steps)}] if steps else [])
    if not isinstance(scenarios, list):
        raise StoryError("scenarios: expected a list")
    for key, scenario in (_records(scenarios, "scenarios") if scenarios else {}).items():
        _text(scenario.get("label"), f"scenarios.{key}.label")
        _refs(scenario.get("step_ids"), steps, f"scenarios.{key}.step_ids", required=True)
    uncertainties = story.setdefault("uncertainties", [])
    if not isinstance(uncertainties, list) or any(not isinstance(s, str) or not s.strip() for s in uncertainties):
        raise StoryError("uncertainties: expected a list of non-empty strings")
    repo = story.setdefault("repo", {})
    if not isinstance(repo, dict):
        raise StoryError("repo: expected an object")
    ui_strings = story.setdefault('ui_strings', {})
    if not isinstance(ui_strings, dict) or any(not isinstance(k, str) or not isinstance(v, str) or not v.strip() for k, v in ui_strings.items()):
        raise StoryError('ui_strings: expected a dictionary of interface keys and translated text')
    translations = story.setdefault('translations', {})
    if not isinstance(translations, dict):
        raise StoryError('translations: expected language-tagged display text')
    collections = {'nodes': (nodes, {'label', 'description'}), 'edges': (edges, {'label'}), 'groups': (groups, {'label'}), 'steps': (steps, {'title', 'description'}), 'scenarios': ({s['id']: s for s in scenarios}, {'label'})}
    for locale, display in translations.items():
        if not isinstance(locale, str) or not re.fullmatch(r'[a-zA-Z]{2,8}(?:-[a-zA-Z0-9]{1,8})*', locale) or not isinstance(display, dict):
            raise StoryError('translations: expected valid language tags and display objects')
        for field, value in display.items():
            if field in ('title', 'question', 'summary'):
                _text(value, 'translations.'+field)
            elif field == 'uncertainties':
                if not isinstance(value, list) or any(not isinstance(v, str) for v in value):
                    raise StoryError('translations.uncertainties: expected text entries')
            elif field in collections:
                available, allowed = collections[field]
                if not isinstance(value, dict):
                    raise StoryError('translations.'+field+': expected display text by id')
                for identity, fields in value.items():
                    if identity not in available or not isinstance(fields, dict) or set(fields) - allowed:
                        raise StoryError('translations: display text cannot change graph topology or evidence')
                    for text_value in fields.values():
                        _text(text_value, 'translations.'+field)
            else:
                raise StoryError('translations: unsupported display field '+field)
    return story


def source_path(root, relative):
    """Allow repository-local files, including symlinks that stay inside root."""
    path = PurePosixPath(relative)
    if "\\" in relative or path.is_absolute() or PureWindowsPath(relative).is_absolute() or ".." in path.parts:
        raise StoryError(f"source path must stay inside the repository: {relative!r}")
    if not path.parts or relative in (".", ""):
        raise StoryError("source path must name a file")
    try:
        resolved = (root / Path(*path.parts)).resolve(strict=True)
        resolved.relative_to(root)
    except (ValueError, OSError, RuntimeError) as error:
        raise StoryError(f"source file is missing or escapes the repository: {relative!r}") from error
    if not resolved.is_file():
        raise StoryError(f"source is not a regular file: {relative!r}")
    return resolved


def _git(root, *args):
    env = dict(os.environ, GIT_NO_LAZY_FETCH="1", GIT_TERMINAL_PROMPT="0")
    try:
        result = subprocess.run(["git", "--no-pager", "-C", str(root), *args], env=env, capture_output=True, timeout=10)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    return result.stdout if result.returncode == 0 else None


def repository_url(value):
    """Return a credential-free HTTPS repository URL, never an executable scheme."""
    if not isinstance(value, str) or not value:
        return None
    if re.fullmatch(r"[^/@\s]+@[^/:\s]+:.+", value):
        authority, path = value.split(":", 1)
        value = "https://" + authority.split("@", 1)[1] + "/" + path
    parts = urlsplit(value)
    if parts.scheme == "ssh":
        parts = parts._replace(scheme="https", netloc=parts.hostname or "")
    if parts.scheme != "https" or not parts.hostname:
        return None
    path = parts.path.rstrip("/")
    if path.endswith(".git"):
        path = path[:-4]
    if len([part for part in path.split("/") if part]) < 2:
        return None
    return urlunsplit(("https", parts.hostname, path, "", ""))


def repository_snapshot(root):
    root = Path(root).resolve(strict=True)
    top = _git(root, "rev-parse", "--show-toplevel")
    if top is None or Path(os.fsdecode(top).strip()).resolve() != root:
        return {"name": root.name, "commit": None, "dirty": None, "url": None}
    head = _git(root, "rev-parse", "HEAD")
    origin = _git(root, "remote", "get-url", "origin")
    status = _git(root, "status", "--porcelain", "--untracked-files=normal")
    return {
        "name": root.name,
        "commit": os.fsdecode(head).strip() if head else None,
        "dirty": bool(status) if status is not None else None,
        "url": repository_url(os.fsdecode(origin).strip()) if origin else None,
    }


def prepare_story(data, repository):
    """Ground author-written claims in current files; never certify their interpretation."""
    story = validate_structure(data)
    root = Path(repository).resolve(strict=True)
    if not root.is_dir():
        raise StoryError("repository: expected a directory")
    snapshot = repository_snapshot(root)
    supplied_repo = story["repo"]
    expected_commit = supplied_repo.get("commit")
    if expected_commit is not None and expected_commit != snapshot["commit"]:
        raise StoryError("repo.commit: checkout does not match the story; re-read the intended revision")
    snapshot["name"] = _text(supplied_repo.get("name", root.name), "repo.name")
    story["repo"] = snapshot  # Do not carry absolute roots, credentials, or arbitrary author metadata.
    for source in story["sources"]:
        context = "source " + source["id"]
        path = source_path(root, source["path"])
        contents = path.read_bytes()
        if len(contents) > 8_000_000:
            raise StoryError(f"{context}: source exceeds the 8 MB text-file limit")
        try:
            lines = contents.decode("utf-8").splitlines()
        except UnicodeDecodeError as error:
            raise StoryError(f"{context}: source must be UTF-8 text") from error
        if source["end"] > len(lines):
            raise StoryError(f"{context}: lines {source['start']}–{source['end']} exceed the file's {len(lines)} lines")
        digest = hashlib.sha256(contents).hexdigest()
        if source.get("sha256") is not None and source["sha256"] != digest:
            raise StoryError(f"{context}: file changed since the story was grounded; re-read it")
        excerpt = "\n".join(lines[source["start"] - 1:source["end"]])
        if source.get("excerpt") is not None and source["excerpt"] != excerpt:
            raise StoryError(f"{context}: supplied excerpt does not match these lines")
        source["sha256"] = digest
        source["excerpt"] = excerpt
        source["excerpt_sha256"] = hashlib.sha256(excerpt.encode("utf-8")).hexdigest()
        source.pop("url", None)
        source.pop("commit", None)
        at_head = _git(root, "show", f"{snapshot['commit']}:{source['path']}") if snapshot["commit"] else None
        source["revision"] = "commit" if at_head == contents else "working-tree"
        if source["revision"] == "commit":
            source["commit"] = snapshot["commit"]
            origin = snapshot["url"]
            if origin and urlsplit(origin).hostname == "github.com":
                encoded_path = quote(source["path"], safe="/")
                source["url"] = f"{origin}/blob/{snapshot['commit']}/{encoded_path}#L{source['start']}-L{source['end']}"
    if repository_snapshot(root)["commit"] != snapshot["commit"]:
        raise StoryError("repo.commit changed while capturing sources; re-read the intended revision")
    story["grounding"] = {
        "status": "files-and-ranges-checked",
        "scope": "Source existence, line ranges and fingerprints. The author must verify the interpretation; this is not a runtime trace.",
    }
    return story


def read_story(path):
    try:
        text = Path(path).read_text(encoding="utf-8")
        if len(text) > 16_000_000:
            raise StoryError("story JSON exceeds the 16 MB limit")
        return json.loads(text)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise StoryError(f"cannot read story JSON: {error}") from error


def write_story(path, story):
    """Replace only after a complete serialization; never leave half-written output."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, prefix=path.name+".", suffix=".tmp", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(json.dumps(story, ensure_ascii=False, indent=2) + "\n")
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
