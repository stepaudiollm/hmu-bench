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
- Complete per-question model responses and compact judge scores are included.
- Audio paths are relative to `audio/`.

## Publication requirements

- Final licenses are still to be assigned.
- Audio redistribution rights must be confirmed.

## Audio naming and annotation update — 2026-10-14

- Replace genre-bearing track names, audio paths, and question IDs with neutral IDs.
- Synchronize all bilingual questions, answers, manifests, model outputs, and scores.
- Add 92 original full-track ABC annotations in one normalized public JSONL.
- Preserve MP3 bytes and original annotation text; omit editorial workflow fields.
- Regenerate package checksums; distribute the ID migration map separately.

## Paper and demo update

- Add the published paper link and complete author citation.
- Add Audio Table 3 configuration means and FCR, reproduced from released scores.
- Document paper Table 1 aggregate results separately from compact raw-score summaries.
- The separate static demo uses only three audio examples and twelve notation examples; full release packages retain all 92 tracks.

## Audio annotation package

The standalone annotation ZIP includes all 92 complete MP3s alongside the matched JSONL, schema documentation, and checksums.
