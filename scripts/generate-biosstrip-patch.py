import sys
import re
import shutil
import subprocess

orig_path = sys.argv[1]      # path to original pc-bios/meson.build
patch_output = sys.argv[2]   # where to write the .patch file

with open(orig_path) as f:
    original = f.read()

content = original

fds_pattern = re.compile(r"fds = \[\s*.*?\]", re.MULTILINE | re.DOTALL)
content, fds_count = fds_pattern.subn("fds = [\n  ]", content)
print(f"Stripped fds (UEFI blobs) block: {fds_count} match")

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
    print("ERROR: one or more expected blocks not found, aborting")
    sys.exit(1)

# Write modified version to a temp file, then diff against original.
modified_path = orig_path + ".wvm-modified"
with open(modified_path, "w") as f:
    f.write(content)

# Generate a unified diff with paths relative to source root (a/pc-bios/... b/pc-bios/...),
# matching the format 'patch -p1' expects (used by termux_step_patch_package).
result = subprocess.run(
    ["diff", "-u",
     f"a/pc-bios/meson.build", f"b/pc-bios/meson.build"],
    input=None,
    capture_output=True
)

# diff doesn't read file content via 'input', so build the diff differently:
result = subprocess.run(
    ["diff", "-u", "--label", "a/pc-bios/meson.build", "--label", "b/pc-bios/meson.build",
     orig_path, modified_path],
    capture_output=True, text=True
)

# diff exit code 1 means differences found (expected), 0 means no diff, >1 means error
if result.returncode not in (0, 1):
    print(f"ERROR: diff failed with code {result.returncode}: {result.stderr}")
    sys.exit(1)

with open(patch_output, "w") as f:
    f.write(result.stdout)

print(f"Patch written to {patch_output} ({len(result.stdout)} bytes)")
