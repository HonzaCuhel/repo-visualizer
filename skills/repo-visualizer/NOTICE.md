# Third-party notices

Repo Visualizer's original code and skill instructions are MIT-licensed. The following components retain their own licenses:

- **elkjs 0.12.1**, unmodified browser bundle, copyright its Eclipse Layout Kernel contributors. Distributed under **EPL-2.0**, selected from its EPL-2.0 OR GPL-3.0-or-later licensing. License: `assets/vendor/ELK-LICENSE.md`. Original package and corresponding source: https://registry.npmjs.org/elkjs/-/elkjs-0.12.1.tgz and https://github.com/kieler/elkjs/tree/v0.12.1 (the ELK Java source is linked by that project). You may obtain the source under the same EPL-2.0 terms. Package provenance is recorded beside the bundle. No changes are made to its implementation; HTML assembly only escapes script closing delimiters for safe embedding.
- **gifenc 1.0.3**, copyright Matt DesLauriers and contributors, **MIT**. Unmodified CommonJS bundle wrapped for browser exports. License and package provenance are in `assets/vendor/`. Source: https://github.com/mattdesl/gifenc.
- **Atkinson Hyperlegible Next**, copyright its font authors, **SIL Open Font License 1.1**. License and exact source provenance: `assets/fonts/`. Font source: https://github.com/google/fonts/tree/main/ofl/atkinsonhyperlegiblenext.

Generated standalone HTML includes the layout engine and font. Their license texts and source availability notices remain accessible in the artifact. Repository source excerpts belong to their original authors and licenses; publication of a generated artifact must respect those permissions.

Export tools are optional and separately installed. HyperFrames is Apache-2.0; Playwright is Apache-2.0; Pillow uses the HPND license. FFmpeg builds have build-specific licensing and are not included in this distribution. See those tools' installed distributions for their notices.
