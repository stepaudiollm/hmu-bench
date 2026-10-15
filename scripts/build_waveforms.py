#!/usr/bin/env python3
"""Extract real MP3 amplitude envelopes for the demo (requires ffmpeg)."""
import argparse
import array
import concurrent.futures
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def extract(path):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", "1600", "-f", "f32le", "-"])
    samples = array.array("f")
    samples.frombytes(raw)
    count = 140
    peaks = [max((abs(v) for v in samples[len(samples)*i//count:len(samples)*(i+1)//count]), default=0) for i in range(count)]
    scale = max(peaks, default=1) or 1
    return path.stem, [round(p/scale, 3) for p in peaks]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audio_dir", type=Path)
    args = parser.parse_args()
    paths = sorted(args.audio_dir.glob("HMU-A*.mp3"))
    if len(paths) != 92:
        raise ValueError("Expected 92 neutrally named MP3s")
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        waves = dict(pool.map(extract, paths))
    (ROOT / "demo/waveforms.json").write_text(json.dumps(waves, separators=(",", ":")) + "\n", encoding="utf-8")
    print("Extracted amplitude envelopes from 92 real tracks")
