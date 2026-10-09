# HMU-Bench

HMU-Bench is a bilingual benchmark for hierarchical music understanding by
omni models. It contains:

- **ABC Q&A:** 1,029 Chinese questions and 1,029 English questions.
- **Audio Q&A:** 460 Chinese questions and 460 English questions over 92
  complete tracks.

This repository contains benchmark data, public musical facts, model answers,
compact judge scores, prompts, and usage documentation.

## Repository layout

```text
data/public/       questions, public gold, prompts, model outputs, scores
docs/              dataset card
scripts/           local validation helper
```

The full audio-inclusive package and the minimal ready-to-use package are
distributed as GitHub Release assets rather than ordinary Git history. The
repository copy omits MP3 payloads.

## Quick start

From the repository root:

```bash
python3 scripts/validate_repo.py
```

### ABC

Use `data/public/abc/data/{zh,en}/questions.json` for inference. Join a model
response to the matching `with_answers.json` by `id`.

### Audio

Use `data/public/audio/data/{zh,en}/questions.json` for inference. Download
the full or minimal Release asset when audio files are needed. Resolve each
`audio_path` relative to the package's `audio/` directory and provide the
complete track.

### Model answers and scores

- Complete model answers: `data/public/model_outputs/responses/`
- Compact per-item judge scores: `data/public/model_outputs/scores/`
- Aggregate score summary: `data/public/model_outputs/score_summary.json`

Score files contain `id`, `score`, `label`, model name, and judge model only.
Judge rationales and missing/wrong explanations are not included.

### Prompts

The answering and evaluator prompts are under `data/public/prompts/`.
Evaluator prompts use the question, reference answer, public musical facts,
and candidate answer.

## Release assets

- Full: `HMUBench-2026-10-08-final-public.zip`
- Minimal: `HMUBench-2026-10-08-minimal.zip`

Both assets contain the benchmark's English documentation. The minimal asset
is intended for direct use and includes questions, reference answers, prompts,
92 MP3 files, and checksums.

## License and citation

The license placeholder must be replaced with approved data, code, and audio
notices before broad redistribution. See [`CITATION.cff`](CITATION.cff).
