'''BuildIt: A plugin for asynchronous project building from Neovim'''

from builders import BUILDER_DEFS
import neovim
import os


@neovim.plugin
class BuildIt(object):
  '''The main plugin class'''
  def __init__(self, vim):
    self.vim = vim
    self.builds = {}
    self.builders = self.load_builders()

  @neovim.command('BuildIt', range='', nargs='*', sync=True)
  def buildit(self, args, char_range):
    '''Handles the build-triggering command'''
    pass

  @neovim.function('build')
  def start_build(self, args):
    '''Starts a build'''
    pass

  @neovim.command('BuildItStatus', range='', nargs='*', sync=True)
  def buildit_status(self, args, char_range):
    '''Gets the status of all running builds'''
    pass

  @neovim.function('build_status')
  def check_build(self, args):
    '''Checks the status of a build'''
    pass

  def find_builder(self, buf_dir):
    '''Locates the correct builder for the given buffer'''
    pass

  def load_builders(self):
    '''Search the relevant variable and a pre-configured list for builder templates'''
    known_builders = dict(BUILDER_DEFS)
    custom_builders = self.vim.vars.get('buildit_builders', {})
    known_builders.update(custom_builders)
    return known_builders
