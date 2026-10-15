#!/usr/bin/env python3
"""Prepare neutral IDs and public annotations, without committing or publishing."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/public"
MAPPING = DATA / "audio/assets/id_mapping.json"


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def transform(value, replacements, track_indices):
    if isinstance(value, str):
        return replacements.get(value, value)
    if isinstance(value, list):
        return [transform(v, replacements, track_indices) for v in value]
    if isinstance(value, dict):
        result = {replacements.get(k, k): transform(v, replacements, track_indices) for k, v in value.items()}
        identity = next((result[k] for k in ("trackKey", "track_key", "id", "questionId") if k in result), "")
        match = re.match(r"^(HMU-A\d{6})(?:-Q\d{2})?$", str(identity))
        if match:
            for field in ("trackIndex", "track_index"):
                if field in result:
                    result[field] = track_indices[match[1]]
        return result
    return value


def replacements_for(mapping):
    replacements, indices = {}, {}
    for row in mapping["tracks"]:
        replacements[row["old_track_key"]] = row["track_id"]
        replacements[row["old_audio_path"]] = row["audio_path"]
        indices[row["track_id"]] = row["track_index"]
    for row in mapping["questions"]:
        replacements[row["old_id"]] = row["id"]
    return replacements, indices


def refresh_checksums(directory):
    paths = sorted(p for p in directory.rglob("*") if p.is_file() and p.name != "SHA256SUMS")
    (directory / "SHA256SUMS").write_text("".join(
        f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(directory).as_posix()}\n" for p in paths
    ), encoding="utf-8")


def prepare(source_zip):
    manifest_path = DATA / "audio/assets/manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if MAPPING.exists():
        mapping = json.loads(MAPPING.read_text(encoding="utf-8"))
    else:
        tracks, questions = [], []
        by_old_key = {}
        for index, (key, track) in enumerate(manifest["tracks"].items(), 1):
            row = {"old_track_key": key, "old_audio_path": track["assetPath"],
                   "track_id": f"HMU-A{index:06d}", "track_index": index,
                   "audio_path": f"assets/full/HMU-A{index:06d}.mp3", "audio_sha256": track["sha256"]}
            tracks.append(row)
            by_old_key[key] = row
        for old_id, item in manifest["questions"].items():
            row = by_old_key[item["trackKey"]]
            qindex = int(old_id.rsplit("-Q", 1)[1])
            questions.append({"old_id": old_id, "id": f"{row['track_id']}-Q{qindex:02d}"})
        mapping = {"schema_version": "1.0", "note": "Legacy labels identify source collections, not verified genres.",
                   "tracks": tracks, "questions": questions}
        write_json(MAPPING, mapping)
    replacements, indices = replacements_for(mapping)
    for path in sorted(DATA.rglob("*")):
        if path == MAPPING or path.suffix not in (".json", ".jsonl"):
            continue
        text = path.read_text(encoding="utf-8")
        if path.suffix == ".json":
            before = json.loads(text)
            after = transform(before, replacements, indices)
            if after != before:
                write_json(path, after)
        else:
            before = [json.loads(line) for line in text.splitlines() if line.strip()]
            after = transform(before, replacements, indices)
            if after != before:
                path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in after), encoding="utf-8")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["namingVersion"] = "neutral-audio-ids-v1"
    manifest["annotations"] = "annotations/tracks.jsonl"
    write_json(manifest_path, manifest)
    with zipfile.ZipFile(source_zip) as archive:
        source = [json.loads(line) for name in archive.namelist() if name.endswith(".jsonl")
                  for line in archive.read(name).decode("utf-8").splitlines() if line.strip()]
    by_key = {row["track_key"]: row for row in source}
    expected = {row["old_track_key"] for row in mapping["tracks"]}
    if len(source) != 92 or len(by_key) != 92 or set(by_key) != expected:
        raise ValueError("Source annotations must match all 92 tracks exactly")
    annotations = []
    for row in mapping["tracks"]:
        original = by_key[row["old_track_key"]]
        digest = hashlib.sha256(original["annotation"].encode("utf-8")).hexdigest()
        if original.get("annotation_sha256") and original["annotation_sha256"] != digest:
            raise ValueError(f"Annotation hash mismatch: {row['track_id']}")
        if original.get("audio_sha256") and original["audio_sha256"] != row["audio_sha256"]:
            raise ValueError(f"Audio hash mismatch: {row['track_id']}")
        annotations.append({"schema_version": "1.0", "track_id": row["track_id"],
                            "track_index": row["track_index"], "audio_path": row["audio_path"],
                            "audio_sha256": row["audio_sha256"], "annotation_format": original["annotation_format"],
                            "annotation": original["annotation"], "annotation_sha256": digest})
    path = DATA / "audio/annotations/tracks.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in annotations), encoding="utf-8")
    package_manifest = json.loads((DATA / "MANIFEST.json").read_text(encoding="utf-8"))
    package_manifest["public_contents"]["audio_annotations"] = "audio/annotations/tracks.jsonl"
    package_manifest["tracks"]["audio"]["annotation_count"] = len(annotations)
    package_manifest["audio_naming_version"] = "neutral-audio-ids-v1"
    write_json(DATA / "MANIFEST.json", package_manifest)
    refresh_checksums(DATA)
    review = [{"track_id": row["track_id"],
               "review_status": by_key[row["old_track_key"]].get("review_status"),
               "validation_warnings": by_key[row["old_track_key"]].get("validation_warnings", [])}
              for row in mapping["tracks"]]
    write_json(ROOT / "__preview__/annotation-review.json", review)
    print(json.dumps({"tracks": len(annotations), "questions": len(mapping["questions"]),
                      "source_records_with_warnings": sum(bool(r["validation_warnings"]) for r in review)}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_zip", type=Path)
    prepare(parser.parse_args().source_zip)
