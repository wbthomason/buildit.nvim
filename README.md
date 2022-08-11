[![Stories in Ready](https://badge.waffle.io/wbthomason/buildit.nvim.png?label=ready&title=Ready)](https://waffle.io/wbthomason/buildit.nvim)
[![Github All Releases](https://img.shields.io/github/downloads/wbthomason/buildit.nvim/total.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/maintenance/yes/2018.svg)]()

# buildit.nvim

A better async project builder for Neovim. If you want a builder implemented, comment on [the relevant issue](https://github.com/wbthomason/buildit.nvim/issues/4) or submit a PR.

# Why would I use this?

`buildit` does a good job of automatically detecting the correct builder to use for a given buffer,
and runs said builder in a new process, asynchronously. Further, it does not interfere with your
working directory, and it can handle several simultaneous builds.

What this boils down to is that you can very easily trigger builds for several subprojects, have
them work correctly without having to fiddle around with configuration, and keep editing
uninterrupted.

For more, see [the FAQ](#faq) or the [docs](doc/buildit.txt)

# Installation

Use your favorite plugin manager.

With `packer.nvim`:
```lua
use 'wbthomason/buildit.nvim'
```

# Usage

TODO rewrite for Lua rewrite of plugin.
