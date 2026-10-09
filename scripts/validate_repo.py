#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/public"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate():
    errors = []
    abc_zh = load(DATA / "abc/data/zh/questions.json")
    abc_en = load(DATA / "abc/data/en/questions.json")
    abc_gold_zh = load(DATA / "abc/data/zh/with_answers.json")
    abc_gold_en = load(DATA / "abc/data/en/with_answers.json")
    audio_zh = load(DATA / "audio/data/zh/questions.json")
    audio_en = load(DATA / "audio/data/en/questions.json")
    audio_gold_zh = load(DATA / "audio/data/zh/with_answers.json")
    audio_gold_en = load(DATA / "audio/data/en/with_answers.json")
    manifest = load(DATA / "audio/assets/manifest.json")

    abc_ids = [item["id"] for item in abc_zh["questions"]]
    audio_ids = [item["id"] for item in audio_zh["questions"]]
    if len(abc_ids) != 1029 or len(set(abc_ids)) != 1029:
        errors.append("ABC count/uniqueness check failed")
    if abc_ids != [item["id"] for item in abc_en["questions"]]:
        errors.append("ABC bilingual IDs differ")
    if abc_ids != [item["id"] for item in abc_gold_zh["questions"]]:
        errors.append("ABC Chinese questions/gold IDs differ")
    if abc_ids != [item["id"] for item in abc_gold_en["questions"]]:
        errors.append("ABC English questions/gold IDs differ")
    if len(audio_ids) != 460 or len(set(audio_ids)) != 460:
        errors.append("Audio count/uniqueness check failed")
    if audio_ids != [item["id"] for item in audio_en["questions"]]:
        errors.append("Audio bilingual IDs differ")
    if audio_ids != [item["id"] for item in audio_gold_zh["questions"]]:
        errors.append("Audio Chinese questions/gold IDs differ")
    if audio_ids != [item["id"] for item in audio_gold_en["questions"]]:
        errors.append("Audio English questions/gold IDs differ")

    forbidden = {
        "verification",
        "provenance",
        "source_collection_id",
        "source_sample_id",
        "source_index",
        "original_reviewer",
        "item_id",
        "integration",
        "gold",
        "target",
    }
    for label, dataset in (
        ("abc/zh", abc_zh),
        ("abc/en", abc_en),
        ("audio/zh", audio_zh),
        ("audio/en", audio_en),
    ):
        for item in dataset["questions"]:
            leaked = sorted(forbidden.intersection(item))
            if leaked:
                errors.append(f"{label}/{item['id']} leaks {leaked}")
                break

    for label, dataset, audio in (
        ("abc-gold/zh", abc_gold_zh, False),
        ("abc-gold/en", abc_gold_en, False),
        ("audio-gold/zh", audio_gold_zh, True),
        ("audio-gold/en", audio_gold_en, True),
    ):
        for item in dataset["questions"]:
            if not str(item.get("reference_answer") or "").strip():
                errors.append(f"{label}/{item['id']} lacks reference answer")
                break
            if audio and (
                not isinstance(item.get("answer_key"), dict)
                or not isinstance(item.get("musical_facts"), dict)
            ):
                errors.append(f"{label}/{item['id']} lacks public scoring fields")
                break
            if forbidden.intersection(item):
                errors.append(f"{label}/{item['id']} contains internal fields")
                break

    if manifest.get("trackCount") != 92:
        errors.append("Audio manifest does not report 92 tracks")
    if len(manifest.get("questions", {})) != 460:
        errors.append("Audio manifest does not report 460 questions")
    for group in list(manifest.get("tracks", {}).values()) + list(
        manifest.get("questions", {}).values()
    ):
        if "sourceDataset" in group:
            errors.append("Audio manifest contains sourceDataset")
            break

    aggregate = load(DATA / "aggregate_results/abc_aggregate_results.json")
    if aggregate.get("question_count_per_language") != 1029:
        errors.append("ABC aggregate count is not 1,029")
    return {
        "status": "PASS" if not errors else "FAIL",
        "checks": {
            "abc_questions_per_language": len(abc_ids),
            "audio_questions_per_language": len(audio_ids),
            "abc_gold_per_language": len(abc_gold_zh["questions"]),
            "audio_gold_per_language": len(audio_gold_zh["questions"]),
            "audio_tracks_in_manifest": manifest.get("trackCount"),
            "abc_aggregate_models": len(aggregate.get("models", [])),
        },
        "errors": errors,
    }


if __name__ == "__main__":
    result = validate()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["status"] == "PASS" else 1)
