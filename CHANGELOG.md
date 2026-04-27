log21
=====

Help this project by [Donation](DONATE.md)

Changes
-------

### v3.3.1

Get rid of `invalid NoneType value` error message.

In the previous versions, if you used an optional union type such as `int | float | None`
which ended with `None`, you'd get an error saying `invalid NoneType value` that didn't
make any sense to the user. The code has been updated to use the name of the last
non-None type for the error message in these situations.

#### v3.3.1 update demonstration

```python
import log21
from log21.helper_types import FileSize


def main(min_size: FileSize | None = None, max_size: FileSize | None = None) -> None:
    log21.info("Min Size: %s, Max Size: %s", args=(min_size, max_size))

if __name__ == "__main__":
    log21.argumentify(main)
```

Before v3.3.1:

```shell
$ python test.py -m Hello
usage: test.py [-h] [--min-size MIN_SIZE] [--max-size MAX_SIZE]

test.py: error: argument --min-size/-m: invalid NoneType value: 'Hello'
```

With v3.3.1 update:

```shell
$ python test.py -m Hello
usage: test.py [-h] [--min-size MIN_SIZE] [--max-size MAX_SIZE]

test.py: error: argument --min-size/-m: invalid FileSize value: 'Hello'
```

### v3.3.0

Add `log21.helper_types` module.

This module contains a collection of useful types meant for using with argument parser
to parse CLI arguments to more usable formats.

- `FileSize`: Can take `str` and `int` values. Will convert human inputs such as "121 KB",
  "21MiB", or "4.56 GB" to bytes. Can also be used to represent bytes value in more
  human-readable formats.

For even more control you can still define Logger, Handlers, and Formatters manually.

#### Example of `FileSize` usage

```python
from pathlib import Path

import log21
from log21.helper_types import FileSize


def main(path: Path, min_size: FileSize, max_size: FileSize, /):
    log21.info(
        "Files that are smaller than %s or bigger than %s will be ignored.",
        args=(min_size, max_size),
    )

    for file in path.iterdir():
        if not file.is_file():
            continue
        if min_size <= (size := file.stat().st_size) <= max_size:
            log21.print(
                "`%s` is %s.",
                args=(file, FileSize(size).humanize(binary=False, fmt="%.4f")),
            )


if __name__ == "__main__":
    log21.argumentify(main)
```

Example usage and output:

```shell
$ uv run test.py . "1.23MiB" "0.5 GB"
[21:21:21] [INFO] Files that are smaller than 1.23 MiB or bigger than 476.84 MiB will be
ignored.
`myfile21.zip` is 35.1856 MB.
```

### v3.2.0

Add `file_mode` and `file_encoding` parameters to `get_logger` for finer control over
the way a simple logger handles files.

For even more control you can still define Logger, Handlers, and Formatters manually.

#### Example of using `get_logger` with a file

```python
import log21

logger = log21.get_logger(
    "My File Logger", show_level=False, show_time=True, file="myapp.log", file_mode="a",
    file_encoding="utf-8"
)

logger.info("Hello World!")
```

### v3.1.0

Change the way `argumentify` handles function parameters to argument-parser arguments
conversion.

- `POSITIONAL_ONLY` and `VAR_POSITIONAL` parameters will be positional arguments.
- `POSITIONAL_OR_KEYWORD` and `KEYWORD_ONLY` parameters have flags assigned to them.
- `POSITIONAL_OR_KEYWORD` parameters will be required if at least one `KEYWORD_ONLY`
  parameter is there, otherwise they are optional.
- `VAR_KEYWORD` parameters are still not supported.

#### Example 1

```python
def main(path: Path, /, output: Path, *, verbose: bool = False):
    """Process a file.

    :param path: The input file path
    :param output: The output file
    :param verbose: Write more logs to the standard output.
    """
    ...


if __name__ == "__main__":
    argumentify(main)
```

The help looks like this:

