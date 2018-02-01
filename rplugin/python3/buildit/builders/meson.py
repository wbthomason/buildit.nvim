''' Builder definitions for Meson '''
import os
from subprocess import check_call, DEVNULL, CalledProcessError


def meson_init(meson_dir):
  '''Initialize meson if it hasn't already been (if the build dir isn't there)'''
  if not os.path.isdir(os.path.join(meson_dir, 'build')):
    curr_dir = os.path.curdir
    try:
      os.chdir(meson_dir)
      check_call(['meson', 'build'], stdout=DEVNULL, stderr=DEVNULL)
    except CalledProcessError:
      return False
    finally:
      os.chdir(curr_dir)

  return True

meson = {
    'sig': r'meson\.build',
    'cmd': 'ninja',
    'func': meson_init,
    'ft': None,
    'subdir': 'build',
    'shell': True
}
