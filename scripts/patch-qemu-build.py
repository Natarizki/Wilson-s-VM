import sys
import re

path = sys.argv[1]

with open(path) as f:
    content = f.read()

# Replace the QEMU_TARGETS assignment block using regex, tolerant of whitespace.
# Matches from 'local QEMU_TARGETS=""' up to the last QEMU_TARGETS+= line
# before the closing of that logical block (before CFLAGS+=).
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

new_content, count = pattern.subn(replacement, content)

if count == 0:
    print("ERROR: QEMU_TARGETS block not found via regex, aborting patch")
    sys.exit(1)

print(f"Replaced QEMU_TARGETS block ({count} match)")

# Disable KVM
new_content, kvm_count = re.subn(r'--enable-kvm\s*\\', '--disable-kvm \\\\', new_content)
print(f"Replaced --enable-kvm ({kvm_count} match)")

with open(path, "w") as f:
    f.write(new_content)

print("Patch applied successfully")
