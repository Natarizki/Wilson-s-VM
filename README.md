## Wilson's VM

**Wilson's VM** is a strip-down fork of [QEMU](https://www.qemu.org/), build for **lightweight** system emulation
on edge devices. It focuses on modern virtual machine use cases only — legacy boards, alternate host platforms, 
and unused subsystems have been removed to keep the build lean and fast.

## Whats the difference?

**Wilson's VM** have striped down all this systems:
- legacy devices (old, ancient devices)
- **KVM** support (pure MTCG emulation)
- Target achitectures: **ARM64**, **X86_64**, and **RISC-V64**
- **BIOS/FIRMWARE** are strip BIOS/FIRMWARE except **OpenSBI** (required foe RISC-V boot)
- **Trace backend:** fixed to nop (no runtime tracing overhead)
- *Removed**: docs build, bundled test suite, VNC, SPICE
- **Kept*: local GUI display (GTK, SDL)

## How to run

use:
```Bash
wvm create myvm --arch riscv64 --mem 1024 --disk ./disk.img --kernel ./Image
```
to create your own VM
```Bash
wvm run myvm
```
to run (need to specify whats your vm is)
```Bash
wvm list
```
to see all your created VM's
```Bash
wvm status myvm
```
to see the status of your VM
```Bash
wvm delete myvm
```
to delete your unwanted VM

## How to install

to install, you just need to:
```Bash
git clone https://github.com/Natarizki/Wilson-s-VM.git wvm # to clone the repo and turn it to wvm
cd ~wvm # go to the directory
./install.sh # to install the wvm system
```

## How we Compiled it

we compiled it not locally, but using **Github Actions** because my local device was a po5ato
phone (Honest)
we run it in termux (android)
by using the **gh** CLI
what we need to do:
```Bash
gh workflow run build.yml
```
this is used after push

## LICENSE

Because we fork QEMU, we inherits the QEMU's **LICESE**
see at

[COPYING](COPYING)
[COPYING.LIB](COPYING.LIB)
