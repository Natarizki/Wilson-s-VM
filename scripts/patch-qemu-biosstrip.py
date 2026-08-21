import sys
import re

path = sys.argv[1]

with open(path) as f:
    content = f.read()

# Strip the edk2 UEFI blob list (fds array) down to empty.
fds_pattern = re.compile(r"fds = \[\s*.*?\]", re.MULTILINE | re.DOTALL)
content, fds_count = fds_pattern.subn("fds = [\n  ]", content)
print(f"Stripped fds (UEFI blobs) block: {fds_count} match")

# Strip the blobs array down to only bios.bin, bios-256k.bin (SeaBIOS)
# and the two OpenSBI RISC-V firmware files.
blobs_pattern = re.compile(r"blobs = \[\s*.*?\]", re.MULTILINE | re.DOTALL)

new_blobs = """blobs = [
  'bios.bin',
  'bios-256k.bin',
  'opensbi-riscv32-generic-fw_dynamic.bin',
  'opensbi-riscv64-generic-fw_dynamic.bin',
]"""

content, blobs_count = blobs_pattern.subn(new_blobs, content)
print(f"Stripped blobs block: {blobs_count} match")

if fds_count == 0 or blobs_count == 0:
    print("ERROR: one or more expected blocks not found, aborting patch")
    sys.exit(1)

with open(path, "w") as f:
    f.write(content)

print("BIOS/firmware strip patch applied successfully")
