#!/usr/bin/env python3
"""Reproduce paper Table 3 from released per-question scores and question labels."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/public"
CONFIGURATIONS = [("global", "easy"), ("global", "hard"), ("local", "easy"), ("local", "medium"), ("local", "hard")]
MODELS = [("qwen35_omni_plus", "Qwen 3.5 Omni"), ("gemini31_pro", "Gemini 3.1 Pro"),
          ("gemini37_flash", "Gemini 3.7 Flash"), ("seed_lite", "Seed Lite"),
          ("qwen3_omni_flash", "Qwen 3 Omni"), ("stepaudio3_0909", "StepAudio 3"), ("gemini25_pro", "Gemini 2.5 Pro")]


def build():
    questions = {r["id"]: r for r in json.loads((DATA / "audio/data/en/questions.json").read_text(encoding="utf-8"))["questions"]}
    models = []
    for model, label in MODELS:
        overall, rows = {}, []
        for lang in ("zh", "en"):
            values = [json.loads(line) for line in (DATA / f"model_outputs/scores/audio/{lang}/{model}.jsonl").read_text(encoding="utf-8").splitlines()]
            assert len(values) == 460 and {r["id"] for r in values} == set(questions)
            overall[lang] = round(sum(r["score"] for r in values) / len(values), 3)
            rows.extend(values)
        groups = {}
        for scope, difficulty in CONFIGURATIONS:
            scores = [r["score"] for r in rows if (questions[r["id"]]["scope"], questions[r["id"]]["difficulty"]) == (scope, difficulty)]
            assert len(scores) == 184
            groups[f"{scope}_{difficulty}"] = {"score": round(sum(scores) / len(scores), 3), "fcr_percent": round(100 * scores.count(4) / len(scores), 2)}
        models.append({"id": model, "label": label, "overall": overall, "configurations": groups})
    result = {"schema_version": "hmu-bench-audio-aggregate-v1", "paper": "https://arxiv.org/abs/2610.15773v1", "paper_table": 3,
              "question_pairs": 460, "track_count": 92, "configuration_question_pairs": 92,
              "subgroup_language_policy": "Each subgroup aggregates both languages (184 responses per model)",
              "fcr_definition": "Percentage of responses with score 4", "models": models}
    path = DATA / "aggregate_results/audio_aggregate_results.json"
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Built paper-aligned Audio Table 3 aggregates")


if __name__ == "__main__":
    build()
