#!/usr/bin/env python3
"""Export a standalone static demo with verified, neutrally named audio."""
import argparse
import hashlib
import json
import shutil
import html
from pathlib import Path

from build_demo_data import ROOT, DATA, build


def inline_page(directory):
    """Keep a fully styled first view even in viewers that disable JavaScript."""
    page = (directory / "index.html").read_text(encoding="utf-8")
    data_text = (directory / "data.js").read_text(encoding="utf-8")
    bundle = json.loads(data_text.removeprefix("window.HMU_DATA = ").strip().removesuffix(";"))
    track = bundle["tracks"][0]
    def bars(peaks, center, scale, color):
        return ''.join(f'<rect x="{i*5+1}" y="{center-max(3,p*scale)/2:.2f}" width="3" height="{max(3,p*scale):.2f}" rx="1.5" fill="{color}"/>' for i,p in enumerate(peaks))
    peaks = bundle.get("waveforms", {}).get(track["id"], [])
    page = page.replace('aria-label="Amplitude envelope of track 01"></svg>', 'aria-label="Amplitude envelope of track 01">'+bars(peaks,60,98,'#def383')+'</svg>')
    page = page.replace('id="track-waveform" viewBox="0 0 700 90" aria-hidden="true"></svg>', 'id="track-waveform" viewBox="0 0 700 90" aria-hidden="true">'+bars(peaks,45,75,'#a7bd87')+'</svg>')
    options = ''.join(f'<option value="{t["id"]}">Track {t["index"]:02d} · {t["id"]}</option>' for t in bundle['tracks'])
    page = page.replace('<select id="track-select"></select>', '<select id="track-select">'+options+'</select>')
    questions = []
    for i,q in enumerate(bundle['audio']['en'][:5],1):
        questions.append(f'<article class="question"><div class="question-meta"><span>Q{i:02d}</span><span class="tag">{html.escape(q["scope"])}</span><span>{html.escape(q["domain"].replace("_"," "))}</span></div><h3>{html.escape(q["question"])}</h3><details><summary>Show reference answer</summary><p class="answer">{html.escape(q["reference_answer"])}</p></details></article>')
    page = page.replace('<div id="audio-questions" class="questions"></div>', '<div id="audio-questions" class="questions">'+''.join(questions)+'</div>')
    page = page.replace('<pre id="annotation-text"></pre>', '<pre id="annotation-text">'+html.escape(track['annotation'])+'</pre>')
    page = page.replace('<audio id="player"', '<audio src="./audio/assets/full/HMU-A000001.mp3" id="player"')
    scores = []
    for row in bundle['paper_results']['audio']['models']:
        values = [f'{row["overall"][lang]:.3f}' for lang in ('zh','en')]
        for group in row['configurations'].values(): values.extend([f'{group["score"]:.3f}',f'{group["fcr_percent"]:.2f}'])
        scores.append('<tr><td>'+html.escape(row['label'])+'</td>'+''.join('<td>'+v+'</td>' for v in values)+'</tr>')
    page = page.replace('<tbody id="score-rows"></tbody>', '<tbody id="score-rows">'+''.join(scores)+'</tbody>')
    header = '<tr><th rowspan="3">Model</th><th colspan="2">Overall score</th><th colspan="4">Global</th><th colspan="6">Local</th></tr><tr><th rowspan="2">ZH (460)</th><th rowspan="2">EN (460)</th>'+''.join('<th colspan="2">'+name+' (92)</th>' for name in ['Easy','Hard','Easy','Medium','Hard'])+'</tr><tr>'+('<th>Score</th><th>FCR %</th>'*5)+'</tr>'
    page = page.replace('<thead id="score-head"></thead>','<thead id="score-head">'+header+'</thead>')
    page = page.replace('<link rel="stylesheet" href="style.css">', '<style>\n'+(directory/'style.css').read_text(encoding='utf-8')+'\n</style>')
    scripts=[]
    for name in ('config.js','data.js','app.js'):
        page = page.replace(f'<script src="{name}" defer></script>', '')
        scripts.append('<script>\n'+(directory/name).read_text(encoding='utf-8').replace('</script', '<\\/script')+'\n</script>')
    page = page.replace('</body>', '\n'.join(scripts)+'\n</body>')
    (directory/'HMUBench-demo.html').write_text(page,encoding='utf-8')


def export(audio_dir, output, refresh=False):
    if output.exists() and not refresh:
        raise ValueError("Output already exists; choose a new directory")
    build()
    data_text = (ROOT / "demo/data.js").read_text(encoding="utf-8")
    selected = json.loads(data_text.removeprefix("window.HMU_DATA = ").strip().removesuffix(";"))["tracks"]
    selected_ids = {row['id'] for row in selected}
    tracks = {k:v for k,v in json.loads((DATA / "audio/assets/manifest.json").read_text(encoding="utf-8"))["tracks"].items() if k in selected_ids}
    for track in tracks.values():
        path = audio_dir / Path(track["assetPath"]).name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != track["sha256"]:
            raise ValueError(f"Audio integrity check failed: {path.name}")
    output.mkdir(parents=True,exist_ok=True)
    for name in ("index.html", "style.css", "app.js", "data.js"):
        shutil.copyfile(ROOT / "demo" / name, output / name)
    (output / "config.js").write_text('window.HMU_AUDIO_BASE = "./audio/";\n', encoding="utf-8")
    for old in (output / 'audio/assets/full').glob('HMU-A*.mp3'):
        if old.stem not in selected_ids: old.unlink()
    for track in tracks.values():
        destination = output / "audio" / track["assetPath"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        if not destination.exists() or hashlib.sha256(destination.read_bytes()).hexdigest() != track["sha256"]:
            shutil.copyfile(audio_dir / destination.name, destination)
    inline_page(output)
    print(f"Exported static demo and {len(tracks)} verified tracks to {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audio-dir", type=Path, default=ROOT / "demo/audio/assets/full")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--refresh", action="store_true", help="Refresh app files in an existing export; preserve matching MP3s")
    args = parser.parse_args()
    export(args.audio_dir, args.output, args.refresh)
