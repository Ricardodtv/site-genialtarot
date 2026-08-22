#!/usr/bin/env bash
# Poe o codigo das estatisticas em qualquer pagina HTML que ainda nao o tenha.
#
# 22/08/2026, ordem dele: "quero que coloques de forma automatica nas novas
# paginas senao eu nao me lembro". Nao pode depender de ninguem se lembrar --
# nem dele, nem de mim.
#
# Corre sozinho antes de cada commit (.git/hooks/pre-commit). Tambem se pode
# correr a mao:  bash por-beacon.sh
#
# Sem argumentos, trata todos os .html. Com argumentos, so esses.
set -uo pipefail
cd "$(dirname "$0")" || exit 1

BEACON='<!-- Cloudflare Web Analytics --><script type='"'"'module'"'"' src='"'"'https://static.cloudflareinsights.com/beacon.min.js'"'"' data-cf-beacon='"'"'{"token": "803a58a6fccd4bd9ac12cce898a73bce"}'"'"'></script><!-- End Cloudflare Web Analytics -->'

alvos=("$@")
[ ${#alvos[@]} -eq 0 ] && mapfile -t alvos < <(ls *.html 2>/dev/null)

postos=()
for f in "${alvos[@]}"; do
  [ -f "$f" ] || continue
  case "$f" in *.html) ;; *) continue ;; esac
  grep -q "cloudflareinsights" "$f" && continue
  if ! grep -qi "</head>" "$f"; then
    echo "  ⚠️ $f nao tem </head> -- deixado como esta, ve a mao" >&2
    continue
  fi
  # insere na PRIMEIRA ocorrencia de </head>, preservando o resto tal e qual
  python3 - "$f" "$BEACON" <<'PY'
import sys, io, re
f, beacon = sys.argv[1], sys.argv[2]
t = io.open(f, encoding="utf-8").read()
m = re.search(r"</head>", t, re.I)
io.open(f, "w", encoding="utf-8").write(t[:m.start()] + beacon + "\n" + t[m.start():])
PY
  postos+=("$f")
done

if [ ${#postos[@]} -gt 0 ]; then
  echo "📊 codigo das estatisticas posto em ${#postos[@]} pagina(s): ${postos[*]}"
  printf '%s\n' "${postos[@]}"   # a lista, para quem chamar poder fazer git add
fi
exit 0
