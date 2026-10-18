# Ficha rápida da fábrica (modo enxuto, a dona, 2026-10-15)

Um agente faz tudo numa passada só, sem reler outros arquivos de regras. O resultado é o `qNN.json` do produto, no formato de `lote/hoje1015/p11v2.json` e `p05.json`.

Antes de criar, leia `principios.md` inteiro (todos os livros) e aplique.

## 1. Pesquisa (5 linhas mentais)
1. Qual é o desejo de massa?
2. Qual é a prova mais forte do anúncio? Número, medida, quantidade, material; nota e avaliações só como "bem avaliado", nunca o número.
3. Qual é o mecanismo único?
4. Qual é a objeção principal?
5. Qual é o risco de letras ou detalhes finos?
5b. Contagem: quantas prateleiras, gavetas, anéis, peças? Grave `"contagem"` no JSON e use só fotos com essa mesma contagem (`regras_de_erros.md` 1.1).
6. Oceano Azul (`principios.md`): o que todo vídeo parecido faz (clichê) e o que o nosso cria de diferente? Ao menos 1 edição usa esse ângulo novo, e nenhum gancho pode servir para o concorrente.

## 2. Textos: 3 edições, cada uma com gancho e CTA próprios, curtos e fiéis ao produto
- **`shopee`**: vitrine com texto animado.
  - Cena 1 tem `"abertura": {"grande": "<até 4 caracteres: número ou palavra>", "texto": "<até 5 palavras>"}`.
  - Cada cena tem `rotulo`, `titulo` com um `[destaque]`, até 6 palavras.
  - Cena 3 tem `fichas` (3 itens curtos) e `cta`.
- **`shopee2`**: `"estilo": "tiktok"`, letras grandes no topo.
  - Cada cena tem `titulo` em até 5 palavras com `[destaque]` e um `sub` curto.
  - Cena 3: o próprio título é o CTA, por exemplo "Leve o seu no [carrinho]".
- **`reels`**: `"estilo": "reels_faixas"` para impacto, impulso e preço, ou `"reels_cartao"` para prova e quantidade (selo em palavra, ex.: TOP avaliado).
  - O cartão leva `"selo": {"n": "...", "t": "..."}` no nível do produto.
  - Cada cena tem `rotulo`, `titulo` (até 2 linhas) e `sub` opcional.
  - Cena 3 tem `cta` "Link no 1º comentário".
- **Ganchos:** curiosidade, quantidade + preço por comparação, prova social, dor, POV ou medida. Escolha o padrão que serve a ESTE produto.
- **`legendas`:**
  - `shopee` e `shopee2`: descrição simples + 4 hashtags de nicho (nunca #achadinhosshopee), menos de 150 caracteres, sem emoji.
  - `reels`: gancho + benefício + "Link do produto: <link>" na própria legenda, e `hashtags.reels`.
- **`comentario`:** "🛒 <produto> aqui: {link}".

## 3. Cenas (3 de 5 s, prompts em inglês)
- **`fotos`:** `["qNN-fotos/01.jpg", ...]`. A 01 vem sempre primeiro; acrescente no máximo 1 a 2 fotos reais úteis.
- **Cena com `"editar"`:** Seedream coloca o produto num ambiente. Siga esta ordem no texto:
  1. Formato: "Photorealistic full-frame photo, 9:16 vertical."
  2. O produto exato, "from reference photo 1": cor, material e formato de cada parte, tudo como na foto 01.
  3. Cenário simples e coerente com o uso, descrevendo só o que existe ("minimalist, only the objects described").
  4. Plano, lente e luz: por exemplo "85 mm, shallow depth of field, soft window light, neutral white balance".
  5. "The whole product fills 25-60% of the image height, centered, empty floor below."
- **Cena com `"foto": i`:** anima a própria foto do anúncio. É o modo mais fiel e não gasta imagem.
- **`movimento`:** um só, entre slow push-in, gentle lateral dolly, crane up reveal ou rack focus. Arco só se `"angulos_reais": true`.

## Letras e detalhes mínimos
Vale para rótulo, embalagem, painel, display, logo e escrita miúda:
- A IA nunca redesenha esses elementos.
- Use `"foto"` com movimento mínimo, ou mostre o produto num ângulo e escala em que as letras fiquem grandes e simples.
- Para embalagem, marque `"embalagem_com_letras": true` e componha a foto real com `"sobrepor"`.

## Nunca
- Pessoas, mãos ou álcool.
- Citar o proibido no prompt, nem negando.
- Prazo de entrega ou "envio imediato".
- Afirmação que o anúncio não prove.
- Preço exato (só por comparação, com conta certa).
- Cor diferente da foto 01.

## Formato do JSON
- `nome`: "qNN_slug".
- `link`, `titulo_produto`, `fotos`, `cor_destaque` ("auto" ou o hex que combina com o produto), `cenas`, `versoes` {shopee, shopee2, reels}, `legendas`, `hashtags`, `comentario`, `selo` (se cartão).
- Flags quando couber: `embalagem_com_letras`, `angulos_reais`.

## Checagens de edição (regra, 2026-10-15, após o lote de 22)
Olhar o vídeo pronto em 5 instantes (1 s, meio e fim de cada cena), em TODAS as versões, nunca só um quadro:
- Texto nunca sobre o produto, em nenhuma cena. Reels: o cartão/faixas ocupam y 1140-1620; produto quadrado já sobe por padrão (desloc -320).
- Letras do texto nunca se sobrepõem entre si: título que quebra em 2 linhas empurra as fichas (a Shopee mede a altura real).
- Letras miúdas da embalagem ou do painel não podem bugar quando o ângulo muda: a IA (Seedance) distorce escrita pequena em foto animada. Para embalagem ou painel com letras, usar movimento feito por código sobre a foto real (zoom/pan), nunca animação por IA.
- Cena de IA nunca pode inventar peças (parafuso, dobradiça, rodinha, cachorro, celular).
- PRIMEIRO TAKE (regra, 2026-10-15): o produto aparece INTEIRO desde o primeiro quadro, limpo e claro, sem zoom que corte, sem objeto ou letra por cima. Nada de recorte apertado nem push-in forte na cena 1; usar a foto inteira com zoom bem leve feito por código (ffmpeg zoompan, grátis), que também não distorce letras miúdas.
