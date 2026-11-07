# Release verification

## Version 0.2

The compact player adds user-controlled light/dark/system themes and English/Czech UI. Graph content can carry display-only translations; custom interface dictionaries support other output languages independently of the agent.

A fresh Codex run received a Czech prompt explicitly requesting French. It independently authored an 8-component, 9-relationship graph and all 103 French interface strings from public source, then produced offline HTML and a GIF with 72 distinct decoded frames. A separate verifier rechecked source fingerprints, dictionary completeness, format placeholders, offline operation and unchanged target files.

New regression checks exercise source-preserving language switches, custom translation safety, dark SVG/HTML downloads and edge endpoint attachment through nested groups. ELK may return root-level edges with coordinates relative to a declared nested container; honoring that container fixes the displaced edges visible in an earlier local repository output. The same correction is applied to all rebuilt examples.

Browser QA covers 320, 390, 1280, 1440 and 1672 pixel layouts, both themes, both bundled languages, persistence, unavailable storage, system preferences, installation copy controls, reduced motion and scroll reveals.

The independent Impeccable review returned `ship` for the scoped version 0.2 refinements after seven landing and five standalone viewport captures. It found no material visual repair within this scope. The version 0.1 workflow-ledger exception below remains historical and is not claimed as closed.

## Version 0.1

Verified locally on 7 November 2026. These checks establish artifact behavior and source matching, not the semantic correctness of every explanation.

## Fresh coding-agent runs

Both agents received the installed skill and a clean public stack-diagram fixture at revision `1ed53e3e9525364ae5d82e0430f2bb3f7ef4c838`. Each independently inventoried the code, read implementation, authored a graph, prepared its evidence and built HTML and GIF. Neither received a prewritten graph. Target scripts were not executed.

| Agent | Components / relationships / source references | GIF verification | Result |
| --- | --- | --- | --- |
| Codex 0.164.0 | 12 / 14 / 10 | 68 of 68 decoded frames distinct, 1440 × 900 | Complete after approval of the trusted export command outside the macOS sandbox |
| Claude Code 2.1.312 | 17 / 22 / 30 | Normal path: 120 of 120 frames distinct; missing-asset branch: 69 of 69, both 1200 × 1200 | Complete |

A separate verifier rechecked the source bytes, line ranges and fingerprints; opened each HTML with external HTTP(S) blocked; exercised component selection, source inspection and timeline seeking; and decoded the GIFs. No JavaScript errors, outbound requests or target-source modifications were found. An earlier Codex run without export approval produced valid HTML but no GIF; that run is not counted as a complete pipeline.

## Renderer and packaging

The automated suite covers graph validation, safe paths and source drift; static inventory; preserved nested groups, branches, cycles, parallel edges and disconnected nodes; hostile labels; deterministic seeking; source links; offline HTML downloads; package completeness; local PNG/SVG/GIF/MP4/WebM exports; and the optional HyperFrames adapter contract.

The public example has also been exported through the real HyperFrames renderer: H.264, 960 × 640, 10.5 seconds, 84 of 84 decoded frames distinct. Its deterministic GIF also has 84 of 84 distinct frames. Browser video recording is tested separately: it uses live capture and its duration can differ from the deterministic local exporter.

## Limits

- The agent authors the semantic explanation. Static imports are hints, and fingerprint validation is not proof that a relationship was interpreted correctly.
- Large graphs can make video labels too small. Start with a specific question, keep overviews scoped, and retain the zoomable HTML companion.
- HTML embeds source excerpts. Private-repository outputs stay local unless publication is authorized.
- Browser export needs an installed compatible Chromium and optional dependencies. OS sandbox approval may be required.
- A selected path illustrates source-derived behavior; it is not a recorded runtime execution.

## Historical version 0.1 design review exception

The independent Impeccable review checked the complete page at 320, 390, 1280, 1440 and 1672 pixels. Its requested SVG icon correction was resolved with no observed regression or remaining UI repair. The user approved the actual nonlinear graph workspace and explicitly authorized publication.

The Impeccable workflow ledger nevertheless remains `hero/open`, with later phases pending, because its comparison gate keeps applying an earlier illustrative linear mock. The restored first viewport matched the genuinely approved screenshot pixel for pixel before the icon correction. The historical form seed also could not be resolved by the current tool. The review therefore retains overall disposition `fix` for these tooling/provenance findings; no closed or passing design gate is claimed. This exception does not describe a failed rendering or agent test.
