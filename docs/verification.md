# Release verification

## Public examples, width and scroll reveal — 8 November 2026

The public gallery now includes source-pinned Superpowers (13 components, 20 relationships) and OpenAI Whisper (12 components, 17 relationships) instead of the two stack-diagram rows. Each has full graph translations in English, Czech, German, French and Spanish, embedded source excerpts and the exact upstream MIT notice. Both were authored in this Codex session using the skill's scan, source inspection, prepare and build workflow; target repositories remained clean. No target agent, model weights or audio inference were executed. Superpowers describes prescribed instructions; Whisper explains implemented computation and transcription control, not learned-weight interpretation.

Both six-step highlight paths render to actual 18-second GIFs at 1200×800 and 6fps, with 108 distinct decoded frames each. Per-artifact provenance records hashes and source revisions. Browsers exercised both graphs in five languages, two themes, Map/Focus/Path, all component source panes, deterministic seeking, mobile/tablet layouts and actually downloaded offline HTML. No outbound requests or JavaScript errors were observed in the standalone tests.

The landing's header, explorer, status and footer share a maximum 1480px frame; measured boundaries match at 2756px. Reader-position reveals were checked at intermediate scroll positions, with focus/anchor completion, reduced-motion and no-JavaScript visibility. Responsive checks cover 390, 768, short 1440, 1920 and 2756px viewports, in addition to the 70 language/theme/width combinations. A visual-review finding in the German mobile export control was fixed with a wrapping toolbar; child-control bounds, overlap and open menus passed in 20 width/language combinations. The layout detector returned no findings. All 37 automated tests pass. The historical comparison-ledger exception below remains separate and is not claimed as closed.

## Landscape landing and language controls — 8 November 2026

The user selected the landscape composition and explicitly approved the assembled page. The public landing adds an original generated landscape, a real copyable installation command, a full interactive Codex graph, five language catalogs with flag icons, and separate light/dark/system buttons. The landscape is atmosphere, not a claim to depict a real location. Standalone HTML exports remove the landing assets and retain embedded fonts and source excerpts.

Verification for this change:

- 37 automated tests pass, including browser integration and localization checks.
- Browser checks pass for 70 combinations of seven widths (320–1600px), five languages and two themes, including pane boundaries; copy, empty-search recovery, Map/Focus/Path, playback, source inspection, keyboard language selection and an actually downloaded offline HTML were exercised.
- All 30 showcase media artifacts have matching source and artifact hashes. All ten GIFs decode to 120 frames at 1200×800 with changing content. All ten MP4 variants were actually played in Chromium and decoded at 1200×800.
- Scroll movement and reduced motion were exercised. Reduced motion disables the landscape transform. Graph playback remains an explicit action.
- Independent visual review identified mobile/tablet pane overlap; it was repaired and recaptured.

The Impeccable comparison ledger remains `hero/open` on the small GitHub navigation control despite an aggregate visual match and the user's explicit approval of the actual assembled page. No browser approval receipt or closed phase gate has been fabricated. This tooling limitation is separate from the functional checks above. The direction seed was issued and corroborated; shipping raster sources carry their generation prompt or runtime origin.

## Codex showcase

A fresh Codex CLI 0.164.0 session used the globally installed public v0.2.0 skill against `openai/codex` revision `33b3f80a0935e51a49cbbda7d6473ef757d4241b`. Given a question and no prewritten graph, it produced 11 components, 19 relationships, 37 revision-pinned sources, offline HTML, complete Czech display translations and a 15-second GIF with 90 of 90 decoded frames distinct. The target working tree remained clean. [Source, licensing and test receipt](../examples/codex/README.md).

The landing page and all public showcase media use the complete, unmodified agent-loop graph from that result: 11 components and 19 relationships, with English, Czech, German, French and Spanish display translations and light/dark themes. A focused shell execution graph remains an additional example. Both source graphs retain Codex's exact Apache-2.0 license and NOTICE. These are source interpretations, not runtime traces or a complete map of Codex.

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
