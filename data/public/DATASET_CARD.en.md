# HMUBench Dataset Card

Version: `2026-10-08-final`

## ABC

- 1,029 questions aligned in Chinese and English.
- Day distribution: 257 / 256 / 256 / 260.
- Final revision: `abc-manual-revision-20261008`.
- Both answer-blind model inputs and public reference answers are included.

## Audio

- 460 questions over 92 full tracks, aligned in Chinese and English.
- Neutral track IDs: `HMU-A000001` through `HMU-A000092`; no genre labels in IDs.
- Full-track ABC annotations: 92 records in `audio/annotations/tracks.jsonl`.
- Audio paths are relative to `audio/` and use `assets/full/...`.
- Audio gold includes `reference_answer`, structured scoring fields, and
  public musical evidence.

## Evaluation

- The ABC aggregate table is included in machine-readable form.
- Audio includes seven-model aggregate results on a 0–4 scale.
- Audio judge: `qwen3.5-flash`.

## Public scope

- Data: included.
- Gold and public musical evidence: included.
- Answering and evaluator prompts: included.
- Aggregate results: included.
- Question-level graded responses: not included yet.

## Publication requirements

- Confirm dataset, code, and audio licenses.
- Confirm audio redistribution rights.

## Paper

[HMU-Bench: Hierarchical Music Understanding Benchmark for Omni Models](https://arxiv.org/abs/2610.15773), arXiv:2610.15773v1. Detailed results are in paper Tables 1 and 3.
