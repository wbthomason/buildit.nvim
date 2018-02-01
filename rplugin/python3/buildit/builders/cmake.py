''' Builder definitions for CMake '''
import os


def cmake_check_build_dir(cmakelist_dir):
  '''Makes the build directory if it does not already exist'''
  build_dir = os.path.join(cmakelist_dir, 'build')
  if not os.path.isdir(build_dir):
    os.mkdir(build_dir)

  return True


cmake = {
    'sig': r'CMakeLists\.txt',
    'cmd': 'cmake .. && make',
    'func': cmake_check_build_dir,
    'ft': None,
    'subdir': 'build',
    'shell': True
}
