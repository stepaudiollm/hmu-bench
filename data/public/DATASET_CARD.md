# HMUBench Dataset Card

Version: `2026-10-08-final`

## ABC

- 1,029 questions aligned in Chinese and English.
- Day distribution: 257 / 256 / 256 / 260.
- Final revision: `abc-manual-revision-20261008`.
- Both answer-blind model inputs and public reference answers are included.

## Audio

- 460 questions over 92 full tracks, aligned in Chinese and English.
- Source groups: Jazz16, Rock31, and Pop45.
- Audio paths are relative to `audio/` and use `assets/full/...`.
- Audio gold includes `reference_answer`, structured scoring fields, and
  public musical evidence.

## Evaluation

- ABC aggregate results are included in machine-readable form.
- Audio includes seven-model aggregate results on a 0–4 scale.
- Audio judge: `qwen3.5-flash`.

## Public scope

- Data: included.
- Gold and public musical evidence: included.
- Answering and evaluator prompts: included.
- Aggregate results: included.
- Question-level graded responses: not included.

## Publication requirements

- Confirm dataset, code, and audio licenses.
- Confirm audio redistribution rights.
