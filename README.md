# HMU-Bench: Hierarchical Music Understanding Benchmark for Omni Models


[Paper](https://arxiv.org/abs/2610.15773) · [Data release](https://github.com/stepaudiollm/hmu-bench/releases/tag/v2026.10.08-data-final) · [Demo](https://stepaudiollm.github.io/hmu-bench/)

HMU-Bench evaluates music understanding through **ABC notation** and **complete-track audio**, with paired Chinese–English questions and open-ended reference answers. Each question identifies the evidence and operations a correct answer requires.

| Component | Question pairs | Evidence | Hierarchy |
| --- | ---: | --- | --- |
| ABC Q&A | 1,029 | 1,166 notation excerpts from 997 songs | Extraction, single-step inference, multi-step inference |
| Audio Q&A | 460 | 92 complete recordings | Global/easy, global/hard, local/easy, local/medium, local/hard |

ABC covers six musical domains and 38 task types. Audio has one question pair per track in each of the five configurations. All music is Suno-generated; references are grounded in notation or human audio annotations. The two components use different songs and tasks, so they are reported separately.

## News

- **2026-10-11:** [The paper is available on arXiv](https://arxiv.org/abs/2610.15773).
- **2026-10-14 update:** neutral audio names and IDs, matched 92-track ABC annotations in JSONL, refreshed documentation and checksums, and a compact example demo.

## Demo

[**Explore the interactive demo →**](https://stepaudiollm.github.io/hmu-bench/)

## Results

Complete results from paper Tables 1 and 3. Scores are on a 0–4 scale. Overall ZH/EN scores are reported separately; subgroup means aggregate both languages. Counts denote question pairs.

### ABC Q&A — Table 1

Bold marks the best omni model in each column. The two ABC-only reference systems are reported separately.

| Model | ZH<br>(1,029) | EN<br>(1,029) | Global<br>(49) | Pitch<br>(268) | Harmony<br>(392) | Rhythm<br>(208) | Form<br>(25) | Symbolic<br>(87) | Extraction<br>(335) | Single<br>(441) | Multi<br>(253) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Gemini 3.7 Flash | **3.840** | **3.864** | **3.97** | **3.69** | **3.91** | **3.95** | **3.76** | **3.83** | **3.81** | **3.86** | **3.89** |
| Seed Lite | 3.516 | 3.521 | 3.79 | 3.34 | 3.52 | 3.72 | 3.40 | 3.47 | 3.56 | 3.51 | 3.48 |
| StepAudio 3 | 3.306 | 3.408 | 3.64 | 3.12 | 3.38 | 3.57 | 3.38 | 3.32 | 3.38 | 3.35 | 3.35 |
| Gemini 3.1 Pro | 3.274 | 3.236 | 3.73 | 2.95 | 3.45 | 3.24 | 3.16 | 3.12 | 3.11 | 3.26 | 3.44 |
| Gemini 2.5 Pro | 2.912 | 2.979 | 3.45 | 2.54 | 3.04 | 3.16 | 3.10 | 2.93 | 2.78 | 2.96 | 3.14 |
| Qwen 3.5 Omni | 2.740 | 2.621 | 3.33 | 2.40 | 2.72 | 2.81 | 2.94 | 2.60 | 2.50 | 2.77 | 2.77 |
| Qwen 3 Omni | 1.914 | 1.898 | 2.47 | 1.72 | 1.84 | 2.18 | 2.46 | 1.64 | 1.73 | 2.00 | 1.98 |
| **ABC-only reference systems** | | | | | | | | | | | |
| GPT-6 Astra | 3.964 | 3.945 | 3.99 | 3.93 | 3.96 | 3.98 | 3.84 | 3.93 | 3.95 | 3.95 | 3.96 |
| DeepSeek V4.1 | 2.982 | 3.033 | 3.58 | 2.60 | 3.19 | 3.07 | 3.00 | 2.95 | 2.87 | 3.04 | 3.12 |

Global: global information; Pitch: pitch and melody; Harmony: tonality and harmony; Form: form and temporal structure; Symbolic: verifiable symbolic tasks. Single/Multi mean single-step/multi-step inference. [Machine-readable Table 1](data/public/aggregate_results/abc_aggregate_results.json).

### Audio Q&A — Table 3

Each scope/difficulty configuration contains 92 question pairs (184 responses per model across both languages). FCR is the percentage of responses graded 4. Bold marks the best result per column.

| Model | ZH | EN | Global easy<br>Score | Global easy<br>FCR % | Global hard<br>Score | Global hard<br>FCR % | Local easy<br>Score | Local easy<br>FCR % | Local medium<br>Score | Local medium<br>FCR % | Local hard<br>Score | Local hard<br>FCR % |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen 3.5 Omni | **1.330** | **1.333** | **2.522** | **48.37** | **1.212** | **9.24** | **1.815** | **23.37** | 0.848 | 5.98 | **0.261** | 0.00 |
| Gemini 3.1 Pro | 1.176 | 1.122 | 2.250 | 44.02 | 0.924 | 4.35 | 1.554 | 22.28 | 0.891 | 10.33 | 0.125 | **0.54** |
| Gemini 3.7 Flash | 1.159 | 1.028 | 1.859 | 35.87 | 0.913 | 4.89 | 1.543 | 22.83 | **1.000** | **10.87** | 0.152 | **0.54** |
| Seed Lite | 1.093 | 0.941 | 1.891 | 35.33 | 0.815 | 2.72 | 1.511 | 20.11 | 0.766 | 7.61 | 0.103 | 0.00 |
| Qwen 3 Omni | 0.965 | 0.913 | 1.630 | 26.63 | 0.929 | 3.80 | 1.429 | 20.11 | 0.636 | 4.35 | 0.071 | 0.00 |
| StepAudio 3 | 0.946 | 0.863 | 1.647 | 27.72 | 0.799 | 2.17 | 1.375 | 19.57 | 0.641 | 7.07 | 0.060 | 0.00 |
| Gemini 2.5 Pro | 0.917 | 0.898 | 1.755 | 30.43 | 0.826 | 2.17 | 1.217 | 14.67 | 0.674 | 3.80 | 0.065 | 0.00 |

[Machine-readable Table 3](data/public/aggregate_results/audio_aggregate_results.json). The configuration means and FCR are reproducible from the released per-question scores with `python3 scripts/build_audio_results.py`.

## Data and usage

```text
data/public/
  abc/data/{zh,en}/                 questions and reference answers
  audio/data/{zh,en}/               questions and reference answers
  audio/annotations/tracks.jsonl    92 full-track ABC annotations
  audio/assets/manifest.json        question/audio mapping and hashes
  aggregate_results/               paper-aligned aggregate tables
  model_outputs/                   model responses and compact judge scores
  prompts/                         answering and evaluator prompts
demo/                              small static example page
scripts/                           validation and packaging helpers
```

MP3 payloads for the full dataset are in the release assets, rather than ordinary repository history.

### Model inputs and scoring

- Use `abc/data/{zh,en}/questions.json` or `audio/data/{zh,en}/questions.json` for inference.
- Join outputs to the corresponding `with_answers.json` by `id`; reference answers and annotation evidence enter the grader, not the answering model.
- For audio, send one question per request and provide the **complete track**, including for local questions. `time_range`, `section`, and `bar_range` locate the target passage.
- Resolve `audio_path` relative to the package's `audio/` directory.
- The minimal package uses `abc/{zh,en}/questions.json`, `audio/{zh,en}/questions.json`, and simplified `answers.json` files; see its included README.

### Neutral audio names and annotations

Audio IDs are `HMU-A000001` through `HMU-A000092`; question IDs append `-Q01` through `-Q05`. Files are named `assets/full/HMU-A000001.mp3`. Names do not encode genre. The naming update preserves MP3 bytes, question and answer text, model responses, and scores.

`audio/annotations/tracks.jsonl` has one matched ABC annotation per recording. Join by `track_id`; its audio and annotation hashes support integrity checks. Reviewer/editor workflow fields are omitted. See the [annotation schema](data/public/audio/annotations/README.md).

## Release packages

- `HMUBench-2026-10-08-final-public.zip`: full public data, 92 MP3s, annotations, reference answers, prompts, model outputs, paper-aligned aggregates, and checksums.
- `HMUBench-2026-10-08-minimal.zip`: ready-to-use questions, simplified answers, 92 MP3s, annotations, prompts, and checksums.
- `HMUBench_audio_annotations_20261014.zip`: all 92 complete MP3 tracks, their matched annotation JSONL, schema, and checksums.

To reproduce the release packages from an extracted original minimal package:

```bash
python3 scripts/build_release_packages.py \
  --legacy-minimal /path/to/HMUBench-2026-10-08-minimal \
  --output release-review
```

The full package uses repository public data plus verified MP3s from the original minimal release. All MP3s are checked against the published SHA-256 values before packaging. Validate repository data with:

```bash
python3 scripts/validate_repo.py
```

## Evaluation notes

The paper uses Qwen 3.5 Flash for reference-based judging and reports reviewer audits. It also documents limitations, including 82 audio references awaiting further listening review, unmeasured human–grader agreement, and the need for event-level checks and consistent logged prompts for affected symbolic outputs. Removing workflow metadata or passing checksums does not constitute a new musical-content review.

## Citation and use

```bibtex
@article{dai2026hmubench,
  title={HMU-Bench: Hierarchical Music Understanding Benchmark for Omni Models},
  author={Dai, Zheqi and Wang, Boyang and Wu, Zhiyue and Xu, Yiyang and Shi, Xinming and Yuan, Ruibin and Yang, Xuerui and Yan, Chao and Kong, Qiuqiang},
  journal={arXiv preprint arXiv:2610.15773},
  year={2026}
}
```

See [CITATION.cff](CITATION.cff). The paper describes evaluation-only use subject to applicable Suno terms. The repository's license placeholder still needs approved data, code, and audio notices; see [LICENSE_PLACEHOLDER.md](LICENSE_PLACEHOLDER.md).
