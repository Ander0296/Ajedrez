#!/usr/bin/env bash
# Candado pedagógico: Claude NO toca el trabajo del usuario.
#
# La regla de CLAUDE.md dice que el usuario resuelve, analiza y escribe su
# repertorio a mano, y que Claude solo crea el ARCHIVO DE ARRANQUE
# (enunciado + prompt). Una regla escrita se cumple casi siempre; este hook
# la vuelve mecánica.
#
# Permitido:  crear un archivo NUEVO en las carpetas protegidas (Write).
# Bloqueado:  editar o sobrescribir cualquier archivo que YA existe ahí.
#
# Si alguna vez hace falta saltearlo: `/hooks` para desactivarlo, o pedirle a
# Claude el cambio EN EL CHAT y aplicarlo a mano (que es justamente el punto).

set -u

# Carpetas donde vive el trabajo del usuario: soluciones de prácticas,
# autoanálisis de partidas y repertorio de aperturas.
CARPETAS_PROTEGIDAS='/(ejercicios|analisis|repertorio)/'

entrada=$(cat)
herramienta=$(printf '%s' "$entrada" | jq -r '.tool_name // empty')
archivo=$(printf '%s' "$entrada" | jq -r '.tool_input.file_path // empty')

[ -z "$archivo" ] && exit 0
printf '%s' "$archivo" | grep -qE "$CARPETAS_PROTEGIDAS" || exit 0

# Crear un archivo de arranque nuevo sí está permitido.
if [ "$herramienta" = "Write" ] && [ ! -e "$archivo" ]; then
  exit 0
fi

motivo="BLOQUEADO por el candado del proyecto: ese archivo es trabajo del usuario.
Claude solo puede CREAR archivos nuevos en las carpetas de trabajo
(el archivo de arranque: enunciado + prompt, sin solución).
Editar o sobrescribir lo que el usuario ya escribió está prohibido: la
corrección va AL CHAT y, en 3 líneas como máximo, a EJERCICIOS.md."

jq -n --arg motivo "$motivo" '{
  hookSpecificOutput: {
    hookEventName: "PreToolUse",
    permissionDecision: "deny",
    permissionDecisionReason: $motivo
  }
}'
exit 0
