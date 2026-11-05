# Ligar o envio dos emails de entrada

Isto corre no cerebro, depois de publicar. Enquanto o vigia não estiver ligado, o botão «Entrar» aparece mas o email não chega.

## Ordem

1. Ligar o vigia **antes** de publicar não dá nada, porque a rota ainda não existe. Publicar primeiro, ligar logo a seguir.
2. Copiar a pasta: `cp -r ~/site-genialtarot/conta-painel ~/conta-painel`
3. Com o cofre aberto: `sudo cp ~/conta-painel/conta-vigia.service /etc/systemd/system/ && sudo systemctl daemon-reload && sudo systemctl enable --now conta-vigia`
4. Provar: entrar no site com um email dele e confirmar que o email chega em segundos. `journalctl -u conta-vigia -n 20` não mostra emails nem ligações.

## O que convém saber

- As chaves saem do cofre (`Chaves/site-estatisticas.pass`, `Mail/contas/genialtarot.pass`) e ficam em memória. **O serviço tem de arrancar com o cofre aberto**; se arrancar fechado, espera e avisa no Telegram. Depois do arranque, a noite de cofre fechado não o afecta.
- Se o cerebro estiver em baixo, os emails não saem e o pedido caduca aos 15 minutos. A entrada por Google continua a funcionar.
- Limites: 3 pedidos em 15 min e 8 por dia por email; 5 em 15 min e 20 por dia por IP; 60 por hora e 300 por dia no total. O Gmail é o mesmo das promoções (limite delas: 400/dia).

## Lista de promoções (por ligar, é decisão dele)

Só depois do vigia a funcionar: `touch ~/conta-painel/promo-LIGADA`.
- Marcou a caixa: entra no `extras.json` (`grupo: autorizou`, `codigo: conta`), sem ficha de cliente, com a prova do consentimento.
- Desmarcou: vai para `saidas.json` e sai do `extras.json`.
- Apagou a conta: sai de tudo, pelo hash do email.
- Enquanto o ficheiro não existir, os eventos esperam no site até 30 dias.
- **Falta um sentido:** quem carrega em «sair» num email fica fora da lista, mas a caixa em «Os meus dados» continua marcada.
