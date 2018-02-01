''' Builder definitions for Meson '''
import os
from subprocess import check_call, CalledProcessError


def meson_init(meson_dir):
  '''Initialize meson if it hasn't already been (if the build dir isn't there)'''
  if not os.path.isdir(os.path.join(meson_dir, 'build')):
    try:
      check_call("meson build")
    except CalledProcessError:
      return False

  return True

meson = {
    'sig': r'meson\.build',
    'cmd': 'ninja',
    'func': meson_init,
    'ft': None,
    'subdir': 'build',
    'shell': True
}