```help
usage: test.py [-h] --output OUTPUT [--verbose] path

Process a file.

positional arguments:
  path              The input file path

options:
  -h, --help
                        show this help message and exit
  --output OUTPUT, -o OUTPUT
                        The output file
  --verbose, -v
                        Write more logs to the standard output.

```

_Note that `path` and `output` are required._

#### Example 2

```python
def main(output: Path, /, *inputs: Path):
    """Process multiple files into one.

    :param output: The output file
    :param inputs: The path to the input files
    """
    # Since `inputs` is a VAR_POSITIONAL, while being a positional argument, it can have
    # zero length which is in many cases not intended.
    # You might want to add a check for its length and raise an ArgumentError if it does
    # not match your needs

    # Check if at least one input has been passed and mark the argument as required
    # if len(inputs) < 1:
    #     raise RequiredArgumentError("inputs")

    # Raise an error unless at least two inputs are present
    if len(inputs) < 2:
        raise ArgumentError(message="You need to pass at least two files as input.")
    ...
```

The help looks like this:

```help
usage: test.py [-h] output [inputs ...]

Process multiple files into one.

positional arguments:
  output            The output file
  inputs            The path to the input files

options:
  -h, --help
                        show this help message and exit

```

#### Example 3

```python
def main(first_name: str, last_name: str, output: Path, verbose: bool = False):
    """Write a greeting message.

    :param first_name: The first name of the user to greet (optional)
    :param last_name: The last name of the user to greet (optional)
    :param output: The output file (stdout if none is provided)
    :param verbose: If provided, will write the debug logs to stdout
    """
    ...


if __name__ == "__main__":
    argumentify(main)
```

The help looks like this:

```help
usage: test.py [-h] [--first-name FIRST_NAME] [--last-name LAST_NAME] [--output OUTPUT]
               [--verbose]

Write a greeting message.

options:
  -h, --help
                        show this help message and exit
  --first-name FIRST_NAME, -f FIRST_NAME
                        The first name of the user to greet (optional)
  --last-name LAST_NAME, -l LAST_NAME
                        The last name of the user to greet (optional)
  --output OUTPUT, -o OUTPUT
                        The output file (stdout if none is provided)
  --verbose, -v
                        If provided, will write the debug logs to stdout

```

_Note that all the options are optional and default to None. `verbose` is False by
default since a default value is provided for it in function definition._

### v3.0.2

Change `argumentify` to use the whole function description as the argument-parser
description instead of the one-line short description.

- Example:

```python
def main(verbose: bool = False) -> None:
    """This is a very useful tool and I will describe it thoroughly. It is so good that
    we have a second line in the first part of the description.

    And now we can talk more about the tool...

    :param verbose: This flag will make the logs more verbose!
    """

argumentify(main)
```

The way old versions would look:

```help
usage: test.py [-h] [--verbose]

This is a very useful tool and I will describe it thoroughly. It is so good that

options:
  -h, --help
                        show this help message and exit
  --verbose, -v
                        This flag will make the logs more verbose!

```

Now at v3.0.2:

```help
usage: test.py [-h] [--verbose]

This is a very useful tool and I will describe it thoroughly. It is so good that we have
second line in the first part of the description. And now we can talk more about the tool...

options:
  -h, --help
                        show this help message and exit
  --verbose, -v
                        This flag will make the logs more verbose!

```

### v3.0.1

Fix the issue with `argumentify` which would result in falsy default values to be
replaced with None.

- Example:

```python
def main(offset: int = 0) -> None:
    ...

argumentify(main)
```

if no value was provided for `--offset`, the default would be `None` instead of `0`
which was unexpected and can lead to issues.

### v3.0.0

This release introduces a cleaned-up internal structure, stricter naming conventions,
and several quality-of-life improvements. While most users will not notice behavioral
changes, **v3 contains breaking changes for code that relies on internal imports or
specific exception names**.

#### Breaking Changes

