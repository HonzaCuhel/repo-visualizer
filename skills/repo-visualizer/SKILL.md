---
name: repo-visualizer
description: Explain how a repository or feature works as a source-grounded component graph, with an interactive HTML explorer and optional animated GIF or video exports. Use for architecture maps, code walkthroughs, onboarding, dependency explanations, and visual answers to questions like “how does why-moving work?”.
---

# Repo Visualizer

Turn code into a graph someone can understand. The graph is the artifact; a narrated path is optional. Preserve branches, parallel relationships, cycles, disconnected components, and subsystem boundaries. Never force a repository into a sequence of boxes.

## Workflow

1. **Choose the question, scope and language.** Read the repository guide and entry points. If the user names a feature, trace that feature. Otherwise identify the major responsibilities and produce an overview. Ask at most one useful clarification while continuing independent inspection. Use the output language explicitly requested by the user; otherwise use the user's language. This is independent of whether the agent is Codex, Claude Code or another compatible agent. Set the graph's BCP-47 `language` tag, and write its title, descriptions, labels, walkthrough and uncertainties in that language. Keep source code, symbols and paths unchanged.
2. **Inventory without running the target.** `python3 <skill>/scripts/repo_story.py scan --repo <repo> --output <artifacts>/inventory.json`. Use repeated `--path` to narrow large repositories. Python AST imports and call candidates are hints; other languages require your own source inspection. This is not a complete behavioral analysis.
3. **Read and model the mechanism.** Follow definitions, callers, configuration, state stores, queues, retries and failure exits. Group by responsibility rather than directory alone. Prefer 8–20 meaningful components for a first overview; offer deeper graphs when useful. A component can represent a module, service, function, store, queue or external actor. Keep distinct components and parallel edges when they mean different things.
4. **Write the canonical graph.** Follow [references/graph-format.md](references/graph-format.md). Every factual node and relationship needs exact source references. Read those ranges; do not invent line numbers. Record uncertain relationships as `evidence: inferred` with a concrete reason, and list important unknowns. Static code is evidence of implementation, not an observed runtime trace. Optional steps highlight paths through the existing graph. A component tour must be labeled as a tour, never as execution order.
5. **Prepare and build.** `python3 <skill>/scripts/repo_story.py prepare graph.json --repo <repo> -o prepared.json`, then `python3 <skill>/scripts/repo_story.py build prepared.json -o explorer.html`. Preparation checks local paths, ranges, fingerprints and Git revision. Inspect the resulting graph and source pane; structural validation cannot prove your explanation is correct.
6. **Export when requested.** The HTML is portable and interactive. Use `python3 <skill>/scripts/export.py explorer.html -o output.gif` (or `.mp4`, `.webm`, `.png`, `.svg`). The exporter drives the same deterministic scene. See [references/exports.md](references/exports.md) for dependencies and the optional HyperFrames adapter. Never describe an animation as exported until the actual output has been inspected.
7. **Deliver.** Link the HTML and requested exports, summarize what the graph explains, disclose unresolved relationships and static-analysis limits. Preserve source attribution and include the repository’s exact license notice as `source_license` when available. Keep private repository content local unless the user explicitly authorizes publication. An HTML file contains its embedded source excerpts.

## Model quality

- Put responsibilities and meaningful verbs on nodes and edges. Avoid file-count hairballs and generic “connects to” labels.
- Keep the introduction concise: one or two short sentences, with detailed context in uncertainties. Do not put a full commit hash, component counts or duration into prose; the explorer formats those separately. Optional `overview.lead` is a short visible introduction and `overview.path` contains `{node_id, label}` entries referencing real components. It is orientation, not a replacement graph or a claimed execution trace.
- Preserve topology. A retry loop stays a loop; two independent consumers stay branches. Do not turn import ordering into execution ordering.
- Include important gates, empty results, errors and retries. Separate “accepted”, “attempted”, “sent” and “completed” when the code does.
- Link evidence to the selected component or relationship, pinned to the analyzed revision when possible. Dirty files use embedded local evidence rather than a false remote permalink.
- Keep public examples grounded in public source. Do not upload target code, run migrations, call production services, invoke agents with paid APIs, or execute target scripts as part of extraction.
- Maintain one graph model for every view and output. Layout coordinates and animation state are presentation, never another hand-maintained graph.

## Presentation

Use the shipped professional explorer: compact component navigation, a dominant graph, and a readable source inspector. White/cool neutral background, charcoal text, restrained blue selection, thin rules, no decorative 3D or glowing effects. The overview is immediately visible; animation is optional and respects reduced motion. Make sources and controls work by keyboard. For large graphs, scope before shrinking text into illegibility.

## Tools and paths

The explorer has user-controlled light/dark/system appearance and interface language. English and Czech controls are bundled. For another requested language, translate every value from `assets/locales/en.json` into the graph's `ui_strings` object; preserve keys and `{placeholders}`. Optional `translations` provide display text in multiple graph languages while preserving ids, topology and source evidence. See [references/localization.md](references/localization.md). Do not claim automatic translation of existing graph content or source code.

Resolve `<skill>` to this skill's directory. Core scan/prepare/build use Python 3.9+ standard library. Rendering exports has optional dependencies; do not install them silently into the target repository. Store generated artifacts outside source paths, preferably a user-selected output directory. Output creation must not overwrite source files. The skill works in Codex and Claude Code without a repository-specific runtime or server.
