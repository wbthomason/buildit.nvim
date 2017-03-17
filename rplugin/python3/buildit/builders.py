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


# TODO: More builders!
BUILDER_DEFS = {
    # make
    'make': {'sig': r'Makefile', 'cmd': 'make', 'func': None, 'ft': None, 'subdir': None},
    # cmake
    'cmake': {
        'sig': r'CMakeLists\.txt',
        'cmd': 'cmake .. && make',
        'func': cmake_check_build_dir,
        'ft': None,
        'subdir': 'build'
    },
    # cargo
    'cargo': {
        'sig': r'Cargo\.toml|Cargo\.lock',
        'cmd': 'cargo build',
        'func': None,
        'ft': 'rust',
        'subdir': None
    },
    # go build
    # TODO: I'm not sure if we want go build or go install... This also seems like a dumb thing,
    # having a signature that will match *every* directory. Maybe there's a better option?
    'go build': {'sig': r'', 'cmd': 'go build', 'func': None, 'ft': 'go', 'subdir': None},
    # stack build
    'stack': {
        'sig': r'stack\.yaml',
        'cmd': 'stack build',
        'func': None,
        'ft': 'haskell',
        'subdir': None
    },
    # oasis build
    'oasis': {
        'sig': r'_oasis',
        'cmd': 'make',
        'func': oasis_check_build_files,
        'ft': 'ocaml',
        'subdir': None
    }
}
