#!/bin/bash
# make-universal.sh
# Bundles qemu-system-x86_64, qemu-system-aarch64, qemu-system-riscv64
# into a single self-extracting file: wvm-system-universal
# Intended to be invoked via the `wvm` CLI, not called directly.

set -e

SRC_DIR="${1:-build}"
OUT="wvm-system-universal"
TMP_TAR="$(mktemp)"

echo "Bundling binaries from $SRC_DIR..."

tar -czf "$TMP_TAR" -C "$SRC_DIR" \
  qemu-system-x86_64 \
  qemu-system-aarch64 \
  qemu-system-riscv64

{
cat << 'HEADER'
#!/bin/bash
# wvm-system-universal - WVM binary backend (internal use)
# Not meant to be called directly. Use `wvm run <vm-name>` instead.
# Requires WVM_ARCH env var to be set to x86_64, aarch64, or riscv64.

set -e

ARCH="$WVM_ARCH"

case "$ARCH" in
  x86_64|aarch64|riscv64) ;;
  *)
    echo "Error: wvm-system-universal must be invoked via 'wvm run'." >&2
    echo "(WVM_ARCH env var missing or invalid: '$ARCH')" >&2
    exit 1
    ;;
esac

CACHE_DIR="${WVM_CACHE_DIR:-$HOME/.wvm/bin-cache}"
BIN_NAME="qemu-system-$ARCH"
BIN_PATH="$CACHE_DIR/$BIN_NAME"

if [ ! -x "$BIN_PATH" ]; then
  mkdir -p "$CACHE_DIR"
  ARCHIVE_LINE=$(awk '/^__ARCHIVE_BELOW__/{print NR + 1; exit 0; }' "$0")
  tail -n +"$ARCHIVE_LINE" "$0" | tar -xzf - -C "$CACHE_DIR"
  chmod +x "$CACHE_DIR"/qemu-system-x86_64 "$CACHE_DIR"/qemu-system-aarch64 "$CACHE_DIR"/qemu-system-riscv64
fi

exec "$BIN_PATH" "$@"

__ARCHIVE_BELOW__
HEADER
cat "$TMP_TAR"
} > "$OUT"

chmod +x "$OUT"
rm -f "$TMP_TAR"

echo "Created $OUT ($(du -h "$OUT" | cut -f1))"
