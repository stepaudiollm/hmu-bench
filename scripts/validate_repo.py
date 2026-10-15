#!/usr/bin/env python3
from __future__ import annotations

import json
import hashlib
import re
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

    tracks = manifest.get("tracks", {})
    expected_tracks = {f"HMU-A{index:06d}" for index in range(1, 93)}
    if set(tracks) != expected_tracks:
        errors.append("Neutral track IDs must cover HMU-A000001 through HMU-A000092")
    if set(manifest.get("questions", {})) != set(audio_ids):
        errors.append("Audio manifest question IDs differ from dataset")
    for track_id, track in tracks.items():
        if track.get("trackKey") != track_id or track.get("assetPath") != f"assets/full/{track_id}.mp3":
            errors.append(f"Incorrect neutral track identity/path: {track_id}")
        if track.get("trackIndex") != int(track_id.removeprefix("HMU-A")):
            errors.append(f"Incorrect global track index: {track_id}")
    for dataset in (audio_zh, audio_en, audio_gold_zh, audio_gold_en):
        for item in dataset["questions"]:
            entry = manifest["questions"].get(item["id"], {})
            track = tracks.get(entry.get("trackKey"), {})
            if not re.fullmatch(r"HMU-A\d{6}-Q0[1-5]", item["id"]):
                errors.append(f"Non-neutral audio question ID: {item['id']}")
            if (item.get("audio_path") != track.get("assetPath") or
                    item.get("audio_relpath") != track.get("relativePath") or
                    item.get("audio_sha256") != track.get("sha256") or
                    item.get("track_index") != track.get("trackIndex")):
                errors.append(f"Audio question/manifest join failed: {item['id']}")
    annotations = [json.loads(line) for line in (DATA / "audio/annotations/tracks.jsonl").read_text(encoding="utf-8").splitlines()]
    if len(annotations) != 92 or {r["track_id"] for r in annotations} != expected_tracks:
        errors.append("Annotation track coverage is not exactly 92 unique tracks")
    annotation_fields = {"schema_version", "track_id", "track_index", "audio_path", "audio_sha256", "annotation_format", "annotation", "annotation_sha256"}
    for item in annotations:
        track = tracks.get(item["track_id"], {})
        if set(item) != annotation_fields:
            errors.append(f"Unexpected public annotation fields: {item['track_id']}")
        if (item["audio_path"] != track.get("assetPath") or item["audio_sha256"] != track.get("sha256") or
                item["annotation_sha256"] != hashlib.sha256(item["annotation"].encode("utf-8")).hexdigest()):
            errors.append(f"Annotation integrity failed: {item['track_id']}")
    for kind in ("responses", "scores"):
        for modality, expected in (("abc", set(abc_ids)), ("audio", set(audio_ids))):
            for path in (DATA / f"model_outputs/{kind}/{modality}").rglob("*.jsonl"):
                rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
                ids = [r["id"] for r in rows]
                if len(ids) != len(expected) or set(ids) != expected:
                    errors.append(f"Model output coverage/join failed: {path.relative_to(DATA)}")

    for line in (DATA / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        path = DATA / name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            errors.append(f"Checksum failed: {name}")

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
            "audio_annotations": len(annotations),
            "abc_aggregate_models": len(aggregate.get("models", [])),
        },
        "errors": errors,
    }


if __name__ == "__main__":
    result = validate()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["status"] == "PASS" else 1)
