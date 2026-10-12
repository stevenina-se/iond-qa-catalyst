// Build de los documentos SDLC IOND: Markdown -> HTML (marked + mermaid vía CDN) -> PDF (Chrome/Edge headless).
// Uso:  node docs/sdlc-iond/_build/build.mjs [filtro]
//   filtro opcional: prefijo del archivo (p. ej. "02") para construir solo ese documento.
// Requisitos: Node >= 18, Chrome o Edge instalados, acceso a cdn.jsdelivr.net.
import { readFileSync, writeFileSync, mkdirSync, readdirSync, existsSync, statSync } from "node:fs";
import { dirname, join, resolve, basename } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { execFileSync } from "node:child_process";

const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(here, "..");
const srcDir = join(root, "src");
const htmlDir = join(here, "html");
const pdfDir = join(root, "pdf");
const vendorDir = join(here, "vendor");
mkdirSync(htmlDir, { recursive: true });
mkdirSync(pdfDir, { recursive: true });
mkdirSync(vendorDir, { recursive: true });

// Librerías del navegador: se descargan una vez a _build/vendor/ para no depender de la red al imprimir.
const VENDOR = {
  "marked.min.js": "https://cdn.jsdelivr.net/npm/marked@12.0.2/marked.min.js",
  "mermaid.min.js": "https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js",
};
for (const [file, url] of Object.entries(VENDOR)) {
  const target = join(vendorDir, file);
  if (!existsSync(target)) {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`No se pudo descargar ${url}: ${res.status}`);
    writeFileSync(target, Buffer.from(await res.arrayBuffer()));
    console.log("Descargado:", target);
  }
}

const BROWSERS = [
  process.env.CHROME_PATH,
  "C:/Program Files/Google/Chrome/Application/chrome.exe",
  "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
  "/usr/bin/google-chrome",
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
].filter(Boolean);
const browser = BROWSERS.find((p) => existsSync(p));
if (!browser) throw new Error("No se encontró Chrome/Edge. Define CHROME_PATH.");