- **Internal module renaming and normalization**
  - All internal modules were renamed to lowercase and, in some cases, split or
    reorganized.
  - Imports such as `log21.Colors`, `log21.Logger`, `log21.ProgressBar`, etc. are no
    longer valid.
  - Users importing from internal modules must update their imports to the new module
    names.
  - Public imports from `log21` remain supported.

- **Argumentify exception renames**
  - Several exceptions were renamed to follow a consistent `*Error` naming convention:
    - `TooFewArguments` → `TooFewArgumentsError`
    - `RequiredArgument` → `RequiredArgumentError`
    - `IncompatibleArguments` → `IncompatibleArgumentsError`
  - Code that explicitly raises or catches these exceptions must be updated.

#### V3 Changes

- **Crash reporter behavior improvement**
  - Prevented the default file crash reporter from creating `.crash_report` files when it
    is not actually used.
  - Implemented using an internal `FakeModule` helper.

- **Argparse compatibility update**
  - Bundled and used the Python 3.13 `argparse` implementation to ensure consistent
    behavior across supported Python versions.

- **Progress bar module rename**
  - Renamed the internal progress bar module to `progress_bar` for consistency with the
    new naming scheme.
  - This will not break the usages of `log21.progress_bar(...)` since the call
    functionality was added to the module using the `FakeModule` helper.

- **Examples added and updated**
  - Added new example code files.
  - Updated existing examples to match the v3 API and conventions.

#### Fixes

- Resolved various linting and static-analysis issues across the codebase.
- Addressed minor compatibility issues uncovered by running linters and pre-commit hooks.
- Resolved errors occurring in environments with newer versions of argparse.

#### Internal and Maintenance Changes

- Migrated the build system configuration to `uv`.
- Updated Python version classifiers and set the supported Python version to 3.9+.
- Added `vermin` to the pre-commit configuration.
- Updated `.gitignore`, license metadata, and tool configurations.
- Silenced and resolved a large number of linter warnings.
- General internal refactoring with no intended user-visible behavioral changes.

#### Notes

- There are **no intentional behavioral changes** in logging output, argument parsing
  logic, or UI components.
- Most projects will require **minimal or no changes** unless they depend on internal
  modules or renamed exceptions.
