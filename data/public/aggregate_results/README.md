# HMU-Bench Aggregate Results

This directory contains aggregate-only results. It does not include
question-level judge rationales or private workflow metadata.

## ABC

- `abc_aggregate_results.json`
- `abc_aggregate_results.md`

These files provide the aggregate ABC results for this benchmark release.

## Audio

Compact per-item judge scores and aggregate score summaries are under:

- `../model_outputs/scores/audio/`
- `../model_outputs/score_summary.json`

`audio_aggregate_results.json` reproduces paper Table 3, including five
scope/difficulty configurations and full-credit rates. These aggregates are
recomputed from the released scores; the display precision follows the paper.

Paper: https://arxiv.org/abs/2610.15773v1.
