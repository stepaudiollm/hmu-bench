# Public model outputs and judge scores

This directory contains complete model answers aligned to the final question IDs and compact judge scores. It does not contain judge rationales, missing/wrong explanations, private workflow fields, or source-audit metadata.

- `responses/`: one JSONL file per model and language.
- `scores/`: one JSONL file per model and language with `id`, `score`, and `label`.
- `score_summary.json`: aggregate score counts and means.
