# HMU-Bench audio and annotations

This package contains all **92 complete MP3 recordings** and their matched
full-track ABC annotations, using neutral track IDs.

```text
audio/
  assets/full/HMU-A000001.mp3     complete recordings, up to HMU-A000092
  assets/manifest.json           track paths, durations, sizes, and hashes
  annotations/tracks.jsonl       one ABC annotation per recording
  annotations/README.md          JSONL field definitions
MANIFEST.json                   package overview
SHA256SUMS                      checksums of all other files
```

Each JSONL record's `track_id` matches its MP3 filename without the extension.
Resolve `audio_path` relative to the package's `audio/` directory:

```python
import json
from pathlib import Path

with open("audio/annotations/tracks.jsonl", encoding="utf-8") as f:
    for record in map(json.loads, f):
        audio_file = Path("audio") / record["audio_path"]
        abc = record["annotation"]
```

The MP3 bytes and ABC annotation text are preserved from the source release.
Reviewer/editor workflow metadata is omitted. The full and minimal benchmark
packages separately provide questions and reference answers; this package is
for working directly with audio and annotations.

On macOS, verify package integrity from this directory:

```bash
shasum -a 256 -c SHA256SUMS
```

Paper: https://arxiv.org/abs/2610.15773. The benchmark is intended for
evaluation use subject to the applicable data and audio terms.
