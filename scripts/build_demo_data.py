#!/usr/bin/env python3
"""Export real public benchmark examples and reported scores for the static demo."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/public"
EXAMPLES = json.loads((ROOT / "demo/examples.json").read_text(encoding="utf-8"))
EXAMPLE_TRACK_IDS = tuple(EXAMPLES["audio_track_ids"])


def load(path):
    return json.loads((DATA / path).read_text(encoding="utf-8"))


def build():
    manifest = load("audio/assets/manifest.json")
    annotations = {r["track_id"]: r for r in map(json.loads, (DATA / "audio/annotations/tracks.jsonl").read_text(encoding="utf-8").splitlines())}
    audio = {}
    for lang in ("en", "zh"):
        audio[lang] = [{k: r.get(k) for k in ("id", "question", "reference_answer", "scope", "domain", "difficulty", "section", "time_range", "bar_range")}
                       for r in load(f"audio/data/{lang}/with_answers.json")["questions"]]
    # A small, deterministic symbolic example set spanning question types.
    abc = {}
    english = load("abc/data/en/with_answers.json")["questions"]
    selected = EXAMPLES["abc_question_ids"]
    for lang in ("en", "zh"):
        by_id = {r["id"]: r for r in load(f"abc/data/{lang}/with_answers.json")["questions"]}
        abc[lang] = [by_id[key] for key in selected]
        for item in abc[lang]:
            item["display_key_withheld"] = item["id"] in EXAMPLES["key_withheld_question_ids"]
    bundle = {"tracks": [{"id": key, "index": r["trackIndex"], "duration": r["durationSec"],
                          "audio_path": r["assetPath"], "annotation": annotations[key]["annotation"]}
                         for key, r in manifest["tracks"].items() if key in EXAMPLE_TRACK_IDS],
              "audio": {lang: [r for r in rows if r["id"].rsplit("-Q", 1)[0] in EXAMPLE_TRACK_IDS] for lang, rows in audio.items()}, "abc": abc,
              "scores": load("model_outputs/score_summary.json")["models"],
              "paper_results": {"abc": load("aggregate_results/abc_aggregate_results.json"), "audio": load("aggregate_results/audio_aggregate_results.json")},
              "paper": {"url": "https://arxiv.org/abs/2610.15773", "version": "v1", "abc_table": 1, "audio_table": 3}}
    waveforms = ROOT / "demo/waveforms.json"
    if waveforms.exists():
        bundle["waveforms"] = {k: v for k,v in json.loads(waveforms.read_text(encoding="utf-8")).items() if k in EXAMPLE_TRACK_IDS}
    bundle["abc_svgs"] = {key: [(ROOT / f"demo/scores/{key}-{i}.svg").read_text(encoding="utf-8") for i,_ in enumerate(abc["en"][selected.index(key)]["materials"])] for key in selected}
    path = ROOT / "demo/data.js"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("window.HMU_DATA = " + json.dumps(bundle, ensure_ascii=False).replace("<", "\\u003c") + ";\n", encoding="utf-8")
    print(f"Built {path.name}: {len(bundle['tracks'])} audio examples, 15 audio questions per language, {len(selected)} ABC examples, paper Tables 1/3")


if __name__ == "__main__":
    build()
