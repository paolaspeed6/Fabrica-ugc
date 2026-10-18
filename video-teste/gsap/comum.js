// Funções comuns das camadas GSAP.
function el(tag, cls, pai, txt) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (txt != null) e.textContent = txt;
  (pai || document.body).appendChild(e);
  return e;
}
// "O [ferro] preto" -> "O ferro preto"
function limpo(t) { return t.replace(/\[|\]/g, ""); }
// divide uma frase em 2 linhas: na vírgula, se houver; senão no meio, por palavras
function duasLinhas(t) {
  const mv = t.match(/,(?!\d)/), v = mv ? mv.index : -1;
  if (v > 0 && v < t.length - 2) return [t.slice(0, v + 1).trim(), t.slice(v + 1).trim()];
  const p = t.split(" ");
  if (p.length < 3) return [t];
  let melhor = 1, dif = 1e9;
  for (let k = 1; k < p.length; k++) {
    const d = Math.abs(p.slice(0, k).join(" ").length - p.slice(k).join(" ").length);
    if (d < dif) { dif = d; melhor = k; }
  }
  return [p.slice(0, melhor).join(" "), p.slice(melhor).join(" ")];
}
// reduz a fonte até o elemento caber na largura
function caber(e, larg, max, min) {
  let t = max;
  e.style.fontSize = t + "px";
  while (e.getBoundingClientRect().width > larg && t > min) { t -= 2; e.style.fontSize = t + "px"; }
}
// "[destaque]" vira <em>
function destaque(e, t) {
  t.split(/(\[[^\]]+\])/).forEach(p => {
    if (!p) return;
    if (p[0] === "[") el("em", null, e, p.slice(1, -1)); else e.appendChild(document.createTextNode(p));
  });
}
