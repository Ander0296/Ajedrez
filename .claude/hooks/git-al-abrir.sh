#!/usr/bin/env bash
# Trae lo último del repo al abrir la sesión, sin depender de que el usuario
# se acuerde de correr /arranque. Con dos PCs, entrenar sobre una copia vieja
# es la forma más rápida de perder trabajo (y de analizar dos veces la misma
# partida).
#
# Silencioso cuando no hay nada que traer o cuando el repo todavía no tiene
# remoto. Si algo falla, lo dice y sigue: un hook de arranque nunca debe
# impedir que la sesión abra.

set -u
cd "${CLAUDE_PROJECT_DIR:-.}" 2>/dev/null || exit 0
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0
# Sin rama remota configurada (repo recién creado, todavía no está en GitHub).
git rev-parse --abbrev-ref --symbolic-full-name '@{u}' >/dev/null 2>&1 || exit 0

salida=$(git pull --rebase --autostash 2>&1)
estado=$?

if [ $estado -ne 0 ]; then
  jq -n --arg s "$salida" '{systemMessage: ("git pull falló al abrir la sesión — revisalo antes de entrenar:\n" + $s)}'
elif ! printf '%s' "$salida" | grep -q 'Already up to date\|Ya está actualizado'; then
  jq -n '{systemMessage: "git pull: se bajaron cambios del otro PC."}'
fi

exit 0
