# HMU-Bench demo

A compact English research page with three audio examples, twelve ABC notation
examples rendered as sheet music, and complete paper Tables 1 and 3.

- Audio examples: `HMU-A000001`, `HMU-A000017`, and `HMU-A000062`, with five paired questions each.
- ABC examples: 12 tasks, two per musical domain, covering extraction, single-step, and multi-step inference. The set includes paper Table 2's `ABC-V2-0128`.
- The selected IDs are shared by the data and SVG builders through `demo/examples.json`.
- The three sample MP3s total 11.9 MB and are included in `demo/audio/assets/full/`.
- The complete benchmark remains in the release packages; the demo does not bundle all 92 tracks.

## Preview and hosting

From the repository root:

```bash
python3 -m http.server 8000
```

Open `http://localhost:8000/demo/`. All required media are included; no full
release download, external fonts, CDN scripts, or backend is required.

For a standalone static export:

```bash
python3 scripts/export_demo.py --output __preview__/site
```

Open the exported `HMUBench-demo.html` locally for the single-file UI preview.
CSS, SVG scores, benchmark data, and JavaScript are inline; its three MP3s stay
in the adjacent `audio/` folder. Host the exported directory on any static host.
Use `--refresh` to update a previously generated export. Nothing is committed,
pushed, deployed, or uploaded by these scripts.

## Examples and rendering

The player shows amplitude envelopes extracted from the real MP3s. Local
questions label their target passage explicitly; the complete recording remains
available. There is no separate “Jump to passage” button.

Sheet music is pre-rendered with abcjs 6.5.2 and included as responsive SVG.
Original ABC text is available in a collapsed source panel. For the example
whose key field is intentionally hidden, rendering adds `K:none` internally
and does not infer or expose the reference key; original benchmark text is
unchanged. Both languages share the same score.

To regenerate SVGs, install the optional development dependency `linkedom`
and run `node scripts/render_demo_scores.mjs` (or supply an absolute module
path in `HMU_DOM_MODULE`). The pinned abcjs renderer and its MIT license are in
`demo/vendor/`; they are only needed to regenerate SVGs, not to load the page.

## Data and result sources

Regenerate the example bundle with `python3 scripts/build_demo_data.py`.
`waveforms.json` retains the 92-track source envelopes for regeneration, but
only the three example envelopes enter the page bundle and static export.
Paper Table 1 comes from `data/public/aggregate_results/abc_aggregate_results.json`;
Table 3 comes from `audio_aggregate_results.json`, which is reproducible with
`python3 scripts/build_audio_results.py`. Table headings, counts, precision,
model order, and reference-system grouping follow arXiv:2610.15773v1.

The compact raw-score summary is retained as originally released. It is not
used to replace the paper's Table 1 aggregates. Score cells reproduce paper
values rather than silently changing raw per-question scores.

Release buttons point to the benchmark's GitHub data release.

## GitHub Pages automatic deployment

The workflow in `.github/workflows/pages.yml` builds and deploys the demo on
changes to the page or public data on `main`; it also supports manual runs.
It publishes only the small example site, not the full release packages.
In the repository's **Settings → Pages**, select **GitHub Actions** as the
publishing source once. After the first successful approved deployment, the
site URL is https://stepaudiollm.github.io/hmu-bench/. The workflow is prepared
locally; it has not been committed or run yet.
