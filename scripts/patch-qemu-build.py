import sys
import re

path = sys.argv[1]

with open(path) as f:
    content = f.read()

# --- Strip QEMU_TARGETS down to 3 architectures ---
pattern = re.compile(
    r'local QEMU_TARGETS=""\n(?:.*\n)*?\s*QEMU_TARGETS\+="x86_64-linux-user"',
    re.MULTILINE
)

replacement = (
    'local QEMU_TARGETS=""\n\n'
    '    # WVM: stripped to 3 target architectures only.\n'
    '    QEMU_TARGETS+="aarch64-softmmu,"\n'
    '    QEMU_TARGETS+="riscv64-softmmu,"\n'
    '    QEMU_TARGETS+="x86_64-softmmu"'
)

content, count = pattern.subn(replacement, content)
if count == 0:
    print("ERROR: QEMU_TARGETS block not found via regex, aborting patch")
    sys.exit(1)
print(f"Replaced QEMU_TARGETS block ({count} match)")

# --- Disable KVM ---
content, kvm_count = re.subn(r'--enable-kvm\s*\\', '--disable-kvm \\\\', content)
print(f"Replaced --enable-kvm ({kvm_count} match)")

# --- Inject termux_step_post_extract_package() hook to strip BIOS/firmware ---
hook_marker = "termux_step_pre_configure() {"

hook_code = '''termux_step_post_extract_package() {
    # WVM: strip BIOS/firmware blobs, keeping only SeaBIOS and OpenSBI.
    python3 /home/builder/termux-packages/wvm-biosstrip.py \\\\
        "$TERMUX_PKG_SRCDIR/pc-bios/meson.build"
}

termux_step_pre_configure() {'''

if hook_marker not in content:
    print("ERROR: termux_step_pre_configure marker not found, aborting patch")
    sys.exit(1)

content = content.replace(hook_marker, hook_code, 1)
print("Injected termux_step_post_extract_package hook")

with open(path, "w") as f:
    f.write(content)

print("Patch applied successfully")
