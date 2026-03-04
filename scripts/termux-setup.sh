#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

pkg update -y
pkg upgrade -y
pkg install -y python git curl

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-termux.txt

mkdir -p "$HOME"

if [[ ! -f "$HOME/.cerebro-central.env" ]]; then
	cat > "$HOME/.cerebro-central.env" <<'EOF'
LLM_PROVIDER=vertex
VERTEX_AUTH_MODE=env
VERTEX_PROJECT_ID=
VERTEX_LOCATION=us-central1
VERTEX_MODEL=gemini-1.5-flash
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

echo ""
echo "[ok] Ambiente Termux preparado"
echo "[ok] Comando global instalado: cerebro"
echo ""
echo "Configure credenciais em:"
echo "  nano ~/.cerebro-central.env"
echo ""
echo "Use direto:"
echo "  cerebro central"
