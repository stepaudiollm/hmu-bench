# HMUBench Final Public Release

- `abc/` contains 1,029 bilingual ABC-notation questions and reference answers.
- `audio/` contains 460 audio questions, 92 full-track MP3 assets, and audio results.
- `prompts/` contains answering and evaluator prompt templates.
- `aggregate_results/` contains compact aggregate score summaries.
- `model_outputs/responses/` contains complete final-set model answers.
- `model_outputs/scores/` contains compact per-item judge scores and labels.
- `model_outputs/score_summary.json` contains aggregate score counts and means.
- `MANIFEST.json` records the final version and publication requirements.
- `SHA256SUMS` contains SHA-256 checksums.
- `CITATION.cff` is a citation template.

Each language directory provides:

- `questions.json` for answer-blind model inference;
- `with_answers.json` with public gold for scoring and research inspection.

Audio gold also includes structured scoring fields and public musical evidence.
Complete model answers and compact judge scores are under `model_outputs/`;
judge rationales are not included.

## Quick start

Use the language-matched question file for inference and join responses to
the corresponding answer file by `id`.

### 2. Run ABC inference

Use only `questions.json` as model input:

```python
import json

with open("abc/data/en/questions.json", encoding="utf-8") as f:
    dataset = json.load(f)

item = dataset["questions"][0]
model_input = {
    "id": item["id"],
    "question": item["question"],
    "materials": item["materials"],
}
```

Do not put `with_answers.json` into the model context.

### 3. Run Audio inference

Use only `audio/data/{zh,en}/questions.json`. The `audio_path` is relative to
the `audio/` directory:

```python
import json
from pathlib import Path

with open("audio/data/en/questions.json", encoding="utf-8") as f:
    dataset = json.load(f)

item = dataset["questions"][0]
audio_file = Path("audio") / item["audio_path"]
question = item["question"]
```

Send one question per request and provide the complete track. For local items,
use `time_range`, `section`, and `bar_range` to identify the target window.

### 4. Score responses

Join model responses to the language-matched `with_answers.json` by `id`:

```python
with open("abc/data/en/with_answers.json", encoding="utf-8") as f:
    gold = {item["id"]: item for item in json.load(f)["questions"]}

reference = gold[item["id"]]["reference_answer"]
```

Audio scoring can additionally use `answer_key` and public musical evidence.
Do not pass these fields to the answering model.

### 5. Prompts and aggregate results

- Answering and evaluator prompts: `prompts/`
- ABC aggregate table: `aggregate_results/abc_aggregate_results.json`
- Model answers and compact scores: `model_outputs/`

Gold answers, complete model answers, and compact judge scores are public under
this release policy. Judge rationales are not included.
