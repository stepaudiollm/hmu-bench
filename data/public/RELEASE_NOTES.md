# HMUBench 2026-10-08-final Release Notes

## Included

- HMUBench-ABC: 1,029 Chinese questions and 1,029 English questions.
- HMUBench-Audio: 460 Chinese questions and 460 English questions.
- 92 portable full-track MP3 assets.
- Audio seven-model aggregate results.
- ABC aggregate results.
- ABC and Audio answering/evaluator prompt templates.
- Public reference answers, model answers, and compact judge scores.
- Current bilingual ID alignment, checksum, and portability validation.

## Packaging

- Public question files are answer-blind.
- Current gold answers are included as separate `with_answers.json` files.
- Model inference must use `questions.json`, not the gold files.
- Results are aggregate-only; per-question model responses are not included.
- Audio paths are relative to `audio/`.

## Publication requirements

- Final licenses are still to be assigned.
- Audio redistribution rights must be confirmed.
