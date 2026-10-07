// Run with the path to an installed KaTeX module (authoring only).
// The generated site needs no JavaScript or third-party requests for math.
const fs = require('node:fs');
const path = require('node:path');
const katex = require(process.argv[2] || 'katex');
const file = path.join(__dirname, '../site/index.html');
let page = fs.readFileSync(file, 'utf8');
let count = 0;
function render(tex, displayMode) {
  count++;
  const decoded = tex.replaceAll('&lt;', '<').replaceAll('&gt;', '>').replaceAll('&amp;', '&');
  return katex.renderToString(decoded, { displayMode, throwOnError: true, trust: false, output: 'htmlAndMathml' });
}
page = page.replace(/\\\[([\s\S]*?)\\\]/g, (_, tex) => render(tex, true));
page = page.replace(/\\\(([\s\S]*?)\\\)/g, (_, tex) => render(tex, false));
fs.writeFileSync(file, page);
console.log(`Typeset ${count} math expressions without errors.`);
