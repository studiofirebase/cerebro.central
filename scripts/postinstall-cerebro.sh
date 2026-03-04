#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ -z "${PREFIX:-}" || ! -d "${PREFIX:-}" ]]; then
  exit 0
fi

if [[ ! -w "$PREFIX/bin" ]]; then
  exit 0
fi

if [[ ! -f "$HOME/.cerebro-central.env" ]]; then
  cat > "$HOME/.cerebro-central.env" <<'EOF'
LLM_PROVIDER=vertex
VERTEX_AUTH_MODE=env
VERTEX_PROJECT_ID=
VERTEX_LOCATION=us-central1
VERTEX_MODEL=gemini-1.5-flash
VERTEX_API_KEY=
VERTEX_ACCESS_TOKEN=
EOF
fi

cat > "$PREFIX/bin/cerebro" <<EOF
#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

PROJECT_ROOT="$ROOT_DIR"

if [[ -f "\$HOME/.cerebro-central.env" ]]; then
  set -a
  source "\$HOME/.cerebro-central.env"
  set +a
fi

cd "\$PROJECT_ROOT"
exec "\$PROJECT_ROOT/cerebro" "\$@"
EOF

chmod +x "$PREFIX/bin/cerebro"

echo "[cerebro] comando instalado em $PREFIX/bin/cerebro"
