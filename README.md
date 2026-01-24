log21
=====

![version](https://img.shields.io/pypi/v/log21)
![stars](https://img.shields.io/github/stars/MPCodeWriter21/log21)
![forks](https://img.shields.io/github/forks/MPCodeWriter21/log21)
![repo size](https://img.shields.io/github/repo-size/MPCodeWriter21/log21)
[![CodeFactor](https://www.codefactor.io/repository/github/mpcodewriter21/log21/badge)](https://www.codefactor.io/repository/github/mpcodewriter21/log21)

A simple logging package that helps you log colorized messages in Windows console and
other operating systems.

Features
--------

+ Colors : The main reason for this package was to log text in the Windows console with
  the support of ANSI colors.
+ Argument parsing : log21's argument parser can be used like python's argparse, but it
  also colorizes the output.
+ Logging : A similar logger to logging. Logger but with colorized output and other
  options such as levelname modifications. It can also decolorize the output if you want
  to log into a file.
+ Pretty printing : Have you ever wanted to colorize the output of the pprint module?
  log21's pretty printer can do that.
+ Tree printing : You can pass a dict or list to `log21.tree_print` function, and it
  will print it in a tree-like structure. It's also colorized XD.
+ ProgressBar : log21's progress bar can be used to show progress of a process in a
  beautiful way.
+ LoggingWindow : Helps you to log messages and debug your code in a window other than
  the console.
+ CrashReporter : log21's crash reporter can be used to report crashes in different
  ways. You can use it to log crashes to console or files or use it to receive crash
  reports of your program through email. And you can also define your own crash
  reporter functions and use them instead!
+ Argumentify : You can use the argumentify feature to decrease the number of lines you
  need to write to parse command-line arguments. It's colored by the way!
+ Any idea? Feel free to [open an issue](https://github.com/MPCodeWriter21/log21/issues)
  or submit a pull request.

![Issues](https://img.shields.io/github/issues/MPCodeWriter21/log21)
![contributors](https://img.shields.io/github/contributors/MPCodeWriter21/log21)

Installation
------------

Well, this is a python package so the first thing you need is python.

If you don't have python installed, please visit [Python.org](https://python.org) and
install the latest version of python.

Then you can install log21 using pip module:

```bash
python -m pip install log21 -U
```

Or you can clone [the repository](https://github.com/MPCodeWriter21/log21) and run:

```bash
pip install .
```

Or let the pip get it using git:

```bash
pip install git+https://github.com/MPCodeWriter21/log21
```

Changelog
---------

### v3.0.0

This release introduces a cleaned-up internal structure, stricter naming conventions,
and several quality-of-life improvements. While most users will not notice behavioral
changes, **v3 contains breaking changes for code that relies on internal imports or
specific exception names**.

#### Breaking Changes

+ **Internal module renaming and normalization**
  + All internal modules were renamed to lowercase and, in some cases, split or
    reorganized.
  + Imports such as `log21.Colors`, `log21.Logger`, `log21.ProgressBar`, etc. are no
    longer valid.
  + Users importing from internal modules must update their imports to the new module
    names.
  + Public imports from `log21` remain supported.

+ **Argumentify exception renames**
  + Several exceptions were renamed to follow a consistent `*Error` naming convention:
    + `TooFewArguments` → `TooFewArgumentsError`
    + `RequiredArgument` → `RequiredArgumentError`
    + `IncompatibleArguments` → `IncompatibleArgumentsError`
  + Code that explicitly raises or catches these exceptions must be updated.

#### Changes

+ **Crash reporter behavior improvement**
  + Prevented the default file crash reporter from creating `.crash_report` files when it
    is not actually used.
  + Implemented using an internal `FakeModule` helper.

+ **Argparse compatibility update**
  + Bundled and used the Python 3.13 `argparse` implementation to ensure consistent
    behavior across supported Python versions.

+ **Progress bar module rename**
  + Renamed the internal progress bar module to `progress_bar` for consistency with the
    new naming scheme.
  + This will not break the usages of `log21.progress_bar(...)` since the call
    functionality was added to the module using the `FakeModule` helper.

+ **Examples added and updated**
  + Added new example code files.
  + Updated existing examples to match the v3 API and conventions.

#### Fixes

+ Resolved various linting and static-analysis issues across the codebase.
+ Addressed minor compatibility issues uncovered by running linters and pre-commit hooks.
+ Resolved errors occurring in environments with newer versions of argparse.

#### Internal and Maintenance Changes

+ Migrated the build system configuration to `uv`.
+ Updated Python version classifiers and set the supported Python version to 3.9+.
+ Added `vermin` to the pre-commit configuration.
+ Updated `.gitignore`, license metadata, and tool configurations.
+ Silenced and resolved a large number of linter warnings.
+ General internal refactoring with no intended user-visible behavioral changes.

#### Notes

+ There are **no intentional behavioral changes** in logging output, argument parsing
  logic, or UI components.
+ Most projects will require **minimal or no changes** unless they depend on internal
  modules or renamed exceptions.
+ See [MIGRATION-V2-V3.md](https://github.com/MPCodeWriter21/log21/blob/master/MIGRATION-V2-V3.md)
for detailed upgrade instructions.

[Full CHANGELOG](https://github.com/MPCodeWriter21/log21/blob/master/CHANGELOG.md)

Usage Examples
---------------

See [EXAMPLES.md](https://github.com/MPCodeWriter21/log21/blob/master/EXAMPLES.md)

About
-----

Author: CodeWriter21 (Mehrad Pooryoussof)

GitHub: [MPCodeWriter21](https://github.com/MPCodeWriter21)

Telegram Channel: [@CodeWriter21](https://t.me/CodeWriter21)

### License

![License](https://img.shields.io/github/license/MPCodeWriter21/log21)

[apache-2.0](http://www.apache.org/licenses/LICENSE-2.0)

### Donate

In order to support this project you can donate some crypto of your choice 8D

[Donate Addresses](https://github.com/MPCodeWriter21/log21/blob/master/DONATE.md)

Or if you can't, give [this project](https://github.com/MPCodeWriter21/log21) a star on
GitHub :)

References
----------

+ ANSI Color Codes (Wikipedia):
[https://en.wikipedia.org/wiki/ANSI_escape_code](https://en.wikipedia.org/wiki/ANSI_escape_code#Colors)
