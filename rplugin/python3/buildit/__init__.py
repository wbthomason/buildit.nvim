'''BuildIt: A plugin for asynchronous project building from Neovim'''

import os
import re
import shlex
from subprocess import Popen, DEVNULL

import neovim

from buildit.builders import BUILDER_DEFS


@neovim.plugin
class BuildIt(object):
  '''The main plugin class'''
  def __init__(self, vim):
    self.vim = vim
    self.builds = {}
    self.builders = self.load_builders()
    self.known_paths = {}
    self.config = {
        'statusloc': vim.vars.get('buildit_status_location', 'right'),
        'promptmult': vim.vars.get('buildit_prompt_multiple', False),
        'pruneafter': vim.vars.get('buildit_prune_after_status', True),
        'showout': vim.vars.get('buildit_show_output', False)
    }

  @neovim.command('BuildIt', range='', nargs='*', sync=True)
  def buildit(self, args, char_range):
    '''Handles the build-triggering command'''
    self.start_build(args)

  @neovim.function('Build')
  def start_build(self, args):
    '''Starts a build'''
    current_buffer = self.vim.current.buffer
    buf_path, fname = os.path.split(current_buffer.name)
    builder_name, build_path = self.find_builder(buf_path, current_buffer.options['ft'])
    builder = self.builders[builder_name]
    ready_func = builder.get('func', None)
    self.add_job(builder_name, build_path, fname, ready_func(build_path) if ready_func else True)

  @neovim.command('BuildItStatus', range='', nargs='*', sync=True)
  def buildit_status(self, args, char_range):
    '''Gets the status of all running builds'''
    statuses = [create_status(build) for build in self.builds.values()]
    location = self.config['statusloc']
    if location == 'right':
      self.vim.command('botright vnew')
      self.vim.command('vertical resize 40%')
    elif location == 'left':
      self.vim.command('topleft vnew')
      self.vim.command('vertical resize 40%')
    elif location == 'bottom':
      self.vim.command('bot new')
      self.vim.command('horizontal resize 40%')
    elif location == 'top':
      self.vim.command('top new')
      self.vim.command('horizontal resize 40%')

    self.vim.command('nnoremap <buffer> q :bd!<CR>')
    for status in statuses:
      self.vim.current.buffer.append(status)

    if self.config['pruneafter']:
      self.prune()

  @neovim.command('BuildItPrune', range='', nargs='*', sync=True)
  def prune_builds(self, args, char_range):
    '''Handles the build-pruning command'''
    self.prune()

  @neovim.function('Prune')
  def prune(self):
    '''Remove builds which have failed or finished'''
    for build_key in self.builds:
      build = self.builds[build_key]
      pruned_builds = dict(self.builds)
      if build['failed'] or build['proc'].returncode is not None:
        del pruned_builds[build_key]
      self.builds = pruned_builds

  def find_builder(self, buf_dir, filetype):
    '''Locates the correct builder for the given buffer'''
    prefixes = [(path, os.path.commonprefix([path, buf_dir])) for path in self.known_paths]
    # Options for builders are the builders associated with any path that is a prefix for
    # the current path
    options = [path for path, prefix in prefixes if path == prefix]
    if options:
      # Pick the most specific option that works with the current filetype.
      options = sorted(options, key=len, reverse=True)
      for option in options:
        builder_names = self.known_paths[option]
        builder_names = [name for name in builder_names if check_ft(self.builders[name], filetype)]
        if builder_names:
          builder_name = self.ft_or_generic(builder_names, filetype)
          return builder_name, option

    # If we didn't find anything that works, already, it's time to search upward.
    search_dir = buf_dir[:]
    builder_name = None
    while search_dir != '/':
      files = '    '.join(os.listdir(search_dir))
      options = [name for name in self.builders if self.builders[name]['sig'].search(files)]
      options = [name for name in options if check_ft(self.builders[name], filetype)]
      # If there's nothing matching the files and filetype, move up a directory
      if not options:
        search_dir = os.path.dirname(search_dir)
        continue

      # Prefer a more specific builder, i.e. one with a matching filetype
      builder_name = self.ft_or_generic(options, filetype)
      break
    return builder_name, search_dir

  def load_builders(self):
    '''Search the relevant variable and a pre-configured list for builder templates'''
    known_builders = dict(BUILDER_DEFS)
    custom_builders = self.vim.vars.get('buildit_builders', {})
    known_builders.update(custom_builders)
    for name in known_builders:
      known_builders[name]['sig'] = re.compile(known_builders[name]['sig'])
    return known_builders

  def add_job(self, builder_name, build_path, fname, ready):
    '''Adds a job in the correct state to the current set of builds'''
    key = (build_path, builder_name)
    if key in self.builds:
      build = self.builds[key]
      if not build['failed'] and build['proc'].poll() is None:
        return

    builder = self.builders[builder_name]
    proc = None
    if ready:
      subdir = builder.get('subdir', None)
      execution_dir = os.path.join(build_path, subdir if subdir else '')
      proc = Popen(
          shlex.split(builder['cmd']),
          cwd=execution_dir,
          stdout=DEVNULL,
          stderr=DEVNULL
      )

    build = {
        'builder': builder_name,
        'buffer': fname,
        'failed': not ready,
        'proc': proc
    }

    self.builds[key] = build

  def ft_or_generic(self, options, filetype):
    '''Selects the ft-matching builder option if one exists, and return the first generic option if
    no ft-match exists.'''
    ft_options = [name for name in options if self.builders[name].get('ft', None) == filetype]
    return ft_options[0] if ft_options else options[0]


def check_ft(builder, filetype):
  '''Filter function to remove builders that require a certain filetype other than the filetype of
  the current buffer.'''
  return builder.get('ft', None) == filetype if builder.get('ft', None) else True


def create_status(build):
  '''Builds a status string from a build'''
  buf_name = build['buffer']
  builder_name = build['builder']
  returncode = build['proc'].poll() if build['proc'] else 1
  if build['failed'] or (returncode and returncode > 0):
    status = 'Failed\t✖'
  elif returncode == 0:
    status = "Completed\t✔"
  else:
    status = "Running..."
  return f'{buf_name} ({builder_name}): {status}'
