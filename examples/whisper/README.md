# Whisper: from audio to text

Audio preprocessing, the encoder–decoder Transformer, autoregressive token generation and transcription fallback. This is a static source explanation, not a model run or an interpretation of learned weights.

Source: [openai/whisper](https://github.com/openai/whisper/tree/86098128c0b4f24f0e2aa2994de830614b474227) at `86098128c0b4f24f0e2aa2994de830614b474227`.

12 components; 17 relationships; six optional animated highlights. Graph text and interface in English, Czech, German, French and Spanish. Source excerpts are embedded with byte fingerprints and pinned links. Upstream MIT notice: [LICENSE.upstream](LICENSE.upstream).

[Open the explorer](https://honzacuhel.github.io/repo-visualizer/whisper.html).

Generated with the repo-visualizer scan → inspect → graph → prepare → build workflow. No target scripts, model weights or paid agents were run.

[Animated GIF, 18 seconds](https://honzacuhel.github.io/repo-visualizer/media/whisper.gif) · [Render provenance](../../site/media/whisper.gif.provenance.json). The HTML companion preserves clickable source evidence.

## Decoder detail

[Decoder loop](https://honzacuhel.github.io/repo-visualizer/whisper-decoder.html) is a focused 7-component, 7-relationship view with the encoder above and token context below the decoder computation. Shared bands reuse actual source-grounded nodes. The full transcription graph above retains windows, silence handling and fallback. [Canonical focused graph](decoder-loop.json).

[Decoder GIF, 12 seconds](https://honzacuhel.github.io/repo-visualizer/media/whisper-decoder.gif) · [Video](https://honzacuhel.github.io/repo-visualizer/media/whisper-decoder.mp4) · [SVG](https://honzacuhel.github.io/repo-visualizer/media/whisper-decoder.svg). These exports use the same diagram and source model as the interactive HTML.
