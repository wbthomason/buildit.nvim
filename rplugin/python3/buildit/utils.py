''' Utility functions for BuildIt not a part of the main plugin class '''


def check_ft(builder, filetype):
  '''Filter function to remove builders that require a certain filetype other than the filetype of
  the current buffer.'''
  return builder.get('ft', None) == filetype if builder.get('ft', None) else True


def create_status(build):
  '''Builds a status string from a build'''
  buf_name = build['buffer']
  builder_name = build['builder']
  returncode = build['proc'].poll() if build['proc'] else 1
  if build['failed']:
    status = "Couldn't start!\t⚠"
    error = None
  elif returncode is not None and returncode > 0:
    build['err'].seek(0)
    err = build['err'].read()
    status = 'Failed\t✖'
    error = f'\tError:\t{err}'
  elif returncode is not None and returncode == 0:
    status = 'Completed\t✔'
    error = None
  else:
    status = 'Running...'
    error = None

  return f'{buf_name} ({builder_name}): {status}', error
