log21
=====

A simple logging package that helps you log colorized messages in Windows console and other operating systems.

Features
--------

+ Colors : Main reason for this package was to have a simple logging package that can be used in Windows console and
  supports ANSI colors.
+ Argument parsing : log21's argument parser can be used like python's argparse but it also colorizes the output.
+ Logging : A similar logger to logging.Logger but with colorized output and other options such as levelname
  modifications. It can also decolorize the output if you want to log to a file.
+ Pretty printing : Have you ever wanted to colorize the output of the pprint module? log21's pretty printer can do
  that.
+ Tree printing : You can pass a dict or list to log21.tree_print function and it will print it in a tree like
  structure. Its also colorized XD.
+ ProgressBar : log21's progress bar can be used to show progress of a process in a beautiful way.
+ Any idea? Feel free to [open an issue](https://github.com/MPCodeWriter21/log21/issues) or submit a pull request.

Installation
------------

Well, this is a python package so the first thing you need is python.

If you don't have python installed, please visit [Python.org](https://python.org) and install the latest version of
python.

Then you can install log21 using pip module:

```shell
python -m pip install log21 -U
```

Or you can clone [the repository](https://github.com/MPCodeWriter21/log21) and run:

```shell
python setup.py install
```

Changes
-------

### 1.5.10

Added `ProgressBar` class!

You can directly print a progress bar to the console using `print_progress` method of `log21.Logger` class.

OR

Use `log21.ProgressBar` class witch is specifically designed for this purpose.

OR

Use `log21.progress_bar` function (I don't recommend it!).

[Full Changes Log](https://github.com/MPCodeWriter21/log21/blob/master/CHANGES-LOG.md)


Usage Examples:
---------------

```python3
import log21

log21.print(log21.get_color('#FF0000') + 'This' + log21.get_color((0, 255, 0)) + ' is' + log21.get_color('Blue') +
            ' Blue' + log21.get_colors('BackgroundWhite', 'Black') + ' 8)')

logger = log21.get_logger('My Logger', level_names={21: 'SpecialInfo', log21.WARNING: ' ! ', log21.ERROR: '!!!'})
logger.info('You are reading the README.md file...')

logger.log(21, 'Here', '%s', 'GO!', args=('we',))

logger.setLevel(log21.WARNING)
logger.warning("We can't log messages with a level less than 30 anymore!")

logger.debug("You won't see this!")
logger.info("Am I visible?")

logger.error(log21.get_colors('LightRed') + "I'm still here ;1")
```

![Basic Logging](https://github.com/MPCodeWriter21/log21/raw/master/screen-shots/example-1.png)

----------------

```python3
import log21
from log21 import ColorizingArgumentParser, get_logger, get_colors as gc

parser = ColorizingArgumentParser(description="This is a simple example of a ColorizingArgumentParser.",
                                  colors={'help': 'LightCyan'})
parser.add_argument('test1', action='store', help='Test 1')
parser.add_argument('test2', action='store', help='Test 2')
parser.add_argument('--optional-arg', '-o', action='store', type=int, help='An optional integer')
parser.add_argument('--verbose', '-v', action='store_true', help='Increase verbosity.')

args = parser.parse_args()

logger = get_logger('My Logger', level_names={log21.DEBUG: ' ? ', log21.INFO: ' + ', log21.WARNING: ' ! ',
                                              log21.ERROR: '!!!'})

if args.verbose:
    logger.setLevel(log21.DEBUG)
else:
    logger.setLevel(log21.INFO)

logger.debug(gc('LightBlue') + 'Verbose mode on!')

logger.debug('Arguments:\n'
             '\tTest 1: %s\n'
             '\tTest 2: %s\n'
             '\tOptional: %s', args=(args.test1, args.test2, args.optional_arg))

logger.info(gc('LightGreen') + args.test1)

logger.info(gc('LightWhite') + 'Done!')

```

![No argument](https://github.com/MPCodeWriter21/log21/raw/master/screen-shots/example-2.1.png)

![Help](https://github.com/MPCodeWriter21/log21/raw/master/screen-shots/example-2.2.png)

![Valid example 1](https://github.com/MPCodeWriter21/log21/raw/master/screen-shots/example-2.3.png)

![Valid example 2](https://github.com/MPCodeWriter21/log21/raw/master/screen-shots/example-2.4.png)

![Valid example 3](https://github.com/MPCodeWriter21/log21/raw/master/screen-shots/example-2.5.png)

------------------

```python3
import json
import log21

data = json.load(open('json.json', 'r'))

# Prints data using python's built-in print function
print(data)

# Uses `log21.pprint` to print the data
log21.pprint(data)

# Uses `log21.tree_print` to print the data
log21.tree_print(data)
```

![Python print](https://github.com/MPCodeWriter21/log21/raw/master/screen-shots/example-3.1.png)
![log21 pretty print](https://github.com/MPCodeWriter21/log21/raw/master/screen-shots/example-3.2.png)
![log21 tree print 1](https://github.com/MPCodeWriter21/log21/raw/master/screen-shots/example-3.3.1.png)
![log21 tree print 1](https://github.com/MPCodeWriter21/log21/raw/master/screen-shots/example-3.3.2.png)

------------------

About
-----
Author: CodeWriter21 (Mehrad Pooryoussof)

GitHub: [MPCodeWriter21](https://github.com/MPCodeWriter21)

Telegram Channel: [@CodeWriter21](https://t.me/CodeWriter21)

Aparat Channel: [CodeWriter21](https://www.aparat.com/CodeWriter21)

### License

[apache-2.0](http://www.apache.org/licenses/LICENSE-2.0)

### Donate

In order to support this project you can donate some crypto of your choice 8D

[Donate Addresses](https://github.com/MPCodeWriter21/log21/blob/master/DONATE.md)

