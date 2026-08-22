import sys
import re
import subprocess

# args: <src_dir> <output_patch_dir>
src_dir = sys.argv[1]
patch_dir = sys.argv[2]

def strip_configs(content, names):
    count = 0
    for name in names:
        pattern = re.compile(
            r'(config ' + re.escape(name) + r'\n(?:.*\n)*?\s*default )y',
            re.MULTILINE
        )
        content, n = pattern.subn(r'\g<1>n', content)
        count += n
    return content, count

def make_patch(rel_path, names, patch_name):
    full_path = f"{src_dir}/{rel_path}"
    with open(full_path) as f:
        original = f.read()

    modified, count = strip_configs(original, names)
    print(f"{rel_path}: stripped {count}/{len(names)} configs")

    if count == 0:
        print(f"WARNING: no configs stripped in {rel_path}, skipping patch")
        return

    modified_path = full_path + ".wvm-modified"
    with open(modified_path, "w") as f:
        f.write(modified)

    result = subprocess.run(
        ["diff", "-u", "--label", f"a/{rel_path}", "--label", f"b/{rel_path}",
         full_path, modified_path],
        capture_output=True, text=True
    )

    if result.returncode not in (0, 1):
        print(f"ERROR: diff failed for {rel_path}: {result.stderr}")
        sys.exit(1)

    patch_path = f"{patch_dir}/{patch_name}"
    with open(patch_path, "w") as f:
        f.write(result.stdout)
    print(f"Patch written: {patch_path} ({len(result.stdout)} bytes)")

# x86_64: strip ISAPC, I440FX
make_patch("hw/i386/Kconfig", ["ISAPC", "I440FX"], "legacy-strip-i386.patch")

# ARM: strip legacy dev boards, keep ARM_VIRT, SBSA_REF, RASPI
arm_strip = [
    "CUBIEBOARD", "DIGIC", "EXYNOS4", "INTEGRATOR", "MAX78000FTHR", "MPS3R",
    "MUSCA", "MUSICPAL", "NETDUINO2", "NETDUINOPLUS2", "OLIMEX_STM32_H405",
    "REALVIEW", "SABRELITE", "STELLARIS", "STM32VLDISCOVERY", "COLLIE", "SX1",
    "VERSATILE", "VEXPRESS", "ZYNQ", "ALLWINNER_H3", "ALLWINNER_R40",
    "B_L475E_IOT01A", "XLNX_ZYNQMP_ARM", "XLNX_VERSAL", "NPCM7XX", "NPCM8XX",
    "FSL_IMX25", "FSL_IMX31", "ASPEED_SOC", "MPS2", "FSL_IMX7",
    "FSL_IMX8MP_EVK", "FSL_IMX8MM_EVK", "FSL_IMX6UL", "MICROBIT",
    "EMCRAFT_SF2", "AXIADO_EVK"
]
make_patch("hw/arm/Kconfig", arm_strip, "legacy-strip-arm.patch")

# RISC-V: strip vendor boards, keep RISCV_VIRT, SPIKE
riscv_strip = [
    "MICROCHIP_PFSOC", "MICROBLAZE_V", "OPENTITAN", "SHAKTI_C", "SIFIVE_E",
    "SIFIVE_U", "TENSTORRENT", "XIANGSHAN_KUNMINGHU", "MIPS_BOSTON_AIA", "K230"
]
make_patch("hw/riscv/Kconfig", riscv_strip, "legacy-strip-riscv.patch")

print("Done generating legacy device strip patches")
