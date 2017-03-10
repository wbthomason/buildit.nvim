'''BuildIt: A plugin for asynchronous project building from Neovim'''

import neovim


@neovim.plugin
class BuildIt(object):
  '''The main plugin class'''
  def __init__(self, vim):
    self.vim = vim
    self.builds = []

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
