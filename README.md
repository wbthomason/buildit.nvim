[![Stories in Ready](https://badge.waffle.io/wbthomason/buildit.nvim.png?label=ready&title=Ready)](https://waffle.io/wbthomason/buildit.nvim)
# buildit.nvim
A better async project builder for Neovim

# Why would I use this?

`buildit` does a good job of automatically detecting the correct builder to use for a given buffer,
and runs said builder in a new process, asynchronously. Further, it does not interfere with your
working directory, and it can handle several simultaneous builds.

What this boils down to is that you can very easily trigger builds for several subprojects, have
them work correctly without having to fiddle around with configuration, and keep editing
uninterrupted.

For more, see [the FAQ](#faq) or the [docs](docs/buildit.txt)

# Installation

Installation with [dein.vim](https://github.com/Shougo/dein.vim) has been tested to work:

```vimscript
 call dein#add('wbthomason/buildit.nvim')
```

I have not tested it myself, but I assume that installation with most other methods will work as
well. The plugin's structure is fairly simple.

Once you've installed, be sure to run `:UpdateRemotePlugins` to register `buildit` with Neovim.

# Usage

`buildit` currently provides two commands and a function. The number of functions is likely to grow
as features are added, but the command interface is likely to stay quite simple (though more
commands may be added for major features).

## Building

Building is what `buildit` does. To build, run `:BuildIt`. Then (in proper operation), the correct
builder will be started in the background.

## Checking on builds

Once you have one or more builders running, use `:BuildItStatus` to pop open a new window with the
current set of running builds and their statuses. Note that `buildit` checks for completed or
failed builds when you run `:BuildItStatus`, and will prune these builds from the list after the
command is run.

## Triggering builds from other contexts

`buildit` also provides the `start_build` function, in case you'd like to trigger a build using
`buildit` from some other plugin or custom interface. All `:BuildIt` does is call `start_build`, so
the behavior is as you'd expect.

# FAQ

## What?

`buildit` builds it. It finds the closest "buildable"<sup id=fn1>[1](#whatsbuildable)</sup> directory to the 
directory of a file you open. If it can't find one, then it asks you what to do (by default, at 
least). Then it runs the appropriate build command asynchronously, and reports and interesting 
results.

Notably, `buildit` does **not** change the working directory. This is so you can have things like 
`fzf` easily search from the project root/wherever, but still build from the appropriate directory.

More features might happen once I think of them/they are suggested.

## But why? Don't we already have Neomake and vim-dispatch and the like?

We sure do, and they mostly work. However, I have a few problems with all of the solutions I've 
found (which I'm sure stem from my improper usage of the existing options, but oh well).

First, some of them (Neomake) try to **do too much**. I have a nice async linting framework already;
I don't want something that tries to do both linter running and compilation/test running (though I 
do acknowledge the similarities between the tasks). I just want something that I can use to trigger 
the right build tool in the right way for whatever buffer I'm currently in.

Second, these existing solutions all seem to fail when you deviate from the pattern of having the 
build files at the top level. While this may be considered a bad practice in many cases, there are a
fair number of projects (e.g. multi-language projects, or projects with several discrete components)
where it doesn't make sense to split each "buildable" project into its own repo. In my experience 
with these sorts of projects, the existing tools often try to build from the wrong directory, or 
otherwise fail to do what I want.

Also, I'm mostly writing this for fun/to try out writing plugins for Neovim. Thus, duplication of 
functionality isn't the worst thing in the world.

# Footnotes

<a name="whatsbuildable">**1:** A "buildable" directory is one that contains some file indicating 
that a build tool is in place, e.g. `Makefile`, `Cargo.toml`, etc.[↩](#a1)</a>
