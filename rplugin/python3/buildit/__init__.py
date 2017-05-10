'''BuildIt: A plugin for asynchronous project building from Neovim'''

import os
import re
import shlex
from subprocess import DEVNULL, call
from tempfile import TemporaryFile

from buildit.builders import BUILDER_DEFS
from buildit.utils import check_ft, create_status

from concurrent.futures import ProcessPoolExecutor as Pool
import neovim


@neovim.plugin
class BuildIt(object):
  '''The main plugin class'''
  def __init__(self, vim):
    self.vim = vim
    self.builds = {}
    self.builders = self.load_builders()
    self.known_paths = {}
    self.config = {}
    self.pool = Pool()

  def load_config(self):
    '''Loads the plugin configuration'''
    config = {
        'statusloc': self.vim.vars.get('buildit_status_location', 'right'),
        'promptmult': self.vim.vars.get('buildit_prompt_multiple', False),
        'pruneafter': self.vim.vars.get('buildit_prune_after_status', True)
    }

    return config

  @neovim.command('BuildIt', sync=False)
  def buildit(self):
    '''Handles the build-triggering command'''
    self.start_build()

  @neovim.function('Build', sync=False)
  def start_build(self):
    '''Starts a build'''
    if self.config == {}:
      self.config = self.load_config()
    current_buffer = self.vim.current.buffer
    buf_path, fname = os.path.split(current_buffer.name)
    builder_name, build_path = self.find_builder(buf_path, current_buffer.options['ft'])
    if builder_name is None:
      self.vim.command('echom "No builder found!"')
    else:
      builder = self.builders[builder_name]
      ready_func = builder.get('func', None)
      self.add_job(builder_name, build_path, fname, ready_func(build_path) if ready_func else True)

  @neovim.command('BuildItStatus', sync=False)
  def buildit_status(self):
    '''Gets the status of all running builds'''
    if self.config == {}:
      self.config = self.load_config()
    statuses = [create_status(build) for build in self.builds.values()]
    location = self.config['statusloc']
    if location == 'right':
      self.vim.command('botright vnew')
      self.vim.command('vertical resize 40')
    elif location == 'left':
      self.vim.command('topleft vnew')
      self.vim.command('vertical resize 40')
    elif location == 'bottom':
      self.vim.command('bot new')
      self.vim.command('resize 20')
    elif location == 'top':
      self.vim.command('top new')
      self.vim.command('resize 20')

    self.vim.command('nnoremap <buffer> q :bd!<CR>')
    # TODO: It is not clear why center() over-pads, but this stupid hack seems to fix it. Still,
    # stupid hacks should be removed wherever possible.
    width = self.vim.current.window.width - 4
    self.vim.current.line = '============================'.center(width)
    self.vim.current.buffer.append('|      BuildIt Status      |'.center(width))
    self.vim.current.buffer.append('============================'.center(width))
    self.vim.current.buffer.append('')
    for status, error in statuses:
      self.vim.current.buffer.append(status)
      if error:
        self.vim.current.buffer.append(error)

    if self.config['pruneafter']:
      self.prune()

  @neovim.command('BuildItPrune', sync=False)
  def prune_builds(self):
    '''Handles the build-pruning command'''
    self.prune()

  @neovim.function('Prune', sync=False)
  def prune(self):
    '''Remove builds which have failed or finished'''
    pruned_builds = dict(self.builds)
    for build_key in self.builds:
      build = self.builds[build_key]
      if build['failed'] or build['future'].done():
        if build['err'] != DEVNULL:
          build['err'].close()

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
          builder_names = self.ft_or_generic(builder_names, filetype)
          if self.config['promptmult']:
            builder_name = self.prompt_for_preference(builder_names)
          else:
            builder_name = builder_names[0]
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
      builder_names = self.ft_or_generic(options, filetype)
      if self.config['promptmult']:
        builder_name = self.prompt_for_preference(builder_names)
      else:
        builder_name = builder_names[0]
      break
    return builder_name, search_dir

  def prompt_for_preference(self, builder_names):
    '''Asks the user which of the builder options they prefer'''
    prompt = f'Enter the index of your preferred builder: {builder_names}: '
    index = self.vim.funcs.input(prompt)
    return builder_names[index]

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
      if not build['failed'] and not build['future'].done():
        return

    builder = self.builders[builder_name]
    future = None
    if ready:
      subdir = builder.get('subdir', None)
      execution_dir = os.path.join(build_path, subdir if subdir else '')
      errfile = TemporaryFile()
      cmd = builder['cmd'] if builder['shell'] else shlex.split(builder['cmd'])

      def done_callback(future):
        ''' Handle status display when the future ends '''
        key = future.key
        build = self.builds[key]
        result, error = create_status(build)
        if error:
          echo_fmt = f'echohl Error | echom "{result}" | echohl Normal'
        else:
          echo_fmt = f'echom "{result}"'
        self.vim.command(echo_fmt)

      future = self.pool.submit(
          call,
          cmd,
          cwd=execution_dir,
          stdout=DEVNULL,
          stderr=errfile,
          shell=builder['shell']
      )

      future.key = key
      future.add_done_callback(done_callback)

    build = {
        'builder': builder_name,
        'buffer': fname,
        'failed': not ready,
        'future': future,
        'err': errfile
    }

    self.builds[key] = build

  def ft_or_generic(self, options, filetype):
    '''Selects the ft-matching builder option if one exists, and return the first generic option if
    no ft-match exists.'''
    ft_options = [name for name in options if self.builders[name].get('ft', None) == filetype]
    return ft_options if ft_options else options