// <!-- @include ruta/relativa.md#seccion -->  ->  contenido entre <!-- BEGIN:seccion --> y <!-- END:seccion -->
function resolveIncludes(md, fromFile) {
  return md.replace(/<!--\s*@include\s+([^#\s]+)(?:#([\w-]+))?\s*-->/g, (_, rel, section) => {
    const target = resolve(dirname(fromFile), rel);
    let text = readFileSync(target, "utf8");
    if (section) {
      const re = new RegExp(`<!--\\s*BEGIN:${section}\\s*-->([\\s\\S]*?)<!--\\s*END:${section}\\s*-->`);
      const m = text.match(re);
      if (!m) throw new Error(`Sección "${section}" no encontrada en ${target}`);
      text = m[1];
    }
    return resolveIncludes(text, target);
  });
}

const css = readFileSync(join(here, "print.css"), "utf8");

function toHtml(md, title) {
  const payload = JSON.stringify(md).replace(/<\/script/gi, "<\\/script");
  return `<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${title}</title>
<style>${css}</style>
<script src="../vendor/marked.min.js"></script>
<script src="../vendor/mermaid.min.js"></script>
</head><body>
<main id="content"></main>
<script>
(async () => {
  const md = ${payload};
  const main = document.getElementById('content');
  // Portada: todo lo anterior a la primera línea "---" (saltos de línea respetados)
  const m = md.match(/^---\\s*$/m);
  const coverMd = m ? md.slice(0, m.index) : '';
  const bodyMd = m ? md.slice(m.index + m[0].length) : md;
  if (coverMd.trim()) {
    const cover = document.createElement('section');
    cover.className = 'cover';
    cover.innerHTML = marked.parse(coverMd, { gfm: true, breaks: true });
    main.appendChild(cover);
  }
  const body = document.createElement('div');
  body.innerHTML = marked.parse(bodyMd, { gfm: true, breaks: false });
  main.appendChild(body);
  // Bloques mermaid
  main.querySelectorAll('pre > code.language-mermaid').forEach((code) => {
    const div = document.createElement('div');
    div.className = 'mermaid';
    div.textContent = code.textContent;
    code.parentElement.replaceWith(div);
  });
  // Tablas anchas -> clase para letra menor
  main.querySelectorAll('table').forEach((t) => {
    const cols = t.querySelectorAll('tr:first-child > *').length;
    if (cols >= 6) t.classList.add('wide');
    const head = [...t.querySelectorAll('tr:first-child > *')].map((c) => c.textContent.trim());
    if (head[0] === '#' && head[1] === 'Tarjeta (tipo)') t.classList.add('cards');
  });
  mermaid.initialize({ startOnLoad: false, theme: 'neutral', securityLevel: 'loose',
    flowchart: { htmlLabels: true, useMaxWidth: true, curve: 'basis', nodeSpacing: 30, rankSpacing: 36, padding: 8 },
    gantt: { useMaxWidth: true }, sequence: { useMaxWidth: true } });
  try { await mermaid.run({ querySelector: '.mermaid' }); }
  catch (e) { document.body.insertAdjacentHTML('afterbegin', '<pre class="build-error">MERMAID ERROR: ' + e + '</pre>'); }
  // Ajuste a la hoja A4: ancho útil 182 mm (~688 px) y alto máximo ~230 mm (~870 px).
  const MAX_W = 688, MAX_H = 870;
  main.querySelectorAll('.mermaid svg').forEach((svg) => {
    const vb = svg.viewBox && svg.viewBox.baseVal;
    if (!vb || !vb.width || !vb.height) return;
    const scale = Math.min(1, MAX_W / vb.width, MAX_H / vb.height);
    const w = Math.round(vb.width * scale), h = Math.round(vb.height * scale);
    svg.removeAttribute('style');
    svg.setAttribute('width', w); svg.setAttribute('height', h);
    svg.style.width = w + 'px'; svg.style.height = h + 'px'; svg.style.maxWidth = '100%';
    svg.parentElement.setAttribute('data-fit-scale', scale.toFixed(2));
    svg.parentElement.setAttribute('data-natural', Math.round(vb.width) + 'x' + Math.round(vb.height));
  });
  document.body.classList.add('rendered');
})();
</script>
</body></html>`;
}

const filter = process.argv[2] || "";
const files = readdirSync(srcDir).filter((f) => f.endsWith(".md") && !f.startsWith("_") && f.startsWith(filter)).sort();
for (const f of files) {
  const srcPath = join(srcDir, f);
  const md = resolveIncludes(readFileSync(srcPath, "utf8"), srcPath);
  const firstH1 = (md.match(/^#\s+(.+)$/m) || [, basename(f, ".md")])[1].trim();
  const html = toHtml(md, firstH1);
  const htmlPath = join(htmlDir, f.replace(/\.md$/, ".html"));
  writeFileSync(htmlPath, html, "utf8");
  const pdfPath = join(pdfDir, f.replace(/\.md$/, ".pdf"));
  // Reintenta si el PDF sale casi vacío (render incompleto).
  for (let attempt = 1; attempt <= 3; attempt++) {
    execFileSync(browser, [
      "--headless=new", "--disable-gpu", "--no-sandbox", "--no-pdf-header-footer",
      "--run-all-compositor-stages-before-draw", "--virtual-time-budget=30000",
      `--print-to-pdf=${pdfPath}`, pathToFileURL(htmlPath).href,
    ], { stdio: "pipe" });
    if (statSync(pdfPath).size > 80_000) break;
    console.warn(`PDF sospechosamente pequeño (intento ${attempt}): ${pdfPath}`);
  }
  console.log("PDF:", pdfPath);
  // Reporte de escala de diagramas (escala < 0.6 = texto demasiado pequeño: conviene rediseñar el diagrama).
  if (process.env.CHECK_DIAGRAMS) {
    const dom = execFileSync(browser, ["--headless=new", "--disable-gpu", "--no-sandbox",
      "--virtual-time-budget=30000", "--dump-dom", pathToFileURL(htmlPath).href], { encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] });
    const rows = [...dom.matchAll(/data-fit-scale="([\d.]+)" data-natural="([\dx]+)"/g)];
    rows.forEach(([, s, n], i) => console.log(`   diagrama ${i + 1}: escala ${s} (natural ${n})${Number(s) < 0.6 ? "  <-- pequeño" : ""}`));
  }
}
