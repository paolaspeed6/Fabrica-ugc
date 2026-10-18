// Renderiza uma camada GSAP quadro a quadro (PNG transparente) e manda para o ffmpeg como .mov com alfa.
// Uso: node render.js <pagina.html> <dados.json> <saida.mov> [fps]
const { chromium } = require("/opt/node-tools/node_modules/playwright");
const { spawn } = require("child_process");
const fs = require("fs"), path = require("path");
(async () => {
  const [pagina, dados, saida, fpsArg] = process.argv.slice(2);
  const fps = Number(fpsArg || 30), D = JSON.parse(fs.readFileSync(dados, "utf8"));
  const nq = Math.round(D.fim * fps);
  const nav = await chromium.launch({ args: ["--disable-dev-shm-usage", "--disable-gpu"] });
  const pg = await nav.newPage({ viewport: { width: 1080, height: 1920 } });
  pg.on("crash", () => { console.error("navegador caiu"); process.exit(1); });
  pg.on("pageerror", e => console.error("erro na página:", e.message));
  await pg.addInitScript(d => { window.DADOS = d; }, D);
  // copia página, GSAP e fonte para um disco local: ler do disco compartilhado travava o Chromium
  const local = fs.mkdtempSync(path.join(require("os").tmpdir(), "camada-"));
  const dir = path.dirname(path.resolve(pagina));
  fs.mkdirSync(path.join(local, "gsap")); fs.mkdirSync(path.join(local, "fontes"));
  for (const a of [path.basename(pagina), "gsap.min.js", "comum.js"]) fs.copyFileSync(path.join(dir, a), path.join(local, "gsap", a));
  fs.copyFileSync(path.join(dir, "..", "fontes", "Montserrat.ttf"), path.join(local, "fontes", "Montserrat.ttf"));
  await pg.goto("file://" + path.join(local, "gsap", path.basename(pagina)));
  await pg.evaluate(async () => { await document.fonts.ready; });
  await pg.waitForFunction(() => !!window.TL, null, { polling: 100, timeout: 20000 });
  const ff = spawn("ffmpeg", ["-loglevel", "error", "-y", "-f", "image2pipe", "-framerate", String(fps), "-i", "-",
    "-c:v", "qtrle", "-pix_fmt", "argb", saida], { stdio: ["pipe", "inherit", "inherit"] });
  for (let q = 0; q < nq; q++) {
    await pg.evaluate(t => { window.TL.seek(t, false); }, q / fps);  // sem retorno: serializar a timeline travava
    ff.stdin.write(await pg.screenshot({ omitBackground: true, type: "png" }));
  }
  ff.stdin.end();
  await new Promise(r => ff.on("close", r));
  await nav.close();
  fs.rmSync(local, { recursive: true, force: true });
  console.log(`camada: ${nq} quadros -> ${saida}`);
})();
