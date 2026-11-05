# Criar o acesso Google para o botão «Entrar»

Faça isto com a conta **genialtarot@gmail.com**. Demora cerca de 10 minutos e não custa nada.

1. Abra <https://console.cloud.google.com/> e, em cima, escolha o projecto **cerebro** (é onde já está a Search Console).
2. Menu > **Google Auth Platform** > **Vista geral** > **Começar** (se ainda não estiver configurado).
3. Preencha:
   - Nome da aplicação: `Genial Tarot`
   - Email de apoio: `genialtarot@gmail.com`
   - Público: **Externo**
   - Contacto: `genialtarot@gmail.com`
4. Em **Marca** (Branding), ponha:
   - Página inicial: `https://genialtarot.com`
   - Política de privacidade: `https://genialtarot.com/privacidade`
   - Termos: `https://genialtarot.com/termos`
   - Domínio autorizado: `genialtarot.com`
5. Em **Acesso a dados** (Data Access), não acrescente nada: `openid`, `email` e `profile` já chegam.
6. Em **Público** (Audience), carregue em **Publicar aplicação**. Sem isto, só as contas de teste conseguem entrar.
7. Em **Clientes** > **Criar cliente**:
   - Tipo: **Aplicação Web**
   - Nome: `Site genialtarot.com`
   - Origens JavaScript autorizadas, adicione as duas:
     - `https://genialtarot.com`
     - `https://www.genialtarot.com`
   - URIs de redirecionamento: deixe vazio.
8. Carregue em **Criar** e copie o **ID de cliente**, que termina em `.apps.googleusercontent.com`.
9. Envie-me esse ID. É público, pode ir pelo Telegram. **Não precisa do segredo do cliente**: não é usado e não o envie.

Eu ponho o ID em `GOOGLE_CLIENT_ID`, no início do bloco CONTA do `worker.js`, e o botão Google aparece sozinho na janela de entrar.
