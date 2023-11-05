log21
=====

Help this project by [Donation](DONATE.md)

Changes
-----------

### 2.8.0a0

+ Ability to add new methods to the Logger object for each custom level.

### 2.7.1

+ Improved compatibility

### 2.7.0

+ Modified `automatic-release.yml` and `pypi.yml` workflows to check the
  version
+ Added the support for more `type`s to pass to
  `ColorizingArgumentParser().add_argument(...)`: `typing.Union`, `typing.Optional`,
  `typing.Literal`, `enum.Enum`, `tuple` and `typing.Required`.
+ Modified the way `Enum`s are handled in the Argument Parser.
+ Handled some `typing._SpecialForm`s.
+ A normal ArgumentGroup can now be required! (Unlike MutuallyExclusiveGroup it can 
  have more than 1 option used at the same time)
+ `argumentify` now supports async functions as the entry point.

### 2.6.2

Change in README.md.

### 2.6.1

+ Added `encoding` to `log21.CrashReporter.FileReporter`.
+ Added configs for `pylint`, `yapf` and `isort` to `pyproject.toml`.
+ Added optional `dev` dependencies to `pyproject.toml`.
+ Improved overall code quality.

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
`colors` in `Argparse.ColorizingHelpFormatter` class.
`_level_name` in `Formatters._Formatter` class and `level_colors` in `Formatters.ColorizingFormatter` class.
`sign_colors` in `PPrint.PrettyPrinter` class.
`colors` in `TreePrint.TreePrint.Node` class.

### 2.5.2

Improved type-hintings.

### 2.5.1

Switched from `setup.py` build system to `pyproject.toml`

### 2.5.0

Added `level_colors` argument to `log21.get_logger` function with will be passed to the formatter and allows
user to set custom level colors while making a new logger.
Also changed most `Dict` type hints to be `Mapping` and `list` to `Sequence` to make the functions more general
and less strict.

### 2.4.7

Added `extra_values` argument to `CrashReporter.Formatter` which will let you pass extra static or dynamic values to the
report formatter.
They can be used in the format string. For dynamic values you can pass a function that takes no
arguments as the value.

### 2.4.6

Shortened the usage syntax for the CrashReporters:

```python
import log21

# Define a ConsoleReporter object
console_reporter = log21.CrashReporter.ConsoleReporter()


# This works with other `log21.CrashReporter.Reporter` subclasses as well.

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

+ Made it more compatible with multi-threading.
+ Fixed some bugs.

### 2.3.10

Minor fixes and improvements.

### 2.3.9

Minor fixes and improvements.

### 2.3.8

Added `catch` and `ignore` methods to `log21.CrashReporter.Reporter`.

### 2.3.7

Added `exceptions_to_catch` and `exceptions_to_ignore` arguments to `log21.CrashReporter.Reporter` class.

### 2.3.6

Added `Print` logging level.

### 2.3.5

Minor improvements.

### 2.3.4

Added a new method to `log21.Logger` class: `log21.Logger.clear_line`. This method clears the current line in the
console and moves the cursor to the beginning of the line.

### 2.3.3

Fixed a bug that would cause an error creating a progress bar with no value set for width in systems without support for
os.get_terminal_size().

### 2.3.2

Added `additional_variables` argument to `log21.ProgressBar` class. You can use it in order to add additional variables
to the progress bar:

```python3
import log21, time

progress_bar = log21.ProgressBar(format_='Iteration: {i} {prefix}{bar}{suffix} {percentage}%', style='{',
                                 additional_variables={"i": 0})

for i in range(100):
    progress_bar(i + 1, 100, i=i)
    time.sleep(0.1)
# Iteration: 99 |██████████████████████████████████████████████████████████████████████████████| 100%
```

### 2.3.1

Added `formatter` argument to `StreamHandler` and `FileHandler`. You can use it to set the formatter of the handler when
you create it. Added `handlers` argument to `Logger`. You can use it to add handlers to the logger when you create it.

### 2.3.0

Added progressbar custom formatting.

Now you can use your own formatting for the progressbar instead of the default one.

Let's see an example:

```python
# We import the ProgressBar class from log21
from log21 import ProgressBar
# psutil is a module that can be used to get the current memory usage or cpu usage of your system
# If you want to try this example, you need to install psutil: pip install psutil
import psutil
# We use the time module to make a delay between the progressbar updates
import time

cpu_bar = ProgressBar(format_='CPU Usage: {prefix}{bar}{suffix} {percentage}%', style='{', new_line_when_complete=False)

while True:
    cpu_bar.update(psutil.cpu_percent(), 100)
    time.sleep(0.1)
```

### 2.2.0

Added CrashReporter!

You can use Reporter classes to monitor your program and send crash reports to the developer. It can help you fix the
bugs and improve your program before your users get upset about it. See some examples in
the [log21/CrashReporter/Reporters.py](https://github.com/MPCodeWriter21/log21/blob/master/log21/CrashReporter/Reporters.py)
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

You can directly print a progress bar to the console using `print_progress` method of `log21.Logger` class.

OR

Use `log21.ProgressBar` class witch is specifically designed for this purpose.

OR

Use `log21.progress_bar` function (I don't recommend it!).

### 1.5.9

Minor changes.

### 1.5.8

Added `log21.log`, `log21.debug`, `log21.info`, `log21.warning`, `log21.error` and some other functions.

### 1.5.7

Added `log21.tree_print()` function.

### 1.5.6

Added `log21.pprint()` function. It is similar to `pprint.pprint()` function.

### 1.5.5

Added `level_names` argument to Formatter classes.
`level_names` can be used to change the name of logging level that appears while logging messages.

### 1.5.3-4

Minor changes.

### 1.5.2

`log21.print` function added!

### 1.5.1

More description added.

### 1.5.0

`ColorizingArgumentParser` improvements.

### 1.4.12

Setting custom formatting style and custom date-time formatting added to `log21.get_logger` function.

### 1.4.11

`Logger.write` edited. It's same as `Logger.warning` but its default `end` argument value is an empty string.

### 1.4.10

`Logger.write` added. It's same as `Logger.warning`

### 1.4.9

Bug fixed:

```
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

You can use `Logger.print` to print a message using the current level of the logger class.

*It gets printed with any level.*

### 1.4.6

`ColorizingArgumentParser` added.

You can use `ColorizingArgumentParser` to have a colorful ArgumentParser.

### 1.4.5

`StreamHandler` can handle new-line characters at the beginning of the message.

### 1.4.4

`get_color` function now supports hexadecimal and decimal RGB values.
