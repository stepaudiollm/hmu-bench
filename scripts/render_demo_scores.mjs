// Optional regeneration tool: requires linkedom, or an absolute HMU_DOM_MODULE.
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const { parseHTML } = await import(process.env.HMU_DOM_MODULE || 'linkedom');
const { window, document } = parseHTML('<html><body><div id="score"></div></body></html>');
globalThis.window = window;
globalThis.document = document;
const require = createRequire(import.meta.url);
const abcjs = require(path.join(root, 'demo/vendor/abcjs-basic-min.js'));
const questions = JSON.parse(fs.readFileSync(path.join(root, 'data/public/abc/data/en/with_answers.json'), 'utf8')).questions;
const ids = JSON.parse(fs.readFileSync(path.join(root, 'demo/examples.json'), 'utf8')).abc_question_ids;
const output = path.join(root, 'demo/scores');
fs.mkdirSync(output, { recursive: true });
for (const id of ids) {
  const item = questions.find(q => q.id === id);
  item.materials.forEach((material, index) => {
    let abc = material.abc;
    if (!/^X:/m.test(abc)) abc = 'X:1\n' + abc;
    if (!/^K:/m.test(abc)) {
      const lines = abc.split('\n');
      const firstMusic = lines.findIndex(line => line.trim() && !/^[A-Za-z]:|^%/.test(line));
      lines.splice(firstMusic < 0 ? lines.length : firstMusic, 0, 'K:none');
      abc = lines.join('\n');
    }
    const tunes = abcjs.renderAbc('score', abc, { responsive: 'resize', staffwidth: 850, add_classes: true,
      paddingtop: 18, paddingbottom: 18, foregroundColor: '#233b35', ariaLabel: 'Notation example ' + id });
    if (tunes[0]?.warnings?.length) throw new Error(id + ': ' + tunes[0].warnings.join('; '));
    const renderedSvg = document.getElementById('score').querySelector('svg');
    // abcjs responsive output positions the SVG absolutely inside its own wrapper.
    // We embed the SVG directly, so restore normal document flow.
    renderedSvg.removeAttribute('style');
    renderedSvg.setAttribute('width', '100%');
    const svg = renderedSvg.outerHTML;
    if (!svg.includes('<svg') || !svg.includes('<path')) throw new Error('Missing score rendering for ' + id);
    fs.writeFileSync(path.join(output, `${id}-${index}.svg`), svg + '\n');
    console.log(`Rendered ${id}: ${svg.length} SVG bytes, no parser warnings`);
  });
}
