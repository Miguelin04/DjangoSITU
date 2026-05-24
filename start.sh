#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/miguel/Escritorio/Computación Nube/Situ/DjangoSITU"
PYTHON="$ROOT/env/bin/python"
APP_DIR="$ROOT/src/ProyectoSITU"
PORT="${PORT:-8000}"

is_port_in_use() {
	local port="$1"
	if command -v ss >/dev/null 2>&1; then
		ss -ltn | grep -q ":${port} "
		return $?
	fi

	if command -v lsof >/dev/null 2>&1; then
		lsof -i ":${port}" -sTCP:LISTEN -t >/dev/null 2>&1
		return $?
	fi

	return 1
}

if is_port_in_use "$PORT"; then
	echo "[SITU] El puerto $PORT está ocupado. Buscando uno libre..."
	ALT_PORT="$((PORT + 1))"
	while is_port_in_use "$ALT_PORT"; do
		ALT_PORT="$((ALT_PORT + 1))"
	done
	PORT="$ALT_PORT"
fi

cd "$APP_DIR"

echo "[SITU] Verificando proyecto..."
"$PYTHON" manage.py check

echo "[SITU] Aplicando migraciones..."
"$PYTHON" manage.py migrate --noinput

echo "[SITU] Iniciando servidor en http://127.0.0.1:$PORT"
exec "$PYTHON" manage.py runserver "0.0.0.0:$PORT"
