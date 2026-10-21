#!/usr/bin/env bash
# One-command setup for Black Forge on macOS / Linux.
# Made with love Rohan Malyadri From Obscuron X Labs
set -e
cd "$(dirname "$0")"

echo "=== Black Forge setup ==="

# 1. Find a Python 3.10+ interpreter (macOS ships 3.9, which is too old)
PY=""
for cand in python3.13 python3.12 python3.11 python3.10 python3 python; do
  if command -v "$cand" >/dev/null 2>&1 && \
     "$cand" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null; then
    PY="$cand"; break
  fi
done
if [ -z "$PY" ]; then
  echo "ERROR: Black Forge needs Python 3.10 or newer, and none was found."
  echo "  macOS:  brew install python@3.12   (or download from https://www.python.org/downloads/)"
  echo "  Ubuntu: sudo apt install python3.12 python3.12-venv"
  echo "Then run ./setup.sh again."
  exit 1
fi
echo "Using $($PY --version) ($(command -v $PY))"

# 2. Virtual environment + dependencies
if [ ! -x .venv/bin/python ]; then
  "$PY" -m venv .venv || { echo "ERROR: could not create a venv. On Ubuntu: sudo apt install python3-venv"; exit 1; }
fi
.venv/bin/python -m pip install --quiet --upgrade pip
echo "Installing dependencies (first run takes a minute)..."
.venv/bin/python -m pip install --quiet -r requirements.txt

# 3. API key
if [ ! -f .env ]; then
  cp .env.example .env
  printf "Paste your Gemini API key (https://aistudio.google.com/apikey), or press Enter to add it later: "
  read -r KEY || true
  if [ -n "$KEY" ]; then
    .venv/bin/python - "$KEY" <<'PYEOF'
import sys
p = ".env"
s = open(p).read().replace("your_gemini_api_key_here", sys.argv[1].strip())
open(p, "w").write(s)
PYEOF
  fi
fi

chmod +x blackforge
echo
echo "Done! Try:"
echo "  ./blackforge about"
echo "  ./blackforge chat \"List the files in this folder\""
echo "  ./blackforge optimize --goal \"Launch Black Forge\" --platform LinkedIn --draft \"Black Forge is an AI agent for your terminal.\""
