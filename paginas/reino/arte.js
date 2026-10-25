/* =====================================================================
   ARTE DO REINO  (desenhos em SVG, sem dados)
   Personagens, construções, encomendas e a floresta.
   Recebe só cores e tipos vindos de tema.js. Nada aqui lê o banco.
   Os estados (trabalhando, sua vez...) mudam o desenho só por CSS:
   janelas acesas, brilho, nuvem de chuva, estrelas.
   ===================================================================== */
window.ARTE = (() => {
  const T = "var(--traco)";
  const W = 1.6;

  /* ---------- personagens ---------- */
  function cabeloTras(p) {
    const c = p.corCabelo;
    const cap = `<path d="M18.5 41 Q18 27.5 30 27.5 Q42 27.5 41.5 41 Z" fill="${c}"/>`;
    switch (p.cabelo) {
      case "coque": return `<circle cx="30" cy="26" r="6.2" fill="${c}" stroke="${T}" stroke-width="${W}"/>` + cap;
      case "trancas": return cap + `<path d="M19.5 42 Q16 51 18 61" fill="none" stroke="${c}" stroke-width="4.6" stroke-linecap="round"/><path d="M40.5 42 Q44 51 42 61" fill="none" stroke="${c}" stroke-width="4.6" stroke-linecap="round"/><circle cx="18" cy="61" r="1.8" fill="#e8a7bd"/><circle cx="42" cy="61" r="1.8" fill="#e8a7bd"/>`;
      case "rabo": return cap + `<path d="M40 33 Q51 39 47 55 Q45 46 39 42 Z" fill="${c}" stroke="${T}" stroke-width="${W}" stroke-linejoin="round"/>`;
      case "curto": return `<path d="M18 43 Q16 27 30 27 Q44 27 42 43 L42 48 Q38.5 46 38.5 41 L21.5 41 Q21.5 46 18 48 Z" fill="${c}" stroke="${T}" stroke-width="${W}" stroke-linejoin="round"/>`;
      default: return `<path d="M18.5 39 Q17 26 30 26 Q43 26 41.5 39 L44 57 Q37 59.5 30 55.5 Q23 59.5 16 57 Z" fill="${c}" stroke="${T}" stroke-width="${W}" stroke-linejoin="round"/>`;
    }
  }
  function franja(p) {
    return `<path d="M18.6 39 Q21 28 30 28.6 Q39 28 41.4 39 Q36 33.5 31 35.4 Q25.5 32.6 18.6 39 Z" fill="${p.corCabelo}" stroke="${T}" stroke-width="1.2" stroke-linejoin="round"/>`;
  }
  function chapeu(p) {
    const k = p.corChapeu || "#d8b45e";
    switch (p.chapeu) {
      case "pontudo": return `<path d="M16.5 36 Q24 31 30 31 Q36 31 43.5 36 Q39 23 35 13 Q32 6 25 7.5 Q30.5 10 30.3 15 Q24 26 16.5 36 Z" fill="${k}" stroke="${T}" stroke-width="${W}" stroke-linejoin="round"/><ellipse cx="30" cy="35.6" rx="14.3" ry="3.3" fill="${k}" stroke="${T}" stroke-width="${W}"/><circle cx="37" cy="31.5" r="1.9" fill="#fbe7a6" stroke="${T}" stroke-width=".9"/>`;
      case "coroa": return `<path d="M21.5 31 L22.5 22.5 L26.5 26.5 L30 19.5 L33.5 26.5 L37.5 22.5 L38.5 31 Z" fill="${k}" stroke="${T}" stroke-width="${W}" stroke-linejoin="round"/><circle cx="30" cy="27.5" r="1.7" fill="#e8a7bd" stroke="${T}" stroke-width=".8"/><circle cx="24" cy="28.6" r="1" fill="#fff"/><circle cx="36" cy="28.6" r="1" fill="#fff"/>`;
      case "laco": return `<path d="M36 29 L30.5 24 L31 33 Z M36 29 L42 24.5 L41 33.5 Z" fill="${k}" stroke="${T}" stroke-width="1.3" stroke-linejoin="round"/><circle cx="36" cy="29" r="2" fill="${k}" stroke="${T}" stroke-width="1.2"/>`;
      case "tiara": return `<path d="M20.5 32.5 Q30 25.5 39.5 32.5" fill="none" stroke="${k}" stroke-width="2.4" stroke-linecap="round"/><path d="M30 22.6 l1.6 3 3 .4 -2.2 2 .6 3 -3-1.5 -3 1.5 .6-3 -2.2-2 3-.4z" fill="#fff6dc" stroke="${k}" stroke-width="1"/>`;
      case "flores": {
        const pts = [[20.5, 34], [24.5, 30.2], [30, 28.8], [35.5, 30.2], [39.5, 34]];
        return pts.map(([x, y], i) => `<circle cx="${x}" cy="${y}" r="2.6" fill="${i % 2 ? "#fbf3e6" : k}" stroke="${T}" stroke-width=".9"/><circle cx="${x}" cy="${y}" r=".9" fill="#d8b45e"/>`).join("") +
          `<path d="M22 33 q2 -3 4 -2" stroke="#8fae86" stroke-width="1.2" fill="none"/>`;
      }
      default: return "";
    }
  }
  const NA_MAO = {
    prancheta: `<rect x="40.5" y="57" width="10" height="12.5" rx="1.5" fill="#c9a35b" stroke="${T}" stroke-width="${W}"/><rect x="42.2" y="59.5" width="6.6" height="8.5" fill="#fffaf2"/><path d="M43.5 62h4M43.5 64.5h4M43.5 67h2.5" stroke="#b9a4d8" stroke-width=".9"/><rect x="43.5" y="56" width="4" height="2.4" rx=".8" fill="#9f86c8" stroke="${T}" stroke-width=".8"/>`,
    livro: `<g class="brilho-suave"><path d="M39.5 61 l6 -2.5 6 2.5 v8 l-6 -2.5 -6 2.5z" fill="#9f86c8" stroke="${T}" stroke-width="${W}" stroke-linejoin="round"/><path d="M45.5 58.5 v8" stroke="${T}" stroke-width="1"/><path d="M50 54 l.8 1.6 1.6.3 -1.2 1.1 .3 1.6 -1.5-.8 -1.5.8 .3-1.6 -1.2-1.1 1.6-.3z" fill="#f2d27a"/></g>`,
    camera: `<rect x="39" y="59" width="13" height="9" rx="2.2" fill="#5a4652" stroke="${T}" stroke-width="${W}"/><circle cx="45.5" cy="63.5" r="3.1" fill="#cfe3f2" stroke="#fff" stroke-width="1.1"/><rect x="40.5" y="57.5" width="4" height="2" rx=".6" fill="#e8a7bd"/><circle class="flash" cx="49.8" cy="60.6" r="1" fill="#fff6dc"/>`,
    varinha: `<path d="M45.5 66 L54 52" stroke="#c9a35b" stroke-width="2" stroke-linecap="round"/><path class="brilho" d="M54.5 46.5 l1.6 3.2 3.4.5 -2.5 2.3 .6 3.4 -3.1-1.6 -3.1 1.6 .6-3.4 -2.5-2.3 3.4-.5z" fill="#fbe7a6" stroke="#c9a35b" stroke-width="1"/>`,
    lupa: `<path d="M46 66 L49.5 61" stroke="#8a6146" stroke-width="2.6" stroke-linecap="round"/><circle cx="51.5" cy="57.5" r="5" fill="rgba(214,232,245,.75)" stroke="#c9a35b" stroke-width="2"/><path d="M49.3 55.6 q1.2-1.4 2.8-1.2" stroke="#fff" stroke-width="1.1" fill="none"/>`,
    cartas: `<rect x="39.5" y="59.5" width="12" height="8.5" rx="1" fill="#fffaf2" stroke="${T}" stroke-width="${W}"/><path d="M39.8 60 l5.7 4.4 5.7 -4.4" fill="none" stroke="${T}" stroke-width="1"/><path d="M45.5 64.6 c-.9-1.1-2.3-.3-1.5.8 l1.5 1.3 1.5-1.3 c.8-1.1-.6-1.9-1.5-.8z" fill="#e8a7bd"/>`,
    cristal: `<path class="brilho-suave" d="M47.5 51 l4 4.5 -4 9 -4 -9 z" fill="#d9ccf0" stroke="#9f86c8" stroke-width="1.3" stroke-linejoin="round"/><path d="M47.5 51 v13.5 M43.5 55.5 h8" stroke="#fff" stroke-width=".7" opacity=".8"/>`,
    moeda: `<circle cx="47.5" cy="62" r="5" fill="#e9c77b" stroke="#a9853d" stroke-width="1.6"/><circle cx="47.5" cy="62" r="3" fill="none" stroke="#fbe7a6" stroke-width="1"/><path d="M46.6 60.5 h2 M46.2 62.2 h2.6" stroke="#a9853d" stroke-width=".9"/>`,
    tesoura: `<circle cx="44" cy="66" r="2.2" fill="none" stroke="#c97f95" stroke-width="1.5"/><circle cx="48.6" cy="66.6" r="2.2" fill="none" stroke="#c97f95" stroke-width="1.5"/><path d="M45.2 64.4 L52 55.5 M47.6 64.8 L49.5 54.8" stroke="#a8a3b3" stroke-width="1.6" stroke-linecap="round"/>`,
    lanterna: `<path d="M45.5 66 v3" stroke="${T}" stroke-width="1.1"/><path d="M42.5 69.5 h6 l1 2 v6 l-1 1.5 h-6 l-1-1.5 v-6z" fill="#c9a35b" stroke="${T}" stroke-width="1.3" stroke-linejoin="round"/><rect class="chama" x="43.5" y="72" width="4" height="5" rx="1.6" fill="#fbe7a6"/>`,
    claquete: `<rect x="39" y="61" width="13" height="8" rx="1" fill="#4a3b46" stroke="${T}" stroke-width="${W}"/><path class="claque" d="M39 61 l12.6 -3.6 1 3.2 L39.4 61z" fill="#fffaf2" stroke="${T}" stroke-width="1.1"/><path d="M42 59.6 l1.2 1.4 M45.5 58.6 l1.2 1.5 M49 57.6 l1.2 1.5" stroke="#4a3b46" stroke-width="1.1"/>`,
    espelho: `<path d="M46 67 L47.5 62.5" stroke="#c9a35b" stroke-width="2.2" stroke-linecap="round"/><ellipse cx="49" cy="56.5" rx="4.2" ry="5.4" fill="#e6effa" stroke="#c9a35b" stroke-width="1.8"/><path class="brilho-suave" d="M47.4 54 q1-1.6 2.4-1.6" stroke="#fff" stroke-width="1.2" fill="none"/>`,
    luneta: `<path d="M42.5 64 L55 55.5" stroke="#c9a35b" stroke-width="4" stroke-linecap="round"/><path d="M50.5 58.5 L55 55.5" stroke="#8a6146" stroke-width="4.6" stroke-linecap="round"/><circle cx="55.6" cy="55.1" r="1.5" fill="#cfe3f2"/>`,
    grafico: `<rect x="39" y="56.5" width="13" height="11" rx="1.5" fill="#fffaf2" stroke="${T}" stroke-width="${W}"/><rect x="41" y="62.5" width="2.3" height="3.5" fill="#a8bfa0"/><rect x="44.4" y="60.2" width="2.3" height="5.8" fill="#e8a7bd"/><rect x="47.8" y="58.2" width="2.3" height="7.8" fill="#9f86c8"/>`,
    frasco: `<path d="M45 52.5 h4.6 v3.6 l4 7.4 q1 2.6-1.8 2.6 h-9 q-2.8 0-1.8-2.6 l4-7.4z" fill="rgba(240,250,246,.8)" stroke="${T}" stroke-width="1.4" stroke-linejoin="round"/><path d="M42.6 61.5 h9.4 l1.6 2.6 q.7 1.6-1.3 1.6 h-9.8 q-2 0-1.4-1.6z" fill="#e8a7bd"/><circle class="bolha" cx="47.5" cy="58.5" r=".9" fill="#e8a7bd"/><circle class="bolha b2" cx="49" cy="56" r=".7" fill="#b9a4d8"/>`,
    trofeu: `<path d="M42.5 56 h9 v3 a4.5 4.5 0 0 1-9 0z" fill="#e9c77b" stroke="#a9853d" stroke-width="1.4"/><path d="M42.5 57 h-2 a2 2 0 0 0 2.3 3 M51.5 57 h2 a2 2 0 0 1-2.3 3" fill="none" stroke="#a9853d" stroke-width="1.1"/><rect x="45.8" y="63" width="2.4" height="2.6" fill="#e9c77b"/><rect x="43.6" y="65.4" width="6.8" height="2.4" rx=".8" fill="#c97f95" stroke="#a9853d" stroke-width=".9"/>`
  };
  const NO_CORPO = {
    oculos: `<circle cx="26" cy="41.6" r="3.3" fill="rgba(255,255,255,.28)" stroke="#6b4a3a" stroke-width="1.2"/><circle cx="34" cy="41.6" r="3.3" fill="rgba(255,255,255,.28)" stroke="#6b4a3a" stroke-width="1.2"/><path d="M29.3 41.4 h1.4" stroke="#6b4a3a" stroke-width="1.1"/>`,
    bolsa: `<path d="M23 52.5 L39 66" stroke="#8a6146" stroke-width="1.6"/><rect x="34.5" y="63" width="10" height="7.5" rx="2" fill="#b98962" stroke="${T}" stroke-width="1.3"/><path d="M34.5 65.5 h10" stroke="${T}" stroke-width="1"/><circle cx="39.5" cy="66.6" r=".9" fill="#d8b45e"/>`,
    fones: `<path d="M17.5 41 Q17.5 25 30 25 Q42.5 25 42.5 41" fill="none" stroke="#c97f95" stroke-width="2.4"/><rect x="15" y="37.5" width="5" height="8" rx="2.2" fill="#e8a7bd" stroke="${T}" stroke-width="1.2"/><rect x="40" y="37.5" width="5" height="8" rx="2.2" fill="#e8a7bd" stroke="${T}" stroke-width="1.2"/>`
  };

  function personagem(p, tam) {
    tam = tam || 56;
    if (p.tipo === "coruja") return coruja(p, tam);
    const ac = String(p.acessorio || "").split("+");
    const mao = ac.map(a => NA_MAO[a] || "").join("");
    const corpoAtras = ac.filter(a => a === "bolsa").map(a => NO_CORPO[a]).join("");
    const corpoFrente = ac.filter(a => a !== "bolsa").map(a => NO_CORPO[a] || "").join("");
    const fada = p.tipo === "fada", elfa = p.tipo === "elfa";
    return `<svg class="pers-svg" viewBox="0 0 60 84" width="${tam}" height="${Math.round(tam * 1.4)}" aria-hidden="true"><g class="pers">
      <ellipse cx="30" cy="81" rx="14" ry="2.6" fill="#3b2633" opacity=".16"/>
      ${fada ? `<g class="asas"><path d="M24 55 C9 39 2 58 13 65 C18 68 22 63 24.5 59Z" fill="rgba(226,214,248,.78)" stroke="#b9a4d8" stroke-width="1.2"/><path d="M36 55 C51 39 58 58 47 65 C42 68 38 63 35.5 59Z" fill="rgba(226,214,248,.78)" stroke="#b9a4d8" stroke-width="1.2"/><path d="M22 58 C14 62 14 72 21 70Z M38 58 C46 62 46 72 39 70Z" fill="rgba(248,214,226,.7)" stroke="#e8a7bd" stroke-width="1"/></g>` : ""}
      ${cabeloTras(p)}
      <path d="M21 53 Q30 48.5 39 53 L44.5 76 Q30 80.5 15.5 76 Z" fill="${p.roupa}" stroke="${T}" stroke-width="${W}" stroke-linejoin="round"/>
      <path d="M19.2 66 Q30 69.5 40.8 66" fill="none" stroke="#fffaf2" stroke-width="1.3" opacity=".7"/>
      <path d="M24 53.5 Q30 57 36 53.5" fill="none" stroke="#fffaf2" stroke-width="1.6" opacity=".85"/>
      <ellipse cx="25" cy="78.4" rx="3.4" ry="1.8" fill="#6b4a3a"/><ellipse cx="35" cy="78.4" rx="3.4" ry="1.8" fill="#6b4a3a"/>
      <path d="M22.5 56 Q16 61.5 17 68" fill="none" stroke="${p.roupa}" stroke-width="4.6" stroke-linecap="round"/><path d="M22.5 56 Q16 61.5 17 68" fill="none" stroke="${T}" stroke-width=".9" opacity=".35"/>
      <circle cx="17" cy="69" r="2.5" fill="${p.pele}" stroke="${T}" stroke-width="1"/>
      ${corpoAtras}
      <g class="braco-d"><path d="M37.5 56 Q44 60.5 45 66" fill="none" stroke="${p.roupa}" stroke-width="4.6" stroke-linecap="round"/><circle cx="45.4" cy="67" r="2.5" fill="${p.pele}" stroke="${T}" stroke-width="1"/>${mao}</g>
      ${elfa ? `<path d="M19 39.5 L11.5 32.5 L19.6 44.5 Z M41 39.5 L48.5 32.5 L40.4 44.5 Z" fill="${p.pele}" stroke="${T}" stroke-width="1.3" stroke-linejoin="round"/>` : ""}
      <circle cx="30" cy="40.5" r="11.6" fill="${p.pele}" stroke="${T}" stroke-width="${W}"/>
      <g class="olhos"><ellipse cx="26" cy="41.8" rx="1.65" ry="2.1" fill="#3b2633"/><ellipse cx="34" cy="41.8" rx="1.65" ry="2.1" fill="#3b2633"/><circle cx="26.6" cy="41" r=".65" fill="#fff"/><circle cx="34.6" cy="41" r=".65" fill="#fff"/></g>
      <path d="M24 39.2 l-1.2 -1 M35.9 39.2 l1.2 -1" stroke="#3b2633" stroke-width=".9" stroke-linecap="round"/>
      <ellipse cx="23.3" cy="45.4" rx="2.4" ry="1.4" fill="#f29fb0" opacity=".7"/><ellipse cx="36.7" cy="45.4" rx="2.4" ry="1.4" fill="#f29fb0" opacity=".7"/>
      <path d="M28 46.6 Q30 48.6 32 46.6" fill="none" stroke="#a14d63" stroke-width="1.2" stroke-linecap="round"/>
      ${p.cabelo === "curto" ? "" : franja(p)}
      ${corpoFrente}
      ${chapeu(p)}
      <g class="zz"><text x="44" y="26" font-size="7" font-weight="900" fill="#9f86c8" font-family="Nunito,system-ui,sans-serif">z</text><text x="49" y="19" font-size="5.5" font-weight="900" fill="#9f86c8" font-family="Nunito,system-ui,sans-serif">z</text></g>
    </g></svg>`;
  }
  function coruja(p, tam) {
    const c = p.roupa || "#b89a7a";
    return `<svg class="pers-svg" viewBox="0 0 60 84" width="${tam}" height="${Math.round(tam * 1.4)}" aria-hidden="true"><g class="pers">
      <ellipse cx="30" cy="81" rx="14" ry="2.6" fill="#3b2633" opacity=".16"/>
      <path d="M17 36 L15 24 L24 31 Z M43 36 L45 24 L36 31 Z" fill="${c}" stroke="${T}" stroke-width="${W}" stroke-linejoin="round"/>
      <path d="M30 28 C46 28 47 50 44 64 C42 75 18 75 16 64 C13 50 14 28 30 28 Z" fill="${c}" stroke="${T}" stroke-width="${W}"/>
      <path d="M30 50 C39 50 40 62 38 68 C35 73 25 73 22 68 C20 62 21 50 30 50 Z" fill="#f4e6d4"/>
      <path d="M25 58 q2 1.6 4 0 M31 58 q2 1.6 4 0 M27 64 q2 1.6 4 0 M33 64 q2 1.6 4 0" stroke="#d6bfa3" stroke-width="1" fill="none"/>
      <g class="olhos"><circle cx="24" cy="40" r="6.2" fill="#fffaf2" stroke="${T}" stroke-width="1.2"/><circle cx="36" cy="40" r="6.2" fill="#fffaf2" stroke="${T}" stroke-width="1.2"/><circle cx="24.5" cy="40.5" r="3" fill="#3b2633"/><circle cx="35.5" cy="40.5" r="3" fill="#3b2633"/><circle cx="25.4" cy="39.4" r="1" fill="#fff"/><circle cx="36.4" cy="39.4" r="1" fill="#fff"/></g>
      <path d="M28 46 L30 50 L32 46 Z" fill="#e9c77b" stroke="${T}" stroke-width="1" stroke-linejoin="round"/>
      <path d="M36.5 30 l5 -4 0 7z M36.5 30 l-1 -5 5 2z" fill="${p.corChapeu || "#e8a7bd"}" stroke="${T}" stroke-width="1"/>
      <path d="M16 52 C10 58 12 66 18 66" fill="${c}" stroke="${T}" stroke-width="${W}"/>
      <g class="braco-d"><path d="M44 52 C50 56 50 63 44 66" fill="${c}" stroke="${T}" stroke-width="${W}"/>${NA_MAO[p.acessorio] ? `<g transform="translate(2 4)">${NA_MAO[p.acessorio]}</g>` : ""}</g>
      <path d="M25 74 v4 M28 74 v4 M32 74 v4 M35 74 v4" stroke="#e9c77b" stroke-width="1.6" stroke-linecap="round"/>
      <g class="zz"><text x="44" y="26" font-size="7" font-weight="900" fill="#9f86c8" font-family="Nunito,system-ui,sans-serif">z</text></g>
    </g></svg>`;
  }

  /* ---------- construções ---------- */
  const jan = (x, y, w, h, arco) => `<rect class="jan" x="${x}" y="${y}" width="${w}" height="${h}" rx="${arco ? w / 2 : 1.5}" stroke="${T}" stroke-width="${W}"/><path d="M${x + w / 2} ${y + (arco ? 2 : 0)} V${y + h} M${x} ${y + h * .58} H${x + w}" stroke="${T}" stroke-width="1" opacity=".55"/>`;
  const janRed = (cx, cy, r) => `<circle class="jan" cx="${cx}" cy="${cy}" r="${r}" stroke="${T}" stroke-width="${W}"/><path d="M${cx - r} ${cy} H${cx + r} M${cx} ${cy - r} V${cy + r}" stroke="${T}" stroke-width="1" opacity=".55"/>`;
  const porta = (x, y, w, h, c) => `<path d="M${x} ${y + h} V${y + w / 2} a${w / 2} ${w / 2} 0 0 1 ${w} 0 V${y + h} Z" fill="${c || "#a67a5b"}" stroke="${T}" stroke-width="${W}"/><path d="M${x + w / 2} ${y + 2} V${y + h}" stroke="${T}" stroke-width=".9" opacity=".4"/><circle cx="${x + w * .74}" cy="${y + h * .62}" r="1.1" fill="#e9c77b"/>`;
  const chao = `<ellipse cx="60" cy="98" rx="50" ry="6.5" fill="var(--relva-2)"/>`;
  const flor = (x, y, c) => `<circle cx="${x}" cy="${y}" r="2.4" fill="${c}" stroke="${T}" stroke-width=".7"/><circle cx="${x}" cy="${y}" r=".8" fill="#f2d27a"/>`;
  const flores = (lista) => lista.map(([x, y, c]) => flor(x, y, c)).join("");
  const pintas = (lista) => lista.map(([x, y, r]) => `<ellipse cx="${x}" cy="${y}" rx="${r}" ry="${r * .8}" fill="#fffaf2" opacity=".9"/>`).join("");
  const cone = (x1, y, x2, topo, c) => `<path d="M${x1} ${y} Q${(x1 + x2) / 2} ${topo - 6} ${(x1 + x2) / 2} ${topo} Q${(x1 + x2) / 2} ${topo - 6} ${x2} ${y} Z" fill="${c}" stroke="${T}" stroke-width="${W}" stroke-linejoin="round"/>`;
  const conePonta = (x1, y, x2, topo, c) => `<path d="M${x1 - 2} ${y} L${(x1 + x2) / 2} ${topo} L${x2 + 2} ${y} Q${(x1 + x2) / 2} ${y + 4} ${x1 - 2} ${y} Z" fill="${c}" stroke="${T}" stroke-width="${W}" stroke-linejoin="round"/>`;
  const bandeira = (x, y, c) => `<path d="M${x} ${y} v-12" stroke="${T}" stroke-width="1.2"/><path class="bandeira" d="M${x} ${y - 12} l9 2.6 -9 2.6z" fill="${c}" stroke="${T}" stroke-width="1"/>`;
  const pedras = (x, y, w, h) => { let s = ""; for (let j = 0; j < h; j += 8) for (let i = (j / 8) % 2 ? 4 : 0; i < w; i += 9) s += `<path d="M${x + i + 1} ${y + j + 4} h6" stroke="${T}" stroke-width=".8" opacity=".22"/>`; return s; };
  const cogumeloCasa = (x, y, s, c) => `<g transform="translate(${x} ${y}) scale(${s})">
      <path d="M-11 0 V-16 Q-11 -20 -7 -20 H7 Q11 -20 11 -16 V0 Z" fill="${c.parede}" stroke="${T}" stroke-width="${W / s}"/>
      ${porta(-4, -12, 8, 12, "#a67a5b")}
      <path d="M-20 -17 Q-19 -40 0 -41 Q19 -40 20 -17 Q0 -12 -20 -17 Z" fill="${c.telhado}" stroke="${T}" stroke-width="${W / s}" stroke-linejoin="round"/>
      ${pintas([[-10, -28, 3], [3, -34, 2.6], [11, -24, 2.2], [-2, -24, 1.6]])}
      <circle class="jan" cx="7.2" cy="-10" r="2.6" stroke="${T}" stroke-width="${1.2 / s}"/>
    </g>`;

  const PREDIOS = {
    casinha: c => `${chao}<rect x="32" y="52" width="56" height="44" rx="3" fill="${c.parede}" stroke="${T}" stroke-width="${W}"/>${porta(52, 70, 16, 26)}${jan(37, 62, 11, 13, true)}${jan(72, 62, 11, 13, true)}
      <path d="M22 57 Q24 20 60 18 Q96 20 98 57 Q60 63 22 57 Z" fill="${c.telhado}" stroke="${T}" stroke-width="${W}" stroke-linejoin="round"/>${pintas([[40, 36, 5], [62, 28, 4], [80, 40, 4.4], [56, 46, 2.6]])}
      ${flores([[28, 95, c.detalhe], [92, 94, "#fbf3e6"], [96, 97, c.detalhe]])}`,

    portal: c => `${chao}<path class="portal-luz" d="M40 96 V62 a20 20 0 0 1 40 0 V96 Z" fill="${c.parede}"/>
      <g class="espiral"><path d="M60 78 m-1 0 a2 2 0 1 1 3 1 a5 5 0 1 1 -7 -4 a9 9 0 1 1 13 7 a13 13 0 1 1 -19 -9" fill="none" stroke="#fffaf2" stroke-width="1.8" stroke-linecap="round" opacity=".85"/></g>
      <path d="M30 97 V62 a30 30 0 0 1 60 0 V97 H80 V62 a20 20 0 0 0 -40 0 V97 Z" fill="#d9cfc4" stroke="${T}" stroke-width="${W}" stroke-linejoin="round"/>
      <path d="M33 70 h6 M81 70 h6 M33 84 h6 M81 84 h6 M36 48 l5 3 M84 48 l-5 3 M50 35 l2 5 M70 35 l-2 5 M60 32 v6" stroke="${T}" stroke-width="1" opacity=".35"/>
      <path d="M28 96 C24 80 30 60 38 46 C44 36 54 30 60 31" fill="none" stroke="#6f8f63" stroke-width="2" stroke-linecap="round"/>
      <path d="M92 96 C96 82 90 62 84 50" fill="none" stroke="#6f8f63" stroke-width="2" stroke-linecap="round"/>
      ${flores([[30, 82, c.detalhe], [33, 64, "#fbf3e6"], [40, 47, c.detalhe], [52, 33, c.telhado], [90, 80, c.detalhe], [88, 62, "#fbf3e6"]])}
      <circle cx="60" cy="32" r="3.6" fill="#e9c77b" stroke="${T}" stroke-width="1.2"/>`,

    vila: c => `${chao}${cogumeloCasa(32, 96, .9, c)}${cogumeloCasa(84, 94, .78, { parede: c.parede, telhado: "#b9a4d8" })}${cogumeloCasa(60, 99, 1.12, c)}
      <path d="M8 97 q4 -6 8 0 M104 96 q4 -5 8 0" stroke="#6f8f63" stroke-width="1.6" fill="none"/>${flores([[14, 93, c.detalhe], [108, 92, "#fbf3e6"]])}`,

    castelo: c => `${chao}<rect x="38" y="44" width="44" height="52" fill="${c.parede}" stroke="${T}" stroke-width="${W}"/>
      <path d="M38 44 v-6 h6 v6 h5 v-6 h6 v6 h5 v-6 h6 v6 h5 v-6 h7 v6" fill="${c.parede}" stroke="${T}" stroke-width="${W}" stroke-linejoin="round"/>
      <rect x="16" y="36" width="22" height="60" rx="2" fill="${c.parede}" stroke="${T}" stroke-width="${W}"/><rect x="82" y="36" width="22" height="60" rx="2" fill="${c.parede}" stroke="${T}" stroke-width="${W}"/>
      ${pedras(18, 40, 18, 52)}${pedras(84, 40, 18, 52)}
      ${conePonta(16, 38, 38, 6, c.telhado)}${conePonta(82, 38, 104, 6, c.telhado)}${bandeira(27, 6, c.detalhe)}${bandeira(93, 6, "#b9a4d8")}
      ${porta(51, 70, 18, 26, "#8a6146")}${jan(21, 52, 10, 14, true)}${jan(89, 52, 10, 14, true)}${jan(44, 52, 9, 11, true)}${jan(67, 52, 9, 11, true)}
      <path d="M54 66 h12" stroke="${c.detalhe}" stroke-width="2.2"/><circle cx="60" cy="47" r="3" fill="${c.detalhe}" stroke="${T}" stroke-width="1"/>
      ${flores([[12, 95, "#e8a7bd"], [108, 95, "#fbf3e6"], [46, 97, "#e8a7bd"]])}`,

    torre: c => `${chao}<path d="M42 96 V34 Q60 30 78 34 V96 Z" fill="${c.parede}" stroke="${T}" stroke-width="${W}"/>${pedras(44, 38, 32, 56)}
      ${cone(36, 36, 84, 2, c.telhado)}<circle cx="60" cy="4" r="2.2" fill="#e9c77b" stroke="${T}" stroke-width="1"/>
      ${jan(54, 42, 12, 15, true)}<path d="M38 66 h44 v4 h-44z" fill="#a67a5b" stroke="${T}" stroke-width="1.3"/><path d="M40 66 v-5 M48 66 v-5 M56 66 v-5 M64 66 v-5 M72 66 v-5 M80 66 v-5 M38 61 h44" stroke="${T}" stroke-width="1.1"/>
      ${porta(53, 76, 14, 20)}${flores([[36, 94, c.detalhe], [86, 95, "#fbf3e6"], [90, 92, c.detalhe]])}
      <path d="M78 50 q10 4 6 16" stroke="#6f8f63" stroke-width="1.8" fill="none"/>${flor(84, 58, c.detalhe)}`,

    biblioteca: c => `${chao}<path d="M36 97 C40 88 40 70 42 52 H78 C80 70 80 88 84 97 Z" fill="${c.parede}" stroke="${T}" stroke-width="${W}" stroke-linejoin="round"/>
      <path d="M46 60 q2 14 0 30 M72 58 q-2 16 0 32 M58 54 v8" stroke="${T}" stroke-width=".9" opacity=".3" fill="none"/>
      <path d="M26 97 q6 -4 14 -2 M94 97 q-6 -4 -14 -2" stroke="${c.parede}" stroke-width="4" stroke-linecap="round"/>
      <g fill="${c.telhado}" stroke="${T}" stroke-width="${W}"><circle cx="40" cy="44" r="17"/><circle cx="80" cy="44" r="17"/><circle cx="60" cy="32" r="22"/><circle cx="60" cy="50" r="15"/></g>
      <path d="M44 38 q4-4 8-2 M70 30 q4-3 8 0" stroke="#fffaf2" stroke-width="1.4" opacity=".5" fill="none"/>
      ${porta(53, 74, 14, 23, "#7c5640")}${janRed(47, 66, 4.6)}${janRed(73, 66, 4.6)}
      <path d="M81 76 h12 v9 h-12z" fill="#f4e6d4" stroke="${T}" stroke-width="1.2"/><path d="M84 79 h6 M84 82 h4" stroke="${c.detalhe}" stroke-width="1.2"/><path d="M87 76 v-5" stroke="${T}" stroke-width="1"/>
      ${flores([[30, 96, c.detalhe], [100, 95, "#fbf3e6"]])}${flor(48, 30, c.detalhe)}${flor(72, 24, "#fbf3e6")}${flor(84, 48, c.detalhe)}`,

    atelie: c => `${chao}<rect x="28" y="56" width="64" height="40" rx="3" fill="${c.parede}" stroke="${T}" stroke-width="${W}"/>
      <path d="M22 59 L60 26 L98 59 Z" fill="${c.telhado}" stroke="${T}" stroke-width="${W}" stroke-linejoin="round"/>
      <path d="M44 52 L60 38 L76 52 Z" fill="rgba(207,227,242,.85)" stroke="${T}" stroke-width="1.3" stroke-linejoin="round"/><path d="M60 38 V52 M52 45 L68 45" stroke="${T}" stroke-width=".9" opacity=".6"/>
      ${porta(53, 72, 14, 24)}${jan(34, 66, 13, 12)}${jan(73, 66, 13, 12)}
      <path d="M96 96 l4 -20 M108 96 l-4 -20 M98 84 h8" stroke="#8a6146" stroke-width="1.6"/><rect x="94" y="66" width="16" height="12" fill="#fffaf2" stroke="${T}" stroke-width="1.2"/><path d="M96 76 l4 -5 3 3 2 -2 3 4z" fill="${c.telhado}"/><circle cx="105.5" cy="69.5" r="1.4" fill="#f2d27a"/>
      ${flores([[22, 95, c.telhado], [30, 97, "#fbf3e6"]])}`,

    estufa: c => `${chao}<path d="M24 96 V64 Q24 30 60 30 Q96 30 96 64 V96 Z" fill="${c.parede}" fill-opacity=".72" stroke="${T}" stroke-width="${W}"/>
      <path d="M60 30 V96 M42 33.5 Q36 60 38 96 M78 33.5 Q84 60 82 96 M24 64 H96 M27 47 H93" stroke="${T}" stroke-width="1" opacity=".45" fill="none"/>
      <g fill="${c.telhado}" stroke="${T}" stroke-width="1"><circle cx="34" cy="86" r="8"/><circle cx="86" cy="86" r="8"/><circle cx="46" cy="90" r="6"/><circle cx="76" cy="90" r="6"/></g>
      ${flores([[34, 80, c.detalhe], [30, 88, "#fbf3e6"], [86, 80, c.detalhe], [90, 88, "#f2d27a"], [46, 86, "#fbf3e6"], [76, 86, c.detalhe]])}
      ${porta(53, 74, 14, 22, "#a8bfa0")}<path d="M60 30 v-6" stroke="${T}" stroke-width="1.4"/><circle cx="60" cy="22" r="3" fill="#e9c77b" stroke="${T}" stroke-width="1.1"/>
      <path class="reflexo" d="M34 54 q6 -14 18 -18" stroke="#fff" stroke-width="2" fill="none" opacity=".7"/>`,

    cinema: c => `${chao}<rect x="26" y="54" width="68" height="42" fill="${c.parede}" stroke="${T}" stroke-width="${W}"/>
      <path d="M20 56 L60 20 L100 56 Z" fill="#fbf3e6" stroke="${T}" stroke-width="${W}" stroke-linejoin="round"/>
      <path d="M60 20 L28 56 H36 Z M60 20 L44 56 H52 Z M60 20 L60 56 H68 Z M60 20 L76 56 H84 Z M60 20 L92 56 H100 Z" fill="${c.telhado}" opacity=".9"/>
      <path d="M20 56 q5 6 10 0 q5 6 10 0 q5 6 10 0 q5 6 10 0 q5 6 10 0 q5 6 10 0 q5 6 10 0 q5 6 10 0" fill="${c.telhado}" stroke="${T}" stroke-width="1.3"/>
      <rect x="34" y="64" width="52" height="12" rx="3" fill="#4a3b46" stroke="${T}" stroke-width="1.3"/>
      <g class="luzes">${[38, 45, 52, 59, 66, 73, 80].map((x, i) => `<circle class="luz l${i % 3}" cx="${x + 1}" cy="70" r="1.8" fill="${c.detalhe}"/>`).join("")}</g>
      <path d="M48 96 V84 a12 12 0 0 1 24 0 V96Z" fill="#9f86c8" stroke="${T}" stroke-width="${W}"/><path d="M60 72 V96" stroke="${T}" stroke-width="1" opacity=".4"/>
      <path d="M60 20 v-8" stroke="${T}" stroke-width="1.3"/><path class="brilho" d="M60 5 l1.6 3.2 3.4.5 -2.5 2.3 .6 3.4 -3.1-1.6 -3.1 1.6 .6-3.4 -2.5-2.3 3.4-.5z" fill="#f2d27a" stroke="${T}" stroke-width=".9"/>`,

    inspecao: c => `${chao}<path d="M40 96 V40 H80 V96 Z" fill="${c.parede}" stroke="${T}" stroke-width="${W}"/>${pedras(42, 44, 36, 50)}
      <path d="M34 42 Q34 12 60 10 Q86 12 86 42 Z" fill="${c.telhado}" stroke="${T}" stroke-width="${W}"/>
      <circle cx="60" cy="30" r="11" fill="#fbf3e6" stroke="${T}" stroke-width="${W}"/><circle class="jan" cx="60" cy="30" r="7.5" stroke="${T}" stroke-width="1.2"/><circle class="pupila" cx="60" cy="30" r="3" fill="#4a3b46"/><circle cx="61.2" cy="28.8" r="1" fill="#fff"/>
      ${jan(53, 50, 14, 14, true)}${porta(53, 74, 14, 22)}
      <circle cx="47" cy="60" r="4" fill="#fbf3e6" stroke="${T}" stroke-width="1.1"/><path d="M47 60 v-2.6 M47 60 h2" stroke="${T}" stroke-width=".9"/>
      ${flores([[34, 95, "#e8a7bd"], [86, 95, "#fbf3e6"]])}`,

    salao: c => `${chao}<rect x="14" y="58" width="92" height="38" rx="3" fill="${c.parede}" stroke="${T}" stroke-width="${W}"/>
      <path d="M8 62 Q12 34 38 32 Q60 32 62 52 Q64 32 86 32 Q110 34 112 62 Q60 68 8 62 Z" fill="${c.telhado}" stroke="${T}" stroke-width="${W}" stroke-linejoin="round"/>${pintas([[26, 46, 3.6], [44, 40, 3], [80, 42, 3.4], [98, 48, 3]])}
      <rect x="20" y="64" width="80" height="7" fill="#4a3b46"/>${[24, 34, 44, 54, 64, 74, 84, 94].map(x => `<rect x="${x}" y="65.4" width="4" height="4.2" rx=".6" fill="${c.detalhe}"/>`).join("")}
      ${jan(22, 76, 12, 12)}${jan(86, 76, 12, 12)}${porta(52, 74, 16, 22)}
      ${flores([[10, 95, c.detalhe], [110, 95, "#fbf3e6"]])}`,

    espelho: c => `${chao}<path d="M42 97 h36 l-4 -8 h-28 z" fill="#d9cfc4" stroke="${T}" stroke-width="${W}"/>
      <ellipse cx="60" cy="54" rx="24" ry="33" fill="${c.telhado}" stroke="${T}" stroke-width="${W}"/>
      <ellipse class="vidro" cx="60" cy="54" rx="18" ry="27" fill="#e6effa" stroke="${T}" stroke-width="1.2"/>
      <path class="reflexo" d="M50 40 q4 -10 12 -12 M48 52 q2 -6 6 -9" stroke="#fff" stroke-width="2.2" fill="none" stroke-linecap="round"/>
      <path d="M60 18 l3 -6 3 6 -3 3z" fill="${c.detalhe}" stroke="${T}" stroke-width="1"/>
      <g fill="${c.detalhe}" stroke="${T}" stroke-width=".9"><circle cx="38" cy="38" r="4"/><circle cx="35" cy="52" r="3.4"/><circle cx="38" cy="66" r="4"/><circle cx="82" cy="38" r="4"/><circle cx="85" cy="52" r="3.4"/><circle cx="82" cy="66" r="4"/></g>
      ${flores([[36, 45, "#fbf3e6"], [84, 45, "#fbf3e6"], [37, 59, "#fbf3e6"], [83, 59, "#fbf3e6"]])}
      <path d="M38 80 q-6 6 -4 16 M82 80 q6 6 4 16" stroke="#6f8f63" stroke-width="1.8" fill="none"/>${flores([[30, 95, c.detalhe], [90, 95, c.detalhe]])}`,

    correio: c => `${chao}<rect x="28" y="56" width="58" height="40" rx="3" fill="${c.parede}" stroke="${T}" stroke-width="${W}"/>
      <path d="M22 60 L57 28 L92 60 Z" fill="${c.telhado}" stroke="${T}" stroke-width="${W}" stroke-linejoin="round"/>
      <path d="M57 28 v-10" stroke="${T}" stroke-width="1.3"/><path class="brilho" d="M57 6 l2 4 4.4.6 -3.2 3 .8 4.4 -4 -2.1 -4 2.1 .8-4.4 -3.2-3 4.4-.6z" fill="#f2d27a" stroke="${T}" stroke-width="1"/>
      ${porta(50, 72, 14, 24)}${jan(34, 66, 11, 12, true)}${jan(70, 66, 11, 12, true)}
      <path d="M100 96 V74" stroke="#8a6146" stroke-width="2.4"/><path d="M92 74 h16 v-6 a8 8 0 0 0 -16 0 z" fill="${c.telhado}" stroke="${T}" stroke-width="1.3"/>
      <rect x="95" y="66" width="10" height="7" rx="1" fill="#fffaf2" stroke="${T}" stroke-width="1"/><path d="M95.3 66.4 l4.7 3.4 4.7 -3.4" fill="none" stroke="${T}" stroke-width=".8"/><path d="M108 68 v-6 h4 l-1 2 1 2 h-4" fill="${c.detalhe}" stroke="${T}" stroke-width=".8"/>
      ${flores([[22, 95, "#e8a7bd"], [30, 97, "#fbf3e6"]])}`,

    observatorio: c => `${chao}<rect x="32" y="60" width="56" height="36" rx="2" fill="${c.parede}" stroke="${T}" stroke-width="${W}"/>${pedras(34, 64, 52, 30)}
      <path d="M30 61 a30 30 0 0 1 60 0 Z" fill="${c.telhado}" stroke="${T}" stroke-width="${W}"/>
      <path d="M56 33 h8 l3 28 h-14 z" fill="#4a3b46" opacity=".75"/>
      <g class="luneta-grande"><path d="M62 46 L88 22" stroke="#c9a35b" stroke-width="7" stroke-linecap="round"/><path d="M82 27 L90 20" stroke="#8a6146" stroke-width="8" stroke-linecap="round"/><circle cx="91" cy="19" r="2.6" fill="#cfe3f2" stroke="${T}" stroke-width="1"/></g>
      ${porta(53, 76, 14, 20)}${jan(38, 70, 10, 12, true)}${jan(72, 70, 10, 12, true)}
      <g class="estrelinhas"><path d="M24 30 l1 2 2 .3 -1.5 1.4 .4 2 -1.9-1 -1.9 1 .4-2 -1.5-1.4 2-.3z M100 40 l.8 1.6 1.6.2 -1.2 1.1 .3 1.6 -1.5-.8 -1.5.8 .3-1.6 -1.2-1.1 1.6-.2z M40 20 l.7 1.4 1.4.2 -1 1 .2 1.4 -1.3-.7 -1.3.7 .2-1.4 -1-1 1.4-.2z" fill="${c.detalhe}"/></g>`,

    numeros: c => `${chao}<path d="M46 96 V30 H74 V96 Z" fill="${c.parede}" stroke="${T}" stroke-width="${W}"/>${pedras(48, 34, 24, 60)}
      <path d="M42 32 L60 16 L78 32 Z" fill="${c.telhado}" stroke="${T}" stroke-width="${W}" stroke-linejoin="round"/>
      <path class="brilho-suave" d="M60 -1 l7 8 -7 10 -7 -10 z" fill="#d9ccf0" stroke="#9f86c8" stroke-width="1.5" stroke-linejoin="round"/><path d="M60 -1 v18 M53 7 h14" stroke="#fff" stroke-width=".8" opacity=".8"/>
      <rect x="51" y="40" width="18" height="18" rx="2" fill="#fbf3e6" stroke="${T}" stroke-width="1.3"/><rect class="barra b1" x="54" y="50" width="3" height="6" fill="#a8bfa0"/><rect class="barra b2" x="58.5" y="46" width="3" height="10" fill="#e8a7bd"/><rect class="barra b3" x="63" y="43" width="3" height="13" fill="#9f86c8"/>
      ${jan(54, 62, 12, 10)}${porta(53, 76, 14, 20)}
      <g fill="${c.detalhe}" stroke="${T}" stroke-width="1"><path d="M28 96 l5 -12 5 12z"/><path d="M84 96 l4 -10 4 10z"/></g>${flores([[100, 95, "#e8a7bd"]])}`,

    laboratorio: c => `${chao}<rect x="26" y="56" width="62" height="40" rx="3" fill="${c.parede}" stroke="${T}" stroke-width="${W}"/>
      <path d="M20 60 Q22 30 57 28 Q92 30 94 60 Q57 66 20 60 Z" fill="${c.telhado}" stroke="${T}" stroke-width="${W}" stroke-linejoin="round"/>${pintas([[36, 44, 3.6], [72, 38, 3], [84, 50, 2.6]])}
      <path d="M74 34 h8 v6 l7 12 h-22 l7 -12 z" fill="rgba(240,250,246,.85)" stroke="${T}" stroke-width="1.3" stroke-linejoin="round"/><path d="M70 47 h16 l3 5 h-22z" fill="${c.detalhe}"/>
      <g class="fumaca"><circle cx="78" cy="26" r="3" fill="${c.detalhe}" opacity=".7"/><circle cx="82" cy="18" r="2.4" fill="#e8a7bd" opacity=".6"/><circle cx="77" cy="11" r="1.8" fill="#a8bfa0" opacity=".6"/></g>
      ${porta(50, 72, 14, 24)}${jan(32, 66, 12, 12, true)}${jan(70, 66, 12, 12, true)}
      <rect x="94" y="84" width="14" height="12" rx="2" fill="#a67a5b" stroke="${T}" stroke-width="1.2"/><path d="M97 84 v-4 h3 v4 M102 84 v-6 h3 v6" fill="rgba(240,250,246,.8)" stroke="${T}" stroke-width=".9"/>${flores([[20, 95, c.detalhe]])}`,

    cofre: c => `${chao}<path d="M28 97 C32 86 32 66 34 52 H86 C88 66 88 86 92 97 Z" fill="${c.parede}" stroke="${T}" stroke-width="${W}" stroke-linejoin="round"/>
      <ellipse cx="60" cy="52" rx="26" ry="8" fill="#d9b48e" stroke="${T}" stroke-width="${W}"/><ellipse cx="60" cy="52" rx="16" ry="4.8" fill="none" stroke="#a67a5b" stroke-width="1"/><ellipse cx="60" cy="52" rx="7" ry="2.2" fill="none" stroke="#a67a5b" stroke-width="1"/>
      <path d="M40 44 q-4 -10 4 -14 M80 46 q6 -10 -2 -16" stroke="${c.telhado}" stroke-width="2.4" fill="none" stroke-linecap="round"/><circle cx="44" cy="30" r="4.5" fill="${c.telhado}" stroke="${T}" stroke-width="1"/><circle cx="78" cy="30" r="4" fill="${c.telhado}" stroke="${T}" stroke-width="1"/>
      <circle cx="60" cy="76" r="14" fill="${c.detalhe}" stroke="${T}" stroke-width="${W}"/><circle cx="60" cy="76" r="9.5" fill="#e9c77b" stroke="#a9853d" stroke-width="1.2"/><path d="M60 69 v14 M53 76 h14" stroke="#a9853d" stroke-width="1.6"/><circle cx="60" cy="76" r="2.4" fill="#a9853d"/>
      ${[48, 72, 50, 70].map((x, i) => `<circle cx="${x}" cy="${i < 2 ? 66 : 86}" r="1.2" fill="#a9853d"/>`).join("")}
      <g class="moedas">${[[94, 94], [99, 94], [104, 94], [96.5, 90], [101.5, 90], [99, 86]].map(([x, y]) => `<ellipse cx="${x}" cy="${y}" rx="3" ry="1.8" fill="#e9c77b" stroke="#a9853d" stroke-width=".9"/>`).join("")}</g>`,

    trofeus: c => `${chao}<path d="M24 96 h72 v-5 h-72z" fill="#d9cfc4" stroke="${T}" stroke-width="${W}"/>
      <path d="M30 91 V46 M90 91 V46 M50 91 V50 M70 91 V50" stroke="${c.parede}" stroke-width="5"/><path d="M30 91 V46 M90 91 V46 M50 91 V50 M70 91 V50" stroke="${T}" stroke-width="1" opacity=".3"/>
      <path d="M20 48 Q60 8 100 48 Z" fill="${c.telhado}" stroke="${T}" stroke-width="${W}" stroke-linejoin="round"/><path d="M20 48 q10 5 20 0 q10 5 20 0 q10 5 20 0 q10 5 20 0" fill="${c.telhado}" stroke="${T}" stroke-width="1.2"/>
      <rect x="53" y="76" width="14" height="15" fill="#fbf3e6" stroke="${T}" stroke-width="1.2"/>
      <g class="brilho-suave"><path d="M50 56 h20 v6 a10 10 0 0 1 -20 0z" fill="#e9c77b" stroke="#a9853d" stroke-width="1.5"/><path d="M50 58 h-4 a4 4 0 0 0 5 6 M70 58 h4 a4 4 0 0 1 -5 6" fill="none" stroke="#a9853d" stroke-width="1.3"/><rect x="57" y="71" width="6" height="5" fill="#e9c77b" stroke="#a9853d" stroke-width="1"/></g>
      <path d="M60 22 v-6" stroke="${T}" stroke-width="1.2"/><circle cx="60" cy="14" r="2.6" fill="${c.detalhe}" stroke="${T}" stroke-width="1"/>
      <path d="M28 70 q-4 -10 4 -18 M92 70 q4 -10 -4 -18" stroke="#6f8f63" stroke-width="1.8" fill="none"/>${flores([[29, 62, "#e8a7bd"], [32, 54, "#fbf3e6"], [91, 62, "#e8a7bd"], [88, 54, "#fbf3e6"], [40, 94, "#e8a7bd"], [80, 94, "#e8a7bd"]])}`,

    mural: c => `${chao}<path d="M34 97 V40 M86 97 V40" stroke="${c.parede}" stroke-width="5"/><path d="M34 97 V40 M86 97 V40" stroke="${T}" stroke-width="1" opacity=".35"/>
      <path d="M24 42 L60 22 L96 42 Z" fill="${c.telhado}" stroke="${T}" stroke-width="${W}" stroke-linejoin="round"/>
      <rect x="30" y="44" width="60" height="40" rx="2" fill="#d9b48e" stroke="${T}" stroke-width="${W}"/>
      <rect x="36" y="49" width="15" height="13" fill="#fffaf2" stroke="${T}" stroke-width=".9" transform="rotate(-4 43 55)"/><rect x="56" y="48" width="14" height="15" fill="#f6d6e0" stroke="${T}" stroke-width=".9" transform="rotate(3 63 55)"/><rect x="73" y="50" width="12" height="12" fill="#e4dcf4" stroke="${T}" stroke-width=".9"/>
      <rect x="40" y="66" width="18" height="13" fill="#e2ecd9" stroke="${T}" stroke-width=".9" transform="rotate(2 49 72)"/><rect x="63" y="66" width="18" height="13" fill="#fffaf2" stroke="${T}" stroke-width=".9" transform="rotate(-3 72 72)"/>
      ${[[43, 49], [63, 48], [79, 50], [49, 66], [72, 66]].map(([x, y], i) => `<circle cx="${x}" cy="${y}" r="1.4" fill="${["#e8a7bd", "#9f86c8", "#d8b45e"][i % 3]}"/>`).join("")}
      ${flores([[28, 95, "#e8a7bd"], [92, 95, "#fbf3e6"]])}`
  };

  function predio(tipo, c, tam) {
    tam = tam || 120;
    const f = PREDIOS[tipo] || PREDIOS.casinha;
    return `<svg class="predio-svg" viewBox="0 -8 120 112" width="${tam}" height="${Math.round(tam * 112 / 120)}" aria-hidden="true">${f(c)}</svg>`;
  }

  /* ---------- encomendas (produtos de verdade, um desenho por produto até 3) ---------- */
  const caixa = (x, y, c) => `<g transform="translate(${x} ${y})"><rect x="-6" y="-6" width="12" height="11" rx="1.5" fill="${c}" stroke="${T}" stroke-width="1.2"/><path d="M0 -6 V5 M-6 -1.5 H6" stroke="#e9c77b" stroke-width="1.6"/><path d="M0 -6 c-3 -4 -6 -1 -2 0 M0 -6 c3 -4 6 -1 2 0" fill="none" stroke="#e9c77b" stroke-width="1.3"/></g>`;
  function encomendas(qtd) {
    const n = Math.min(3, qtd);
    const pos = [[9, 26], [22, 26], [15.5, 15]];
    const cores = ["#c8b6e2", "#f0c6d3", "#d6e6d2"];
    let s = `<svg class="encomendas-svg" viewBox="0 0 32 34" width="40" height="42" aria-hidden="true">`;
    for (let i = 0; i < n; i++) s += caixa(pos[i][0], pos[i][1], cores[i]);
    return s + `</svg>`;
  }

  /* ---------- decoração da floresta ---------- */
  function arvore(x, y, s, v) {
    const copa = ["#8fae86", "#a8bfa0", "#7d9c74", "#b8c9a8"][v % 4];
    const flor = ["#e8a7bd", "#fbf3e6", "#c8b6e2", "#f2d27a"][v % 4];
    return `<g transform="translate(${x} ${y}) scale(${s})">
      <path d="M-4 0 C-3 -10 -3 -18 -2 -26 H2 C3 -18 3 -10 4 0 Z" fill="#a67a5b" stroke="${T}" stroke-width="${1.4 / s}"/>
      <g fill="${copa}" stroke="${T}" stroke-width="${1.4 / s}"><circle cx="-12" cy="-30" r="12"/><circle cx="12" cy="-31" r="12"/><circle cx="0" cy="-42" r="15"/></g>
      <path d="M-8 -44 q4 -5 9 -4" stroke="#fffaf2" stroke-width="${1.6 / s}" opacity=".45" fill="none"/>
      <circle cx="-10" cy="-32" r="2" fill="${flor}"/><circle cx="7" cy="-44" r="2" fill="${flor}"/><circle cx="14" cy="-28" r="1.8" fill="${flor}"/></g>`;
  }
  function pinheiro(x, y, s) {
    return `<g transform="translate(${x} ${y}) scale(${s})"><path d="M-2.5 0 V-8 H2.5 V0Z" fill="#a67a5b"/><path d="M0 -46 L-14 -18 H-7 L-17 -6 H17 L7 -18 H14 Z" fill="#6f8f63" stroke="${T}" stroke-width="${1.3 / s}" stroke-linejoin="round"/><path d="M-4 -30 l4 -6 M2 -20 l5 -5" stroke="#a8bfa0" stroke-width="${1.4 / s}"/></g>`;
  }
  function cogumelo(x, y, s, c) {
    return `<g transform="translate(${x} ${y}) scale(${s})"><path d="M-2.5 0 V-6 H2.5 V0 Z" fill="#fbf3e6" stroke="${T}" stroke-width="${1 / s}"/><path d="M-7 -5 Q0 -15 7 -5 Z" fill="${c}" stroke="${T}" stroke-width="${1 / s}"/><circle cx="-2" cy="-9" r="1.1" fill="#fff"/><circle cx="2.5" cy="-7.5" r=".9" fill="#fff"/></g>`;
  }
  function flor2(x, y, c) { return `<g><path d="M${x} ${y} v6" stroke="#6f8f63" stroke-width="1.1"/>${flor(x, y, c)}</g>`; }
  function poste(x, y) {
    return `<g transform="translate(${x} ${y})"><path d="M0 0 V-22" stroke="#8a6146" stroke-width="2"/><path d="M0 -22 q6 0 6 5" stroke="#8a6146" stroke-width="1.6" fill="none"/><path d="M3 -17 h6 l-1 6 h-4 z" fill="#e9c77b" stroke="${T}" stroke-width="1"/><circle class="lampiao" cx="6" cy="-13.5" r="5" fill="#fbe7a6" opacity=".35"/></g>`;
  }
  function borboleta(c) {
    return `<svg viewBox="0 0 20 16" width="22" height="18" aria-hidden="true"><g class="asa-b"><path d="M10 8 C4 0 0 4 3 9 C5 12 8 11 10 8Z" fill="${c}" stroke="${T}" stroke-width=".8"/><path d="M10 8 C16 0 20 4 17 9 C15 12 12 11 10 8Z" fill="${c}" stroke="${T}" stroke-width=".8"/></g><path d="M10 5 v7" stroke="${T}" stroke-width="1.2" stroke-linecap="round"/></svg>`;
  }
  function coelho() {
    return `<svg viewBox="0 0 40 34" width="38" height="32" aria-hidden="true"><g class="coelho"><path d="M14 4 q-3 9 1 12 M20 3 q1 9 -2 12" stroke="${T}" stroke-width="1.3" fill="#fbf3e6"/><ellipse cx="24" cy="24" rx="11" ry="8" fill="#fbf3e6" stroke="${T}" stroke-width="1.3"/><circle cx="15" cy="17" r="6.5" fill="#fbf3e6" stroke="${T}" stroke-width="1.3"/><circle cx="13" cy="16.5" r="1" fill="#3b2633"/><ellipse cx="10.4" cy="19" rx="1.4" ry="1" fill="#f29fb0"/><circle cx="35" cy="22" r="2.6" fill="#fff" stroke="${T}" stroke-width="1"/><path d="M14.5 4.5 q-1.6 6 .5 9" stroke="#f29fb0" stroke-width="1.2" fill="none"/></g></svg>`;
  }

  /* Ícone de estado para o selo (forma, além da cor) */
  const ICONE = {
    trabalhando: `<svg viewBox="0 0 12 12" width="12" height="12" aria-hidden="true"><path d="M6 1 l1.2 3 3 .4 -2.3 2 .7 3 -2.6-1.6 -2.6 1.6 .7-3 -2.3-2 3-.4z" fill="currentColor"/></svg>`,
    sua_vez: `<svg viewBox="0 0 12 12" width="12" height="12" aria-hidden="true"><path d="M6 10.5 C1 7 1.2 3 3.6 2.6 5 2.4 6 3.6 6 3.6 S7 2.4 8.4 2.6 C10.8 3 11 7 6 10.5z" fill="currentColor"/></svg>`,
    aguardando: `<svg viewBox="0 0 12 12" width="12" height="12" aria-hidden="true"><path d="M7.8 1.6 A4.6 4.6 0 1 0 10.4 8 A3.6 3.6 0 1 1 7.8 1.6z" fill="currentColor"/></svg>`,
    concluido: `<svg viewBox="0 0 12 12" width="12" height="12" aria-hidden="true"><path d="M2 6.4 l2.6 2.6 5.4 -6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
    erro: `<svg viewBox="0 0 12 12" width="12" height="12" aria-hidden="true"><path d="M6 1.5 L11 10.5 H1 Z" fill="currentColor"/><path d="M6 4.6 v2.8" stroke="#fff" stroke-width="1.4" stroke-linecap="round"/><circle cx="6" cy="9" r=".8" fill="#fff"/></svg>`
  };

  /* Enfeites por estado, desenhados por cima da construção */
  const ENFEITE = `<svg class="enfeite" viewBox="0 0 120 60" aria-hidden="true">
      <g class="ef-faiscas"><path d="M20 30 l1.4 2.8 3 .4 -2.2 2 .5 3 -2.7-1.4 -2.7 1.4 .5-3 -2.2-2 3-.4z" fill="#f2d27a"/><path d="M98 18 l1 2 2.2.3 -1.6 1.5 .4 2.2 -2-1 -2 1 .4-2.2 -1.6-1.5 2.2-.3z" fill="#fbe7a6"/><circle cx="84" cy="40" r="1.6" fill="#fbe7a6"/></g>
      <g class="ef-chuva"><path d="M44 22 a8 8 0 0 1 14 -6 a10 10 0 0 1 18 4 a6 6 0 0 1 0 12 h-30 a6 6 0 0 1 -2 -10z" fill="#c9c3d4" stroke="${T}" stroke-width="1.3"/><path class="gota g1" d="M50 36 l-2 5" stroke="#8fa7d0" stroke-width="1.6" stroke-linecap="round"/><path class="gota g2" d="M60 36 l-2 5" stroke="#8fa7d0" stroke-width="1.6" stroke-linecap="round"/><path class="gota g3" d="M70 36 l-2 5" stroke="#8fa7d0" stroke-width="1.6" stroke-linecap="round"/></g>
      <g class="ef-estrelas"><path d="M16 26 l1.6 3.2 3.4.5 -2.5 2.3 .6 3.4 -3.1-1.6 -3.1 1.6 .6-3.4 -2.5-2.3 3.4-.5z" fill="#f2d27a" stroke="${T}" stroke-width=".7"/><path d="M102 30 l1.2 2.4 2.6.4 -1.9 1.8 .5 2.6 -2.4-1.2 -2.4 1.2 .5-2.6 -1.9-1.8 2.6-.4z" fill="#f2d27a" stroke="${T}" stroke-width=".7"/><circle cx="26" cy="50" r="2.6" fill="#e8a7bd" stroke="${T}" stroke-width=".7"/><circle cx="94" cy="50" r="2.6" fill="#fbf3e6" stroke="${T}" stroke-width=".7"/></g>
    </svg>`;

  return { personagem, predio, encomendas, arvore, pinheiro, cogumelo, flor: flor2, poste, borboleta, coelho, ICONE, ENFEITE, PREDIOS };
})();
