#!/data/data/com.termux/files/usr/bin/bash
# install.sh - Installer for WVM (Wilson's Virtual Machine)

set -e

REPO="Natarizki/Wilson-s-VM"
WVM_HOME="$HOME/.wvm"
CLI_SRC="$(dirname "$0")/cli/wvm"

echo "== WVM Installer =="

echo "[1/5] Checking dependencies..."
for pkg in curl git; do
  if ! command -v "$pkg" >/dev/null 2>&1; then
    echo "  Installing $pkg..."
    pkg install -y "$pkg"
  fi
done

echo "[2/5] Setting up ~/.wvm..."
mkdir -p "$WVM_HOME/vms" "$WVM_HOME/run" "$WVM_HOME/bin-cache"

echo "[3/5] Downloading latest wvm-system-universal from GitHub Releases..."
DOWNLOAD_URL="https://github.com/$REPO/releases/latest/download/wvm-system-universal"
curl -fL "$DOWNLOAD_URL" -o "$WVM_HOME/wvm-system-universal"
chmod +x "$WVM_HOME/wvm-system-universal"

echo "[4/5] Installing wvm CLI..."
if [ -f "$CLI_SRC" ]; then
  cp "$CLI_SRC" "$WVM_HOME/wvm"
else
  echo "Error: could not find cli/wvm relative to this script." >&2
  echo "Run install.sh from inside the WVM repo directory." >&2
  exit 1
fi
chmod +x "$WVM_HOME/wvm"

BIN_LINK="$PREFIX/bin/wvm"
ln -sf "$WVM_HOME/wvm" "$BIN_LINK"

echo "[5/5] Done."
echo ""
echo "WVM installed successfully."
echo "Run 'wvm --help' to get started."
