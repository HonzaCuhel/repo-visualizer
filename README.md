<div align="center">

<img src="site/assets/brand-mark.svg" width="52" height="52" alt="Repo Visualizer graph mark">

# Repo Visualizer

Ask how the code works. Explore the answer.

An open skill for **Codex** and **Claude Code**. Turn a repository question into an interactive component graph with source references and shareable animation.

[**Explore the demo**](https://honzacuhel.github.io/repo-visualizer/) · [Install](#quick-start) · [Download](https://github.com/HonzaCuhel/repo-visualizer/releases)

[![Check skill](https://github.com/HonzaCuhel/repo-visualizer/actions/workflows/check.yml/badge.svg)](https://github.com/HonzaCuhel/repo-visualizer/actions/workflows/check.yml)
[![Release](https://img.shields.io/github/v/release/HonzaCuhel/repo-visualizer?color=2164c7)](https://github.com/HonzaCuhel/repo-visualizer/releases)
[![MIT license](https://img.shields.io/badge/license-MIT-64748b)](LICENSE)

English · [Česky](README.cs.md)

</div>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="site/media/walkthrough-dark.gif">
  <img src="site/media/walkthrough.gif" alt="The Codex agent loop: user input, model responses, tool dispatch, approvals, sandbox execution and results fed back into conversation history." width="100%">
</picture>

**The example is Codex explaining Codex.** A fresh Codex CLI session used the installed skill to produce 11 components, 19 relationships and 37 revision-pinned source references. Explore the [complete agent loop](https://honzacuhel.github.io/repo-visualizer/codex-agent-loop.html), select a component and open the code behind it. [Source and test record](examples/codex/README.md).

<a id="install"></a>

## Quick start

Run inside the repository you want to understand:

```sh
npx skills add HonzaCuhel/repo-visualizer --skill repo-visualizer -a codex -a claude-code
```

Then ask your agent:

> Use repo-visualizer to explain how this feature works. Include components, branches and failure paths, with source references. Export an interactive HTML graph and a short GIF.

Keep one `-a` option to choose a single agent; add `-g` to install across projects. The command uses the existing [skills CLI](https://github.com/vercel-labs/skills) to fetch this GitHub repository. A complete skill ZIP and SHA-256 checksum are also available in [Releases](https://github.com/HonzaCuhel/repo-visualizer/releases).

<details>
<summary>Requirements</summary>

| Requirement | Purpose |
| --- | --- |
| Codex or Claude Code | Read implementation and author the explanation |
| Node.js 22.20+ | Install through npx |
| Python 3.9+ | Inventory, source validation and HTML assembly |
| Optional rendering environment | GIF, video and image exports; [setup](skills/repo-visualizer/references/exports.md) |

</details>

## Follow the mechanism

The agent reads the implementation and authors a graph of responsibilities and relationships. Branches, cycles, parallel edges and subsystem boundaries remain part of that graph.

| View | Use it to |
| --- | --- |
| **Map** | See the complete topology |
| **Focus** | Inspect a component and its immediate relationships |
| **Path** | Follow a source-derived walkthrough over the same graph |

Select a component or relationship to read embedded excerpts and open revision-pinned source links. Search, pan, zoom and seek at your own pace. The portable HTML works offline.

[Codex agent loop](https://honzacuhel.github.io/repo-visualizer/codex-agent-loop.html) · [Shell execution](https://honzacuhel.github.io/repo-visualizer/codex-shell.html) · [Portable HTML builder](https://honzacuhel.github.io/repo-visualizer/portable-builder.html)

## Share the explanation

**Interactive HTML · JSON · SVG · PNG · GIF · MP4 · WebM**

One canonical graph and one seekable scene drive the player and its exports. HTML keeps the clickable evidence; images and animation carry the visual explanation. [Export guide](skills/repo-visualizer/references/exports.md), including the optional HyperFrames adapter.

Choose light, dark or system appearance. Explanations follow your requested language, independently of the agent. English and Czech interface translations are bundled; other interface languages can provide an explicit dictionary. [Language and appearance](skills/repo-visualizer/references/localization.md).

## Evidence and limits

The skill inventories source without importing or executing the target repository. The agent then reads implementation, models the mechanism and validates source paths, ranges, fingerprints and revision before building the explorer.

Source matching checks the bytes; the agent's interpretation still needs review. A walkthrough illustrates source-derived behavior rather than recording a running application. Dense maps are best explored with zoom and component selection.

Generated HTML embeds source excerpts. Keep private outputs private. Rendering and exports run locally; your coding agent's existing data settings still apply.

Fresh Codex and Claude Code sessions have independently produced graphs, offline HTML and changing GIFs from public source. Automated checks cover topology, source matching, safe inputs, localization, themes, offline use, packaging and decoded animation frames. [Verification record](docs/verification.md).

## Development

```sh
python3 -m unittest discover -s tests -v
uv sync --locked --extra export
python3 scripts/build_site.py
python3 scripts/package_skill.py
```

Set `REPO_VISUALIZER_BROWSER` to an existing Chromium executable to include browser integration checks. The optional export environment uses Python 3.10+. See the [skill instructions](skills/repo-visualizer/SKILL.md), [graph format](skills/repo-visualizer/references/graph-format.md) and [export guide](skills/repo-visualizer/references/exports.md).

## Credits and license

The main example analyzes [openai/codex](https://github.com/openai/codex) at a pinned revision. Its Apache-2.0 license and NOTICE are retained with the embedded excerpts. [Source and test record](examples/codex/README.md).

Inspired by [caru-ini/stack-diagram](https://github.com/caru-ini/stack-diagram). Additional builder examples analyze its MIT-licensed source at a pinned revision and retain attribution.

Original code is **MIT**. Vendored ELK is **EPL-2.0**, gifenc is **MIT**, and Atkinson Hyperlegible Next is **OFL-1.1**. Full licenses and provenance ship with the skill. [Third-party notices](skills/repo-visualizer/NOTICE.md).
