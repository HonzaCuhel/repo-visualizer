# Repo Visualizer

Explain how a repository works as a component graph, with inspectable code and animated exports. An open skill for Codex and Claude Code.

**Current status:** working local preview. The graph explorer, source inspection, standalone HTML and export engines are implemented and tested. Website review and public release are still in progress; no deployed site or published release is claimed yet.

The coding agent reads the repository, extracts responsibilities and relationships, and writes one canonical graph. The player visualizes that graph. Optional paths explain a feature without flattening the architecture into a linear diagram.

- Source references pinned to the analyzed revision, with embedded excerpts for offline inspection.
- Cycles, branches, parallel relationships, disconnected components and nested groups.
- A professional component explorer with graph and source inspection.
- Portable HTML plus PNG, SVG, GIF, MP4 and WebM through the same deterministic scene.

## Install the skill

From a local checkout, the tested installer command is:

```sh
npx skills@1.7.6 add ./skills/repo-visualizer --agent codex --agent claude-code --copy --yes
```

This installs project skills for both agents. Alternatively, copy `skills/repo-visualizer` into your agent's personal skills directory, or your repository's supported skill directory. Keep the folder intact: scripts, assets and notices are required. No npm package or server is needed for scan, validation and HTML assembly. Python 3.9+ is sufficient for those commands.

Ask your agent:

> Use repo-visualizer to explain how this feature works. Extract its main components and relationships, include failure paths, and give me an interactive graph with code references and a short animated walkthrough.

The skill's [instructions](skills/repo-visualizer/SKILL.md) describe the full workflow. [Graph format](skills/repo-visualizer/references/graph-format.md) and [exports](skills/repo-visualizer/references/exports.md) are documented separately.

## How extraction works

`scan` inventories source modules and Python static imports without importing or executing target code. It provides a starting point, not a complete architecture detector. The coding agent inspects real implementations and refines the inventory into meaningful components and typed relationships. Source fingerprints catch code drift; they do not prove the agent's interpretation.

```sh
python3 skills/repo-visualizer/scripts/repo_story.py scan --repo /path/to/repository -o /path/to/artifacts/inventory.json
python3 skills/repo-visualizer/scripts/repo_story.py prepare graph.json --repo /path/to/repository -o prepared.json
python3 skills/repo-visualizer/scripts/repo_story.py build prepared.json -o explorer.html
```

Generated HTML contains source excerpts. Keep private repositories' artifacts private unless publication is authorized.

## Development

```sh
python3 -m unittest discover -s tests -v
uv sync --locked --extra export
python3 scripts/package_skill.py
```

The optional export environment requires Python 3.10+. Playwright Chromium must be installed, or an existing Chromium executable supplied with `--browser`.

Original code: MIT. Vendored ELK layout engine: EPL-2.0. Font: OFL-1.1. See [third-party notices](skills/repo-visualizer/NOTICE.md). Inspired by [stack-diagram](https://github.com/caru-ini/stack-diagram); its public source example retains its own MIT attribution.
