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
- `annotations/tracks.jsonl`: 92 complete-track ABC annotations, matched by
  neutral track ID and MP3 SHA-256.
- `annotations/README.md`: annotation schema and checksum definitions.

The `audio_path` and `audio_relpath` fields are relative to this `audio/`
directory. For example:

```text
assets/full/HMU-A000001.mp3
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

## Neutral naming

Track IDs are `HMU-A000001` through `HMU-A000092`; question IDs are
`HMU-A000001-Q01` through the fifth question per track. Track indexes are global
and unique across all 92 tracks. The names do not assert a genre.

The naming patch changes identifiers and paths only: question text, reference
answers, model responses, scores, MP3 bytes, and ABC annotation text are
preserved. A separate migration mapping lets existing users convert old IDs.

Annotations are reference data for research and scoring; do not include them
in audio-only answering model inputs. See `annotations/README.md` for fields.
