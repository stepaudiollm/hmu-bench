# Full-track audio annotations

`tracks.jsonl` contains one UTF-8 JSON object per track: 92 records in total.
Each record provides the original ABC annotation matched to the complete MP3.
The annotation text is preserved exactly from the supplied source JSONL files.

| Field | Meaning |
| --- | --- |
| `schema_version` | Public annotation schema, currently `1.0`. |
| `track_id` | Neutral stable ID, such as `HMU-A000001`. |
| `track_index` | Global index from 1 to 92; not a genre label. |
| `audio_path` | MP3 path relative to the package's `audio/` directory. |
| `audio_sha256` | SHA-256 of the MP3 bytes. |
| `annotation_format` | `abc`. |
| `annotation` | Original ABC text, with newlines encoded inside the JSON string. |
| `annotation_sha256` | SHA-256 of the decoded annotation's UTF-8 bytes. |

Join questions to annotations using the track portion of the question ID:

```python
import json

with open("audio/annotations/tracks.jsonl", encoding="utf-8") as f:
    annotations = {r["track_id"]: r for r in map(json.loads, f)}

track_id = "HMU-A000001-Q01".rsplit("-Q", 1)[0]
abc = annotations[track_id]["annotation"]
```

Annotations are reference material for scoring and analysis. Keep them out of
the context supplied to audio-only answering models. Source collection names,
sample identifiers, editor package identifiers, and draft metadata are omitted
from this normalized public schema, together with review statuses and editor
validation messages. This does not change the annotation text.
