# HMUBench-Audio

## Data

- `data/zh/questions.json`: 460 Chinese questions without answers.
- `data/en/questions.json`: 460 English questions without answers.
- `data/zh/with_answers.json`: Chinese reference answers and structured scoring
  fields.
- `data/en/with_answers.json`: English reference answers and structured scoring
  fields.
- `assets/full/`: 92 complete-track MP3 files.
- `assets/manifest.json`: question-to-audio paths, durations, byte sizes, and
  SHA-256 values.

The `audio_path` and `audio_relpath` fields are relative to this `audio/`
directory. For example:

```text
assets/full/jazz16/T01_01_12902ac27cb356db494b1b667c160c3e_0.mp3
```

Use only `questions.json` for model inference. During scoring, join the
matching `with_answers.json` by `id`. Do not add gold fields to the model
context.

## Input protocol

- Send one question per request.
- Provide the complete track for every question.
- When `scope=local`, use `time_range`, `section`, and `bar_range` to locate
  the target passage.

Public musical evidence is available in `with_answers.json`; complete model
answers and compact judge scores are under `model_outputs/`.
