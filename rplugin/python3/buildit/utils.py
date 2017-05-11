''' Utility functions for BuildIt not a part of the main plugin class '''

from subprocess import call, DEVNULL
from tempfile import TemporaryFile


def check_ft(builder, filetype):
  '''Filter function to remove builders that require a certain filetype other than the filetype of
  the current buffer.'''
  return builder.get('ft', None) == filetype if builder.get('ft', None) else True


def create_status(build):
  '''Builds a status string from a build'''
  buf_name = build['buffer']
  builder_name = build['builder']
  returncode, err = build['future'].result() if build['future'].done() else (1, None)
  if build['failed']:
    status = "Couldn't start! ⚠"
    error = None
  elif returncode is not None and returncode > 0:
    status = 'Failed ✖'
    error = f'\tError: {err}'
  elif returncode is not None and returncode == 0:
    status = 'Completed ✔'
    error = None
  else:
    status = 'Running...'
    error = None

  return f'{buf_name} ({builder_name}): {status}', error


def run_build(args):
  '''Run the build command using a subprocess call'''
  cmd, execution_dir, shell = args
  errfile = TemporaryFile()
  result = call(cmd, cwd=execution_dir, stdout=DEVNULL, stderr=errfile, shell=shell)
  err = None
  if result != 0:
    errfile.seek(0)
    err = errfile.read()
  errfile.close()
  return result, err
