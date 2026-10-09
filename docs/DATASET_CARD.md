# HMUBench Dataset Card

Version: `2026-10-08-final`

## HMUBench-ABC

- Input: ABC notation excerpts and natural-language questions.
- Scale: 1,029 aligned questions in Chinese and English.
- Day distribution: 257 / 256 / 256 / 260.
- Coverage: tonality and harmony, pitch and melody, rhythm, form and
  chronology, global metadata, and other verifiable symbolic-music tasks.
- ABC materials: 1,168 excerpts.
- Final revision: `abc-manual-revision-20261008`.

## HMUBench-Audio

- Input: a complete track and one question per request.
- Scale: 460 aligned questions in Chinese and English over 92 tracks.
- Source groups: Jazz16, Rock31, and Pop45.
- Local questions use `time_range`, `section`, and `bar_range` as locators,
  while the model still receives the complete track.
- Public audio paths are relative to `PUBLIC_RELEASE/audio/` and use
  `assets/full/...`.

## Data layers

- `questions.json` is the answer-free model input.
- `with_answers.json` provides public reference answers; Audio editions also
  include structured scoring fields and public musical evidence.
- Answering prompts, evaluator prompts, complete model answers, and compact
  judge scores are public.
- Judge rationales and missing/wrong explanations are not included.

## Evaluation

- 460 questions per language.
- Seven evaluated models on a 0–4 scale.
- Judge: `qwen3.5-flash`.

## Publication requirements

1. Confirm the dataset, code, and audio licenses.
2. Confirm redistribution rights for all 92 audio files.
3. Add the approved citation and contact information.
