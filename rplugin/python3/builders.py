'''Standard builder defintiions and utility functions for BuildIt'''

import os
from subprocess import run


def cmake_check_build_dir(cmakelist_dir):
  '''Makes the build directory if it does not already exist'''
  build_dir = os.path.join(cmakelist_dir, 'build')
  if not os.path.isdir(os.path.join(cmakelist_dir, 'build')):
    os.mkdir(build_dir)

  return True


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


# TODO: More builders?
BUILDER_DEFS = {
  # make
  'make': {'sig': 'Makefile', 'cmd': 'make', 'func': None, 'ft': None},
  # cmake
  'cmake': {'sig': 'CMakeLists.txt', 'cmd': 'make', 'func': cmake_check_build_dir, 'ft': None},
  # cargo
  'cargo': {'sig': 'Cargo.toml|Cargo.lock', 'cmd': 'cargo build', 'func': None, 'ft': 'rust'},
  # go build
  # TODO: I'm not sure if we want go build or go install...
  'go build': {'sig': '', 'cmd': 'go build', 'func': None, 'ft': 'go'},
  # stack build
  'stack': {'sig': 'stack.yaml', 'cmd': 'stack build', 'func': None, 'ft': 'haskell'},
  # oasis build
  'oasis': {'sig': '_oasis', 'cmd': 'make', 'func': oasis_check_build_files, 'ft': 'ocaml'}
}