- See [MIGRATION-V2-V3.md](https://github.com/MPCodeWriter21/log21/blob/master/MIGRATION-V2-V3.md)
for detailed upgrade instructions.

### 2.10.2

- Update README.md and CHANGELOG.md.

### 2.10.1

- Updated the Argparse module to be usable with python 3.12.3.

### 2.10.0

- Added some exception classes to raise in the "argumentified" functions to show
  **parser error** to the user: `ArgumentError`, `IncompatibleArguments`,
  `RequiredArgument`, `TooFewArguments`

### 2.9.2

- Added `Sequence[T]` as a supported type to the ColorizingArgumentParser.
- Bug fixes.

### 2.9.1

- Update `README.md`.

### 2.9.0

- Added `<<` and `>>` (left shift and right shift operators) to `log21.Logger.Logger`.

### 2.8.1

- Fixed Carriage Return Handling.
- Fixed setting level using `log21.basic_config`
- Added more configuration for developer tools to the `pyproject.toml` file.
- Added pre-commit.

### 2.8.1b0

- Fixed setting level using `log21.basic_config`

### 2.8.1a0

- Fixed Carriage Return Handling.

### 2.8.0

- Update python version
- Renamed `crash_report.log` to `.crash_report.log`.
- Added "force" error handling method to `Logger.add_level`.
- Changed the adding level error handling method to "ignore".
- Ability to add new methods to the Logger object for each custom level.

### 2.8.0b1

- Renamed `crash_report.log` to `.crash_report.log`.

### 2.8.0b0

- Changed the adding level error handling method to "ignore".

### 2.8.0a0-2

- Ability to add new methods to the Logger object for each custom level.
- Update python version
- Added "force" error handling method to `Logger.add_level`.

### 2.7.1

- Improved compatibility

### 2.7.0

- Modified `automatic-release.yml` and `pypi.yml` workflows to check the
  version
- Added the support for more `type`s to pass to
  `ColorizingArgumentParser().add_argument(...)`: `typing.Union`, `typing.Optional`,
  `typing.Literal`, `enum.Enum`, `tuple` and `typing.Required`.
- Modified the way `Enum`s are handled in the Argument Parser.
- Handled some `typing._SpecialForm`s.
- A normal ArgumentGroup can now be required! (Unlike MutuallyExclusiveGroup it can
  have more than 1 option used at the same time)
- `argumentify` now supports async functions as the entry point.

### 2.6.2

Change in README.md.

### 2.6.1

- Added `encoding` to `log21.crash_reporter.FileReporter`.
- Added configs for `pylint`, `yapf` and `isort` to `pyproject.toml`.
- Added optional `dev` dependencies to `pyproject.toml`.
- Improved overall code quality.

### 2.6.0

Added the `Argumentify` module. Check the examples.

### 2.5.5

Fixed a bug in the `TreePrint` class.

### 2.5.4

Added constant colors directly to the Colors module. Now you can do this:

```python
from log21 import print
from log21.colors import GREEN, WHITE, RED

print(GREEN + 'This' + WHITE + ' is' + RED + ' Red')
```

### 2.5.3

Moved some dictionaries to `__init__` methods.

- `colors` in `Argparse.ColorizingHelpFormatter` class.
- `_level_name` in `Formatters._Formatter` class and `level_colors` in
  `Formatters.ColorizingFormatter` class.
- `sign_colors` in `PPrint.PrettyPrinter` class.
- `colors` in `TreePrint.TreePrint.Node` class.

### 2.5.2

Improved type-hintings.

### 2.5.1

Switched from `setup.py` build system to `pyproject.toml`

### 2.5.0

Added `level_colors` argument to `log21.get_logger` function with will be passed to the
formatter and allows user to set custom level colors while making a new logger.
Also changed most `Dict` type hints to be `Mapping` and `list` to `Sequence` to make the
functions more general and less strict.

### 2.4.7

Added `extra_values` argument to `crash_reporter.Formatter` which will let you pass extra
static or dynamic values to the report formatter.
They can be used in the format string. For dynamic values you can pass a function that
takes no arguments as the value.

### 2.4.6

Shortened the usage syntax for the CrashReporters:

```python
import log21

# Define a ConsoleReporter object
console_reporter = log21.crash_reporter.ConsoleReporter()


# This works with other `log21.crash_reporter.reporter` subclasses as well.

# Old syntax (still supported)
@console_reporter.reporter
def divide_old(a, b):
    return a / b


# New Syntax
@console_reporter.reporter
def divide_new(a, b):
    return a / b

```

`console_crash_reporter` and `file_crash_reporter` are removed!

### 2.4.5

Added `no_color` parameter to ProgressBar.

### 2.4.4

Some bug fixes.

### 2.4.3

Improvements.

### 2.4.2

Bug Fixes.

### 2.4.1

Bug fixes and improvements.

### 2.4.0

- Made it more compatible with multi-threading.
- Fixed some bugs.

### 2.3.10

Minor fixes and improvements.

### 2.3.9

Minor fixes and improvements.

### 2.3.8

Added `catch` and `ignore` methods to `log21.CrashReporter.Reporter`.

### 2.3.7

Added `exceptions_to_catch` and `exceptions_to_ignore` arguments to
`log21.CrashReporter.Reporter` class.

### 2.3.6

Added `Print` logging level.

### 2.3.5

Minor improvements.

### 2.3.4

Added a new method to `log21.Logger` class: `log21.Logger.clear_line`. This method
clears the current line in the console and moves the cursor to the beginning of the line.

### 2.3.3

Fixed a bug that would cause an error creating a progress bar with no value set for
width in systems without support for `os.get_terminal_size()`.

### 2.3.2

Added `additional_variables` argument to `log21.ProgressBar` class. You can use it in
order to add additional variables to the progress bar:

```python3
import log21, time

progress_bar = log21.ProgressBar(
    format_='Iteration: {i} {prefix}{bar}{suffix} {percentage}%',
    style='{',
    additional_variables={"i": 0}
)

for i in range(100):
    progress_bar(i + 1, 100, i=i)
    time.sleep(0.1)
# Iteration: 99 |████████████████████████████████████████████████████████████████| 100%
```

### 2.3.1

Added `formatter` argument to `StreamHandler` and `FileHandler`. You can use it to set
the formatter of the handler when you create it. Added `handlers` argument to `Logger`.
You can use it to add handlers to the logger when you create it.

### 2.3.0

Added progressbar custom formatting.

Now you can use your own formatting for the progressbar instead of the default one.

Let's see an example:

```python
# We import the ProgressBar class from log21
from log21 import ProgressBar
# psutil is a module that can be used to get the current memory usage or cpu usage of
# your system
# If you want to try this example, you need to install psutil: pip install psutil
import psutil
# We use the time module to make a delay between the progressbar updates
import time

cpu_bar = ProgressBar(format_='CPU Usage: {prefix}{bar}{suffix} {percentage}%',
                      style='{', new_line_when_complete=False)

while True:
    cpu_bar.update(psutil.cpu_percent(), 100)
    time.sleep(0.1)
```

### 2.2.0

Added CrashReporter!

You can use Reporter classes to monitor your program and send crash reports to the
developer. It can help you fix the bugs and improve your program before your users get
upset about it. See some examples in the [log21/crash\_reporter/reporters.py](https://github.com/MPCodeWriter21/log21/blob/master/log21/CrashReporter/Reporters.py)
file.

### 2.1.8

Bug fixes.

### 2.1.7

Added `getpass` method to `log21.Logger` class and added `log21.getpass` function.

### 2.1.4-6

Bug fixes.

### 2.1.3

Added log21.input function.

### 2.1.2

Fixed import error in tkinter-less environments.

### 2.1.1

Minor changes.

### 2.1.0

Added optional shell support to the LoggingWindow.

### 2.0.0

Added LoggingWindow!

### 1.5.10

Added `ProgressBar` class!

You can directly print a progress bar to the console using `print_progress` method of
`log21.Logger` class.

OR

Use `log21.ProgressBar` class witch is specifically designed for this purpose.

OR

Use `log21.progress_bar` function (I don't recommend it!).

### 1.5.9

Minor changes.

### 1.5.8

Added `log21.log`, `log21.debug`, `log21.info`, `log21.warning`, `log21.error` and some
other functions.

### 1.5.7

Added `log21.tree_print()` function.

### 1.5.6

Added `log21.pprint()` function. It is similar to `pprint.pprint()` function.

### 1.5.5

Added `level_names` argument to Formatter classes.
`level_names` can be used to change the name of logging level that appears while logging
messages.

### 1.5.3-4

Minor changes.

### 1.5.2

`log21.print` function added!

### 1.5.1

More description added.

### 1.5.0

`ColorizingArgumentParser` improvements.

### 1.4.12

Setting custom formatting style and custom date-time formatting added to
`log21.get_logger` function.

### 1.4.11

`Logger.write` edited. It's same as `Logger.warning` but its default `end` argument
value is an empty string.

### 1.4.10

`Logger.write` added. It's same as `Logger.warning`

### 1.4.9

Bug fixed:

```python
>>> log21.get_logger()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "C:\...\Python37-32\lib\site-packages\log21\__init__.py", line 44, in get_logger
    raise TypeError('A logger name must be a string')
TypeError: A logger name must be a string
```

### 1.4.8

`get_logger` improved.

### 1.4.7

`Logger.print` added.

You can use `Logger.print` to print a message using the current level of the logger
class.

_It gets printed with any level._

### 1.4.6

`ColorizingArgumentParser` added.

You can use `ColorizingArgumentParser` to have a colorful ArgumentParser.

### 1.4.5

`StreamHandler` can handle new-line characters at the beginning of the message.

### 1.4.4

`get_color` function now supports hexadecimal and decimal RGB values.
