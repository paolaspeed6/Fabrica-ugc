# Mapa da Fábrica (opcional, a dona escolhe o visual)

`mapa.html` é o "jogo" da fábrica original: abas Missões (o que é a vez dela + botões para cada página), Mapa (estrada com as
estações), Gasto total (coleção `gastos`) e Desperdício. Funciona como está, mas o visual é para ela escolher.

Antes de publicar, pergunte como ela quer o design. Sugestão do Kevin para ela: mais delicado e feminino, estilo Tumblr/Pinterest,
luxuoso, fashion, conceitual, com elementos da mitologia greco-romana (colunas, mármore, folhas de louro, ouro suave, deusas como
estações: Ártemis caçadora no Tinder, Atena na Conferência, Hermes no Postador...), com funcionalidades e estética melhoradas.
Faça 2-3 prévias em imagem estática feita por código/HTML (grátis), nunca gere imagem paga para isso sem ela pedir.

Ao publicar: capabilities {db: {}, user: {}}; troque COLE_URL_TINDER / COLE_URL_POSTAGENS / COLE_URL_CONFERENCIA pelas URLs dela.
Banco: `postagens_resumo/atual` (contador, tarefa das 23:55 com mapa/resumo_postados.py) e `gastos/<id>` com
{nome, grupo: contado|preencher|gratis, moeda: USD|BRL, valor (null = ela preenche), detalhe, ordem}. Semeie: WaveSpeed (contado, USD,
some os gasto.json dos lotes), plano Claude e outras assinaturas (preencher), Shopee API, Drive, Meta, GitHub (gratis).
Atualize Missões e o "Rodando sozinho" quando algo mudar.
