# Repo Visualizer

Explain how a repository works as a component graph, with inspectable code and animated exports. An open skill for Codex and Claude Code.

[Explore the live example](https://honzacuhel.github.io/repo-visualizer/) · [Download the skill](https://github.com/HonzaCuhel/repo-visualizer/releases) · [Verification](docs/verification.md)

![A source-grounded walkthrough of stack-diagram](site/media/walkthrough.gif)

The coding agent reads the repository, extracts responsibilities and relationships, and writes one canonical graph. The player visualizes that graph. Optional paths explain a feature without flattening the architecture into a linear diagram.

- Source references pinned to the analyzed revision, with embedded excerpts for offline inspection.
- Cycles, branches, parallel relationships, disconnected components and nested groups.
- A professional component explorer with graph and source inspection.
- Portable HTML plus PNG, SVG, GIF, MP4 and WebM through the same deterministic scene.

## Install the skill

Run inside your repository:

```sh
npx skills add HonzaCuhel/repo-visualizer --skill repo-visualizer -a codex -a claude-code
```

This installs project skills for both agents through the open [skills CLI](https://github.com/vercel-labs/skills). Choose one agent by keeping only its `-a` option; add `-g` for a personal installation across projects. The installer requires Node.js 22.20+. For a pinned release, use `HonzaCuhel/repo-visualizer@v0.1.0` as the source.

Alternatively, extract the release ZIP and copy the complete `repo-visualizer` folder into your agent's supported skill directory. Scripts, assets and notices must stay together. Core scan, validation and HTML assembly use Python 3.9+ and need no server. Animated exports need the [optional rendering environment](skills/repo-visualizer/references/exports.md).

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

## What has been tested

Fresh Codex and Claude Code sessions independently read the public stack-diagram source and produced their own graphs, offline HTML and changing GIF frames. A separate verification checked source fingerprints, graph interaction, offline operation and unchanged target source. Codex on macOS required approval of the trusted browser export command outside its OS sandbox. See [the test record and limits](docs/verification.md).

## Development

```sh
python3 -m unittest discover -s tests -v
uv sync --locked --extra export
python3 scripts/package_skill.py
```

The optional export environment requires Python 3.10+. Playwright Chromium must be installed, or an existing Chromium executable supplied with `--browser`.

Original code: MIT. Vendored ELK layout engine: EPL-2.0. Font: OFL-1.1. See [third-party notices](skills/repo-visualizer/NOTICE.md). Inspired by [stack-diagram](https://github.com/caru-ini/stack-diagram); its public source example retains its own MIT attribution.
