# Contas e chaves que VOCÊ cria (uma vez só)

Tudo no seu nome e no seu cartão. Nenhuma chave vai em arquivo nem no chat: cada uma vira uma variável de ambiente.
- Windows: `setx NOME "valor"` no terminal, depois feche e abra o terminal.
- Mac/Linux: acrescente `export NOME="valor"` ao fim do `~/.zshrc` ou `~/.bashrc` e abra um terminal novo.

| O quê | Para quê | Custo | Variáveis |
|---|---|---|---|
| Plano Claude Pro ou Max | o Claude que roda a fábrica | assinatura | (login no Claude Code) |
| WaveSpeed | imagens e animações das cenas | ~US$ 0,42 por produto | WAVESPEED_API_KEY |
| Shopee Afiliados, Open API | varredura do Tinder e links com Sub ID | grátis | SHOPEE_APP_ID, SHOPEE_APP_SECRET |
| Google Cloud (Drive) | guardar os vídeos no seu Drive | grátis | GDRIVE_CLIENT_ID, GDRIVE_CLIENT_SECRET, GDRIVE_REFRESH_TOKEN |
| App da Meta | postar sozinho no Instagram, Facebook e Threads | grátis | META_PAGE_TOKEN, META_PAGE_ID, META_IG_ID, THREADS_TOKEN |
| Sua marca | assinatura pequena no topo do vídeo | grátis | MARCA_NOME (ex.: o nome da sua loja) |
| Pasta do Drive | nome da pasta raiz | grátis | DRIVE_PASTA (padrão "Fabrica Videos") |

## 1. WaveSpeed
1. Crie a conta em wavespeed.ai com seu e-mail.
2. Coloque crédito (US$ 10 dá uns 20 produtos, 80 vídeos).
3. Em API Keys, gere uma chave e grave como WAVESPEED_API_KEY.

## 2. Shopee Afiliados (Open API)
1. Entre em affiliate.shopee.com.br com a SUA conta de afiliada.
2. No menu, abra Open API e peça o acesso (pode levar alguns dias para aprovar).
3. Aprovado, copie o AppID e a Secret. Grave como SHOPEE_APP_ID e SHOPEE_APP_SECRET.
4. Teste: peça ao Claude "teste a API da Shopee" (ele gera 1 link de teste com Sub ID, grátis).

## 3. Google Drive
1. Abra console.cloud.google.com com a sua conta Google e crie um projeto (ex.: "Fabrica Videos").
2. APIs e serviços > Biblioteca > "Google Drive API" > Ativar.
3. Tela de consentimento OAuth: tipo Externo, nome do app, seu e-mail; em Usuários de teste, adicione o seu e-mail.
   Depois publique o app ("Publicar aplicativo"), senão o token vence em 7 dias.
4. Credenciais > Criar credenciais > ID do cliente OAuth > tipo "Aplicativo da Web", com o URI de redirecionamento
   `https://developers.google.com/oauthplayground`. Guarde o ID e a chave secreta como GDRIVE_CLIENT_ID e GDRIVE_CLIENT_SECRET.
5. Abra developers.google.com/oauthplayground, toque na engrenagem, marque "Use your own OAuth credentials" e cole o ID e a chave.
   No campo de escopo escreva `https://www.googleapis.com/auth/drive.file`, toque em Authorize APIs, entre na sua conta e autorize.
   Toque em "Exchange authorization code for tokens" e guarde o Refresh token como GDRIVE_REFRESH_TOKEN.
   (No PC dá para usar `python video-teste/drive_token.py` no lugar, com um cliente do tipo "App para computador".)

## 4. Meta (Instagram, Facebook e Threads)
Precisa de: Instagram profissional (Comercial ou Criador de conteúdo) ligado a uma Página do Facebook sua, e um perfil no Threads.
1. developers.facebook.com > Meus apps > Criar app. Deixe no modo Desenvolvimento: postar só nas suas próprias contas não precisa de revisão da Meta.
2. Casos de uso: "Gerenciar tudo na sua Página", "Gerenciar mensagens e conteúdo no Instagram" (pelo login do Facebook) e "Acessar a API do Threads".
   Se a Meta não deixar o Threads no mesmo app, crie um segundo app só para ele.
3. Página e Instagram: no Explorador da Graph API, escolha o app, gere um token de usuário com
   pages_show_list, pages_read_engagement, pages_manage_posts, pages_manage_engagement, instagram_basic,
   instagram_content_publish e business_management. Troque por um token de longa duração (Ferramentas > Depurador de token >
   "Estender"). Com ele, `me/accounts` mostra o token da sua Página, que não vence. Grave como META_PAGE_TOKEN.
4. Threads: no caso de uso do Threads, adicione seu perfil como testador (aceite o convite no app ou site do Threads)
   e gere o token no "Gerador de token" (se travar, use uma janela anônima). Vale 60 dias: o Claude renova antes de vencer. Grave como THREADS_TOKEN.
5. Peça ao Claude "confira a postagem automática". Ele roda `meta/postar.py conferir`, mostra os ids da Página e do Instagram
   e você grava como META_PAGE_ID e META_IG_ID.
6. Política de privacidade: a Meta pede um link. Uma página simples sua serve (o Claude pode fazer uma).

## 5. Onde guardar a pasta do kit
- No seu PC, numa pasta comum (ex.: Documentos/fabrica-shopee). É o caminho recomendado.
- Se um dia quiser o Git/GitHub: só repositório PRIVADO. Nunca suba chave, token, link de afiliado ou vídeo em repositório público
  (o `.gitignore` do kit já deixa de fora lotes, vídeos e registros).
