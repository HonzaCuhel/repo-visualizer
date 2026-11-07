# Codex: tool execution and the agent loop

Public source: [openai/codex](https://github.com/openai/codex), pinned to revision `33b3f80a0935e51a49cbbda7d6473ef757d4241b`.

- `graph.json`: focused shell execution example used on the landing page, with 6 components, 9 relationships, 25 source references and a 14.4-second walkthrough.
- `agent-loop.json`: the complete fresh Codex CLI result, with 11 components, 19 relationships, 37 source references and a 15-second walkthrough.
- `SOURCE-LICENSE` and `SOURCE-NOTICE`: exact Apache-2.0 license and NOTICE copied from the analyzed revision. Both are embedded in each graph's source license.
- `test-receipt.json`: sanitized record of the real skill installation and CLI run.

## Actual skill test

The official skill-installer fetched the public Repo Visualizer v0.2.0 skill into the global Codex skill directory. A fresh Codex CLI 0.164.0 session read that installed skill and the target source. It was given the question and output requirements, with no prewritten graph. It scanned, read implementation, authored canonical JSON and Czech display translations, prepared evidence, built offline HTML, and exported a 1200 × 800 GIF: 90 of 90 decoded frames differ, over 15 seconds. The session completed successfully in 280.78 seconds; this is a test record, not a generation-speed benchmark.

The OS sandbox blocked the initial browser launch. The approved local export used the installed exporter with Chromium's sandbox explicitly enabled. Neither the target application nor its scripts, builds or application APIs were run. Target source remained clean.

## Showcase scope

The complete agent-loop map is intentionally retained as the deeper example. The landing graph is an editorially scoped projection of its shell mechanism, with shorter labels and a new focused walkthrough. It retains the original cited source ranges and relationships, including conditional approval, parallel attempt/retry edges and the denial cycle. All landing HTML, GIF, MP4, PNG and SVG outputs are built from this one focused canonical graph. The overview does not claim to cover every Codex subsystem.

The source paths in this revision include `session/turn.rs`, tool routing and parallel dispatch, split `tools/handlers/unified_exec/` preparation, `tools/orchestrator.rs`, approvals, the unified execution runtime and process manager. Historical monolithic shell paths were not assumed.

## Meaning and limits

The walkthrough illustrates source-derived branches, not one observed execution. Approval rejection, sandbox denial and ordinary command failure remain distinct. A sandbox denial does not grant permission to retry; policy and the applicable review govern that decision. Backend, sandbox and reviewer behavior depend on configuration and platform. Source fingerprints establish matching bytes and ranges, not semantic correctness.

## Rebuild

```sh
python3 scripts/build_site.py
uv run --locked --extra export python scripts/render_showcase.py --browser /path/to/chromium
```

The source graph already contains pinned excerpts, so site/media rebuilding does not fetch or execute Codex. To independently revalidate its ranges and fingerprints, check out the exact source revision and run the skill's prepare command against that checkout.
