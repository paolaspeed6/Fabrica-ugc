/* =====================================================================
   BRINCAR: os 3 jogos da fábrica (Pode ou não pode, Memória, Ganchos).
   As regras das cartas vêm das regras reais da fábrica.
   Recordes ficam só no aparelho (navegador).
   ===================================================================== */
window.JOGOS = (() => {
  const CENAS = [
    ["Mão segurando o produto na capa do vídeo", 0, "Capa sempre com o produto inteiro e sem mão (regra 13)."],
    ["Taça de vinho na mesa ao lado do produto", 0, "Nada de bebida alcoólica, taça ou garrafa em cena."],
    ["Gancho: \"Cansada de bagunça na lavanderia?\"", 1, "Pergunta com problema real: é o estilo de gancho que você pediu."],
    ["\"Chega amanhã na sua casa\"", 0, "Nunca prometer prazo de entrega."],
    ["\"Nota 4,9 com 3.200 avaliações\"", 0, "Nota e avaliações nunca em número exato: mudam com o tempo."],
    ["\"Linhas retas e formato quadrado\" como qualidade", 0, "Característica neutra não é benefício (regra 11)."],
    ["Filtro de cor quente em todo o vídeo", 0, "Estilo natural, sem filtro: o filtro tirava qualidade."],
    ["Transição whip entre um take e outro", 1, "Transições whip e zoom são o padrão do estilo natural."],
    ["Voz narrando o produto", 0, "Agora é sem voz, só música calma."],
    ["\"Aguiiar Lar\" fixo no topo do vídeo", 1, "A assinatura fica fixa e centralizada no topo."],
    ["Os 3 vídeos começando com o mesmo take", 0, "Cada vídeo começa com um take diferente (regra 12)."],
    ["Logo da marca escrito torto pela IA", 0, "Letra inventada ou distorcida reprova o take (regra 14)."],
    ["O produto girando sozinho na cena", 0, "Produto parado; quem se mexe é a câmera."],
    ["Câmera se aproximando devagar do produto", 1, "Movimento suave de câmera deixa o vídeo real."],
    ["\"100 copos de alumínio\" quando o anúncio diz 100", 1, "Número tirado do anúncio pode e deve aparecer grande."],
    ["\"30% de desconto só hoje\"", 0, "Porcentagem de desconto não entra."],
    ["Produto inteiro no primeiro quadro", 1, "É a capa certa."],
    ["Inversor mostrando 1600 W quando o anúncio diz 1000 W", 0, "Só o que o anúncio confirma. Detalhe errado da IA não passa."],
    ["Música calma de fundo, trocando entre vídeos", 1, "A biblioteca de músicas alterna sozinha."],
    ["Pedaço do drone bugando no ar", 0, "Só os momentos que não bugam."],
    ["Gancho: \"Sua piscina ainda fica verde?\"", 1, "Problema real que o produto resolve."],
    ["Gerar imagem paga sem o seu OK", 0, "Nada pago sem o seu OK, com teto em dólar."],
    ["Cadeira de carro no chão da sala", 0, "Cenário do uso real do produto."],
    ["Kit de 10 cadeiras mostrando as 10 inteiras", 1, "Se o anúncio tem 10, o vídeo mostra as 10."]
  ];
  const GANCHOS = ["Ainda sofrendo com [problema]?", "Sua [cômodo] estava pedindo isso", "Chega de [problema] em casa", "Por que ninguém me contou disso antes?",
    "Quem tem [situação] precisa ver isso", "Esse achadinho resolveu [problema]", "Olha o que vem na caixa: [itens do anúncio]", "Você ainda [hábito chato]?",
    "O detalhe que muda a sua [cômodo]", "Antes de comprar [produto], veja isso", "[número do anúncio] num pedido só", "A sua casa merece esse upgrade"];
  const SORTES = ["Hoje um produto raro aparece no Tinder.", "Quem posta no fim da tarde tem mais sorte.", "Confira a capa antes de tudo.",
    "As redes estão ouvindo hoje.", "Luz de janela e casa arrumada vendem mais.", "Nada pago sem teto: o cofre agradece.",
    "Pergunta curta prende o dedo.", "O erro de ontem virou regra.", "Tem venda chegando perto de você.",
    "Só qualidades reais do anúncio.", "Música calma e corte no ritmo.", "Divida o trabalho e descanse."];

  function iniciar({ $, esc, confete, ls, poucoMovimento }) {
    const personagens = Object.values(TEMA.estacoes).map(e => e.personagem).concat(TEMA.areas.map(a => a.personagem));
    $("j1-pers").innerHTML = ARTE.personagem(TEMA.estacoes.fiscal_imagem.personagem, 50);

    // Jogo 1
    let at = { on: false, ronda: [], i: 0, pts: 0 };
    const atRec = () => $("at-rec").textContent = "recorde " + (ls.get("atena-rec") || 0);
    function atMostra() {
      const [t] = at.ronda[at.i]; const c = $("at-carta"); c.className = "carta"; c.textContent = t;
      $("at-porque").textContent = ""; $("at-rod").textContent = `Rodada ${at.i + 1} de ${at.ronda.length}`;
      $("at-sim").disabled = false; $("at-nao").disabled = false;
    }
    function atResp(v) {
      if (!at.on) return; const [, certo, pq] = at.ronda[at.i]; const ok = (v === certo);
      if (ok) at.pts++;
      $("at-carta").className = "carta " + (ok ? "certo" : "errado");
      $("at-porque").textContent = (ok ? "Acertou! " : "Errou. ") + pq;
      $("at-pts").textContent = at.pts + (at.pts === 1 ? " acerto" : " acertos");
      $("at-sim").disabled = true; $("at-nao").disabled = true;
      const bt = $("at-ir");
      if (at.i < at.ronda.length - 1) { bt.textContent = "Próxima"; bt.hidden = false; }
      else {
        at.on = false; const rec = Number(ls.get("atena-rec") || 0); if (at.pts > rec) ls.set("atena-rec", at.pts); atRec();
        $("at-carta").textContent = at.pts === 10 ? "Coroa de ouro! A fada fiscal aprova o seu reino." : at.pts >= 7 ? `${at.pts} de 10. Mandou bem!` : `${at.pts} de 10. Bora mais uma rodada?`;
        if (at.pts === 10) confete(); bt.textContent = "Jogar de novo"; bt.hidden = false;
      }
    }
    $("at-ir").onclick = () => {
      if (!at.on) { at = { on: true, ronda: CENAS.slice().sort(() => Math.random() - .5).slice(0, 10), i: 0, pts: 0 }; $("at-pts").textContent = "0 acertos"; }
      else at.i++;
      $("at-ir").hidden = true; atMostra();
    };
    $("at-sim").onclick = () => atResp(1); $("at-nao").onclick = () => atResp(0);
    atRec();

    // Jogo 2: memória das divas
    const PARES = personagens.slice(0, 8);
    let me = {};
    function mePlaca() {
      $("me-jog").textContent = me.jog + (me.jog === 1 ? " jogada" : " jogadas"); $("me-par").textContent = me.pares + " de 8 pares";
      const r = ls.get("memoria-rec"); $("me-rec").textContent = "recorde " + (r ? r + " jogadas" : "-");
    }
    function meNovo() {
      me = { cartas: [...PARES.keys(), ...PARES.keys()].sort(() => Math.random() - .5).map(k => ({ k, ok: false })), abertas: [], jog: 0, pares: 0, trava: false };
      const tab = $("me-tab"); tab.innerHTML = "";
      me.cartas.forEach((c, i) => {
        const b = document.createElement("button"); b.type = "button"; b.className = "peca"; b.setAttribute("aria-label", "Carta " + (i + 1));
        b.innerHTML = '<span class="verso" aria-hidden="true"></span>'; b.onclick = () => meVira(i, b); c.el = b; tab.append(b);
      });
      mePlaca();
    }
    function meVira(i, b) {
      const c = me.cartas[i]; if (me.trava || c.ok || me.abertas.includes(i)) return;
      b.classList.add("virada"); b.innerHTML = ARTE.personagem(PARES[c.k], 44); b.setAttribute("aria-label", PARES[c.k].nome); me.abertas.push(i);
      if (me.abertas.length < 2) return;
      me.jog++; const [a, z] = me.abertas.map(k => me.cartas[k]);
      if (a.k === z.k) {
        a.ok = z.ok = true; a.el.classList.add("par"); z.el.classList.add("par"); me.abertas = []; me.pares++;
        if (me.pares === 8) { const r = Number(ls.get("memoria-rec") || 0); if (!r || me.jog < r) ls.set("memoria-rec", me.jog); confete(); }
      } else {
        me.trava = true;
        setTimeout(() => { [a, z].forEach(c => { c.el.classList.remove("virada"); c.el.innerHTML = '<span class="verso" aria-hidden="true"></span>'; c.el.setAttribute("aria-label", "Carta virada"); }); me.abertas = []; me.trava = false; }, 850);
      }
      mePlaca();
    }
    $("me-novo").onclick = meNovo; meNovo();

    // Jogo 3: poço dos ganchos
    let ganchoAtual = "";
    const hojeIdx = () => { const d = new Date(); return (d.getFullYear() * 372 + d.getMonth() * 31 + d.getDate()) % SORTES.length; };
    $("or-bt").onclick = () => {
      const tela = $("or-txt"); let n = 0;
      const gira = setInterval(() => {
        tela.innerHTML = esc(GANCHOS[Math.floor(Math.random() * GANCHOS.length)]) + "<small>a água está girando...</small>";
        if (++n > 7) {
          clearInterval(gira);
          let g; do { g = GANCHOS[Math.floor(Math.random() * GANCHOS.length)]; } while (g === ganchoAtual && GANCHOS.length > 1); ganchoAtual = g;
          tela.innerHTML = `${esc(g)}<small>Sorte do dia: ${esc(SORTES[hojeIdx()])}</small>`; $("or-copiar").disabled = false;
        }
      }, poucoMovimento() ? 0 : 90);
    };
    $("or-copiar").onclick = e => {
      const b = e.currentTarget;
      const ok = () => { b.textContent = "Copiado!"; setTimeout(() => b.textContent = "Copiar gancho", 1500); };
      try { navigator.clipboard.writeText(ganchoAtual).then(ok, () => {}); } catch (x) { }
    };
  }
  return { iniciar };
})();
