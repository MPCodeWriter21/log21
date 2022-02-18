log21
=====

Help this project by [Donation](DONATE.md)

Changes log
-----------

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