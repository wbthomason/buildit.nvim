# buildit.nvim
A better async project builder for Neovim

# Installation

There will be instructions once there's something to install.

# Usage

There will be instructions once there's something to use.

# FAQ

## What?

`buildit` builds it. It finds the closest "buildable"^[1](#whatsbuildable)^ directory to the 
directory of a file you open. If it can't find one, then it asks you what to do (by default, at 
least). Then it runs the appropriate build command asynchronously, and reports and interesting 
results.

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

<a name="whatsbuildable">**1: **A "buildable" directory is one that contains some file indicating 
that a build tool is in place, e.g. `Makefile`, `Cargo.toml`, etc.</a>
