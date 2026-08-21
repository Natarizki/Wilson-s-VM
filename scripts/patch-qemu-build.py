import sys

path = sys.argv[1]

with open(path) as f:
    content = f.read()

old_targets = '''    local QEMU_TARGETS=""

    # System emulation.
    QEMU_TARGETS+="aarch64-softmmu,"
    QEMU_TARGETS+="arm-softmmu,"
    QEMU_TARGETS+="i386-softmmu,"
    QEMU_TARGETS+="m68k-softmmu,"
    QEMU_TARGETS+="ppc64-softmmu,"
    QEMU_TARGETS+="ppc-softmmu,"
    QEMU_TARGETS+="riscv32-softmmu,"
    QEMU_TARGETS+="riscv64-softmmu,"
    QEMU_TARGETS+="x86_64-softmmu,"

    # User mode emulation.
    QEMU_TARGETS+="aarch64-linux-user,"
    QEMU_TARGETS+="arm-linux-user,"
    QEMU_TARGETS+="i386-linux-user,"
    QEMU_TARGETS+="m68k-linux-user,"
    QEMU_TARGETS+="ppc64-linux-user,"
    QEMU_TARGETS+="ppc-linux-user,"
    QEMU_TARGETS+="riscv32-linux-user,"
    QEMU_TARGETS+="riscv64-linux-user,"
    QEMU_TARGETS+="x86_64-linux-user"'''

new_targets = '''    local QEMU_TARGETS=""

    # WVM: stripped to 3 target architectures only.
    QEMU_TARGETS+="aarch64-softmmu,"
    QEMU_TARGETS+="riscv64-softmmu,"
    QEMU_TARGETS+="x86_64-softmmu"'''

if old_targets not in content:
    print("ERROR: old_targets block not found, aborting patch")
    sys.exit(1)

content = content.replace(old_targets, new_targets)
content = content.replace('--enable-kvm \\', '--disable-kvm \\')

with open(path, "w") as f:
    f.write(content)

print("Patch applied successfully")
