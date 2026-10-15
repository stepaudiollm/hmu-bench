# HMU-Bench — Minimal Ready-to-Use Release

Data version: `2026-10-08-final`. Audio naming patch: `2026-10-14`.

This package contains bilingual ABC questions and reference answers (1,029 per
language), bilingual audio questions and reference answers (460 per language),
92 complete MP3 tracks, 92 matched ABC annotations in JSONL, prompts, and checksums.

| Input | Questions | Reference answers |
| --- | --- | --- |
| ABC | `abc/{zh,en}/questions.json` | `abc/{zh,en}/answers.json` |
| Audio | `audio/{zh,en}/questions.json` | `audio/{zh,en}/answers.json` |

Use only `questions.json` for model inference. Answer files contain `id` and
`reference_answer`; join model responses to answers by `id`.

## Audio and annotations

Audio IDs are neutral: `HMU-A000001` through `HMU-A000092`. Question IDs append
`-Q01` through `-Q05`. File names and IDs do not encode a musical genre.

- MP3s: `audio/assets/full/HMU-A000001.mp3` and subsequent tracks.
- Audio manifest: `audio/assets/manifest.json`.
- Full-track ABC annotations: `audio/annotations/tracks.jsonl`.
- Annotation schema: `audio/annotations/README.md`.

Resolve each question's `audio_path` relative to `audio/`. Send one question per
request and supply the complete track, including for local questions. Use
`time_range`, `section`, and `bar_range` to locate the passage.

Keep reference answers and track annotations out of audio-only model inputs.
The naming patch preserves MP3 bytes, question text, answers, and annotation
text. Existing outputs using old IDs can be joined using the separately
distributed migration mapping.

## Integrity and prompts

`SHA256SUMS` covers every other file in this package. On macOS:

```bash
shasum -a 256 -c SHA256SUMS
```

Answering and evaluator prompt templates are in `prompts/`.

## Paper

[HMU-Bench: Hierarchical Music Understanding Benchmark for Omni Models](https://arxiv.org/abs/2610.15773). The full public package additionally provides the detailed aggregates from paper Tables 1 and 3.
