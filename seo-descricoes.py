#!/usr/bin/env python3
"""Descrições na medida certa (110–160 car.) para as páginas que estavam fora dela — 01/11/2026, pedido dele («corrige
isso tudo»). Troca a description, a og:description e a twitter:description. Idempotente; o gerar-signos.py chama-o no fim.
(Os sonhos acertam-se no ~/sonhos/construir.py; os temas e as rezas nos seus *-textos.py.)"""
import os, re, html
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DESC = {
 "aniversarios": "Os artistas e personalidades do Brasil e de Portugal que fazem anos hoje, e o signo de cada um. Descubra quem nasceu no mesmo dia que você.",
 "anual": "Previsão Anual 2026 do Mestre Alberto para os 12 signos: escolha o seu e veja o vídeo completo com as previsões do ano para o seu signo.",
 "compatibilidade": "Compatibilidade entre signos: escolha dois signos e veja o que os une, o que pede cuidado no amor e a carta do Tarot para o par. Grátis.",
 "horoscopo-do-dia": "O horóscopo do dia de cada signo, feito a partir do céu real de hoje: a Lua, os aspetos dos planetas e uma dica nova todos os dias. Grátis.",
 "noticias-do-ceu": "Notícias do Céu: as mudanças de signo, os planetas retrógrados, as Luas Cheias e os eclipses das próximas semanas, explicados em linguagem simples.",
 "lua": "Calendário Lunar com as fases da Lua, a Lua em cada signo dia a dia, os eclipses e as superluas, na hora de Brasília ou de Portugal.",
 "horoscopo-chines": "Descubra o seu animal e o seu elemento no Horóscopo Chinês pela data de nascimento, com o Ano Novo Chinês calculado ano a ano.",
}
mudou = 0
for slug, d in DESC.items():
    f = slug + ".html"
    if not os.path.exists(f): continue
    s = open(f, encoding="utf-8").read(); a = s; v = html.escape(d, quote=True)
    s = re.sub(r'(<meta\s+name="description"\s+content=")[^"]*(")', lambda m: m.group(1) + v + m.group(2), s, count=1)
    s = re.sub(r'(<meta\s+property="og:description"\s+content=")[^"]*(")', lambda m: m.group(1) + v + m.group(2), s, count=1)
    s = re.sub(r'(<meta\s+name="twitter:description"\s+content=")[^"]*(")', lambda m: m.group(1) + v + m.group(2), s, count=1)
    if s != a: open(f, "w", encoding="utf-8").write(s); mudou += 1
print(f"seo-descricoes: {mudou} páginas acertadas")
