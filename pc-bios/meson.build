roms = []
if unpack_edk2_blobs
  fds = [
  ]

  foreach f : fds
    roms += custom_target(f,
                  build_by_default: have_system,
                  output: f,
                  input: files('@0@.bz2'.format(f)),
                  capture: true,
                  install: get_option('install_blobs'),
                  install_dir: qemu_datadir,
                  command: [ bzip2, '-dc', '@INPUT0@' ])
  endforeach
endif

blobs = [
  'opensbi-riscv32-generic-fw_dynamic.bin',
  'opensbi-riscv64-generic-fw_dynamic.bin',
]

if get_option('install_blobs')
  install_data(blobs, install_dir: qemu_datadir, install_mode: 'rw-r--r--')
endif

subdir('descriptors')
subdir('dtb')
subdir('keymaps')
