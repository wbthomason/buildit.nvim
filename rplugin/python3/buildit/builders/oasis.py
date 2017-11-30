''' Builder definitions for OCaml Oasis '''

import os
from subprocess import run


def oasis_check_build_files(oasis_dir):
  '''Ensures that the Oasis configure step has been run'''
  files_exist = True
  for build_file in ['setup.ml', 'configure', 'Makefile']:
    path = os.path.join(oasis_dir, build_file)
    files_exist &= os.path.exists(path)

  if not files_exist:
    oasis_result = run(['oasis', 'setup', '-setup-update', 'dynamic'])
    return oasis_result.returncode == 0

  return True


oasis = {
    'sig': r'_oasis',
    'cmd': 'make',
    'func': oasis_check_build_files,
    'ft': ['ocaml'],
    'subdir': None,
    'shell': False
}
