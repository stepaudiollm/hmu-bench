"use strict";
(() => {
  const data = window.HMU_DATA;
  const $ = id => document.getElementById(id);
  let language = "en", mode = "audio", scoreMode = "audio";
  const player = $("player");
  document.body.classList.add("js");
  const node = (tag, text, className) => {
    const el = document.createElement(tag);
    if (text != null) el.textContent = text;
    if (className) el.className = className;
    return el;
  };
  const clock = seconds => `${Math.floor(seconds / 60)}:${String(Math.floor(seconds % 60)).padStart(2, "0")}`;
  function drawWaveform(id, track, hero = false) {
    const svg = $(id);
    svg.replaceChildren();
    const peaks = data.waveforms?.[track.id] || [];
    const center = hero ? 60 : 45;
    peaks.forEach((amplitude, index) => {
      const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
      const height = Math.max(3, amplitude * (hero ? 98 : 75));
      for (const [key, value] of Object.entries({x: index * 5 + 1, y: center - height/2, width: 3, height, rx: 1.5,
        fill: hero ? "#def383" : "#a7bd87"})) rect.setAttribute(key, String(value));
      svg.append(rect);
    });
  }
  function updatePlayer() {
    const track = data.tracks.find(t => t.id === $("track-select").value);
    const duration = Number.isFinite(player.duration) ? player.duration : track.duration;
    const current = player.currentTime || 0;
    $("current-time").textContent = clock(current);
    $("seek-track").value = String(Math.round(current / duration * 1000));
    $("play-icon").textContent = player.paused ? "▶" : "Ⅱ";
    $("play-toggle").setAttribute("aria-label", player.paused ? "Play track" : "Pause track");
    [...$("track-waveform").children].forEach((bar, i, bars) => bar.setAttribute("fill", i / bars.length < current / duration ? "#244b3b" : "#a7bd87"));
  }
  $("play-toggle").addEventListener("click", async () => {
    try { if (player.paused) await player.play(); else player.pause(); }
    catch (_) { $("audio-status").textContent = "Audio could not be loaded. The release contains the complete recordings."; }
    updatePlayer();
  });
  $("seek-track").addEventListener("input", event => {
    const track = data.tracks.find(t => t.id === $("track-select").value);
    const duration = Number.isFinite(player.duration) ? player.duration : track.duration;
    player.currentTime = Number(event.target.value) / 1000 * duration;
    updatePlayer();
  });
  for (const event of ["timeupdate", "play", "pause", "ended", "loadedmetadata"]) player.addEventListener(event, updatePlayer);
  function selectButtons(ids, active) {
    for (const id of ids) {
      const selected = id === active;
      $(id).classList.toggle("selected", selected);
      $(id).setAttribute("aria-pressed", String(selected));
    }
  }
  function makeQuestion(item, index, audio = false) {
    const article = node("article", null, "question");
    article.lang = language === "zh" ? "zh-CN" : "en";
    const metadata = node("div", null, "question-meta");
    metadata.append(node("span", `Q${String(index + 1).padStart(2, "0")}`));
    if (item.scope) metadata.append(node("span", item.scope === "global" ? "Global" : "Local", "tag"));
    const domain = item.domain || item.subtype || item.category;
    if (domain) metadata.append(node("span", domain.replaceAll("_", " ")));
    article.append(metadata, node("h3", item.question));
    if (audio && item.scope === "local") {
      const text = "Target passage: " + [item.section, item.time_range, item.bar_range && `Bars ${item.bar_range}`].filter(Boolean).join(" · ");
      const locator = node("p", text, "locator");
      article.append(locator);
    }
    const details = node("details");
    details.append(node("summary", "Show reference answer"), node("p", item.reference_answer, "answer"));
    article.append(details);
    return article;
  }
  function renderAudioQuestions() {
    const track = data.tracks.find(t => t.id === $("track-select").value);
    $("audio-questions").replaceChildren(...data.audio[language]
      .filter(q => q.id.startsWith(`${track.id}-Q`)).map((q, i) => makeQuestion(q, i, true)));
    $("annotation-text").textContent = track.annotation;
  }
  function changeTrack() {
    player.pause();
    const track = data.tracks.find(t => t.id === $("track-select").value);
    const base = window.HMU_AUDIO_BASE || "./audio/";
    player.src = new URL(track.audio_path, new URL(base, window.location.href)).href;
    player.load();
    $("duration").textContent = `${clock(track.duration)} · MP3`;
    $("total-time").textContent = clock(track.duration);
    drawWaveform("track-waveform", track);
    updatePlayer();
    $("audio-status").textContent = "Every question uses the complete track. Local questions identify a specific passage.";
    renderAudioQuestions();
  }
  player.addEventListener("error", () => {
    $("audio-status").textContent = "Audio could not be loaded. The release contains the complete recordings.";
  });
  function renderABC() {
    const index = Number($("abc-select").value || 0);
    const item = data.abc[language][index];
    const content = $("abc-question");
    content.replaceChildren();
    (item.materials || []).forEach((material, materialIndex) => {
      content.append(node("p", material.label || "ABC excerpt", "material-title"));
      const sheet = node("div", null, "sheet-music");
      sheet.setAttribute("aria-label", "Sheet music for " + item.id);
      content.append(sheet);
      if (item.display_key_withheld && !/^\s*K:/m.test(material.abc || ""))
        content.append(node("p", "Key signature withheld", "score-note"));
      try {
        if (!data.abc_svgs?.[item.id]?.[materialIndex]) throw new Error("Score unavailable");
        sheet.innerHTML = data.abc_svgs[item.id][materialIndex];
      } catch (_) { sheet.append(node("p", "View the original notation below.", "score-note")); }
      const source = node("details", null, "abc-source");
      source.append(node("summary", "View ABC source"), node("pre", material.abc || ""));
      content.append(source);
    });
    const requirements = { e: "Extraction", "1": "Single-step inference", n: "Multi-step inference" };
    content.append(node("p", requirements[item.reasoning_level] || item.reasoning_level, "requirement-label"));
    content.append(makeQuestion(item, index));
  }
  function setLanguage(value) {
    language = value;
    selectButtons(["lang-en", "lang-zh"], `lang-${value}`);
    renderAudioQuestions();
    renderABC();
  }
  function setMode(value) {
    mode = value;
    selectButtons(["mode-audio", "mode-abc"], `mode-${value}`);
    $("audio-panel").hidden = value !== "audio";
    $("abc-panel").hidden = value !== "abc";
    if (mode === "abc") player.pause();
  }
  function renderScores() {
    const result = data.paper_results[scoreMode];
    const head = $("score-head");
    head.replaceChildren();
    const group = node("tr");
    const modelHead = node("th", "Model"); modelHead.setAttribute("rowspan", "3"); modelHead.setAttribute("scope", "col"); group.append(modelHead);
    const groups = scoreMode === "abc" ? [["Overall score",2],["Musical domain",6],["Solution requirement",3]] : [["Overall score",2],["Global",4],["Local",6]];
    groups.forEach(([label, span]) => {const th = node("th",label);th.setAttribute("colspan",String(span));th.setAttribute("scope","colgroup");group.append(th);});
    head.append(group);
    const second = node("tr"), third = node("tr");
    const overallLabels = ["ZH (1,029)","EN (1,029)"];
    if(scoreMode === "audio") { overallLabels[0]="ZH (460)";overallLabels[1]="EN (460)"; }
    overallLabels.forEach(label=>{const th=node("th",label);th.setAttribute("rowspan",scoreMode === "abc" ? "1" : "2");th.setAttribute("scope","col");second.append(th);});
    if (scoreMode === "abc") {
      const labels=["Global (49)","Pitch (268)","Harmony (392)","Rhythm (208)","Form (25)","Symbolic (87)","Extraction (335)","Single (441)","Multi (253)"];
      labels.forEach(label=>{const th=node("th",label);th.setAttribute("scope","col");second.append(th);});
    } else {
      ["Easy (92)","Hard (92)","Easy (92)","Medium (92)","Hard (92)"].forEach(label=>{const th=node("th",label);th.setAttribute("colspan","2");th.setAttribute("scope","colgroup");second.append(th);third.append(node("th","Score"),node("th","FCR %"));});
    }
    head.append(second); if(scoreMode === "audio")head.append(third);
    if(scoreMode === "abc") modelHead.setAttribute("rowspan","2");
    const columns = row => scoreMode === "abc"
      ? [row.overall.zh,row.overall.en,...Object.values(row.domains),...Object.values(row.solution_requirements)]
      : [row.overall.zh,row.overall.en,...Object.values(row.configurations).flatMap(r=>[r.score,r.fcr_percent])];
    const ranked = result.models.filter(r => scoreMode !== "abc" || r.group === "omni");
    const maxima = columns(ranked[0]).map((_,i)=>Math.max(...ranked.map(r=>columns(r)[i])));
    let separated = false;
    const rows = [];
    result.models.forEach(row=>{
      if(scoreMode === "abc" && row.group !== "omni" && !separated) {
        const tr=node("tr",null,"reference-divider"),td=node("td","ABC-only reference systems");td.setAttribute("colspan","12");tr.append(td);rows.push(tr);separated=true;
      }
      const tr=node("tr"); tr.append(node("td",row.label.replace("Seed2.0 Lite","Seed Lite").replace("StepAudio 3 Realtime","StepAudio 3").replace("Qwen 3.5 Omni Plus","Qwen 3.5 Omni").replace("Qwen 3 Omni Flash","Qwen 3 Omni").replace("DeepSeek V4.1 Flash","DeepSeek V4.1")));
      columns(row).forEach((value,i)=>{const digits=i<2 ? 3 : scoreMode === "abc" ? 2 : i%2 === 0 ? 3 : 2;const td=node("td",value.toFixed(digits));if((scoreMode !== "abc" || row.group === "omni")&&value===maxima[i])td.classList.add("best-score");tr.append(td);});rows.push(tr);
    });
    $("score-rows").replaceChildren(...rows);
    $("table-note").textContent = scoreMode === "abc"
      ? "Paper Table 1. Domain and solution-requirement means aggregate both languages. Counts are question pairs. Bold marks the best omni model; ABC-only references are separate."
      : "Paper Table 3. Each configuration has 92 question pairs (184 responses across both languages). FCR is the percentage graded 4. Bold marks the best score per column.";
  }
  $("track-select").replaceChildren();
  $("abc-select").replaceChildren();
  for (const track of data.tracks) {
    const option = node("option", `Track ${String(track.index).padStart(2, "0")} · ${track.id}`);
    option.value = track.id;
    $("track-select").append(option);
  }
  const abcGroups = new Map();
  data.abc.en.forEach((item, index) => {
    if (!abcGroups.has(item.category)) {
      const group = node("optgroup");
      group.setAttribute("label", item.category);
      abcGroups.set(item.category, group);
      $("abc-select").append(group);
    }
    const option = node("option", `${String(index + 1).padStart(2, "0")} · ${item.subtype}`);
    option.value = String(index);
    abcGroups.get(item.category).append(option);
  });
  $("track-select").addEventListener("change", changeTrack);
  $("abc-select").addEventListener("change", renderABC);
  for (const lang of ["en", "zh"]) $("lang-" + lang).addEventListener("click", () => setLanguage(lang));
  for (const value of ["audio", "abc"]) {
    $("mode-" + value).addEventListener("click", () => setMode(value));
    $("scores-" + value).addEventListener("click", () => {
      scoreMode = value;
      selectButtons(["scores-audio", "scores-abc"], `scores-${value}`);
      renderScores();
    });
  }
  changeTrack();
  drawWaveform("hero-waveform", data.tracks[0], true);
  renderABC();
  renderScores();
})();
