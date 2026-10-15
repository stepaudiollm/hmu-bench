#!/usr/bin/env python3
"""Build review copies of both releases from public data and verified legacy MP3s."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

from prepare_audio_update import DATA, ROOT, MAPPING, refresh_checksums, replacements_for, transform, write_json


def build(legacy_minimal, output):
    legacy_minimal = legacy_minimal.resolve()
    output = output.resolve()
    if not legacy_minimal.is_dir():
        raise ValueError("Pass an extracted minimal package directory")
    if output.exists():
        raise ValueError("Output directory already exists; choose a new directory")
    mapping = json.loads(MAPPING.read_text(encoding="utf-8"))
    replacements, indices = replacements_for(mapping)
    # Verify all inputs before writing either package.
    audio = []
    for row in mapping["tracks"]:
        source = legacy_minimal / "audio" / row["old_audio_path"]
        if not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest() != row["audio_sha256"]:
            raise ValueError(f"Missing or mismatched MP3 for {row['track_id']}")
        audio.append((source, row["audio_path"]))
    output.mkdir(parents=True)
    full = output / "HMUBench-2026-10-08-final-public"
    minimal = output / "HMUBench-2026-10-08-minimal"
    shutil.copytree(DATA, full)
    shutil.copytree(legacy_minimal, minimal, ignore=shutil.ignore_patterns("*.mp3", "SHA256SUMS", ".DS_Store"))
    for path in minimal.rglob("*"):
        if path.suffix == ".json":
            write_json(path, transform(json.loads(path.read_text(encoding="utf-8")), replacements, indices))
        elif path.suffix == ".jsonl":
            rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
            path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in transform(rows, replacements, indices)), encoding="utf-8")
    for package in (full, minimal):
        asset_root = package / "audio/assets/full"
        if asset_root.exists():
            shutil.rmtree(asset_root)
        for source, relative in audio:
            dest = package / "audio" / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, dest)
        # The mapping is a standalone migration aid, not part of the public packages.
        (package / "audio/assets/id_mapping.json").unlink(missing_ok=True)
        shutil.copytree(DATA / "audio/annotations", package / "audio/annotations", dirs_exist_ok=True)
        shutil.copyfile(DATA / "audio/README.md", package / "audio/README.md")
        shutil.copyfile(DATA / "audio/assets/manifest.json", package / "audio/assets/manifest.json")
    manifest = json.loads((minimal / "MANIFEST.json").read_text(encoding="utf-8"))
    manifest.update({"audio_naming_version": "neutral-audio-ids-v1", "audio_annotation_count": 92,
                     "audio_annotations": "audio/annotations/tracks.jsonl", "naming_patch_date": "2026-10-14"})
    write_json(minimal / "MANIFEST.json", manifest)
    # Minimal paths differ from the full package's data/{language} layout.
    manifest = json.loads((minimal / "audio/assets/manifest.json").read_text(encoding="utf-8"))
    manifest["dataset"] = {lang: f"{lang}/questions.json" for lang in ("en", "zh")}
    manifest["pathBase"] = "audio"
    write_json(minimal / "audio/assets/manifest.json", manifest)
    (minimal / "README.md").write_text((ROOT / "docs/MINIMAL_README.md").read_text(encoding="utf-8"), encoding="utf-8")
    minimal_audio_readme = (minimal / "audio/README.md").read_text(encoding="utf-8")
    for lang in ("en", "zh"):
        minimal_audio_readme = minimal_audio_readme.replace(f"data/{lang}/questions.json", f"{lang}/questions.json")
        minimal_audio_readme = minimal_audio_readme.replace(f"data/{lang}/with_answers.json", f"{lang}/answers.json")
    minimal_audio_readme = minimal_audio_readme.replace("Chinese reference answers and structured scoring\n  fields.", "Chinese reference answers.")
    minimal_audio_readme = minimal_audio_readme.replace("English reference answers and structured scoring\n  fields.", "English reference answers.")
    minimal_audio_readme = minimal_audio_readme.replace("`with_answers.json`", "`answers.json`")
    minimal_audio_readme = minimal_audio_readme.replace("Public musical evidence is available in `answers.json`; complete model\nanswers and compact judge scores are under `model_outputs/`.", "The full package additionally includes structured musical facts, model answers,\nand compact judge scores.")
    (minimal / "audio/README.md").write_text(minimal_audio_readme, encoding="utf-8")
    # Validate bilingual joins and byte-for-byte audio integrity in each package.
    checks = {}
    for package in (full, minimal):
        tracks = json.loads((package / "audio/assets/manifest.json").read_text(encoding="utf-8"))["tracks"]
        for item in tracks.values():
            path = package / "audio" / item["assetPath"]
            if path.stat().st_size != item["bytes"] or hashlib.sha256(path.read_bytes()).hexdigest() != item["sha256"]:
                raise ValueError(f"Packaged audio integrity failed: {path}")
        for modality, count in (("audio", 460), ("abc", 1029)):
            datasets = []
            for lang in ("en", "zh"):
                base = package / modality / (f"data/{lang}" if package == full else lang)
                question = json.loads((base / "questions.json").read_text(encoding="utf-8"))
                answer = json.loads((base / ("with_answers.json" if package == full else "answers.json")).read_text(encoding="utf-8"))
                qrows = question["questions"]
                arows = answer.get("questions", answer.get("answers")) if isinstance(answer, dict) else answer
                if isinstance(arows, dict):
                    arows = [{"id": k} for k in arows]
                qids = [q["id"] for q in qrows]
                if len(qids) != count or len(set(qids)) != count or set(qids) != {a["id"] for a in arows}:
                    raise ValueError(f"Question/answer join failed: {base}")
                if modality == "audio" and any(not (package / "audio" / q["audio_path"]).is_file() for q in qrows):
                    raise ValueError(f"Audio path check failed: {base}")
                datasets.append(qids)
            if datasets[0] != datasets[1]:
                raise ValueError(f"Bilingual IDs differ: {package}/{modality}")
        refresh_checksums(package)
        archive_path = output / f"{package.name}.zip"
        with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
            for path in sorted(package.rglob("*")):
                if path.is_file():
                    archive.write(path, path.relative_to(output).as_posix())
        checks[package.name] = {"mp3_count": len(list((package / "audio/assets/full").glob("*.mp3"))),
                                "sha256": hashlib.sha256(archive_path.read_bytes()).hexdigest(),
                                "zip_bytes": archive_path.stat().st_size}
    migration = output / "HMUBench-audio-id-mapping.json"
    shutil.copyfile(MAPPING, migration)
    annotation_zip = output / "HMUBench_audio_annotations_20261014.zip"
    annotation_package = output / "HMUBench_audio_annotations_20261014"
    for source, relative in audio:
        dest = annotation_package / "audio" / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, dest)
    shutil.copytree(DATA / "audio/annotations", annotation_package / "audio/annotations")
    track_manifest = json.loads((DATA / "audio/assets/manifest.json").read_text(encoding="utf-8"))
    write_json(annotation_package / "audio/assets/manifest.json", {
        "schemaVersion": "hmu-audio-annotation-assets-v1", "trackCount": 92,
        "pathBase": "audio", "tracks": track_manifest["tracks"]})
    write_json(annotation_package / "MANIFEST.json", {
        "name": "HMU-Bench audio and annotations", "track_count": 92,
        "annotation_count": 92, "annotations": "audio/annotations/tracks.jsonl",
        "audio_manifest": "audio/assets/manifest.json",
        "paper": "https://arxiv.org/abs/2610.15773"})
    shutil.copyfile(ROOT / "docs/ANNOTATIONS_README.md", annotation_package / "README.md")
    refresh_checksums(annotation_package)
    with zipfile.ZipFile(annotation_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(annotation_package.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(output).as_posix())
    checks[annotation_package.name] = {"mp3_count": len(audio), "annotation_count": 92,
        "sha256": hashlib.sha256(annotation_zip.read_bytes()).hexdigest(), "zip_bytes": annotation_zip.stat().st_size}
    write_json(output / "validation_report.json", {"status": "PASS", "packages": checks,
                                                  "annotation_count": 92, "audio_bytes_unchanged": True})
    print(json.dumps(checks, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--legacy-minimal", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    build(args.legacy_minimal, args.output)
