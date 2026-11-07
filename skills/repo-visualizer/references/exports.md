# Exports

Build the standalone HTML first. It contains the graph, code excerpts, layout engine and font; it works offline and preserves clickable evidence. Excerpts may contain private code: publication needs the repository owner's authorization.

## Browser menu

The explorer can download HTML, graph JSON, SVG, PNG and animated GIF directly. Its offline GIF encoder is vendored under MIT. MP4/WebM use the browser's video recorder when the selected codec is supported; timing depends on live capture performance. The local exporters below are preferable for reproducible dimensions and frame timing. Unsupported browser codecs produce an actionable error; no file is renamed to pretend to be another format.

Browser HTML downloads embed the font and source excerpts and reopen with working controls. Source licenses are retained in HTML and SVG metadata. PNG/GIF/video show a rendered explanation; the HTML companion preserves clickable evidence.

## Deterministic local renderer

Core build uses only Python 3.9+ standard library. Optional export dependencies are Playwright and Pillow; video additionally needs FFmpeg, or imageio-ffmpeg. Install them in an isolated environment, not in the analyzed repository.

```sh
uv run --with playwright --with pillow --with imageio-ffmpeg python <skill>/scripts/export.py explorer.html -o explanation.mp4
```

Install Chromium in that environment using `python -m playwright install chromium`, or pass `--browser /path/to/an/existing/chromium`. Export blocks outbound HTTP(S) requests. `--width`, `--height`, `--fps`, `--scenario` set output. `--theme light|dark|system` selects appearance; `--language <tag>` selects the interface and any supplied graph translation; `--at` is a static capture position in milliseconds. PNG captures the explorer viewport. SVG exports the complete vector graph at its layout bounds, including embedded styles/font. GIF, MP4 and WebM animate the authored path, or a clearly labeled component tour if no path exists. They use the same `window.renderAt(ms)` as the interactive player. MP4/WebM pad odd dimensions by one pixel for codec compatibility.

On macOS, a coding agent's OS sandbox can prevent Chromium from launching even when HTML assembly succeeds. Request approval for the specific trusted export command using the agent's normal approval mechanism. Do not disable browser or agent protections to work around this. If approval is unavailable, deliver the working HTML and report the animation as incomplete.

The output is replaced only after a successful render. GIF encoding retains frames in memory: use lower resolution/fps for long graphs. Prefer MP4 for long explanations and GIF for compact README previews. A video cannot retain clickable source links; ship the HTML alongside it.

## HyperFrames

HyperFrames is an optional video rendering adapter, not the canonical graph format. Its root composition and seekable timeline drive the same deterministic player; React and GSAP are not required. The adapter caches the graph layout coordinates from the actual player, removes the browser-only playback clock, and drives the shared scene through a seekable timeline. The integration is pinned and must be verified with a real rendered video, including duration and changing decoded frames. Use the supplied adapter command rather than rebuilding a second scene by hand:

```sh
uv run --with playwright python <skill>/scripts/hyperframes_export.py explorer.html -o explanation.mp4
```

`--hyperframes /path/to/executable` selects an existing CLI. Otherwise it invokes the pinned `hyperframes@0.9.20` through pnpm or npx. Node 22+, HyperFrames Chrome and FFmpeg/FFprobe must be available; `hyperframes browser ensure` prepares its browser. The generated composition is temporary and contains the same embedded source excerpts as the HTML. Rendering is local; no login or cloud publishing command is used. It declares a readiness barrier so graph layout completes before capture. HyperFrames uses Apache-2.0; its browser/FFmpeg dependencies remain separately installed.

Remotion can consume the same graph/time model in a future adapter. It currently requires a React composition and has separate licensing terms, so it is not a mandatory dependency of this open skill.
