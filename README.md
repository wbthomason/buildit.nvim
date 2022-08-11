# buildit.nvim

An async project builder for Neovim.
Compatible with (but not reliant on) VS Code-style `tasks.json` specifications.

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
use {'wbthomason/buildit.nvim', requires = 'nvim-lua/plenary.nvim'}
```

# Usage

TODO rewrite for Lua rewrite of plugin.
