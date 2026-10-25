/* =====================================================================
   MOTOR DO REINO
   Junta o fluxo real (fluxo.js), a aparência (tema.js + arte.js) e o
   banco da página. Não decide nada da produção: só mostra.

   Banco desta página (coleções):
   - reino/estado          estado real de cada etapa (gravado pelo Claude com
                           paginas/reino/sincronizar.py; veja paginas/reino/LEIA.md)
   - postagens_resumo/atual contador de postados
   - metas, mural, gastos  (iguais ao jogo antigo)
   ===================================================================== */
(() => {
  const $ = id => document.getElementById(id);
  const esc = t => String(t ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const ls = { get: k => { try { return localStorage.getItem(k); } catch (e) { return null; } }, set: (k, v) => { try { localStorage.setItem(k, v); } catch (e) { } } };
  const poucoMovimento = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
  const VALIDOS = ["trabalhando", "sua_vez", "aguardando", "concluido", "erro"];
  const brl = v => "R$ " + v.toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const usd = v => "US$ " + v.toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const MES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"];
  const dataCurta = s => { const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(s || ""); return m ? `${+m[3]} ${MES[+m[2] - 1]}` : ""; };
  const dataLonga = d => { try { return new Date(d + "T12:00:00Z").toLocaleDateString("pt-BR", { day: "2-digit", month: "long", timeZone: "UTC" }); } catch (e) { return d; } };

  let ESTADO = null, carregou = false, METAS = [], MURAL = [], GASTOS = [], RESUMO = null, dbRef = null;

  /* ---------- visual de cada etapa (tema por cima do fluxo) ---------- */
  function visual(etapa) {
    const t = TEMA.estacoes[etapa.id] || TEMA.padrao;
    return { nome: t.nome || etapa.nome, predio: t.predio, cores: t.cores, personagem: t.personagem, fala: t.fala || "" };
  }
  function estadoDe(id) {
    const e = ESTADO && ESTADO.etapas && ESTADO.etapas[id];
    if (e && VALIDOS.includes(e.estado)) return { estado: e.estado, texto: e.texto || "", qtd: Number(e.qtd) || 0, itens: Array.isArray(e.itens) ? e.itens : [] };
    return { estado: "aguardando", qtd: 0, itens: [], semNoticia: true,
      texto: !carregou ? "Lendo o estado do reino..." : dbRef ? "Ainda sem notícia desta etapa. Peça no chat: Atualiza o reino." : "Abra logada no app do Claude para ver o estado real." };
  }
  const rotulo = e => (TEMA.estados[e] || {}).rotulo || e;
  const selo = e => `<span class="selo" data-e="${e}">${ARTE.ICONE[e] || ""}${esc(rotulo(e))}</span>`;

  /* ---------- topo e abas ---------- */
  $("marca").textContent = TEMA.marca; $("titulo").textContent = TEMA.titulo; $("subtitulo").textContent = TEMA.rodape; $("rodape").textContent = TEMA.rodape;
  const diretora = TEMA.estacoes.capataz || TEMA.padrao;
  $("cena-topo").innerHTML = ARTE.predio(diretora.predio, diretora.cores, 92) + ARTE.personagem(diretora.personagem, 46);

  const ORDEM = ["castelo", "floresta", "conquistas", "mural", "cofre", "brincar", "perdas"];
  const ALIAS = { missoes: "castelo", mapa: "floresta", metas: "conquistas", gasto: "cofre", jogos: "brincar", desperdicio: "perdas", desp: "perdas" };
  $("abas").innerHTML = ORDEM.map(k => `<button type="button" role="tab" id="t-${k}" aria-controls="aba-${k}" aria-selected="false">${esc(TEMA.abas[k] || k)}</button>`).join("");
  let abaAtual = null, mapaSujo = true;
  function aba(k) {
    k = ALIAS[k] || k; if (!ORDEM.includes(k)) k = "castelo";
    abaAtual = k;
    ORDEM.forEach(n => { $("t-" + n).setAttribute("aria-selected", String(n === k)); $("aba-" + n).hidden = n !== k; });
    if (k === "floresta" && mapaSujo) montarMapa();
    ls.set("aba", k);
  }
  ORDEM.forEach(n => $("t-" + n).onclick = () => aba(n));
  document.addEventListener("click", ev => { const b = ev.target.closest("[data-ir]"); if (b) { aba(b.dataset.ir); scrollTo({ top: 0 }); } });

  /* ---------- floresta ---------- */
  function rnd(seed) { return () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  const PASSO = 214, TOPO = 46;
  function montarMapa() {
    const mapa = $("mapa"); if (!mapa.offsetParent) { mapaSujo = true; return; }
    mapaSujo = false;
    const W = Math.max(320, mapa.clientWidth || 360);
    const EST = FLUXO.etapas, n = EST.length;
    const H = TOPO + n * PASSO + 30;
    mapa.style.height = H + "px";
    const r = rnd(7);
    const pts = EST.map((e, i) => ({ x: i % 2 ? W * .70 : W * .30, y: TOPO + i * PASSO + 64 }));
    const anc = pts.map(p => ({ x: p.x, y: p.y + 44 }));
    const seg = i => { const a = anc[i], b = anc[i + 1], k = PASSO * .6; return `M${a.x} ${a.y} C${a.x} ${a.y + k}, ${b.x} ${b.y - k}, ${b.x} ${b.y}`; };
    let d = `M${anc[0].x} ${anc[0].y - 60} L${anc[0].x} ${anc[0].y}`;
    for (let i = 1; i < n; i++) { const a = anc[i - 1], b = anc[i], k = PASSO * .6; d += ` C${a.x} ${a.y + k}, ${b.x} ${b.y - k}, ${b.x} ${b.y}`; }

    let s = "";
    // relva
    for (let k = 0; k < n * 7; k++) { const x = r() * W, y = r() * H; s += `<path d="M${x.toFixed(1)} ${y.toFixed(1)} q1.5 -6 3 0 q1.5 -5 3 0" stroke="var(--relva-3)" stroke-width="1.4" fill="none" opacity=".8"/>`; }
    // rio entre a 7ª e a 8ª etapa, com ponte
    const ri = Math.min(6, n - 2);
    const m = { x: (anc[ri].x + anc[ri + 1].x) / 2, y: (anc[ri].y + anc[ri + 1].y) / 2 };
    let rio = "", rio2 = "";
    for (let x = -30; x <= W + 30; x += 15) { const y = m.y + 13 * Math.sin((x - m.x) / W * Math.PI * 2.4); rio += (x === -30 ? "M" : "L") + x + " " + y.toFixed(1) + " "; rio2 += (x === -30 ? "M" : "L") + x + " " + (y - 6).toFixed(1) + " "; }
    s += `<path d="${rio}" stroke="var(--rio)" stroke-width="40" fill="none" stroke-linecap="round"/><path d="${rio2}" stroke="var(--rio-brilho)" stroke-width="2.2" fill="none" stroke-dasharray="14 22" opacity=".9"/>`;
    // trilha de pedras
    s += `<path d="${d}" stroke="var(--trilha-borda)" stroke-width="36" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="${d}" stroke="var(--trilha)" stroke-width="29" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="${d}" stroke="var(--pedra)" stroke-width="8" fill="none" stroke-linecap="round" stroke-dasharray="1 12"/>`;
    // ponte (direção da trilha no meio do trecho)
    const ang = Math.atan2(PASSO * .6, 1.5 * (anc[ri + 1].x - anc[ri].x)) * 180 / Math.PI;
    s += `<g transform="translate(${m.x} ${m.y}) rotate(${(ang - 90).toFixed(1)})"><rect x="-21" y="-30" width="42" height="60" rx="3" fill="#b98962" stroke="var(--traco)" stroke-width="1.6"/>${[-24, -14, -4, 6, 16].map(y => `<path d="M-21 ${y} H21" stroke="var(--traco)" stroke-width="1" opacity=".45"/>`).join("")}<path d="M-24 -32 V32 M24 -32 V32" stroke="#8a6146" stroke-width="4" stroke-linecap="round"/></g>`;
    // árvores do lado vazio, pinheiros na borda, flores e cogumelos
    pts.forEach((p, i) => {
      const lx = i % 2 ? W * .19 : W * .81;
      if (i !== ri && i !== ri + 1) s += ARTE.arvore(lx + (r() - .5) * 20, p.y + 54, .95 + r() * .2, i);
      else s += ARTE.cogumelo(lx, p.y + 40, 2, "#e8a7bd");
      s += ARTE.cogumelo(lx + 34, p.y + 74, 1.3, ["#e8a7bd", "#c8b6e2", "#e9c77b"][i % 3]);
      s += ARTE.flor(lx - 30, p.y + 78, ["#e8a7bd", "#fbf3e6", "#c8b6e2"][i % 3]) + ARTE.flor(lx - 22, p.y + 84, "#f2d27a");
      if (i % 2 === 0) s += ARTE.pinheiro(W * .955, p.y + 150, .8); else s += ARTE.pinheiro(W * .045, p.y + 150, .8);
      if (i < n - 1 && i !== ri) { const a = anc[i], b = anc[i + 1]; s += ARTE.poste((a.x + b.x) / 2 + 26, (a.y + b.y) / 2 + 8); }
    });
    // placa de entrada
    s += `<g transform="translate(${anc[0].x + 46} ${TOPO - 4})"><path d="M0 34 V4" stroke="#8a6146" stroke-width="3"/><path d="M-30 -8 H28 L36 1 L28 10 H-30 Z" fill="#c79a77" stroke="var(--traco)" stroke-width="1.5"/><text x="-26" y="5.5" font-family="Caprasimo,Georgia,serif" font-size="11.5" fill="#3b2633">Entrada</text></g>`;

    // encomendas andando (só quando a etapa está trabalhando de verdade e tem produtos)
    if (!poucoMovimento()) EST.forEach((e, i) => {
      const st = estadoDe(e.id); if (st.estado !== "trabalhando" || !st.qtd || i >= n - 1) return;
      s += `<g><g transform="translate(-6 -10)"><rect width="12" height="11" rx="1.5" fill="#f0c6d3" stroke="var(--traco)" stroke-width="1.2"/><path d="M6 0 V11 M0 4.5 H12" stroke="#e9c77b" stroke-width="1.6"/></g><animateMotion dur="7s" repeatCount="indefinite" path="${seg(i)}"/></g>`;
    });

    mapa.innerHTML = `<svg class="chao" viewBox="0 0 ${W} ${H}" preserveAspectRatio="none" aria-hidden="true">${s}</svg>`;

    EST.forEach((e, i) => mapa.appendChild(estacao(e, i, pts[i], W)));

    // bichinhos: borboletas, coelho e vaga-lumes (enfeite, não atrapalham o toque)
    const enf = document.createDocumentFragment();
    [["#f4c2d1", .12, .18], ["#d9ccf0", .62, .44], ["#f2d27a", .3, .78]].forEach(([c, x, y], k) => {
      const b = document.createElement("div"); b.className = "bicho borb"; b.style.left = (x * W) + "px"; b.style.top = (y * H) + "px"; b.style.animationDelay = (-k * 6) + "s";
      b.innerHTML = ARTE.borboleta(c); enf.append(b);
    });
    // coelho ao pé da árvore do lado vazio da 3ª estação (longe dos nomes)
    const pc = pts[Math.min(2, n - 1)];
    const co = document.createElement("div"); co.className = "bicho"; co.style.left = (W * .81 - 58) + "px"; co.style.top = (pc.y + 26) + "px"; co.innerHTML = ARTE.coelho(); enf.append(co);
    for (let k = 0; k < 14; k++) { const v = document.createElement("i"); v.className = "vaga"; v.style.left = (r() * W) + "px"; v.style.top = (r() * H) + "px"; v.style.animationDelay = (-r() * 3.6) + "s"; enf.append(v); }
    mapa.append(enf);
  }

  function estacao(e, i, pt, W) {
    const v = visual(e), st = estadoDe(e.id);
    const b = document.createElement("button"); b.type = "button";
    b.className = "est " + (i % 2 ? "lado-d" : "lado-e"); b.dataset.e = st.estado;
    const L = 172; b.style.left = Math.max(6, Math.min(W - L - 6, pt.x - L / 2)) + "px"; b.style.top = (pt.y - 64) + "px";
    const enc = st.qtd > 0 ? `<span class="encomendas">${ARTE.encomendas(st.qtd)}<b>${st.qtd}</b></span>` : "";
    b.innerHTML = `<div class="cena"><span class="num">${i + 1}</span>${selo(st.estado)}${ARTE.ENFEITE}${ARTE.predio(v.predio, v.cores, 118)}${ARTE.personagem(v.personagem, 50)}${enc}</div>
      <div class="nome"><b>${esc(v.nome)}</b><small>${esc(e.nome)}${e.papel ? " · " + esc(e.papel) : ""}</small></div>`;
    b.setAttribute("aria-label", `${i + 1}. ${v.nome}, etapa ${e.nome}. ${rotulo(st.estado)}${st.qtd ? ", " + st.qtd + " produtos" : ""}`);
    b.onclick = () => abrirEtapa(e, i);
    return b;
  }

  /* ---------- folha ---------- */
  const veu = $("veu"), folha = $("folha"); let ultimo = null;
  const link = (t, u) => `<a class="btn" href="${esc(u)}" target="_blank" rel="noopener">${esc(t)}</a>`;
  function abrirFolha(html) {
    ultimo = document.activeElement;
    folha.innerHTML = `<div class="folha-in"><div class="alca"></div>${html}</div>`;
    veu.hidden = false; folha.hidden = false; folha.scrollTop = 0;
    folha.querySelectorAll("[data-fechar]").forEach(x => x.onclick = fechar);
    folha.querySelectorAll("[data-copiar]").forEach(x => x.onclick = () => copiar(x.dataset.copiar, x));
    folha.querySelectorAll("[data-aba]").forEach(x => x.onclick = () => { fechar(); aba(x.dataset.aba); scrollTo({ top: 0 }); });
    const f = folha.querySelector("[data-fechar]"); if (f) f.focus({ preventScroll: true });
  }
  function fechar() { veu.hidden = true; folha.hidden = true; if (ultimo && ultimo.focus) ultimo.focus(); }
  veu.onclick = fechar;
  document.addEventListener("keydown", ev => { if (ev.key === "Escape" && !folha.hidden) fechar(); });

  function abrirEtapa(e, i) {
    const v = visual(e), st = estadoDe(e.id), p = v.personagem || {};
    const quando = ESTADO && ESTADO.atualizado_em ? new Date(ESTADO.atualizado_em).toLocaleString("pt-BR", { timeZone: "America/Sao_Paulo", day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit" }) : "";
    const acoes = (e.acao || []).map(([t, u]) => link(t, u)).join("") + (e.comando ? `<button class="btn lilas" type="button" data-copiar="${esc(e.comando)}">Copiar: ${esc(e.comando)}</button>` : "");
    abrirFolha(`<div class="f-topo"><div class="arte">${ARTE.predio(v.predio, v.cores, 112)}${ARTE.personagem(p, 50)}</div>
        <div><div class="quem">Estação ${i + 1} · ${esc(p.nome || "")}${p.titulo ? ", " + esc(p.titulo) : ""}</div><h2 id="f-nome">${esc(v.nome)}</h2></div></div>
      <div class="real"><span class="rot">Etapa real</span><b>${esc(e.nome)}${e.papel ? " · " + esc(e.papel) : ""}</b><span class="rot">Quem faz</span><b>${e.quem === "voce" ? "Você" : "Claude, sozinho"}</b></div>
      <div class="agora-box" data-e="${st.estado}"><div class="linha1">${selo(st.estado)}${quando && !st.semNoticia ? `<small>atualizado ${quando}</small>` : ""}</div>
        <div style="margin-top:6px">${esc(st.texto)}</div>${st.itens.length ? `<ul>${st.itens.slice(0, 6).map(t => `<li>${esc(t)}</li>`).join("")}</ul>` : ""}</div>
      <p class="fala">“${esc(v.fala)}”</p>
      <div class="f-corpo"><p>${esc(e.faz)}</p>
        <div class="dupla"><b>Entra</b><span>${esc(e.entra)}</span></div>
        <div class="dupla"><b>Sai</b><span>${esc(e.sai)}</span></div>
        <div class="dupla"><b>Custo</b><span>${esc(e.custo)}</span></div></div>
      <div class="botoes">${acoes}<button class="btn sec" type="button" data-fechar>Fechar</button></div>`);
  }
  function abrirArea(a) {
    const f = FLUXO.areas.find(x => x.id === a.id) || {}, p = a.personagem || {};
    const ir = a.abre && a.abre.aba ? `<button class="btn" type="button" data-aba="${esc(a.abre.aba)}">Entrar: ${esc(TEMA.abas[a.abre.aba] || a.abre.aba)}</button>` : a.abre && a.abre.link ? link("Abrir", a.abre.link) : "";
    abrirFolha(`<div class="f-topo"><div class="arte">${ARTE.predio(a.predio, a.cores, 112)}${ARTE.personagem(p, 50)}</div>
        <div><div class="quem">${esc(p.nome || "")}${p.titulo ? ", " + esc(p.titulo) : ""}</div><h2 id="f-nome">${esc(a.nome)}</h2></div></div>
      <div class="real"><span class="rot">Na fábrica</span><b>${esc(f.nome || a.nome)}${f.papel ? " · " + esc(f.papel) : ""}</b></div>
      <p class="fala">“${esc(a.fala || "")}”</p>
      <div class="f-corpo">${f.faz ? `<p>${esc(f.faz)}</p>` : ""}${f.entra ? `<div class="dupla"><b>Entra</b><span>${esc(f.entra)}</span></div><div class="dupla"><b>Sai</b><span>${esc(f.sai)}</span></div><div class="dupla"><b>Custo</b><span>${esc(f.custo)}</span></div>` : ""}</div>
      <div class="botoes">${ir}<button class="btn sec" type="button" data-fechar>Fechar</button></div>`);
  }

  /* ---------- áreas, legenda, leis ---------- */
  function montarAreas() {
    const box = $("areas"); box.innerHTML = "";
    TEMA.areas.forEach(a => {
      const f = FLUXO.areas.find(x => x.id === a.id) || {};
      const b = document.createElement("button"); b.type = "button"; b.className = "area";
      b.innerHTML = `<div class="mini">${ARTE.predio(a.predio, a.cores, 100)}${ARTE.personagem(a.personagem, 40)}</div><h3>${esc(a.nome)}</h3><p>${esc(f.papel || "")}</p>`;
      b.onclick = () => abrirArea(a); box.append(b);
    });
    $("legenda").innerHTML = VALIDOS.map(e => selo(e)).join("");
    $("leis").innerHTML = FLUXO.leis.map(l => `<li>${esc(l)}</li>`).join("");
  }

  /* ---------- castelo (painel) ---------- */
  function copiar(t, el) {
    const ok = () => { const o = el.dataset.txt || el.innerHTML; el.dataset.txt = o; const sm = el.querySelector("small"); if (sm) sm.textContent = "copiado"; else el.textContent = "Copiado!"; setTimeout(() => { el.innerHTML = el.dataset.txt; }, 1600); };
    try { navigator.clipboard.writeText(t).then(ok, () => {}); } catch (e) { }
  }
  function renderCastelo() {
    const EST = FLUXO.etapas;
    const sv = EST.filter(e => estadoDe(e.id).estado === "sua_vez");
    const er = EST.filter(e => estadoDe(e.id).estado === "erro");
    // avisos do topo: o que espera você e o que deu erro
    $("avisos").innerHTML = "";
    er.concat(sv).forEach(e => {
      const st = estadoDe(e.id), v = visual(e), i = EST.indexOf(e);
      const b = document.createElement("button"); b.type = "button"; b.className = "aviso" + (st.estado === "erro" ? " erro" : "");
      b.innerHTML = `${ARTE.personagem(v.personagem, 50)}<div><div>${selo(st.estado)}</div><h3>${esc(v.nome)}</h3><p>${esc(st.texto)}</p></div>`;
      b.onclick = () => abrirEtapa(e, i); $("avisos").append(b);
    });
    // números
    const prod = FLUXO.producao.reduce((t, id) => t + estadoDe(id).qtd, 0);
    const fila = estadoDe("fila").qtd;
    $("k-andando").textContent = carregou && ESTADO ? prod : "-";
    $("k-andando-d").textContent = carregou && ESTADO ? `em produção agora · ${fila} na Vila das Encomendas` : "esperando o estado do reino";
    $("k-voce").textContent = carregou && ESTADO ? sv.length : "-";
    $("k-voce-d").textContent = sv.length ? sv.map(e => visual(e).nome).join(", ") : (carregou && ESTADO ? "nada pendente" : "esperando o estado do reino");
    const trab = EST.filter(e => estadoDe(e.id).estado === "trabalhando");
    const auto = ESTADO && ESTADO.automaticas ? FLUXO.automaticas.filter(a => ESTADO.automaticas[a.id] && ESTADO.automaticas[a.id].ligada) : [];
    $("k-auto").textContent = carregou && ESTADO ? (trab.length + auto.length) : "-";
    $("k-auto-d").textContent = carregou && ESTADO ? `${trab.length} etapas trabalhando · ${auto.length} de ${FLUXO.automaticas.length} feitiços ligados` : "esperando o estado do reino";
    const mv = METAS.find(m => m.id === "videos");
    $("k-videos").textContent = mv ? (mv.atual || 0).toLocaleString("pt-BR") : "-";
    // missões
    const box = $("missoes"); box.innerHTML = "";
    const ord = { erro: 0, sua_vez: 1, trabalhando: 2, concluido: 3, aguardando: 4 };
    FLUXO.missoes.map(m => ({ m, st: EST.some(e => e.id === m.id) ? estadoDe(m.id) : null }))
      .sort((a, b) => (a.st ? ord[a.st.estado] : 5) - (b.st ? ord[b.st.estado] : 5))
      .forEach(({ m, st }) => {
        const t = TEMA.estacoes[m.id] || TEMA.areas.find(a => a.id === m.id) || TEMA.padrao;
        const a = document.createElement("article"); a.className = "missao cartao";
        a.innerHTML = `<div>${ARTE.personagem(t.personagem, 50)}</div><div><h3>${esc(m.n)}</h3>
          <div class="linha-selo">${st && !st.semNoticia ? selo(st.estado) + `<span>${esc(st.texto)}</span>` : `<span>${esc(m.agora)}</span>`}</div>
          <p>${esc(m.t)}</p>${(m.acao || []).length ? `<div class="botoes">${m.acao.map(([x, u]) => link(x, u)).join("")}</div>` : ""}</div>`;
        box.append(a);
      });
    // automáticas
    $("automaticas").innerHTML = FLUXO.automaticas.map(a => {
      const x = ESTADO && ESTADO.automaticas && ESTADO.automaticas[a.id];
      return `<li><span class="ponto${x && x.ligada ? " ok" : ""}"></span><span><b>${esc(a.nome)}</b> ${esc(a.quando)}.<small>${x ? (x.ligada ? "Ligado. " : "Parado. ") + esc(x.texto || "") : "Sem notícia ainda."}</small></span></li>`;
    }).join("");
    renderRecentes();
  }
  function renderRecentes() {
    const r = ESTADO && Array.isArray(ESTADO.recentes) ? ESTADO.recentes.slice(0, 12) : [];
    const html = r.length ? r.map(x => `<li><time>${esc(dataCurta(x.quando))}</time><span>${esc(x.texto)}</span></li>`).join("") : `<li><span></span><span class="vazio">${carregou ? "Ainda sem novidades registradas." : "Lendo as novidades..."}</span></li>`;
    $("recentes").innerHTML = r.length ? r.slice(0, 4).map(x => `<li><time>${esc(dataCurta(x.quando))}</time><span>${esc(x.texto)}</span></li>`).join("") : html;
    $("recentes-2").innerHTML = html;
  }
  function montarFixos() {
    $("cmds").innerHTML = "";
    FLUXO.comandos.forEach(([t, d]) => {
      const b = document.createElement("button"); b.type = "button"; b.className = "cmd";
      b.innerHTML = `<span>${esc(t)}</span><small>${esc(d)}</small>`; b.onclick = () => copiar(t, b); $("cmds").append(b);
    });
    $("paginas").innerHTML = FLUXO.paginas.map(([n, d, u]) => `<a class="pag" href="${esc(u)}" target="_blank" rel="noopener"><b>${esc(n)}</b><span>${esc(d)}</span></a>`).join("");
    $("monstros").innerHTML = FLUXO.monstros.map((m, k) => `<article class="monstro cartao"><div>${nuvem(k)}</div>
      <div><h3>${esc(m.n)}</h3><div class="valor">Custou US$ ${esc(m.usd)} na fábrica original</div><p>${esc(m.o)}</p><div class="regra">Regra em vigor: ${esc(m.r)}</div></div></article>`).join("");
    $("d-monstros").textContent = FLUXO.monstros.length;
    $("testes").innerHTML = FLUXO.testes.map(t => `<li>${esc(t[0])}: <b>US$ ${esc(t[1])}</b>. ${esc(t[2].charAt(0).toUpperCase() + t[2].slice(1))}.</li>`).join("");
    $("aprender").innerHTML = FLUXO.aprender.map(([a, b]) => `<li><b>${esc(a)}</b> ${esc(b)}</li>`).join("");
    $("g-teto").textContent = brl(FLUXO.teto.porProduto).replace(",00", "");
    $("g-medio").textContent = usd(FLUXO.teto.custoMedioUSD);
    $("g-cambio").textContent = FLUXO.teto.cambio.toLocaleString("pt-BR");
  }
  // monstrinho do desperdício: uma nuvenzinha de chuva já domada
  const nuvem = k => `<svg viewBox="0 0 56 50" width="54" height="48" aria-hidden="true"><path d="M10 30 a10 10 0 0 1 8 -14 a14 14 0 0 1 26 2 a9 9 0 0 1 2 18 H14 a8 8 0 0 1 -4 -6z" fill="${["#c8b6e2", "#c9c3d4", "#b9cdaa", "#b7d2df", "#d9cfc4", "#f0c6d3", "#f3e4bd"][k % 7]}" stroke="var(--traco)" stroke-width="1.6"/><circle cx="23" cy="26" r="2" fill="#3b2633"/><circle cx="35" cy="26" r="2" fill="#3b2633"/><path d="M26 32 q3 2 6 0" stroke="#3b2633" stroke-width="1.4" fill="none" stroke-linecap="round"/><path d="M18 42 l-2 4 M28 42 l-2 4 M38 42 l-2 4" stroke="#8fa7d0" stroke-width="1.6" stroke-linecap="round"/></svg>`;

  /* ---------- conquistas e nível ---------- */
  function confete() {
    if (poucoMovimento()) return;
    const c = document.createElement("div"); c.className = "confete";
    const cores = ["#e8a7bd", "#f2d27a", "#c8b6e2", "#a8bfa0", "#fbf3e6"];
    for (let i = 0; i < 46; i++) { const p = document.createElement("i"); p.style.left = Math.random() * 100 + "%"; p.style.background = cores[i % cores.length]; p.style.animationDelay = (Math.random() * .5) + "s"; c.append(p); }
    document.body.append(c); setTimeout(() => c.remove(), 2800);
  }
  const TROFEU = '<svg viewBox="0 0 40 40" width="30" height="30" aria-hidden="true"><path d="M12 6 h16 v8 a8 8 0 0 1 -16 0z" fill="#e9c77b" stroke="#a9853d" stroke-width="2"/><path d="M12 9 h-5 a5 5 0 0 0 6 7 M28 9 h5 a5 5 0 0 1 -6 7" fill="none" stroke="#a9853d" stroke-width="1.8"/><rect x="17" y="22" width="6" height="6" fill="#e9c77b" stroke="#a9853d" stroke-width="1.6"/><rect x="12" y="28" width="16" height="5" rx="2" fill="#e8a7bd" stroke="#a9853d" stroke-width="1.6"/></svg>';
  function renderMetas() {
    const lista = METAS.slice().sort((a, b) => (a.ordem || 0) - (b.ordem || 0));
    const ganhas = lista.filter(m => m.alvo && m.atual >= m.alvo).length;
    const frac = lista.length ? lista.reduce((t, m) => t + Math.min(1, (m.atual || 0) / (m.alvo || 1)), 0) / lista.length : 0;
    const N = TEMA.niveis; let nv = N[0], prox = N[1];
    N.forEach((x, i) => { if (frac >= x[1]) { nv = x; prox = N[i + 1] || null; } });
    $("nv-nome").textContent = nv[0];
    $("nv-pts").textContent = lista.length ? `${ganhas} de ${lista.length} troféus${prox ? " · próximo: " + prox[0] : ""}` : "";
    $("nv-barra").style.width = (prox ? Math.min(100, (frac - nv[1]) / (prox[1] - nv[1]) * 100) : 100) + "%";
    $("mt-cont").textContent = lista.length ? `${ganhas} de ${lista.length} metas cumpridas.` : "";
    $("k-metas").textContent = lista.length ? `${ganhas}/${lista.length}` : "-";
    $("k-metas-d").textContent = lista.length ? `troféus · nível ${nv[0]}` : "sem metas salvas";
    const mv = METAS.find(m => m.id === "videos"); $("k-videos").textContent = mv ? (mv.atual || 0).toLocaleString("pt-BR") : "-";
    if (!lista.length) { $("metas").innerHTML = '<p class="vazio">Ainda sem metas salvas.</p>'; return; }
    $("metas").innerHTML = lista.map(m => {
      const ok = m.alvo && m.atual >= m.alvo, pc = Math.min(100, (m.atual || 0) / (m.alvo || 1) * 100);
      return `<article class="meta cartao${ok ? " ganhou" : ""}"><div class="medalha">${TROFEU}</div><h3>${esc(m.nome)}</h3><span class="qt">${(m.atual || 0).toLocaleString("pt-BR")} / ${(m.alvo || 0).toLocaleString("pt-BR")}${m.unidade ? " " + esc(m.unidade) : ""}</span>
        <div class="trilho"><i style="width:${pc}%"></i></div>${m.detalhe ? `<p>${esc(m.detalhe)}</p>` : ""}</article>`;
    }).join("");
  }

  /* ---------- mural ---------- */
  const TIPOS = { todos: "Todos", pedido: "Pedidos seus", prompt: "Prompts", geracao: "Erros de geração", layout: "Layout e edição", regra: "Regras", sistema: "Sistema" };
  const SITU = { tudo: "Tudo", feito: "Feitas", a_fazer: "Vão ser feitas" };
  let fTipo = "todos", fEst = "tudo";
  function filtros(id, mapaF, atual, set) {
    $(id).innerHTML = Object.entries(mapaF).map(([k, t]) => `<button type="button" data-k="${k}" aria-pressed="${k === atual}">${t}</button>`).join("");
    $(id).querySelectorAll("button").forEach(b => b.onclick = () => { set(b.dataset.k); renderMural(); });
  }
  function renderMural() {
    filtros("mu-estado", SITU, fEst, k => fEst = k); filtros("mu-tipo", TIPOS, fTipo, k => fTipo = k);
    const feitas = MURAL.filter(m => m.status !== "a_fazer").length;
    $("mu-cont").textContent = MURAL.length ? `${feitas} feitas · ${MURAL.length - feitas} por fazer` : "";
    const lista = MURAL.filter(m => (fTipo === "todos" || m.tipo === fTipo) && (fEst === "tudo" || (fEst === "feito" ? m.status !== "a_fazer" : m.status === "a_fazer")))
      .sort((a, b) => ((a.status === "a_fazer") === (b.status === "a_fazer") ? 0 : a.status === "a_fazer" ? -1 : 1) || (b.data || "").localeCompare(a.data || "") || (a.ordem || 0) - (b.ordem || 0));
    if (!lista.length) { $("mural").innerHTML = `<p class="vazio">${MURAL.length ? "Nada neste filtro." : carregou ? "Ainda sem correções salvas." : "O mural aparece aqui assim que a página carrega."}</p>`; return; }
    let grupo = null, html = "";
    lista.forEach(m => {
      const g = m.status === "a_fazer" ? "Vão ser feitas" : dataLonga(m.data);
      if (g !== grupo) { grupo = g; html += `<div class="dia">${esc(g)}</div>`; }
      html += `<article class="nota-m cartao${m.status === "a_fazer" ? " afazer" : ""}"><div class="top"><span class="tipo ${esc(m.tipo)}">${esc(TIPOS[m.tipo] || m.tipo)}</span>${m.status === "a_fazer" ? `<span class="selo" data-e="sua_vez">pedido em ${esc(dataLonga(m.data))}</span>` : ""}</div>
        <h3>${esc(m.titulo)}</h3>${m.citacao ? `<q>${esc(m.citacao)}</q>` : ""}${m.texto ? `<p>${esc(m.texto)}</p>` : ""}</article>`;
    });
    $("mural").innerHTML = html;
  }

  /* ---------- cofre ---------- */
  const CAMBIO = FLUXO.teto.cambio;
  const emBRL = g => g.valor == null ? null : (g.moeda === "USD" ? g.valor * CAMBIO : g.valor);
  function renderGasto() {
    const grupos = { contado: [], preencher: [], gratis: [] };
    GASTOS.slice().sort((a, b) => (a.ordem || 0) - (b.ordem || 0)).forEach(g => (grupos[g.grupo] || grupos.contado).push(g));
    const somaC = grupos.contado.reduce((t, g) => t + (emBRL(g) || 0), 0), somaP = grupos.preencher.reduce((t, g) => t + (emBRL(g) || 0), 0);
    const faltam = grupos.preencher.filter(g => g.valor == null).length, tot = somaC + somaP;
    $("g-total").textContent = brl(tot);
    $("g-sub").textContent = GASTOS.length ? (faltam ? `Faltam ${faltam} valores seus, então o total real é maior.` : "Tudo preenchido.") : "Ainda sem valores salvos.";
    $("k-gasto").textContent = GASTOS.length ? brl(tot) : "-";
    $("k-gasto-d").textContent = GASTOS.length ? (faltam ? `faltam ${faltam} valores seus · teto R$ ${FLUXO.teto.porProduto} por produto` : `teto R$ ${FLUXO.teto.porProduto} por produto`) : "sem valores salvos";
    const pc = tot ? somaC / tot * 100 : 0;
    $("g-barra").innerHTML = tot ? `<i style="width:${pc}%;background:var(--st-trab)"></i><i style="width:${100 - pc}%;background:var(--rosa)"></i>` : "";
    $("g-leg").innerHTML = `<span><i style="background:var(--st-trab)"></i>Contado pelo Claude ${brl(somaC)}</span><span><i style="background:var(--rosa)"></i>Você preencheu ${brl(somaP)}</span>`;
    const linha = g => { const v = emBRL(g); return `<div class="g-item"><span class="gn">${esc(g.nome)}</span><span class="gv">${v == null ? "" : brl(v)}${g.moeda === "USD" && g.valor != null ? `<small>${usd(g.valor)}</small>` : ""}</span>${g.detalhe ? `<span class="gd">${esc(g.detalhe)}</span>` : ""}</div>`; };
    if (grupos.contado.length) $("g-contado").innerHTML = grupos.contado.map(linha).join("");
    if (grupos.gratis.length) $("g-gratis").innerHTML = grupos.gratis.map(g => `<div class="g-item"><span class="gn">${esc(g.nome)}</span><span class="gv">R$ 0</span>${g.detalhe ? `<span class="gd">${esc(g.detalhe)}</span>` : ""}</div>`).join("");
    if (!grupos.preencher.length) return;
    const foco = document.activeElement && document.activeElement.id;
    $("g-preencher").innerHTML = grupos.preencher.map(g => `<div class="g-item${g.valor == null ? " falta" : ""}"><label class="gn" for="gi-${esc(g.id)}">${esc(g.nome)}</label>
      <span class="g-campo">R$ <input id="gi-${esc(g.id)}" data-id="${esc(g.id)}" inputmode="decimal" placeholder="0,00" value="${g.valor == null ? "" : g.valor.toFixed(2).replace(".", ",")}" ${dbRef ? "" : "disabled"}></span>
      ${g.detalhe ? `<span class="gd">${esc(g.detalhe)}</span>` : ""}<span class="g-ok" id="go-${esc(g.id)}"></span></div>`).join("");
    $("g-preencher").querySelectorAll("input").forEach(inp => inp.addEventListener("change", () => salvar(inp)));
    if (foco && $(foco)) $(foco).focus();
  }
  async function salvar(inp) {
    const id = inp.dataset.id, ok = $("go-" + id);
    const t = inp.value.trim().replace(/\./g, "").replace(",", ".");
    const v = t === "" ? null : Number(t);
    if (v !== null && (!isFinite(v) || v < 0)) { ok.textContent = "Digite só o número, por exemplo 110,00"; ok.style.color = "var(--st-erro)"; return; }
    ok.style.color = ""; ok.textContent = "Salvando...";
    try { await dbRef.doc("gastos/" + id).update({ valor: v, atualizado_em: new Date().toISOString() }); ok.textContent = "Salvo"; }
    catch (e) { ok.style.color = "var(--st-erro)"; ok.textContent = "Não salvou. Abra a página no app do Claude logada e tente de novo."; }
  }

  /* ---------- contador de postados ---------- */
  function renderResumo() {
    const r = RESUMO;
    $("p-dias").hidden = !(r && r.dia_ref);
    if (!r || !r.dia_ref) { $("p-atual").textContent = carregou ? "O contador diário ainda não está ligado (tarefa das 23:55)." : "Lendo o contador..."; return; }
    const ref = r.dia_ref, agoraBR = new Date(Date.now() - 3 * 3600e3).toISOString().slice(0, 10);
    const seg = s => { const d = new Date(s + "T12:00:00Z"); d.setUTCDate(d.getUTCDate() - (d.getUTCDay() + 6) % 7); return d.toISOString().slice(0, 10); };
    $("p-hoje").textContent = ref === agoraBR ? r.hoje : 0;
    $("p-semana").textContent = seg(ref) === seg(agoraBR) ? r.semana : 0;
    $("p-mes").textContent = ref.slice(0, 7) === agoraBR.slice(0, 7) ? r.mes : 0;
    $("p-atual").textContent = "Conta o que você marcou como Postei. Atualizado " + new Date(r.atualizado_em).toLocaleString("pt-BR", { timeZone: "America/Sao_Paulo", day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit" }) + ".";
    const dias = r.dias || {}, lista = [];
    for (let k = 6; k >= 0; k--) { const d = new Date(agoraBR + "T12:00:00Z"); d.setUTCDate(d.getUTCDate() - k); const id = d.toISOString().slice(0, 10); lista.push([id, dias[id] || 0]); }
    const mx = Math.max(1, ...lista.map(x => x[1]));
    $("p-dias").innerHTML = lista.map(([id, n]) => `<div class="${id === agoraBR ? "hj" : ""}"><span>${n || ""}</span><i style="height:${Math.round(n / mx * 38)}px"></i><span>${["dom", "seg", "ter", "qua", "qui", "sex", "sáb"][new Date(id + "T12:00:00Z").getUTCDay()]}</span></div>`).join("");
  }

  function quando() {
    $("quando").textContent = ESTADO && ESTADO.atualizado_em ? "estado de " + new Date(ESTADO.atualizado_em).toLocaleString("pt-BR", { timeZone: "America/Sao_Paulo", day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit" })
      : carregou ? (dbRef ? "sem estado salvo ainda" : "abra logada no app do Claude") : "lendo o estado...";
  }
  function tudo() { renderCastelo(); quando(); mapaSujo = true; if (abaAtual === "floresta") montarMapa(); }

  /* ---------- início ---------- */
  montarFixos(); montarAreas(); renderMural(); renderMetas(); renderCastelo(); renderResumo(); quando();
  JOGOS.iniciar({ $, esc, confete, ls, poucoMovimento });
  const hash = (location.hash || "").slice(1);
  aba(hash || ls.get("aba") || "castelo");
  let rz; addEventListener("resize", () => { clearTimeout(rz); rz = setTimeout(() => { mapaSujo = true; if (abaAtual === "floresta") montarMapa(); }, 160); });

  (async () => {
    const db = window.claude && window.claude.use ? await window.claude.use("db") : null;
    carregou = true;
    if (!db) { $("g-sub").textContent = "Abra logada no app do Claude para ver e salvar os valores."; tudo(); renderMural(); renderResumo(); return; }
    dbRef = db;
    db.doc("reino/estado").onSnapshot(sn => { ESTADO = sn.exists ? sn.data() : null; tudo(); }, () => tudo());
    db.doc("postagens_resumo/atual").onSnapshot(sn => { RESUMO = sn.exists ? sn.data() : null; renderResumo(); }, () => renderResumo());
    db.collection("metas").onSnapshot(snap => { METAS = snap.docs.map(d => ({ id: d.id, ...d.data() })); renderMetas(); }, () => { });
    db.collection("mural").onSnapshot(snap => { MURAL = snap.docs.map(d => ({ id: d.id, ...d.data() })); renderMural(); }, () => { });
    db.collection("gastos").onSnapshot(snap => { GASTOS = snap.docs.map(d => ({ id: d.id, ...d.data() })); renderGasto(); }, () => { $("g-sub").textContent = "Não consegui ler os valores agora."; });
  })();
})();
