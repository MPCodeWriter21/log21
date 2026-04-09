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

### v3.1.0

Change the way `argumentify` handles function parameters to argument-parser arguments
conversion.

+ `POSITIONAL_ONLY` and `VAR_POSITIONAL` parameters will be positional arguments.
+ `POSITIONAL_OR_KEYWORD` and `KEYWORD_ONLY` parameters have flags assigned to them.
+ `POSITIONAL_OR_KEYWORD` parameters will be required if at least one `KEYWORD_ONLY`
  parameter is there, otherwise they are optional.
+ `VAR_KEYWORD` parameters are still not supported.

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
